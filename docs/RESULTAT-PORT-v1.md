# Resultat — porten på de hundre (v1)

> **Oppdatert 2026-09-26 etter ADDENDUM-10 og ADDENDUM-11.** ADDENDUM-10 avgjorde de 48
> tvilstilfellene etter tre presiseringer av treffkravet, skrevet *etter* at data var sett; én av de
> 48 endret verdikt. ADDENDUM-11 kodet de samme 320 passasjene på nytt med en uavhengig instans.
>
> **Leseregel:** hvert tall i dette dokumentet er gjeldende der det står. Tall fra før ADDENDUM-10
> er merket «før ADDENDUM-10» i samme setning eller rad, aldri stående alene. Tall som bærer
> koderidentitet — presisjon, M2, løftbar andel, klassefordeling — er oppgitt for **begge** kodere.
> Sammenstillingene ligger i avsnittene **«Etter ADDENDUM-10»** og **«Uavhengig omkoding»** nederst.
>
> Rettet 2026-09-26: seksjonene over bar tall fra før ADDENDUM-10 uten at det gikk fram av
> seksjonen selv. En leser som startet øverst, fikk 71 % der resten av dokumentsettet sa 68 %.

Alle tall er målt, ikke anslått. Kilden står ved hvert tall. Ingen tall i dette dokumentet er nye:
de er hentet fra `data/port/presisjon-resultater.json`, `data/falsifisering-2026-09-21.json` og
`docs/LAERDOM.md`, som igjen bygger på de låste PREREG- og ADDENDUM-filene.

**Materialet:** 100 verk, 25 per felt (energimodellering, arkeologi, klinisk epidemiologi,
tekstvitenskap), 66 833 setninger → 22 243 passasjer à ±2 setninger. Dommer A (gemma2:9b, temp 0,
frø 734248, vekt-sha256 `ff1d1fc7…`) dømte alle 22 243 og fant 2 173 treff.
*Kilde: `data/port/spesifikasjon.json`, LAERDOM §12–13.*

## Hovedfunnet

**H7 er den største klassen i begge lesninger: spørsmålet ble parkert fordi dataene ikke fantes.**
**Koder 1: 17 av 25 ekte treff (68 %)** — resten H5 3, H8 2, H2 2, H9 1.
**Koder 2: 12 av 19 (63 %)** — resten H1/H7-uavklart 2, H9 2, H5 1, H2 1, H8 1.
*Før ADDENDUM-10 sto koder 1 som 17 av 24 (71 %) med H5 2.*
*Kilde: `koder2-sammenlikning.json` → `hovedtall`; `presisjon-resultater.json` for tallene før
ADDENDUM-10; LAERDOM §17, §20–21.* Det er ikke regnekraft, ikke lesekapasitet og ikke språk som stanser arbeidet i dette
materialet — det er kilder som aldri ble skapt, ikke overlevde, eller ikke ble målt.

## M1 — prevalens

| | M1-rå ≥1 | ≥2 | ≥3 | **M1-korrigert, koder 1** | **koder 2** |
|---|---|---|---|---|---|
| samlet | 0,93 | 0,85 | 0,83 | **0,671** (før ADDENDUM-10: 0,652) | **0,604** |
| uten de tre atypiske | 0,94 | 0,88 | 0,86 | 0,668 — *før ADDENDUM-10, ikke regnet om* | — |

M1-streng korrigert: **koder 1 0,667** (før ADDENDUM-10: 0,649) · **koder 2 0,599**.

M1-korrigert per felt, **før ADDENDUM-10 og ikke regnet om etterpå**: arkeologi 0,87 · klinisk
epidemiologi 0,75 · energimodellering 0,59 · tekstvitenskap 0,40. Bare presisjonen i
energimodellering flyttet seg (5,3 → 7,0 %), så det er det feltet der et omregnet tall ville skilt
seg mest fra det som står. *Kilde: `presisjon-resultater.json` → `M1` for feltene og tallene før
ADDENDUM-10; `koder2-sammenlikning.json` → `hovedtall` for de samlede.*

