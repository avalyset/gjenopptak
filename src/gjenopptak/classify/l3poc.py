"""L3-POC: to dommere mot recall-fasitene. **Ikke M1/M2, ikke utvalget.**

Materialet er de 55 fasittreffene i ``data/recall-sett.jsonl`` (28) og
``data/recall-sett-2.jsonl`` (27), og 55 negative passasjer fra de samme leste
dokumentene, trukket med målefrøet 734 248. Dommerne ser bare passasjeteksten.

Ledeteksten bygges ordrett fra de låste tekstene: treffdefinisjonen i PREREG §2
med presiseringene i ADDENDUM-03 §1.2 og ADDENDUM-04 §4, typologien i PREREG §5,
de fire uavklarte klassene i ADDENDUM-05 §2 og ankersetningene i ADDENDUM-02 §3.
Løftbarhet står ikke i ledeteksten: den slås opp, aldri av dommeren (ADR-0004).
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .liftability import NON_HITS, PREREG_TABLE, UNRESOLVED

MAALEFRO = 734248
WINDOW = 2
HIT_CLASSES = tuple(PREREG_TABLE) + tuple(UNRESOLVED)
NONHIT_CLASSES = NON_HITS + ("INGEN",)
ALL_CLASSES = HIT_CLASSES + NONHIT_CLASSES
PROMPT_VERSION = "l3-poc-v1"
LIFTABLE = frozenset(k for k, v in PREREG_TABLE.items() if v in ("ja", "ja_med_forbehold", "delvis"))

#: JSON-skjemaet begge dommerne svarer etter. Begrunnelsen kommer først.
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "begrunnelse": {"type": "string"},
        "treff": {"type": "boolean"},
        "klasse": {"type": "string", "enum": list(ALL_CLASSES)},
    },
    "required": ["begrunnelse", "treff", "klasse"],
}


# --------------------------------------------------------------------------- #
# Ledeteksten
# --------------------------------------------------------------------------- #

_ANKER = re.compile(r"^\d\. (?:⚠ )?\S+ \(\d{4}\)(?:, `[^`]*`)?: (.*)$")


def anchors_from_addendum02(text: str) -> list[tuple[str, list[str], list[str]]]:
    """(klasseoverskrift, ankere, merknader) fra ADDENDUM-02 §3, ordrett, uten DOI og seksjon."""
    start = text.index("## 3 Rubrikkankere")
    slutt = text.index("### 3.1 Hvor mange ankere")
    ut: list[tuple[str, list[str], list[str]]] = []
    for blokk in re.split(r"^### ", text[start:slutt], flags=re.M)[1:]:
        linjer = blokk.strip().splitlines()
        tittel = re.sub(r"\s*\*\([^)]*\)\*\s*$", "", linjer[0].strip())    # løftbarheten står ikke i ledeteksten
        ankere = [m.group(1).strip() for l in linjer[1:] if (m := _ANKER.match(l.strip()))]
        merk = [l.strip() for l in linjer[1:] if l.strip().startswith("Merk ")]
        ut.append((tittel, ankere, merk))
    return ut


def build_system_prompt(repo: Path) -> str:
    a02 = (repo / "ADDENDUM-02.md").read_text(encoding="utf-8")
    ankere = anchors_from_addendum02(a02)
    deler = [
        "Du er koder i forskningsprosjektet «gjenopptak». Du får én passasje fra en vitenskapelig "
        "tekst og skal kode den etter rubrikken under. Svar bare med JSON etter skjemaet til slutt.",
        "",
        "## Hva som er et treff",
        "Et treff er et parkert spørsmål: forfatteren navngir noe de ikke fikk gjort OG oppgir en hindring.",
        "Observasjonsenheten er passasjen: treffsetningen pluss ±2 setninger. Et treff krever at det ugjorte "
        "og hindringen begge står innenfor passasjen, og at de er knyttet til hverandre — hindringen må være "
        "oppgitt som grunn for det ugjorte, ikke bare befinne seg i nærheten.",
        "Et treff krever at det ugjorte tilhører den undersøkelsen teksten rapporterer. Utsagn om "
        "organisasjonens generelle praksis, om fagets vanlige framgangsmåte, eller om hva andre ikke har "
        "gjort, er ikke treff — selv når hindringen er navngitt.",
        "",
        "## Hindringstypologi",
        "Hvert treff kodes i én klasse:",
        "H1 — menneskelig lesning eller koding i skala",
        "H2 — lesbarhet: håndskrift, skadet kilde, lyd",
        "H3 — språkbarriere",
        "H4 — mønster i bilder eller signaler i volum",
        "H5 — simulering og regnekraft",
        "H6 — strukturslutning fra sekvens",
        "H7 — dataene fantes ikke",
        "H8 — tilgang, juss, etikk, samtykke",
        "H9 — begrepet eller teorien manglet",
        "",
        "## Uavklart",
        "Er passasjen ikke tilstrekkelig til å avgjøre om hindringen var arbeidsmengde eller manglende data, "
        "kodes treffet som uavklart. Verdiene er H1/H7-uavklart, H2/H7-uavklart, H3/H7-uavklart og "
        "H5/H7-uavklart. Regelen er en kodingsregel, ikke en tolkningsfrihet: koderen skal ikke gjette. "
        "Står det ikke i passasjen hvorfor noe ikke lot seg gjøre, er klassen uavklart — også når konteksten "
        "gjør én lesning sannsynlig.",
        "",
        "## Ikke-treff",
        "N1 — besvart i samme artikkel",
        "N2 — nyhetspåstand («to the best of our knowledge, this is the first…»)",
        "N3 — omfangsvalg uten navngitt hindring",
        "INGEN — passasjen navngir ikke noe forfatterne ikke fikk gjort",
        "",
        "## Ankersetninger, to per klasse",
    ]
    for tittel, ank, merk in ankere:
        deler.append(tittel)
        deler += [f"- {x}" for x in ank]
        deler += merk
    deler += [
        "",
        "## Svar",
        "Svar med JSON: {\"begrunnelse\": \"høyst to setninger\", \"treff\": true eller false, "
        "\"klasse\": \"én av " + ", ".join(ALL_CLASSES) + "\"}.",
        "treff er true bare for H1–H9 og de fire uavklarte klassene.",
    ]
    return "\n".join(deler) + "\n"


def user_prompt(passage_text: str) -> str:
    return f"Passasje:\n{passage_text}\n"


def prompt_sha256(system: str, user: str) -> str:
    return hashlib.sha256((system + "\n\n" + user).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Materialet
# --------------------------------------------------------------------------- #

def window_for(hit_index: int, span: dict, n_sentences: int, w: int = WINDOW) -> tuple[int, int]:
    """Passasjen: ±w rundt treffsetningen, eller rundt spennets midte hvis spennet ellers faller utenfor."""
    s, e = span["start_index"], span["end_index"]
    c = hit_index if (hit_index - w <= s and e <= hit_index + w) else (s + e) // 2
    if not (c - w <= s and e <= c + w):
        raise ValueError(f"fasitspennet {s}–{e} får ikke plass i ±{w}")
    return max(0, c - w), min(n_sentences - 1, c + w)


def draw_negatives(docs: dict[str, list[str]], blocked: dict[str, list[tuple[int, int]]], n: int,
                   rng: random.Random, w: int = WINDOW) -> list[tuple[str, int, int]]:
    """n negative vinduer: ingen overlapp med fasitvinduer eller med hverandre."""
    kandidater = [(d, c) for d in sorted(docs) for c in range(len(docs[d]))]
    rng.shuffle(kandidater)
    tatt: dict[str, list[tuple[int, int]]] = {}
    ut: list[tuple[str, int, int]] = []
    for d, c in kandidater:
        lo, hi = max(0, c - w), min(len(docs[d]) - 1, c + w)
        opptatt = blocked.get(d, []) + tatt.get(d, [])
        if any(not (hi < a or b < lo) for a, b in opptatt):
            continue
        tatt.setdefault(d, []).append((lo, hi))
        ut.append((d, lo, hi))
        if len(ut) == n:
            return ut
    raise ValueError(f"fant bare {len(ut)} av {n} negative vinduer")


# --------------------------------------------------------------------------- #
# Svar
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Parsed:
    klasse: str          # en av ALL_CLASSES, eller UGYLDIG
    treff: bool
    inkonsistent: bool   # treff-flagget stred mot klassen; klassen avgjør


def parse_response(raw: str | None) -> Parsed:
    try:
        d = json.loads(raw or "")
        k = d["klasse"]
        if k not in ALL_CLASSES:
            raise ValueError(k)
    except (ValueError, KeyError, TypeError):
        return Parsed("UGYLDIG", False, False)
    treff = k in HIT_CLASSES
    return Parsed(k, treff, bool(d.get("treff")) != treff)


# --------------------------------------------------------------------------- #
# Målinger
# --------------------------------------------------------------------------- #

def merge_h1h7(k: str) -> str:
    return "H1∪H7" if k in ("H1", "H7", "H1/H7-uavklart") else k


def kappa(a: Sequence[str], b: Sequence[str]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def metrics(rows: Sequence[dict]) -> dict:
    """rows: {fasit_klasse | None, dømt: Parsed-dict}. None = negativ passasje."""
    pos = [r for r in rows if r["fasit_klasse"] is not None]
    neg = [r for r in rows if r["fasit_klasse"] is None]
    tp = sum(r["treff"] for r in pos)
    fp = sum(r["treff"] for r in neg)
    fn = len(pos) - tp
    judged_hits = [r for r in rows if r["treff"]]
    return {
        "n": len(rows), "n_pos": len(pos), "n_neg": len(neg),
        "tp": tp, "fp": fp, "fn": fn,
        "presisjon": tp / (tp + fp) if (tp + fp) else None,
        "recall": tp / len(pos) if pos else None,
        "negative_dømt_treff": fp / len(neg) if neg else None,
        "eksakt_klasse": sum(r["klasse"] == r["fasit_klasse"] for r in pos) / len(pos) if pos else None,
        "eksakt_klasse_blant_dømte_treff": (sum(r["klasse"] == r["fasit_klasse"] for r in pos if r["treff"]) / tp) if tp else None,
        "klasse_h1h7_slått_sammen": sum(merge_h1h7(r["klasse"]) == merge_h1h7(r["fasit_klasse"]) for r in pos) / len(pos) if pos else None,
        "andel_dømt_uavklart_av_alle": sum(r["klasse"] in UNRESOLVED for r in rows) / len(rows) if rows else None,
        "andel_dømt_uavklart_av_dømte_treff": (sum(r["klasse"] in UNRESOLVED for r in judged_hits) / len(judged_hits)) if judged_hits else None,
        "ugyldige": sum(r["klasse"] == "UGYLDIG" for r in rows),
        "inkonsistente": sum(r.get("inkonsistent", False) for r in rows),
    }


def judge_agreement(a: Sequence[dict], b: Sequence[dict]) -> dict:
    """Enighet mellom to dommere på samme elementer, uavhengig av fasit."""
    ta = ["treff" if x["treff"] else "ikke-treff" for x in a]
    tb = ["treff" if x["treff"] else "ikke-treff" for x in b]
    ka = [x["klasse"] if x["treff"] else "ikke-treff" for x in a]
    kb = [x["klasse"] if x["treff"] else "ikke-treff" for x in b]
    begge = [(x["klasse"], y["klasse"]) for x, y in zip(a, b) if x["treff"] and y["treff"]]
    return {
        "n": len(a),
        "treff_enighet": sum(x == y for x, y in zip(ta, tb)) / len(a) if a else None,
        "treff_kappa": kappa(ta, tb),
        "klasse_enighet": sum(x == y for x, y in zip(ka, kb)) / len(a) if a else None,
        "klasse_kappa": kappa(ka, kb),
        "n_begge_treff": len(begge),
        "klasse_enighet_når_begge_treff": sum(x == y for x, y in begge) / len(begge) if begge else None,
    }


def severity(fasit: str | None, klasse: str) -> int | None:
    """Forhåndsfastsatt alvorlighet; lavere er verre. None = ingen bom."""
    treff = klasse in HIT_CLASSES
    if fasit is None:
        if not treff:
            return None
        return 1 if klasse in LIFTABLE else 3
    if klasse == fasit:
        return None
    if klasse in LIFTABLE and fasit not in LIFTABLE:
        return 1              # falsk løftbarhet: verktøyet lover noe fasit ikke gir
    if not treff:
        return 2              # fasittreff dømt ikke-treff
    return 4                  # annen klassefeil blant treff


def worst_misses(rows: Sequence[dict], k: int = 10) -> list[dict]:
    bom = [dict(r, alvorlighet=s) for r in rows if (s := severity(r["fasit_klasse"], r["klasse"])) is not None]
    return sorted(bom, key=lambda r: (r["alvorlighet"], r["fasit_klasse"] is None, r["id"]))[:k]


# --------------------------------------------------------------------------- #
# Variant B: eksplisitt skille mellom H7 og H1/H2
# --------------------------------------------------------------------------- #

PROMPT_VERSION_B = "l3-poc-B"
B_INNSETT_FØR = "## Uavklart"


def select_examples(fasit_rows: Sequence[dict], seed: int = MAALEFRO) -> tuple[dict, dict]:
    """Ett eksempel per side av skillet, trukket med målefrøet fra fasitens egne passasjer.

    H7-siden: setningstreff i H7, ikke grensetilfelle, eneste treff i dokumentet.
    H1/H2-siden: setningstreff i H1 eller H2, ikke grensetilfelle (ingen av dem er eneste treff
    i sitt dokument, så det kravet kan ikke stilles). Utvalget ser ikke på noen dom.
    """
    per_dok = Counter((r["sett"], r["doc_id"]) for r in fasit_rows)
    nøkkel = lambda r: (r["sett"], r["doc_id"], r["hit_index"])
    h7 = sorted((r for r in fasit_rows if r["klasse"] == "H7" and r["unit"] == "sentence"
                 and not r["grensetilfelle"] and per_dok[(r["sett"], r["doc_id"])] == 1), key=nøkkel)
    h12 = sorted((r for r in fasit_rows if r["klasse"] in ("H1", "H2") and r["unit"] == "sentence"
                  and not r["grensetilfelle"]), key=nøkkel)
    if not h7 or not h12:
        raise ValueError("fant ikke eksempel på begge sider")
    return h7[random.Random(seed).randrange(len(h7))], h12[random.Random(seed).randrange(len(h12))]


def build_system_prompt_b(prompt_a: str, eksempel_h7: str, eksempel_h1h2: str) -> str:
    """Ledetekst A med ett innskutt avsnitt før «## Uavklart». Ingen andre endringer."""
    if prompt_a.count(B_INNSETT_FØR) != 1:
        raise ValueError("fant ikke innsettingspunktet i ledetekst A")
    avsnitt = (
        "## Skillet mellom H7 og H1/H2\n"
        "- Hindringen er at dataene ikke finnes eller aldri ble samlet inn → H7.\n"
        f"  Eksempel: «{eksempel_h7}»\n"
        "- Hindringen er arbeidet med data som finnes → H1 (lesning/koding i skala) eller H2 (lesbarhet).\n"
        f"  Eksempel: «{eksempel_h1h2}»\n"
        "\n"
    )
    return prompt_a.replace(B_INNSETT_FØR, avsnitt + B_INNSETT_FØR)


def contains_example(item_text: str, examples: Iterable[str]) -> bool:
    flat = " ".join(item_text.split())
    return any(" ".join(e.split()) in flat for e in examples)


def comparison_metrics(rows: Sequence[dict]) -> dict:
    """Tallene for sammenligningen A mot B. rows som i ``metrics``."""
    m = metrics(rows)
    n = len(rows)
    falsk = [r for r in rows if r["klasse"] in LIFTABLE and (r["fasit_klasse"] is None or r["fasit_klasse"] not in LIFTABLE)]
    return {
        "n": n, "n_pos": m["n_pos"], "n_neg": m["n_neg"],
        "recall": m["recall"], "presisjon": m["presisjon"],
        "eksakt_klasse": m["eksakt_klasse"], "klasse_h1h7_slått_sammen": m["klasse_h1h7_slått_sammen"],
        "andel_dømt_H7": sum(r["klasse"] == "H7" for r in rows) / n if n else None,
        "andel_dømt_INGEN": sum(r["klasse"] == "INGEN" for r in rows) / n if n else None,
        "falsk_løftbarhet_n": len(falsk),
        "falsk_løftbarhet_andel": len(falsk) / n if n else None,
    }
