# KORRIGENDUM 2026-09-28 — funn i låste filer, frys-lesningen før v0.4.0

**Ingen av filene under er endret.** `PREREG-v1.md` og hvert `ADDENDUM-*.md` er låst når det er
committet (INSTRUKSER-v1.2 § 2), og `docs/MASTER-PATCH-2026-09-26.md` er en påført, historisk patch.
Det som er feil eller innhentet i dem, føres her, etter mønsteret i
[`INNHENTET-2026-09-26-en-koder.md`](INNHENTET-2026-09-26-en-koder.md): per funn fil og linje, hva som
står, hva som er riktig, kilden, og om slutningen endres.

**Grunnlag:** frys-lesningens funnregister, Vault
`zenodo/v0.4.0-bygg/frys-lesning-funn-2026-09-28.jsonl` (sha256 `22835a0ec6170707…`), der hvert funn er
sjekket på nytt mot kilden før det er ført her; og `python -m gjenopptak.kryssjekk`, som fra 28.09.2026
regner alle addenda som låste og rapporterer treff i dem for seg. Linjenumrene gjelder filene slik de
står i treet 28.09.2026.

**Samlet: ingen slutning snur.** To tall endres i en retning som betyr noe for lesningen — løftbar andel
(nevneren) og κ-intervallet for 0,812 — men ingen port, terskel eller klassifisering flytter seg.

---

## A κ = 0,812 står med intervallet til κ = 0,826

**Kilden:** ADDENDUM-11 § 4, tabellen: treff/ikke-treff, alle 320, **κ = 0,812, 95 % KI 0,697–0,906**.
Raden «mot koder 1s **første** lesning (før ADDENDUM-10)» har κ = 0,826, KI **0,712–0,917**. Avskriftsfeilen
startet i ADDENDUM-21 § 5 og spredte seg. Overlappet mot Opus ett kall (19b, [0,478–0,768]) er derfor
**0,697–0,768**, ikke 0,712–0,768.

| fil:linje | står | riktig | slutningen |
|---|---|---|---|
| ADDENDUM-21.md:69 | «κ = 0,812 … bootstrap-intervall **0,712–0,917** (ADDENDUM-11 §4)» | 0,812 [0,697–0,906] | tersklene i § 5 (l. 74–75: «innenfor 0,712–0,917», «≥ 0,70 men under 0,712») **ble satt på feil intervall**; koder 3 er ukjørt, så ingen klassifisering er gjort på dem |
| ADDENDUM-19.md:116 | kriteriet, låst før kjøring: «innenfor koder 2s intervall 0,712–0,917» | 0,697–0,906 | utfallet 0,636 ligger i båndet 0,30–0,70 under begge intervaller; **klassifiseringen endres ikke** |
| ADDENDUM-19.md:184 | «koder 2 (Opus, én sammenhengende økt) \| 0,812 \| 0,712–0,917» | 0,812 \| 0,697–0,906 | ingen |
| ADDENDUM-19.md:196–197 | «koder 2 gir [0,712–0,917] — intervallene overlapper i 0,712–0,768» | [0,697–0,906]; overlapp **0,697–0,768** | står: øktformens bidrag er ikke påvist |

Rettet i rettbare filer samme dag: ADR-0012, METODE § 9, MANUSKRIPT-FAKTA § 2 og § 8. Kryssjekken har
fått størrelsen «κ-intervall for 0,812», så feilen fanges heretter.

## B Løftbar andel er regnet med alle treff som nevner

**Kilden:** ADDENDUM-05 § 4 — løftbar andel har **avklarte treff** som nevner, uavklart andel har alle
treff, og de to oppgis alltid sammen; `classify.liftability.format_liftable` håndhever det. Regnet på
nytt 28.09.2026 med `liftable_share`, Wilson 95 %:

