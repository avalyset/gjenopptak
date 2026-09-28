# SAK-11 — stoppet før kriteriet. Scenariosettet finnes ikke, og det var en `[V]` triagen ikke navnga.

**28.09.2026. Ingen kriteriefil låst, ingen terskel beregnet.** Saken stanser på oppdragets steg 3 —
*«Reproduser kildens egne tall først. Klarer du ikke det, STOPP saken og før hvorfor»* — og grunnen
er ført her.

**Sak:** `W4206850274`, passasje **AL-2516**, feltet energimodellering, klasse **H5 regnekraft**.
**Verket:** Michael Bynum, Andrea Staid, Bryan Arguello, Anya Castillo, Bernard Knueven, Carl D.
Laird, «Proactive Operations and Investment Planning via Stochastic Optimization to Enhance Power
Systems Extreme Weather Resilience», *Journal of Infrastructure Systems* **27**(2), 2021.
DOI `10.1061/(asce)is.1943-555x.0000603`, Sandia-rapport SAND2018-9647J. Åpen gjennom OSTI.

## Det ugjorte, ordrett fra artikkelen

> «Even for a small test network such as case30, including all possible scenarios in the stochastic
> programming formulation is intractable. On average, the scenarios for case30 contained 7
> transmission line outages. **Over 22 million scenarios would be necessary to consider every
> combination of 7 outages.** To demonstrate that only a small fraction of all possible scenarios is
> needed to obtain a high quality solution, a cross validation case study was performed with case30.»

Hindringen er navngitt i samme setning: beregningsmessig umulighet. Klassen er H5.

## `[V]` 1 — case30 er offentlig. **Holder, og bekrefter artikkelens eget tall.**

Slått opp **28.09.2026**: `https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case30.m`,
HTTP 200, 4 999 B. Filen gir **30 busser, 41 transmisjonslinjer, 6 generatorer** — som stemmer med
artikkelens tabell 1.

Og da lar artikkelens eget tall seg kontrollere: **C(41, 7) = 22 481 940.** «Over 22 million» er
korrekt, og det er nå verifisert mot nettverket i stedet for tatt på tro. C(40,7) = 18,6 mill. og
C(42,7) = 27,0 mill., så tallet festes til nøyaktig 41 linjer.

## `[V]` som triagen ikke navnga — og som binder: **scenariosettet**

Triagen skrev: «Ressurs: case30 er offentlig (MATPOWER) **[V]**, formuleringen står i artikkelen.»
Begge holder. Men kriteriets steg (1) er *«reproduser artikkelens utvalgsresultat»*, og det krever en
tredje ressurs som triagen ikke førte opp: **de 100 scenarioene**. Den finnes ikke. Tre uavhengige
grunner, hver av dem tilstrekkelig:

**(a) Fordelingen er navngitt, men ikke parametrisert.** Artikkelen sier at antallet linjeutfall per
scenario er trukket fra en negativ binomialfordeling og linjene fra en uniform fordeling. **Ingen av
fordelingens parametere er oppgitt** — verken *r*, *p*, forventning eller varians — og ordet «seed»
forekommer **0 ganger** i artikkelen. Scenarioene kan derfor ikke genereres på nytt.

**(b) Kryssvalideringsresultatet finnes bare som en figur.** § 4.1 rapporterer utfallet for 10, 30 og
100 scenarioer i **figur 6**, en kurveplott. Det finnes **ingen tabell** med tallene bak, og figurens
tekstlag er OCR-grøt. Det er ingenting å reprodusere *mot*.

**(c) Ingen kode og ingen data er deponert.** Artikkelen har **ingen datatilgjengelighetserklæring**
(0 treff), nevner ingen repositorium (0 treff på github/gitlab/zenodo/osf/figshare), og **Crossref
registrerer ingen relasjoner** for DOI-en — ingen komponent, intet datasett. GitHub-søk på
forfatterlaget og på emnet ga **0 treff**. Modellen er bygget i Pyomo og løst med **CPLEX**, en
kommersiell løser; ingen MILP-løser i det hele tatt finnes på maskinen (`cplex`, `gurobi_cl`,
`glpsol`, `cbc`, `highs`, `scip` — alle fraværende, og heller ikke `pyomo`, `pulp`, `mip`, `highspy`).

**Det følger at steg 3 ikke kan utføres.** Å trekke mine egne 100 scenarioer ville gitt en annen
studie: herdingsbeslutningene ville blitt sammenlignet mot en figur jeg ikke kan lese tall av, med
scenarioer forfatterne ikke brukte. Det er samme sirkel som i SAK-08, og den tas ikke.

## Hva det ugjorte ville kostet — målt, ikke gjettet

Selv om scenariosettet hadde vært publisert, er full enumerering ikke «treg». Den **passer ikke på
maskinen.** Artikkelens tabell 2 oppgir problemstørrelsen for case30 med 100 scenarioer, og
andrestegsvariablene skalerer lineært med antall scenarioer:

