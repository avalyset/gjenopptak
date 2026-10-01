# ADR-0013 — Opphevelse: definisjon, tre vilkår

**Dato:** 2026-09-28. **Status:** besluttet. **Gjelder fra:** før fase 3-sakene.
**Bakgrunn:** seks gjennomførte saker, **null opphevelser**. Vilkårene under er ikke utledet av teori;
de er de tre stedene de seks sakene faktisk stanset.

## Problemet ADR-en løser

Hypotesens ledd 2 er at «en del av hindringene er opphevet». Ordet **opphevet** har til nå vært brukt
uten definisjon, og seks saker viste at det dekker tre utfall som ikke skal føres likt:

* en sak der **spørsmålet ikke kan stilles** fordi inndataen ikke finnes,
* en sak der **kildens tall ikke kan reproduseres**, så et nytt tall ville erstattet dem og ikke prøvd dem,
* en sak der **terskelen ikke ble nådd**.

Uten skillet blir alle tre «ikke opphevet», og registeret mister det som betyr mest: **hvorfor**. Én av
dem kan endre seg i morgen, én kan aldri endre seg, og én er et målt negativt svar.

## Beslutning: en hindring er opphevet når og bare når alle tre vilkår er oppfylt

### Vilkår 1 — tilgang: inndataen det ugjorte krever, finnes og er hentbar

Det ugjorte har en inndata. Finnes den ikke, eller kan den ikke hentes, er spørsmålet **ikke besvart
negativt — det er ustilt**. Klassen er **H8**, og den føres med **varighet**:

* **varig** når sperren er av et slag som ikke skal falle — samtykke, personvern, tapt materiale;
* **utløser** når sperren bare er at ingen har publisert ennå.

Vilkåret oppfylles av tilgangen, ikke av vår innsats. Vi spør ikke forfattere om materiale
(`docs/INSTRUKSER-v1.2.md` § 2), så et «nei» fra oss er aldri et «nei» fra verden.

### Vilkår 2 — reproduksjon: kildens egne tall lar seg reprodusere først

Før noe nytt beregnes, må kildens publiserte tall kunne reproduseres fra det som er hentbart. Uten det
måler et nytt tall **en ny studie**, ikke om hindringen er opphevet: sammenligningsgrunnlaget mangler,
og en avvikende konklusjon kan like godt komme av vår implementasjon som av det ugjorte.

Kravet er **PS-246-mønsteret**, og det er strengt: reprodusert betyr **samme tall**, ikke samme retning.

### Vilkår 3 — terskel: et kriterium låst før beregning er nådd

Kriteriet skal ligge i egen fil med sha256, låsecommit og kanon-bundle **før** noe beregnes, og
tersklene flyttes ikke etterpå. 89 % mot en terskel på 90 % er **ikke opphevet**. Intervallet oppgis,
men avgjørelsen følger det målte forholdet.

Er kriteriet ikke kjørbart som skrevet — for eksempel en konjunktiv port der det ene leddet ikke kan
måles (LAERDOM § 37) — er utfallet **ikke opphevet**, og svakheten føres i kriteriet, ikke bortforklart.

## Det som IKKE er et vilkår, men alltid skal rapporteres

**Om løftet har en konsekvens.** En hindring kan være løftbar og løftet **konsekvensløst**: i SAK-09b
ga tvungen partisjonering nøyaktig den blokkstrukturen avhandlingen alt hadde. Det er et annet funn enn
en hindring som ikke kan løftes. Dimensjonen er **ortogonal** på de tre vilkårene og har tre verdier:
`konsekvens ja` · `konsekvens nei` · `ikke målt`.

**Om middelet var det navngitte.** Triagen navngir et middel. Mangler middelet det som trengs, er
utfallet «**ikke opphevet av det navngitte middelet**» — ikke «ikke løftbar». Det første er en
opplysning om et verktøy, det andre om verden.

## De seks sakene mappet inn som instanser

*(Rettet 30.09.2026, frys-lesning 4: overskriften sa «De fem sakene»; tabellen har seks, med PS-246.)*