M1-streng og M1-passasje er like (0,93 mot 0,93), fordi dommeren merket 2 128 av 2 173 treff
(97,9 %) som samme setning. Følsomhetsanalysen ADDENDUM-03 §1.2 krever, måler derfor ingenting slik
den nå er bygget. *Kilde: LAERDOM §16.*

**M1-rå skal ikke rapporteres alene.** 0,93 er en grunnrate for dommeren, ikke en prevalens.

## M2 — bedømbarhet

**M2 finnes ikke som ett tall.** Koder 1: **88,0 % (22 av 25)** (før ADDENDUM-10: 87,5 %, 21 av 24).
Koder 2: **31,6 % (6 av 19)**. Samme 320 passasjer, samme ordlyd i protokollen.

Dommerens egne merker gir 10,5 %, men 1 688 av 2 173 er «usikker», så de merkene kan ikke brukes.
Spriket mellom koderne skyldes at PREREG-v1 §2 ikke definerer «uten domeneekspert» stramt nok til å
tvinge én lesning; tallet bærer koderidentitet eller ingenting. *Kilde: `koder2-sammenlikning.json`
→ `hovedtall`; `presisjon-resultater.json` → `M2_min_lesning`, `M2_dommerens`; ADDENDUM-11 §5.*

## Dommerens kvalitet

* **Presisjon, koder 1: 16,7 % (25 av 150), Wilson 11,6–23,4 %** (før ADDENDUM-10: 16,0 %, 24 av
  150, 11,0–22,7 %). **Koder 2: 12,7 % (19 av 150), Wilson 8,3–18,9 %.** Intervallene overlapper.
  Per felt, koder 1 → koder 2: arkeologi 26,0 → 22,0 · klinisk 22,2 → 22,2 · tekstvitenskap
  16,0 → 12,0 · energimodellering **7,0** (før ADDENDUM-10: 5,3) → 1,8 %.
  Per dømt klasse er H7 den eneste med signal: 21 av 63 = 33,3 %, uendret av ADDENDUM-10. H5 gikk
  fra 0 av 6 til 1 av 6, fordi den ene endrede saken (PS-031) var dømt H5. H5/H7- og
  H1/H7-uavklart holdt 0 av 40 også etter ADDENDUM-10.
  *Kilde: `koder2-sammenlikning.json` → `hovedtall`; `presisjon-resultater.json` → `presisjon`.*
* **Bom blant ikke-treffene, tredelt:** INGEN 2,0 % (1/50), N3 2,0 % (1/50), N1 0/37 og N2 0/13
  rått. Vektet med materialets fordeling: 2,0 %. *Samme kilde → `presisjon.ikke_treff`.*
* Omregnet, **før ADDENDUM-10 og ikke regnet om etterpå**: ≈348 ekte treff [239–493] blant de
  dømte, mot ≈401 tapte [110–1405] blant de 20 070 ikke-treffene → **implisert recall ≈ 46 %**.
  Med presisjonen etter ADDENDUM-10 (16,7 %) blir punktanslaget ≈363 i stedet for ≈348; intervallet
  er ikke regnet om, og recall-størrelsen ≈46 % er den manuskriptet oppgir. *Kilde: LAERDOM §16.*
* **Ankerne viser ingen drift:** 12 av 12 kjente treff og 8 av 8 kjente ikke-treff ble lest likt som
  fasiten skrevet før dommeren fantes; eksakt klasseenighet 75 % (9/12). De tre avvikene går mot
  H7 (to) og H1 (ett) — lesningen skyver i samme retning som dommeren når klassen settes.
  *Kilde: `presisjon-resultater.json` → `ankere`.*

## Løftbarhet

**Koder 1: 5 av 25 ekte treff (20,0 %) er i en løftbar klasse (H1–H6)** etter ADR-0004-tabellen: to
H2 og tre H5. 20 av 25 (80,0 %) er H7–H9. *Før ADDENDUM-10: 4 av 24 = 16,7 %, to H2 og to H5, og
20 av 24 = 83,3 % H7–H9.*
**Koder 2: 2 av 19 (10,5 %).** Ankerne gir **17–25 %** avhengig av om det ene H1/H7-uavklarte regnes
med (2 eller 3 av 12) — samme størrelsesorden som koder 1.
*Kilde: `koder2-sammenlikning.json` → `hovedtall`; `presisjon-resultater.json`, LAERDOM §17.*

