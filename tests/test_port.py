"""Porten: passasjeuttrekk uten markørfiltrering, og M1/M2. Ingen modell, ingen nettkall."""

from collections import Counter
import pytest

from gjenopptak.classify import port as PO


def _rader(n, doc="D"):
    return [{"doc_id": doc, "sentence_index": i, "text": f"s{i}",
             "section_raw": "Intro" if i < 5 else "Metode", "section_label_provenance": "source"} for i in range(n)]


def test_passasjene_dekker_hele_teksten_og_bevarer_paringen():
    for n in (5, 7, 22, 23, 100):
        ps = PO.passasjer(_rader(n), "felt", stride=3)
        assert PO.dekker_alle_setninger(ps, n), n
        par = [(i, i + 2) for i in range(n - 2)]
        assert all(any(p.start_index <= a and b <= p.end_index for p in ps) for a, b in par), n


def test_korte_dokumenter_gir_én_passasje():
    ps = PO.passasjer(_rader(3), "felt")
    assert len(ps) == 1 and ps[0].start_index == 0 and ps[0].end_index == 2
    assert PO.passasjer([], "felt") == []


def test_seksjon_og_provenance_følger_sentersetningen():
    ps = PO.passasjer(_rader(12), "felt", stride=3)
    assert [p.section_raw for p in ps][:2] == ["Intro", "Metode"]
    assert all(p.section_label_provenance == "source" for p in ps)
    assert ps[1].seksjoner_i_vindu == ("Intro", "Metode")     # vinduet spenner over skiftet


def test_ingen_markorfiltrering():
    """Alle passasjer går videre: uttrekket har ingen markør og ingen terskel."""
    rader = _rader(20)
    assert len(PO.passasjer(rader, "felt", stride=3)) == len(PO.passasjer(
        [dict(r, text="could not because") for r in rader], "felt", stride=3))


def test_m1_streng_og_passasje():
    verk = [{"work_id": "A"}, {"work_id": "B"}, {"work_id": "C"}]
    treff = {"A": [{"klasse": "H7", "samme_setning": True}],
             "B": [{"klasse": "H1", "samme_setning": False}]}
    assert PO.m1(verk, treff, streng=False) == {"n_verk": 3, "verk_med_treff": 2, "M1": 2 / 3}
    assert PO.m1(verk, treff, streng=True) == {"n_verk": 3, "verk_med_treff": 1, "M1": 1 / 3}


def test_m2_teller_usikre_for_seg():
    rader = [{"bedømbar": "ja"}, {"bedømbar": "nei"}, {"bedømbar": "usikker"}, {"bedømbar": "ja"}]
    m = PO.m2(rader)
    assert m["M2"] == 0.5 and m["M2_uten_usikre"] == 2 / 3 and m["usikker"] == 1
    assert PO.m2([])["M2"] is None
    assert PO.m2([{"bedømbar": "nei", "bedømbar_endelig": "ja"}])["M2"] == 1.0   # overprøving vinner


def test_treff_per_verk_teller_bare_hindringsklasser():
    d = [{"doc_id": "A", "klasse": "H7"}, {"doc_id": "A", "klasse": "INGEN"},
         {"doc_id": "B", "klasse": "N3"}, {"doc_id": "A", "klasse": "H1/H7-uavklart"}]
    t = PO.treff_per_verk(d)
    assert set(t) == {"A"} and len(t["A"]) == 2


def test_batchsignatur_etter_adr0008():
    """ADR-0003 krever keep_alive=0; ADR-0008 åpner for batch, men bare merket som batch."""
    from gjenopptak.classify import judge as J
    J.check_signature("local:m", {f: 1 for f in J.SIGNATURE_FIELDS} | {"keep_alive": 0})
    J.check_signature("local:m", {f: 1 for f in J.SIGNATURE_FIELDS} | {"keep_alive": "30m", "batch": True})
    with pytest.raises(J.JudgeError):
        J.check_signature("local:m", {f: 1 for f in J.SIGNATURE_FIELDS} | {"keep_alive": "30m"})
    with pytest.raises(J.JudgeError):
        J.check_signature("local:m", {f: 1 for f in J.SIGNATURE_FIELDS} | {"keep_alive": 0, "batch": True})


