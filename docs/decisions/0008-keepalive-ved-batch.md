# ADR-0008 — keep_alive under batch-dømming

**Repo:** gjenopptak
**Status:** Accepted
**Dato:** 2026-09-16

## Kontekst

ADR-0003 krever `keep_alive=0` per dom: modellen lastes ut mellom forespørslene, slik at ingen
setning kan dømmes i skyggen av en tidligere. Kravet ble skrevet for POC-en, der hver dom skulle
være uavhengig og antallet dommer var lite (110).

Porten dømmer hele teksten i de 100 trukne verkene: **22 243 passasjer**. Med `keep_alive=0` er
takten målt til **11,6 sekunder per passasje** (median over 47 dommer), altså om lag **64 timer**.

Målingen viser samtidig at lasting ikke er hovedkostnaden: **median `load_duration` er 1,5 s av
11,6 s**. Resten går med til prefill av ledeteksten på om lag 1 400 tokens, og den ledeteksten er
identisk for hver passasje. En modell som blir stående lastet, kan gjenbruke den prefiksen fra
hurtigbufferet. Det er der gevinsten ligger, ikke i spart lasting.

## Beslutning

**Ved batch-dømming med én modell over ett frosset materiale kan modellen holdes lastet**
(`keep_alive ≠ 0`).

Betingelsene:

1. **Signaturkravet er uendret.** `model_id`, `weights_sha256`, `temperature`, `seed`, `keep_alive`,
   `runtime`, `prompt_sha256` og `judged_at` føres per dom. Signaturen merkes i tillegg `batch: true`.
2. **Vektfilen verifiseres før og etter kjøringen**, ikke bare før. Begge sha256-verdiene føres.
3. **Temperatur 0 og fast frø som før.**
4. **Determinismen verifiseres før batchen starter:** de alt dømte passasjene kjøres på nytt med
   lastet modell, og utfallet må være identisk — råsvaret, ikke bare klassen. **Avviker én eneste,
   rulles denne beslutningen tilbake for kjøringen, og dømmingen fortsetter med `keep_alive=0`.**
5. **Sjekken gjentas etter kjøringen** på et frøtrukket utsnitt av de batch-dømte passasjene, med
   `keep_alive=0`. Avvik der ruller beslutningen tilbake på samme måte.
6. Sjekken kjøres på nytt ved bytte av modell, ledetekst eller kjøretid.

## Målingen som utløste beslutningen (2026-09-16)

| | |
|---|---|
| passasjer dømt med `keep_alive=0` før sjekken | 47 |
| identiske råsvar ved ny dom med lastet modell | **47 av 47** |
| identiske klasser | 47 av 47 |
| vektfil før og etter | uendret, `ff1d1fc7…0373` |
| takt med `keep_alive=0` | 11,6 s per passasje |
| takt med lastet modell | **3,96 s per passasje** |
| gjenstående tid for porten | fra om lag 64 til om lag 24 timer |

## Konsekvens

* ADR-0003 står for enkeltdommer, for POC-er og for alt materiale som ikke er frosset. Denne
  beslutningen gjelder bare batch over ett frosset materiale med én modell.
* `classify/judge.py` godtar `keep_alive ≠ 0` bare når signaturen er merket `batch: true`, og avviser
  `batch: true` sammen med `keep_alive = 0`. Begge retninger er testet.
* Risikoen ADR-0003 pekte på — at en dom farges av den forrige — er ikke borte i prinsippet. Den er
  målt på dette materialet og ga null avvik på 47 dommer. Derfor punkt 4, 5 og 6: målingen er kravet,
  ikke antakelsen.
* Tallene i en batch-kjøring er knyttet til signaturen sin som før. Byttes modellen, må de måles på nytt.
