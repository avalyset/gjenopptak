# ADDENDUM-14 — embeddings som førsteledd, og hvorfor det ikke ble et førsteledd

**Skrevet:** 2026-09-26. **Gjelder:** PREREG-v1 §8 og L2-rørledningen.
**Utfall: negativt.** Semantisk likhet mot kjente treff rangerer ikke parkerte spørsmål høyt nok til
å brukes som billig førsteledd. Det finnes signal — AUC 0,71–0,75 mot 0,50 for tilfeldig — men halen
er dødelig: for å beholde 90 % av treffene må dommeren se **62–72 %** av materialet.

## 1 Hvorfor spørsmålet ble stilt

Markørlisten er forkastet: 25,9 % recall på uavhengig materiale (ADDENDUM-07 §2). Uten et billig
førsteledd må dommeren se alt, og dommeren bruker **3,8 s per passasje** — 22 243 passasjer er
**23,5 timer** for 100 verk. Et rammesveip er titusener av timer. Spørsmålet er derfor ikke om
embeddings er interessante, men om de kan kutte materialet uten å miste treffene.

## 2 Modellvalg, med signatur

**Valgt: `bge-m3`, fordi materialet ikke er engelsk.** Stoppordtelling over alle 22 243 passasjer:
**52,9 % engelsk, 13,1 % fransk, 12,0 % spansk, 2,7 % tysk**, 17,9 % for korte å avgjøre.
**27,7 % er klart et annet språk enn engelsk**, og tekstvitenskap er dominert av fransk og spansk.
`nomic-embed-text` er enspråklig og ville vært blind på over en fjerdedel av materialet — samme
feilform som de engelskspråklige bildetekstene i ADDENDUM-13 §5.

| | |
|---|---|
| modell | `bge-m3` via ollama |
| familie · parametre · kvantisering | bert · 566,70 M · F16 |
| **vekt-sha256 før kjøring** | `daec91ffb5dd0c27411bd71f29932917c49cf529a641d0168496c3a501e3062c` |
| **vekt-sha256 etter kjøring** | samme — **uendret** (ADR-0008) |
| dimensjon | 1024 |
| `truncate` | **false** — avkorting ville feilet kallet, ikke skjult seg |

## 3 Kjøringen

**Frøsettet:** de 55 ekte treffene fra recall-sett 1 (28) og 2 (27), som alt har manuell fasit.
**Alle 55 lot seg embedde uten avkorting**, på 3,8 s.

**Portmaterialet:** alle **22 243** passasjer, **én kjøring**, **16,5 minutter**, **22,5 passasjer/s**,
**0 feilede**. Batch 32. Diskvakt sjekket underveis, 261 GB ledig ved start. Utdata til Vault etter
ADR-0009: `embeddings/port-bge-m3.npy` (45,5 MB, float16), `froesett-bge-m3.npy`, `port-index.json`,
`kjoring.json`.

At embedding av alt tar **16,5 minutter** mot dommerens **23,5 timer** er forholdstallet som gjorde
forsøket verdt å gjøre: førsteleddet koster 1,2 % av det det skal spare.

## 4 To varianter, rapportert som to målinger

Ingen tuning mot fasiten. To aggregeringer av frøsettet, begge på samme embeddinger:

* **A — maks cosinus mot enkeltfrø:** høyeste likhet mot noen av de 55.
* **B — cosinus mot frøsentroiden:** likhet mot gjennomsnittsvektoren.

**Evalueringssettet er de 25 ekte treffene i treff-stratumet** i presisjonssettet. **De 12
anker-treffene er utelatt: de *er* frøsettets egne passasjer**, og ville rangert på topp ved
konstruksjon. Frøsettets 23 dokumenter og portens 100 verk er **disjunkte** — 0 overlapp, kontrollert.

| kuttpunkt | A: treff av 25 | B: treff av 25 |
|---|---|---|
| **topp 1 %** (222 passasjer) | **2 = 8,0 %** | **1 = 4,0 %** |
| **topp 5 %** (1 112) | **5 = 20,0 %** | **8 = 32,0 %** |
| **topp 10 %** (2 224) | **7 = 28,0 %** | **12 = 48,0 %** |
| topp 20 % (4 449) | 10 = 40,0 % | 14 = 56,0 % |
| topp 50 % (11 122) | 20 = 80,0 % | 21 = 84,0 % |
| median persentil | 23,7 % | **11,8 %** |
| verste treff | 81,6 % | 85,7 % |
| **AUC** | **0,711** | **0,750** |

