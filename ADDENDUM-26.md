# ADDENDUM-26 — fase 4: håndskriftstudier, prospektiv port på et nytt felt

**Skrevet:** 2026-10-02, **før trekking og før kjøring.** **Status: LÅST ved commit, før noe verk er trukket.**
**Gjelder:** ledd 3-statusen «vist prospektivt på ett felt, 100 verk» (RESULTAT-ADDENDUM-25 § 1), og løftbar
andel per felt. **Mal:** ADDENDUM-25. **Ingen Anthropic-API.** Modellene er lokal ollama og Claude Code-instanser
på abonnementet.

## 1 Hvorfor

Ledd 3 er vist prospektivt på arkeologi, feltet med høyest treffrate av de fire. Fase 4 prøver samme kjede, samme
regelfil og samme porter på et humanistisk felt der hindringene oftere ventes å være tilgang til kilder —
håndskrifter som ikke er digitalisert, katalogisert eller utlånt. **Hypotesen er at løftbar andel (H1–H6) er
høyere her** enn i arkeologi og i første runde. Den rapporteres uten terskel (§ 6). Første rundes tekstvitenskap
peker motsatt vei — 3 av 35 avklarte treff løftbare — og det står her før data, ikke etter.

## 2 Feltet og materialet, låst

**Feltet er «håndskriftstudier, tittelfiltrert underfelt av tekstvitenskap-rammen (799 av 807 overlapper)».**

* **Ingen OpenAlex-topic avgrenser feltet.** Ti feltnære søk (`title_and_abstract.search` på palaeography,
  paleography, codicology, medieval manuscript, manuscript studies, textual criticism, scholarly edition, early
  modern manuscript, scribe, illuminated manuscript; 2015–2020; `group_by=primary_topic.id`) samler seg i
  **T10595** «Medieval Literature and History» og **T14210** «Historical and Linguistic Studies» — begge godkjent
  5/5 i ADDENDUM-01 § 4, begge i tekstvitenskap-rammen. Ingen annen kandidat består godkjenningsregelen som eget
  felt (rådata `fase4/raw/`, `f4-*`).
* **Rammen er derfor topics pluss et ordfilter på tittelen**, og godkjenningsregelen fra ADDENDUM-01 § 4 er anvendt
  på rammen selv. Filteret (`harvest/coverage.py`, `PROSPEKTIVE_FELT["haandskrift"]`):
  `topics.id:T10595|T14210,title.search:(manuscript OR manuscripts OR palaeography OR paleography OR
  palaeographical OR paleographic OR codicology OR codicological OR scribe OR scribes OR scriptorium OR codex OR
  codices),publication_year:2015-2020,open_access.is_oa:true`.
* **De fem mest siterte i vinduet, med filteret: 5/5 i feltet** — «The Monastic Origins of the Nag Hammadi Codices»
  (2018), «Chaucer's Scribes» (2018), «The Latin New Testament: A Guide to its Early History, Texts, and
  Manuscripts» (2018), «Christians and the Codex: Generic Materiality and Early Gospel Traditions» (2019),
  «Facsimiles of Biblical Manuscripts in the British Museum» (2018).
* **Forkastet:** tittel og sammendrag med samme ord (2 670 verk) — 4/5, «Literature as Recreation in the Later
  Middle Ages» er litteraturhistorie; frasefilter på tittel og sammendrag (1 167 verk) — 4/5, «Genres of Rewriting
  in Second Temple Judaism».
* **Navnet beskriver sentrum, filteret definerer feltet.** OpenAlex kan ikke filtrere på periode. T14210 tar med
  senantikke og bibelske håndskrifter; «middelalder og tidlig moderne tid» er der tyngden ligger, ikke en grense.

