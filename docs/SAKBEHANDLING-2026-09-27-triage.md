# Sakbehandling — triage av de 50 kandidatene

**27.09.2026. Datert vurdering (ADR-0010).** Grunnlag: `docs/SAKBEHANDLING-2026-09-27-kandidater.md`
(50 passasjer, løftbar/uavklart klasse, tvil=false). Alle 50 lest før noe under ble skrevet.
«Finnes ressursen i dag» er merket **[V]** der det må slås opp av CC før kriteriet låses — ingen
av dem er antatt sanne her.

## Strukturelt funn

50 passasjer er **17 saker**. 23 passasjer er ett ugjort (Pring 2016, SPAW/partikkeltetthet);
fire er samme setning i to overlappende vindu. Enheten for sakbehandling er **verk × hindring**.
Registeret bør bære en sak-id som grupperer passasjer (B3-tillegg: `sak`-felt, gruppert på
verk + hindringens kjerneord; ingen ny måling).

## Kortliste — kan låses, i denne rekkefølgen

### SAK-14 · Haouachi 2016 (W2474595476) · H3 språk · **AI-aksen**
AL-0738, AL-2370. Ugjort: de greske kildene (Dionysios fra Halikarnassos, *Antiquitates Romanae*
m.fl.) er bare lest i fransk oversettelse fordi avhandlingen oppgir manglende greskkunnskap. Hva opphever:
LLM-assistert lesning av den greske originalteksten. Ressurs: gresk tekst av Dionysios er
offentlig eiendom (Perseus) **[V]**. Kriterium til låsing: (1) alle steder i avhandlingen der
en gresk kilde siteres bare i oversettelse listes opp med referanse; (2) for hvert sted hentes
den greske teksten fra åpen kilde og verifiseres ved eksakt strengmatch mot kildeutgaven;
(3) hindringen regnes opphevet hvis ≥ 90 % av stedene får gresk tekst med de bærende termene
identifisert; (4) forskningsresultatet er antall steder der LSJ-glossen for den bærende termen
avviker fra den franske gjengivelsen på den aksen avhandlingen argumenterer (kjønn, etnisitet,
status) — rapportert som N uten terskel, negativt utfall likt. Kostnad: lav. Ingen fysisk ressurs.
**Første sak å kjøre.**

### SAK-09c · Toronto-avhandling 2018 (W7133020405) · H1/H7-uavklart · **AI-aksen**
AL-2606. Ugjort: automatisk generering av avhandlingens begrepsnettverk fra casestudie-tekstene;
avhandlingen skriver at teknologien «kanskje alt finnes» men at oppgaven ikke er triviell med få
tekstressurser og umoden AI (2018). Hva opphever: LLM-ekstraksjon av begreper og relasjoner.
Ressurs: det manuelle nettverket står i avhandlingen; kildetekstene må være hentbare **[V]** —
er de bak betalingsmur, er saken H8. Kriterium til låsing: nodesett og kantsett i det manuelle
nettverket transkriberes først (sha); normalisering (lemma, små bokstaver, definert synonymliste
skrevet før kjøring); fast ledetekst med sha; opphevet hvis node-recall ≥ 0,70 og kant-recall
≥ 0,50 mot det manuelle nettverket. Under: ikke opphevet, ført. Kostnad: middels.

### SAK-08 · Riris 2018 (W2784603861) · H5 regnekraft
AL-1280. Ugjort: kjøringene delt i to sett fordi kontinuerlig målte kjøringer tok uoverkommelig
lang tid. Hva opphever: regnekraft og tid. Ressurs: kode og data for modellen **[V]** — sjekk
artikkelens datatilgang, Bournemouth eprints, OSF, GitHub. Kriterium: (1) reproduser artikkelens
rapporterte tall for de to separate settene før noe nytt kjøres (PS-246-mønsteret); (2) kjør alle
som ett sammenhengende sett; opphevet hvis fullført på Macen innen 24 t; resultat: om
konklusjonene endres, rapportert uansett retning. Uten kode: H8/H7, lukket.

