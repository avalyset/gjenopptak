"""ADDENDUM-28: rekkefølgen er sperrelisten, vinduet avgjør partiets gyldighet, hver dom bærer signatur.

Syntetisk materiale og falsk modell. Ingen test åpner blindfilen, koderne eller ollama.
"""
import hashlib
import json

import pytest

from gjenopptak.classify import reanalyse_fagfelle as rf
from gjenopptak.classify import tredje_koder as tk
from gjenopptak.kjede.leser import LokalLeser, partimelding


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _dom(i, treff):
    return {"id": i, "ekte_treff": treff, "min_klasse": "H7" if treff else "INGEN",
            "min_bedømbar": True if treff else None, "tvil": False, "begrunnelse": "x"}


@pytest.fixture
def rigg(tmp_path, monkeypatch):
    """Tolv passasjer i fire verk på et liksom-Vault. Koderfilene skrives ikke før testen ber om det."""
    v = tmp_path / "vault"
    (v / "p").mkdir(parents=True)
    ids = [f"PS-{i:03d}" for i in range(1, 13)]
    blind = v / "p" / "blind.jsonl"
    blind.write_text("".join(json.dumps({"id": i, "tekst": f"tekst {i} " * (3 if i == "PS-007" else 1)}) + "\n"
                             for i in ids), encoding="utf-8")
    regler = v / "p" / "regler.md"
    regler.write_text("REGEL\n", encoding="utf-8")
    instruks = tmp_path / "instruks.txt"
    instruks.write_text("INSTRUKS", encoding="utf-8")
    vekt = tmp_path / "vekt.bin"
    vekt.write_bytes(b"vekt")
    monkeypatch.setattr(tk, "require_vault", lambda: v)
    monkeypatch.setattr(tk, "REPO", tmp_path)
    monkeypatch.setattr(tk, "_vekt_blob", lambda digest: vekt)
    monkeypatch.setattr(tk, "_ollama", lambda leser: {"ollama_versjon": "test"})
    monkeypatch.setattr(tk, "B", 200)
    monkeypatch.setattr(rf, "B", 200)
    for nøkkel, verdi in {"vekt_sha256": _sha(vekt), "instruks": "instruks.txt", "instruks_sha256": _sha(instruks),
                          "regelfil": "p/regler.md", "regelfil_sha256": _sha(regler),
                          "blindfil": "p/blind.jsonl", "blindfil_sha256": _sha(blind),
                          "koder1": "p/k1.jsonl", "koder2": "p/k2.jsonl", "utdir": "ut"}.items():
        monkeypatch.setitem(tk.OPPSETT, nøkkel, verdi)

    tilstand = {"kall": [], "treff": {"PS-001", "PS-002", "PS-006", "PS-011"}, "inn": 100, "ut": 50,
                "done_reason": "stop", "dropp": set()}

    def _kall(self, system, bruker):
        tilstand["kall"].append((system, bruker))
        i_partiet = [l[4:] for l in bruker.splitlines() if l.startswith("### ")]
        dommer = [_dom(i, i in tilstand["treff"]) for i in i_partiet if i not in tilstand["dropp"]]
        return {"message": {"content": json.dumps({"dommer": dommer})}, "done_reason": tilstand["done_reason"],
                "prompt_eval_count": tilstand["inn"], "eval_count": tilstand["ut"]}
    monkeypatch.setattr(LokalLeser, "_kall", _kall)

    def skriv_kodere(k1_treff, k2_treff):
        (v / "p" / "k1.jsonl").write_text("".join(json.dumps(
            {"id": i, "ekte_treff": i in k1_treff, "doc_id": f"W{(n // 3) + 1}",
             "utvalgstype": "treff" if n < 6 else "ingen"}) + "\n" for n, i in enumerate(ids)), encoding="utf-8")
        (v / "p" / "k2.jsonl").write_text("".join(json.dumps(
            {"id": i, "ekte_treff": i in k2_treff}) + "\n" for i in ids), encoding="utf-8")
        monkeypatch.setitem(tk.OPPSETT, "koder1_sha256", _sha(v / "p" / "k1.jsonl"))
        monkeypatch.setitem(tk.OPPSETT, "koder2_sha256", _sha(v / "p" / "k2.jsonl"))
    return v, ids, tilstand, skriv_kodere


