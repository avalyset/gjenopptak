# ADDENDUM-18 — frontier under Opus som dommer: preregistrert, ukjørt

**Skrevet:** 2026-09-27, **før** noen nøkkel finnes og før noe er kjørt. **Gjelder:** PREREG-v1 §2, §8
og ADR-0003 (modellsignatur). **Status: preregistrert og ukjørt** — se §6.

## 1 Hvorfor spørsmålet stilles nå

Den lokale dommeren (gemma2:9b) er målt fra flere kanter, og bildet er entydig:

| måling | verdi | kilde |
|---|---|---|
| presisjon blant flaggede | 16,7 % [11,6–23,4] | `data/port-presisjonssett-ADDENDUM10.jsonl` |
| implisert recall | ≈ 47,5 % | `data/port/presisjon-resultater.json` |
| **κ mot en blind leser av samme modellfamilie** | **0,289** | `ekstraksjon/2026-09-26/d1-2x2.json` |

Den siste er ny og er grunnen til dette addendumet. **En dommer som er uenig med en blind leser av sin
egen modellfamilie på to av tre linjer, måler ikke regelen — den måler seg selv.** Spørsmålet er om en
sterkere modell under Opus treffer regelen godt nok til å kalles en detektor, eller om den også bare er
en sil.

## 2 Materialet, låst

**De 320 verdiktene i presisjonssettet**, `data/port-presisjonssett-ADDENDUM10.jsonl`, med **koder 1 som
referanse** (`ekte_treff`). Fordelingen er kjent og røres ikke: 150 dommer-flaggede, 50 dømt INGEN, 50
N1/N2, 50 N3, 20 ankere. Sanne hos koder 1: 25 + 1 + 0 + 1 + 12.

Kandidatmodellen får **nøyaktig det koder 2 fikk**: blindfilen med `id` og `tekst`, og et regelutdrag
bygget av ordrette avsnitt fra **PREREG-v1 § 2** og **ADDENDUM-10 § 3** — ingenting annet. Ikke koder 1s
verdikter, ikke nøkkelfilen, ikke dommerutdata, ikke LAERDOM, ikke resultatnotatet, ikke registeret.

## 3 Kandidater

* **Haiku 4.5** (`claude-haiku-4-5-20251001`)
* **Sonnet 5** (`claude-sonnet-5`)

Opus selv er ikke kandidat: den leser dette sporet og kan ikke måles blindt mot sin egen fasit.

## 4 Kriteriet, låst

**κ ≥ 0,70 på treffbeslutningen (treff / ikke treff) over alle 320, mot koder 1, lever.**
**Under 0,70 er modellen sil-klasse** — den kan brukes til å redusere en mengde, ikke til å avgjøre om
noe er et treff.

Referansepunkter som er målt og ikke kan flyttes etterpå: koder 2 (samme familie som koder 1) fikk
**κ = 0,812 [0,697–0,906]**; den lokale dommeren mot en blind leser fikk **κ = 0,289**. Terskelen 0,70
ligger under koder 2 og godt over den lokale dommeren, og er valgt før kandidatene er kjørt.

κ regnes med `gjenopptak.classify.reliabilitet` (Cohen, paret bootstrap, 10 000 repetisjoner, frø
734248) — samme kode som ADDENDUM-11.

## 5 Signatur og kostnad

Hver kjøring logger, etter ADR-0003: modell-id med versjonsstreng, temperatur **0**, `max_tokens`,
ledetekst-sha256, tidspunkt, og tokens inn og ut per kall som API-et rapporterer.

Volumet er kjent: **de 320 med ±2 og kriteriet i hver prompt er 0,418 M tokens inn** (målt anslag,
1,653 tokens per ord, `ekstraksjon/2026-09-26/d2-tokenvolum.json`). **Ingen prisoppslag er gjort, og
ingen kostnad påstås.**

## 6 Kjørebetingelsen, og hvorfor dette addendumet står ukjørt

**Kjøres bare hvis en nøkkel ligger i miljøet.** Kontrollert 2026-09-27: `ANTHROPIC_API_KEY`,
`CLAUDE_API_KEY` og `ANTHROPIC_KEY` er ikke satt, og `~/.env` inneholder ingen `ANTHROPIC`- eller
`sk-ant`-streng (0 treff; bare `GEMINI_API_KEY` og tre Tripletex-variabler, kontrollert på variabelnavn
uten å lese verdier).

**Addendumet står derfor som preregistrert og ukjørt.** Når en nøkkel finnes, verifiseres den i samme
prosess med `len()` og `startswith()`, aldri skrevet ut, og kjøringen skjer uten at kriteriet i § 4
røres. Utfallet føres som et tillegg her, med dato.

