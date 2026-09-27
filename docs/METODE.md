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

**Kryssdokumentsjekk** (skal gi 0 umerkede foreldede verdier over 40 filer):

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

**Testene** (354 grønne, én nettverkstest deselektert):

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
  dekker de materialet.

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
omfangsvalg uten navngitt hindring. **`N3`-grensen bærer koderidentitet** — åtte uavhengige kodere på
tilfeldig delt materiale spredte seg over **5,8–13,6 %** (ADDENDUM-22 §9.4). Det er ikke støy; det er
en grense reglene ikke avgjør.

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
som sorteringsnøkkel, ikke som filter. **Kostnaden er 6,6 leserpassasjer per bekreftet treff**
(2 844 / 432).

**Koblingen mellom Q-linje og tekstbit er alle-treff, ikke første-treff.** En Q-linje ligger ofte i mer
enn ett overlappende vindu (473 av de koblede gjorde det). Med første-treff mistet unionen PS-300 og
dekket 26 av 27; med alle-treff dekker den 27 av 27 og reproduserer D1s tall for ekstraksjonen eksakt.

**Ikke-prosa merkes og fjernes aldri** (`ikkeprosa.py`, versjonert): 18,1 % av dømt materiale er ikke
prosa, men bare 2,5 % av treffene. Nevneren er materialet slik porten så det.

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
| Opus 5, **agentisk, én sammenhengende økt** | **0,812** [0,712–0,917] | **leser** |

Rekken er monoton, og Haiku/Opus-spennene overlapper ikke. **Ett-kall-modeller under Opus er
sil-klasse:** de kan redusere en mengde, men ikke avgjøre et register. Mellom per-kall-Opus og agentisk
Opus overlapper intervallene i 0,712–0,768, så **øktformens bidrag er mulig og umålt**.

**Øktene er serielle.** Sju parallelle Opus-instanser falt på leverandørens øktgrense ved 87 % dekning
og kostet fem av åtte økter. Hver instans har egen kladdekatalog. Øktstørrelsen er ≤ 356 passasjer,
målt til 25 034 kontekst-tokens per passasje og 29,5 minutter per økt.

**Leserens `tvil`-flagg er den enkeltopplysningen som forutsier presisjon best:** blind presisjon
**97,6 %** der `tvil` er `false`, **75,9 %** der den er `true` (ADDENDUM-23 §7.2).

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
   alene er 14 % presis.
