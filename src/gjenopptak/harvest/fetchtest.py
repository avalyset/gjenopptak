"""Hentingsprøven: rammekriteriet i ADDENDUM-04 §1.

Et verk er i rammen når porten gir en fil med uttrekkbar tekst:

* **P1** Europe PMC har pmcid, ``inEPMC=Y`` og ``isOpenAccess=Y``, og JATS fra
  ``/{pmcid}/fullTextXML`` gir minst ``MIN_SENTENCES`` setninger.
* **P3** ``best_oa_location.pdf_url`` svarer 200 med en PDF som gir minst
  ``MIN_CHARS`` tegn.

P2 (OpenAlex' TEI-arkiv) inngår ikke: ruten krever nøkkel, og den offentlige
ruten er valgt for at sveipet skal kunne kjøres uten nøkkel (ADDENDUM-02 §8.1).

Prøven bruker **ikke OpenAlex** og kan derfor kjøres samme døgn som en frysing.
Ingen blokkering omgås: egen ærlig User-Agent, ingen spoofing, ingen alternative
kilder. En 403 er et måleresultat og betyr «utenfor rammen».
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import urlparse

import httpx

from ..parse import sentences_from_jats
from .openalex import write_raw

EPMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
EPMC_XML = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"

UA = "gjenopptak/0.1.0 (research; contact via repo)"
MIN_SENTENCES = 20
MIN_CHARS = 2_000
EPMC_CHUNK = 5          # målt grense: lengre URL-er gir 404 (ADDENDUM-01 §5.1)
RETRY_STATUS = (404, 429, 500, 502, 503, 504)


@dataclass
class FetchVerdict:
    """Utfallet for ett verk. ``in_frame`` er rammemedlemskapet."""

    work_id: str
    doi: str | None
    in_frame: bool = False
    gate: str | None = None          # P1-JATS | P3-PDF | None
    status: int | None = None
    host: str | None = None
    chars: int = 0
    reason: str | None = None
    #: Den lagrede filen porten ble avgjort på (JATS for P1, PDF for P3).
    bytes: int | None = None
    sha256: str | None = None
    file: str | None = None

    def as_row(self) -> dict:
        return asdict(self)


class OpenAlexForbidden(RuntimeError):
    """Hentingsprøven skal aldri kalle OpenAlex (ADDENDUM-04 §1: egen rute, egen kvote)."""


#: Serialiserer skriving til MANIFEST.md når prøven kjøres med flere tråder.
_RAW_LOCK = threading.Lock()


def _lagre(blob: bytes, url: str, raw_dir: Path, *, stem: str):
    with _RAW_LOCK:
        return write_raw(blob, url, raw_dir, stem=stem)


def _host(url: str) -> str:
    return urlparse(url).netloc.lower().replace("www.", "")


class HostGate:
    """Høflighet per vert: høyst ``max_concurrent`` samtidige kall og minst
    ``interval`` sekunder mellom hver start mot samme vert.

    ``per_host`` overstyrer for en vert og dens undervert (``"arxiv.org"``
    gjelder også ``export.arxiv.org``). Ingen blokkering omgås; grensen gjør
    bare at prøven ikke belaster én utgiver mer enn en leser ville gjort.
    """

    def __init__(self, *, interval: float = 1.0, max_concurrent: int = 2,
                 per_host: dict[str, tuple[float, int]] | None = None,
                 clock: Callable[[], float] = time.monotonic,
                 sleep: Callable[[float], None] = time.sleep) -> None:
        self.interval, self.max_concurrent = interval, max_concurrent
        self.per_host = dict(per_host or {})
        self._clock, self._sleep = clock, sleep
        self._lock = threading.Lock()
        self._sem: dict[str, threading.BoundedSemaphore] = {}
        self._next: dict[str, float] = {}

    def config(self, host: str) -> tuple[float, int]:
        for navn, cfg in self.per_host.items():
            if host == navn or host.endswith("." + navn):
                return cfg
        return self.interval, self.max_concurrent

    @contextmanager
    def slot(self, host: str):
        interval, maks = self.config(host)
        with self._lock:
            sem = self._sem.setdefault(host, threading.BoundedSemaphore(maks))
        sem.acquire()
        try:
            with self._lock:
                naa = self._clock()
                start = max(naa, self._next.get(host, 0.0))
                self._next[host] = start + interval
            if start > naa:
                self._sleep(start - naa)
            yield
        finally:
            sem.release()


def _get(c: httpx.Client, url: str, headers: dict, *, retries: int = 3,
         gate: HostGate | None = None, **kw) -> httpx.Response:
    host = _host(url)
    if host == "openalex.org" or host.endswith(".openalex.org"):
        raise OpenAlexForbidden(url)
    last: httpx.Response | None = None
    for attempt in range(retries):
        if gate is None:
            r = c.get(url, headers=headers, **kw)
        else:
            with gate.slot(host):
                r = c.get(url, headers=headers, **kw)
        if r.status_code not in RETRY_STATUS:
            return r
        last = r
        time.sleep(1.5 ** attempt)
    return last if last is not None else r


def epmc_pmcid(c: httpx.Client, doi: str, raw_dir: Path, *, stem: str,
               gate: HostGate | None = None) -> str | None:
    """PMCID for en DOI, men bare når JATS faktisk kan hentes."""
    r = _get(c, EPMC_SEARCH, {"User-Agent": UA, "Accept": "application/json"}, gate=gate,
             params={"query": f'DOI:"{doi}"', "resultType": "core",
                     "format": "json", "pageSize": "5"})
    if r.status_code != 200:
        return None
    _lagre(r.content, str(r.url), raw_dir, stem=stem)
    for x in json.loads(r.content).get("resultList", {}).get("result", []):
        if (x.get("doi") or "").lower() == doi and x.get("pmcid") \
           and x.get("inEPMC") == "Y" and x.get("isOpenAccess") == "Y":
            return x["pmcid"]
    return None


def epmc_pmcids(c: httpx.Client, dois: list[str], raw_dir: Path, *, stem: str,
                gate: HostGate | None = None) -> dict[str, str | None]:
    """P1-oppslaget for opptil ``EPMC_CHUNK`` DOI-er i ett kall.

    Samme krav som ``epmc_pmcid``: DOI-en må stemme, og posten må ha pmcid,
    ``inEPMC=Y`` og ``isOpenAccess=Y``. Første kvalifiserende post per DOI i
    resultatrekkefølge vinner. Svarer tjenesten ikke 200, eller har søket flere
    treff enn én side, faller oppslaget tilbake til ett kall per DOI — et
    ufullstendig svar skal ikke se ut som «ikke i Europe PMC».
    """
    if len(dois) > EPMC_CHUNK:
        raise ValueError(f"høyst {EPMC_CHUNK} DOI-er per kall, fikk {len(dois)}")

    def enkeltvis() -> dict[str, str | None]:
        return {d: epmc_pmcid(c, d, raw_dir, stem=f"{stem}-{i}", gate=gate)
                for i, d in enumerate(dois)}

    q = " OR ".join(f'DOI:"{d}"' for d in dois)
    r = _get(c, EPMC_SEARCH, {"User-Agent": UA, "Accept": "application/json"}, gate=gate,
             params={"query": q, "resultType": "core", "format": "json", "pageSize": "100"})
    if r.status_code != 200:
        return enkeltvis()
    payload = json.loads(r.content)
    treff = payload.get("resultList", {}).get("result", [])
    if int(payload.get("hitCount") or 0) > len(treff):
        return enkeltvis()
    _lagre(r.content, str(r.url), raw_dir, stem=stem)
    ut: dict[str, str | None] = {d: None for d in dois}
    for x in treff:
        d = (x.get("doi") or "").lower()
        if d in ut and ut[d] is None and x.get("pmcid") \
           and x.get("inEPMC") == "Y" and x.get("isOpenAccess") == "Y":
            ut[d] = x["pmcid"]
    return ut


def pdf_text_chars(pdf_bytes: bytes, tmp_dir: Path, name: str) -> int:
    """Tegn i uttrukket tekst. Bruker pdftotext; 0 om ingenting kan hentes ut."""
    tmp_dir.mkdir(parents=True, exist_ok=True)
    p = tmp_dir / f"{name}.pdf"
    p.write_bytes(pdf_bytes)
    try:
        out = subprocess.run(["pdftotext", "-q", str(p), "-"],
                             capture_output=True, text=True, timeout=120)
        return len(out.stdout.strip())
    except (subprocess.SubprocessError, OSError):
        return 0
    finally:
        p.unlink(missing_ok=True)


_UNSET = object()


def test_work(c: httpx.Client, row: dict, raw_dir: Path, tmp_dir: Path, *,
              pmcid: object = _UNSET, gate: HostGate | None = None) -> FetchVerdict:
    """Kjør porten for én rad fra rammelisten.

    ``pmcid`` er et forhåndsgjort P1-oppslag (``epmc_pmcids``); ``None`` betyr at
    oppslaget er gjort og ga ingen JATS-rute. Uten argumentet slås DOI-en opp her.
    """
    v = FetchVerdict(work_id=row["work_id"], doi=row.get("doi"))

    # --- P1 JATS ---
    if v.doi:
        if pmcid is _UNSET:
            pmcid = epmc_pmcid(c, v.doi, raw_dir, stem=f"ft-epmc-{v.work_id}", gate=gate)
        if pmcid:
            url = EPMC_XML.format(pmcid=pmcid)
            r = _get(c, url, {"User-Agent": UA, "Accept": "application/xml"}, gate=gate)
            v.status, v.host = r.status_code, "europepmc.org"
            if r.status_code == 200 and r.content.strip():
                rec = _lagre(r.content, url, raw_dir, stem=f"ft-jats-{pmcid}")
                v.bytes, v.sha256, v.file = rec.bytes_len, rec.sha256, rec.path.name
                try:
                    rows = sentences_from_jats(r.content, doc_id=pmcid)
                    if len(rows) >= MIN_SENTENCES:
                        v.in_frame, v.gate = True, "P1-JATS"
                        v.chars = sum(len(x["text"]) for x in rows)
                        return v
                    v.reason = f"jats-for-kort-{len(rows)}-setn"
                except Exception as e:                      # noqa: BLE001
                    v.reason = f"jats-parse-{type(e).__name__}"

    # --- P3 PDF ---
    pdf = (row.get("best_oa_location") or {}).get("pdf_url")
    if not pdf:
        v.gate = v.gate or "ingen-rute"
        v.reason = v.reason or "ingen-pdf-lenke"
        return v
    v.host = urlparse(pdf).netloc.replace("www.", "")
    try:
        r = _get(c, pdf, {"User-Agent": UA, "Accept": "application/pdf,*/*"}, gate=gate)
    except OpenAlexForbidden:
        v.gate, v.reason = "P3-PDF", "openalex-lenke-ikke-hentet"
        return v
    except Exception as e:                                   # noqa: BLE001
        v.gate, v.reason = "P3-PDF", type(e).__name__
        return v
    v.status, v.gate = r.status_code, "P3-PDF"
    if r.status_code != 200 or r.content[:4] != b"%PDF":
        v.reason = f"http-{r.status_code}-{r.headers.get('content-type','')[:30]}"
        return v
    rec = _lagre(r.content, pdf, raw_dir, stem=f"ft-pdf-{v.work_id}")
    v.bytes, v.sha256, v.file = rec.bytes_len, rec.sha256, rec.path.name
    v.chars = pdf_text_chars(r.content, tmp_dir, v.work_id)
    if v.chars >= MIN_CHARS:
        v.in_frame = True
    else:
        v.reason = f"pdf-uten-tekst-{v.chars}tegn"
    return v


def run(rows: Iterable[dict], raw_dir: Path, tmp_dir: Path, *, pause: float = 0.3,
        out_path: Path | None = None) -> list[FetchVerdict]:
    """Kjør prøven på hele rammelisten. Skriver fortløpende når out_path er gitt."""
    verdicts: list[FetchVerdict] = []
    fh = out_path.open("w", encoding="utf-8") if out_path else None
    try:
        with httpx.Client(timeout=90, follow_redirects=True) as c:
            for row in rows:
                v = test_work(c, row, raw_dir, tmp_dir)
                verdicts.append(v)
                if fh:
                    fh.write(json.dumps(v.as_row(), ensure_ascii=False, sort_keys=True) + "\n")
                    fh.flush()
                time.sleep(pause)
    finally:
        if fh:
            fh.close()
    return verdicts


def summarise(verdicts: Iterable[FetchVerdict]) -> dict:
    """Rammestørrelse og frafall etter årsak og vert."""
    from collections import Counter

    vs = list(verdicts)
    inne = [v for v in vs if v.in_frame]
    ute = [v for v in vs if not v.in_frame]
    return {
        "n_tested": len(vs),
        "n_in_frame": len(inne),
        "share_in_frame": len(inne) / len(vs) if vs else 0.0,
        "by_gate": dict(Counter(v.gate for v in inne)),
        "excluded_by_host": dict(Counter(v.host or "(ingen lenke)" for v in ute).most_common()),
        "excluded_by_status": dict(Counter(str(v.status) for v in ute).most_common()),
    }


# --------------------------------------------------------------------------- #
# Manifestskillet: rammeprøve er ikke lesning
# --------------------------------------------------------------------------- #

#: Merkelappen som skiller filer hentet av rammeprøven fra filer som er lest.
#: En fil hentet av prøven er et rammekriterium, ikke en observasjon: ingen
#: setning er vurdert, ingen hindringsklasse tildelt. Filene lagres, men verket
#: havner IKKE i data/leste-kontrollkandidater.json og er fortsatt trekkbart.
#: Kollapser dette skillet, blir hele rammen «lest» og utvalget umulig.
FRAME_PROBE_TAG = "RAMMEPRØVE-IKKE-LEST"
READ_TAG = "LEST-UTELATT-FRA-TREKKING"

MANIFEST_NOTE = f"""
## Om rammeprøvens filer og de leste filene

