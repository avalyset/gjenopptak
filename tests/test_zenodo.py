"""Opplastings- og publiseringsskriptet, kjørt mot en falsk Zenodo. Ingen test rører nettet."""
import hashlib
import json
import urllib.request

import pytest

from gjenopptak import zenodo as Z

NØKKEL = "t" * 60
API = Z.API


@pytest.fixture(autouse=True)
def _ingen_nett(monkeypatch):
    def nei(*a, **k):
        raise AssertionError("testen forsøkte et nettkall")
    monkeypatch.setattr(urllib.request, "urlopen", nei)


class FalskZenodo:
    """Det av deponerings-API-et skriptet bruker: newversion, utkast, fillisten, bucket, metadata, publish."""

    def __init__(self, arvet: dict[str, bytes], forrige="111", utkast=222):
        self.forrige, self.utkast, self.bucket = forrige, utkast, f"{API}/files/bøtte-1"
        self.filer = {n: {"id": f"id-{i}", "b": arvet[n]} for i, n in enumerate(sorted(arvet))}
        self.metadata = {"title": "Gjenopptak", "version": "0.5.0", "publication_date": "2026-10-03",
                         "prereserve_doi": {"doi": f"10.5281/zenodo.{utkast}", "recid": utkast}}
        self.opprettet = self.publisert = False
        self.logg: list[tuple[str, str]] = []
        self.hoder: list[dict] = []
        self.feil_en_gang: dict[tuple[str, str], int] = {}

    def _utkast(self):
        return {"id": self.utkast, "submitted": self.publisert, "metadata": self.metadata,
                "links": {"bucket": self.bucket}}

    def send(self, metode, url, hoder, kropp, lengde):
        sti = url.removeprefix(API)
        self.logg.append((metode, sti))
        self.hoder.append(hoder)
        if (status := self.feil_en_gang.pop((metode, sti), None)):
            return status, b'{"message": "midlertidig"}', {"Retry-After": "0"}
        if hoder.get("Authorization") != f"Bearer {NØKKEL}":
            return 401, b"{}", {}
        d = f"/deposit/depositions/{self.utkast}"
        if (metode, sti) == ("POST", f"/deposit/depositions/{self.forrige}/actions/newversion"):
            self.opprettet = True
            return 201, json.dumps({"id": int(self.forrige), "links": {"latest_draft": API + d}}).encode(), {}
        if not self.opprettet:
            return 404, b"{}", {}
        if (metode, sti) == ("GET", d):
            return 200, json.dumps(self._utkast()).encode(), {}
        if (metode, sti) == ("PUT", d):
            if self.publisert:
                return 403, b"{}", {}
            self.metadata = json.loads(kropp)["metadata"] | {"prereserve_doi": self.metadata["prereserve_doi"]}
            return 200, json.dumps(self._utkast()).encode(), {}
        if (metode, sti) == ("GET", d + "/files"):
            return 200, json.dumps([{"id": f["id"], "filename": n, "filesize": len(f["b"]),
                                     "checksum": hashlib.md5(f["b"]).hexdigest()} for n, f in self.filer.items()]).encode(), {}
        if metode == "DELETE" and sti.startswith(d + "/files/"):
            fid = sti.rsplit("/", 1)[1]
            navn = [n for n, f in self.filer.items() if f["id"] == fid]
            if self.publisert or not navn:
                return 404, b"{}", {}
            del self.filer[navn[0]]
            return 204, b"", {}
        if metode == "PUT" and sti.startswith("/files/bøtte-1/"):
            if self.publisert:
                return 403, b"{}", {}
            from urllib.parse import unquote
            b = kropp.read()
            assert lengde == len(b)
            navn = unquote(sti.removeprefix("/files/bøtte-1/"))
            self.filer[navn] = {"id": f"ny-{len(self.logg)}", "b": b}
            return 201, json.dumps({"key": navn, "checksum": "md5:" + hashlib.md5(b).hexdigest()}).encode(), {}
        if (metode, sti) == ("POST", d + "/actions/publish"):
            if self.publisert:
                return 400, b"{}", {}
            self.publisert = True
            return 202, json.dumps({"id": self.utkast, "doi": f"10.5281/zenodo.{self.utkast}", "conceptdoi": "10.5281/zenodo.1",
                                    "links": {"record_html": f"https://zenodo.org/records/{self.utkast}"}}).encode(), {}
        return 404, json.dumps({"message": "ukjent"}).encode(), {}


