# SAK-09b — resultat. Hindringen er **ikke opphevet av det navngitte middelet**.

**Gjennomført 27.09.2026.** Sak: Aragao 2018, `W7133020405`, passasje **AL-0852**, klasse
**H5 verktøygrense**. Kriteriet låst før beregning: [`KRITERIUM.md`](KRITERIUM.md), sha256
`2fa587a056ce7094531496fe77460510d822f3fb21cf4047d58eec40e09ce141`, låsecommit `feb0c31`,
kanon-bundle `gjenopptak-2026-09-27-feb0c3102504.bundle` (sha256 `d298debb…`, 154 commits).

**Kortsvaret, i tre deler.** Reproduksjonen av avhandlingens egne tall **bestod fullstendig**, i to
uavhengige implementasjoner. Porten **falt**: R-pakken `blockmodeling` 1.1.8 har ingen mekanisme for
å tvinge mellomnivåets rad- og kolonnepartisjon like, åtte år etter at avhandlingen skrev at Pajek
ikke har det. Og forskningsresultatet er at **det ikke hadde gjort noen forskjell**: avhandlingens
egen omgåelse *er* en tvungen løsning, og en formålsbygget tvungen kjøring finner ingenting bedre.

---

## Steg 3 — kildens egne tall, reprodusert eksakt

Kriteriets presisering 2 krevde to delkontroller før noe annet. Begge bestod.

### Nabomatrisene: tabell D.1, 12 av 12 verdier eksakt

De fem 34 × 34-binærmatrisene ligger i PDF-ens tekstlag (figur D.1–D.4 på s. 241–243, figur E.1 på
s. 251) og ble lest med `pdftotext -layout`.

| nettverk | bånd | fasit | snittgrad | fasit | tetthet | fasit |
|---|---|---|---|---|---|---|
| Prosjekt A | **148** | 148 | **4,353** | 4,353 | **0,132** | 0,132 |
| Prosjekt B | **146** | 146 | **4,294** | 4,294 | **0,130** | 0,130 |
| Prosjekt C | **133** | 133 | **3,912** | 3,912 | **0,119** | 0,119 |
| samlet case | **249** | 249 | **7,324** | 7,324 | **0,222** | 0,222 |

**0 avvik.** Matrisene er avhandlingens. Grunnraten bak tallene: snittgrad = bånd / 34, tetthet =
bånd / (34 · 33), altså rettet nettverk uten symmetrisering.

### Beskrankningene: 109, rekonstruert fra en avkuttet liste

Vedlegg H oppgir syntaksen og reglene, men listen er «abbreviated for the sake of space savings»
med ellipser. Reglene rekonstruerer til:

| form | hva den gjør | antall |
|---|---|---|
| `1 100 y z` | fester hver av de 13 aktivitetene til sin funksjonelle klynge | 13 |
| `2 100 y z` | utelukker de 9 systemene fra de fire faktorklyngene (9–12) | 36 |
| `2 100 y z` | utelukker de 12 faktorene fra de fire systemklyngene (5–8) | 48 |
| `6 50 y z` | grense for antall noder per klynge | 12 |
| | **sum** | **109** |

Avhandlingen oppgir **109**. Rekonstruksjonen er dermed verifisert, ikke antatt.

### Total feil 14, reprodusert i to implementasjoner

Partisjonen er ikke oppgitt som liste i avhandlingen, men den er **gjenfinnbar**: figur 8.3s
akserekkefølge og figur 8.4s reduserte graf gir de samme 12 klyngene, og de stemmer med prosaen i
§ 8.6 («buildings/civil structures form a complete block with structural civil works, and a null
block with electro-mechanical works» — blokk (3,8) = `com`, (4,8) = null, som bildematrisen viser).

| | min implementasjon | `blockmodeling` 1.1.8 | figur 8.2 |
|---|---|---|---|
| blokk (1,7), type `reg` | **3** | **3** | 3 |
| blokk (1,8), type `com` | **2** | **2** | 2 |
| de 32 tre-modus-blokkene | **14** | **14** | «the total error is 14» |
| alle 144 blokkene | 163 | 163 | — |

**Feilfunksjonen er ikke antatt — den er utledet av avhandlingens egne blokkfeil.** De fire
variantene fra litteraturen (nullrad-tall, nullkolonne-tall, maks, min) gir alle **1** for blokk
(1,7), mens figuren oppgir **3**. Blokken har én nullrad over tre kolonner, og definisjonen som
treffer, er at **en nullrad koster blokkens kolonnetall og en nullkolonne radtallet**. Den
definisjonen ble deretter bekreftet uavhengig: R-pakken gir samme tall i hver enkelt celle, og samme
163 over alle 144 blokker.