**Beste AI-kandidat er funnet, vurdert og parkert på tilgang:** Heron-kollasjonen i W3000588547 (93 sider i tre British Library-håndskrifter) er den sterkeste av de fire løftbare, men hindringen har skiftet klasse siden publisering — H1 i 2019, H8 fra oktober 2023 da bildene falt ut av åpen kanal (ADR-0010, LAERDOM §18).

**Letekostnad, koder 1: ~30 dømte treff per løftbart ekte treff** (150 leste gav 5). Skalert til
materialet svarer det til om lag **72** løftbare ekte treff blant de 2 173 dømte. *Før ADDENDUM-10:
~37 per løftbart (150 gav 4), skalert ~58.* **Koder 2: ~75 per løftbart** (150 gav 2), skalert ~29.
Spennet mellom koderne, 29 mot 72, er større enn presisjonsintervallene og skal leses som en
størrelsesorden, ikke et anslag. *Utledet av `hovedtall` i `koder2-sammenlikning.json`.*

## Falsifisering

**Fire av de fem løftbare treffene er prøvd** mot de siterende arbeidene: ett `cites:`-oppslag og
ett `fulltext.search` på kjernebegrepene i det ugjorte, 36 kreditter i alt. Prøven ble kjørt
2026-09-21, da løftbar-listen hadde fire saker. **Den femte, PS-031, kom til med ADDENDUM-10
(2026-09-25) og er ikke prøvd.**

| kandidat | klasse | verk | siterende | fulltekstdekning | treff | utfall |
|---|---|---|---|---|---|---|
| PS-202 | H2 | W2936215896 | 12 | 58 % | 0 | overlever |
| PS-266 | H2 | W3217588367 | 0 | — | — | overlever |
| PS-119 | H5 | W2551114598 | 1 | 100 % | 0 | overlever |
| PS-246 | H5 | W2551114598 | 1 | 100 % | 0 | overlever |

*Kilde: `data/falsifisering-2026-09-21.json`.*

**Forbehold:** to av tre verk har 0 og 1 siterende arbeid. «Overlever» betyr her **ingen har
svart**, ikke at ingen kunne ha svart. Bare PS-202 har et siteringsgrunnlag som gjør et nullresultat
interessant, og der er fulltekstdekningen 58 % — fire av tolv siterende er usynlige for søket.

## Forbehold ved hele målingen

1. **To kodere, begge LLM-baserte; ingen menneskelig annotør.** *Rettet 2026-09-26: dette punktet
   sa «Én koder» og var innhentet av ADDENDUM-11.* De 320 passasjene er kodet to ganger — først av
   instansen som også bygget dommeren og ledeteksten, så av en separat instans med tom kontekst.
   κ = 0,81 [0,70–0,91] på treffbeslutningen, og hovedfunnet står i begge lesninger. To forbehold
   står igjen: **ingen menneskelig annotør har kodet materialet**, så κ mot menneskelig lesning er
   fortsatt umålt, og begge kodere deler modellfamilie og regelverk. Enigheten er dessuten ujevn
   mellom felt: κ = 1,00 i klinisk epidemiologi mot **0,39 i energimodellering**.
2. **Formålsvalgt utvalg.** Fire felt valgt for å spenne humaniora mot biomedisin, ikke trukket fra
   vitenskapen som helhet. Tallene gjelder disse fire feltene. *PREREG §4.*
3. **Hentbar-OA-seleksjon.** Rammen krever `is_oa:true` og at fulltekst faktisk lar seg hente.
   I energimodelleringsrammen var 9 713 av 30 362 verk hentbare (32,0 %). Det utvalget er ikke
   tilfeldig. *ADDENDUM-04 §1.1, LAERDOM §3.*
