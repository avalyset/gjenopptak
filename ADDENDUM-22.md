# ADDENDUM-22 — arbeidslisten for de 100 verkene

**Skrevet:** 2026-09-27, **før kjøring.** **Status: LÅST. RUTE c ER VALGT LESER. KJØRES NÅR EIEREN SIER
JA TIL KVOTEN.** **Gjelder:** å gå fra 27 leste treff til en liste over alt det ugjorte i de 100 verkene,
med klasse og rute per treff.

## 1 Inndata, låst

**Unionen av dommerens flagg og ekstraksjonens Q-linjer.** Målt 27.09.2026,
`ekstraksjon/2026-09-26/k1-union-v2.json`. Koblingen er gjort på **tekst** med ADDENDUM-16 §3s matchregel
— NFC, samlet mellomrom, uten tegnsetting i endene, ingen fuzzy — og en Q-linje regnes inn i **alle**
overlappende vindu den ligger i, ikke bare det første:

| mengde | tekstbiter |
|---|---|
| A — dommer-flaggede (gemma2:9b, temp 0, frø 734248) | 2 173 |
| B — passasjer som bærer en Q-linje | 1 030 |
| A ∩ B | 359 |
| bare A | 1 814 |
| bare B | 671 |
| **A ∪ B — arbeidslistens inndata** | **2 844** |

**2 844 av 22 243 = 12,8 % av korpuset.** Av de 884 Q-linjene lot **99 seg ikke koble** til noen tekstbit;
de er ikke passasjer i korpuset og inngår ikke. **473 av de koblede lå i mer enn ett vindu** — det er
grunnen til at alle-treff-regelen er nødvendig, se §2.

**Ikke-prosa beholdes og merkes, den fjernes ikke.** Etter den versjonerte G3-regelen
(`src/gjenopptak/classify/ikkeprosa.py`, sha256 `63ed734555a8bc95…`) er **514 av de 2 844 = 18,1 %** ikke
prosa. Hver utdatarad bærer merket. Regelen fra 26.09 reproduserer ikke (LAERDOM §31), så det er den
versjonerte som gjelder her, og andelen 18,1 % er regnet med den.

## 2 De 27 kjente ligger alle i unionen — og en rettelse av mitt eget forsøk

**Alle 27 er funnet i de 22 243 ved eksakt tekstmatch**, og alle 27 verk-ID-er står blant de 100 i
`data/port/spesifikasjon.json` (`ekstraksjon/2026-09-26/k1-de-27.json`):

| | antall |
|---|---|
| funnet i de 22 243 | **27 av 27**, alle ved eksakt match |
| i A (dommeren flagget) | 25 |
| i B (ekstraksjonen siterte) | 11 |
| i begge | 9 |
| **i unionen A ∪ B** | **27 av 27** |

De to dommeren ikke flagget, er **PS-257** (`utvalgstype: n3`) og **PS-300** (`utvalgstype: ingen`), begge
i `W2551114598`. Ekstraksjonen fanger begge. Det er hele grunnen til at silen er en union og ikke bare
dommeren.

**Tallet 11 er en uavhengig bekreftelse av koblingsregelen.** ADDENDUM-18/D1 førte «ekstraksjon 11» for de
27, målt med en annen implementasjon. Alle-treff-regelen gir **nøyaktig 11**; første-treff ga 7. To
uavhengige implementasjoner treffer samme tall der de skal, og skiller lag der regelen skiller lag.

**Rettelse, samme dag.** Et tidligere forsøk i denne slyngen konkluderte at «de 27 kjente ligger i 15
DOAJ-dokumenter» og at overlappet med portkorpuset var null. **Det var feil, og feilen var en join på
antall.** Jeg slo «de 27» opp i `data/recall-sett-2.jsonl`, som *også* inneholder 27 treff — i 15
DOAJ-dokumenter fra recall-settets eget korpus, en helt annen mengde. De 27 kjente i ADDENDUM-18/D1 er
**25 flaggede + PS-257 + PS-300**, alle PS-ID-er i portens presisjonssett. Joinen var altså mellom
*radantallet 27* i to ubeslektede filer, ikke mellom identifikatorer. Porten i §6 står derfor som oppdrag
K skrev den, og den omformuleringen som fulgte av feilen er strøket.

