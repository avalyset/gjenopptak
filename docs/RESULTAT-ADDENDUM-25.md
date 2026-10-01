# Utfall av ADDENDUM-25 — fase 3

**Status 30.09.2026: målt — port (1) bestått, lista heter «arbeidsliste (prospektiv port)» (§ 1).** *(Sto 28.09.2026:
«kjøringen pågår. Portene i ADDENDUM-25 § 5 er ikke målt.»)* Denne fila tar utfallet;
§ 0 er ført **før** utfallet, fra en disiplinkontroll samme dag, og endres ikke når tallene kommer.

## 0 Ført før utfallet (disiplinkontroll 28.09.2026)

### 0.1 Presisjonsportens oppdrag og sperreliste, med sha256

ADDENDUM-25 § 5 viser til formen i ADDENDUM-23 § 4, men fører ingen sha for fase 3s eget oppdrag. Malen er
`PRESISJON_OPPDRAG` i `classify/fase3.py`, som er låst med sha256 i § 9. Gjengitt med fase 3s stier og lagt på
Vault før leserleddet har kjørt:

| fil på Vault | bytes | sha256 |
|---|---|---|
| `fase3/presisjon/oppdrag-presisjon-MAL.md` (oppdraget; `{N}` fylles med antall trukne treff ved kjøring) | 3 077 | `aebd975593942f892252771e3048bdce5f04a8e0ce57a77036c0e3f1faaed4cd` |
| `fase3/presisjon/sperreliste-presisjon.md` (sperrelisten, ordrett utdrag av malen) | 506 | `cc201ac2451ba86d9165fd104810d885de1c691a35091dddbae6a32b5fa4f133` |

Det ferdige oppdraget skrives til `fase3/presisjon/oppdrag-presisjon.md` ved kjøring; det skal være malen med
`{N}` byttet ut og ellers byte-identisk, og det kontrolleres i utfallet. De 20 referanseoppdragene står med
sha256 i `MANIFEST-VAULT.md`, seksjonen «Fase 3: oppdrag og sperrelister ført med sha».

### 0.2 (d) Modell-ID per verdikt kommer fra konfigurasjonen, ikke fra svaret

**Kontrollert i koden:** alle tre `claude -p`-veiene pinner `--model claude-opus-5`, som ADDENDUM-25 låser —
referanseleserne og presisjonsporten gjennom `fase3.MODELL`, kjedens leser gjennom `[leser] modell` i
`kjede.toml` (`kjede/leser.py:204`).

**Avvik:** signaturen per verdikt i registeret (`ledd.steg_register`, `"leser": {"modell": …}`) tar modell-ID fra
`kjede.toml`, **ikke fra svaret**. `CCLeser.kjør_økt` fører `usage`, men **ikke `modelUsage`**, så modell-ID fra
svaret logges ikke for kjedens leserøkter. **Ikke rettet underveis** (kjøringen går med den låste koden).

**Hva som finnes i stedet:**
* **Referansesettet:** `fase3/referanse/bruk/R01–R20.json` fører `modelUsage` fra svaret. **20 av 20 oppgir bare
  `claude-opus-5`.** Presisjonsporten fører det samme (`bruk-presisjon.json`).
* **Kjedens leserøkter: modell-ID verifiseres fra øktutskriftene etter kjøringen, som for referansesettet**
  (eierens regel 28.09.2026). Claude Code fører `message.model` per melding i
  `~/.claude/projects/<arbeidskatalog>/<økt>.jsonl` — `-Users-eirikbottennicolaysen-dev-gjenopptak` for den
  løpende kjøringen, worktreets katalog om den gjenopptas derfra. Utskriftene sikres på Vault med utfallet, og
  modell-ID per økt regnes derfra og føres her. Lar de seg ikke koble til øktene, står modell-ID for kjedens
  leser som **ikke verifisert fra svaret**.
* **`kjede/leser.py` røres ikke før fase 3 er ferdig.** Rettingen — `modelUsage` fra svaret inn i bruken og
  signaturen — gjøres etterpå, som egen commit, og gjelder bare kjøringer etter den.

### 0.3 Referanseporten var prosa, ikke kode