def _bygg(vault, filer: dict[str, bytes], forrige: dict[str, bytes], versjon="0.6.0"):
    """Et utkast på «Vault» med byggemanifest og filkart, slik utgivelse.bygg skriver dem."""
    ut = vault / "zenodo" / f"v{versjon}-utkast"
    (vault / "zenodo" / f"v{versjon}-bygg").mkdir(parents=True)
    ut.mkdir()
    rader = []
    for n, b in sorted(filer.items()):
        (ut / n).write_bytes(b)
        rader.append({"navn": n, "kilde": "test", "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                      "md5": hashlib.md5(b).hexdigest()})
    kart = {"uendret": sorted(n for n in filer if forrige.get(n) == filer[n]),
            "endret": sorted(n for n in filer if n in forrige and forrige[n] != filer[n]),
            "ny": sorted(n for n in filer if n not in forrige), "fjernet": sorted(n for n in forrige if n not in filer)}
    m = {"versjon": versjon, "head": "abc", "utkast": str(ut), "publisert": False, "filer": rader, "filkart": kart}
    Z.manifeststi(vault, versjon).write_text(json.dumps(m), encoding="utf-8")
    return m


def _bygg_om(vault, m, versjon="0.6.0"):
    """Manifestet regnet på nytt fra filene i utkastet, som etter et nytt bygg."""
    ut = vault / "zenodo" / f"v{versjon}-utkast"
    for f in m["filer"]:
        b = (ut / f["navn"]).read_bytes()
        f |= {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "md5": hashlib.md5(b).hexdigest()}
    Z.manifeststi(vault, versjon).write_text(json.dumps(m), encoding="utf-8")
    return m


FORRIGE = {"README.md": b"gammel", "METODE.md": b"metode", "B5-PORTSTATUS.md": b"ut", "saker.zip": b"zip-1"}
NYE = {"README.md": b"ny forside", "METODE.md": b"metode", "saker.zip": b"zip-2", "maalefiler.zip": b"maal",
       "GJENOPPTAK_ADDENDUMSTATUS_v1_2026-10-10.md": b"status", "navn med mellomrom og æøå.md": b"x"}


@pytest.fixture
def oppsett(tmp_path):
    fz = FalskZenodo(FORRIGE)
    pauser = []
    k = Z.Klient(NØKKEL, send=fz.send, sov=pauser.append)
    m = _bygg(tmp_path, NYE, FORRIGE)
    return fz, k, tmp_path, m, pauser


def test_nøkkelen_leses_fra_fil_og_vises_aldri(tmp_path):
    f = tmp_path / "zenodo.env"
    f.write_text(f"# kommentar\nANNET=1\nexport ZENODO_TOKEN='{NØKKEL}'\n", encoding="utf-8")
    assert Z.les_nøkkel(f) == NØKKEL
    assert NØKKEL not in repr(Z.Klient(Z.les_nøkkel(f)))
    f.write_text("ANNET=1\n", encoding="utf-8")
    with pytest.raises(Z.ZenodoFeil, match="ZENODO_TOKEN står ikke"):
        Z.les_nøkkel(f)
    with pytest.raises(Z.ZenodoFeil, match="finnes ikke"):
        Z.les_nøkkel(tmp_path / "ingen.env")


def test_nøkkelen_går_bare_i_hodet_og_aldri_i_url_eller_feilmelding(oppsett):
    fz, k, vault, m, _ = oppsett
    Z.reserver(k, vault, "0.6.0", "111")
    Z.last_opp(k, vault, "0.6.0")
    assert all(NØKKEL not in sti and "access_token" not in sti for _, sti in fz.logg)
    assert all(h["Authorization"] == f"Bearer {NØKKEL}" for h in fz.hoder)
    with pytest.raises(Z.ZenodoFeil, match="aldri i en URL"):
        k.kall("GET", f"{API}/deposit/depositions?access_token={NØKKEL}")
    with pytest.raises(Z.ZenodoFeil, match="går ikke til"):
        k.kall("GET", "https://example.org/api/x")
    k2 = Z.Klient(NØKKEL, send=lambda *a: (500, f"feil med {NØKKEL} i svaret".encode(), {}), sov=lambda s: None)
    with pytest.raises(Z.ZenodoFeil) as e:
        k2.kall("POST", f"{API}/x")
    assert NØKKEL not in str(e.value) and "[nøkkel]" in str(e.value)


def test_planen_sletter_endrede_og_fjernede_og_laster_opp_nye_og_endrede(oppsett):
    fz, k, vault, m, _ = oppsett
    assert Z.plan_fra_filkart(m) == {"slett": ["B5-PORTSTATUS.md", "README.md", "saker.zip"],
                                     "last_opp": sorted(set(NYE) - {"METODE.md"}), "behold": ["METODE.md"]}
    Z.reserver(k, vault, "0.6.0", "111")
    p = Z.plan(m, Z.fjernfiler(k, Z.les_tilstand(vault, "0.6.0")))
    assert sorted(f["navn"] for f in p["slett"]) == ["B5-PORTSTATUS.md", "README.md", "saker.zip"]
    assert p["behold"] == ["METODE.md"] and p["last_opp"] == sorted(set(NYE) - {"METODE.md"})
    # records-API-et skriver md5 med prefiks; planen leser begge former
    assert Z.plan(m, [{"id": "a", "filename": "METODE.md", "checksum": "md5:" + hashlib.md5(b"metode").hexdigest()}])["behold"] == ["METODE.md"]


def test_reserver_skriver_tilstand_og_gjenbruker_utkastet(oppsett):
    fz, k, vault, m, _ = oppsett
    t = Z.reserver(k, vault, "0.6.0", "111")
    assert t["utkast_id"] == 222 and t["doi"] == "10.5281/zenodo.222" and t["publisert"] is False
    assert t["bucket"] == fz.bucket and json.loads(Z.tilstandssti(vault, "0.6.0").read_text()) == t
    n = len(fz.logg)
    assert Z.reserver(k, vault, "0.6.0", "111") == t and len(fz.logg) == n          # ingen ny versjon ved gjentak
    assert [x for x in fz.logg if x[0] == "POST"] == [("POST", "/deposit/depositions/111/actions/newversion")]


def test_last_opp_gjør_zenodo_likt_utkastet_og_kan_gjentas(oppsett):
    fz, k, vault, m, pauser = oppsett
    with pytest.raises(Z.ZenodoFeil, match="kjør reserver først"):
        Z.last_opp(k, vault, "0.6.0")
    Z.reserver(k, vault, "0.6.0", "111")
    assert Z.verifiser(k, vault, "0.6.0")                                             # før opplasting: avvik
    r = Z.last_opp(k, vault, "0.6.0", dato="2026-10-12")
    assert r == {"slettet": 3, "lastet_opp": 5, "sto": 1}
    assert {n: f["b"] for n, f in fz.filer.items()} == NYE
    assert fz.metadata["version"] == "0.6.0" and fz.metadata["publication_date"] == "2026-10-12"
    assert fz.metadata["title"] == "Gjenopptak"                                       # øvrig metadata er arvet urørt
    assert Z.verifiser(k, vault, "0.6.0") == []
    assert Z.last_opp(k, vault, "0.6.0") == {"slettet": 0, "lastet_opp": 0, "sto": 6}
    assert len(pauser) >= k.kall_gjort and set(pauser) == {Z.PAUSE}                   # ett opphold per kall
    assert not fz.publisert and not any(sti.endswith("/actions/publish") for _, sti in fz.logg)


def test_last_opp_nekter_når_utkastet_på_disk_ikke_er_manifestets(oppsett):
    fz, k, vault, m, _ = oppsett
    Z.reserver(k, vault, "0.6.0", "111")
    ut = vault / "zenodo" / "v0.6.0-utkast"
    (ut / "saker.zip").write_bytes(b"zip-X")                                          # samme størrelse, annet innhold
    assert Z.kontroller_utkast(m) == ["feil sjekksum: saker.zip"]
    with pytest.raises(Z.ZenodoFeil, match="ikke det manifestet beskriver"):
        Z.last_opp(k, vault, "0.6.0")
    assert not any(metode in ("PUT", "DELETE") for metode, _ in fz.logg)
    (ut / "saker.zip").write_bytes(b"zip-2")
    (ut / "uvedkommende.txt").write_bytes(b"?")
    (ut / "METODE.md").unlink()
    assert Z.kontroller_utkast(m) == ["mangler på disk: METODE.md", "på disk, ikke i manifestet: uvedkommende.txt"]


def test_midlertidig_feil_prøves_igjen_men_aldri_for_post(oppsett):
    fz, k, vault, m, _ = oppsett
    fz.feil_en_gang[("POST", "/deposit/depositions/111/actions/newversion")] = 503
    with pytest.raises(Z.ZenodoFeil, match="ga 503"):
        Z.reserver(k, vault, "0.6.0", "111")
    assert not Z.tilstandssti(vault, "0.6.0").exists() and len(fz.logg) == 1
    Z.reserver(k, vault, "0.6.0", "111")
    fz.feil_en_gang[("GET", "/deposit/depositions/222/files")] = 429
    Z.last_opp(k, vault, "0.6.0")
    assert Z.verifiser(k, vault, "0.6.0") == []


def test_publiser_krever_eierens_ja_ordrett_og_null_avvik(oppsett):
    fz, k, vault, m, _ = oppsett
    Z.reserver(k, vault, "0.6.0", "111")
    for ja in ("", "ja", "publiser", "publiser v0.5.0", "PUBLISER V0.6.0"):
        with pytest.raises(Z.ZenodoFeil, match="eierens ja ordrett"):
            Z.publiser(k, vault, "0.6.0", ja)
    with pytest.raises(Z.ZenodoFeil, match="avvik, ingenting publisert"):              # riktig ja, men ikke lastet opp
        Z.publiser(k, vault, "0.6.0", "publiser v0.6.0")
    Z.last_opp(k, vault, "0.6.0")
    fz.filer["README.md"]["b"] = b"endret etter opplasting"
    with pytest.raises(Z.ZenodoFeil, match="avvik, ingenting publisert"):
        Z.publiser(k, vault, "0.6.0", "publiser v0.6.0")
    fz.filer["README.md"]["b"] = NYE["README.md"]
    fz.metadata["version"] = "0.5.0"
    with pytest.raises(Z.ZenodoFeil, match="avvik, ingenting publisert"):
        Z.publiser(k, vault, "0.6.0", "publiser v0.6.0")
    assert not fz.publisert


def test_publiser_skriver_doi_og_kan_ikke_gjentas(oppsett):
    fz, k, vault, m, _ = oppsett
    Z.reserver(k, vault, "0.6.0", "111")
    Z.last_opp(k, vault, "0.6.0")
    t = Z.publiser(k, vault, "0.6.0", "publiser v0.6.0")
    assert fz.publisert and t["publisert"] is True and t["doi"] == "10.5281/zenodo.222"
    assert t["antall_filer"] == 6 and t["utkast_sha256"] == Z.utkast_sha256(m) and t["head"] == "abc"
    assert json.loads(Z.tilstandssti(vault, "0.6.0").read_text())["publisert"] is True
    for steg in (lambda: Z.publiser(k, vault, "0.6.0", "publiser v0.6.0"), lambda: Z.last_opp(k, vault, "0.6.0")):
        with pytest.raises(Z.ZenodoFeil, match="alt publisert"):
            steg()
    assert [sti for metode, sti in fz.logg if sti.endswith("/actions/publish")] == ["/deposit/depositions/222/actions/publish"]


def test_manifestet_avvises_over_hundre_filer_og_ved_feil_versjon(tmp_path):
    _bygg(tmp_path, {f"f{i:03d}.md": b"x" for i in range(101)}, {})
    with pytest.raises(Z.ZenodoFeil, match="høyst 100"):
        Z.les_manifest(tmp_path, "0.6.0")
    sti = Z.manifeststi(tmp_path, "0.6.0")
    m = json.loads(sti.read_text()); m["versjon"] = "0.5.0"; sti.write_text(json.dumps(m))
    with pytest.raises(Z.ZenodoFeil, match="ikke 0.6.0"):
        Z.les_manifest(tmp_path, "0.6.0")


def test_utkastets_sha256_følger_innholdet_og_ikke_rekkefølgen(oppsett):
    _, _, _, m, _ = oppsett
    snudd = m | {"filer": list(reversed(m["filer"]))}
    assert Z.utkast_sha256(snudd) == Z.utkast_sha256(m)
    annen = m | {"filer": [f | ({"sha256": "0" * 64} if f["navn"] == "README.md" else {}) for f in m["filer"]]}
    assert Z.utkast_sha256(annen) != Z.utkast_sha256(m)


def test_kommandolinjen_skriver_ikke_uten_ja_og_plan_gjør_ingen_kall(oppsett, capsys):
    fz, k, vault, m, _ = oppsett
    assert Z.main(["plan", "--versjon", "0.6.0"], klient=k, vault=vault) == 0
    ut = capsys.readouterr().out
    assert "slett 3 · last opp 5 · står 1" in ut and Z.utkast_sha256(m) in ut and fz.logg == []
    for steg in ("reserver", "last-opp", "publiser"):
        assert Z.main([steg, "--versjon", "0.6.0", "--forrige", "111"], klient=k, vault=vault) == 2
    assert "krever --ja" in capsys.readouterr().err and fz.logg == []
    assert Z.main(["reserver", "--versjon", "0.6.0", "--ja"], klient=k, vault=vault) == 2          # uten --forrige
    assert Z.main(["reserver", "--versjon", "0.6.0", "--forrige", "111", "--ja"], klient=k, vault=vault) == 0
    assert Z.main(["verifiser", "--versjon", "0.6.0"], klient=k, vault=vault) == 1                # ikke lastet opp ennå
    assert Z.main(["last-opp", "--versjon", "0.6.0", "--ja"], klient=k, vault=vault) == 0
    assert Z.main(["verifiser", "--versjon", "0.6.0"], klient=k, vault=vault) == 0
    assert Z.main(["publiser", "--versjon", "0.6.0", "--ja"], klient=k, vault=vault) == 2          # «ja» alene holder ikke
    assert not fz.publisert
    assert Z.main(["publiser", "--versjon", "0.6.0", "--ja", "publiser v0.6.0"], klient=k, vault=vault) == 0
    assert fz.publisert and "PUBLISERT v0.6.0 · 10.5281/zenodo.222 · 6 filer" in capsys.readouterr().out


def test_plassholderne_er_gyldige_etter_cff_skjemaet():
    import re
    assert re.fullmatch(r"10\.\d{4,9}(\.\d+)?/[A-Za-z0-9:/_;\-\.\(\)\[\]\\]+", Z.PLASSHOLDER_DOI)          # doi-mønsteret i CFF 1.2.0
    assert re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])", Z.PLASSHOLDER_DATO)        # datomønsteret
    assert not re.fullmatch(r"10\.5281/zenodo\.\d+", Z.PLASSHOLDER_DOI)                                    # og kan ikke forveksles med en ekte


