# ADDENDUM-13 — verket som beslutningsenhet, og hva materialtilgangen følger

**Skrevet:** 2026-09-26. **Gjelder:** PREREG-v1 §8 (hva verktøyet kan love) og ADDENDUM-12 §7.
**Forutsetning:** ADDENDUM-12 viste at 89,5 % av de dømte løftbare passasjene ikke henviser til
materiale i det hele tatt. Dette addendumet flytter derfor beslutningen ett nivå opp.

## 1 Hvorfor verket, ikke passasjen

**Passasjen bærer hindringen, verket bærer ressursen.** En forfatter som parkerer et spørsmål,
skriver hvorfor noe ikke ble gjort — ikke hvor materialet ligger. Datatilgangserklæring, supplementer,
tabellstruktur og lisens står et helt annet sted i teksten, i seksjoner som ingen treffpassasje
overlapper med.

Regnestykket følger av det: **100 verk mot 22 243 passasjer.** Beslutningen om gjennomførbarhet er
fire størrelsesordener billigere på verksnivå, og det er det eneste nivået der svaret finnes.

## 2 Kriteriet

Avgjort før tallene, på de 100 rådokumentene som alt lå på Vault (74 PDF, 17 JATS-XML, 9 HTML):

* **ÅPEN** = datatilgangserklæring som dekker **forfatterens egne** data og sier at de er
  tilgjengelige (arkiv, DOI, «within the paper», supplement) **og** materialet er maskinlesbart
  (JATS med strukturerte tabeller, eller minst halvparten av tabellene har tekstlag).
* **DELVIS** = nøyaktig én av de to · eller egne data bare «on request» · eller erklæringen dekker
  bare tredjeparts data.
* **LUKKET** = ingen erklæring som dekker egne data, og ingen tabeller med tekstlag.

Skillet mellom **egne** og **tredjeparts** data er nettopp det ADDENDUM-12 §6 fant at signal a ikke
klarte. Kriteriefilene ligger på Vault: v1 sha256
`af4fcc0ed06d5a221c293b779ba59354f290d96be807960ef0c57e45254f9f6e`, den språkrettede v2
`d410c73419406a739921aba63d08d25e32f59e6fe83ca033baafb36660978e13`.

## 3 Fordelingen, før og etter språkrettingen

| | ÅPEN | DELVIS | LUKKET |
|---|---|---|---|
| **v1 (engelske bildetekster)** | 3 | 49 | 48 |
| **v2 (flerspråklige)** | **3** | **55** | **42** |

**Seks verk flyttet seg, alle i samme retning: LUKKET → DELVIS.** Ingen flyttet motsatt vei, og ingen
ÅPEN endret seg.

| felt | ÅPEN | DELVIS v1 → v2 | LUKKET v1 → v2 |
|---|---|---|---|
| arkeologi | 2 | 11 → **14** | 12 → **9** |
| energimodellering | — | 18 → **21** | 7 → **4** |
| klinisk epidemiologi | 1 | 18 → 18 | 6 → 6 |
| tekstvitenskap | — | 2 → 2 | **23 → 23** |

Blant de **52 verkene med minst ett løftbart dømt treff** går «forsøk mulig» (ikke LUKKET) fra
**39 til 43**.

## 4 Blindtesten: fem tilfeller, ikke en rate

PS-246 og Heron er **røyktest, ikke validering**: kriteriet er formulert med begge i tankene, så et
treff viser bare at det ble skrevet etter dem — samme sirkularitet som markørlisten hadde etter
utvidelsen i ADDENDUM-06. Røyktesten peker riktig vei (PS-246-verket DELVIS, Heron LUKKET).

Den ekte testen ble trukket med målefrøet 734248 blant verk der materialtilgangen ikke alt var
vurdert, rekkefølgen stokket, nivået lagt i egen nøkkelfil, og verdiktene skrevet og lagret **før**
nøkkelen ble åpnet. **Bestillingen var 3 ÅPNE + 3 LUKKEDE; bare 2 ÅPNE var tilgjengelige, så trekket
ble fem verk.** Fem er for få til et tall med intervall, og rapporteres som fem enkelttilfeller.

| verk | min lesning | v1 | v2 |
|---|---|---|---|
| W7133387653 (energi, spansk) | DELVIS | **LUKKET — bom** | **DELVIS — treff** |
| W2614396966 (klinisk, konferansesammendrag) | LUKKET | treff | treff |
| W2897185883 (arkeologi, PLOS) | ÅPEN | treff | treff |
| W2898394602 (tekstvit., Cod Sang 555) | LUKKET | treff | treff |
| W2936215896 (arkeologi, PLOS) | ÅPEN | treff | treff |

