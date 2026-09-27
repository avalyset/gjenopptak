"""Felt som konfigurasjon (byggeplanen B2).

Et felt er en fil, ikke kode. Alt som gjør et felt til et felt — emne-ID-ene, årsspennet,
rammelisten med sjekksum, tersklene — står i ``felt/<navn>.yaml``. Å legge til et felt krever
derfor ingen kodeendring: legg filen der, og ``gjenopptak run --felt <navn>`` finner den.

**Emne-ID-ene er hentet fra spørringen, ikke fra verkene.** Rammen ble frosset med et
``topics.id:``-filter, og den URL-en står i det frosne rådata-manifestet
(``raw/MANIFEST.md``). Verkenes egne ``primary_topic_id`` er noe annet — de er *resultatet* av
spørringen, hundrevis per felt, og kan ikke brukes til å definere feltet.

**Rammelistens sha256 er kilden til at listen ikke har flyttet seg.** Er filen der og sha-en
stemmer ikke, avvises feltet. Er filen ikke der ennå, er feltet planleggbart men ikke kjørbart:
``--torr`` regner kostnaden for å bygge rammen, en ekte kjøring krever at den finnes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .konfig import Konfig, KonfigFeil, sha256_fil

KATALOG = "felt"


@dataclass(frozen=True)
class Felt:
    navn: str
    topics: list[str]
    ar: tuple[int, int]
    ar_spurt: tuple[int, int]
    ramme_fil: str
    ramme_sha256: str
    ramme_rader: int
    ramme_krav: str
    terskler: dict
    kilde: Path

    @property
    def n_verk(self) -> int:
        return int(self.terskler.get("n_verk", 0))

    @property
    def gulv(self) -> int:
        return int(self.terskler.get("gulv", 0))


def katalog(k: Konfig) -> Path:
    return k.rot / KATALOG


def navn_liste(k: Konfig) -> list[str]:
    d = katalog(k)
    return sorted(p.stem for p in d.glob("*.yaml")) if d.is_dir() else []


def last_felt(k: Konfig, navn: str) -> Felt:
    """Les én feltfil. Kaster :class:`KonfigFeil` med de kjente navnene om den mangler."""
    import yaml

    p = katalog(k) / f"{navn}.yaml"
    if not p.is_file():
        kjente = navn_liste(k)
        raise KonfigFeil(f"finner ingen feltfil {p}. Kjente felt: {', '.join(kjente) or 'ingen'}")
    d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    for påkrevd in ("felt", "topics", "ar", "ramme", "terskler"):
        if påkrevd not in d:
            raise KonfigFeil(f"{p}: nøkkelen {påkrevd!r} mangler")
    if d["felt"] != navn:
        raise KonfigFeil(f"{p}: feltnavnet i filen er {d['felt']!r}, men filen heter {navn!r}")
    r = d["ramme"]
    for påkrevd in ("fil", "sha256", "rader"):
        if påkrevd not in r:
            raise KonfigFeil(f"{p}: ramme.{påkrevd} mangler")
    return Felt(navn=navn, topics=list(d["topics"]), ar=tuple(d["ar"]),
                ar_spurt=tuple(d.get("ar_spurt", d["ar"])), ramme_fil=str(r["fil"]),
                ramme_sha256=str(r["sha256"]), ramme_rader=int(r["rader"]),
                ramme_krav=str(r.get("krav", "hentbar")), terskler=dict(d["terskler"]), kilde=p)


def ramme_status(k: Konfig, f: Felt) -> tuple[str, str]:
    """``(ok|mangler|avvik, forklaring)`` for rammelisten feltet peker på."""
    p = Path(f.ramme_fil)
    p = p if p.is_absolute() else (k.vault_mål / p)
    if not p.is_file():
        return "mangler", (f"{p} finnes ikke — feltet er planleggbart, ikke kjørbart; "
                           f"rammen må frosses først")
    fikk = sha256_fil(p)
    if fikk != f.ramme_sha256:
        return "avvik", f"{p}: sha256 {fikk[:16]}… ≠ {f.ramme_sha256[:16]}… i {f.kilde.name}"
    return "ok", f"{p} ({f.ramme_rader:,} rader, sha256 stemmer)"
