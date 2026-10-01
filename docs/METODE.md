# METODE — hvordan porten kjøres, og hva tallene kan bære

**Skrevet 2026-09-26.** Dette dokumentet skal være tilstrekkelig alene: en utenforstående skal kunne
kjøre porten fra kommandoene, stiene, frøene og sha-summene her, uten å lese koden først.

## Stoppvilkåret for dette dokumentet

**En utenforstående skal kunne kjøre porten på et nytt felt fra dette dokumentet alene.** Er det noe
her som krever at man spør oss, er dokumentet ikke ferdig. Rekkefølgen under er den man trenger:

| § | hva |
|---|---|
| 1 | grunnraten, og korrigeringen for presisjon |
| 2 | hva fasiten kan måle, og hva den ikke kan |
| 3 | ADR-ene metoden hviler på |
| 4 | kjør porten — kommandoer, stier, frø, sha |
| 5 | enhet og ruting |
| **6** | **rammen** — hvordan feltet avgrenses, og hva som faller ut |
| **7** | **typologien**, med ankersetningene skrevet før første artikkel ble lest |
| **8** | **silen** — hva som er prøvd, hva som ble valgt, og hva det koster |
| **9** | **leseren** — regelfil, øktform, og hvorfor ett kall ikke holder |
| **10** | **falsifisering** mot siteringer |
| **11** | **kjente grenser** |

## 1 Grunnraten, regnet tre veier

Alle tre tallene gjelder samme materiale: **22 243 tekstbiter** fra 100 verk
(`data/port/spesifikasjon.json` → `sum_passasjer`), hvorav dommeren flagget **2 173**
(`data/port/presisjon-resultater.json` → `n_treff_i_alt`) og **20 070** ikke ble flagget (samme fil →
`presisjon.ikke_treff.vektet`).

| | koder 1 | koder 2 | hva tallet er |
|---|---|---|---|
| **a) bekreftede treff / alle tekstbiter** | 25/22 243 = **0,112 %** = ett per **890** | 19/22 243 = **0,085 %** = ett per **1 171** | **måler utvalget, ikke materialet.** Telleren er de sanne i et stratifisert utvalg av 150 flaggede; nevneren er alt. Tallet er meningsløst som prevalens og skal ikke brukes. |
| **b) presisjon × flaggede / alle** | 0,1667 × 2 173 = 362 → **1,63 %** = ett per **61** [1,13–2,29 %] | 0,1267 × 2 173 = 275 → **1,24 %** = ett per **81** [0,81–1,85 %] | **et gulv.** Teller bare sanne blant de flaggede; alt dommeren mistet, er utenfor. Intervallet er presisjonens Wilson. |
| **c) b delt på implisert recall** | 362/0,475 = 763 → **3,43 %** = ett per **29** [2,12–7,95 %] | 275/0,407 = 676 → **3,04 %** = ett per **33** [1,73–7,55 %] | **beste anslag.** Korrigerer for tapte treff. Intervallet er dominert av usikkerheten i tapte, ikke i presisjonen. |

**Implisert recall** = sanne blant flaggede / (sanne blant flaggede + tapte). Tapte er regnet av
bomraten blant de 100 leste ikke-flaggede (INGEN 1/50 + N3 1/50 = 2/100), Wilson **0,55–7,00 %**, ×
20 070 ikke-flaggede = **400 tapte [110–1 405]**
(`data/port/presisjon-resultater.json` → `presisjon.ikke_treff.vektet.bomrate`).

**Presisjon per koder:** koder 1 25 av 150 = 16,7 % [11,6–23,4]
(`data/port-presisjonssett-ADDENDUM10.jsonl` → `ekte_treff`, `utvalgstype == "treff"`); koder 2 19 av
150 = 12,7 % [8,3–18,9] (`data/port-presisjonssett-verdikter-koder2.jsonl`).

## 2 Hva fasiten kan måle, og hva den ikke kan

Fasiten er 25 ekte treff funnet ved blind lesing av 320 tekstbiter: **150 dommer-flaggede** + 50
dømt INGEN + 50 N1/N2 + 50 N3 + 20 ankere (`data/port-presisjonssett-ADDENDUM10.jsonl` →
`utvalgstype`).

**Fasiten er 25 sanne blant 150 leste flaggede.** De 320 bar i tillegg **2 sanne blant de
ikke-flaggede** (én i INGEN-stratumet, én i N3) og **12 ankertreff** med kjent fasit fra recall-sett 1
og 2 — koder 1, kilde `data/port-presisjonssett-ADDENDUM10.jsonl` → `utvalgstype` og `ekte_treff`.
De 12 ankerne er frøsettets egne passasjer og hører ikke i en recall-måling av en ny metode; de 2
ikke-flaggede er dommerens tapte treff og måles for seg, utenfor kriteriet.

**Den kan måle:** recall-tap for en ny metode *relativt til dommeren* — altså hvor mange av de 25
en ny rute finner. Det er sammenlignbart mellom metoder fordi tallet er det samme 25.

**Den kan ikke måle:** (a) **presisjon** for en ny metode, fordi de 25 er funnet blant dommerens
flagg og ikke er et tilfeldig utvalg av materialet; (b) **absolutt recall**, fordi teller og nevner
begge er dommerbetinget — treff dommeren aldri flagget, og som ikke falt i de 150 leste
ikke-flaggede, finnes ikke i fasiten; (c) **prevalens**, jf. §1 rad a.

**Fasiten er dommerbetinget.** Enhver ny metode måles derfor mot et mål som selv har en blindsone,
og et tall som «21 av 25» betyr «21 av de 25 dommeren fant og vi bekreftet», ikke «21 av alle treff
i materialet».

