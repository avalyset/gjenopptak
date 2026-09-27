"""Måleverktøyet for ADDENDUM-01. Offline; nettdelen ligger i test_smoke_network.py."""

import pytest
from control import Corpus

from gjenopptak.harvest import coverage as cv


def test_frøet_for_dekningsmåling_er_ikke_prereg_frøet():
    """PREREG-v1 §4-frøet hører til trekkingen. Målingene skal ikke røre det."""
    assert cv.COVERAGE_SEED_HEX == "2ef3dee8"
    assert cv.COVERAGE_SEED_INT == 734248
    assert cv.COVERAGE_SEED_HEX != "05988b23"


def test_filterstrengen_er_den_addendumet_oppgir():
    f = f"{cv.topic_filter(cv.TOPIC_IDS['energimodellering'])},{cv.year_filter()}"
    assert f == "topics.id:T10424|T11185|T11941,publication_year:2015-2020"


def test_alle_fire_felt_har_verifiserte_id_er():
    assert set(cv.TOPIC_IDS) == {"tekstvitenskap", "klinisk_epidemiologi", "arkeologi", "energimodellering"}
    for felt, ids in cv.TOPIC_IDS.items():
        assert ids, felt
        assert all(t.startswith("T") and t[1:].isdigit() for t in ids), ids


def test_kontrollens_topic_er_med_i_energirammen():
    """PREREG-v1 §7: faller den positive kontrollen utenfor rammen, er rammen gal.

    Kontrollen har T11941 som primary_topic og T10424 blant øvrige topics —
    men ikke T11185, som et fritekstsøk peker mot.
    """
    ids = cv.TOPIC_IDS[cv.POSITIVE_CONTROL_FIELD]
    assert "T11941" in ids and "T10424" in ids


def test_godkjente_og_forkastede_id_er_er_disjunkte():
    for felt, ids in cv.TOPIC_IDS.items():
        forkastet = {t for t, _, _ in cv.TOPIC_REJECTED.get(felt, ())}
        assert not (set(ids) & forkastet), felt


def test_pdf_url_faller_tilbake_til_primærplassering():
    assert cv.pdf_url_of({"best_oa_location": {"pdf_url": "a"}}) == "a"
    assert cv.pdf_url_of({"best_oa_location": None, "primary_location": {"pdf_url": "b"}}) == "b"
    assert cv.pdf_url_of({"best_oa_location": {"pdf_url": None}, "primary_location": {}}) is None
    assert cv.pdf_url_of({}) is None


def test_wilson_dekker_kantene():
    p, lo, hi = cv.wilson(0, 48)          # nullresultatet i energimodellering
    assert p == 0.0 and lo == 0.0 and 0.0 < hi < 0.15
    p, lo, hi = cv.wilson(19, 50)         # klinisk epidemiologi, 38 %
    assert abs(p - 0.38) < 1e-9 and lo < p < hi
    assert cv.wilson(0, 0) == (0.0, 0.0, 0.0)
    p, lo, hi = cv.wilson(10, 10)
    assert p == 1.0 and hi == 1.0 and lo < 1.0


def test_jats_kriteriet_krever_alle_tre_betingelser():
    full = cv.EpmcHit("10.1/x", "PMC1", True, True)
    assert full.jats_available
    for h in (
        cv.EpmcHit("10.1/x", None, True, True),    # ingen pmcid
        cv.EpmcHit("10.1/x", "PMC1", False, True), # ikke i EPMC
        cv.EpmcHit("10.1/x", "PMC1", True, False), # ikke OA
    ):
        assert not h.jats_available


def test_retry_dekker_de_målte_feilkodene():
    """Europe PMC svarer sporadisk 404 på en query som virker ved neste forsøk."""
    for kode in (404, 429, 500, 502, 503, 504):
        assert kode in cv._RETRY_STATUS


