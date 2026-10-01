# Faktasjekk av MANUSKRIPT-v2.1-UTKAST — bare det som fortsatt avviker — 28.09.2026

**Manuskript:** `docs/MANUSKRIPT-v2.1-UTKAST.md`, sha256 `cec17a3913cfb7a6f31190f2df7546029e17cc72ab699f062f4db69d4cd16a77`.
**Fasit:** `docs/MANUSKRIPT-FAKTA-2026-09-28.md`, sha256 `685d6ea0335bd0e8…` (commit `acfd915`, med de fire daterte
rettelsene fra faktasjekken av v2) og de samme kildene som forrige runde. **Ingen prosa er omskrevet.**
Forrige runde: `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md`.

## Metode

Hvert av de 56 avvikene fra v2 ble slått opp i v2.1 og vurdert på nytt, også der ordlyden var endret. Hver av de
83 nye eller endrede linjene i v2.1 ble faktasjekket fullt: tall, DOI, sitat, sha, id og dato. Uendrede linjer
som stemte i v2, ble kontrollert på nytt bare der fasiten er rettet i dag. Delrapporter på Vault,
`manuskript/faktasjekk-v2.1/`: del A (l. 1–250) sha256 `20e24becc5e64926…`, del B (l. 251–492) sha256
`2c946589421e0867…`. Kartet v2 → v2.1: `manuskript/faktasjekk-v2/kart-v2-til-v2.1.json`.

## Utfall

| | antall |
|---|---|
| avvik i v2 | 56 |
| **riktig rettet i v2.1** | **20** |
| **fortsatt avvikende** | **36** |
| **nye avvik i v2.1** | **9** |
| **avvik i v2.1 i alt** | **45** — 3 feil, 16 overclaim, 20 uklart, 4 uten kilde, 2 foreldet |
| venter på ADDENDUM-25-utfall | 4 |

**Merk ved linje 3:** v2.1 oppgir at 12 feil og 20 overclaim fra forrige faktasjekk er rettet. Minst ti av de 20
overclaim står ordrett i v2.1, og én feil (v2 l. 204) er byttet mot en ny feil (l. 210).

## Avvik i v2.1, sortert på linje

