"""Seksjonsfordeling, alltid delt på etikettens opphav (ADR-0007 punkt 4).

Regelen er at ingen påstand om hvor i teksten en setning sto, får rapporteres
som ett samlet tall. Den er skrevet i ADR-0007, og håndheves her: modulen
tilbyr ingen funksjon som slår `source` og `parser` sammen. Vil noen ha et
samlet tall, må de skrive summeringen selv — og da står det i deres egen kode,
ikke i vår.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping

PROVENANCES = ("source", "parser")


class ProvenanceMissing(ValueError):
    """En post uten opphav kan ikke telles (ADR-0007 punkt 1)."""


@dataclass(frozen=True)
class SplitCount:
    """Én seksjonsetikett, to tall. Aldri ett."""

    section: str
    source: int
    parser: int

    @property
    def n_source(self) -> int:
        return self.source

    @property
    def n_parser(self) -> int:
        return self.parser

    def as_row(self) -> tuple[str, int, int]:
        return (self.section, self.source, self.parser)


def split_by_provenance(rows: Iterable[Mapping]) -> dict[str, Counter]:
    """Tell seksjonsetiketter per opphav.

    Returnerer {"source": Counter, "parser": Counter}. Poster uten gyldig
    opphav avvises; de skal ikke stilltiende havne i den ene kolonnen.
    """
    out: dict[str, Counter] = {p: Counter() for p in PROVENANCES}
    for i, row in enumerate(rows):
        prov = row.get("section_label_provenance")
        if prov not in PROVENANCES:
            raise ProvenanceMissing(
                f"post {i}: section_label_provenance={prov!r}; "
                f"må være en av {PROVENANCES} (ADR-0007)"
            )
        if prov == "parser" and not (row.get("parser_version") and row.get("parser_model_version")):
            raise ProvenanceMissing(
                f"post {i}: parser-opphav uten parser_version/parser_model_version "
                "er ugyldig og telles ikke (ADR-0007 punkt 3)"
            )
        out[prov][row.get("section_raw", "")] += 1
    return out


def rows_for_report(rows: Iterable[Mapping]) -> list[SplitCount]:
    """Rapporterbare rader, sortert etter samlet forekomst, men aldri slått sammen.

    Sorteringsnøkkelen bruker summen; tallet vises ikke. Å ordne en tabell er
    ikke det samme som å rapportere ett tall.
    """
    split = split_by_provenance(rows)
    seksjoner = set(split["source"]) | set(split["parser"])
    ut = [SplitCount(s, split["source"][s], split["parser"][s]) for s in seksjoner]
    ut.sort(key=lambda sc: (-(sc.source + sc.parser), sc.section))
    return ut


def format_table(rows: Iterable[Mapping], *, total_label: str = "sum") -> str:
    """Markdown-tabell med to kolonner og to sumtall. Ingen totalkolonne."""
    data = rows_for_report(rows)
    linjer = ["| seksjon (rå) | n source | n parser |", "|---|---|---|"]
    for sc in data:
        linjer.append(f"| {sc.section or '(uten tittel)'} | {sc.source} | {sc.parser} |")
    linjer.append(f"| **{total_label}** | **{sum(s.source for s in data)}** | **{sum(s.parser for s in data)}** |")
    return "\n".join(linjer)