**B er bedre enn A på alle kuttpunkter over 1 %,** og forskjellen er én aggregeringsvalg, ikke en
forbedring av metoden. Begge står som separate målinger.

## 5 Sammenligning mot markørlisten, på samme materiale og samme treff

Markørlisten er et binært filter og har bare ett driftspunkt:

| filter | kandidatmengde | fanget av de 25 |
|---|---|---|
| markørliste **v1** | 53 = 0,2 % | **1 = 4,0 %** |
| markørliste **v2** (utvidet, ADDENDUM-06) | **230 = 1,0 %** | **2 = 8,0 %** |
| embeddings **A** ved samme mengde (230) | 230 | **2 = 8,0 %** |
| embeddings **B** ved samme mengde (230) | 230 | 1 = 4,0 % |

**Ved markørlistens eget driftspunkt er embeddingene ikke bedre.** Forskjellen er at embeddingene har
en skrue: markørlisten kan ikke skaleres til 5 eller 10 % kandidatmengde i det hele tatt, mens B ved
10 % mengde når **48 %** recall — et nivå markørlisten aldri når ved noen mengde. Begge er likevel
langt under det en måling krever.

## 6 Kostnaden ved de recall-nivåene som betyr noe

Dommeren: 3,8 s per passasje. Hele materialet: 22 243 passasjer = **23,5 timer**.

| ønsket recall | variant A: passasjer (andel) | faktor | timer | variant B | faktor | timer |
|---|---|---|---|---|---|---|
| 30 % | 2 598 (11,7 %) | 8,6× | 2,7 t | 1 042 (4,7 %) | 21,4× | 1,1 t |
| 50 % | 5 264 (23,7 %) | 4,2× | 5,6 t | 2 630 (11,8 %) | 8,5× | 2,8 t |
| **90 %** | **13 842 (62,2 %)** | **1,6×** | **14,6 t** | **16 051 (72,2 %)** | **1,4×** | **16,9 t** |

**Ved 90 % recall er det ikke noe førsteledd.** Man sparer 7–9 timer av 23,5, og prisen er at én av
ti treff er borte før dommeren har sett dem. For et rammesveip — der hele poenget var å slippe å se
alt — er en faktor på 1,4–1,6 uten verdi.

## 7 Hvorfor det feiler, så langt materialet rekker

Embeddinger måler **tema**, og de 55 frøene deler ikke tema: de kommer fra fire urelaterte felt.
Sentroiden av fire fagfelt er nær ingenting, og maks-mot-enkeltfrø domineres av hvilket frø som
tilfeldigvis deler felt med passasjen. **Det parkerte spørsmålet er en retorisk funksjon — «dette ble
ikke gjort, fordi X» — ikke et emne.** Funksjonen er spredt over hele det semantiske rommet, og et
mål bygget på emnelikhet kan ikke samle den. Dette er en forklaring som passer tallene, ikke en
måling: den ville krevd et forsøk der frøsettet holdes innenfor ett felt.

## 8 Hva målingen ikke viser

* **Den viser ikke at embeddinger er ubrukelige til noe annet.** AUC 0,75 er reelt signal. Det er for
  svakt til å kutte på, ikke for svakt til å rangere innenfor en alt filtrert mengde.
* **Den er ikke sirkulær i materialet, men den er ikke uavhengig av koderen.** Frøsettets 23
  dokumenter og portens 100 verk er disjunkte, og anker-treffene er utelatt. Men begge sett er markert
  av samme leser mot samme regelverk, så et uavhengig annotørsett ville målt noe annet.
* **25 treff er få.** Ett treff er fire prosentpoeng. Ingen intervaller er oppgitt, og ingen bør leses
  inn i tallene.
* **Den prøvde ikke feltvise frø, andre likhetsmål enn cosinus, eller finjustering på fasiten.** Det
  siste ville vært tuning mot evalueringssettet og er utelatt med hensikt.
