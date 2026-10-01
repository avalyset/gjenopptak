# Fakta for manuskript v2 — hvert tall med sti og sha256

**28.09.2026.** Denne filen finnes for at utkastet skal skrives **fra den**, ikke fra chat. Hvert tall
har en sti og en sha256, og der to kilder oppgir ulike tall, står begge med grunnen til at de skiller
seg. Ingenting her er avrundet for å passe en setning.

**Regel for bruk:** finner du et tall i utkastet som ikke står her, er det ikke belagt. Finner du et
tall her som motsier chat, gjelder dette.

> **Datert rettelse 28.09.2026, etter utgivelse v0.3.** Sakdokumentene ble redigert før push —
> evaluerende setninger adressert til verket i stedet for til personen — og seks sha256-er i tabellen
> under endret seg som følge. De er rettet **her**, men **v0.3 som publisert bærer de gamle**:
> `967254a` inneholder både de redigerte filene og en faktafil som siterer sha-ene fra før
> redigeringen. Publiseringspolicyen tillater bare **én utgivelsescommit per MASTER-versjon** og
> **aldri force-push**, så rettelsen følger med neste MASTER-versjon. **Bytte-tallene i tabellen er
> også fra før redigeringen** for de samme seks filene. De to låste kriteriefilene er urørt, og deres
> sha-er står uendret og riktige.

> **Datert rettelse 28.09.2026, frys-lesningen før v0.4.0.** Rettet her: sha-tabellen i § 0 er regnet
> om for alle rader (fire sto på tilstanden før `0b4c979`/`9f07987`/`72c59a1`, og flere filer er endret
> av frys-rettelsene selv); sakregisterets og triagens sha i § 4 og § 5; κ-intervallet for 0,812 i
> leserstigen (sto [0,712–0,917], som hører til 0,826) og overlappet (0,712–0,768 → 0,697–0,768); løftbar
> andel med avklarte treff som nevner (ADDENDUM-05 § 4): 77/406, ikke 77/432; H7-sammenligningen;
> ADDENDUM-18-tallene; silens presisjon (15,2 %, ikke 14,3 %); vilkårsfordelingen (2–1–3, ikke 3–1–2);
> «fire av fem» → tre av fem; koder 4 ført inn. Ingen slutning snur.

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
| ADR-0012 (kjeden) | `docs/decisions/0012-kjeden-er-en-sti.md` | 11 452 | `6ee627a16bda7ddd2714f61c…` |
| METODE | `docs/METODE.md` | 35 529 | `6523425b17953dd440098d36…` |
| kjede.toml | `kjede.toml` | 5 029 | `65620200fb2a3ca7bc45273c…` |
| **register v1 (fasit)** | Vault: `register/claims.jsonl` | 40 639 | `a56cac542d26a296231351bd…` |
| **register v2 (kandidatlista)** | `data/kjede/kandidat432/8-register.jsonl` | 537 493 | `c6895202b76199aac1b35b53…` |
| registerhode v2 | `data/kjede/kandidat432/8-register-header.json` | 1 604 | `38366d7ce18d3360432a9505…` |
| koder 2s regelfil (gjenvunnet) | Vault: `koder2/koderegler-gjenvunnet.md` | 9 805 | `234695dd4e1777a958801ddf…` |
| recall-sett 2 | Vault: `logs/recall-sett-2.jsonl` | 27 728 | `40b3776ecb34c9e1748f086c…` |
| SAK-14 kriterium / resultat | `docs/saker/SAK-14/` | 4 022 / 17 622 | `5330c7017c5263c0173c4f2f…` / `cbb92c564782b4ab39fd01ff…` |
| SAK-09b kriterium / resultat | `docs/saker/SAK-09b/` | 6 913 / 11 438 | `2fa587a056ce7094531496fe…` / `0ff7a73213a647035a38e694…` |
| SAK-09c lukket | `docs/saker/SAK-09c/LUKKET.md` | 6 821 | `8c5430324a2a71fd4033dcff…` |
| SAK-08 lukket | `docs/saker/SAK-08/LUKKET.md` | 6 723 | `704155d25e12353f18e42d00…` |
| SAK-11 lukket | `docs/saker/SAK-11/LUKKET.md` | 8 767 | `d7d652f34cf7ed4a9107ddd9…` |
| sakregister | `docs/saker/REGISTER-SAKER.md` | 11 885 | `2c911716f6688e5b822b5eea…` |
| triage + L5-tillegg | `docs/SAKBEHANDLING-2026-09-27-triage.md` | 13 925 | `c3475829f18c2207b5a8ccd3…` |
*(Bytes og sha256 regnet om maskinelt mot disk 28.09.2026 etter frys-lesning 2: sju rader var foreldet av
senere commits — ADR-0012, METODE, SAK-14-resultatet, SAK-09c, SAK-08, sakregisteret og triagen. Tabellen
føres for dokumenter som fortsatt endres, og må regnes om ved hver endring av en fil den fører. Regnet om igjen 28.09.2026 for sakregisteret og triagen etter
SAK-08-tillegget, og for SAK-11 etter noten om forfattertallet, og for ADR-0012 etter
eierens bundleavgjørelse 29.09., og 30.09.2026 for docs/METODE.md etter tilleggene om fase 3-utfallet, og igjen etter frys-lesning 4 for docs/METODE.md, docs/SAKBEHANDLING-2026-09-27-triage.md, docs/decisions/0012-kjeden-er-en-sti.md, docs/saker/REGISTER-SAKER.md, docs/saker/SAK-11/LUKKET.md.)*

