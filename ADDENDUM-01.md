# ADDENDUM-01 — frø, emne-ID-er og hentbarhetsramme

**Skrevet:** 2026-09-12
**Hører til:** PREREG-v1.md, sha256 `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`
**Status:** operasjonalisering **og korreksjon** av PREREG §4. Skrevet før trekking, før én artikkel er lest, før noe utfall er sett.
**PREREG-v1.md er ikke endret og skal aldri endres.**

---

## 1 Frøet

**Frø: `05988b23`**

De første åtte heksadesimale tegnene i sha256 av PREREG-v1.md:

```
05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a
^^^^^^^^
```

Som heltall: `int("05988b23", 16)` = **93 883 171**.

**Determinismekrav.** OpenAlex' egen `sample`/`seed` er ikke tilstrekkelig: frøet gir samme utvalg bare så lenge korpuset er uendret, og korpuset vokser daglig. Trekkingen skal derfor gjøres i to trinn, og begge loggføres:

1. **Frys rammen.** Hent alle work-ID-er i den operasjonelle rammen (§3) per felt med cursor-paginering, sorter dem leksikografisk, lagre listen og dens sha256. Dette er utvalgsgrunnlaget.
2. **Trekk lokalt.** `random.Random(93883171)` over den frosne, sorterte listen.

Frøet alene er ikke nok til å reprodusere et utvalg. Frøet pluss sha256 av den frosne rammelisten er det.

**Et annet frø brukes til dekningsmåling.** Utsnittene i §5 er måleinstrumenter og inngår ikke i utvalget. De bruker `sha256("ADDENDUM-01 dekningsmaaling")[:8]` = `2ef3dee8`, som heltall mod 10⁶ = **734 248**. Prereg-frøet er ikke brukt til noen måling i dette dokumentet.

---

## 2 Korreksjon av PREREG §4: `has_fulltext` er ikke en hentbarhetsramme

PREREG §4 fester utvalgsrammen til `has_fulltext: true`. **Det er en indekseringsramme, ikke en hentbarhetsramme, og den forkastes som utvalgskriterium.** Korreksjonen er gjort før trekking og før noe utfall er sett.

### 2.1 Det dokumentasjonen sier

`has_fulltext` betyr at verkets fulltekst er indeksert **for søk hos OpenAlex**, fra én av to kilder: en åpen PDF, eller n-grammer hentet fra Internet Archives General Index. Kilden skulle kunne leses av feltet `fulltext_origin`.

To ting følger:

* **N-grammer kan ikke rekonstrueres til et dokument.** De er en ordliste, ikke en tekst. Et verk kan ha `has_fulltext: true` og likevel være utilgjengelig som lesbar tekst.
* **`fulltext_origin` eksponeres ikke lenger i work-objektet.** Målt 2026-09-12 på den positive kontrollen (10.1016/j.apenergy.2018.04.048): objektet har `has_fulltext: true`, men ingen `fulltext_origin`. Kilden kan altså ikke inspiseres per verk. Et kriterium hvis innhold ikke kan etterprøves, kan ikke bære et utvalg.

Kilder: OpenAlex Help Center, «Fulltext» (help.openalex.org/access/fulltext/); OpenAlex-bloggen, «Fulltext search in OpenAlex»; API-referansen for works.

### 2.2 To begrunnelser som ble prøvd og som ikke holder

Disse føres fordi de var utgangspunktet for korreksjonen, og fordi de er gale:

**(a) «Røyktesten bekreftet det — ti av ti rader kom med `fulltext_format: "none"`.»** Nei. `fulltext_format` settes hardkodet til `"none"` i `src/gjenopptak/harvest/openalex.py:164`, fordi L0 ikke henter fulltekst. Verdien er en konstant i vår egen kode, ikke en måling av OpenAlex. Røyktesten sier ingenting om hentbarhet.

**(b) «Vinduet 2015–2020 ligger der n-gram-andelen er høyest.»** Nei. Hvis n-grammer dominerte `has_fulltext`, skulle andelen falle etter 2020, siden General Index stopper der. Målt andel `has_fulltext: true` per år, alle fire felt, ti tellinger per år:

| år | tekstvitenskap | klinisk epi. | arkeologi | energimodellering |
|---|---|---|---|---|
| 2015 | 7,4 % | 26,9 % | 15,3 % | 18,1 % |
| 2018 | 12,7 % | 30,7 % | 17,2 % | 24,8 % |
| 2020 | 14,4 % | 40,2 % | 22,5 % | 30,4 % |
| 2021 | 15,3 % | 43,1 % | 23,1 % | 33,1 % |
| 2022 | 20,2 % | 47,8 % | 25,0 % | 33,4 % |
| 2023 | 21,3 % | 56,3 % | 29,3 % | 31,2 % |
| 2024 | 15,3 % | 53,7 % | 28,7 % | 27,4 % |

Andelen stiger fra 2015 til 2020 i alle fire felt, og **fortsetter å stige etter 2020**. Toppen ligger i 2022–2023, ikke i 2020: 20,2–56,3 % mot 14,4–40,2 %. Nedgangen i 2024, og fra 2022 for energimodellering, er forenlig med at de nyeste årene ennå ikke er ferdig indeksert; den inntreffer i alle fall ikke ved 2020-grensen.

Hadde n-grammer dominert `has_fulltext`, måtte andelen falt umiddelbart etter 2020. Den gjør det motsatte. **Vinduet 2015–2020 er den dårligst dekkede delen av perioden, ikke den best dekkede**, og `has_fulltext` drives i dag i hovedsak av PDF-parsing, ikke av n-grammer.

### 2.3 Den målte grunnen til at rammen likevel må forkastes

**`has_fulltext` er samtidig for løs og for stram.**

* **For løs:** den lover søkbarhet hos OpenAlex, ikke tilgang for oss, og kilden kan ikke etterprøves (§2.1).
* **For stram:** den utelukker verk vi faktisk kan hente. Antall verk med PDF-lenke er **større** enn antall verk med `has_fulltext: true` i alle fire felt — forholdet R3/R1 er 1,05–1,45 (§5). I historisk tekstvitenskap betyr det 46 888 mot 32 343: rammen kaster nær en tredjedel av de hentbare arbeidene.

Innenfor `has_fulltext: true` har 93,5–95,5 % av verkene også en PDF-lenke (§5). De to kriteriene overlapper altså sterkt, men `has_fulltext` er det som skjærer bort mest, uten at det gir noe hentbarhetsløfte tilbake.

**Den egentlige hentbarhetsaksen er tredelt**, og ingen av trinnene er `has_fulltext`:

| trinn | kilde | hva vi får | seksjoner |
|---|---|---|---|
| P1 | Europe PMC, `/{pmcid}/fullTextXML` | forlagets JATS | rå seksjonsetiketter, ferdig merket |
| P2 | OpenAlex' fulltekstarkiv | TEI XML, parset av GROBID | avledede seksjoner, varierende kvalitet |
| P3 | `best_oa_location.pdf_url` | PDF | må parses selv |

---

## 3 Ny operasjonell ramme

Rammen er en **tellbar filterstreng** pluss en **hentbarhetsport**. Porten kan ikke uttrykkes i filterstrengen, fordi `best_oa_location.pdf_url` ikke er et filtrerbart felt i OpenAlex (API-et svarer 400: «is not a valid field»).

### 3.1 Filterstreng (tellbar, reproduserbar)

```
topics.id:<felt-ID-er, «|»-separert>,publication_year:2015-2020,open_access.is_oa:true
```

Per felt, ordrett:

```
tekstvitenskap        topics.id:T10595|T10165|T14210,publication_year:2015-2020,open_access.is_oa:true
klinisk_epidemiologi  topics.id:T11095|T10556,publication_year:2015-2020,open_access.is_oa:true
arkeologi             topics.id:T10421|T10087,publication_year:2015-2020,open_access.is_oa:true
energimodellering     topics.id:T10424|T11185|T11941,publication_year:2015-2020,open_access.is_oa:true
```

`has_fulltext` inngår ikke. `open_access.is_oa:true` beholdes fordi lagringsretten i ADR-0001 krever åpen lisens, og fordi feltet er filtrerbart. `topics.id` er valgt framfor `primary_topic.id`: det fanger også verk der topicet ikke er det primære — målt på den positive kontrollen, som treffes av `topics.id:T10424` men ikke av `primary_topic.id:T10424`.

### 3.2 Hentbarhetsport (etterfilter, i rekkefølge)

