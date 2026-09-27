"""Frysing av rammelisten for ett felt (ADDENDUM-04 §5, ADDENDUM-01 §1).

Ett felt per døgn. Kvoten er 1 000 kall i døgnet uten polite pool, og en frysing
som stopper midt i er en ubrukelig liste og et tapt døgn — derfor to vakter:

1. **Forhåndssjekk.** Kvoten leses før pagineringen begynner. Er det ikke nok
   kall igjen for hele listen med margin, startes ingenting.
2. **Løpende vakt.** Faller ``x-ratelimit-remaining`` under terskelen, stopper
   pagineringen, det som er hentet skrives, og filen merkes ufullstendig i
   manifestet med cursoren den kom til.

Listen sorteres på work-ID, slik at den er byte-identisk ved gjenkjøring, og
lagres med sha256. Frøet alene gir ikke determinisme (ADDENDUM-01 §1) — frøet
pluss denne filens sha256 gjør det.

Ingen fulltekst hentes her. Hentingsprøven som avgjør rammemedlemskap etter
ADDENDUM-04 §1 er et eget steg og bruker ikke OpenAlex.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import httpx

from ..vault import VaultUnavailable, secure_frame_file
from .coverage import frame_filter, client
from .openalex import write_raw

OPENALEX = "https://api.openalex.org/works"
PER_PAGE = 200
SELECT = "id,doi,publication_year,primary_topic,open_access,best_oa_location"

#: Under dette antallet gjenstående kall stopper frysingen.
REMAINING_FLOOR = 50

#: Margin over det beregnede sidetallet som kreves før frysingen starter.
#: Den kan ikke være lavere enn gulvet: starter frysingen med færre enn
#: sidetall + gulv kall igjen, faller remaining under gulvet før siste side, og
#: listen blir garantert ufullstendig — et tapt døgn. Sidetall + 50 er regelen.
START_MARGIN = REMAINING_FLOOR


class QuotaTooLow(RuntimeError):
    """Ikke nok kvote til å fullføre. Ingenting er hentet."""


@dataclass
class FreezeResult:
    field_key: str
    filter_str: str
    total_expected: int | None = None
    rows: list[dict] = field(default_factory=list)
    calls_used: int = 0
    remaining_at_end: int | None = None
    complete: bool = False
    stopped_at_cursor: str | None = None
    started_at: str = ""
    finished_at: str = ""

    @property
    def n_rows(self) -> int:
        return len(self.rows)


def _limits(r: httpx.Response) -> tuple[int | None, int | None]:
    def num(name: str) -> int | None:
        v = r.headers.get(name)
        try:
            return int(v) if v is not None else None
        except ValueError:
            return None
    return num("x-ratelimit-remaining"), num("x-ratelimit-limit")


def check_quota(c: httpx.Client, filter_str: str, raw_dir: Path, *, stem: str) -> tuple[int, int, int]:
    """Ett kall: (antall verk, gjenstående kall, sider som kreves)."""
    r = c.get(OPENALEX, params={"filter": filter_str, "per-page": "1", "select": "id"})
    remaining, limit = _limits(r)
    if r.status_code != 200:
        raise QuotaTooLow(
            f"kvotesjekk ga HTTP {r.status_code}; remaining={remaining}, "
            f"retry-after={r.headers.get('retry-after')}s. Ingenting er hentet."
        )
    write_raw(r.content, str(r.url), raw_dir, stem=stem)
    total = int(json.loads(r.content)["meta"]["count"])
    pages = -(-total // PER_PAGE)  # tak-divisjon
    return total, (remaining if remaining is not None else -1), pages


def to_row(work: dict) -> dict:
    """Én rad i RAW-listen. Ingen avledning, ingen tolkning."""
    pt = work.get("primary_topic") or {}
    oa = work.get("open_access") or {}
    bol = work.get("best_oa_location") or {}
    doi = work.get("doi")
    return {
        "work_id": work["id"].rsplit("/", 1)[-1],
        "openalex_id": work["id"],
        "doi": doi.replace("https://doi.org/", "").lower() if doi else None,
        "publication_year": work.get("publication_year"),
        "primary_topic_id": pt.get("id", "").rsplit("/", 1)[-1] or None,
        "primary_topic_name": pt.get("display_name"),
        "oa_status": oa.get("oa_status"),
        "is_oa": oa.get("is_oa"),
        "best_oa_location": {
            "pdf_url": bol.get("pdf_url"),
            "landing_page_url": bol.get("landing_page_url"),
            "license": bol.get("license"),
            "version": bol.get("version"),
            "source": (bol.get("source") or {}).get("display_name"),
        },
    }


def freeze_field(
    field_key: str,
    raw_dir: Path,
    *,
    floor: int = REMAINING_FLOOR,
    margin: int = START_MARGIN,
    max_pages: int | None = None,
    http: httpx.Client | None = None,
) -> FreezeResult:
    """Hent hele rammelisten for ett felt med cursor-paginering.

    ``http`` lar en test injisere en klient med egen transport; i produksjon
    opprettes klienten her.
    """
    margin = max(margin, floor)          # se START_MARGIN
    filter_str = frame_filter(field_key)
    res = FreezeResult(field_key=field_key, filter_str=filter_str,
                       started_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    egen_klient = http is None
    c = http or client()
    try:
        total, remaining, pages = check_quota(c, filter_str, raw_dir, stem=f"freeze-count-{field_key}")
        res.total_expected = total
        res.calls_used = 1
        if remaining >= 0 and remaining < pages + margin:
            raise QuotaTooLow(
                f"{field_key}: listen krever {pages} sider, kvoten har {remaining} kall igjen "
                f"(margin {margin}). Ingenting er hentet — kom tilbake når kvoten er nullstilt."
            )

        cursor = "*"
        page = 0
        while cursor:
            if max_pages is not None and page >= max_pages:
                res.stopped_at_cursor = cursor
                break
            r = c.get(OPENALEX, params={"filter": filter_str, "per-page": str(PER_PAGE),
                                        "cursor": cursor, "select": SELECT})
            res.calls_used += 1
            remaining, _ = _limits(r)
            res.remaining_at_end = remaining
            if r.status_code != 200:
                res.stopped_at_cursor = cursor
                break
            write_raw(r.content, str(r.url), raw_dir, stem=f"freeze-{field_key}-p{page:04d}")
            payload = json.loads(r.content)
            batch = payload["results"]
            res.rows.extend(to_row(w) for w in batch)
            cursor = (payload.get("meta") or {}).get("next_cursor")
            page += 1
            if not batch:
                break
            if remaining is not None and remaining < floor:
                res.stopped_at_cursor = cursor
                break
    finally:
        if egen_klient:
            c.close()

    res.rows.sort(key=lambda x: x["work_id"])
    res.complete = res.stopped_at_cursor is None and res.n_rows >= (res.total_expected or 0)
    res.finished_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return res


def write_frame(res: FreezeResult, out_dir: Path) -> tuple[Path, str]:
    """Skriv RAW-listen og returner (sti, sha256)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = "" if res.complete else "-UFULLSTENDIG"
    path = out_dir / f"frame-{res.field_key}-RAW{suffix}.jsonl"
    with path.open("w", encoding="utf-8") as fh:
        for row in res.rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return path, digest