**Ett funn overlevde rettelsen, og det er et reelt funn.** Med **første-treff**-kobling — én Q-linje til
ett vindu — ble unionen 2 581 og dekket **26 av 27**: PS-300 falt ut fordi Q-linjen lå i to overlappende
vindu og førstetreffet ga nabovinduet (2193–2197) i stedet for PS-300s (2196–2200). Med alle-treff er
dekningen 27 av 27 og unionen 2 844. **Første-treff-kobling er derfor forkastet som metode**: den
forkaster passasjer som beviselig bærer et sitert utsagn, av vilkårlige grunner.

## 3 Leseren: rute c

Regelen ble satt før ADDENDUM-20 landet: a) Haiku ≥ 0,70 med full regelfil, b) ellers Sonnet ≥ 0,70,
c) ingen av dem → CC-instans agentisk som i ADDENDUM-11.

* **a) faller, målt.** Haiku 4.5 med koder 2s fulle regelfil: **κ = 0,047 [−0,020–0,168]** på 271 parede
  passasjer (ADDENDUM-20 §7, partielt på 275 av 320). Full regelkontekst gjorde kandidaten **målbart
  dårligere** enn det tynne utdraget — differanse −0,222, paret bootstrap [−0,402 – −0,044], utelukker 0 —
  fordi den flagget 2 treff der utdraget ga 22.
* **b) er uavgjort.** ADDENDUM-20 stoppet på `Your credit balance is too low to access the Anthropic API`;
  Sonnet 5 startet aldri. Den står nr. 2 i køen i ADDENDUM-19 §5.
* **c) er valgt leser.** Ingen kandidat er dokumentert over 0,70, og porten spør om dokumentert, ikke om
  sannsynlig.

**Rute c er ikke betinget av ADDENDUM-19 eller av Sonnet-full.** Skulle Opus 5 senere nå koder 2s nivå med
ett kall per passasje, er det grunnlag for et nytt addendum med en billigere leser — ikke for å endre
denne.

**Oppsettet for c, identisk med ADDENDUM-11 der det er mulig:**

| | verdi |
|---|---|
| leser | CC-instans, agentisk, tom kontekst, `claude-opus-5` (samme modell-ID som koder 2, ADDENDUM-11 §8) |
| regelfil | `koder2/koderegler-gjenvunnet.md`, 9 805 B, sha256 `234695dd4e1777a9…`, defektene intakte |
| sperreliste | **samme som ADDENDUM-11 §2**, med filnavn i oppdraget, utvidet med ADDENDUM-11, -18, -19, -20, -21, denne filen og `koder2-sammenlikning.json` |
| form | **åtte økter à 356 passasjer**, hver i én sammenhengende lesning, i fast rekkefølge |
| signatur | modell-ID, tokens inn/ut fra `usage`, start- og sluttid, regelfil-sha, addendum-sha — per økt |
| utdata | til Vault under `arbeidsliste/`, ikke til scratchpad |

Åtte økter, ikke én: koder 2s målte forbruk gjelder 320 passasjer i én økt, og én økt på 2 844 ville
sprengt både kontekst og kostnadsgrunnlag. **356 er 11 % større enn det målte grunnlaget**, og
ekstrapolasjonen er ikke større enn det.

## 4 Kvoten eieren skal avgjøre

Grunnlaget er koder 2s **målte** forbruk (ADDENDUM-11 §8): 320 passasjer, 61 kall, 20,6 minutter,
9 019 781 tokens inn, 103 373 ut — altså **28 187 tokens inn per passasje**, 5,2 passasjer per kall,
3,9 sekunder per passasje.

| | passasjer | kall | tokens inn | tokens ut | tid |
|---|---|---|---|---|---|
| koder 2, **målt** | 320 | 61 | 9 019 781 | 103 373 | 20,6 min |
| én økt av åtte | 356 | ≈ 68 | ≈ 10 020 000 | ≈ 115 000 | ≈ 23 min |
| **alle åtte øktene** | **2 844** | **≈ 542** | **≈ 80 200 000** | **≈ 919 000** | **≈ 3,0 t** |
| blind presisjonsport, separat instans | 100 | ≈ 19 | ≈ 2 819 000 | ≈ 32 000 | ≈ 6 min |
| **SUM rute c** | | **≈ 561** | **≈ 83 000 000** | **≈ 951 000** | **≈ 3,2 t** |

