"""Hentingsprøven på hele rammelisten (ADDENDUM-04 §1.3). Ingen nettkall: mock-transport."""

import hashlib
import json
from pathlib import Path

import httpx
import pytest

from gjenopptak.harvest import fetchtest as ft

PDF = b"%PDF-1.7\n" + b"x" * 5000


def _rad(i: int, *, doi: str | None = "auto", pdf: str | None = "auto") -> dict:
    return {
        "work_id": f"W{1000 + i}",
        "doi": f"10.1234/x{i}" if doi == "auto" else doi,
        "publication_year": 2015 + i % 6,
        "best_oa_location": {"pdf_url": f"https://pub{i % 3}.example/{i}.pdf" if pdf == "auto" else pdf},
    }


class Opptak:
    """Mock-transport som fører hvert kall: EPMC-søk gir tomt, PDF-er gis ut."""

    def __init__(self, *, pdf_status: int = 200, epmc_results=None, hitcount=None):
        self.kall: list[httpx.Request] = []
        self.pdf_status = pdf_status
        self.epmc_results = epmc_results or []
        self.hitcount = hitcount

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.kall.append(request)
        if "ebi.ac.uk" in request.url.host:
            res = self.epmc_results
            return httpx.Response(200, json={"hitCount": self.hitcount if self.hitcount is not None else len(res),
                                             "resultList": {"result": res}})
        if self.pdf_status != 200:
            return httpx.Response(self.pdf_status)
        return httpx.Response(200, content=PDF, headers={"content-type": "application/pdf"})

    def klient(self) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(self), follow_redirects=True)


@pytest.fixture(autouse=True)
def ingen_pdftotext(monkeypatch):
    monkeypatch.setattr(ft, "pdf_text_chars", lambda b, d, n: 5000)


@pytest.fixture(autouse=True)
def _adr0009_port(tmp_path, monkeypatch):
    """ADR-0009-porten slippes forbi her; Vault-nektelsen testes i test_vault_standard.py.

    Testene under prøver fetchtestens egen Vault-sjekk i probe_dir, som er en annen port.
    """
    from gjenopptak.harvest import fetchtest as _ft
    monkeypatch.setattr(_ft, "krev", lambda d=None, **kw: Path(d) if d else tmp_path)


def test_verdiktet_baerer_filstorrelse_og_sha256(tmp_path):
    op = Opptak()
    v = ft.test_work(op.klient(), _rad(1), tmp_path / "raw", tmp_path / "tmp", pmcid=None)
    assert v.in_frame and v.gate == "P3-PDF"
    assert v.bytes == len(PDF)
    assert v.sha256 == hashlib.sha256(PDF).hexdigest()
    assert v.file.startswith("ft-pdf-W1001-") and (tmp_path / "raw" / v.file).read_bytes() == PDF


def test_hentbar_rammefil_har_storrelse_og_sha256(tmp_path):
    op = Opptak()
    vs = [ft.test_work(op.klient(), _rad(i), tmp_path / "raw", tmp_path / "tmp", pmcid=None) for i in (3, 1)]
    n, _ = ft.write_frame_file(vs, tmp_path / "frame-HENTBAR.jsonl")
    rader = [json.loads(l) for l in (tmp_path / "frame-HENTBAR.jsonl").read_text().splitlines()]
    assert n == 2 and [r["work_id"] for r in rader] == ["W1001", "W1003"]
    assert all(len(r["sha256"]) == 64 and r["bytes"] == len(PDF) and r["gate"] == "P3-PDF" for r in rader)


def test_armering_opptaket_ser_vanlige_kall(tmp_path):
    """Kontrollen: uten dette kunne «ingen kall» i testen under bety at opptaket er dødt."""
    op = Opptak()
    ft.test_work(op.klient(), _rad(2), tmp_path / "raw", tmp_path / "tmp", pmcid=None)
    assert [r.url.host for r in op.kall] == ["pub2.example"]