| fil:linje | står | riktig | kilde |
|---|---|---|---|
| ADDENDUM-11.md:79 | koder 2: løftbar andel «2/19 = 10,5 %» | **2/17 avklarte = 11,8 %** [3,3–34,3]; uavklart **2/19 = 10,5 %** [2,9–31,4] | `data/port-presisjonssett-verdikter-koder2.jsonl`, de 150 med `utvalgstype == "treff"`: H7 12, H1/H7-uavklart 2, H9 2, H5 1, H2 1, H8 1 |
| ADDENDUM-22.md:321 | «løftbar H1–H6 **77 av 432 = 17,8 %** [14,5–21,7]» | **77/406 = 19,0 %** [15,4–23,1]; uavklart 26/432 = 6,0 % [4,1–8,7] | `data/kjede/kandidat432/8-register.jsonl` |
| ADDENDUM-22.md:251–252 | partiell tilstand: «69 av 374 = 18,4 %», uavklart 5,6 % | 69/353 = 19,5 % [15,7–24,0] (21 uavklarte = 5,6 % av 374) | samme addendum |
| MASTER-PATCH-2026-09-26.md:104 | «17,8 % [14,5–21,7] av treffene har løftbar klasse H1–H6» | 19,0 % [15,4–23,1] av de avklarte; 6,0 % uavklart | som over |

Koder 1 har ingen uavklarte blant sine 25, så 5/25 = 20,0 % er uendret. **Slutningen endres ikke:**
løftbar klasse er fortsatt en liten minoritet, og koder 2 ligger fortsatt under koder 1. Tallet
10,5 % var tilfeldigvis den uavklarte andelen, og det gikk videre som kryssjekkens kanoniske verdi;
den er rettet.

## C «Én koder» og «menneskelig leser»

Ført i [`INNHENTET-2026-09-26-en-koder.md`](INNHENTET-2026-09-26-en-koder.md), utvidet samme dag:

| fil:linje | hva | der |
|---|---|---|
| ADDENDUM-02.md:191 | § 5 pålegger «Designet har én koder» i sammendraget av enhver rapportering | INNHENTET § 3 |
| ADDENDUM-04.md:58 | viser til én-koder-svakheten som noe som skal stå i sammendraget | INNHENTET § 3 |
| ADDENDUM-08.md:27 | forbehold 2: «Designet har én koder» | INNHENTET § 3 |
| ADDENDUM-06.md:18, :118 | recall-fasiten «markert for hånd», «en menneskelig leser» — koderen var en Claude-økt | INNHENTET § 4; slutningen i § 3 står |

## D Enkelttall som ikke stemmer med egen kilde

