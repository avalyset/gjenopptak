"""Sikring av kildematerialet til et eksternt volum.

En frossen rammeliste koster et helt kvotedøgn å hente på nytt (1 000 kall,
~11 timers nullstilling), og den finnes i utgangspunktet bare på én disk. Denne
modulen kopierer materialet til Vault med sha256-verifisering fil for fil.

**Ingen fallback-sti.** Er volumet ikke montert og skrivbart, kastes
``VaultUnavailable``. En kopi som havner på systemdisken ser ut som en sikring
og er ikke det.

**Verifisering på innhold, ikke på navn.** ``diff -r`` gir falske avvik på macOS
fordi filnavn kan ligge i NFC på den ene siden og NFD på den andre. Sammenligningen
går derfor på sha256 av innholdet, og navneoppslag normaliseres til NFC.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

VAULT_ROOT = Path("/Volumes/Vault")
DEST_NAME = "gjenopptak-kilder"
SUBDIRS = ("raw", "frames", "fulltext", "logs")

#: Filnavnprefikser som er hentet fulltekst, ikke API-svar. For disse føres
#: kilde-URL og hentedato i manifestet: det er det som gjør rammemedlemskap
#: etterprøvbart når en lenke senere svarer 403.
FULLTEXT_PREFIXES = ("jats-", "dl-jats-", "ft-jats-", "cs-jats-",
                     "pdf-", "dl-pdf-", "ft-pdf-")


#: Gulv på systemdisken. Vakten stopper FØR disken fylles, ikke etter.
DISK_GULV_GB = float(os.environ.get("GJENOPPTAK_DISK_GULV_GB", "5"))


class DiskFull(RuntimeError):
    """Systemdisken er under gulvet. Kjøringen startes ikke."""


class VaultUnavailable(RuntimeError):
    """Volumet er ikke montert eller ikke skrivbart. Ingen fallback brukes."""


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def sha256_file(path: Path, *, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while blokk := fh.read(chunk):
            h.update(blokk)
    return h.hexdigest()


def require_vault(root: Path = VAULT_ROOT) -> Path:
    """Bekreft at volumet er montert og skrivbart. Returnerer målkatalogen."""
    if not root.is_dir():
        raise VaultUnavailable(f"{root} finnes ikke — volumet er ikke montert.")
    try:
        mounts = subprocess.run(["mount"], capture_output=True, text=True, timeout=30).stdout
    except (subprocess.SubprocessError, OSError) as e:
        raise VaultUnavailable(f"kunne ikke lese mount-tabellen: {e}") from e
    if f" on {root} " not in mounts:
        raise VaultUnavailable(
            f"{root} er en katalog, men ikke et montert volum. "
            "En kopi hit ville ligget på systemdisken."
        )
    prove = root / f".gjenopptak-write-probe-{datetime.now(timezone.utc).timestamp():.0f}"
    try:
        prove.write_text("probe\n", encoding="utf-8")
        prove.unlink()
    except OSError as e:
        raise VaultUnavailable(f"{root} er montert men ikke skrivbar: {e}") from e
    return root / DEST_NAME


def ensure_layout(dest: Path) -> list[Path]:
    """Opprett gjenopptak-kilder/ med underkatalogene."""
    laget = []
    for sub in ("",) + SUBDIRS:
        p = dest / sub if sub else dest
        p.mkdir(parents=True, exist_ok=True)
        laget.append(p)
    return laget


def is_fulltext(name: str) -> bool:
    return any(nfc(name).startswith(p) for p in FULLTEXT_PREFIXES)


def parse_source_manifest(path: Path) -> dict[str, dict]:
    """Les data/raw/MANIFEST.md til oppslag: filnavn -> bytes, sha256, url, hentet.

    Siste rad for et filnavn vinner: manifestet er append-only, og samme URL kan
    være hentet flere ganger.
    """
    ut: dict[str, dict] = {}
    if not path.exists():
        return ut
    rad = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([0-9a-f]{64})\s*\|\s*(.+?)\s*\|\s*([^|]+?)\s*\|")
    for line in path.read_text(encoding="utf-8").splitlines():
        m = rad.match(line)
        if not m:
            continue
        navn, bytes_, sha, url, hentet = m.groups()
        ut[nfc(navn)] = {"bytes": int(bytes_), "sha256": sha, "source_url": url,
                         "fetched_at": hentet}
    return ut


@dataclass
class CopyResult:
    src: Path
    dst: Path
    bytes: int
    sha256: str
    copied_at: str
    source_url: str | None = None
    fetched_at: str | None = None
    mismatch: bool = False
    dst_sha256: str | None = None


@dataclass
class SecureReport:
    dest: Path
    results: list[CopyResult] = field(default_factory=list)
    skipped: list[tuple[Path, str]] = field(default_factory=list)

    @property
    def n_files(self) -> int:
        return len(self.results)

    @property
    def total_bytes(self) -> int:
        return sum(r.bytes for r in self.results)

    @property
    def mismatches(self) -> list[CopyResult]:
        return [r for r in self.results if r.mismatch]

    def by_subdir(self) -> dict[str, tuple[int, int]]:
        ut: dict[str, list[int]] = {}
        for r in self.results:
            sub = r.dst.parent.name
            a = ut.setdefault(sub, [0, 0])
            a[0] += 1
            a[1] += r.bytes
        return {k: (v[0], v[1]) for k, v in sorted(ut.items())}


def copy_verified(src: Path, dst_dir: Path, meta: dict | None = None) -> CopyResult:
    """Kopier med cp -p og verifiser sha256 mot kilden.

    Sammenligningen går på innhold. Avvik markeres, filen slettes ikke — en
    halvskrevet kopi skal være synlig, ikke ryddet bort.
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    src_sha = sha256_file(src)
    try:
        subprocess.run(["cp", "-p", str(src), str(dst)], check=True,
                       capture_output=True, timeout=600)
    except subprocess.CalledProcessError as e:
        raise OSError(f"cp -p feilet for {src}: {e.stderr.decode()[:200]}") from e
    dst_sha = sha256_file(dst)
    meta = meta or {}
    return CopyResult(
        src=src, dst=dst, bytes=src.stat().st_size, sha256=src_sha,
        copied_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        source_url=meta.get("source_url"), fetched_at=meta.get("fetched_at"),
        mismatch=(src_sha != dst_sha), dst_sha256=dst_sha,
    )