For hvert trukket verk, første trinn som gir treff vinner:

```
P1  Europe PMC-oppslag på DOI gir pmcid, inEPMC=Y og isOpenAccess=Y
      → hent JATS fra /{pmcid}/fullTextXML
P2  OpenAlex' fulltekstarkiv har TEI XML for work-ID-en
      → hent TEI
P3  best_oa_location.pdf_url er ikke null, og lisensen tillater lagring
      → hent PDF, parse selv
ellers → uhentbar, substitueres etter §6 med årsak «ingen rute»
```

Ruten som ble brukt, loggføres per dokument (`fulltext_source`, `fulltext_format`), fordi den avgjør hva seksjonsetikettene er verdt (ADR-0002).

### 3.3 To forbehold ved porten

* **P2 er ikke målt.** OpenAlex' fulltekstarkiv oppgir 50 mill. PDF-er og ~43 mill. GROBID-parsede TEI-filer, adressert med UUID via et daglig Parquet-manifest. Tilgang krever API-nøkkel: fri nøkkel gir ~100 filer per døgn, betalt uttak $0,01 per fil. Dekningen per felt er derfor **ukjent** i dette dokumentet. For n = 100 er gratisnivået tilstrekkelig på ett døgn og betalt uttak koster ~$1. **Eier må velge nivå før trekking**; ingen nøkkel er opprettet.
* **P2-kvalitet er ikke JATS-kvalitet.** OpenAlex oppgir selv at «a meaningful share of files will contain errors — missing or duplicated references», og at GROBID ikke kan parse skannede eller rene bilde-PDF-er. ADR-0002 antar rå seksjonsetiketter fra kilden; det holder for P1, ikke for P2 og P3, der etiketten er avledet av en parser. Rute må derfor stå ved siden av seksjonsetiketten i all rapportering.

---

## 4 Verifiserte emne-ID-er

**Godkjenningsregel.** En ID godtas bare hvis alle fem kontrollarbeidene ligger i feltet, eller er metodeverktøy publisert for og brukt av feltet. Kontrollarbeidene er de fem mest siterte **innenfor PREREG-vinduet 2015–2020**. Over all tid domineres humaniora-topics av klassiske monografier — T14170 ga Geertz' «The Interpretation of Cultures» som mest sitert — og kriteriet blir da uten informasjon om hva topicet inneholder i perioden som måles.

**Fritekstoppslag er forkastet som metode.** «power system modeling» mot `/topics` ga T11270 «Complex Systems and Time Series Analysis», et annet fagfelt. ID-ene under er funnet ved `group_by=primary_topic.id` over feltnære søk, og deretter kontrollert enkeltvis.

### 4.1 historisk tekstvitenskap / diplomatisk kildeutgivelse

Tre ID-er. Ingen enkelt topic dekker feltet: OpenAlex skiller middelalderstudier, klassisk antikkvitenskap og orientalsk filologi, og kildeutgivelse ligger spredt i alle tre.

| ID | display_name (ordrett) | subfield | field | domain |
|---|---|---|---|---|
| T10595 | Medieval Literature and History | Classics | Arts and Humanities | Social Sciences |
| T10165 | Classical Antiquity Studies | Anthropology | Social Sciences | Social Sciences |
| T14210 | Historical and Linguistic Studies | Sociology and Political Science | Social Sciences | Social Sciences |

**T10595** — kontrollarbeider: «Forms: Whole, Rhythm, Hierarchy, Network» (2016); «Christian Rite and Christian Drama in the Middle Ages» (2019); «The making of English law: King Alfred to the twelfth century» (2016); «Medieval English Literature» (2016); «History, Frankish Identity and the Framing of Western Ethnicity, 550–850» (2015). 5/5 middelalderstudier.

**T10165** — kontrollarbeider: «Attica. Unknown provenance. Foedus Atheniensium et Lacedaemoniorum, a. 265/4a.» (2016, en epigrafisk kildeutgivelse); «The history of the decline and fall of the Roman Empire» (2019); «The Presocratic Philosophers» (2018); «Ekphrasis, Imagination and Persuasion in Ancient Rhetorical Theory and Practice» (2016); «Lexicon Iconographicum Mythologiae Classicae» (2016). 5/5 klassisk antikkvitenskap, med kildeutgivelse øverst.