### SAK-09b · Toronto-avhandling 2018 · H5 verktøygrense
AL-0852. Ugjort: Pajek kan ikke tvinge like partisjoner for mellomnivåets noder i to-modus
blokkmodellering. Hva opphever: annet verktøy med forhåndsgitt blokkstruktur (R-pakken
`blockmodeling`, generalisert to-modus) **[V]** — merk: fantes trolig i 2018, så dette er
verktøyvalg, ikke tidsakse. Ressurs: matrisen M må stå i avhandlingen **[V]**. Kriterium:
reproduser avhandlingens Pajek-resultat først; kjør med tvungen partisjonering; opphevet hvis
kjøringen gir like partisjoner; resultat: endres blokkstrukturen, rapportert.

### SAK-11 · ASCE/OSTI 2020 (W4206850274) · H5 regnekraft
AL-2516. Ugjort: alle ~22 mill. 7-utfallsscenarioer for case30 var uhåndterlige i den
stokastiske formuleringen. Ressurs: case30 er offentlig (MATPOWER) **[V]**, formuleringen står i
artikkelen. Kriterium: reproduser artikkelens utvalgsresultat; full enumerering opphevet hvis
løsbar innen 48 t lokalt; resultat: endres herdingsbeslutningene. Tung — sist på lista.

### SAK-13 · Biblindex 2020 (W3165757969) · H1 tid · AI-aksen, svakt kriterium
AL-0374. Ugjort: svake semantiske enheter segmentert bare der det ikke ga «unødig kompleksitet»,
for å holde tiden. Hva opphever: automatisk segmentering/justering av versjoner. Ressurs:
Biblindex' referanser åpne? **[V]** Kriteriet er svakt fordi det ugjorte ikke har fasit — bare
ekspertvurdering kan si om auto-segmenteringen holder. Parkert bak de fem over.

## L5-sjekker — har noen gjort det siden? (CC, siteringsoppslag, ≤ 10 kreditter hver)

- **SAK-15** Mythos 2018 (W2974992769), AL-0681: smykker og metallfunn fra deponeringsgrop H ikke
  datert. Sjekk siterende arbeider etter 2018 for datering. Ja → hindringen opphevet av andre,
  sak lukket med DOI; nei → H7, parkert med utløser.
- **SAK-16** Eythra 2017 (W4317830072), AL-0070: felles vurdering med kollegene på hus og
  gjenstander. Sjekk Eythra-publikasjoner etter 2017.
- **SAK-17** Pietrele 2019 (W2936215896), AL-1440: flere digelanalyser. Sjekk siterende.
- **PS-246-utvidelse** Pring 2016, AL-0110/AL-2127: saltholdighet satt til null fordi
  simulatoren ikke tar osmotisk justering. Saxton–Rawls 2006 har termen; PS-246-implementasjonen
  kan utvides — bare hvis avhandlingen har målt EC **[V]**. Uten EC-data: H7 for delsaken.

## Forkastet — krever fysisk materiale, feltarbeid eller mennesker

| sak | passasjer | hvorfor |
|---|---|---|
| SAK-01 SPAW partikkeltetthet | 23 (AL-0068 … AL-2836) | **gjennomført som PS-246** 25.09; ingen ny sak |
| SAK-02 CCC borehull | AL-1966, AL-2440 | H1 som krever feltarbeid; DART-data dekker uttrykkelig ikke CCC |
| SAK-03 tre sesonger / matrisetetthet | AL-1390, AL-1609, AL-2387 | nye feltdata; H7 i praksis |
| SAK-04 Nahal Hemar-belegg | AL-0021 | krever prøvene; laboratorieløftbar, utenfor verktøyets rekkevidde |
| SAK-05 Transylvania glassperler | AL-0119, AL-2522 | krever prøvene, som er få og brent |
| SAK-06 Rheidae-eggeskall | AL-0126 | krever prøvene (ZooMS/aDNA ville krevd materialet) |
| SAK-07 kursiv forkortelse | AL-0925 | avbildning krever objektet; parallellsøk i EDCS/EDR mulig men lav verdi — parkert |
| SAK-10 Pye/ESME og deltakerkrets | AL-2459, AL-2252, AL-1878 | ESME ikke åpen **[V]**; mennesker |
| SAK-12 konferanseabstrakt | AL-0928 | H7: flere pasienter |
| SAK-09a/d validering og virkelig prosjekt | AL-0041, AL-2642, AL-1064 | krever prosjekter og mennesker |

