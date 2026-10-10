"""Fase 4 (ADDENDUM-26): referansesett, nøkkelsikring, presisjonsport, recall med klyngefølsomhet, og
tilleggsmålet for løftbar andel.

    PYTHONPATH=src python -m gjenopptak.classify.fase4 referansetekst
    PYTHONPATH=src python -m gjenopptak.classify.fase4 referanseoppdrag
    PYTHONPATH=src python -m gjenopptak.classify.fase4 referanse-les
    PYTHONPATH=src python -m gjenopptak.classify.fase4 sikre-nokkel
    PYTHONPATH=src python -m gjenopptak.classify.fase4 presisjon-bygg
    PYTHONPATH=src python -m gjenopptak.classify.fase4 presisjon-les
    PYTHONPATH=src python -m gjenopptak.classify.fase4 maal

Samme form som fase 3 (``classify/fase3.py``, låst i ADDENDUM-25): samme regelfil, samme modell-ID, samme
oppdragsmaler med fase 4s stier, samme definisjon av *beholdt* og *bekreftet*. Tre forskjeller, låst i
ADDENDUM-26:

1. **Referanseleseren bekrefter siste setning.** Oppdraget ber om linjen ``LEST TIL: S<n>`` sist i svaret.
   Et verk er lest bare når den linjen nevner verkets siste setning og økten ikke endte med feil. Et
   avbrutt forsøk flyttes til ``referanse/avbrutt/`` og verket leses i sin helhet av en ny instans.
2. **Klyngefølsomhet i recall** er låst før data: verket (eller verkene, ved likt antall) med flest
   referansetreff tas ut, og snittet per verk rapporteres (fase 3 la dem til etter frys-lesning 4).
3. **Tilleggsmålet:** løftbar andel H1–H6 blant leserens avklarte treff, mot arkeologi i fase 3 (101 av 628),
   kandidatlista fra de første 100 (77 av 406) og tekstvitenskap-delen av den (3 av 35) — uten terskel.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

from ..vault import require_vault, sha256_file
from . import fase3 as F3
from .fase3 import MAKS_SPENN, MODELL, REGELFIL, _jsonl, dekker, nå, wilson

REPO = F3.REPO
UT = "fase4"
UTVALG = "utvalg-fase4-haandskrift.jsonl"
KJØRING = "fase4-kjede"
FRØ = 734248
N_PRESISJON = 100
PREFIKS = "P4"
TIDSAVBRUDD_S = 4 * 3600
#: Sammenligningsgrunnlaget for tilleggsmålet: løftbar H1–H6 av avklarte (ADDENDUM-26 § 5). Arkeologi i fase 3 og
#: hele kandidatlista fra RESULTAT-ADDENDUM-25 § 1.3; tekstvitenskap-delen av kandidatlista regnet 02.10.2026 fra
#: register v2 (`kandidat432/8-register.jsonl`, sha256 c6895202…, feltet `obstacle_class`, `liftable_share`) —
#: samme regning gir 77/406 for hele lista.
SAMMENLIGNING = {"arkeologi_fase3": (101, 628), "første_100_kandidatlista": (77, 406),
                 "tekstvitenskap_første_runde": (3, 35)}

_SLUTT_GML = "Les hele verket. Ikke stopp før siste setning.\n"
_SLUTT_NY = (_SLUTT_GML + "\n**Siste linje i svaret ditt** skal være `LEST TIL: S<nummer>`, med nummeret på den "
             "siste setningen du faktisk leste.\n")
assert F3.OPPDRAG.count(_SLUTT_GML) == 1
OPPDRAG = F3.OPPDRAG.replace(_SLUTT_GML, _SLUTT_NY)
assert F3.PRESISJON_OPPDRAG.count('"id": "P3-001"') == 1
PRESISJON_OPPDRAG = F3.PRESISJON_OPPDRAG.replace('"id": "P3-001"', f'"id": "{PREFIKS}-001"')
_LEST_TIL = re.compile(r"LEST TIL:\s*S(\d+)")


def referansetekst() -> int:
    v = require_vault()
    ut = v / UT
    ref = json.loads((ut / "referanse-verk.json").read_text(encoding="utf-8"))["verk"]
    utv = {r["work_id"]: r for r in _jsonl(ut / UTVALG)}
    td = ut / "referanse" / "tekst"
    td.mkdir(parents=True, exist_ok=True)
    tmp = REPO / "data" / "tmp-fase4"
    tmp.mkdir(parents=True, exist_ok=True)
    rader = []
    for i, wid in enumerate(ref, 1):
        rows = F3.setninger(v, utv[wid], tmp)
        f = td / f"R{i:02d}.txt"
        f.write_text("\n".join(f"S{r['sentence_index']}: {r['text']}" for r in rows) + "\n", encoding="utf-8")
        rader.append({"ref": f"R{i:02d}", "work_id": wid, "setninger": len(rows),
                      "siste": max((r["sentence_index"] for r in rows), default=None),
                      "tegn": sum(len(r["text"]) for r in rows), "fil": f.name, "sha256": sha256_file(f)})
        print(f"R{i:02d} {wid}: {len(rows)} setninger")
    (ut / "referanse" / "tekster.json").write_text(json.dumps(rader, ensure_ascii=False, indent=1) + "\n",
                                                   encoding="utf-8")
    return 0


def referanseoppdrag() -> int:
    v = require_vault()
    ut = v / UT
    tekster = json.loads((ut / "referanse" / "tekster.json").read_text(encoding="utf-8"))
    od = ut / "referanse" / "oppdrag"
    od.mkdir(parents=True, exist_ok=True)
    (ut / "referanse" / "treff").mkdir(parents=True, exist_ok=True)
    for t in tekster:
        o = OPPDRAG.format(
            KLADD=ut / "referanse" / "kladd" / t["ref"], REGLER=v / REGELFIL,
            TEKST=ut / "referanse" / "tekst" / t["fil"], N=t["setninger"], REPO=REPO, VAULT=v, UT=UT,
            MAKS=MAKS_SPENN, MAKS1=MAKS_SPENN - 1, WID=t["work_id"], REF=t["ref"],
            UTFIL=ut / "referanse" / "treff" / f"{t['ref']}.jsonl")
        (od / f"oppdrag-{t['ref']}.md").write_text(o, encoding="utf-8")
    print(f"{len(tekster)} oppdrag i {od}")
    return 0


def lest_til(resultat: str | None) -> int | None:
    """Setningsnummeret i den siste ``LEST TIL: S<n>``-linjen i svaret, eller None."""
    funn = _LEST_TIL.findall(resultat or "")
    return int(funn[-1]) if funn else None


def ferdig_lest(bruk: dict, siste: int | None) -> bool:
    return (not bruk.get("is_error") and bool(bruk.get("treffil_finnes")) and siste is not None
            and bruk.get("lest_til") == siste)


def _sett_til_side(ut: Path, ref: str) -> Path:
    """Flytt et avbrutt forsøk (treffil og brukslogg) til ``referanse/avbrutt/<ref>-<k>/``. Telles ikke."""
    ad = ut / "referanse" / "avbrutt"
    k = 1 + len(list(ad.glob(f"{ref}-*"))) if ad.is_dir() else 1
    d = ad / f"{ref}-{k}"
    d.mkdir(parents=True)
    for p in (ut / "referanse" / "treff" / f"{ref}.jsonl", ut / "referanse" / "bruk" / f"{ref}.json"):
        if p.is_file():
            p.rename(d / p.name)
    return d


def referanse_les() -> int:
    """Én ``claude -p``-instans per verk, serielt, arbeidskatalog på Vault utenfor repoet, ingen MCP. Et verk
    er ferdig bare når svaret bekrefter siste setning. Et avbrutt forsøk settes til side, og kjøringen
    stopper (rc 2); neste kall leser verket på nytt i en ny instans."""
    import subprocess
    import time
    v = require_vault()
    ut = v / UT
    tekster = json.loads((ut / "referanse" / "tekster.json").read_text(encoding="utf-8"))
    bd = ut / "referanse" / "bruk"
    bd.mkdir(parents=True, exist_ok=True)
    for t in tekster:
        ref = t["ref"]
        treff, bruk = ut / "referanse" / "treff" / f"{ref}.jsonl", bd / f"{ref}.json"
        if bruk.is_file():
            if ferdig_lest(json.loads(bruk.read_text(encoding="utf-8")), t["siste"]):
                print(f"{ref}: ferdig, hopper over")
                continue
            print(f"{ref}: forrige forsøk er ikke ferdig — settes til side i {_sett_til_side(ut, ref)}")
        elif treff.is_file():
            print(f"{ref}: treffil uten brukslogg — settes til side i {_sett_til_side(ut, ref)}")
        kladd = ut / "referanse" / "kladd" / ref
        kladd.mkdir(parents=True, exist_ok=True)
        oppdrag = (ut / "referanse" / "oppdrag" / f"oppdrag-{ref}.md").read_text(encoding="utf-8")
        t0 = time.time()
        r = subprocess.run(["claude", "-p", "--model", MODELL, "--output-format", "json",
                            "--permission-mode", "acceptEdits", "--strict-mcp-config",
                            "--add-dir", str(v)], cwd=kladd, capture_output=True, text=True,
                           timeout=TIDSAVBRUDD_S, input=oppdrag)
        try:
            svar = json.loads(r.stdout)
        except ValueError:
            svar = {"is_error": True, "result": "kunne ikke lese JSON", "stderr": r.stderr[-400:]}
        rad = {"ref": ref, "work_id": t["work_id"], "modell": MODELL, "start": nå(),
               "minutter": round((time.time() - t0) / 60, 1), "is_error": svar.get("is_error"),
               "usage": svar.get("usage"), "modelUsage": svar.get("modelUsage"),
               "num_turns": svar.get("num_turns"), "total_cost_usd": svar.get("total_cost_usd"),
               "resultat": str(svar.get("result"))[:1500], "lest_til": lest_til(svar.get("result")),
               "siste": t["siste"], "treffil_finnes": treff.is_file(),
               "treff": len(_jsonl(treff)) if treff.is_file() else None}
        bruk.write_text(json.dumps(rad, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{ref} {t['work_id']}: {rad['treff']} treff, lest til S{rad['lest_til']} av S{t['siste']}, "
              f"{rad['minutter']} min, feil={rad['is_error']}", flush=True)
        if not ferdig_lest(rad, t["siste"]):
            print(f"STOPP ved {ref}: økten feilet, skrev ingen treffil eller bekreftet ikke siste setning",
                  file=sys.stderr)
            return 2
    return 0


def sikre_nokkel() -> int:
    """Samle referansetreffene til én nøkkel, sha256 i manifestet, ots-stempel. Før silen."""
    from ..tidsstempel import stamp
    v = require_vault()
    ut = v / UT
    tekster = json.loads((ut / "referanse" / "tekster.json").read_text(encoding="utf-8"))
    rader, mangler = [], []
    for t in tekster:
        f = ut / "referanse" / "treff" / f"{t['ref']}.jsonl"
        b = ut / "referanse" / "bruk" / f"{t['ref']}.json"
        if not (f.is_file() and b.is_file() and ferdig_lest(json.loads(b.read_text(encoding="utf-8")), t["siste"])):
            mangler.append(t["ref"])
            continue
        for r in _jsonl(f):
            s = sorted(int(x) for x in r["setninger"])
            rader.append({**r, "work_id": t["work_id"], "ref": t["ref"], "setninger": s,
                          "gyldig_spenn": (s[-1] - s[0]) <= MAKS_SPENN - 1 if s else False})
    if mangler:
        raise SystemExit(f"STOPP — ikke ferdig lest: {mangler}; nøkkelen sikres ikke ufullstendig")
    nf = ut / "referanse" / "NOKKEL-referansesett.jsonl"
    if nf.exists():
        raise SystemExit("nøkkelen finnes alt — skrives ikke om")
    nf.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rader), encoding="utf-8")
    sha = sha256_file(nf)
    st = stamp(nf, ut_dir=ut / "referanse" / "ots")
    with (v / "MANIFEST-VAULT.md").open("a", encoding="utf-8") as fh:
        fh.write(f"\n## Fase 4: referansenøkkel sikret før silen, {nå()}\n\n"
                 f"| sti | bytes | sha256 | sikret | kilde-URL | merknad |\n|---|---|---|---|---|---|\n"
                 f"| {UT}/referanse/{nf.name} | {nf.stat().st_size} | {sha} | {nå()} | — | "
                 f"{len(rader)} referansetreff fra {len(tekster)} verk (ADDENDUM-26 § 3); "
                 f"ots: {'ok' if st.ok else st.feil} |\n")
    print(json.dumps({"treff": len(rader), "verk": len(tekster), "sha256": sha,
                      "ugyldig_spenn": sum(not r["gyldig_spenn"] for r in rader),
                      "ots": str(st.kvittering) if st.ok else st.feil}, ensure_ascii=False))
    return 0


def kjøringsdir(v: Path, navn: str = KJØRING) -> Path:
    """Kjøringens katalog: i fasens worktree på Vault (ADDENDUM-26 § 4), nøyaktig ett."""
    treff = sorted((v / UT).glob(f"worktree-*/data/kjede/{navn}"))
    if len(treff) != 1:
        raise SystemExit(f"fant {len(treff)} kjøringskataloger for {navn} under {v / UT}/worktree-*")
    return treff[0]


def _leserdommer(kd: Path, v: Path, navn: str) -> list[dict]:
    nøkkel = {r["id"]: r for r in _jsonl(v / navn / "nokkel.jsonl")}
    return [{**nøkkel[r["id"]], **r} for f in sorted(kd.glob("7-verdikter-okt-*.jsonl")) for r in _jsonl(f)]


def presisjon_bygg(navn: str = KJØRING) -> int:
    v = require_vault()
    kd = kjøringsdir(v, navn)
    treff = [d for d in _leserdommer(kd, v, navn) if d.get("treff") is True]
    n = min(N_PRESISJON, len(treff))
    utvalg = random.Random(FRØ).sample(sorted(treff, key=lambda d: d["id"]), n)
    tekst = {r["id"]: r["tekst"] for f in sorted((kd / "blind").glob("blind-okt-*.jsonl")) for r in _jsonl(f)}
    pd = v / UT / "presisjon"
    pd.mkdir(parents=True, exist_ok=True)
    if (pd / "blind-presisjon.jsonl").exists():
        raise SystemExit("blindfila for presisjonsporten finnes alt — trekkes ikke om")
    blind = [{"id": f"{PREFIKS}-{i:03d}", "tekst": tekst[d["id"]]} for i, d in enumerate(utvalg, 1)]
    nøkkel = [{"id": f"{PREFIKS}-{i:03d}", "leser_id": d["id"], "doc_id": d["doc_id"],
               "start_index": d["start_index"], "end_index": d["end_index"]} for i, d in enumerate(utvalg, 1)]
    (pd / "blind-presisjon.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in blind),
                                              encoding="utf-8")
    (pd / "nokkel-presisjon.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in nøkkel),
                                               encoding="utf-8")
    print(json.dumps({"leser_treff": len(treff), "trukket": n, "frø": FRØ,
                      "blind_sha256": sha256_file(pd / "blind-presisjon.jsonl"),
                      "nokkel_sha256": sha256_file(pd / "nokkel-presisjon.jsonl")}, ensure_ascii=False))
    return 0


def presisjon_les() -> int:
    """Presisjonsporten: én separat instans, arbeidskatalog på Vault utenfor repoet."""
    import subprocess
    import time
    v = require_vault()
    pd = v / UT / "presisjon"
    blind = pd / "blind-presisjon.jsonl"
    n = len(_jsonl(blind))
    utfil = pd / "verdikter-presisjon.jsonl"
    if utfil.is_file():
        print("verdiktfilen finnes — kjøres ikke om", file=sys.stderr)
        return 2
    kladd = pd / "kladd"
    kladd.mkdir(parents=True, exist_ok=True)
    o = PRESISJON_OPPDRAG.format(N=n, KLADD=kladd, REGLER=v / REGELFIL, BLIND=blind, REPO=REPO,
                                 VAULT=v, UT=UT, UTFIL=utfil)
    (pd / "oppdrag-presisjon.md").write_text(o, encoding="utf-8")
    t0 = time.time()
    r = subprocess.run(["claude", "-p", "--model", MODELL, "--output-format", "json",
                        "--permission-mode", "acceptEdits", "--strict-mcp-config", "--add-dir", str(v)],
                       cwd=kladd, capture_output=True, text=True, timeout=TIDSAVBRUDD_S, input=o)
    try:
        svar = json.loads(r.stdout)
    except ValueError:
        svar = {"is_error": True, "result": "kunne ikke lese JSON", "stderr": r.stderr[-400:]}
    rad = {"modell": MODELL, "minutter": round((time.time() - t0) / 60, 1),
           "is_error": svar.get("is_error"), "usage": svar.get("usage"),
           "modelUsage": svar.get("modelUsage"), "num_turns": svar.get("num_turns"),
           "total_cost_usd": svar.get("total_cost_usd"), "resultat": str(svar.get("result"))[:1500],
           "dømt": len(_jsonl(utfil)) if utfil.is_file() else 0, "av": n}
    (pd / "bruk-presisjon.json").write_text(json.dumps(rad, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: rad[k] for k in ("minutter", "is_error", "dømt", "av")}, ensure_ascii=False))
    return 0 if rad["dømt"] == n else 2


def _andel(k: int, n: int) -> dict:
    return {"k": k, "n": n, "andel": round(k / n, 3) if n else None, "wilson95": wilson(k, n)}


def recall(nøkkel: list[dict], union: list[dict], dommer: dict) -> tuple[list[dict], dict]:
    """Beholdt og bekreftet per referansetreff (ADDENDUM-25 § 5, uendret), med klyngefølsomheten fra
    ADDENDUM-26 § 5: uten verket/verkene med flest referansetreff, og snittet per verk."""
    per_verk: dict[str, list[dict]] = {}
    for u in union:
        per_verk.setdefault(u["doc_id"], []).append(u)
    rader = []
    for h in nøkkel:
        s = h["setninger"]
        dek = [u for u in per_verk.get(h["work_id"], []) if dekker(u, s)]
        bk = [u for u in dek if (dommer.get((u["doc_id"], u["start_index"], u["end_index"])) or {}).get("treff") is True]
        rader.append({"ref": h["ref"], "work_id": h["work_id"], "setninger": s, "klasse": h.get("klasse"),
                      "tvil": h.get("tvil"), "gyldig_spenn": h.get("gyldig_spenn"), "beholdt": bool(dek),
                      "bekreftet": bool(bk), "kilder": sorted({u["kilde"] for u in dek})})

    def tall(rr: list[dict]) -> dict:
        b = sum(r["beholdt"] for r in rr)
        k = sum(r["bekreftet"] for r in rr)
        return {"beholdt": _andel(b, len(rr)), "bekreftet": _andel(k, len(rr)),
                "bekreftet_blant_beholdte": _andel(k, b)}

    antall: dict[str, int] = {}
    for r in rader:
        antall[r["work_id"]] = antall.get(r["work_id"], 0) + 1
    maks = max(antall.values(), default=0)
    ute = sorted(w for w, n in antall.items() if n == maks) if maks else []
    snitt = {}
    for felt in ("beholdt", "bekreftet"):
        andeler = [sum(r[felt] for r in rader if r["work_id"] == w) / n for w, n in antall.items()]
        snitt[felt] = round(sum(andeler) / len(andeler), 3) if andeler else None
    res = {"alle": tall(rader),
           "uten_tvil": tall([r for r in rader if not r["tvil"]]),
           "uten_ugyldig_spenn": tall([r for r in rader if r["gyldig_spenn"] is not False]),
           "klynger": {"verk_med_treff": len(antall), "flest_treff": maks, "tatt_ut": ute,
                       "uten_største": tall([r for r in rader if r["work_id"] not in ute]),
                       "snitt_per_verk": snitt}}
    return rader, res


def tillegg_loftbar(klasser: list[str]) -> dict:
    """Løftbar andel H1–H6 av avklarte treff (ADDENDUM-05 § 4), mot fase 3 og de første 100. Uten terskel."""
    from .liftability import format_liftable, liftable_share
    ls = liftable_share(klasser)
    ut = {"løftbar_av_avklarte": _andel(ls["n_liftable"], ls["n_resolved"]),
          "uavklart_av_alle": _andel(len(klasser) - ls["n_resolved"], len(klasser)),
          "format_liftable": format_liftable(klasser), "terskel": None, "sammenligning": {}}
    for navn, (k, n) in SAMMENLIGNING.items():
        p4 = ut["løftbar_av_avklarte"]["andel"]
        ut["sammenligning"][navn] = {**_andel(k, n), "differanse_fase4_minus":
                                     round(p4 - k / n, 3) if p4 is not None else None}
    return ut


def maal(navn: str = KJØRING) -> int:
    v = require_vault()
    kd = kjøringsdir(v, navn)
    ut = v / UT
    nøkkel = _jsonl(ut / "referanse" / "NOKKEL-referansesett.jsonl")
    leser = _leserdommer(kd, v, navn)
    dommer = {(d["doc_id"], d["start_index"], d["end_index"]): d for d in leser}
    rader, rec = recall(nøkkel, _jsonl(kd / "5-union.jsonl"), dommer)
    treff = [d for d in leser if d.get("treff") is True]
    res = {"tid": nå(), "kjøring": navn, "kjøringsdir": str(kd),
           "referanse": {"verk": len({t["work_id"] for t in json.loads((ut / "referanse" / "tekster.json").read_text())}),
                         "treff": len(nøkkel), "treff_uten_tvil": sum(1 for h in nøkkel if not h.get("tvil")),
                         "ugyldig_spenn": sum(1 for h in nøkkel if not h.get("gyldig_spenn"))},
           "port2_recall": rec,
           "leser": {"dømt": len(leser), "treff": len(treff), "verk_med_treff": len({d["doc_id"] for d in treff})},
           "tillegg_loftbar": tillegg_loftbar([d["klasse"] for d in treff])}
    pv = ut / "presisjon" / "verdikter-presisjon.jsonl"
    if pv.is_file():
        vs = _jsonl(pv)
        k = sum(1 for r in vs if r.get("treff") is True)
        res["port1_presisjon"] = {**_andel(k, len(vs)), "terskel": 0.70, "bestått": k / len(vs) >= 0.70}
        res["navn"] = "arbeidsliste (prospektiv port)" if res["port1_presisjon"]["bestått"] else "kandidatliste"
    (ut / "maaling-fase4.json").write_text(json.dumps({**res, "rader": rader}, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("kommando", choices=("referansetekst", "referanseoppdrag", "referanse-les", "sikre-nokkel",
                                        "presisjon-bygg", "presisjon-les", "maal"))
    p.add_argument("--kjoring", default=KJØRING)
    a = p.parse_args(argv)
    return {"referansetekst": referansetekst, "referanseoppdrag": referanseoppdrag,
            "referanse-les": referanse_les, "sikre-nokkel": sikre_nokkel, "presisjon-les": presisjon_les,
            "presisjon-bygg": lambda: presisjon_bygg(a.kjoring), "maal": lambda: maal(a.kjoring)}[a.kommando]()


if __name__ == "__main__":
    sys.exit(main())
