# Sakregister — fase 2d, status per sak

**Datert vurdering (ADR-0010).** Oppdatert **28.09.2026** (sjette oppdatering: L5-sjekkene kjørt; hele oppdrag R er ferdig). Én rad per sak, der en sak er
**verk × hindring**. Grunnlag: [`../SAKBEHANDLING-2026-09-27-triage.md`](../SAKBEHANDLING-2026-09-27-triage.md).
Statusen gjelder den datoen den bærer, ikke saken for all tid: Heron gikk fra H1 til H8 uten at
teksten endret seg.

| sak | verk | klasse | passasjer | status 27.09.2026 | kriterium låst | resultat |
|---|---|---|---|---|---|---|
| **SAK-14** | Haouachi 2016 `W2474595476` | H3 språk | AL-0738, AL-2370 | **ikke opphevet** — 87,8 % mot terskel 90 % | [`SAK-14/KRITERIUM.md`](SAK-14/KRITERIUM.md) `5330c701` | [`SAK-14/RESULTAT.md`](SAK-14/RESULTAT.md) `5cc8128c` |
| **SAK-09c** | Aragao 2018 `W7133020405` | H1/H7-uavklart → **H8** | AL-2606 | **lukket på `[V]`** — kildeteksten finnes ikke utenfor samtykket | *ingen — saken nådde ikke dit* | [`SAK-09c/LUKKET.md`](SAK-09c/LUKKET.md) `4e76f32f` |
| **SAK-08** | Riris 2018 `W2784603861` | H5 → **H8** (utløser) | AL-1280 | **lukket på `[V]`** — modellkoden er ikke deponert noe sted | *ingen — saken nådde ikke dit* | [`SAK-08/LUKKET.md`](SAK-08/LUKKET.md) `229599c4` |
| **SAK-09b** | Aragao 2018 `W7133020405` | H5 verktøygrense | AL-0852 | **ikke opphevet av det navngitte middelet** — `blockmodeling` 1.1.8 mangler mekanismen Pajek manglet | [`SAK-09b/KRITERIUM.md`](SAK-09b/KRITERIUM.md) `2fa587a0` | [`SAK-09b/RESULTAT.md`](SAK-09b/RESULTAT.md) `092d446c` |
| **SAK-11** | Bynum m.fl. 2021 `W4206850274` | H5 → **H8** (utløser) | AL-2516 | **stoppet på steg 3** — scenariosettet er ikke publisert | *ingen — saken nådde ikke dit* | [`SAK-11/LUKKET.md`](SAK-11/LUKKET.md) `4246f62e` |
| SAK-13 | Biblindex 2020 `W3165757969` | H1 tid | AL-0374 | **parkert** — svakt kriterium, ugjort har ingen fasit | — | — |
| SAK-01 | Pring 2016 `W2551114598` | H5 verktøygrense | 23 passasjer | **gjennomført 25.09 som PS-246**; utvidelsen med saltholdighet: **H7** — avhandlingen rapporterer ingen EC, eneste verdi er `0.0μS/cm` som ble *satt* | — | [triagen, datert tillegg 28.09](../SAKBEHANDLING-2026-09-27-triage.md) |
| SAK-15 | Mythos 2018 `W2974992769` | H1/H7 → **H7** | AL-0681 | **L5 nei** — 3 siteringer, ingen daterer grop H i Knossos; 137 treff i bredere søk | — | [triagen, datert tillegg 28.09](../SAKBEHANDLING-2026-09-27-triage.md) |
| SAK-16 | Eythra 2017 `W4317830072` | H1/H7 → **H7** | AL-0070 | **L5 nei** — 2 siteringer om annen keramikk; de to Eythra-treffene er anmeldelser av et bind fra 2016 | — | [triagen, datert tillegg 28.09](../SAKBEHANDLING-2026-09-27-triage.md) |
| SAK-17 | Pietrele 2019 `W2936215896` | H1/H7 → **H7** | AL-1440 | **L5 nei** — 12 siteringer, ingen analyserer flere digler fra 5. årtusen ved Nedre Donau | — | [triagen, datert tillegg 28.09](../SAKBEHANDLING-2026-09-27-triage.md) |
| SAK-02 … SAK-12 (forkastet) | — | — | 33 passasjer | **utenfor rekkevidde** — krever fysisk materiale, feltarbeid eller mennesker | — | — |