def route(path: Path, data_dir: Path) -> str:
    """Hvilken underkatalog filen hører i.

    Avledet materiale (L2-utdata, oppsummeringer) hører i ``logs/``, ikke i
    ``raw/``: det kan regenereres fra rådata, og å blande det inn ville gjort
    ``raw/`` til noe annet enn «slik det kom fra kilden» (ADR-0001).
    """
    if path.parent.name == "frames":
        return "frames"
    if path.parent.name == "raw":
        return "fulltext" if is_fulltext(path.name) else "raw"
    if path.parent == data_dir:
        return "logs"
    rel = path.parent.relative_to(data_dir) if data_dir in path.parents else None
    if rel is not None:
        return f"logs/{rel.as_posix()}"
    return "raw"


def secure_tree(data_dir: Path, dest: Path, *, only: Iterable[Path] | None = None) -> SecureReport:
    """Kopier data-treet til Vault med verifisering."""
    rep = SecureReport(dest=dest)
    ensure_layout(dest)
    kilde_manifest = parse_source_manifest(data_dir / "raw" / "MANIFEST.md")

    if only is not None:
        filer = [Path(p) for p in only]
    else:
        filer = sorted(p for p in data_dir.rglob("*") if p.is_file())

    for p in filer:
        if p.name.startswith("."):
            rep.skipped.append((p, "skjult fil"))
            continue
        sub = route(p, data_dir)
        meta = kilde_manifest.get(nfc(p.name)) if sub == "fulltext" else None
        try:
            rep.results.append(copy_verified(p, dest / sub, meta))
        except OSError as e:
            rep.skipped.append((p, str(e)[:120]))
    return rep