ADDENDUM-25 § 3.5 krevde at ingen del av kjeden kjøres før nøkkelens rad står i manifestet. Kjeden håndhevet det
ikke. **Rekkefølgen holdt i denne kjøringen**, belagt med tidsstempler: nøkkelen skrevet 10:20:02Z, manifestraden
10:20:05Z (sha256 `6e38c3a7…`, ots-stemplet), kjedeprosessen startet 10:20:33Z, `1-hentet.jsonl` 10:20:34Z.

Porten er lagt inn i koden etterpå (ADR-0014, tillegg 28.09.2026; `kjede/referanseport.py`, testet med seks
tilfeller den skal feile på). **Avvik fra låsen:** koblingen står i `kjede/cli.py`, som § 9 låser til sha256
`c2eb33bc361557371a2ed86d6d3530fcd090865ca9cdc0e9fe8ae6a108731e0b`; ny sha256
`40ebef04ce7e5347e392fa9852e9bb29b97f8e80964348d839784be88e5a6243`. Kjøringen som går, lastet den låste
versjonen ved start og berøres ikke.

**Gjenopptak etter avbrudd skjer fra låsecommiten, aldri fra arbeidstreet** (eierens regel 28.09.2026). Slik
kjører alle ledd med de sha256-ene § 9 låser, også etter at arbeidstreet har fått referanseporten:

* **Worktree:** `git worktree add --detach /Volumes/Vault/gjenopptak-kilder/fase3/worktree-f19a3e3 f19a3e3`,
  med `data/` som symlenke til repoets `data/`, så kjøringens tilstand, spesifikasjon og kladd er de samme.
  Symlenken er usporet og endrer ingen sporet fil.
* **Rutinen:** `python -m gjenopptak.kjede.gjenoppta` (`--sjekk` for bare sjekkene). Før start: Vault montert;
  worktreets HEAD er `f19a3e3` og ingen sporet fil er endret; **hver fil i § 9-tabellen, lest fra
  `f19a3e3:ADDENDUM-25.md`, har låst sha256 i worktreet — `kjede/cli.py` eksplisitt**; `gjenopptak` importeres
  fra worktreet; referanseporten bestås (rutinen kjører den selv, fordi den ikke står i den låste `cli.py`); og
  ingen annen kjøring av `fase3-kjede` går. Ett avvik, og ingenting startes. Hver gjenopptakelse føres i
  `fase3/gjenopptak-logg.jsonl`.
* **Kontrollert 28.09.2026:** `--sjekk` mot worktreet gir 7 av 7 filer med låst sha256, `cli.py`
  `c2eb33bc…`, import fra worktreet, referanseporten bestått, og den løpende kjøringen oppdaget (så en
  gjenopptakelse nå ville blitt nektet). Samme sjekk mot arbeidstreet gir ett avvik: `cli.py` `40ebef04…` ≠
  låst `c2eb33bc…`. Testet i `tests/test_gjenoppta.py`.
* **Den løpende kjøringen:** startet fra arbeidstreet 10:20:33Z, da det var lik `f19a3e3` i alle filer
  kjeden leser. Siden da er bare `cli.py` (alt lastet) og én ny fil endret i `src/`; modulene kjeden laster
  først når et ledd starter (bl.a. `kjede/leser.py`), er byte-like med låsen. **Ingen endring i `src/` som
  kjeden importerer, før fase 3 er ferdig.**

### 0.4 Lisens for de 100 nye verkene

Fra den frosne rammens `best_oa_location.license`: cc-by 40, **ingen oppgitt 30**, cc-by-nc-nd 10, cc-by-nc 10,
cc-by-nc-sa 6, cc-by-sa 2, public-domain 1, other-oa 1 — **26 med NC/ND**. Tabell i `docs/LISENS-PER-VERK.md`;
maskinlesbart i `fase3/lisens-per-verk-fase3.json` (sha256 `c5e4157da2ec0b6356e7419e7e117b276eef54f7049330b41dc55c0fd5aa7218`).
Andelen uten lisens og med NC/ND er høyere enn blant de 60 fra første runde (17 og 13 av 60).

## 1 Utfall

