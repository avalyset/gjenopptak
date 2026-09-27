"""Sekvensiell trekking i frørekkefølge (ADDENDUM-09). Ingen nettkall, ingen ekte rammeliste."""

import json
import random

import pytest

from gjenopptak.harvest import draw as dr
from gjenopptak.harvest.fetchtest import FetchVerdict

FELT = ("T10001", "T10002")


def _ids(n: int) -> list[str]:
    return [f"W{i:04d}" for i in range(n)]


def _rad(wid: str, *, doi: str | None = None, pdf: str | None = "https://pub.example/x.pdf") -> dict:
    return {"work_id": wid, "doi": doi, "publication_year": 2018, "best_oa_location": {"pdf_url": pdf}}


def _meta(wid: str, *, type_: str = "article", topics=("T10001",), title: str = "Et helt vanlig verk om noe",
          pmcid: str | None = None) -> dict:
    return {"id": f"https://openalex.org/{wid}", "type": type_, "display_name": title,
            "topics": [{"id": f"https://openalex.org/{t}", "score": 1.0 - i / 10} for i, t in enumerate(topics)],
            "ids": {"pmcid": pmcid} if pmcid else {}}


def _inne(wid: str, gate: str = "P3-PDF") -> FetchVerdict:
    return FetchVerdict(work_id=wid, doi=None, in_frame=True, gate=gate, sha256="a" * 64, file=f"{wid}.pdf", bytes=10)


def _ute(wid: str, reason: str = "http-403-text/html") -> FetchVerdict:
    return FetchVerdict(work_id=wid, doi=None, in_frame=False, gate="P3-PDF", reason=reason)


def _tom_logg(tmp_path, rows=()):
    p = tmp_path / "leste.json"
    p.write_text(json.dumps(list(rows)), encoding="utf-8")
    return dr.Exclusions.from_log(p)


# --------------------------------------------------------------------------- #

def test_rekkefolgen_er_stokkingen_i_addendum01():
    ids = _ids(10)
    forventet = list(ids)
    random.Random(93883171).shuffle(forventet)
    assert dr.PREREG_SEED == int("05988b23", 16) == 93883171
    assert dr.draw_order(ids) == forventet
    # festet vektor: endrer Python stokkingen, feiler denne før en trekking gjør det
    assert dr.draw_order(ids) == [f"W{i:04d}" for i in (5, 4, 2, 0, 9, 6, 7, 8, 1, 3)]
    assert dr.order_sha256(dr.draw_order(ids)) == dr.order_sha256(dr.draw_order(ids))


def test_usortert_eller_duplikat_liste_avvises():
    with pytest.raises(ValueError):
        dr.draw_order(["W2", "W1"])
    with pytest.raises(ValueError):
        dr.draw_order(["W1", "W1"])


def test_vilkaarene_i_rekkefolge_og_stopp_ved_n(tmp_path):
    order = _ids(12)
    rader = {w: _rad(w) for w in order}
    rader["W0000"]["doi"] = "10.1016/J.APENERGY.2018.04.048"          # kontroll, store bokstaver
    meta = {w: _meta(w) for w in order}
    meta["W0002"] = _meta("W0002", type_="erratum")
    meta["W0003"] = _meta("W0003", topics=("T99999", "T88888", "T77777", "T10001"))   # feltets ID bare som fjerde
    meta["W0005"] = None
    verdikter = {w: _inne(w) for w in order}
    verdikter["W0006"] = _ute("W0006")
    verdikter["W0008"] = _inne("W0008", gate="P1-JATS")
    tekst = {w: "Et helt vanlig verk om noe" for w in order}
    tekst["W0007"] = "en helt annen artikkel"
    kalt: list[str] = []

    def vf(pos, row):
        kalt.append(row["work_id"])
        return verdikter[row["work_id"]]

    ut = dr.decide(order, rader, field_ids=FELT, exclusions=_tom_logg(tmp_path), drawn_elsewhere={"W0004"},
                   meta_for=lambda p, w: meta[w], verdict_for=vf, text_for=lambda v: tekst[v.work_id], n=3)
    grunner = {d.work_id: (d.utfall, d.grunn) for d in ut}
    assert grunner["W0000"] == ("hoppet", "kontroll")
    assert grunner["W0001"] == ("trukket", None)
    assert grunner["W0002"] == ("hoppet", "ikke_artikkel:erratum")
    assert grunner["W0003"] == ("hoppet", "utenfor_felt")
    assert grunner["W0004"] == ("hoppet", "dobbeltramme")
    assert grunner["W0005"] == ("hoppet", "mangler-metadata")
    assert grunner["W0006"][0] == "hoppet" and grunner["W0006"][1].startswith("port:http-403")
    assert grunner["W0007"][0] == "hoppet" and grunner["W0007"][1].startswith("identitet:")
    assert grunner["W0008"] == ("trukket", None)               # P1: DOI-matchet, ingen tekstsjekk
    assert grunner["W0009"] == ("trukket", None)
    assert [d.trekkposisjon for d in ut if d.utfall == "trukket"] == [2, 9, 10]
    assert len(ut) == 10                                       # stopper ved n, ser ikke W0010
    assert kalt == ["W0001", "W0006", "W0007", "W0008", "W0009"]   # porten bare for dem som besto 1–4
    rows = dr.utvalg_rows(ut)
    assert [r["trekkposisjon"] for r in rows] == [2, 9, 10]
    assert set(rows[0]) == {"work_id", "doi", "aar", "trekkposisjon", "port_ledd", "sha256"}


