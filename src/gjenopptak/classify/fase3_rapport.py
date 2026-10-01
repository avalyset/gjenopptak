"""ADDENDUM-25 §5–§7: det ``fase3 maal`` ikke regner ut — recall-følsomhet, kostnad, klasser, felt-tetthet.

    PYTHONPATH=src python -m gjenopptak.classify.fase3_rapport --kjoring fase3-kjede

Leser bare. ``fase3.py``, ``ledd.py`` og ``cli.py`` er låst i ADDENDUM-25 §9 og røres ikke; denne modulen
importerer dem og regner på filene de har skrevet. Skriver ``fase3/rapport-fase3.json`` på Vault.

Sammenligningstallene for de 100 første er ADDENDUM-22 §10 (treff og dømt) og ``data/kjede/kandidat432``
(tekstbiter per felt, telt fra ``3-dommer.jsonl``). ADDENDUM-25 §7 sier «treff per 1 000 tekstbiter» uten å si
om nevneren er korpusets tekstbiter (ledd 2) eller de dømte i unionen; begge føres, ingen velges.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from ..vault import require_vault, sha256_file
from .fase3 import REPO, UT, _jsonl, _kjøring, _leserdommer, nå, wilson
from .liftability import format_liftable, liftable_share

#: ADDENDUM-22 §10 (treff, dømt) og kandidat432/3-dommer.jsonl (tekstbiter, verk).
FØRSTE_100 = {
    "arkeologi": {"treff": 274, "dømt": 990, "tekstbiter": 6741, "verk": 25},
    "alle": {"treff": 432, "dømt": 2844, "tekstbiter": 22243, "verk": 100},
}


def andel(k: int, n: int) -> dict:
    return {"k": k, "n": n, "andel": round(k / n, 3) if n else None, "wilson95": wilson(k, n)}


def tetthet(treff: int, dømt: int, tekstbiter: int, verk: int) -> dict:
    return {"treff": treff, "verk": verk, "treff_per_verk": round(treff / verk, 2),
            "treff_per_1000_korpus_tekstbiter": round(1000 * treff / tekstbiter, 1),
            "treff_per_1000_dømte": round(1000 * treff / dømt, 1),
            "tekstbiter": tekstbiter, "dømt": dømt}


def recall_følsomhet(ut: Path) -> dict:
    m = json.loads((ut / "maaling-fase3.json").read_text(encoding="utf-8"))
    nøkkel = _jsonl(ut / "referanse" / "NOKKEL-referansesett.jsonl")
    assert len(nøkkel) == len(m["rader"])
    rader = [{**r, "gyldig_spenn": h.get("gyldig_spenn")} for r, h in zip(m["rader"], nøkkel)]
    assert all(r["work_id"] == h["work_id"] and r["setninger"] == h["setninger"] for r, h in zip(rader, nøkkel))

    def to(rr: list[dict]) -> dict:
        return {"beholdt": andel(sum(r["beholdt"] for r in rr), len(rr)),
                "bekreftet": andel(sum(r["bekreftet"] for r in rr), len(rr))}
    return {"merknad": "følsomhet (ADDENDUM-25 §5), ikke port",
            "alle": to(rader),
            "uten_tvil": to([r for r in rader if not r["tvil"]]),
            "uten_ugyldig_spenn": to([r for r in rader if r["gyldig_spenn"] is not False])}


def recall_klynger(ut: Path) -> dict:
    """Referansetreffene er ikke uavhengige: de ligger i få verk, og ett verk kan bære halvparten. Wilson over
    treffene gir da for smale intervall. Føres som følsomhet (frys-lesning 4, 30.09.2026): per verk, uten det
    største verket, og snitt per verk."""
    rader = json.loads((ut / "maaling-fase3.json").read_text(encoding="utf-8"))["rader"]
    per = Counter(r["ref"] for r in rader)
    størst, n_størst = per.most_common(1)[0]
    uten = [r for r in rader if r["ref"] != størst]

    def snitt(felt: str) -> float:
        return round(sum(sum(r[felt] for r in rader if r["ref"] == v) / n for v, n in per.items()) / len(per), 3)
    return {"merknad": "følsomhet, ikke port; Wilson over treff antar uavhengighet mellom treff i samme verk",
            "verk_med_treff": len(per), "treff_per_verk": dict(per.most_common()),
            "største_verk": {"ref": størst, "treff": n_størst,
                             "beholdt": sum(r["beholdt"] for r in rader if r["ref"] == størst),
                             "bekreftet": sum(r["bekreftet"] for r in rader if r["ref"] == størst)},
            "uten_største": {"beholdt": andel(sum(r["beholdt"] for r in uten), len(uten)),
                             "bekreftet": andel(sum(r["bekreftet"] for r in uten), len(uten))},
            "snitt_per_verk": {"beholdt": snitt("beholdt"), "bekreftet": snitt("bekreftet")}}


def presisjon_følsomhet(ut: Path, dommer: list[dict]) -> dict | None:
    """Presisjonsporten brutt ned, ikke port: etter **leserens** tvil-flagg (som ADDENDUM-23 § 7.2), klasseenighet
    blant de bekreftede, og klassene instansen ga de avviste."""
    pd = ut / "presisjon"
    if not (pd / "verdikter-presisjon.jsonl").is_file():
        return None
    nk = {r["id"]: r for r in _jsonl(pd / "nokkel-presisjon.jsonl")}
    les = {d["id"]: d for d in dommer}
    vs = [(v, les[nk[v["id"]]["leser_id"]]) for v in _jsonl(pd / "verdikter-presisjon.jsonl")]
    bekreftet = [(v, l) for v, l in vs if v.get("treff") is True]

    def del_(f) -> dict:
        rr = [v for v, l in vs if f(l)]
        return andel(sum(1 for v in rr if v.get("treff") is True), len(rr))
    return {"merknad": "følsomhet, ikke port; tvil er leserens flagg, ikke presisjonsinstansens",
            "leser_tvil_false": del_(lambda l: not l.get("tvil")),
            "leser_tvil_true": del_(lambda l: bool(l.get("tvil"))),
            "samme_klasse_blant_bekreftede": andel(sum(1 for v, l in bekreftet if v["klasse"] == l["klasse"]),
                                                   len(bekreftet)),
            "avviste_klasser": dict(Counter(v["klasse"] for v, l in vs if v.get("treff") is not True).most_common()),
            "instansens_tvil": sum(1 for v, l in vs if v.get("tvil"))}


def klasser(treff: list[dict]) -> dict:
    """Klassefordeling og løftbarhet. ADDENDUM-05 § 4: løftbar andel har **avklarte** treff som nevner, uavklart
    andel **alle** treff, og de to oppgis alltid sammen — gjennom ``liftability``, ikke regnet her."""
    n = len(treff)
    kl = [d["klasse"] for d in treff]
    k = Counter(kl)
    ls = liftable_share(kl)
    return {"n": n, "fordeling": dict(k.most_common()),
            "H7": andel(k.get("H7", 0), n),
            "løftbar_av_avklarte": andel(ls["n_liftable"], ls["n_resolved"]),
            "uavklart_av_alle": andel(ls["n_unresolved"], ls["n_hits"]),
            "ikke_løftbar_av_avklarte": andel(ls["n_resolved"] - ls["n_liftable"], ls["n_resolved"]),
            "format_liftable": format_liftable(kl), "tabell": ls["table_version"],
            "tvil_blant_treff": andel(sum(1 for d in treff if d.get("tvil")), n)}


def _bruk(u: dict | str | None) -> dict:
    """``usage`` er ført som dict eller som ``str(dict)``; summerbare felt hentes ut."""
    if isinstance(u, str):
        import ast
        u = ast.literal_eval(u)
    u = u or {}
    felt = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
    return {f: int(u.get(f) or 0) for f in felt}


def _sum(rader: list[dict]) -> dict:
    s = Counter()
    for r in rader:
        s.update(_bruk(r.get("usage")))
    s["kontekst_inn"] = s["input_tokens"] + s["cache_creation_input_tokens"] + s["cache_read_input_tokens"]
    s["økter"] = len(rader)
    s["minutter"] = round(sum(float(r.get("minutter") or 0) for r in rader), 1)
    s["total_cost_usd_oppgitt"] = round(sum(float(r.get("total_cost_usd") or 0) for r in rader), 2)
    return dict(s)


#: Leserleddet overskriver forbrukslisten ved hver kjøring. Forbruket ligger derfor i tilstanden før flyttingen
#: (de 12 blokkerte øktene), i kopiene ``gjenoppta`` tok før hvert gjenopptak, i siste tilstand, og i loggene fra
#: fullføringene av delvise økter. Hver kilde bærer økt-statusene fra samme kjøring, så dømt per økt er kjent.
FLYTTET = REPO / "data" / "kjede" / "fase3-kjede.foer-flytting-2026-09-30" / "tilstand.json"


def leserøkter(ut: Path, kd: Path) -> list[dict]:
    kilder = [("blokkert (sandkasse)", FLYTTET)] if FLYTTET.is_file() else []
    kilder += [(p.stem.replace("tilstand-foer-gjenopptak-", "før "), p)
               for p in sorted(ut.glob("tilstand-foer-gjenopptak-*.json"))]
    kilder.append(("siste", kd / "tilstand.json"))
    sett, ut_ = {}, []
    for navn, p in kilder:
        les = json.loads(p.read_text(encoding="utf-8"))["ledd"].get("les") or {}
        status = {ø["okt"]: ø for ø in les.get("økter", [])}
        nøkkel = (les.get("tid"),)
        if nøkkel in sett:              # samme kjøring sett to ganger (kopi og siste)
            continue
        sett[nøkkel] = navn
        for f in les.get("forbruk", []):
            s = status.get(f.get("okt"), {})
            dømt = s.get("n") if s.get("status") == "ferdig" else s.get("dømt", 0)
            ut_.append({**f, "kilde": navn, "dømt": int(dømt or 0)})
    for lg in sorted((kd / "fullforing").glob("okt-*-rest*/logg.json")):
        d = json.loads(lg.read_text(encoding="utf-8"))
        ut_.append({**(d.get("bruk") or {}), "okt": f"{d['okt']}-rest{d['rest']}", "kilde": "fullføring",
                    "dømt": int(d.get("føyd_til") or 0)})
    return ut_


def modell_fra_utskrifter(katalog: Path) -> list[dict]:
    """Modell-ID per leserøkt fra Claude Codes øktutskrifter (RESULTAT-ADDENDUM-25 § 0.2): ``message.model`` for
    hver svarmelding, koblet til økta gjennom oppdragets første linje."""
    import hashlib
    import re
    ut = []
    for p in sorted(katalog.glob("*.jsonl")):
        første, tider, modeller = None, [], Counter()
        for l in p.read_text(encoding="utf-8").splitlines():
            try:
                d = json.loads(l)
            except ValueError:
                continue
            if d.get("timestamp"):
                tider.append(d["timestamp"])
            if første is None and d.get("type") == "queue-operation" and d.get("content"):
                første = d["content"]
            if d.get("type") == "assistant":
                modeller[(d.get("message") or {}).get("model")] += 1
        t = første or ""
        økt = re.search(r"økt (\d+) av 12", t)
        rest = re.search(r"fullforing/okt-(\d+)-rest(\d+)", t)
        ut.append({"utskrift": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                   "økt": (f"{økt.group(1)}-rest{rest.group(2)}" if rest else økt.group(1)) if økt else None,
                   "start": min(tider) if tider else None, "slutt": max(tider) if tider else None,
                   "modeller": dict(modeller)})
    return sorted(ut, key=lambda u: u["start"] or "")


def kostnad(ut: Path, kd: Path, tilstand: dict, leser_treff: int, presisjon: float | None) -> dict:
    ref = _sum([json.loads(p.read_text(encoding="utf-8")) for p in sorted((ut / "referanse" / "bruk").glob("*.json"))])
    økter = leserøkter(ut, kd)
    les = _sum([ø for ø in økter if ø["dømt"] > 0])
    spill = _sum([ø for ø in økter if ø["dømt"] == 0])
    pf = ut / "presisjon" / "bruk-presisjon.json"
    pres = _sum([json.loads(pf.read_text(encoding="utf-8"))]) if pf.is_file() else None
    # Dommeren fører ollamas total_duration (ns) per dom; ekstraksjonen fører veggtid (s) per vindu.
    ns = sum(int((r.get("bruk") or {}).get("total_duration") or 0) for r in _jsonl(kd / "3-dommer.jsonl"))
    s = sum(float(r.get("veggtid") or 0) for r in _jsonl(kd / "4-ekstraksjon.jsonl"))
    lokal = {"dommer": {"modelltid_timer": round(ns / 3.6e12, 2), "kilde": "sum bruk.total_duration i 3-dommer.jsonl"},
             "ekstraksjon": {"modelltid_timer": round(s / 3600, 2), "kilde": "sum veggtid i 4-ekstraksjon.jsonl"}}
    trekk = json.loads((ut / "trekkresultat-fase3.json").read_text(encoding="utf-8"))
    bekreftet = round(leser_treff * presisjon) if presisjon is not None else None
    per = None
    per_treff = {"leser_kontekst_inn": round(les["kontekst_inn"] / leser_treff)} if leser_treff else None
    if bekreftet:
        per = {navn: {"kontekst_inn": round(b["kontekst_inn"] / bekreftet), "output": round(b["output_tokens"] / bekreftet),
                      "minutter": round(b["minutter"] / bekreftet, 2)}
               for navn, b in (("referansesett", ref), ("leser", les), ("presisjonsport", pres)) if b}
    return {"openalex": {"kall": trekk.get("openalex_kall"), "remaining_etter": trekk.get("openalex_remaining"),
                         "remaining_før": None,
                         "merknad": "før-verdien ble ikke ført av trekkingen (draw_fase3.py, låst); avvik fra §6"},
            "lokal": lokal, "max_økter": {"referansesett": ref, "leser": les, "presisjonsport": pres,
                                          "leser_uten_dom": spill},
            "leserøkter": [{k: ø[k] for k in ("kilde", "okt", "dømt", "minutter", "is_error")} for ø in økter],
            "bekreftede_treff_skalert": bekreftet,
            "per_bekreftet_treff": per,
            "per_leser_treff": per_treff,
            "merknad": "per bekreftet treff = forbruk / (leserens treff × presisjon), ADDENDUM-25 §6; "
                       "total_cost_usd er claude -p sitt oppgitte API-ekvivalent, ikke fakturert på Max"}


def rapport(navn: str) -> dict:
    v = require_vault()
    ut = v / UT
    kd = _kjøring(navn)
    tilstand = json.loads((kd / "tilstand.json").read_text(encoding="utf-8"))
    dommer = _leserdommer(kd, v, navn)
    treff = [d for d in dommer if d.get("treff") is True]
    korpus = int(tilstand["ledd"]["tekstbiter"]["tekstbiter"])
    verk = int(tilstand["ledd"]["tekstbiter"]["verk"])
    m = json.loads((ut / "maaling-fase3.json").read_text(encoding="utf-8"))
    presisjon = (m.get("port1_presisjon") or {}).get("andel")
    per_verk = Counter(d["doc_id"] for d in treff)
    return {
        "tid": nå(), "kjøring": navn,
        "kilder": {"maaling-fase3.json": sha256_file(ut / "maaling-fase3.json"),
                   "tilstand.json": sha256_file(kd / "tilstand.json"),
                   "verdikter": {p.name: sha256_file(p) for p in sorted(kd.glob("7-verdikter-okt-*.jsonl"))}},
        "leser": {"dømt": len(dommer), "treff": andel(len(treff), len(dommer)),
                  "verk_med_treff": len(per_verk)},
        "recall_følsomhet": recall_følsomhet(ut),
        "recall_klynger": recall_klynger(ut),
        "bekreftet_blant_beholdte": andel(m["leser_gitt_beholdt"]["k"], m["leser_gitt_beholdt"]["n"]),
        "presisjon_følsomhet": presisjon_følsomhet(ut, dommer),
        "sil_andel_av_korpus": andel(int(tilstand["ledd"]["union"]["union"]), korpus),
        "klasser_blant_treff": klasser(treff),
        "felt_tetthet": {
            "fase3_arkeologi": tetthet(len(treff), len(dommer), korpus, verk),
            "første_100_arkeologi": tetthet(**FØRSTE_100["arkeologi"]),
            "første_100_alle": tetthet(**FØRSTE_100["alle"]),
            "merknad": "nevneren for «per 1 000 tekstbiter» er ikke gitt i §7; begge føres",
        },
        "kostnad": kostnad(ut, kd, tilstand, len(treff), presisjon),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--kjoring", default="fase3-kjede")
    a = p.parse_args(argv)
    r = rapport(a.kjoring)
    f = require_vault() / UT / "rapport-fase3.json"
    f.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: r[k] for k in ("leser", "klasser_blant_treff", "felt_tetthet")}, ensure_ascii=False, indent=1))
    print(f"sha256 {sha256_file(f)}  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