**T14210** — kontrollarbeider: «The Old Testament Pseudepigrapha» (2019); «Bibliotheca Orientalis» (2018); «Paul and Palestinian Judaism» (2017); «A Grammar of the Arabic Language» (2019); «Pause and Effect» (2016, om tegnsettingens historie i vestlige håndskrifter). 5/5 historisk-filologiske studier.

Vurdert og forkastet: **T14170** Classical Studies and Philology (3/5 — Geertz og en Seneca-biografi utenfor feltet, selv om topicet er det eneste med «Textual Criticism» blant nøkkelordene); **T12377** Digital Humanities and Scholarship (1/5 — vitenskapsteori dominerer); **T11657** Digital and Traditional Archives Management (0/5 — arkivvitenskap og datastyring, ikke kildeutgivelse); **T10362** Biblical Studies and Interpretation (0/5 — religionsvitenskap).

### 4.2 klinisk epidemiologi / journalgjennomgang

To ID-er, og feltet er det svakest operasjonaliserte av de fire. **OpenAlex' taksonomi er sykdomsorganisert, ikke metodeorganisert:** det finnes ikke noe topic for «journalgjennomgang» eller «klinisk epidemiologi» som metode. Søk på «retrospective chart review» grupperer til COVID-19, tuberkulose og HIV — sykdommer, ikke framgangsmåte. De to ID-ene er valgt fordi de fanger forskning **på journal- og registerdata**, som er der H8 (tilgang, juss, etikk, samtykke) faktisk oppstår.

| ID | display_name (ordrett) | subfield | field | domain |
|---|---|---|---|---|
| T11095 | Emergency and Acute Care Studies | Emergency Medicine | Medicine | Health Sciences |
| T10556 | Global Cancer Incidence and Screening | Oncology | Medicine | Health Sciences |

**T11095** — kontrollarbeider: «The Danish National Patient Registry: a review of content, data quality…» (2015, mest sitert i vinduet); «Diagnosis and Treatment of Adults with Community-acquired Pneumonia» (2019); «Emergency department crowding: A systematic review of causes, consequences» (2018); «Part 8: Post–Cardiac Arrest Care» (2015); «Impact of the COVID-19 Pandemic on Emergency Department Visits — United States» (2020). 5/5 klinisk tjeneste- og registerforskning.

**T10556** — kontrollarbeider: «Global cancer statistics 2018: GLOBOCAN…» (2018); «Global cancer statistics, 2012» (2015); «Cancer statistics, 2020»; «Cancer statistics, 2019»; «Cancer statistics in China, 2015» (2016). 5/5 registerbasert kreftepidemiologi.

Vurdert og forkastet: **T10350** Electronic Health Records Systems (4/5 — «Mobile App Rating Scale» utenfor; topicet er helseinformatikk, ikke klinisk epidemiologi); **T10845** Advanced Causal Inference Techniques (3/5 — to av fem er økonometri); **T10261** Genetic Associations and Epidemiology (annet felt: genomikk, UK Biobank); **T12790** Nursing Diagnosis and Documentation (0/5 — forskningsmetode i sykepleie); **T10391** Healthcare Policy and Management (0/5 — helseøkonomi).

**Dette er et feltvalg eier må ta stilling til**, jf. §8.

### 4.3 arkeologi

To ID-er.

| ID | display_name (ordrett) | subfield | field | domain |
|---|---|---|---|---|
| T10421 | Pleistocene-Era Hominins and Archaeology | Anthropology | Social Sciences | Social Sciences |
| T10087 | Archaeology and ancient environmental studies | Paleontology | Earth and Planetary Sciences | Physical Sciences |

**T10421** — kontrollarbeider: «SHCal20 Southern Hemisphere Calibration, 0–55,000 Years cal BP» (2020); «New fossils from Jebel Irhoud, Morocco and the pan-African origin of Homo sapiens» (2017); «Human occupation of northern Australia by 65,000 years ago» (2017); «3.3-million-year-old stone tools from Lomekwi 3, West Turkana, Kenya» (2015); «bModelTest: Bayesian phylogenetic site model averaging and model comparison» (2017). 5/5, der kalibreringskurve og fylogeniprogramvare er metodeverktøy publisert for og brukt av feltet.