## 7 Hva testen ikke kan avgjøre

* **Ikke om koder 1 har rett.** Referansen er koder 1, ikke sannheten. En kandidat som er uenig med
  koder 1, kan ha lest riktigere; κ måler samsvar, ikke gyldighet.
* **Ikke noe om menneskelig lesning.** Ingen menneskelig annotør har kodet dette materialet, og det
  forblir den største åpne posten uansett hva κ blir.
* **Ikke prevalens.** De 320 er et stratifisert utvalg av dommerens flagg; et bedre κ endrer ikke
  grunnraten i `docs/METODE.md` § 1.

## Rettelse 2026-09-27, samme døgn: § 2 sa mer enn som var sant

**§ 2 påstår at kandidatmodellen får «nøyaktig det koder 2 fikk». Det er galt, og påstanden er ikke
redigert bort — den står med denne rettelsen under.**

Koder 2 fikk, etter ADDENDUM-11 § 2 ordrett, «en regelfil bygget av ordrette utdrag fra PREREG-v1 §2,
PREREG-v1 §5, ADDENDUM-03 §1.2, ADDENDUM-05, ADDENDUM-04 §4 og ADDENDUM-10 §1–3» — **seks kilder**.
Haiku 4.5 og Sonnet 5 fikk **to**: PREREG-v1 § 2 og ADDENDUM-10 § 3, filen `blind-q-regler.md`,
sha256 `00d69c09ed8b9045…`, som ble bygget for den blinde presisjonsmålingen i steg 2d og gjenbrukt her.

**Det manglet dermed:** hindringstypologien H1–H9 og ikke-treffene N1–N3 (PREREG-v1 § 5),
passasjeregelen med koblingskravet (ADDENDUM-03 § 1.2), de uavklarte parene (ADDENDUM-05), kravet om at
det ugjorte tilhører arbeidet som rapporteres (ADDENDUM-04 § 4), og ADDENDUM-10 § 1–2.

**Hva det gjør med tallene i dette addendumet:** κ-ene er målt som angitt og står, men
**sammenligningen mot koder 2s 0,812 er konfundert** — den måler modell og regelkontekst samtidig.
Utfallet «sil-klasse» gjelder derfor **kandidaten lest under dette utdraget**, ikke kandidaten som
modell. **ADDENDUM-19** avgjør hvilken av de to som svikter, ved å kjøre `claude-opus-5` på samme 320
med samme utdrag; under 0,70 der betyr at dette addendumet ikke kan avskrive noen modell.

Terskelen på 0,70 er ikke rørt, og ingen κ er regnet om.

## 7 Utfall 2026-09-27

**Begge kandidatene faller. Terskelen var 0,70 over 320; ingen kommer i nærheten.** Tall fra
`ekstraksjon/2026-09-26/addendum-18/a18-kappa.json`.

| | dømt | uparsede | n | rå enighet | κ mot koder 1 | 95 % KI | κ kun port |
|---|---|---|---|---|---|---|---|
| Haiku 4.5 | 320 | 5 | 315 | 86,3 % | **0,266** | 0,108–0,421 | 0,185 (295) |
| Sonnet 5, pass 1 | 320 | 13 | 307 | 89,9 % | **0,321** | 0,137–0,493 | 0,329 (290) |
| Sonnet 5, pass 2 | 320 | 12 | 308 | 89,3 % | 0,280 | 0,104–0,453 | 0,284 (290) |

**Til sammenlikning:** koder 2 — en CC-instans (Opus 5, agentisk, seks regelkilder), **ikke et
menneske** — fikk κ = 0,812. Den lokale gemma2-dommeren fikk 0,289 mot en blind leser. Kandidatene
ligger i samme klasse som den lokale dommeren, ikke i koder 2s. Ingen menneskelig annotør finnes
(ADDENDUM-11 §3.1).

**Gjenfinningen er problemet, ikke presisjonen.** Haiku finner 11 av koder 1s 39 treff, Sonnet 9 av 34
— begge mister rundt tre fjerdedeler. Haiku flagger 15 koder 1 ikke har, Sonnet bare 6.

**Kandidatene er enigere med hverandre enn med koder 1.** Haiku mot Sonnet pass 1: rå enighet 94,4 %,
**κ = 0,512 [0,288–0,699]** over 302 felles. Det er ikke støy som overlapper tilfeldig; det er to
lesninger som deler noe koder 1 ikke deler. Hvilken av dem som er nærmere reglene, avgjør ikke dette
addendumet.

### Avviket fra §5, og hva det kostet

