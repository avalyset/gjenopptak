"""OpenTimestamps på kanon-bundlene — T2.

**Hvorfor.** En kanon-bundle beviser at en låst fil hadde et gitt innhold *i vår egen historikk*.
Den beviser ikke **når**. Et OpenTimestamps-bevis forankrer hashen i Bitcoins blokkjede gjennom
offentlige kalendere, gratis og uten konto, og gjør «låst før beregning» til en påstand en
utenforstående kan etterprøve mot en tredjepart i stedet for mot oss.

**Hva som stemples.** Bundlen selv. Den attesterte hashen er da nøyaktig de bytene
`MANIFEST-VAULT.md` fører sha256 for, så de to stemmer ved konstruksjon. Å stemple en fil som
*inneholder* hashen ville attestert at en tekststreng fantes, som er et svakere utsagn.

**Hvorfor stemplingen ikke er en forutsetning.** Kalenderne kan være nede. En lås som ikke kan
føres fordi et eksternt nettverk ikke svarer, er verre enn en lås uten tidsstempel: den første
mister revisjonssporet, den andre mister bare tredjepartsbekreftelsen, og den kan settes i
ettertid på samme fil. `stamp()` returnerer derfor en feil i stedet for å kaste.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

#: Kalenderne ots bruker som standard. Oppgis her fordi rapporten skal kunne si hvem som attesterte.
KALENDERE = ("a.pool.opentimestamps.org", "b.pool.opentimestamps.org",
             "a.pool.eternitywall.com", "ots.btc.catallaxy.com")

#: ots krever minst to attestasjoner. Under det finnes ingen kvittering.
MIN_ATTESTASJONER = 2


@dataclass(frozen=True)
class Stempel:
    kilde: Path
    kvittering: Path | None
    bytes: int | None
    feil: str | None

    @property
    def ok(self) -> bool:
        return self.kvittering is not None


def _ots_kjørbar() -> str | None:
    for kandidat in ("ots", str(Path(__file__).resolve().parents[2] / ".venv" / "bin" / "ots")):
        if shutil.which(kandidat) or Path(kandidat).is_file():
            return kandidat
    return None


def _ca_bunt() -> str | None:
    """venv-Pythonen har ikke systemets CA-lager; uten dette feiler hver kalender stille
    på SSL og ots melder «received 0 attestations». Det tok en feilsøkingsrunde å finne."""
    try:
        import certifi
    except ImportError:
        return None
    return certifi.where()


def stamp(fil: Path, *, ut_dir: Path | None = None) -> Stempel:
    """Stempl `fil` og legg kvitteringen i `ut_dir` (standard: `<fil>.ots` ved siden av).

    Stempler på en kopi i en midlertidig katalog, slik at ots ikke skriver i arkivet.
    """
    kjørbar = _ots_kjørbar()
    if kjørbar is None:
        return Stempel(fil, None, None, "ots ikke installert (pip install opentimestamps-client)")
    ut_dir = ut_dir or fil.parent
    ut_dir.mkdir(parents=True, exist_ok=True)
    mål = ut_dir / (fil.name + ".ots")
    if mål.is_file():
        return Stempel(fil, mål, mål.stat().st_size, None)      # idempotent
    miljø = {}
    ca = _ca_bunt()
    if ca:
        miljø["SSL_CERT_FILE"] = ca
    with tempfile.TemporaryDirectory() as td:
        kopi = Path(td) / fil.name
        shutil.copy2(fil, kopi)
        import os
        r = subprocess.run([kjørbar, "stamp", str(kopi)], capture_output=True, text=True,
                           env={**os.environ, **miljø})
        lagd = kopi.with_suffix(kopi.suffix + ".ots")
        if not lagd.is_file():
            siste = (r.stderr or r.stdout or "").strip().splitlines()
            return Stempel(fil, None, None, siste[-1][:160] if siste else "ots ga ingen kvittering")
        shutil.move(str(lagd), mål)
    return Stempel(fil, mål, mål.stat().st_size, None)