| fil:linje | står | riktig | kilde | slutningen |
|---|---|---|---|---|
| ADDENDUM-01.md:249, :289 | «For historisk tekstvitenskap og energisystemmodellering finnes JATS-ruten ikke»; «i to av fire felt finnes ingen forlagsmerket JATS i det hele tatt» | et utvalgsnull (0/25 og 0/48 i utsnittet, § 5.2), ikke et fravær: energimodelleringsrammen har **21 + 30 verk hentbare via Europe PMC** (JATS) | ADDENDUM-08, tabellen l. 194–196 | parserbehovet for de fleste verk i de to feltene står; «ingen i det hele tatt» faller. ADR-0007 l. 16–20 gjentar påstanden |
| ADDENDUM-11.md:124 | regelfilen ble åpnet «25.09.2026 kl. 19:35» | **17:14:55 UTC** (19:14:55 CEST); økten gikk 17:14:53–17:35:26 UTC, og 19:35 CEST er øktens siste linje og filens mtime | øktutskriften, Vault `oppdrag-gjenvunnet/utskrifter/agent-abf6e3798610fb9c1.jsonl`, linje 1, 13 og 151 | ingen; lekkasjesjekken står |
| ADDENDUM-13.md:15 | «fire størrelsesordener billigere på verksnivå» | 100 verk mot 22 243 passasjer = faktor 222, **om lag to størrelsesordener** | samme linje | beslutningen om verksnivå står; gevinsten er mindre |
| ADDENDUM-13.md:84 | «Den er brukbar til å **velge bort** — et verk som scorer ÅPEN, var åpent i 2 av 2» | brukbar til å **velge ut**, ikke til å avskrive: feilen er ensidig mot LUKKET (l. 83), så det er ÅPEN-scoren som er pålitelig | samme § | setningen snudde sin egen slutning; den riktige står i neste ledd |
| ADDENDUM-15.md:4 | «**Ingen av de to rutene** når 90 % recall ved noe kuttpunkt» | **A2** når ikke 90 %; **A1** når 25/25 = 100 %, men bare ved 91,5 % av materialet (faktor 1,09×) | samme addendum l. 39–41 | kravet faller for begge i praksis; utsagnet var for sterkt for A1 |
| ADDENDUM-15.md:110 | etiketten «dropp resultat og innledning» \| 20 374 | 22 243 − 1 518 − 217 = 20 508. 20 374 dropper **resultat, innledning, sammendrag (55), konklusjon (41) og takk/ref (38)** | Vault `a1-seksjon-2026-09-26.json`; samme feil i `form-ruter/a2-kombinasjon-2026-09-26.json` | ingen: recall og faktor gjelder tallet, ikke etiketten |
| ADDENDUM-15.md:81, :66–68, :89–99 | kurven for n = 40, 200 og 400 («677 kandidater»), rolledekningen og «rollelistene er låst i `a2-naersok-2026-09-26.json`» | den deponerte `form-ruter/a2-naersok-2026-09-26.json` har bare n = 3–20 og ingen rollelister; n = 40 finnes indirekte i `a2-kombinasjon`; rollelistene ligger i `a2.py` | Vault, lest 28.09.2026 | **tall uten deponert inndata**: n = 200, n = 400 og rolletabellen kan ikke etterprøves før kurven og rolletabellen deponeres med sha |
| ADDENDUM-16.md:11 | «dømmes hver setning om lag fem ganger: 22 243 dommer for om lag 222 setninger per verk» | hver setning inngår i **≈ 1,67** tekstbiter; 222 er **tekstbiter** per verk, setningene er **668** | `data/port/spesifikasjon.json` (stride 3, vindu ±2, 66 833 setninger); ADR-0011 tillegg C1 | hypotesen står; mekanismen (redundans) var feil |
| ADDENDUM-17.md:63 | «585 vinduer, 9 tekniske feil, **219,1 min** dommertid» | **208,8 min** — tabellen l. 76 og «1 % mer veggtid» l. 79 er regnet på det | Vault `ekstraksjon/2026-09-26/a17-2p-mot-2d.json` → `p2.tid_min` | ingen; hva 219,1 var, er ikke funnet i noen kilde |
| ADDENDUM-19.md:154 | «27,4 % av de 22 243 tekstbitene og 22,5 % av de 2 173 flaggede er ikke prosa» | tallene er etter regelen slik den ble kjørt 26.09, **ikke reprodusert**; den versjonerte regelen (`ikkeprosa.py`, sha `63ed7345…`) gir **24,5 %** (5 455) og **20,8 %** (453) | MASTER-PATCH-2026-09-26 l. 60–67, rettelse 27.09 | ingen: poenget (en betydelig del er ikke prosa) står |

## E Foreldet status i låste filer

| fil:linje | står | nå | kilde |
|---|---|---|---|
| ADDENDUM-20.md:75–76 | «**Ingen modell-ID for koder 2.** … «Opus 5» er eierens opplysning» | modell-ID-en er gjenvunnet 27.09: `claude-opus-5`, ført i alle 61 API-svar | ADDENDUM-11 § 8; METODE § 4 |
| ADDENDUM-20.md:130, :134 | «Sonnet ble ikke målt i det hele tatt»; «Sonnet 5 med full regelfil krever kreditt som ikke finnes» | Sonnet 5 og full Haiku ble senere kjørt med koder 2s fulle regelfil: Sonnet κ 0,294 (n 319), Haiku 0,031 (n 316) | Vault `ekstraksjon/2026-09-26/a19-a20-full-regelfil.json`, `addendum-20/sonnet5-dommer.jsonl`; ADDENDUM-19 § 7.1 |