def test_oppsettet_er_det_addendumet_laaser():
    o = tk.OPPSETT
    assert (o["modell"], o["parti"], o["num_ctx"], o["temperatur"], o["frø"], o["keep_alive"]) == \
        ("gemma2:9b", 5, 8192, 0, 734248, 0)
    assert o["vekt_sha256"].startswith("ff1d1fc7") and o["blindfil_sha256"].startswith("15ce72a7")
    assert o["koder1"] in tk.SPERRET and o["koder2"] in tk.SPERRET
    assert o["blindfil"] not in tk.SPERRET and o["regelfil"] not in tk.SPERRET


def test_vinduet_rommer_ledetekst_og_svar():
    assert tk.vindusbrudd({"prompt_eval_count": 6000, "eval_count": 2191, "done_reason": "stop"}) == []
    assert tk.vindusbrudd({"prompt_eval_count": 6000, "eval_count": 2192, "done_reason": "stop"})   # sum = num_ctx
    assert tk.vindusbrudd({"prompt_eval_count": 100, "eval_count": 2048, "done_reason": "length"})
    assert tk.vindusbrudd({"prompt_eval_count": 100, "eval_count": 5, "done_reason": "stop", "parsefeil": True})
    assert tk.vindusbrudd({"done_reason": "stop"})                                                   # tokentall mangler


def test_kanari_stoerste_parti_med_setningen_sist(rigg):
    v, ids, tilstand, _ = rigg
    assert tk.kanari() == 0
    k = json.loads((v / "ut" / "kanari.json").read_text())
    assert k["bestått"] and k["kanari_sist_i_vinduet"] and "PS-007" in k["parti_ids"]
    system, bruker = tilstand["kall"][0]
    assert bruker.rstrip().endswith(tk.OPPSETT["kanari_tekst"]) and system.endswith("# REGLENE\n\nREGEL\n")
    assert k["signatur"]["bruker_sha256"] == hashlib.sha256(bruker.encode()).hexdigest()
    assert k["signatur"]["system_sha256"] == hashlib.sha256(system.encode()).hexdigest()


def test_kanari_faller_naar_vinduet_er_fullt(rigg):
    v, _, tilstand, _ = rigg
    tilstand["inn"] = tk.OPPSETT["num_ctx"] - 50
    assert tk.kanari() == 2
    assert not json.loads((v / "ut" / "kanari.json").read_text())["bestått"]
    with pytest.raises(SystemExit, match="kanarien"):
        tk.kjør()


def test_kjoer_aapner_ingen_koderfil_og_signerer_hver_dom(rigg):
    v, ids, tilstand, _ = rigg
    tk.kanari()
    assert not (v / "p" / "k1.jsonl").exists() and not (v / "p" / "k2.jsonl").exists()   # finnes ikke: kan ikke leses
    assert tk.kjør() == 0
    rader = [json.loads(l) for l in (v / "ut" / "dommer.jsonl").read_text().splitlines()]
    assert [r["id"] for r in rader] == ids and all(r["gyldig"] for r in rader)
    s = rader[6]["signatur"]
    assert s["modell"] == "gemma2:9b" and s["parti"] == 2 and s["partier"] == 3 and "PS-007" in s["parti_ids"]
    assert s["num_ctx"] == 8192 and s["temperatur"] == 0 and s["frø"] == 734248 and s["keep_alive"] == 0
    for felt in ("vekt_sha256", "instruks_sha256", "regelfil_sha256", "blindfil_sha256", "kode_sha256",
                 "system_sha256", "bruker_sha256", "råsvar_sha256", "ollama_versjon"):
        assert s[felt], felt
    parti2 = [{"id": i, "tekst": f"tekst {i} " * (3 if i == "PS-007" else 1)} for i in ids[5:10]]
    assert s["bruker_sha256"] == hashlib.sha256(partimelding(parti2, 2, 3).encode()).hexdigest()
    segl = json.loads((v / "ut" / "SEGL.json").read_text())
    assert segl["sha256"] == _sha(v / "ut" / "dommer.jsonl") and segl["gyldige"] == 12
    with pytest.raises(SystemExit, match="forseglet"):
        tk.kjør()                                                                         # ingen omkjøring


