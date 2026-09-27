# ADDENDUM-15 — form framfor tema: seksjonsfordeling og nærsøk som førsteledd

**Skrevet:** 2026-09-26. **Gjelder:** PREREG-v1 §8 og L2-rørledningen, etter ADDENDUM-14.
**Utfall: negativt på kravet, positivt på sammenligningen.** **Ingen av de to rutene når 90 % recall
ved noe kuttpunkt**, og for den ene er grunnen strukturell: fire av de 25 treffene inneholder ikke
ordene i det hele tatt. Men der den beste ruten *kan* nå — 84 % recall — koster den **5,25×** mot
embeddingenes **2,0×** ved samme recall.

Fasit og kostnadsakse er identiske med ADDENDUM-14: de **25 ekte treffene i treff-stratumet**, og
andelen av **22 243** passasjer dommeren må se. Dommeren bruker 3,8 s per passasje; alt er 23,5 timer.
Referansen å slå var **1,4–1,6×** (embeddinger ved 90 % recall).

## 1 A1 — seksjonsfordeling

**`section_normalised` finnes ikke i materialet.** Det som finnes er `section_raw` (251 distinkte
verdier) og `section_label_provenance`. Normaliseringen til elleve kanoniske seksjoner er låst i
`a1-seksjon-2026-09-26.json` før tallene ble sett, og er flerspråklig der kildene er det.

**Det avgjørende tallet kommer først: 18 099 av 22 243 passasjer (81,4 %) har ingen seksjonsmerking.**

| seksjon | alle passasjer | % | treff | % | berikelse |
|---|---|---|---|---|---|
| **(ingen merking)** | **18 099** | **81,4** | **20** | **80,0** | 0,98× |
| annet (merket) | 1 579 | 7,1 | 2 | 8,0 | 1,13× |
| resultat | 1 518 | 6,8 | **0** | 0,0 | 0,00× |
| **diskusjon** | 404 | 1,8 | 2 | 8,0 | **4,40×** |
| **metode** | 281 | 1,3 | 1 | 4,0 | **3,17×** |
| innledning | 217 | 1,0 | 0 | 0,0 | 0,00× |
| sammendrag · konklusjon · takk/ref · datatilgang · begrensninger | 145 | 0,7 | 0 | 0,0 | 0,00× |

Berikelsen er reell der merkingen finnes: diskusjon 4,4×, metode 3,2×, og **resultat inneholder null
av 25 treff** trass i 1 518 passasjer. Men kumulativt:

| seksjoner beholdt | treff | passasjer | faktor |
|---|---|---|---|
| diskusjon | 2/25 = 8 % | 404 = 1,8 % | 55,06× |
| + metode | 3/25 = 12 % | 685 = 3,1 % | 32,47× |
| + annet (merket) | 5/25 = 20 % | 2 264 = 10,2 % | 9,82× |
| **+ (ingen merking)** | **25/25 = 100 %** | **20 363 = 91,5 %** | **1,09×** |

**90 %-terskelen krever den umerkede bunken, og da er faktoren 1,09×.** Ruten er dårligere enn
embeddingene.

### Provenance: ruten finnes bare for en femtedel av materialet

| provenance | passasjer | med merking | treff |
|---|---|---|---|
| **source** (JATS) | 4 328 = 19,5 % | 4 144 = **95,7 %** | 5 = 20 % |
| **parser** (PDF/HTML) | 17 915 = 80,5 % | **0 = 0,0 %** | 20 = 80 % |

Per felt: klinisk epidemiologi 83,4 % merket, arkeologi 18,3 %, **energimodellering 0,0 %,
tekstvitenskap 0,0 %.**

**Begrenset til JATS-delmengden virker ruten:** diskusjon + metode + annet dekker 5 av 5 treff der,
på 2 264 passasjer. Men det er 10,2 % av alt materiale for 20 % av treffene. **Et filter som bare
gjelder en femtedel av materialet, filtrerer ikke** — og de fire fem­delene som mangler merking, er
der 80 % av treffene ligger. Dette er ikke en svakhet ved normaliseringen; det er at PDF-parseren
ikke gir seksjonsmerker i det hele tatt (ADR-0007, `section_label_provenance`).

## 2 A2 — nærsøk i posisjonsindeks

Ingen modell, ingen kvote. Posisjonsindeks over alle 22 243 passasjer, median 75 tokens.
Spørringen er en **struktur**: et mangels-/negasjonsord innenfor *n* tokens av et modal-/evneord
innenfor *n* tokens av et handlingsverb. Rollelistene er bygget om fra markørlistens ordmateriale
(`passage.py` UNDONE/OBSTACLE) til tre roller og **utvidet til fransk, spansk og tysk**, fordi 27,7 %
av passasjene ikke er engelske. Rollelistene er låst i `a2-naersok-2026-09-26.json`.

Rolledekning i materialet: mangel/negasjon 31,4 % · modal/evne 27,3 % · handling 53,5 %.

**To varianter, rapportert som to målinger, ingen tuning.**