## Koblingen til kandidatregisteret

`sak`-feltet i `kandidat.schema.json` (B3-tillegg) grupperer passasjer til sakbehandlingsenheten.
Per 28.09.2026 er feltet satt på **6 av 432 rader** i `data/kjede/kandidat432/8-register.jsonl`:
AL-0738 og AL-2370 → `SAK-14`, AL-2606 → `SAK-09c`, AL-1280 → `SAK-08`, AL-0852 → `SAK-09b`, AL-2516 → `SAK-11`. Gruppering er ikke en
måling: feltet endrer ingen andel og inngår i ingen nevner.

**Hva som føres i registeret og hva som føres her — et valg, ikke en forglemmelse.** En sak kan
ende på to ulike måter, og bare den ene er en endring av klassen:

* **Klassen endres** når tilgangssituasjonen utenfor materialet endrer seg. AL-2606 og AL-1280 fikk
  derfor en **datert vurdering `H8`, `loftbar: nei`** i `loftbarhet` (ADR-0010) — samme form som
  Heron, som gikk fra H1 til H8 uten at teksten endret seg. Den kodede klassen fra teksten står
  urørt. **De to H8-ene er ikke like varige:** SAK-09c er sperret av et samtykke som ikke skal
  falle, SAK-08 bare av at ingen har deponert modellen ennå. SAK-08 er derfor ført som **utløser** —
  dukker modellen opp på CoMSES, GitHub, Zenodo eller i ORCID-posten, kan saken gjenåpnes med
  kriteriet uendret.
* **Klassen endres ikke** når et kriterium er kjørt og ikke nådde terskelen. SAK-14 falt på 87,8 %
  mot 90 %, og SAK-09b falt fordi det navngitte verktøyet mangler mekanismen — men H3 er fortsatt H3
  og H5 fortsatt H5. Det som falt, var **den navngitte framgangsmåten på den datoen**. AL-0852 fikk
  derfor `loftbar: ja` med dato: hindringen *er* løftbar av en formålsbygget implementasjon, og det
  målte løftet er **konsekvensløst** — blokkstrukturen tvangen gir, er den avhandlingen alt hadde. Å skrive `loftbar: nei` på AL-0738 og AL-2370 ville
  gjort et målt utfall om til en påstand om klassen. Utfallet står derfor her, i sakregisteret,
  koblet til registeret gjennom `sak`-feltet.

## To feil i register v2, funnet og rettet 27.09.2026

De ble funnet fordi `sak`-feltet skulle settes og registeret da ble validert mot sitt eget skjema.
**Registeret validerte ikke.** Ingen av rettingene er en ny måling, og ingen låst fil siterte de
gamle sha-ene.

1. **`sil.presisjon_ki` manglet på alle 432 rader.** `presisjon` var til stede og stemte eksakt med
   `kjede.toml` for alle tre silkilder (dommer 0,143 · ekstraksjon 0,072 · begge 0,345), så
   intervallet som hører til verdien ble fylt inn derfra. Rader der `presisjon` ikke stemte med
   konfigurasjonen, ville stoppet jobben; det var ingen.
2. **`cites_coverage` bar et umålt nulltall på alle 432 rader** — `fulltext_available: 0`,
   `fulltext_total: 0`, `coverage_ratio: null`, **uten `status`**. `falsified` er `false` på alle
   432: falsifiseringsleddet ga aldri et tall for denne kjøringen. Et umålt nulltall leses som
   «ingen siterende fulltekst fantes», og det var ett av de ti grønn-og-feil-tilfellene skjemaet ble
   skrevet for å hindre. Rettet til `status: "ikke målt"` med `null` på alle tre tallene.

| | før | etter |
|---|---|---|
| `register_sha256` | `aa8f7c2eb27d58e2…` | `6caabaffff28432b…` |
| `register_innhold_sha256` | `76efce7596fb2494…` | `bceb9203cd9f5c53…` |

Hodet bærer en `rettet`-linje med det samme. Porten i hodet er uendret:
**«kandidatliste (post hoc port)»**.

## Registerets sha-er, per oppdatering 27.09.2026

