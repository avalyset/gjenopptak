# ADDENDUM-24 — lokal agentisk leser: regelfil og parti i samme kontekst

**Skrevet:** 2026-09-28, **før kjøring.** **Status: LÅST ved commit, før kanarien er kjørt.**
**Gjelder:** ADR-0012 («ett-kall-modeller er sil-klasse») og leserleddet i kjeden. **Ingen Anthropic-API.**

## 1 Hvorfor

Lokale modeller er bare målt i **ett kall per tekstbit** uten reglene: den lokale gemma2-dommeren fikk
κ = 0,289 mot en blind leser (ADDENDUM-18, linje 114). De to leserne som er dokumentert over 0,70 mot
koder 1, leste **reglene og mange tekstbiter i samme kontekst**: koder 2, en agentisk Opus-instans,
κ = 0,812 (ADDENDUM-11), og koder 4, Fable 5.1 i chat, κ = 0,781 (`docs/METODE.md`, «Koder 4», commit
`dfccd02`, 28.09.2026). Oppdraget til dette addendumet sa at bare den første finnes; den andre ble
committet samme morgen, og står her fordi den er en andre forekomst av samme modus.

ADDENDUM-19b målte Opus 5 i ett kall per tekstbit, med regelutdraget, til κ = 0,636 [0,478–0,768] mot
koder 1, og konkluderte at modellen bærer det meste og at en resteffekt av øktformen er **mulig og
umålt**. Ingen lokal modell er målt i agentisk modus.

**Hypotese:** modusen — regelfil og et parti tekstbiter i samme kontekst — forklarer en del av gapet
mellom lokale modeller og de agentiske leserne.

**Hva målingen kan og ikke kan si.** Den gir κ for én lokal modell i én modus. Et utfall under 0,70
skiller ikke «modusen hjelper ikke» fra «modellen er for svak»; det ville kreve samme modell i
ett-kall-modus med regelfilen, som ikke kjøres her. Et utfall over 0,70 viser at en lokal leser i denne
modusen når terskelen på denne blindfilen — ikke at modusen er årsaken.

## 2 Oppsettet, låst

| | verdi |
|---|---|
| modell | **`qwen2.5:7b`** (ollama), Q4_K_M, 7,6 B parametre, kontekst 32 768 |
| vekt | blob sha256 **`2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730`**, verifisert før og etter kjøring |
| instruks | `prompts/leser-lokal-v1.txt` (sha256 `6dc74bbc…`, §7) — koder 2s metodeavsnitt (ADDENDUM-11 §2, oppdraget ordrett i `oppdrag-gjenvunnet/oppdrag-koder2-ADDENDUM-11.md` på Vault), oversatt til norsk; ingen treffrate, ingen eksempler |
| regelfil | `koder2/koderegler-gjenvunnet.md` på Vault, 9 805 B, sha256 **`234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449`**, defektene intakte |
| materiale | portens blindfil `data/port-presisjonssett-blind.jsonl`, 320 rader, sha256 **`15ce72a7687cea57ac1e7f774aa0303f0bedfc3c2867244d24173a1ec211d4a5`** |
| partier | **16 à 20**, i blindfilens rekkefølge (PS-001–020, 021–040, …) |
| kontekst per kall | systemmelding = instruks + regelfil; brukermelding = partiet med id som overskrift |
| utdata | JSON-skjema tvunget av ollama (`kjede/leser.py`, `SKJEMA`): `id`, `ekte_treff`, `min_klasse`, `min_bedømbar`, `tvil`, `begrunnelse` — koder 2s felter |
| klasseverdier | H1–H9, `H1/H7-uavklart`, N1–N3, INGEN — de verdiene regelfilen navngir, som for koder c |
| `num_ctx` | 32 768 |
| `num_predict` | 8 192, og `done_reason` føres per parti (LAERDOM § 34) |
| temperatur, frø | 0, **734248** |
| kode | `src/gjenopptak/kjede/leser.py` (`Leser`, `LokalLeser`, `CCLeser`), `src/gjenopptak/classify/leser_port.py` |

**Valget av modell.** Kravet var kontekst ≥ 32k. Av de installerte modellene har `qwen2.5:7b` (32 768) og
`llama3.1:8b` (131 072) det; `gemma2:9b` har 8 192 og faller. `qwen2.5:7b` er valgt fordi dens vekter og
32k-cache får plass i 16 GB samlet minne med margin (≈ 4,7 GB vekter), der `llama3.1:8b-instruct-q8_0`
med 32k-cache ville ligget nær taket. Valget er gjort **før** noen modell er prøvd på materialet, og
ingen annen modell kjøres under dette addendumet.