4. **Forleggerskjevhet.** Hentbarheten følger leveringen, ikke forretningsmodellen: ScienceDirect
   falt fra 1 994 til 30 verk, IOP fra 1 221 til 4, mens arXiv steg fra 4,7 til 14,5 % og MDPI fra
   6,8 til 17,4 % av rammen. Materialet er skjøvet mot preprint- og MDPI-lignende kanaler.
   *LAERDOM §3, ADDENDUM-08 §2.*
5. **Preregistreringen er ikke eksternt tidsstemplet før data.** PREREG-v1 og addenda ligger låst i
   git med sha256 og er uendret gjennom hele kjøringen, men uten ekstern tidsstempling (OSF eller
   liknende) hviler rekkefølgen på repoets egen historikk.
6. **Recall-enden er dårligst målt.** Intervallet for tapte treff spenner fra 110 til 1 405. Uten
   flere leste ikke-treff kan ikke recall strammes inn.

## Verksnivå — materialtilgang i de 100 verkene (2026-09-26)

Beslutningen om gjennomførbarhet er flyttet fra passasjen til verket, fordi 89,5 % av de dømte
løftbare passasjene ikke henviser til materiale i det hele tatt (ADDENDUM-12 §4). Kriteriet er avgjort
før tallene og kjørt på de 100 rådokumentene: **ÅPEN** = datatilgangserklæring for forfatterens egne
data *og* maskinlesbart materiale · **DELVIS** = én av de to, eller egne data på forespørsel, eller
erklæring bare for tredjeparts data · **LUKKET** = ingen av dem. *Kilde: ADDENDUM-13,
`verksniva-2026-09-26-v2.json` (Vault).*

| | ÅPEN | DELVIS | LUKKET |
|---|---|---|---|
| **gjeldende (v2, flerspråklige bildetekster)** | **3** | **55** | **42** |
| før språkrettingen (v1) | 3 | 49 | 48 |

Seks verk flyttet seg, alle **LUKKET → DELVIS**, ingen motsatt vei.

| felt | ÅPEN | DELVIS | LUKKET | *før språkrettingen: DELVIS / LUKKET* |
|---|---|---|---|---|
| arkeologi | 2 | 14 | 9 | *11 / 12* |
| energimodellering | — | 21 | 4 | *18 / 7* |
| klinisk epidemiologi | 1 | 18 | 6 | *18 / 6* |
| tekstvitenskap | — | 2 | **23** | *2 / 23* |

Blant de **52 verkene med minst ett løftbart dømt treff** er 43 ikke-LUKKET (før språkrettingen: 39).

**Tilgangen følger publiseringsformatet, ikke faget:**

| kilde | ÅPEN | DELVIS | LUKKET | sum | ikke LUKKET |
|---|---|---|---|---|---|
| **JATS** | **3** | 14 | **0** | 17 | **100 %** |
| HTML | 0 | 5 | 4 | 9 | 56 % |
| **PDF** | 0 | 36 | 38 | 74 | **49 %** |

Alle tre ÅPNE verk er JATS, og ingen JATS-verk er lukket. Tallet under: **bare 4 av 100 verk har en
datatilgangserklæring som dekker forfatterens egne data**, **29** omtaler tredjeparts data, og **67**
har ingen erklæring. Tilgang er «ikke nevnt» i 94 av 100, «åpne» i 4, «på forespørsel» i 2. Lisens er
ikke oppgitt i 54 verk, «All rights reserved» i 6.

### Blindtesten: fem enkelttilfeller, ikke en rate

Trukket med målefrø 734248 blant verk der materialtilgangen ikke alt var vurdert, rekkefølgen stokket,
nivået lagt i egen nøkkelfil, verdiktene skrevet og lagret **før** nøkkelen ble åpnet. Bestillingen var
3 ÅPNE + 3 LUKKEDE; **bare 2 ÅPNE var tilgjengelige, så trekket ble fem verk.** Fem er for få til et
tall med intervall.

