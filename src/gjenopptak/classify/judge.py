"""L3-stillas: klassifiseringskontrakten. **Ingen modell kjøres her.**

Dommeren er en injisert avhengighet. Modulen definerer hva en dommer må svare og
hva som gjøres med svaret; den inneholder ingen modell, ingen ledetekst og ingen
nettkall. Testene bruker en fast stub. Dette er kontrakten, ikke dommen.

Tre regler fra tidligere beslutninger håndheves her, ikke i dommeren:

* **Løftbarhet slås opp**, aldri av dommeren (ADR-0004). En dommer som forsøker å
  sette ``liftable`` får svaret forkastet.
* **Modellsignatur kreves** når dommeren ikke er eieren (ADR-0003): modell-ID,
  vekt-sha256, temperatur, frø, ``keep_alive=0``, kjøretid, ledetekst-hash.
* **Uavklarte naboklasser** mot H7 er gyldige svar og gir løftbarhet ``uavklart``
  (ADDENDUM-05). En dommer som tvinges til å velge mellom H1 og H7 uten grunnlag,
  produserer den overvurderingen ADDENDUM-05 ble skrevet for å stoppe.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from ..extract import Passage
from .liftability import NON_HITS, PREREG_TABLE, TABLE_VERSION, UNRESOLVED, liftability

#: Alle lovlige svar fra en dommer.
VALID_CLASSES = tuple(PREREG_TABLE) + tuple(UNRESOLVED) + NON_HITS + ("UNSURE",)

#: Feltene en modellsignatur må ha (ADR-0003).
SIGNATURE_FIELDS = ("model_id", "weights_sha256", "temperature", "seed",
                    "keep_alive", "runtime", "prompt_sha256", "judged_at")


class JudgeError(ValueError):
    """Dommerens svar kan ikke brukes. Oppføringen telles ikke."""


@dataclass(frozen=True)
class Verdict:
    """Det en dommer svarer. Ingenting mer, ingenting avledet."""

    obstacle_class: str
    is_hit: bool
    judgeable: str | None = None        # ja | nei | usikker (M2)
    rationale: str | None = None


class Judge(Protocol):
    """Kontrakten. En dommer er kallbar og navngir seg selv."""

    name: str

    def __call__(self, passage: Passage) -> Verdict: ...


def check_verdict(v: Verdict) -> None:
    """Avvis svar som ikke kan brukes, før noe skrives."""
    if v.obstacle_class not in VALID_CLASSES:
        raise JudgeError(f"ukjent klasse fra dommer: {v.obstacle_class!r}")
    if v.obstacle_class in NON_HITS and v.is_hit:
        raise JudgeError(f"{v.obstacle_class} er et ikke-treff, men is_hit=True")
    if v.obstacle_class in PREREG_TABLE and not v.is_hit and v.obstacle_class != "UNSURE":
        raise JudgeError(f"{v.obstacle_class} er en hindringsklasse, men is_hit=False")
    if v.judgeable not in (None, "ja", "nei", "usikker"):
        raise JudgeError(f"ugyldig judgeable: {v.judgeable!r}")
    if hasattr(v, "liftable"):          # en dommer skal ikke kunne sette den
        raise JudgeError("dommeren forsøkte å sette liftable; det slås opp (ADR-0004)")


def check_signature(judge_name: str, signature: dict | None) -> None:
    """Modellsignatur kreves for alt annet enn eierens egen koding (ADR-0003)."""
    if judge_name == "owner":
        return
    if not signature:
        raise JudgeError(f"dommer {judge_name!r} mangler modellsignatur (ADR-0003)")
    mangler = [f for f in SIGNATURE_FIELDS if f not in signature]
    if mangler:
        raise JudgeError(f"modellsignatur mangler {mangler} (ADR-0003)")
    if signature.get("keep_alive") != 0 and not signature.get("batch"):
        raise JudgeError("keep_alive må være 0: modellen lastes ut mellom setninger")
    if signature.get("batch") and signature.get("keep_alive") == 0:
        raise JudgeError("batch=True krever at keep_alive er noe annet enn 0 (ADR-0008)")


def judge_passage(passage: Passage, judge: Judge, *, field_key: str,
                  signature: dict | None = None, round_: int = 1) -> dict:
    """Kjør dommeren på én passasje og bygg en skjemagyldig kandidatpost.

    Løftbarhet settes av oppslaget, ikke av dommeren. For uavklarte naboklasser
    blir den ``uavklart`` (ADDENDUM-05), og for ikke-treff utelates den.
    """
    v = judge(passage)
    check_verdict(v)
    check_signature(getattr(judge, "name", "ukjent"), signature)

    nå = datetime.now(timezone.utc).isoformat(timespec="seconds")
    post = {
        "schema_version": "candidates-1",
        "candidate_id": f"{passage.doc_id}:{passage.hit_index}",
        "sentence_id": f"{passage.doc_id}:{passage.hit_index}",
        "doc_id": passage.doc_id,
        "field_key": field_key,
        "section_raw": passage.section_raw,
        "section_label_provenance": passage.section_label_provenance,
        "unit": passage.unit,
        "passage_span": passage.span(),
        "is_hit": v.is_hit,
        "obstacle_class": v.obstacle_class,
        "liftability_table_version": TABLE_VERSION,
        "judge": getattr(judge, "name", "ukjent"),
        "judged_at": nå,
        "round": round_,
    }
    if v.obstacle_class in NON_HITS:
        post["liftable"] = "usikker"          # ikke-treff har ingen løftbarhet
        post["unsure"] = False
    elif v.obstacle_class == "UNSURE":
        post["liftable"] = "usikker"
        post["unsure"] = True
    else:
        post["liftable"] = liftability(v.obstacle_class)
        post["unsure"] = v.obstacle_class in UNRESOLVED
    if v.judgeable:
        post["judgeable"] = v.judgeable
    if v.rationale:
        post["rationale"] = v.rationale
    if signature:
        post["model_signature"] = signature
    return post
