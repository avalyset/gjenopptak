# ADDENDUM-20 — kandidater under Opus med koder 2s regelfil

**Skrevet:** 2026-09-27, **før kjøring.** **Gjelder:** om ADDENDUM-18s utfall skyldes modellen eller
regelkonteksten.

## 1 Hvorfor

ADDENDUM-18 målte to kandidater mot koder 1 og fikk κ = 0,266 (Haiku 4.5) og 0,321 (Sonnet 5), mot
koder 2s 0,812. Den datert rettelsen i ADDENDUM-18 slo fast at sammenlikningen ikke var rettferdig:
**kandidatene fikk et regelutdrag med to kilder** (PREREG-v1 §2 + ADDENDUM-10 §3,
sha256 `00d69c09ed8b9045`), **koder 2 fikk seks** (PREREG-v1 §2, PREREG-v1 §5, ADDENDUM-03 §1.2,
ADDENDUM-05, ADDENDUM-04 §4, ADDENDUM-10 §1–3). To forklaringer sto åpne: kandidatene er svakere
lesere, eller de leste tynnere regler.

Dette addendumet skiller dem. **Alt holdes fast unntatt regelfilen.**

## 2 Regelfilen

Koder 2s regelfil, gjenvunnet 27.09.2026 fra koder 2s egen øktutskrift og dokumentert i ADDENDUM-11
§8: **167 linjer, 9 805 bytes, sha256
`234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449`**, på Vault som
`koder2/koderegler-gjenvunnet.md`. Ikke rekonstruert.

**Filen brukes med defektene sine intakte.** ADDENDUM-05-blokken bærer `grep -n`-prefiks, seks linjer
i spennet 29–72 er utelatt, og tabellen med de tre øvrige uavklarte parene mangler. Å rette det ville
gitt kandidatene bedre regler enn koder 2 hadde, og da måler ikke tallet det det skal.

## 3 Oppsettet

Identisk med ADDENDUM-18 på alle punkter unntatt ett:

| | ADDENDUM-18 | ADDENDUM-20 |
|---|---|---|
| passasjer | 320, `data/port-presisjonssett-ADDENDUM10.jsonl` | **samme 320** |
| referanse | koder 1 etter ADDENDUM-10 | **samme** |
| kall | ett per passasje | **samme** |
| svarkontrakt | `{"treff": bool, "begrunnelse": "<én setning>"}` | **samme** |
| `max_tokens` | 300 | **samme** |
| temperatur | 0; utelatt og ført per kall der modellen avviser den | **samme** |
| **regelfil** | **to kilder, `00d69c09ed8b9045`** | **seks kilder, `234695dd4e1777a9`** |

Svarkontrakten holdes med vilje lik ADDENDUM-18 og ikke lik koder 2s (`id`, `ekte_treff`,
`min_klasse`, `min_bedømbar`, `tvil`, `begrunnelse`), fordi κ måles på treffstatus. Ett forsøk skal
endre én ting.

**Hurtigbuffer.** Regelfilen er identisk prefiks i alle 320 kall og legges i systemledeteksten med
`cache_control: {"type":"ephemeral"}`. `cache_creation_input_tokens` og `cache_read_input_tokens`
føres per kall fra `usage` og rapporteres. Slår bufferen ikke inn — for eksempel fordi prefikset er
kortere enn modellens minstelengde — skal det stå, ikke utelates.

## 4 Terskelen, fastsatt før kjøring

**κ mot koder 1 over alle 320:**

* **≥ 0,70:** kandidaten er **detektor** med disse reglene. ADDENDUM-18s utfall var da en egenskap ved
  regelutdraget, ikke ved modellen, og kandidatsporet er åpent igjen.
* **< 0,70:** kandidaten er **sil-klasse også med full regelkontekst**. Da er ikke tynne regler
  forklaringen, og forskjellen mot koder 2 ligger et annet sted: modellklasse, eller at koder 2 leste
  alle 320 i én sammenhengende økt mens kandidaten får dem én for én.

**κ over de 300 portpassasjene** (uten de 20 ankerne) rapporteres ved siden av, ikke i stedet for.
Begge med paret bootstrap, 10 000 gjentak, frø 734248.

**Differansen mot ADDENDUM-18 rapporteres som et tall med intervall**, på de passasjene begge kjøringene
har parsebart svar for. Et løft som ikke overlever intervallet, er ikke et løft.

## 5 Hva dette ikke kan vise

* **Ingenting om menneskelig lesning.** Ingen menneskelig annotør har lest materialet. Alle kodere i
  dette sporet er LLM-baserte, og koder 2 var en CC-instans (Opus 5, agentisk), ikke et menneske.
* **Ett kall per passasje er ikke koder 2s oppsett.** Koder 2 leste alle 320 i én økt, i blindfilens
  rekkefølge, og kunne bygge tolkningslinjer underveis — de tre ADDENDUM-11 §3.4 nevner. Kandidaten
  her starter tom for hver passasje. Forskjellen er tilsiktet (den gjør kallene uavhengige), men den
  er en forskjell, og en κ under terskelen kan skyldes den like godt som modellklassen.
* **Ingen modell-ID for koder 2.** ADDENDUM-11 fører ingen modellsignatur for koder 2, i strid med
  ADR-0003. «Opus 5» er eierens opplysning. Sammenlikningen mot 0,812 bærer det hullet.