| | verdi |
|---|---|
| ramme | `frames/frame-haandskrift-RAW.jsonl` på Vault, **807 rader**, sha256 **`6e444a0837d6559906096b15ff6371ee6b630391d387702cc4171410225eaf75`** (`felt/haandskrift.yaml`), frosset 02.10.2026 med 6 kall. Første forsøk fikk 429 på side 1 (OpenAlex tillater ett kall i sekundet for filtre med mer enn fem boolske operatorer) og skrev en tom liste merket UFULLSTENDIG (sha256 `e3b0c442…`, ført i manifestene); frysingen er strupet siden |
| sammensetning | type: article 469, book-chapter 124, dissertation 63, book 38, book-review 32, other 22, dataset 19, conference-paper 16, paratext 10, øvrige 14; PDF-lenke 405; lisens uoppgitt 289, cc-by 138, cc-by-nc-nd 133, other-oa 114, cc-by-nc 60, cc-by-sa 38 |
| overlapp | **799 av 807** i tekstvitenskap-rammen, 0 i arkeologi-rammen; **ett verk blant de første 100: `W2619979143`** (tekstvitenskap, 10.18778/2084-140x.06.07) — **ekskludert før trekkingen** som brukt; 0 blant fase 3s 100 |
| rekkefølge | `random.Random(734248).shuffle` av den leksikografisk sorterte rammelisten (`draw.draw_order`, frø **734248**); rekkefølgens sha256 i trekkspesifikasjonen |
| ekskludert | **de 200 verkene som alt er brukt** (første rundes 100, `data/utvalg/utvalg-*.jsonl`, og fase 3s 100, `fase3/utvalg-fase3-arkeologi.jsonl`) som `brukt`; kontrollene og de leste (`logs/leste-kontrollkandidater.json`) som i ADDENDUM-09 |
| vilkår | uendret fra ADDENDUM-09 og fase 3 (`draw.decide`): typefilteret (bøker og avhandlinger kan trekkes, som i fase 3), feltets emne blant verkets tre høyeste topics (T10595, T14210), hentingsporten P1/P3, identitetsporten på P3, engelsk (ADDENDUM-07 § 8) |
| antall | **100**, sekvensielt; trekkingen stopper ved 100. **Rekker rammen ikke, stopper trekkingen ved rammens slutt, og N føres som det ble.** Ingen substitusjon, ingen utvidelse av rammen |
| OpenAlex | `x-ratelimit-remaining` **før og etter** trekkingen (fase 3 førte bare etter) |
| kode | `src/gjenopptak/harvest/draw_fase4.py` (sha256 i § 10) |
| utdata | Vault `fase4/`: trekkspesifikasjon, trekklogg, `utvalg-fase4-haandskrift.jsonl`, `verk-fase4.txt`, `fase4/utvalg/` |

## 3 Referansesettet — bygget FØR silen og leseren

Som ADDENDUM-25 § 3, med fase 4s stier (`classify/fase4.py`):

1. **20 av de trukne** (alle, om færre enn 20), `random.Random(734248).sample(sorted(work_id), 20)`.
2. Hvert verk skrives ut som nummererte setninger med kjedens egen parser.
3. **Én `claude -p`-instans per verk, `claude-opus-5`**, tom kontekst, serielt, egen kladdekatalog, arbeidskatalog på
   Vault utenfor repoet, `--strict-mcp-config`. Nøyaktig to filer: regelfilen `koder2/koderegler-gjenvunnet.md`
   (sha256 **`234695dd…`**) og verket. Oppdraget er fase 3s `OPPDRAG` med fase 4s stier og **én tilføyelse: svaret
   avslutter med `LEST TIL: S<n>`**.
4. **Et verk er lest** bare når den linjen nevner verkets siste setning og økten ikke endte med feil. **Avvik fra
   ADDENDUM-25 § 8:** et avbrutt forsøk flyttes til `fase4/referanse/avbrutt/` og telles ikke; verket leses **i sin
   helhet** av en ny instans. Grunnen: instansen fører treff, ikke framdrift, så et avbrutt forsøk har ingen kjent
   setning å fortsette fra.
5. **Nøkkelen sikres før neste steg:** `fase4/referanse/NOKKEL-referansesett.jsonl`, sha256 i `MANIFEST-VAULT.md`,
   OpenTimestamps-stempel. **Referanseporten (ADR-0014) håndhever det i kode:** kjeden nekter `dommer`–`register`
   før raden står i manifestet. Nøkkelen redigeres aldri etterpå.

## 4 Kjeden, uendret i form — kjørt fra låsecommiten fra første ledd