def test_openalex_kalles_aldri(tmp_path):
    op = Opptak()
    rad = _rad(4, pdf="https://api.openalex.org/works/W1.pdf")
    v = ft.test_work(op.klient(), rad, tmp_path / "raw", tmp_path / "tmp", pmcid=None)
    assert op.kall == [] and not v.in_frame
    assert v.reason == "openalex-lenke-ikke-hentet"
    with pytest.raises(ft.OpenAlexForbidden):
        ft._get(op.klient(), "https://openalex.org/W1", {})


def test_epmc_batch_krever_det_samme_som_enkeltoppslaget(tmp_path):
    res = [
        {"doi": "10.1/ja", "pmcid": "PMC1", "inEPMC": "Y", "isOpenAccess": "Y"},
        {"doi": "10.1/lukket", "pmcid": "PMC2", "inEPMC": "Y", "isOpenAccess": "N"},
        {"doi": "10.1/annen", "pmcid": "PMC3", "inEPMC": "Y", "isOpenAccess": "Y"},
    ]
    op = Opptak(epmc_results=res)
    ut = ft.epmc_pmcids(op.klient(), ["10.1/ja", "10.1/lukket", "10.1/mangler"], tmp_path, stem="ft-epmc-t")
    assert ut == {"10.1/ja": "PMC1", "10.1/lukket": None, "10.1/mangler": None}
    assert len(op.kall) == 1, "fem DOI-er er ett kall"


def test_epmc_batch_faller_tilbake_naar_svaret_er_ufullstendig(tmp_path):
    op = Opptak(epmc_results=[], hitcount=500)
    ut = ft.epmc_pmcids(op.klient(), ["10.1/a", "10.1/b"], tmp_path, stem="ft-epmc-t")
    assert ut == {"10.1/a": None, "10.1/b": None}
    assert len(op.kall) == 3, "ett batch-kall + ett per DOI når svaret har flere treff enn siden"
    with pytest.raises(ValueError):
        ft.epmc_pmcids(op.klient(), [f"10.1/{i}" for i in range(6)], tmp_path, stem="x")


def test_vertsgrensen_holder_avstand():
    klokke = {"t": 0.0}
    sov: list[float] = []

    def sleep(s):
        sov.append(s)
        klokke["t"] += s

    g = ft.HostGate(interval=1.0, max_concurrent=2, per_host={"arxiv.org": (3.0, 1)},
                    clock=lambda: klokke["t"], sleep=sleep)
    with g.slot("pub.example"):
        pass
    with g.slot("pub.example"):
        pass
    with g.slot("annen.example"):
        pass
    assert sov == [1.0], "samme vert venter intervallet, en annen vert gjør det ikke"
    assert g.config("export.arxiv.org") == (3.0, 1)


def test_gjenopptar_og_diskvakten_stopper(tmp_path):
    rows = [_rad(i) for i in range(5)]
    ut = tmp_path / "verdikter.jsonl"
    ferdig = ft.FetchVerdict("W1000", "10.1234/x0", in_frame=False, gate="P3-PDF", status=403)
    ut.write_text(json.dumps(ferdig.as_row()) + "\n")
    op = Opptak()
    ledig = iter([10**12, 10**12, 0, 0, 0, 0])
    st = ft.run_frame(rows, tmp_path / "raw", tmp_path / "tmp", ut, workers=1,
                      gate=ft.HostGate(interval=0.0), disk_free=lambda: next(ledig),
                      scratch_free=lambda: 10**12, client_factory=op.klient)
    assert st.n_done_before == 1 and st.n_tested_now == 2 and st.stopped == "disk-vault"
    assert (tmp_path / "verdikter-epmc.json").exists()
    st2 = ft.run_frame(rows, tmp_path / "raw", tmp_path / "tmp", ut, workers=1,
                       gate=ft.HostGate(interval=0.0), disk_free=lambda: 10**12,
                       scratch_free=lambda: 10**12, client_factory=op.klient)
    assert st2.n_done_before == 3 and st2.n_tested_now == 2 and st2.stopped is None
    v = ft.read_verdicts(ut)
    assert sorted(v) == [r["work_id"] for r in rows]
    assert v["W1000"].status == 403, "et verdikt som alt står, testes ikke på nytt"
    assert not any("openalex" in r.url.host for r in op.kall)


# ------------------------------------------------------------------ skrivestrategien: Vault