### Klasse-κ per klasse — hvilke grenser reglene avgjør, og hvilke de ikke gjør

Regnet 28.09.2026 av de to koderfilene alene (`port-presisjonssett-ADDENDUM10.jsonl` og
`port-presisjonssett-verdikter-koder2.jsonl`), n = 320. **Samlet klasse-κ over alle klasser
samtidig: 0,722**, rå enighet 85,6 %. Per klasse, den mot resten:

| klasse | koder 1 | koder 2 | begge | κ |
|---|---|---|---|---|
| `INGEN` | 213 | 220 | 208 | **0,879** |
| `H7` | 26 | 22 | 20 | **0,820** |
| `H2` | 2 | 1 | 1 | 0,665 |
| `H5` | 4 | 2 | 2 | 0,664 |
| `N1` | 6 | 12 | 6 | 0,658 |
| `N2` | 8 | 21 | 8 | **0,535** |
| `N3` | 54 | 34 | 26 | **0,530** |
| `H1/H7-uavklart` | 1 | 3 | 1 | 0,498 |
| `H9` | 1 | 3 | 1 | 0,498 |
| `H8` | 3 | 2 | 1 | 0,395 |
| `H1`, `H3` | 1 | 0 | 0 | — (n = 1, ingen overlapp) |

**De to svakeste grensene er ikke-treff-klassene.** `N3` og `N2` ligger på 0,53, mot 0,88 for `INGEN`
og 0,82 for `H7`. For `N3` avvek de to koderne med en faktor **1,6** på hvor ofte de brukte klassen —
54 mot 34, enige om 26. Det er grunnen til at N3-grensen nå har en **eksplisitt beslutningsregel** med
ankereksempler, versjonert: [`REGEL-N3-v1.md`](REGEL-N3-v1.md), sha256 `96cd8372e3f847f0da15…`.

**Klassene med n = 1 til 4 har ikke et tolkbart κ.** `H1`, `H3`, `H8`, `H9` og `H1/H7-uavklart` er
oppført fordi utelatelse ville sett ut som enighet, men tallene skal ikke siteres som mål på grensene —
de måler at klassen nesten ikke forekom i de 320.

**Den stabile kjernen er tre av 27.** Av de 27 kjente treffene i portmaterialet er det bare **tre** —
PS-044, PS-205, PS-266 — der koder 1 og koder 2 er enige om treffstatus *og* ingen av dem har merket
`tvil`. Delkriteriene: enige 19 av 27, uten tvil hos koder 1 bare **7**, hos koder 2 bare **4**
(ADDENDUM-23 §1, regnet fra `data/port-presisjonssett-ADDENDUM10.jsonl` og
`data/port-presisjonssett-verdikter-koder2.jsonl` alene).

**Det setter en grense for hva fasiten kan bære.** En port som krever at en ny leser bekrefter 22 av 27,
forutsetter at de 27 er stabile. De er ikke det: koder 1 merket **20 av 27** med tvil. Da ADDENDUM-22s
port ble prøvd, bekreftet en tredje uavhengig koder **21 av 27**, og alle seks tapene var tvilsmerkede
passasjer — fire av dem allerede blant koder 2s uenigheter. **Fasiten kan bære et hovedfunn om
klassefordeling; den kan ikke bære en terskel nær sin egen ytterkant.**

## 3 ADR-ene metoden hviler på

| ADR | hva den binder |
|---|---|
| 0001 | korpusgrensen: åpen fulltekst |
| 0002 | seksjonsbevaring |
| **0003** | **modellsignatur i hver dom** — modell-id med vekt-sha256, temperatur, frø |
| 0004 | løftbarhet slås opp i låst tabell, settes aldri av modellen |
| 0007 | seksjonsetikettens opphav: `source` eller `parser`, aldri blandet |
| **0008** | **keep_alive ved batch** — vekt verifisert før og etter, ettersjekk med `keep_alive=0` |
| **0009** | **Vault som standard** for alle skrivende moduler, ingen fallback, diskvakt med gulv |
| 0010 | løftbarhet er datert; vurderinger føyes til, endres aldri |
| **0011** | **enheten for søk er setningen, ekstrahert per dokumentvindu** |

## 4 Kjør porten — kommandoer, stier, frø, sha

Forutsetninger: Vault montert på `/Volumes/Vault`, `ollama serve` i gang, repoet på `~/dev/gjenopptak`,
`PYTHONPATH=src`.

```bash
cd ~/dev/gjenopptak
PYTHONPATH=src .venv/bin/python -c "from gjenopptak.vault import require_vault; print(require_vault())"
```

**Modell og frø, låst:** `gemma2:9b`, vekt-sha256
`ff1d1fc78170d787ee1201778e2dd65ea211654ca5fb7d69b5a2e7b123a50373`, temperatur **0**, frø **734248**.
Verifiser vekten før og etter en batch (ADR-0008):

```bash
curl -sS http://localhost:11434/api/show -d '{"name":"gemma2:9b"}' | python3 -c "import json,sys;d=json.load(sys.stdin);print([l for l in d['modelfile'].splitlines() if 'blobs/sha256-' in l])"
```

**Dømming av alle tekstbiter** (det som ga de 2 173 flaggene):

```bash
PYTHONPATH=src .venv/bin/python -m gjenopptak.classify.port_run døm
PYTHONPATH=src .venv/bin/python -m gjenopptak.classify.port_run mål
PYTHONPATH=src .venv/bin/python -m gjenopptak.classify.port_run determinisme --keep-alive 0 --utsnitt 50 --bare-batch
```

