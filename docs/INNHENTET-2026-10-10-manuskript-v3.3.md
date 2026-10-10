# INNHENTET 2026-10-10 — manuskript v3.3 (innsendt): tre steder som rettes i revisjonen

**`MANUSKRIPT-v3.3.md` og `MANUSKRIPT-v3.3.docx` er uendret.** De ble sendt til *Scientometrics* 03.10.2026, og
en innsendt fil rettes ikke. Den uavhengige kontrollen av v0.6.0-utkastet 10.10.2026 fant tre steder der teksten
sier noe annet enn kilden, eller mangler kilden. Ingen av dem endrer et tall eller en konklusjon. De føres her,
med ordlyden som skal inn når manuskriptet revideres.

De samme tre stedene står i v3.1 og v3.2 (i `manuskript-tidligere.zip`). v3.2 er preprinten
10.20944/preprints202610.0368.v1 og kan heller ikke endres; rettingen der kommer med en ny preprintversjon.

## 1 Klasse-κ 0,722 er regnet over alle 320 passasjer, ikke blant treffene

| | |
|---|---|
| **Står** (v3.3 linje 232; v3.1 og v3.2 linje 216–217) | «Agreement on the class, among passages both coders call hits, is lower (coders 1–2: κ 0.722).» |
| **Kilden sier** (`docs/METODE.md` linje 74–75) | «Samlet klasse-κ over alle klasser samtidig: 0,722», rå enighet 85,6 %, n = 320 |
| **Regnet på nytt 10.10.2026** | 0,7216 over alle 320 passasjer, rå enighet 85,6 % |

Tallet er riktig. Beskrivelsen av hva det er regnet over, er feil. Regnet av de to koderfilene alene
(`presisjonssett/port-presisjonssett-ADDENDUM10.jsonl` og `port-presisjonssett-verdikter-koder2.jsonl`, feltet
`min_klasse`), som METODE sier. Neste setning i manuskriptet peker selv på det riktige utvalget: de svakeste
grensene er N3 og N2, og de er ikke-treff-klasser som ikke kan forekomme blant passasjer begge koder som treff.

Blant de 30 passasjene begge koderne kaller treff, gir samme regning 0,7315 (rå enighet 86,7 %). Det er en
kontrollregning gjort for denne filen, ikke et preregistrert mål, og tallet står ikke i manuskriptet. Den viser at
beskrivelsen ville svart til et annet tall enn det som er oppgitt.

**Rettet ordlyd for revisjonen:**

> Agreement on the class, computed over all 320 passages and all classes at once, is lower (coders 1–2: κ 0.722).

## 2 Sitatet i innledningen mangler kilde

| | |
|---|---|
| **Står** (v3.3 linje 37; v3.1 og v3.2 linje 36) | «"we were unable to code all data about discharge diagnosis and insurance status"», uten kildeangivelse |
| **Kilden** | Takeuchi, S., Funakoshi, H., Nakashima, Y., Homma, Y., Takahashi, J., & Shiga, T. (2019). Unique characteristics of frequent presenters to the emergency department in a Japanese population: a retrospective analysis. *Acute Medicine & Surgery*, *6*(2), 145–151. https://doi.org/10.1002/ams2.395 (PMC6442527) |
| **Setningen i kilden** (Discussion) | «We were unable to code all data about discharge diagnosis and insurance status, which also leads to selection bias.» |

Sitatet er ordrett, bortsett fra liten forbokstav. Verket er **ikke** blant de 200 trukne verkene. Det ble funnet
i frasesøket etter kontrollartikler (ADDENDUM-03 § 3) og er ført i `logs/leste-kontrollkandidater.json` med kilde
`H1H4-kontrollsok-dogn2-H1`; verk i den listen er utelatt fra trekkingen. Setningen er setning 238 i
rørledningstesten (`logs/pipeline-test/sentences-PIPELINETEST.jsonl`, `PMC6442527:238`). Fullteksten ligger på Vault,
`fulltext/cs-jats-PMC6442527-5b378c4c0acd.json`, sha256
`5b378c4c0acd57682ee0d9156430a6f2b34688379792510a00b238830fcbf55c`, og deponeres ikke. Verket er lisensiert
CC BY-NC-ND 4.0; et sitat på 77 tegn med kildeangivelse hviler på sitatretten.

Faktasjekken av manuskript v2 fant at sitatet stemte med kilden og noterte at manuskriptet ikke oppga den
(`manuskript/faktasjekk-v2/del-1.jsonl` på Vault). Faktasjekken av v3 førte sitatet som «STEMMER»
(`FAKTASJEKK-MANUSKRIPT-v3-2026-10-03.md` punkt 15). Ingen av dem førte til at kilden kom inn.

**Rettet ordlyd for revisjonen:**

> For example: "we were unable to code all data about discharge diagnosis and insurance status" (Takeuchi et al.,
> 2019).

med denne oppføringen i referanselista:

> Takeuchi, S., Funakoshi, H., Nakashima, Y., Homma, Y., Takahashi, J., & Shiga, T. (2019). Unique characteristics
> of frequent presenters to the emergency department in a Japanese population: A retrospective analysis. *Acute
> Medicine & Surgery*, *6*(2), 145–151. https://doi.org/10.1002/ams2.395

## 3 Tallmanifestet dekker 45 maskinleste verdier, ikke hvert tall

| | |
|---|---|
| **Står** (v3.3 linje 405–406; v3.1 og v3.2 linje 383–384) | «… and a number manifest that links each number in this paper to its file, hash and generating script.» |
| **Depositumet har** | `TALLMANIFEST.md`: 45 verdier lest maskinelt ut av kildefilene, hver med fil, sha256 og skript. Det er generert for manuskript v3.1 og ikke på nytt for v3.2 eller v3.3 |
| **De øvrige tallene** | alle 144 tall- og påstandspunkter i manuskript v3 er kontrollert mot kilde i `FAKTASJEKK-MANUSKRIPT-v3-2026-10-03.md` (i `faktasjekk-manuskript.zip`), punkt for punkt, men uten sha256 og skript for hvert |

Påstanden er for sterk. Manifestet knytter 45 verdier til fil, sha256 og skript; resten er faktasjekket, ikke
manifestført.

**Rettet ordlyd for revisjonen:**

> … and a number manifest that links 45 machine-read values in this paper to their file, hash and generating script;
> the remaining figures are checked against their sources in the fact-check file.

Alternativet er å generere manifestet på nytt for den reviderte versjonen og utvide det til alle tallpunktene. Da
kan setningen stå.

## 4 Hva som ikke endres

Ingen måling, ingen κ-verdi, ingen feltrate og ingen konklusjon. `METODE.md` og `MANUSKRIPT-FAKTA-2026-09-28.md`
beskriver 0,722 riktig og er ikke rørt for dette punktet.
