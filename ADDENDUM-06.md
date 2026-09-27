# ADDENDUM-06 — Filterets recall målt mot en fasit, og dekningsgraden festet

**Skrevet:** 2026-09-12
**Hører til:** PREREG-v1.md `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`,
ADDENDUM-01.md `aa78d1be50ac17f8e26a92513aa115b3d504bdde3556e43b4f2317ea47cc255f`,
ADDENDUM-02.md `7c0542c92c54a586e3b387794272bed171ee285b75c8ebe4ee8fe1fa16f6f713`,
ADDENDUM-03.md `0b577ae6c3d0278e811e674c78e4e2948be46252e5aca9c94e94466c1f985c4e`,
ADDENDUM-04.md `7f7d067b80468a7016e398d1120930c98eb8a705b0e1c0102ad97e9db42f8a9c`,
ADDENDUM-05.md `b12c85b2a731517f9d0c5742194b2b8a900177cb82d662f8bf20e7d67fef5e9d`
**Status:** operasjonalisering etter lås. Endrer uttrekksmønsteret (L2) og rapporteringskravet for falsifiseringstesten (PREREG §8). Skrevet før trekking og før koding. Ingen av de seks låste filene er endret.

---

## 1 Recall og presisjon mot fasiten

### 1.1 Fasiten

`data/recall-sett.jsonl` er en manuell fasit: **30 dokumenter lest i sin helhet, uten markørlisten og uten søk**, hver passasje som oppfyller PREREG §2 under passasjekravet (ADDENDUM-03 §1) markert for hånd, med spenn, klasse og begrunnelse per treff.

Dokumentene er trukket med målefrøet `2ef3dee8` = **734248** fra de **46** av de 394 lagrede fulltekstfilene som **ikke** ble funnet ved frasesøk. De øvrige 348 er ankersøk (153), kontrollsøk (74), ADDENDUM-02-kontrollsøk (56), H1/H4-søk (48) og tekstvitenskapssøk (17) — de er valgt fordi de inneholder frasene, og kan derfor ikke brukes til å måle om frasene finner noe. De 46 kommer fra nedlastbarhetsmålingen i ADDENDUM-03 §2, som var et frøtrukket utsnitt, ikke et frasesøk.

40 dokumenter ble trukket av de 46. Ti falt ut på en språk- og innholdssjekk: sju ikke-engelske (spansk, fransk, italiensk, gresk, kinesisk), én uten uttrekkbar tekst (PDF uten tekstlag), og to med for stor andel ikke-latinsk skrift. **30 ble lest.** Feltfordeling: klinisk epidemiologi 7, tekstvitenskap 7, arkeologi 6, energisystemmodellering 6, ikke tilskrivbar 4. De fire er PMC-dokumenter der loggene bare bærer PMC-id og ikke feltspørringen; feltet er ikke rekonstruerbart og oppgis som ukjent i stedet for å gjettes.

**Settet er et verktøy, ikke et utvalg.** Åtte av de 30 dokumentene har minst ett treff. Det tallet er **ikke M1** og skal ikke leses som prevalens: 30 dokumenter er trukket fra et hentbarhetsutsnitt, ikke fra rammen. Alle 40 er ført i `data/leste-kontrollkandidater.json` med merke `LEST-I-SIN-HELHET-UTELATT-FRA-TREKKING` (30) eller `SPRAAKSJEKKET-IKKE-LEST-UTELATT-FRA-TREKKING` (10), og utelates fra trekkingen.

Fasiten har **28 treff** i 8 dokumenter. Klassefordeling: H7 12, H2 5, H4 3, H3 2, H1/H7-uavklart 2, H2/H7-uavklart 2, H8 1, H9 1 — fire av 28 uavklarte etter ADDENDUM-05. Fem av de 28 (17,9 %) oppfyller kravet bare på passasje, ikke på setning.

### 1.2 Målingen

Treffregelen står i kode (`gjenopptak.extract.recall.dekker`): et fasittreff er fanget når en filterpassasje fra samme dokument har `start_index ≤ fasit.hit_index ≤ end_index`. Samme regel brukes begge veier. Presisjonen måles over **alle 30** dokumentene, også de 22 uten fasittreff — ellers ville falske positive i de treffløse dokumentene falt utenfor nevneren.