def test_fullt_vindu_gjoer_hele_partiet_ugyldig_og_ingenting_fylles_ut(rigg):
    v, ids, tilstand, skriv_kodere = rigg
    tk.kanari()
    tilstand["dropp"] = {"PS-012"}                      # modellen hopper over én id i siste parti
    kall = LokalLeser._kall

    def fullt_i_parti_1(self, system, bruker):
        svar = kall(self, system, bruker)
        if "### PS-001" in bruker:
            svar["prompt_eval_count"] = tk.OPPSETT["num_ctx"]
        return svar
    LokalLeser._kall = fullt_i_parti_1
    try:
        tk.kjør()
    finally:
        LokalLeser._kall = kall
    rader = {r["id"]: r for r in map(json.loads, (v / "ut" / "dommer.jsonl").read_text().splitlines())}
    assert [i for i in ids if not rader[i]["gyldig"]] == ids[:5] + ["PS-012"]
    assert rader["PS-001"]["dom"] is None and rader["PS-001"]["dom_forkastet"]["ekte_treff"] is True
    assert "vinduet fullt" in rader["PS-003"]["ugyldig_grunn"] and "ingen gyldig dom" in rader["PS-012"]["ugyldig_grunn"]
    skriv_kodere({"PS-001", "PS-006"}, {"PS-006"})
    assert tk.mål() == 0
    m = json.loads((v / "ut" / "maaling.json").read_text())
    assert m["gyldige"] == 6 and m["utfall"]["n"] == 6                      # delmengden er de gyldige
    assert m["utfall"]["koder1_mot_koder2"]["n"] == 6                       # alle tre på samme delmengde
    assert m["følsomhet_ugyldige"]["alle_treff"]["gemma2_mot_koder1"]["n"] == 12


def test_maal_nekter_foer_segl_og_ved_brutt_segl(rigg):
    v, _, _, skriv_kodere = rigg
    skriv_kodere(set(), set())
    with pytest.raises(SystemExit, match="ikke forseglet"):
        tk.mål()
    tk.kanari()
    tk.kjør()
    with (v / "ut" / "dommer.jsonl").open("a") as fh:
        fh.write("\n")
    with pytest.raises(SystemExit, match="seglet"):
        tk.mål()


def test_maal_regner_de_tre_kappaene_paa_samme_delmengde(rigg, monkeypatch):
    v, ids, tilstand, skriv_kodere = rigg
    tk.kanari()
    tk.kjør()
    k1 = {"PS-001", "PS-002", "PS-006", "PS-010"}       # gemma2: 001, 002, 006, 011
    k2 = {"PS-001", "PS-002", "PS-006"}
    skriv_kodere(k1, k2)
    monkeypatch.setitem(tk.OPPSETT, "kontroll_kappa_k1_k2_320", 0.8)
    assert tk.mål() == 0
    m = json.loads((v / "ut" / "maaling.json").read_text())
    u = m["utfall"]
    # g mot k1: 10 av 12 enige, pe = (4/12)(4/12) + (8/12)(8/12) = 5/9 → κ = (10/12 − 5/9)/(4/9) = 0,625
    assert u["gemma2_mot_koder1"]["kappa"] == 0.625 and u["gemma2_mot_koder1"]["verk"] == 4
    # k1 mot k2: 11 av 12, pe = (4/12)(3/12) + (8/12)(9/12) = 7/12 → κ = 0,8
    assert u["koder1_mot_koder2"]["kappa"] == 0.8
    assert u["differanse_k1k2_minus_gemma2k1"]["punkt"] == 0.175
    for par in ("gemma2_mot_koder1", "gemma2_mot_koder2", "koder1_mot_koder2"):
        lo, hi = u[par]["klynge_bootstrap95"]
        assert lo <= u[par]["kappa"] <= hi and {"rå_enighet", "pabak", "gwet_ac1"} <= set(u[par])
    assert m["kontroll_koder1_mot_koder2_alle_320"]["stemmer"] and m["følsomhet_ugyldige"] is None
    assert m["mønster_gemma2_koder1_koder2"] == {"000": 7, "010": 1, "100": 1, "111": 3}
    assert m["etter_dommerens_flagg"]["flagget"]["n"] == 6 and m["etter_dommerens_flagg"]["ikke_flagget"]["n"] == 6
    assert m["etter_dommerens_flagg"]["treff_per_utvalgstype"]["treff"] == {"n": 6, "gemma2": 3, "koder1": 3, "koder2": 3}
    assert m["innfiler"]["dommer.jsonl"] == _sha(v / "ut" / "dommer.jsonl")
