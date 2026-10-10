"""Fase 4 (ADDENDUM-26): referanselesingens fullføringsvilkår, recall med klyngefølsomhet, tilleggsmålet.
Uten Vault, uten modeller."""
import json

from gjenopptak.classify import fase3 as F3
from gjenopptak.classify import fase4 as F4


def test_oppdragene_er_fase3s_maler_med_bare_de_laaste_endringene():
    assert F4.OPPDRAG.replace(F4._SLUTT_NY, F4._SLUTT_GML) == F3.OPPDRAG
    assert "LEST TIL: S<nummer>" in F4.OPPDRAG
    assert F4.PRESISJON_OPPDRAG.replace('"id": "P4-001"', '"id": "P3-001"') == F3.PRESISJON_OPPDRAG


def test_et_verk_er_lest_bare_naar_svaret_bekrefter_siste_setning():
    assert F4.lest_til("ferdig.\nLEST TIL: S412") == 412
    assert F4.lest_til("LEST TIL: S10 … LEST TIL: S20") == 20 and F4.lest_til("ingen linje") is None
    ok = {"is_error": False, "treffil_finnes": True, "lest_til": 412}
    assert F4.ferdig_lest(ok, 412)
    assert not F4.ferdig_lest({**ok, "lest_til": 300}, 412)          # stoppet underveis
    assert not F4.ferdig_lest({**ok, "is_error": True}, 412)
    assert not F4.ferdig_lest({**ok, "treffil_finnes": False}, 412)


def _u(doc, a, b):
    return {"doc_id": doc, "start_index": a, "end_index": b, "kilde": "dommer"}


def test_recall_med_klyngefoelsomhet_tar_ut_verket_med_flest_treff():
    nøkkel = ([{"ref": "R01", "work_id": "W1", "setninger": [i, i + 1], "tvil": False, "gyldig_spenn": True}
               for i in range(0, 40, 4)]
              + [{"ref": "R02", "work_id": "W2", "setninger": [5, 6], "tvil": True, "gyldig_spenn": True},
                 {"ref": "R03", "work_id": "W3", "setninger": [1, 2], "tvil": False, "gyldig_spenn": True}])
    union = [_u("W1", i, i + 4) for i in range(0, 40, 4)] + [_u("W2", 4, 8)]
    dommer = {("W1", 0, 4): {"treff": True}, ("W2", 4, 8): {"treff": True}}
    rader, r = F4.recall(nøkkel, union, dommer)
    assert r["alle"]["beholdt"]["k"] == 11 and r["alle"]["beholdt"]["n"] == 12
    assert r["alle"]["bekreftet"]["k"] == 2
    kl = r["klynger"]
    assert kl["tatt_ut"] == ["W1"] and kl["flest_treff"] == 10 and kl["verk_med_treff"] == 3
    assert kl["uten_største"]["beholdt"]["n"] == 2 and kl["uten_største"]["beholdt"]["k"] == 1
    assert kl["snitt_per_verk"]["beholdt"] == round((1 + 1 + 0) / 3, 3)
    assert r["uten_tvil"]["beholdt"]["n"] == 11


def test_likt_antall_tar_ut_alle_verkene_med_flest():
    nøkkel = [{"ref": "R", "work_id": w, "setninger": [1], "tvil": False, "gyldig_spenn": True}
              for w in ("A", "A", "B", "B", "C")]
    _, r = F4.recall(nøkkel, [], {})
    assert r["klynger"]["tatt_ut"] == ["A", "B"] and r["klynger"]["uten_største"]["beholdt"]["n"] == 1


def test_tilleggsmaalet_regner_av_avklarte_og_sammenligner_uten_terskel():
    kl = ["H1"] * 3 + ["H7"] * 6 + ["H1/H7-uavklart"]
    t = F4.tillegg_loftbar(kl)
    assert t["løftbar_av_avklarte"]["k"] == 3 and t["løftbar_av_avklarte"]["n"] == 9
    assert t["uavklart_av_alle"]["k"] == 1 and t["terskel"] is None
    assert t["sammenligning"]["arkeologi_fase3"]["k"] == 101 and t["sammenligning"]["arkeologi_fase3"]["n"] == 628
    assert t["sammenligning"]["første_100_kandidatlista"]["n"] == 406
    assert (t["sammenligning"]["tekstvitenskap_første_runde"]["k"], t["sammenligning"]["tekstvitenskap_første_runde"]["n"]) == (3, 35)