GIB = 2**30


def _ramme(data, rows):
    (data / "frames").mkdir(parents=True)
    with (data / "frames" / "frame-energimodellering-RAW.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")


class Kalt(Exception):
    pass


def test_proven_nekter_aa_starte_uten_vault(tmp_path, monkeypatch):
    data = tmp_path / "data"
    _ramme(data, [_rad(1)])
    monkeypatch.setattr(ft, "run_frame", lambda *a, **k: (_ for _ in ()).throw(AssertionError("startet")))
    kode = ft.main(["--field", "energimodellering", "--data-dir", str(data),
                    "--vault-root", str(tmp_path / "Vault-finnes-ikke")])
    assert kode == 2
    assert sorted(p.relative_to(data).as_posix() for p in data.rglob("*")) == \
        ["frames", "frames/frame-energimodellering-RAW.jsonl"], "ingenting skal være skrevet"


def test_armering_proven_starter_naar_vault_finnes(tmp_path, monkeypatch):
    """Kontrollen: nektelsen over skyldes Vault, ikke noe annet i main()."""
    from gjenopptak import vault
    data = tmp_path / "data"
    _ramme(data, [_rad(1)])
    dest = tmp_path / "Vault" / "gjenopptak-kilder"
    monkeypatch.setattr(vault, "require_vault", lambda root=None: dest)

    def kalt(*a, **k):
        raise Kalt()
    monkeypatch.setattr(ft, "run_frame", kalt)
    with pytest.raises(Kalt):
        ft.main(["--field", "energimodellering", "--data-dir", str(data)])


def test_proven_skriver_fulltekst_til_vault_ikke_til_systemdisken(tmp_path, monkeypatch):
    from gjenopptak import vault
    data = tmp_path / "data"
    rows = [_rad(1), _rad(2, doi=None)]
    _ramme(data, rows)
    dest = tmp_path / "Vault" / "gjenopptak-kilder"
    dest.mkdir(parents=True)
    monkeypatch.setattr(vault, "require_vault", lambda root=None: dest)
    op = Opptak()
    ekte = httpx.Client
    monkeypatch.setattr(ft.httpx, "Client", lambda *a, **k: ekte(transport=httpx.MockTransport(op),
                                                              follow_redirects=True))
    monkeypatch.setattr(ft, "default_gate", lambda: ft.HostGate(interval=0.0))
    monkeypatch.setattr(ft.shutil, "disk_usage", lambda p: type("U", (), {"free": 100 * GIB})())
    assert ft.main(["--field", "energimodellering", "--data-dir", str(data)]) == 0

    maal = dest / "fulltext-rammeprove-energimodellering"
    pdf = sorted(maal.glob("ft-pdf-*"))
    assert [p.name.split("-")[2] for p in pdf] == ["W1001", "W1002"]
    assert (maal / "MANIFEST.md").exists() and (maal / "verdikter-energimodellering.jsonl").exists()
    lokalt = [p for p in data.rglob("*") if p.is_file()]
    assert all(p.parent.name == "frames" for p in lokalt), f"bare rammefiler lokalt, fikk {lokalt}"
    assert not any(p.name.startswith("ft-") for p in data.rglob("*"))
    assert (dest / "frames" / "frame-energimodellering-HENTBAR.jsonl").exists()


def test_scratchvakten_stopper_paa_systemdisken(tmp_path):
    rows = [_rad(i) for i in range(3)]
    op = Opptak()
    st = ft.run_frame(rows, tmp_path / "vault", tmp_path / "tmp", tmp_path / "v.jsonl", workers=1,
                      gate=ft.HostGate(interval=0.0), disk_free=lambda: 100 * GIB,
                      scratch_free=lambda: 1 * GIB, client_factory=op.klient)
    assert st.stopped == "disk-scratch" and st.n_tested_now == 0


def test_ingen_terskel_er_senket():
    import inspect
    assert ft.DISK_FLOOR_BYTES == 6 * GIB
    assert ft.SCRATCH_FLOOR_BYTES >= 6 * GIB
    assert "disk-floor" not in inspect.getsource(ft.main), "tersklene skal ikke kunne senkes fra CLI"
