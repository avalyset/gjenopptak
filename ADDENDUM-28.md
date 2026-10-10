# ADDENDUM-28 — tredje koder fra en annen modellfamilie: lokal gemma2 (preregistrert, ikke kjørt)

**Skrevet:** 2026-10-10, **før kanarien er kjørt og før koden har åpnet blindfilen.** **Status: LÅST ved commit.**
**Gjelder:** κ = 0,812 mellom koder 1 og koder 2 (ADDENDUM-11), forbeholdet «samme modellfamilie» (ADDENDUM-11 § 3
pkt. 1) og ekstern fagfellevurdering 03.10.2026, hovedinnvending 1. **Ingen Anthropic-API.** Alt kjøres lokalt, og alle
datafiler leses fra og skrives til Vault.

## 1 Hensikt

Koder 1 og koder 2 er begge Opus-instanser (`docs/METODE.md`, «Koder 4»). Enigheten mellom dem, κ = 0,812, kan
derfor delvis skyldes at de deler modellfamilie og ikke at regelsettet styrer lesningen. Dette addendumet legger til
en **tredje koder som ikke deler leverandør, treningsløp eller vekter med de to**: `gemma2:9b` (Google), kjørt lokalt
i ollama, på de samme 320 passasjene med den samme regelfilen. Målet er å se hvor mye av enigheten som står igjen når
en koder utenfor familien leser det samme.

**Dette er ikke menneskelig validering, og det erstatter ikke ADDENDUM-27.** ADDENDUM-27 står uendret og ukjørt.
Språkregelen i ADDENDUM-27 § 1 («reference-positive», «second-model agreement», «confirmation rate») gjelder uansett
hva dette addendumet gir. Tre språkmodeller som er enige, er fortsatt språkmodell mot språkmodell.

Koder 4 (Fable 5.1) er i `docs/METODE.md` omtalt som en annen modellfamilie, men kommer fra samme leverandør som
koder 1 og 2. κ = 0,899 mot koder 2 og 0,781 mot koder 1 svarer derfor ikke på om enigheten holder utenfor leverandøren.

At treningsdataene ikke overlapper, kan ikke verifiseres: alle tre er trent på åpen nettekst. «Annen familie» betyr
her annen leverandør, annen arkitektur og andre vekter — ikke bevist uavhengig treningsmateriale.

**Det finnes ett tall av samme slag fra før.** `qwen2.5:7b` (Alibaba), regelfil og parti på 20 i samme kontekst, ga
κ = 0,248 [0,113–0,376] mot koder 1 og 0,239 [0,104–0,368] mot koder 2 (RESULTAT-ADDENDUM-24). Det ble målt som port
for en lokal leser med terskel 0,70, ikke som familiekontroll, med passasjebootstrap og uten verksklynging. Dette
addendumet gjør sammenstillingen mot κ mellom koder 1 og koder 2 for en andre modell utenfor familien.

## 2 Forbehold som følger tallet overalt

Disse står ved siden av tallet hver gang det siteres — i utfallet, i METODE, i FAKTA og i manuskriptet.

1. **Modell eller modus er ikke avklart.** ADDENDUM-19b målte Opus 5 i ett kall per passasje til κ = 0,636 mot
   koder 1, mot 0,812 for koder 2 i én sammenhengende økt, og konkluderte at øktformens bidrag er «mulig og umålt»
   (ADDENDUM-19 § 7.2). Reanalysen 03.10.2026 viste at differansen utelukker 0 (paret, verksklynget [0,057–0,318]),
   så forskjellen er reell; hva som bærer den — øktformen eller den ene økten — er ikke skilt. ADDENDUM-21 arm A, som
   kunne skilt dem, er ukjørt. gemma2 leser her i en tredje form: 64 uavhengige kall à 5 passasjer, uten kontekst
   mellom kallene. **Et lavt κ kan derfor være modusen, ikke modellen og ikke familien.**
2. **Familie og kapasitet er sammenblandet.** gemma2 er 9,2 B parametre i Q4_0; koder 1 og 2 er Opus. Samme regelfil
   og samme kallstruktur ga Haiku 0,031, Sonnet 0,294 og Opus 0,636 mot koder 1 (ADDENDUM-19 § 7.1) — innenfor én
   familie. Et lavt κ skiller ikke «annen familie» fra «for svak modell».
