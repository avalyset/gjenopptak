# ADDENDUM-07 — Recall-sett 2: den utvidede markørlisten målt på materiale den ikke har sett

**Skrevet:** 2026-09-12
**Hører til:** PREREG-v1.md `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`,
ADDENDUM-01.md `aa78d1be50ac17f8e26a92513aa115b3d504bdde3556e43b4f2317ea47cc255f`,
ADDENDUM-02.md `7c0542c92c54a586e3b387794272bed171ee285b75c8ebe4ee8fe1fa16f6f713`,
ADDENDUM-03.md `0b577ae6c3d0278e811e674c78e4e2948be46252e5aca9c94e94466c1f985c4e`,
ADDENDUM-04.md `7f7d067b80468a7016e398d1120930c98eb8a705b0e1c0102ad97e9db42f8a9c`,
ADDENDUM-05.md `b12c85b2a731517f9d0c5742194b2b8a900177cb82d662f8bf20e7d67fef5e9d`,
ADDENDUM-06.md `0f0e9a8126804f8a8fdf185864e80612c76816c2a536cf696df29e65d8c05687`
**Status:** måling etter lås. Endrer ingen markør, ingen terskel, ingen klasse og ingen enhet. Legger to krav til høstingen (§2.2, §2.3) og retter tall i ADDENDUM-06 som ble regnet på avkortet tekst (§2.2). Skrevet før trekking og før koding. Ingen av de sju låste filene er endret.

---

## 1 Settet

### 1.1 Kilder og krav

40 dokumenter, trukket med målefrøet **734248** (ADDENDUM-01):

* **25 biomedisin og naturvitenskap fra Europe PMC.** Søket er `(FIRST_PDATE:[<dag> TO <dag>]) AND OPEN_ACCESS:Y AND IN_EPMC:Y AND LANG:eng` over 30 frøtrukne dager i 2015–2020, 25 poster per dag: en pulje på 750. Europe PMC ignorerer `page` for rene filtersøk, derfor er puljen stratifisert på dato og ikke på side. Fulltekst er JATS fra Europe PMC.
* **15 humaniora fra DOAJ.** Sju fagspørringer med 150 kandidater hver: en pulje på 1 050. Kvoten per fag er satt før lesing: historie 3, arkeologi 3, filologi 2, klassiske fag 2, religionsvitenskap 2, bibelvitenskap 2, diplomatikk og arkiv 1. Oppdraget nevnte historie, filologi, arkeologi, klassiske fag og religionsvitenskap. Bibelvitenskap og diplomatikk og arkiv ble lagt til før lesing, det siste for sjangerhullet i ADDENDUM-06 §1.5.

Kravene håndheves før lesing, per kandidat, i frørekkefølge. De første som oppfyller alle krav, utgjør settet:

1. publiseringsår 2015–2020;
2. ikke i `data/recall-sett.jsonl`, ikke i `data/leste-kontrollkandidater.json`, ikke funnet ved frasesøk (utelukkelsesliste: 130 OpenAlex-verk, 384 PMCID, 449 DOI, 20 PMID);
3. henting: 403 og 418 er utgiverens svar og står, en robotsperre omgås ikke, og forbigående feil prøves etter fast regel (to forsøk med 10 s pause, deretter én runde med 30 s tidsavbrudd);
4. **identitet**: teksten må høre til posten (ny, §2.3);
5. uttrekkbar tekst, verifisert ved faktisk uttrekk;
6. minst 6 000 tegn, og minst 60 setninger på HTML-ruten;
7. søppelandel høyst 5 %;
8. engelsk, avgjort med `langdetect` 1.0.9 (fast frø 0) både på hele teksten og på kroppsteksten: toppspråk `en` med p ≥ 0,90 og høyst 10 % ikke-latinsk skrift.

### 1.2 Frafall per kriterium

| Kriterium | Biomed | Humaniora |
|---|---|---|
| Pulje | 750 | 1 050 |
| Vurdert | 30 | 186 |
| **Valgt** | **25** | **15** |
| År | 2 | 0 |
| Utelukket | 0 | 0 |
| Hentefeil | 0 | 20 |
| Identitet | 0 | 68 (herav 66 robotsperre, §2.3) |
| Ingen tekst | 0 | 0 |
| For kort | 3 | 11 |
| Søppel | 0 | 3 |
| Språk, hele teksten | 0 | 69 |
| Språk, kroppsteksten | 0 | 0 |

Hentefeilene i humaniora: 8 SSL-sertifikatfeil, 4 × 404, 3 × 403, 2 tidsavbrudd, 1 × 418, 1 død vert og 1 DOAJ-post uten lenke.

Per fag, humaniora:

| Fag | Vurdert | Valgt | Forkastet |
|---|---|---|---|
| historie | 19 | 3 | hentefeil 8, språk 7, for kort 1 |
| arkeologi | 7 | 3 | språk 3, for kort 1 |
| filologi | 17 | 2 | språk 13, for kort 1, hentefeil 1 |
| klassiske fag | 9 | 2 | språk 5, identitet 1, hentefeil 1 |
| religionsvitenskap | 3 | 2 | språk 1 |
| bibelvitenskap | 4 | 2 | språk 1, for kort 1 |
| diplomatikk og arkiv | 127 | 1 | identitet 67, språk 39, hentefeil 10, for kort 7, søppel 3 |

