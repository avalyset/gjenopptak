"""L4 — falsifiseringstest mot siteringsgrafen.

Låst: dekningsgrad rapporteres per felt; lav dekning svekker kandidaten
og styrker den aldri (PREREG-v1 §8). Rutene er Europe PMC og Crossref,
ikke OpenAlex — siteringssjekken skal ikke koste kvote.
"""

from .citations import (  # noqa: F401
    ARM_DOI,
    ArmingFailed,
    CitationCoverage,
    arm,
    crossref_count,
    epmc_citations,
    epmc_ids,
    measure,
    summarise,
)