3. **gemma2 er ikke uavhengig av utvalget.** Samme vekt (`ff1d1fc7…`) var portens dommer. De 320 er trukket på
   dommerens egne dommer: 150 den flagget som treff, 150 den ikke flagget (50 `INGEN`, 50 `N1`/`N2`, 50 `N3`) og 20
   ankre. Dommeren så én tekstbit per kall uten regelfilen; her får samme vekt regelfilen og et parti. Uavhengigheten
   gjelder mot koder 1 og 2, ikke mot utvalget. § 5.2 måler derfor de tre κ-ene også innenfor de 150 flaggede.
4. **Referansen er ikke sannheten.** Verken koder 1 eller koder 2 er fasit. Ingen menneskelig annotatør har lest
   materialet.
5. **Regelfil og instruks er på norsk, passasjene på engelsk,** og regelfilen bærer defektene fra gjenvinningen
   (`grep -n`-prefiks, avkuttet tabell). Det er samme fil koder 2, koder 4 og qwen fikk; den rettes ikke.

## 3 Arkitektur, låst

| | verdi |
|---|---|
| blindfil | `presisjonssett/port-presisjonssett-blind.jsonl` på Vault, 320 rader (`id`, `tekst`), 227 287 B, sha256 **`15ce72a7687cea57ac1e7f774aa0303f0bedfc3c2867244d24173a1ec211d4a5`** — filen koder 2, koder 4 og qwen leste |
| regelfil | `koder2/koderegler-gjenvunnet.md` på Vault, 9 805 B, sha256 **`234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449`**, defektene intakte |
| instruks | `prompts/leser-lokal-v1.txt`, 1 698 B, sha256 `6dc74bbc…` (§ 10) — uendret fra ADDENDUM-24: koder 2s metodeavsnitt på norsk, ingen treffrate, ingen eksempler |
| modell | **`gemma2:9b`** i ollama 0.35.1: arkitektur gemma2, 9,2 B parametre, Q4_0, trent kontekst 8 192 |
| vekt | blob sha256 **`ff1d1fc78170d787ee1201778e2dd65ea211654ca5fb7d69b5a2e7b123a50373`**, 5 443 143 296 B, verifisert på innhold 10.10.2026 og igjen før og etter kjøring |
| modus | **regelfil og et parti passasjer i samme kontekst**, ett kall per parti, ingen kontekst mellom kall, ingen verktøy, ingen filtilgang |
| kontekst per kall | systemmelding = instruks + `# REGLENE` + regelfil; brukermelding = partiet med id som overskrift (`kjede/leser.py`, `partimelding`). gemma2s mal har ingen systemrolle; ollama setter systemteksten først i brukerturen |
| partier | **64 à 5**, i blindfilens rekkefølge (PS-001–005, 006–010, …) |
| `num_ctx` | **8 192, satt eksplisitt** i hvert kall — modellens trente kontekst |
| `num_predict` | 2 048; `done_reason` føres per parti |
| temperatur, frø | 0, **734248** |
| `keep_alive` | 0 — modellen lastes ut etter hvert kall, så ingen hurtigbuffer bærer noe mellom partier |
| utdata | JSON-skjema tvunget av ollama (`kjede/leser.py`, `SKJEMA`): `id`, `ekte_treff`, `min_klasse`, `min_bedømbar`, `tvil`, `begrunnelse` — koder 2s felter |
| klasseverdier | H1–H9, `H1/H7-uavklart`, N1–N3, INGEN |
| koder 1 | `presisjonssett/port-presisjonssett-ADDENDUM10.jsonl`, sha256 `6a04079c…` (§ 10), 39 treff |
| koder 2 | `presisjonssett/port-presisjonssett-verdikter-koder2.jsonl`, sha256 `7852f862…` (§ 10), 33 treff |
| kode | `src/gjenopptak/classify/tredje_koder.py` (`kanari`, `kjør`, `mål`) |

**Hvorfor de 320 og ikke ADDENDUM-27s blindfil.** κ = 0,812 er målt på de 320, og bare der har koder 1 og koder 2
dømt hver passasje. ADDENDUM-27s blindfil (149 passasjer, `8483ea42…`) har koder 1- og koder 2-etikett for 85 av dem,
trukket med ulik sannsynlighet per stratum. Den filen åpnes ikke her. De 85 ligger også i de 320, så gemma2 kommer til
å ha dømt dem; å stille de dommene mot menneskelige koder krever et eget addendum.