**Sperreliste trengs ikke, og det er ikke et avvik.** Den lokale leseren har ingen filtilgang og ingen
verktøy; den ser nøyaktig systemmeldingen og partiet. Sperrelisten til koder 2 og koder c fantes fordi
de kunne åpne filer.

## 3 Kanari, før kjøring

Det største partiet (flest tegn) sendes med én ekstra tekstbit sist, id `KANARI`, tekst «We could not
date the layer, because no suitable sample was preserved.» (kjedens kanarisetning, `kjede.toml`).
**Bestått** krever alle fire: `prompt_eval_count` < `num_ctx`, `done_reason` ≠ `length`, svaret parser,
og `KANARI` har en gyldig dom. Kanariens **klasse** kreves ikke — det ville målt leserens kvalitet, ikke
om konteksten nådde fram. Faller kanarien: **STOPP**, ingen kjøring, rapporter. Kanariens dommer over
de ekte tekstbitene brukes ikke i målingen.

## 4 Kriteriet, låst

**Cohens κ på treffbeslutningen (`ekte_treff`) mot koder 1 over alle 320**, der koder 1 er
`data/port-presisjonssett-ADDENDUM10.jsonl` (samme kilde som gir κ = 0,812 mellom koder 1 og 2).

* **κ ≥ 0,70 → lokal agentisk leser er godkjent leser.**
* **κ < 0,70 → sil-klasse**, ført som det i METODE, kjede.toml og LAERDOM.

**Ugyldige dommer teller i verste fall.** En tekstbit uten gyldig dom — parsefeil, avkuttet utdata,
manglende eller dublert id — settes til **motsatt av koder 1** i kriteriet. Ingenting fylles ut og
ingenting kjøres om: temperatur 0 og fast frø gir samme svar på samme inndata. κ over de gyldige alene
rapporteres ved siden av, men avgjør ikke.

**En dom der `ekte_treff` og klassen spriker** (treff med N/INGEN, eller ikke-treff med H-klasse) føres
som inkonsistent. `ekte_treff` er det som telles, som for koder 1 og 2.

## 5 Rapporteres i tillegg, uten terskel

κ mot koder 2 og mot koder 4 over 320 (samme verste-fall-regel), bootstrap-intervall (paret, 10 000,
frø 734248, `reliabilitet.kappa_bootstrap`), rå enighet, antall treff, klassefordeling, antall ugyldige og
inkonsistente, veggtid, tokens inn og ut per parti og samlet (`prompt_eval_count`, `eval_count`).

## 6 Dødsbetingelser

* **Ingen ny instruks, modell eller partistørrelse etter at første parti er kjørt.** Faller kriteriet, er
  det utfallet. Et nytt forsøk krever et nytt addendum med ny sha.
* **Ingen omkjøring av enkeltpartier.** Et avbrudd gjenopptas fra første manglende parti; ferdige partier
  røres ikke.
* **Vekten verifiseres før og etter.** Avvik etter kjøring gjør målingen ugyldig.
* **Utdata til Vault** (`leser-lokal-ADDENDUM-24/`), med sha i manifestet.

## 7 Filer låst med dette addendumet

Regnet på filene slik de står i commit `f38bd74`, commiten før låsen.

| fil | sha256 |
|---|---|
| `prompts/leser-lokal-v1.txt` | `6dc74bbca307a24186b49b257210df58e06c19e9e9b6e70d8c437111d02a6137` |
| `src/gjenopptak/kjede/leser.py` | `957310f746b7a9a0f8effc561fa592f2d2b2d744c2c7aa8ad5f9e300d9113a6d` |
| `src/gjenopptak/classify/leser_port.py` | `5f04b0e1724a50c62e64b494dfc8a5fd32d6e8c81a485f8a8f2b9c98f458323f` |
| vekt `qwen2.5:7b` (ollama-blob) | `2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730` |
| regelfil `koder2/koderegler-gjenvunnet.md` | `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449` |
| blindfil `data/port-presisjonssett-blind.jsonl` | `15ce72a7687cea57ac1e7f774aa0303f0bedfc3c2867244d24173a1ec211d4a5` |
| koder 1 `data/port-presisjonssett-ADDENDUM10.jsonl` (lik Vault-kopien i `presisjonssett/`) | `6a04079c31fbbc60a8a189232a7ef37f55756ce18c74545d10bf062fcea70c36` |

`leser_port.py` verifiserer vekt, regelfil og blindfil på sha256 før kanarien og før kjøringen, og stopper
ved avvik.