Alle sju fag nådde kvoten. **Diplomatikk og arkiv** krevde 127 vurderinger for ett dokument. Tidsskriftene som ble vurdert der: Acervo 66 (alle robotsperre), Documenta & Instrumenta 17 (15 på språk, spansk; 1 for kort; 1 tidsavbrudd), Revista Informação na Sociedade Contemporânea 16 (portugisisk: 10 på språk, 3 søppel, 2 for korte, 1 identitet), Khazanah 14 (10 på språk, indonesisk; 4 for korte), Vestiges: Traces of Record 6 (3 × 404, 2 på språk, fransk; 1 valgt), Archeion 6 (alle SSL-sertifikatfeil, ikke omgått), Belgeler 2 (tyrkisk).

### 1.3 Fag, tidsskrifter og sjangre: hva settet dekker og ikke dekker

**Biomed (25):** kjemi og materialer (RSC Advances ×2, Chemical Science, ACS Omega), klinisk medisin (Transplantation Direct, Surgical Neurology International, International Journal of Neuropsychopharmacology, Molecular and Clinical Oncology, Journal of Cancer, Hepatology, Videosurgery and Other Miniinvasive Techniques, Dermatopathology, Nephro-Urology Monthly, Journal of Diabetes Investigation, EJVES Short Reports, African Journal of Emergency Medicine), folkehelse (Journal of Injury & Violence Research), veterinærmedisin (Veterinary Medicine and Science), evolusjon og økologi (Genome Biology and Evolution, Ecology and Evolution, Evolutionary Psychology), nevrovitenskap (Brain, Behavior, & Immunity – Health), proteomikk (Journal of Proteomics & Bioinformatics), språkteknologi i medisin (Journal of Participatory Medicine) og matematikk (Monatshefte für Mathematik).

**Humaniora (15):** historie — Codrul Cosminului, Aestimatio, Revista Brasileira de História; arkeologi — Bulletin of the History of Archaeology, Journal of Lithic Studies, Journal of Open Archaeology Data; filologi — Íkala, Journal of Modern Languages; klassiske fag — The Journal of Classics Teaching, thersites; religionsvitenskap — Zygon, Journal of Islamic and Religious Studies; bibelvitenskap — HTS Teologiese Studies ×2; diplomatikk og arkiv — Vestiges: Traces of Record.

**Sjangre**, etter de fem kategoriene i oppdraget:

| Sjanger | Biomed | Humaniora |
|---|---|---|
| forskningsartikkel | 18 | 9 |
| oversiktsartikkel | 7 | 5 |
| kildeutgivelse | 0 | 1 |
| avhandling | 0 | 0 |
| konferansebidrag | 0 | 0 |

Kategoriene sier mindre enn tabellen ser ut til. Av de 12 oversiktsartiklene er fem reelle oversikter. Sju er tekster som ikke passer i noen av de fem kategoriene: policykommentar, lederkommentar, bokanmeldelse, praksisrefleksjon, intervju, programmatisk essay og refleksjonsessay (§3.2 punkt 5). Den ene «kildeutgivelsen» er en datapublikasjon, en digitalisering av et håndtegnet surveykart fra 1980. To av forskningsartiklene er omarbeidede konferanseinnlegg (DOAJ018ce4a798, DOAJ0415b451da).

**Settet dekker ikke:**

* **diplomatisk eller tekstkritisk kildeutgivelse** — ingen, se §6;
* katalog og arkivregistrant, avhandling og konferanserapport;
* ikke-engelsk humaniora — utelukket av kravet, og kravet tok 69 av 186 humanistiske kandidater. Delsettet er den engelskspråklige delen av DOAJs humaniora, ikke humaniora;
* ingeniørfag, fysikk og informatikk utenfor det Europe PMC indekserer, samfunnsvitenskap ut over folkehelse, og juss.

### 1.4 Kryssjekk mot Crossref

37 av de 40 har DOI. Crossref svarte for 36; for thersites-artikkelen gir DOI-en 404 hos Crossref. 34 har samme år som kilden. To avviker innenfor vinduet: PMC6372861 (kilde 2019, Crossref 2018) og PMC7089651 (2017 mot 2016). Tre DOAJ-poster mangler DOI (DOAJ0117483246, DOAJ00b6e27b0a, DOAJ26bf8fdfc1). Kryssjekken kontrollerer posten, ikke teksten; se §2.3.

---

## 2 Defekter funnet under arbeidet

Tre slags feil ble funnet. De første ble oppdaget før lesing, slik kravet var. Den andre lå i parseren og traff også sett 1 og rørledningstesten. Den tredje ble oppdaget **under** lesingen, etter 30 dokumenter, og brøt kravet om at alt skulle være avgjort før lesing. Alle er rettet, og alle er målt.

### 2.1 Valgdefekter oppdaget og rettet før lesing