MANIFEST_HEADER = """# MANIFEST-VAULT — sikret kildemateriale for gjenopptak

Kopiert med `cp -p` fra `~/dev/gjenopptak/data/`. Verifisert med sha256 fil for fil,
på innhold og ikke på filnavn: `diff -r` gir falske avvik på macOS når navn ligger i
NFC på den ene siden og NFD på den andre.

**Hvorfor dette finnes:** en frossen rammeliste koster et helt kvotedøgn å hente på
nytt (OpenAlex: 1 000 kall, ~11 timers nullstilling). For hentet fulltekst er
`kilde-URL` og `hentedato` det som gjør rammemedlemskap etter ADDENDUM-04 §1
etterprøvbart den dagen en lenke svarer 403.

**Filene under `fulltext/` er ikke lest.** De er hentet av rammeprøven og er
rammekriterium, ikke observasjon — jf. `RAMMEPRØVE-IKKE-LEST` i `raw/MANIFEST.md`.

"""


class ManifestWouldShrink(OSError):
    """Manifestet ville mistet filer. Sikringssteget nektet å skrive."""


#: Repo-seksjonene skrives av securerepo med append, kildelisten av
#: write_vault_manifest med full overskriving. De to deler samme fil.
REPO_SECTION = re.compile(r"^## Repo-sikring, ", re.M)


def split_repo_sections(text: str) -> str:
    """Alt fra første «## Repo-sikring, »-overskrift og utover.

    Tom streng når ingen finnes. Brukes for å bære repo-seksjonene over en
    overskriving av kildelisten: securerepo appender dem, write_vault_manifest
    skriver hele filen, og uten dette forsvant de.
    """
    m = REPO_SECTION.search(text)
    return text[m.start():] if m else ""


