# Feltguide — legge til et felt, og lese tallene det gir

Et felt er en fil. Denne guiden er alt som trengs for å legge til ett, kjøre det, og vite hva tallene
betyr — og hva de ikke betyr — for nettopp det feltet.

## 1 Legg til feltet

Lag `felt/<navn>.yaml`. Fem nøkler, ingen kode:

```yaml
felt: arkivvitenskap
topics: [T11657]                 # OpenAlex topic-ID-er, fra SPØRRINGEN
ar: [2015, 2020]
ar_spurt: [2015, 2020]

ramme:
  fil: frames/frame-arkivvitenskap-RAW.jsonl   # relativ til Vault-målet
  sha256: 0000…                                # nuller til rammen er frosset
  rader: 149061
  krav: hentbar

terskler:
  n_verk: 25                     # hvor mange verk som skal trekkes
  gulv: 0                        # måleskranke i treffstratumet, ikke en vekting
```

Så:

```bash
gjenopptak run --felt arkivvitenskap --navn min-kjoring --torr
```

Tørrkjøringen sier hva feltet koster før noe hentes. Den svarer også om feltet er **kjørbart** eller
bare **planleggbart**: uten en frosset ramme er det det siste.

### Hvor emne-ID-ene kommer fra

**Fra spørringen, ikke fra verkene.** Verkenes egne `primary_topic_id` er spørringens *resultat* —
hundrevis per felt — og kan ikke definere feltet. Finn dem i OpenAlex' emnesøk, og skriv dem ned med
navn i en kommentar, slik at en leser kan se hva feltet var ment å være:

```bash
curl -s 'https://api.openalex.org/topics?search=archives+management&per-page=5' \
  | python3 -c 'import json,sys; [print(t["id"].rsplit("/",1)[-1], t["works_count"], t["display_name"]) for t in json.load(sys.stdin)["results"]]'
```

De fire eksisterende feltene bruker: arkeologi `T10087 T10421` · energimodellering
`T10424 T11185 T11941` · klinisk epidemiologi `T10556 T11095` · tekstvitenskap
`T10165 T10595 T14210`.

### `gulv` — les dette før du setter det

`gulv` er et **minsteantall** verk fra feltet i treffstratumet når presisjonssettet trekkes. Det er en
**måleskranke, ikke en vekting**. Tekstvitenskap har `gulv: 25`, og konsekvensen er målt: proporsjonal
trekking ville gitt feltet om lag 12 av de 150 leste treffene, ikke 25 (179 av 2 173 flaggede,
`ekstraksjon/2026-09-26/b2-nevner.json`; 5 ved delkjøringen i LAERDOM § 15, etter 18 964 av 22 243
dømte). Presisjonen blir dermed **utvalgets**,
ikke materialets. Vektet mot feltfordelingen er forskjellen liten (16,69 % mot 16,67 %), men den skal
oppgis. **Sett `gulv: 0` med mindre du har en grunn du kan skrive ned.**

## 2 Hva som kan gå galt

| symptom | hva det er | hva du gjør |
|---|---|---|
| `finner ingen feltfil felt/x.yaml` | feltnavnet i filnavnet og i `felt:` må være like | rett filnavnet, eller nøkkelen |
| `ramme: avvik — sha256 … ≠ …` | rammelisten har flyttet seg siden feltfilen ble skrevet | **ikke** oppdater sha-en for å bli kvitt meldingen. Finn ut hvorfor listen endret seg først |
| `ramme: mangler` | rammen er ikke frosset | feltet er planleggbart. `--torr` koster ut frysingen |
| `kvoteport les: NEKTER … harness-kvoten er ukjent` | leserkvoten kan ikke leses av kode | `gjenopptak kvote --skriv-harness <prosent>` fra Claude Codes bruksvisning |
| `kanari: prompt_eval_count ≥ num_ctx` | vinduet avkuttes stille | senk `vindu_tegn`, eller hev `num_ctx` — **ikke** hopp over kanarien |
| `kanari: dommeren svarte 'UGYLDIG'` | dommeren fikk noe den ikke kan svare på | sjekk at `ledetekst`-sha stemmer; dommerens enhet er **én** tekstbit, ikke et vindu |
| `leserøkt …: claude-CLI-en kunne ikke autentisere` | `claude -p` mangler innlogging | `claude auth login` én gang, så `--from les` |
| `cachen mangler N av M passasjer` | leser-cachen dekker ikke materialet | kjør uten `--cache-leser`. Kjeden **fyller ikke hull** |
| `tekstbitene dekker ikke alle N setningene` | parseren tapte setninger | et reelt datafunn, ikke en konfigurasjonsfeil. JATS-parseren tapte 39 519 setninger én gang |
| `[api] står i kjede.toml` | noen har prøvd å slå på API-stien | den finnes ikke (ADR-0012, datert tillegg). Fjern seksjonen |

