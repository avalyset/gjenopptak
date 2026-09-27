"""Hentbarhetsmåling for ADDENDUM-01.

Skiller fire rammer for samme felt og vindu:

* ``R0`` feltet og vinduet, uten hentbarhetskrav
* ``R1`` ``has_fulltext:true`` — OpenAlex' eget indekseringsflagg (prereg-rammen)
* ``R2`` ``R1 AND is_oa:true``
* ``R3`` ``best_oa_location.pdf_url`` finnes — hentbar PDF
* ``R4`` finnes i Europe PMC med JATS-XML — hentbar XML, seksjoner ferdig merket

``best_oa_location.pdf_url`` er **ikke et filtrerbart felt** i OpenAlex (API-et
svarer 400). R3 kan derfor ikke telles, bare estimeres: et frøsatt tilfeldig
utsnitt hentes med ``sample``/``seed``, andelen med ``pdf_url`` måles, og
andelen ganges opp mot den tellbare rammen. Wilson-intervall oppgis; punktet
alene ville skjult at tallet er et estimat.

Alle nettkall lagrer rå respons urørt under ``data/raw/`` med rad i
MANIFEST.md (ADR-0001). Ingen fulltekst hentes: PDF-lenker og XML-endepunkter
telles, aldri lastes ned.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import httpx

from .openalex import YEAR_FROM, YEAR_TO, _headers, write_raw

OPENALEX = "https://api.openalex.org"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

#: Frø for dekningsmålingen. Ikke prereg-frøet: utsnittene her er
#: måleinstrumenter og inngår ikke i utvalget (PREREG-v1 §4).
COVERAGE_SEED_PHRASE = "ADDENDUM-01 dekningsmaaling"
COVERAGE_SEED_HEX = hashlib.sha256(COVERAGE_SEED_PHRASE.encode("utf-8")).hexdigest()[:8]
COVERAGE_SEED_INT = int(COVERAGE_SEED_HEX, 16) % 1_000_000

# is_oa finnes bare inne i open_access; som toppnivåfelt gir det 400.
WORK_SELECT = "id,doi,title,publication_year,cited_by_count,has_fulltext,open_access,best_oa_location,primary_location"


#: Statuskoder som er verdt et nytt forsøk. Europe PMC svarer sporadisk 404 på
#: en query som virker ved neste forsøk — målt: samme DOI-søk ga 404 med
#: pageSize=25 og 200 med pageSize=30 i samme sekund.
_RETRY_STATUS = (404, 425, 429, 500, 502, 503, 504)


def _get(
    client: httpx.Client,
    url: str,
    params: dict[str, str],
    raw_dir: Path,
    stem: str,
    *,
    retries: int = 5,
) -> Any:
    """Hent, lagre rå respons, returner parset JSON. Bare vellykkede svar
    havner i manifestet — det skal være loggen over det som faktisk ble brukt."""
    last: httpx.Response | None = None
    for attempt in range(retries):
        r = client.get(url, params=params)
        if r.status_code == 200:
            write_raw(r.content, str(r.url), raw_dir, stem=stem)
            return json.loads(r.content)
        last = r
        if r.status_code in _RETRY_STATUS:
            # 429 krever tålmodighet, ikke iver: OpenAlex avviser bursts selv
            # godt under dagskvoten. Målt under diagnostikken i ADDENDUM-02.
            ventetid = 10.0 * (attempt + 1) if r.status_code == 429 else 1.5 ** attempt
            time.sleep(ventetid)
            continue
        r.raise_for_status()
    assert last is not None
    last.raise_for_status()


def client() -> httpx.Client:
    return httpx.Client(headers=_headers(), timeout=60.0, follow_redirects=True)


# --------------------------------------------------------------------------- #
# STEG 1: emne-ID-er
# --------------------------------------------------------------------------- #

def search_topics(c: httpx.Client, query: str, raw_dir: Path, *, per_page: int = 10) -> list[dict]:
    stem = "topics-search-" + query.replace(" ", "_")[:40]
    payload = _get(c, f"{OPENALEX}/topics", {"search": query, "per-page": str(per_page)}, raw_dir, stem)
    return payload["results"]


def get_topic(c: httpx.Client, topic_id: str, raw_dir: Path) -> dict:
    short = topic_id.rsplit("/", 1)[-1]
    return _get(c, f"{OPENALEX}/topics/{short}", {}, raw_dir, f"topic-{short}")


def top_works(
    c: httpx.Client,
    topic_id: str,
    raw_dir: Path,
    *,
    n: int = 5,
    in_window: bool = False,
) -> list[dict]:
    """De n mest siterte arbeidene under topicet. Kontrollgrunnlag, ikke utvalg.

    ``in_window`` begrenser til PREREG-vinduet. Det er nødvendig i humaniora:
    over all tid domineres siteringstoppen av klassiske monografier som sier
    lite om hva topicet inneholder i perioden som faktisk måles.
    """
    short = topic_id.rsplit("/", 1)[-1]
    filter_str = f"topics.id:{topic_id}"
    if in_window:
        filter_str += "," + year_filter()
    payload = _get(
        c,
        f"{OPENALEX}/works",
        {
            "filter": filter_str,
            "sort": "cited_by_count:desc",
            "per-page": str(n),
            "select": "id,doi,title,publication_year,cited_by_count,primary_topic",
        },
        raw_dir,
        f"topworks-{short}" + ("-vindu" if in_window else ""),
    )
    return payload["results"]


# --------------------------------------------------------------------------- #
# STEG 2: tellinger og utsnitt
# --------------------------------------------------------------------------- #

def topic_filter(topic_ids: Sequence[str]) -> str:
    return "topics.id:" + "|".join(topic_ids)


def count(c: httpx.Client, filter_str: str, raw_dir: Path, *, stem: str) -> int:
    payload = _get(c, f"{OPENALEX}/works", {"filter": filter_str, "per-page": "1", "select": "id"}, raw_dir, stem)
    return int(payload["meta"]["count"])


def sample_works(
    c: httpx.Client,
    filter_str: str,
    raw_dir: Path,
    *,
    stem: str,
    n: int = 200,
    seed: int = COVERAGE_SEED_INT,
) -> list[dict]:
    payload = _get(
        c,
        f"{OPENALEX}/works",
        {"filter": filter_str, "sample": str(n), "seed": str(seed),
         "per-page": str(min(n, 200)), "select": WORK_SELECT},
        raw_dir,
        stem,
    )
    return payload["results"]


def pdf_url_of(work: dict) -> str | None:
    """PDF-lenke fra beste OA-plassering, ellers primærplassering. Lenken
    telles; den følges ikke."""
    for key in ("best_oa_location", "primary_location"):
        loc = work.get(key) or {}
        if loc.get("pdf_url"):
            return loc["pdf_url"]
    return None


def wilson(hits: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """(punkt, nedre, øvre). Wilson, fordi andelene kan ligge nær 0 og 1."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = hits / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, centre - half), min(1.0, centre + half))