def manifest_file_count(path: Path) -> int | None:
    """Hvor mange filer et eksisterende MANIFEST-VAULT.md beskriver.

    ``None`` når filen ikke finnes eller ikke bærer feltet. Leses fra
    ``**Filer:**``-linjen, ikke ved å telle tabellrader: repo-seksjonen legger
    til rader som ikke er kildefiler.
    """
    if not path.exists():
        return None
    m = re.search(r"\*\*Filer:\*\*\s*(\d+)", path.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def write_vault_manifest(rep: SecureReport, *, note: str = "",
                         allow_shrink: bool = False) -> tuple[Path, str]:
    """Skriv MANIFEST-VAULT.md. Returnerer (sti, sha256).

    Skrivingen er en full overskriving. Et manifest skrevet fra en delvis
    sikring (``secure_tree(..., only=[...])``) ville derfor slettet raden for
    hver fil som ikke var med — uten feilmelding. Sperren nekter når det
    eksisterende manifestet beskriver flere filer enn rapporten. Den samme
    lærdommen som bundle-overskrivingen: et sikringssteg skal testes mot om det
    kan skade det det skal beskytte.
    """
    path = rep.dest / "MANIFEST-VAULT.md"
    før = manifest_file_count(path)
    if før is not None and rep.n_files < før and not allow_shrink:
        raise ManifestWouldShrink(
            f"{path} beskriver {før} filer, rapporten har {rep.n_files}. "
            "En delvis sikring kan ikke skrive manifestet: kjør secure_tree over "
            "hele data-treet, eller send allow_shrink=True hvis krympingen er "
            "tilsiktet."
        )
    linjer = [MANIFEST_HEADER]
    if note:
        linjer.append(note.rstrip() + "\n\n")
    linjer.append(f"**Skrevet:** {datetime.now(timezone.utc).isoformat(timespec='seconds')}  \n")
    linjer.append(f"**Filer:** {rep.n_files}  **Bytes:** {rep.total_bytes:,}  "
                  f"**Avvikende sjekksummer:** {len(rep.mismatches)}\n\n")
    for sub, (n, b) in rep.by_subdir().items():
        linjer.append(f"* `{sub}/` — {n} filer, {b:,} byte\n")
    linjer.append("\n## Filer\n\n")
    linjer.append("| filsti | bytes | sha256 | kopiert | kilde-URL | hentedato |\n")
    linjer.append("|---|---|---|---|---|---|\n")
    for r in sorted(rep.results, key=lambda r: (r.dst.parent.name, r.dst.name)):
        rel = r.dst.relative_to(rep.dest)
        url = r.source_url or "—"
        hentet = r.fetched_at or "—"
        flagg = " **AVVIK**" if r.mismatch else ""
        linjer.append(f"| {rel} | {r.bytes} | {r.sha256}{flagg} | {r.copied_at} | {url} | {hentet} |\n")
    if rep.skipped:
        linjer.append("\n## Hoppet over\n\n")
        for p, grunn in rep.skipped:
            linjer.append(f"* `{p.name}` — {grunn}\n")
    if før is not None:
        hale = split_repo_sections(path.read_text(encoding="utf-8"))
        if hale:
            linjer.append("\n" + hale.rstrip() + "\n")
    path.write_text("".join(linjer), encoding="utf-8")
    return path, sha256_file(path)


# --------------------------------------------------------------------------- #
# Sikringssteget som frysingen kaller
# --------------------------------------------------------------------------- #

def secure_frame_file(path: Path, *, root: Path = VAULT_ROOT) -> CopyResult:
    """Kopier én frossen rammeliste til Vault og verifiser sha256.

    Kalles av frysingen i samme kjøring som listen skrives. Kaster
    ``VaultUnavailable`` hvis volumet ikke er tilgjengelig — da er listen ikke
    sikret, og det skal være synlig med en gang, ikke oppdages senere.
    """
    dest = require_vault(root)
    ensure_layout(dest)
    res = copy_verified(path, dest / "frames")
    if res.mismatch:
        raise OSError(
            f"sha256 avvek etter kopiering av {path.name}: "
            f"kilde {res.sha256}, kopi {res.dst_sha256}"
        )
    with (dest / "MANIFEST-VAULT.md").open("a", encoding="utf-8") as fh:
        fh.write(f"| frames/{path.name} | {res.bytes} | {res.sha256} | {res.copied_at} "
                 f"| (frysing, lokal) | — |\n")
    return res


# --------------------------------------------------------------------------- #
# Repo-sikring: bundelen bærer historikken
# --------------------------------------------------------------------------- #

#: Filene som er låst og aldri skal endres. Kopieres i tillegg som rene filer:
#: en bundle krever git for å åpnes, disse skal kunne leses med hva som helst.
LOCKED_FILES = (
    "PREREG-v1.md",
    "ADDENDUM-01.md",
    "ADDENDUM-02.md",
    "ADDENDUM-03.md",
    "ADDENDUM-04.md",
    "ADDENDUM-05.md",
    "ADDENDUM-06.md",
    "ADDENDUM-07.md",
    "ADDENDUM-08.md",
    "ADDENDUM-09.md",
)

#: Kjente sha256 for de låste filene. Avvik betyr at en låst fil er endret.
LOCKED_SHA256 = {
    "PREREG-v1.md": "05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a",
    "ADDENDUM-01.md": "aa78d1be50ac17f8e26a92513aa115b3d504bdde3556e43b4f2317ea47cc255f",
    "ADDENDUM-02.md": "7c0542c92c54a586e3b387794272bed171ee285b75c8ebe4ee8fe1fa16f6f713",
    "ADDENDUM-03.md": "0b577ae6c3d0278e811e674c78e4e2948be46252e5aca9c94e94466c1f985c4e",
    "ADDENDUM-04.md": "7f7d067b80468a7016e398d1120930c98eb8a705b0e1c0102ad97e9db42f8a9c",
    "ADDENDUM-05.md": "b12c85b2a731517f9d0c5742194b2b8a900177cb82d662f8bf20e7d67fef5e9d",
    "ADDENDUM-06.md": "0f0e9a8126804f8a8fdf185864e80612c76816c2a536cf696df29e65d8c05687",
    "ADDENDUM-07.md": "06eb4fb365413d089601d592bf273b08fa96d25b94390d771ad38a45b9c2a3c3",
    "ADDENDUM-08.md": "6888efb33a6bba03545d6891f78936c6c15006d0a148a6da414f24c165ae3a26",
    "ADDENDUM-09.md": "79f1baf58aba19f43324cd823759b9638620c932cac457154649c80b244466c3",
}

BUNDLE_NOTE = (
    "**Nyeste bundle i `repo/kanon/` er den autoritative kopien.** De rene filene "
    "under `repo/laste-filer/` kan leses uten git, men bare bundelen bærer "
    "historikken — og det er historikken som beviser at hver låsecommit bar "
    "nøyaktig én fil. Uten den er en låsedato en påstand."
)

CODE_NOTE = (
    "**Kodebundler er restaureringsmateriale, ikke arkiv.** De bærer samme "
    "historikk som kanonbundlene pluss senere kodearbeid, men de fester ingen "
    "låserekkefølge og kan ikke siteres som kilde for en låsedato. Er de to i "
    "konflikt, gjelder nyeste bundle i `repo/kanon/`."
)

#: De to arkivsporene. De ligger i hver sin katalog og har hvert sitt
#: navneprefiks, slik at ingen fil kan være tvetydig klassifisert.
BUNDLE_CLASSES = {
    "kanon": {"dir": "kanon", "prefix": "gjenopptak-",
              "trigger": "PREREG- eller ADDENDUM-commit", "authoritative": True},
    "kode": {"dir": "kode", "prefix": "gjenopptak-kode-",
             "trigger": "alt annet, --force, eller manuelt", "authoritative": False},
}


class WrongBundleClass(ValueError):
    """En kodebundle ble forsøkt skrevet til kanon/. Sporene skal ikke blandes."""


@dataclass
class BundleResult:
    path: Path
    bytes: int
    sha256: str
    commits: int
    written_at: str
    head: str
    bundle_class: str = "kanon"
    covers: tuple[str, ...] = ()      # hvilke låste filer commiten førte inn

    @property
    def authoritative(self) -> bool:
        return BUNDLE_CLASSES[self.bundle_class]["authoritative"]


def _git(repo: Path, *args: str, check: bool = True) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       text=True, timeout=600)
    if check and r.returncode != 0:
        raise OSError(f"git {' '.join(args)} feilet: {r.stderr.strip()[:300]}")
    return r.stdout