Målt 30.09.2026 med `classify/fase3.py` (låst, sha `28cd7717…`) og `classify/fase3_rapport.py` (bare lesing).
Tall i `fase3/maaling-fase3.json` (sha256 `441cff4f1d949cbc…`) og `fase3/rapport-fase3.json` (`f5770e738bdce2c8…`; tidligere tall uendret, klyngene lagt til 30.09),
begge i `MANIFEST-VAULT.md` under «Fase 3: leserleddet, portene og utfallet».

**Port (1) er bestått. Lista heter «arbeidsliste (prospektiv port)».** Navnet endres ikke i ettertid (§ 5).

### 1.1 Port (1): blind presisjon

**85 av 100 = 85,0 % [76,7–90,7]**, terskel 0,70. De 100 er trukket med `random.Random(734248).sample` fra
leserens **673 treff** sortert på id (blindfil `f795de32…`, nøkkel `d3b58f15…`). Oppdraget er malen fra § 0.1 med
`{N}` = 100 og ellers byte-identisk (kontrollert). Instansen: én `claude -p`, `claude-opus-5` i `modelUsage`,
13,8 min, 100 av 100 dømt i blindfilens rekkefølge, alle gyldige; sluttrapporten bekrefter at bare regelfilen og
blindfilen ble åpnet.

**Feltnavnet:** § 5 skriver «andel instansen kaller `ekte_treff: true`». Oppdraget i ADDENDUM-23-formen som § 5
viser til, og den låste `fase3.py`, bruker feltet `treff` med samme definisjon. Målt på `treff`; ført, ikke rettet.

Følsomhet, ikke port — etter **leserens** tvil-flagg (som ADDENDUM-23 § 7.2): `tvil: false` **37 av 38 = 97,4 %
[86,5–99,5]**, `tvil: true` **48 av 62 = 77,4 % [65,6–86,0]**. Samme klasse som leseren i 76 av 85 bekreftede.
De 15 avviste: `INGEN` 8, `N3` 7.

### 1.2 Port (2): recall, uten terskel

Referansenøkkelen: **104 treff i 20 verk**, 60 uten tvil, 0 med ugyldig spenn.

| | k / n | andel | Wilson 95 % |
|---|---|---|---|
| **beholdt av silen** | 95 / 104 | **91,3 %** | 84,4–95,4 |
| **bekreftet av leseren** | 85 / 104 | **81,7 %** | 73,2–88,0 |
| bekreftet blant beholdte | 85 / 95 | 89,5 % | 81,7–94,2 |

Følsomhet, merket slik (§ 5): uten referansetreff merket `tvil` — beholdt **56 / 60 = 93,3 % [84,1–97,4]**,
bekreftet **56 / 60 = 93,3 %**; uten `gyldig_spenn: false` — identisk med hovedtallene (ingen slike treff).
**Klyngene (lagt til 30.09.2026, frys-lesning 4):** de 104 referansetreffene ligger i **12 av de 20 verkene**, og
**R08 alene har 51** (50 beholdt, 47 bekreftet). Wilson-intervallene over regner treffene som uavhengige og er
derfor for smale. Følsomhet, ikke port: **uten R08** beholdt silen **45 av 53 = 84,9 % [72,9–92,1]** og bekreftet
leseren **38 av 53 = 71,7 % [58,4–82,0]**; **snittet per verk** er 85,9 % og 76,3 % (`rapport-fase3.json`,
`recall_klynger`).

**Dette er det første målte recall-tallet for silen.** «Bekreftet» er enighet mellom to lesninger av samme
modellfamilie og regelfil, ikke mot et menneske (§ 5).

### 1.3 Leserens treff og klasser (§ 7)

**673 av 4 107 dømte = 16,4 % [15,3–17,6]**; 73 av 100 verk har minst ett treff.
**Klasse:** H7 425 · H9 68 · H2 56 · H1/H7-uavklart 45 · H8 34 · H1 20 · H5 12 · H4 9 · H3 3 · H6 1.

Løftbarhet etter ADDENDUM-05 § 4 — løftbar andel av **avklarte** treff, uavklart andel av **alle** treff, oppgitt
sammen (`liftability.format_liftable`: «løftbar 101/628 av avklarte; uavklart 45/673»):

