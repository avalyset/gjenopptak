"""Kryssdokumentsjekk: samme størrelse skal ha samme verdi i alle filer som deponeres.

    python -m gjenopptak.kryssjekk [--fil ekstra.txt ...]

Bakgrunnen står i LAERDOM § 24. Frys-lesningen før v0.2.0 leste hver fil for seg. Hver fil var
konsistent med seg selv, så alle bestod — men `RESULTAT-PORT-v1.md` bar elleve størrelser som
ADDENDUM-10 og -11 hadde foreldet, mens abstract, manuskript og faktaark bar de nye. Avviket lå
mellom filene, ikke i noen av dem.

Regelen som håndheves: en foreldet verdi får bare stå når linjen (eller de tre linjene over) sier
hvilken versjon den tilhører — «før ADDENDUM-10», «Foreldet», «ikke regnet om».

Exit-koder: 0 ingen umerkede foreldede verdier · 1 avvik funnet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MERKER = ("før ADDENDUM", "Før ADDENDUM", "Foreldet", "foreldet", "ikke regnet om",
          "før A10", "eldre liste", "mot gjeldende",
          "før språkretting", "Før språkretting", "før spraakretting",
          "v1 (engelske bildetekster)")

#: En linje som daterer verdien selv, er merket. «4 av 24 er løftbare» er ikke en gjeldende
#: påstand når samme setning sier «er en påstand om 2026-09-20».
DATO = re.compile(r"\b20\d\d-\d\d-\d\d\b")

#: Seksjoner som HANDLER om de foreldede verdiene, og derfor må kunne sitere dem.
#: Navngitt framfor å løsne regelen for alle.
SEKSJONSUNNTAK = ("## 24 Frys-lesning per fil",)

#: Filer hvis oppgave ER å gjengi et innhentet utsagn. En slik fil må kunne sitere utsagnet,
#: ellers kan den ikke skrives. Navngitt, ikke gjettet.
FILUNNTAK = ("INNHENTET-",)

#: (størrelse, gjeldende verdi, foreldede skrivemåter, gjeldende skrivemåter)
#: En linje som bærer BEGGE er en sammenstilling («før | etter»), ikke et foreldet tall.
STØRRELSER: tuple[tuple[str, str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("H7-andel av ekte treff", "17 av 25 = 68 % (koder 1) · 12 av 19 = 63 % (koder 2)",
     (r"17 av 24", r"\(71 %\)", r"71 ?% er H7"), (r"17 av 25", r"68 ?%")),
    ("M1-passasje korrigert", "0,671 (koder 1) · 0,604 (koder 2)", (r"0,652",), (r"0,671",)),
    ("M1-streng korrigert", "0,667 (koder 1) · 0,599 (koder 2)", (r"0,649",), (r"0,667",)),
    ("M2 på leste ekte treff", "88,0 % = 22/25 (koder 1) · 31,6 % = 6/19 (koder 2)",
     (r"87,5 ?%(?=[^\n]*(M2|ekte treff))", r"21 av 24"), (r"88,0 ?%", r"22 av 25")),
    ("presisjon samlet", "16,7 % = 25/150 (koder 1) · 12,7 % = 19/150 (koder 2)",
     (r"16,0 ?% \(24", r"24 av 150", r"24/150"), (r"16,7 ?%", r"25 av 150", r"25/150")),
    ("presisjon energimodellering", "7,0 % (koder 1) · 1,8 % (koder 2)",
     (r"energimodellering 5,3", r"3/57"), (r"7,0 ?%", r"4/57")),
    ("løftbar andel", "5 av 25 = 20,0 % (koder 1) · 2 av 19 = 10,5 % (koder 2)",
     (r"4 av 24", r"20 av 24", r"83,3 ?%"), (r"5 av 25", r"20 av 25", r"20,0 ?%", r"80,0 ?%")),
    ("letekostnad per løftbart", "~30 dømte treff (koder 1) · ~75 (koder 2)",
     (r"37 dømte treff", r"ca\. 37 dømte"), (r"30 dømte treff", r"~30")),
    ("skalert løftbare i materialet", "~72 (koder 1) · ~29 (koder 2)",
     (r"58 løftbare",), (r"72 løftbare", r"\*\*72\*\*")),
    ("de 48 tvilstilfellene", "avgjort av ADDENDUM-10, tvilsmarkeringen står",
     (r"48 tvilstilfeller[^.]*uavgjort", r"tvilstilfeller i [^.]*uavgjort"), (r"avgjort",)),
    ("falsifiseringens dekning", "fire av fem løftbare prøvd; PS-031 ikke prøvd",
     (r"[Aa]lle fire løftbare",), (r"[Ff]ire av (de )?fem",)),
    ("antall kodere", "to, begge LLM-baserte", (r"\*\*Én koder\.\*\*",), (r"[Tt]o kodere",)),
    ("verksnivå, materialtilgang", "3 ÅPNE · 55 DELVIS · 42 LUKKEDE (v2, språkrettet)",
     (r"49 DELVIS", r"48 LUKKED", r"3 / 49 / 48", r"3 ÅPNE / 49", r"\| 3 \| 49 \| 48 \|"),
     (r"55 DELVIS", r"42 LUKKED", r"3 / 55 / 42", r"\| 3 \| 55 \| 42 \|")),
)


def er_laast(f: Path) -> bool:
    """Låste filer er daterte referat og kan ikke redigeres (PREREG-v1 + ADDENDUM-01..09).

    De flagges derfor ikke. At de inneholder utsagn som senere er innhentet, rettes med et
    datert korrigendum i EGEN fil, aldri inn i den låste — jf. ADDENDUM-11 §7-mønsteret.
    """
    from .vault import LOCKED_FILES
    return f.name in LOCKED_FILES


def merket(linjer: list[str], i: int) -> bool:
    """Er verdien merket med hvilken versjon den tilhører?

    Tre måter: på linjen selv, på en av de tre linjene over, eller ved at seksjonen
    den står i åpner med en peker («Foreldet av …»). Det siste gjelder daterte logger:
    § 16 i LAERDOM er referat fra 20. september og rettes ikke, men sier det selv.
    """
    for j in range(max(0, i - 3), i + 1):
        if any(m in linjer[j] for m in MERKER):
            return True
    if DATO.search(linjer[i]):
        return True
    for j in range(i, -1, -1):          # tilbake til seksjonsstart
        if linjer[j].startswith("## "):
            if any(linjer[j].startswith(s) for s in SEKSJONSUNNTAK):
                return True
            for k in range(j, min(j + 8, len(linjer))):
                if linjer[k].startswith(">") and any(m in linjer[k] for m in MERKER):
                    return True
            return False
    return False


def sjekk(filer: list[Path]) -> list[tuple[str, Path, int, str]]:
    avvik = []
    for f in filer:
        if not f.is_file():
            avvik.append(("FIL MANGLER", f, 0, ""))
            continue
        if any(f.name.startswith(x) for x in FILUNNTAK):
            continue
        laast = er_laast(f)
        linjer = f.read_text(encoding="utf-8", errors="replace").splitlines()
        for navn, _gjeldende, gamle, nye in STØRRELSER:
            for i, linje in enumerate(linjer):
                if not any(re.search(m, linje) for m in gamle):
                    continue
                if any(re.search(m, linje) for m in nye):   # sammenstilling før|etter
                    continue
                if merket(linjer, i):
                    continue
                avvik.append((("LÅST — krever korrigendum: " if laast else "") + navn,
                              f, i + 1, linje.strip()[:110]))
    return avvik


#: Filsettet oppdages, ikke listes. Bakgrunnen: kryssjekken slapp gjennom en foreldet verdi
#: fordi filen den sto i, ikke var i settet (LAERDOM § 28). Alt som er skrevet for en ekstern
#: leser, skal være med — addenda, beslutningsnotater, resultatnotat, manuskript, README,
#: deponeringsbeskrivelse, metode og oppgavetekst.
GLOBBER = ("ADDENDUM-*.md", "OPPGAVEN*.md", "docs/OPPGAVEN*.md", "docs/*.md",
           "docs/decisions/*.md", "README.md", "CITATION.cff", "PREREG-v1.md")


def dokumentsett(rot: Path) -> list[Path]:
    """Alle dokumenter skrevet for eksterne lesere, oppdaget fra disk."""
    ut: list[Path] = []
    for g in GLOBBER:
        ut.extend(sorted(rot.glob(g)))
    sett = {}
    for p in ut:
        if p.is_file():
            sett[p.resolve()] = p
    return list(sett.values())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rot", type=Path, default=Path.cwd())
    ap.add_argument("--fil", type=Path, action="append", default=[],
                    help="Ekstra fil utenfor repoet, f.eks. faktaarket.")
    args = ap.parse_args(argv)

    filer = dokumentsett(args.rot) + list(args.fil)

    print("Gjeldende verdier:")
    for navn, gjeldende, *_ in STØRRELSER:
        print(f"  {navn:32} {gjeldende}")
    print(f"\nLeser {len(filer)} filer mot hverandre.\n")

    avvik = sjekk(filer)
    laaste = [a for a in avvik if a[0].startswith("LÅST")]
    rettbare = [a for a in avvik if not a[0].startswith("LÅST")]
    for navn, f, nr, linje in rettbare:
        print(f"AVVIK  {navn}\n       {f.name}:{nr}  {linje}")
    if laaste:
        print("\nLåste filer — vises, rettes aldri i filen. Et utsagn som er innhentet, "
              "føres i et datert korrigendum i EGEN fil:")
        for navn, f, nr, linje in laaste:
            print(f"  {f.name}:{nr}  {navn.split(': ',1)[1]}\n      {linje}")
    print(f"\n{len(rettbare)} umerkede foreldede verdier i rettbare filer · "
          f"{len(laaste)} i låste filer")
    return 1 if rettbare else 0


if __name__ == "__main__":
    raise SystemExit(main())
