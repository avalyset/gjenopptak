# ADDENDUM-19 — Opus via API som kalibrering av regelutdraget

**Skrevet:** 2026-09-27, **før kjøring**. **Kjøres ikke før eieren sier ja.**
**Gjelder:** ADDENDUM-18, og gyldigheten av å sammenligne κ på tvers av kodere.

## 1 Hvorfor dette addendumet finnes: en feil i ADDENDUM-18

ADDENDUM-18 § 2 sier at kandidatmodellen får «**nøyaktig det koder 2 fikk**». **Det er galt.**
Kontrollert mot ADDENDUM-11 § 2, ordrett:

> Den fikk nøyaktig to filer: blindfilen (320 rader, bare `id` og `tekst`, stokket) og en regelfil
> bygget av ordrette utdrag fra PREREG-v1 §2, PREREG-v1 §5, ADDENDUM-03 §1.2, ADDENDUM-05,
> ADDENDUM-04 §4 og ADDENDUM-10 §1–3.

Koder 2 fikk altså utdrag fra **seks** kilder. Haiku 4.5 og Sonnet 5 fikk **to**:
`blind-q-regler.md` (sha256 `00d69c09ed8b9045…`) med **PREREG-v1 § 2** og **ADDENDUM-10 § 3**.

**Det som manglet, er ikke pynt:**

| kilde koder 2 hadde | hva den avgjør |
|---|---|
| **PREREG-v1 § 5** | hele hindringstypologien H1–H9 **og** ikke-treffene N1–N3 |
| **ADDENDUM-03 § 1.2** | passasjeregelen: ugjort og hindring innenfor ±2 og **knyttet til hverandre** |
| **ADDENDUM-05** | de uavklarte parene (H1/H7 m.fl.) |
| **ADDENDUM-04 § 4** | at det ugjorte må tilhøre **arbeidet som rapporteres** |
| ADDENDUM-10 § 1–2 | feltgap og oversiktsarbeid |

**Følgen:** sammenligningen κ 0,266 (Haiku) mot κ 0,812 (koder 2) er **konfundert**. Den måler modell
*og* regelkontekst samtidig, og ADDENDUM-18 kan ikke skille dem. Feilen er ført som datert seksjon i
ADDENDUM-18 selv; den er ikke redigert bort.

## 2 Omskrevet 2026-09-27, før kjøring: hva ADDENDUM-20 gjorde med spørsmålet

ADDENDUM-20 kjørte Haiku 4.5 med koder 2s **fulle** regelfil og fikk **κ = 0,047** mot 0,270 med det
tynne utdraget — differanse −0,222, paret bootstrap [−0,402 – −0,044], utelukker 0. Full regelkontekst
gjorde kandidaten **dårligere**, ikke bedre. Kjøringen stoppet på tom API-kreditt etter 275 av 320, og
Sonnet 5 med full regelfil ble aldri målt.

Det flytter spørsmålet. «Var det for tynne regler?» er besvart for Haiku, og svaret er nei. Det som står
igjen, er en tabell med ett tomt felt:

| | tynt utdrag, ett kall per passasje | **full regelfil, ett kall per passasje** | full regelfil, én sammenhengende økt |
|---|---|---|---|
| Haiku 4.5 | 0,270 | **0,047** (ADDENDUM-20, partielt) | — |
| Sonnet 5 | 0,321 | **i kø** (ADDENDUM-20, ukjørt) | — |
| **Opus 5** | — | **DETTE ADDENDUMET** | **0,812** (koder 2) |

**Dette addendumet fyller Opus-cellen, og den avgjør hvilken av to forklaringer som står.** Med regelfil
og kallstruktur holdt fast mot ADDENDUM-20 isolerer den **modellen**. Med regelfil og modell holdt fast
mot koder 2 isolerer den **øktformen** — 320 uavhengige kall mot én økt der leseren bygger kontekst.

* **Opus ≈ 0,8:** modellen er forklaringen. Haiku og Sonnet er for svake til oppgaven, og kallstrukturen
  betyr lite.
