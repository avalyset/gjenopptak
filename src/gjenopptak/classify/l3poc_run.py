"""Kjøring av L3-POC: bygg materialet, døm, mål. Se ``l3poc.py`` for rammene.

    python -m gjenopptak.classify.l3poc_run bygg
    python -m gjenopptak.classify.l3poc_run røyk --dommer lokal|frontier
    python -m gjenopptak.classify.l3poc_run døm --dommer lokal|frontier
    python -m gjenopptak.classify.l3poc_run mål

Dommerne leser bare ``elementer-blind.jsonl`` (id og tekst). Fasiten leses først i ``mål``.
Ingen OpenAlex-kall.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx

from . import l3poc as P

UT = Path("data/l3-poc")
PROMPTFIL = Path("src/gjenopptak/classify/prompts/l3-poc-v1-system.txt")
PROMPTFIL_B = Path("src/gjenopptak/classify/prompts/l3-poc-B-system.txt")
BLIND_SHA256 = "e3988fae0c8ff498e8f41fddb68833937a37f8ee5bf3cb12bba7122e69fbeaaa"
LOKAL_MODELL = "gemma2:9b"
LOKAL_OPTIONS = {"temperature": 0.0, "seed": P.MAALEFRO, "num_ctx": 8192, "num_predict": 512}
OLLAMA = "http://localhost:11434"
#: gemini-3.1-pro-preview og gemini-pro-latest har ingen kvote på nøkkelens gratisnivå (429, målt 2026-09-14),
#: og gemini-2.5-pro svarte 503. Den nyeste Flash-modellen er dommeren; den er ikke en Pro-modell.
FRONTIER_MODELL = "gemini-3.8-flash"
FRONTIER_CONFIG = {"temperature": 1.0, "seed": P.MAALEFRO, "maxOutputTokens": 8192,
                   "thinkingConfig": {"thinkingLevel": "high"}}
RØYKTEKST = ("We were not able to transcribe the remaining letters, because the ink had faded beyond "
             "legibility in most of them. The transcribed letters are listed in Appendix 2.")


def nå() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_fil(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def skriv_jsonl(rader, p: Path) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    t = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rader)
    p.write_text(t, encoding="utf-8")
    return hashlib.sha256(t.encode()).hexdigest()


def les_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


# --------------------------------------------------------------------------- #
# bygg
# --------------------------------------------------------------------------- #

def bygg() -> int:
    system = P.build_system_prompt(Path("."))
    if not PROMPTFIL.exists() or PROMPTFIL.read_text(encoding="utf-8") != system:
        print(f"ledeteksten avviker fra {PROMPTFIL}: skriv den og commit før dom", file=sys.stderr)
        PROMPTFIL.write_text(system, encoding="utf-8")
        return 2

    f1 = [json.loads(l) for l in open("data/recall-sett.jsonl")][1:]
    f2 = [json.loads(l) for l in open("data/recall-sett-2.jsonl")][1:]
    lese1 = json.load(open("data/pipeline-test/sett1-lesetekster-slynge10.json"))
    logg = [x for x in json.load(open("data/leste-kontrollkandidater.json")) if x.get("kilde") == "recall-sett-ADDENDUM-06"]
    lest1 = {(x.get("work") or x.get("pmcid")): x.get("felt") for x in logg
             if (x.get("merke") or "").startswith("LEST-I-SIN-HELHET")}
    docs: dict[tuple[int, str], list[str]] = {}
    lag: dict[tuple[int, str], str] = {}
    for d, felt in lest1.items():
        rader = lese1[d]
        assert [e["i"] for e in rader] == list(range(len(rader))), d
        docs[(1, d)] = [e["t"] for e in rader]
        lag[(1, d)] = "humaniora" if (d.startswith("W") and felt in ("tekstvitenskap", "arkeologi")) else "biomed"
    s2: dict[str, dict[int, str]] = {}
    for l in open("data/recall-sett-2-setninger.jsonl"):
        r = json.loads(l)
        s2.setdefault(r["doc_id"], {})[r["sentence_index"]] = r["text"]
    for m in json.load(open("data/recall-sett-2-meta.json")):
        idx = s2[m["doc_id"]]
        assert sorted(idx) == list(range(len(idx))), m["doc_id"]
        docs[(2, m["doc_id"])] = [idx[i] for i in range(len(idx))]
        lag[(2, m["doc_id"])] = m["delsett"]

    elementer, blokkert = [], {}
    for sett, fasit in ((1, f1), (2, f2)):
        for x in fasit:
            key = (sett, x["doc_id"])
            s = docs[key]
            assert " ".join(s[x["hit_index"]].split()) == " ".join(x["sentence_text"].split())
            lo, hi = P.window_for(x["hit_index"], x["passage_span"], len(s))
            blokkert.setdefault(key, []).append((lo, hi))
            elementer.append({"sett": sett, "doc_id": x["doc_id"], "lag": lag[key], "type": "treff", "unit": x["unit"],
                              "fasit_klasse": x["klasse"], "grensetilfelle": x["grensetilfelle"],
                              "hit_index": x["hit_index"], "fra": lo, "til": hi, "tekst": " ".join(s[lo:hi + 1])})
    trekk = []
    for sett in (1, 2):
        for l_ in ("humaniora", "biomed"):
            n = sum(1 for e in elementer if e["sett"] == sett and e["lag"] == l_)
            if not n:
                continue
            kand = {k[1]: v for k, v in docs.items() if k[0] == sett and lag[k] == l_}
            blk = {k[1]: v for k, v in blokkert.items() if k[0] == sett and lag[k] == l_}
            for d, lo, hi in P.draw_negatives(kand, blk, n, random.Random(P.MAALEFRO)):
                s = kand[d]
                elementer.append({"sett": sett, "doc_id": d, "lag": l_, "type": "negativ", "unit": None,
                                  "fasit_klasse": None, "grensetilfelle": None, "hit_index": None,
                                  "fra": lo, "til": hi, "tekst": " ".join(s[lo:hi + 1])})
                trekk.append((sett, l_, d, lo, hi))
    elementer.sort(key=lambda e: (e["sett"], e["doc_id"], e["fra"], e["type"], e["hit_index"] or -1))
    random.Random(P.MAALEFRO).shuffle(elementer)
    for i, e in enumerate(elementer, 1):
        e["id"] = f"L3-{i:03d}"
    blind = [{"id": e["id"], "tekst": e["tekst"]} for e in elementer]
    fasit = [{k: v for k, v in e.items() if k != "tekst"} for e in elementer]
    UT.mkdir(parents=True, exist_ok=True)
    sha_blind = skriv_jsonl(blind, UT / "elementer-blind.jsonl")
    sha_fasit = skriv_jsonl(fasit, UT / "fasit.jsonl")
    kilder = ["data/recall-sett.jsonl", "data/recall-sett-2.jsonl", "data/recall-sett-2-setninger.jsonl",
              "data/recall-sett-2-meta.json", "data/pipeline-test/sett1-lesetekster-slynge10.json",
              "ADDENDUM-02.md", str(PROMPTFIL)]
    spes = {
        "tid": nå(), "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "målefrø": P.MAALEFRO, "vindu": P.WINDOW, "prompt_versjon": P.PROMPT_VERSION,
        "system_prompt_sha256": hashlib.sha256(system.encode()).hexdigest(),
        "kilder": {k: sha256_fil(Path(k)) for k in kilder},
        "lagregel": "humaniora = sett 2 delsett humaniora + sett 1 PDF-er i tekstvitenskap/arkeologi; resten biomed",
        "negativregel": "per (sett, lag) like mange som treff; ny random.Random(734248) per lag; ingen overlapp med fasitvinduer eller andre negative; bare leste dokumenter",
        "rekkefølge": "sortert på (sett, doc, fra, type), stokket med ny random.Random(734248)",
        "antall": dict(Counter(f"sett{e['sett']}-{e['lag']}-{e['type']}" for e in elementer)),
        "elementer_blind_sha256": sha_blind, "fasit_sha256": sha_fasit,
        "lokal": {"modell": LOKAL_MODELL, "options": LOKAL_OPTIONS, "keep_alive": 0},
        "frontier": {"modell": FRONTIER_MODELL, "generationConfig": FRONTIER_CONFIG},
    }
    (UT / "spesifikasjon.json").write_text(json.dumps(spes, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: spes[k] for k in ("antall", "system_prompt_sha256", "elementer_blind_sha256", "fasit_sha256")},
                     ensure_ascii=False, indent=1))
    return 0


# --------------------------------------------------------------------------- #
# dommere
# --------------------------------------------------------------------------- #

class Lokal:
    navn = f"local:{LOKAL_MODELL}"

    def __init__(self, keep_alive: int | str = 0) -> None:
        """``keep_alive=0`` laster modellen ut mellom dommer (ADR-0003). En annen verdi er
        bare tillatt ved batch-dømming over frosset materiale, og krever ADR-0008: samme
        signatur per dom, og vektfilen verifisert før og etter kjøringen."""
        self.keep_alive = keep_alive
        self.c = httpx.Client(timeout=900)
        self.versjon = self.c.get(f"{OLLAMA}/api/version").json()["version"]
        vis = self.c.post(f"{OLLAMA}/api/show", json={"model": LOKAL_MODELL}).json()
        self.detaljer = vis["details"]
        self.manifest = Path.home() / ".ollama/models/manifests/registry.ollama.ai/library" / LOKAL_MODELL.replace(":", "/")
        self.digest = self._digest()
        self.blob = Path.home() / ".ollama/models/blobs" / self.digest.replace(":", "-")
        print(f"verifiserer vekter {self.blob.name} ...", flush=True)
        self.verifisert = "sha256:" + sha256_fil(self.blob)
        if self.verifisert != self.digest:
            raise RuntimeError(f"vektfilen stemmer ikke med manifestet: {self.verifisert} ≠ {self.digest}")

    def _digest(self) -> str:
        m = json.loads(self.manifest.read_text())
        return next(l["digest"] for l in m["layers"] if l["mediaType"] == "application/vnd.ollama.image.model")

    def __call__(self, system: str, user: str, format: dict | None = None) -> dict:
        """``format`` er JSON-skjemaet svaret tvinges inn i; uten det brukes dommer A sitt."""
        if self._digest() != self.verifisert:
            raise RuntimeError("modellmanifestet er endret under kjøringen")
        r = self.c.post(f"{OLLAMA}/api/chat", json={
            "model": LOKAL_MODELL, "stream": False, "keep_alive": self.keep_alive,
            "format": format or P.RESPONSE_SCHEMA,
            "options": LOKAL_OPTIONS,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]})
        r.raise_for_status()
        d = r.json()
        grense = LOKAL_OPTIONS["num_ctx"] - LOKAL_OPTIONS["num_predict"]
        return {
            "råsvar": d["message"]["content"],
            "avkortet_kontekst": d.get("prompt_eval_count", 0) >= grense,
            "bruk": {k: d.get(k) for k in ("prompt_eval_count", "eval_count", "total_duration", "load_duration", "done_reason")},
            "signatur": {
                "model_id": f"{LOKAL_MODELL}@{self.digest}", "weights_sha256": self.verifisert.split(":", 1)[1],
                "temperature": LOKAL_OPTIONS["temperature"], "seed": LOKAL_OPTIONS["seed"],
                "keep_alive": self.keep_alive, "batch": self.keep_alive != 0,
                "runtime": f"ollama {self.versjon}; {self.detaljer.get('format')} {self.detaljer.get('quantization_level')}; "
                           f"{self.detaljer.get('family')} {self.detaljer.get('parameter_size')}; num_ctx {LOKAL_OPTIONS['num_ctx']}",
                "prompt_sha256": P.prompt_sha256(system, user), "judged_at": nå()},
        }


def gemini_schema(s: dict) -> dict:
    t = {"object": "OBJECT", "string": "STRING", "boolean": "BOOLEAN"}
    ut = {"type": t[s["type"]]}
    if "enum" in s:
        ut["enum"] = s["enum"]
    if "properties" in s:
        ut["properties"] = {k: gemini_schema(v) for k, v in s["properties"].items()}
        ut["required"] = s["required"]
        ut["propertyOrdering"] = list(s["properties"])
    return ut


class Frontier:
    navn = f"external:{FRONTIER_MODELL}"

    def __init__(self) -> None:
        nøkkel = next((l.split("=", 1)[1].strip().strip("'\"") for l in (Path.home() / ".env").read_text().splitlines()
                       if l.strip().startswith("GEMINI_API_KEY=")), None)
        if not nøkkel:
            raise RuntimeError("GEMINI_API_KEY finnes ikke i ~/.env")
        self.c = httpx.Client(timeout=600, headers={"x-goog-api-key": nøkkel})
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{FRONTIER_MODELL}:generateContent"

    def __call__(self, system: str, user: str) -> dict:
        body = {"systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
                "generationConfig": dict(FRONTIER_CONFIG, responseMimeType="application/json",
                                         responseSchema=gemini_schema(P.RESPONSE_SCHEMA))}
        for forsøk in range(10):
            r = self.c.post(self.url, json=body)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(120, 5 * 2 ** forsøk))
                continue
            break
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
        d = r.json()
        kand = (d.get("candidates") or [{}])[0]
        tekst = "".join(p.get("text", "") for p in (kand.get("content") or {}).get("parts", []) if not p.get("thought"))
        return {
            "råsvar": tekst, "avkortet_kontekst": False,
            "bruk": {"usage": d.get("usageMetadata"), "finishReason": kand.get("finishReason"), "responseId": d.get("responseId")},
            "signatur": {
                "model_id": f"{FRONTIER_MODELL}@{d.get('modelVersion')}",
                "weights_sha256": "utilgjengelig: API-modell, vektene er ikke eksponert",
                "temperature": FRONTIER_CONFIG["temperature"], "seed": FRONTIER_CONFIG["seed"], "keep_alive": 0,
                "runtime": f"Gemini API v1beta generateContent; thinkingLevel {FRONTIER_CONFIG['thinkingConfig']['thinkingLevel']}",
                "prompt_sha256": P.prompt_sha256(system, user), "judged_at": nå()},
        }


def lag_dommer(navn: str):
    return Lokal() if navn == "lokal" else Frontier()


def røyk(navn: str) -> int:
    system = PROMPTFIL.read_text(encoding="utf-8")
    svar = lag_dommer(navn)(system, P.user_prompt(RØYKTEKST))
    p = P.parse_response(svar["råsvar"])
    rad = {"dommer": navn, "røyktekst": RØYKTEKST, **svar, "tolket": p.__dict__}
    with (UT / f"røyk-{navn}.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rad, ensure_ascii=False) + "\n")
    print(json.dumps({"råsvar": svar["råsvar"][:400], "tolket": p.__dict__, "bruk": svar["bruk"],
                      "model_id": svar["signatur"]["model_id"]}, ensure_ascii=False, indent=1))
    return 0


def døm(navn: str, arbeidere: int, variant: str = "A") -> int:
    if variant == "B":
        if navn != "lokal":
            print("variant B kjøres bare med lokal dommer", file=sys.stderr)
            return 2
        system = PROMPTFIL_B.read_text(encoding="utf-8")
        spes = json.loads((UT / "spesifikasjon-B.json").read_text())
    else:
        system = PROMPTFIL.read_text(encoding="utf-8")
        spes = json.loads((UT / "spesifikasjon.json").read_text())
    if hashlib.sha256(system.encode()).hexdigest() != spes["system_prompt_sha256"]:
        print("ledeteksten er endret etter bygg: dom avbrytes", file=sys.stderr)
        return 2
    if sha256_fil(UT / "elementer-blind.jsonl") != BLIND_SHA256:
        print("de blindede elementene er ikke de frosne: dom avbrytes", file=sys.stderr)
        return 2
    blind = les_jsonl(UT / "elementer-blind.jsonl")
    utfil = UT / (f"dommer-{navn}.jsonl" if variant == "A" else f"dommer-{navn}-{variant}.jsonl")
    ferdige = {r["id"] for r in les_jsonl(utfil)}
    todo = [e for e in blind if e["id"] not in ferdige]
    dommer = lag_dommer(navn)
    laas = threading.Lock()

    def én(e: dict) -> None:
        try:
            svar = dommer(system, P.user_prompt(e["tekst"]))
            p = P.parse_response(svar["råsvar"])
            if svar.get("avkortet_kontekst"):
                p = P.Parsed("UGYLDIG", False, False)
            rad = {"id": e["id"], "dommer": dommer.navn, **svar, "klasse": p.klasse, "treff": p.treff,
                   "inkonsistent": p.inkonsistent}
        except Exception as ex:                                   # noqa: BLE001
            # Transportfeil er ingen dom: raden skrives ikke, og en ny kjøring tar elementet på nytt.
            with laas:
                print(f"{e['id']} FEIL {type(ex).__name__}: {str(ex)[:200]}", flush=True)
            return
        with laas:
            with utfil.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rad, ensure_ascii=False) + "\n")
            print(f"{rad['id']} {rad['klasse']}", flush=True)

    with ThreadPoolExecutor(max_workers=arbeidere) as ex:
        list(ex.map(én, todo))
    if navn == "lokal":
        slutt = "sha256:" + sha256_fil(dommer.blob)
        (UT / "vekter-lokal-slutt.json").write_text(json.dumps({"tid": nå(), "digest": slutt,
                                                                  "lik_start": slutt == dommer.verifisert}) + "\n")
    return 0


# --------------------------------------------------------------------------- #
# mål
# --------------------------------------------------------------------------- #

def mål() -> int:
    fasit = {r["id"]: r for r in les_jsonl(UT / "fasit.jsonl")}
    tekst = {r["id"]: r["tekst"] for r in les_jsonl(UT / "elementer-blind.jsonl")}
    dommer = {}
    for navn in ("lokal", "frontier"):
        rader = {r["id"]: r for r in les_jsonl(UT / f"dommer-{navn}.jsonl")}
        if len(rader) != len(fasit):
            print(f"{navn}: {len(rader)} av {len(fasit)} dommer", file=sys.stderr)
        if rader:
            dommer[navn] = rader
    ut: dict = {"tid": nå(), "per_dommer": {}, "dommere_imellom": {}}
    for navn, rader in dommer.items():
        rows = [{"id": i, "fasit_klasse": f["fasit_klasse"], "klasse": rader[i]["klasse"], "treff": rader[i]["treff"],
                 "inkonsistent": rader[i].get("inkonsistent", False), "lag": f["lag"], "unit": f["unit"], "sett": f["sett"]}
                for i, f in fasit.items() if i in rader]
        blokk = {"alle": P.metrics(rows)}
        for l_ in ("humaniora", "biomed"):
            blokk[f"lag:{l_}"] = P.metrics([r for r in rows if r["lag"] == l_])
        for u in ("sentence", "passage"):
            blokk[f"enhet:{u}"] = P.metrics([r for r in rows if r["unit"] == u])
        for s in (1, 2):
            blokk[f"sett:{s}"] = P.metrics([r for r in rows if r["sett"] == s])
        verst = P.worst_misses(rows)
        blokk["verste_bommer"] = [dict(v, tekst=tekst[v["id"]], doc_id=fasit[v["id"]]["doc_id"],
                                       fra=fasit[v["id"]]["fra"], til=fasit[v["id"]]["til"],
                                       begrunnelse=_begrunnelse(rader[v["id"]])) for v in verst]
        blokk["signaturer"] = sorted({json.dumps({k: r["signatur"][k] for k in ("model_id", "weights_sha256", "runtime")},
                                                  ensure_ascii=False) for r in rader.values() if "signatur" in r})
        ut["per_dommer"][navn] = blokk
    if len(dommer) < 2:
        ut["dommere_imellom"] = {"merknad": "bare én dommer har dømt; enighet mellom dommere kan ikke regnes"}
        (UT / "resultater.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return 0
    felles = [i for i in fasit if i in dommer["lokal"] and i in dommer["frontier"]]
    ut["dommere_imellom"]["alle"] = P.judge_agreement([dommer["lokal"][i] for i in felles], [dommer["frontier"][i] for i in felles])
    for l_ in ("humaniora", "biomed"):
        ids = [i for i in felles if fasit[i]["lag"] == l_]
        ut["dommere_imellom"][f"lag:{l_}"] = P.judge_agreement([dommer["lokal"][i] for i in ids], [dommer["frontier"][i] for i in ids])
    (UT / "resultater.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({n: {k: v for k, v in b.items() if k not in ("verste_bommer",)} for n, b in ut["per_dommer"].items()},
                     ensure_ascii=False, indent=1)[:6000])
    print(json.dumps(ut["dommere_imellom"], ensure_ascii=False, indent=1))
    return 0


def bygg_b() -> int:
    if sha256_fil(UT / "elementer-blind.jsonl") != BLIND_SHA256:
        print("de blindede elementene er ikke de frosne", file=sys.stderr)
        return 2
    fasitrader = [dict(json.loads(l), sett=1) for l in open("data/recall-sett.jsonl")][1:] + \
                 [dict(json.loads(l), sett=2) for l in open("data/recall-sett-2.jsonl")][1:]
    h7, h12 = P.select_examples(fasitrader)
    system_b = P.build_system_prompt_b(PROMPTFIL.read_text(encoding="utf-8"), h7["passage_text"], h12["passage_text"])
    if not PROMPTFIL_B.exists() or PROMPTFIL_B.read_text(encoding="utf-8") != system_b:
        PROMPTFIL_B.write_text(system_b, encoding="utf-8")
        print(f"skrev {PROMPTFIL_B}: commit den før dom", file=sys.stderr)
        return 2
    blind = les_jsonl(UT / "elementer-blind.jsonl")
    utenfor = sorted(e["id"] for e in blind if P.contains_example(e["tekst"], [h7["passage_text"], h12["passage_text"]]))
    felt = ("sett", "doc_id", "hit_index", "klasse", "unit", "grensetilfelle", "passage_text")
    spes = {
        "tid": nå(), "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "prompt_versjon": P.PROMPT_VERSION_B, "system_prompt_sha256": hashlib.sha256(system_b.encode()).hexdigest(),
        "prompt_A_sha256": hashlib.sha256(PROMPTFIL.read_bytes()).hexdigest(),
        "elementer_blind_sha256": BLIND_SHA256,
        "eksempel_H7": {k: h7[k] for k in felt}, "eksempel_H1H2": {k: h12[k] for k in felt},
        "eksempelregel": "H7: setningstreff, ikke grensetilfelle, eneste treff i dokumentet; H1/H2: setningstreff, "
                         "ikke grensetilfelle; én trukket per side med ny random.Random(734248) over sortert liste",
        "elementer_med_eksempeltekst": utenfor,
        "lokal": {"modell": LOKAL_MODELL, "options": LOKAL_OPTIONS, "keep_alive": 0},
    }
    (UT / "spesifikasjon-B.json").write_text(json.dumps(spes, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: spes[k] for k in ("system_prompt_sha256", "eksempel_H7", "eksempel_H1H2", "elementer_med_eksempeltekst")},
                     ensure_ascii=False, indent=1))
    return 0


def sammenlign() -> int:
    fasit = {r["id"]: r for r in les_jsonl(UT / "fasit.jsonl")}
    spes_b = json.loads((UT / "spesifikasjon-B.json").read_text())
    utenfor = set(spes_b["elementer_med_eksempeltekst"])
    varianter = {"A": {r["id"]: r for r in les_jsonl(UT / "dommer-lokal.jsonl")},
                 "B": {r["id"]: r for r in les_jsonl(UT / "dommer-lokal-B.jsonl")}}
    ut: dict = {"tid": nå(), "elementer_med_eksempeltekst": sorted(utenfor), "målinger": {}}
    for v, rader in varianter.items():
        if len(rader) != len(fasit):
            print(f"variant {v}: {len(rader)} av {len(fasit)} dommer", file=sys.stderr)
        for omfang, ids in (("alle", list(fasit)), ("uten_eksempelelementer", [i for i in fasit if i not in utenfor])):
            for lag in (None, "humaniora", "biomed"):
                rows = [{"id": i, "fasit_klasse": fasit[i]["fasit_klasse"], "klasse": rader[i]["klasse"],
                         "treff": rader[i]["treff"]} for i in ids if i in rader and (lag is None or fasit[i]["lag"] == lag)]
                ut["målinger"][f"{v}|{omfang}|{lag or 'alle lag'}"] = P.comparison_metrics(rows)
        ut[f"signatur_{v}"] = sorted({json.dumps({k: r["signatur"][k] for k in ("model_id", "weights_sha256", "temperature", "seed", "keep_alive", "runtime")},
                                                  ensure_ascii=False) for r in rader.values() if "signatur" in r})
        ut[f"prompt_sha256_{v}"] = sorted({r["signatur"]["prompt_sha256"] for r in rader.values() if "signatur" in r})[:1]
    (UT / "sammenligning-AB.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k, m in ut["målinger"].items():
        print(k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in m.items()})
    return 0


def _begrunnelse(rad: dict) -> str | None:
    try:
        return json.loads(rad.get("råsvar") or "").get("begrunnelse")
    except (ValueError, AttributeError):
        return None


from ..vault import krev, utkatalog  # ADR-0009


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="L3-POC (ikke M1/M2). Ingen OpenAlex-kall.")
    sub = ap.add_subparsers(dest="kommando", required=True)
    sub.add_parser("bygg")
    sub.add_parser("bygg-b")
    for k in ("røyk", "døm"):
        s = sub.add_parser(k)
        s.add_argument("--dommer", choices=("lokal", "frontier"), required=True)
        s.add_argument("--arbeidere", type=int, default=1)
        s.add_argument("--variant", choices=("A", "B"), default="A")
    sub.add_parser("mål")
    sub.add_parser("sammenlign")
    a = ap.parse_args(argv)
    global UT
    UT = utkatalog("logs/l3-poc")  # ADR-0009: ingen fallback
    if a.kommando == "bygg":
        return bygg()
    if a.kommando == "røyk":
        return røyk(a.dommer)
    if a.kommando == "døm":
        return døm(a.dommer, a.arbeidere, a.variant)
    if a.kommando == "bygg-b":
        return bygg_b()
    if a.kommando == "sammenlign":
        return sammenlign()
    return mål()


if __name__ == "__main__":
    raise SystemExit(main())
