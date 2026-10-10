"""Kryssdokumentsjekk: samme størrelse skal ha samme verdi i alle filer som deponeres.

    python -m gjenopptak.kryssjekk [--fil ekstra.txt ...] [--mappe levende/ ...] [--frosset sendt/ ...]

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
          "v1 (engelske bildetekster)",
          # 28.09.2026: en datert rettelse som siterer det som sto, er merket.
          "ettet 28.09.2026", "ettet 10.10.2026")

#: En linje som daterer verdien selv, er merket. «4 av 24 er løftbare» er ikke en gjeldende
#: påstand når samme setning sier «er en påstand om 2026-09-20».
DATO = re.compile(r"\b20\d\d-\d\d-\d\d\b")

#: Seksjoner som HANDLER om de foreldede verdiene, og derfor må kunne sitere dem.
#: Navngitt framfor å løsne regelen for alle.
SEKSJONSUNNTAK = ("## 24 Frys-lesning per fil",)

#: Filer hvis oppgave ER å gjengi et innhentet utsagn. En slik fil må kunne sitere utsagnet,
#: ellers kan den ikke skrives. Navngitt, ikke gjettet.
FILUNNTAK = ("INNHENTET-", "KORRIGENDUM-")

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
    # 28.09.2026: «83,3 ?%» sto her uten emneord og ga falsk positiv på SAK-14s
    # Perseus-rate «75/90 = 83,3 %», som ikke har noe med løftbarhet å gjøre. En bar
    # prosentsats er ikke en signatur for en påstand. Kravet er nå at tallet står på
    # samme linje som emnet sitt.
    # 28.09.2026 (frys-lesningen): løftbar andel har AVKLARTE treff som nevner og oppgis sammen
    # med uavklart andel (ADDENDUM-05 § 4, classify.liftability.format_liftable). Kanon sto som
    # «2 av 19 = 10,5 %» for koder 2 — det er den uavklarte andelen. Regnet fra
    # data/port-presisjonssett-verdikter-koder2.jsonl over de 150 med utvalgstype «treff».
    ("løftbar andel", "5 av 25 = 20,0 % (koder 1, 0 uavklarte) · 2 av 17 avklarte = 11,8 % "
     "[3,3–34,3], uavklart 2 av 19 = 10,5 % (koder 2)",
     (r"4 av 24", r"20 av 24",
      r"83,3 ?%[^\n]{0,60}løftbar", r"løftbar[^\n]{0,60}83,3 ?%",
      r"løftbar[^\n]{0,40}2/19", r"løftbar[^\n]{0,60}2 av 19 = 10,5",
      r"2/19 = 10,5 ?% \|$"),
     (r"5 av 25", r"20 av 25", r"20,0 ?%", r"80,0 ?%", r"2 av 17", r"2/17", r"11,8 ?%")),
    # Samme regel for kandidatlista, regnet fra data/kjede/kandidat432/8-register.jsonl.
    ("løftbar andel, kandidatlista", "77 av 406 avklarte = 19,0 % [15,4–23,1] · uavklart 26 av 432 = 6,0 %",
     (r"77 av 432", r"77/432", r"17,8 ?%[^\n]{0,80}løftbar", r"løftbar[^\n]{0,80}17,8 ?%"),
     (r"77 av 406", r"77/406", r"19,0 ?%")),
    # κ = 0,812 har intervallet [0,697–0,906] (ADDENDUM-11 § 4). [0,712–0,917] hører til κ = 0,826
    # mot koder 1s FØRSTE lesning; avskriftsfeilen startet i ADDENDUM-21 og spredte seg (frys-lesningen
    # 28.09.2026). Signaturen krever 0,812 på samme linje, så 0,826-raden er ikke et avvik.
    ("κ-intervall for 0,812", "0,812 [0,697–0,906]; overlapp mot Opus ett kall 0,697–0,768",
     (r"0,812[^\n]{0,80}0,712[–-]0,917", r"0,712[–-]0,917[^\n]{0,80}0,812",
      r"overlapper i \**0,712[–-]0,768"),
     (r"0,697[–-]0,906", r"0,697[–-]0,768")),
    ("letekostnad per løftbart", "~30 dømte treff (koder 1) · ~75 (koder 2)",
     (r"37 dømte treff", r"ca\. 37 dømte"), (r"30 dømte treff", r"~30")),
    ("skalert løftbare i materialet", "~72 (koder 1) · ~29 (koder 2)",
     (r"58 løftbare",), (r"72 løftbare", r"\*\*72\*\*")),
    ("de 48 tvilstilfellene", "avgjort av ADDENDUM-10, tvilsmarkeringen står",
     (r"48 tvilstilfeller[^.]*uavgjort", r"tvilstilfeller i [^.]*uavgjort"), (r"avgjort",)),
    ("falsifiseringens dekning", "fire av fem løftbare prøvd; PS-031 ikke prøvd",
     (r"[Aa]lle fire løftbare",), (r"[Ff]ire av (de )?fem",)),
    # 28.09.2026: «to» er foreldet siden koder 4 (docs/METODE.md «Koder 4»).
    ("antall kodere", "tre på de 320, alle LLM-baserte (koder 1 og 2 Opus, koder 4 Fable 5.1); "
     "ingen menneskelig annotør",
     (r"\*\*Én koder\.\*\*", r"Designet har én koder", r"One coder read the sample"),
     (r"[Tt]re (LLM-)?kodere", r"[Kk]oder 4")),
    ("verksnivå, materialtilgang", "3 ÅPNE · 55 DELVIS · 42 LUKKEDE (v2, språkrettet)",
     (r"49 DELVIS", r"48 LUKKED", r"3 / 49 / 48", r"3 ÅPNE / 49", r"\| 3 \| 49 \| 48 \|"),
     (r"55 DELVIS", r"42 LUKKED", r"3 / 55 / 42", r"\| 3 \| 55 \| 42 \|")),
    # 07.10.2026: fase 4 (ADDENDUM-26) ble avbrutt 03.10.2026 før noen port var målt. Størrelsene under er det
    # som ble målt før avbruddet, hentet fra docs/RESULTAT-ADDENDUM-26.md § 0 («Hvor langt kjøringen kom»)
    # og ADDENDUM-26.md (§ 2, rammeraden). Ingen av dem har vært foreldet; signaturene fanger en annen verdi på
    # samme linje som emnet (fase 4 / håndskrift), ikke fase 3-tall på egne linjer.
    ("fase 4: rammerader", "807 (frames/frame-haandskrift-RAW.jsonl, sha256 6e444a08…; ADDENDUM-26 § 2)",
     (r"(?i:håndskrift|haandskrift)[^\n]{0,80}\b(?!807\b)\d{3} rader",), (r"\b807\b",)),
    ("fase 4: overlapp med tekstvitenskap-rammen", "799 av 807 (ADDENDUM-26 § 2)",
     (r"\b(?!799\b)\d{3} av 807\b",), (r"\b799 av 807\b",)),
    ("fase 4: trukne verk", "100 (RESULTAT-ADDENDUM-26 § 0, trekking 02.10.2026)",
     (r"(?i:fase 4|håndskrift)[^\n]{0,80}\b(?!100\b)\d{2,3} verk\b",), (r"\b100 verk\b",)),
    ("fase 4: tekstbiter", "31 031 (RESULTAT-ADDENDUM-26 § 0, `hent`/`tekstbiter`)",
     (r"(?i:fase 4|håndskrift)[^\n]{0,80}\b(?!31 031\b)\d{1,3}(?: \d{3})* tekstbiter",), (r"\b31 031\b",)),
    ("fase 4: dømte tekstbiter", "830 av 31 031 (RESULTAT-ADDENDUM-26 § 0, `dommer` delvis; ingen port målt)",
     (r"(?i:fase 4|håndskrift)[^\n]{0,80}\b(?!830\b)\d+ av 31 031\b",), (r"\b830 av 31 031\b",)),
    # 10.10.2026: differansen mellom Opus i én økt og Opus i ett kall ble kalt «ikke statistisk etablert» fordi to
    # separate intervaller overlappet. Den parede testen i reanalysen 03.10.2026 etablerte den
    # (docs/REANALYSE-2026-10-03.md b; docs/INNHENTET-2026-10-10-differansen-0812-0636.md).
    ("differansen 0,812 − 0,636", "0,177; paret bootstrap [0,044–0,323], verksklynget [0,057–0,318]",
     (r"ikke\W{0,4} statistisk etablert", r"not statistically established",
      r"øktformens bidrag er \**(mulig og umålt|ikke påvist)", r"resteffekt av øktformen er \**mulig"),
     (r"0[,.]177", r"0,044[–-]0,323", r"0[,.]057[–-]0[,.]318")),
    # 10.10.2026: grunnrate c) sto med [2,12–7,95], bygget av punktpresisjonen og Wilson-grensene for bomraten alene —
    # ikke et konfidensintervall. Reanalysen 03.10.2026 e) gir 3,42 %, verksklynget [1,3–7,5].
    ("grunnrate c), intervall", "3,42 %, verksklynget [1,3–7,5] % (stratifisert [1,3–7,2] %); sekundær størrelse",
     (r"2[,.]12[–-]7[,.]95",),
     # en linje som sier at det gamle intervallet var feil, er en rettelse og ikke en foreldet påstand
     (r"1[,.]3[–-]7[,.]5", r"1[,.]3[–-]7[,.]2", r"ikke et konfidensintervall", r"previous interval", r"erstatter")),
    # 10.10.2026: i leserstigen «samme regelfil, ett kall» er Sonnet 5 0,294 (n = 319). 0,297 er Sonnet med det
    # tynne utdraget (ADDENDUM-18 § 9). Signaturen krever stigen på samme linje.
    ("Sonnet 5 med full regelfil", "0,294 [0,126–0,455], n = 319 (ADDENDUM-19 § 7.1)",
     (r"Sonnet 0,297[^\n]{0,40}Opus 0,636", r"Haiku 0,031[^\n]{0,40}Sonnet 0,297"), (r"0,294",)),
    # 10.10.2026: MetaArXiv-preprinten zvc34 ble avvist 30.09.2026; gjeldende preprint er Preprints.org
    # 10.20944/preprints202610.0368.v1, publisert 07.10.2026 (docs/MASTER-PATCH-2026-10-07.md).
    ("preprintens status", "MetaArXiv zvc34 avvist 30.09.2026; Preprints.org 10.20944/preprints202610.0368.v1",
     (r"zvc34[^\n]{0,100}(pending|pre-moderering|under moderation)",
      r"(pending|pre-moderering)[^\n]{0,100}zvc34"),
     (r"avvist", r"rejected", r"preprints202610")),
)

#: Versjonerte dokumenter som er publisert eller sendt. Bytene endres ikke etter det (LAERDOM § 49-regelen):
#: en rettelse kommer i neste versjon, og det innhentede føres i en INNHENTET-fil. Av instruksfilene er bare
#: den høyeste versjonen levende.
VERSJONERT = (r"MANUSKRIPT-v[\d.]+(-UTKAST)?\.md", r"PREPRINT(-v\d+)?\.md", r"RELEASE-NOTES-v[\d.]+\.md")
INSTRUKS = re.compile(r"(?:GJENOPPTAK_)?INSTRUKSER[-_]v(\d+)\.(\d+)")

#: Kataloger gitt med --frosset: sendte og frosne filer utenfor repoet. Settes av main().
FROSNE_RØTTER: list[Path] = []


def er_laast(f: Path) -> bool:
    """Låste filer er daterte referat og kan ikke redigeres: PREREG-v1 og **alle** addenda.

    INSTRUKSER-v1.2 § 2 regner hvert `ADDENDUM-*.md` som låst når det er committet; `LOCKED_FILES`
    (01..09) er bare de som også har kjent sha256. Før 28.09.2026 flagget kryssjekken ADDENDUM-10+
    som rettbare, og et funn der kunne bare «rettes» ved å redigere en låst fil.

    De flagges derfor ikke. At de inneholder utsagn som senere er innhentet, rettes med et
    datert korrigendum i EGEN fil, aldri inn i den låste — jf. ADDENDUM-11 §7-mønsteret.
    """
    from .vault import LOCKED_FILES
    if f.name in LOCKED_FILES or re.fullmatch(r"ADDENDUM-\d+\.md", f.name):
        return True
    if any(re.fullmatch(m, f.name) for m in VERSJONERT):
        return True
    if any(rot == f.resolve() or rot in f.resolve().parents for rot in FROSNE_RØTTER):
        return True
    m = INSTRUKS.match(f.name)
    if m:       # en instruksversjon er levende bare så lenge ingen høyere finnes ved siden av
        andre = [INSTRUKS.match(p.name) for p in f.parent.iterdir()]
        return any(a and (int(a[1]), int(a[2])) > (int(m[1]), int(m[2])) for a in andre)
    # En påført MASTER-patch er et historisk dokument: den beskriver hva som ble skrevet inn i en
    # MASTER-versjon, og rettes ikke i ettertid. Funn der føres i korrigendum (28.09.2026).
    return f.name.startswith("MASTER-PATCH-")


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
    ap.add_argument("--mappe", type=Path, action="append", default=[],
                    help="Katalog utenfor repoet med levende dokumenter for eksterne lesere (.md, .txt, rekursivt).")
    ap.add_argument("--frosset", type=Path, action="append", default=[],
                    help="Katalog utenfor repoet med sendte, frosne dokumenter: funn der krever INNHENTET, ikke retting.")
    args = ap.parse_args(argv)

    FROSNE_RØTTER[:] = [d.resolve() for d in args.frosset]
    filer = dokumentsett(args.rot) + list(args.fil)
    for d in args.mappe + args.frosset:
        if not d.is_dir():      # en katalog som ikke kan leses, skal ikke se ut som en tom katalog
            print(f"MAPPE MANGLER ELLER KAN IKKE LESES: {d}", file=sys.stderr)
            return 1
        funnet = sorted(p for p in d.rglob("*") if p.is_file() and p.suffix.lower() in (".md", ".txt"))
        if not funnet:
            print(f"MAPPE UTEN LESBARE DOKUMENTER: {d}", file=sys.stderr)
            return 1
        filer += funnet

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
        print("\nLåste, versjonerte og frosne filer — vises, rettes aldri i filen. Et utsagn som er innhentet, "
              "føres i et datert korrigendum i EGEN fil:")
        for navn, f, nr, linje in laaste:
            print(f"  {f.name}:{nr}  {navn.split(': ',1)[1]}\n      {linje}")
    print(f"\n{len(rettbare)} umerkede foreldede verdier i rettbare filer · "
          f"{len(laaste)} i låste filer")
    return 1 if rettbare else 0


if __name__ == "__main__":
    raise SystemExit(main())