Repo: `https://github.com/avalyset/gjenopptak`, offentlig gren = rotcommit `5fcb353` + utgivelsescommit
`967254a` (v0.3), 168 filer publisert; oppdateres ved v0.4.0.
Konsept-DOI **10.5281/zenodo.22959326**. MASTER v0.3, Vault, sha256 `46aeb328b4b04ab68b980350…`.

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

### κ mellom koderne

`ADDENDUM-11.md` § 4. Cohen, paret bootstrap, 10 000 repetisjoner, frø **734248**.

| sammenlikning | n | rå enighet | κ | 95 % KI |
|---|---|---|---|---|
| treff / ikke-treff, alle 320 | 320 | 96,2 % | **0,812** | 0,697–0,906 |
| kun portmaterialet | 300 | 96,7 % | 0,774 | 0,623–0,898 |
| mot koder 1s **første** lesning | 320 | 96,6 % | 0,826 | 0,712–0,917 |

**Forbehold som må med:** alle kodere er LLM-baserte. **Ingen menneskelig annotør finnes.** Koder 2 var
en agentisk Claude Code-instans på `claude-opus-5`, ikke et menneske — modell-ID gjenvunnet fra
øktutskriften 27.09.2026 sammen med regelfilen (9 805 B, sha256 `234695dd4e1777a9…`), som aldri var
versjonert. κ = 0,812 er derfor **etterprøvbar på sin egen inndata**, men den måler samsvar mellom to
modeller, ikke gyldighet.

**Koder 4 (28.09.2026, `docs/METODE.md` «Koder 4»):** Fable 5.1 i chat, en **annen modellfamilie**, samme
320 passasjer, blindfil og regelfil. κ **0,899** [0,808–0,969] mot koder 2 og **0,781** [0,659–0,883] mot
koder 1. Retningen er motsatt av det modellfamilie-forbeholdet forutså, men intervallene overlapper.
**7 av 320 rader var eksponert** for koder 4 før kodingen (METODE, datert note); uten dem 0,874 og 0,757.
Koder 4 er heller ikke et menneske.

---

## 2 Leserstigen

`ADDENDUM-19.md` § 7.1. **Samme regelfil og samme kallstruktur** — ett kall per passasje, koder 2s fulle
regelfil, samme 320 passasjer. Gjengitt identisk i `ADR-0012`.

| leser | κ mot koder 1 | 95 % KI | flagget treff | klasse |
|---|---|---|---|---|
| Haiku 4.5 | **0,031** | −0,024–0,129 | 3 | **sil** |
| Sonnet 5 | **0,294** | 0,126–0,455 | 14 | **sil** |
| Opus 5, ett kall per passasje | **0,636** | 0,478–0,768 | 21 | grensetilfelle |
| koder 2 — Opus 5, **agentisk, én sammenhengende økt** | **0,812** | 0,697–0,906 | — | **leser** |

**Hovedfunnet:** rekken **0,031 → 0,294 → 0,636** er monoton, og intervallene for Haiku og Opus
**overlapper ikke**. Modellkapasitet dominerer.

**Forbeholdet som må med, og som er lett å utelate:** differansen mellom **0,636** og **0,812** er
**ikke statistisk etablert**. Intervallene overlapper i **0,697–0,768**, og punktanslagene skiller
0,176. Øktformens bidrag er derfor ikke påvist (ADDENDUM-19 § 7.2). §4s kriterium plasserer 0,636 i
båndet 0,30–0,70: «begge bidrar, ingen enkel forklaring står».