**Kryssdokumentsjekk** (skal gi 0 umerkede foreldede verdier over alle dokumentene den finner; 69 filer etter frys-rettelsene 28.09.2026):

```bash
PYTHONPATH=src .venv/bin/python -m gjenopptak.kryssjekk
```

**Speiling til Vault** (skal gi 0 bak):

```bash
PYTHONPATH=src .venv/bin/python -m gjenopptak.speil --check
```

**Sikring av repoet** (utløses av PREREG-/ADDENDUM-commits, skriver kanon-bundle):

```bash
PYTHONPATH=src .venv/bin/python -m gjenopptak.securerepo --check
```

**Testene** (403 grønne ved frys-rettelsene 28.09.2026, én nettverkstest deselektert):

```bash
.venv/bin/python -m pytest -q
```

**Ekstraksjonsprompten** (ADR-0011, ADDENDUM-16): `prompts/ekstraksjon-v1.txt`, 594 bytes, sha256
`c8c276df9ffe62c906db566c24abcf6f415746a8271f737928f426f94dbeb534`. `num_ctx` **8192** eksplisitt;
4096 trunkerer stille, og signaturen på det er `prompt_eval_count == num_ctx`.

**Regelfilen koder 2 leste** (ADDENDUM-11 §2, gjenvunnet 27.09.2026) og **koder 2s modellsignatur**
er ført i `MANIFEST-VAULT.md` på Vault, seksjonen «Koder 2-gjenvinning — 2026-09-27», med sti, bytes,
sha256, opphav og autentisitetsgrunnlag. Manifestet er stedet slike sha-er føres; de gjentas ikke her.
Kort: `koder2/koderegler-gjenvunnet.md`, 9 805 B, sha256 `234695dd4e1777a9…`, koder 2 = `claude-opus-5`.

## 5 Enhet og ruting

**Ekstraksjon per dokumentvindu er målt og død.** Testen var preregistrert i ADR-0011 og ADDENDUM-16;
resultatet, med dødsbetingelsene fra ADDENDUM-16 § 6 anvendt:

| vilkår | målt | kilde | utfall |
|---|---|---|---|
| recall ≥ 21/25 | **9 av 25 = 36,0 %** | `ekstraksjon/2026-09-26/2d-recall.json` | **DØD** |
| samlet tid under 4,48 t | **4,28 t** (ekstraksjon 3,45 + dømming 0,83) | `2d-tid.json` | lever |
| blind presisjon > 23,4 % | **17 av 100 = 17,0 % [10,9–25,5]** | `2d-blind-presisjon.json` | **DØD** |

598 vinduer, 884 Q-linjer, 124 vinduer med NONE. Tre vinduer nådde `num_ctx`-taket 8192 i alle tre
forsøk og mangler; ingen fasit-treff lå i dem.

**Det som likevel er verdt å vite fra en død test:**

* **Ekstraksjonen fant begge treffene dommeren mistet** (PS-257 og PS-300, sanne blant de
  ikke-flaggede) og **to av de fire treffene uten markørord**. Den er altså ikke bundet av
  markørvokabularet — den rakk bare ikke kravet.
* **Dommeren flagget 49,5 % av Q-linjene** mot 9,8 % av alle tekstbiter: strømmen er fem ganger
  tettere. Men den blinde lesningen fant 17 % ekte. **To LLM-ledd som er enige, er ikke bevis** — de
  deler modellfamilie og regelsett, og enigheten måler det.
* **Ekstraksjonen gir færre kandidater, samme presisjon, lavere recall.** Kandidatmengde **884 mot
  dommerens 2 173 flaggede** (2,46× færre). Presisjon **17,0 % [10,9–25,5] mot 16,7 % [11,6–23,4]** —
  intervallene overlapper fullstendig. Recall **9 av 25 mot dommerens 25 av 25** (den siste er sann ved
  konstruksjon: fasiten er trukket fra dommerens flagg). Den renser altså ikke, og den finner mindre;
  den koster bare mindre — **2,02 M tokens inn mot 30,19 M for å dømme alt**
  (`ekstraksjon/2026-09-26/d2-tokenvolum.json`).
* **Kaskaden er bedre enn hvert ledd for seg.** På de 100 blindede Q-linjene flagget dommeren 51, og
  **16 av de 17 sanne lå blant dem**: presisjon i snittet **31,4 % [20,3–45,0]** ved **94,1 %
  [73,0–99,0]** bevaring av de sanne (`ekstraksjon/2026-09-26/d1-2x2.json`). Og på de 27 kjente treffene
  er **unionen av dommer og ekstraksjon 27 av 27**, snittet 9. Ingen av leddene er en detektor; sammen
  dekker de de 27 kjente treffene. Om de dekker materialet, er ikke målt (§ 8).

**Ruting har fortsatt ingen ADR og ingen kode.** Den skrives når det finnes kode den styrer.

Test 2′ (ADDENDUM-17, deduplisert tekst) kjører etter 2d og rapporteres ved siden av, aldri i stedet
for. Dedupliseringen fjernet **2,0 % av ordene** (1 089 734 → 1 068 017) og 598 → 588 vinduer — som er
sitt eget funn: terskelen som utløste 2′, målte tegnsettingsfragmenter, ikke tekstvolum.

## 6 Rammen — hvordan et felt avgrenses

Et felt er en fil (`felt/<navn>.yaml`, byggeplanen B2). Rammen den peker på, er bygget slik:

1. **Emnefilter.** `topics.id:<T…>|<T…>`, hentet fra spørringen som ble kjørt, ikke fra verkenes egne
   `primary_topic` — de er spørringens *resultat*, hundrevis per felt. Spørringen står i det frosne
   rådata-manifestet (`raw/MANIFEST.md`), med kilde-URL per kall.