# --------------------------------------------------------------------------- #
# R4: Europe PMC
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class EpmcHit:
    doi: str
    pmcid: str | None
    in_epmc: bool
    is_oa: bool

    @property
    def jats_available(self) -> bool:
        """JATS-XML kan hentes når verket ligger i Europe PMC som OA med PMCID."""
        return bool(self.pmcid) and self.in_epmc and self.is_oa


def epmc_lookup(c: httpx.Client, dois: Sequence[str], raw_dir: Path, *, stem: str, chunk: int = 5) -> dict[str, EpmcHit]:
    """Slå opp DOI-er mot Europe PMC. Metadata only — ingen fulltekst hentes.

    Chunk er 5, ikke 10: målt oppfører endepunktet seg ustabilt når URL-en
    vokser (404 uten kropp ved ~470 tegn, stabil ved ~300). POST svarer 405.
    Retry i _get tar de sporadiske 404-ene som gjenstår."""
    found: dict[str, EpmcHit] = {}
    for i in range(0, len(dois), chunk):
        batch = dois[i : i + chunk]
        query = " OR ".join(f'DOI:"{d}"' for d in batch)
        payload = _get(
            c,
            EPMC,
            {"query": query, "resultType": "core", "format": "json", "pageSize": str(chunk * 3)},
            raw_dir,
            f"{stem}-{i // chunk:02d}",
        )
        for res in payload.get("resultList", {}).get("result", []):
            doi = (res.get("doi") or "").lower()
            if not doi:
                continue
            found[doi] = EpmcHit(
                doi=doi,
                pmcid=res.get("pmcid"),
                in_epmc=res.get("inEPMC") == "Y",
                is_oa=res.get("isOpenAccess") == "Y",
            )
        time.sleep(0.2)  # høflig mot Europe PMC
    return {d.lower(): found.get(d.lower(), EpmcHit(d.lower(), None, False, False)) for d in dois}