def test_karakteriseringen_tester_de_forste_posisjonene_uansett_vilkaar(tmp_path):
    order = _ids(10)
    rader = {w: _rad(w) for w in order}
    meta = {w: _meta(w) for w in order}
    meta["W0001"] = _meta("W0001", type_="paratext")
    kalt: list[str] = []

    def vf(pos, row):
        kalt.append(row["work_id"])
        return _inne(row["work_id"]) if pos % 2 else _ute(row["work_id"])

    ut = dr.decide(order, rader, field_ids=FELT, exclusions=_tom_logg(tmp_path), drawn_elsewhere=set(),
                   meta_for=lambda p, w: meta[w], verdict_for=vf, text_for=lambda v: "Et helt vanlig verk om noe",
                   n=1, n_char=6)
    assert kalt == _ids(6)                                     # alle seks, også paratext-verket
    assert [d.utfall for d in ut] == ["trukket"] + ["etter-stopp"] * 5
    assert ut[1].grunn == "ikke_artikkel:paratext"             # grunnen føres også etter stopp
    k = dr.characterize(ut)
    assert k["n_forsok"] == 6 and k["hentbar"] == 3 and k["andel"] == 0.5
    assert k["verter"] == [{"vert": "pub.example", "raa": 6, "hentbar": 3}]
    assert k["frafall"] == {"403": 3}


def test_eksklusjoner_fra_leseloggen(tmp_path):
    ex = _tom_logg(tmp_path, [
        {"felt": "x", "doi": "10.1/ABC", "work": "W0001"},
        {"felt": "x", "doi": None, "pmcid": "PMC4342813"},
        {"felt": "x", "doaj_id": "d1", "tittel": "Food for Thought: The Translation"},
        {"felt": "x", "doi": "10.1/tittel-ignoreres", "tittel": "Et helt vanlig verk om noe"},
    ])
    assert ex.reason(_rad("W0001"), None) == "lest"
    assert ex.reason(_rad("W0009", doi="10.1/abc"), None) == "lest"
    assert ex.reason(_rad("W0009"), _meta("W0009", pmcid="https://www.ncbi.nlm.nih.gov/pmc/articles/4342813")) == "lest"
    assert ex.reason(_rad("W0009"), _meta("W0009", title="Food for thought — the translation")) == "lest"
    assert ex.reason(_rad("W0009"), _meta("W0009")) is None     # tittelmatch bare for rader uten ID
    assert ex.reason(_rad("W3000588547"), None) == "kontroll"
    assert ex.n_log == 4 and len(ex.log_sha256) == 64


def test_topp3_etter_score():
    m = {"topics": [{"id": "T3", "score": 0.5}, {"id": "T1", "score": 0.9}, {"id": "T4", "score": 0.1},
                    {"id": "T2", "score": 0.7}]}
    assert dr.top3_topics(m) == ["T1", "T2", "T3"]
    assert dr.in_field(m, {"T3"}) and not dr.in_field(m, {"T4"})


def test_wilson_stemmer_med_addendum03():
    lo, hi = dr.wilson(5, 30)                                  # energimodellering: 17 % (7–34 %)
    assert round(lo, 2) == 0.07 and round(hi, 2) == 0.34


def test_feltrekkefolgen_haandheves_og_utvalg_overskrives_aldri(tmp_path):
    with pytest.raises(dr.DrawRefused):
        dr.drawn_in_earlier_fields(tmp_path, "arkeologi")
    assert dr.drawn_in_earlier_fields(tmp_path, "energimodellering") == set()
    (tmp_path / "utvalg-energimodellering.jsonl").write_text('{"work_id": "W1"}\n', encoding="utf-8")
    assert dr.drawn_in_earlier_fields(tmp_path, "arkeologi") == {"W1"}
    with pytest.raises(dr.DrawRefused):
        dr.assert_not_drawn(tmp_path, "energimodellering")
    dr.assert_not_drawn(tmp_path, "arkeologi")


def test_frafallskategorier():
    assert dr.failure_category("http-403-text/html; charset=UTF-8") == "403"
    assert dr.failure_category("http-200-text/html") == "HTML i stedet for PDF"
    assert dr.failure_category("ingen-pdf-lenke") == "ingen PDF-lenke"
    assert dr.failure_category("ConnectError") == "nettverksfeil"