**Hvorfor parti 5 og ikke 20.** ADDENDUM-24 § 2 valgte bort gemma2 fordi kravet der var kontekst ≥ 32k. Her er
modellen gitt av hensikten, og vinduet er 8 192. Vinduet må romme ledetekst og svar. qwens kanari i ADDENDUM-24
brukte 8 128 tokens inn på regelfil, instruks og 21 passasjer (partiet på 20 er 15 645 tegn) og 1 689 ut. Største
parti à 5 er nr. 21 (PS-101–105, 5 550 tegn). Anslaget — ikke en måling, gemma2 er ikke kalt før låsen — er
5 500–6 600 tokens inn og under 1 000 ut for det partiet. Kanarien i § 4 måler det før kjøring. Følgen står i § 2
pkt. 1: partiene er mindre enn hos qwen, og langt mindre enn koder 2s ene økt.

### 3.1 Sperreliste

Modellen har ingen filtilgang; den ser systemmeldingen og partiet. Sperrelisten binder derfor **koden og den som
kjører den**, og den er bygget inn i rekkefølgen:

* `kanari` og `kjør` åpner bare blindfilen, regelfilen, instruksen og vekten. Testen
  `test_kjoer_aapner_ingen_koderfil_og_signerer_hver_dom` kjører dem uten at koderfilene finnes.
* `mål` åpner koder 1 og koder 2 først når `kjør` har skrevet `dommer.jsonl` og ført filens sha256 i `SEGL.json`, og
  nekter om seglet ikke stemmer.
* Mellom første parti og seglet åpner ingen — verken kode eller operatør — filene i `SPERRET` i `tredje_koder.py`.
  Listen er datafilene i koder 2s sperreliste (`oppdrag-gjenvunnet/oppdrag-koder2-ADDENDUM-11.md`, sha256
  `61fdfe6a…`, § 10) slik de ligger på Vault, pluss alt som er kodet på de samme 320 siden: koder 2, koder 4,
  qwen-kjøringen, ADDENDUM-18–20, ADDENDUM-27s nøkkel og reanalysen.
* Ingen partifil leses for å vurdere dommene før seglet. Framdriftslinjen per parti viser antall gyldige, tokens og
  `done_reason`, ikke dommer.

### 3.2 Signatur per dom

`dommer.jsonl` har én rad per passasje i blindfilens rekkefølge. Hver rad bærer sin egen signatur: modell, vekt-sha256,
instruksens, regelfilens og blindfilens sha256, kodens sha256, ollama-versjon, `num_ctx`, `num_predict`, temperatur,
frø, `keep_alive`, partinummer og partiets id-er, sha256 av systemmeldingen, brukermeldingen og råsvaret,
`prompt_eval_count`, `eval_count` og `done_reason`. I tillegg: passasjetekstens sha256 og tidspunkt. Råsvaret selv
ligger i partifilen.

## 4 Kanari, før kjøring

Største parti (flest tegn) sendes med én ekstra tekstbit **sist**, id `KANARI`, tekst «We could not date the layer,
because no suitable sample was preserved.» (kjedens kanarisetning). **Bestått** krever alle fem:

1. kanarisetningen er de siste tegnene i brukermeldingen;
2. `prompt_eval_count` + `eval_count` < `num_ctx` — vinduet rommet ledetekst **og** svar;
3. `done_reason` = `stop`;
4. svaret parser;
5. `KANARI` har en gyldig dom.

Kanariens klasse kreves ikke; det ville målt koderens kvalitet. Krav 2 er det som beviser at hele ledeteksten sto i
vinduet. En kanari sist beviser bare at slutten kom med; kuttes starten, er det reglene som faller ut, og det ser
kanarien ikke.

Faller kanarien: **STOPP**, ingen kjøring, rapporter. En annen partistørrelse krever nytt addendum. Kanariens dommer
over de ekte passasjene brukes ikke i målingen, og leses ikke.

## 5 Utfall, låst før kjøring

