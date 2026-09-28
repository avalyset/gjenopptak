# Fakta for manuskript v2 — hvert tall med sti og sha256

**28.09.2026.** Denne filen finnes for at utkastet skal skrives **fra den**, ikke fra chat. Hvert tall
har en sti og en sha256, og der to kilder oppgir ulike tall, står begge med grunnen til at de skiller
seg. Ingenting her er avrundet for å passe en setning.

**Regel for bruk:** finner du et tall i utkastet som ikke står her, er det ikke belagt. Finner du et
tall her som motsier chat, gjelder dette.

## 0 Kilder, med sha256

| kilde | sti | bytes | sha256 |
|---|---|---|---|
| PREREG-v1 | `PREREG-v1.md` | 6 403 | `05988b238d9f22f9e7506524…` |
| ADDENDUM-11 (κ) | `ADDENDUM-11.md` | 10 091 | `1b64d8843dc0548ce4da933b…` |
| ADDENDUM-18 (kandidatlesere) | `ADDENDUM-18.md` | 10 873 | `3c1b3238a5070869e9b48081…` |
| ADDENDUM-19 (leserstigen) | `ADDENDUM-19.md` | 13 057 | `41a2f0cb38b26713bcf74680…` |
| ADDENDUM-20 (Haiku, full regelfil) | `ADDENDUM-20.md` | 8 505 | `604a17430f530a3dca2a10e4…` |
| ADDENDUM-21 (koder 3, ukjørt) | `ADDENDUM-21.md` | 7 751 | `de6c49743a0fc652776aa759…` |
| ADDENDUM-22 (porten) | `ADDENDUM-22.md` | 19 606 | `fc11ff062a0e0c2d620fdd3c…` |
| ADDENDUM-23 (post hoc port) | `ADDENDUM-23.md` | 7 604 | `d0eb2ca4818ea965ec722da7…` |
| ADR-0012 (kjeden) | `docs/decisions/0012-kjeden-er-en-sti.md` | 6 716 | `d5511a500822220263cfa7b1…` |
| METODE | `docs/METODE.md` | 20 416 | `33fabb6cd687b65fe5c8e437…` |
| kjede.toml | `kjede.toml` | 5 029 | `65620200fb2a3ca7bc45273c…` |
| **register v1 (fasit)** | Vault: `register/claims.jsonl` | 40 639 | `a56cac542d26a296231351bd…` |
| **register v2 (kandidatlista)** | `data/kjede/kandidat432/8-register.jsonl` | 537 493 | `c6895202b76199aac1b35b53…` |
| registerhode v2 | `data/kjede/kandidat432/8-register-header.json` | 1 414 | `93f7cafe140b5d734943a81d…` |
| koder 2s regelfil (gjenvunnet) | Vault: `koder2/koderegler-gjenvunnet.md` | 9 805 | `234695dd4e1777a958801ddf…` |
| recall-sett 2 | Vault: `logs/recall-sett-2.jsonl` | 27 728 | `40b3776ecb34c9e1748f086c…` |
| SAK-14 kriterium / resultat | `docs/saker/SAK-14/` | 4 022 / 15 781 | `5330c7017c5263c0173c4f2f…` / `5cc8128ce4947614361e45d5…` |
| SAK-09b kriterium / resultat | `docs/saker/SAK-09b/` | 6 913 / 10 975 | `2fa587a056ce7094531496fe…` / `092d446ceee48ddfbab159ab…` |
| SAK-09c lukket | `docs/saker/SAK-09c/LUKKET.md` | 6 543 | `4e76f32f823a2d003014d8f0…` |
| SAK-08 lukket | `docs/saker/SAK-08/LUKKET.md` | 5 840 | `229599c48925492347b04155…` |
| SAK-11 lukket | `docs/saker/SAK-11/LUKKET.md` | 8 044 | `4246f62ec891e8a7b8b31484…` |
| sakregister | `docs/saker/REGISTER-SAKER.md` | 10 157 | `f97a4c9843961bed44736d40…` |
| triage + L5-tillegg | `docs/SAKBEHANDLING-2026-09-27-triage.md` | 12 939 | `1d8ee07eb3165cd33adbce1b…` |