**Én ting som ikke er en feil:** `port: ubekreftet kandidatliste` i registerhodet. Det betyr at lista
ikke har bestått noen port, og det er den ærlige tilstanden til en liste som ikke er testet.

## 3 Hva tallene betyr for feltet

### Treffraten varierer med en faktor 4,6 mellom felt

Målt over 2 844 dømte passasjer i de fire eksisterende feltene (ADDENDUM-22 §10):

| felt | treff / dømt | rate | Wilson 95 % |
|---|---|---|---|
| arkeologi | 274 / 990 | **27,7 %** | 25,0–30,5 |
| klinisk epidemiologi | 53 / 347 | 15,3 % | 11,9–19,4 |
| tekstvitenskap | 37 / 378 | 9,8 % | 7,2–13,2 |
| energimodellering | 68 / 1 129 | **6,0 %** | 4,8–7,6 |

**Forvent ikke at ditt felt ligner noen av dem.** Spredningen er ikke støy: intervallene for arkeologi
og energimodellering overlapper ikke i nærheten av hverandre.

### Hindringsklassene varierer også

Andelen **H7** — «dataene fantes ikke», som er **ikke-løftbar** — gikk fra 46 % i energimodellering til
96 % i klinisk epidemiologi i delkjøringen (374 treff, ADDENDUM-22 § 9.3); per felt for den fullførte kjøringen
er ikke regnet. *(Merket 30.09.2026, frys-lesning 4.)* Et felt der nesten alt er H7, gir en lang kandidatliste og nesten ingen
løftbare kandidater. Samlet er **19,0 %** [15,4–23,1] av de avklarte treffene i løftbar klasse H1–H6 (77 av 406), og
6,0 % av alle treff er uavklarte (26 av 432; ADDENDUM-05 § 4).

**Det er den viktigste forventningen å justere:** et felt med mange treff er ikke et felt med mange
muligheter.

### Grunnraten skal ikke leses som prevalens

Tre tall, samme materiale (METODE § 1): ett treff per **890** tekstbiter måler *utvalget* og skal ikke
brukes; ett per **61** er et **gulv**; ett per **29** er beste anslag, korrigert for tapte. Bruk det
siste, med intervallet, og si hvilket du bruker.

### Hva som følger hver rad

Hver kandidatrad bærer sin egen usikkerhet: silleddets **målte** presisjon med intervall, leserens
`tvil`-flagg med presisjonen målt for den verdien (post hoc, ADDENDUM-23 § 7.2: 41/42 = 97,6 %
[87,7–99,6] mot 44/58 = 75,9 % [63,5–85,0], målt i de fire eksisterende feltene), verksnivåets materialtilgang
og **hva den ikke ser**, falsifiseringens dekningsgrad eller `"ikke målt"`, og løftbarhet **med dato**.
Se [`UTGANG.md`](UTGANG.md) for én rad forklart felt for felt. *(Rettet 28.09.2026: `tvil`-tallene sto uten
intervall og uten «post hoc».)*

### Det feltguiden ikke kan love

Presisjonen per **klasse** er ikke målt — bare per silledd. Recall for et nytt felt er ikke målt i det
hele tatt: de 27 kjente treffene ligger i de fire eksisterende feltene, og en ny ramme har ingen fasit
før noen leser blindt i den. **Et nytt felt gir en kandidatliste, ikke en målt liste**, til det er gjort.
*(Tillegg 30.09.2026: fase 3 (ADDENDUM-25) viser hvordan det gjøres — et referansesett lest og sikret før
silen, og to porter låst før trekkingen. For arkeologi er recall og presisjon nå målt prospektivt
(`docs/RESULTAT-ADDENDUM-25.md` § 1); for de tre andre feltene og for nye felt gjelder avsnittet over.)*