| | fase 3 (673 treff) | kandidatlista, de første 100 (432 treff) |
|---|---|---|
| H7, av alle treff | **63,2 %** [59,4–66,7] (425) | 66,9 % [62,3–71,2] (289) |
| **løftbar H1–H6, av avklarte** | **16,1 %** [13,4–19,2] (101 av 628) | 19,0 % [15,4–23,1] (77 av 406) |
| **uavklart, av alle treff** | **6,7 %** [5,0–8,8] (45 av 673) | 6,0 % (26 av 432) |
| ikke-løftbar H7–H9, av avklarte | 83,9 % [80,8–86,6] (527 av 628) | 81,0 % (329 av 406) |
| tvil blant treff | 53,8 % | 49,5 % |

### 1.4 Felt-tetthet mot de 100 første (§ 7)

§ 7 sier «treff per 1 000 tekstbiter» uten å si om nevneren er korpusets tekstbiter eller de dømte i unionen.
Begge føres; ingen er valgt.

| | treff | verk | treff per verk | per 1 000 korpus-tekstbiter | per 1 000 dømte |
|---|---|---|---|---|---|
| **fase 3, arkeologi** | 673 | 100 | **6,73** | **31,5** (av 21 361) | **163,9** (av 4 107) |
| første 100, arkeologi | 274 | 25 | 10,96 | 40,6 (av 6 741) | 276,8 (av 990) |
| første 100, alle fire felt | 432 | 100 | 4,32 | 19,4 (av 22 243) | 151,9 (av 2 844) |

Silen slapp gjennom 4 107 av 21 361 = 19,2 % [18,7–19,8] av korpuset (de første 100: 12,8 %).

### 1.5 Kostnad, målt (§ 6)

**OpenAlex:** 8 kall; `remaining` 985 etter trekkingen. **Før-verdien ble ikke ført** av den låste trekkingen
(`draw_fase3.py` fører bare etter-verdien) — avvik fra § 6.
**Lokalt:** dommeren 25,8 t modelltid (sum `total_duration`, 21 361 dommer); ekstraksjonen 5,6 t (sum `veggtid`,
1 923 vinduer). Veggklokke per ledd føres ikke: avbruddet 29.09 og gjenopptakene gjør den meningsløs.

| Max-økter | økter | kontekst-tokens inn | output-tokens | minutter |
|---|---|---|---|---|
| referansesett | 20 | 13 767 605 | 219 726 | 64,7 |
| leser, økter som dømte | 14 | 79 538 395 | 1 239 475 | 283,1 |
| presisjonsport | 1 | 2 963 207 | 75 769 | 13,8 |
| leserøkter uten dom (12 blokkert, 14 avvist ved grensen) | 26 | 6 593 971 | 72 674 | 23,1 |

**Pris per bekreftet treff** (§ 6: forbruk / (leserens treff × presisjon) = 673 × 0,85 = 572): referansesett
24 069 kontekst-tokens, leser **139 053**, presisjonsport 5 180. Per leser-treff, som i ADDENDUM-22 § 10: 118 185
kontekst-tokens (de første 100: 164 805). *(Rettet 30.09.2026, frys-lesning 4: sto «164 815», regnet på
den avrundede 71,2 M; eksakt 71 195 665 / 432.)* Leserforbruket er samlet fra alle kjøringene
(`fase3_rapport.leserøkter`), fordi leserleddet overskriver forbrukslisten ved hvert gjenopptak (§ 0.7).

### 1.6 Modell-ID fra svaret (§ 0.2)

Fra Claude Codes øktutskrifter, sikret i `fase3/utskrifter/` (41 leser + 1 presisjon, tabell
`modell-fra-utskrifter.json`, sha256 `ef8fd30bfb73b213…`): **alle 14 leserøkter som dømte — økt 1–12 og
restene 3-rest1 og 7-rest1 — har bare `claude-opus-5`.** De 14 avviste har én `<synthetic>`-melding (grensen);
de 12 blokkerte og sandkasseprøven bare `claude-opus-5`. Presisjonsporten: bare `claude-opus-5` i både
`modelUsage` og utskrift. **Modell-ID for kjedens leser er dermed verifisert fra svaret.**

### 1.7 Registeret

