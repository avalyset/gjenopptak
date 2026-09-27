"""Konfigurasjonen for kjeden, lest fra én fil.

ADR-0012: modell, frø, ``num_ctx``, øktstørrelse og stier står i én fil, slik at en
kjøring kan gjentas på en annen maskin uten å redigere kode. Ingen sti er hardkodet i
koden; alt går gjennom :class:`Konfig`.

Filen finnes ved å gå oppover fra arbeidskatalogen til ``kjede.toml`` dukker opp, eller
den oppgis med ``--konfig``. Katalogen filen ligger i, er **rota**: alle relative stier i
filen løses mot den, ikke mot arbeidskatalogen.
"""

from __future__ import annotations

import hashlib
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

FILNAVN = "kjede.toml"


class KonfigFeil(RuntimeError):
    """Konfigurasjonen mangler, er ufullstendig, eller en sha stemmer ikke."""


def finn_konfig(start: Path | None = None) -> Path:
    """Gå oppover fra ``start`` til ``kjede.toml`` finnes. Ingen fallback."""
    p = (start or Path.cwd()).resolve()
    for kandidat in (p, *p.parents):
        f = kandidat / FILNAVN
        if f.is_file():
            return f
    raise KonfigFeil(f"fant ikke {FILNAVN} i {p} eller noen foreldrekatalog")


def sha256_fil(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for blokk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blokk)
    return h.hexdigest()


@dataclass(frozen=True)
class Konfig:
    """Hele konfigurasjonen, med rota og de utregnede stiene."""

    rot: Path
    fil: Path
    raa: dict

    # --- oppslag ---------------------------------------------------------------
    def seksjon(self, navn: str) -> dict:
        try:
            return self.raa[navn]
        except KeyError as e:
            raise KonfigFeil(f"seksjonen [{navn}] mangler i {self.fil}") from e

    def verdi(self, seksjon: str, nøkkel: str):
        s = self.seksjon(seksjon)
        try:
            return s[nøkkel]
        except KeyError as e:
            raise KonfigFeil(f"{nøkkel} mangler i [{seksjon}] i {self.fil}") from e

    def sti(self, seksjon: str, nøkkel: str) -> Path:
        """Sti fra konfigurasjonen, løst mot rota om den er relativ."""
        p = Path(str(self.verdi(seksjon, nøkkel)))
        return p if p.is_absolute() else (self.rot / p)

    # --- de stiene kjeden bruker ofte ------------------------------------------
    @property
    def vault_rot(self) -> Path:
        return Path(str(self.verdi("vault", "rot")))

    @property
    def vault_mål(self) -> Path:
        return self.vault_rot / str(self.verdi("vault", "navn"))

    @property
    def arbeid(self) -> Path:
        return self.sti("kjede", "arbeid")

    def kjøring(self, navn: str) -> Path:
        """Arbeidskatalogen for én navngitt kjøring."""
        return self.arbeid / navn

    def vault_sti(self, seksjon: str, nøkkel: str) -> Path:
        """Sti oppgitt relativt til Vault-målet (regelfil, oppdragsmal)."""
        p = Path(str(self.verdi(seksjon, nøkkel)))
        return p if p.is_absolute() else (self.vault_mål / p)

    # --- kontroll --------------------------------------------------------------
    def sjekk_sha(self, par: list[tuple[str, Path, str]]) -> list[str]:
        """Verifiser oppgitte sha256. Returnerer avvikene, kaster ikke."""
        avvik = []
        for navn, p, ventet in par:
            if not p.is_file():
                avvik.append(f"{navn}: filen finnes ikke ({p})")
                continue
            fikk = sha256_fil(p)
            if fikk != ventet:
                avvik.append(f"{navn}: sha256 {fikk[:16]}… ≠ ventet {ventet[:16]}… ({p})")
        return avvik

    def laaste_filer(self) -> list[tuple[str, Path, str]]:
        """Alt kjeden leser som er låst med en sha i konfigurasjonen."""
        return [
            ("dommerens ledetekst", self.sti("dommer", "ledetekst"),
             str(self.verdi("dommer", "ledetekst_sha256"))),
            ("ekstraksjonens ledetekst", self.sti("ekstraksjon", "ledetekst"),
             str(self.verdi("ekstraksjon", "ledetekst_sha256"))),
            ("ikke-prosa-regelen", self.sti("sil", "ikke_prosa_regel"),
             str(self.verdi("sil", "ikke_prosa_sha256"))),
            ("leserens regelfil", self.vault_sti("leser", "regelfil"),
             str(self.verdi("leser", "regelfil_sha256"))),
            ("leserens oppdragsmal", self.vault_sti("leser", "oppdrag_mal"),
             str(self.verdi("leser", "oppdrag_mal_sha256"))),
        ]


def last(fil: Path | None = None, *, start: Path | None = None) -> Konfig:
    """Les konfigurasjonen. ``fil`` overstyrer søket."""
    f = (fil or finn_konfig(start)).resolve()
    if not f.is_file():
        raise KonfigFeil(f"konfigurasjonsfilen finnes ikke: {f}")
    with f.open("rb") as fh:
        raa = tomllib.load(fh)
    for påkrevd in ("kjede", "vault", "tekstbiter", "dommer", "ekstraksjon", "sil",
                    "leser", "register", "kvote"):
        if påkrevd not in raa:
            raise KonfigFeil(f"seksjonen [{påkrevd}] mangler i {f}")
    # ADR-0012, datert tillegg 27.09.2026: verktøyet kaller ikke Anthropics API. En konfigurasjon
    # som prøver å slå den på igjen, avvises her og ikke først ved kallet.
    if "api" in raa:
        raise KonfigFeil(
            f"[api] står i {f}, men verktøyet kaller ikke Anthropics API (ADR-0012, datert "
            f"tillegg 27.09.2026). Fjern seksjonen.")
    return Konfig(rot=f.parent, fil=f, raa=raa)
