"""Røyktest for L0: ett OpenAlex-kall, maks 10 works, ett felt.

    python -m gjenopptak.harvest.smoketest --field energimodellering --limit 10

Hensikten er å vise at kjeden virker ende-til-ende på L0: kall → rådata urørt
på disk → manifestrad → avledet documents.jsonl. Den er **ikke** trekking av
utvalget. Trekkingen skjer først etter at ADDENDUM-01 er skrevet med frø og
oppløste emne-ID-er (PREREG-v1 §4), og den bruker ikke emne-ID-en under.

Fulltekst hentes ikke, hverken her eller i volum.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx

from .openalex import (
    FIELD_KEYS,
    build_document,
    fetch_works,
    write_documents,
    write_raw,
    _headers,  # noqa: F401  (samme kontaktpolicy som i fetch_works)
)

TOPICS_API = "https://api.openalex.org/topics"

#: Søkeord per felt, kun for å finne en emne-ID til røyktesten. Den oppløste
#: ID-en herfra har ingen status som utvalgsramme.
SMOKE_TOPIC_QUERY = {
    "tekstvitenskap": "textual criticism",
    "klinisk_epidemiologi": "clinical epidemiology",
    "arkeologi": "archaeology",
    "energimodellering": "power system modeling",
}


def resolve_smoke_topic(field_key: str, raw_dir: Path) -> tuple[str, str]:
    """Slå opp én emne-ID for røyktesten. Rå respons lagres med manifest."""
    query = SMOKE_TOPIC_QUERY[field_key]
    with httpx.Client(headers=_headers(), timeout=30.0, follow_redirects=True) as client:
        r = client.get(TOPICS_API, params={"search": query, "per-page": "1"})
        r.raise_for_status()
        blob, url = r.content, str(r.url)
    write_raw(blob, url, raw_dir, stem=f"topics-{field_key}")
    results = json.loads(blob)["results"]
    if not results:
        raise SystemExit(f"fant ingen emne-ID for {query!r}")
    return results[0]["id"], results[0]["display_name"]


from ..vault import krev  # ADR-0009


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--field", choices=FIELD_KEYS, default="energimodellering")
    ap.add_argument("--limit", type=int, default=10, help="maks works i kallet (<= 10)")
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--topic-id", default=None, help="hopp over emneoppslaget")
    args = ap.parse_args(argv)
    args.data_dir = krev(getattr(args, 'data_dir', None))  # ADR-0009: ingen fallback

    if args.limit > 10:
        ap.error("røyktesten henter maks 10 works")

    raw_dir = args.data_dir / "raw"
    if args.topic_id:
        topic_id, topic_name = args.topic_id, "(oppgitt)"
    else:
        topic_id, topic_name = resolve_smoke_topic(args.field, raw_dir)
    print(f"felt        : {args.field}")
    print(f"emne (røyk) : {topic_id}  {topic_name}")

    blob, url = fetch_works([topic_id], per_page=args.limit)
    raw = write_raw(blob, url, raw_dir, stem=f"works-{args.field}")
    print(f"rådata      : {raw.path}  {raw.bytes_len} bytes")
    print(f"sha256      : {raw.sha256}")
    print(f"kilde-URL   : {raw.source_url}")
    print(f"hentet      : {raw.harvested_at}")

    payload = json.loads(blob)
    docs = [build_document(w, field_key=args.field, raw=raw) for w in payload["results"]]
    out = args.data_dir / "documents.jsonl"
    n = write_documents(docs, out)
    print(f"documents   : {out}  {n} rader")
    print(f"treff totalt i OpenAlex (meta.count): {payload['meta']['count']}")
    print("fulltekst   : ikke hentet (L0 fester bare rammen)")
    print("utvalg      : IKKE trukket — ADDENDUM-01 mangler frø og emne-ID-er")
    return 0


if __name__ == "__main__":
    sys.exit(main())