def verify_jats_endpoint(c: httpx.Client, pmcid: str) -> int:
    """Sjekk at JATS-endepunktet svarer. Statuskode returneres; kroppen leses ikke.

    Accept må være XML: klientens standard ``application/json`` gir 406 fra
    dette endepunktet, som ville sett ut som «ingen JATS» og vært et falskt
    negativt."""
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    hdr = {"Accept": "application/xml"}
    r = c.head(url, headers=hdr)
    if r.status_code in (405, 501):  # HEAD ikke støttet: be om én byte, kast den
        r = c.get(url, headers={**hdr, "Range": "bytes=0-0"})
    return r.status_code


def year_filter(year_from: int = YEAR_FROM, year_to: int = YEAR_TO) -> str:
    return f"publication_year:{year_from}-{year_to}"


# --------------------------------------------------------------------------- #
# Verifiserte emne-ID-er (ADDENDUM-01 STEG 1)
# --------------------------------------------------------------------------- #

#: Godkjenningsregelen: alle fem kontrollarbeidene — de mest siterte *innenfor
#: PREREG-vinduet* — må ligge i feltet, eller være metodeverktøy publisert for
#: og brukt av feltet. Over all tid domineres humaniora-topics av klassiske
#: monografier og kriteriet blir meningsløst; derfor vinduet.
TOPIC_IDS: dict[str, tuple[str, ...]] = {
    "tekstvitenskap": ("T10595", "T10165", "T14210"),
    "klinisk_epidemiologi": ("T11095", "T10556"),
    "arkeologi": ("T10421", "T10087"),
    "energimodellering": ("T10424", "T11185", "T11941"),
}

#: Vurdert og forkastet, med antall kontrollarbeider innenfor feltet.
TOPIC_REJECTED: dict[str, tuple[tuple[str, str, str], ...]] = {
    "tekstvitenskap": (
        ("T14170", "Classical Studies and Philology", "3/5 — Geertz og Seneca-biografi utenfor"),
        ("T12377", "Digital Humanities and Scholarship", "1/5 — vitenskapsteori dominerer"),
        ("T11657", "Digital and Traditional Archives Management", "0/5 — arkivvitenskap, ikke kildeutgivelse"),
        ("T10362", "Biblical Studies and Interpretation", "0/5 — religionsvitenskap"),
    ),
    "klinisk_epidemiologi": (
        ("T10350", "Electronic Health Records Systems", "4/5 — mHealth-appvurdering utenfor"),
        ("T10845", "Advanced Causal Inference Techniques", "3/5 — økonometri utenfor"),
        ("T10261", "Genetic Associations and Epidemiology", "annet felt: genomikk"),
        ("T12790", "Nursing Diagnosis and Documentation", "0/5 — forskningsmetode i sykepleie"),
        ("T10391", "Healthcare Policy and Management", "0/5 — helseøkonomi"),
    ),
    "arkeologi": (
        ("T13621", "Ancient and Medieval Archaeology Studies", "3/5 — jordbunnslære og kvartærgeologi inne"),
        ("T13372", "Archaeology and Historical Studies", "antikkhistorie, ikke arkeologisk praksis"),
    ),
    "energimodellering": (),
}

#: Den positive kontrollen i PREREG-v1 §7. Rammen MÅ fange den.
POSITIVE_CONTROL_DOI = "10.1016/j.apenergy.2018.04.048"
POSITIVE_CONTROL_FIELD = "energimodellering"


@dataclass
class FieldCoverage:
    field_key: str
    topic_ids: tuple[str, ...]
    r0: int
    r1: int
    r2: int
    n_sample_r0: int
    pdf_in_r0: int
    n_sample_r1: int
    pdf_in_r1: int
    n_epmc_checked: int
    epmc_jats: int

    @property
    def p_pdf_r0(self) -> tuple[float, float, float]:
        return wilson(self.pdf_in_r0, self.n_sample_r0)

    @property
    def p_pdf_r1(self) -> tuple[float, float, float]:
        return wilson(self.pdf_in_r1, self.n_sample_r1)

    @property
    def r3_estimate(self) -> int:
        return round(self.p_pdf_r0[0] * self.r0)

    @property
    def r3_interval(self) -> tuple[int, int]:
        _, lo, hi = self.p_pdf_r0
        return (round(lo * self.r0), round(hi * self.r0))

    @property
    def p_jats(self) -> tuple[float, float, float]:
        return wilson(self.epmc_jats, self.n_epmc_checked)

    @property
    def r4_estimate(self) -> int:
        return round(self.p_jats[0] * self.r3_estimate)