* **Reglene er defekte på samme vis for begge.** Det gjør sammenlikningen gyldig og resultatet
  strengere: ingen av leserne hadde de tre uavklarte parene.

## 6 Dødsbetingelser

* Kandidaten kjøres **én gang** per modell. Ingen ny ledetekst, ingen ny svarkontrakt, ingen ny
  regelfil hvis tallet blir lavt. Blir det lavt, er det utfallet.
* **401/403:** stopp, rapporter, ikke bytt nøkkel.
* Uparsebare svar telles og rapporteres som uparsede; de fylles ikke inn med en gjetning og
  behandles ikke som «ikke treff».
* **Opus (ADDENDUM-19) kjøres ikke** i dette addendumet.
* Haiku 4.5 kjøres nå. Sonnet 5 kjøres når ADDENDUM-17/ADDENDUM-18 pass 2 er ferdig — den er ferdig
  (320/320), så begge kjøres i denne slyngen.

## 7 Utfall 2026-09-27 — AVBRUTT, og hypotesen faller i motsatt retning

**Kjøringen er avbrutt.** Haiku 4.5 dømte **275 av 320** passasjer, så svarte API-et HTTP 400 med
`Your credit balance is too low to access the Anthropic API`. Det er «nøkkelen er uten kreditt», altså
stoppbetingelsen i §6, og kjøringen ble drept. **Sonnet 5 startet aldri.** Ingen annen nøkkel er
forsøkt, ingen nøkkel er laget. Tall i `ekstraksjon/2026-09-26/addendum-20/a20-partiell.json`.

**De 275 er ikke et skjevt utsnitt.** Prefikset er ikke et tilfeldig utvalg, så det er kontrollert
først: arkeologi 29,1 % mot 29,4, energimodellering 32,0 mot 31,6, klinisk epidemiologi 16,7 mot 16,2,
tekstvitenskap 16,0 mot 16,6; 17 av 20 ankere; koder 1s sanne treff 11,3 % mot 12,2 %. Avvikene er
under ett prosentpoeng, og den partielle κ er dermed lesbar — men den er ikke terskelmålingen §4 satte,
som gjaldt alle 320.

**Partielt utfall, Haiku med full regelfil:** 4 uparsede, n = 271, rå enighet 88,6 %,
**κ = 0,047 [−0,020–0,168]**. 2×2 mot koder 1: 1 treff begge, 30 treff koder 1 fant og kandidaten ikke,
1 kandidaten fant alene, 239 begge ikke.

### Side om side: tynt utdrag mot full regelfil, samme passasjer

Sammenlikningen er paret — de samme 269 passasjene har parsebart svar i begge kjøringer — så den er
gyldig selv om kjøringen ble avbrutt:

| Haiku 4.5, samme 269 passasjer | regelkilder | κ mot koder 1 | 95 % KI | flagget treff |
|---|---|---|---|---|
| ADDENDUM-18, `00d69c09ed8b9045` | **2** | **0,270** | 0,091–0,444 | **22** |
| ADDENDUM-20, `234695dd4e1777a9` | **6** | **0,047** | −0,021–0,168 | **2** |

**Differanse −0,222, paret bootstrap [−0,402 – −0,044], 10 000 gjentak, frø 734248. Intervallet
utelukker 0.** 20 av 269 verdikter endret seg, 7,4 %.

**Hypotesen faller, og den faller i motsatt retning enn ventet.** ADDENDUM-18 §7 lot to forklaringer
stå: svakere leser, eller tynnere regler. Dette måler den andre og avviser den — **full regelkontekst
gjorde kandidaten målbart dårligere, ikke bedre.** Mekanismen står i siste kolonne: med to regelkilder
flagget Haiku 22 treff, med koder 2s seks flagget den **2**. Reglene den fikk i tillegg — ADDENDUM-04
§4s krav om at det ugjorte må tilhøre arbeidet som rapporteres, ADDENDUM-10s tre presiseringer,
ADDENDUM-03 §1.2s passasjekrav — er alle *innsnevrende*, og kandidaten anvendte dem så strengt at den
nesten sluttet å flagge. Koder 2 leste de samme reglene og fikk κ = 0,812. Forskjellen ligger altså
ikke i regelteksten.

**§4s terskel er ikke avgjort.** κ over alle 320 ble ikke målt, og Sonnet ble ikke målt i det hele
tatt. Men retningen er entydig nok til at «kandidatene hadde for tynne regler» ikke lenger er en åpen
forklaring for Haiku: mer regel ga mindre κ, med et intervall som utelukker null.

**Hva som gjenstår, og hva det koster.** Sonnet 5 med full regelfil krever kreditt som ikke finnes.
Kostnaden er målt, ikke anslått: Haiku brukte **1 059 182 tokens inn og 20 181 ut på 275 kall** — 3 852
tokens per kall mot ADDENDUM-18s 735, altså **5,2 ganger dyrere per passasje**, fordi regelfilen er
identisk prefiks i hvert kall og **hurtigbufferen ikke slo inn for Haiku 4.5** (prefikset var 3 703
tokens). For Sonnet 5 slo den inn i kanaritesten — 4 705 tokens skrevet, deretter lest, og
`input_tokens` falt til 47 — så en Sonnet-kjøring ville kostet langt mindre per kall enn Haikus. Det er
ført her fordi §3 krevde det rapportert uansett utfall.