* **Opus ≈ 0,3 eller lavere:** **øktformen** er forklaringen. Koder 2s 0,812 skyldes da at den leste alle
  320 i sammenheng og festet tolkningslinjer underveis — de tre ADDENDUM-11 §3.4 nevner — og et
  per-passasje-oppsett kan ikke nå dit uansett modell. Det ville være det mest konsekvensrike funnet i
  hele kandidatsporet, fordi hver eneste sil vi har bygget er per passasje.

## 3 Oppsettet, låst

| | verdi |
|---|---|
| modell | **`claude-opus-5`** — samme modell-ID som koder 2, gjenvunnet fra øktutskriften (ADDENDUM-11 §8) |
| passasjer | **samme 320**, `data/port-presisjonssett-ADDENDUM10.jsonl` |
| referanse | koder 1 etter ADDENDUM-10 |
| kall | **ett per passasje**, ingen kontekst mellom kall |
| regelfil | **koder 2s gjenvunnede fil**, `koder2/koderegler-gjenvunnet.md`, 9 805 B, sha256 `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449` — **samme fil som ADDENDUM-20 brukte**, med defektene intakte |
| svarkontrakt | `{"treff": bool, "begrunnelse": "<én setning>"}`, `max_tokens` 300 |
| temperatur | 0; avvises den, kjøres uten og føres per kall i `signatur.temperature_utelatt` |
| hurtigbuffer | `cache_control` ephemeral på systemblokken; `cache_creation`/`cache_read` føres per kall og rapporteres, også om den ikke slår inn |

**Regelfilen rettes ikke.** Koder 2 hadde `grep -n`-prefikset og den avkuttede tabellen; retter vi det,
måler vi ikke lenger samme cellen.

### 3b Datert teknisk rettelse 2026-09-27: `max_tokens` heves til 2 000, og første kjøring er ugyldig

**Første kjøring (`max_tokens` 300) er teknisk ugyldig. Årsak: avkutting.** Av 320 svar var **36
uparsebare, og alle 36 hadde `output_tokens` = 300**, altså nøyaktig taket — 23 av dem helt tomme fordi
hele budsjettet gikk før teksten. Median utdata for de **gyldige** svarene var 95 tokens, 95-persentilen
239. Taket bandt bare halen, og halen var ikke tilfeldig: **27 av koder 1s 39 treff (69 %) ligger i det
avkuttede settet.** κ målt på de 284 parsebare er derfor målt på et delsett som mangler to tredeler av
treffene, og tallet er ikke et utsagn om Opus.

`stop_reason` ble ikke lagret i loggradene — bare `usage` — så avkuttingen er påvist med
`output_tokens` mot taket, ikke med API-feltet. Det er en mangel i loggformatet, og den er reell.

**ADDENDUM-19b: identisk kjøring med `max_tokens` = 2 000.** Samme modell, samme regelfil (sha256
`234695dd4e1777a9…`), samme 320 passasjer, samme svarkontrakt, samme temperatur-håndtering, samme
hurtigbuffer. **Eneste endring er taket**, og 2 000 kan ikke binde: 95-persentilen for gyldige svar var
239. Utdata til `addendum-19/opus5-b-dommer.jsonl`.

**Begge κ føres, og den første beholdes merket ugyldig med årsak.** Den slettes ikke.

**Samme behandling for de øvrige avkuttede passasjene.** Målt på alle kjøringer med taket 300:

| kjøring | uparsede | av dem avkuttet (ut = 300) | helt tomme |
|---|---|---|---|
| ADDENDUM-19 Opus 5 | 36 | **36** | 23 |
| **ADDENDUM-18 Sonnet 5 pass 1** | 13 | **12** | 10 |
| ADDENDUM-18 Haiku 4.5 | 5 | **1** | 0 |
| ADDENDUM-20 Sonnet 5 | 1 | 0 | 1 (tomt svar, ikke avkutting) |
| ADDENDUM-20 Haiku 4.5 | 4 | 0 | 0 |

**ADDENDUM-18s Sonnet-tall er altså rammet av samme feil**: 12 av 320 passasjer ble avkuttet, og κ = 0,321
er målt uten dem. De 13 avkuttede passasjene (12 Sonnet + 1 Haiku) kjøres om med taket 2 000, logges i
`addendum-18/<modell>-avkuttet-rekjort.jsonl`, og ADDENDUM-18s κ regnes på nytt med dem inne. Det gamle
tallet beholdes ved siden av, merket med hvor mange passasjer som manglet.

