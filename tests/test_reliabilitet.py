"""κ og rå enighet: kjente tilfeller fra lærebøkene."""

import pytest

from gjenopptak.classify import reliabilitet as R


def test_full_enighet_gir_kappa_1():
    a = ["ja", "nei", "ja", "nei", "ja"]
    assert R.ra_enighet(a, a) == 1.0
    assert R.cohen_kappa(a, a) == 1.0


def test_tilfeldig_enighet_gir_kappa_0():
    # begge koder 50/50, men uavhengig: rå enighet 0,5, κ ≈ 0
    a = ["ja", "ja", "nei", "nei"]
    b = ["ja", "nei", "ja", "nei"]
    assert R.ra_enighet(a, b) == 0.5
    assert abs(R.cohen_kappa(a, b)) < 1e-12


def test_skjevt_materiale_straffer_kappa():
    """98 av 100 er «nei» hos begge, og de er uenige om de to siste."""
    a = ["nei"] * 98 + ["ja", "ja"]
    b = ["nei"] * 98 + ["ja", "nei"]
    assert R.ra_enighet(a, b) == 0.99
    assert R.cohen_kappa(a, b) < 0.7, "høy rå enighet på skjevt materiale gir lavere κ"


def test_bootstrapintervallet_omslutter_punktestimatet():
    a = ["nei"] * 80 + ["ja"] * 20
    b = ["nei"] * 75 + ["ja"] * 5 + ["ja"] * 15 + ["nei"] * 5
    k = R.cohen_kappa(a, b)
    lo, hi = R.kappa_bootstrap(a, b, n_rep=2000)
    assert lo <= k <= hi


def test_sammenslaaing_av_uavklarte():
    assert R.slaa_sammen("H1/H7-uavklart") == R.slaa_sammen("H7") == "H1~H7"
    assert R.slaa_sammen("H8") == "H8"
    assert R.slaa_sammen(None) is None