**Skrevet 30.09.2026 av det rettede registerleddet (§ 0.8):** `8-register.jsonl`, 673 rader, sha256
`b7d9230c93970c26…`, innholds-sha `f590f25afcd33ab7…`; hodet `8-register-header.json` (sha256 `f586cc46e1259ab1…`)
med `port: "arbeidsliste (prospektiv port)"`, `bekreftet: true`, `n_dømt: 4107`, `navnepolicy: "verk, ikke person"`
og forbeholdene `leser_datert` (30.09.2026, `claude-opus-5`, regelfil `234695dd4e1777a9`), `silrecall: "ikke målt"`
og `verksnivaa` (verksnivået teller silens flagg, § 0.7). Kopiert til Vault `fase3-kjede/`. Portene bygger ikke
på registerfila.

**`silrecall` står som «ikke målt»**, fordi skjemaet bare tillater den verdien (`registerhode.schema.json`,
`forbehold.silrecall`). Recall er målt for denne kjøringen (§ 1.2), men å føre tallet i hodet krever en
skjemaendring ut over registerleddet, og den er ikke gjort. *(Sto til rettingen: «hodet er ikke skrevet, fordi
det låste registerleddet bryter sitt eget skjema».)*

### 0.5 Avbrudd i ekstraksjonsleddet 29.09.2026, og hvordan det ble gjenopptatt

**Hva skjedde:** dommerleddet ble ferdig 29.09 kl. 17:01 (21 361 av 21 361). Ekstraksjonen startet og hadde
skrevet 1 357 vinduer fra 81 av 100 verk da kjedeprosessen og ollama-tjenesten døde med Claude Code-økten de var
startet fra (siste skriving 21:09).

**Fellen, funnet før gjenopptak:** den låste `steg_ekstraksjon` fortsetter ikke et påbegynt ledd. Finnes
`4-ekstraksjon.jsonl`, hopper leddet over hele kjøringen (`if not gjort`) og merker seg ferdig med delresultatet.
En gjenopptakelse på den tilstanden ville stille latt 19 verk mangle i unionen og ødelagt recall-målingen.

**Gjort, uten kodeendring i kjeden:** delresultatet og tilstandsfila sikret på Vault
(`fase3/avbrudd-2026-09-29/`, sha i manifestet), delresultatet tatt ut av kjøringens katalog, og ekstraksjonen
kjørt **helt på nytt** med den låste koden fra worktreet på `f19a3e3`, via `gjenopptak.kjede.gjenoppta`. Første
forsøk 21:23Z stoppet på kanarien (ollama nede, ingenting skrevet); ollama startet, andre forsøk 21:24Z går.
Ekstraksjonen er deterministisk (temp 0, fast frø), så de 1 357 vinduene i delresultatet sammenlignes med de
nye når leddet er ferdig; utfallet føres her.

**Prosessene kjører nå frikoblet fra Claude Code** (`setsid`, `nohup`, `caffeinate`), slik at et øktkrasj ikke
dreper dem.

**Vakten i gjenopptaksrutinen var blind** for kjøringer den selv startet: den søkte etter «kjede.cli run», men
rutinen setter `--konfig` mellom dem. Rettet i `kjede/gjenoppta.py` (ikke importert av kjeden, ikke i § 9) og
testet; et nytt startforsøk mens kjøringen går, nektes nå (rc 2).

**Determinismesjekk etter gjenopptak (30.09.2026, `fase3/avbrudd-2026-09-29/determinisme.json`, sha256
`3b66fa5e1284b20f70e591abdeb2314adc0dc95e658f5b01c8bab6cd64e02591`):** sha256 av `utdata_raa` per vindu, de 1 357
vinduene i det sikrede delresultatet (81 verk) mot de samme `(work_id, vindu)` i den nye kjøringen (1 923 vinduer i
alt). **Identiske 1 357, ulike 0, mangler i ny kjøring 0**; `tokens_inn` ulik i 0. Samlet sha over de 1 357 i
delresultatet `f6b5a9074278d6f0d851dae54ca56bfb5f92025995f875682604b96fcece30e6`, i den nye kjøringen over de samme
vinduene `f6b5a9074278d6f0d851dae54ca56bfb5f92025995f875682604b96fcece30e6`. Skript: `determinisme.py` i samme katalog.

### 0.6 Leserleddet kjørte uten å lese — og ble ført ferdig (30.09.2026)