def bundle_name(repo: Path, *, date: str | None = None, head: str | None = None,
                bundle_class: str = "kanon") -> str:
    """Filnavn med dato **og** HEAD.

    Dato alene er ikke nok: to bundler samme dag ville overskrevet hverandre.
    Det ble oppdaget da en dummy-commit på en throwaway-gren skrev over den
    ekte bundelen i en test. Med HEAD i navnet er en ny commit en ny fil, og
    samme commit gir samme fil — idempotent, ikke destruktivt.
    """
    if bundle_class not in BUNDLE_CLASSES:
        raise WrongBundleClass(f"ukjent bundleklasse: {bundle_class!r}")
    dag = date or datetime.now(timezone.utc).date().isoformat()
    h = (head or _git(repo, "rev-parse", "HEAD").strip())[:12]
    return f"{BUNDLE_CLASSES[bundle_class]['prefix']}{dag}-{h}.bundle"


def write_bundle(repo: Path, *, root: Path = VAULT_ROOT, date: str | None = None,
                 bundle_class: str = "kanon", rev: str = "HEAD") -> BundleResult:
    """Skriv en git bundle med --all til riktig arkivspor.

    **Invariant:** kanon/ tar bare commits som faktisk fører inn en låst fil.
    Er kravet ikke oppfylt, kastes ``WrongBundleClass`` og ingenting skrives —
    en kodebundle skal ikke kunne havne i kanon/ ved noen kombinasjon av flagg.
    """
    if bundle_class not in BUNDLE_CLASSES:
        raise WrongBundleClass(f"ukjent bundleklasse: {bundle_class!r}")
    covers = tuple(commit_touches_locked(repo, rev))
    if bundle_class == "kanon" and not covers:
        raise WrongBundleClass(
            f"{rev} fører ingen låst fil inn og kan ikke skrives til kanon/. "
            "Kanon bærer låserekkefølgen; kodearbeid hører i kode/."
        )
    dest = require_vault(root)
    spor = dest / "repo" / BUNDLE_CLASSES[bundle_class]["dir"]
    spor.mkdir(parents=True, exist_ok=True)
    path = spor / bundle_name(repo, date=date, bundle_class=bundle_class)
    _git(repo, "bundle", "create", str(path), "--all")
    _git(repo, "bundle", "verify", str(path))      # git sin egen integritetssjekk
    head = _git(repo, "rev-parse", rev).strip()
    return BundleResult(
        path=path, bytes=path.stat().st_size, sha256=sha256_file(path),
        commits=int(_git(repo, "rev-list", "--count", "--all").strip()),
        written_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        head=head, bundle_class=bundle_class, covers=covers,
    )