| hendelse | `register_sha256` |
|---|---|
| som produsert (validerte ikke mot skjemaet) | `aa8f7c2eb27d58e2…` |
| etter rettingen av de to feltene og SAK-14 | `6caabaffff28432b…` |
| etter SAK-09c: sak på AL-2606/AL-0852 + H8-vurdering | `c2d4b577bcc382d4…` |
| etter SAK-08: sak på AL-1280 + H8-vurdering | `50bc061a2e4cc4f5…` |
| etter SAK-09b: vurdering H5/ja på AL-0852 | `ffda71628d3a4891…` |
| etter SAK-11: sak på AL-2516 + H8-vurdering | `c6895202b76199aa…` |

## Hva fase 2d har gitt, 27.–28.09.2026

Fem saker behandlet — hele kortlisten fra triagen — og de faller i fire ulike former, som er selve funnet:

| sak | form | utfall |
|---|---|---|
| SAK-14 | kjørt, port med terskel | **falt på terskelen** (87,8 % mot 90 %), men ga et funn i motsatt retning: to feilhenvisninger i Dionysios |
| SAK-09c | `[V]` falt før kriteriet | **H8, varig** — inndataen er sperret av et samtykke som ikke skal falle |
| SAK-08 | `[V]` falt før kriteriet | **H8, utløser** — modellkoden er bare ikke deponert ennå |
| SAK-09b | kjørt, port uten terskel | **falt på middelet** — det navngitte verktøyet mangler mekanismen, og løftet er konsekvensløst |
| SAK-11 | stoppet på steg 3 | **reproduksjonen er umulig** — fordelingens parametere, seed, scenariosett og kode er alle uoppgitt; og full enumerering er målt til 5,03 mrd. beskrankninger |

**Ingen av de fem ble opphevet.** Fire av fem ga likevel et forskningsresultat, og alle fire kom på
steder kriteriene ikke pekte: feilhenvisninger funnet ved å lese originalen (SAK-14), at inndataen til
AI-aksens saker ofte er samtykkesperret primærdata (SAK-09c), at en verktøygrense kan sperre en
representasjon uten å sperre et resultat (SAK-09b), og at artikkelen selv kan ha målt at det ugjorte
sperret ingen resultat (SAK-11: 100 av 22 481 940 scenarioer = 0,000445 %, som bekrefter artikkelens egen
påstand om «less than 0.001 %»). **Det er formen ledd 2 har: porten avgjør om hindringen er opphevet,
ikke om arbeidet var verdt å gjøre.**

**Og ett mønster går igjen i fire av fem:** det som stanser saken, er sjelden hindringen selv. Det er
at inndataen ikke er publisert — profiler holdt tilbake av samtykke (SAK-09c), modellkode aldri
deponert (SAK-08), scenariosett og fordelingsparametere aldri oppgitt (SAK-11) — eller at det
navngitte middelet ikke gjør det triagen antok (SAK-09b). **Bare SAK-14 kom helt fram til en terskel,
og den falt med 2,2 prosentpoeng.** Det er den viktigste forventningen å justere for fase 2d: porten
er ikke det som siler, tilgangen er.

## L5-sjekkene, 28.09.2026 — fire av fire nei

Spørsmålet «har noen gjort det siden?» ble stilt for fire saker og besvart med **nei i alle fire**,
med DOI per siterende arbeid. Belegget står i triagens [datert tillegg](../SAKBEHANDLING-2026-09-27-triage.md).
**10 OpenAlex-kreditter brukt av 40 tillatte**, og ingen `mailto` sendt til tjenesten.

**Ingen av nei-ene skyldes at feltet er dødt.** Pietrele er sitert 12 ganger, Eythra-søket ga 81 treff,
Knossos-søket 137. Det ugjorte er likevel ikke tatt opp av noen. **En hindring blir ikke opphevet av at
feltet arbeider videre i nærheten** — det er et eget funn om ledd 2, og det gjelder alle fire.

PS-246-utvidelsen fikk det skarpeste svaret: avhandlingen *har* EC-instrumentering (TDR), men EC-en er
aldri rapportert som data — den er et mellomledd på vei til vanninnhold — og den eneste EC-verdien i
581 864 tegn er `0.0μS/cm`, verdien som ble satt. Dessuten er bulk-TDR-EC den gale størrelsen:
Saxton–Rawls krever `ECe` i dS/m fra mettet pastautdrag. **Termen finnes, inndataen gjør ikke.**
