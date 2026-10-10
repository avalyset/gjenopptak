# ADDENDUM-27 — menneskelig validering av måleinstrumentet (preregistrert, ikke kjørt)

**Skrevet:** 2026-10-03, **før prøven er trukket og før noe menneske har lest den.** **Status: LÅST ved commit.**
**Gjelder:** ekstern fagfellevurdering 03.10.2026, hovedinnvending 1 (ingen menneskelig kriterievalidering) og spørsmål 1–2.
**Ingen Anthropic-API.** Ingen modell koder i denne målingen; modellenes etiketter finnes fra før og leses bare i analysen.

## 1 Hvorfor

Alle tall i sporet om treff, klasser, presisjon og recall er språkmodell mot språkmodell: koder 1, koder 2, koder 4,
referanselesningene i fase 3 og leseren. Enigheten måler stabilitet i ett modell- og instruksjonssystem, ikke om
systemet treffer det et menneske ville kalle en erklæring om ugjort arbeid med navngitt hindring. Dette addendumet låser
en måling som kan svare på det. **Fram til den er kjørt** brukes «reference-positive», «second-model agreement» og
«confirmation rate» i stedet for «true», «confirmed» og «precision/recall» der referansen er en modell.

## 2 Prøven, låst

Trekkes med `classify/menneskevalidering.py bygg` (sha256 i § 9), frø **734248**, `random.Random(frø).sample` over
populasjonens id-er sortert, per stratum. En passasje som havner i to strata, telles i det første. **Prøven trekkes etter
denne commiten**; blindfilens, nøkkelens og utvalgsfilas sha256 føres i `MANIFEST-VAULT.md` og i
`docs/RESULTAT-ADDENDUM-27.md` § 0 før noen annotatør får fila.

| stratum | kilde | populasjon | trekkes |
|---|---|---|---|
| **A1** | 320-settet (første runde, fire felt), flagget av dommeren, koder 1 positiv | 25 | alle 25 |
| **A2** | 320-settet, flagget, koder 1 negativ | 125 | 30 |
| **A3** | 320-settet, ikke flagget (INGEN, N3, N1/N2) | 150 | 30, **de to radene koder 1 kalte positive tas alltid med** |
| **B1** | fase 3 (arkeologi), leser positiv, `tvil: false` | 311 | 15 |
| **B2** | fase 3, leser positiv, `tvil: true` | 362 | 15 |
| **B3** | fase 3, leser negativ (unionen) | 3 434 | 15 |
| **B4** | fase 3, referansetreff som silen eller leseren mistet (`bekreftet: false`); passasjen er treffets setninger ±2 | 19 | alle 19 |

Ankrene i 320-settet (20) er utenfor prøven. **Ti av dem** (`random.Random(734248).sample` over ankrene sortert) er
øvingsoppgaver med fasit (§ 4). Passasjer som er tabellrester eller tall uten setninger, er med når de trekkes: de er en
del av populasjonen silen slipper gjennom. Tørrkjøring før låsen (ingenting skrevet): 149 passasjer fra 75 verk; arkeologi
103, energimodellering 21, tekstvitenskap 14, klinisk epidemiologi 11.

## 3 Annotatørene

**Minst to mennesker**, uavhengige av hverandre og av prosjektet, som leser engelsk faglitteratur. Helst én med humanistisk
og én med naturvitenskapelig eller medisinsk bakgrunn. De får **bare** blindfila (id og tekst), kodeboka
(`docs/KODEBOK-MENNESKER-v1.md`, sha256 i § 9) og skjemaet. De får ikke manuskriptet, repoet, nøkkelen, modellenes svar,
hverandres koder eller vite hvordan prøven er trukket. Rekrutteres av eieren; hvem føres i utfallet.

## 4 Prosedyre

1. Øving på ti ankre; fasit vises etter at alle ti er kodet. Kodeboka endres ikke etter øvingen.
2. Hver annotatør koder alle passasjene alene, i blindfilas rekkefølge, i skjemaet.
3. **Adjudikering:** der de to er uenige om `treff`, avgjør en **tredje person** — eller de to i fellesskap, om ingen
   tredje finnes — med tilgang til de to menneskelige kodingene og teksten, **aldri til modellenes svar**. Klasse
   adjudikeres bare for passasjer der den adjudikerte verdien er treff.
4. Skjemaene sikres med sha256 før analysen.

## 5 Analyseplan, låst

Alle intervaller: **verksklynget bootstrap**, 10 000 replikater, frø 734248, persentil. Enighet: rå enighet, Cohens κ,
PABAK og Gwets AC1, alltid sammen.

**Primær 1 — menneske mot menneske** på treffbeslutningen, over alle passasjer og per blokk (A, B).

**Primær 2 — modell mot adjudikert fasit**, per modell og stratum:

| spørsmål | strata | modell |
|---|---|---|
| andel modell-positive som er menneske-positive | A1 (koder 1); A1+A2 for koder 2, koder 4, Opus ett kall | etikettene i 320-settet |
| andel modell-negative blant flaggede som er menneske-positive | A2 | koder 1 |
| menneske-positiv rate blant ikke-flaggede, vektet med INGEN/N3/N1-N2-størrelsene | A3 | dommeren (silens bom) |
| andel leser-positive som er menneske-positive, vektet med populasjonene 311 og 362 | B1, B2 | fase 3-leseren |
| menneske-positiv rate blant leser-negative | B3 | fase 3-leseren |
| andel referansetreff som mennesker også kaller treff | B4 | referanselesningene |

Vektede anslag bruker inklusjonssannsynlighetene i `utvalg.json`. **Sekundært:** klasseenighet blant adjudikerte treff
(eksakt klasse, løftbar/ikke-løftbar, H7-andel).

**Tolkningen, låst nå:**

* **Menneske–menneske κ < 0,60** på treffbeslutningen → konstruksjonen er ikke stabilt operasjonalisert for mennesker.
  Klasse- og forekomstpåstander rapporteres da som **modelldefinerte**, og ordet «parkert spørsmål» brukes ikke om dem som
  et fenomen uavhengig av instrumentet.
* **Koder 2 mot adjudikert κ < 0,60** → «presisjon» og «recall» brukes ikke om modellreferansene i manuskriptet;
  «second-model agreement» står.
* Ingen andre terskler. Alle tall rapporteres uansett retning.

## 6 Hva denne målingen ikke er

Den måler instrumentet på 149 passasjer, de fleste fra arkeologi. Den estimerer ikke forekomst i litteraturen, og den
validerer ikke løftbarhetstabellen (PREREG § 5), som er en fastsatt tabell, ikke en måling.

## 7 Dødsbetingelser

* Prøven trekkes ikke om. Kodeboka endres ikke etter at første annotatør har startet.
* Ingen modell ser menneskenes koder før analysen er kjørt, og ingen modellkode brukes i adjudikeringen.
* Kjøres ikke før eieren har rekruttert annotatørene; dato for start føres i utfallet.

## 8 Status

**Preregistrert, ikke kjørt.** Ingen annotatør er rekruttert.

## 9 Filer låst med dette addendumet

Regnet på filene slik de står i commit `b8b2ea7`, commiten før låsen.

| fil | sha256 |
|---|---|
| `src/gjenopptak/classify/menneskevalidering.py` | `9ff992ffae555e92d79cc719cabcde8c63868496a706e07250be39c8bca6eece` |
| `docs/KODEBOK-MENNESKER-v1.md` | `e8c50b1c07a536eff137ff810041b4adad05400e93e7ed084ee2193093cdd5e5` |
| regelfil `koder2/koderegler-gjenvunnet.md` | `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449` |
