"""L1 → L2 over lagret materiale. **Rørledningstest, ikke måling.**

Grunnlaget er de hentede fulltekstfilene under ``data/raw/``: rammeprøve- og
kontrolljaktmateriale. Det er **ikke et utvalg**, og ingen tall herfra er M1
eller M2. Filnavnene bærer ``PIPELINETEST`` for at de ikke skal kunne forveksles
med utvalgsdata senere, og hver utdatafil får en topplinje som sier det samme.

Det som måles her er **filterets oppførsel**: hvor mange dokumenter som gir
kandidater, fordelingen per dokument, og hvilke markører som utløser treff. Et
filter der én frase står for nesten alt, har skjør recall selv om totalen ser bra ut.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .extract import UNDONE, WINDOW, passages
from .parse import sentences_from_jats, sentences_from_pdf
from .schemas import validate

FULLTEXT_PREFIXES = ("jats-", "dl-jats-", "ft-jats-", "cs-jats-",
                     "pdf-", "dl-pdf-", "ft-pdf-")

WARNING = (
    "RØRLEDNINGSTEST — IKKE UTVALGSDATA. Grunnlaget er rammeprøve- og "
    "kontrolljaktmateriale, ikke en tilfeldig trukket ramme. Ingen tall fra "
    "denne filen er M1 eller M2. Se ADDENDUM-04 §1 og ADDENDUM-03 §2.3."
)

#: Markørene i UNDONE, hver for seg, slik at treff kan tilskrives én frase.
MARKERS = (
    "were unable to", "was not possible", "could not", "did not have",
    "did not attempt", "did not allow", "did not assess", "prevented us from",
    "prevented me from", "was not feasible", "no attempt was made",
    "too time-consuming", "too time consuming", "prohibitiv", "only a subset",
    "we manually reviewed", "we coded a random sample", "remains unread",
    "remains untranscribed", "have not been read", "have not been transcribed",
    "have not been collated", "have not been digiti",
)
_MARKER_RE = {m: re.compile(re.escape(m), re.I) for m in MARKERS}


@dataclass
class DocResult:
    doc_id: str
    source_file: str
    kind: str                    # jats | pdf
    provenance: str              # source | parser
    n_sentences: int
    n_passages: int
    units: Counter = field(default_factory=Counter)
    markers: Counter = field(default_factory=Counter)
    error: str | None = None


def classify_file(path: Path) -> str:
    """jats eller pdf, avgjort på innhold — filnavnet lyver (alt heter .json)."""
    head = path.open("rb").read(5)
    if head.startswith(b"%PDF"):
        return "pdf"
    if head.lstrip().startswith(b"<"):
        return "jats"
    return "ukjent"


def fulltext_files(raw_dir: Path) -> list[Path]:
    return sorted(p for p in raw_dir.iterdir()
                  if p.is_file() and any(p.name.startswith(x) for x in FULLTEXT_PREFIXES))


def doc_id_for(path: Path) -> str:
    """Stabil id fra filnavnet: prefiks og sha-suffiks strippet."""
    navn = path.stem
    navn = re.sub(r"-[0-9a-f]{12}$", "", navn)
    for p in sorted(FULLTEXT_PREFIXES, key=len, reverse=True):
        if navn.startswith(p):
            navn = navn[len(p):]
            break
    return navn or path.stem


def markers_in(text: str) -> list[str]:
    return [m for m, rx in _MARKER_RE.items() if rx.search(text)]


def run(raw_dir: Path, out_dir: Path, tmp_dir: Path, *, limit: int | None = None) -> dict:
    """Kjør L1 → L2 over alt lagret fulltekstmateriale."""
    out_dir.mkdir(parents=True, exist_ok=True)
    filer = fulltext_files(raw_dir)[:limit]
    nå = datetime.now(timezone.utc).isoformat(timespec="seconds")

    s_path = out_dir / "sentences-PIPELINETEST.jsonl"
    p_path = out_dir / "passages-PIPELINETEST.jsonl"
    c_path = out_dir / "candidates-PIPELINETEST.jsonl"
    docs: list[DocResult] = []

    with s_path.open("w", encoding="utf-8") as sf, \
         p_path.open("w", encoding="utf-8") as pf, \
         c_path.open("w", encoding="utf-8") as cf:
        for fh in (sf, pf, cf):
            fh.write(json.dumps({"_warning": WARNING, "_written_at": nå},
                                ensure_ascii=False) + "\n")

        for path in filer:
            kind = classify_file(path)
            doc_id = doc_id_for(path)
            d = DocResult(doc_id=doc_id, source_file=path.name, kind=kind,
                          provenance="source" if kind == "jats" else "parser",
                          n_sentences=0, n_passages=0)
            try:
                if kind == "jats":
                    rows = sentences_from_jats(path.read_bytes(), doc_id=doc_id, parsed_at=nå)
                elif kind == "pdf":
                    rows = sentences_from_pdf(path.read_bytes(), doc_id=doc_id,
                                              tmp_dir=tmp_dir, parsed_at=nå)
                else:
                    d.error = f"ukjent innholdstype"
                    docs.append(d)
                    continue
            except Exception as e:                          # noqa: BLE001
                d.error = f"{type(e).__name__}: {str(e)[:80]}"
                docs.append(d)
                continue

            d.n_sentences = len(rows)
            for r in rows:
                sf.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

            for i, p in enumerate(passages(rows)):
                d.n_passages += 1
                d.units[p.unit] += 1
                for m in markers_in(p.sentence_text):
                    d.markers[m] += 1
                pf.write(json.dumps({
                    "doc_id": p.doc_id, "hit_index": p.hit_index, "unit": p.unit,
                    "passage_span": p.span(), "sentence": p.sentence_text,
                    "passage": p.text, "section_raw": p.section_raw,
                    "section_label_provenance": p.section_label_provenance,
                    "markers": markers_in(p.sentence_text),
                }, ensure_ascii=False, sort_keys=True) + "\n")

                # Skjemagyldig kandidat, men UTEN dom: ingen dommer har kjørt.
                kand = {
                    "schema_version": "candidates-1",
                    "candidate_id": f"{doc_id}:{p.hit_index}",
                    "sentence_id": f"{doc_id}:{p.hit_index}",
                    "doc_id": doc_id,
                    "field_key": "energimodellering",     # plassholder, se _warning
                    "section_raw": p.section_raw,
                    "section_label_provenance": p.section_label_provenance,
                    "unit": p.unit,
                    "passage_span": p.span(),
                    "is_hit": False,
                    "obstacle_class": "UNSURE",
                    "liftable": "usikker",
                    "liftability_table_version": "PREREG-v1-§5 + ADDENDUM-05",
                    "unsure": True,
                    "judge": "pipeline:ingen-dommer",
                    "judged_at": nå,
                    "rationale": "Rørledningstest. Ingen dommer har kjørt; "
                                 "obstacle_class er ikke tildelt.",
                }
                if p.section_label_provenance == "parser":
                    kand["parser_version"] = next(
                        (r.get("parser_version") for r in rows if r.get("parser_version")), "ukjent")
                    kand["parser_model_version"] = next(
                        (r.get("parser_model_version") for r in rows if r.get("parser_model_version")), "ukjent")
                validate("candidates", kand)
                cf.write(json.dumps(kand, ensure_ascii=False, sort_keys=True) + "\n")
            docs.append(d)

    return {"docs": docs, "files": {"sentences": s_path, "passages": p_path,
                                    "candidates": c_path}, "written_at": nå}


def summarise(docs: list[DocResult]) -> dict:
    """Filterets oppførsel — ikke prevalens."""
    ok = [d for d in docs if d.error is None]
    uten = [d for d in ok if d.n_passages == 0]
    fordeling = Counter(d.n_passages for d in ok)
    markører: Counter = Counter()
    enheter: Counter = Counter()
    for d in ok:
        markører.update(d.markers)
        enheter.update(d.units)
    total_markørtreff = sum(markører.values())
    topp = markører.most_common(20)
    return {
        "n_docs": len(docs),
        "n_ok": len(ok),
        "n_error": len(docs) - len(ok),
        "n_sentences": sum(d.n_sentences for d in ok),
        "n_passages": sum(d.n_passages for d in ok),
        "docs_without_candidate": len(uten),
        "share_without_candidate": len(uten) / len(ok) if ok else 0.0,
        "per_doc_distribution": dict(sorted(fordeling.items())),
        "units": dict(enheter),
        "by_provenance": dict(Counter(d.provenance for d in ok)),
        "top_markers": topp,
        "marker_hits_total": total_markørtreff,
        "top_marker_share": (topp[0][1] / total_markørtreff) if topp and total_markørtreff else 0.0,
        "n_markers_used": len(markører),
    }