## F MASTER-PATCH-2026-09-26.md — påført i MASTER, ikke rettet i fila

| linje | står | riktig | kilde | slutningen |
|---|---|---|---|---|
| 98 | «**98 %** på de radene leseren ikke er i tvil om» | **97,6 % (41/42) [87,7–99,6]** i en **post hoc delgruppe**; lista er «kandidatliste (post hoc port)», og den preregistrerte porten falt (21 av 27) | ADDENDUM-23 § 7.2, ADDENDUM-22 § 10 | «Deteksjon: ja» må bære at porten som bestod, er post hoc |
| 99 | «164 805 kontekst-tokens **per bekreftet treff**» | 164 805 per treff koder c **meldte** (71 195 665 / 432); per treff bekreftet av uavhengig leser ved 85 %: **≈ 194 000** | Vault `arbeidsliste/koder-c-komplett.json` → `tokens_inn`, `tokens_per_treff` | prisen er om lag 18 % høyere enn oppgitt |
| 104 | løftbar andel 17,8 % | se B | — | — |
| 157–159 | «avhandling 1,200 fasit-treff/verk mot artikkel 0,208 = **5,77×**», felt 3,25×, leveringsform 1,53×; «Begrunnelsen er målt» | samme fil l. 128–132 har alt rettet nevneren til per 1 000 tekstbiter: type **2,22×**, felt **3,10×**, leveringsform **1,55×** (dør) | Vault `ekstraksjon/2026-09-26/b2-nevner.json` | utfallet (type og felt lever, leveringsform dør) står; tallene i begrunnelsen er fra før nevnerrettingen |

## Runde 2 — frys-lesning 2, 28.09.2026

**Grunnlag:** frys-lesning 2s funnregister, Vault
`zenodo/v0.4.0-bygg/frys2/frys-lesning-2-funn-2026-09-28.jsonl` (160 funn, sha256 `c219f274a7c2c845…`).
Hvert funn under er sjekket mot kilden før det er ført. Funnene i rettbare filer er rettet i filene selv,
med datert markør der fila er en logg; her står bare det som ikke kan rettes i fila.

### G Låsecommiten i «Filer låst med dette addendumet»

| fil:linje | står | riktig | kontroll | slutningen |
|---|---|---|---|---|
| ADDENDUM-24.md:97 | «Regnet på filene slik de står i commit `f38bd74`, commiten før låsen» | commiten før låsen `c0ec731` er **`78044f6`** (i tidsrekkefølge `f38bd74` → `78044f6` → `c0ec731`) | de tre repo-filene i § 7 (`prompts/leser-lokal-v1.txt`, `kjede/leser.py`, `classify/leser_port.py`) har samme sha256 i `f38bd74` og `78044f6`; de fire andre ligger utenfor git | **låsen holder**; bare utsagnet om hvilken commit er feil |
| ADDENDUM-25.md:110 | «Regnet på filene slik de står i commit `7972867`, commiten før låsen» | commiten før låsen `f19a3e3` er **`58b69fb`** (i tidsrekkefølge `7972867` → `66a68da` → `58b69fb` → `f19a3e3`) | alle sju repo-filene i § 9 har samme sha256 i `7972867`, `66a68da`, `58b69fb` og `f19a3e3` | **låsen holder**; sha-ene er regnet på `7972867`, og filene er byte-like i `58b69fb` |

Begge var «merk» i registeret. De føres her fordi en låst fil ikke kan rettes.

### H `REGEL-N3-v1.md` — «Gjelder fra: fase 3-kodingen»

`REGEL-N3-v1.md` er ikke et addendum, men den er festet med sha256 (`96cd8372…`, `docs/METODE.md` l. 94) og
sier selv at en ny versjon krever en ny fil (l. 98). Rettelsen står derfor her.

