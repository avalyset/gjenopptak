"""Sekvensiell trekking i frørekkefølge (ADDENDUM-09).

Rekkefølgen er stokkingen i ADDENDUM-01 §6.1: en ny ``random.Random(93883171)``
stokker feltets frosne, leksikografisk sorterte rammeliste. Trekkingen går
nedover rekkefølgen og tar et verk når alle vilkårene holder:

1. ikke positiv kontroll og ikke lest (ADDENDUM-02 §1);
2. ikke alt trukket i et felt som trekkes tidligere (ADDENDUM-02 §7, ``dobbeltramme``);
3. OpenAlex-typen er ikke erratum, paratext, retraction eller peer-review
   (ADDENDUM-01 §6, ``ikke_artikkel``);
4. minst én av feltets emne-ID-er blant verkets tre høyest rangerte topics
   (ADDENDUM-02 §7, ``utenfor_felt``);
5. porten gir tekst på P1 eller P3 (ADDENDUM-04 §1.1), med samme kode som rammeprøven;
6. teksten fra P3 består identitetsporten (ADDENDUM-07 §8).

Et verk som faller på et vilkår, er ikke i rammen og hoppes over. Ingen
substitusjon. Trekkingen stopper ved ``N_PER_FELT`` verk per felt.

For felt uten hentingsprøve på hele listen testes de første ``KARAKTERISERING``
posisjonene med porten uansett vilkår 1–4: et tilfeldig utsnitt av rålisten.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Sequence
from urllib.parse import urlparse

import httpx

from .fetchtest import FetchVerdict, read_verdicts, run_frame
from .recallset2 import identity_verdict

#: Prereg-frøet, ADDENDUM-01 §1: int("05988b23", 16).
PREREG_SEED = 0x05988B23
N_PER_FELT = 25
KARAKTERISERING = 200
#: Frysingsrekkefølgen. Avgjør bare ``dobbeltramme``: et verk trukket i et
#: tidligere felt hoppes over i et senere.
FELTREKKEFOLGE = ("energimodellering", "arkeologi", "klinisk_epidemiologi", "tekstvitenskap")
#: Felt med hentingsprøve på hele listen (ADDENDUM-08 §4). Verdiktene derfra brukes.
FULL_PROVE = {"energimodellering": ("fulltext-rammeprove-energimodellering", "verdikter-energimodellering.jsonl")}
#: OpenAlex-typer som er errata, innholdsfortegnelse eller lignende (ADDENDUM-01 §6).
IKKE_ARTIKKEL_TYPER = frozenset({"erratum", "paratext", "retraction", "peer-review"})
#: De positive kontrollene (ADDENDUM-08 §1.7). Fjernes før trekking (ADDENDUM-02 §1).
KONTROLL_VERK = frozenset({"W3000588547"})
KONTROLL_DOI = frozenset({
    "10.5525/gla.thesis.76774",          # H1, tekstvitenskap
    "10.1038/s41467-019-11357-9",        # H7, arkeologi
    "10.1016/s2468-2667(17)30217-7",     # H8, klinisk epidemiologi
    "10.1016/j.apenergy.2018.04.048",    # PREREG §7, energimodellering
})
UTVALG_TAG = "UTVALG-IKKE-LEST"
META_BATCH = 50
META_SELECT = "id,doi,display_name,type,topics,ids"
OPENALEX = "https://api.openalex.org/works"
REMAINING_FLOOR = 50


class DrawRefused(RuntimeError):
    """Trekkingen startes ikke: feil rekkefølge, eksisterende utvalg eller manglende liste."""


# --------------------------------------------------------------------------- #
# Rekkefølgen
# --------------------------------------------------------------------------- #

def draw_order(work_ids: Sequence[str], seed: int = PREREG_SEED) -> list[str]:
    """Stokkingen i ADDENDUM-01 §6.1 over den frosne, sorterte listen."""
    ids = list(work_ids)
    if ids != sorted(ids):
        raise ValueError("rammelisten må være leksikografisk sortert (ADDENDUM-01 §1)")
    if len(set(ids)) != len(ids):
        raise ValueError("rammelisten har duplikate work-ID-er")
    random.Random(seed).shuffle(ids)
    return ids


def order_sha256(order: Sequence[str]) -> str:
    return hashlib.sha256(("\n".join(order) + "\n").encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Vilkår 1–4
# --------------------------------------------------------------------------- #

def _norm_doi(d: str | None) -> str | None:
    if not d:
        return None
    d = d.strip().lower()
    return d.removeprefix("https://doi.org/").removeprefix("http://doi.org/") or None


def _norm_pmcid(p: object) -> str | None:
    digits = re.sub(r"\D", "", str(p or ""))
    return f"PMC{digits}" if digits else None


def _norm_title(t: str | None) -> str:
    return " ".join(re.findall(r"\w+", (t or "").casefold()))


@dataclass(frozen=True)
class Exclusions:
    """Kontrollene og leseloggen (ADDENDUM-02 §1), slik de sto da trekkingen startet."""

    read_works: frozenset
    read_dois: frozenset
    read_pmcids: frozenset
    read_titles: frozenset
    log_sha256: str
    n_log: int

    @classmethod
    def from_log(cls, path: Path) -> "Exclusions":
        blob = path.read_bytes()
        rows = json.loads(blob)
        uten_id = [x for x in rows if not (x.get("work") or x.get("doi") or x.get("pmcid"))]
        return cls(
            read_works=frozenset(x["work"] for x in rows if x.get("work")),
            read_dois=frozenset(_norm_doi(x["doi"]) for x in rows if x.get("doi")),
            read_pmcids=frozenset(_norm_pmcid(x["pmcid"]) for x in rows if x.get("pmcid")),
            read_titles=frozenset(_norm_title(x.get("tittel")) for x in uten_id if x.get("tittel")),
            log_sha256=hashlib.sha256(blob).hexdigest(),
            n_log=len(rows),
        )

    def reason(self, row: dict, meta: dict | None) -> str | None:
        doi = _norm_doi(row.get("doi")) or _norm_doi((meta or {}).get("doi"))
        if row["work_id"] in KONTROLL_VERK or doi in KONTROLL_DOI:
            return "kontroll"
        if row["work_id"] in self.read_works or (doi and doi in self.read_dois):
            return "lest"
        if meta:
            pm = _norm_pmcid((meta.get("ids") or {}).get("pmcid"))
            if pm and pm in self.read_pmcids:
                return "lest"
            if self.read_titles and _norm_title(meta.get("display_name")) in self.read_titles:
                return "lest"
        return None


def top3_topics(meta: dict) -> list[str]:
    """Verkets tre høyest rangerte topics, etter score."""
    ts = sorted(meta.get("topics") or [], key=lambda t: -(t.get("score") or 0.0))
    return [t["id"].rsplit("/", 1)[-1] for t in ts[:3] if t.get("id")]


def in_field(meta: dict, field_ids: Iterable[str]) -> bool:
    ids = set(field_ids)
    return any(t in ids for t in top3_topics(meta))


# --------------------------------------------------------------------------- #
# Beslutningsløkken
# --------------------------------------------------------------------------- #

@dataclass
class Decision:
    """Én rad i trekkloggen."""

    trekkposisjon: int
    work_id: str
    doi: str | None
    aar: int | None
    utfall: str                    # trukket | hoppet | etter-stopp
    grunn: str | None
    utvalgsnr: int | None
    karakterisering: bool
    vert_raa: str
    type: str | None = None
    topics_topp3: list | None = None
    port_testet: bool = False
    port_inne: bool | None = None
    port_ledd: str | None = None
    port_grunn: str | None = None
    identitet: str | None = None
    sha256: str | None = None
    fil: str | None = None
    bytes: int | None = None

    def as_row(self) -> dict:
        return asdict(self)


def raw_host(row: dict) -> str:
    u = (row.get("best_oa_location") or {}).get("pdf_url")
    return urlparse(u).netloc.lower().replace("www.", "") if u else "(ingen PDF-lenke)"


def decide(order: Sequence[str], rows_by_id: dict[str, dict], *, field_ids: Iterable[str],
           exclusions: Exclusions, drawn_elsewhere: set[str],
           meta_for: Callable[[int, str], dict | None],
           verdict_for: Callable[[int, dict], FetchVerdict],
           text_for: Callable[[FetchVerdict], str],
           n: int = N_PER_FELT, n_char: int = 0) -> list[Decision]:
    """Gå nedover rekkefølgen. Nettkall skjer bare i callbackene."""
    field_ids = set(field_ids)
    ut: list[Decision] = []
    valgt = 0
    for pos, wid in enumerate(order, 1):
        karakter = pos <= n_char
        if valgt >= n and not karakter:
            break
        row = rows_by_id[wid]
        meta = meta_for(pos, wid)
        d = Decision(trekkposisjon=pos, work_id=wid, doi=row.get("doi"), aar=row.get("publication_year"),
                     utfall="", grunn=None, utvalgsnr=None, karakterisering=karakter, vert_raa=raw_host(row))
        if meta is not None:
            d.type, d.topics_topp3 = meta.get("type"), top3_topics(meta)

        grunn = exclusions.reason(row, meta)
        if grunn is None and wid in drawn_elsewhere:
            grunn = "dobbeltramme"
        if grunn is None and meta is None:
            grunn = "mangler-metadata"
        if grunn is None and meta.get("type") in IKKE_ARTIKKEL_TYPER:
            grunn = f"ikke_artikkel:{meta.get('type')}"
        if grunn is None and not in_field(meta, field_ids):
            grunn = "utenfor_felt"

        trenger_port = karakter or (grunn is None and valgt < n)
        if trenger_port:
            v = verdict_for(pos, row)
            d.port_testet, d.port_inne, d.port_ledd, d.port_grunn = True, v.in_frame, v.gate, v.reason
            if v.in_frame:
                d.sha256, d.fil, d.bytes = v.sha256, v.file, v.bytes
                if v.gate == "P3-PDF":
                    iv = identity_verdict(text_for(v), title=(meta or {}).get("display_name") or "",
                                          doi=row.get("doi"))
                    d.identitet = ("ok-doi" if iv.doi_funnet else "ok-tittel") if iv.ok else \
                        f"feil:{iv.grunn or 'ukjent'}"
                else:
                    d.identitet = "p1-doi"
            if grunn is None and valgt < n:
                if not v.in_frame:
                    grunn = f"port:{v.reason or 'ukjent'}"
                elif d.identitet and d.identitet.startswith("feil:"):
                    grunn = f"identitet:{d.identitet[5:]}"

        if valgt < n and grunn is None:
            valgt += 1
            d.utfall, d.utvalgsnr = "trukket", valgt
        elif valgt < n:
            d.utfall, d.grunn = "hoppet", grunn
        else:
            d.utfall, d.grunn = "etter-stopp", grunn
        ut.append(d)
    return ut


# --------------------------------------------------------------------------- #
# Karakterisering
# --------------------------------------------------------------------------- #

def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson-intervall, 95 %."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    den = 1 + z * z / n
    sentrum = (p + z * z / (2 * n)) / den
    halv = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, sentrum - halv), min(1.0, sentrum + halv)


def failure_category(reason: str | None) -> str:
    """Portens frafallsgrunn i samme kategorier som ADDENDUM-08 §3.1."""
    rs = reason or ""
    if rs.startswith("http-403"):
        return "403"
    if rs.startswith("http-200"):
        return "HTML i stedet for PDF"
    if rs.startswith("http-404"):
        return "404"
    if rs.startswith("http-5"):
        return "5xx"
    if rs.startswith("http-"):
        return "annen HTTP-status"
    if rs.startswith("pdf-uten-tekst"):
        return "PDF uten tekst"
    if rs == "ingen-pdf-lenke":
        return "ingen PDF-lenke"
    if rs.startswith("jats-"):
        return "JATS uten nok tekst"
    if "Redirect" in rs:
        return "for mange omdirigeringer"
    return "nettverksfeil" if rs else "ukjent"


def characterize(decisions: Sequence[Decision], *, top: int = 10) -> dict:
    ds = [d for d in decisions if d.karakterisering]
    inne = [d for d in ds if d.port_inne]
    p3 = [d for d in inne if d.port_ledd == "P3-PDF"]
    ident_ok = [d for d in p3 if (d.identitet or "").startswith("ok")]
    raa = Counter(d.vert_raa for d in ds)
    hb = Counter(d.vert_raa for d in inne)
    lo, hi = wilson(len(inne), len(ds))
    return {
        "n_forsok": len(ds),
        "hentbar": len(inne),
        "andel": len(inne) / len(ds) if ds else 0.0,
        "wilson95": [lo, hi],
        "per_ledd": dict(Counter(d.port_ledd for d in inne)),
        "p3_identitet_ok": len(ident_ok),
        "p3_inne": len(p3),
        "hentbar_med_identitet": len(inne) - len(p3) + len(ident_ok),
        "frafall": dict(Counter(failure_category(d.port_grunn) for d in ds if not d.port_inne).most_common()),
        "verter": [{"vert": h, "raa": nr, "hentbar": hb.get(h, 0)} for h, nr in raa.most_common(top)],
    }


# --------------------------------------------------------------------------- #
# Filer
# --------------------------------------------------------------------------- #

def utvalg_rows(decisions: Sequence[Decision]) -> list[dict]:
    return [{"work_id": d.work_id, "doi": d.doi, "aar": d.aar, "trekkposisjon": d.trekkposisjon,
             "port_ledd": d.port_ledd, "sha256": d.sha256}
            for d in sorted((d for d in decisions if d.utfall == "trukket"), key=lambda d: d.trekkposisjon)]


def write_jsonl(rows: Iterable[dict], path: Path) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    tekst = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    path.write_text(tekst, encoding="utf-8")
    return tekst.count("\n"), hashlib.sha256(tekst.encode("utf-8")).hexdigest()


def drawn_in_earlier_fields(utvalg_dir: Path, field_key: str) -> set[str]:
    """Work-ID-ene trukket i feltene før ``field_key``. Mangler ett, startes ingenting."""
    tidligere = FELTREKKEFOLGE[:FELTREKKEFOLGE.index(field_key)]
    ut: set[str] = set()
    for f in tidligere:
        p = utvalg_dir / f"utvalg-{f}.jsonl"
        if not p.exists():
            raise DrawRefused(f"{f} er ikke trukket; feltrekkefølgen er {', '.join(FELTREKKEFOLGE)}")
        ut |= {json.loads(l)["work_id"] for l in p.read_text(encoding="utf-8").splitlines() if l.strip()}
    return ut


def assert_not_drawn(utvalg_dir: Path, field_key: str) -> None:
    p = utvalg_dir / f"utvalg-{field_key}.jsonl"
    if p.exists():
        raise DrawRefused(f"{p} finnes: et utvalg trekkes én gang og overskrives aldri")


def pdf_text(pdf_bytes: bytes, tmp_dir: Path, name: str) -> str:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    p = tmp_dir / f"{name}.pdf"
    p.write_bytes(pdf_bytes)
    try:
        out = subprocess.run(["pdftotext", "-q", str(p), "-"], capture_output=True, text=True, timeout=180)
        return out.stdout
    except (subprocess.SubprocessError, OSError):
        return ""
    finally:
        p.unlink(missing_ok=True)


class MetaFetcher:
    """OpenAlex-metadata i bolker av ``META_BATCH`` work-ID-er, i trekkrekkefølge."""

    def __init__(self, client: httpx.Client, order: Sequence[str], raw_dir: Path, stem: str) -> None:
        from .openalex import write_raw
        self._write_raw = write_raw
        self.c, self.order, self.raw_dir, self.stem = client, list(order), raw_dir, stem
        self.cache: dict[str, dict | None] = {}
        self.calls = 0
        self.remaining: int | None = None

    def __call__(self, pos: int, wid: str) -> dict | None:
        if wid not in self.cache:
            bolk = [w for w in self.order[pos - 1:pos - 1 + META_BATCH] if w not in self.cache]
            self.fetch(bolk, pos)
        return self.cache[wid]

    def fetch(self, ids: list[str], pos: int) -> None:
        if self.remaining is not None and self.remaining < REMAINING_FLOOR:
            raise DrawRefused(f"OpenAlex remaining {self.remaining} under gulvet {REMAINING_FLOOR}")
        r = self.c.get(OPENALEX, params={"filter": "ids.openalex:" + "|".join(ids),
                                         "per-page": str(len(ids)), "select": META_SELECT})
        self.calls += 1
        rem = r.headers.get("x-ratelimit-remaining")
        self.remaining = int(rem) if rem is not None else self.remaining
        r.raise_for_status()
        self._write_raw(r.content, str(r.url), self.raw_dir, stem=f"{self.stem}-{pos:05d}")
        funnet = {x["id"].rsplit("/", 1)[-1]: x for x in json.loads(r.content)["results"]}
        for w in ids:
            self.cache[w] = funnet.get(w)


# --------------------------------------------------------------------------- #
# Kjøring
# --------------------------------------------------------------------------- #

from ..vault import krev  # ADR-0009


def main(argv: list[str] | None = None) -> int:
    """Trekk ett felt. Exit 0: n trukket. 1: færre enn n. 2: ikke startet."""
    import argparse

    from ..vault import require_vault, sha256_file, copy_verified
    from .coverage import TOPIC_IDS, client

    ap = argparse.ArgumentParser(description="Sekvensiell trekking i frørekkefølge (ADDENDUM-09).")
    ap.add_argument("--field", choices=list(FELTREKKEFOLGE), required=True)
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args(argv)
    args.data_dir = krev(getattr(args, 'data_dir', None))  # ADR-0009: ingen fallback

    felt, data = args.field, args.data_dir
    utdir = data / "utvalg"
    try:
        vault = require_vault()
        assert_not_drawn(utdir, felt)
        tidligere = drawn_in_earlier_fields(utdir, felt)
        liste = data / "frames" / f"frame-{felt}-RAW.jsonl"
        if not liste.exists():
            raise DrawRefused(f"{liste} finnes ikke: feltet er ikke frosset")
    except (DrawRefused, OSError) as e:
        print(f"IKKE STARTET: {e}", file=sys.stderr)
        return 2

    rows = [json.loads(l) for l in liste.open(encoding="utf-8")]
    by_id = {r["work_id"]: r for r in rows}
    order = draw_order([r["work_id"] for r in rows])
    excl = Exclusions.from_log(data / "leste-kontrollkandidater.json")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    spes = {
        "felt": felt, "tid": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "frø": PREREG_SEED, "python": sys.version.split()[0], "commit": commit,
        "rammeliste": liste.name, "rammeliste_sha256": sha256_file(liste), "N": len(rows),
        "rekkefolge_sha256": order_sha256(order), "leselogg_sha256": excl.log_sha256, "leselogg_rader": excl.n_log,
        "tidligere_trukket": len(tidligere), "n": N_PER_FELT,
        "karakterisering": 0 if felt in FULL_PROVE else KARAKTERISERING,
    }
    write_jsonl([spes], utdir / f"trekkspesifikasjon-{felt}.jsonl")

    tmp = data / "tmp-trekking"
    tekster: dict[str, str] = {}
    if felt in FULL_PROVE:
        katalog, vfil = FULL_PROVE[felt]
        filer = vault / katalog
        verdikter = read_verdicts(filer / vfil)
        n_char = 0

        def verdict_for(pos: int, row: dict) -> FetchVerdict:
            return verdikter[row["work_id"]]
    else:
        filer = vault / f"trekking-{felt}"
        vfil = filer / f"verdikter-trekking-{felt}.jsonl"
        n_char = KARAKTERISERING
        forste = [by_id[w] for w in order[:n_char]]
        st = run_frame(forste, filer, tmp, vfil, workers=args.workers)
        if st.stopped:
            print(f"STOPPET under karakteriseringen: {st.stopped}", file=sys.stderr)
            return 1
        verdikter = read_verdicts(vfil)
        (filer / "LES-MEG.md").write_text(
            f"# Trekking — {felt}\n\nFilene er hentet av trekkingen etter ADDENDUM-09, med porten fra "
            "hentingsprøven (ADDENDUM-04 §1.1). Posisjonene 1–200 i trekkrekkefølgen er karakterisering "
            "(RAMMEPRØVE-IKKE-LEST). De trukne verkene (UTVALG-IKKE-LEST) står i `utvalg-" + felt + ".jsonl` "
            "og er kopiert til `../utvalg/" + felt + "/`. Ingen fil er lest.\n", encoding="utf-8")

        def verdict_for(pos: int, row: dict) -> FetchVerdict:
            if row["work_id"] not in verdikter:
                neste = [by_id[w] for w in order[pos - 1:pos - 1 + 50] if w not in verdikter]
                s = run_frame(neste, filer, tmp, vfil, workers=args.workers)
                if s.stopped:
                    raise RuntimeError(f"hentingen stoppet: {s.stopped}")
                verdikter.update(read_verdicts(vfil))
            return verdikter[row["work_id"]]

    def text_for(v: FetchVerdict) -> str:
        if v.sha256 not in tekster:
            tekster[v.sha256] = pdf_text((filer / v.file).read_bytes(), tmp, v.work_id)
        return tekster[v.sha256]

    with client() as c:
        meta = MetaFetcher(c, order, data / "raw", stem=f"trekk-meta-{felt}")
        beslutninger = decide(order, by_id, field_ids=TOPIC_IDS[felt], exclusions=excl,
                              drawn_elsewhere=tidligere, meta_for=meta, verdict_for=verdict_for,
                              text_for=text_for, n=N_PER_FELT, n_char=n_char)

    logg_n, logg_sha = write_jsonl((d.as_row() for d in beslutninger), utdir / f"trekklogg-{felt}.jsonl")
    utv = utvalg_rows(beslutninger)
    utv_n, utv_sha = write_jsonl(utv, utdir / f"utvalg-{felt}.jsonl")

    ut_katalog = vault / "utvalg" / felt
    manifest = [f"# Utvalg — {felt}\n\n**{UTVALG_TAG}** — trukket etter ADDENDUM-09. Ingen setning er lest, "
                "ingen hindringsklasse tildelt.\n\n| trekkposisjon | work_id | ledd | fil | bytes | sha256 |\n"
                "|---|---|---|---|---|---|\n"]
    for d in sorted((d for d in beslutninger if d.utfall == "trukket"), key=lambda d: d.trekkposisjon):
        res = copy_verified(filer / d.fil, ut_katalog)
        if res.mismatch or res.sha256 != d.sha256:
            print(f"AVVIK ved kopiering av {d.fil}", file=sys.stderr)
            return 1
        manifest.append(f"| {d.trekkposisjon} | {d.work_id} | {d.port_ledd} | {d.fil} | {d.bytes} | {d.sha256} |\n")
    (ut_katalog / "MANIFEST-UTVALG.md").write_text("".join(manifest), encoding="utf-8")

    karakter = characterize(beslutninger) if n_char else None
    if karakter:
        (utdir / f"karakterisering-{felt}.json").write_text(json.dumps(karakter, ensure_ascii=False, indent=1) + "\n",
                                                              encoding="utf-8")
    for p in sorted(utdir.glob(f"*-{felt}.json*")):
        copy_verified(p, vault / "utvalg")

    print(f"felt              : {felt}")
    print(f"rekkefølge sha256 : {spes['rekkefolge_sha256']}")
    print(f"posisjoner besøkt : {len(beslutninger)}")
    print(f"trukket           : {utv_n} av {N_PER_FELT}")
    print(f"utvalg            : {utdir / f'utvalg-{felt}.jsonl'}  sha256 {utv_sha}")
    print(f"trekklogg         : {logg_n} rader  sha256 {logg_sha}")
    print(f"hoppet over       : {dict(Counter((d.grunn or '').split(':')[0] for d in beslutninger if d.utfall == 'hoppet'))}")
    if karakter:
        lo, hi = karakter["wilson95"]
        print(f"karakterisering   : {karakter['hentbar']}/{karakter['n_forsok']} = {karakter['andel']:.1%} "
              f"(95 % {lo:.1%}–{hi:.1%}); med identitet {karakter['hentbar_med_identitet']}")
    print(f"OpenAlex-kall     : {meta.calls}  remaining {meta.remaining}")
    return 0 if utv_n == N_PER_FELT else 1


if __name__ == "__main__":
    raise SystemExit(main())
