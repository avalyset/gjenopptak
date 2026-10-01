"""ADDENDUM-24: lokal agentisk leser mot koder 1 over portens 320.

    PYTHONPATH=src python -m gjenopptak.classify.leser_port kanari
    PYTHONPATH=src python -m gjenopptak.classify.leser_port kjør
    PYTHONPATH=src python -m gjenopptak.classify.leser_port mål

Alt som styrer kjøringen står i ``OPPSETT`` og er låst av ADDENDUM-24 med sha256: modell og
vekt, instruks, regelfil, blindfil, partistørrelse, temperatur, frø, ``num_ctx``,
``num_predict``. Utdata går til Vault, aldri til scratchpad (LAERDOM § 30).

**Hva som ikke gjøres:** ingen omkjøring av et parti som ga ugyldige dommer (temp 0 og fast frø
gir samme svar), ingen utfylling, ingen ny ledetekst etter å ha sett et utfall.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from ..kjede.leser import LokalLeser, sha256_blob, sha256_tekst
from ..vault import require_vault, sha256_file
from .reliabilitet import cohen_kappa, kappa_bootstrap, ra_enighet

REPO = Path(__file__).resolve().parents[3]

OPPSETT = {
    "modell": "qwen2.5:7b",
    "vekt_sha256": "2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730",
    "instruks": "prompts/leser-lokal-v1.txt",
    "regelfil": "koder2/koderegler-gjenvunnet.md",
    "regelfil_sha256": "234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449",
    "blindfil": "data/port-presisjonssett-blind.jsonl",
    "blindfil_sha256": "15ce72a7687cea57ac1e7f774aa0303f0bedfc3c2867244d24173a1ec211d4a5",
    "parti": 20,
    "num_ctx": 32768,
    "num_predict": 8192,
    "temperatur": 0,
    "frø": 734248,
    "kanari_id": "KANARI",
    "kanari_tekst": "We could not date the layer, because no suitable sample was preserved.",
    "koder1": "data/port-presisjonssett-ADDENDUM10.jsonl",
    "koder2": "data/port-presisjonssett-verdikter-koder2.jsonl",
    "koder4": "koder4/koder4-fable51-verdikter.jsonl",   # relativ til Vault
    "terskel_kappa": 0.70,
    "utdir": "leser-lokal-ADDENDUM-24",                 # relativ til Vault
}


def _vekt_blob(digest: str) -> Path:
    return Path.home() / ".ollama" / "models" / "blobs" / f"sha256-{digest}"


def _jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def forutsetninger() -> tuple[Path, str, list[dict], LokalLeser]:
    """Verifiser alt som er låst før noe kjøres. Ett avvik stopper."""
    v = require_vault()
    avvik = []
    blob = _vekt_blob(OPPSETT["vekt_sha256"])
    if not blob.is_file() or sha256_blob(blob) != OPPSETT["vekt_sha256"]:
        avvik.append(f"vekten {OPPSETT['modell']} stemmer ikke med {OPPSETT['vekt_sha256'][:16]}…")
    rf = v / OPPSETT["regelfil"]
    if sha256_file(rf) != OPPSETT["regelfil_sha256"]:
        avvik.append("regelfilen har endret sha256")
    bf = REPO / OPPSETT["blindfil"]
    if sha256_file(bf) != OPPSETT["blindfil_sha256"]:
        avvik.append("blindfilen har endret sha256")
    if avvik:
        raise SystemExit("STOPP — " + "; ".join(avvik))
    instruks = (REPO / OPPSETT["instruks"]).read_text(encoding="utf-8")
    leser = LokalLeser(modell=OPPSETT["modell"], vekt_sha256=OPPSETT["vekt_sha256"],
                       instruks=instruks, num_ctx=OPPSETT["num_ctx"],
                       temperatur=OPPSETT["temperatur"], frø=OPPSETT["frø"],
                       num_predict=OPPSETT["num_predict"])
    return v, rf.read_text(encoding="utf-8"), _jsonl(bf), leser


def partier(blind: list[dict]) -> list[list[dict]]:
    n = OPPSETT["parti"]
    return [blind[i:i + n] for i in range(0, len(blind), n)]


def kanari() -> int:
    """Største parti + kanaritekstbit sist. Bestått: ingen avkutting inn eller ut, og kanarien
    har en gyldig dom. Kanariens klasse kreves ikke — det ville målt leserens kvalitet."""
    v, regler, blind, leser = forutsetninger()
    største = max(partier(blind), key=lambda p: sum(len(r["tekst"]) for r in p))
    prøve = største + [{"id": OPPSETT["kanari_id"], "tekst": OPPSETT["kanari_tekst"]}]
    l = leser(regler, prøve, nr=0, av=0)
    b = l.bruk
    ok = (not b.get("avkuttet_inn") and not b.get("avkuttet_ut") and not b.get("parsefeil")
          and OPPSETT["kanari_id"] not in l.ugyldige)
    ut = {"bestått": ok, "tid": datetime.now(timezone.utc).isoformat(timespec="seconds"),
          "parti_ids": [r["id"] for r in største], "parti_tegn": sum(len(r["tekst"]) for r in største),
          "prompt_eval_count": b.get("prompt_eval_count"), "num_ctx": OPPSETT["num_ctx"],
          "vindusfylling": round((b.get("prompt_eval_count") or 0) / OPPSETT["num_ctx"], 3),
          "eval_count": b.get("eval_count"), "done_reason": b.get("done_reason"),
          "gyldige": len(l.dommer), "ugyldige": l.ugyldige,
          "kanari_dom": next((d for d in l.dommer if d["id"] == OPPSETT["kanari_id"]), None),
          "sekunder": b.get("sekunder"), "signatur": leser.signatur()}
    d = v / OPPSETT["utdir"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "kanari.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: ut[k] for k in ut if k not in ("parti_ids", "signatur")}, ensure_ascii=False))
    return 0 if ok else 2


def kjør() -> int:
    v, regler, blind, leser = forutsetninger()
    d = v / OPPSETT["utdir"]
    if not (d / "kanari.json").is_file() or not json.loads((d / "kanari.json").read_text())["bestått"]:
        raise SystemExit("STOPP — kanarien er ikke bestått")
    ps = partier(blind)
    t0 = time.time()
    for i, p in enumerate(ps, 1):
        f = d / f"parti-{i:02d}.json"
        if f.is_file():
            print(f"parti {i}: finnes, hopper over (ingen omkjøring)")
            continue
        l = leser(regler, p, nr=i, av=len(ps))
        f.write_text(json.dumps({"parti": i, "ids": [r["id"] for r in p], "dommer": l.dommer,
                                 "ugyldige": l.ugyldige, "bruk": l.bruk,
                                 "signatur": leser.signatur(),
                                 "tid": datetime.now(timezone.utc).isoformat(timespec="seconds")},
                                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"parti {i}/{len(ps)}: {len(l.dommer)} gyldige, {len(l.ugyldige)} ugyldige, "
              f"inn {l.bruk.get('prompt_eval_count')}, ut {l.bruk.get('eval_count')}, "
              f"{l.bruk.get('done_reason')}, {l.bruk.get('sekunder')} s", flush=True)
    if sha256_blob(_vekt_blob(OPPSETT["vekt_sha256"])) != OPPSETT["vekt_sha256"]:
        raise SystemExit("STOPP — vekten endret seg under kjøringen")
    print(f"ferdig, {round((time.time() - t0) / 60, 1)} min")
    return 0


def _kappa(a: dict, b: dict, ids: list[str]) -> dict:
    x, y = [a[i] for i in ids], [b[i] for i in ids]
    lo, hi = kappa_bootstrap(x, y, seed=OPPSETT["frø"])
    return {"n": len(ids), "kappa": round(cohen_kappa(x, y), 3), "bootstrap_95": [round(lo, 3), round(hi, 3)],
            "rå_enighet": round(ra_enighet(x, y), 3), "treff_a": sum(x), "treff_b": sum(y)}


def mål() -> int:
    v = require_vault()
    d = v / OPPSETT["utdir"]
    blind = _jsonl(REPO / OPPSETT["blindfil"])
    ids = [r["id"] for r in blind]
    lokal, ugyldige, bruk = {}, [], []
    for i in range(1, len(partier(blind)) + 1):
        f = d / f"parti-{i:02d}.json"
        if not f.is_file():
            raise SystemExit(f"parti {i} mangler — målingen regnes ikke på et ufullstendig sett")
        p = json.loads(f.read_text(encoding="utf-8"))
        for dom in p["dommer"]:
            lokal[dom["id"]] = dom
        ugyldige += p["ugyldige"]
        bruk.append({k: p["bruk"].get(k) for k in ("prompt_eval_count", "eval_count", "done_reason",
                                                    "sekunder", "avkuttet_ut", "parsefeil")})
    k1 = {r["id"]: bool(r["ekte_treff"]) for r in _jsonl(REPO / OPPSETT["koder1"])}
    k2 = {r["id"]: bool(r["ekte_treff"]) for r in _jsonl(REPO / OPPSETT["koder2"])}
    k4 = {r["id"]: bool(r["treff"]) for r in _jsonl(v / OPPSETT["koder4"])}
    L = {i: bool(lokal[i]["ekte_treff"]) for i in lokal}
    # Kriteriet (ADDENDUM-24 §4): over alle 320, ugyldig dom = motsatt av koder 1 (verste fall).
    L_verst = {i: L[i] if i in L else (not k1[i]) for i in ids}
    gyldige = [i for i in ids if i in L]
    res = {
        "tid": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "gyldige": len(gyldige), "ugyldige": sorted(set(ugyldige)),
        "kriterium": {"mot": "koder 1", "terskel": OPPSETT["terskel_kappa"], **_kappa(L_verst, k1, ids)},
        "mot_koder1_bare_gyldige": _kappa(L, k1, gyldige),
        "mot_koder2": _kappa(L_verst, k2, ids),
        "mot_koder4": _kappa(L_verst, k4, ids),
        "treff_lokal": sum(L.values()),
        "klasser_lokal": {},
        "veggtid_s": round(sum(b["sekunder"] or 0 for b in bruk), 1),
        "tokens_inn": sum(b["prompt_eval_count"] or 0 for b in bruk),
        "tokens_ut": sum(b["eval_count"] or 0 for b in bruk),
        "done_reason": sorted({str(b["done_reason"]) for b in bruk}),
        "partier": bruk,
    }
    for dom in lokal.values():
        res["klasser_lokal"][dom["min_klasse"]] = res["klasser_lokal"].get(dom["min_klasse"], 0) + 1
    # konsistens: treff med N/INGEN-klasse, eller ikke-treff med H-klasse — føres, rettes ikke
    res["inkonsistente"] = sorted(i for i, dom in lokal.items()
                                  if dom["ekte_treff"] != dom["min_klasse"].startswith("H"))
    res["bestått"] = res["kriterium"]["kappa"] >= OPPSETT["terskel_kappa"]
    res["klasse_leser"] = "godkjent leser" if res["bestått"] else "sil-klasse"
    (d / "maaling.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ut = {k: v_ for k, v_ in res.items() if k != "partier"}
    print(json.dumps(ut, ensure_ascii=False, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("kommando", choices=("kanari", "kjør", "mål"))
    a = p.parse_args(argv)
    return {"kanari": kanari, "kjør": kjør, "mål": mål}[a.kommando]()


if __name__ == "__main__":
    sys.exit(main())