2. **Årsspenn:** `publication_year:2015-2020` for de fire eksisterende feltene.
3. **Åpenhet:** `open_access.is_oa:true`.
4. **Hentbarhet** (ADDENDUM-04 §2): rammen er verk som er åpne **og** faktisk hentbare på den
   offentlige ruten — P1 JATS via Europe PMC, ellers P3: PDF med minst **2 000 tegn** uttrekkbar tekst.
   Et verk som er `is_oa:true` men svarer 403, er **ikke** i rammen.
5. **Frysing.** Rammelisten skrives til `frames/frame-<felt>-RAW.jsonl` med sha256 i feltfilen. Er
   sha-en endret, avvises feltet. Rammen hentes aldri på nytt for en måling.

**Hva som faller ut, og hvorfor det betyr noe.** Hentbarheten følger **leveringen**, ikke
forretningsmodellen: ScienceDirect 1 994 → 30, IOP 1 221 → 4, Wiley 698 → 2, mens arXiv går fra 4,7 til
14,5 % og MDPI fra 6,8 til 17,4 % av rammen. Hindawi og E3S er rene OA og svarte 403; IEEE og Springer
selger abonnement og beholdt 89 %. **Rammen er derfor skjev på en måte «åpen tilgang» ikke forklarer**,
og det skal stå ved siden av hvert tall.

**Trekkingen** er sekvensiell med preregistrert frø (ADDENDUM-09): den frosne listen sorteres, stokkes
med `random.Random(0x05988B23)`, og hentbarhet prøves i trekkrekkefølge til 25 hentbare verk per felt.
Hver avgjørelse, også utelukkelsene, står i `utvalg/trekklogg-<felt>.jsonl`.

## 7 Typologien, med ankersetningene

Ni hindringsklasser, låst i PREREG-v1 §5 **før data**. Løftbarheten er en tabell, aldri en modell
(ADR-0004), og den er datert (ADR-0010).

| klasse | hindring | løftbar av AI i dag |
|---|---|---|
| H1 | menneskelig lesning eller koding i skala | ja |
| H2 | lesbarhet: håndskrift, skadet kilde, lyd | ja |
| H3 | språkbarriere | ja, med forbehold |
| H4 | mønster i bilder eller signaler i volum | ja |
| H5 | simulering og regnekraft | delvis |
| H6 | strukturslutning fra sekvens | ja |
| H7 | dataene fantes ikke | nei |
| H8 | tilgang, juss, etikk, samtykke | nei |
| H9 | begrepet eller teorien manglet | nei |

**To ankersetninger per klasse ble skrevet i ADDENDUM-02 før første artikkel i utvalget ble lest.** De
er hele grunnen til at klassene ikke kan bøyes etter hva materialet viste seg å inneholde. Fire
eksempler, ordrett:

* **H1** — «As manual review of all records was not feasible» (10.1136/bmjopen-2026-121412, `Discussion`)
* **H2** — «caregiver utterances were inaudible, or not clear enough for the coders to transcribe»
  (10.1371/journal.pone.0324106)
* **H7** — «Insufficient material remained from the small molecule extraction to enable DNA extraction»
  (10.1038/s41467-023-42247-w, `DNA extraction`)
* **H9** — «No consensus definition exists for OMPC» (10.3390/cancers14246194)

**Ikke-treff telles og rapporteres for seg:** `N1` besvart i samme passasje, `N2` nyhetspåstand, `N3`
omfangsvalg uten navngitt hindring. **`N3`-grensen er en grense reglene ikke avgjør** — åtte Opus-økter på
ulike tilfeldige delmengder spredte seg over **5,8–13,6 %** (ADDENDUM-22 §9.4). Materialet er ulikt fra
økt til økt, så spredningen er ikke testet mot utvalgsvariasjon, og den er ikke vist å være koderidentitet.

**De uavklarte parene** (ADDENDUM-05): der passasjen ikke avgjør om hindringen var arbeidsmengde eller
manglende data, er klassen `<klasse>/H7-uavklart`, og løftbarheten **`uavklart`** — ikke naboens verdi.

## 8 Silen — hva som er prøvd, og hva det koster

Silen er `sil(tekstbiter) -> kandidater` (B4), med **én** implementasjon: **dommer ∪ ekstraksjon**.

| kandidat | målt | utfall |
|---|---|---|
| markørliste v1/v2 | recall for lav | forkastet |
| embeddings (bge-m3) | 84 % recall ved 2,0× kostnad | forkastet |
| seksjonsplassering | 1,09× — under terskelen | forkastet |
| nærsøk | 84 % recall ved 5,25× kostnad | forkastet |
| ekstraksjon per dokument alene | 36 % recall som enhet | forkastet |
| **dommer ∪ ekstraksjon** | **27 av 27 kjente**, 12,8 % av korpuset | **valgt** |

**Presisjon per silledd**, målt over 2 844 dømte passasjer (ADDENDUM-22 §10), med Wilson 95 %:

| kilde | treff / dømt | presisjon |
|---|---|---|
| begge (A ∩ B) | 124 / 359 | **34,5 %** [29,8–39,6] |
| bare dommeren | 260 / 1 814 | 14,3 % [12,8–16,0] |
| bare ekstraksjonen | 48 / 671 | 7,2 % [5,4–9,4] |

