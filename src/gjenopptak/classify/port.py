"""Porten: L1 + L2 + dommer A på de hundre trukne verkene. Ingen OpenAlex-kall.

L1 parser hvert verk fra Vault (JATS eller PDF) til setninger med seksjonsetikett og
proveniens. L2 deler hele teksten i passasjer på ±2 setninger — **ingen markørfiltrering**
(LAERDOM §1: det leksikalske førsteleddet er forkastet). Hver passasje dømmes av dommer A
med ledetekst `l3-poc-v1-system.txt`, uendret fra målingen som ga 95,7 % presisjon.

For hvert treff kjøres ett oppfølgingskall med egen ledetekst: står det ugjorte og hindringen
i samme setning (enheten i ADDENDUM-03 §1.2), og lar «er hindringen opphevet i dag» seg avgjøre
uten domeneekspert (M2 i PREREG §2). Oppfølgingen er et eget kall nettopp for at ledetekst A
skal stå urørt.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from . import l3poc as P

UT = Path("data/port")
PROMPT_A = Path("src/gjenopptak/classify/prompts/l3-poc-v1-system.txt")
PROMPT_OPPF = Path("src/gjenopptak/classify/prompts/port-oppfolging-v1-system.txt")
FELT = ("energimodellering", "arkeologi", "klinisk_epidemiologi", "tekstvitenskap")
WINDOW = 2
#: Steg 3 er det minste som bevarer ±2-paringen: to setninger med avstand ≤ 2 havner alltid
#: i samme vindu. Steg 5 ser hver setning én gang, men deler par over vindusgrensen.
STRIDE = 3

OPPF_SCHEMA = {
    "type": "object",
    "properties": {
        "begrunnelse": {"type": "string"},
        "samme_setning": {"type": "boolean"},
        "bedømbar": {"type": "string", "enum": ["ja", "nei", "usikker"]},
    },
    "required": ["begrunnelse", "samme_setning", "bedømbar"],
}

OPPF_PROMPT = """Du er koder i forskningsprosjektet «gjenopptak». Du får én passasje som alt er kodet som et parkert spørsmål: forfatteren navngir noe de ikke fikk gjort, og oppgir en hindring. Du skal svare på to spørsmål om passasjen. Svar bare med JSON etter skjemaet til slutt.

## 1 Enheten
Står det ugjorte og hindringen i **samme setning**? Sett `samme_setning` til true bare da. Står de i ulike setninger innenfor passasjen, settes den til false.

## 2 Bedømbarhet
Lar spørsmålet «er hindringen opphevet i dag» seg avgjøre **uten domeneekspert i faget**?

- `ja`: en leser uten fagbakgrunn kan avgjøre det, fordi hindringen er av en art som kan sjekkes generelt — for eksempel om et verktøy, en metode eller en datakilde finnes i dag.
- `nei`: det krever fagkunnskap i feltet å avgjøre om hindringen er borte.
- `usikker`: passasjen gir ikke nok til å avgjøre hvilken av de to det er.

Du skal ikke avgjøre om hindringen faktisk er opphevet, bare om spørsmålet lar seg avgjøre uten domeneekspert.

