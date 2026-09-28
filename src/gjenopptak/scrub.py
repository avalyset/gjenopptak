"""Scrub over det treet som skal publiseres — ADR-0012, datert tillegg 28.09.2026 punkt 6.

Kjøres over **utgivelsestreet**, ikke over diffen: en hemmelighet som ble lagt inn før forrige
utgivelse og ikke rørt siden, står ikke i diffen, men står i treet.

**Verdier skrives aldri ut.** Bare mønsternavn, fil, linjenummer og en redigert form som viser at
mønsteret traff uten å gjengi det som traff. Det er hele poenget: et scrub-verktøy som logger
hemmeligheten, har lekket den til hver logg og hver terminalbuffer.

Exit-koder: 0 ingen treff · 1 treff funnet (som kan være redegjort for; scrubben avgjør ikke).
"""
from __future__ import annotations

import re
import subprocess
import sys

#: Scrubbens egne filer. De inneholder mønstrene og testfixturer for hvert mønster, så de
#: treffer alltid. En skanner som ikke kan skanne et repo som inneholder en skanner, er ubrukelig
#: som port. Listen er bevisst to navn lang, står i utdata ved hver kjøring, og er låst av en test:
#: filunntak er nøyaktig måten en scrub blir satt ut av spill, så den skal ikke kunne vokse stille.
SELVUNNTAK: tuple[str, ...] = ("src/gjenopptak/scrub.py", "tests/test_scrub.py")

#: Elleve mønstre. Rekkefølgen er stabil fordi rapporten sammenlignes mellom utgivelser.
MØNSTRE: list[tuple[str, str]] = [
    ("Anthropic-nøkkel", r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    ("OpenAI-nøkkel", r"\bsk-[A-Za-z0-9]{32,}"),
    ("Google-nøkkel", r"AIza[A-Za-z0-9_\-]{30,}"),
    ("GitHub-token", r"gh[pousr]_[A-Za-z0-9]{30,}"),
    ("AWS-nøkkel", r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    ("PEM-privatnøkkel", r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY"),
    ("Bearer-token", r"[Bb]earer\s+[A-Za-z0-9._\-]{20,}"),
    ("privat e-post", r"[A-Za-z0-9._%+-]+@(?:gmail|hotmail|outlook|icloud|live|yahoo)\.[a-z]{2,}"),
    ("forretnings-e-post", r"[A-Za-z0-9._%+-]+@ecodeco\.no"),
    ("absolutt hjemmesti", r"/Users/[a-z]+"),
    ("ordet «sealed»", r"\bsealed\b"),
]


def redigert(linje: str, monster: str) -> str:
    """Linjen med det som traff, byttet ut. Fire tegn beholdes så formen er lesbar."""
    return re.sub(monster, lambda m: m.group(0)[:4] + "…REDIGERT…", linje)


def sjekk_tre(ref: str = "HEAD") -> dict[str, list[tuple[str, int, str]]]:
    filer = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref],
                           capture_output=True, text=True, check=True).stdout.split()
    treff: dict[str, list[tuple[str, int, str]]] = {}
    for f in filer:
        if f in SELVUNNTAK:
            continue
        b = subprocess.run(["git", "show", f"{ref}:{f}"], capture_output=True, check=True).stdout
        try:
            tekst = b.decode("utf-8")
        except UnicodeDecodeError:
            continue                                  # binærfil: ingen linjer å lese
        for navn, m in MØNSTRE:
            for i, linje in enumerate(tekst.splitlines(), 1):
                if re.search(m, linje):
                    treff.setdefault(navn, []).append((f, i, redigert(linje, m).strip()[:100]))
    return treff


def main(argv: list[str] | None = None) -> int:
    ref = (argv or sys.argv[1:] or ["HEAD"])[0]
    n = len(subprocess.run(["git", "ls-tree", "-r", "--name-only", ref],
                           capture_output=True, text=True, check=True).stdout.split())
    treff = sjekk_tre(ref)
    grønne = [navn for navn, _ in MØNSTRE if navn not in treff]
    print(f"scrub over {ref}: {n} filer, {len(MØNSTRE)} mønstre")
    print(f"  SELVUNNTAK ({len(SELVUNNTAK)}): {', '.join(SELVUNNTAK)} — "
          f"inneholder mønstrene selv")
    print(f"  GRØNNE ({len(grønne)}/{len(MØNSTRE)}): {', '.join(grønne)}")
    for navn, rader in treff.items():
        print(f"\n  TREFF  {navn} — {len(rader)} linje(r)")
        for f, i, r in rader[:8]:
            print(f"      {f}:{i}  {r}")
        if len(rader) > 8:
            print(f"      … og {len(rader) - 8} flere")
    if treff:
        print("\nTreff betyr ikke nødvendigvis en hemmelighet. Hvert treff skal redegjøres for i "
              "utgivelsesnotatet, og scrubben avgjør ikke om det er greit.")
    return 1 if treff else 0


if __name__ == "__main__":
    raise SystemExit(main())