Snittet er det presiseste leddet, men **unionen** er den eneste som fanget alt — snittet brukes derfor
som sorteringsnøkkel, ikke som filter. **Kostnaden er 6,6 leserpassasjer per treff leseren meldte**
(2 844 / 432); **≈ 7,7 per treff bekreftet av en uavhengig leser** ved 85 % (ADDENDUM-23 § 7.2, 2 844 / 367).
*(Rettet 28.09.2026, frys-lesning 2: sto «per bekreftet treff»; 432 er treffene koder c meldte, jf.
KORRIGENDUM-2026-09-28 § F.)*

**Koblingen mellom Q-linje og tekstbit er alle-treff, ikke første-treff.** En Q-linje ligger ofte i mer
enn ett overlappende vindu (473 av de koblede gjorde det). Med første-treff mistet unionen PS-300 og
dekket 26 av 27; med alle-treff dekker den 27 av 27 og reproduserer D1s tall for ekstraksjonen eksakt.

**Ikke-prosa merkes og fjernes aldri** (`ikkeprosa.py`, versjonert): 18,1 % av dømt materiale er ikke
prosa, men bare 2,5 % av treffene. Nevneren er materialet slik porten så det.
**Silens recall er «ikke målt», og det er ikke en formulering — det er tilstanden.** Presisjonen er målt
per silkilde (begge 0,345 · dommer 0,143 · ekstraksjon 0,072), men **recall for silen som helhet kan ikke
måles av dette materialet**: teller og nevner er begge dommerbetinget, og et treff dommeren aldri flagget,
og som ikke falt i de 150 leste ikke-flaggede, finnes ikke i fasiten (§ 2). De 27 kjente treffene er
dommerens egne flagg pluss to ekstraksjonen fant, så de er ikke et uavhengig mål. **Et tall for
silrecall skal ikke oppgis**, verken som anslag eller som intervall, før noen har lest blindt i en ramme
silen ikke har sett.
*(Tillegg 30.09.2026: den lesningen er gjort for ett felt. Fase 3 (ADDENDUM-25) bygde et referansesett — 20 av
100 nye arkeologiverk lest perm til perm før silen kjørte — og silen beholdt **95 av 104 = 91,3 % [84,4–95,4]**
av referansetreffene (`docs/RESULTAT-ADDENDUM-25.md` § 1.2). Tallet gjelder de 20 verkene, mot en LLM-lesning
av samme modellfamilie og regelfil, ikke et menneske. For de første 100 verkene og kandidatlista på 432 står
«ikke målt» uendret, og registerhodets skjema tillater fortsatt bare den verdien. **Treffene er klynget** — 104 i
12 av 20 verk, 51 i ett — så intervallet er for smalt; uten det største verket er det 45 av 53 = 84,9 %
[72,9–92,1], RESULTAT § 1.2.)*


## 9 Leseren — regelfil, øktform, og hvorfor ett kall ikke holder

Leseren er en **agentisk Claude Code-instans på Opus**, som underinstans eller `claude -p`. Den får
**nøyaktig to filer**: regelfilen og sin egen blindfil med `id` og `tekst`. Sperrelisten navngir de
forbudte filene i oppdraget og genereres av kjeden.

**Regelfilen** er `koder2/koderegler-gjenvunnet.md`, 167 linjer, sha256 `234695dd4e1777a9…`, bygget av
ordrette utdrag fra seks kilder: PREREG-v1 §2, PREREG-v1 §5, ADDENDUM-03 §1.2, ADDENDUM-05,
ADDENDUM-04 §4 og ADDENDUM-10 §1–3. **Den brukes med defektene sine intakte** — ADDENDUM-05-utdraget
bærer `grep -n`-prefiks og mangler tabellraden for tre uavklarte par. Å rette det ville gitt leseren
bedre regler enn referansekoderen hadde.

**Målt med samme regelfil og samme kallstruktur**, ett kall per passasje, mot koder 1:

| leser | κ | klasse |
|---|---|---|
| Haiku 4.5 | 0,031 [−0,024–0,129] | **sil** |
| Sonnet 5 | 0,294 [0,126–0,455] | **sil** |
| Opus 5, ett kall per passasje | 0,636 [0,478–0,768] | grensetilfelle |
| Opus 5, **agentisk, én sammenhengende økt** | **0,812** [0,697–0,906] | **leser** |
| qwen2.5:7b lokalt, **agentisk: regelfil + parti på 20 i samme kontekst** (ADDENDUM-24, 28.09.2026) | 0,248 [0,113–0,376] | **sil** |

Rekken er monoton, og Haiku/Opus-spennene overlapper ikke. **Ett-kall-modeller under Opus er
sil-klasse:** de kan redusere en mengde, men ikke avgjøre et register. Mellom per-kall-Opus og agentisk
Opus overlapper intervallene i 0,697–0,768, så **øktformens bidrag er mulig og umålt**.
**Lokal agentisk leser er sil-klasse** (ADDENDUM-24, `docs/RESULTAT-ADDENDUM-24.md`): samme modus som gjorde
Opus til leser, gir en lokal 7B-modell κ = 0,248 — på høyde med gemma2 i ett kall (0,289). `LokalLeser` i
`kjede/leser.py` er implementasjonen av `Leser`, klassifisert som sil.
*(Rettet 28.09.2026, frys-lesningen: intervallet sto som [0,712–0,917], som hører til κ = 0,826 mot koder 1s
første lesning; for 0,812 gir ADDENDUM-11 § 4 [0,697–0,906]. Ingen slutning endres.)*

**Øktene er serielle.** Sju parallelle Opus-instanser falt på leverandørens øktgrense ved 87 % dekning
og kostet fem av åtte økter. Hver instans har egen kladdekatalog. Øktstørrelsen er ≤ 356 passasjer,
målt til 25 034 kontekst-tokens per passasje og 29,5 minutter per økt.