## Svar
Svar med JSON: {"begrunnelse": "høyst to setninger", "samme_setning": true eller false, "bedømbar": "ja, nei eller usikker"}.
"""


# --------------------------------------------------------------------------- #
# L1 + L2
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Passasje:
    doc_id: str
    felt: str
    start_index: int
    end_index: int
    senter_index: int
    section_raw: str
    section_label_provenance: str
    seksjoner_i_vindu: tuple
    tekst: str

    def nøkkel(self) -> str:
        return f"{self.doc_id}:{self.start_index}"


def passasjer(rows: Sequence[dict], felt: str, *, stride: int = STRIDE, window: int = WINDOW) -> list[Passasje]:
    """Hele teksten i passasjer på ±``window`` setninger, med ``stride`` mellom sentrene."""
    ut: list[Passasje] = []
    n = len(rows)
    if not n:
        return ut
    for c in range(window, max(window + 1, n - window), stride):
        lo, hi = max(0, c - window), min(n - 1, c + window)
        vindu = rows[lo:hi + 1]
        ut.append(Passasje(
            doc_id=rows[0]["doc_id"], felt=felt, start_index=rows[lo]["sentence_index"],
            end_index=rows[hi]["sentence_index"], senter_index=rows[c]["sentence_index"],
            section_raw=rows[c].get("section_raw") or "",
            section_label_provenance=rows[c].get("section_label_provenance") or "parser",
            seksjoner_i_vindu=tuple(sorted({(r.get("section_raw") or "") for r in vindu})),
            tekst=" ".join(r["text"] for r in vindu)))
    if ut and ut[-1].end_index < rows[-1]["sentence_index"]:
        lo = max(0, n - (2 * window + 1))
        ut.append(Passasje(
            doc_id=rows[0]["doc_id"], felt=felt, start_index=rows[lo]["sentence_index"],
            end_index=rows[-1]["sentence_index"], senter_index=rows[min(lo + window, n - 1)]["sentence_index"],
            section_raw=rows[min(lo + window, n - 1)].get("section_raw") or "",
            section_label_provenance=rows[min(lo + window, n - 1)].get("section_label_provenance") or "parser",
            seksjoner_i_vindu=tuple(sorted({(r.get("section_raw") or "") for r in rows[lo:]})),
            tekst=" ".join(r["text"] for r in rows[lo:])))
    return ut


def dekker_alle_setninger(ps: Sequence[Passasje], n_sentences: int) -> bool:
    sett = {i for p in ps for i in range(p.start_index, p.end_index + 1)}
    return sett == set(range(n_sentences))


# --------------------------------------------------------------------------- #
# Aggregering
# --------------------------------------------------------------------------- #

def treff_per_verk(dommer: Iterable[dict]) -> dict[str, list[dict]]:
    ut: dict[str, list[dict]] = {}
    for d in dommer:
        if d.get("klasse") in P.HIT_CLASSES:
            ut.setdefault(d["doc_id"], []).append(d)
    return ut


def m1(verk: Sequence[dict], treff: dict[str, list[dict]], *, streng: bool) -> dict:
    """M1 som andel verk med minst ett treff. ``streng`` krever samme setning (ADDENDUM-03 §1.2)."""
    med = 0
    for v in verk:
        t = treff.get(v["work_id"], [])
        if streng:
            t = [x for x in t if x.get("samme_setning") is True]
        med += bool(t)
    n = len(verk)
    return {"n_verk": n, "verk_med_treff": med, "M1": med / n if n else None}


def m2(treff_rader: Sequence[dict]) -> dict:
    """M2: andel treff der «er hindringen opphevet» lar seg avgjøre uten domeneekspert."""
    b = Counter(t.get("bedømbar_endelig") or t.get("bedømbar") for t in treff_rader)
    n = len(treff_rader)
    return {"n_treff": n, "ja": b["ja"], "nei": b["nei"], "usikker": b["usikker"],
            "M2": (b["ja"] / n) if n else None,
            "M2_uten_usikre": (b["ja"] / (b["ja"] + b["nei"])) if (b["ja"] + b["nei"]) else None}


# --------------------------------------------------------------------------- #
# Presisjonssett
# --------------------------------------------------------------------------- #

N_TREFF = 150
N_INGEN = 50
N_N3 = 50
GULV = {"tekstvitenskap": 25}


def feltkvoter(rader: Sequence[dict], n: int, gulv: dict[str, int]) -> dict[str, int]:
    """Antall per felt: proporsjonalt, men med et gulv for felt som ellers blir for tynne.

    Gulvet er en måleskranke, ikke en vekting av materialet: et felt med for få leste treff kan
    ikke få presisjon målt separat. Feltet låses på gulvet (eller på alt det har, om det har
    mindre), og resten fordeles proporsjonalt mellom de andre feltene med største rest.
    """
    tell = Counter(r["felt"] for r in rader)
    if not tell:
        return {}
    låst = {}
    for f, g in gulv.items():
        krav = min(g, tell.get(f, 0))
        if krav and n * tell.get(f, 0) / len(rader) < krav:
            låst[f] = krav
    rest = n - sum(låst.values())
    andre = {f: c for f, c in tell.items() if f not in låst}
    N = sum(andre.values())
    kvote = {f: min(andre[f], int(rest * andre[f] / N)) for f in andre} if N else {}
    navn = sorted(kvote)
    i = 0
    rekke = sorted(navn, key=lambda f: (-(rest * andre[f] / N - kvote[f]), f)) if navn else []
    while rekke and sum(kvote.values()) < min(rest, N):
        f = rekke[i % len(rekke)]
        if kvote[f] < andre[f]:
            kvote[f] += 1
        i += 1
    return {**låst, **{f: k for f, k in kvote.items() if k}}


def _fordel(k: int, bøtter: dict, mål: dict) -> dict:
    """``k`` plasser fordelt på bøtter etter måltettheten, kappet av det bøttene faktisk har.

    Aksen er ordinal, så krav en tom bøtte ikke kan dekke, flyttes til nærmeste bøtte som har
    rader — ikke jevnt utover. Ved lik avstand velges den lengre bøtta, fordi skjevheten som
    skal dempes går mot for korte passasjer.
    """
    ideal = {b: k * mål.get(b, 0.0) for b in mål} | {b: k * mål.get(b, 0.0) for b in bøtter}
    alloc = {b: min(len(bøtter[b]), int(ideal.get(b, 0.0))) for b in bøtter}
    krav = {b: ideal[b] - alloc.get(b, 0) for b in ideal}
    tak = min(k, sum(len(g) for g in bøtter.values()))
    while sum(alloc.values()) < tak:
        kand = [b for b in sorted(bøtter) if alloc[b] < len(bøtter[b])]
        b = max(sorted(krav), key=lambda b: (krav[b], -b))
        mottaker = min(kand, key=lambda c: (abs(c - b), -c))
        alloc[mottaker] += 1
        krav[b] -= 1
    return alloc


def stratifisert(rader: Sequence[dict], n: int, nøkkel, seed: int = P.MAALEFRO,
                 sekundær=None, mål: dict | None = None) -> list[dict]:
    """``n`` rader fordelt proporsjonalt på strata, med største rest, trukket med målefrøet.

    ``sekundær`` er en underordnet akse (f.eks. lengdekvartil) som fordeles *innenfor* hvert
    stratum mot tettheten i ``mål``. Stratumkvotene røres ikke, så den underordnede aksen kan
    aldri bryte den overordnede — den omfordeler bare hvilke rader som trekkes i hver celle.
    """
    import random
    grupper: dict = {}
    for r in rader:
        grupper.setdefault(nøkkel(r), []).append(r)
    navn = sorted(grupper)
    N = len(rader)
    kvote = {k: min(len(grupper[k]), int(n * len(grupper[k]) / N)) for k in navn}
    rest = sorted(navn, key=lambda k: (-(n * len(grupper[k]) / N - kvote[k]), k))
    i = 0
    while sum(kvote.values()) < min(n, N):
        k = rest[i % len(rest)]
        if kvote[k] < len(grupper[k]):
            kvote[k] += 1
        i += 1
    rng = random.Random(seed)
    ut: list[dict] = []
    for k in navn:
        if not kvote[k]:
            continue
        if sekundær is None:
            ut += rng.sample(grupper[k], kvote[k])
            continue
        bøtter: dict = {}
        for r in grupper[k]:
            bøtter.setdefault(sekundær(r), []).append(r)
        alloc = _fordel(kvote[k], bøtter, mål or {})
        for b in sorted(bøtter):
            if alloc[b]:
                ut += rng.sample(bøtter[b], alloc[b])
    ut.sort(key=lambda r: (r["doc_id"], r["start_index"]))
    return ut


def lengdegrenser(ankere: Sequence[dict]) -> tuple[float, float, float]:
    """Kvartilgrensene i tegn, regnet på ankernes lengdefordeling."""
    L = sorted(len(a["tekst"]) for a in ankere)
    return tuple(_kvantil(L, q) for q in (0.25, 0.5, 0.75))  # type: ignore[return-value]


def _kvantil(sortert: Sequence[float], q: float) -> float:
    if not sortert:
        return 0.0
    i = (len(sortert) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(sortert) - 1)
    return sortert[lo] + (sortert[hi] - sortert[lo]) * (i - lo)


def kvartil(lengde: int, grenser: tuple[float, float, float]) -> int:
    """0–3: hvilken av ankernes lengdekvartiler en passasje faller i."""
    return sum(1 for g in grenser if lengde > g)


def lengdemål(ankere: Sequence[dict], grenser: tuple[float, float, float]) -> dict[int, float]:
    """Måltettheten portradene skal treffe: ankernes egen fordeling over de fire kvartilene."""
    tell = Counter(kvartil(len(a["tekst"]), grenser) for a in ankere)
    return {b: tell.get(b, 0) / len(ankere) for b in range(4)}


def presisjon(fasit: Sequence[dict], vekter: dict[str, int] | None = None) -> dict:
    """Presisjon per felt og per dømt klasse, og hva de falske treffene ble dømt som.

    ``vekter`` er antallet dømte passasjer per ikke-treff-klasse i portmaterialet, og brukes
    bare til den vektede bomraten. De tre bomratene rapporteres hver for seg og slås aldri sammen.
    """
    treff = [f for f in fasit if f["utvalgstype"] == "treff"]
    ekte = [f for f in treff if f["ekte_treff"]]
    falske = [f for f in treff if not f["ekte_treff"]]
    per_felt, per_klasse = {}, {}
    for nøkkel, mål in (("felt", per_felt), ("dømt_klasse", per_klasse)):
        for f in treff:
            b = mål.setdefault(f[nøkkel], {"n": 0, "ekte": 0})
            b["n"] += 1
            b["ekte"] += bool(f["ekte_treff"])
        for b in mål.values():
            b["presisjon"] = b["ekte"] / b["n"] if b["n"] else None
    h7h8 = [f for f in falske if f["dømt_klasse"] in ("H7", "H8")]
    ingen = [f for f in fasit if f["utvalgstype"] == "ingen"]
    funnet = [f for f in ingen if f["ekte_treff"]]
    return {
        "ikke_treff": _ikke_treff(fasit, vekter or {}),
        "n_treff_lest": len(treff), "ekte": len(ekte), "falske": len(falske),
        "presisjon": len(ekte) / len(treff) if treff else None,
        "per_felt": per_felt, "per_dømt_klasse": per_klasse,
        "falske_klassefordeling": dict(Counter(f["dømt_klasse"] for f in falske).most_common()),
        "falske_dømt_H7_eller_H8": len(h7h8),
        "andel_falske_H7_H8": len(h7h8) / len(falske) if falske else None,
        "n_ingen_lest": len(ingen), "ekte_blant_ingen": len(funnet),
        "bomrate_blant_ingen": len(funnet) / len(ingen) if ingen else None,
    }


def topicdeling(verk: Sequence[dict], fasit: Sequence[dict], topic_ids: dict) -> dict:
    """Presisjon delt på om feltet er verkets primærtopic eller bare et sekundærtopic."""
    primær = {v["work_id"]: v["primary_topic_id"] in topic_ids.get(v["felt"], ()) for v in verk}
    ut: dict = {"verk": {"primærtopic": sum(1 for v in verk if primær[v["work_id"]]),
                         "sekundærtopic": sum(1 for v in verk if not primær[v["work_id"]])}}
    for navn, flagg in (("primærtopic", True), ("sekundærtopic", False)):
        rader = [f for f in fasit if f["utvalgstype"] == "treff" and primær.get(f["doc_id"]) is flagg]
        ekte = [f for f in rader if f["ekte_treff"]]
        ut[navn] = {"n_lest": len(rader), "ekte": len(ekte),
                    "presisjon": len(ekte) / len(rader) if rader else None}
    return ut


def _ikke_treff(fasit: Sequence[dict], vekter: dict[str, int]) -> dict:
    """Bom blant ikke-treffene, delt på INGEN, N3 og N1/N2 — og vektet med materialets fordeling."""
    typer = {"ingen": "INGEN", "n3": "N3", "n1n2": "N1/N2"}
    ut: dict = {}
    for typ, navn in typer.items():
        rader = [f for f in fasit if f["utvalgstype"] == typ]
        if typ == "n1n2":
            for klasse in ("N1", "N2"):
                k = [f for f in rader if f["dømt_klasse"] == klasse]
                if k:
                    ut[klasse] = {"n_lest": len(k), "bom": sum(1 for f in k if f["ekte_treff"]),
                                  "bomrate_rå": sum(1 for f in k if f["ekte_treff"]) / len(k),
                                  "merknad": "alle som finnes er lest; rått tall, ingen ekstrapolering"}
            continue
        if rader:
            ut[navn] = {"n_lest": len(rader), "bom": sum(1 for f in rader if f["ekte_treff"]),
                        "bomrate": sum(1 for f in rader if f["ekte_treff"]) / len(rader)}
    if vekter:
        N = sum(vekter.values())
        ledd, dekket = {}, 0
        for navn, b in ut.items():
            v = vekter.get(navn, 0)
            rate = b.get("bomrate", b.get("bomrate_rå"))
            if v and rate is not None:
                ledd[navn] = {"vekt": v / N, "bomrate": rate}
                dekket += v
        ut["vektet"] = {"bomrate": sum(l["vekt"] * l["bomrate"] for l in ledd.values()) / (dekket / N) if dekket else None,
                        "ledd": ledd, "n_ikke_treff_i_materialet": N,
                        "andel_av_ikke_treffene_dekket": dekket / N if N else None}
    return ut


def m1_varianter(verk: Sequence[dict], treff: dict[str, list[dict]], pres_per_klasse: dict,
                 pres_samlet: float | None, *, streng: bool = False) -> dict:
    """M1 rå ved terskel 1, 2 og 3, og korrigert med målt presisjon per klasse.

    ``streng`` krever at det ugjorte og hindringen sto i samme setning (ADDENDUM-03 §1.2).
    """
    if streng:
        treff = {d: [x for x in ts if x.get("samme_setning") is True] for d, ts in treff.items()}
    ut = {}
    for k in (1, 2, 3):
        med = sum(1 for v in verk if len(treff.get(v["work_id"], [])) >= k)
        ut[f"M1_minst_{k}"] = {"verk_med_treff": med, "n_verk": len(verk),
                               "M1": med / len(verk) if verk else None}
    forventet = 0.0
    for v in verk:
        p_ingen_ekte = 1.0
        for t in treff.get(v["work_id"], []):
            b = pres_per_klasse.get(t["klasse"])
            p = b["presisjon"] if b and b["n"] >= 5 else pres_samlet
            p_ingen_ekte *= (1 - (p if p is not None else 0.0))
        forventet += 1 - p_ingen_ekte
    ut["M1_korrigert"] = {"forventet_verk_med_ekte_treff": forventet, "n_verk": len(verk),
                          "M1": forventet / len(verk) if verk else None,
                          "metode": "1 − Π(1 − presisjon(klasse)) per verk; klasser med under fem leste treff bruker samlet presisjon"}
    return ut


# --------------------------------------------------------------------------- #
# Ankere: kjente treff og kjente ikke-treff fra recall-settenes fasit
# --------------------------------------------------------------------------- #

N_ANKER_TREFF = 12
N_ANKER_IKKE = 8


def _vindu(s: int, e: int, n: int, w: int = WINDOW) -> tuple[int, int]:
    """±w-vindu rundt et notert spenn, klippet mot dokumentgrensene."""
    c = (s + e) // 2
    lo = max(0, c - w)
    hi = min(n - 1, lo + 2 * w)
    return max(0, hi - 2 * w), hi


def ankere(repo: Path = Path("."), seed: int = P.MAALEFRO) -> list[dict]:
    """12 kjente treff og 8 kjente ikke-treff fra fasitarbeidet, trukket med målefrøet.

    Treffene er fasittreffene i recall-sett 1 og 2, med laget (humaniora/biomed) og klassen slik de
    ble kodet før dommeren fantes; passasjen er den samme ±2-teksten som ble brukt i L3-POC-en.
    Ikke-treffene er fasitens ikke-treff: de noterte nestentreffene i sett 2, som koderen leste og
    forkastet, pluss de trukne negativene fra begge sett — begge sett ble lest i sin helhet, så et
    parkert spørsmål i dem ville vært notert. Noterte rader med spenn større enn én passasje faller
    ut; de er ikke sammenliknbare enheter (det tar også med raden som er merket feil dokument).
    Ankerne bærer ingen markering ut mot lesningen; fasiten ligger i nøkkelfilen.
    """
    fasit = [json.loads(l) for l in (repo / "data/l3-poc/fasit.jsonl").open(encoding="utf-8")]
    tekst = {r["id"]: r["tekst"] for r in
             (json.loads(l) for l in (repo / "data/l3-poc/elementer-blind.jsonl").open(encoding="utf-8"))}

    def fra_poc(f: dict) -> dict:
        return {"doc_id": f["doc_id"], "start_index": f["fra"], "end_index": f["til"], "lag": f["lag"],
                "fasit_klasse": f.get("fasit_klasse"), "tekst": tekst[f["id"]],
                "kilde": f"L3-POC {f['id']} (sett {f['sett']})"}

    treff = [fra_poc(f) for f in fasit if f["type"] == "treff"]
    valgt_t = stratifisert(treff, N_ANKER_TREFF, lambda r: (r["lag"], r["fasit_klasse"]), seed)

    lag = {m["doc_id"]: m["delsett"] for m in json.loads((repo / "data/recall-sett-2-meta.json").read_text())}
    setn: dict[str, dict[int, str]] = {}
    for l in (repo / "data/recall-sett-2-setninger.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        setn.setdefault(r["doc_id"], {})[r["sentence_index"]] = r["text"]
    ikke = [fra_poc(f) for f in fasit if f["type"] == "negativ"]
    for l in (repo / "data/recall-sett-2-noterte-ikke-treff.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        s, e = r["setninger"]
        if e - s + 1 > 2 * WINDOW + 1:
            continue
        lo, hi = _vindu(s, e, len(setn[r["doc_id"]]))
        ikke.append({"doc_id": r["doc_id"], "start_index": lo, "end_index": hi, "lag": lag[r["doc_id"]],
                     "fasit_klasse": None, "tekst": " ".join(setn[r["doc_id"]][i] for i in range(lo, hi + 1)),
                     "kilde": f"notert ikke-treff sett 2 ({s}–{e})"})
    valgt_i = stratifisert(ikke, N_ANKER_IKKE, lambda r: r["lag"], seed)
    return [dict(r, utvalgstype="anker-treff") for r in valgt_t] + \
           [dict(r, utvalgstype="anker-ikke-treff") for r in valgt_i]


def ankermål(fasit: Sequence[dict]) -> dict:
    """Ankerne måles for seg: de er kalibrering av lesningen, ikke måling av dommeren."""
    t = [f for f in fasit if f["utvalgstype"] == "anker-treff"]
    i = [f for f in fasit if f["utvalgstype"] == "anker-ikke-treff"]
    lest_t = sum(1 for f in t if f["ekte_treff"])
    lest_i = sum(1 for f in i if not f["ekte_treff"])
    enig = sum(1 for f in t if f.get("min_klasse") == f["fasit_klasse"])
    return {
        "n_kjente_treff": len(t), "lest_som_treff": lest_t,
        "andel_kjente_treff_lest_som_treff": lest_t / len(t) if t else None,
        "n_kjente_ikke_treff": len(i), "lest_som_ikke_treff": lest_i,
        "andel_kjente_ikke_treff_lest_som_ikke_treff": lest_i / len(i) if i else None,
        "eksakt_klasseenighet_med_opprinnelig_fasit": enig / len(t) if t else None,
        "klasseavvik": [{"kilde": f["kilde"], "fasit": f["fasit_klasse"], "lest_nå": f.get("min_klasse")}
                        for f in t if f.get("min_klasse") != f["fasit_klasse"]],
        "kilder_ikke_treff": dict(Counter("notert" if f["kilde"].startswith("notert") else "negativ"
                                          for f in i).most_common()),
    }