## 4 Kriteriet, låst før kjøring

κ mot koder 1 over alle 320, paret bootstrap 10 000 gjentak, frø 734248. κ over de 300 portpassasjene
rapporteres ved siden av.

| utfall | slutning |
|---|---|
| **innenfor koder 2s intervall 0,712–0,917** | modellen er forklaringen; per-passasje-oppsettet er ikke hindringen |
| **≥ 0,70 men utenfor intervallet** | modellen bærer det meste, øktformen noe |
| **0,30–0,70** | begge bidrar; ingen enkel forklaring står |
| **under 0,30**, altså i Haikus og Sonnets klasse | **øktformen er forklaringen.** Da er ikke kandidatsporets problem modellvalget, men at vi har spurt per passasje |

**Differansen mot ADDENDUM-20s Haiku rapporteres med paret bootstrap** på de passasjene begge har
parsebart svar for. Et løft som ikke overlever intervallet, er ikke et løft.

## 5 Kostnadsgrunnlag, målt — og køen

**Kreditten er tom.** ADDENDUM-20 stoppet på `Your credit balance is too low to access the Anthropic
API`. Dette addendumet kjøres **når kreditt finnes**, ikke før, og ingen annen nøkkel forsøkes.

Målt fra ADDENDUM-20s Haiku-kjøring med samme regelfil: **3 852 tokens inn per kall** uten hurtigbuffer
(prefikset er 3 703 tokens, under Haikus minstelengde). For Opus 5 er minstelengden lavere, og
kanaritesten på Sonnet 5 viste at bufferen da slår inn: `input_tokens` faller til 47 og prefikset leses
fra buffer. Anslag for 320 kall, som **budsjett og ikke resultat**:

* **uten buffer:** ≈ 1,23 M tokens inn, ≈ 25 000 ut
* **med buffer:** ≈ 4 705 skrevet én gang, deretter ≈ 517 effektivt per kall ≈ 0,17 M inn

**Køen, i denne rekkefølgen, når kreditt finnes:**

1. **Dette addendumet** — Opus 5, full regelfil, ett kall per passasje. Fyller den tomme cellen.
2. **ADDENDUM-20, Sonnet 5 med full regelfil** — fullfører den halve sammenlikningen der.
3. ADDENDUM-20s Haiku-rest, de 45 passasjene som ikke ble dømt, hvis noen vil ha κ på hele 320.

**ADDENDUM-22s rute c er ikke betinget av noen av disse.** Rute c er valgt fordi ingen kandidat er
dokumentert over 0,70, og et senere Opus-resultat endrer ikke den porten — det ville i så fall være
grunnlag for et nytt addendum, ikke en omskriving av dette.

## 6 Hva kalibreringen ikke avgjør

* **Ikke om koder 1 har rett.** Referansen er koder 1, ikke sannheten.
* **Ikke noe om menneskelig lesning.** Ingen menneskelig annotør har lest materialet.
* **Ikke om Opus er en god dommer i drift.** Opus leser dette sporet og er derfor ikke kandidat i
  ADDENDUM-18; her brukes den bare som målestokk på regelutdraget, på materiale den ikke har sett
  verdiktene til.
* **Ikke hvor mye av materialet som i det hele tatt er tekst.** Målt separat: **27,4 % av de 22 243
  tekstbitene og 22,5 % av de 2 173 flaggede er ikke prosa** etter en fast regel (under 50 % bokstaver
  eller referansemønster), `ekstraksjon/2026-09-26/g3-ikke-prosa.json`. Et κ-tall bærer den
  forurensningen uansett hvilken modell som leser.

## 7 Utfall 2026-09-27 — 19b: κ = 0,636, og modellen forklarer mesteparten

**ADDENDUM-19b, `max_tokens` = 2 000: 320 av 320 dømt, 0 uparsede, 0 avkuttede.** Maks utdata ble 1 360
tokens, så det gamle taket på 300 bandt grovt, og 2 000 bandt ikke. Tall i
`ekstraksjon/2026-09-26/a19b-utfall.json`.