## Hva dette gir sporet

Ledd 2 har til nå ett gjennomført tilfelle (PS-246), ingen på AI-aksen. SAK-14 og SAK-09c er de to
første kandidatene der hindringen er språk eller ekstraksjon og opphevelsen er en språkmodell.
SAK-08 og SAK-11 er regnekraft-aksen. Alle fire har kriterium som kan låses før beregning og
negativt utfall som gyldig resultat.

---

## Datert tillegg 28.09.2026 — L5-sjekkene er kjørt. Fire ganger nei.

Spørsmålet var: **har noen gjort det siden?** Svaret er nei i alle fire, og her står belegget med DOI.
**10 OpenAlex-kreditter brukt av 40 tillatte.** Ingen `mailto`-parameter ble sendt — fellespoolen
holdt for ti kall, og da går ingen adresse til tjenesten.

### SAK-15 · Mythos 2018 (`W2974992769`), AL-0681 — **nei**

Det ugjorte, presist: smykkene og metallsmåfunnene fra **deponeringsgrop H ved Demeter-helligdommen i
Knossos** er ikke datert, så det kan ikke avgjøres om mynter erstattet metallgjenstander. Kilden er
ordrett: «More than 300 gold, silver, bronze jewellery, and small finds were also found in the deposit
pit H. … As the jewellery and metal small finds from this site have not yet been dated, it is not
obvious to what extant coins have replaced metal objects…» Materialet hviler på **Jackson 1973**.

Verket er sitert **3 ganger** (`10.4000/mythos.297`), og ingen av dem daterer materialet:

| år | siterende arbeid | DOI |
|---|---|---|
| 2020 | Bronze vessels of the Late Republican period from Sarmatian burials | `10.18503/1992-0431-2020-4-70-41-109` |
| 2021 | Rituals and Votive Offerings at the Sanctuary of Demeter in **Kaunos** — annen helligdom | `10.3138/mous.17.2.004` |
| 2025 | Persephones khthoniske side, kulter og kultpraksis (tyrkisk) | `10.35237/suitder.1746526` |

Bredere søk på «Knossos Demeter sanctuary» etter 2018 ga 137 treff; de fremste er kildeverket selv,
Kaunos-helligdommen, Knossos-urbanisme og kretiske mynter. **Ingen dateringsstudie av grop H.**
→ **H7, parkert med utløser.**

### SAK-16 · Eythra 2017 (`W4317830072`), AL-0070 — **nei**

Det ugjorte: det andre forskningsspørsmålet krevde en **felles vurdering med kollegene som undersøker
gjenstandene og husene**. Verket er sitert **2 ganger** (`10.35686/ar.2017.12`), begge om neolittisk
keramikk andre steder: Lengyel-keramikkproduksjon (`10.1016/j.jasrep.2024.104739`, 2024) og
petrografisk keramikkutveksling (`10.1007/s12520-020-01244-6`, 2021).

Triagen ba også om et bredere søk på Eythra-publikasjoner etter 2017: **81 treff**, og de to som
gjelder boplassen, er **anmeldelser** av Stäuble & Veits bind — `10.11588/ai.2017.1.42531` (2017) og
`10.11588/ger.2019.78651` (2021) — av et bind utgitt i **2016**, altså **før** kildeverket. Ingen
senere felles vurdering av gjenstander og hus finnes. → **H7, parkert med utløser.**