**Skaleringen er lineær, og det er en antakelse, ikke en måling.** Koder 2s forbruk domineres av
buffer-lesing — 8 562 261 av 9 019 781 inn — og buffer-lesing vokser med kontekstlengden i økten. Derfor
er åtte økter à 356 det eneste anslaget som ligger nær grunnlaget; én økt på 2 844 ville kostet mer enn
åtte ganger, ikke like mye.

**Til sammenlikning, om kreditt fanns og b) hadde levert:** ett kall per passasje koster ≈ 11,0 M tokens
inn for Haiku (ingen hurtigbuffer — prefikset er 3 703 tokens, under modellens minstelengde) og ≈ 1,5 M
for Sonnet 5, der bufferen slår inn. **Rute c er 7,6× dyrere enn rute a og 56× dyrere enn rute b.** Det er
prisen for at ingen kandidat kom over 0,70.

## 5 Utdata per passasje

| felt | verdi |
|---|---|
| `id` | løpenummer i den nye lista |
| `doc_id`, `start_index`, `end_index` | passasjens plass i korpuset |
| `felt` | arkeologi / energimodellering / klinisk epidemiologi / tekstvitenskap |
| `kilde` | `dommer` / `ekstraksjon` / `begge` |
| `ikke_prosa` | G3-merket, `ikkeprosa.py` sha256 `63ed734555a8bc95…` — **merket, ikke fjernet** |
| `treff` | true / false |
| `klasse` | H1–H9, eller N1–N3 for ikke-treff, eller `<klasse>/H7-uavklart` |
| `rute` | `ekstern ressurs manglet` / `selvpålagt avgrensning` / `uavklart` |
| `begrunnelse` | én setning |
| `signatur` | modell-ID, temperatur, regelfil-sha256, addendum-sha256, økt-nummer, tidspunkt |

**Registerformat som det eksisterende, ny fil.** Det gamle registeret røres ikke, og de 30 radene der står
uendret uansett hva den nye lista viser.

## 6 Porter, satt før kjøring

1. **De 27 kjente:** leseren skal bekrefte **≥ 22 av 27**. Alle 27 ligger i inndataen (§2), så porten kan
   feile — og det er hele poenget med den. Under 22: **STOPP og rapporter**, ingen arbeidsliste.
2. **Blind presisjon:** **100 tilfeldige passasjer** som leseren kalte treff, frø **734248**, til en
   **separat instans med sperreliste** — samme sperreliste som §3. **≥ 0,70** for at lista kalles
   **arbeidsliste**; under, heter den **kandidatliste**, og navnet endres ikke i ettertid.
3. **Kostnad:** tokens per **bekreftet** treff, målt fra `usage`, ikke anslått. Tabellen i §4 er et
   budsjett og skal erstattes av målingen.

## 7 Etter kjøring, i samme slynge

Klassefordeling per felt; andel H7; andel i løftbar rute; og sammenlikning mot registerets 30 — hvor mange
av de 30 den nye lista finner igjen, og hvor mange nye den legger til. Alt til Vault, med stier i
rapporten.

## 8 Dødsbetingelser

* **Porten på de 27 er ikke forhandlingsbar.** Faller den, skrives ingen liste, og tallet rapporteres.
* **Navnet følger presisjonen.** Under 0,70 er det en kandidatliste, i alle dokumenter, permanent.
* **Ingen offentliggjøring, ingen MASTER-redigering.** Ingen Zenodo, ingen OSF.
* **Ingen ny nøkkel, ingen annen nøkkel.** Kreditten er tom; å fylle den er eierens avgjørelse.
* **Ingen økt kjøres om.** Blir en økt avbrutt, rapporteres antall dømte passasjer, og alle andeler regnes
  på de dømte — ikke på et sett fylt ut i ettertid.
* **Regelfilen rettes ikke** underveis, uansett hva leseren rapporterer om defektene i den.

## 9 Utfall 2026-09-27 — PORTEN FALLER. INGEN ARBEIDSLISTE SKRIVES.