| Filter | Recall | Presisjon |
|---|---|---|
| **v1** (mønsteret som sto i `passage.py`) | **0/28 = 0,0 %** | **0/6 = 0,0 %** |
| **v2** (etter utvidelsen i §1.4) | 28/28 = 100 % (i utvalget det er lest av) | 32/52 = 61,5 % |

**v1-tallet er funnet i denne slyngen.** Filteret som har båret hele rørledningstesten fant **ingenting** i 30 dokumenter lest uavhengig av det, og alle seks kandidatene det ga, var falske positive: fire handler om andres arbeid eller er normative utsagn («researchers … were unable to convince Platonists»), én er et ekskluderingskriterium («Participants were excluded if they were unable to complete all portions»), én er en observasjon om romersk rett.

De to sidene faller ikke likt. Av de 28 bommene traff `UNDONE` på 3, og på nettopp de tre traff `OBSTACLE` verken i setningen eller i vinduet. `OBSTACLE` traff i vinduet for 16 av de 28, i setningen for 12. Fordelingen av de 28 bommene: **3 faller bare på hindringssiden, 16 bare på markørsiden, og 9 på begge.** Markørlisten alene forklarer altså under to tredjedeler av dem. Det var ikke forutsett — markørlisten var det vi trodde var hele flaskehalsen.

To defekter er rene regexfeil som fasiten avdekket:

* `lack(ing|ed|s)? of` krevde preposisjonen. «data … **is lacking**, doubtful or incomplete» og «we **lack** quantitative data» falt derfor utenfor hindringssiden.
* `no (copy|copies|surviving|extant|record|material|data)` krevde at ordene stod inntil hverandre. «There were **no similar data** available» falt utenfor.

### 1.3 Presisjonen er 61,5 %, og det er som det skal være

20 av 52 v2-kandidater er ikke i fasiten. De er ikke feil i filteret, men N2/N3-tilfeller som PREREG §5 krever at telles: «further investigations **are needed**», «**cannot** be justified by improved patient outcomes», «we **cannot** draw the conclusion that the awl signifies female identity». Uttrekket er en kandidatgenerator, ikke en dommer. Andelen sier hva én koder må lese for hvert reelt treff: i dette settet 1,6 kandidater per treff.

### 1.4 Utvidelsen, og hva den ikke er

**36 tillegg er lest ut av de faktiske bommene** — 25 på `UNDONE` og 11 på `OBSTACLE`, ingen fra fantasi. Hvert tillegg står i `passage.py` som `(mønster, doc_id, setningsindeks, sitatfragment)`, og testpakken krever at mønsteret treffer den setningen det oppgir å komme fra (`tests/test_recall.py`, armeringskravet: et nullresultat teller ikke før en streng som MÅ treffe har truffet). De formene fasiten hadde og v1 ikke dekket, i utvalg:

| Formulering | Fra |
|---|---|
| «it **has not been possible** to characterize them» | W2768163024 #95 |
| «we **cannot** favour a northern or southern route» | PMC4342813 #698 |
| «our data **lacked sufficient** power» | W246600566 #137 |
| «**limiting our ability** to understand evaluations» | PMC5020840 #27 |
| «they **have not been individually quantified**» | W2225860453 #111 |
| «Length **has not been taken into consideration**» | W2225860453 #141 |
| «sample size … **hampers** statistical comparisons» | W2225860453 #191 |
| «we **would not consider** a more detailed dating reliable» | PMC4342813 #653 |
| «We **leave for another occasion** …» | W2505978088 #44 |
| «we are **still waiting for** DNA analyses» | W2505978088 #137 |
| «The results have so far been **unfruitful**» | W2505978088 #538 |
| «is **not yet reliable** enough» | W2505978088 #544 |
| «**with the exception of** … nine cases in which data … is lacking» | W2505978088 #573 |

