# ADDENDUM-02 — kontroller, rubrikkankere og rammediagnostikk

**Skrevet:** 2026-09-12
**Hører til:** PREREG-v1.md, sha256 `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`
og ADDENDUM-01.md, sha256 `aa78d1be50ac17f8e26a92513aa115b3d504bdde3556e43b4f2317ea47cc255f`
**Status:** operasjonalisering etter lås. Skrevet før trekking. Ingen av de to låste filene er endret.

---

## 1 Kontrollene ligger utenfor nevneren

**M1 og M2 regnes utelukkende på de 100 tilfeldig trukne.** Positive kontroller kodes separat, føres separat og inngår i ingen prevalensnevner eller -teller.

PREREG §7 sier at den positive kontrollen «legges inn i energiutvalget». Det presiseres her, fordi den ordlyden gjør porten selvbekreftende: en kjent treffer blant 25 hever feltets prevalens med fire prosentpoeng av konstruksjon, mot en terskel i PREREG §6 som skiller ved fem prosent. Et felt uten et eneste ekte treff ville dermed så vidt bestå «sporet parkeres»-porten på kontrollen alene.

Kontrollene har én oppgave: å vise at rubrikken koder et kjent treff som treff. De måler rubrikken, ikke litteraturen.

**Følger av dette:**

1. Kontrollene fjernes fra rammelisten **før** trekking, slik at de ikke kan trekkes inn i de 100.
2. **Alle verk som er lest under arbeidet med å finne kontroller, fjernes også.** I denne slyngen er 56 artikler åpnet og gjennomsøkt for kandidatsetninger. Listen ligger i `data/leste-kontrollkandidater.json` med felt, DOI og PMCID, og er en del av utvalgsgrunnlaget: et verk eieren alt har sett, kan ikke være en blind observasjon. Antallet fjernede verk oppgis sammen med prevalenstallet.
3. Kontrollkodingen rapporteres i egen tabell, med samme felter som utvalgskodingen, og med teksten «ikke i M1/M2» i overskriften.

---

## 2 Positive kontroller, én per felt

Krav til en kontroll: innenfor feltets ramme og vinduet, hentbar, og med en setning der forfatteren navngir noe de ikke fikk gjort **og** oppgir hindringen.

| felt | DOI | klasse | seksjon setningen står i | `section_label_provenance` |
|---|---|---|---|---|
| energimodellering | 10.1016/j.apenergy.2018.04.048 | — se §2.4 | **ikke verifisert** | ikke verifisert |
| klinisk epidemiologi | 10.1016/s2468-2667(17)30217-7 | **H8** | `Discussion` | `source` |
| arkeologi | 10.1038/s41467-019-11357-9 | **H7** | `AMS radiocarbon dating` | `source` |
| historisk tekstvitenskap | **ingen funnet** — se §2.5 | — | — | — |

### 2.1 Klinisk epidemiologi — 10.1016/s2468-2667(17)30217-7

Den parkerte setningen, i diskusjonsseksjonen: forfatterne kunne ikke måle kontinuitet i lege–pasientforholdet, og oppgir hvorfor — «**we were unable to measure continuity of care with specific general practitioners**», begrunnet med begrensninger som følger av datakonfidensialitet.

Klasse **H8** (tilgang, juss, etikk, samtykke). Hindringen er konfidensialitetsregimet rundt journaldata, ikke ressurser eller evne. Løftbarhet er dermed `nei` ved oppslag i PREREG §5, og kontrollen tester derfor også at rubrikken kan kode et treff som **ikke** er løftbart — jf. ADR-0004, der de to spørsmålene skal holdes atskilt. Klassen sammenfaller med PREREG §4, som fester dette feltet som det der H8 dominerer.

Hentet som JATS fra Europe PMC (PMCID via DOI-oppslag), seksjonsetikett fra kildens egen `<sec>`-merking, altså `source`.

### 2.2 Arkeologi — 10.1038/s41467-019-11357-9

Den parkerte setningen, i en resultatseksjon om AMS-datering: «**We were unable to generate a radiocarbon date for individual I3401**», med hindringen oppgitt i samme setning — det var ikke nok beinpulver igjen til analysen.

Klasse **H7** (dataene fantes ikke). Det fysiske materialet var oppbrukt. Løftbarhet `nei`.

At seksjonen er en resultatseksjon og ikke limitations, er en andre, uavhengig forekomst av mønsteret ADR-0002 er bygget rundt. Hentet som JATS, `source`.