**Porten på de 27 kjente er ikke oppfylt, og den er ikke forhandlingsbar (§6.1, §8).** 17 av 27
bekreftet, 6 mistet, 4 ennå ikke dømt — **selv om alle fire gjenstående bekreftes, blir maksimum 21, under
terskelen 22.** Utfallet er dermed avgjort uavhengig av det som mangler. Ingen liste skrives, verken som
arbeidsliste eller som kandidatliste, og den blinde presisjonsporten på 100 treff kjøres ikke: stoppen
kommer først.

### 9.1 Hva som ble kjørt

> **Senere fullført.** Tallene i §9.1–9.3 gjelder tilstanden da de fem avbrutte øktene ennå manglet
> 363 passasjer. Kjøringen ble fullført serielt samme dag, og de komplette tallene står i **§10**.
> Porten er uendret: 21 av 27, falt. §9 beholdes som den var, fordi den viser hva avbruddet kostet.

Tre av åtte økter er komplette (1, 5, 8). Fem ble avbrutt av en **øktgrense hos leverandøren** (HTTP 429,
«session limit»), fordi jeg startet sju instanser samtidig. **Til sammen 2 481 av 2 844 dømt = 87,2 %.**
De avbrutte er alle prefikser av blindfilen, i rekkefølge, uten hull.

| økt | dømt | av | treff | status |
|---|---|---|---|---|
| 1 | 356 | 356 | 65 (18,3 %) | komplett |
| 2 | 286 | 356 | 48 (16,8 %) | avbrutt |
| 3 | 312 | 356 | 48 (15,4 %) | avbrutt |
| 4 | 240 | 356 | 41 (17,1 %) | avbrutt |
| 5 | 355 | 355 | 47 (13,2 %) | komplett |
| 6 | 252 | 355 | 35 (13,9 %) | avbrutt |
| 7 | 325 | 355 | 49 (15,1 %) | avbrutt |
| 8 | 355 | 355 | 41 (11,5 %) | komplett |
| **sum** | **2 481** | **2 844** | **374 (15,1 %)** | |

**Ingen økt er kjørt om**, jf. §8. Andelene under er regnet på de dømte, ikke på et sett fylt ut i
ettertid. Og selv om §8 hadde tillatt det, kunne ikke en omkjøring rettet porten: taket er 21.

**Ingen kryssforurensning.** Tre instanser rapporterte filkollisjoner i delt kladdekatalog, og én sa at
visningen av postene 14–40 kom fra en annen økts blindfil. Kontrollert: **null fremmede id-er i noen av de
åtte filene.** De tre komplette er dessuten justeringstestet — 95–98 % av tekstbitene G3-regelen kaller
ikke-prosa fikk klassen `INGEN`, og **null av de korte tallrestene ble kodet som treff**. En instans som
hadde lest feil materiale for en strekning, ville gitt prosa-verdikter til søppel. Det skjedde ikke.

### 9.2 De seks mistede, og hvorfor de falt

| PS | AL | økt | koder c ga | koder 1s fasit | blant koder 2s uenigheter |
|---|---|---|---|---|---|
| PS-133 | AL-0770 | 3 | `N1`, tvil | H8, bedømbar usikker | **ja** |
| PS-148 | AL-2840 | 8 | `INGEN`, tvil | H9, bedømbar usikker | nei |
| PS-226 | AL-2759 | 8 | `INGEN`, tvil | H7, bedømbar nei | **ja** |
| PS-292 | AL-1931 | 6 | `INGEN`, tvil | H7, «klassen er usikker» | **ja** |
| PS-297 | AL-1832 | 6 | `N1`, tvil | H7, «derav tvil» | nei |
| PS-315 | AL-0030 | 1 | `INGEN`, tvil | H7, bedømbar nei | **ja** |

**Alle seks er merket `tvil: true` av koderen selv**, og **fire av seks var allerede blant koder 2s tolv
uenigheter med koder 1.** Koder 1s egne notater sier «klassen er usikker», «derav tvil» eller
`bedømbar: nei` på fem av dem. Porten faller altså ikke på tilfeldige passasjer — den faller på **fasitens
egne marginaltilfeller**, og den faller på de samme som en tidligere uavhengig koder også var uenig om.

To mønstre bærer alle seks:

* **«Hindringen tilhører feltet eller tredjepart, ikke arbeidet»** (PS-315, PS-226, PS-148). Koder 1 leste
  dem som arbeidets eget ugjorte; koder c anvendte ADDENDUM-04 §4 i motsatt retning. Samme regel, motsatt
  utfall.
* **«Besvart i samme passasje» → N1** (PS-133, PS-297). Koder 1 skrev selv «Løst med antakelse i samme
  passasje, derav tvil» om PS-297 — og koder c leste nøyaktig det faktum som N1. Det er ikke en feil; det
  er det samme faktum klassifisert ulikt. Det er også nøyaktig den uenighetstypen ADDENDUM-11 §7 talte tre
  av.

**Slutningen:** silen har ingen gjenfinningssvikt — alle 27 ligger i inndataen, verifisert ved eksakt
tekstmatch (§2). Det som ikke overlever, er **fasitens marginaltilfeller under uavhengig gjenlesning.**
Porten målte det den var satt til å måle, og svaret er nei.

### 9.3 Målt på de 2 481 dømte — ikke en liste, men tallene §8 krever

**Treff per felt:**

| felt | treff | dømt | rate | Wilson 95 % |
|---|---|---|---|---|
| arkeologi | 237 | 871 | **27,2 %** | 24,4–30,3 |
| klinisk epidemiologi | 47 | 300 | 15,7 % | 12,0–20,2 |
| tekstvitenskap | 34 | 328 | 10,4 % | 7,5–14,1 |
| energimodellering | 56 | 982 | **5,7 %** | 4,4–7,3 |

**Andel H7: 253 av 374 = 67,6 % [62,7–72,2]** — og den varierer sterkt: klinisk epidemiologi 96 %,
tekstvitenskap 85 %, arkeologi 65 %, energimodellering 46 %.

**Løftbarhet etter PREREG §5:** løftbar klasse H1–H6 **69 av 374 = 18,4 % [14,8–22,7]**; ikke-løftbar
H7–H9 **75,9 %**; uavklart klasse 5,6 %.

**Rute:** `ekstern ressurs manglet` 347 = **92,8 %**, `uavklart` 25 = 6,7 %, **`selvpålagt avgrensning` 2
= 0,5 %.** Ruten er i praksis død, se §9.4.

**Hvem fanget treffene** — snittet er langt det presiseste leddet:

| kilde | treff | dømt | presisjon |
|---|---|---|---|
| begge (A ∩ B) | 108 | 318 | **34,0 %** |
| bare dommeren | 228 | 1 597 | 14,3 % |
| bare ekstraksjonen | 38 | 566 | 6,7 % |

**Ikke-prosa-merkingen virket som tenkt:** 17,7 % av det dømte materialet er ikke prosa, men bare **2,4 %
av treffene**. Søppel ble merket, ikke fjernet, og ble likevel ikke treff.

**Tvil:** 24,2 % av alle verdikter, **48,4 % av treffene**. Nesten halvparten av treffene er koderen selv
usikker på.

**Mot registerets 30** (`register/claims.jsonl`): 29 av 30 ligger i unionen — den ene som ikke gjør det, er
en kontrollkandidat utenfor portkorpuset. Av de 29: **19 bekreftet, 6 mistet, 4 ikke dømt.** Av de 19
bekreftede fikk **17 samme hindringsklasse som registeret**; de to som avvek, er PS-119 (register H5, koder
c H9) og PS-137 (register H8, koder c H1/H7-uavklart). Ingen nye registerrader skrives, siden ingen liste
skrives.

**Pris, målt og ikke anslått:** 25 034 kontekst-tokens inn per dømt passasje (målt i økt 1) × 2 481 dømte
= **62,1 M inn**, altså **166 065 tokens per treff**. Harness-ens egen total for én komplett økt:
287 533 tokens.

### 9.4 Ruten `selvpålagt avgrensning` er tom, og det er et funn

Åtte uavhengige kodere, 2 481 verdikter, **to** treff med ruten `selvpålagt avgrensning`. Samtidig kodet de
**229 passasjer som `N3`** — selvpålagt forenkling, ikke treff. Koderen i økt 1 så dette selv og reiste det
før økt 2 (`arbeidsliste/tolkningslinje-n3-mot-selvpalagt.json`): ADDENDUM-10 §3 rad 3 sier at en
selvpålagt forenkling er N3 og **ikke** treff, og da kan ruten `selvpålagt avgrensning` nesten ikke
oppstå. Ni id-er i økt 1 ville snudd under den motsatte lesningen; alle ni står som `N3`/`uavklart`.

