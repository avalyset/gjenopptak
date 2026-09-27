"""Speiling av dokumenter til Vault: `resultat/` skal aldri ligge bak repoet.

    python -m gjenopptak.speil            # frisk opp det som ligger bak
    python -m gjenopptak.speil --check    # bare rapporter avvik (exit 1 ved avvik)

Bakgrunnen er et målt etterslep. Speilet ble holdt ved lag med `cp` for hånd, én
fil per slynge. Da `7fb32fc` rettet navneformen i `LICENSE`, `LICENSE-DATA` og
`README.md`, rørte den ingen låst fil — `securerepo` svarte «ingen bundle
nødvendig» og returnerte *før* noe ble kopiert, og speilet sto med den gale
navneformen i et døgn uten at noe meldte fra.

Derfor: sammenligningen går på **innhold**, ikke på tidsstempel eller på om en
bundle ble skrevet, og speilingen kjøres *først* i `securerepo`, før sporvalget
kan returnere tidlig. En fil i speilet som ikke har noen kilde i repoet
(byggeartefakter som PDF-en og abstraktet) rapporteres som foreldreløs og røres
aldri — speilet sletter ingenting.

Exit-koder: 0 à jour · 1 avvik funnet ved --check · 3 speiling mislyktes.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from .vault import (
    VAULT_ROOT,
    CopyResult,
    VaultUnavailable,
    copy_verified,
    require_vault,
    sha256_file,
)

SPEILKATALOG = "resultat"

#: Kataloger et speilnavn slås opp i, i rekkefølge. Første treff vinner, og den
#: løste stien føres i rapporten slik at oppslaget kan etterprøves.
KILDEROTER = (
    ".",
    "docs",
    "docs/decisions",
    "src/gjenopptak/schemas",
    "src/gjenopptak/falsify",
)

#: Dokumenter som *skal* ligge i speilet. Settet er de repo-sporede filene som er
#: deponert på Zenodo — er en fil god nok å publisere, er den god nok å sikre.
#: Nye dokumenter føres inn her bevisst, ikke ved at noen husker å kopiere.
PLIKT = (
    "CITATION.cff",
    "LICENSE",
    "LICENSE-DATA",
    "README.md",
    "ADDENDUM-10.md",
    "ADDENDUM-11.md",
    "docs/HERON-KOLLASJON-VURDERING-v1.md",
    "docs/HERON-KOLLASJON-VURDERING-v2.md",
    "docs/LAERDOM.md",
    "docs/METODE.md",
    "docs/LOFTBARE-VURDERING-v1.md",
    "docs/MANUSKRIPT-v0.1.md",
    "docs/PREPRINT.md",
    "docs/PS-246-KRITERIUM.md",
    "docs/PS-246-RESULTAT.md",
    "docs/RESULTAT-PORT-v1.md",
    "docs/ZENODO.md",
    "docs/laerdom-sikring.md",
    "docs/decisions/0001-korpusgrense-aapen-fulltekst.md",
    "docs/decisions/0002-seksjonsbevaring.md",
    "docs/decisions/0003-modellsignatur.md",
    "docs/decisions/0004-loftbarhet-fra-tabell.md",
    "docs/decisions/0007-seksjonsetikettens-opphav.md",
    "docs/decisions/0008-keepalive-ved-batch.md",
    "docs/decisions/0009-vault-som-standard.md",
    "docs/decisions/0010-loftbarhet-er-datert.md",
    "src/gjenopptak/schemas/claims.schema.json",
    "src/gjenopptak/falsify/saxton_rawls.py",
)

LIK = "lik"
UTDATERT = "utdatert"
MANGLER = "mangler"
FORELDRELOES = "foreldreløs"

#: Statusene som krever handling. Foreldreløse filer gjør det ikke.
ETTERSLEP = (UTDATERT, MANGLER)


@dataclass(frozen=True)
class Avvik:
    """Én linje i speilsjekken. `kilde` er None for foreldreløse filer."""

    navn: str
    status: str
    kilde: Path | None = None
    speil: Path | None = None
    kilde_sha: str | None = None
    speil_sha: str | None = None

    @property
    def maa_rettes(self) -> bool:
        return self.status in ETTERSLEP


def finn_kilde(repo: Path, navn: str) -> Path | None:
    """Slå et speilnavn tilbake til kildefilen i repoet."""
    for rot in KILDEROTER:
        kandidat = repo / rot / navn
        if kandidat.is_file():
            return kandidat.resolve()
    return None


def avvik(repo: Path, root: Path = VAULT_ROOT, *,
          speilkatalog: str = SPEILKATALOG) -> list[Avvik]:
    """Sammenlign speilet med repoet på innhold. Rapporterer også det som er likt."""
    dest = require_vault(root)
    speilsti = dest / speilkatalog
    ut: list[Avvik] = []
    sett: set[str] = set()

    for rel in PLIKT:
        src = repo / rel
        navn = Path(rel).name
        sett.add(navn)
        mål = speilsti / navn
        if not src.is_file():
            # Kilden er borte fra repoet. Ikke vår sak å rydde i speilet.
            ut.append(Avvik(navn, FORELDRELOES, None, mål if mål.exists() else None,
                            None, sha256_file(mål) if mål.is_file() else None))
            continue
        ksha = sha256_file(src)
        if not mål.is_file():
            ut.append(Avvik(navn, MANGLER, src, mål, ksha, None))
            continue
        ssha = sha256_file(mål)
        ut.append(Avvik(navn, LIK if ksha == ssha else UTDATERT, src, mål, ksha, ssha))

    # Alt annet som ligger i speilet: byggeartefakter og gamle kopier. De skal
    # ses, ikke fjernes — men en fil som *har* en kilde i repoet og likevel
    # avviker fra den, er et etterslep uansett om den står i PLIKT.
    if speilsti.is_dir():
        for mål in sorted(speilsti.iterdir()):
            if not mål.is_file() or mål.name in sett or mål.name.startswith("."):
                continue
            src = finn_kilde(repo, mål.name)
            if src is None:
                ut.append(Avvik(mål.name, FORELDRELOES, None, mål, None, sha256_file(mål)))
                continue
            ksha, ssha = sha256_file(src), sha256_file(mål)
            ut.append(Avvik(mål.name, LIK if ksha == ssha else UTDATERT,
                            src, mål, ksha, ssha))

    return sorted(ut, key=lambda a: (a.status != LIK, a.navn))


def etterslep(rader: list[Avvik]) -> list[Avvik]:
    return [a for a in rader if a.maa_rettes]


def speil(repo: Path, root: Path = VAULT_ROOT, *,
          speilkatalog: str = SPEILKATALOG) -> list[CopyResult]:
    """Kopier alt som ligger bak, og verifiser sha256 begge veier.

    Et avvik mellom kilde og kopi etter `cp` er en feil, ikke en advarsel:
    da har speilet fortsatt ikke det innholdet det skal ha.
    """
    dest = require_vault(root)
    ut: list[CopyResult] = []
    for a in etterslep(avvik(repo, root, speilkatalog=speilkatalog)):
        assert a.kilde is not None
        res = copy_verified(a.kilde, dest / speilkatalog)
        if res.mismatch or res.sha256 != a.kilde_sha:
            raise OSError(
                f"{a.navn}: kopien fikk sha256 {res.dst_sha256}, kilden har {res.sha256}. "
                "Speilet er ikke à jour — speiling avbrutt."
            )
        ut.append(res)
    return ut


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--vault-root", type=Path, default=VAULT_ROOT)
    ap.add_argument("--speilkatalog", default=SPEILKATALOG)
    ap.add_argument("--check", action="store_true", help="Rapporter uten å skrive.")
    ap.add_argument("--stille", action="store_true", help="Bare avvik, ikke det som er likt.")
    args = ap.parse_args(argv)

    try:
        rader = avvik(args.repo, args.vault_root, speilkatalog=args.speilkatalog)
    except VaultUnavailable as e:
        print(f"IKKE SPEILET: {e}", file=sys.stderr)
        return 3

    bak = etterslep(rader)
    for a in rader:
        if args.stille and a.status == LIK:
            continue
        merke = {LIK: "lik        ", UTDATERT: "UTDATERT   ",
                 MANGLER: "MANGLER    ", FORELDRELOES: "foreldreløs"}[a.status]
        print(f"{merke} {a.navn}")

    n_lik = sum(1 for a in rader if a.status == LIK)
    n_foreldre = sum(1 for a in rader if a.status == FORELDRELOES)
    print(f"\n{len(rader)} filer: {n_lik} like, {len(bak)} bak, {n_foreldre} foreldreløse")

    if not bak:
        return 0
    if args.check:
        for a in bak:
            print(f"  {a.status}: {a.navn}  kilde {(a.kilde_sha or '')[:12]}  "
                  f"speil {(a.speil_sha or '—')[:12]}", file=sys.stderr)
        return 1

    try:
        kopier = speil(args.repo, args.vault_root, speilkatalog=args.speilkatalog)
    except (OSError, VaultUnavailable) as e:
        print(f"IKKE SPEILET: {e}", file=sys.stderr)
        return 3
    for r in kopier:
        print(f"speilet    {r.dst.name}  {r.bytes:,} B  sha256 {r.sha256[:12]}")
    print(f"{len(kopier)} filer friskmeldt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
