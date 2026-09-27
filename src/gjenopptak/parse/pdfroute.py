"""PDF-ruten i L1: tekst uten kildemerkede seksjoner (ADR-0007).

JATS gir forlagets egen seksjonsmerking, og setningene derfra får
``section_label_provenance = "source"``. En PDF gir ingen slik merking. Uten
GROBID finnes ingen seksjonsinndeling i det hele tatt, og da er den ærlige
verdien en **tom** ``section_raw`` med opphav ``parser`` — ikke en gjetning fra
skriftstørrelse som utgir seg for å være kildens.

Følgen, som skal stå i rapporteringen: setninger hentet via PDF bidrar bare til
``parser``-kolonnen i seksjonsfordelingen (ADR-0007 punkt 4), og de kan ikke
brukes til å si *hvor i teksten* noe sto. De kan brukes til å si *at* det står der.

Seksjonsinndeling fra PDF krever GROBID og er ikke installert. Når den kommer,
settes ``section_raw`` fra TEI-en og ``parser_model_version`` til GROBID-modellen;
opphavet blir fortsatt ``parser``.
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .jats import split_sentences

#: pdftotext-versjon, lest én gang. Loggføres per setning (ADR-0007 punkt 3).
def pdftotext_version() -> str:
    try:
        r = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True, timeout=30)
        ut = (r.stdout + r.stderr).splitlines()
        return ut[0].strip() if ut else "pdftotext-ukjent"
    except (subprocess.SubprocessError, OSError):
        return "pdftotext-mangler"


#: Ingen seksjonsmodell er kjørt. Verdien er eksplisitt, ikke tom av vanvare.
NO_SECTION_MODEL = "ingen-seksjonsmodell"

_WS = re.compile(r"[ \t]+")
_BREAK = re.compile(r"\n{2,}")


def pdf_to_text(pdf_bytes: bytes, tmp_dir: Path, name: str) -> str:
    """Trekk ut tekst med pdftotext. Tom streng hvis ingenting kan hentes."""
    tmp_dir.mkdir(parents=True, exist_ok=True)
    p = tmp_dir / f"{name}.pdf"
    p.write_bytes(pdf_bytes)
    try:
        r = subprocess.run(["pdftotext", "-q", "-nopgbrk", str(p), "-"],
                           capture_output=True, text=True, timeout=180)
        return r.stdout
    except (subprocess.SubprocessError, OSError):
        return ""
    finally:
        p.unlink(missing_ok=True)


def blocks_from_text(txt: str) -> list[str]:
    """Del i avsnitt på blanke linjer. Ikke seksjoner — avsnitt."""
    ut = []
    for blokk in _BREAK.split(txt):
        t = _WS.sub(" ", blokk.replace("\n", " ")).strip()
        if len(t) >= 40:          # hopp over sidetall, kolumnetitler, løse ord
            ut.append(t)
    return ut


def sentences_from_pdf(pdf_bytes: bytes, *, doc_id: str, tmp_dir: Path,
                       parsed_at: str | None = None,
                       parser_version: str | None = None) -> list[dict]:
    """PDF → sentences-poster med opphav ``parser`` og tom seksjonsetikett."""
    parsed_at = parsed_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    pv = parser_version or pdftotext_version()
    txt = pdf_to_text(pdf_bytes, tmp_dir, doc_id)
    rows: list[dict] = []
    offset = 0
    index = 0
    for blokk in blocks_from_text(txt):
        for start, end, setning in split_sentences(blokk):
            rows.append({
                "schema_version": "sentences-1",
                "sentence_id": f"{doc_id}:{index}",
                "doc_id": doc_id,
                "text": setning,
                "char_start": offset + start,
                "char_end": offset + end,
                "sentence_index": index,
                "section_raw": "",                     # ingen kildemerking finnes
                "section_path_raw": [],
                "section_id_raw": None,
                "section_type_raw": None,
                "section_norm": "unknown",
                "section_norm_rule": "pdf-ingen-seksjonsmodell",
                "section_label_provenance": "parser",  # ADR-0007
                "parser_version": pv,
                "parser_model_version": NO_SECTION_MODEL,
                "block_kind": "p",
                "parser": f"gjenopptak.parse.pdfroute/{pv}",
                "parsed_at": parsed_at,
            })
            index += 1
        offset += len(blokk) + 1
    return rows