def copy_locked_files(repo: Path, *, root: Path = VAULT_ROOT) -> list[CopyResult]:
    """Kopier de låste filene som rene filer, og sjekk dem mot kjent sha256."""
    dest = require_vault(root)
    ut = []
    for navn in LOCKED_FILES:
        src = repo / navn
        if not src.exists():
            raise OSError(f"låst fil mangler i repoet: {navn}")
        res = copy_verified(src, dest / "repo" / "laste-filer")
        ventet = LOCKED_SHA256.get(navn)
        if ventet and res.sha256 != ventet:
            raise OSError(
                f"{navn} har sha256 {res.sha256}, ventet {ventet}. "
                "En låst fil er endret — sikring avbrutt."
            )
        ut.append(res)
    return ut


def append_repo_manifest(dest: Path, bundle: BundleResult,
                         locked: list[CopyResult] | None = None) -> None:
    """Før bundelen inn i sin egen seksjon i MANIFEST-VAULT.md.

    De to sporene får hver sin seksjon. Kanon fører hvilken ADDENDUM hver bundle
    dekker; kode føres som restaureringsmateriale.
    """
    man = dest / "MANIFEST-VAULT.md"
    kanon = bundle.bundle_class == "kanon"
    with man.open("a", encoding="utf-8") as fh:
        if kanon:
            fh.write(f"\n## Repo-sikring, kanon — {bundle.written_at}\n\n")
            fh.write(BUNDLE_NOTE + "\n\n")
            fh.write("| filsti | bytes | sha256 | skrevet | dekker | merknad |\n")
            fh.write("|---|---|---|---|---|---|\n")
            fh.write(f"| repo/kanon/{bundle.path.name} | {bundle.bytes} | {bundle.sha256} "
                     f"| {bundle.written_at} | {', '.join(bundle.covers) or '—'} "
                     f"| git bundle --all, {bundle.commits} commits, "
                     f"HEAD {bundle.head[:12]} — AUTORITATIV |\n")
        else:
            fh.write(f"\n## Repo-sikring, kode — {bundle.written_at}\n\n")
            fh.write(CODE_NOTE + "\n\n")
            fh.write("| filsti | bytes | sha256 | skrevet | merknad |\n|---|---|---|---|---|\n")
            fh.write(f"| repo/kode/{bundle.path.name} | {bundle.bytes} | {bundle.sha256} "
                     f"| {bundle.written_at} | git bundle --all, {bundle.commits} commits, "
                     f"HEAD {bundle.head[:12]} — RESTAURERINGSMATERIALE, ikke arkiv |\n")
        for r in (locked or []):
            fh.write(f"| repo/laste-filer/{r.dst.name} | {r.bytes} | {r.sha256} "
                     f"| {r.copied_at} |{' låst fil |' if not kanon else ' — | låst fil, lesbar uten git |'}\n")