def test_fyll_setter_doi_og_dato_og_nekter_det_som_ikke_er_det(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/ZENODO.md").write_text(f"Gjeldende: 0.6.0 ({Z.PLASSHOLDER_DATO}). DOI {Z.PLASSHOLDER_DOI}. Post https://doi.org/{Z.PLASSHOLDER_DOI}\n", encoding="utf-8")
    (tmp_path / "CITATION.cff").write_text(f'date-released: "{Z.PLASSHOLDER_DATO}"\n    value: "{Z.PLASSHOLDER_DOI}"\n', encoding="utf-8")
    (tmp_path / "docs/RELEASE-NOTES-v0.6.0.md").write_text("ingen plassholder her\n", encoding="utf-8")
    for doi, dato in (("10.5281/zenodo.abc", "2026-10-12"), (Z.PLASSHOLDER_DOI, "2026-10-12"), ("10.5281/zenodo.24000001", "12.10.2026"),
                      ("10.5281/zenodo.24000001", Z.PLASSHOLDER_DATO)):
        with pytest.raises(Z.ZenodoFeil):
            Z.fyll(tmp_path, "0.6.0", doi, dato)
    assert Z.PLASSHOLDER_DOI in (tmp_path / "CITATION.cff").read_text()                                 # ingenting skrevet ved feil
    assert Z.fyll(tmp_path, "0.6.0", "10.5281/zenodo.24000001", "2026-10-12") == {"docs/ZENODO.md": 3, "CITATION.cff": 2, "docs/RELEASE-NOTES-v0.6.0.md": 0}
    assert (tmp_path / "CITATION.cff").read_text() == 'date-released: "2026-10-12"\n    value: "10.5281/zenodo.24000001"\n'
    assert "https://doi.org/10.5281/zenodo.24000001" in (tmp_path / "docs/ZENODO.md").read_text()
    with pytest.raises(Z.ZenodoFeil, match="ingen plassholder igjen"):
        Z.fyll(tmp_path, "0.6.0", "10.5281/zenodo.24000001", "2026-10-12")


def test_utkast_med_plassholder_eller_feil_doi_lastes_ikke_opp_og_publiseres_ikke(tmp_path):
    fz = FalskZenodo(FORRIGE)
    k = Z.Klient(NØKKEL, send=fz.send, sov=lambda s: None)
    ufylt = NYE | {"ZENODO.md": f"Versjons-DOI {Z.PLASSHOLDER_DOI}, publisert {Z.PLASSHOLDER_DATO}".encode(), "CITATION.cff": f'date-released: "{Z.PLASSHOLDER_DATO}"'.encode()}
    m = _bygg(tmp_path, ufylt, FORRIGE)
    assert Z.plassholdere(m) == ["plassholder ikke fylt: CITATION.cff", "plassholder ikke fylt: ZENODO.md"]
    Z.reserver(k, tmp_path, "0.6.0", "111")
    with pytest.raises(Z.ZenodoFeil, match="ikke klart for opplasting"):
        Z.last_opp(k, tmp_path, "0.6.0")
    assert not any(metode in ("PUT", "DELETE") for metode, _ in fz.logg)
    with pytest.raises(Z.ZenodoFeil, match="avvik, ingenting publisert"):
        Z.publiser(k, tmp_path, "0.6.0", "publiser v0.6.0")
    assert not fz.publisert


def test_zenodo_md_maa_foere_den_reserverte_doien(tmp_path):
    fz = FalskZenodo(FORRIGE)
    k = Z.Klient(NØKKEL, send=fz.send, sov=lambda s: None)
    m = _bygg(tmp_path, NYE | {"ZENODO.md": b"Versjons-DOI 10.5281/zenodo.999, publisert 2026-10-12"}, FORRIGE)
    t = Z.reserver(k, tmp_path, "0.6.0", "111")
    assert Z.doi_ført(m, t) == ["ZENODO.md fører ikke den reserverte DOI-en 10.5281/zenodo.222"]
    with pytest.raises(Z.ZenodoFeil, match="ikke klart for opplasting"):
        Z.last_opp(k, tmp_path, "0.6.0")
    (tmp_path / "zenodo/v0.6.0-utkast/ZENODO.md").write_bytes(b"Versjons-DOI 10.5281/zenodo.222, publisert 2026-10-12")
    m2 = _bygg_om(tmp_path, m)
    assert Z.doi_ført(m2, t) == [] and Z.last_opp(k, tmp_path, "0.6.0")["lastet_opp"] == 6
    assert Z.publiser(k, tmp_path, "0.6.0", "publiser v0.6.0")["publisert"] is True


def test_fyll_fra_kommandolinjen_leser_doien_fra_tilstandsfilen(oppsett, tmp_path, capsys):
    fz, k, vault, m, _ = oppsett
    repo = tmp_path / "repo"; (repo / "docs").mkdir(parents=True)
    (repo / "docs/ZENODO.md").write_text(Z.PLASSHOLDER_DOI + " " + Z.PLASSHOLDER_DATO, encoding="utf-8")
    (repo / "CITATION.cff").write_text(Z.PLASSHOLDER_DATO, encoding="utf-8")
    (repo / "docs/RELEASE-NOTES-v0.6.0.md").write_text(Z.PLASSHOLDER_DOI, encoding="utf-8")
    assert Z.main(["fyll", "--versjon", "0.6.0", "--dato", "2026-10-12"], klient=k, vault=vault, repo=repo) == 2      # ingen tilstandsfil ennå
    Z.reserver(k, vault, "0.6.0", "111")
    n = len(fz.logg)
    assert Z.main(["fyll", "--versjon", "0.6.0", "--dato", "2026-10-12"], klient=k, vault=vault, repo=repo) == 0
    assert (repo / "docs/ZENODO.md").read_text() == "10.5281/zenodo.222 2026-10-12" and len(fz.logg) == n             # ingen nettkall
    assert "docs/ZENODO.md: 2 plassholdere fylt" in capsys.readouterr().out