| verk | min lesning | v1 | v2 |
|---|---|---|---|
| W7133387653 (energi, spansk) | DELVIS | **bom** | treff |
| W2614396966 (klinisk, konferansesammendrag) | LUKKET | treff | treff |
| W2897185883 (arkeologi, PLOS) | ÅPEN | treff | treff |
| W2898394602 (tekstvit., Cod Sang 555) | LUKKET | treff | treff |
| W2936215896 (arkeologi, PLOS) | ÅPEN | treff | treff |

**v1: fire av fem. v2: fem av fem.** Bommen hadde en målt systematisk årsak: kriteriet talte bare
engelske bildetekster, og **7 av 100 verk** hadde bildetekster på annet språk — alle sju lå i LUKKET,
seks av dem med ekte tabeller (spansk ×5, fransk ×1). De fire som traff i v1, flyttet seg ikke i v2,
så rettingen er ikke for bred.

### To grenser som følger med tallene

* **Kriteriet ser ikke H8-hindringer utenfor verket.** Heron-avhandlingen kommer ut LUKKET, men på
  grunnlag av sitt eget materiale (0 tabeller, 35 figurer, ingen erklæring) — den ekte hindringen er
  tilgang til tre håndskrifter i et annet bibliotek. **Utfallet er riktig av feil grunn.** Denne
  blindsonen kan ikke lappes med flere mønstre, fordi opplysningen ikke står i dokumentet.
* **Feilen er ensidig.** Et manglende mønster kan bare gjøre et verk *for* lukket, aldri for åpent.
  Rangeringen **underrapporterer gjennomførbarhet**. Den er brukbar til å **velge bort** — et verk som
  scorer ÅPEN, var åpent i 2 av 2 blindtilfeller — men **ikke til å avskrive**.

## Hva som står åpent

De 48 tvilstilfellene i `data/port-tvil.jsonl` er **avgjort** av ADDENDUM-10 (én endret verdikt);
tvilsmarkeringen står, fordi en avgjort tvil fortsatt er en sak der to lesninger var mulige.
*Dette avsnittet sa «uavgjort» til 2026-09-26.* De uavklarte klassene (H5/H7, H1/H7) holdt 0 av 40
og bør ikke telle i noe M1-tall før mekanismen er endret. Enheten (streng mot passasje) må avgjøres
av spennet i teksten, ikke av modellens eget svar.

Fortsatt åpent: **M2 er ikke operasjonalisert** (88,0 mot 31,6 % mellom koderne), **PS-031 er ikke
falsifiseringsprøvd**, **per-felt M1-korrigert er ikke regnet om etter ADDENDUM-10**, og **ingen
menneskelig annotør har lest materialet**.

## Etter ADDENDUM-10 (2026-09-25)

De 48 tvilstilfellene er avgjort: 7 under §1 (feltgap → ikke treff), 2 under §2 (oversiktsarbeid →
treff H7), 10 under §3 (modellbegrensning), og 29 utenfor reglene, avgjort på passasjen som før.
**Én verdikt endret seg:** PS-031 (energimodellering), der regnekraft er navngitt som grunn til at
etterspørselen grupperes i klasser — ikke treff før, treff i klasse H5 etter.

| tall | før ADDENDUM-10 | etter ADDENDUM-10 |
|---|---|---|
| presisjon samlet | 24/150 = **16,0 %** [11,0–22,7] | 25/150 = **16,7 %** [11,6–23,4] |
| arkeologi | 13/50 = 26,0 % | 13/50 = 26,0 % |
| klinisk epidemiologi | 4/18 = 22,2 % | 4/18 = 22,2 % |
| tekstvitenskap | 4/25 = 16,0 % | 4/25 = 16,0 % |
| energimodellering | 3/57 = 5,3 % | 4/57 = **7,0 %** |
| M1-passasje ≥1 / ≥2 / ≥3 | 0,930 / 0,850 / 0,830 | 0,930 / 0,850 / 0,830 |
| **M1-passasje korrigert** | **0,652** | **0,671** |
| M1-streng ≥1 / ≥2 / ≥3 | 0,930 / 0,850 / 0,820 | 0,930 / 0,850 / 0,820 |
| **M1-streng korrigert** | **0,649** | **0,667** |
| M2 på leste ekte treff | 21/24 = 87,5 % | 22/25 = **88,0 %** |
| løftbar andel (H1–H6) | 4/24 = 16,7 % | 5/25 = **20,0 %** |
| klassefordeling | H7 17, H5 2, H8 2, H2 2, H9 1 | H7 17, **H5 3**, H8 2, H2 2, H9 1 |
| bom blant ikke-treff (INGEN / N3 / vektet) | 2,0 / 2,0 / 2,0 % | uendret |