**Hva skjedde:** etter ekstraksjon, union (4 107 tekstbiter) og blindfiler (12 økter à 342–343) startet leddet
`les` tolv `claude -p`-økter serielt, 05:0x–05:26. **Alle tolv ble blokkert fra materialet**: i worktreet var
`data` en symlenke til repoets `data/`, utenfor katalogene en `claude -p`-instans får lese og skrive
(arbeidskatalogen og `--add-dir` Vault). Hver instans leste regelfilen, fant at blindfilen og verdiktfilen lå
utenfor, stoppet og sa det i sluttsvaret — ingen forsøkte å omgå sperren. **0 tekstbiter dømt.** Forbruk: 12
økter, 1,4–2,5 min hver.

**Feilen er min, i gjenopptakskonstruksjonen fra 28.09** (§ 0.3): symlenken ble valgt for å dele kjøringens
tilstand mellom repoet og worktreet, uten å prøve om leserinstansene nådde den.

**Og den låste koden førte leddet som ferdig:** `steg_les` registrerte 12 × «AVVIK, dømt 0» og markerte `les`
gjort; kjeden fortsatte med verksnivå og falsifisering og stoppet først i `register` (rc 2). Et ledd som leverer
null av det det skal, meldte ferdig — samme mønster som ekstraksjonens gjenbruk av delresultat (§ 0.5).

**Gjort:** kjøringens katalog er flyttet inn i worktreet på Vault som ekte katalog
(`worktree-f19a3e3/data/kjede/fase3-kjede`, 32 filer, sha for sha identisk med originalen); repoets
`data/kjede/fase3-kjede` er en symlenke dit, og originalen står urørt som `fase3-kjede.foer-flytting-2026-09-30`.
`gjenoppta` har nytt startvilkår — `data` i worktreet må være en ekte katalog innenfor Vault — og kan kjøre
`--from les --om`. Prøve før gjenopptak: en `claude -p`-instans med leserens oppsett leste en fil i `data/` og
skrev i kladdkatalogen. **`les`, verksnivå, falsifisering og register kjøres på nytt** med de samme blindfilene og
den samme nøkkelen; ingen blindfil er endret.

### 0.7 Leserleddet stoppet på øktgrensen i økt 3 — og ble ført ferdig igjen (30.09.2026)

**Hva skjedde:** gjenopptatt fra `les` 06:48. Økt 1 og 2 ble dømt fullt (343 + 343, 26,1 og 28,5 min). Økt 3 stoppet
etter **30 av 343** da Max-økta nådde grensen (07:49; instansens sluttsvar sier det selv), og økt 4–12 ble avvist
straks med samme melding, **0 dømt**. `steg_les` førte igjen `les` som gjort (økt 3–12 «AVVIK»), og kjeden kjørte
videre: verksnivå (07:50), falsifisering («alt gjort») og register, som stoppet med rc 1.

**Register feiler på sitt eget skjema i låsecommiten.** `steg_register` bygger et hode uten `navnepolicy` og uten
forbeholdene `leser_datert` og `silrecall`; skjemaet ble strammet til med alle tre i `6666d4f` (T1–T5, 28.09), før
låsen, uten at leddet fulgte. Radene i `8-register.jsonl` består kandidatskjemaet; hodet skrives ikke. Feilen er
deterministisk og gjentar seg ved hver kjøring fra `f19a3e3`. **Portene i § 5 bygger ikke på registeret** —
presisjon på leserens verdikter, recall på unionen og verdiktene — så de kan måles; registerhodet føres som kjent
feil i den låste koden, rettes etter fase 3 i egen commit.

**Verksnivå teller silens flagg, ikke leserens.** `steg_verksniva` leser `treff` fra `3-dommer.jsonl` (dommeren,
2 188 flagg), ikke fra verdiktfilene. Derfor ga kjøringen 07:50, med 716 dommer, samme sha som kjøringen 05:25
med 0 (`ebacf20c…`). Det er leddets definisjon, ikke en feil; feltene `n_doemte_treff`/`n_loftbare` er silens.