def note_in_manifest(res: FreezeResult, path: Path, digest: str, raw_dir: Path) -> None:
    """Før frysingen i MANIFEST.md, med tilstand."""
    manifest = raw_dir / "MANIFEST.md"
    tilstand = "KOMPLETT" if res.complete else f"UFULLSTENDIG (stoppet ved cursor {res.stopped_at_cursor})"
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write(
            f"| {path.name} | {path.stat().st_size} | {digest} | frysing: {res.filter_str} "
            f"| {res.finished_at} | rader={res.n_rows}/{res.total_expected} kall={res.calls_used} "
            f"remaining={res.remaining_at_end} {tilstand} |\n"
        )


# --------------------------------------------------------------------------- #
# CLI: python -m gjenopptak.harvest.freeze --field energimodellering
# --------------------------------------------------------------------------- #

from ..vault import krev  # ADR-0009


def main(argv: list[str] | None = None) -> int:
    """Frys ett felt. Returnerer 0 komplett, 1 ufullstendig, 2 ikke startet."""
    import argparse
    import sys

    from .coverage import TOPIC_IDS

    ap = argparse.ArgumentParser(description="Frys rammelisten for ett felt (ett felt per døgn).")
    ap.add_argument("--field", choices=list(TOPIC_IDS), required=True)
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--floor", type=int, default=REMAINING_FLOOR)
    ap.add_argument("--margin", type=int, default=START_MARGIN)
    ap.add_argument("--max-pages", type=int, default=None,
                    help="Bare for prøvekjøring; en avkortet liste merkes UFULLSTENDIG.")
    ap.add_argument("--no-vault", action="store_true",
                    help="Ikke sikre til Vault. Bruk bare når volumet med vilje er utilgjengelig.")
    args = ap.parse_args(argv)
    args.data_dir = krev(getattr(args, 'data_dir', None))  # ADR-0009: ingen fallback

    raw_dir = args.data_dir / "raw"
    try:
        res = freeze_field(args.field, raw_dir, floor=args.floor, margin=args.margin,
                           max_pages=args.max_pages)
    except QuotaTooLow as e:
        print(f"STOPPET FØR START: {e}", file=sys.stderr)
        return 2

    path, digest = write_frame(res, args.data_dir / "frames")
    note_in_manifest(res, path, digest, raw_dir)

    # En frossen liste som bare finnes ett sted er et kvotedøgn i risiko:
    # å hente den på nytt koster 1 000 kall og ~11 timers nullstilling.
    # Sikringen skjer i samme kjøring, med sha256-verifisering.
    vault_note = ""
    if not args.no_vault:
        try:
            vr = secure_frame_file(path)
            vault_note = f"{vr.dst}  (sha256 verifisert)"
        except (VaultUnavailable, OSError) as e:
            vault_note = f"IKKE SIKRET: {e}"

    print(f"felt        : {res.field_key}")
    print(f"filter      : {res.filter_str}")
    print(f"forventet   : {res.total_expected} verk")
    print(f"hentet      : {res.n_rows} rader")
    print(f"kall brukt  : {res.calls_used}")
    print(f"remaining   : {res.remaining_at_end}")
    print(f"komplett    : {'JA' if res.complete else 'NEI - stoppet ved ' + str(res.stopped_at_cursor)}")
    print(f"fil         : {path}")
    print(f"sha256      : {digest}")
    print(f"vault       : {vault_note or '(hoppet over med --no-vault)'}")
    if vault_note.startswith("IKKE SIKRET"):
        print("ADVARSEL: listen finnes bare på systemdisken.", file=sys.stderr)
        return 3
    return 0 if res.complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
