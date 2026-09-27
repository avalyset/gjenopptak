# ADDENDUM-05 — H1 mot H7: når formen ikke skiller ressursmangel fra datamangel

**Skrevet:** 2026-09-12
**Hører til:** PREREG-v1.md `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`,
ADDENDUM-01.md `aa78d1be50ac17f8e26a92513aa115b3d504bdde3556e43b4f2317ea47cc255f`,
ADDENDUM-02.md `7c0542c92c54a586e3b387794272bed171ee285b75c8ebe4ee8fe1fa16f6f713`,
ADDENDUM-03.md `0b577ae6c3d0278e811e674c78e4e2948be46252e5aca9c94e94466c1f985c4e`,
ADDENDUM-04.md `7f7d067b80468a7016e398d1120930c98eb8a705b0e1c0102ad97e9db42f8a9c`
**Status:** operasjonalisering etter lås. **Rører løftbarhetsanslaget i PREREG §5.** Skrevet før koding og før trekking. Ingen av de fem låste filene er endret.

---

## 1 Det utløsende funnet

Søket etter en H1-kontroll i døgn 2 fant denne passasjen, i seksjonen `Potential confounders`:

> **10.1080/20008198.2017.1380470** — «…these details about the reported events are missing, hence **we were unable to code all events** according to the DSM-5.»

Setningen leste som H1 på formen. Den navngir noe forfatterne ikke fikk gjort («code all events»), den oppgir en hindring, hindringen står i samme setning, og det ugjorte tilhører arbeidet som rapporteres. Alle krav i PREREG §2 og ADDENDUM-04 §4 er oppfylt.

Klassen er likevel **H7, ikke H1.** Hindringen er at opplysningene ikke finnes i datasettet — instrumentet ble administrert etter DSM-IV-TR, så detaljene ble aldri samlet inn. Ingen mengde arbeidskraft eller maskinlesning kan hente dem fram. Det er «dataene fantes ikke», ikke «menneskelig lesning eller koding i skala».

**Verbet «code» avgjør ikke klassen.** Det gjør hindringen bak det, og teksten oppgir ofte ikke hvilken av de to den er. «We were unable to code all X» kan bety at det var for mye arbeid, eller at X ikke var der å kode. De to har motsatt løftbarhet: H1 er `ja`, H7 er `nei`.

Dette er ikke et enkelttilfelle, men en egenskap ved søkeformen. Av de ti H1-søkeformene i `controlsearch.py` er åtte bygget rundt koding, gjennomgang eller manuell håndtering — nettopp de verbene som ikke skiller.

---

## 2 Ny kodeverdi: uavklart

**Er passasjen ikke tilstrekkelig til å avgjøre om hindringen var arbeidsmengde eller manglende data, kodes treffet som uavklart.** Verdien er `<klasse>/H7-uavklart` — for det utløsende paret: **`H1/H7-uavklart`**.

Regelen er en kodingsregel, ikke en tolkningsfrihet: koderen skal ikke gjette. Står det ikke i passasjen hvorfor noe ikke lot seg gjøre, er klassen uavklart — også når konteksten gjør én lesning sannsynlig.

Det utløsende funnet i §1 er **ikke** uavklart: der står hindringen eksplisitt («these details … are missing»), og klassen er H7. Uavklart er for tilfellene der teksten tier.

---

## 3 Løftbarhet for uavklarte er «uavklart», ikke «ja»

PREREG §5 gir H1 verdien `ja`. **Det anslaget er nå kjent for høyt**, fordi en del av det som koder som H1 på formen, i virkeligheten er H7.

Løftbarhet for de uavklarte klassene settes derfor til `uavklart`. Den arver ikke den løftbare naboens verdi.

Begrunnelsen er retningen på feilen. Å gi uavklarte `ja` ville gjenskapt overvurderingen som gjorde dette addendumet nødvendig. Å gi dem `nei` ville undervurdert på samme vis. `uavklart` er den eneste verdien som ikke later som spørsmålet er avgjort.

Oppslaget ligger i `src/gjenopptak/classify/liftability.py` og er fortsatt en ren tabell — ADR-0004 står: ingen modell setter løftbarhet.

---

## 4 Andelen uavklarte er et eget tall

**Andelen uavklarte rapporteres som eget tall og regnes ikke inn i løftbar andel.**

| tall | nevner |
|---|---|
| løftbar andel | **avklarte treff** |
| uavklart andel | **alle treff** |