| fil:linje | står | riktig | kilde |
|---|---|---|---|
| REGEL-N3-v1.md:3 | «**Gjelder fra:** fase 3-kodingen.» | **Regelen er ikke i bruk i fase 3.** ADDENDUM-25 gir referanseinstansene «nøyaktig to filer»: regelfilen `koder2/koderegler-gjenvunnet.md` (sha256 `234695dd…`) og eget verk, og sperrer `docs/`. Kjedens leser bruker samme regelfil (`kjede.toml` [leser], `classify/fase3.py` `REGELFIL_SHA256`). Regelfilen inneholder ikke REGEL-N3 (0 treff), og verken koden eller ADDENDUM-25 viser til den. Regelen gjelder fra første koding som får den som inndata. | ADDENDUM-25 § 3 punkt 3, § 4 og § 9; `kjede.toml`; `src/gjenopptak/classify/fase3.py` |

**Slutningen endres:** løftet i l. 87 om at «en ny κ-måling etter fase 3 vil vise hvor mye den var verdt»,
kan ikke fase 3 innfri, fordi fase 3 ikke bruker regelen. Om og når regelen tas i bruk, avgjøres i en
`REGEL-N3-v2.md` eller et nytt addendum, ikke her. Fase 3-kjøringen er ikke rørt.

---

## Runde 4 — frys-lesning av det endelige v0.4.0-bygget, 30.09.2026

Fem lesere leste hver linje i 96 dokumenter i utkastet (16 008 linjer), register på Vault
`zenodo/v0.4.0-bygg/frys4/leser-1…5.jsonl`. Funnene i låste filer står her; **ingen låst fil er endret.**

### I ADDENDUM-10 og -11 fikk daterte tillegg etter låsen

ADDENDUM-10 § 7 og ADDENDUM-11 § 8 fikk 27.09.2026 daterte tillegg etter at filene var låst og deponert i v0.3.0 —
45 og 40 innsatte linjer, ingen fjernet (portstatus § 1). Det bryter regelen om at en låst fil aldri endres, og
står her som brudd, ikke som unntak. README sa at låste filer «are never edited»; den er rettet 30.09.

### J Funn som bør rettes

