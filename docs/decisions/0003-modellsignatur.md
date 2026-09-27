# ADR-0003 — Modellsignatur loggføres per dømt setning

**Repo:** gjenopptak
**Status:** Accepted
**Dato:** 2026-09-12

## Kontekst

Klassifiseringen bruker en lokal språkmodell i minst ett ledd. Lokale modeller er ikke stabile
mellom kjøringer: vekter byttes bak samme tag, kvantisering endres, standardparametre flyttes,
og kontekst kan lekke mellom forespørsler når modellen holdes varm i minne. En kjøring som ikke
bærer med seg hvilken modell som svarte, er ikke reproduserbar og kan ikke sammenlignes med en
senere kjøring.

PREREG-v1 §6 fester en terskel på lokal modells enighet med eiers koding (< 70 % ⇒ arkitektur B),
og §7 krever at dommer oppgis per oppføring. Begge kravene forutsetter at det er kjent hvem som
dømte, per setning, ikke per kjøring.

## Beslutning

For **hver dømt setning** loggføres en modellsignatur i oppføringen:

| Felt | Innhold |
|---|---|
| `model_id` | modell-ID med tag, slik den ble bedt om, og oppløst digest |
| `weights_sha256` | sha256 av vektfilen(e) som faktisk ble lastet |
| `temperature` | temperatur, eksplisitt satt, aldri arvet fra en standardverdi |
| `seed` | frø sendt til modellen |
| `keep_alive` | settes til `0` og loggføres |
| `runtime` | kjøretid og versjon (f.eks. llama.cpp/ollama-versjon), quantisering |
| `prompt_sha256` | sha256 av den faktiske ledeteksten, etter all interpolering |
| `judged_at` | tidspunkt, ISO |

`keep_alive=0` er et krav, ikke en innstilling: modellen lastes ut mellom forespørsler, slik at
ingen setning kan dømmes i skyggen av en tidligere. Dommeridentiteten (`judge`: `owner`,
`local:<model_id>`, `external:<model_id>`) står i samme oppføring.

Mangler ett av feltene, er oppføringen ugyldig og telles ikke. Kjeden skal feile på manglende
signatur, ikke fylle inn en antakelse.

## Konsekvens

- Enighetstallet i §6 kan knyttes til én bestemt modelltilstand. Byttes modellen, må tallet
  måles på nytt; det gamle tallet forblir gyldig for den gamle signaturen.
- Kjøringer blir tregere fordi modellen lastes ut mellom setninger. Det er akseptert; alternativet
  er dommer med ukjent minnetilstand.
- Signaturen gjør det mulig å skille to forklaringer på endrede tall: endret korpus eller endret
  dommer. Uten den kan de ikke skilles.
- Loggen inneholder ledetekst-hash, ikke ledeteksten, i den enkelte oppføringen. Ledetekstene
  versjoneres i repoet slik at hashen kan slås opp.