def test_dommeren_sender_keep_alive_som_bedt_om(monkeypatch):
    import json as json_mod

    import httpx

    from gjenopptak.classify import l3poc_run as R
    sendt = {}

    def transport(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/version":
            return httpx.Response(200, json={"version": "0.0.0"})
        if request.url.path == "/api/show":
            return httpx.Response(200, json={"details": {"format": "gguf", "quantization_level": "Q",
                                                         "family": "f", "parameter_size": "9B"}})
        sendt.update(json_mod.loads(request.content))
        return httpx.Response(200, json={"message": {"content": '{"begrunnelse":"x","treff":false,"klasse":"INGEN"}'},
                                         "prompt_eval_count": 10, "eval_count": 5, "total_duration": 1,
                                         "load_duration": 1, "done_reason": "stop"})

    ekte = httpx.Client
    monkeypatch.setattr(R.httpx, "Client", lambda **kw: ekte(transport=httpx.MockTransport(transport)))
    monkeypatch.setattr(R.Lokal, "_digest", lambda self: "sha256:" + "a" * 64)
    monkeypatch.setattr("gjenopptak.classify.l3poc_run.sha256_fil", lambda p: "a" * 64)
    d = R.Lokal(keep_alive="30m")
    svar = d("system", "bruker")
    assert sendt["keep_alive"] == "30m"
    assert svar["signatur"]["keep_alive"] == "30m" and svar["signatur"]["batch"] is True


def test_presisjon_og_falske_klasser():
    fasit = [
        {"utvalgstype": "treff", "felt": "a", "dømt_klasse": "H7", "ekte_treff": True},
        {"utvalgstype": "treff", "felt": "a", "dømt_klasse": "H7", "ekte_treff": False},
        {"utvalgstype": "treff", "felt": "b", "dømt_klasse": "H8", "ekte_treff": False},
        {"utvalgstype": "treff", "felt": "b", "dømt_klasse": "H1", "ekte_treff": True},
        {"utvalgstype": "ingen", "felt": "a", "dømt_klasse": "INGEN", "ekte_treff": True},
        {"utvalgstype": "ingen", "felt": "b", "dømt_klasse": "INGEN", "ekte_treff": False},
    ]
    p = PO.presisjon(fasit)
    assert p["presisjon"] == 0.5 and p["per_felt"]["a"]["presisjon"] == 0.5
    assert p["andel_falske_H7_H8"] == 1.0 and p["falske_dømt_H7_eller_H8"] == 2
    assert p["bomrate_blant_ingen"] == 0.5 and p["n_ingen_lest"] == 2


def test_m1_varianter_og_korrigering():
    verk = [{"work_id": "A"}, {"work_id": "B"}, {"work_id": "C"}]
    treff = {"A": [{"klasse": "H7"}, {"klasse": "H7"}, {"klasse": "H1"}], "B": [{"klasse": "H7"}]}
    pres = {"H7": {"n": 10, "presisjon": 0.5}, "H1": {"n": 2, "presisjon": 1.0}}
    m = PO.m1_varianter(verk, treff, pres, 0.4)
    assert m["M1_minst_1"]["M1"] == 2 / 3 and m["M1_minst_2"]["M1"] == 1 / 3 and m["M1_minst_3"]["M1"] == 1 / 3
    # A: 1−0,5·0,5·0,6 = 0,85 (H1 har under fem leste, så samlet presisjon 0,4 brukes); B: 0,5
    assert round(m["M1_korrigert"]["M1"], 4) == round((0.85 + 0.5) / 3, 4)


def test_ankere_trekkes_stratifisert_og_deterministisk():
    a = PO.ankere()
    assert len(a) == 20
    treff = [x for x in a if x["utvalgstype"] == "anker-treff"]
    ikke = [x for x in a if x["utvalgstype"] == "anker-ikke-treff"]
    assert len(treff) == 12 and len(ikke) == 8
    assert all(x["fasit_klasse"] for x in treff)
    assert {x["lag"] for x in a} == {"humaniora", "biomed"}
    assert Counter(x["lag"] for x in ikke) == Counter({"humaniora": 4, "biomed": 4})
    assert all(x["tekst"].strip() for x in a)
    assert [x["kilde"] for x in a] == [x["kilde"] for x in PO.ankere()]
    # ingen notert rad med spenn større enn én passasje
    assert all(x["end_index"] - x["start_index"] <= 2 * PO.WINDOW for x in ikke)


def test_ankere_holdes_utenfor_presisjonen():
    fasit = [
        {"utvalgstype": "treff", "felt": "a", "dømt_klasse": "H7", "ekte_treff": True},
        {"utvalgstype": "ingen", "felt": "a", "dømt_klasse": "INGEN", "ekte_treff": False},
        {"utvalgstype": "anker-treff", "felt": None, "dømt_klasse": None, "ekte_treff": False,
         "fasit_klasse": "H2", "min_klasse": None, "kilde": "L3-POC X"},
        {"utvalgstype": "anker-ikke-treff", "felt": None, "dømt_klasse": None, "ekte_treff": True,
         "fasit_klasse": None, "kilde": "notert ikke-treff sett 2 (1–1)"},
    ]
    p = PO.presisjon(fasit)
    assert p["n_treff_lest"] == 1 and p["n_ingen_lest"] == 1 and p["presisjon"] == 1.0
    m = PO.ankermål(fasit)
    assert m["andel_kjente_treff_lest_som_treff"] == 0.0
    assert m["andel_kjente_ikke_treff_lest_som_ikke_treff"] == 0.0
    assert m["eksakt_klasseenighet_med_opprinnelig_fasit"] == 0.0
    assert m["klasseavvik"] == [{"kilde": "L3-POC X", "fasit": "H2", "lest_nå": None}]


def test_lengdeakse_bryter_ikke_stratumkvotene():
    # tre felt á 40 rader, halvparten korte og halvparten lange
    rader = [{"doc_id": f"D{f}", "start_index": i, "felt": f,
              "tekst": "x" * (200 if i < 20 else 900)}
             for f in ("a", "b", "c") for i in range(40)]
    ank = [{"tekst": "x" * n} for n in (700, 750, 800, 850, 900, 950, 1000, 1050)]
    grenser = PO.lengdegrenser(ank)
    mål = PO.lengdemål(ank, grenser)
    kv = lambda r: PO.kvartil(len(r["tekst"]), grenser)
    uten = PO.stratifisert(rader, 30, lambda r: r["felt"])
    med = PO.stratifisert(rader, 30, lambda r: r["felt"], sekundær=kv, mål=mål)
    assert len(med) == 30
    # feltkvotene er identiske med og uten lengdeaksen
    assert Counter(r["felt"] for r in med) == Counter(r["felt"] for r in uten)
    # men lengdefordelingen har flyttet seg mot ankernes; bøtte 1 er tom i materialet, så
    # kravet derfra går til nærmeste bøtte med rader (den lange)
    lange = sum(1 for r in med if len(r["tekst"]) == 900)
    assert lange > sum(1 for r in uten if len(r["tekst"]) == 900) and lange == 21


def test_kvartil_og_maaltetthet():
    ank = [{"tekst": "x" * n} for n in (100, 200, 300, 400)]
    g = PO.lengdegrenser(ank)
    assert PO.kvartil(50, g) == 0 and PO.kvartil(1000, g) == 3
    assert abs(sum(PO.lengdemål(ank, g).values()) - 1.0) < 1e-9


def test_fordel_kappes_av_tilgang():
    bøtter = {0: [1] * 10, 1: [1] * 1, 2: [1] * 10, 3: [1] * 10}
    a = PO._fordel(8, bøtter, {b: 0.25 for b in range(4)})
    assert sum(a.values()) == 8 and a[1] == 1  # bøtte 1 har bare én rad; resten fordeles videre


def test_feltgulv_loefter_tynt_felt_og_fordeler_resten():
    rader = ([{"felt": "a"}] * 900 + [{"felt": "b"}] * 700 + [{"felt": "c"}] * 400
             + [{"felt": "tekstvitenskap"}] * 67)
    k = PO.feltkvoter(rader, 150, {"tekstvitenskap": 25})
    assert k["tekstvitenskap"] == 25 and sum(k.values()) == 150
    # de andre er proporsjonale seg imellom
    assert k["a"] > k["b"] > k["c"]
    # har feltet mindre enn gulvet, tas alt det har
    k2 = PO.feltkvoter([{"felt": "tekstvitenskap"}] * 10 + [{"felt": "a"}] * 100, 150,
                       {"tekstvitenskap": 25})
    assert k2["tekstvitenskap"] == 10


def test_recall_rapporteres_tredelt_og_vektet():
    fasit = [{"utvalgstype": "treff", "felt": "a", "dømt_klasse": "H7", "ekte_treff": True}]
    fasit += [{"utvalgstype": "ingen", "felt": "a", "dømt_klasse": "INGEN",
               "ekte_treff": i < 1} for i in range(10)]          # 10 % bom
    fasit += [{"utvalgstype": "n3", "felt": "a", "dømt_klasse": "N3",
               "ekte_treff": i < 3} for i in range(10)]          # 30 % bom
    fasit += [{"utvalgstype": "n1n2", "felt": "a", "dømt_klasse": "N1", "ekte_treff": False}] * 4
    fasit += [{"utvalgstype": "n1n2", "felt": "a", "dømt_klasse": "N2", "ekte_treff": True}]
    p = PO.presisjon(fasit, {"INGEN": 1500, "N3": 500, "N1": 40, "N2": 10})
    it = p["ikke_treff"]
    assert it["INGEN"]["bomrate"] == 0.1 and it["N3"]["bomrate"] == 0.3
    assert it["N1"]["bomrate_rå"] == 0.0 and it["N2"]["bomrate_rå"] == 1.0
    assert "bomrate" not in it["N1"]  # rått tall, ikke ekstrapolert
    v = it["vektet"]
    assert abs(v["bomrate"] - (1500 * 0.1 + 500 * 0.3 + 40 * 0 + 10 * 1.0) / 2050) < 1e-9
    assert v["andel_av_ikke_treffene_dekket"] == 1.0
    # presisjonstallet er urørt av ikke-treffene
    assert p["presisjon"] == 1.0 and p["n_treff_lest"] == 1