| Defekt | Virkning før rettelse | Rettelse |
|---|---|---|
| DOAJ-trekket var ustratifisert | 0 historie og 0 arkeologi blant 15 | kvote per fag, satt før lesing (§1.1) |
| Landingssider passerte tegngrensen | en side med 42 setninger (sammendrag og menyer) talte som artikkel | minst 60 setninger på HTML-ruten; JATS-ruten har ingen setningsgrense, fordi en kort JATS-kommentar er en hel tekst |
| Språk ble avgjort på hele teksten alene | et sammendrag eller en litteraturliste på et annet språk kan styre helhetens språk; obsidian-artikkelens første uttrekk var dominert av en spansk litteraturliste | språk avgjøres både på helheten og på kroppsteksten, uten tittelblokk og litteraturliste |
| Binærsøppel | et Word-dokument levert som HTML ga 67 % søppeltegn med engelsk imellom | søppelandel høyst 5 % |
| OJS `article/view/ID/GALLEY` er en HTML-ramme | rammen ga et par hundre tegn, og artikkelen falt som for kort — systematisk for tidsskrifter som leverer PDF | omskriving til `article/download/ID/GALLEY` |
| Foreldet DOAJ-lenke (død vert) | hentefeil for en artikkel som finnes | DOI-resolveren som reserve ved nettverksfeil og 404; 403 og 418 står |
| 503-storm fra Europe PMC | 573 hentefeil i én kjøring styrte hvilke dokumenter som kom med | JATS leses fra det lokale råarkivet når filen finnes, tilbaketrekk ved 429 og 5xx. To kjøringer ga identisk biomed-utvalg |

### 2.2 JATS-parseren droppet artikkelkroppen tilfeldig

`blocks_from_jats` holdt rede på besøkte elementer med `id()` på lxml-proxyer. En proxy kan samles inn og id-en gjenbrukes av et annet element, som da ble hoppet over som «allerede besøkt». Samme XML-bytes ga svært ulikt antall setninger fra kjøring til kjøring (observert: 537 og 20). Rettet i commit `296ea2e` ved å bruke elementets sti i treet (`getpath`) i stedet for `id`. Testen er armert: den gamle algoritmen mister kroppen på fiksturen, den nye gir 302 blokker i 200 av 200 kjøringer.

**Omfang i den lagrede rørledningstesten** (`data/pipeline-test/reparse-tall-ADDENDUM07.json`): 143 av 341 JATS-filer var avkortet, og **39 519 setninger manglet** (147 675 lagret mot 187 194 med rettet parser). Ingen fil var lengre i den lagrede versjonen. De lagrede utdataene er ikke overskrevet. Den rettede parsen ligger i `sentences-REPARSE-ADDENDUM07.jsonl` med egen advarselslinje.

**Rettede tall for ADDENDUM-06.** Dette er rørledningstest, ikke prevalens, med samme forbehold som der:

| Størrelse | Avkortet tekst (lagret; tallene i ADDENDUM-06) | Full tekst |
|---|---|---|
| v1-kandidater (§1.7, §3) | 217 | **277** |
| Dokumenter uten v1-kandidat | 259/392 = 66,1 % | **224/393 = 57,0 %** |
| Bare passasje, v1 (§3) | 81/217 = 37,3 % | **98/277 = 35,4 %** |
| v2-kandidater (§1.7) | 607 | **766** |
| Dokumenter uten v2-kandidat | 167/392 = 42,6 % | **112/393 = 28,5 %** |
| Bare passasje, v2 (ikke oppgitt i ADDENDUM-06) | 280/607 = 46,1 % | 352/766 = 46,0 % |

Konklusjonen i ADDENDUM-06 §3 står: passasjekravet bærer omtrent en tredjedel av v1-kandidatene også på full tekst.

**Sett 1 ble delvis lest på avkortet tekst.** Lesetekstene fra slynge 10 er bevart (`data/pipeline-test/sett1-lesetekster-slynge10.json`). Sammenlignet med rettet parse var **fire av de 30 dokumentene avkortet da de ble lest**:

| Dokument | Setninger lest | Setninger i dokumentet |
|---|---|---|
| PMC4351561 | 11 | 123 |
| PMC4593355 | 22 | 635 |
| PMC4625467 | 24 | 397 |
| PMC5454651 | 196 | 199 |

**1 101 setninger i sett 1 er aldri lest.** ADDENDUM-06 §1.1 sier at 30 dokumenter ble lest i sin helhet. Det holder for 26 av dem. De 28 fasittreffene er treff i det som ble lest; hvor mange treff de 1 101 setningene inneholder, er ukjent. To andre dokumenter (PMC4874576, PMC5020840) var avkortet i den lagrede rørledningsfilen, men hele i lesetekstene: feilen trakk på nytt ved hver parse. Tegntallet i ADDENDUM-06 §1.5 (1 068 021) kom fra enda en parse og kan ikke reproduseres. Lesetekstene har 1 093 735 tegn, full tekst 1 161 686.

På full tekst, mot de samme 28 treffene, er v1s recall 0/28 og presisjon **0/7** (ADDENDUM-06: 0/6). v2s recall er 28/28 og presisjon **32/56 = 57,1 %** (ADDENDUM-06: 32/52 = 61,5 %). De nye kandidatene ligger i tekst som aldri ble lest, og om de er treff, er ikke avgjort. Bomfordelingen for v1 i sett 1 (§4.3) er den samme på full tekst som på avkortet tekst.

Sett 2 er parset med rettet parser. Alle 25 JATS-tekster er kontrollert mot tittelen (§2.3).

### 2.3 Feil dokument bak riktig post — oppdaget under lesing