**v2s recall på 100 % er ikke en måling.** Markørene er lest ut av nettopp disse 28 setningene; tallet er en øvre grense og bekrefter bare at utvidelsen traff det den ble laget for. **Bare v1-tallet (0/28) er målt utenfor utvalget.** v2 må måles mot en fasit bygget etter at v2 var frosset. Hva den fasiten må inneholde, står i §1.6.

To av tilleggene er svakere enn de andre og merkes her, ikke bortgjemt i koden:

* `limitation of (this|our) study` (fra PMC5454651 #193) markerer **sjangeren begrensningsavsnitt**, ikke det ugjorte. Setningen oppgir det ugjorte bare indirekte — «the lack of information about women who had chosen to follow-up at private sector» — og ingen verbfrase bærer det. Den koster ingenting i presisjon på de 30, men klinisk sjanger er tynt representert der, og dette er markøren som først vil blåse opp kandidatmengden i klinisk epidemiologi.
* `cannot\b` er det bredeste tillegget. Det henter fem av de 20 falske positive alene.

En strukturell konsekvens: **noen parkerte spørsmål oppgir det ugjorte og hindringen i ett og samme ord** — «we **lack** quantitative data», «still **waiting for** DNA analyses». To mønstre som må treffe hver sin ting, er dårlig tilpasset den formen, og `we lack` og `waiting for` står derfor på begge sider. Det er et designproblem i totrinnsfilteret, ikke en markørmangel, og det er ikke løst her.

### 1.5 De ti døde markørene beholdes

Ti av de 23 markørene ga null treff i rørledningstesten: `did not attempt`, `prevented me from`, `no attempt was made`, `we coded a random sample`, `remains unread`, `remains untranscribed`, `have not been read`, `have not been transcribed`, `have not been collated`, `have not been digiti`.

De er døde **også** mot fasiten: null forekomster i de 28 fasitpassasjene og null i 1 068 021 tegn av de 30 dokumentene (telt i Python; armering: `was not possible` forekommer, så tellingen leser teksten).

**Ingen fjernes.** De fem arkivmarkørene koder sjangeren diplomatisk kildeutgivelse og katalogarbeid, og ingen av de 30 dokumentene er av den sjangeren — de sju tekstvitenskapsdokumentene er en Platon-studie, en teologisk artikkel og liknende, ikke kildeutgivelser. Et nullresultat i et materiale som mangler sjangeren markøren dekker, er ikke evidens mot markøren. Fjerning krever en fasit som inneholder sjangeren. Testen `test_de_ti_dode_markorene_star_fortsatt_i_listen` holder dem på plass og bærer begrunnelsen.

### 1.6 Hva som gjenstår før v2 kan tas for god fisk

* En **ny fasit, bygget etter at v2 er frosset**, på dokumenter som ikke er lest. De 46 har seks uleste igjen — for få. Kilden må være et nytt frøtrukket utsnitt utenfor rammen.
* Fasiten må inneholde **minst én diplomatisk kildeutgivelse**, ellers står §1.5 uavgjort.
* **Én koder.** Fasiten er markert av samme koder som skrev markørene. Det er den samme svakheten PREREG §4 kaller designets største, og den slår her dobbelt: koderen som bestemmer hva et treff er, er også den som skrev filteret som skal finne det. To grensetilfeller er merket `grensetilfelle: true` i fasiten (PMC5020840 #379, W2505978088 #346) med recall oppgitt både med og uten dem, men det dekker bare de tilfellene koderen selv så som tvilsomme.

### 1.7 Hva utvidelsen koster i volum

På de 392 av de 394 lagrede filene som har minst én setning (to PDF-er ga null uttrekkbar tekst) gir v2 **607 kandidater mot v1s 217**, og andelen dokumenter uten kandidat faller fra 259/392 = 66,1 % til 167/392 = 42,6 %. Den lagrede rørledningstesten oppgir 261/394 = 66,2 % fordi de to tomme filene der ligger i nevneren. Dette er **rørledningstest, ikke prevalens**: materialet er frasesøkt, og tallene beskriver bare filterets oppførsel. De er tatt med fordi de sier hva kodearbeidet vokser til.

---

## 2 Markørfordelingen fra rørledningstesten kan ikke leses som recall

Rørledningstesten ga denne fordelingen over de 220 markørtreffene: `could not` 97 (44,1 %), `were unable to` 34, `did not have` 17, `was not possible` 17, `too time-consuming` 14, `prohibitiv` 12, `only a subset` 8, og sju former under 8. 13 av 23 markører i bruk.

**Den fordelingen er sirkulær.** 348 av de 394 dokumentene ble hentet ved å søke i fulltekst etter nettopp disse frasene. At `could not` dominerer, sier hva søkene lette mest etter, ikke hva som finnes i litteraturen og ikke hva filteret fanger. Tallene er gyldige som beskrivelse av én ting: hvor skjevt fordelt filterets egne treff er i det materialet det selv har hentet. En markørliste der én frase står for 44 % av treffene har skjør recall — men **hvor skjør, kan ikke leses av fordelingen.** Det krevde fasiten i §1, og svaret var 0 %.

Dette gjelder også framover: så lenge et tall er regnet på materiale som er funnet ved frasesøk, kan det ikke brukes som recall-, presisjons- eller prevalensanslag. Rapporteringen av markørfordelingen skal alltid bære denne setningen.

---

## 3 Passasjen som enhet: empirisk støtte for ADDENDUM-03 §1

ADDENDUM-03 §1 flyttet observasjonsenheten fra setningen til passasjen (±2 setninger) fordi uttrekket alltid hadde båret vinduet mens målingen ble definert på setningen.

Tallene:

* **Rørledningstesten:** 81 av 217 kandidater (**37,3 %**) oppfyller kravet bare på passasje. Hadde enheten blitt stående på setningen, ville 37,3 % av kandidatene forsvunnet — i et materiale som er valgt for å inneholde frasene.
* **Fasiten, uavhengig av filteret:** 5 av 28 treff (**17,9 %**) har det ugjorte og hindringen i forskjellige setninger. Blant v2s 32 sanne kandidater er andelen 21,9 %.

De to tallene måler ikke det samme og skal ikke slås sammen. Det første er filterets oppførsel i sirkulært materiale; det andre er hvor ofte en menneskelig leser fant de to delene spredt. **Begge peker samme vei, og det andre er det som teller:** nesten en femtedel av reelle parkerte spørsmål ville falt ut av et setningskrav. ADDENDUM-03 §1 var ikke en formalitet.

M1 rapporteres fortsatt som to tall, M1-streng og M1-passasje, aldri ett alene (`format_m1` gir ingen enkelttallsvariant).

---

## 4 Dekningsgrad: hva Europe PMC kan se, og hva det gjør med PREREG §8

Falsifiseringstesten i PREREG §8 spør om et parkert spørsmål er tatt opp senere, målt på verkene som siterer artikkelen. Ruten gjennom Europe PMC er kvotefri, og derfor målt i denne slyngen: 20 verk fra det lagrede materialet, siteringer hentet fra Crossref (`is-referenced-by-count`) og Europe PMC (`CITES:{id}_{source}`), med samme frø (734248).

| Størrelse | Måling |
|---|---|
| Siteringer Crossref kjenner | 1 156 |
| Siteringer Europe PMC kjenner | 617 = **53,4 %** |
| Av dem med fulltekst i EPMC | 333 = 54,0 % av EPMCs |
| **Søkbar andel av alle kjente siteringer** | **333/1 156 = 28,8 %** |
| Median per verk (EPMC/Crossref) | 0,72 |
| Verk helt utenfor EPMC | 0 av 20 |

**Konsekvensene festes her:**

1. **Falsifiseringstesten for PORT-en kjøres mot OpenAlex, ikke mot den kvotefrie ruten.** Europe PMC kan i beste fall se 53,4 % av de siteringene Crossref kjenner, og kan søke i fulltekst hos 28,8 %. En overlevelsesrate regnet på den ruten ville måle Europe PMCs dekning like mye som litteraturens oppfølging. Den kvotefrie ruten beholdes som **kryssjekk og som armering** (den ga 391/194/75/66 på 10.7554/elife.09560), ikke som målerute.
2. **Overlevelsesrate rapporteres aldri uten dekningsgrad ved siden av.** Hvert tall fra falsifiseringstesten bærer nevneren sin: hvor mange siterende verk kilden kjente, og hvor mange av dem det fantes søkbar fulltekst for. Et tall uten det paret er ikke rapporterbart.
3. Ruten som faktisk brukes, koster kvote. Det er innarbeidet i budsjettet i ADDENDUM-04 §2: 1 000 kall/døgn, ingen polite pool, ~11 timers tilbakestilling som ikke følger kalenderdøgnet.

### 4.1 EPMC er en nedre grense i aggregat, ikke per verk

53,4 % er et aggregat. Per verk holder grensen ikke: **ett av 20 verk har flere siteringer i Europe PMC enn i Crossref** (10.15441/ceem.16.144: 14 mot 13, 108 %), og **fire av 20 ligger på eller over 100 %** (de tre andre på nøyaktig 100 %: 10.1097/cm9.0000000000000390, 10.1186/s12971-015-0060-9, 10.1038/s41598-020-69807-0). Spredningen er 0,14 til 1,08.

*Rettelse til slyngens forutsetning:* oppdraget oppgav to av 20 over 100 %. Den lagrede målingen viser **ett** over og **fire** på eller over. Poenget står uendret på de målte tallene: de to kildene teller ikke det samme, og den ene er ikke en delmengde av den andre. Crossref teller registrerte referanser fra DOI-bærende verk; EPMC indekserer også referanser fra verk uten Crossref-registrert referanseliste. **«Nedre grense» er derfor en egenskap ved aggregatet, ikke en garanti per verk, og skal ikke brukes som per-verk-argument i noen enkeltvurdering.**

---

## 5 Hva som endres, og hva som ikke endres

**Endres:**

* Uttrekket bruker v2-mønstrene (`UNDONE_V2`, `OBSTACLE_V2`). v1 står urørt i koden, med test, fordi den produserte rørledningstestens tall og de skal kunne reproduseres.
* Falsifiseringstestens rute (§4.1) og rapporteringskravet om dekningsgrad ved siden av overlevelsesrate.

**Endres ikke:**

* Tersklene i PREREG §6. Ingen av dem er rørt; grunnlaget de regnes på er blitt ærligere, ikke flyttet.
* Klassene og løftbarheten i PREREG §5 og ADDENDUM-05.
* Enheten (passasje, ±2) og kravet om to tall for M1 fra ADDENDUM-03 §1.
* Utvalgsdesignet i PREREG §4. n = 25 per felt, frø `05988b23` = 93 883 171, trekking etter at dette addendumet er skrevet.

---

## 6 Erklæring

* **Ingen trekking av utvalg er utført**, ingen koding av utvalget er begynt. Fasiten er et verktøysett, ikke et utvalg, og ingen tall i den er M1 eller M2.
* **Ingen OpenAlex-kall** er brukt på denne slyngen. Dekningstallene i §4 er lest fra `data/pipeline-test/l4-dekning-PIPELINETEST.json`, målt tidligere mot Crossref og Europe PMC.
* Alle 40 trukne dokumenter står i `data/leste-kontrollkandidater.json` (nå 314 rader) og **utelates fra trekkingen**.
* **PREREG-v1.md og ADDENDUM-01/02/03/04/05.md er uendret**, sha256 `05988b23…ba23a`, `aa78d1be…c255f`, `7c0542c9…f713`, `0b577ae6…5c4e`, `7f7d067b…8a9c`, `b12c85b2…5e9d`.
* Ingen remote, ingen push.
* Rådata er ikke committet. `data/` er git-ignorert; fasiten og loggen ligger der og sikres til Vault.
* **Åpne poster:** de tre punktene i §1.6 (ny fasit etter frysing, kildeutgivelse i fasiten, én-koder-svakheten); designproblemet i §1.4 om formuleringer der det ugjorte og hindringen er samme ord; feltet for fire av de 30 dokumentene er ikke rekonstruerbart fra loggene; og postene som står fra ADDENDUM-04 §6 og ADDENDUM-05 §7.