**T10087** — kontrollarbeider: «The IntCal20 Northern Hemisphere Radiocarbon Age Calibration Curve» (2020); «Massive migration from the steppe was a source for Indo-European languages in Europe» (2015); «Ancient DNA and the rewriting of human history» (2016); «Marine20 — The Marine Radiocarbon Age Calibration Curve» (2020); «SHCal20 Southern Hemisphere Calibration» (2020). 5/5 arkeometri og arkeogenetikk.

Vurdert og forkastet: **T13621** Ancient and Medieval Archaeology Studies (3/5 — «Scheffer/Schachtschabel Lehrbuch der Bodenkunde» og kvartærgeologi innenfor topicet); **T13372** Archaeology and Historical Studies (antikkhistorie, ikke arkeologisk praksis).

Merk: begge de godkjente ID-ene ligger utenfor subfeltet «Archeology». De to topicene som *har* det subfeltet, blander inn antikkhistorie og jordbunnslære. Feltet nås gjennom Anthropology og Paleontology, ikke gjennom taksonomiens eget arkeologi-subfelt.

### 4.4 energisystemmodellering

Tre ID-er. **Sammensetningen er bundet av den positive kontrollen**, ikke valgt fritt.

| ID | display_name (ordrett) | subfield | field | domain |
|---|---|---|---|---|
| T10424 | Electric Power System Optimization | Electrical and Electronic Engineering | Engineering | Physical Sciences |
| T11185 | Integrated Energy Systems Optimization | Electrical and Electronic Engineering | Engineering | Physical Sciences |
| T11941 | Power System Reliability and Maintenance | Safety, Risk, Reliability and Quality | Engineering | Physical Sciences |

**T10424** — kontrollarbeider: «Long-term patterns of European PV output using 30 years of validated hourly reanalysis» (2016); «Using bias-corrected reanalysis to simulate current and future wind power output» (2016); «Probabilistic electric load forecasting: A tutorial review» (2016); «A review of deep learning for renewable energy forecasting» (2019); «Probabilistic energy forecasting: Global Energy Forecasting Competition 2014» (2016). 5/5.

**T11185** — kontrollarbeider: «Net-zero emissions energy systems» (2018); «Review of energy system flexibility measures to enable high levels of variable renewable electricity» (2015); «Using bias-corrected reanalysis to simulate current and future wind power output» (2016); «Direct utilization of geothermal energy 2015 worldwide review» (2016); «Achieving a 100% Renewable Grid» (2017). 5/5.

**T11941** — kontrollarbeider: «Genetic algorithm solution to unit commitment problem» (2016); «The Grid: Stronger, Bigger, Smarter?» (2015); «Metrics and Quantification of Operational and Infrastructure Resilience in Power Systems» (2017); «Power System Resilience to Extreme Weather» (2016); «Power System Dynamic State Estimation» (2019). 5/5.

**Kontrollbindingen.** Den positive kontrollen i PREREG §7 (10.1016/j.apenergy.2018.04.048) har T11941 som `primary_topic`, med T10424 (score 0,994) og T14276 som øvrige topics. **T11185 er ikke blant dem.** Hadde feltet blitt operasjonalisert med T11185 alene — det topicet et fritekstsøk på «energy system modelling» peker mot — ville den positive kontrollen falt utenfor rammen, og kontrollen i §7 vært umulig å gjennomføre. Rammen er verifisert: `topics.id:T10424|T11185|T11941,publication_year:2015-2020` med kontrollens DOI gir treff = 1.

---

## 5 Hentbarhetstabell

Alle tall målt 2026-09-12, år 2015–2020, med ID-ene i §4. Rådata i `data/raw/` med sha256 i MANIFEST.md.

| felt | R0 alle | R1 `has_fulltext` | R2 R1∧OA | R3 PDF (est.) | R3/R1 | R4 JATS (est.) |
|---|---|---|---|---|---|---|
| tekstvitenskap | 323 363 | 32 343 | 32 101 | **46 888** | **1,45** | **0** |
| klinisk epidemiologi | 84 255 | 26 904 | 26 830 | **32 017** | **1,19** | 12 166 |
| arkeologi | 98 954 | 17 393 | 17 158 | **18 306** | **1,05** | 2 953 |
| energimodellering | 75 311 | 18 516 | 18 409 | **20 711** | **1,12** | **0** |

