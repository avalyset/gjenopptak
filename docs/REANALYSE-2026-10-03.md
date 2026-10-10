# Reanalyse etter ekstern vurdering gjort av en språkmodell — 03.10.2026

**Generert** av `src/gjenopptak/classify/reanalyse_fagfelle.py` fra `revisjon-2026-10/reanalyse.json` på Vault (sha256 `ac782709d90ada772493b546ba9466e8a75ff89e593d84b47f73fd21b12a4824`). Ingen tall er skrevet av for hånd. Bootstrap: 10 000 replikater, frø 734248, persentilintervall; **klyngeenheten er verket**. Ingen låst fil er endret.

## a) Verksklynget usikkerhet, side om side med manuskriptet

**320-settet:** 92 verk; rader per verk {1: 31, 2: 29, 3: 8, 4: 7, 5: 7, 6: 1, 7: 2, 8: 2, 12: 1, 17: 1, 22: 1, 24: 1, 33: 1}; største verk 33 rader.

| par | κ | manus (passasjebootstrap) | **verksklynget 95 %** | rå enighet | PABAK | Gwet AC1 | positive a/b |
|---|---|---|---|---|---|---|---|
| koder 1 mot koder 2 | 0,812 | 0,812 [0,697–0,906] | **[0,711–0,909]** | 96,2 % | 0,925 | 0,953 | 39/33 |
| koder 4 mot koder 2 | 0,899 | 0,899 [0,808–0,969] | **[0,833–0,974]** | 98,1 % | 0,963 | 0,977 | 33/33 |
| koder 4 mot koder 1 | 0,781 | 0,781 [0,659–0,883] | **[0,675–0,877]** | 95,6 % | 0,912 | 0,945 | 33/39 |
| Opus ett kall mot koder 1 | 0,636 | 0,636 [0,478–0,768] | **[0,503–0,744]** | 93,8 % | 0,875 | 0,925 | 21/39 |

## b) Paret bootstrap på differansen κ 0,812 − κ 0,636 (begge mot koder 1, samme 320 passasjer)

Punkt **0,177**; paret passasjebootstrap **[0,044–0,323]** (andel replikater ≤ 0: 0,42 %); paret verksklynget **[0,057–0,318]** (0,31 %). **Intervallet utelukker 0 i begge.** Manuskriptets «not statistically established», bygget på overlappende separate intervaller, er feil: med en paret test er differansen etablert.

## a) Porter, recall og klasseandeler

| mål | k / n | manus (Wilson, passasjer) | **verksklynget 95 %** | verk | rader per verk | største verk |
|---|---|---|---|---|---|---|
| blind bekreftelse, post hoc port (ADDENDUM-23) | 85/100 | 85/100 [76,7–90,7] | **[75,7–92,3]** | 33 | {1: 12, 2: 10, 3: 5, 4: 3, 10: 2, 21: 1} | 21 |
| blind bekreftelse, fase 3 (ADDENDUM-25) | 85/100 | 85/100 [76,7–90,7] | **[76,2–93,8]** | 38 | {1: 15, 2: 15, 3: 6, 17: 1, 20: 1} | 20 |
| silens recall, fase 3 | 95/104 | 95/104 = 91,3 % [84,4–95,4] | **[76,9–96,7]** | 12 | {1: 2, 2: 2, 5: 3, 6: 2, 10: 2, 51: 1} | 51 |
| leserens recall, fase 3 | 85/104 | 85/104 = 81,7 % [73,2–88,0] | **[60,9–89,7]** | 12 | {1: 2, 2: 2, 5: 3, 6: 2, 10: 2, 51: 1} | 51 |
| register v2 (432): H7 av alle rader | 289/432 | 289/432 = 66,9 % [62,3–71,2] | **[58,2–79,7]** | 60 | — | 118 |
| register v2 (432): løftbar H1–H6 av avklarte | 77/406 | 77/406 = 19,0 % [15,4–23,1] | **[9,0–26,5]** | 59 | — | 113 |
| fase 3-register (673): H7 av alle rader | 425/673 | 425/673 = 63,2 % [59,4–66,7] | **[56,7–73,7]** | 73 | — | 129 |
| fase 3-register (673): løftbar H1–H6 av avklarte | 101/628 | 101/628 = 16,1 % [13,4–19,2] | **[9,5–20,5]** | 72 | — | 126 |

## d) Felt: positiv rate blant silkandidatene (riktig navngitt) og silkandidatenes andel

| felt | tekstbiter | silkandidater | andel av tekstbitene | leser-positive | **positiv rate blant silkandidater** | per 1 000 tekstbiter |
|---|---|---|---|---|---|---|
| arkeologi | 6741 | 990 | 14,7 % | 274 | **27,7 %** [25,0–30,5] | 40,65 |
| energimodellering | 6432 | 1129 | 17,5 % | 68 | **6,0 %** [4,8–7,6] | 10,57 |
| klinisk_epidemiologi | 3487 | 347 | 10,0 % | 53 | **15,3 %** [11,9–19,4] | 15,2 |
| tekstvitenskap | 5583 | 378 | 6,8 % | 37 | **9,8 %** [7,2–13,2] | 6,63 |