# --------------------------------------------------------------------------- #
# Fast steg: ny bundle når en ADDENDUM committes
# --------------------------------------------------------------------------- #

#: Filer som utløser en ny bundle når de kommer inn i en commit.
TRIGGER_PATTERN = re.compile(r"^(PREREG-v1\.md|ADDENDUM-\d+\.md)$")


def commit_touches_locked(repo: Path, rev: str = "HEAD") -> list[str]:
    """Filnavnene i commiten som utløser sikring."""
    ut = _git(repo, "show", "--pretty=format:", "--name-only", rev)
    return [n for n in (l.strip() for l in ut.splitlines()) if n and TRIGGER_PATTERN.match(n)]


def bundle_exists_for(dest: Path, head: str, *, bundle_class: str = "kanon") -> Path | None:
    """Finn en bundle i det angitte sporet som alt dekker denne commiten."""
    spor = dest / "repo" / BUNDLE_CLASSES[bundle_class]["dir"]
    if not spor.is_dir():
        return None
    for p in spor.glob("*.bundle"):
        if head[:12] in p.name:
            return p
    return None


def latest_canon(dest: Path) -> Path | None:
    """Nyeste bundle i kanon/ — den autoritative kopien."""
    spor = dest / "repo" / "kanon"
    if not spor.is_dir():
        return None
    kandidater = sorted(spor.glob("gjenopptak-*.bundle"), key=lambda p: p.stat().st_mtime)
    return kandidater[-1] if kandidater else None


def ledig_gb(sti: Path | None = None) -> float:
    """Ledig plass i GB der ``sti`` ligger (systemdisken når intet er oppgitt)."""
    return shutil.disk_usage(sti or Path.cwd()).free / 1e9


def diskvakt(sti: Path | None = None, gulv: float = DISK_GULV_GB) -> float:
    """Stopp før disken fylles. Kaster ``DiskFull`` når det er mindre enn gulvet igjen."""
    ledig = ledig_gb(sti)
    if ledig < gulv:
        raise DiskFull(
            f"{ledig:.1f} GB ledig på {sti or Path.cwd()}, gulvet er {gulv:.1f} GB. "
            "Kjøringen startes ikke. Sett GJENOPPTAK_DISK_GULV_GB for å endre gulvet."
        )
    return ledig


def krev(data_dir: Path | str | None = None, *, gulv: float = DISK_GULV_GB) -> Path:
    """Vault er standard for alt som skrives (ADR-0009). Ingen fallback.

    Uten montert og skrivbart volum kastes ``VaultUnavailable`` før modulen gjør noe.
    En eksplisitt katalog godtas bare når den ligger under Vault-roten — ellers ville en
    kjøring se ut som en sikring og havne på systemdisken.
    """
    dest = require_vault()
    diskvakt(gulv=gulv)
    if data_dir is None:
        dest.mkdir(parents=True, exist_ok=True)
        return dest
    d = Path(data_dir).resolve()
    rot = VAULT_ROOT.resolve()
    if d != rot and rot not in d.parents:
        raise VaultUnavailable(
            f"{d} ligger ikke under {rot}. ADR-0009: skrivende moduler skriver til Vault, "
            "systemdisken brukes bare til det som kan regenereres på minutter."
        )
    d.mkdir(parents=True, exist_ok=True)
    return d


def utkatalog(under: str, *, gulv: float = DISK_GULV_GB) -> Path:
    """Utdatakatalog på Vault, f.eks. ``utkatalog("logs/port")``."""
    p = krev(gulv=gulv) / under
    p.mkdir(parents=True, exist_ok=True)
    return p