`gjenopptak run --verk fase4/verk-fase4.txt --utvalg fase4/utvalg-fase4-haandskrift.jsonl --navn fase4-kjede --leser
cli`, **startet gjennom gjenopptaksrutinen** (`python -m gjenopptak.kjede.gjenoppta --fase fase4`) fra worktreet på
låsecommiten, `fase4/worktree-<lås>` på Vault, med `data/` som ekte katalog i worktreet. Slik gjelder
etterkontrollen per ledd fra første kall, og et avbrudd gjenopptas med den samme koden.

`kjede.toml` som i låsecommiten: dommer `gemma2:9b` (ledetekst `de9f8229…`), ekstraksjon (`c8c276df…`), unionen med
alle-treff-kobling, G3-merking (`63ed7345…`), blindfiler stokket med frø 734248, leseren `claude-opus-5`, serielt,
≤ 356 tekstbiter per økt, egen kladdekatalog per økt.

**Endret i kjeden siden ADDENDUM-25**, alt før denne låsen og hver i egen commit: ekstraksjonen fortsetter et
påbegynt ledd og føres ferdig bare med alle vinduer; en halvskrevet siste linje kuttes før dommer og ekstraksjon
føyer til; `les` føres ikke ferdig med delvise økter (`07dc97f`); `modelUsage` fra svaret føres per leserøkt
(`f70e794`); gjenopptaksrutinen gjelder hver fase og etterkontrollerer ekstraksjonens dekning (`cceb19a`).

Prosessene kjører frikoblet (`setsid`, `nohup`, `caffeinate`), ollama likeså. En delvis leserøkt fullføres med
`--fullfor-okt N` i **én ny instans**; ingen leserøkt kjøres om. **Ingen commit-melding nevner referansesettets
innhold eller tall før målingen i § 5 er gjort.**

## 5 Portene, låst nå

**(1) Blind presisjon.** **100 tilfeldige** av leserens treff (alle, om færre), `random.Random(734248).sample` over
treffene sortert på id, til **en separat `claude -p`-instans** med regelfilen og sperreliste — fase 3s
`PRESISJON_OPPDRAG` med fase 4s stier og id-er `P4-001` …. Presisjon = andel med **`treff: true`** (feltet
fase 3 målte på, RESULTAT-ADDENDUM-25 § 1.1), Wilson 95 %. **≥ 0,70 → «arbeidsliste (prospektiv port)». Under →
«kandidatliste».** Navnet endres ikke i ettertid.

**(2) Recall — uten terskel.** Som ADDENDUM-25 § 5: *beholdt* = en tekstbit i unionen fra samme verk dekker alle
setningsnumrene treffet består av; *bekreftet* = minst én slik tekstbit fikk `treff: true` av leseren. Andel beholdt,
andel bekreftet og bekreftet blant beholdte, med Wilson 95 %. Følsomhet: uten referansetreff merket `tvil`, og uten
`gyldig_spenn: false`. **Klyngefølsomhet, låst nå** (fase 3 la den til etter frys-lesning 4): de samme andelene
**uten verket med flest referansetreff — alle verk med det antallet, ved likhet** — og **snittet per verk**.

Recall er målt mot én lesning av samme modellfamilie med samme regelfil, ikke mot et menneske.

## 6 Tilleggsmålet, låst nå — uten terskel

**Løftbar andel H1–H6 blant leserens avklarte treff** (ADDENDUM-05 § 4, `liftability.liftable_share`: uavklarte
utenfor brøken, oppgitt ved siden av), med Wilson 95 %, mot tre referanser:

| referanse | løftbar av avklarte | Wilson 95 % | kilde |
|---|---|---|---|
| arkeologi, fase 3 | **101 / 628 = 16,1 %** | 13,4–19,2 | RESULTAT-ADDENDUM-25 § 1.3 |
| første runde samlet (kandidatlista, 432 rader) | **77 / 406 = 19,0 %** | 15,4–23,1 | RESULTAT-ADDENDUM-25 § 1.3 |
| **tekstvitenskap-delen av første runde** | **3 / 35 = 8,6 %** | 3,0–22,4 | **regnet 02.10.2026** fra register v2 (`kandidat432/8-register.jsonl`, sha256 `c6895202b76199aa…`), feltet `obstacle_class`, `field_key = tekstvitenskap`, `liftable_share`; samme regning gir 77/406 for hele lista |