**2×2 for Opus, ett kall (19b):** 20 av koder 1s 39 treff funnet, 19 mistet, **bare 1 falsk positiv**,
280 begge enige om ikke-treff. **Presis men taper halvparten.**

**Tall som er UGYLDIGE og ikke skal siteres:** ADDENDUM-19s første Opus-kjøring ga κ = 0,390, rammet av
`max_tokens = 300`, som avkuttet 36 av 320 Opus-svar. ADDENDUM-18s Sonnet-tall **0,321** (n = 307) er
rammet av samme tak (12 avkuttet) og **erstattet av 0,297 [0,125–0,456], n = 319** (ADDENDUM-19 § 7.3) —
det er tallet som siteres. **Haikus 0,266 (n = 315) er gyldig og uendret**: det ene uparsede svaret var
ikke et takproblem. **27 av koder 1s 39 treff lå i det avkuttede settet.** Kjøringene
er beholdt, merket ugyldige, og skal ikke slettes — men de skal ikke brukes.

**Haiku med full regelfil ble dårligere:** κ = 0,047 (**partielt**, ADDENDUM-19:44; det komplette tallet er 0,031, l. 151) mot 0,270 med et tynt utdrag, differanse −0,222,
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
| løftbar klasse **H1–H6**, av avklarte (ADDENDUM-05 § 4) | **77 av 406 = 19,0 %** [15,4–23,1] |
| ikke-løftbar **H7–H9** | **329 av 432 = 76,2 %** [71,9–79,9] av alle treff; **av avklarte 329 av 406 = 81,0 %** [76,9–84,6], samme nevner som § 9 *(lagt til 30.09.2026)* |
| uavklart klasse, av alle treff | **26 av 432 = 6,0 %** [4,1–8,7] |

Løftbar andel har **avklarte treff** som nevner og oppgis alltid sammen med uavklart andel (ADDENDUM-05
§ 4, `classify.liftability.format_liftable`). *(Rettet 28.09.2026: sto 77 av 432 = 17,8 % [14,5–21,7],
med alle treff som nevner.)* H7–H9 er her oppgitt av alle 432, som i ADDENDUM-22.

**Klassefordeling:** H7 **289**, H5 **50**, H9 **29**, H1/H7-uavklart **26**, H2 **14**, H8 **11**,
H1 **10**, H3 **2**, H4 **1**.

> **Avvik som må håndteres i manuskriptet.** ADDENDUM-22 § 9.3 oppgir løftbar andel som **69 av 374 =
> 18,4 %** [14,8–22,7] — også den med alle treff som nevner. Det er **ikke en motsigelse**: 374 er tilstanden
> da fem av åtte leserøkter var avbrutt av leverandørens øktgrense (2 481 av 2 844 dømt, § 9.1). Addendumet
> ble **låst før kjøring**, og § 10 fører de komplette tallene. Tallene over er regnet fra det **ferdige**
> registeret med 432 rader. **Bruk 432-tallene, og oppgi at § 9.3 bærer den partielle tilstanden.**
> *(Rettet 28.09.2026, faktasjekk av manus v2: sto «ADDENDUM-22 § 10 oppgir» og at 374 var tilstanden «da addendumet ble låst, midt i
> kjøringen». Addendumet sier selv «Skrevet … før kjøring»; 69/374 står i § 9.3.)* Samme gjelder H7-andelen: H7 alene 253/374 = 67,6 %
> i addendumet, 289/432 = 66,9 % [62,3–71,2] ferdig; H7–H9 samlet 75,9 % i addendumet, 329/432 = 76,2 %
> ferdig. *(Rettet 28.09.2026: sto H7 alene mot H7–H9 samlet.)*

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

**`tvil` skiller presisjonen sterkt:** 97,6 % mot 75,9 %, 21,7 prosentpoeng, i en post hoc delgruppe.
Andre prediktorer (f.eks. silkilde) er ikke sammenlignet på de 100, og forskjellen er ikke testet.

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
hindringen.** Kilde: `docs/saker/REGISTER-SAKER.md`, sha i § 0.

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
* **Tre nevnere, merket som i `docs/saker/SAK-14/RESULTAT.md` § «Steg 1».** Grammatikken som ble kjørt, ble
  **utvidet etter første parse, altså etter låsing** (81 → 90 steder), og føres som avvik.
  * **90**, grammatikken som ble kjørt — **porten**: 79 = **87,8 %** [79,4–93,0].
  * **81**, første parse: 70 = **86,4 %** [77,3–92,2] (71 = 87,7 % hvis `HAL. AR`-stedet uten
    posisjonstreff regnes som oppløst).
  * **60**, bare formen presisering 1 ordrett krever: 55 = **91,7 %** [81,9–96,4], over terskelen — men
    **følsomhet, post hoc, nevner valgt etter utfall; ikke port**.
  * **Nevneren er 90, avgjort av eieren 28.09.2026**; utfallet står: ikke opphevet.
  *(Rettet 28.09.2026, frys-lesning 2: nevnerne 81 og 60, grammatikkutvidelsen etter låsing og eierens
  avgjørelse manglet her. Regnet fra `saker/SAK-14/tabell.json`, `steder.json` og `steder-v2.json` på
  Vault.)*
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
* Avhandlingens løsning **14** mot **18** for beste tvungne søk fra 120 starter og **15** for beste
  utvungne. Søk startet fra avhandlingens partisjon finner **ingen** forbedring. *(Rettet 28.09.2026:
  sto «Forfatterens»/«forfatterens»; navnepolicyen, samme ordlyd som SAK-09b/RESULTAT.md etter `0b4c979`.)*
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

