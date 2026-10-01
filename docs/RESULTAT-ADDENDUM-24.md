# Utfall av ADDENDUM-24 — lokal agentisk leser: sil-klasse

**28.09.2026.** Kjørt etter låsen i `c0ec731`, uten avvik fra oppsettet. Utdata på Vault
`leser-lokal-ADDENDUM-24/` (kanari, 16 partier med råsvar og bruk, `maaling.json`), sha256 i
`MANIFEST-VAULT.md`.

## Kriteriet: FALT

**κ = 0,248 [0,113–0,376] mot koder 1 over alle 320** (terskel 0,70). `qwen2.5:7b` i agentisk modus —
regelfil og 20 tekstbiter i samme kontekst — er **sil-klasse**, ikke godkjent leser.

| | koder 1 treff | koder 1 ikke treff |
|---|---|---|
| **lokal treff** | 18 | 43 |
| **lokal ikke treff** | 21 | 238 |

Rå enighet 0,800. Den lokale leseren kalte 61 treff mot koder 1s 39, fant 18 av dem og mistet 21.

## Tilleggstall (uten terskel)

| mot | κ | bootstrap 95 % | rå enighet |
|---|---|---|---|
| koder 1 | **0,248** | 0,113–0,376 | 0,800 |
| koder 2 | 0,239 | 0,104–0,368 | 0,806 |
| koder 4 | 0,239 | 0,106–0,368 | 0,806 |

* **Gyldighet:** 320 av 320 gyldige dommer, 0 ugyldige, 0 inkonsistente, `done_reason: stop` i alle 16
  partier. Verste-fall-regelen i § 4 slo derfor ikke inn; κ over gyldige alene er det samme tallet.
* **Kanari:** bestått, 8 128 tokens inn av 32 768 (25 %), alle 21 dommer gyldige.
* **Klasser:** N1 96 · N2 89 · N3 74 · H7 49 · H5 5 · H9 5 · H1 2 · **INGEN 0**. Leseren brukte aldri
  `INGEN`, som er den vanligste klassen hos alle tre kodere (213–265 av 320); den fordelte ikke-treffene på
  N1–N3 i stedet. Det påvirker ikke κ på treff, men viser at klassegrensene i regelfilen ikke ble lest
  som koderne leste dem.
* **Kostnad:** veggtid 30,9 min (1 849 s modelltid, ≈ 116 s per parti), 122 970 tokens inn, 26 069 ut,
  lokalt, null kroner.

## Hva utfallet sier, og ikke sier

κ = 0,248 er i samme område som gemma2:9b i ett kall (0,289, ADDENDUM-18) — men det er en annen modell,
et annet materiale (100 blindede tekstbiter fra 2d, `ekstraksjon/2026-09-26/d1-2x2.json`, ikke de 320) og
en annen referanse (en blind leser, ikke koder 1). **Modusens bidrag er ikke målt for `qwen2.5:7b`**, som
aldri er kjørt i ett-kall-modus. Som ADDENDUM-24 § 1 sa før kjøring: utfallet skiller ikke «modusen hjelper
ikke» fra «modellen er for svak». Hypotesen er verken bekreftet eller forkastet for modeller i Opus- og
Fable-klassen; den er forkastet for **`qwen2.5:7b` i denne modusen**. `llama3.1:8b` (131k kontekst,
ADDENDUM-24 § 2) er installert og ikke prøvd.

*(Rettet 28.09.2026, frys-lesning 2: avsnittet sto «ligger på høyde med gemma2:9b i ett-kall-modus …,
altså ingen målbar gevinst av modusen for en 7B-modell» og «forkastet som vei til en godkjent lokal leser
på denne maskinen i dag». Sammenligningen krysser modell, materiale og referanse, og slutningen
generaliserte fra én av to installerte modeller med ≥ 32k kontekst. Kriteriet og klassen står.)*

**Ført:** METODE (leserklassene), LAERDOM § 42. `kjede.toml` og `kjede/leser.py` er ikke endret, fordi
ADDENDUM-25 låser deres sha256; `LokalLeser` står i koden som implementasjon av `Leser`, klassifisert som
sil-klasse her og i METODE.
