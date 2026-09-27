"""Rammeverket testes før det brukes: en kontroll som ikke kan feile, måler ingenting."""

import pytest
from control import ControlMissed, ControlNotArmed, Corpus


def corpus() -> Corpus:
    return Corpus("prøve", ["alfa beta", "gamma", "beta delta"])


def test_count_teller_i_python():
    c = corpus()
    assert c.count("beta") == 2
    assert c.count("gamma", exact=True) == 1
    assert c.count("gamma") == 1


def test_must_hit_armerer():
    c = corpus()
    assert not c.armed
    assert c.must_hit("beta", at_least=2) == 2
    assert c.armed


def test_must_hit_feiler_naar_kontrollstrengen_mangler():
    c = corpus()
    with pytest.raises(ControlMissed) as e:
        c.must_hit("finnes-ikke")
    assert "Nullresultater" in str(e.value)
    assert not c.armed


def test_nullresultat_avvises_for_arming():
    """Kjernen i regelen: expect_none uten arming er ikke et funn."""
    c = corpus()
    with pytest.raises(ControlNotArmed):
        c.expect_none("epsilon")


def test_nullresultat_godtas_etter_arming():
    c = corpus()
    c.must_hit("beta")
    assert c.expect_none("epsilon") == 0


def test_tomt_korpus_kan_ikke_armeres():
    """Den vanligste feilkilden: søket ser ingenting fordi korpuset er tomt."""
    tom = Corpus("tom", [])
    with pytest.raises(ControlMissed):
        tom.must_hit("hva som helst")
    with pytest.raises(ControlNotArmed):
        tom.expect_none("hva som helst")


def test_expect_none_feiler_naar_noe_finnes():
    c = corpus()
    c.must_hit("beta")
    with pytest.raises(AssertionError):
        c.expect_none("gamma")
