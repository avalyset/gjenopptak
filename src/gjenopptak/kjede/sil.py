"""Silen bak ett grensesnitt (byggeplanen B4).

    sil(tekstbiter) -> kandidater

Det finnes **én** implementasjon, ``dommer_union_ekstraksjon``, og den er valgt fordi den er den
eneste silen som fanget alle 27 kjente treff. Grensesnittet finnes for at en bedre sil skal kunne
settes inn uten å røre resten av kjeden — men bare preregistrert, og ikke i denne byggeplanen.

**Hva som er prøvd og forkastet**, med målt grunn (står i ``[sil.implementasjon]`` i ``kjede.toml``
og i ``docs/METODE.md`` § 5, slik at en ny sil kan sammenliknes mot noe):

===========================  ==================================================  ============
kandidat                     målt                                                utfall
===========================  ==================================================  ============
markørliste v1/v2            recall for lav                                      forkastet
embeddings (bge-m3)          84 % recall ved 2,0× kostnad                         forkastet
seksjonsplassering           1,09× — under terskelen på 50 % av tekstbitene      forkastet
nærsøk                       84 % recall ved 5,25× kostnad                        forkastet
ekstraksjon per dokument     36 % recall som enhet                                forkastet
**dommer ∪ ekstraksjon**     **27 av 27 kjente**, 12,8 % av korpuset             **valgt**
===========================  ==================================================  ============

Snittet A ∩ B er det presiseste enkeltleddet (34,5 % mot 14,3 % og 7,2 %), men **unionen** er den
eneste som fanget alt. Snittet brukes derfor som sorteringsnøkkel, ikke som filter (ADR-0012).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable, Iterable, Protocol

from ..classify.ikkeprosa import er_ikke_prosa


def norm(s: str) -> str:
    """ADDENDUM-16 §3: NFC, samlet mellomrom, uten tegnsetting i endene. Ingen fuzzy."""
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip().strip(".,;:!?\"»«'()[]").lower()


@dataclass(frozen=True)
class Tekstbit:
    """Enheten silen ser: én tekstbit med sin plass i verket."""

    doc_id: str
    start_index: int
    end_index: int
    felt: str
    tekst: str
    section_raw: str = ""
    section_label_provenance: str = "parser"

    @property
    def nøkkel(self) -> tuple[str, int, int]:
        return (self.doc_id, self.start_index, self.end_index)


@dataclass(frozen=True)
class Kandidat:
    """Det silen leverer: en tekstbit med kilden som fanget den, og ikke-prosa merket."""

    bit: Tekstbit
    kilde: str                      # "dommer" | "ekstraksjon" | "begge"
    ikke_prosa: bool

    def som_rad(self) -> dict:
        return {"doc_id": self.bit.doc_id, "start_index": self.bit.start_index,
                "end_index": self.bit.end_index, "felt": self.bit.felt,
                "tekst": self.bit.tekst, "kilde": self.kilde,
                "ikke_prosa": self.ikke_prosa, "section_raw": self.bit.section_raw,
                "section_label_provenance": self.bit.section_label_provenance}


class Sil(Protocol):
    """``sil(tekstbiter) -> kandidater``. En ny implementasjon trenger bare denne formen."""

    navn: str

    def __call__(self, tekstbiter: Iterable[Tekstbit], **kilder) -> list[Kandidat]:
        ...


@dataclass
class Måling:
    """Det en sil må kunne oppgi om seg selv før den brukes."""

    navn: str
    recall_kjente: str
    andel_av_korpus: float
    leserpassasjer_per_bekreftet_treff: float
    kilde: str


def dommer_union_ekstraksjon(
    tekstbiter: Iterable[Tekstbit], *,
    flagget: set[tuple[str, int, int]],
    q_linjer: Iterable[tuple[str, str]],
    alle_treff: bool = True,
) -> tuple[list[Kandidat], dict]:
    """A ∪ B: dommerens flagg forent med tekstbitene som bærer en Q-linje.

    ``alle_treff`` er ikke en innstilling å velge fritt. Med **første-treff** — én Q-linje til ett
    vindu — mistet unionen PS-300, fordi Q-linjen lå i to overlappende vindu og førstetreffet ga
    nabovinduet. Alle-treff gir 27 av 27 og reproduserer D1s tall for ekstraksjonen eksakt (11).
    """
    biter = list(tekstbiter)
    per_verk: dict[str, list[Tekstbit]] = {}
    for b in biter:
        per_verk.setdefault(b.doc_id, []).append(b)
    A = {b.nøkkel for b in biter if b.nøkkel in flagget}
    B: set[tuple[str, int, int]] = set()
    ukoblet = 0
    flere = 0
    for wid, q in q_linjer:
        qn = norm(q)
        if not qn:
            continue
        traff = [b.nøkkel for b in per_verk.get(wid, []) if qn in norm(b.tekst)]
        if not traff:
            ukoblet += 1
        elif alle_treff:
            B.update(traff)
            if len(traff) > 1:
                flere += 1
        else:
            B.add(traff[0])
    kandidater = []
    for b in sorted(biter, key=lambda b: b.nøkkel):
        if b.nøkkel not in A and b.nøkkel not in B:
            continue
        kilde = "begge" if (b.nøkkel in A and b.nøkkel in B) else ("dommer" if b.nøkkel in A else "ekstraksjon")
        kandidater.append(Kandidat(bit=b, kilde=kilde, ikke_prosa=er_ikke_prosa(b.tekst)))
    stat = {"A": len(A), "B": len(B), "snitt": len(A & B), "union": len(A | B),
            "q_ukoblet": ukoblet, "q_i_flere_vindu": flere,
            "kobling": "alle-treff" if alle_treff else "første-treff",
            "ikke_prosa": sum(1 for k in kandidater if k.ikke_prosa),
            "andel_av_korpus": round(len(A | B) / len(biter), 4) if biter else 0.0}
    return kandidater, stat


dommer_union_ekstraksjon.navn = "dommer ∪ ekstraksjon"

#: Registeret over siler. Én implementasjon; en ny settes inn her og velges i konfigurasjonen.
SILER: dict[str, Callable] = {"dommer_union_ekstraksjon": dommer_union_ekstraksjon}


def velg(navn: str) -> Callable:
    if navn not in SILER:
        raise ValueError(f"ukjent sil {navn!r}; kjente: {', '.join(SILER)}")
    return SILER[navn]
