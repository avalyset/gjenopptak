"""Recall og presisjon for passasjefilteret, målt mot en manuell fasit.

Fasiten (``data/recall-sett.jsonl``) er laget uten filteret og uten søk: 30
dokumenter lest i sin helhet, hver passasje som oppfyller PREREG §2 markert for
hånd. Dokumentene er trukket med målefrøet blant de 46 filene som ikke ble
funnet ved frasesøk, så tallene er ikke sirkulære.

**Markørfordelingen fra rørledningstesten kan ikke leses som recall.** De 348
dokumentene der fordelingen ble målt, ble funnet ved å søke på nettopp de
frasene markørlisten består av. At «could not» står for 44 % av markørtreffene
der, sier hva søket lette etter, ikke hva filteret fanger. Recall finnes bare
mot en fasit som er laget uavhengig av filteret. Det er denne modulen.

Treffregelen: et fasittreff er fanget hvis en filterpassasje fra samme dokument
har ``start_index <= fasit.hit_index <= end_index``. Samme regel brukes begge
veier, så presisjon og recall er målt på én definisjon.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from .passage import OBSTACLE, OBSTACLE_V2, UNDONE, UNDONE_V2, Passage, passages


@dataclass(frozen=True)
class FasitTreff:
    """Én manuelt markert passasje."""

    doc_id: str
    hit_index: int
    start_index: int
    end_index: int
    klasse: str
    unit: str
    sentence_text: str
    passage_text: str
    begrunnelse: str
    grensetilfelle: bool


@dataclass(frozen=True)
class Maaling:
    n_dokumenter: int
    fanget: tuple[FasitTreff, ...]
    bom: tuple[FasitTreff, ...]
    kandidater: tuple[Passage, ...]
    i_fasiten: tuple[Passage, ...]

    @property
    def n_fasit(self) -> int:
        return len(self.fanget) + len(self.bom)

    @property
    def recall(self) -> float:
        if not self.n_fasit:
            raise ValueError("recall krever minst ett fasittreff")
        return len(self.fanget) / self.n_fasit

    @property
    def presisjon(self) -> float:
        if not self.kandidater:
            raise ValueError("presisjon krever minst én filterkandidat")
        return len(self.i_fasiten) / len(self.kandidater)

    def recall_uten_grensetilfeller(self) -> tuple[int, int]:
        kjerne = [t for t in (*self.fanget, *self.bom) if not t.grensetilfelle]
        fanget = [t for t in self.fanget if not t.grensetilfelle]
        return len(fanget), len(kjerne)


def les_fasit(path: Path) -> list[FasitTreff]:
    """Les fasiten. Topplinjen er advarselen og hoppes over."""
    ut: list[FasitTreff] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if "_warning" in r:
                continue
            s = r["passage_span"]
            ut.append(
                FasitTreff(
                    doc_id=r["doc_id"],
                    hit_index=r["hit_index"],
                    start_index=s["start_index"],
                    end_index=s["end_index"],
                    klasse=r["klasse"],
                    unit=r["unit"],
                    sentence_text=r["sentence_text"],
                    passage_text=r["passage_text"],
                    begrunnelse=r["begrunnelse"],
                    grensetilfelle=r["grensetilfelle"],
                )
            )
    if not ut:
        raise ValueError(f"{path} inneholder ingen fasittreff")
    return ut


def dekker(p: Passage, t: FasitTreff) -> bool:
    """Fanger filterpassasjen dette fasittreffet?"""
    return p.doc_id == t.doc_id and p.start_index <= t.hit_index <= p.end_index


def maal(
    setninger: Mapping[str, Sequence[Mapping]],
    fasit: Sequence[FasitTreff],
    *,
    undone: re.Pattern = UNDONE,
    obstacle: re.Pattern = OBSTACLE,
) -> Maaling:
    """Kjør filteret over alle dokumentene og sammenlign med fasiten.

    ``setninger`` er doc_id → setningsrader (L1-utdata), alle leste dokumenter,
    også de uten fasittreff: presisjonen måles på hele lesesettet, ellers ville
    falske positive i de treffløse dokumentene falt utenfor nevneren.
    """
    mangler = {t.doc_id for t in fasit} - set(setninger)
    if mangler:
        raise ValueError(f"mangler setninger for {sorted(mangler)}")

    kandidater: list[Passage] = []
    for doc_id in sorted(setninger):
        kandidater.extend(
            passages(list(setninger[doc_id]), undone=undone, obstacle=obstacle)
        )

    fanget = [t for t in fasit if any(dekker(p, t) for p in kandidater)]
    bom = [t for t in fasit if not any(dekker(p, t) for p in kandidater)]
    i_fasiten = [p for p in kandidater if any(dekker(p, t) for t in fasit)]
    return Maaling(
        n_dokumenter=len(setninger),
        fanget=tuple(fanget),
        bom=tuple(bom),
        kandidater=tuple(kandidater),
        i_fasiten=tuple(i_fasiten),
    )


def foer_og_etter(
    setninger: Mapping[str, Sequence[Mapping]], fasit: Sequence[FasitTreff]
) -> dict[str, Maaling]:
    """v1 og v2 på samme fasit. Begge oppgis; v2 alene sier ingenting."""
    return {
        "v1": maal(setninger, fasit, undone=UNDONE, obstacle=OBSTACLE),
        "v2": maal(setninger, fasit, undone=UNDONE_V2, obstacle=OBSTACLE_V2),
    }


def format_maaling(m: Maaling, navn: str) -> str:
    f, n = m.recall_uten_grensetilfeller()
    return (
        f"{navn}: recall {len(m.fanget)}/{m.n_fasit} = {m.recall:.1%} "
        f"(uten grensetilfeller {f}/{n} = {f / n:.1%}); "
        f"presisjon {len(m.i_fasiten)}/{len(m.kandidater)} = {m.presisjon:.1%} "
        f"over {m.n_dokumenter} dokumenter"
    )


# --------------------------------------------------------------------------- #
# Hvilken side som sviktet (ADDENDUM-07 §3)
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Bomfordeling:
    """Hvor bommene faller: markørsiden, hindringssiden, eller begge.

    Sett 1 ga 3 bare på hindringssiden, 16 bare på markørsiden, 9 på begge.
    Tallene er ikke utbyttbare: en bom på hindringssiden rettes ved å utvide
    OBSTACLE, og en markørutvidelse hjelper ikke.
    """

    bare_ugjort: tuple[FasitTreff, ...] = ()
    bare_hindring: tuple[FasitTreff, ...] = ()
    begge: tuple[FasitTreff, ...] = ()

    def as_dict(self) -> dict[str, int]:
        return {"bare_ugjort": len(self.bare_ugjort),
                "bare_hindring": len(self.bare_hindring),
                "begge": len(self.begge)}


def bomfordeling(
    setninger: Mapping[str, Sequence[Mapping]],
    bom: Sequence[FasitTreff],
    *,
    undone: re.Pattern,
    obstacle: re.Pattern,
    window: int = 2,
) -> Bomfordeling:
    """Del bommene på hvilket mønster som ikke traff.

    «bare_ugjort» = markøren manglet, hindringen sto i passasjen.
    «bare_hindring» = markøren traff, hindringsmønsteret gjorde ikke.
    «begge» = ingen av dem.
    """
    bare_u: list[FasitTreff] = []
    bare_h: list[FasitTreff] = []
    begge: list[FasitTreff] = []
    for t in bom:
        rader = list(setninger[t.doc_id])
        pos = {r["sentence_index"]: i for i, r in enumerate(rader)}
        i = pos[t.hit_index]
        s = rader[i]["text"]
        lo, hi = max(0, i - window), min(len(rader) - 1, i + window)
        vindu = " ".join(rader[j]["text"] for j in range(lo, hi + 1))
        u = bool(undone.search(s))
        o = bool(obstacle.search(s) or obstacle.search(vindu))
        if u and not o:
            bare_h.append(t)
        elif o and not u:
            bare_u.append(t)
        else:
            begge.append(t)
    return Bomfordeling(tuple(bare_u), tuple(bare_h), tuple(begge))


def marker_hits(setninger: Mapping[str, Sequence[Mapping]],
                markers: Sequence[str]) -> dict[str, int]:
    """Hvor mange setninger hver markør treffer. Telt i Python, ikke grep."""
    rx = {m: re.compile(re.escape(m), re.I) for m in markers}
    ut = {m: 0 for m in markers}
    for rader in setninger.values():
        for r in rader:
            for m, p in rx.items():
                if p.search(r["text"]):
                    ut[m] += 1
    return ut