M1-rå er uendret ved alle tre tersklene: den teller dømte treff per verk, og ADDENDUM-10 rører ikke
dommerens utdata. Bare de korrigerte tallene flytter seg, fordi de hviler på den målte presisjonen.

**Hva endringen ikke er:** ingen klasse er lagt til eller omdefinert, og tallene flytter seg innenfor
konfidensintervallet fra før. At tre presiseringer skrevet etter data bare flytter én av 48 saker,
er den viktigste enkeltopplysningen i denne oppdateringen — hadde de flyttet mange, ville de vært
en regelendring i forkledning.

## Uavhengig omkoding (ADDENDUM-11, 2026-09-25)

De samme 320 passasjene ble kodet på nytt av en separat instans med tom kontekst, uten tilgang til
koder 1s verdikter, nøkkelfilen, dommerens utdata, LAERDOM, dette notatet eller manuskriptet.
**Koder 2-kolonnen står ved siden av koder 1, ikke i stedet for den.** Ingen sammenslått fasit er
laget, og ingen uenighet er brutt av en tredje stemme.

| tall | koder 1 | koder 2 |
|---|---|---|
| presisjon | 25/150 = **16,7 %** [11,6–23,4] | 19/150 = **12,7 %** [8,3–18,9] |
| presisjon per felt | ark 26,0 · klin 22,2 · tekst 16,0 · energi 7,0 % | ark 22,0 · klin 22,2 · tekst 12,0 · energi 1,8 % |
| M1-passasje korrigert | **0,671** | **0,604** |
| M1-streng korrigert | 0,667 | 0,599 |
| M1-rå ≥1 / ≥2 / ≥3 | 0,930 / 0,850 / 0,830 | uendret (rører ikke dommeren) |
| **M2 på leste ekte treff** | **22/25 = 88,0 %** | **6/19 = 31,6 %** |
| løftbar andel (H1–H6) | 5/25 = 20,0 % | 2/19 = 10,5 % |
| klassefordeling | H7 17, H5 3, H8 2, H2 2, H9 1 | H7 12, H1/H7-uavklart 2, H9 2, H5 1, H2 1, H8 1 |
| H7-andel av ekte treff | 68 % | 63 % |
| bom blant INGEN / N3 | 2,0 % / 2,0 % | 2,0 % / 2,0 % |

**Enighet:** κ = 0,812 [0,697–0,906] på treffbeslutningen over alle 320, κ = 0,774 [0,623–0,898] på
portmaterialet alene, κ = 0,732 [0,481–0,936] på klasse blant de 30 passasjene begge kodet som treff.
Rå enighet 96,2 % og 96,7 %.

**Per felt:** klinisk epidemiologi 1,000 · tekstvitenskap 0,847 · arkeologi 0,748 ·
**energimodellering 0,390**. **Seks av tolv** uenigheter om treffstatus gjelder samme strid: om en
modell-, metode- eller omfangsbegrensning har en navngitt hindring eller er en selvpålagt forenkling
(koder 2 kodet alle seks N3). Tre av de øvrige gjelder om passasjen besvarer sitt eget spørsmål, og
i tre fant koder 2 et treff koder 1 ikke fant.

**M2 rapporteres per koder.** PREREG-v1 §2 definerer ikke «uten domeneekspert», og de to lesningene
— hindringens art mot fagets nåværende metodelandskap — er begge forenlige med ordlyden. Begrepet er
ikke operasjonalisert, og tallet bærer koderidentitet eller ingenting.