**Delmengden D** = passasjene der gemma2 har en gyldig dom. Et parti er ugyldig i sin helhet når krav 2–4 i § 4 ikke
holder for det, eller tokentallene mangler i svaret (da kan dommene være avsagt uten regelfilen); ellers er en passasje
ugyldig når svaret mangler en gyldig dom for id-en. Ingenting fylles ut, og ingenting kjøres om.

### 5.1 De tre utfallene

Cohens κ på treffbeslutningen (`ekte_treff`), **alle tre på samme D**:

1. **κ gemma2 mot koder 1**
2. **κ gemma2 mot koder 2**
3. **κ koder 1 mot koder 2**

Intervaller: **verksklynget bootstrap** — klyngeenhet verket (`doc_id`; 92 verk i de 320, største 33 rader), 10 000
replikater, frø 734248, persentil — med `boot_kappa` fra `classify/reanalyse_fagfelle.py`, samme funksjon som ga
0,812 [0,711–0,909] i reanalysen 03.10.2026. Rå enighet, PABAK og Gwets AC1 oppgis alltid sammen med κ.

**Ingen terskel for «suksess».** Ingen verdi er bestått eller falt. Tallet er funnet, og alle tre rapporteres uansett
retning.

### 5.2 Rapporteres i tillegg, uten terskel

* Differansene κ(koder 1, koder 2) − κ(gemma2, koder 1) og κ(koder 1, koder 2) − κ(gemma2, koder 2) på D, paret
  verksklynget bootstrap (samme verk i begge ledd), med andel replikater ≤ 0.
* **De tre κ-ene innenfor de 150 dommeren flagget**, og innenfor de 150 den ikke flagget (§ 2 pkt. 3), og antall treff
  per utvalgstype for hver koder.
* Kontroll: κ koder 1 mot koder 2 over alle 320 skal gi 0,8124. Gjør den ikke det, er en innfil eller koden feil, og
  utfallet rapporteres ikke før avviket er forklart.
* Hvis D er mindre enn 320: gemma2-κ-ene over alle 320 med de ugyldige satt til treff, og satt til ikke-treff. Begge
  veier, slik at ingen koder favoriseres.
* Trekodermønsteret (åtte celler), gemma2s klassefordeling, antall ugyldige med grunn, antall inkonsistente (treff med
  N/INGEN-klasse eller omvendt — føres, rettes ikke), passasjebootstrap ved siden av det verksklyngede, veggtid og
  tokens inn og ut.

## 6 Hva tallet kan bære, låst nå

Ikke terskler, men retninger. Lesningen er skjev, og det er fastsatt før tallet finnes:

* **Høy enighet mellom gemma2 og begge koderne** er informativ: en koder utenfor familien, med mindre kapasitet og i
  mindre partier, kom likevel til samme beslutninger. Da trengs ikke felles familie for å forklare 0,812. Slutningen
  bæres av κ innenfor de 150 flaggede (§ 5.2), ikke av κ over D alene: over D deler gemma2 og utvalget opphav
  (§ 2 pkt. 3).
* **Lav enighet** er ikke informativ om familien. Etter § 2 kan den skyldes modus, kapasitet eller familie, og designet
  skiller dem ikke. Lav enighet rapporteres som det den er, og brukes ikke som belegg for at 0,812 er en
  familieeffekt.
* **Uansett utfall** sier tallet ingenting om hvorvidt koderne treffer det et menneske ville kalt en erklæring om
  ugjort arbeid. Det er ADDENDUM-27.

## 7 Hva målingen ikke er

Ikke menneskelig validering. Ikke en port: gemma2 blir verken godkjent leser eller sil-klasse av dette, og
`kjede.toml` røres ikke. Ikke en måling av forekomst. Ikke en gjentakelse av ADDENDUM-11 (det er ADDENDUM-21, ukjørt).
Ikke et svar på om modus eller modell forklarer gapet i ADDENDUM-19.

## 8 Dødsbetingelser

* **Ingen ny instruks, modell, partistørrelse, `num_ctx` eller `num_predict` etter at kanarien er kjørt.** Et nytt
  forsøk krever nytt addendum med ny sha.
* **Ingen omkjøring av enkeltpartier.** Et avbrudd gjenopptas fra første manglende parti; ferdige partier røres ikke.
* **Vekten verifiseres før og etter.** Avvik etter kjøring gjør målingen ugyldig.
* **Ingen annen modell er lastet i ollama under kjøringen**, og ingen annen tung jobb går samtidig; koden stopper om
  `/api/ps` viser en annen modell.