**v1: fire av fem. v2: fem av fem.** De fire som traff i v1, flyttet seg ikke i v2 — rettingen er
altså ikke for bred.

## 5 Bommen hadde en systematisk årsak, og den er målt

W7133387653 er en spanskspråklig avhandling med **8 «Tabla» og 28 «Figura»**, talt som 0 tabeller av
et engelskspråklig mønster. Omfanget: **7 av 100 verk har null engelske «Table» men bildetekster på
annet språk, og alle 7 lå i LUKKET.** Seks av dem har ekte tabeller (spansk ×5, fransk ×1) =
**12,5 % av LUKKET-bunken**. Det sjuende (W2898394602) bruker «Illus» om illustrasjoner, ikke
tabeller, og står korrekt som LUKKET også etter rettingen.

**Feilen er ensidig.** Et manglende mønster kan bare gjøre et verk *for* lukket, aldri for åpent.
Rangeringen underrapporterer derfor gjennomførbarhet. **Den er brukbar til å velge bort — et verk som
scorer ÅPEN, var åpent i 2 av 2 blindtilfeller — men ikke til å avskrive.**

## 6 Blindsonen som ikke kan lappes med mønstre

**Heron kommer ut LUKKET av feil grunn.** Kriteriet leser verkets eget materiale og finner 0 tabeller,
35 figurer, ingen erklæring. Men den ekte hindringen er tilgang til tre håndskrifter i et *annet*
bibliotek (ADDENDUM-12 §7 og `docs/HERON-KOLLASJON-VURDERING-v2.md`). At utfallet ble riktig, er
tilfeldig sammenfall.

**Dette er en egen blindsone: H8-hindringer utenfor verket.** Den kan ikke lukkes ved å legge til
mønstre, fordi informasjonen ikke finnes i dokumentet — den finnes i et bibliotekskatalogsystem,
en tilgangspolicy eller en cyberangrepshistorie. Et verksnivåkriterium vil systematisk vurdere slike
tilfeller på det gale grunnlaget.

## 7 Materialtilgang følger publiseringsformat, ikke fag

| kilde | ÅPEN | DELVIS | LUKKET | sum | ikke LUKKET |
|---|---|---|---|---|---|
| **JATS** | **3** | 14 | **0** | 17 | **100 %** |
| HTML | 0 | 5 | 4 | 9 | 56 % |
| **PDF** | 0 | 36 | 38 | 74 | **49 %** |

**Alle tre ÅPNE verk er JATS.** Ingen JATS-verk er LUKKET. Grunnen ligger i det underliggende tallet:
**bare 4 av 100 verk har en datatilgangserklæring som dekker forfatterens egne data.** 29 omtaler
tredjeparts data, og **67 har ingen erklæring i det hele tatt**. Tilgangen er «ikke nevnt» i 94 av
100; «åpne» i 4, «på forespørsel» i 2. Lisens er ikke oppgitt i 54 verk, og 6 sier «All rights
reserved».

Erklæringen er altså ikke en egenskap ved faget, men ved **tidsskriftmalen**: der JATS-strukturen
tvinger en `Data Availability`-seksjon, finnes den; der dokumentet er en PDF-avhandling, finnes den
ikke. Tekstvitenskap har **23 av 25 lukkede** — ikke fordi feltet skjuler data, men fordi det
publiserer artikler og avhandlinger som PDF uten tabellstruktur.

**Dette er samme mønster som hentbarheten fulgte** (ADDENDUM-08 §2, LAERDOM §3): der falt 1 994
ScienceDirect-verk til 30 mens arXiv steg fra 4,7 til 14,5 %, og skillet fulgte leveringen, ikke
forretningsmodellen. Nå følger materialtilgangen publiseringsformatet, ikke disiplinen. **To
uavhengige målinger på ulike ledd i kjeden peker samme vei:** det som avgjør om et parkert spørsmål
kan gjenopptas, er infrastrukturen rundt publiseringen, ikke fagets innhold.

## 8 Hva dette ikke er

Ikke en måling av prevalens, ikke en revisjon av portens tall, og ikke en påstand om at de 43
«mulige» forsøkene vil lykkes. Kriteriet sier om materialet er *til stede og lesbart*, ikke om det er
*tilstrekkelig*. Blindtesten er fem tilfeller. De 214 uleste passasjene fra ADDENDUM-12 står uleste.
