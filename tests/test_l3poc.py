"""L3-POC: ledetekst, materiale, tolkning og målinger. Ingen modell, ingen nettkall."""

import random
from pathlib import Path

import pytest

from gjenopptak.classify import l3poc as P

REPO = Path(__file__).resolve().parents[1]


def test_ankerne_hentes_ordrett_fra_addendum02():
    ank = P.anchors_from_addendum02((REPO / "ADDENDUM-02.md").read_text(encoding="utf-8"))
    titler = [t.split(" — ")[0] for t, _, _ in ank]
    assert titler == ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "N1", "N2", "N3"]
    assert all(len(a) == 2 for _, a, _ in ank)
    assert "«As manual review of all records was not feasible»" in ank[0][1][0]
    assert not any("10." in x.split("«")[0] for _, a, _ in ank for x in a)      # DOI-er er fjernet
    assert [bool(m) for _, _, m in ank][9:] == [True, False, True]              # merknadene til N1 og N3


def test_ledeteksten_har_alle_klasser_og_ingen_loftbarhet():
    s = P.build_system_prompt(REPO)
    for k in P.ALL_CLASSES:
        assert k in s
    assert "løftbar" not in s.lower() and "ja_med_forbehold" not in s
    assert s == P.build_system_prompt(REPO)                                     # deterministisk


def test_vinduet_rundt_treffsetningen_og_sentrert_ved_langt_spenn():
    assert P.window_for(10, {"start_index": 9, "end_index": 10}, 100) == (8, 12)
    assert P.window_for(10, {"start_index": 10, "end_index": 13}, 100) == (9, 13)
    assert P.window_for(1, {"start_index": 1, "end_index": 1}, 100) == (0, 3)
    with pytest.raises(ValueError):
        P.window_for(10, {"start_index": 10, "end_index": 16}, 100)


def test_negative_vinduer_er_deterministiske_og_overlapper_ikke():
    docs = {"A": [f"a{i}" for i in range(40)], "B": [f"b{i}" for i in range(40)]}
    blokk = {"A": [(10, 14)], "B": [(0, 4)]}
    n1 = P.draw_negatives(docs, blokk, 8, random.Random(P.MAALEFRO))
    n2 = P.draw_negatives(docs, blokk, 8, random.Random(P.MAALEFRO))
    assert n1 == n2 and len(n1) == 8
    for d, lo, hi in n1:
        alle = blokk[d] + [(a, b) for dd, a, b in n1 if dd == d and (a, b) != (lo, hi)]
        assert all(hi < a or b < lo for a, b in alle)
    with pytest.raises(ValueError):
        P.draw_negatives({"A": ["x"] * 5}, {"A": [(0, 4)]}, 1, random.Random(1))


def test_tolkningen_lar_klassen_avgjore():
    assert P.parse_response('{"begrunnelse": "x", "treff": true, "klasse": "H7"}') == P.Parsed("H7", True, False)
    assert P.parse_response('{"begrunnelse": "x", "treff": true, "klasse": "N3"}') == P.Parsed("N3", False, True)
    assert P.parse_response('{"treff": false, "klasse": "H9"}').treff is True
    assert P.parse_response('{"klasse": "H10"}').klasse == "UGYLDIG"
    assert P.parse_response("ikke json").klasse == "UGYLDIG"


def _r(i, fasit, klasse, **kw):
    return dict({"id": i, "fasit_klasse": fasit, "klasse": klasse, "treff": klasse in P.HIT_CLASSES}, **kw)


def test_malingene():
    rows = [_r("1", "H7", "H7"), _r("2", "H1", "H7"), _r("3", "H2", "INGEN"), _r("4", None, "H1"),
            _r("5", None, "INGEN"), _r("6", "H1/H7-uavklart", "H1/H7-uavklart")]
    m = P.metrics(rows)
    assert (m["tp"], m["fp"], m["fn"]) == (3, 1, 1)
    assert m["presisjon"] == 3 / 4 and m["recall"] == 3 / 4 and m["negative_dømt_treff"] == 1 / 2
    assert m["eksakt_klasse"] == 2 / 4 and m["klasse_h1h7_slått_sammen"] == 3 / 4
    assert m["andel_dømt_uavklart_av_alle"] == 1 / 6


def test_kappa_og_enighet():
    assert P.kappa(["a", "a", "b", "b"], ["a", "a", "b", "b"]) == 1.0
    assert P.kappa(["a", "b", "a", "b"], ["a", "a", "b", "b"]) == 0.0
    a = [{"treff": True, "klasse": "H7"}, {"treff": False, "klasse": "INGEN"}]
    b = [{"treff": True, "klasse": "H1"}, {"treff": False, "klasse": "N3"}]
    g = P.judge_agreement(a, b)
    assert g["treff_enighet"] == 1.0 and g["klasse_enighet"] == 0.5 and g["n_begge_treff"] == 1


def test_alvorlighet_og_verste_bommer():
    assert P.severity(None, "H1") == 1 and P.severity("H7", "H4") == 1
    assert P.severity("H7", "INGEN") == 2 and P.severity(None, "H7") == 3 and P.severity("H7", "H8") == 4
    assert P.severity("H7", "H7") is None and P.severity(None, "N3") is None
    rows = [_r("b", "H7", "INGEN"), _r("a", None, "H1"), _r("c", "H7", "H1"), _r("d", "H7", "H8")]
    assert [r["id"] for r in P.worst_misses(rows)] == ["c", "a", "b", "d"]


def test_variant_b_endrer_bare_ett_avsnitt():
    a = P.build_system_prompt(REPO)
    b = P.build_system_prompt_b(a, "eksempel sju", "eksempel en/to")
    avsnitt = b[b.index("## Skillet mellom H7 og H1/H2"):b.index("## Uavklart")]
    assert b.replace(avsnitt, "") == a
    assert "→ H7." in avsnitt and "H1 (lesning/koding i skala) eller H2 (lesbarhet)" in avsnitt
    assert avsnitt.count("Eksempel: «") == 2


def test_eksemplene_trekkes_etter_regelen_og_deterministisk():
    rows = [
        {"sett": 1, "doc_id": "A", "hit_index": 1, "klasse": "H7", "unit": "sentence", "grensetilfelle": False},
        {"sett": 1, "doc_id": "B", "hit_index": 2, "klasse": "H7", "unit": "sentence", "grensetilfelle": False},
        {"sett": 1, "doc_id": "B", "hit_index": 9, "klasse": "H2", "unit": "sentence", "grensetilfelle": False},
        {"sett": 2, "doc_id": "C", "hit_index": 3, "klasse": "H7", "unit": "passage", "grensetilfelle": False},
        {"sett": 2, "doc_id": "D", "hit_index": 4, "klasse": "H1", "unit": "sentence", "grensetilfelle": True},
    ]
    h7, h12 = P.select_examples(rows)
    assert h7["doc_id"] == "A"                      # B har to treff, C er passasje
    assert h12["klasse"] == "H2"                    # D er grensetilfelle
    assert P.select_examples(rows) == (h7, h12)


def test_sammenligningstallene():
    rows = [_r("1", "H7", "H1"), _r("2", None, "H4"), _r("3", "H2", "H2"), _r("4", None, "INGEN"), _r("5", "H7", "H7")]
    c = P.comparison_metrics(rows)
    assert c["falsk_løftbarhet_n"] == 2 and c["andel_dømt_H7"] == 1 / 5 and c["andel_dømt_INGEN"] == 1 / 5
    assert P.contains_example("a  b\nc d", ["b c"]) and not P.contains_example("a b", ["c"])