Forholdet høyest/lavest er **4,6** blant silkandidatene (manuskriptets «4,6») og **6,13** per tekstbit. Ingen av dem er feltets prevalens: silens kandidatandel og sensitivitet per felt er ikke målt i første runde.

## e) Prevalensestimatoren bak 3,43 %

**Estimator:** T̂ = Σ_c N_c·k_c/n_c (flaggede, celle = felt × dømt klasse) + Σ_s N_s·k_s/n_s (ikke-flaggede: INGEN, N3) + k(N1)+k(N2) (lest i sin helhet); prevalens = T̂/N.

N = 22243; flagget av dommeren 2173. **Ikke-flaggede strata:**

| stratum | N | lest | positive (koder 1) |
|---|---|---|---|
| INGEN | 18395 | 50 | 1 |
| N1 | 37 | 37 | 0 |
| N2 | 13 | 13 | 0 |
| N3 | 1625 | 50 | 1 |

**Flaggede:** 42 celler (felt × dømt klasse), 150 lest, 25 positive; 14 celler med til sammen 26 flaggede tekstbiter har ingen leste rader og får feltets rate. Full celletabell i JSON-fila.

**Punkt:** T̂ = 759,9 (flaggede 359,5, ikke-flaggede 400,4) → **3,42 %**.

**Intervall:** stratifisert passasjebootstrap **[1,3–7,2] %**; verksklynget **[1,3–7,5] %**. Manuskriptets [2,12–7,95] er rekonstruert: (362 + 110)/22 243 og (362 + 1 405)/22 243: punktpresisjonen uvektet (25/150) pluss Wilson-grensene for en uvektet bomrate 2/100 — presisjonens usikkerhet og klyngene er ikke med.

**Vurdering:** estimatoren kan skrives ut entydig, med én antakelse (cellene uten leste rader). Punktet står (3,42 % mot 3,43 %); intervallet er feil i manuskriptet og byttes. Tallet hviler på 2 positive blant 100 leste ikke-flaggede, og flyttes fra «beste anslag» i sammendraget til en sekundær størrelse med dette intervallet.

## f) Duplikater: rader som deler setning med en annen rad i samme verk

| register | rader | rader som deler setning | **unike erklæringer** | komponenter > 1 rad | største | blandet klasse | H7 av unike | H1–H6 av avklarte unike |
|---|---|---|---|---|---|---|---|---|
| register v2 (432) | 432 | 269 | **276** | 113 | 6 | 19 | 183/257 = 71,2 % [65,4–76,4] | 42/245 = 17,1 % [12,9–22,4] |
| fase 3-register (673) | 673 | 443 | **424** | 194 | 6 | 22 | 265/402 = 65,9 % [61,2–70,4] | 53/375 = 14,1 % [11,0–18,0] |

Regel: rader i samme verk med overlappende setningsspenn slås sammen til én komponent (én erklæring); komponentens klasse er den hyppigste, og komponenter med delt flertall («blandet») holdes utenfor klasseandelene. Kjeden deduplikerer ikke i dag: tekstbitene har stride 3 og vindu ±2, og en erklæring kan dermed bære flere rader.

## Kilder

| fil (Vault) | sha256 |
|---|---|
| `presisjonssett/port-presisjonssett-ADDENDUM10.jsonl` | `6a04079c31fbbc60…` |
| `presisjonssett/port-presisjonssett-verdikter-koder2.jsonl` | `7852f86231347099…` |
| `koder4/koder4-fable51-verdikter.jsonl` | `36a3465acd195355…` |
| `ekstraksjon/2026-09-26/addendum-19/opus5-b-dommer.jsonl` | `296fdb78ab459aa3…` |
| `arbeidsliste/nokkel.jsonl` | `805ce5a2d8154bfa…` |
| `arbeidsliste/presisjon-100-verdikter.jsonl` | `667dffc4a075405b…` |
| `arbeidsliste/presisjon-rest-verdikter.jsonl` | `fcea39ce253be406…` |
| `fase3/presisjon/nokkel-presisjon.jsonl` | `d3b58f15cfb19803…` |
| `fase3/presisjon/verdikter-presisjon.jsonl` | `5eb347d23cc9b5a8…` |
| `fase3/maaling-fase3.json` | `441cff4f1d949cbc…` |
| `kandidat432/8-register.jsonl` | `c6895202b76199aa…` |
| `kandidat432/nokkel.jsonl` | `805ce5a2d8154bfa…` |
| `fase3-kjede/8-register.jsonl` | `b7d9230c93970c26…` |

---

*(Rettet 10.10.2026: tittelen sa «Reanalyse etter ekstern fagfellevurdering». Leseren var en språkmodell (GPT); ingen menneskelig fagfelle har lest manuskriptet. Generatoren er låst med sha256 i
ADDENDUM-28 og skriver fortsatt den gamle tittelen; kjøres den på nytt, må rettingen gjøres om. Merknaden står sist i
filen for at linjenumrene over skal stå.)*