**§5 låste temperatur 0. Sonnet 5 kjørte alle 320 kall uten den** — API-et svarte HTTP 400 med at
`temperature` er deprecated for modellen, og `kall()` gjentok uten parameteren. Avviket er ført per
kall i `signatur.temperature_utelatt`: **Haiku 0 av 320, Sonnet 320 av 320** i begge pass. Ingen
kjøring er stille.

**Prisen er målt, ikke antatt.** Pass 2 er identisk pass 1 på alt annet enn tidspunktet:

* **300 av 302 verdikter identiske = 99,3 %**, κ mellom passene 0,920 [0,774–1,000]. **To verdikter
  snudde**, begge fra treff til ikke-treff.
* De to flyttet κ mot koder 1 fra **0,321 til 0,280** — et sprang på 0,041 fra to passasjer av 302.

Determinismen er altså nesten intakt, men **κ er så følsomt ved denne grunnraten at to snudde
verdikter beveger tallet med 0,04.** Det er den egentlige lærdommen av avviket: ikke at Sonnet vakler,
men at et κ oppgitt uten gjentak ikke kan skilles fra støy på tredje desimal. Hovedtallet 0,321 endrer
ikke utfallet — begge pass er dypt under 0,70 — men det skal oppgis med pass 2 ved siden av, ikke alene.

**Tokens, fra `usage`:** Haiku inn 235 326 / ut 23 295. Sonnet inn 300 672 / ut 27 784 per pass. Ingen
hurtigbuffer var i bruk i ADDENDUM-18.

### Hva som følger

ADDENDUM-18s hypotese — at en sterkere modell ville nå koder 2s nivå — **faller.** Men §2s daterte
rettelse står: kandidatene fikk **to** regelkilder, koder 2 fikk **seks**, så dette addendumet kan
ikke skille «svakere leser» fra «tynnere regler». **ADDENDUM-20** (sha256
`8118dd541e725d99701378d176f0ad6e9ee5f2343a6bb26dbf24aec8f60e489f`) bytter regelfilen til koder 2s
gjenvunnede fil og holder alt annet fast. **ADDENDUM-19** (Opus) står låst og ukjørt.

## 8 Tilføyelse 2026-09-27: side om side mot full regelfil

§7 ble skrevet før ADDENDUM-20 hadde landet. Utfallet der endrer ikke et tall i §7, men det lukker den
forklaringen §7 lot stå åpen, og hører derfor her:

| Haiku 4.5, samme 269 passasjer | regelkilder | κ mot koder 1 | 95 % KI | flagget treff |
|---|---|---|---|---|
| ADDENDUM-18, tynt utdrag `00d69c09` | 2 | 0,270 | 0,091–0,444 | 22 |
| ADDENDUM-20, koder 2s fil `234695dd` | 6 | **0,047** | −0,021–0,168 | **2** |

Differanse **−0,222**, paret bootstrap **[−0,402 – −0,044]**, utelukker 0. **Full regelkontekst gjorde
kandidaten dårligere.** §7s setning om at dette addendumet «ikke kan skille svakere leser fra tynnere
regler» står — men skillet er nå gjort andre steder, og svaret er at reglene ikke var forklaringen.

**Sonnet 5 med full regelfil er ikke målt.** ADDENDUM-20-kjøringen ble avbrutt etter 275 av 320
Haiku-dommer fordi API-kreditten tok slutt; Sonnet startet aldri. Den halvdelen av sammenlikningen står
altså åpen, og ADDENDUM-20 §7 fører hva den vil koste.

## 9 Datert rettelse 2026-09-27: Sonnets κ er 0,297, ikke 0,321

§7 oppgav κ = 0,321 [0,137–0,493] for Sonnet 5 pass 1, målt på n = 307 fordi 13 svar var uparsebare.
**Tolv av de 13 var avkuttet på `max_tokens` = 300** — `output_tokens` var nøyaktig 300, og 10 av dem var
helt tomme. Det ble oppdaget da ADDENDUM-19 falt på samme feil (ADDENDUM-19 §3b).

De 12 er kjørt om med taket 2 000 og **samme tynne regelfil** (`00d69c09ed8b9045`):

| | κ | 95 % KI | n | flagget |
|---|---|---|---|---|
| §7, uten de avkuttede | 0,321 | 0,137–0,493 | 307 | 15 |
| **rettet, med de avkuttede** | **0,297** | **0,125–0,456** | **319** | 18 |

**Tallet som skal siteres er 0,297 med n = 319.** Slutningen i §7 endres ikke — Sonnet er dypt under
terskelen 0,70, og rangeringen mot Haiku står. Haikus κ = 0,266 er uendret: den ene avkuttede passasjen
der ble uparsebar igjen, nå med `output_tokens` = 2 000, altså ikke et takproblem.

§8s parede sammenlikning mot full regelfil er regnet på Haiku og berøres ikke.