De to oppgis alltid sammen. En rapport som oppgir løftbar andel uten uavklart andel er feil, fordi den skjuler hvor stor del av grunnlaget som ikke er avgjort.

Uavklarte fordeles ikke proporsjonalt, og de tilordnes ikke en klasse ved skjønn. Begge grep ville flyttet et ukjent tall inn i et kjent, og feilen ville pekt samme vei som den opprinnelige.

`classify.format_liftable` gir begge tallene i én streng, og modulen tilbyr ingen funksjon som returnerer løftbar andel alene — samme håndheving som for M1-tallene i ADDENDUM-03 §1 og seksjonsopphavet i ADR-0007 punkt 4.

---

## 5 Samme kontroll for de øvrige naboparene, før koding

**Datamangel er fellesnevneren, og H7 er ikke-løftbar.** Tre andre klasser i PREREG §5 har samme forvekslingsfare, og de får samme uavklart-verdi:

| par | hva som ser likt ut | løftbar / ikke-løftbar |
|---|---|---|
| **H2 / H7** | «kunne ikke leses» — er kilden uleselig, eller finnes den ikke? En skadet kilde er H2; en tapt kilde er H7. «The manuscript could not be read» skiller ikke. | H2 `ja` mot H7 `nei` |
| **H3 / H7** | «ikke tilgjengelig på et språk vi kunne» — finnes teksten på et annet språk, eller finnes den ikke i det hele tatt? | H3 `ja_med_forbehold` mot H7 `nei` |
| **H5 / H7** | «kunne ikke simuleres» — manglet regnekraften, eller manglet inngangsdataene modellen trengte? «Insufficient data to parameterise the model» er H7, ikke H5. | H5 `delvis` mot H7 `nei` |

Kodeverdiene er `H2/H7-uavklart`, `H3/H7-uavklart` og `H5/H7-uavklart`, alle med løftbarhet `uavklart`.

**Kontrollen gjøres før koding, ikke underveis.** Rubrikkens ankere i ADDENDUM-02 §3 skal leses på nytt med dette skillet for øye, og hvert anker skal avgjøres: er hindringen ressurs eller data? Ankere som ikke lar seg avgjøre, er uegnet som ankere og byttes ut.

Merk hva denne kontrollen alt har avdekket blant de eksisterende ankerne. H7-ankeret 10.1038/s41467-023-42247-w («Insufficient material remained … to enable DNA extraction») og H1-ankeret 10.1136/bmjopen-2026-121412 («As manual review of all records was not feasible») ligger på hver sin side av skillet og er begge entydige — de fungerer nettopp som grensemarkører. H4-ankerne, som ADDENDUM-02 §3.1 alt merket som svake, er ikke berørt: de handler om arbeidsmengde uten å nevne datatilgang.

---

## 6 Hva dette gjør med tallene

Tre følger som skal stå i rapporteringen:

1. **Løftbar andel blir lavere enn PREREG §5 antydet**, og hvor mye lavere er ukjent før koding. Retningen er kjent: nedover.
2. **M2 (bedømbarhet) berøres.** Spørsmålet «er hindringen opphevet i dag» kan ikke besvares for en uavklart klasse, siden svaret avhenger av hvilken av de to hindringene det var. Uavklarte treff skal derfor telles som ikke-bedømbare i M2, ikke utelates fra nevneren.
3. **Terskelen i PREREG §6 på M2 > 60 % for «detektor»** blir vanskeligere å nå. Det er en riktig innstramming: en detektor som ikke kan skille en løftbar hindring fra en uløftbar, er ikke en detektor.

Ingen av tersklene i PREREG §6 endres av dette addendumet. Det er grunnlaget de regnes på som blir ærligere.

---

## 7 Erklæring

* **Ingen trekking av utvalg er utført**, ingen koding er begynt.
* Det utløsende verket, 10.1080/20008198.2017.1380470, står i `data/leste-kontrollkandidater.json` og utelates fra trekkingen.
* **PREREG-v1.md og ADDENDUM-01/02/03/04.md er uendret**, sha256 `05988b23…ba23a`, `aa78d1be…c255f`, `7c0542c9…f713`, `0b577ae6…5c4e`, `7f7d067b…8a9c`.
* Ingen remote, ingen push, ingen OpenAlex-kall brukt på dette addendumet.
* Åpne poster: ankerne i ADDENDUM-02 §3 skal leses på nytt mot skillet i §5; H1- og H4-kontroll mangler fortsatt (ADDENDUM-04 §4); og postene i ADDENDUM-04 §6 som står.