### SAK-17 · Pietrele 2019 (`W2936215896`), AL-1440 — **nei**

Det ugjorte: kan ikke avgjøre om digelen er et **enkelttilfelle eller en trend** før flere liknende
digler er analysert. Verket er godt sitert — **12 ganger** (`10.1371/journal.pone.0214218`) — og fire
av dem er nære nok til å måtte leses:

| år | siterende arbeid | hva det gjør | DOI |
|---|---|---|---|
| 2021 | Early Balkan Metallurgy 6200–3700 BC | **syntese** av eksisterende data, inkl. bly; ingen nye digelanalyser | `10.1007/s10963-021-09155-7` |
| 2023 | From Galena to Lead: Western Mediterranean | galena på Iberia/Sør-Frankrike; ikke balkanske digler | `10.46586/metalla.v27.2023.i2.95-117` |
| 2026 | An early lead-smelting tradition in north-east Iberia | tre **slaggnoduler** på Minferri, tidlig 2. årtusen f.Kr. — annen region, ~3 årtusener senere | `10.15184/aqy.2026.10388` |
| 2021 | Traditional Chinese Technology of Crucible Lead Smelting | digler, men Kina, historisk tid | `10.3724/sp.j.1461.2021.01027` |

**Ingen har analysert flere blyforedlende digler fra 5. årtusen f.Kr. ved Nedre Donau.** Det nærmeste
er 2021-syntesen, som drøfter balkansk blymetallurgi på grunnlag av *eksisterende* data — adjacent,
men ikke det ugjorte. → **H7, parkert med utløser.** Utløseren er skarpere her enn i de to andre: 12
siteringer og et aktivt felt gjør det sannsynlig at noen gjør dette.

### PS-246-utvidelsen · Pring 2016 (`W2551114598`), AL-0110/AL-2127 — **nei, og grunnen er skarpere enn ventet**

`[V]` var: *bare hvis avhandlingen har målt EC.* Svaret er **både ja og nei**, og nei-en avgjør.

**Ja:** avhandlingen har EC-instrumentering. TDR-sondene i DART-prosjektet «measure both the
electrical conductivity and electrical permittivity of the soil».

**Nei, og det er det som gjelder:** EC-en er **ikke rapportert som data**. Den er et mellomledd —
«post-processing of the data returns a volumetric water content». Søk i hele avhandlingen
(581 864 tegn): **`dS/m` 0 treff, `ECe` 0 treff, «saturated paste» 0 treff, «soluble salts» 0 treff**,
og den **eneste** EC-verdien som forekommer, er `0.0μS/cm` — verdien som ble *satt*, ikke målt:

> «Though the soil water characteristic module allows assessment of osmotic SWCC with electrical
> conductivity inputs, these adjustments cannot be used in the simulator. Therefore this parameter has
> not been included for simulations and salinity of 0.0μS/cm has been applied to the soil for analysis.»

**Og det er dessuten den gale EC-en.** Saxton & Rawls' saltholdighetsledd tar `ECe` i dS/m fra en
mettet pastautdrag; TDR-sondens bulk-EC er en annen størrelse og kan ikke settes inn i stedet.
→ **H7 for delsaken.** PS-246-implementasjonen kan ikke utvides med saltholdighetsleddet, ikke fordi
termen mangler i Saxton–Rawls, men fordi avhandlingen ikke har inndataen termen krever.

### Hva de fire sjekkene til sammen sier

Fire av fire nei, og ingen av dem fordi feltet er dødt — Pietrele er sitert 12 ganger, Eythra-søket ga
81 treff. **Det ugjorte i disse fire sakene er ikke noe andre har tatt opp**, selv der feltet er
aktivt. Det er et eget funn om ledd 2: en hindring blir ikke opphevet av at feltet arbeider videre i
nærheten. Alle fire står nå med utløser, og utløseren for SAK-17 er den mest sannsynlige å slå til.