Repo: `https://github.com/avalyset/gjenopptak`, én rotcommit `5fcb353`, 153 filer publisert.
Konsept-DOI **10.5281/zenodo.22959326**. MASTER v0.3, Vault, sha256 `8914a2cced4d5d10a00b8834…`.

---

## 1 Fasit og stabil kjerne

**Tre tall forveksles lett, og manuskriptet må skille dem.** `docs/METODE.md` § 2.

| tall | hva det er | hvor |
|---|---|---|
| **25** | ekte treff funnet ved **blind lesing av 320 tekstbiter**, blant de **150 dommer-flaggede** som ble lest. Dette er fasiten for **recall-tap relativt til dommeren**. | METODE § 2 |
| **27** | **kjente treff i portmaterialet** — de 25 pluss PS-257 og PS-300, som ekstraksjonen fant og dommeren ikke. Dette er nevneren i ADDENDUM-22s port. | ADDENDUM-22 |
| **30** | rader i **register v1**, koder 1s bekreftede treff | Vault: `register/claims.jsonl` |

De 320 bar i tillegg **2 sanne blant de ikke-flaggede** (én i INGEN-stratumet, én i N3) — dommerens
tapte treff, målt for seg — og **12 ankertreff** med kjent fasit fra recall-sett 1 og 2, som er
frøsettets egne passasjer og ikke hører i en recall-måling.

### Hva fasiten kan og ikke kan måle

**Kan:** recall-tap for en ny metode *relativt til dommeren*, sammenlignbart mellom metoder fordi tallet
er det samme 25.

**Kan ikke:** (a) **presisjon** for en ny metode — de 25 er funnet blant dommerens flagg og er ikke et
tilfeldig utvalg; (b) **absolutt recall** — teller og nevner er begge dommerbetinget; (c) **prevalens**.

**Setningen manuskriptet må bruke:** «21 av 25» betyr «21 av de 25 dommeren fant og vi bekreftet», ikke
«21 av alle treff i materialet».

### Den stabile kjernen er **tre av 27**

`ADDENDUM-23.md` § 1, regnet fra `data/port-presisjonssett-ADDENDUM10.jsonl` (koder 1) og
`data/port-presisjonssett-verdikter-koder2.jsonl` (koder 2) alene.

| delkriterium | tall |
|---|---|
| koder 1 og koder 2 enige om treffstatus | **19 av 27** |
| uten `tvil` hos koder 1 | **7 av 27** |
| uten `tvil` hos koder 2 | **4 av 27** |
| **enige *og* ingen av dem i tvil** | **3 av 27** — PS-044, PS-205, PS-266 |
| koder 1 merket med `tvil` | **20 av 27** |

**Konsekvensen, ordrett fra METODE § 2:** «Fasiten kan bære et hovedfunn om klassefordeling; den kan
ikke bære en terskel nær sin egen ytterkant.»

### Grunnraten — tre tall, samme materiale

`docs/METODE.md` § 1. Materialet er **22 243 tekstbiter fra 100 verk**
(`data/port/spesifikasjon.json` → `sum_passasjer`), hvorav dommeren flagget **2 173**.

| regnemåte | koder 1 | hva det er |
|---|---|---|
| a) bekreftede treff / alle tekstbiter | 25/22 243 = **0,112 %** = ett per **890** | **måler utvalget — skal ikke brukes** |
| b) presisjon × flaggede / alle | 0,1667 × 2 173 = 362 → **1,63 %** = ett per **61** [1,13–2,29 %] | et **gulv** |
| c) b delt på implisert recall | 362/0,475 = 763 → **3,43 %** = ett per **29** [2,12–7,95 %] | **beste anslag** |

**Bruk c, med intervallet, og si hvilken du bruker.**

### κ mellom de to koderne

`ADDENDUM-11.md` § 4. Cohen, paret bootstrap, 10 000 repetisjoner, frø **734248**.

