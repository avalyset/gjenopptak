"""Fast steg: ny bundle hver gang en ADDENDUM eller PREREG committes.

    python -m gjenopptak.securerepo              # sikre hvis nødvendig
    python -m gjenopptak.securerepo --force      # sikre uansett
    python -m gjenopptak.securerepo --check      # bare si om det mangler
    python -m gjenopptak.securerepo --install-hook

Samme mønster som frysingens sikringssteg: exit-kode og advarsel hvis bundelen
ikke ble skrevet. Repoet har ingen remote, så en låst fil som bare finnes på
systemdisken kan ikke gjenskapes — og det er historikken, ikke filene, som
beviser at hver låsecommit bar nøyaktig én fil.

Dokumentspeilet (`resultat/` på Vault) friskes opp i samme steg, før sporvalget
— se `gjenopptak.speil` for hvorfor det må ligge først.

Exit-koder: 0 sikret eller ikke nødvendig · 1 noe mangler ved --check (bundle
eller speil) · 3 sikring eller speiling mislyktes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .speil import avvik as speilavvik, etterslep, speil
from .vault import (
    BUNDLE_CLASSES,
    VAULT_ROOT,
    VaultUnavailable,
    WrongBundleClass,
    append_repo_manifest,
    bundle_exists_for,
    commit_touches_locked,
    copy_locked_files,
    require_vault,
    write_bundle,
    _git,
)

HOOK = """#!/bin/sh
# Skrevet av gjenopptak.securerepo --install-hook
# Ny bundle til Vault når en ADDENDUM eller PREREG committes.
cd "$(git rev-parse --show-toplevel)" || exit 0
PYTHONPATH=src .venv/bin/python -m gjenopptak.securerepo || {
    echo "ADVARSEL: repoet ble ikke sikret til Vault. Kjør securerepo manuelt." >&2
}
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--vault-root", type=Path, default=VAULT_ROOT)
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--force", action="store_true",
                    help="Skriv en kodebundle uansett. Går ALLTID til kode/, aldri til kanon/.")
    ap.add_argument("--check", action="store_true", help="Rapporter uten å skrive.")
    ap.add_argument("--install-hook", action="store_true")
    args = ap.parse_args(argv)

    if args.install_hook:
        hook = args.repo / ".git" / "hooks" / "post-commit"
        hook.write_text(HOOK, encoding="utf-8")
        hook.chmod(0o755)
        print(f"post-commit-hook skrevet: {hook}")
        return 0

    # Speilingen går først, og alltid. En commit som bare rører dokumenter
    # utløser ingen bundle, og før dette steget kom hit returnerte funksjonen
    # under med «ingen bundle nødvendig» — uten at speilet ble rørt. Det er
    # nøyaktig slik LICENSE sto med gal navneform i et døgn (jf. speil.py).
    try:
        if args.check:
            bak = etterslep(speilavvik(args.repo, args.vault_root))
            if bak:
                print(f"SPEILET LIGGER BAK: {len(bak)} fil(er) — "
                      f"{', '.join(a.navn for a in bak)}", file=sys.stderr)
                speil_mangler = True
            else:
                speil_mangler = False
        else:
            speil_mangler = False
            kopier = speil(args.repo, args.vault_root)
            for r in kopier:
                print(f"speilet    resultat/{r.dst.name}  sha256 {r.sha256[:12]}")
    except (OSError, VaultUnavailable) as e:
        print(f"IKKE SPEILET: {e}", file=sys.stderr)
        return 3

    utloest = commit_touches_locked(args.repo, args.rev)
    head = _git(args.repo, "rev-parse", args.rev).strip()

    # Sporvalget følger commiten, ikke flagget: --force kan aldri løfte noe inn
    # i kanon/, bare bestille en kodebundle.
    klasse = "kanon" if (utloest and not args.force) else "kode"

    if not utloest and not args.force:
        print(f"{args.rev[:12]} rører ingen låst fil — ingen bundle nødvendig.")
        return 1 if speil_mangler else 0

    try:
        dest = require_vault(args.vault_root)
    except VaultUnavailable as e:
        print(f"IKKE SIKRET: {e}", file=sys.stderr)
        return 3

    alt = bundle_exists_for(dest, head, bundle_class=klasse)
    if alt and not args.force:
        print(f"{head[:12]} er alt dekket av {klasse}/{alt.name}")
        return 1 if speil_mangler else 0

    if args.check:
        print(f"MANGLER BUNDLE ({klasse}) for {head[:12]} "
              f"(utløst av: {', '.join(utloest) or 'force'})")
        return 1

    try:
        bundle = write_bundle(args.repo, root=args.vault_root,
                              bundle_class=klasse, rev=args.rev)
        # De låste filene følger kanon; en kodebundle rører dem ikke.
        locked = copy_locked_files(args.repo, root=args.vault_root) if klasse == "kanon" else []
        append_repo_manifest(dest, bundle, locked)
    except WrongBundleClass as e:
        print(f"IKKE SIKRET (sporfeil): {e}", file=sys.stderr)
        return 3
    except (OSError, VaultUnavailable) as e:
        print(f"IKKE SIKRET: {e}", file=sys.stderr)
        return 3

    merke = "AUTORITATIV" if bundle.authoritative else "restaureringsmateriale"
    print(f"spor       : {klasse}/   ({merke})")
    print(f"utløst av  : {', '.join(utloest) or '--force'}")
    print(f"bundle     : {bundle.path}")
    print(f"bytes      : {bundle.bytes:,}")
    print(f"sha256     : {bundle.sha256}")
    print(f"commits    : {bundle.commits}   HEAD {bundle.head[:12]}")
    if bundle.covers:
        print(f"dekker     : {', '.join(bundle.covers)}")
    if locked:
        print(f"låste filer: {len(locked)} kopiert til repo/laste-filer/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
