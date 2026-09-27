"""ADDENDUM-03 §2.3: substitusjonsregnskapet, og at usikkerheten bæres med."""

import math

import pytest
from control import Corpus

from gjenopptak.registry import Substitution


def test_punktanslaget_er_n_delt_paa_p():
    s = Substitution("prøve", 25, 15, 30)
    assert s.p == 0.5
    assert s.expected_draws == 50
    assert s.expected_substitutions == 25


def test_de_maalte_tallene_gir_de_rapporterte():
    """Tallene i ADDENDUM-03 §2.3 skal kunne regnes fram på nytt."""
    ventet = {
        "tekstvitenskap": (13, 58, 73),
        "klinisk_epidemiologi": (14, 54, 67),
        "arkeologi": (10, 75, 96),
        "energimodellering": (5, 150, 198),
    }
    for felt, (ok, trekk, k95) in ventet.items():
        s = Substitution(felt, 25, ok, 30)
        assert round(s.expected_draws) == trekk, felt
        assert s.draws_for_confidence() == k95, felt


def test_flagget_ved_over_seksti_trekk():
    assert not Substitution("klinisk", 25, 14, 30).expected_draws > 60
    assert Substitution("arkeologi", 25, 10, 30).expected_draws > 60
    assert Substitution("energi", 25, 5, 30).expected_draws > 60


def test_k95_er_alltid_stoerre_enn_punktanslaget():
    """Punktanslaget holder om lag halvparten av gangene — derfor K95."""
    for ok in (5, 10, 13, 14, 20, 25):
        s = Substitution("f", 25, ok, 30)
        assert s.draws_for_confidence() > s.expected_draws


def test_intervallet_snur_riktig_vei():
    """Lav p gir mange trekk: øvre p-grense gir nedre trekk-grense."""
    s = Substitution("arkeologi", 25, 10, 30)
    lo_p, hi_p = s.p_interval
    lo_d, hi_d = s.draws_interval
    assert lo_p < s.p < hi_p
    assert lo_d < s.expected_draws < hi_d
    assert round(lo_d) == 49 and round(hi_d) == 130


def test_null_hentbare_gir_uendelig():
    s = Substitution("tomt", 25, 0, 30)
    assert s.p == 0.0
    assert s.expected_draws == math.inf
    assert s.expected_substitutions == math.inf


def test_alle_fire_felt_utloeser_stoppregelen_i_addendum01():
    """Forventede substitusjoner overstiger de 25 plassene i alle fire felt."""
    for ok in (13, 14, 10, 5):
        assert Substitution("f", 25, ok, 30).expected_substitutions > 25


def test_addendum03_gjengir_enheten_og_kvoten():
    from pathlib import Path

    add = Path(__file__).resolve().parent.parent / "ADDENDUM-03.md"
    tekst = Corpus("ADDENDUM-03", add.read_text(encoding="utf-8").splitlines())
    tekst.must_hit("M1-streng")
    tekst.must_hit("M1-passasje")
    tekst.must_hit("10.4073/cmdp.2018.2")      # H1-kontrollen
    tekst.must_hit("PMC4875724")               # armeringen av H4-nullresultatet
    tekst.must_hit("1 000")                    # kvotetaket
    tekst.must_hit("895")                      # kall frysingen krever
    tekst.must_hit("Ingen trekking av utvalg er utført")
    # Ingen påstand om at mailto hjelper:
    tekst.expect_none("mailto gir høyere")