def measure_field(
    c: httpx.Client,
    field_key: str,
    raw_dir: Path,
    *,
    sample_n: int = 200,
    epmc_n: int = 50,
) -> FieldCoverage:
    """Mål R0-R4 for ett felt. Ingen fulltekst hentes: lenker telles."""
    ids = TOPIC_IDS[field_key]
    base = f"{topic_filter(ids)},{year_filter()}"
    r0 = count(c, base, raw_dir, stem=f"count-R0-{field_key}")
    r1 = count(c, f"{base},has_fulltext:true", raw_dir, stem=f"count-R1-{field_key}")
    r2 = count(c, f"{base},has_fulltext:true,is_oa:true", raw_dir, stem=f"count-R2-{field_key}")

    s0 = sample_works(c, base, raw_dir, stem=f"sample-R0-{field_key}", n=sample_n)
    s1 = sample_works(c, f"{base},has_fulltext:true", raw_dir, stem=f"sample-R1-{field_key}", n=sample_n)
    pdf0 = [w for w in s0 if pdf_url_of(w)]
    pdf1 = [w for w in s1 if pdf_url_of(w)]

    dois = [
        (w.get("doi") or "").replace("https://doi.org/", "").lower()
        for w in pdf0
        if w.get("doi")
    ][:epmc_n]
    hits = epmc_lookup(c, dois, raw_dir, stem=f"epmc-{field_key}") if dois else {}
    jats = sum(1 for h in hits.values() if h.jats_available)

    return FieldCoverage(
        field_key=field_key,
        topic_ids=ids,
        r0=r0,
        r1=r1,
        r2=r2,
        n_sample_r0=len(s0),
        pdf_in_r0=len(pdf0),
        n_sample_r1=len(s1),
        pdf_in_r1=len(pdf1),
        n_epmc_checked=len(dois),
        epmc_jats=jats,
    )


# --------------------------------------------------------------------------- #
# Rammediagnostikk (ADDENDUM-02 §6-§7)
# --------------------------------------------------------------------------- #

def frame_filter(field_key: str, *, year: int | None = None) -> str:
    """Den operasjonelle rammen fra ADDENDUM-01 §3.1, eventuelt for ett år."""
    ids = TOPIC_IDS[field_key]
    aar = f"publication_year:{year}" if year else year_filter()
    return f"{topic_filter(ids)},{aar},open_access.is_oa:true"


def year_distribution(c: httpx.Client, field_key: str, raw_dir: Path) -> dict[int, int]:
    """Antall works per år i vinduet, på den nye rammen."""
    return {
        y: count(c, frame_filter(field_key, year=y), raw_dir, stem=f"frame-yr-{field_key}-{y}")
        for y in range(YEAR_FROM, YEAR_TO + 1)
    }


def union_filter(field_keys: Sequence[str]) -> str:
    """Rammen for unionen av flere felt: ID-ene slås sammen, år og OA er felles."""
    ids: list[str] = []
    for fk in field_keys:
        for t in TOPIC_IDS[fk]:
            if t not in ids:
                ids.append(t)
    return f"{topic_filter(ids)},{year_filter()},open_access.is_oa:true"


def intersections_from_unions(unions: Mapping[frozenset[str], int]) -> dict[frozenset[str], int]:
    """Snittstørrelser av unionsstørrelser, ved dual inklusjon–eksklusjon.

    |∩_{i∈S} F_i| = Σ_{∅≠T⊆S} (-1)^(|T|+1) · |∪_{i∈T} F_i|

    OpenAlex kan telle unioner (`topics.id:A|B`) men ikke snitt mellom to
    topic-lister, så snittene må regnes ut, ikke spørres om.
    """
    out: dict[frozenset[str], int] = {}
    for S in unions:
        total = 0
        for T in unions:
            if T <= S and T:
                total += (-1) ** (len(T) + 1) * unions[T]
        out[S] = total
    return out


def exactly_k_from_intersections(
    intersections: Mapping[frozenset[str], int], fields: Sequence[str]
) -> dict[int, int]:
    """Antall works som ligger i nøyaktig k av rammene, for k = 1..n."""
    from itertools import combinations

    n = len(fields)
    ut: dict[int, int] = {}
    for k in range(1, n + 1):
        s = 0
        for j in range(k, n + 1):
            binom = math.comb(j, k)
            for combo in combinations(fields, j):
                s += (-1) ** (j - k) * binom * intersections[frozenset(combo)]
        ut[k] = s
    return ut