| fil:linje | står | riktig |
|---|---|---|
| ADDENDUM-02.md:61 | Europe PMC har ingen JATS for feltet (ADDENDUM-01 §5.2: 0 av 48), så P1 finnes ikke. | Låst. Samme utvalgsnull-som-fravær som KORRIGENDUM D retter i ADDENDUM-01:249/:289 (og ADR-0007): 0/48 er et utsnitt; energimodelleringsrammen har 21 + 30 verk hentbare via Europe PMC (ADDENDUM-08 l. 194–196, KORRIGENDUM:70). ADDENDUM-02:61 står ikke i KORRIGENDUM D; føres der. |
| ADDENDUM-02.md:90 | Tre ankere bryter regelen og er merket ⚠ — de er fra 2017 og 2019, og rammetilhørigheten er **ikke** verifisert | Låst. Bare to ankere er merket ⚠ og ligger i vinduet 2015–2020: H2 nr. 2 (2019, l. 100) og H7 nr. 2 (2017, l. 129); tabellen l. 165 sier «ett anker hver ⚠» for H2 og H7 = 2. Samme «tre ankere» i l. 286 og l. 298. Ikke i KORRIGENDUM; føres der. |
| ADDENDUM-10.md:95 | «**Proporsjonal trekking ville gitt tekstvitenskap 5 av de 150 leste treffene**» | Egen tabell l. 105 gir tekstvitenskap 8,2 % av de 2 173 flaggede → proporsjonal trekking ≈ 12 av 150 (179 av 2 173, FELTGUIDE.md:54–56). «5» er fra delkjøringen etter 18 964 av 22 243 dømte (LAERDOM.md:265, § 15, 2026-09-17), sitert uten at tilstanden oppgis. Låst — ikke i KORRIGENDUM; bør føres der |
| ADDENDUM-14.md:34 | «**Frøsettet:** de 55 ekte treffene fra recall-sett 1 (28) og 2 (27), som alt har manuell fasit.» | Recall-fasiten (sett 1 og 2, 55 treff) er kodet av en Claude-økt, ikke for hånd av et menneske (INNHENTET-2026-09-26-en-koder.md:64–75, § 4; KORRIGENDUM-2026-09-28-frys-v0.4.0.md:64, seksjon C). INNHENTET § 4 fører bare ADDENDUM-06:18 og :118; «manuell fasit» her er samme utsagn og mangler. Låst — b |
| ADDENDUM-15.md:133 | Formen er bare ikke *uttrykt* i hver fjerde av dem. | LÅST. 4 av 25 treff mangler ordene (samme fil l. 5, l. 97; taket 21/25 = 84 %, l. 94–95), altså 16 % = om lag hver sjette, ikke hver fjerde (25 %). Ikke i KORRIGENDUM. |
| ADDENDUM-16.md:20 | Engelsk ledetekst fordi korpuset er 52,9 % engelsk og resten romansk/tysk (ADDENDUM-14 §2) | LÅST. ADDENDUM-14 §2 (l. 18–19): 52,9 % engelsk, 13,1 % fransk, 12,0 % spansk, 2,7 % tysk og 17,9 % for korte å avgjøre; «klart et annet språk» er 27,7 %, ikke hele resten (47,1 %). |
| ADDENDUM-16.md:34 | et vindu på om lag 2 900 anslåtte tokens pluss prompt overskred 4096 reelle tokens, og halen ble kuttet bort. Med 8192 gir samme vindu `prompt_eval_co | LÅST. 3013 < 4096: vinduet kan ikke ha overskredet 4096 reelle tokens hvis samme vindu gir 3013 (også l. 48–49). Enten var vinduene ulike, eller trunkeringsforklaringen er feil. Valget av 8192 står. Ikke i KORRIGENDUM. |
| ADDENDUM-17.md:64 | `ekstraksjon/2026-09-26/a17-2p-mot-2d.json`. Begge står ved siden av hverandre, som §3 krever | LÅST. Fila har ingen rad i MANIFEST-VAULT.md (0 treff på «a17»/«2p-mot»; ekstraksjon/2026-09-26 har ellers rader, l. 2674–2749), og det har heller ikke 2′-loggen. Hele utfallstabellen (l. 67–76) og METODE:222 hviler på den. KORRIGENDUM D (l. 78) leste fila på Vault 28.09, så den finnes: før den i ma |
| ADDENDUM-17.md:84 | tok med seg innhold ekstraksjonen ville brukt: tre vinduer forsvant, og med dem to kjente treff. | LÅST. Tabellen i samme fil (l. 69) gir 595 → 585 = −10 vinduer, og METODE:222 gir 598 → 588 (også −10). Ingen kilde i settet gir tre. Ikke i KORRIGENDUM (der står bare 219,1 min, l. 63). |
| ADDENDUM-18.md:169 | «**Sonnet 5 med full regelfil er ikke målt.** … Sonnet startet aldri. Den halvdelen av sammenlikningen står altså åpen» | Sonnet 5 er senere kjørt med koder 2s fulle regelfil: κ 0,294 (n 319) (KORRIGENDUM-2026-09-28-frys-v0.4.0.md:86; MANUSKRIPT-FAKTA-2026-09-28.md:152). KORRIGENDUM E fører samme foreldede utsagn for ADDENDUM-20:130/134, men ikke dette. Låst — bør føyes til KORRIGENDUM E. |
| ADDENDUM-22.md:76 | **b) er uavgjort.** ADDENDUM-20 stoppet på `Your credit balance is too low to access the Anthropic API`; Sonnet 5 startet aldri. | Foreldet: Sonnet 5 og full Haiku ble senere kjørt med koder 2s fulle regelfil — Sonnet κ 0,294 (n 319), Haiku 0,031 (n 316) (KORRIGENDUM-2026-09-28-frys-v0.4.0.md:86, som fører samme foreldelse for ADDENDUM-20:130/134, men ikke for denne linjen). b) faller altså også; valget av rute c står. Låst — f |
| ADDENDUM-23.md:118 | Tvilsmerket forutsier altså hvor to lesere skiller lag. En liste sortert på `tvil: false` ville hatt presisjon nær 98 % på dette utvalget. | LÅST. 41/42 = 97,6 % [87,7–99,6] i en post hoc-delgruppe med n = 42. Forskjellen mot 75,9 % er ikke testet, og andre prediktorer er ikke sammenlignet (FAKTA:259–260, METODE:368–370, :445–447). KORRIGENDUM F retter samme «98 %» i MASTER-PATCH l. 98, men ikke kilden her. |
| MASTER-PATCH-2026-09-26.md:86 | §8 fører opphavet (øktutskrift, linje 13, 25.09 kl. 19:35) | Datert patch. Regelfilen ble åpnet 17:14:55 UTC (19:14:55 CEST); 19:35 CEST er øktens siste linje og filens mtime (KORRIGENDUM:71, rettelsen av ADDENDUM-11:124). Samme feil står her, men KORRIGENDUM F (l. 88–95) fører den ikke; føres der. |
| MASTER-PATCH-2026-09-26.md:123 | **«Én koder» står i PREREG-v1 § 4 og ADDENDUM-06**, innhentet av ADDENDUM-11 siden 25.09.2026. | Datert patch. «Én koder» står i PREREG-v1 § 9 punkt 1 (PREREG-v1:99–101), som samme patch sier i l. 137 og INNHENTET:10 fører. § 4 er «Utvalg». Ikke i KORRIGENDUM F; føres der. |

### K Småfunn («merk»)

28 funn i låste filer er ført som «merk» i registeret og ikke gjentatt her, blant dem: ADDENDUM-02.md:14; ADDENDUM-02.md:269; ADDENDUM-02.md:287; ADDENDUM-06.md:101; ADDENDUM-06.md:141; ADDENDUM-06.md:156; ADDENDUM-10.md:114; ADDENDUM-11.md:136; ADDENDUM-11.md:63; ADDENDUM-12.md:97; ADDENDUM-14.md:18; ADDENDUM-15.md:143; ADDENDUM-18.md:153; ADDENDUM-18.md:17; ADDENDUM-18.md:4; ADDENDUM-19.md:44; ADDENDUM-20.md:8; ADDENDUM-21.md:107; ADDENDUM-21.md:9; ADDENDUM-22.md:219; ADDENDUM-22.md:223; ADDENDUM-22.md:322; MASTER-PATCH-2026-09-26.md:35; MASTER-PATCH-2026-09-26.md:79; PREREG-v1.md:104; PS-246-KRITERIUM.md:14; REGEL-N3-v1.md:60; saker-SAK-09b-KRITERIUM.md:70.

## Hva som ikke er gjort

Ingen låst fil og ingen MASTER-fil er endret. `LOCKED_SHA256` for PREREG-v1 og ADDENDUM-01..09 er
uendret. Kryssjekken (`src/gjenopptak/kryssjekk.py`) regner nå hvert `ADDENDUM-*.md` og hver
`MASTER-PATCH-*` som låst, og viser treff i dem for seg uten å feile; denne filen er unntatt fordi
oppgaven dens er å sitere det som sto. Pekt til fra README («Statements superseded in locked files»).

**Runde 2:** ingen låst fil er endret, og `REGEL-N3-v1.md` er uendret (sha256 `96cd8372…`). Den ene
MASTER-fila som er rørt, `docs/patch/MASTER-2026-09-28-koder4.md`, har bare fått en datert merknad øverst om
to steder som ikke skal påføres slik de står; patchteksten er ikke omskrevet.