| sammenlikning | n | rå enighet | κ | 95 % KI |
|---|---|---|---|---|
| treff / ikke-treff, alle 320 | 320 | 96,2 % | **0,812** | 0,697–0,906 |
| kun portmaterialet | 300 | 96,7 % | 0,774 | 0,623–0,898 |
| mot koder 1s **første** lesning | 320 | 96,6 % | 0,826 | 0,712–0,917 |

**Forbehold som må med:** begge kodere er LLM-baserte. **Ingen menneskelig annotør finnes.** Koder 2 var
en agentisk Claude Code-instans på `claude-opus-5`, ikke et menneske — modell-ID gjenvunnet fra
øktutskriften 27.09.2026 sammen med regelfilen (9 805 B, sha256 `234695dd4e1777a9…`), som aldri var
versjonert. κ = 0,812 er derfor **etterprøvbar på sin egen inndata**, men den måler samsvar mellom to
modeller, ikke gyldighet.

---

## 2 Leserstigen

`ADDENDUM-19.md` § 7.1. **Samme regelfil og samme kallstruktur** — ett kall per passasje, koder 2s fulle
regelfil, samme 320 passasjer. Gjengitt identisk i `ADR-0012`.

| leser | κ mot koder 1 | 95 % KI | flagget treff | klasse |
|---|---|---|---|---|
| Haiku 4.5 | **0,031** | −0,024–0,129 | 3 | **sil** |
| Sonnet 5 | **0,294** | 0,126–0,455 | 14 | **sil** |
| Opus 5, ett kall per passasje | **0,636** | 0,478–0,768 | 21 | grensetilfelle |
| koder 2 — Opus 5, **agentisk, én sammenhengende økt** | **0,812** | 0,712–0,917 | — | **leser** |

**Hovedfunnet:** rekken **0,031 → 0,294 → 0,636** er monoton, og intervallene for Haiku og Opus
**overlapper ikke**. Modellkapasitet dominerer.

**Forbeholdet som må med, og som er lett å utelate:** differansen mellom **0,636** og **0,812** er
**ikke statistisk etablert**. Intervallene overlapper i **0,712–0,768**, og punktanslagene skiller
0,176. Øktformens bidrag er derfor ikke påvist (ADDENDUM-19 § 7.2). §4s kriterium plasserer 0,636 i
båndet 0,30–0,70: «begge bidrar, ingen enkel forklaring står».

**2×2 for Opus, ett kall (19b):** 20 av koder 1s 39 treff funnet, 19 mistet, **bare 1 falsk positiv**,
280 begge enige om ikke-treff. **Presis men taper halvparten.**

**To tall som er UGYLDIGE og ikke skal siteres:** ADDENDUM-19s første Opus-kjøring ga κ = 0,390, og
ADDENDUM-18 ga Haiku 0,266 og Sonnet 0,321. Alle tre er rammet av `max_tokens = 300`, som avkuttet 36
av 320 Opus-svar og 12 av Sonnets. **27 av koder 1s 39 treff lå i det avkuttede settet.** Kjøringene
er beholdt, merket ugyldige, og skal ikke slettes — men de skal ikke brukes.

**Haiku med full regelfil ble dårligere:** κ = 0,047 mot 0,270 med et tynt utdrag, differanse −0,222,
paret bootstrap [−0,402 – −0,044], utelukker 0 (ADDENDUM-20). ADDENDUM-19 § 7.1 snur tolkningen: det
var en egenskap ved Haiku, ikke ved reglene — **Opus bruker de samme reglene til κ = 0,64**.

---

## 3 Kandidatlista og presisjonen

### Lista

`data/kjede/kandidat432/8-register.jsonl`, sha256 `c6895202b76199aa…`, **432 rader** over **2 844 dømte
passasjer**. Registerhodet bærer porten som navn: **`«kandidatliste (post hoc port)»`**, `bekreftet: true`.

**Viktig tall som ofte antas feil:** de 432 radene dekker **60 unike verk**, ikke 100. Porten hadde 100
verk; 40 av dem ga ingen kandidatrad.