**Leserens `tvil`-flagg skiller presisjonen sterkt:** blind presisjon **97,6 %** (41/42) der `tvil` er
`false`, **75,9 %** der den er `true` (ADDENDUM-23 §7.2), i en post hoc delgruppe. Andre prediktorer
(f.eks. silkilde) er ikke sammenlignet, og forskjellen er ikke testet.
### Koder 4 — Fable 5.1, chat, ikke menneske (28.09.2026)

**Hvorfor den finnes:** de to første koderne er begge Opus-instanser, og «uavhengig» har hittil betydt
tom kontekst og egen kladdekatalog, ikke uavhengig dømmekraft. Koder 4 er en **annen modellfamilie**
på samme 320 passasjer, samme blindfil (`15ce72a7687cea57…`), samme regelfil
(`234695dd4e1777a9…`), én gjennomgang i PS-rekkefølge. **Den er fortsatt ikke et menneske**, så
`κ` mot menneskelig lesning er uendret ukjent.

**Treffbeslutningen, tre par side om side.** Cohens κ, paret bootstrap, 10 000 gjentak, frø 734248.

| par | n | rå enighet | κ | bootstrap 95 % |
|---|---|---|---|---|
| **koder 4 mot koder 2** | 320 | 0,981 | **0,899** | 0,808–0,969 |
| koder 1 mot koder 2 | 320 | 0,963 | 0,812 | 0,697–0,906 |
| koder 4 mot koder 1 | 320 | 0,956 | **0,781** | 0,659–0,883 |
| koder 4 mot koder 2 | 300 uten ankere | 0,983 | 0,875 | 0,751–0,971 |
| koder 1 mot koder 2 | 300 uten ankere | 0,967 | 0,774 | 0,623–0,898 |
| koder 4 mot koder 1 | 300 uten ankere | 0,957 | 0,711 | 0,540–0,847 |

**Funnet:** en annen modellfamilie gjenskaper koder 2s treffbeslutning **bedre (0,899) enn koder 1 og
koder 2 gjenskaper hverandres (0,812)**. Intervallene overlapper, så rekkefølgen er ikke etablert — men
retningen er motsatt av det modellfamilie-forbeholdet forutså, og **koder 1 er den av de tre som
avviker mest** fra de to andre. 2×2 mot koder 1: 29 begge, 4 bare koder 4, **10 bare koder 1**, 277 ingen.

**Klasse er en svakere enighet enn treff, for alle tre par.** κ blant passasjer begge kaller treff:

| par | n felles treff | rå enighet | κ | bootstrap |
|---|---|---|---|---|
| koder 1 mot koder 2 | 30 | 0,867 | 0,732 | 0,481–0,936 |
| koder 4 mot koder 2 | 30 | 0,800 | 0,683 | 0,435–0,890 |
| koder 4 mot koder 1 | 29 | 0,690 | **0,501** | 0,248–0,728 |

**Konfusjonen har ett dominerende felt, og det er N3 mot INGEN.** Koder 4 satte `INGEN` der koder 1
satte `N3` **40 ganger** — den største enkeltcellen utenfor diagonalen i hele tabellen. Koder 4 brukte
`N3` **13** ganger, koder 1 **54**. Det er en **definisjonsforskjell**, ikke støy: N3 krever at det
finnes et ugjort uten navngitt hindring, og koder 4 leser de samme passasjene som at det ikke finnes
noe ugjort i det hele tatt. Med koder 1 mot koder 2 var κ for N3 **0,530**; koder 4 gjør den grensen til
det klareste uenighetspunktet i sporet, og det er en tredje uavhengig bekreftelse av at
[`REGEL-N3-v1.md`](REGEL-N3-v1.md) trengtes.

**M1 og M2, oppgitt hver for seg og aldri sammenslått** (ADDENDUM-03 § 1.2, PREREG § 6):

| mål | koder 4 | dommeren (`gemma2`) på koder 1s 39 treff |
|---|---|---|
| treff | 33 av 320 | 39 av 320 (koder 1) |
| **M1-streng** (samme setning) | **27 av 33 treff = 81,8 %** [65,6–91,4] · 8,44 % av 320 [5,86–12,00] | 23 av 39 = 59,0 % (14 ikke dømt av dommeren) |
| **M1-passasje** (±2 setninger) | 33 av 33 · 10,31 % av 320 [7,44–14,13] | — |
| **M2** `ja` | **17 av 33 = 51,5 %** [35,2–67,5] | 4 av 39 |
| M2 `usikker` | 15 = 45,5 % [29,8–62,0] | 15 |
| M2 `nei` | 1 = 3,0 % [0,5–15,3] | 6 (14 ikke dømt) |

**Høyre kolonne er ikke koder 1s koding** *(rettet 28.09.2026, frys-lesningen)*. Sammenligningsskriptet
(`tmp-koder4b.py` på Vault, `koder4/`) leste `samme_setning` og `bedømbar` i
`data/port-presisjonssett-ADDENDUM10.jsonl`; det er dommerens felt fra oppfølgingskallet (§ 11 punkt 6),
og de mangler for de 14 av koder 1s treff dommeren ikke flagget. Koder 1s eget felt er `min_bedømbar`:
**35 av 39 = 89,7 %** [76,4–95,9] `True`, 4 `False`. Koder 1 har ikke eget felt for samme setning.

**Slutningen som sto her — at koder 4s treff er «tettere og mer avgjørbare» enn koder 1s — er trukket.**
Den sammenlignet koder 4 med dommeren, ikke med koder 1. M2 for koder 4 (tre verdier) og for koder 1
(to verdier) er dessuten ikke samme skala, og ADDENDUM-11 § 5 viser at M2 bærer koderidentitet.