| | 100 scenarioer (artikkelens tall) | per scenario | full enumerering, 22 481 940 scenarioer |
|---|---|---|---|
| kontinuerlige variabler | 14 579 | 145,8 | **≈ 3,28 · 10⁹** |
| likhetsbeskrankninger | 10 762 | 107,6 | **≈ 2,42 · 10⁹** |
| ulikhetsbeskrankninger | 11 613 | 116,1 | **≈ 2,61 · 10⁹** |
| **rader i alt** | 22 375 | 223,8 | **≈ 5,03 · 10⁹** |

Skaleringsfaktoren er **224 819**. Tallene er **lineære skaleringer med tre signifikante siffer**, ikke eksakte opptellinger: tabell 2 gir fem siffer, og per-scenario-verdiene er de tallene delt på 100. Et tisifret produkt ville latet som om presisjonen er ti siffer. Bare koeffisientmatrisen, med et nøkternt anslag på 3–6 ikke-nuller
per rad og 12 B per ikke-null, blir **0,2–0,4 TB** — mot **11 GB** ledig diskplass på maskinen, altså
**minst 16 ganger for stort** før løseren har allokert en byte til arbeidsminne eller en eneste
LP-relaksasjon i forgreningstreet. Terskelen i triagen var «løsbar innen 48 t lokalt». Den er ikke
det, og nå er det et regnestykke og ikke et inntrykk.

**Merk hva det betyr for klassen:** H5 er riktig, og hindringen er **ikke løftbar av regnekraften i
en bærbar maskin** — ikke i 2020 og ikke i 2026. Det er den ene av de fire sakene der hindringen står
uendret av grunner som ikke har med tilgang å gjøre.

## Det forfatterne selv gjorde, som er verdt å føre

Artikkelen gjør ikke bare en unnskyldning for utvalget — den **måler at utvalget holder**. Sammendraget
sier at modellen gir «a near-optimal solution (with respect to out-of-sample performance) considering
**less than 0.001 %** of all possible outage realizations», og § 4.1 viser med ut-av-utvalg-
kryssvalidering at 10, 30 og 100 scenarioer nærmer seg «True Scenarios»-kurven.

100 av 22 481 940 er **0,000445 %** — under 0,001 %, som påstått. Det er den ene delen av artikkelens
utvalgsresultat som *lar seg* kontrollere uten scenariosettet, og den holder.

Det gjør det ugjorte til noe annet enn en mangel: forfatterne argumenterer for at full enumerering er
**unødvendig**, og de gir belegg. Det er samme form som SAK-09b, der omgåelsen alt oppnådde det det
ugjorte skulle oppnå — men her kan vi ikke etterprøve belegget, bare påstandens aritmetikk.

## En rute jeg ikke fikk lest, ført som uavklart

**OSTI var uoppnåelig fra maskinen.** Tre forsøk mot `www.osti.gov` endte i tilkoblingsfeil
(`curl (28)`, 75 s tidsavbrudd hver gang) — ikke 403, men ingen forbindelse. Om OSTI-posten har
tilleggsfiler med scenarioer eller kode, er derfor **ikke avklart av meg**. Crossrefs tomme
relasjonsliste og de tomme GitHub-søkene taler mot, men de erstatter ikke oppslaget. Selve artikkelen
ble hentet frosset fra `osti.gov` (status 200, sha256 `11ec80a5422581791da4c1c7c63792777b33fd01389810e4bdbdce644498c93a`) da rammen ble laget.

## Klassifisering

| | før | nå |
|---|---|---|
| kodet klasse fra teksten | `H5` | uendret — teksten har ikke endret seg |
| datert vurdering (ADR-0010) | — | **H8**, `loftbar: nei`, 28.09.2026 — utløser |

H8 fordi det som stanser saken, er **tilgang til materialet** (scenariosettet), ikke hindringen selv.
Ført som **utløser**, som SAK-08: publiserer forfatterne scenarioene eller koden, kan saken tas opp
— men da møter den H5-en, og den er målt til 0,2–0,4 TB koeffisientmatrise.

## Hva som ikke ble gjort, og bevisst ikke ble gjort

* **Ingen e-post til noen.** Ingen forespørsel til Sandia eller forfatterne om scenariosettet, selv om
  det er den åpenbare veien videre. Eierens valg, ikke mitt.
* **Ingen egne scenarioer trukket** for å «kunne kjøre noe». Det ville byttet ut kildens tall med mine.
* **Ingen løser installert.** CPLEX er kommersiell; en åpen erstatning ville ikke vært verktøyet
  artikkelen brukte, og steg 3 ville fortsatt vært umulig.
* **Ingen kriteriefil låst**, og ingen kanon-bundle utløst.
* **Ingen nye OpenAlex-kreditter.** Rammeopplysningene er lest av den frosne rammelisten.