| oppdeling | tall |
|---|---|
| `tvil = false` / `tvil = true` | **218** / **214** |
| silkilde: dommer / begge / ekstraksjon | **260** / **124** / **48** |
| merket `ikke_prosa` | **11** av 432 = 2,5 % |
| løftbar klasse **H1–H6** | **77 av 432 = 17,8 %** [14,5–21,7] |
| ikke-løftbar **H7–H9** | **329 av 432 = 76,2 %** [71,9–79,9] |
| uavklart klasse | **26 av 432 = 6,0 %** [4,1–8,7] |

**Klassefordeling:** H7 **289**, H5 **50**, H9 **29**, H1/H7-uavklart **26**, H2 **14**, H8 **11**,
H1 **10**, H3 **2**, H4 **1**.

> **Avvik som må håndteres i manuskriptet.** ADDENDUM-22 § 10 oppgir løftbar andel som **69 av 374 =
> 18,4 %** [14,8–22,7]. Det er **ikke en motsigelse**: 374 var tilstanden da addendumet ble låst, midt
> i kjøringen. Tallene over er regnet fra det **ferdige** registeret med 432 rader. **Bruk 432-tallene,
> og oppgi at addendumet bærer den partielle tilstanden.** Samme gjelder H7-andelen: 253/374 = 67,6 % i
> addendumet, 329/432 = 76,2 % ferdig (H7–H9 samlet).

### Treffrate per felt

Målt over de 2 844 dømte passasjene. Summene stemmer: 274 + 53 + 37 + 68 = 432 og
990 + 347 + 378 + 1 129 = 2 844.

| felt | treff / dømt | rate | Wilson 95 % |
|---|---|---|---|
| arkeologi | 274 / 990 | **27,7 %** | 25,0–30,5 |
| klinisk epidemiologi | 53 / 347 | 15,3 % | 11,9–19,4 |
| tekstvitenskap | 37 / 378 | 9,8 % | 7,2–13,2 |
| energimodellering | 68 / 1 129 | **6,0 %** | 4,8–7,6 |

**Spredningen er en faktor 4,6 og er ikke støy:** intervallene for arkeologi og energimodellering
overlapper ikke i nærheten av hverandre.

### Silens presisjon — per kilde, ikke per klasse

`kjede.toml` `[sil]`, målt i ADDENDUM-22 § 10.

| silkilde | presisjon | Wilson 95 % |
|---|---|---|
| **begge** (dommer ∩ ekstraksjon) | **0,345** | 0,298–0,396 |
| dommer | **0,143** | 0,128–0,160 |
| ekstraksjon | **0,072** | 0,054–0,094 |

**Presisjon per hindringsklasse er ikke målt.** Bare per silkilde. Det skal stå.

### De to portene

**Den preregistrerte porten falt.** ADDENDUM-22 § 9–10: en tredje uavhengig koder bekreftet **21 av 27**
kjente treff mot terskel **22**. **Alle seks tapene var tvilsmerkede passasjer**, fire av dem allerede
blant koder 2s uenigheter. Terskelen ble ikke flyttet. **Lista heter derfor kandidatliste, permanent.**

**Den post hoc porten bestod.** ADDENDUM-23 § 7.2: **100 tilfeldige passasjer** som leseren kalte treff,
frø **734248**, lest blindt av en separat instans.

| mål | tall |
|---|---|
| bekreftet | **85 av 100 = 85,0 %**, Wilson 95 % **[76,7–90,7]** |
| klasseenighet blant de bekreftede | 74 av 85 = 87,1 % |
| der leseren **ikke** var i tvil | **41 av 42 = 97,6 %** |
| der leseren **var** i tvil | **44 av 58 = 75,9 %** |

**`tvil` er den enkeltopplysningen som forutsier presisjon best**, og forskjellen er 21,7 prosentpoeng.