**De 27 kjente treffene: koder 4 fant 18 = 66,7 %** [47,8–81,4]. **Alle ni tapte var merket `tvil` av
koder 1**, og sju av de ni ble også mistet av koder 2. Tapene ligger altså i nøyaktig den ustabile
delen av fasiten, og det er en tredje kilde til funnet at **den stabile kjernen er tre av 27**.

**Tvil forutsier presisjon også her.** 25 av koder 4s 33 treff bærer `tvil` (75,8 % [59,0–87,2]).
Mot koder 1:

| | n | rå enighet | κ | presisjon blant koder 4s treff |
|---|---|---|---|---|
| `tvil = false` | 283 | 0,982 | 0,753 | **8 av 8 = 100 %** [67,6–100] |
| `tvil = true` | 37 | 0,757 | 0,433 | 21 av 25 = 84,0 % [65,3–93,6] |

Samme retning som ADDENDUM-23 § 7.2 fant for koder c (97,6 % mot 75,9 %, post hoc), nå i en annen
modellfamilie. **`tvil` peker samme vei i to modellfamilier; forskjellen er ikke testet, og andre
prediktorer er ikke sammenlignet** — intervallene over, [67,6–100] og [65,3–93,6], overlapper nesten helt.
*(Rettet 28.09.2026, frys-lesning 2: sto «`tvil` er den mest overførbare enkeltopplysningen i kjeden», en
rangering ingen har målt; jf. § 9 om andre prediktorer.)*

#### Datert note 28.09.2026 — koder 4 var delvis eksponert, og følsomheten er regnet

**Koder 4 leste `docs/SAKBEHANDLING-2026-09-27-kandidater.md` dagen før kodingen**, og kjente PS-246,
PS-257 og PS-300 på id fra sporets dokumenter. **7 av 320 rader er derfor ikke blindt kodet.**

| PS | grunn til eksponering | kilde |
|---|---|---|
| PS-266 | **eksakt tekstmatch** | AL-0925 (`W3217588367`) |
| PS-246 | 2 felles setninger | AL-0314 (`W2551114598`) — og kjent på id |
| PS-288 | 2 felles setninger | AL-2440 (`W2551114598`) |
| PS-289 | 2 felles setninger | AL-0681 (`W2974992769`) |
| PS-319 | 2 felles setninger | AL-0068 (`W2551114598`) |
| PS-257 | kjent på id | sporets dokumenter |
| PS-300 | kjent på id | sporets dokumenter |

Matchregelen er NFC og samlet mellomrom. **Settet er komplett:** en romsligere grense (≥ 1 felles lang
setning) fant **ingen nye**. **Ingen av de sju er anker.** 116 rader stammer fra verk kandidatfila
navngir, men med annen tekst — det er kjennskap til verket, ikke til passasjen, og telles ikke.

**Følsomhet: κ med og uten de eksponerte radene.** Samme bootstrap, 10 000 gjentak, frø 734248. Koder 1
og koder 2 er ikke regnet om utover samme radutvalg, som kontroll.

| par | alle 320 | 320 − eksponerte (313) | 300 uten ankere | 300 − eksponerte (293) |
|---|---|---|---|---|
| koder 4 mot koder 2 | **0,899** [0,808–0,969] | **0,874** [0,756–0,962] | 0,875 [0,751–0,971] | 0,819 [0,623–0,955] |
| koder 1 mot koder 2 *(kontroll, aldri eksponert)* | 0,812 [0,697–0,906] | 0,794 [0,662–0,900] | 0,774 [0,623–0,898] | 0,727 [0,523–0,882] |
| koder 4 mot koder 1 | **0,781** [0,659–0,883] | **0,757** [0,614–0,871] | 0,711 [0,540–0,847] | 0,645 [0,426–0,817] |

**Kontrollparet er det som gjør tallene lesbare.** κ faller for **alle tre par** når de sju radene tas
ut — også for koder 1 mot koder 2, som aldri var eksponert. Grunnen er ikke eksponering, men at de sju
inneholder **6 av de 27 kjente treffene**: å fjerne dem krymper den positive klassen og senker κ for
enhver koder. Fallet per par, på 320-grunnlaget: koder 4–1 **−0,024**, koder 4–2 **−0,025**, kontrollen
**−0,018**. **Differansen mot kontrollen er 0,006 og 0,007 — langt inne i støyen.**

På 300-grunnlaget er fallene større (−0,066 · −0,056 · −0,047) fordi n blir minst der, men bildet er det
samme: **koder 4s par faller knapt mer enn kontrollparet**, og **rekkefølgen koder 4–2 > koder 1–2 >
koder 4–1 holder i alle fire radutvalg.**

**De 27 kjente, fordelt på eksponering.** Koder 4 fant 18, mistet 9.

| | n | eksponerte |
|---|---|---|
| funnet | 18 | **6** — PS-246, PS-257, PS-266, PS-289, PS-300, PS-319 |
| tapt | 9 | **0** |

**Alle seks eksponerte kjente treff ble funnet, og ingen av de ni tapte var eksponert.** Recall på de
27 med alt inne er **66,7 %** [47,8–81,4]; på de **21 ueksponerte** er den **57,1 %** [36,5–75,5].

