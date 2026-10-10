"""Reanalysen etter fagfellevurderingen: enighetsmålene og dedupliseringen. Uten Vault."""
from gjenopptak.classify import reanalyse_fagfelle as R


def test_enighet_gir_kappa_pabak_og_ac1():
    a = [True] * 10 + [False] * 90
    b = [True] * 8 + [False] * 2 + [True] * 2 + [False] * 88
    e = R.enighet(a, b)
    assert e["rå_enighet"] == 0.96 and e["pabak"] == 0.92
    pe = 0.1 * 0.1 + 0.9 * 0.9
    assert abs(e["kappa"] - round((0.96 - pe) / (1 - pe), 4)) < 1e-9
    pi = 0.1
    assert abs(e["gwet_ac1"] - round((0.96 - 2 * pi * (1 - pi)) / (1 - 2 * pi * (1 - pi)), 4)) < 1e-9


def _r(doc, a, b, k):
    return {"doc_id": doc, "passage_span": {"start_index": a, "end_index": b}, "obstacle_class": k}


def test_overlappende_spenn_i_samme_verk_er_en_erklaering():
    rader = [_r("W1", 0, 4, "H7"), _r("W1", 3, 7, "H7"), _r("W1", 6, 10, "H1"),   # én kjede: 0–10
             _r("W1", 20, 24, "H1"), _r("W2", 0, 4, "H7"), _r("W2", 2, 6, "H1")]  # W2: blandet (1–1)
    d = R.duplikater(rader, "test")
    assert d["unike_erklæringer"] == 3 and d["rader_som_deler_setning"] == 5
    assert d["blandet_klasse"] == 1 and d["største_komponent"] == 3
    assert d["H7_av_unike"]["n"] == 2 and d["H7_av_unike"]["k"] == 1