def test_select_inneholder_ikke_is_oa():
    """is_oa finnes bare inne i open_access; som toppnivåfelt gir det 400."""
    felter = cv.WORK_SELECT.split(",")
    assert "is_oa" not in felter
    assert "open_access" in felter and "best_oa_location" in felter


def test_addendum01_gjengir_de_verifiserte_id_ene():
    """Dokumentet og koden skal ikke kunne skli fra hverandre."""
    from pathlib import Path

    add = Path(__file__).resolve().parent.parent / "ADDENDUM-01.md"
    tekst = Corpus("ADDENDUM-01", add.read_text(encoding="utf-8").splitlines())
    tekst.must_hit("05988b23")                      # prereg-frøet
    tekst.must_hit("2ef3dee8")                      # målefrøet, et annet
    for ids in cv.TOPIC_IDS.values():
        for t in ids:
            tekst.must_hit(t)
    for rej in cv.TOPIC_REJECTED.values():
        for t, _, _ in rej:
            tekst.must_hit(t)
    tekst.must_hit("Ingen trekking av utvalg er utført")
    tekst.expect_none("has_fulltext: true er beholdt")


# --------------------------------------------------------------------------- #
# Rammediagnostikk (ADDENDUM-02 §6-§7)
# --------------------------------------------------------------------------- #

def test_rammefilteret_er_det_addendum01_oppgir():
    assert cv.frame_filter("arkeologi") == (
        "topics.id:T10421|T10087,publication_year:2015-2020,open_access.is_oa:true")
    assert cv.frame_filter("arkeologi", year=2017).endswith(
        "publication_year:2017,open_access.is_oa:true")


def test_unionsfilteret_slaar_sammen_id_ene_uten_duplikater():
    f = cv.union_filter(["arkeologi", "energimodellering"])
    ids = f.split(",")[0].removeprefix("topics.id:").split("|")
    assert ids == ["T10421", "T10087", "T10424", "T11185", "T11941"]
    assert len(ids) == len(set(ids))


def test_snitt_av_unioner_er_riktig_paa_kjente_tall():
    """|A∩B| = |A| + |B| - |A∪B|, og dual inklusjon-eksklusjon for fler."""
    A, B = frozenset(["a"]), frozenset(["b"])
    unions = {A: 10, B: 20, frozenset(["a", "b"]): 25}
    snitt = cv.intersections_from_unions(unions)
    assert snitt[frozenset(["a", "b"])] == 5
    assert snitt[A] == 10


def test_noeyaktig_k_summerer_til_unionen():
    """De målte tallene: 140 verk i to rammer, ingen i tre eller fire."""
    felt = ["a", "b", "c"]
    unions = {}
    for r in (1, 2, 3):
        from itertools import combinations
        for combo in combinations(felt, r):
            unions[frozenset(combo)] = {1: 100, 2: 190, 3: 280}[r]
    snitt = cv.intersections_from_unions(unions)
    k = cv.exactly_k_from_intersections(snitt, felt)
    assert sum(k.values()) == unions[frozenset(felt)]


def test_addendum02_gjengir_kontrollene_og_de_aapne_postene():
    from pathlib import Path

    add = Path(__file__).resolve().parent.parent / "ADDENDUM-02.md"
    tekst = Corpus("ADDENDUM-02", add.read_text(encoding="utf-8").splitlines())
    tekst.must_hit(cv.POSITIVE_CONTROL_DOI)
    tekst.must_hit("10.1016/s2468-2667(17)30217-7")     # klinisk epidemiologi, H8
    tekst.must_hit("10.1038/s41467-019-11357-9")        # arkeologi, H7
    tekst.must_hit("ingen funnet")                      # tekstvitenskap, åpen post
    tekst.must_hit("section_label_provenance")          # ADR-0007 bæres videre
    tekst.must_hit("Ingen trekking av utvalg er utført")
    # Kontrollene skal aldri havne i nevneren:
    tekst.must_hit("utenfor nevneren")
