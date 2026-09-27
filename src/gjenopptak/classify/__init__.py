"""L3 — klassifisering i H1-H9 / N1-N3. Ikke implementert.

Låst: løftbarhet slås opp i PREREG §5-tabellen og settes aldri av en
modell (ADR-0004); modellsignatur loggføres per dømt setning (ADR-0003).
Naboparene mot H7 kan være uavklarte, og får da «uavklart» (ADDENDUM-05).
"""

from .liftability import (  # noqa: F401
    NON_HITS,
    PREREG_TABLE,
    TABLE_VERSION,
    UNRESOLVED,
    UnknownClass,
    format_liftable,
    is_unresolved,
    liftability,
    liftable_share,
)

from .judge import (  # noqa: F401,E402
    SIGNATURE_FIELDS,
    VALID_CLASSES,
    Judge,
    JudgeError,
    Verdict,
    check_signature,
    check_verdict,
    judge_passage,
)