Ved dokument 31 av 40, etter at 30 var lest ferdig, viste teksten under posten «Settlement Dynamics on the Banks of the Upper Tigris, Iraq: The Mosul Dam Reservoir Survey (1980)» (Journal of Open Archaeology Data 2020, 10.5334/joad.63) seg å være en annen artikkel i samme tidsskrift: et museumsinventar publisert i **2026** (joad.220). Årskravet var sjekket mot metadata, og Crossref bekreftet 2020 — for posten, ikke for teksten.

En identitetssjekk av alle 40 fant ett til. Under en portugisisk artikkel i Revista Informação na Sociedade Contemporânea (2019) lå et **bokkapittel fra 2013** om praksisplasser for geografer, hentet fra en PDF-lenke til et annet nettsted på artikkelsiden. **To av de 15 humanistiske dokumentene hadde feil tekst; ingen av de 25 biomedisinske.** JATS hentes med PMCID.

**Årsak.** `galley_links` (commit `82df4e0`) sorterer PDF-lenker først. Sorteringen løfter enhver `.pdf`-lenke på landingssiden foran artikkelens egen fil, også lenker til andre artikler og til andre nettsteder. Hvor på siden de to lenkene sto, er ikke kjent: landingssidene ble ikke lagret når en PDF ble valgt. Lenkerekkefølgen er dessuten ikke stabil: av fire hentinger av joad.63 i løpet av dagen fikk to feil PDF først og to riktig (råmanifestet, kl. 16:59, 17:31, 19:42 og 20:45 UTC). Rekkefølgen kan derfor ikke rettes til å bli riktig; identiteten må avgjøres på teksten.

**Rettelse** (commit `3dc08ad`). `identity_verdict` godtar et uttrekk når postens DOI står i teksten, med mellomrom fjernet fordi PDF-uttrekk bryter lenker over linjer. Ellers kreves at minst **60 %** av tittelens ord på fire tegn eller mer finnes blant tekstens ord. En tittel med færre enn to slike ord avgjøres ikke uten DOI. Terskelen ble satt før revisjonen under ble kjørt. Porten brukes **per lenke**: en tekst som ikke hører til posten, hoppes over og neste lenke prøves; fører DOAJ-lenken ikke til dokumentet, prøves DOI-resolveren. «identitet» er ny frafallsgrunn.

**Revisjon.** Porten ble kjørt på beslutningsteksten til de 139 av de 157 vurderte kandidatene som fikk en beslutning på tekst; de øvrige 18 falt på år eller henting før noen tekst fantes. Beslutningsteksten ble gjenfunnet i `data/raw2` som den filen som ved nytt uttrekk gir nøyaktig det loggførte tegntallet, med ruten fra filnavnet. Alle 139 ble gjenfunnet.

* **Biomed, 30 vurdert:** 28 beslutninger på tekst, alle **28 identitetsverifisert** (25 valgt, 3 for korte). 2 falt på år.
* **Humaniora, 127 vurdert:** 16 hentefeil uten tekst. Av 111 beslutninger på tekst hvilte **47 på tekst som ikke kan identifiseres som dokumentet**: 2 av de 15 valgte, 7 språkforkastelser, 37 lengdeforkastelser og 1 søppelforkastelse.

Beslutninger truffet på verifisert tekst, eller før noen tekst fantes, står (80). De 47 ble truffet på nytt med identitetskrav per lenke, og posisjoner utover det første trekket ble vurdert der kvoten ikke lenger var fylt. Regelen for forbigående feil var den samme som i trekket.

| | Antall | Utfall |
|---|---|---|
| Beslutninger som står | 80 | 13 valgt, 44 språk, 7 for kort, 16 hentefeil |
| Truffet på nytt | 47 | 1 valgt, 37 identitet, 5 språk, 3 for kort, 1 søppel |
| Nye posisjoner (diplomatikk og arkiv, 68–126) | 59 | 1 valgt, 31 identitet, 20 språk, 1 for kort, 2 søppel, 4 hentefeil |

Utfallet for de to feildokumentene:

* **DOAJ010517efa8** (joad.63) fikk riktig tekst: 18 979 tegn, 176 setninger, DOI funnet i teksten, tittelandel 1,0. Den riktige teksten er lest i sin helhet.
* **DOAJ109826304b** fikk sin egen tekst og falt på språk (portugisisk). Diplomatikk og arkiv ble fylt på posisjon 126 av **DOAJ26bf8fdfc1**, «Probing inter-ethnic relations between Cameroon-Nigeria: the case of Menchum Division, 1922 to 1961» (Vestiges: Traces of Record, 2019). Den har tittelandel 1,0, ingen DOI, og ingen treff i lese-loggen, sett 1 eller frasesøkmaterialet på tittel.

De 13 andre humanistiske dokumentene sto, og setningene deres i det reviderte settet er byte-identiske med dem som ble lest.

**Robotsperre.** 66 av de 68 identitetsfallene er ikke et uttrekksproblem, men en robotsperre hos Acervo (Arquivo Nacional, Brasil): siden svarer HTTP 200 med en F5-side som ber besøkeren skrive inn en bildekode, i stedet for artikkelen. Sperren er ikke omgått. I det første trekket ble disse sidene ført som «for kort» (224 tegn). De er utgiverens nektelse og hører i praksis sammen med 403. De to øvrige identitetsfallene er poster med tittelen «Editorial» uten DOI.

**Lesing av feiltekstene.** Setning 0–114 av feilteksten under dokument 31 ble lest før feilen ble oppdaget. Ingen treff er ført fra den teksten, og den er logget som delvis lest. Setning 0–39 av bokkapittelet ble sett under identitetssjekken og er logget likeså.