| linje | manuskriptet sier | riktig | kilde | status |
|---|---|---|---|---|
| 3 | revised after fact-check `136d025` (12 errors, 20 overclaims corrected) | 136d025 fant 12 feil og 20 overclaim; minst 10 av de 20 overclaim står ordrett i v2.1 (v2 l. 3, 26, 34, 67, 120, 122, 134, 160, 298, 461), og v2 l. 204 (feil) er byttet mot en ny feil forklaring (v2.1 l. 210–212) | docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md + Vault: manuskript/faktasjekk-v2/kart-v2-til-v2.1.json (`0e931be7`) | overclaim · **ny** |
| 4 | every number below is anchored there with a path and a sha256 | FAKTA fører fortsatt ikke 356, ~3 000 tokens, 70 %, «eight steps», «three independent grounds» eller XML/PDF-andelene; nye tall i v2.1 (16.09.2026, 20 ankere/8 ikke-treff, «12 errors, 20 overclaims») står heller ikke der | docs/MANUSKRIPT-FAKTA-2026-09-28.md (`685d6ea0`) | overclaim |
| 25 | Among confirmed hits, roughly two thirds name an obstacle of the kind that cannot be lifted by anyone: the data never existed | 289/432 er leserens kandidatrader, ikke bekreftede treff (bare en post hoc blindprøve, 85 av 100); PREREG § 5 fører H7 som «løftbar av AI i dag: nei», og løftbarhet er en datert vurdering (ADR-0010) | data/kjede/kandidat432/8-register.jsonl + PREREG-v1.md + docs/MANUSKRIPT-FAKTA-2026-09-28.md (`c6895202`) | overclaim |
| 31 | three stopped earlier because the input needed was never published | SAK-08: modellkoden «ikke funnet i seks sjekkede ruter», forlagets tilleggsmateriale uavklart (HTTP 403); ikke påvist upublisert (FAKTA § 4, rettet 28.09). SAK-11: OSTI-ruten er også ført som uavklart | docs/MANUSKRIPT-FAKTA-2026-09-28.md + docs/saker/SAK-08/LUKKET.md + docs/saker/SAK-11/LUKKET.md (`685d6ea0`) | overclaim · **ny** |
| 31 | Three cases reached a locked criterion | Tallet 3 stemmer (PS-246, SAK-14, SAK-09b på vilkår iii), men l. 34 sier «the one case that reached its threshold» om de fem nye. SAK-09b nådde låst kriterium uten tallterskel, og abstraktet gjør ikke rede for den; skill kriterium fra terskel | docs/decisions/0013-opphevelse-definisjon.md + docs/MANUSKRIPT-FAKTA-2026-09-28.md (`867f3038`) | uklart · **ny** |
| 33 | the input — interview profiles under consent, model code, a scenario set — was never published | SAK-08: modellkoden ikke funnet i seks sjekkede ruter, forlagets tilleggsmateriale uavklart (HTTP 403); FAKTA § 4 rettet 28.09 fra «modellkode aldri deponert» | docs/MANUSKRIPT-FAKTA-2026-09-28.md + docs/saker/SAK-08/LUKKET.md (`685d6ea0`) | overclaim · **ny** |
| 35 | cited only in translation could be retrieved and read against the original | 79 = referansen oppløst til gresk tekst; bare 11 av 90 steder bærer avhandlingens franske gjengivelse, og sammenligningen mot originalen gjelder 8 kontrollerbare steder | docs/saker/SAK-14/RESULTAT.md + docs/MANUSKRIPT-FAKTA-2026-09-28.md (`cbb92c56`) | overclaim |
| 67 | We report (i) the class distribution on 100 works | Klassefordelingen (432 rader) dekker 60 verk; FAKTA § 8: «Ikke at de 432 radene dekker 100 verk» | docs/MANUSKRIPT-FAKTA-2026-09-28.md + data/kjede/kandidat432/8-register.jsonl (`685d6ea0`) | uklart |
| 68 | (iv) six reopening attempts under a locked procedure | Prosedyren (ADR-0013) ble skrevet 28.09 etter de seks sakene, og bare 3 av 6 har låst kriteriefil, slik manus selv sier i § 3.5 | docs/decisions/0013-opphevelse-definisjon.md + docs/saker/SAK-09c/LUKKET.md (`867f3038`) | overclaim |
| 82 | works delivered as structured XML are almost always retrievable, works delivered as PDF in about half the cases | Ingen kilde fører andelene, og FAKTA har dem ikke. Nærmeste målinger er P3/PDF-leddet per vert (ADDENDUM-08 § 3) og karakterisering-*.json; JATS-hentbarhet er ikke målt som andel | ADDENDUM-08.md + data/utvalg/karakterisering-arkeologi.json (`6888efb3`) | uten kilde |
| 122 | it is deposited with v0.4.0 | v0.4.0 er «Forberedt, IKKE publisert» («publisert»: false); l. 141 sier selv «to be deposited with v0.4.0» | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md + Vault: zenodo/v0.4.0-bygg/UTGIVELSE-0.4.0.json (`03aab10d`) | overclaim |
| 122 | **Coder 4** (28 September) is Claude Fable 5.1 in a chat interface — a different model family | Kildene skriver «Fable 5.1 i chat, en annen modellfamilie»; ingen kilde bruker «Claude Fable», ingen modell-ID er ført, og oppdraget «finnes ikke som fil» | docs/METODE.md + docs/UTGIVELSE-v0.4.0-PORTSTATUS.md (`94c6ad68`) | uklart |
| 124 | Seven of the 320 rows had been seen by coder 4 with the reader's class labels the day before | 7 «ikke blindt kodet»: PS-266 eksakt tekstmatch; PS-246, -288, -289, -319 bare 2 felles setninger med en rad i kandidatfila; PS-257 og PS-300 bare kjent på id | docs/METODE.md + Vault: koder4/eksponerte-rader.json (`94c6ad68`) | overclaim |
| 136 | each locked as a single-file commit that triggers an archived bundle of the full git history | ADDENDUM-16s låsecommit e92620b har 2 filer; bundle-steget kom 12.09 (9e58a4e), og PREREG og ADDENDUM-01–04 har ingen kanon-bundle; ADDENDUM-10 og -11 har fått tillegg etter lås | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md + git show e92620b, 9e58a4e + Vault: repo/kanon/ (`03aab10d`) | overclaim |
| 139 | the lock order rests on the repository history, deposited with each version, and on OpenTimestamps receipts on the bundles (complete Bitcoin attestations from 28 September 2026 | For de 40 bundlene fra før 28.09 attesterer OTS bare at innholdet fantes 28.09, ikke låserekkefølgen; første tredjepartsgaranti er Zenodo-deponeringen 25.09.2026, som ikke nevnes | docs/TIDSSTEMPEL.md + docs/ZENODO.md (`9bad243f`) | uklart |
| 145 | The tool runs as one command in eight steps | Kjeden har ti ledd: hent, tekstbiter, dommer, ekstraksjon, union, blind, les, verksniva, falsify, register (ledd.py LEDD; MASTER-patch 28.09); manus utelater verksniva og falsify | src/gjenopptak/kjede/ledd.py + docs/patch/MASTER-2026-09-28-fase1-2.md (`07fc3a77`) | foreldet |
| 164 | work-level assessment, citation-falsification coverage | Registerradene (432) har ikke noe verksnivå-felt, og cites_coverage har status «ikke målt» på alle 432 («falsifiseringen ikke kjørt for denne kjøringen») | data/kjede/kandidat432/8-register.jsonl (`c6895202`) | overclaim |
| 210 | the figures here are computed from the finished register with decided hits as the denominator for the liftable share (ADDENDUM-05 §4), which is the reason the two sets differ | 374 er partiell tilstand (§ 9.3, 2 481 av 2 844 dømt). H7 253/374 og 289/432 har begge alle treff som nevner, så nevneren forklarer ikke den forskjellen. § 10 fører komplette 77/432 = 17,8 %; sammenlignbar partiell verdi er 69/353 = 19,5 % | ADDENDUM-22.md + docs/MANUSKRIPT-FAKTA-2026-09-28.md + docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md (`fc11ff06`) | feil |
| 229 | Seven of the 320 rows had been seen by coder 4 with labels before coding | Kilden: «7 av 320 rader er derfor ikke blindt kodet». Bare PS-266 var en eksakt tekstmatch; fire delte 2 setninger med en rad i kandidatfila, og to var kjent bare på id | docs/METODE.md (`94c6ad68`) | uklart |
| 246 | The boundary is now an explicit, versioned decision rule with anchor examples (`REGEL-N3-v1`). | REGEL-N3-v1 finnes (28.09, sha 96cd8372…), men «Regelen er ikke i bruk i fase 3». Ingen koding har brukt den, og effekten er ikke målt | docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md (`e42d44d3`) | uklart |
| 268 | Two earlier runs (κ 0.390 for Opus, 0.321 for Sonnet) were invalidated by output truncation at 300 tokens | 0,390 stemmer. 0,321 var ADDENDUM-18s Sonnet (tynt utdrag, n = 307), ikke en tidligere kjøring av stigens Sonnet-celle, og ble rettet, ikke forkastet: erstattet av 0,297 [0,125–0,456], n = 319, «det er tallet som siteres» | docs/MANUSKRIPT-FAKTA-2026-09-28.md § 2 + ADDENDUM-19.md § 7.3 (`685d6ea0`) | uklart |
| 294 | One deviation from the gate's text must stand: "one separate instance" became two, 85 plus 15 | Kilden er norsk: § 4 sa «én separat instans» (ADDENDUM-23 l. 65 og l. 127). Anførselstegnene gjengir en oversettelse; merk den som det eller siter originalen | ADDENDUM-23.md (`d0eb2ca4`) | uklart |
| 305 | six routes checked, no model code deposited | «modellkoden er ikke funnet i seks sjekkede ruter; forlagets tilleggsmateriale er uavklart (HTTP 403)»; triagens OSF-rute er ikke sjekket. «deposited» er ordlyden LUKKET.md trakk 28.09 | docs/saker/SAK-08/LUKKET.md (`704155d2`) | overclaim |
| 309 | Ninety citation places (76 unique references: Dionysius 57, Plutarch 22, Appian 5, Cassius Dio 3, *Moralia* 2, Aristotle 1) | 57/22/5/3/2/1 er per sitatsted og summerer til 90; per unik referanse er fordelingen 48/19/4/3/1/1 = 76. Tallene står etter kolon på «76 unique references» | Vault: saker/SAK-14/tabell.json (`caa70e01`) | uklart |
| 320 | without level-by-level comparison of the resolved against the requested address, all eleven would have been recorded as hits and the case would stand as lifted at 100 % | Holder bare under en ren HTTP 200 = treff-regel: minst seks Perseus-tilbakefall ga 0 greske ordformer og ingen oppløst adresse (n_ord= 0, fikk={}), og «Rom. 19, 9» ga «No document found» | Vault: saker/SAK-14/oppslag.log (`5de8c3e2`) | uklart |
| 337 | with 50 unconstrained starts it returned solutions whose two partitions of the intermediate mode differed | R-kjøringen brukte fritt blokktypevalg per blokk (blocks = nul/com/reg/rre; 11 løsninger med feil 0, det degenererte regimet). RESULTAT, rettet 28.09: ulike partisjoner er «et utfall under fritt typevalg», robustheten «er ikke prøvd» | docs/saker/SAK-09b/RESULTAT.md (`0ff7a732`) | uklart · **ny** |
| 343 | Two errors in the thesis's own description were found | Kilden kaller bare i + k = 21 (blokkformen gir j + k = 22) «en feil i avhandlingens beskrivelse». At «14» bare teller de 32 tre-modus-blokkene, føres som uoppgitt avgrensning («Det står ikke i avhandlingen»), ikke som feil | docs/saker/SAK-09b/RESULTAT.md (`0ff7a732`) | uklart · **ny** |
| 344 | "total error 14" counts only the 32 three-mode blocks without saying so | Avhandlingen ordrett: «the total error is 14». 32 stemmer; anførselstegnene gjengir ikke ordlyden | Vault: utvalg/energimodellering/ft-pdf-W7133020405-3765e3086324.json (`3765e308`) | uklart |
| 361 | Only SAK-14 reached a threshold, and it fell short by 2.2 percentage points. | Presiser som tallterskel: samme avsnitt (l. 364) sier at PS-246, SAK-14 og SAK-09b nådde vilkår iii, som i ADR-0013 heter «terskel» | docs/decisions/0013-opphevelse-definisjon.md (`867f3038`) | uklart |
| 362 | In three of five new cases the input was never published | For SAK-08: modellkoden «ikke funnet i seks sjekkede ruter med forlagets tilleggsmateriale uavklart»; FAKTA § 4 rettet 28.09 fra «modellkode aldri deponert». «never» er ikke målt for forlagets rute. (Var samsvar i v2 l. 352 mot gammel fasit.) | docs/MANUSKRIPT-FAKTA-2026-09-28.md § 4 + docs/saker/SAK-08/LUKKET.md (`685d6ea0`) | overclaim · **ny** |
| 373 | the answer from the citation graph is no in all four | «Nei i alle fire» stemmer, men bare tre ble besvart fra siteringer; PS-246-utvidelsen ble besvart ved søk i avhandlingen selv (manus sier det selv i l. 376–379) | docs/SAKBEHANDLING-2026-09-27-triage.md (`29445995`) | uklart |
| 396 | each of the attempts above took hours of tool-assisted work, and five of the six were done on 27–28 September | Datoene stemmer (fem av seks 27.–28.09, PS-246 25.09). Varigheten gjør ikke: commit-intervallene gir SAK-08 ≈ 20 min, SAK-09b ≈ 36 min, SAK-09c < 1 t, SAK-11 ≈ 1,5 t, SAK-14 ≈ 2 t; alle fem på ≈ 5,5 t (19:10–00:39); PS-246 12 min fra lås til resultat | git log --date=iso 59d4221^..704bbff -- docs/saker/ docs/PS-246-KRITERIUM.md docs/PS-246-RESULTAT.md docs/SAKBEHANDLING-2026-09-27-triage.md (+ Vault: saker/SAK-08/ mtime) (`62c97e3e`) | feil |
| 398 | the best AI-liftable candidate in the material, a critical edition parked for want of time to collate three British Library manuscripts | Heron-kollasjonen (W3000588547) er den positive H1-kontrollen, «utenfor de 100 verkene og utenfor nevneren (ADDENDUM-08 § 1)»; RESULTAT-PORT-v1 rettet 28.09 fra «Beste AI-kandidat» | docs/RESULTAT-PORT-v1.md (`2d1e24ac`) | foreldet |
| 404 | The claim that "some obstacles have since been lifted, some by AI" has no support in this material. | PREREG-v1 § 1.2 ordrett: «En del av disse hindringene er i dag opphevet, en andel av dem av AI.» Anførselstegnene gjengir en oversettelse som også avviker fra manusets egen § 1 (l. 54) | PREREG-v1.md (`05988b23`) | uklart |
| 414 | weakest at two non-hit boundaries (N3 0.530, N2 0.535) until the N3 boundary was written as a decision rule | N2 0,535 stemmer (METODE). «until» antyder at regelen hevet κ: REGEL-N3-v1 «er ikke brukt på de 320», 0,530 er før-tallet, regelen er heller ikke i bruk i fase 3 (KORRIGENDUM H); effekten er ikke målt, og N2 har ingen regel | docs/REGEL-N3-v1.md (`96cd8372`) | overclaim |
| 417 | Two of these results were reached only because the gates were locked before the runs and the losses could not be re-labelled afterwards. | Ingen kilde sier hvilke to resultater dette er eller at de avhang av låsingen. At ADDENDUM-22 ble skrevet før kjøring, stemmer (FAKTA § 3, rettet 28.09), men avsnittets resultater er κ-tall, ikke portutfall | docs/MANUSKRIPT-FAKTA-2026-09-28.md (`685d6ea0`) | uten kilde |
| 437 | the protocol never defined "without a domain expert" | PREREG-v1 § 2 ordrett: «lar seg avgjøre uten domeneekspert i faget». Oversettelse i anførselstegn, «i faget» utelatt; at begrepet er udefinert, stemmer (ADDENDUM-11 § 5) | PREREG-v1.md (`05988b23`) | uklart |
| 448 | corrected without new measurement (register sha256 `aa8f7c2e…` → `c6895202…`). | Rettingen ga aa8f7c2e… → 6caabaff… (de to feltene og SAK-14); c6895202… er tilstanden etter fire senere sakoppdateringer (SAK-09c, SAK-08, SAK-09b, SAK-11). FAKTA § 6.9 rettet 28.09 fra nettopp aa8f7c2e → c6895202 | docs/saker/REGISTER-SAKER.md + docs/MANUSKRIPT-FAKTA-2026-09-28.md § 6.9 (`4b7601fa`) | feil |
| 458 | the full working history is in the git bundles deposited with each Zenodo version | Deponerte bundler (v0.1.0–v0.3.0) dekker historikken til 26.09. Historikken 27.–28.09 (bl.a. 37d7187) er ikke deponert, og om v0.4.0 får den, er eierens valg (§ 4, § 8 pkt. 1) — manus sier det selv i l. 470 | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md (`03aab10d`) | overclaim |
| 463 | Licence per work is recorded in the manifest | LICENSE-DATA: «The licence of each source work is listed per work in docs/LISENS-PER-VERK.md»; MANIFEST-VAULT fører bare filene med sha | LICENSE-DATA (`7b731235`) | uklart |
| 466 | the lessons log, the registers and a bundle of the git history | Ett register: «registeret (claims.jsonl)», register v1. Register v2 (kandidatlista, 432 rader) ligger i ingen deponert versjon og ikke i v0.4.0-bygget (96 filer; data/ er ikke i git) — bare som sha i MANIFEST-VAULT | docs/ZENODO.md + Vault: zenodo/v0.4.0-bygg/UTGIVELSE-0.4.0.json (`8e726f64`) | uklart · **ny** |
| 470 | whether the full history bundle is included again is a decision of the author, recorded in the release notes. | Valget er ikke tatt: § 8 pkt. 1 «Eierens valg om historikkbundlen» mangler før autorisering. Ingen kilde sier at det føres i release notes | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md (`03aab10d`) | uten kilde · **ny** |
| 476 | as described in §2.4 and §3.2, with model identity recorded per verdict | Modell-ID per verdikt finnes for dommer og leser (fra kjede.toml, «ikke fra svaret»), ikke i koder 2- og koder 4-filene; koder 2s modell-ID er gjenvunnet fra øktutskrift; koder 4s oppdrag «finnes ikke som fil» | docs/RESULTAT-ADDENDUM-25.md + docs/UTGIVELSE-v0.4.0-PORTSTATUS.md § 6 (`52fdf5b6`) | overclaim |
| 477 | draft was written by Claude Fable 5.1 | Ingen fil i repoet eller på Vault fører hvilken modell som skrev utkastet; INSTRUKSER-v1.3 § 2 gir chat-Claude rollen «narrativ» uten modellnavn | docs/INSTRUKSER-v1.3.md (`ececde4b`) | uten kilde |
| 478 | every number was then checked against that file by a separate pass | Kontrollen av v2 er kjørt (136d025, mot kildene, ikke bare faktafila) og fant 56 avvik; kontrollen av v2.1 pågår. Manus l. 5–6: «Not for circulation until the fact-check pass (CC) has been run against this file» | docs/MANUSKRIPT-v2.1-UTKAST.md (`cec17a39`) | uklart |

## Venter på ADDENDUM-25-utfall

| linje | manuskriptet sier | merknad |
|---|---|---|
| 157 | The first measured recall will come from phase 3 [pending]. | Fase 3-kjøringen pågår («Status 28.09.2026: kjøringen pågår»); fylles fra utfallsfila |
| 381 | ### 4.7 Phase 3 — prospective gate and first measured recall *[pending]* | Venter: «Status 28.09.2026: kjøringen pågår»; § 1 Utfall «Ikke målt ennå» |
| 445 | Phase 3 supplies the first measured value *[pending]*. | Venter: RESULTAT-ADDENDUM-25 § 1 «Ikke målt ennå» |
| 484 | *[To be assembled from the register and case files. | Plassholder. Kontrollert: fem DOI-er gir 302 og stemmer med Crossref (forfatter/år; Bynum 7 forfattere, 2021), handle 1807/92034 løser; Haouachi har Crossref-DOI 10.70675/8513d3c9ze385z4b4bz910cz221c7718984d (→ theses.fr/2016STRAC019) |

## De fire feilene i faktafila — rettet der, datert

Rettet i `docs/MANUSKRIPT-FAKTA-2026-09-28.md` 28.09.2026 (commit `acfd915`), hver verifisert mot kilden før
rettingen og merket «Rettet 28.09.2026, faktasjekk av manus v2»:

1. **ADDENDUM-22:** 69/374 står i § 9.3, ikke § 10; 374 er tilstanden etter at fem av åtte leserøkter ble avbrutt
   (2 481 av 2 844 dømt). Addendumet ble låst før kjøring, ikke «midt i kjøringen».
2. **§ 6.9:** registerrettingen var **27.09**, ikke 28.09; sha-kjeden er `aa8f7c2e…` → `6caabaff…` ved rettingen,
   `c6895202…` etter fire senere sakoppdateringer.
3. **Pring:** 581 864 er bytes; teksten har **579 109 tegn**.
4. **SAK-08:** «modellkode aldri deponert» → modellkoden **ikke funnet i seks sjekkede ruter**, forlagets
   tilleggsmateriale uavklart (403).

Samme formuleringer står fortsatt i triagen («581 864 tegn»), i REGISTER-SAKER («ikke deponert») og i
registerhodet i `data/`, som ikke røres mens fase 3 går.

## Oppdaget underveis

* **Kandidatlista med 432 rader** (`data/kjede/kandidat432/8-register.jsonl`) finnes ikke i noen deponert
  Zenodo-versjon, og heller ikke i v0.4.0-utkastet: `data/` er ikke i git. Den er bare ført med sha i
  MANIFEST-VAULT. Manuskriptets l. 466 kan leses som om den er deponert.
* Haouachi 2016 har en Crossref-DOI som kan brukes i referanselista:
  `10.70675/8513d3c9ze385z4b4bz910cz221c7718984d`.
