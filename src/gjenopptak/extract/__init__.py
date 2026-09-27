"""L2 — uttrekk av kandidatpassasjer.

Observasjonsenheten er passasjen: treffsetningen pluss ±2 setninger
(ADDENDUM-03 §1). Hele teksten skannes, ingen seksjonsbasert forhåndsfiltrering,
og section_raw bæres videre urørt (ADR-0002) med sitt opphav (ADR-0007).
"""

from .passage import (  # noqa: F401
    OBSTACLE,
    OBSTACLE_ADDITIONS,
    OBSTACLE_V2,
    UNDONE,
    UNDONE_ADDITIONS,
    UNDONE_V2,
    WINDOW,
    NotSplit,
    Passage,
    format_m1,
    passages,
    split_counts,
)
from .recall import (  # noqa: F401
    Bomfordeling,
    FasitTreff,
    Maaling,
    bomfordeling,
    dekker,
    foer_og_etter,
    format_maaling,
    les_fasit,
    maal,
    marker_hits,
)
