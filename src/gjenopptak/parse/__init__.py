"""L1 — JATS-XML til setninger. Rå seksjonsetikett bevares (ADR-0002)."""

from .jats import (  # noqa: F401
    PARSER_ID,
    blocks_from_jats,
    iter_jsonl,
    normalize_section,
    sentences_from_jats,
    split_sentences,
    write_sentences,
)

from .jats import SECTION_LABEL_PROVENANCE  # noqa: F401,E402

from .pdfroute import (  # noqa: F401,E402
    NO_SECTION_MODEL,
    pdftotext_version,
    sentences_from_pdf,
)