**En latent feil til.** Hentekoden sammenlignet `content[:5] == b"%PDF"`, altså fem byte mot fire, og slo aldri til; PDF-gjenkjenningen hvilte på content-type alene. Ingen fil i `data/raw2` er rammet, fordi ingen `r2-html`-fil begynner med `%PDF`. Feilen er rettet i den identitetsrettede hentingen.

---

## 3 Fasiten

### 3.1 Leseregler

Fasiten (`data/recall-sett-2.jsonl`) er laget slik sett 1 ble laget: **hvert dokument lest i sin helhet, uten markørlisten og uten søk.** Hver passasje som oppfyller PREREG §2 under passasjekravet (ADDENDUM-03 §1) er markert med spenn, klasse, sjanger og begrunnelse. Klassene er PREREG §5 med de fire uavklart-verdiene fra ADDENDUM-05. To regler fra sett 1 er brukt uendret:

* **(a)** Hindringen må være en barriere, ikke et fritt valgt design eller en begrensning ved eget opplegg.
* **(b)** Det ugjorte må høre til arbeidet som rapporteres, ikke til andres studier, historiske aktører, organisasjonens praksis eller ekskluderingskriterier.

Hver distinkt passasje telles for seg. Tvilstilfeller er merket `grensetilfelle: true`, og recall oppgis med og uten dem. `unit` er `passage` bare når det ugjorte og hindringen står i ulike setninger, ikke når spennet er utvidet for kontekst. Alle ni flersetningsspenn er gjennomgått mot begrunnelsen, og tre av dem har delene i ulike setninger. Fasiten er markert av én koder, den samme som i sett 1.

### 3.2 Kodebeslutninger tatt under lesingen

Humanistisk materiale stilte spørsmål sett 1 ikke hadde stilt. Beslutningene under ble tatt da spørsmålet oppsto, og er brukt likt på alle 40 dokumentene:

1. **Redaksjonelle sigla telles ikke.** «[illegible word]» i et sitert brev er H2-materiale, men apparat, ikke en setning der forfatteren navngir noe ugjort (DOAJ014a6389f7, setning 283 og 549).
2. **En status kan være hindring når årsakskoblingen står i teksten.** «As Level 4 from C3T1 is still under analysis, we only took into consideration …» er treff, kodet H1/H7-uavklart og grensetilfelle (DOAJ03208f7c8a #151). Samme dokument sier andre steder at bare én komponent er analysert hittil, og at en annen er under studie, uten slik kobling; det er ikke treff (293–295). Linjen er den samme som for sett 1 W2505978088 #137 («still waiting for»).
3. **En anmeldelse av en kildeutgivelse teller ikke utgiverens parkerte spørsmål.** Anmeldelsen av en utgave av babylonske astronomiske tavler (DOAJ012abea391, setning 46–51) beskriver udaterbare tavler med hindring, men det ugjorte er utgiverens, ikke anmelderens (regel b). Det er et funn for §6: kildeutgivelsers parkerte spørsmål kan dukke opp i anmeldelser, som §2 ikke teller.
4. **Kartets presisjon er H7 der ADDENDUM-05 ikke har en verdi.** «difficult to assess which one among several mounds was actually mapped» (DOAJ010517efa8 #68) står mellom H7 (presis posisjon finnes ikke i kilden), H2 (skissepreget kart) og H4 (mønster i satellittbilder). ADDENDUM-05 definerer ingen H4/H7-uavklart. H7 er valgt, og treffet er merket grensetilfelle.
5. **Sjangre utenfor de fem kategoriene** er ført som oversiktsartikkel, med merknad per dokument i `data/recall-sett-2-meta.json`.

### 3.3 Treffene

**27 treff i 15 av 40 dokumenter**: biomed 19 treff i 10 av 25 dokumenter, humaniora 8 treff i 5 av 15.

| | Sett 2 | Sett 1 |
|---|---|---|
| Treff / dokumenter med treff / dokumenter lest | 27 / 15 / 40 | 28 / 8 / 30 |
| H7 | 18 | 12 |
| H4 | 2 | 3 |
| H2 | 1 | 5 |
| H1 | 1 | 0 |
| H8 | 1 | 1 |
| H9 | 1 | 1 |
| H3 | 0 | 2 |
| Uavklart (ADDENDUM-05) | 3 (H1/H7 2, H5/H7 1) | 4 |
| Bare passasje (`unit: passage`) | 3/27 = 11,1 % | 5/28 = 17,9 % |
| Grensetilfeller | 8 (4 biomed, 4 humaniora) | 2 |

Humanioras 8 treff: H7 5, H1/H7-uavklart 1, H4 1, H2 1. Alle tre passasjetreffene er biomedisinske. ADDENDUM-06 §3 fant at nesten en femtedel av reelle parkerte spørsmål ville falt ut av et setningskrav; i sett 2 er andelen omtrent en niendedel. Retningen er den samme, størrelsen mindre.

Ikke-treff av interesse er ført i `data/recall-sett-2-noterte-ikke-treff.jsonl` (18 poster) med grunn.

---

## 4 Målingen

### 4.1 Recall og presisjon

Målingen bruker samme kode som sett 1 (`gjenopptak.extract.recall.maal`). Et fasittreff er fanget når en filterpassasje fra samme dokument har `start_index ≤ hit_index ≤ end_index`. Presisjonen måles over alle dokumentene i delsettet, også dem uten fasittreff. Filteret kjøres på `data/recall-sett-2-setninger.jsonl`: 11 366 setninger og 1 530 473 tegn (biomed 919 808, humaniora 610 665). Intervallene er 95 % Wilson, regnet i Python, og er beskrivende.

**v2 er målingen.** v1 står ved siden av som referanse.

| Delsett | n dok | n treff | **v2 recall** | v2 uten grensetilfeller | **v2 presisjon** | v1 recall | v1 presisjon |
|---|---|---|---|---|---|---|---|
| **Samlet** | 40 | 27 | **7/27 = 25,9 %** (13,2–44,7) | 4/19 = 21,1 % | **6/43 = 14,0 %** (6,6–27,3) | 4/27 = 14,8 % (5,9–32,5) | 2/16 = 12,5 % |
| **Humaniora** | 15 | 8 | **1/8 = 12,5 %** (2,2–47,1) | 1/4 = 25,0 % | **1/20 = 5,0 %** (0,9–23,6) | 0/8 = 0,0 % (0–32,4) | 0/11 = 0,0 % |
| **Biomed** | 25 | 19 | **6/19 = 31,6 %** (15,4–54,0) | 3/15 = 20,0 % | **5/23 = 21,7 %** (9,7–41,9) | 4/19 = 21,1 % (8,5–43,3) | 2/5 = 40,0 % |

v2 gir 43 kandidater: 18 på setning, 25 bare på passasje. Mot v1 fanger v2 tre treff til (PMC6233672 #152, PMC8474669 #883, DOAJ010517efa8 #44) og gir 27 kandidater til.

**Dette er det første målte tallet for v2: omtrent hvert fjerde parkerte spørsmål blir funnet, og i humaniora ett av åtte.** Intervallene er brede, men selv den øvre grensen for samlet recall ligger under halvparten. Tallet står i kontrast til 28/28 fra sett 1 (§5). Tre av de sju fangede treffene er grensetilfeller (PMC6233672 #164, #166, #169, alle i samme dokument).

### 4.2 Bommene, én for én

«Markør» betyr at markørlisten ikke traff treffsetningen mens hindringsmønsteret sto i passasjen. «Hindring» betyr at markøren traff, men hindringsmønsteret ikke gjorde det. «Begge» betyr at ingen av dem traff.

| # | Dokument | Klasse | Fasitens formulering (utdrag) | Siden som sviktet |
|---|---|---|---|---|
| 1 | PMC6233672 #109 | H7 | «remains unknown without more data» | markør |
| 2 | PMC4815471 #344 | H7 | «too small to allow for the comparison» | markør |
| 3 | PMC5174742 #115 | H9 | «not yet possible … precluding any direct assessment» | markør |
| 4 | PMC4761783 #167 | H7 | «no survival and mortality data … so we utilized» | begge |
| 5 | PMC4761783 #470 | H4 | «without a comprehensive aerial survey» | begge |
| 6 | PMC5645861 #280 | H7 | «power … decreased by the death of study participants» | hindring |
| 7 | PMC5645861 #292 | H7 | «a more quantitative comparison was impossible» | begge |
| 8 | PMC4931210 #357 | H8 | «a hurdle to studying a large population» | markør |
| 9 | PMC7434072 #197 | H1/H7-uavklart | «Due to insufficient positive examples … we disregarded» | markør |
| 10 | PMC6277501 #10 | H7 | «died before they could be assessed» | begge |
| 11 | PMC6277501 #54 | H7 | «died before an assessment could be performed» | begge |
| 12 | PMC6277501 #65 | H7 | «we do not know about the presence of ARDS» | markør |
| 13 | PMC5010871 #164 | H5/H7-uavklart, grense | «currently do not pass quality control» | begge |
| 14 | DOAJ03208f7c8a #151 | H1/H7-uavklart, grense | «still under analysis, we only took into consideration» | begge |
| 15 | DOAJ010517efa8 #67 | H4, grense | «gave no clear signs in the satellite images» | markør |
| 16 | DOAJ010517efa8 #68 | H7, grense | «difficult to assess which one … was actually mapped» | markør |
| 17 | DOAJ00b6e27b0a #35 | H7 | «there is no way of determining» | begge |
| 18 | DOAJ00b6e27b0a #40 | H7 | «no other known translated version … analysed singly» | begge |
| 19 | DOAJ018ce4a798 #227 | H2, grense | «the fragmentary state of the text deprives us» | markør |
| 20 | DOAJ26bf8fdfc1 #246 | H7 | «do not reflect variation within the forty year period» | markør |

Formene som mangler, er ikke eksotiske. Markørlisten er bygd på mislykkede handlinger («could not», «were unable to»). Fem av bommene uttrykker det ugjorte som en tilstand i stedet (nr. 1, 12, 16, 17 og 20: «remains unknown», «we do not know», «difficult to assess», «no way of determining», «do not reflect»). Fem uttrykker det som det som ble gjort i stedet (nr. 4, 5, 9, 14 og 18: data fra andre arter, ekstrapolering, teknikker som ble utelatt, et utvalg av trekk, analyse av én versjon). Ellers mangler `impossible`, `precluding`, `hurdle` og `deprives`. På hindringssiden mangler den kausale `as` («as the initial location … is unknown») og hindringer i fagets eget ordforråd («died before», «death of study participants»).

### 4.3 Bomfordelingen, sett 1 og sett 2 side om side

| Bommer | Bare markør | Bare hindring | Begge | Sum |
|---|---|---|---|---|
| Sett 1, v1 (ADDENDUM-06 §1.2) | 16 | 3 | 9 | 28 |
| **Sett 2, v1** | 11 | 0 | 12 | 23 |
| **Sett 2, v2** | 10 | 1 | 9 | 20 |
| Sett 2, v2 — humaniora | 4 | 0 | 3 | 7 |
| Sett 2, v2 — biomed | 6 | 1 | 6 | 13 |

Sammenlignbart par er v1 mot v1: i sett 1 falt 16 av 28 bommer bare på markørsiden, i sett 2 11 av 23. Andelen som faller på **begge** sider, stiger fra 9/28 = 32 % til 12/23 = 52 %. Etter utvidelsen faller fortsatt 19 av 20 v2-bommer helt eller delvis på markørsiden. Utvidelsen fra sett 1 flyttet få bommer: v2 fanger tre flere enn v1. Av de åtte humanistiske treffene fanget tilleggene ett (DOAJ010517efa8 #44, via `cannot\b`).

### 4.4 Presisjonen

37 av de 43 v2-kandidatene er ikke i fasiten, 19 i humaniora og 18 i biomed. Mønstrene som utløste dem: `cannot\b` 14, `could not` 11, `(is|are) needed` 8, `did not have` 2, `did not allow` 1, `with the exception of` 1.

* **Humaniora (19):** 10 gjelder historiske aktører eller andres arbeid («Reinecke could not give an absolute date»), 8 er retoriske eller normative utsagn («cannot be denied», «Scripture cannot be broken»), og 1 er et utslag av tillegget `with the exception of`. **I historiske framstillinger er «could not» ofte fortelling om aktører**, og regel (b) er da ikke en finesse, men hovedkilden til falske positive.
* **Biomed (18):** 7 er «further research is needed» uten hindring (N3), 4 er andres resultater og kjente fakta, 3 er matematiske eller tekniske utsagn, 1 er et ekskluderingskriterium (regel b), 1 er et utvalgsproblem som besvares i teksten (N1), 1 er et eget resultat og 1 en begrensning ved eget studiested (regel a).

De 37 ble lest etter målingen. Ingen av dem er etter lesereglene et oversett treff. To var nær: PMC4761783 #178 besvares i setningene 179–181 (N1), og PMC6277501 #74 er en begrensning ved studiestedet (regel a). **Fasiten er uansett ikke endret etter målingen**; en fasit som justeres etter filterets utdata, er ikke lenger uavhengig av filteret.

Presisjonen på 14,0 % betyr omtrent sju kandidater per kandidat som treffer fasiten. I sett 1 var tallet 1,75 på full tekst. Uttrekket er en kandidatgenerator, og lav presisjon er ikke i seg selv en feil. Men den er ikke lenger kjøpt med høy recall.

---

## 5 Hvorfor 28/28 fra sett 1 er en øvre grense og ikke en måling

To grunner. Den andre er ny i denne slyngen.

1. **Sirkularitet.** De 36 tilleggene i v2 er lest ut av nettopp de 28 fasitsetningene. At v2 finner dem, bekrefter bare at utvidelsen traff det den ble laget for (ADDENDUM-06 §1.4).
2. **Nevneren er ufullstendig.** Fasiten ble laget på tekst der 1 101 setninger i fire dokumenter manglet (§2.2). Treff i den teksten er ikke med i nevneren, og om v2 ville fanget dem, er ukjent. Tallet er derfor en øvre grense også for de 30 dokumentene, ikke bare for markørene.

**Sett 2 er første måling av v2**, og det gir 7/27. Markørlisten ble frosset i commit `a12fe82` (12. september kl. 17:36 norsk tid) før puljene til sett 2 ble hentet (kl. 18:40). `passage.py` er ikke endret siden, og ingen av de 40 dokumentene har bidratt med en markør. Avstanden mellom 28/28 og 7/27 viser hvor lite det første tallet sa. Hvor mye av avstanden som skyldes sirkulariteten, og hvor mye forskjellen mellom materialene, kan ikke skilles med to sett: v1 fanget 0/28 i sett 1 og 4/27 i sett 2.

---

## 6 De ti døde markørene etter møtet med humanistisk materiale

`did not attempt`, `prevented me from`, `no attempt was made`, `we coded a random sample`, `remains unread`, `remains untranscribed`, `have not been read`, `have not been transcribed`, `have not been collated`, `have not been digiti`:

| Delsett | Tegn | Treff for de ti | Kontroll |
|---|---|---|---|
| Humaniora (15) | 610 665 | **0** | `could not` 21, `because` 65 |
| Biomed (25) | 919 808 | **0** | `could not` 4, `because` 61 |

Tellingen er gjort i Python (`marker_hits`). Kontrollstrengene viser at den leser teksten.

**Status: uavgjort, som før.** ADDENDUM-06 §1.6 krevde minst én diplomatisk kildeutgivelse i fasiten, fordi et nullresultat i materiale uten sjangeren ikke er evidens mot markørene. **Sett 2 har ingen.** Stratumet for diplomatikk og arkiv ga etter 127 vurderinger én forskningsartikkel om regional økonomisk historie på muntlige kilder. Den eneste «kildeutgivelsen» er en datapublikasjon av et kart. Det nærmeste kildeutgivelsesmaterialet i settet er en anmeldelse av en utgave (§3.2 punkt 3), og det parkerte spørsmålet der er formulert uten noen av de ti formene. De ti er derfor verken bekreftet eller tilbakevist. **Ingen fjernes.**

Settet sier likevel to ting. De humanistiske treffene er formulert som «no way of determining», «deprives us of», «do not reflect», «cannot be ascertained … since» og «has no other known … version». Ingen av dem er arkivformene de ti koder for. Og DOAJ er ikke en brukbar kilde for engelskspråklige kildeutgivelser: sporet domineres av ikke-engelske tidsskrifter og ett robotsperret tidsskrift (Acervo, 66 av 127 vurderte).

---

## 7 Ingen utvidelse fra sett 2; et tredje sett kreves

**Ingen markør er lagt til fra bommene i §4.2.** `UNDONE_V2` og `OBSTACLE_V2` er uendret, og `src/gjenopptak/extract/passage.py` har ingen endring etter `a12fe82`.

Grunnen er den samme som gjorde sett 2 nødvendig. Legges de 20 bommene inn nå, blir recall for den nye listen mot sett 2 en øvre grense av samme slag som 28/28. **Et tredje sett kreves før en ny utvidelse kan måles:** trukket og lest etter at utvidelsen er frosset, på dokumenter ingen markør er hentet fra. Kravene til sett 3 festes her:

* identitetsporten og den rettede parseren fra første henting;
* **minst én diplomatisk eller tekstkritisk kildeutgivelse**, hentet fra en liste over utgaveserier og tidsskrifter som settes opp før trekkingen, ikke fra DOAJ (§6);
* en uavhengig annenkoder på et frøtrukket delsett før tallene brukes. Én koder er fortsatt svakheten (ADDENDUM-06 §1.6), og i sett 2 er åtte av 27 treff grensetilfeller;
* de 1 101 uleste setningene i sett 1 leses før sett 1 brukes til noe mer (§2.2).

---

## 8 Hva endres, og hva endres ikke

**Endres:**

* Høstingen krever **identitet per lenke** (`identity_verdict`, commit `3dc08ad`) og bruker den **rettede JATS-parseren** (commit `296ea2e`). Begge har armerte tester.
* Tallene i ADDENDUM-06 §1.1, §1.2, §1.5, §1.7 og §3 som ble regnet på avkortet tekst, er rettet i §2.2. Konklusjonene der står.
* Sett 2 er lagt til som fasit og måling: `data/recall-sett-2.jsonl`, `data/recall-sett-2-setninger.jsonl`, `data/recall-sett-2-meta.json` og `data/recall-sett-2-maaling.json`. Utvalgslogger, revisjon, lesetekster og skript ligger i `data/recall2-utvalg/`.

**Endres ikke:**

* Markørlisten. v1 og v2 er urørt.
* Tersklene i PREREG §6.
* Klassene og løftbarheten i PREREG §5 og ADDENDUM-05.
* Enheten (passasje, ±2) og kravet om to tall for M1 fra ADDENDUM-03 §1.
* Utvalgsdesignet i PREREG §4.
* Sett 1s fasit. Den er ikke lest på nytt i denne slyngen.

---

## 9 Erklæring

* **Ingen trekking av utvalg er utført**, og ingen koding av utvalget er begynt. Fasiten er et verktøysett, ikke et utvalg, og ingen tall i den er M1 eller M2.
* **Ingen OpenAlex-kall og ingen OSF-kall.** Kildene er Europe PMC, Crossref, DOAJ, utgivernes egne sider og DOI-resolveren. 403, 418, SSL-feil og robotsperrer er ikke omgått, og brukeragenten er prosjektets egen.
* Alle 40 dokumenter står i `data/leste-kontrollkandidater.json` med merket `LEST-I-SIN-HELHET-UTELATT-FRA-TREKKING`, sammen med de to feiltekstene (`DELVIS-LEST-FEIL-TEKST-UTELATT-FRA-TREKKING` og `DELVIS-SETT-FEIL-TEKST-UTELATT-FRA-TREKKING`). Loggen har nå 356 rader, og alle **utelates fra trekkingen**.
* **PREREG-v1.md og ADDENDUM-01/02/03/04/05/06.md er uendret**, sha256 `05988b23…ba23a`, `aa78d1be…c255f`, `7c0542c9…f713`, `0b577ae6…5c4e`, `7f7d067b…8a9c`, `b12c85b2…5e9d`, `0f0e9a81…5687`.
* Ingen remote, ingen push.
* Rådata er ikke committet. `data/` er git-ignorert, og fasiten, loggene og lesetekstene sikres til Vault.
* **Åpne poster:**
  * de fire kravene til sett 3 i §7;
  * de 1 101 uleste setningene i sett 1;
  * statusen for de ti døde markørene (§6);
  * designproblemet der det ugjorte og hindringen er én frase (ADDENDUM-06 §1.4, bekreftet i §4.2);
  * postene som står fra ADDENDUM-04 §6, ADDENDUM-05 §7 og ADDENDUM-06 §6.
