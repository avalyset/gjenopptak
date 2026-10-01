"""ADDENDUM-25 §5–§7-tallene som ``fase3 maal`` ikke regner: klasser, tetthet, forbruk, modell fra utskrift."""
import json

from gjenopptak.classify import fase3_rapport as R


def test_klasser_følger_oppslagstabellen():
    treff = [{"klasse": k, "tvil": t} for k, t in
             [("H7", False), ("H7", True), ("H2", False), ("H1/H7-uavklart", True), ("H9", False)]]
    k = R.klasser(treff)
    assert k["fordeling"] == {"H7": 2, "H2": 1, "H1/H7-uavklart": 1, "H9": 1}
    # ADDENDUM-05 § 4: løftbar av de avklarte (4), uavklart av alle treff (5)
    assert (k["løftbar_av_avklarte"]["k"], k["løftbar_av_avklarte"]["n"]) == (1, 4)
    assert (k["uavklart_av_alle"]["k"], k["uavklart_av_alle"]["n"]) == (1, 5)
    assert (k["H7"]["k"], k["ikke_løftbar_av_avklarte"]["k"]) == (2, 3)
    assert k["format_liftable"].startswith("løftbar 1/4 av avklarte")
    assert k["tvil_blant_treff"]["k"] == 2


def test_tettheten_fører_begge_nevnerne():
    t = R.tetthet(**R.FØRSTE_100["arkeologi"])
    assert t["treff_per_verk"] == 10.96
    assert t["treff_per_1000_korpus_tekstbiter"] == 40.6       # 274 / 6 741
    assert t["treff_per_1000_dømte"] == 276.8                  # 274 / 990


def test_leserforbruket_samles_fra_alle_kjøringer_uten_dobbelttelling(tmp_path, monkeypatch):
    ut, kd = tmp_path / "fase3", tmp_path / "kd"
    (kd / "fullforing" / "okt-2-rest1").mkdir(parents=True)
    ut.mkdir()
    bruk = {"usage": {"input_tokens": 1, "output_tokens": 10}, "minutter": 5.0}
    første = {"ledd": {"les": {"tid": "T1", "økter": [{"okt": 1, "status": "ferdig", "n": 3},
                                                     {"okt": 2, "status": "AVVIK", "dømt": 1, "ventet": 3}],
                               "forbruk": [{**bruk, "okt": 1}, {**bruk, "okt": 2}]}}}
    siste = {"ledd": {"les": {"tid": "T2", "økter": [{"okt": 1, "status": "alt ferdig", "n": 3},
                                                    {"okt": 2, "status": "alt ferdig", "n": 3}], "forbruk": []}}}
    (ut / "tilstand-foer-gjenopptak-A.json").write_text(json.dumps(første))
    (ut / "tilstand-foer-gjenopptak-B.json").write_text(json.dumps(siste))    # kopi av siste: telles én gang
    (kd / "tilstand.json").write_text(json.dumps(siste))
    (kd / "fullforing" / "okt-2-rest1" / "logg.json").write_text(json.dumps(
        {"okt": 2, "rest": 1, "føyd_til": 2, "bruk": bruk}))
    monkeypatch.setattr(R, "FLYTTET", tmp_path / "finnes-ikke.json")
    økter = R.leserøkter(ut, kd)
    assert [(ø["okt"], ø["dømt"]) for ø in økter] == [(1, 3), (2, 1), ("2-rest1", 2)]
    assert R._sum(økter)["output_tokens"] == 30


def test_modell_leses_per_økt_fra_utskriften(tmp_path):
    rader = [{"type": "queue-operation", "timestamp": "2026-09-30T08:08:55Z",
              "content": "# Oppdrag: uavhengig koding, kjøring fase3-kjede, økt 4 av 12\n"},
             {"type": "assistant", "timestamp": "2026-09-30T08:09:00Z", "message": {"model": "claude-opus-5"}},
             {"type": "assistant", "timestamp": "2026-09-30T08:10:00Z", "message": {"model": "claude-opus-5"}}]
    (tmp_path / "a.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rader))
    rest = [{**rader[0], "content": "# Oppdrag: uavhengig koding, kjøring fase3-kjede, økt 3 av 12\n"
                                    "`data/kjede/fase3-kjede/fullforing/okt-3-rest1/blind.jsonl`"},
            {"type": "assistant", "timestamp": "2026-09-30T09:00:00Z", "message": {"model": "<synthetic>"}}]
    (tmp_path / "b.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rest))
    u = R.modell_fra_utskrifter(tmp_path)
    assert [(x["økt"], x["modeller"]) for x in u] == [("4", {"claude-opus-5": 2}), ("3-rest1", {"<synthetic>": 1})]


def test_presisjonen_brytes_ned_etter_leserens_tvil_ikke_instansens(tmp_path):
    pd = tmp_path / "presisjon"
    pd.mkdir()
    nøkkel = [{"id": f"P3-{i:03d}", "leser_id": f"L{i}"} for i in range(4)]
    vs = [{"id": "P3-000", "treff": True, "klasse": "H7", "tvil": True},     # instansen i tvil, leseren ikke
          {"id": "P3-001", "treff": False, "klasse": "N3", "tvil": False},
          {"id": "P3-002", "treff": True, "klasse": "H2", "tvil": False},
          {"id": "P3-003", "treff": True, "klasse": "H7", "tvil": False}]
    for navn, rader in (("nokkel-presisjon.jsonl", nøkkel), ("verdikter-presisjon.jsonl", vs)):
        (pd / navn).write_text("".join(json.dumps(r) + "\n" for r in rader))
    leser = [{"id": "L0", "klasse": "H7", "tvil": False}, {"id": "L1", "klasse": "H7", "tvil": True},
             {"id": "L2", "klasse": "H7", "tvil": True}, {"id": "L3", "klasse": "H7", "tvil": False}]
    f = R.presisjon_følsomhet(tmp_path, leser)
    assert (f["leser_tvil_false"]["k"], f["leser_tvil_false"]["n"]) == (2, 2)
    assert (f["leser_tvil_true"]["k"], f["leser_tvil_true"]["n"]) == (1, 2)
    assert (f["samme_klasse_blant_bekreftede"]["k"], f["samme_klasse_blant_bekreftede"]["n"]) == (2, 3)
    assert f["avviste_klasser"] == {"N3": 1} and f["instansens_tvil"] == 1


def test_recall_klyngene_tar_ut_det_største_verket(tmp_path):
    ut = tmp_path
    rader = ([{"ref": "R1", "beholdt": True, "bekreftet": True}] * 6
             + [{"ref": "R2", "beholdt": False, "bekreftet": False}, {"ref": "R2", "beholdt": True, "bekreftet": False}])
    (ut / "maaling-fase3.json").write_text(json.dumps({"rader": rader}))
    k = R.recall_klynger(ut)
    assert k["største_verk"] == {"ref": "R1", "treff": 6, "beholdt": 6, "bekreftet": 6}
    assert (k["uten_største"]["beholdt"]["k"], k["uten_største"]["beholdt"]["n"]) == (1, 2)
    assert k["snitt_per_verk"] == {"beholdt": 0.75, "bekreftet": 0.5}
