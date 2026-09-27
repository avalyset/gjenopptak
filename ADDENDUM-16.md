# ADDENDUM-16 — ekstraksjon per dokumentvindu: kriteriene, låst før kjøring

**Skrevet:** 2026-09-26, **før** kjøringen. **Gjelder:** ADR-0011, PREREG-v1 §8.
Alt i dette addendumet — prompt, vindu, matchdefinisjon, dødsbetingelser — er fastsatt før første
vindu ble sendt. Prompten endres ikke etter at filen er committet.

## 1 Hypotesen

Kostnaden i L2 ligger i **enheten**, ikke i silen. Fire siler er prøvd og forkastet mot tekstbiten som
enhet (ADDENDUM-06/07 markørliste, ADDENDUM-14 embeddinger, ADDENDUM-15 seksjonsfordeling og nærsøk).
Med steg 3 og vindu ±2 dømmes hver setning om lag fem ganger: 22 243 dommer for om lag 222 setninger
per verk. **Hypotesen er at en ekstraksjon som leser et dokumentvindu én gang og siterer de setningene
som oppfyller treffkravet, finner de samme treffene for mindre samlet tid.**

## 2 Prompten, låst

Fil: `prompts/ekstraksjon-v1.txt`, **594 bytes**,
**sha256 `c8c276df9ffe62c906db566c24abcf6f415746a8271f737928f426f94dbeb534`**.

Sha-en føres i hver utdatalinje. Engelsk ledetekst fordi korpuset er 52,9 % engelsk og resten
romansk/tysk (ADDENDUM-14 §2), og fordi prompten ber om sitat på originalspråket.

## 3 Vindu og modell

| | |
|---|---|
| vindustørrelse | ca. **3 000 tokens**, overlapp **200**, kuttet på setningsgrense |
| modell | **gemma2:9b**, vekt-sha256 `ff1d1fc78170d787ee1201778e2dd65ea211654ca5fb7d69b5a2e7b123a50373` |
| temperatur · frø | **0** · **734248** |
| **num_ctx** | **8192**, satt eksplisitt i `options` |

**Hvorfor 8192 og ikke 4096.** Spesifikasjonen krever minst 4096. Den første kanarikjøringen med
`num_ctx: 4096` ga `prompt_eval_count = 4096` — altså nøyaktig taket, som er signaturen på stille
trunkering: et vindu på om lag 2 900 anslåtte tokens pluss prompt overskred 4096 reelle tokens, og
halen ble kuttet bort. Med 8192 gir samme vindu `prompt_eval_count = 3013`, godt under taket.

## 4 Kanariverifikasjonen, og en rettelse av den

Kravet: bygg ett vindu på maks lengde med kanarisetningen
«The authors were unable to collate manuscript X owing to lack of time.» **sist**, og bekreft at den
blir sitert.

**Første kjøring rapporterte falsk grønt.** Kontrollen var skrevet som «kanarisetningen inneholder
linjen ELLER linjen inneholder kanarisetningen», uten å utelukke tomme linjer — og den tomme strengen
er delstreng av alt. Utdataene inneholdt ingen `Q:`-linje i det hele tatt; modellen skrev et sammendrag.
Kontrollen er rettet til: **bare linjer som begynner med `Q:`, og tomme sitater diskvalifiseres.**

**Grønt etter rettingen:** vindu med 93 setninger (2 140 ord), kanarisetningen som nr. 93,
`prompt_eval_count = 3013` (ikke trunkert), veggtid 18,7 s. Utdata inneholdt **én** `Q:`-linje, og det
var kanarisetningen, ordrett. Loggført i
`ekstraksjon/2026-09-26/kanaritest.json` på Vault.

## 5 Matchdefinisjonen, låst

> En fasit-treff regnes funnet når kandidatsetningen i fasit-tekstbiten er inneholdt i en sitert
> linje, ELLER den siterte linjen er inneholdt i fasit-tekstbiten (±2), etter NFC-normalisering,
> samlet mellomrom, uten tegnsetting i endene. Ingen fuzzy match.

I tillegg, av erfaringen i §4: en sitert linje med tomt innhold etter normalisering teller ikke som
sitat.

## 6 Dødsbetingelser, ordrett

> Utvalgstesen (steg 1): lever bare hvis treff per verk i den tetteste typen eller
> leveringsformen er ≥ 2 × den glisneste, med minst 5 verk i hver gruppe. Færre enn 5:
> «ikke avgjørbar», ikke «død».
> Seksjonsplassering: dødt for godt hvis alle merkede treff krever > 50 % av de merkede
> tekstbitene.
> Ekstraksjon (steg 2): død hvis ETT av disse inntreffer — recall < 21/25; samlet tid
> ikke under nærsøk-rutens samlede tid; blind presisjon ≤ 23,4 % (dommerens øvre
> intervallgrense). Ingen promptrevisjon i denne slyngen. En revidert prompt er en ny
> preregistrert test med eget addendum, og resultatet rapporteres ved siden av det
> første, ikke i stedet for.

## 7 Referansen som skal slås

Nærsøk-ruten (ADDENDUM-15 §2, variant B ved n = 40): **4 240 kandidater**, 21 av 25 treff. Samlet tid
er søket, som er sekunder i en posisjonsindeks, pluss dømming av 4 240 × 3,8 s = **4,5 timer**.
Ekstraksjonen må komme under det, medregnet både ekstraksjon og dømming av de siterte linjene.

## 8 Hva som måles etterpå, og av hvem

Recall mot de 25 etter §5, med **de fire treffene som mangler markørord** (ADDENDUM-15 §2, taket
21/25) skilt ut. Presisjon måles på **100 tilfeldig trukne siterte linjer** (frø 734248) av en
**separat instans med tom kontekst**, som får PREREG-v1s treffdefinisjon og ADDENDUM-10 §3 og
ingenting annet — ikke fasiten, ikke registeret, ikke dommerutdata, ikke ekstraksjonsloggen, ikke
denne prompten. Wilson-intervall oppgis. **Uavhengigheten rekker bare så langt som modellfamilie og
regelsett:** begge instanser er samme modellfamilie og leser samme regler, så dette måler
regelanvendelse, ikke to uavhengige lesere.