> **Forbehold som ikke skal utelates:** § 4 sa «én separat instans». **Det ble to: 85 + 15.** Den første
> ble avbrutt etter 85 passasjer, og de 15 siste ble kodet av en ny instans med tom kontekst, egen
> kladdekatalog og identisk oppdrag. Det svekker «én lesning»-egenskapen. De 85 er et sammenhengende
> prefiks, ikke et utvalg.

### Grunnlaget for kjeden

`ADR-0012`, og `docs/METODE.md` § 1 og § 8.

| ledd | målt |
|---|---|
| tekstbiter | **22 243** fra 100 verk, setning ± 2, stride 3 |
| dommer (`gemma2:9b`, temp 0, frø 734248, `num_ctx` 8192) | flagget **2 173** av 22 243 |
| ekstraksjon | **884** Q-linjer fra 598 vinduer, 124 vinduer med NONE |
| union, kobling `alle-treff` | **2 844** kandidater, og **27 av 27** kjente treff dekket |

**Koblingsregelen var en retting, og den må nevnes:** første-treff-kobling ga union **2 581** og
**26 av 27**, fordi PS-300s Q-linje lå i to overlappende vindu. Alle-treff gir 2 844 og 27 av 27.

**Kostnadsenheten** er frontier-lesninger per bekreftet treff; for dommeren er den **≈ 6** (2 173
flaggede / 362 forventet sanne).

---

## 4 De fem sakene, med utfall

Fase 2, gjennomført 27.–28.09.2026. Seks saker i alt med PS-246 fra 25.09. **Ingen av dem opphevet
hindringen.** Kilde: `docs/saker/REGISTER-SAKER.md`, sha256 `f97a4c9843961bed…`.

| sak | verk | klasse | utfall | tallet som avgjorde |
|---|---|---|---|---|
| **SAK-14** | Haouachi 2016 `W2474595476` | H3 språk | **ikke opphevet** | **79 av 90 = 87,8 %** [79,4–93,0] mot terskel **90 %** |
| **SAK-09b** | Aragao 2018 `W7133020405` | H5 verktøygrense | **ikke opphevet av det navngitte middelet** | `blockmodeling` 1.1.8 har **ingen mekanisme**; utvunget ble partisjonene like **0 av 120** ganger |
| **SAK-09c** | Aragao 2018 `W7133020405` | H1/H7 → **H8 varig** | **lukket på `[V]`** | arkivposten har **én** innholdsfil; profilene holdt tilbake av samtykke |
| **SAK-08** | Riris 2018 `W2784603861` | H5 → **H8 utløser** | **lukket på `[V]`** | **seks** ruter sjekket, ingen modellkode |
| **SAK-11** | Bynum m.fl. 2021 `W4206850274` | H5 → **H8 utløser** | **stoppet på steg 3** | **C(41,7) = 22 481 940**; full enumerering ≈ **5,03 · 10⁹** beskrankninger |

### SAK-14 — tallene

* **90 greske sitatsteder**, 76 unike referanser, fra avhandlingens egne forkortelser. Dionysios 57,
  Plutark 22, Appian 5, Cassius Dio 3, Moralia 2, Aristoteles 1.
* **79 oppløst = 87,8 %** [79,4–93,0]. Kilde ført per sted: **Perseus 75, Scaife 4**. Perseus alene:
  **75/90 = 83,3 %** [74,3–89,6]. **Utfallet er det samme under begge.**
* De elleve: **7** utgaveadresserbarhet (fransk seksjonsinndeling finere enn de greske utgavenes),
  **3** verket mangler i åpen gresk utgave (Cassius Dio bok 1–35), **1** feilhenvisning.
* **10 461 greske ordformer** hentet. **11 av 90 steder** ville blitt ført som treff uten
  nivå-for-nivå-kontroll av oppløst mot forespurt adresse.
* **Hovedfunnet, post hoc:** **2 av 8** kontrollerbare henvisninger peker på feil sted —
  `AR I, 40, 1` oversetter I, 60, 1 og `AR I, 49, 3` oversetter I, 59, 3. **25 %** [7,1–59,1].