| sak | vilkår 1 tilgang | vilkår 2 reproduksjon | vilkår 3 terskel | utfall | konsekvens |
|---|---|---|---|---|---|
| **PS-246** `W2551114598` | **ja** | **ja** — avhandlingens FC > θS i nøyaktig de fire navngitte horisontene reprodusert (implementasjonen først verifisert mot Saxton & Rawls tabell 3, tolv av tolv rader) | **nei** — 2 av 4 horisonter, begge innenfor ±0,02 | ikke opphevet | ikke målt |
| **SAK-14** `W2474595476` | **ja** — Perseus og Scaife åpne | **ja** — den franske gjengivelsen svarer ledd for ledd til gresken | **nei** — 79/90 = 87,8 % mot 90 % | ikke opphevet | ikke målt |
| **SAK-09b** `W7133020405` | **ja** — matrisene i tekstlaget | **ja** — tabell D.1 12 av 12, total feil 14 i to implementasjoner | **nei** — middelet mangler mekanismen | ikke opphevet av det navngitte middelet | **nei** — blokkstrukturen er den avhandlingen alt hadde |
| **SAK-09c** `W7133020405` | **NEI** — profilene holdt tilbake av samtykke | ikke nådd | ikke nådd | **H8 varig** | ikke målt |
| **SAK-08** `W2784603861` | **NEI** — modellkoden ikke funnet i seks sjekkede ruter, forlagets tilleggsmateriale uavklart (HTTP 403) *(rettet 30.09.2026: sto «ikke deponert», jf. SAK-08 LUKKET 28.09)* | ikke nådd | ikke nådd | **H8 utløser** | ikke målt |
| **SAK-11** `W4206850274` | delvis — case30 åpen, scenariosettet ikke | **NEI** — fordelingens parametere aldri oppgitt, resultatet bare som figur | ikke nådd | **stoppet på vilkår 2** | ikke målt |

**Mønsteret vilkårene gjør synlig:** tre saker stanset på **vilkår 1 eller 2**, altså på tilgang og
reproduserbarhet, og bare tre kom fram til **vilkår 3**. Uten definisjonen ville alle seks stått som
«ikke opphevet», og sporet hadde mistet at **porten ikke er det som siler — tilgangen er**.

## Følger for registeret og for fase 3

1. **`loftbarhet`-raden skal bære hvilket vilkår som stanset saken.** Feltet er en datert vurdering
   (ADR-0010); vilkårsnummeret hører i `tabellversjon` til skjemaet får et eget felt.
2. **H8 skal alltid ha varighet.** «H8» alene skiller ikke et samtykke fra en manglende deponering.
3. **Et kriterium låses ikke for en sak som kan stanse på vilkår 1.** `[V]`-sjekken kommer først;
   ellers får saken en låsecommit og en kanon-bundle som later som om den ble prøvd.
4. **Fase 3 rapporterer vilkårsfordelingen**, ikke bare utfallsfordelingen. Med seks saker er den
   **2–1–3** på vilkår 1 / vilkår 2 / vilkår 3 *(rettet 28.09.2026, sto «3–1–2»; tabellen over gir
   SAK-09c og SAK-08 på vilkår 1, SAK-11 på vilkår 2, PS-246, SAK-14 og SAK-09b på vilkår 3)*, og det er den mest informative enkeltlinjen sporet har.
   *(Merknad 30.09.2026: fase 3-kjøringen i ADDENDUM-25 hadde ingen sakbehandling — den målte deteksjon, ikke
   opphevelse. Vilkårsfordelingen for fase 3 finnes derfor ikke før saker tas fra arbeidslista.)*

## Alternativer som ble forkastet

* **Ett vilkår («terskelen nådd»).** Gjør tre svært ulike utfall til samme tall. Fem av seks saker
  ville stått som ren fiasko, og de tre grunnene ville forsvunnet.
* **Fire vilkår, med «konsekvens» som det fjerde.** Konsekvens er **ortogonal**: en hindring kan løftes
  konsekvensløst, og et vilkår som blander opphevelse med interesse gjør begge uklare.
* **La «opphevet» bety «løftbar i prinsippet».** Det er PREREG § 5s klassetabell, som alt finnes. Denne
  ADR-en handler om en **gjennomført** sak, ikke om en klassifisering.

*Rettet 28.09.2026 (frys-lesningen før v0.4.0): vilkårsfordelingen i følge 4 sto som 3–1–2; PS-246s
vilkår 2 sto som «alle tolv rader i kildens tabell 3», som er verifikasjonen av implementasjonen mot
Saxton & Rawls, ikke reproduksjon av kildens (avhandlingens) egne tall.*