| kjøring | tak | uparsede | n | rå enighet | κ mot koder 1 | 95 % KI |
|---|---|---|---|---|---|---|
| ADDENDUM-19, Opus 5 | 300 | 36 (alle avkuttet) | 284 | 96,8 % | **0,390** | 0,000–0,690 **UGYLDIG** |
| **ADDENDUM-19b, Opus 5** | **2 000** | **0** | **320** | 93,8 % | **0,636** | **0,478–0,768** |

Den ugyldige kjøringen beholdes, merket, og slettes ikke.

**2×2 for 19b:** 20 av koder 1s 39 treff funnet, 19 mistet, **bare 1 falsk positiv**, 280 begge enige om
ikke-treff. Opus er altså **presis** (21 flaggede, 20 riktige) men mister halvparten.

### 7.1 Cellen er fylt, og svaret er at modellen dominerer

Med **samme regelfil og samme kallstruktur** — ett kall per passasje, koder 2s fulle regelfil:

| modell | κ mot koder 1 | 95 % KI | flagget treff |
|---|---|---|---|
| Haiku 4.5 | 0,031 | −0,024–0,129 | 3 |
| Sonnet 5 | 0,294 | 0,126–0,455 | 14 |
| **Opus 5** | **0,636** | **0,478–0,768** | **21** |
| koder 2 (Opus, **én sammenhengende økt**) | 0,812 | 0,712–0,917 | — |

**Modellkapasitet dominerer.** Rekken 0,03 → 0,29 → 0,64 er monoton og spennene overlapper ikke mellom
Haiku og Opus. Det er det klareste funnet i hele kandidatsporet, og det snur konklusjonen i ADDENDUM-20
§7: full regelkontekst gjorde *Haiku* dårligere, men det var en egenskap ved Haiku, ikke ved reglene —
Opus bruker de samme reglene til κ = 0,64.

### 7.2 Øktformens bidrag er **ikke** påvist

§4s kriterium plasserer κ = 0,636 i båndet **0,30–0,70: «begge bidrar, ingen enkel forklaring står»**. Det
er utfallet, og det føres som det.

**Men differansen mot koder 2 er ikke statistisk etablert.** 19b gir [0,478–0,768], koder 2 gir
[0,712–0,917] — **intervallene overlapper i 0,712–0,768**. Punktanslagene skiller 0,176, og det er en
reell forskjell i retning av at én sammenhengende økt hjelper, men den er ikke skilt fra støy. Den
sterkeste påstanden materialet bærer, er: **modellvalget forklarer mesteparten av gapet; en eventuell
resteffekt av øktformen er mulig og umålt.**

Det som *kunne* avgjort det, er en Opus-kjøring i én sammenhengende økt på de samme 320 — altså en
gjentakelse av koder 2 med registrering. Det er ADDENDUM-21 arm A, som står ukjørt.

### 7.3 Følgen for ADDENDUM-18: Sonnets κ rettes fra 0,321 til 0,297

De 13 avkuttede passasjene (12 Sonnet, 1 Haiku) ble kjørt om med taket 2 000, samme **tynne** regelfil
(`00d69c09ed8b9045`) som originalkjøringen.

| | før | med rekjørte |
|---|---|---|
| ADDENDUM-18 Sonnet 5 pass 1 | κ = 0,321 [0,137–0,493], n = 307 | **κ = 0,297 [0,125–0,456], n = 319** |
| ADDENDUM-18 Haiku 4.5 | κ = 0,266 [0,108–0,421], n = 315 | **uendret**, κ = 0,266, n = 315 |

Sonnets tall faller litt: de 12 gjenvunne passasjene ga 1 nytt riktig treff, 4 nye feil, og nevneren vokste.
**Slutningen i ADDENDUM-18 §7 står — Sonnet er langt under 0,70 — men tallet som skal siteres er 0,297 med
n = 319, ikke 0,321 med n = 307.**

Haiku endres ikke, av en grunn som er verdt å føre: **den ene passasjen ble uparsebar igjen, nå med
`output_tokens` = 2 000.** Det er ikke et takproblem lenger; den passasjen får Haiku til å produsere
ubegrenset utdata. Den står som uparset, telt og ikke fylt inn.
