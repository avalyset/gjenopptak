"""L5 — register over kandidater og påstander. Ikke implementert.

Unntaket er seksjonsrapporteringen, som er låst i ADR-0007: enhver påstand om
hvor i teksten en setning sto, rapporteres delt på etikettens opphav.
"""

from .substitution import Substitution  # noqa: F401
from .section_report import (  # noqa: F401
    PROVENANCES,
    ProvenanceMissing,
    SplitCount,
    format_table,
    rows_for_report,
    split_by_provenance,
)