### 2.3 Merknad om klassene i de to verifiserte kontrollene

Begge er H7/H8, altså ikke-løftbare klasser. Det er tilsiktet så langt det gikk: kontrollene skal vise at rubrikken finner **treff**, og løftbarhet avledes uansett fra tabellen, aldri fra lesningen. Men det betyr at ingen av de verifiserte kontrollene tester rubrikken på en løftbar klasse (H1–H6). **Eier bør legge til minst én kontroll i H1–H4 før koding**, ellers er rubrikkens løftbare ende uprøvd.

### 2.4 Energikontrollen kunne ikke verifiseres i denne slyngen

DOI-en er gitt i PREREG §7 og ligger innenfor rammen (verifisert i ADDENDUM-01 §4.4: rammen med kontrollens DOI gir treff = 1). Seksjon og provenance står likevel som **ikke verifisert**, av en målt grunn:

* Europe PMC har ingen JATS for feltet (ADDENDUM-01 §5.2: 0 av 48), så P1 finnes ikke.
* `best_oa_location.pdf_url` peker på `sciencedirect.com/.../pdf`. Forsøk 2026-09-12: **HTTP 403**, 832 805 byte HTML i stedet for PDF. P3 feiler.

Verket er CC-BY og registrert som åpent. **Lenken finnes, filen er ikke hentbar.** Det er samme tilstand som substitusjonsregelen i ADDENDUM-01 §6 kaller `pdf_utilgjengelig`, og det gjelder her selve den positive kontrollen.

To følger, som skal stå i rapporteringen:

1. **R3 i ADDENDUM-01 §5 er en øvre grense.** Den teller registrerte PDF-lenker, ikke nedlastbare filer. Hvor stor andel av lenkene som faktisk svarer, er ikke målt.
2. Når energikontrollens tekst omsider hentes — via P2 (OpenAlex' TEI) eller egen parsing — blir seksjonsetiketten `parser`. Påstanden «den avgjørende setningen sto i en resultatseksjon» vil for dette verket hvile på GROBID, ikke på forlagets merking. Etter ADR-0007 punkt 4 rapporteres den derfor i `parser`-kolonnen.

### 2.5 Historisk tekstvitenskap — ingen kontroll funnet

Søkt innenfor rammen med `fulltext.search` på åtte formuleringer («we were unable to», «too time-consuming», «we did not have access to», «prohibitively», «illegible», «too fragmentary», «not been digitised», «uncatalogued»), og 22 engelskspråklige kandidater med PDF-lenke ble lastet ned og gjennomsøkt. Ingen av dem inneholder en setning som oppfyller kravet: de nærmeste treffene navngir noe ugjort uten å oppgi hindringen.

De to nærmeste, ført her slik at neste slynge ikke gjentar arbeidet:

* 10.5282/journalipp/4841 — «**we were unable to consult the work**». Hindringen er ikke oppgitt; verket var kjent gjennom andres sitater.
* 10.1515/sm-2017-0003 — «**we were unable to reach an exact official number of Assyrians**». Hindringen er ikke oppgitt.

En kontroll som ikke utvetydig er et treff, kan ikke brukes: PREREG §7 sier at hvis rubrikken ikke koder kontrollen som treff, er rubrikken feil og alt stopper. En tvetydig kontroll ville utløse den stoppregelen på feil grunnlag. **Posten står åpen.**

Funnet er samtidig informasjon om feltet: der H1–H2 var ventet å dominere, er indeksert fulltekst så tynn (ADDENDUM-01 §2.2: 7,4–14,4 % i vinduet) at det ikke lot seg finne én kvalifiserende setning gjennom fraseindeksen. Det er en grunn til å vente lav målt M1 i feltet uavhengig av hvor mange parkerte spørsmål som faktisk står der.

---

## 3 Rubrikkankere: to eksempelsetninger per klasse

Alle ankere er hentet fra litteratur **utenfor de fire feltrammene**, verifisert i kildens egen JATS via Europe PMC. Ett sitat per kilde, hvert under femten ord. Klassedefinisjonene står i PREREG §5 og endres ikke her.

**Utvalgsregelen for ankere:** kilden er publisert **utenfor vinduet 2015–2020**. Da kan den ikke havne i utvalget uansett emne, og rammetilhørigheten trenger ikke sjekkes verk for verk. Tre ankere bryter regelen og er merket ⚠ — de er fra 2017 og 2019, og rammetilhørigheten er **ikke** verifisert, fordi OpenAlex-kvoten var oppbrukt (§8.2). De må kontrolleres eller byttes før bruk.

### H1 — menneskelig lesning eller koding i skala *(løftbar: ja)*

1. 10.1136/bmjopen-2026-121412 (2026), `Discussion`: «As manual review of all records was not feasible» — og en proxy ble brukt i stedet.
2. 10.1038/s41538-026-00909-1 (2026), `Introduction`: «purely manual curation is not feasible» — begrunnet med datamengde og inkonsistent terminologi.

### H2 — lesbarhet: håndskrift, skadet kilde, lyd *(ja)*

1. 10.1371/journal.pone.0324106 (2025), `Object labels.`: «caregiver utterances were inaudible, or not clear enough for the coders to transcribe».
2. ⚠ 10.1371/journal.pone.0226257 (2019), `Details and Plausibility`: «Parts of two recordings were inaudible, and therefore could not be properly transcribed».

### H3 — språkbarriere *(ja, med forbehold)*

1. 10.1007/s13659-023-00424-w (2024), `Limitations`: «This language barrier prevented us from accessing potentially relevant research articles».
2. 10.3390/jcm13175100 (2024), `4. Discussion`: «the language barrier prevented us from enrolling the children and parents».

### H4 — mønster i bilder eller signaler i volum *(ja)*

1. 10.1186/s12938-026-01535-4 (2026), `Background and objectives`: «manual segmentation is time-consuming and impractical for large data sets».
2. 10.1097/scs.0000000000012681 (2026), `Abstract`: «manual segmentation is time-consuming and may depend on the radiologist's experience».

**Svakhet, ført åpent:** begge H4-ankerne er hindringsformuleringer i en metodebegrunnelse, ikke fullstendige treffsetninger der forfatteren navngir noe de selv ikke fikk gjort. Fem søkeformuleringer rettet mot den fulle formen ga null treff i Europe PMC utenfor vinduet. H4 er derfor det svakest ankrede klassen, og en annen koder vil trenge mer enn disse to.

### H5 — simulering og regnekraft *(delvis)*

1. 10.1093/bioadv/vbae098 (2024), `2.3 SNP calling and thinning`: «some analyses are computationally prohibitive to run across the entire genome».
2. 10.3390/e26090722 (2024), `2. Quantum Equation of Motion`: «attaining the desired accuracy swiftly becomes computationally prohibitive».

### H6 — strukturslutning fra sekvens *(ja)*

1. 10.1021/acsmaterialslett.4c00400 (2024): «the guest structure could not be resolved due to substantial positional disorder».
2. 10.1002/advs.202409275 (2025), `Microstructural Evolution`: «their crystal structure could not be resolved due to their small size».

**Svakhet, ført åpent:** PREREG §5 definerer H6 som strukturslutning **fra sekvens**. Begge ankerne handler om eksperimentell strukturbestemmelse (diffraksjon, oppløsning), ikke om å slutte struktur fra en sekvens. De viser formen «strukturen lot seg ikke bestemme, og hindringen er oppgitt», men ikke klassens egentlige akse. Eier bør erstatte dem med tilfeller der en sekvens fantes og strukturen ikke kunne utledes.

### H7 — dataene fantes ikke *(nei)*

1. 10.1038/s41467-023-42247-w (2023), `DNA extraction`: «Insufficient material remained from the small molecule extraction to enable DNA extraction».
2. ⚠ 10.1016/j.neo.2017.01.003 (2017), `Discussion`: «18 cases were excluded because insufficient material remained on the tissue blocks».

### H8 — tilgang, juss, etikk, samtykke *(nei)*

1. 10.3390/biomedicines11020242 (2023), `Data Availability Statement`: «Ethical approval did not permit sharing of GS data».
2. 10.1186/s13073-023-01156-9 (2023): «the ethical approval did not permit the sharing of raw genotype data».

### H9 — begrepet eller teorien manglet *(nei)*

1. 10.3390/cancers14246194 (2022), `3. PSMA PET in the Setting…`: «No consensus definition exists for OMPC».
2. 10.1155/2022/9957190 (2022), `1. Introduction`: «No consensus definition exists for treatment-resistant depression».

### N1 — besvart i samme artikkel

1. 10.1021/jacsau.2c00576 (2023), `Reaction Mechanisms…`: «We address this question below».
2. 10.1007/s10519-020-10035-7 (2021), `The Twin Model with Polygenic…`: «We address this question below».

Merk formen: spørsmålet reises og besvares i samme tekst. Kodes N1, aldri som treff.

### N2 — nyhetspåstand

1. 10.12701/jyms.2024.01137 (2025), `Abstract`: «To the best of our knowledge, this is the first report on the association».
2. 10.1016/j.radcr.2024.11.066 (2025), `Abstract`: «To the best of our knowledge, this is the first recorded instance».

### N3 — omfangsvalg uten navngitt hindring

1. 10.1016/j.dib.2024.111152 (2024), `Data Description`: «Detailed information on the annotation types is beyond the scope of this paper».
2. 10.36834/cmej.79242 (2024): prosessen og leveringsmåten for et læreplansforslag «are beyond the scope of this paper».

Merk skillet mot H-klassene: N3 sier hva teksten ikke handler om, uten å navngi noe som hindret forfatteren. Mangler hindringen, er det N3 — også når setningen ellers ser ut som en innrømmelse.

### 3.1 Hvor mange ankere som faktisk holder

| klasse | to ankere | anmerkning |
|---|---|---|
| H1, H3, H5, H8, H9, N1, N2, N3 | ja | ingen |
| H2, H7 | ja | ett anker hver ⚠ i vinduet, rammetilhørighet uverifisert |
| H4 | formelt ja | begge er hindringsformuleringer, ikke treffsetninger |
| H6 | formelt ja | begge treffer strukturbestemmelse, ikke sekvens→struktur |

Åtte av tolv klasser er fullt ankret. Det oppgis slik, fordi en rubrikk som utgir seg for å være ferdigankret der den ikke er, flytter feilen til annotøren.

---

## 4 Rammen ble formet av den positive kontrollen

Energifeltets ID-er er T10424, T11185 og T11941. To av dem er valgt **fordi** den positive kontrollen ellers falt utenfor: kontrollen har T11941 som `primary_topic` og T10424 blant sine øvrige topics, mens T11185 — det topicet et fritekstsøk på «energy system modelling» peker mot — ikke er blant dem (ADDENDUM-01 §4.4).

**Konsekvens som skal stå i enhver rapportering av energifeltet:**

> Kontrollen tester rubrikken, ikke rammevalget. Den kan ikke siteres som belegg for at rammen er godt valgt, siden rammen ble utvidet for å inneholde den.

Rammen for de tre øvrige feltene er ikke formet av noen kontroll, og for tekstvitenskap finnes ingen kontroll i det hele tatt (§2.5). Sammenligning mellom feltene arver derfor en asymmetri: ett felt har en ramme tilpasset et kjent treff, tre har ikke.

---

## 5 OA-betingelsen er en seleksjon

Rammen i ADDENDUM-01 §3.1 krever `open_access.is_oa:true`. Det er en lagringsrettslig nødvendighet (ADR-0001), og samtidig en seleksjon som endrer hva M1 er et tall om.

**Formuleringen som skal stå i sammendraget av enhver rapportering, ved siden av én-koder-svakheten:**

> M1 er prevalens av parkerte spørsmål i **åpent tilgjengelig litteratur innenfor fire formålsvalgte emnerammer, 2015–2020** — ikke i litteraturen. Designet har én koder. Begge forholdene begrenser hva tallet kan brukes til.

Retningen på skjevheten er ukjent og skal ikke gjettes. Det er ingen grunn til å tro at forfattere som publiserer åpent, innrømmer parkerte spørsmål i samme takt som andre — i noen fag følger åpen publisering finansiører med egne rapporteringskrav, i andre er den knyttet til tidsskriftsjikt. Antakelsen «OA er et tilfeldig utsnitt» gjøres ikke.

---

## 6 Årsskjevheten i vinduet

Antall works per år på rammen i ADDENDUM-01 §3.1, målt 2026-09-12:

| felt | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | sum |
|---|---|---|---|---|---|---|---|
| tekstvitenskap | 9 436 | 9 955 | 10 646 | 11 196 | 12 026 | 13 571 | 66 830 |
| klinisk epidemiologi | 5 924 | 6 207 | 6 813 | 7 178 | 7 888 | 9 976 | 43 986 |
| arkeologi | 5 001 | 5 258 | 5 695 | 6 628 | 6 818 | 8 110 | 37 510 |
| energimodellering | 3 427 | 3 859 | 4 765 | 5 215 | 6 132 | 6 964 | 30 362 |

Som andel av feltets ramme:

| felt | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2019+2020 | 2020/2015 |
|---|---|---|---|---|---|---|---|---|
| tekstvitenskap | 14,1 % | 14,9 % | 15,9 % | 16,8 % | 18,0 % | 20,3 % | **38,3 %** | 1,44 |
| klinisk epidemiologi | 13,5 % | 14,1 % | 15,5 % | 16,3 % | 17,9 % | 22,7 % | **40,6 %** | 1,68 |
| arkeologi | 13,3 % | 14,0 % | 15,2 % | 17,7 % | 18,2 % | 21,6 % | **39,8 %** | 1,62 |
| energimodellering | 11,3 % | 12,7 % | 15,7 % | 17,2 % | 20,2 % | 22,9 % | **43,1 %** | 2,03 |

**Forventet fordeling av 25 trukne**, avrundet: 3–4 fra 2015, mot 5–6 fra 2020. Om lag ti av 25 vil ligge i 2019–2020, mot om lag sju i 2015–2016.

**Hva det betyr for tolkningen av tidsaksen.** Prosjektets spørsmål er om hindringen som ble navngitt, er opphevet i dag. Jo nyere verket, jo kortere tid har det hatt til å bli opphevet, og jo større er sjansen for at noen alt har svart uten at det er synlig i siteringsgrafen ennå. Skjevheten mot 2019–2020 trekker derfor i to retninger samtidig: den øker andelen kandidater der hindringen nettopp er falt bort (AI-verktøyene kom etter 2020), og den øker andelen der falsifiseringstesten i PREREG §8 har for kort fartstid til å finne svaret.

Følger:

1. **Publiseringsår rapporteres sammen med hvert kandidatutfall**, ikke bare aggregert.
2. **Overlevelsesraten i §8 oppgis per årskohort** når n tillater det, ellers med årsfordelingen for de overlevende oppgitt ved siden av. Uten det kan en høy overlevelsesrate være en ung kohort.
3. Skjevheten er ikke korrigert med vekting. Utvalget er formålsvalgt fra før (PREREG §4), og en vekting ville gi inntrykk av at rammen representerer noe den ikke representerer.

---

## 7 Overlapp mellom feltrammene

Designet i PREREG §4 forutsetter at de fire feltene har ulik hindringstype. Ligger de samme verkene i flere rammer, er forutsetningen ikke oppfylt.

`topics.id` kan telle unioner, men ikke snitt mellom to topic-lister. Alle femten delmengder er derfor telt som unioner, og snittene beregnet ved inklusjon–eksklusjon.

| par | \|A\| | \|B\| | \|A∪B\| | \|A∩B\| |
|---|---|---|---|---|
| tekstvitenskap + klinisk epidemiologi | 66 830 | 43 986 | 110 816 | **0** |
| tekstvitenskap + arkeologi | 66 830 | 37 510 | 104 200 | **140** |
| tekstvitenskap + energimodellering | 66 830 | 30 362 | 97 192 | **0** |
| klinisk epidemiologi + arkeologi | 43 986 | 37 510 | 81 496 | **0** |
| klinisk epidemiologi + energimodellering | 43 986 | 30 362 | 74 348 | **0** |
| arkeologi + energimodellering | 37 510 | 30 362 | 67 872 | **0** |

Alle fire tripler: 0. Firersnittet: 0.

| | antall |
|---|---|
| i nøyaktig 1 ramme | 178 408 |
| i nøyaktig 2 rammer | **140** |
| i nøyaktig 3 rammer | 0 |
| i nøyaktig 4 rammer | 0 |
| unionen av de fire | 178 548 |
| summen av de fire | 178 688 |

**Forutsetningen holder på dette målet.** 140 verk, 0,078 % av unionen, ligger i to rammer, og alle 140 i samme par: tekstvitenskap og arkeologi. Det er det ventede paret — antikk- og middelaldermateriale behandles av begge fag. Sannsynligheten for at et av de 140 trekkes i to felt, er forsvinnende, men trekkingen skal likevel avvise et verk som alt er trukket i et annet felt, og loggføre det som substitusjon med årsak `dobbeltramme`.

**Hva målet ikke viser.** Disjunkte rammer betyr at verkene er forskjellige, ikke at hindringstypene er forskjellige. Om de fire feltene faktisk fordeler seg ulikt på H1–H9, er et utfall, og det er ukjent før koding. Denne målingen fjerner bare den ene forklaringen som ville gjort spørsmålet meningsløst.

**En kostnad ved `topics.id` er samtidig synlig.** Filteret fanger verk der feltets topic bare er et sekundært, og det slipper inn støy: en marinbiologisk avhandling om interaksjon mellom fisk og maneter (10.5821/dissertation-2117-134622) ligger i tekstvitenskapsrammen, fordi T10165 «Classical Antiquity Studies» er tildelt den som tredje topic med score 0,940. Verket dukket opp blant kandidatene i §2.5. Andelen verk i hver ramme der ingen av feltets ID-er er `primary_topic`, er **ikke målt** — målingen ble avbrutt av kvotetaket (§8.2). Den bør gjøres før trekking, og er ett kall per felt.

Valget står fast likevel: `primary_topic.id` ville utelatt den positive kontrollen (§4). Støyen er prisen for å kunne kontrollere rubrikken i det hele tatt, og substitusjonsregelens kategori `ikke_artikkel` utvides derfor med `utenfor_felt` for verk der ingen av feltets ID-er er blant verkets tre høyest rangerte topics.

---

## 8 Tilgangsruter og kvoter

### 8.1 P2 er ikke verktøyets dokumenterte rute

OpenAlex' fulltekstarkiv (ADDENDUM-01 §3.3) kan brukes til å hente de hundre: gratisnivået på ~100 filer per døgn dekker n = 100 på ett døgn, og betalt uttak koster ~$1.

**Den dokumenterte, offentlige ruten er likevel P3: PDF fra `best_oa_location`.** Grunnen er at sveipet skal kunne kjøres av noen uten nøkkel og uten budsjett. En metode som krever konto hos én leverandør er ikke etterprøvbar for en leser som ikke har den kontoen.

Følger:

1. Metodebeskrivelsen oppgir P3 som rute. Brukes P2 for enkelte verk, føres det per dokument i `fulltext_source`, slik at en leser ser hvilke verk som ikke kan hentes på den offentlige ruten.
2. Seksjonsetiketten er `parser` for både P2 og P3 (ADR-0007). Valget mellom dem endrer kvalitet på parsingen, ikke opphavet til etiketten.
3. **§2.4 viser at P3 ikke er en garanti:** den positive kontrollens registrerte PDF-lenke svarer 403. Hvor ofte det skjer, er ikke målt, og substitusjonsloggen i ADDENDUM-01 §6 blir det første stedet tallet framkommer.
4. **Ingen nøkkel er opprettet i denne slyngen.**

### 8.2 OpenAlex' anonyme kvote er 1 000 kall

Målt 2026-09-12, ved å treffe taket: `x-ratelimit-limit: 1000`, `x-ratelimit-remaining: 0`, `retry-after: 40058` sekunder — **11,1 timer** til kvoten nullstilles. Kostnadsmodellen i de samme svarhodene er `$0,0001` per kall, `$0,1` totalt for det anonyme nivået.

Dette er en operasjonell grense prosjektet må planlegge rundt, ikke en feil:

* Diagnostikken i denne slyngen brukte opp kvoten. Støymålingen i §7 og verifiseringen av tre ankere i §3 ble stående uferdige som følge.
* **Å fryse rammelistene for trekking (ADDENDUM-01 §1) er ikke mulig på ett anonymt døgn.** Rammene har 30 362–66 830 verk; med 200 per side kreves 152–335 kall per felt, i alt om lag 1 000 kall — hele kvoten, uten margin for feilede sider.
* Valgene er: fordele frysingen over flere døgn, eller bruke en nøkkel for det leddet og oppgi det. **Frysingen er uansett et engangsarbeid hvis resultatet lagres med sha256**, slik ADDENDUM-01 §1 krever, og bør derfor gjøres én gang og arkiveres.

---

## 9 Erklæring

* **Ingen trekking av utvalg er utført.** Ingen rammeliste er frosset, ingen work-ID er valgt til de 100.
* 56 artikler er lest i arbeidet med kontroller og ankere. Alle er loggført i `data/leste-kontrollkandidater.json` og skal fjernes fra utvalgsgrunnlaget før trekking (§1).
* **PREREG-v1.md og ADDENDUM-01.md er uendret**, sha256 `05988b23…ba23a` og `aa78d1be…c255f`.
* Ingen remote, ingen push, ingen nøkkel opprettet.
* Åpne poster ved slutten av denne slyngen: positiv kontroll for historisk tekstvitenskap (§2.5); minst én kontroll i en løftbar klasse (§2.3); energikontrollens seksjon og provenance (§2.4); rammetilhørighet for tre ankere (§3); sterkere ankere for H4 og H6 (§3.1); sekundær-topic-andel per felt (§7).
