# Hvordan de seks gjenåpningscasene ble valgt — slik det faktisk skjedde

**Skrevet 03.10.2026, etter ekstern fagfellevurdering (hovedinnvending 5, spørsmål 5).** Kildene er dokumentene som ble
skrevet da valgene ble tatt: `docs/LOFTBARE-VURDERING-v1.md` (21.09.2026) og `docs/SAKBEHANDLING-2026-09-27-triage.md`
(27.09.2026), med sakregisteret `docs/saker/REGISTER-SAKER.md`. Ingenting her er lagt til i ettertid utover sammenstillingen.

**Kort svar: utvalget er skjønn.** Ett trinn er en deterministisk regel; alt etter det er en vurdering av hva som var
gjennomførbart, gjort av samme språkmodellbaserte arbeidsflyt som resten av prosjektet under forfatterens styring. Det
fantes ingen trekkingsregel og ingen kjent inklusjonssannsynlighet. **De seks er en bekvemmelighets-/eksplorativ caseserie.**

## Case 1 — PS-246 (Pring 2016, `W2551114598`), valgt 21.09.2026

| trinn | regel | type |
|---|---|---|
| pool | treffene i 320-settet som koder 1 kalte ekte og ga **løftbar klasse** — fire: PS-202 (H2), PS-266 (H2), PS-119 (H5), PS-246 (H5) | deterministisk (gitt koder 1s etiketter) |
| valg | `LOFTBARE-VURDERING-v1.md`: «Forsøk PS-246. Det er det eneste av de fire der hindringen er en programvareskranke og ikke fravær av» materiale; de tre andre krevde gjenstander, avbildning eller daglige måleserier som ikke var tilgjengelige | **skjønn** (tilgjengelighet av inndata) |

PS-246 ble valgt **fordi** inndataene fantes. Utvalget er dermed betinget på tilgang — og en serie valgt slik kan ikke
brukes til å si noe om hvor ofte tilgang er hindringen.

## Case 2–6 — SAK-14, SAK-09c, SAK-08, SAK-09b, SAK-11, valgt 27.09.2026

| trinn | regel | antall | type |
|---|---|---|---|
| 1 pool | rader i kandidatlista (register v2, 432) med **løftbar eller uavklart klasse** (H1–H6 eller `H1/H7-uavklart`) **og `tvil: false`** hos leseren | 50 passasjer | **deterministisk** |
| 2 gruppering | passasjene gruppert til saker, enhet **verk × hindring** | 19 saker (SAK-01–17, SAK-09 delt i 09a/d, 09b, 09c) | skjønn (hva som er «samme hindring») |
| 3 forkastet | saker som «krever fysisk materiale, feltarbeid eller mennesker», og SAK-01 (= PS-246, alt gjennomført) | 10 saker forkastet | **skjønn** |
| 4 kortliste | de som «kan låses» med et kriterium før beregning og der ressursen trolig fantes (merket **[V]**: ikke kontrollert før kriteriet ble skrevet), i triagens rekkefølge: SAK-14, SAK-09c, SAK-08, SAK-09b, SAK-11, SAK-13 | 6 | **skjønn** |
| 5 parkert | SAK-13: «svakt kriterium, ugjort har ingen fasit» | 1 | skjønn |
| — | SAK-15, -16, -17: bare siteringsoppslag (L5), ikke forsøk | 3 | skjønn |
| 6 kjørt | de fem øvrige | 5 | — |

**Begrunnelsen som sto i triagen:** SAK-14 og SAK-09c ble valgt fordi hindringen var språk eller ekstraksjon og
opphevelsen kunne være en språkmodell («AI-aksen»), SAK-08 og SAK-11 fordi hindringen var regnekraft («regnekraft-aksen»),
SAK-09b fordi et annet verktøy fantes. Kriteriet for å komme på kortlista var altså **at gjenåpningen var tenkbar med de
midlene prosjektet hadde** — det motsatte av et tilfeldig utvalg.

**SAK-15, -16, -17 og PS-246-utvidelsen** er ikke gjenåpningsforsøk, men siteringsoppslag («har noen gjort det siden?»)
på saker som ellers var parkert eller forkastet; de inngår ikke i de seks.

## Hva dette betyr for konklusjonen

* Utvalget favoriserer saker der inndata **så ut til** å finnes og der en modell **kunne** tenkes å løfte hindringen.
  At tre av seks likevel stoppet på manglende inndata (samtykke, kode, scenariosett), er en observasjon om disse tre.
  Det er **ikke** et estimat av hvor ofte tilgang eller samtykke er hindringen, og det er ikke en sammenlikning med
  modellkapasitet — en slik kontrast var ikke designet.
* Formuleringen i sammendraget og diskusjonen («what limits the reopening … is access and consent, not model capability»)
  følger ikke av dette utvalget og skrives om til en deskriptiv caseserie.
* «Lifted» fikk sin definisjon (ADR-0013) 28.09.2026, etter at de seks var forsøkt. Kriteriene for PS-246, SAK-14 og
  SAK-09b var låst før beregning (sakregisteret); SAK-09c, SAK-08 og SAK-11 nådde aldri et låst kriterium, men den overordnede klassifikasjonen av casene er retrospektiv.

## Hva en prospektiv serie ville kreve

En definert samplingramme (for eksempel alle H1–H6 med `tvil: false` i en ny, låst kjøring), en trekkingsregel med kjent
inklusjonssannsynlighet, og utfallene **tilgang manglet / teknisk ikke mulig / kriteriet ikke nådd / løftet** definert og
offentlig tidsstemplet før første case velges. Ikke gjort; ikke låst.