Rapporteres: fase 4s andel, differansen mot hver referanse, og uavklart andel av alle treff. **Ingen test, ingen
terskel.** Fase 4 og fase 3 er leserens treff; første rundes tall er kandidatlista etter kaskaden, og
tekstvitenskap-referansen hviler på 35 treff.

## 7 Kostnad, målt

OpenAlex før og etter trekkingen og antall kall. Lokal modelltid per ledd fra utdataene. Max-økter: antall
`claude -p`-økter, `usage` og `modelUsage` fra hver (referansesett, leser, presisjonsport). Pris per bekreftet
treff som i ADDENDUM-25 § 6.

## 8 Rapporteres i tillegg

Klassefordeling blant leserens treff; H7-andel; løftbar og uavklart andel hver for seg; **felt-tetthet**: treff per
verk og per 1 000 tekstbiter (både korpusets og de dømte), mot fase 3 og første runde. **Kandidatene i H1–H6 med
`tvil: false`** listes i `docs/SAKBEHANDLING-<dato>-haandskrift.md` med ordrett sitat ±2 setninger, verk-ID og
kilde-URL, i samme form som `docs/SAKBEHANDLING-2026-09-27-kandidater.md` — arbeidslista for neste sakbehandling,
med navnet porten gir den.

## 9 Dødsbetingelser

* **Referansenøkkelen er fasit og røres ikke** etter at raden står i manifestet.
* **Ingen leserøkt kjøres om**; delvise økter fullføres serielt. Aldri parallelle instanser (LAERDOM § 32).
* **Regelfilen rettes ikke. Portene flyttes ikke. Rammen utvides ikke.**
* **OpenAlex-gulvet står** (`draw.REMAINING_FLOOR`).
* **Gjenopptak bare fra worktreet på låsecommiten** (`gjenoppta --fase fase4`), aldri fra arbeidstreet.
* **Ingen publisering, ingen push, ingen MASTER-redigering** (MASTER-patch som fil).

## 10 Filer låst med dette addendumet

Regnet på filene slik de står i commit `b54b39c`, commiten før låsen.

| fil | sha256 |
|---|---|
| `src/gjenopptak/harvest/draw_fase4.py` | `6f86a66f57a908323e2a9e2f9791dde9f348d201efbd3eee6cc363528d164313` |
| `src/gjenopptak/harvest/draw.py` | `b36fdcf059df5bd1b126e8457ea9183ed69be8ec0fb4510ffab43b97eb95d0fa` |
| `src/gjenopptak/harvest/coverage.py` | `65f520ae313e6a22f5b91d8306d5a1b7e87fa9e24f0786132657c642018f74eb` |
| `src/gjenopptak/harvest/fetchtest.py` | `3ee4dc996dd78dff86c9642f5b1496837eb19e20808b908042742c3acbdef26c` |
| `src/gjenopptak/classify/fase4.py` | `4a96324e993ef56ffe491e259053209f3877c6f7ca3a972e279001c21caa2985` |
| `src/gjenopptak/classify/fase3.py` | `28cd7717f7a1161c419964e4a2c411df844e4f3e1819ac4d992c18f6d3d65e59` |
| `src/gjenopptak/kjede/ledd.py` | `e99b2b210e0498f9c7674c4ce7c73fb83437b8cbae615c03ed969ae6ebecda74` |
| `src/gjenopptak/kjede/cli.py` | `40ebef04ce7e5347e392fa9852e9bb29b97f8e80964348d839784be88e5a6243` |
| `src/gjenopptak/kjede/leser.py` | `f9535f404d4359a502fe9ea1b644f57777883959491f4a5800f3e57a474ea185` |
| `src/gjenopptak/kjede/referanseport.py` | `e5cccfee22f4f3b0cac2fe856a16aa7b3111cddbad07d0ea8b6befbdaeab8472` |
| `kjede.toml` | `65620200fb2a3ca7bc45273cd12e408cd5b42285d1d1415af0a3a3d15cea77db` |
| regelfil `koder2/koderegler-gjenvunnet.md` | `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449` |
| ramme `frames/frame-haandskrift-RAW.jsonl` | `6e444a0837d6559906096b15ff6371ee6b630391d387702cc4171410225eaf75` |