* **14 bærende termer**, alle maskinelt verifisert til å finnes tegn for tegn i den hentede gresken,
  **0 feil**. Avvik mot LSJ på aksen: **3 av 14** (underinstans, streng) eller **7 av 14** (min lesning);
  **enighet 10 av 14 = 71,4 %** [45,4–88,3]. **Oppgi begge, ikke ett.**
* Sideprodukt: Unicode→betakode-konverter verifisert mot **1 914 / 1 914** sanne par.
* Bare **11 av 90 steder** bærer avhandlingens egen franske gjengivelse = **12,2 %** [7,0–20,6]. Det er
  grunnen til at portens andre ledd var umålbart for resten.

### SAK-09b — tallene

* Reproduksjon: tabell D.1 **12 av 12 verdier eksakt** (bånd 148/146/133/249, snittgrad
  4,353/4,294/3,912/7,324, tetthet 0,132/0,130/0,119/0,222).
* **109 beskrankninger** rekonstruert fra en avkuttet liste: 13 + 36 + 48 + 12.
* **Total feil 14** reprodusert i to implementasjoner, med blokk (1,7) = **3** og (1,8) = **2** fra
  figur 8.2 som kontroll i begge. Over **alle 144** blokker er feilen **163** — et tall avhandlingen
  ikke oppgir, og uten det kan ingen etterprøve 14.
* Forfatterens løsning **14** mot **18** for beste tvungne søk fra 120 starter og **15** for beste
  utvungne. Søk startet fra forfatterens partisjon finner **ingen** forbedring.
* 𝑀 er **25 × 22** med **151 bånd** (109 faktor→aktivitet + 42 aktivitet→system). Avhandlingen skriver
  «𝑖 + 𝑘 columns» = 21; blokkformen gir 𝑗 + 𝑘 = **22**. **Feil i avhandlingens egen beskrivelse.**

### SAK-11 — tallene

* **C(41,7) = 22 481 940**, verifisert mot MATPOWER case30 (30 busser, **41 linjer**, 6 generatorer).
* Full enumerering **skalert lineært** fra artikkelens tabell 2 (100 scenarioer → 22 481 940,
  faktor **224 819**): **≈ 3,28 · 10⁹** kontinuerlige variabler og **≈ 5,03 · 10⁹** beskrankninger.
  Koeffisientmatrisen **0,2–0,4 TB** mot 11 GB ledig = minst **16×** for stort.
  **Skriv disse med to–tre signifikante siffer.** Tabell 2 gir fem siffer (14 579, 10 762, 11 613), og
  per-scenario-verdiene er de tallene delt på 100. Et tisifret produkt av dem later som om presisjonen
  er ti siffer; den er tre. Feilen ble fanget av en aritmetikkontroll som ga 5 030 334 075 der to
  separat avrundede ledd ga 5 030 334 074.
* Artikkelens egen påstand kontrollert: 100 av 22 481 940 = **0,000445 %**, under «less than 0.001 %».

### Mønsteret, som er et funn i seg selv

**Bare SAK-14 kom fram til en terskel, og den falt med 2,2 prosentpoeng.** I **fire av fem** er det som
stanser saken, at **inndataen ikke er publisert** — profiler holdt tilbake av samtykke, modellkode aldri
deponert, scenariosett og fordelingsparametere aldri oppgitt. **Porten siler ikke i ledd 2; tilgangen
gjør det.**

---

## 5 L5-svarene

«Har noen gjort det siden?» stilt for fire saker, besvart **nei i alle fire**. Kilde: triagens datert
tillegg 28.09.2026, sha256 `1d8ee07eb3165cd3…`. **10 OpenAlex-kreditter brukt av 40 tillatte**, ingen
`mailto` sendt til tjenesten.

