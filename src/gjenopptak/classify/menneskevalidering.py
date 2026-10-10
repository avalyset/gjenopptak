"""Menneskelig validering (ADDENDUM-27): trekk den stratifiserte prøven og skriv blindfila. Ikke kjørt mot mennesker.

    PYTHONPATH=src python -m gjenopptak.classify.menneskevalidering bygg

Skriver til Vault `revisjon-2026-10/menneskevalidering/`: `blind.jsonl` (id og tekst, stokket — ingen modellsvar,
ingen kilde), `nokkel.jsonl` (id → stratum, verk, spenn, kilde og alle modelletiketter), `utvalg.json` (strata,
populasjonsstørrelser, trukket antall, inklusjonssannsynligheter, sha256) og `skjema.csv` (tomt kodeskjema).

Strata, låst i ADDENDUM-27 § 2 (frø 734248, `random.Random(frø).sample` over id-er sortert, per stratum):

| stratum | kilde | populasjon |
|---|---|---|
| A1 | 320-settet, flagget av dommeren, koder 1 positiv | `utvalgstype == "treff"`, `ekte_treff` |
| A2 | 320-settet, flagget, koder 1 negativ | `utvalgstype == "treff"`, ikke `ekte_treff` |
| A3 | 320-settet, ikke flagget | `utvalgstype in {"ingen", "n3", "n1n2"}` — de to kjente bommene tas alltid med |
| B1 | fase 3, leser positiv, `tvil: false` | leserens dommer over unionen |
| B2 | fase 3, leser positiv, `tvil: true` | " |
| B3 | fase 3, leser negativ | " |
| B4 | fase 3, referansetreff silen eller leseren mistet | `maaling-fase3.json`, `bekreftet: false` — alle |
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

from ..vault import require_vault, sha256_file

FRØ = 734248
ALLOKERING = {"A1": 25, "A2": 30, "A3": 30, "B1": 15, "B2": 15, "B3": 15, "B4": None}  # None = alle
F3_KJØRING = "fase3/worktree-f19a3e3/data/kjede/fase3-kjede"


def _jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def populasjoner(v: Path) -> dict[str, list[dict]]:
    P = v / "presisjonssett"
    k1 = {r["id"]: r for r in _jl(P / "port-presisjonssett-ADDENDUM10.jsonl")}
    k2 = {r["id"]: r for r in _jl(P / "port-presisjonssett-verdikter-koder2.jsonl")}
    k4 = {r["id"]: r for r in _jl(v / "koder4" / "koder4-fable51-verdikter.jsonl")}
    op = {}
    for r in _jl(v / "ekstraksjon/2026-09-26/addendum-19/opus5-b-dommer.jsonl"):
        try:
            op[r["id"]] = json.loads(r["raasvar"])
        except ValueError:
            op[r["id"]] = None
    tekst = {r["id"]: r["tekst"] for r in _jl(P / "port-presisjonssett-blind.jsonl")}
    A = defaultdict(list)
    for i, r in sorted(k1.items()):
        u = r["utvalgstype"]
        if u.startswith("anker"):
            continue
        rad = {"kilde": "port-320", "kilde_id": i, "doc_id": r["doc_id"], "felt": r["felt"],
               "start_index": int(r["start_index"]), "end_index": int(r["end_index"]), "tekst": tekst[i],
               "modell": {"dommer_flagget": u == "treff", "dommer_klasse": r.get("dømt_klasse"),
                          "koder1": {"treff": bool(r["ekte_treff"]), "klasse": r.get("min_klasse"), "tvil": r.get("tvil")},
                          "koder2": {"treff": bool(k2[i]["ekte_treff"]), "klasse": k2[i].get("min_klasse"), "tvil": k2[i].get("tvil")},
                          "koder4": {"treff": bool(k4[i]["treff"]), "klasse": k4[i].get("klasse"), "tvil": k4[i].get("tvil")},
                          "opus_ett_kall": op.get(i)}}
        if u == "treff":
            A["A1" if r["ekte_treff"] else "A2"].append(rad)
        else:
            rad["ikke_flagget_stratum"] = u
            A["A3"].append(rad)
    # fase 3
    kd = v / F3_KJØRING
    nøkkel = {r["id"]: r for r in _jl(v / "fase3-kjede" / "nokkel.jsonl")}
    btekst = {r["id"]: r["tekst"] for f in sorted((kd / "blind").glob("blind-okt-*.jsonl")) for r in _jl(f)}
    for f in sorted(kd.glob("7-verdikter-okt-*.jsonl")):
        for r in _jl(f):
            n = nøkkel[r["id"]]
            rad = {"kilde": "fase3-union", "kilde_id": r["id"], "doc_id": n["doc_id"], "felt": "arkeologi",
                   "start_index": n["start_index"], "end_index": n["end_index"], "tekst": btekst[r["id"]],
                   "modell": {"sil_kilde": n.get("kilde"), "leser": {k: r.get(k) for k in ("treff", "klasse", "tvil")}}}
            A["B1" if r["treff"] and not r["tvil"] else "B2" if r["treff"] else "B3"].append(rad)
    # B4: referansetreff som ikke ble bekreftet; passasjen er ±2 setninger rundt treffets setninger
    tekster = {t["ref"]: t for t in json.loads((v / "fase3/referanse/tekster.json").read_text(encoding="utf-8"))}
    linjer = {}
    for ref, t in tekster.items():
        d = {}
        for l in (v / "fase3/referanse/tekst" / t["fil"]).read_text(encoding="utf-8").splitlines():
            if l.startswith("S") and ": " in l:
                n_, s = l.split(": ", 1)
                d[int(n_[1:])] = s
        linjer[ref] = d
    for j, r in enumerate(json.loads((v / "fase3/maaling-fase3.json").read_text(encoding="utf-8"))["rader"]):
        if r["bekreftet"]:
            continue
        s = r["setninger"]
        a, b = max(0, min(s) - 2), max(s) + 2
        tekst_ = " ".join(linjer[r["ref"]][k] for k in range(a, b + 1) if k in linjer[r["ref"]])
        A["B4"].append({"kilde": "fase3-referanse", "kilde_id": f"{r['ref']}-{j:03d}", "doc_id": r["work_id"],
                        "felt": "arkeologi", "start_index": a, "end_index": b, "tekst": tekst_,
                        "modell": {"referanse": {"klasse": r["klasse"], "tvil": r["tvil"], "setninger": s},
                                   "beholdt_av_silen": r["beholdt"], "bekreftet_av_leseren": False}})
    return A


def trekk(A: dict[str, list[dict]]) -> list[dict]:
    valgt: list[dict] = []
    sett = set()
    for st, n in ALLOKERING.items():
        pop = sorted(A[st], key=lambda r: r["kilde_id"])
        if st == "A3":
            kjente = [r for r in pop if r["modell"]["koder1"]["treff"]]           # de to kjente bommene
            rest = [r for r in pop if not r["modell"]["koder1"]["treff"]]
            ut = kjente + random.Random(FRØ).sample(rest, n - len(kjente))
        elif n is None:
            ut = pop
        else:
            ut = random.Random(FRØ).sample(pop, min(n, len(pop)))
        for r in ut:
            k = (r["doc_id"], r["start_index"], r["end_index"])
            if k in sett:          # samme passasje i to strata telles én gang, i det første
                continue
            sett.add(k)
            valgt.append({**r, "stratum": st, "populasjon": len(pop), "trukket_i_stratum": len(ut)})
    return valgt


def bygg() -> int:
    v = require_vault()
    od = v / "revisjon-2026-10" / "menneskevalidering"
    if (od / "blind.jsonl").exists():
        print("blindfila finnes — trekkes ikke om", file=sys.stderr)
        return 2
    od.mkdir(parents=True, exist_ok=True)
    A = populasjoner(v)
    valgt = trekk(A)
    rekkefølge = list(range(len(valgt)))
    random.Random(FRØ).shuffle(rekkefølge)
    blind, nøkkel = [], []
    for nr, idx in enumerate(rekkefølge, 1):
        r = valgt[idx]
        hid = f"MV-{nr:03d}"
        blind.append({"id": hid, "tekst": r["tekst"]})
        nøkkel.append({"id": hid, **{k: r[k] for k in ("stratum", "kilde", "kilde_id", "doc_id", "felt", "start_index",
                                                        "end_index", "populasjon", "trukket_i_stratum", "modell")},
                       "tekst_sha256": _sha(r["tekst"]), **({"ikke_flagget_stratum": r["ikke_flagget_stratum"]}
                                                             if "ikke_flagget_stratum" in r else {})})
    (od / "blind.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in blind), encoding="utf-8")
    (od / "nokkel.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in nøkkel), encoding="utf-8")
    with (od / "skjema.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "annotator", "treff", "undone_sentence", "obstacle_sentence", "klasse", "uavklart", "tvil", "kommentar"])
        for r in blind:
            w.writerow([r["id"], "", "", "", "", "", "", "", ""])
    strata = {}
    for st in ALLOKERING:
        rr = [r for r in valgt if r["stratum"] == st]
        pop = len(A[st])
        strata[st] = {"populasjon": pop, "trukket": len(rr), "inklusjonssannsynlighet": round(len(rr) / pop, 4) if pop else None,
                      "verk": len({r["doc_id"] for r in rr}),
                      "felt": {f: sum(1 for r in rr if r["felt"] == f) for f in sorted({r["felt"] for r in rr})}}
    utv = {"frø": FRØ, "n": len(blind), "strata": strata,
           "blind_sha256": sha256_file(od / "blind.jsonl"), "nokkel_sha256": sha256_file(od / "nokkel.jsonl"),
           "skjema_sha256": sha256_file(od / "skjema.csv"),
           "kilder": {str(p.relative_to(v)): sha256_file(p) for p in (
               v / "presisjonssett/port-presisjonssett-ADDENDUM10.jsonl", v / "presisjonssett/port-presisjonssett-blind.jsonl",
               v / "presisjonssett/port-presisjonssett-verdikter-koder2.jsonl", v / "koder4/koder4-fable51-verdikter.jsonl",
               v / "ekstraksjon/2026-09-26/addendum-19/opus5-b-dommer.jsonl", v / "fase3-kjede/nokkel.jsonl",
               v / "fase3/maaling-fase3.json", v / "fase3/referanse/tekster.json")}}
    (od / "utvalg.json").write_text(json.dumps(utv, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(utv, ensure_ascii=False, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("kommando", choices=("bygg",))
    p.parse_args(argv)
    return bygg()


if __name__ == "__main__":
    sys.exit(main())