* **`mål` kjøres én gang på forseglet fil.** Koden endres ikke mellom seglet og målingen; en feil i `mål` føres som
  datert teknisk rettelse med begge tall, som i ADDENDUM-19 § 3b.
* **Utdata til Vault** (`tredje-koder-ADDENDUM-28/`: `kanari.json`, `parti-NN.json`, `dommer.jsonl`, `SEGL.json`,
  `maaling.json`), med sha256 i `MANIFEST-VAULT.md`.

## 9 Status

**Preregistrert, ikke kjørt.** Ingen kanari er kjørt, og gemma2 er ikke kalt. Koden er prøvd bare på syntetisk
materiale med falsk modell (`tests/test_tredje_koder.py`). Kjøringen er et eget oppdrag.

**Hva som er lest før låsen, ført fordi det er lest.** Under rekognoseringen 10.10.2026 ble blindfilen åpnet for
struktur: antall rader, tegn per passasje og partigrensene i § 3. Koderfilene, nøklene og ADDENDUM-27s blindfil og
nøkkel ble åpnet for feltnavn, radtall, strata og sha256, og én rad fra to av dem ble skrevet ut for å se feltene.
`reanalyse.json` og qwen-målingen ble lest for tallene som står sitert her. Ingen enighet med gemma2 er regnet, for
gemma2s dommer finnes ikke.

## 10 Filer låst med dette addendumet

Regnet på filene slik de står i commit `46bbe6b`, commiten før låsen. Låsecommiten bærer bare denne filen.
Vault-filene er urørt siden radene deres i `MANIFEST-VAULT.md`.

| fil | hvor | sha256 |
|---|---|---|
| `src/gjenopptak/classify/tredje_koder.py` | repo | `2098bec2f6ebb38185abbe13286d201a3ae015f7b13e40443520c1b6e46078d1` |
| `tests/test_tredje_koder.py` | repo | `887502b77865f27a6318ea3c9613963edbeffbead8ff27eaeca27a036787c73a` |
| `src/gjenopptak/kjede/leser.py` (`LokalLeser`, `SKJEMA`, `partimelding`, `valider`) | repo | `f9535f404d4359a502fe9ea1b644f57777883959491f4a5800f3e57a474ea185` |
| `src/gjenopptak/classify/reanalyse_fagfelle.py` (`enighet`, `boot_kappa`, `_pct`) | repo | `c75a9feaba6acd79866952af48cc7d50e0d684b5480e7ec2586986553317f09b` |
| `prompts/leser-lokal-v1.txt` | repo | `6dc74bbca307a24186b49b257210df58e06c19e9e9b6e70d8c437111d02a6137` |
| blindfil `presisjonssett/port-presisjonssett-blind.jsonl` | Vault | `15ce72a7687cea57ac1e7f774aa0303f0bedfc3c2867244d24173a1ec211d4a5` |
| regelfil `koder2/koderegler-gjenvunnet.md` | Vault | `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449` |
| koder 1 `presisjonssett/port-presisjonssett-ADDENDUM10.jsonl` | Vault | `6a04079c31fbbc60a8a189232a7ef37f55756ce18c74545d10bf062fcea70c36` |
| koder 2 `presisjonssett/port-presisjonssett-verdikter-koder2.jsonl` | Vault | `7852f8623134709987a499edf142e3a87ce9c300fea861369a7917cce9d1bd0f` |
| vekt `gemma2:9b` (ollama-blob, `/Volumes/Vault/ollama/blobs/`) | Vault | `ff1d1fc78170d787ee1201778e2dd65ea211654ca5fb7d69b5a2e7b123a50373` |
| sperrelistens kilde `oppdrag-gjenvunnet/oppdrag-koder2-ADDENDUM-11.md` (leses ikke av koden) | Vault | `61fdfe6a2b99842489acca3638960f9a76d3f25bdfba85e579d10b3d27c168b0` |

`tredje_koder.py` verifiserer vekt, regelfil, blindfil og instruks på sha256 før kanarien og før kjøringen, og koder 1
og koder 2 før målingen, og stopper ved avvik.