**To lesninger av den asymmetrien, og begge skal stå.** Den ene er at eksponeringen hjalp. Den andre er
at de eksponerte var de **lettest kodbare**: fire av de seks (PS-246, -266, -289, -319) kom via
kandidatfila, som er valgt på `tvil: false`, og i en post hoc delgruppe var blind presisjon der 97,6 %
[87,7–99,6] (ADDENDUM-23 § 7.2); presisjonen for akkurat dette utvalget er ikke målt. PS-257 og PS-300 var
kjent på id. *(Rettet 28.09.2026, frys-lesning 2: sto at alle seks «kom i kandidatfila» på `tvil: false`,
«der blind presisjon er målt til 98 %».)* **Dataene skiller ikke de to**, og intervallene
[47,8–81,4] og [36,5–75,5] overlapper i hele sin lengde. Det ærlige tallet å oppgi er **begge**, med
n = 21 som det eksponeringsfrie.

**Hva noten ikke fjerner:** koder 4s kodinger av de sju radene er fortsatt i fila, uredigert, og de
inngår i alle tall merket «alle 320». Noten gjør ikke kodingen blind i ettertid — den gjør omfanget
målt.

**Én formavvik i inndata, ført og ikke rettet:** `samme_setning` og `bedombar` er til stede på alle
320 rader, ikke bare på treffene, med verdien `null` på de 287 ikke-treffene. Ingen beregning over
leser dem for ikke-treff. **Fila er ikke redigert.**

### Leseren er datert, og lesningen er ikke gjentakbar

**Dette er den mest alvorlige begrensningen i kjeden, og den skal stå her og ikke i et vedlegg.**

En agentisk økt kan ikke spilles av på nytt. Modellen bak leseren er en tjeneste som endrer seg uten et
versjonsnummer vi kan feste; øktens kontekst bygges av leserens egne mellomresultater i en rekkefølge
som ikke er bestemt av inndataen; og temperatur, verktøykall og øktgrenser er utenfor vår kontroll.
**Samme regelfil, samme passasjer, samme frø og samme kommando gir derfor ikke nødvendigvis samme
register.**

Følgene er tre, og ingen av dem er retoriske:

1. **κ = 0,812 er en datert måling**, ikke en egenskap ved leseren. Den gjelder koder 2s økt
   25.09.2026 (17:14:53–17:35:26 UTC, ADDENDUM-11 § 8) på `claude-opus-5` med regelfilen `234695dd4e1777a9…`. Gjentas den i morgen, er et annet
   tall et **nytt datapunkt**, ikke en motsigelse.
2. **Registeret er ikke reproduserbart, bare etterprøvbart.** Radene kan leses om av hvem som helst mot
   passasjene, og det er den formen for etterprøving som gjelder her. `gjenopptak run --from les` gir en
   **ny** lesning, ikke den samme.
3. **Enhver sammenligning mellom lesere bærer datoen.** Rekken 0,031 → 0,294 → 0,636 → 0,812 ble målt
   innenfor tre dager (0,812 25.09.2026, de tre andre 27.09.2026), med samme regelfil og samme 320 passasjer. Det er det som gjør den lesbar; en
   tilsvarende rekke målt over måneder ville ikke vært det.

**Det som *er* gjentakbart:** ramme, tekstbiter, dommer (`gemma2:9b`, temp 0, frø 734248, vektsjekket
sha256), ekstraksjon, union og register-validering. Ledd 1–6 og ledd 8–10 er determinerte. **Ledd 7 er
det ikke**, og skillet går der.


## 10 Falsifisering mot siteringer

To lag, og de må ikke forveksles:

1. **Dekningsgrad** (`falsify/citations.py`, kjedens ledd 7c). Hvor mange siterende arbeider finnes for
   verket, og hvor mange av dem har fulltekst? Europe PMC og Crossref. Klienten **armer seg selv
   først**, og armeringen feiler høyt i stedet for å returnere 0 — et stille nulltall i
   siteringsoppslag var ett av ti tilfeller der en komponent meldte grønt og var feil. Er dekningen
   ikke målt, står `status: "ikke målt"` i registerraden, **aldri 0**.
2. **Falsifiseringen selv.** Er det parkerte spørsmålet besvart i den siterende litteraturen siden?
   Det er et søk per påstand, gjort for fire påstander 21.09.2026, og det finnes **ikke** som
   kriterieskript. Kjeden leverer lag 1; lag 2 er sakbehandling per kandidat (ADR-0010).

## 11 Kjente grenser

1. **Ingen menneskelig annotør.** Alle kodere i sporet er LLM-baserte. κ måler om **regelsettet** gir
   samme utfall i to lesninger, ikke om det er riktig.
2. **Fasitens stabile kjerne er tre av 27.** Bare PS-044, PS-205 og PS-266 har enighet mellom to
   kodere *og* ingen tvil hos noen av dem. Koder 1 merket **20 av 27** med tvil. **En terskel nær
   referansesettets ytterkant måler settet, ikke leseren** — det er grunnen til at en port på 22 av 27
   falt med 21.
3. **Formålsvalgte felt.** Fire felt valgt for å spenne to forskningskulturer. Tallene beskriver de
   feltene, ikke litteraturen.
4. **Rammen er skjev etter levering** (§6), ikke etter forretningsmodell.
5. **Recall-enden er dårligst målt.** Intervallet på tapte treff spenner **110 til 1 405**.
6. **`unit` er dommerbetinget.** Skillet M1-streng/M1-passasje kommer fra dommerens oppfølgingskall.
   For passasjer bare ekstraksjonen fanget, er `samme_setning` ukjent, og `unit` blir `passage`.
7. **Løftbarhet er datert, ikke fast.** Heron gikk fra H1 til H8 uten at teksten endret seg.
8. **Leseren krever et Max-abonnement.** Uten Claude Code med Opus er silen alt man får, og silen
   alene er 15,2 % presis *(rettet 30.09.2026: sto «14 %», som er dommerleddet alene)*.