| n | A: tre roller — kand. (andel) → recall | B: to roller (uten modal) — kand. (andel) → recall |
|---|---|---|
| 3 | 186 (0,8 %) → 2/25 = 8 % | 1 027 (4,6 %) → 6/25 = 24 % |
| 5 | 290 (1,3 %) → 4/25 = 16 % | 1 503 (6,8 %) → 10/25 = 40 % |
| 7 | 406 (1,8 %) → 6/25 = 24 % | 1 921 (8,6 %) → 13/25 = 52 % |
| 9 | 538 (2,4 %) → 7/25 = 28 % | 2 272 (10,2 %) → **15/25 = 60 %** |
| 12 | 721 (3,2 %) → 7/25 = 28 % | 2 672 (12,0 %) → 16/25 = 64 % |
| 16 | 966 (4,3 %) → 7/25 = 28 % | 3 082 (13,9 %) → **17/25 = 68 %** |
| 20 | 1 185 (5,3 %) → 9/25 = 36 % | 3 370 (15,2 %) → 17/25 = 68 % |
| 40 | — | **4 240 (19,1 %) → 21/25 = 84 %** |
| 200 | — | 4 914 (22,1 %) → 21/25 = 84 % |

**Modalkravet koster recall.** Variant A ligger på 28 % fra n = 8 til n = 18 og kommer aldri over
36 %. Variant B, som dropper modalen, er bedre på alle *n*.

### Taket er strukturelt, ikke et spørsmål om n

| rolle | til stede i de 25 treffene |
|---|---|
| mangel/negasjon | 21/25 |
| modal/evne | **15/25** |
| handling | 24/25 |
| **alle tre** | **14/25 = 56 %** ← absolutt tak for variant A |
| **mangel + handling** | **21/25 = 84 %** ← absolutt tak for variant B |

**Fire av de 25 treffene inneholder ikke ordene.** Ingen verdi av *n* kan finne dem, og **90 % recall
er derfor uoppnåelig for begge varianter ved alle kuttpunkter.** Variant B metter ved n ≈ 40:
4 240 passasjer, 21/25, **5,25×, 4,5 timer**. Fra n = 40 til n = 400 kommer 677 kandidater til og
ingen nye treff.

## 3 Kombinasjonen gir ingenting

Seksjonsfilter først, nærsøk (variant B, n = 40) etter:

| filter | etter filter | + nærsøk | recall | faktor | timer |
|---|---|---|---|---|---|
| ingen seksjonsfilter | 22 243 | 4 240 | 21/25 | 5,25× | 4,5 |
| behold umerket + diskusjon/metode/annet | 20 363 | 4 064 | 21/25 | **5,47×** | 4,3 |
| dropp resultat og innledning | 20 374 | 4 070 | 21/25 | 5,47× | 4,3 |
| behold bare merkede treffseksjoner | 2 264 | 471 | **3/25** | 47,23× | 0,5 |

**Gevinsten er 4 %:** 4 240 → 4 064 kandidater, samme recall. Grunnen er triviell når A1s hovedtall
er kjent: når 81 % av passasjene er umerket, finnes det nesten ingenting å filtrere på. **Rutene er
ikke komplementære, fordi den ene ikke har noe å bidra med.**

## 4 Hva som står igjen

| rute | ved 90 % recall | ved sitt eget tak |
|---|---|---|
| markørliste v2 (ADDENDUM-06/07) | uoppnåelig | 2/25 = 8 % på 230 kandidater |
| embeddinger, bge-m3 (ADDENDUM-14) | **1,4–1,6×** | 84 % på 11 122 = **2,0×** |
| **A1 seksjonsfordeling** | **1,09×** | 100 % krever 91,5 % av materialet |
| **A2 nærsøk, variant B** | **uoppnåelig (tak 84 %)** | **84 % på 4 240 = 5,25×** |
| A1 + A2 kombinert | uoppnåelig | 84 % på 4 064 = 5,47× |

**På kravet er alle fire negative.** Ingen rute kan love dommeren 90 % av treffene for under to
tredeler av arbeidet — og to av rutene kan ikke nå 90 % i det hele tatt.

**På sammenligningen er A2 den klart beste.** Ved den recall den kan nå, 84 %, koster nærsøket
**4 240 passasjer mot embeddingenes 11 122** — en faktor **5,25× mot 2,0×**, altså **2,6 ganger
billigere ved samme recall**. Diagnosen fra ADDENDUM-14 §7 holder: et parkert spørsmål er en form, og
et ordmønster på den formen slår et emnemål. Formen er bare ikke *uttrykt* i hver fjerde av dem.

## 5 Hva målingen ikke viser

* **Den viser ikke at 84 % er taket for formbaserte ruter** — bare for *disse* rollelistene. De fire
  treffene uten ord er ikke nødvendigvis uten form; de kan uttrykke den med ordstillinger,
  tempus eller ord ingen av listene har. Å legge til ord etter å ha sett hvilke fire som mangler,
  ville vært tuning mot fasiten og er ikke gjort.
* **25 treff er få.** Ett treff er fire prosentpoeng, og taket 21/25 hviler på fire enkelttilfeller.
* **A1 er ikke målt mot et korpus med god seksjonsmerking.** Der JATS-strukturen finnes, virker ruten
  (5 av 5 treff i tre seksjoner). Konklusjonen gjelder *dette* materialet, der fire av fem passasjer
  kommer fra PDF.
* **Ingen av tallene er presisjon.** Rutene måles på recall og kostnad. Hvor mange av de 4 240
  kandidatene som er ekte treff, er ikke målt her; portmålingen sier 16,7 % blant dømte treff.
