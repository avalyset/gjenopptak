"""Frysing av rammelisten (ADDENDUM-04 §5). Ingen nettkall: mock-transport."""

import hashlib
import json

import httpx
import pytest
from control import Corpus

from gjenopptak.harvest import freeze as fz


def _work(i: int, *, pdf: str | None = None) -> dict:
    return {
        "id": f"https://openalex.org/W{1000 + i}",
        "doi": f"https://doi.org/10.1234/x{i}",
        "publication_year": 2015 + (i % 6),
        "primary_topic": {"id": "https://openalex.org/T10424",
                          "display_name": "Electric Power System Optimization"},
        "open_access": {"is_oa": True, "oa_status": "gold"},
        "best_oa_location": {"pdf_url": pdf, "landing_page_url": "https://ex.invalid",
                             "license": "cc-by", "version": "publishedVersion",
                             "source": {"display_name": "J"}},
    }


def transport(total: int, pages: list[list[dict]], *, remaining: list[int], count_status: int = 200):
    """Mock: første kall er tellingen, deretter én side per kall."""
    state = {"i": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        rem = remaining[min(state["i"], len(remaining) - 1)]
        hdr = {"x-ratelimit-remaining": str(rem), "x-ratelimit-limit": "1000"}
        if "cursor" not in request.url.params:
            state["i"] += 1
            if count_status != 200:
                return httpx.Response(count_status, headers={**hdr, "retry-after": "39178"})
            return httpx.Response(200, json={"meta": {"count": total}, "results": []}, headers=hdr)
        idx = state["i"] - 1
        state["i"] += 1
        batch = pages[idx] if idx < len(pages) else []
        nxt = "cursor-%d" % (idx + 1) if idx + 1 < len(pages) else None
        return httpx.Response(200, json={"meta": {"count": total, "next_cursor": nxt},
                                         "results": batch}, headers=hdr)

    return httpx.MockTransport(handler)


def klient(tr) -> httpx.Client:
    return httpx.Client(transport=tr, base_url="https://api.openalex.org")


def test_raden_bevarer_feltene_addendum04_krever(tmp_path):
    rad = fz.to_row(_work(1, pdf="https://ex.invalid/a.pdf"))
    assert rad["work_id"] == "W1001"
    assert rad["doi"] == "10.1234/x1"            # normalisert, uten URL-prefiks
    assert rad["primary_topic_id"] == "T10424"
    assert rad["oa_status"] == "gold"
    assert rad["best_oa_location"]["pdf_url"] == "https://ex.invalid/a.pdf"


def test_listen_sorteres_deterministisk_paa_work_id(tmp_path):
    sider = [[_work(i) for i in (5, 2, 9)], [_work(i) for i in (1, 7)]]
    tr = transport(5, sider, remaining=[900] * 6)
    res = fz.freeze_field("energimodellering", tmp_path / "raw", http=klient(tr))
    assert [r["work_id"] for r in res.rows] == ["W1001", "W1002", "W1005", "W1007", "W1009"]
    assert res.complete and res.n_rows == 5


def test_samme_liste_gir_samme_sha256(tmp_path):
    sider = [[_work(i) for i in (3, 1, 2)]]
    to = []
    for k in ("a", "b"):
        tr = transport(3, sider, remaining=[900] * 4)
        res = fz.freeze_field("energimodellering", tmp_path / f"raw-{k}", http=klient(tr))
        path, digest = fz.write_frame(res, tmp_path / f"frames-{k}")
        to.append(digest)
        assert digest == hashlib.sha256(path.read_bytes()).hexdigest()
    assert to[0] == to[1], "frysingen må være byte-identisk ved gjenkjøring"


def test_frysingen_starter_ikke_naar_kvoten_er_for_liten(tmp_path):
    """Vakten som gjør at et døgn ikke kan tapes midt i en frysing."""
    tr = transport(30000, [[_work(1)]], remaining=[100] * 3)   # 150 sider, 100 kall igjen
    with pytest.raises(fz.QuotaTooLow) as e:
        fz.freeze_field("energimodellering", tmp_path / "raw", http=klient(tr))
    assert "Ingenting er hentet" in str(e.value)
    assert not (tmp_path / "frames").exists()


def test_429_paa_tellingen_stopper_foer_start(tmp_path):
    tr = transport(30000, [], remaining=[0], count_status=429)
    with pytest.raises(fz.QuotaTooLow) as e:
        fz.freeze_field("energimodellering", tmp_path / "raw", http=klient(tr))
    tekst = Corpus("feil", [str(e.value)])
    tekst.must_hit("429")
    tekst.must_hit("Ingenting er hentet")


def test_loepende_vakt_stopper_og_merker_ufullstendig(tmp_path):
    """Faller remaining under gulvet, skrives det som er hentet — merket."""
    sider = [[_work(i)] for i in range(1, 6)]
    tr = transport(5, sider, remaining=[900, 900, 900, 40, 40, 40, 40])
    res = fz.freeze_field("energimodellering", tmp_path / "raw", http=klient(tr), margin=0)
    assert not res.complete
    assert res.stopped_at_cursor is not None
    path, digest = fz.write_frame(res, tmp_path / "frames")
    assert "UFULLSTENDIG" in path.name
    fz.note_in_manifest(res, path, digest, tmp_path / "raw")
    manifest = Corpus("manifest", (tmp_path / "raw" / "MANIFEST.md").read_text(encoding="utf-8").splitlines())
    manifest.must_hit("UFULLSTENDIG")
    manifest.must_hit(digest)


def test_komplett_liste_merkes_ikke_ufullstendig(tmp_path):
    sider = [[_work(i) for i in range(1, 4)]]
    tr = transport(3, sider, remaining=[900] * 4)
    res = fz.freeze_field("energimodellering", tmp_path / "raw", http=klient(tr))
    path, digest = fz.write_frame(res, tmp_path / "frames")
    assert path.name == "frame-energimodellering-RAW.jsonl"
    linjer = path.read_text(encoding="utf-8").splitlines()
    assert len(linjer) == 3
    assert all(json.loads(l)["work_id"] for l in linjer)
    fz.note_in_manifest(res, path, digest, tmp_path / "raw")
    manifest = Corpus("manifest", (tmp_path / "raw" / "MANIFEST.md").read_text(encoding="utf-8").splitlines())
    manifest.must_hit("KOMPLETT")
    manifest.expect_none("UFULLSTENDIG")


def test_raadata_lagres_per_side(tmp_path):
    sider = [[_work(1)], [_work(2)]]
    tr = transport(2, sider, remaining=[900] * 5)
    fz.freeze_field("energimodellering", tmp_path / "raw", http=klient(tr))
    filer = sorted(p.name for p in (tmp_path / "raw").glob("freeze-*.json"))
    assert any("freeze-count-" in f for f in filer)
    assert sum(1 for f in filer if "-p0" in f) == 2


def test_filteret_er_rammen_fra_addendum01():
    from gjenopptak.harvest.coverage import frame_filter

    assert frame_filter("energimodellering") == (
        "topics.id:T10424|T11185|T11941,publication_year:2015-2020,open_access.is_oa:true")


def test_addendum04_skriver_rammen_som_to_ledd():
    from pathlib import Path

    add = Path(__file__).resolve().parent.parent / "ADDENDUM-04.md"
    tekst = Corpus("ADDENDUM-04", add.read_text(encoding="utf-8").splitlines())
    tekst.must_hit("hentingsprøve")
    tekst.must_hit("LEDD 1")
    tekst.must_hit("LEDD 2")
    tekst.must_hit("10.4073/cmdp.2018.2")     # H1-kontrollen som faller
    tekst.must_hit("1 000 kall per døgn")
    tekst.must_hit("En rå rammeliste er ikke et utvalg")


def _sider(n_sider: int) -> list[list[dict]]:
    return [[_work(i * 200 + j) for j in range(200)] for i in range(n_sider)]


def test_startmarginen_kan_ikke_vaere_lavere_enn_gulvet(tmp_path):
    """Sidetall + gulv er regelen. Med margin 25 og gulv 50 startet en frysing som
    garantert ville stoppet før siste side."""
    assert fz.START_MARGIN >= fz.REMAINING_FLOOR
    tr = transport(1000, _sider(5), remaining=[30, 29, 28, 27, 26, 25])   # 5 sider, 30 igjen
    with pytest.raises(fz.QuotaTooLow):
        fz.freeze_field("energimodellering", tmp_path / "raw", http=klient(tr), margin=25)


def test_akkurat_sidetall_pluss_gulv_blir_komplett(tmp_path):
    tr = transport(600, _sider(3), remaining=[53, 52, 51, 50])
    res = fz.freeze_field("energimodellering", tmp_path / "raw", http=klient(tr))
    assert res.complete and res.n_rows == 600 and res.remaining_at_end == 50