**Og et funn som følger av det:** avhandlingens «total error 14» teller **bare de 32 tre-modus-
blokkene**, ikke alle 144. Over alle blokkene er feilen 163. Det står ikke i avhandlingen, og uten
det tallet kan ingen etterprøve 14.

### 𝑀, og en regnefeil i avhandlingen

𝑀 etter ligning 8.2 er `[[M_ij, 0], [0, M_jk]]` med i = 12 faktorer, j = 13 aktiviteter
(mellomnivået), k = 9 systemer. Bygget gir **25 rader × 22 kolonner** og **151 bånd**, fordelt som
109 faktor→aktivitet og 42 aktivitet→system — som stemmer med båndfordelingen i undersøkelsens
matrise.

Avhandlingen skriver at 𝑀 har «𝑖 + 𝑗 rows and **𝑖 + 𝑘** columns». Blokkformen gir 𝑗 + 𝑘 = **22**
kolonner, ikke 𝑖 + 𝑘 = 21. **Det er en feil i avhandlingens beskrivelse av sin egen matrise**, og den
er liten, men den er der.

## Steg 4 — porten, og den faller

Kriteriet: *kjør med tvungen partisjonering; opphevet hvis kjøringen gir like partisjoner.*
Middelet var navngitt i presisering 5: **R-pakken `blockmodeling`, versjon ≥ 0.3.1.**

### Pakken ble kjørt, og gjør det samme Pajek gjorde

To-modus generalisert blokkmodellering av 𝑀 i `blockmodeling` 1.1.8: `k = c(8, 8)`,
`approaches = "bin"`, `blocks = c("nul","com","reg","rre")`, 50 tilfeldige starter, frø 734248.

* **11 løsninger med minimal feil = 0.**
* Aktivitetenes **radpartisjon**: `6 6 2 6 6 2 2 1 6 6 5 2 5`
* Aktivitetenes **kolonnepartisjon**: `13 13 12 9 12 13 16 11 9 12 12 13 12`
* **Like mengdepartisjoner: nei.** Ikke engang samme antall grupper.

Det er avhandlingens egen bekymring, verifisert i et annet verktøy. Og den er kvantifisert i min egen
implementasjon også: over **120 tilfeldige starter ble mellomnivåets to partisjoner like av seg selv
i 0 av 120 tilfeller.** Det skjer ikke tilfeldig.

### Pakken har ingen mekanisme for å tvinge dem like

Dette er porten, og den ble avgjort mot dokumentasjonen, ikke mot funksjonsnavn. Hele
argumentlisten til `optParC`/`critFunC` ble gjennomgått, og de fire kandidatene er alle noe annet:

| argument | hva det faktisk gjør | tvinger det likhet? |
|---|---|---|
| `fixClusters` | «Clusters to be fixed» — fryser hele klynger mot endring | nei |
| `exchageClusters` | matrise som sier hvilke klynger noder kan flyttes mellom — kategoriskillet, altså avhandlingens 109 beskrankninger | nei |
| `sameIM` | «Should we demand the same blockmodel image for all relations» — samme *bilde* på tvers av relasjoner | nei |
| `minUnitsRowCluster` / `maxUnitsRowCluster` | klyngestørrelsesgrenser — avhandlingens «høyst fire per klynge» | nei |

**Ingen av dem binder en radpartisjon til en kolonnepartisjon.** Åtte år etter avhandlingen har det
navngitte alternativet nøyaktig den grensen Pajek hadde.

**Hindringen er derfor ikke opphevet av det navngitte middelet.** Det er ikke en verktøysvikt etter
presisering 5 — pakken kjørte, og svarte. Det er en målt egenskap ved verktøyet.

### Hva som *kan* tvinge det, og hvorfor det ikke er middelet kriteriet satte

En formålsbygget implementasjon tvinger det uten videre: én klyngevektor for mellomnivået brukt på
begge akser gir **120 av 120 kjøringer med eksakt like mengdepartisjoner**. Men det er et verktøy
skrevet for anledningen, ikke R-pakken kriteriet navnga, og det **erstatter ikke porten**.

## Forskningsresultatet, uten terskel — og det er det som betyr noe

**Avhandlingens omgåelse er selv en tvungen løsning.** Den augmenterte én-modus-matrisen har bare
**én** partisjon av de 34 nodene. Mellomnivåets to representasjoner i 𝑀 — rad 13–25 og kolonne 1–13 —
faller da sammen i én, og likheten er garantert per konstruksjon. Det er nettopp det 𝑀 ikke kunne gi.