**{FRAME_PROBE_TAG}** — hentet av hentingsprøven i ADDENDUM-04 §1. Prøven avgjør
rammemedlemskap: bestått port = i rammen. Filene er lagret, men **ikke lest**.
Ingen setning er vurdert, ingen klasse tildelt, ingen passasje bedømt. Verkene
er fortsatt trekkbare og står ikke i `data/leste-kontrollkandidater.json`.

**{READ_TAG}** — åpnet og gjennomsøkt for kandidatsetninger under arbeidet med
kontroller og ankere (ADDENDUM-02 §1, ADDENDUM-03 §2.3). Disse verkene er sett av
eier og er derfor **ikke** blinde observasjoner. De står i
`data/leste-kontrollkandidater.json` og utelates fra trekkingen.

Skillet er ikke kosmetisk. Rammeprøven må kjøres på hele rammelisten; hadde den
gjort verkene «leste», ville rammen og utvalget vært gjensidig utelukkende.
"""


def ensure_manifest_note(raw_dir: Path) -> bool:
    """Skriv skillet inn i MANIFEST.md én gang. Returnerer True om det ble lagt til."""
    manifest = raw_dir / "MANIFEST.md"
    if manifest.exists() and FRAME_PROBE_TAG in manifest.read_text(encoding="utf-8"):
        return False
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write(MANIFEST_NOTE)
    return True


def write_frame_file(verdicts: Iterable[FetchVerdict], out_path: Path) -> tuple[int, str]:
    """Skriv HENTBAR-rammefilen: bare verk som besto porten, sortert på work-ID.

    Returnerer (radantall, sha256).
    """
    import hashlib

    rader = sorted((v for v in verdicts if v.in_frame), key=lambda v: v.work_id)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for v in rader:
            fh.write(json.dumps(v.as_row(), ensure_ascii=False, sort_keys=True) + "\n")
    return len(rader), hashlib.sha256(out_path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------- #
# Hele rammelisten: parallelt, gjenopptakbart, med diskvakt (ADDENDUM-04 §1.3)
# --------------------------------------------------------------------------- #

#: Stopp før Vault-volumet har mindre enn dette ledig. Rammeprøven lagrer alle
#: hentede filer der, og et fullt arkivvolum ødelegger mer enn en avbrutt prøve.
DISK_FLOOR_BYTES = 6 * 2**30

#: Stopp før systemdisken har mindre enn dette ledig. Den bærer bare det som kan
#: regenereres: scratch for pdftotext, som slettes straks. Samme terskel som
#: diskvakten hadde da den pekte på systemdisken — ingen terskel er senket.
SCRATCH_FLOOR_BYTES = 6 * 2**30


def probe_dir(field_key: str, *, root: Path | None = None) -> Path:
    """Katalogen på Vault der rammeprøven skriver hentet fulltekst og verdikter.

    Hentet fulltekst skrives aldri til systemdisken. Den 2026-09-13 fylte 23 467 verk
    17 GB på systemdisken, og prøven stoppet på diskvakten. ``require_vault`` kaster
    ``VaultUnavailable`` når Vault ikke er montert: da starter prøven ikke, og det
    finnes ingen fallback.
    """
    from .. import vault
    return vault.require_vault(root or vault.VAULT_ROOT) / f"fulltext-rammeprove-{field_key}"


def _naermeste_eksisterende(p: Path) -> Path:
    p = Path(p)
    while not p.exists() and p != p.parent:
        p = p.parent
    return p


def default_gate() -> HostGate:
    """Én start per sekund og to samtidige per vert; arXiv ber om én per tre sekunder."""
    return HostGate(interval=1.0, max_concurrent=2,
                    per_host={"arxiv.org": (3.0, 1), "ebi.ac.uk": (0.1, 4)})


@dataclass
class RunState:
    n_total: int
    n_done_before: int
    n_tested_now: int = 0
    n_epmc_calls: int = 0
    stopped: str | None = None
    notes: list[str] = field(default_factory=list)


def read_verdicts(path: Path) -> dict[str, FetchVerdict]:
    """Verdiktene som alt er skrevet, siste per work-ID. En avkuttet siste linje hoppes over."""
    ut: dict[str, FetchVerdict] = {}
    if not path.exists():
        return ut
    for line in path.open(encoding="utf-8"):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        ut[d["work_id"]] = FetchVerdict(**d)
    return ut


def run_frame(rows: list[dict], raw_dir: Path, tmp_dir: Path, out_path: Path, *,
              workers: int = 16, gate: HostGate | None = None,
              disk_floor: int = DISK_FLOOR_BYTES,
              disk_free: Callable[[], int] | None = None,
              scratch_floor: int = SCRATCH_FLOOR_BYTES,
              scratch_free: Callable[[], int] | None = None,
              client_factory: Callable[[], httpx.Client] | None = None,
              progress: Callable[[str], None] | None = None) -> RunState:
    """Kjør porten på alle rader som ikke alt har et verdikt i ``out_path``.

    ``raw_dir`` er katalogen på Vault (``probe_dir``); ``tmp_dir`` er scratch på
    systemdisken. P1-oppslaget i Europe PMC gjøres først, fem DOI-er per kall, og
    bufres ved siden av verdiktfilen. Deretter testes hvert verk i en tråd.

    To diskvakter sjekkes før hvert verk: ledig plass på volumet ``raw_dir`` ligger
    på (``stopped="disk-vault"``) og på volumet scratch ligger på
    (``stopped="disk-scratch"``). Faller en av dem under gulvet, startes ingen nye.
    Kjøringen kan startes på nytt og fortsetter der den slapp.
    """
    ferdige = read_verdicts(out_path)
    todo = [r for r in rows if r["work_id"] not in ferdige]
    state = RunState(n_total=len(rows), n_done_before=len(ferdige))
    if not todo:
        return state
    gate = gate or default_gate()
    disk_free = disk_free or (lambda: shutil.disk_usage(_naermeste_eksisterende(raw_dir)).free)
    scratch_free = scratch_free or (lambda: shutil.disk_usage(_naermeste_eksisterende(tmp_dir)).free)
    lag_klient = client_factory or (lambda: httpx.Client(timeout=90, follow_redirects=True))
    lokal = threading.local()
    klienter: list[httpx.Client] = []
    klientlaas = threading.Lock()
    si = progress or (lambda _m: None)

    def klient() -> httpx.Client:
        if not hasattr(lokal, "c"):
            lokal.c = lag_klient()
            with klientlaas:
                klienter.append(lokal.c)
        return lokal.c

    # --- P1: forhåndsoppslag i Europe PMC ---
    buffer = out_path.with_name(out_path.stem + "-epmc.json")
    pmcids: dict[str, str | None] = json.loads(buffer.read_text()) if buffer.exists() else {}
    mangler = sorted({r["doi"] for r in todo if r.get("doi")} - set(pmcids))
    biter = [mangler[i:i + EPMC_CHUNK] for i in range(0, len(mangler), EPMC_CHUNK)]

    def slaa_opp(bit: list[str]) -> dict[str, str | None]:
        navn = "ft-epmc-" + hashlib.sha256("|".join(bit).encode()).hexdigest()[:10]
        return epmc_pmcids(klient(), bit, raw_dir, stem=navn, gate=gate)

    try:
        with ThreadPoolExecutor(max_workers=min(workers, 4)) as ex:
            for k, svar in enumerate(ex.map(slaa_opp, biter), 1):
                pmcids.update(svar)
                state.n_epmc_calls += 1
                if k % 250 == 0:
                    buffer.write_text(json.dumps(pmcids, sort_keys=True))
                    si(f"P1-oppslag {k}/{len(biter)}")
        buffer.write_text(json.dumps(pmcids, sort_keys=True))

        # --- porten per verk ---
        stopp = threading.Event()
        grunn: dict[str, str] = {}
        skrivelaas = threading.Lock()
        with out_path.open("a", encoding="utf-8") as fh:
            def ett(row: dict) -> None:
                if stopp.is_set():
                    return
                if disk_free() < disk_floor:
                    grunn.setdefault("v", "disk-vault")
                    stopp.set()
                    return
                if scratch_free() < scratch_floor:
                    grunn.setdefault("v", "disk-scratch")
                    stopp.set()
                    return
                doi = row.get("doi")
                v = test_work(klient(), row, raw_dir, tmp_dir,
                              pmcid=pmcids.get(doi) if doi else None, gate=gate)
                with skrivelaas:
                    fh.write(json.dumps(v.as_row(), ensure_ascii=False, sort_keys=True) + "\n")
                    fh.flush()
                    state.n_tested_now += 1
                    if state.n_tested_now % 500 == 0:
                        si(f"testet {state.n_tested_now}/{len(todo)}, "
                           f"ledig på Vault {disk_free() / 2**30:.1f} GiB, "
                           f"scratch {scratch_free() / 2**30:.1f} GiB")

            with ThreadPoolExecutor(max_workers=workers) as ex:
                list(ex.map(ett, todo))
        if stopp.is_set():
            state.stopped = grunn.get("v", "disk")
            gulv = disk_floor if state.stopped == "disk-vault" else scratch_floor
            state.notes.append(f"ledig plass under {gulv / 2**30:.1f} GiB ({state.stopped})")
    finally:
        for c in klienter:
            c.close()
    return state


from ..vault import krev  # ADR-0009


def main(argv: list[str] | None = None) -> int:
    """Hentingsprøven på en frossen rammeliste.

    Hentet fulltekst, hentemanifest og verdikter skrives til Vault
    (``probe_dir``). Systemdisken bærer bare scratch.

    Exit 0: komplett, HENTBAR skrevet og sikret. 1: stoppet (disk) eller
    ufullstendig — kjør på nytt for å fortsette. 2: Vault er ikke montert, eller
    rammelisten mangler — ingenting er hentet. 3: HENTBAR ble skrevet, men ikke
    sikret til Vault.
    """
    import argparse
    import sys
    from collections import Counter

    from ..vault import VaultUnavailable, secure_frame_file
    from .coverage import TOPIC_IDS

    ap = argparse.ArgumentParser(description="Hentingsprøven på en frossen rammeliste. Ingen OpenAlex-kall.")
    ap.add_argument("--field", choices=list(TOPIC_IDS), required=True)
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--vault-root", type=Path, default=None,
                    help="Monteringspunktet for Vault (standard /Volumes/Vault). Ingen fallback.")
    args = ap.parse_args(argv)
    args.data_dir = krev(getattr(args, 'data_dir', None))  # ADR-0009: ingen fallback

    try:
        raw_dir = probe_dir(args.field, root=args.vault_root)
    except VaultUnavailable as e:
        print(f"IKKE STARTET: {e} Rammeprøven skriver hentet fulltekst bare til Vault; "
              "det finnes ingen fallback til systemdisken.", file=sys.stderr)
        return 2

    frames = args.data_dir / "frames"
    ramme = frames / f"frame-{args.field}-RAW.jsonl"
    if not ramme.exists():
        print(f"STOPPET: {ramme} finnes ikke (ufullstendige lister prøves ikke).", file=sys.stderr)
        return 2
    rows = [json.loads(line) for line in ramme.open(encoding="utf-8")]
    raw_dir.mkdir(parents=True, exist_ok=True)
    ensure_manifest_note(raw_dir)
    ut = raw_dir / f"verdikter-{args.field}.jsonl"

    state = run_frame(rows, raw_dir, args.data_dir / "tmp-hentingsprove", ut,
                      workers=args.workers, progress=lambda m: print(m, flush=True))
    verdikter = read_verdicts(ut)
    print(f"felt        : {args.field}")
    print(f"rammeliste  : {ramme}  ({len(rows)} rader)")
    print(f"skrevet til : {raw_dir}")
    print(f"testet nå   : {state.n_tested_now}  (fra før: {state.n_done_before}; EPMC-kall {state.n_epmc_calls})")
    if state.stopped or len(verdikter) < len(rows):
        print(f"STOPPET     : {state.stopped or 'ufullstendig'} — {len(verdikter)}/{len(rows)} har verdikt. "
              "Kjør på nytt for å fortsette.", file=sys.stderr)
        return 1

    hentbar = frames / f"frame-{args.field}-HENTBAR.jsonl"
    n, digest = write_frame_file([verdikter[r["work_id"]] for r in rows], hentbar)
    aar = {r["work_id"]: r.get("publication_year") for r in rows}
    fordeling = Counter(aar[v.work_id] for v in verdikter.values() if v.in_frame)
    print(f"hentbar     : {n} av {len(rows)} ({n / len(rows):.1%})")
    print(f"per ledd    : {dict(Counter(v.gate for v in verdikter.values() if v.in_frame))}")
    print(f"år          : {dict(sorted(fordeling.items()))}")
    print(f"fil         : {hentbar}")
    print(f"sha256      : {digest}")
    try:
        vr = secure_frame_file(hentbar, **({"root": args.vault_root} if args.vault_root else {}))
        print(f"vault       : {vr.dst}  (sha256 verifisert)")
    except (VaultUnavailable, OSError) as e:
        print(f"IKKE SIKRET : {e}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