**Bare SAK-14 kom fram til en terskel, og den falt med 2,2 prosentpoeng.** I **tre av fem** er det som
stanser saken, at **inndataen ikke er publisert** — profiler holdt tilbake av samtykke (SAK-09c),
modellkoden ikke funnet i seks sjekkede ruter med forlagets tilleggsmateriale uavklart (SAK-08; *(Rettet 28.09.2026, faktasjekk av manus v2: sto «modellkode aldri deponert», som `SAK-08/LUKKET.md` rettet 28.09)*), scenariosett og fordelingsparametere aldri oppgitt (SAK-11). I den
fjerde (SAK-09b) mangler det navngitte middelet mekanismen. **Porten siler ikke i ledd 2; tilgangen
gjør det.**

---

## 5 L5-svarene

«Har noen gjort det siden?» stilt for fire saker, besvart **nei i alle fire**. Kilde: triagens datert
tillegg 28.09.2026, sha i § 0. **10 OpenAlex-kreditter brukt av 40 tillatte**, ingen
`mailto` sendt til tjenesten.

| sak | verk | DOI | siteringer | svar og belegg |
|---|---|---|---|---|
| SAK-15 | Mythos 2018 `W2974992769` | `10.4000/mythos.297` | **3** | **nei** — ingen daterer smykkene og metallsmåfunnene fra deponeringsgrop H ved **Demeter-helligdommen i Knossos**; materialet hviler på Jackson 1973. Bredere søk «Knossos Demeter sanctuary» etter 2018: **137 treff**, ingen dateringsstudie |
| SAK-16 | Eythra 2017 `W4317830072` | `10.35686/ar.2017.12` | **2** | **nei** — begge om neolittisk keramikk andre steder. Bredere Eythra-søk: **81 treff**, og de to som gjelder boplassen, er **anmeldelser** (`10.11588/ai.2017.1.42531`, `10.11588/ger.2019.78651`) av Stäuble & Veits bind fra **2016**, altså før kildeverket |
| SAK-17 | Pietrele 2019 `W2936215896` | `10.1371/journal.pone.0214218` | **12** | **nei** — ingen analyserer flere blyforedlende digler fra 5. årtusen f.Kr. ved Nedre Donau. Nærmest: 2021-syntese på *eksisterende* data (`10.1007/s10963-021-09155-7`) og 2026-artikkel om slaggnoduler i Iberia (`10.15184/aqy.2026.10388`), annen region, ~3 årtusener senere |
| PS-246-utvidelsen | Pring 2016 `W2551114598` | — | — | **nei** — avhandlingen **har** EC-instrumentering (TDR), men EC-en rapporteres aldri som data; den er mellomledd på vei til vanninnhold. I **579 109 tegn** (581 864 bytes; *(Rettet 28.09.2026, faktasjekk av manus v2: sto «581 864 tegn»; tallet er bytes i `pring.txt`, UTF-8)*: `dS/m` **0** treff, `ECe` **0**, «saturated paste» **0**, «soluble salts» **0**, og eneste EC-verdi er **`0.0μS/cm`** — verdien som ble **satt**. Bulk-TDR-EC er dessuten den gale størrelsen: Saxton–Rawls krever `ECe` i dS/m fra mettet pastautdrag |

**Setningen manuskriptet skal bære:** ingen av nei-ene skyldes at feltet er dødt. Pietrele er sitert 12
ganger, Eythra-søket ga 81 treff, Knossos-søket 137. **En hindring blir ikke opphevet av at feltet
arbeider videre i nærheten.**

---

## 6 Forbehold som må følge tallene i manuskriptet

Ti forbehold, fra MASTER v0.3 § 7. De åtte første sto i v0.2; de to siste er nye.

1. **Tre kodere på de 320, alle LLM-baserte, ingen menneskelig annotør.** Koder 1 og 2 er Opus-instanser;
   koder 4 (28.09.2026) er Fable 5.1, en annen modellfamilie, med 7 av 320 rader eksponert.
   κ mot menneskelig lesning er ukjent.
2. **M2 bærer koderidentitet.**
3. **Formålsvalgte felt** — tallene gjelder disse fire.
4. **OA- og hentbarhetsseleksjon** med sterk forleggerskjevhet.
5. **Preregistreringen ikke eksternt tidsstemplet før data.**
6. **Regelpresiseringer skrevet etter data** — ADDENDUM-10 flyttet 1 av 48.
7. **Recall er den dårligst målte enden.**
8. **Ingen frontier-dommer** — API-stien er fjernet ved beslutning (ADR-0012, datert tillegg 27.09.2026), og
   ett-kall-frontiermodellene målte sil-klasse (ADDENDUM-18–20). *(Rettet 30.09.2026: sto «blokkert av gratiskvote».)*
9. **Register v2 validerte ikke mot sitt eget skjema, og er rettet 27.09.2026.** `sil.presisjon_ki`
   manglet på alle 432 rader, og `cites_coverage` bar et **umålt nulltall** (`0/0` uten `status`) på
   alle 432 mens `falsified` var `false` overalt. Rettet uten ny måling. `register_sha256`
   `aa8f7c2e…` → `6caabaff…` etter rettingen av de to feltene og SAK-14; `c6895202…` er tilstanden etter
   fire senere sakoppdateringer
   (REGISTER-SAKER, «Registerets sha-er, per oppdatering»). *(Rettet 28.09.2026, faktasjekk av manus v2: sto
   «rettet 28.09.2026» og `aa8f7c2e…` → `c6895202…`; registerhodet og REGISTER-SAKER daterer rettingen 27.09.)*
10. **Verktøyet er «åpent» i lisens, men ikke i praksis.** Uten Claude Code med Opus er silen alt man
    får, og silen er **15,2 %** presis (432 av 2 844; dommerleddet alene 14,3 %, ADDENDUM-22 § 10).

## 7 De fem ordene som ikke tåler vekt

Manuskriptet vil bruke disse ordene. Hvert av dem bærer mindre enn en leser vil tro, og for hvert er
det et **målt** tall som viser nøyaktig hvor mye mindre. Bruk dem med presiseringen i høyre kolonne,
eller la være å bruke dem.

| ord | hva en leser hører | hva det faktisk bærer |
|---|---|---|
| **«opphevet»** | at hindringen er borte | Ordet hadde **ingen definisjon** før 28.09.2026. Seks saker stanset på **tre ulike steder** — tilgang, reproduksjon, terskel — og ble alle kalt «ikke opphevet». ADR-0013 gir tre vilkår; før den er ethvert «opphevet» i eldre dokumenter et udefinert ord. **Vilkårsfordelingen for de seks er 2–1–3** (stanset på vilkår 1: SAK-09c, SAK-08; på vilkår 2: SAK-11; kom til vilkår 3: PS-246, SAK-14, SAK-09b). |
| **«fasit»** | grunnsannhet | Fasiten er **dommerbetinget**. Den kan måle recall-tap *relativt til dommeren*, og **ikke** presisjon for en ny metode, **ikke** absolutt recall, **ikke** prevalens (METODE § 2). «21 av 25» betyr «21 av de 25 dommeren fant og vi bekreftet». |
| **«bekreftet»** | uavhengig verifisert | **Kandidatlista:** registerhodet har `bekreftet: true`. Det som er bekreftet, er en **post hoc** port på **85 av 100** [76,7–90,7] — ikke den preregistrerte, som falt på 21 av 27. Og **15 av de 100** ble kodet av en **annen** instans etter at den første ble avbrutt etter 85. **Fase 3-lista:** `bekreftet: true` fra en **prospektiv** port, 85 av 100 [76,7–90,7], én instans (§ 9). I begge er «bekreftet» enighet med en annen LLM-lesning, ikke menneskelig validering. *(Fase 3 lagt til 30.09.2026.)* |
| **«stabil»** | en egenskap ved settet | «Stabil kjerne **3 av 27**» er ikke en egenskap ved fasiten, men ved **enigheten mellom to LLM-kodere uten tvilsmerke**. Koder 1 merket **20 av 27** med `tvil`. Delkriteriene: enige 19, uten tvil hos koder 1 bare 7, hos koder 2 bare 4. |
| **«uavhengig»** | en annen kilde til sannhet | Koder 2, koder c (ADDENDUM-22) og den blinde presisjonsleseren er alle **samme modellfamilie**; koder 4 (Fable 5.1) er den eneste av en annen familie, og heller ikke den er et menneske. **Ingen menneskelig annotør finnes** i hele sporet. «Uavhengig» betyr her *tom kontekst og egen kladdekatalog*, ikke uavhengig dømmekraft. κ mot menneskelig lesning er **ukjent**. |

**Tre ord som *tåler* vekten, og bør brukes i stedet der det går:** «kandidatliste» (lista har ikke
bestått en prospektiv port, og navnet sier det), «ikke målt» (en ærlig tilstand, ikke en mangel), og
«datert vurdering» (ADR-0010 — løftbarhet er ikke en egenskap ved teksten).

**En regel for utkastet:** setter du et av de fem ordene i en overskrift, i sammendraget eller i en
figurtekst, må presiseringen stå i samme avsnitt. Står ordet alene der, er det en påstand fila ikke
dekker.

## 8 Det manuskriptet IKKE kan påstå

* **Ikke prevalens.** Grunnraten a måler utvalget. Bruk c med intervall.
* **Ikke absolutt recall.** Fasiten er dommerbetinget.
* **Ikke at øktformen forklarer κ-forskjellen.** Intervallene overlapper i 0,697–0,768.
* **Ikke at lista er en arbeidsliste.** Den preregistrerte porten falt; navnet er kandidatliste,
  permanent, i alle dokumenter.
* **Ikke at presisjon er målt per hindringsklasse.** Bare per silkilde.
* **Ikke at noen hindring ble opphevet.** Seks saker, null opphevelser.
* **Ikke at de 432 radene dekker 100 verk.** De dekker **60**.

---

## 9 Fase 3 / ADDENDUM-25 — prospektiv port på 100 nye arkeologiverk

**Ført 30.09.2026.** Hvert tall under er lest maskinelt fra filene i tabellen, ikke skrevet av. Kildene ligger på
Vault under `fase3/` og står med full sha256 i `MANIFEST-VAULT.md`, seksjonen «Fase 3: leserleddet, portene og
utfallet». Kolonnen «kilde» gir fil og sha-prefiks per tall.

| kilde | sti | sha256 |
|---|---|---|
| preregistrering | `ADDENDUM-25.md` | `008b60be2b6842eb68991a51…` |
| utfall | `docs/RESULTAT-ADDENDUM-25.md` | `cb80085a9a0b7f335d418639…` |
| portmåling | Vault: `fase3/maaling-fase3.json` | `441cff4f1d949cbcc270b139…` |
| tilleggstall (§ 6–7) | Vault: `fase3/rapport-fase3.json` | `f5770e738bdce2c8c77c5f07…` |
| modell-ID fra utskrift | Vault: `fase3/utskrifter/modell-fra-utskrifter.json` | `ef8fd30bfb73b213aaf1f788…` |
| presisjonsinstansens verdikter | Vault: `fase3/presisjon/verdikter-presisjon.jsonl` | `5eb347d23cc9b5a8d98b7024…` |
| referansenøkkelen | Vault: `fase3/referanse/NOKKEL-referansesett.jsonl` | `6e38c3a7e04888934176ca91…` |
| registeret (rettet ledd, § 0.8) | Vault: `fase3-kjede/8-register.jsonl` | `b7d9230c93970c2614a8c4c6…` |
| registerhodet | Vault: `fase3-kjede/8-register-header.json` | `f586cc46e1259ab180370227…` |

*Utfallsraden er regnet om 30.09.2026 etter at registerleddet ble rettet (RESULTAT § 0.8, § 1.7); tabellen regnes om ved hver endring av en fil den fører.*

### Navnet

**Port (1) er bestått, og fase 3-lista heter `«arbeidsliste (prospektiv port)»`** (`maaling-fase3.json` `441cff4f1d949cbc…`). Navnet gjelder **fase 3-lista**
— 673 treff i 100 arkeologiverk — og ikke kandidatlista fra de første 100 (§ 3), som forblir kandidatliste.

### Port (1): blind presisjon

| mål | tall | kilde |
|---|---|---|
| leserens treff (populasjonen det trekkes fra) | **673** av 4 107 dømte | `rapport-fase3.json` `f5770e738bdce2c8…` |
| **presisjon** (terskel 0,70) | **85 av 100 = 85,0 %** [76,7–90,7] | `maaling-fase3.json` `441cff4f1d949cbc…` |
| leserens `tvil: false` | **37 av 38 = 97,4 %** [86,5–99,5] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| leserens `tvil: true` | **48 av 62 = 77,4 %** [65,6–86,0] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| samme klasse som leseren, blant de bekreftede | **76 av 85 = 89,4 %** [81,1–94,3] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| de avviste, instansens klasse | INGEN 8 · N3 7 | `rapport-fase3.json` `f5770e738bdce2c8…` |

Trukket med `random.Random(734248).sample` over treffene sortert på id; **én** instans, 100 av 100 i én
økt (ingen avbrudd, i motsetning til ADDENDUM-23, § 3). Delgruppene etter tvil er følsomhet, ikke port.

### Port (2): recall, uten terskel

Referansenøkkelen: **104 treff i 20 verk**, 60 uten tvil, 0 med ugyldig spenn (`maaling-fase3.json` `441cff4f1d949cbc…`).

| mål | tall | kilde |
|---|---|---|
| **beholdt av silen** | **95 av 104 = 91,3 %** [84,4–95,4] | `maaling-fase3.json` `441cff4f1d949cbc…` |
| **bekreftet av leseren** | **85 av 104 = 81,7 %** [73,2–88,0] | `maaling-fase3.json` `441cff4f1d949cbc…` |
| bekreftet blant beholdte | **85 av 95 = 89,5 %** [81,7–94,2] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| beholdt, uten referansetreff merket `tvil` | **56 av 60 = 93,3 %** [84,1–97,4] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| bekreftet, uten referansetreff merket `tvil` | **56 av 60 = 93,3 %** [84,1–97,4] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| **klynger:** verk med referansetreff; største verk (R08) | **12 av 20**; **51 av 104** treff (50 beholdt, 47 bekreftet) | `rapport-fase3.json` `f5770e738bdce2c8…` |
| beholdt, uten R08 | **45 av 53 = 84,9 %** [72,9–92,1] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| bekreftet, uten R08 | **38 av 53 = 71,7 %** [58,4–82,0] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| snitt per verk: beholdt / bekreftet | **85,9 % / 76,3 %** | `rapport-fase3.json` `f5770e738bdce2c8…` |

**Klyngene (lagt til 30.09.2026, frys-lesning 4):** Wilson over de 104 treffene antar uavhengighet, men treffene
ligger i 12 verk og halvparten i ett; intervallene er derfor for smale, og radene uten R08 er følsomheten.
**Tapene:** 9 i silen, 10 hos leseren. «Bekreftet» er enighet mellom to
lesninger av samme modellfamilie og regelfil, ikke mot et menneske (ADDENDUM-25 § 5); «beholdt» er det renere
tallet. **Dette er det første målte recall-tallet for silen** — § 8 «ikke absolutt recall» gjelder fortsatt: fasiten
er én CC-lesning per verk.

### Leserens treff og klasser

| mål | tall | kilde |
|---|---|---|
| treff av dømte | **673 av 4 107 = 16,4 %** [15,3–17,6] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| verk med minst ett treff | **73 av 100** | `rapport-fase3.json` `f5770e738bdce2c8…` |
| H7, av alle treff | **425 av 673 = 63,2 %** [59,4–66,7] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| **løftbar H1–H6, av avklarte** (ADDENDUM-05 § 4) | **101 av 628 = 16,1 %** [13,4–19,2] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| **uavklart, av alle treff** | **45 av 673 = 6,7 %** [5,0–8,8] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| ikke-løftbar H7–H9, av avklarte | **527 av 628 = 83,9 %** [80,8–86,6] | `rapport-fase3.json` `f5770e738bdce2c8…` |
| tvil blant treff | **362 av 673 = 53,8 %** [50,0–57,5] | `rapport-fase3.json` `f5770e738bdce2c8…` |

**Klassefordeling:** H7 **425**, H9 **68**, H2 **56**, H1/H7-uavklart **45**, H8 **34**, H1 **20**, H5 **12**, H4 **9**, H3 **3**, H6 **1** (`rapport-fase3.json` `f5770e738bdce2c8…`).
`format_liftable`: «løftbar 101/628 av avklarte = 16%; uavklart 45/673 = 7% (tabell: PREREG-v1-§5 + ADDENDUM-05)».

### Felt-tetthet mot de 100 første

ADDENDUM-25 § 7 oppgir ikke nevneren for «per 1 000 tekstbiter»; begge står, ingen er valgt.

| | treff | verk | per verk | per 1 000 korpus-tekstbiter | per 1 000 dømte |
|---|---|---|---|---|---|
| **fase 3, arkeologi** | 673 | 100 | 6,73 | 31,5 (av 21 361) | 163,9 (av 4 107) |
| første 100, arkeologi | 274 | 25 | 10,96 | 40,6 (av 6 741) | 276,8 (av 990) |
| første 100, alle fire felt | 432 | 100 | 4,32 | 19,4 (av 22 243) | 151,9 (av 2 844) |

Kilde: `rapport-fase3.json` `f5770e738bdce2c8…`. Tallene for de første 100 er ADDENDUM-22 § 10 (treff, dømt) og `data/kjede/kandidat432/3-dommer.jsonl`
(tekstbiter per felt), som i `fase3_rapport.FØRSTE_100`.
Silen slapp gjennom **4 107 av 21 361 = 19,2 %** [18,7–19,8] av korpuset (`rapport-fase3.json` `f5770e738bdce2c8…`); de første 100: 2 844 av 22 243 = 12,8 % (§ 3).

### Kostnad

OpenAlex: **8 kall**, `remaining` **985** etter; **før-verdien er ikke ført** (avvik fra § 6). Lokal
modelltid: dommer **25,81 t**, ekstraksjon **5,62 t** (`rapport-fase3.json` `f5770e738bdce2c8…`).

| Max-økter | økter | kontekst-tokens inn | output-tokens | minutter |
|---|---|---|---|---|
| referansesett | 20 | 13 767 605 | 219 726 | 64,7 |
| leser, økter som dømte | 14 | 79 538 395 | 1 239 475 | 283,1 |
| presisjonsport | 1 | 2 963 207 | 75 769 | 13,8 |
| leserøkter uten dom | 26 | 6 593 971 | 72 674 | 23,1 |

**Per bekreftet treff** (leserens treff × presisjon = 572): referansesett 24 069, leser **139 053**, presisjonsport
5 180 kontekst-tokens. **Per leser-treff: 118 185** (de første 100: 164 805, ADDENDUM-22 § 10). Kilde: `rapport-fase3.json` `f5770e738bdce2c8…`.
`total_cost_usd` i fila er `claude -p` sitt oppgitte API-ekvivalent — **ikke fakturert** på Max, og skal ikke stå som pris.

### Modell-ID

Fra øktutskriftene (`modell-fra-utskrifter.json` `ef8fd30bfb73b213…`), 41 i alt: **14 av 14 leserøkter som dømte** — økt 1–12 og
restene 3-rest1 og 7-rest1 — har bare `claude-opus-5`: 1, 2, 3, 3-rest1, 4, 5, 6, 7, 7-rest1, 8, 9, 10, 11, 12.
14 avviste økter har én `<synthetic>`-melding (øktgrensen); 12 sandkasseblokkerte og 1 prøve har bare
`claude-opus-5`. Presisjonsporten: bare `claude-opus-5` i både utskrift og `modelUsage`.

### Registeret

Skrevet av det rettede registerleddet (RESULTAT § 0.8): **673 rader**, `port: "arbeidsliste (prospektiv port)"`,
`bekreftet: true`, `n_dømt: 4107`; innholds-sha `f590f25afcd33ab7…` uendret av rettingen. **`silrecall` står som
«ikke målt»** — skjemaet tillater bare den verdien, og recall-tallet står i RESULTAT § 1.2, ikke i hodet. Hodet
bærer merknaden `verksnivaa`: verksnivåets tellinger (`n_doemte_treff`, `n_loftbare`) er silens flagg, ikke
leserens verdikter.

### Hva fase 3 ikke endrer, og hva manuskriptet ikke kan påstå om den

* **Ikke at kandidatlista fra de første 100 er en arbeidsliste.** § 8 står: den preregistrerte porten for den
  falt. Arbeidslistenavnet gjelder bare fase 3-lista.
* **Ikke at porten er vist for andre felt.** Fase 3 er ett felt, arkeologi, 100 verk. Arkeologi hadde høyest
  treffrate av de fire (§ 3); presisjonen i energimodellering eller tekstvitenskap er ikke målt prospektivt.
* **Ikke prevalens.** 673 av 4 107 er en rate i silens utvalg; felt-tettheten er treff per verk og per tekstbit.
* **Ikke at «bekreftet» er menneskelig validering.** Referanseleseren er samme modellfamilie og regelfil.
* **Ikke at forskjellen i tetthet mot de 25 første arkeologiverkene er et funn om feltet.** Målingen skiller
  ikke utvalg fra felt.
* **Ikke at registerhodet bærer det målte recall-tallet.** Det står «ikke målt» (skjemaet), se over.
