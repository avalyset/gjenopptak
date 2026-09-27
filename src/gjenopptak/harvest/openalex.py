"""Henter works fra OpenAlex på emne-ID + år + has_fulltext.

Kjeden er todelt, med vilje:

1. Svaret fra OpenAlex lagres **urørt** under ``data/raw/`` — byte for byte
   slik det kom — og føres inn i ``data/raw/MANIFEST.md`` med filnavn, bytes,
   sha256, kilde-URL og hentetidspunkt.
2. Deretter avledes ``documents.jsonl``. Avledningen kan gjøres om igjen fra
   rådata uten nytt nettkall.

Rådata committes aldri (ADR-0001). Fulltekst hentes ikke her; dette leddet
fester bare utvalgsrammen og hva som finnes.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

import httpx

API = "https://api.openalex.org/works"
MANIFEST_NAME = "MANIFEST.md"

#: Feltnøklene i PREREG-v1 §4. Emne-ID-ene selv hører i ADDENDUM-01.
FIELD_KEYS = ("tekstvitenskap", "klinisk_epidemiologi", "arkeologi", "energimodellering")

#: Publiseringsvinduet er låst i PREREG-v1 §4.
YEAR_FROM, YEAR_TO = 2015, 2020

MANIFEST_HEADER = """# MANIFEST — rådata

Append-only. Hver rad er én fil under `data/raw/`, lagret urørt slik den kom
fra kilden. Filene committes aldri (ADR-0001); denne listen er beviset på hva
som ble hentet, når, og at det ikke er endret etterpå.

| filnavn | bytes | sha256 | kilde-URL | hentetidspunkt |
|---|---|---|---|---|
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


@dataclass(frozen=True)
class RawRecord:
    """Én lagret rå respons."""

    path: Path
    bytes_len: int
    sha256: str
    source_url: str
    harvested_at: str


def build_filter(topic_ids: Sequence[str], year_from: int = YEAR_FROM, year_to: int = YEAR_TO) -> str:
    """OpenAlex-filterstreng. has_fulltext:true er en låst rammebetingelse."""
    if not topic_ids:
        raise ValueError("minst én emne-ID kreves; de oppløste ID-ene føres i ADDENDUM-01")
    return ",".join(
        (
            "topics.id:" + "|".join(topic_ids),
            f"publication_year:{year_from}-{year_to}",
            "has_fulltext:true",
        )
    )


def _headers() -> dict[str, str]:
    # OpenAlex' polite pool ber om en kontaktadresse. Den sendes bare når
    # OPENALEX_MAILTO er satt eksplisitt i miljøet.
    ua = "gjenopptak/0.1.0 (+https://github.com/avalyset)"
    mailto = os.environ.get("OPENALEX_MAILTO", "").strip()
    if mailto:
        ua += f" mailto:{mailto}"
    return {"User-Agent": ua, "Accept": "application/json"}


def fetch_works(
    topic_ids: Sequence[str],
    *,
    per_page: int = 25,
    year_from: int = YEAR_FROM,
    year_to: int = YEAR_TO,
    timeout: float = 30.0,
) -> tuple[bytes, str]:
    """Ett kall. Returnerer (rå kroppsbytes, endelig URL).

    Ingen paginering her: røyktesten og trekkingen skal ikke kunne dra ned
    volum ved uhell. Trekking skjer først etter ADDENDUM-01 (PREREG-v1 §4).
    """
    params = {
        "filter": build_filter(topic_ids, year_from, year_to),
        "per-page": str(per_page),
        "select": "id,doi,title,publication_year,language,type,has_fulltext,"
        "open_access,best_oa_location,primary_location,topics",
    }
    with httpx.Client(headers=_headers(), timeout=timeout, follow_redirects=True) as client:
        r = client.get(API, params=params)
        r.raise_for_status()
        return r.content, str(r.url)


def write_raw(blob: bytes, source_url: str, raw_dir: Path, *, stem: str) -> RawRecord:
    """Lagre rå respons urørt og før den i MANIFEST.md."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    digest = sha256_bytes(blob)
    harvested_at = _now()
    path = raw_dir / f"{stem}-{digest[:12]}.json"
    path.write_bytes(blob)  # urørt: ingen reserialisering, ingen pen-utskrift

    manifest = raw_dir / MANIFEST_NAME
    if not manifest.exists():
        manifest.write_text(MANIFEST_HEADER, encoding="utf-8")
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write(f"| {path.name} | {len(blob)} | {digest} | {source_url} | {harvested_at} |\n")

    return RawRecord(path, len(blob), digest, source_url, harvested_at)


def _license_of(work: dict) -> str | None:
    for key in ("best_oa_location", "primary_location"):
        loc = work.get(key) or {}
        if loc.get("license"):
            return loc["license"]
    return None


def build_document(work: dict, *, field_key: str, raw: RawRecord) -> dict:
    """Avled én documents-post fra ett OpenAlex-work.

    Lisens avgjør om fulltekst kan lagres senere (ADR-0001). Her settes bare
    feltet; utelating skjer i fulltekst-leddet og telles med grunn.
    """
    if field_key not in FIELD_KEYS:
        raise ValueError(f"ukjent field_key: {field_key!r}")
    oid = work["id"]
    oa = work.get("open_access") or {}
    doi = work.get("doi")
    return {
        "schema_version": "documents-1",
        "doc_id": oid.rsplit("/", 1)[-1],
        "openalex_id": oid,
        "doi": doi.rsplit("doi.org/", 1)[-1] if doi else None,
        "title": work.get("title"),
        "field_key": field_key,
        "openalex_topic_ids": [t["id"] for t in (work.get("topics") or []) if t.get("id")],
        "publication_year": work["publication_year"],
        "has_fulltext": bool(work.get("has_fulltext")),
        "language": work.get("language"),
        "is_oa": oa.get("is_oa"),
        "license": _license_of(work),
        "fulltext_source": None,
        "fulltext_format": "none",
        "raw_path": str(raw.path),
        "raw_sha256": raw.sha256,
        "raw_bytes": raw.bytes_len,
        "source_url": raw.source_url,
        "harvested_at": raw.harvested_at,
        "excluded": False,
        "excluded_reason": None,
        "sample_seed": None,
        "is_control": False,
        "control_kind": None,
    }


def write_documents(records: Iterable[dict], out_path: Path, *, validate_each: bool = True) -> int:
    """Skriv documents.jsonl. Returnerer radantall.

    Ugyldig post stopper skrivingen. Kjeden skal feile, ikke fylle inn.
    """
    from ..schemas import validate

    rows = list(records)
    if validate_each:
        for row in rows:
            validate("documents", row)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return len(rows)