| sak | verk | DOI | siteringer | svar og belegg |
|---|---|---|---|---|
| SAK-15 | Mythos 2018 `W2974992769` | `10.4000/mythos.297` | **3** | **nei** — ingen daterer smykkene og metallsmåfunnene fra deponeringsgrop H ved **Demeter-helligdommen i Knossos**; materialet hviler på Jackson 1973. Bredere søk «Knossos Demeter sanctuary» etter 2018: **137 treff**, ingen dateringsstudie |
| SAK-16 | Eythra 2017 `W4317830072` | `10.35686/ar.2017.12` | **2** | **nei** — begge om neolittisk keramikk andre steder. Bredere Eythra-søk: **81 treff**, og de to som gjelder boplassen, er **anmeldelser** (`10.11588/ai.2017.1.42531`, `10.11588/ger.2019.78651`) av Stäuble & Veits bind fra **2016**, altså før kildeverket |
| SAK-17 | Pietrele 2019 `W2936215896` | `10.1371/journal.pone.0214218` | **12** | **nei** — ingen analyserer flere blyforedlende digler fra 5. årtusen f.Kr. ved Nedre Donau. Nærmest: 2021-syntese på *eksisterende* data (`10.1007/s10963-021-09155-7`) og 2026-artikkel om slaggnoduler i Iberia (`10.15184/aqy.2026.10388`), annen region, ~3 årtusener senere |
| PS-246-utvidelsen | Pring 2016 `W2551114598` | — | — | **nei** — avhandlingen **har** EC-instrumentering (TDR), men EC-en rapporteres aldri som data; den er mellomledd på vei til vanninnhold. I **581 864 tegn**: `dS/m` **0** treff, `ECe` **0**, «saturated paste» **0**, «soluble salts» **0**, og eneste EC-verdi er **`0.0μS/cm`** — verdien som ble **satt**. Bulk-TDR-EC er dessuten den gale størrelsen: Saxton–Rawls krever `ECe` i dS/m fra mettet pastautdrag |

**Setningen manuskriptet skal bære:** ingen av nei-ene skyldes at feltet er dødt. Pietrele er sitert 12
ganger, Eythra-søket ga 81 treff, Knossos-søket 137. **En hindring blir ikke opphevet av at feltet
arbeider videre i nærheten.**

---

## 6 Forbehold som må følge tallene i manuskriptet

Ti forbehold, fra MASTER v0.3 § 7. De åtte første sto i v0.2; de to siste er nye.

1. **To kodere, begge LLM-baserte, ingen menneskelig annotør.** κ mot menneskelig lesning er ukjent.
2. **M2 bærer koderidentitet.**
3. **Formålsvalgte felt** — tallene gjelder disse fire.
4. **OA- og hentbarhetsseleksjon** med sterk forleggerskjevhet.
5. **Preregistreringen ikke eksternt tidsstemplet før data.**
6. **Regelpresiseringer skrevet etter data** — ADDENDUM-10 flyttet 1 av 48.
7. **Recall er den dårligst målte enden.**
8. **Ingen frontier-dommer** — blokkert av gratiskvote.
9. **Register v2 validerte ikke mot sitt eget skjema, og er rettet 28.09.2026.** `sil.presisjon_ki`
   manglet på alle 432 rader, og `cites_coverage` bar et **umålt nulltall** (`0/0` uten `status`) på
   alle 432 mens `falsified` var `false` overalt. Rettet uten ny måling. `register_sha256`
   `aa8f7c2e…` → `c6895202…`.
10. **Verktøyet er «åpent» i lisens, men ikke i praksis.** Uten Claude Code med Opus er silen alt man
    får, og silen er **14,3 %** presis.

## 7 Det manuskriptet IKKE kan påstå

* **Ikke prevalens.** Grunnraten a måler utvalget. Bruk c med intervall.
* **Ikke absolutt recall.** Fasiten er dommerbetinget.
* **Ikke at øktformen forklarer κ-forskjellen.** Intervallene overlapper i 0,712–0,768.
* **Ikke at lista er en arbeidsliste.** Den preregistrerte porten falt; navnet er kandidatliste,
  permanent, i alle dokumenter.
* **Ikke at presisjon er målt per hindringsklasse.** Bare per silkilde.
* **Ikke at noen hindring ble opphevet.** Seks saker, null opphevelser.
* **Ikke at de 432 radene dekker 100 verk.** De dekker **60**.