Til sammenligning, den nye rammens tellbare størrelse (§3.1, `open_access.is_oa:true` uten `has_fulltext`): tekstvitenskap 66 830; klinisk epidemiologi 43 986; arkeologi 37 510; energimodellering 30 362.

### 5.1 Hvordan R3 og R4 er målt

**R3 er et estimat, ikke en telling.** `best_oa_location.pdf_url` er ikke filtrerbart, så andelen er målt på et frøsatt utsnitt (`sample=200`, `seed=734248`) av R0 og ganget opp mot R0. Wilson-intervall, 95 %:

| felt | andel med PDF-lenke i R0 | 95 %-intervall | R3-intervall | andel i R1 |
|---|---|---|---|---|
| tekstvitenskap | 14,5 % | 10,3–20,0 % | 33 300–64 700 | 93,5 % |
| klinisk epidemiologi | 38,0 % | 31,6–44,9 % | 26 600–37 800 | 95,5 % |
| arkeologi | 18,5 % | 13,7–24,5 % | 13 600–24 200 | 94,0 % |
| energimodellering | 27,5 % | 21,8–34,1 % | 16 400–25 700 | 95,0 % |

Den siste kolonnen er poenget i §2.3: nesten alle `has_fulltext`-verk har også PDF-lenke, men PDF-lenke finnes for mange flere verk enn `has_fulltext` fanger.

**R4 er målt på DOI-oppslag i Europe PMC**, på de verkene i R0-utsnittet som har PDF-lenke og DOI: 25 (tekstvitenskap), 50 (klinisk epidemiologi), 31 (arkeologi), 48 (energimodellering). Kriteriet er `pmcid` finnes ∧ `inEPMC=Y` ∧ `isOpenAccess=Y`. Andel med JATS: 0 %, 38,0 % [25,9–51,8 %], 16,1 % [7,1–32,6 %], 0 %.

### 5.2 Nullresultatene i R4 er armert

To felt fikk 0 treff. Et nullresultat teller ikke før en streng som må treffe har truffet, så begge kjøringene ble gjentatt med en kjent Europe PMC-artikkel (10.1186/s12874-016-0165-8) lagt inn i samme forespørselssett:

* tekstvitenskap: kontrollen traff (PMC4875724), feltets egne 0/25.
* energimodellering: kontrollen traff (PMC4875724), feltets egne 0/48.

JATS-endepunktet ble verifisert med statuskode uten å laste ned innhold: 200 for fire faktiske PMC-treff, 404 for en oppdiktet PMCID. En tidligere måling ga 406 for alle — årsaken var `Accept: application/json` mot et XML-endepunkt i vår egen klient, altså et falskt negativt, rettet før tallene over ble fastsatt.

**Følgen:** Europe PMC dekker biomedisin. For historisk tekstvitenskap og energisystemmodellering finnes JATS-ruten ikke. ADR-0002 forutsetter rå seksjonsetiketter fra kilden; i to av fire felt må etiketten avledes av en parser (P2/P3). Det er ikke det samme, og skal ikke rapporteres som om det var.

---

## 6 Substitusjonsregel

Rammen i §3.1 er tellbar; hentbarhet avgjøres først når verket forsøkes hentet. Avstanden mellom de to er et måltall, ikke et problem som skal skjules.

1. **Reserveliste.** Ved trekking trekkes ikke 25, men hele feltets frosne rammeliste stokkes med `random.Random(93883171)`. De 25 første er utvalget; resten er reservelisten, i den rekkefølgen stokkingen ga.
2. **Utløsende årsaker.** Et trukket verk substitueres når, og bare når, alle tre portene i §3.2 feiler. Årsaken føres ordrett i én av disse kategoriene:
   * `ingen_rute` — hverken JATS, TEI eller PDF-lenke finnes
   * `pdf_utilgjengelig` — lenken finnes, men svarer 403/404/betalingsmur
   * `lisens` — lisensen tillater ikke lagring (ADR-0001)
   * `parse_feilet` — filen finnes, men gir ingen brukbar tekst (skannet PDF, GROBID-feil)
   * `ikke_artikkel` — verket er errata, innholdsfortegnelse, anmeldelse eller lignende