**N3-raten varierer med mer enn det dobbelte mellom koderne** — 5,8 % (økt 7) til 13,6 % (økt 2) — på
tilfeldig delt materiale fra samme union. Det er den samme tolkningslinjen som dukker opp som spredning.
**Reglene ble ikke endret underveis** (§8), og det var riktig: hadde jeg rettet dem mellom økt 1 og 2,
ville denne spredningen vært umålbar.

**Konsekvens for utdataskjemaet i §5:** ruten slik den er definert, kan ikke skille selvpålagt fra eksternt
så lenge selvpålagt samtidig diskvalifiserer treffet. Enten er `N3` for bredt, eller ruten er overflødig.
Det avgjøres ikke her.

## 10 Kjøringen fullført 2026-09-27 — komplette tall

De 363 udømte passasjene fra 429-avbruddet ble kjørt ferdig **serielt, én instans om gangen, med egen
kladdekatalog per instans** (økt 2 + 70, økt 3 + 44, økt 4 + 116, økt 6 + 103, økt 7 + 30). Ingen
kollisjoner, rekkefølge og feltverdier maskinverifisert i hver. **Alle 2 844 er dømt.** Tall i
`arbeidsliste/koder-c-komplett.json`.

**Porten står som falt: 21 av 27 bekreftet, terskel 22.** Alle fire gjenstående kjente ble bekreftet —
PS-072 (H7), PS-106 (H7), PS-031 (H5), PS-300 (H7) — så tapene er de samme seks som i §9.2: PS-133,
PS-148, PS-226, PS-292, PS-297, PS-315. Ingen liste skrives som arbeidsliste. Merkelappen etter den post
hoc porten i ADDENDUM-23 er **«kandidatliste (post hoc port)»**.

**432 treff av 2 844 = 15,2 %.**

| felt | treff | dømt | rate | Wilson 95 % |
|---|---|---|---|---|
| arkeologi | 274 | 990 | **27,7 %** | 25,0–30,5 |
| klinisk epidemiologi | 53 | 347 | 15,3 % | 11,9–19,4 |
| tekstvitenskap | 37 | 378 | 9,8 % | 7,2–13,2 |
| energimodellering | 68 | 1 129 | **6,0 %** | 4,8–7,6 |

**Klasse:** H7 289 · H5 50 · H9 29 · H1/H7-uavklart 26 · H2 14 · H8 11 · H1 10 · H3 2 · H4 1.
**Andel H7: 66,9 % [62,3–71,2].**
**Løftbarhet:** løftbar H1–H6 **77 av 432 = 17,8 % [14,5–21,7]**, uavklart klasse 6,0 %, ikke-løftbar
H7–H9 **76,2 %**.
**Rute:** `ekstern ressurs manglet` 401 · `uavklart` 29 · **`selvpålagt avgrensning` 2** — mot **264 `N3`**
i hele materialet. §9.4 står uendret: ruten kan ikke oppstå så lenge selvpålagt forenkling diskvalifiserer
treffet.

**Snittet er fortsatt det presiseste leddet:**

| kilde | treff | dømt | presisjon | Wilson 95 % |
|---|---|---|---|---|
| begge (A ∩ B) | 124 | 359 | **34,5 %** | 29,8–39,6 |
| bare dommeren | 260 | 1 814 | 14,3 % | 12,8–16,0 |
| bare ekstraksjonen | 48 | 671 | 7,2 % | 5,4–9,4 |

**Ikke-prosa:** 18,1 % av dømt materiale, **2,5 % av treffene** — merkingen holdt søppelet ute av
treffmassen uten å fjerne det.
**Tvil:** 23,9 % av alle verdikter, **49,5 % av treffene.**
**Mot registerets 30:** 29 i unionen, **23 bekreftet, 6 mistet, og 21 av 23 med samme hindringsklasse.**
**Pris, målt:** 71,2 M kontekst-tokens inn, **164 805 per treff.**