**Gjort før gjenopptak** (eierens tre krav 30.09): (1) `gjenoppta` etterkontrollerer hvert ledd — ikke-tomme,
validerte utdata i fullt antall, for `les` hver økt id for id mot blindfila, ingen ledd ført før inndataleddet —
og stopper med rc 3 og navnet på det som mangler; testet på tilfellet over (økt 3, 30 av 343). (2) Leddene etter
`les` kjøres alltid om, i et eget kall med `--om`. (3) En delvis økt nekter start; de udømte fullføres med
`--fullfor-okt 3` i **én ny instans** med samme oppdrag (bare blindfil, utfil, kladdekatalog og antall byttet),
under `fullforing/okt-3-rest1/` — utenfor mønstrene målingen globber — og den gyldige delen føyes til verdiktfila.
De 30 dømte, og økt 1 og 2, er byte-kontrollert urørt før og etter (bytes + sha256 i `gjenopptak-logg.jsonl`).
Økt 4–12 er ikke «kjørt om»: ingen av dem dømte noe. Forbruket for økt 1–3 står i
`tilstand-foer-gjenopptak-*.json` på Vault, fordi leserleddet overskriver forbrukslisten ved neste kjøring.

**Og en gang til, i økt 7** *(lagt til 30.09.2026, frys-lesning 4: avsnittet beskrev bare det første stoppet)*.
Gjenopptatt fra `les` 10:08 med de nye kontrollene: økt 4–6 ble dømt fullt (342 hver, 16,7–23,1 min), økt 7 stoppet
etter **270 av 342** ved øktgrensen (11:30), og økt 8–12 ble avvist straks. Etterkontrollen stoppet kjeden med rc 3
og navnet på det som manglet — `verksniva`, `falsify` og `register` ble **ikke** kjørt på ufullstendige data. De 72
udømte ble fullført i én ny instans (`fullforing/okt-7-rest1/`, 6,6 min) med de 270 byte-kontrollert urørt, og
kjeden ble gjenopptatt fra `les` 14:38: økt 8–12 dømt fullt, alle 4 107 dømt, etterkontrollen bestått for `les`.
Til sammen: **14 økter som dømte** (1–12 og restene 3-rest1 og 7-rest1), **12 blokkert** av sandkassen (§ 0.6) og
**14 avvist** ved øktgrensen (4–12 og 8–12).

### 0.8 Registerleddet rettet — eneste endring i et ledd etter låsen (30.09.2026)

**Eierens avgjørelse 30.09.2026:** registerleddet rettes som eneste kodeendring etter lås, og føres her med sha
før og etter. Det er den eneste endringen i et **ledd**; `kjede/cli.py` ble endret alt 28.09 med referanseporten
(§ 0.3), som ikke rører noe ledd. *(Presisert 30.09.2026, frys-lesning 4: overskriften sa «eneste kodeendring i
kjeden».)*

| fil | sha256 før (låst, § 9) | sha256 etter |
|---|---|---|
| `src/gjenopptak/kjede/ledd.py` | `07fc3a77f5bdef3b91fa7b5ce444b01219e04e60b46a15af39264598d4906db8` | `39f8b9ded7f0bdbbbb3c771e77247ca2e441c94ee49e7080e67449f67fca334e` |

**Hva som er endret:** bare hodet. Byggingen er skilt ut i `registerhode()`, som nå fører `navnepolicy`,
`leser_datert` (dato fra leserleddet, modell og regelfil fra `kjede.toml`), `silrecall: "ikke målt"` og
merknaden `verksnivaa` (verksnivået teller silens flagg, § 0.7). Radene er uendret: innholds-sha-en er
**`f590f25afcd33ab7…` før og etter** (regnet uten de daterte feltene, som leddet selv gjør). Test:
`tests/test_kjede.py::test_registerleddets_eget_hode_bestaar_skjemaet` bygger hodet med leddet og validerer det —
testen som manglet da skjemaet ble strammet i `6666d4f`.

**Kjøringen:** `register` alene, fra arbeidstreet, med worktreets låste `kjede.toml` og kjøringens katalog,
`--from register --om --port "arbeidsliste (prospektiv port)"`. Filene som skilte seg fra låsen i kallet:
`ledd.py` (over) og `cli.py` (`40ebef04…`, referanseporten fra § 0.3, som bestås og ikke rører registerleddet).
Registerfila fra kjøringen før rettingen er sikret på Vault `fase3/register-foer-retting/8-register.jsonl`
(`251cc566…`). Worktreet står rent på `f19a3e3`. Etterkontrollen i `gjenoppta` består for alle ti ledd.