Og den løsningen er bedre enn noe søket finner:

| kjøring | beste totale feil | like partisjoner |
|---|---|---|
| avhandlingens partisjon (augmentert rute) | **14** | ja, per konstruksjon |
| tvungent søk **startet fra** avhandlingens partisjon | **14** — ingen forbedring funnet | ja |
| tvungent søk, 120 tilfeldige starter | 18 | 120 av 120 |
| utvunget søk, 120 tilfeldige starter | 15 | **0 av 120** |

Avhandlingens løsning er altså et **lokalt optimum også under tvang**. De utvungne løsningene som ser
bedre ut (15 mot 18), er bedre bare fordi de lar de samme 13 aktivitetene grupperes på to ulike måter
samtidig — en blokkmodell som ikke kan tolkes. Når tvangen legges på, forsvinner den gevinsten.

**Konklusjonen på forskningsspørsmålet «endres blokkstrukturen?» er: nei.** Blokkstrukturen tvangen
gir, er den avhandlingen alt hadde. **Verktøygrensen sperret en representasjon, ikke et resultat.**

Det gjør ikke det ugjorte uinteressant — det viser at verktøygrensen **sperret ingen resultat**, og
det er en annen sak.
Avhandlingen skriver at 𝑀-ruten «is not suitable for blockmodeling three-mode EUCONNs in Pajek»; det
målte svaret er at 𝑀-ruten ikke er nødvendig i det hele tatt, fordi den augmenterte ruten oppnår det
samme og mer.

## Dødsbetingelsene, gjennomgått

* **Terskelen er ikke flyttet.** «Like partisjoner» ble målt som eksakt likhet mellom
  mengdepartisjoner, ikke som likt klyngetall — og det navngitte verktøyet gir ikke likhet.
* **Negativt utfall er ført likt.** Både porten (falt) og forskningsresultatet (ingen endring) er
  negative, og begge står her uten pynt.
* **Ingen verktøysvikt forkledd som resultat.** Pakken ble installert og kjørt; at den mangler
  mekanismen, er et funn, ikke en installasjonsfeil. At R ikke kunne nå CRAN fra maskinen, ble løst
  ved å hente kildepakken (`blockmodeling_1.1.8.tar.gz`, sha256 `3164605aa250f34e…`) og bygge den
  lokalt — det er ført her og var ingen hindring.
* **Kildens egne tall ble reprodusert først**, i to implementasjoner, før noe nytt ble kjørt.
* **Ingen e-post til noen.** Ingen forespørsel om matrisen eller mdl-filen, selv om den ville løst
  én åpen detalj (blokktypenes prioritetsvekter, se under).
* **Ingen Anthropics API.**
* **Én ting kunne ikke reproduseres, og den er ført som åpen:** avhandlingen sier at brukeren kan
  «assign a priority or a weight for each block type», og oppgir ikke verdiene. Uten dem kan
  *optimaliseringen* ikke reproduseres — bare feilen for en gitt partisjon. Derfor er blokktypene
  låst per posisjon til avhandlingens egen bildematrise i alle **egne** søk, og det er en **betingelse på
  resultatet**, ført her og ikke gjemt. **Portkjøringen i R gjorde det ikke:** den brukte
  `blocks = c("nul","com","reg","rre")` fritt per blokk og ga «11 løsninger med minimal feil = 0» —
  nettopp det degenererte regimet avsnittet under beskriver. At partisjonene der ikke ble like, er derfor
  et utfall under fritt typevalg, og om det tåler den degenerasjonen, er ikke prøvd. *(Rettet 28.09.2026,
  frys-lesningen: sto «i alle søk».)* Med fri typevalg blir målet degenerert: både min
  implementasjon og R-pakken når total feil 0 fra nesten hvilken som helst start, fordi `rre` alltid
  kan velges. **Et fritt typevalg gjør generalisert blokkmodellering meningsløs**, og det er den
  viktigste metodiske lærdommen fra kjøringen.

## Klassifisering

| | før | nå |
|---|---|---|
| kodet klasse fra teksten | `H5` | uendret — teksten har ikke endret seg |
| datert vurdering (ADR-0010) | — | `H5`, **ikke opphevet av det navngitte middelet**, 27.09.2026 |

Klassen endres ikke: det som falt, er den navngitte framgangsmåten på den datoen, ikke hindringens
art. Hindringen er **løftbar** — en formålsbygget implementasjon løfter den — men løftet er
**konsekvensløst**, og det er saken i én setning.