3. **Erstatning.** Neste verk i reservelisten for **samme felt** tas inn. Aldri fra et annet felt, aldri ved nytt trekk, aldri ved nytt frø.
4. **Logg.** Hver substitusjon loggføres med: posisjon i utvalget, erstattet work-ID, erstattende work-ID, posisjon i reservelisten, årsakskategori, tidspunkt. Loggen er en del av resultatet.
5. **Rapportering.** **Antall substitusjoner per felt oppgis som eget tall, sammen med prevalenstallet.** Det måler avstanden mellom rammen og virkeligheten. Et felt som trengte 40 substitusjoner for å fylle 25 plasser, har en annen troverdighet enn et felt som trengte 2 — selv om prevalenstallet er likt.
6. **Stoppregel.** Overstiger antall substitusjoner antall plasser i et felt (>25), stopper innsamlingen for feltet og tallet rapporteres som det er. Rammen er da gal, og skal korrigeres i et nytt addendum, ikke kompenseres bort.

---

## 7 Korrigert korpusgrense

PREREG §4 oppgir at fulltekst finnes for 52 249 064 av 326 944 662 works (16 %). **Det tallet gjelder indekserte verk, ikke hentbare.** Det er `has_fulltext`-tellingen, altså kriteriet som forkastes i §2.

Ved siden av den skal hentbar andel stå:

**Globalt, fra OpenAlex' egne oppgitte tall om fulltekstarkivet:**

| mål | antall | andel av 326 944 662 |
|---|---|---|
| indeksert for søk (`has_fulltext`, PREREG §4) | 52 249 064 | 16,0 % |
| PDF i OpenAlex' fulltekstarkiv | ~50 000 000 | ~15,3 % |
| GROBID-parset TEI XML i arkivet | ~43 000 000 | ~13,2 % |

**Per felt, målt i vinduet 2015–2020 (§5):** andel av alle verk i feltet som har PDF-lenke: tekstvitenskap 14,5 %, klinisk epidemiologi 38,0 %, arkeologi 18,5 %, energimodellering 27,5 %. Andel av de PDF-hentbare som i tillegg har ekte JATS: 0 %, 38,0 %, 16,1 %, 0 %.

Formuleringen som skal følge all rapportering, utvidet fra PREREG §4:

> Verktøyet sveiper åpen fulltekst, ikke litteraturen. Av verkene i et felt er 15–38 % hentbare som PDF i 2015–2020-vinduet, og i to av fire felt finnes ingen forlagsmerket JATS i det hele tatt. Skjevheten er mot nyere, engelskspråklig og open access; humaniora publiserer i monografi og er tynnest dekket.

---

## 8 Til eier, før trekking

To valg gjenstår, og ingen av dem kan tas av den som utfører målingen:

1. **Feltet «klinisk epidemiologi / journalgjennomgang» (§4.2).** OpenAlex har ikke et metodetopic for journalgjennomgang. T11095 og T10556 fanger forskning på journal- og registerdata, som er der H8 oppstår, men de er sykdoms- og tjenesteorganiserte, ikke metodeorganiserte. Alternativene er å godta disse to, å bytte felt, eller å definere feltet på en annen akse enn topics.
2. **P2-tilgang (§3.3).** Fri API-nøkkel gir ~100 filer per døgn, betalt uttak $0,01 per fil. Uten P2 er to av fire felt henvist til egen PDF-parsing. Ingen nøkkel er opprettet.

Ingen felt faller på volum: alle fire har titusener av hentbare verk i vinduet, mot n = 25 per felt. Grensen er rutene, ikke mengden.

---

## 9 Erklæring

* **Ingen trekking av utvalg er utført.** Ingen rammeliste er frosset, ingen work-ID er valgt til utvalget.
* **Ingen artikler er lest.** Alt i dette dokumentet er metadata, tellinger og statuskoder. Ingen fulltekst er hentet: PDF-lenker og XML-endepunkter er telt, aldri lastet ned.
* **Ingen utfallsdata er sett.** Ingen setning er vurdert for parkerte spørsmål, ingen hindringsklasse er tildelt.
* **PREREG-v1.md er uendret**, sha256 `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`.
* Prereg-frøet er ikke brukt til noen måling i dette dokumentet; dekningsmålingene bruker `2ef3dee8` / 734 248.
* ADDENDUM-02 (eksempelsetninger per klasse, positive kontroller for de tre øvrige feltene) er ikke skrevet. Trekking skjer ikke før den er det.
