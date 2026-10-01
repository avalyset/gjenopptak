# v0.4.0 — portstatus før publisering

**28.09.2026, bygget på nytt 30.09.2026 med fase 3-utfallet og 01.10.2026 med manus v2.8 og MASTER v0.4.** Publisering er irreversibel og autoriseres av eieren på
grønne porter (`docs/ZENODO.md`). Ingen skrivekall mot Zenodo er gjort; det finnes ikke noe utkast hos
Zenodo. Byggeren er `python -m gjenopptak.utgivelse --versjon 0.4.0 --forrige 22976464`; utkastet ligger på
Vault i `zenodo/v0.4.0-utkast/`, manifestet med sha256 per fil i `zenodo/v0.4.0-bygg/UTGIVELSE-0.4.0.json`.

## 1 Filkart mot v0.3.0 (38 filer)

Regnet av byggeren på det bygde utkastet, mot Zenodos md5 for v0.3.0 (record 22976464). Tallene regnes om
ved hver ny bygging; commit og tidspunkt står i `UTGIVELSE-0.4.0.json`.

| | antall |
|---|---|
| filer i v0.4.0 | **98** — Zenodo tillater høyst 100 per post; tre nye grupper ligger i zip (under) *(sto 30.09: 116, før grensen ble funnet ved opplasting 01.10)* |
| uendret fra v0.3.0 | 18 |
| endret | 18 — ADDENDUM-10 og -11, CITATION.cff, HERON v1, LAERDOM, LICENSE-DATA, MANIFEST-VAULT, MANUSKRIPT-v0.1, PS-246-RESULTAT, README, RESULTAT-PORT-v1, claims.jsonl, ADR-0001, -0002, -0007, -0008, -0009 og git-bundlen |
| nye | 62 — bl.a. manuskriptutkast v2.8 (det nyeste), `faktasjekk-manuskript.zip` (sju rapporter), `saker.zip` (åtte sakfiler med register, katalogstrukturen bevart), `oppdrag.zip` (seks leseroppdrag, byte-identiske), NAVNEKONTROLL, RELEASE-NOTES, ADDENDUM-12–25, ADR-0011–0014, METODE, LISENS-PER-VERK, LISENSAUDIT, TIDSSTEMPEL, REGEL-N3-v1, KORRIGENDUM, resultatnotatene for ADDENDUM-24 og -25, regelfilen, `ots-kvitteringer.zip` (42), `blindfiler-indeks.zip` (31 blindfiler), kildetarballen for 0.4.0, **fase 3-utfallet** (§ 1.1), nøklene til de ferdige målingene (§ 6) og koder 2-sammenligningen uten passasjetekst (§ 6) |
| fjernet | 2 — `gjenopptak-src-0.3.0.tar.gz`, erstattet av tarballen for 0.4.0; `koder2-sammenlikning.json`, erstattet av versjonen uten passasjetekst (§ 6) |
| utelatt fra repoet | 12 — `INSTRUKSER-v1.2/-v1.3`, `BYGGEPLAN`, `ROADMAP`, manuskriptutkastene v2–v2.7 (ekskluderingsliste versjon 1; `docs/patch/**` er også utelatt) |

**ADDENDUM-10 og -11 er endret etter at de ble deponert i v0.3.0**, men bare ved tillegg: `git diff`
mot den deponerte versjonen gir 45 og 40 innsatte linjer og **null fjernede**. Tilleggene er daterte
seksjoner (gjenvunnet regelfil, modellsignatur, fordelingsrettelse). At en låst fil har fått tillegg, er
likevel i strid med «en låst fil endres aldri» slik INNHENTET og KORRIGENDUM formulerer regelen; det står
som funn i runde 2 (§ 3.2).

**Fase 3 er målt (30.09.2026):** port (1) bestått, 85 av 100 [76,7–90,7]; lista heter «arbeidsliste (prospektiv
port)» (`docs/RESULTAT-ADDENDUM-25.md` § 1). *(Sto 28.09: «Fase 3 er ikke ferdig … Avsnitt som venter på det, er
merket «leses etter ADDENDUM-25-utfall»». **Merket ble aldri satt** i noe dokument; runde 3 avgrenset avsnittene
maskinelt i stedet, § 3.3.)*

### 1.1 Fase 3 i depositumet (nytt 30.09.2026)

| fil i depositumet | kilde på Vault | hva |
|---|---|---|
| `fase3-maaling.json` | `fase3/maaling-fase3.json` | portene (1) og (2), låst `fase3.py` |
| `fase3-rapport.json` | `fase3/rapport-fase3.json` | tilleggstallene i ADDENDUM-25 § 6–7 |
| `fase3-register.jsonl`, `fase3-register-header.json` | `fase3-kjede/` | 673 rader, «arbeidsliste (prospektiv port)», skrevet av det rettede registerleddet |
| `fase3-referanse-nokkel.jsonl` | `fase3/referanse/NOKKEL-referansesett.jsonl` | referansesettets 104 treff (fasiten for recall) |
| `fase3-oppdrag-presisjon.md` (i `oppdrag.zip`), `fase3-presisjon-nokkel.jsonl`, `fase3-presisjon-verdikter.jsonl` | `fase3/presisjon/` | presisjonsportens oppdrag, kobling og verdikter |
| `fase3-modell-fra-utskrifter.json` | `fase3/utskrifter/` | modell-ID per leserøkt fra øktutskriftene |
| `fase3-kjede-nokkel.jsonl` | `fase3-kjede/nokkel.jsonl` | blindnøkkelen til fase 3s leserøkter (nøkkelregelen, § 6) |
| `fase3-leser-verdikter.zip` | kjøringens katalog | 12 verdiktfiler (id, treff, klasse, begrunnelse, tvil) og to fullføringslogger |
| `blindfiler-indeks.zip` | + 15 fase 3-blindfiler | indeks uten tekst: 4 107 leser-, 385 rest- og 100 presisjonsrader |

**Ingen tekstbiter:** unionen, blindfilenes tekst og øktutskriftene står utenfor, som før. *(Sto 30.09 før
eierens avgjørelse: «Ett avvik fra § 6 til eierens avgjørelse» om de to fase 3-nøklene. Avgjort samme dag ved at
nøkkelregelen ble omformulert, § 6.)*

## 2 Portene

| port | status | grunnlag |
|---|---|---|
| filkart | **grønn** | alle 38 fra v0.3.0 gjort rede for, § 1; regnet på det endelige bygget 30.09, ekskluderingsliste versjon 1 (12 filer utelatt, `RELEASE-NOTES-v0.4.0.md`) *(sto 29.09: 9 utelatt)* |
| navnekontroll | **grønn** | 0 evaluerende i rettbare filer, 4 i låste; fotnote 83 parafrasert (`NAVNEKONTROLL-2026-09-29.md`) |
| frys-lesning, runde 1 (hver linje, 82 filer) | rettet | 210 funn, 29 blokkerende, § 3.1 |
| frys-lesning, runde 2 (endrede og nye filer) | se § 3.2 | 160 funn, 6 blokkerende |
| kryssjekk (`gjenopptak.kryssjekk`) | grønn, **men ikke bevis** | 0 umerkede foreldede verdier i rettbare filer; den fanger bare størrelser den kjenner, og runde 2 fant at den ikke fanger «2 of 19» i manuskriptet |
| scrub over alle refs og hele historikken | **gul — ett valg er eierens** | § 4 |
| sha-referanser i dokumentene | **gul** | § 5 |
| OpenTimestamps oppgradert til fullt bevis | **grønn** (13:50) | 42 av 42 fullstendige, også ADDENDUM-24 og -25; uoppgraderte kvitteringer bevart i `repo/kanon/ots-for-oppgradering-2026-09-28/`, nye sha i manifestet |
| G3: materiale utenfor git sikret | **grønn** | § 6 |
| lisens | **grønn** | blindfilene som indeks, avgjort av eieren, § 7 |
| manifest | **grønn etter runde 2** | § 6 |
| fase 3 målt | **grønn** | port (1) 85/100 mot 0,70; recall uten terskel; RESULTAT-ADDENDUM-25 § 1 |
| registerleddet rettet — eneste endring i et ledd etter låsen (referanseporten i `cli.py` er ført i RESULTAT § 0.3) | **grønn** | `ledd.py` `07fc3a77…` → `39f8b9de…`, radene uendret, test; RESULTAT-ADDENDUM-25 § 0.8 |
| frys-lesning, runde 3 (avsnitt som avhenger av fase 3) | **rettet** | 16 funn, 3 blokkerende, alle blokkerende og bør-rettes rettet, § 3.3 |
| **frys-lesning, runde 4 (a)–(f), hver linje i bygget 30.09** | **rettet** | 175 funn + ett G3-funn, 6 blokkerende; alle blokkerende og alle bør-rettes i rettbare filer rettet; låste i KORRIGENDUM J; manus som kjent rest, § 3.4 |
| navnekontroll, igjen 30.09 | **grønn** | 0 evaluerende i rettbare filer, 4 i låste — som 29.09 |
| faktasjekk av manus v2.7 (de ni stedene); v2.8 = v2.7 + klyngefølsomheten, ingen ny runde | **grønn med kjent rest** | 7 av 9 rettet, 2 kjent rest; frys-lesning 4 la til 6 «bør rettes» og 3 «merk» i manus, ført som kjent rest uten ny runde (`FAKTASJEKK-MANUSKRIPT-v2.7-2026-09-30.md`) |

## 3 Frys-lesningene

### 3.1 Runde 1

Fire lesere, hver med sin bunke, leste **hver linje** i de 76 repo-filene og de seks Vault-inndatafilene
(12 408 linjer), mot (a) interne motsigelser, (b) tabellverdier, (c) metrikk-overclaim, (d) tall uten
deponert inndata, (e) foreldet status, (f) motsigelser mellom dokumenter, og (g) navnepolicy «verk, ikke
person». Register på Vault: `zenodo/v0.4.0-bygg/frys-lesning-funn-2026-09-28.jsonl` (sha256
`22835a0ec6170707f8887c6f2aaf9d7e4a5880f22c489da2a940d7ec165d7123`).

| | blokkerer | bør rettes | merk | sum |
|---|---|---|---|---|
| runde 1 | 29 | 79 | 102 | 210 |

**De blokkerende, etter rot** — alle rettet i `66a68da` eller ført i korrigendumet:
κ = 0,812 sto med intervallet til κ = 0,826 i fem filer; løftbar andel var regnet med alle treff som nevner,
ikke avklarte (ADDENDUM-05 § 4); foreldede sha-er i MANUSKRIPT-FAKTA og REGISTER-SAKER; foreldet «én koder»
og M2 uten koderidentitet i README; enkelttall som ikke stemte med egen kilde (ADR-0013 2–1–3, «fire av tolv»,
«~93 folier», «422 sitater», METODEs koder 4-tabell, datoen for koder 2s økt); og tre overclaim
(SAKBEHANDLING «98 %», ADR-0011 «beslutningen står», H1-kontrollen som «strongest liftable candidate»).
Funn i låste filer står i `docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md`.

### 3.2 Runde 2

Fire nye lesere leste **hver linje** i de 33 filene som var endret siden runde 1 og de 7 nye dokumentene, pluss
REGEL-N3-v1 og koder 4-patchen (43 filer, 7 713 linjer), mot de samme kategoriene, og kontrollerte for hvert
runde 1-funn i sine filer at det var **riktig** rettet. Register på Vault:
`zenodo/v0.4.0-bygg/frys2/frys-lesning-2-funn-2026-09-28.jsonl` (sha256
`c219f274a7c2c8451dd0388273659bc685c6c8fd822170ce17bc5808db6355e5`).

| | blokkerer | bør rettes | merk | sum |
|---|---|---|---|---|
| runde 2 | 6 | 43 | 111 | 160 |

58 av de 160 er runde 1-funn som var ført videre: de fleste «merk» som ikke var rettet, og **tre som var rettet
men ble foreldet igjen av senere commits**. De 6 blokkerende:

1. **Foreldede sha-er, igjen** — MANUSKRIPT-FAKTA l. 40 og 47, REGISTER-SAKER l. 10. Mønsteret er strukturelt:
   en sha-tabell over dokumenter som fortsatt endres, blir foreldet ved hver commit som rører dem. Tabellene
   regnes derfor om **sist**, etter alle andre rettelser, og kontrolleres maskinelt mot disk.
2. **Filkartet i dette dokumentet** var fra en tørrkjøring (85 filer) mens utkastet var bygd (96). Rettet i § 1.
3. **«422 sitater» sto igjen** i LISENSAUDIT § 3, etter at § 2 og LICENSE-DATA hadde trukket tallet.
4. **ADR-0012 sa at arbeidshistorikken «ikke blir offentlig»** — men hver Zenodo-versjon siden v0.1.0 har
   hatt `git bundle --all`. Se § 4 for valget det reiser.

**Rettet 28.09.2026 etter runde 2:** alle 43 «bør rettes» og de blokkerende i LISENSAUDIT og ADR-0012 i
rettbare filer, med datert markør der fila er en logg; tre funn i låste filer ført i KORRIGENDUM, seksjon
«Runde 2»; ett avvist (LICENSE-DATA om tekstbitene i manifestet — løst av manifestføringen i § 6 før rettingen);
sha-tabellene i MANUSKRIPT-FAKTA § 0 og REGISTER-SAKER regnet om sist og kontrollert mot disk. Kryssjekken
grønn etterpå.

**Utenfor depositumet, men viktig:** koder 4-patchen til MASTER (`docs/patch/MASTER-2026-09-28-koder4.md`)
bærer koder 1-kolonnen og slutningen «tettere og oftere bedømbare» som METODE trakk 28.09. Den er merket og
skal ikke påføres slik den står.

### 3.3 Runde 3 — avsnittene som avhenger av fase 3-utfallet (30.09.2026)

**Avgrensning:** merket «leses etter ADDENDUM-25-utfall» finnes ikke i noe dokument. Avsnittene er derfor funnet
maskinelt i de 88 repodokumentene byggeren tar med, med mønsteret `fase 3 | phase 3 | ADDENDUM-25 | pågår |
kjøringen går | [pending] | venter på | ikke målt ennå | silrecall | recall … ikke målt | arbeidsliste | worklist |
prospektiv`: **115 avsnitt i 28 filer.** Lest i full lengde: de 41 i levende dokumenter. Ikke lest som funn: de
daterte faktasjekkrapportene v2–v2.4 (radene siterer manusets gamle «[pending]»), de låste ADDENDUM-22, -23 og -25
(teksten er før utfallet med vilje), og de fire filene som ble skrevet mot utfallet samme dag (RESULTAT-ADDENDUM-25
§ 1, FAKTA § 9, manus v2.6 — egen faktasjekk — og faktasjekkrapporten). Register på Vault:
`zenodo/v0.4.0-bygg/frys3/frys-lesning-3-fase3-avsnitt-2026-09-30.jsonl` (sha256 `07fbd62d72ea0f71…`).

| | blokkerer | bør rettes | merk | sum |
|---|---|---|---|---|
| runde 3 | 3 | 6 | 7 | 16 |

| nr | sted | kategori | funn | tiltak |
|---|---|---|---|---|
| 1 | UTGIVELSE-v0.4.0-PORTSTATUS.md:28 | blokkerer | «Fase 3 er ikke ferdig … merket «leses etter ADDENDUM-25-utfall»» — utfallet er målt, og merket ble aldri satt i noe dokument (0 forekomster utenfor portstatusen selv) | rettet: § 1 og § 3.3 i portstatusen |
| 2 | RESULTAT-ADDENDUM-25.md:3 | blokkerer | statuslinja «kjøringen pågår … ikke målt» | rettet med datert merke |
| 3 | METODE.md:317 | blokkerer | silrecall «skal ikke oppgis … før noen har lest blindt i en ramme silen ikke har sett» — fase 3 er den lesningen | datert tillegg: 95/104 for 20 arkeologiverk; «ikke målt» står for de første 100 |
| 4 | RESULTAT-ADDENDUM-25.md § 1.7 | bør rettes | «hodet er ikke skrevet» | rettet: skrevet av det rettede leddet (§ 0.8) |
| 5 | UTGANG.md:103 | bør rettes | eksempelhodet (røyktesten 27.09, tre forbehold) består ikke skjemaet og svarer ikke til noen deponert fil; leser_datert, silrecall, verksnivaa og navnepolicy uforklart | byttet til fase 3-hodet ordrett, med forklaringene og verksnivå-merknaden |
| 6 | README.md:210 | bør rettes | «Two registers exist» — fase 3-registeret mangler | tre registre, med portnavn og recall |
| 7 | FELTGUIDE.md:122 | bør rettes | recall for et nytt felt «ikke målt i det hele tatt» | datert tillegg: fase 3 viser metoden; målt for arkeologi |
| 8 | decisions/0014:45 | bør rettes | «Kjedeinstansene startes i repoet» — fase 3s lesere startet i worktreet etter gjenopptakene | datert merknad |
| 9 | decisions/0013:77 | bør rettes | «Fase 3 rapporterer vilkårsfordelingen» — ADDENDUM-25-kjøringen hadde ingen saker | datert merknad |
| 10 | decisions/0014:82 | merk | «Fase 3-kjøringen som går» | datert merknad: ferdig; registerleddet kjørt fra arbeidstreet |
| 11 | LAERDOM.md § 45 | merk | «Ikke gjort: leddene selv er ikke rettet» | datert merke: registerleddet rettet |
| 12 | LAERDOM.md § 46 | merk | «Ikke gjort: registerhodet» | datert merke: skrevet |
| 13 | NAVNEKONTROLL-2026-09-29.md:17 | merk | skanneren «flyttes til src/ når fase 3 er ferdig» — fase 3 er ferdig, flyttingen er ikke gjort | ikke rettet: åpen post (§ 8) |
| 14 | NAVNEKONTROLL-2026-09-29.md:61 | merk | registerets notes-felt «røres ikke mens fase 3 går» | ingen endring: fortsatt urørt |
| 15 | B5-PORTSTATUS.md:102 | merk | «kandidatliste, ikke en arbeidsliste» — datert portstatus (B5), sann for sin tid | ikke rettet: logg |
| 16 | MASTER-PATCH-2026-09-26.md:97, 153 | merk | datert patch; 98 %, 164 805 og 17,8 % står allerede i KORRIGENDUM | ikke rettet: låst/datert |

**Rettet:** alle 3 blokkerende og 6 bør rettes, og 3 av 7 merk, med datert markør. **Ikke rettet:** nr. 13–16
(åpen post, logg, låst). **Observert utenfor runden:** README viser til `kandidat432/8-register.jsonl`, men
kandidatlista på 432 er ikke i depositumet (verken i v0.3.0 eller v0.4.0; `data/` er utenfor git).

### 3.4 Runde 4 — hver linje i det endelige bygget, (a)–(f) (30.09.2026)

Fem lesere leste **hver linje** i de 96 dokumentene i utkastet (16 008 linjer; `MANIFEST-VAULT.md` er en maskinskrevet
sha-tabell og kontrolleres i § 6), direkte fra `zenodo/v0.4.0-utkast/`, mot kategoriene (a)–(f) i INSTRUKSER § 5.
Registre på Vault: `zenodo/v0.4.0-bygg/frys4/leser-1…5.jsonl` (sha256 `c51207d6…`, `3c52bb4d…`, `464fc4f4…`,
`295b3d4d…`, `a43138bb…`). Hvert funn ligger hos leseren som eier fila (kontrollert maskinelt).

| | blokkerer | bør rettes | merk | sum |
|---|---|---|---|---|
| runde 4 | 5 | 56 | 114 | 175 |
| G3 (§ 6) | 1 | — | — | 1 |

**De seks blokkerende, alle rettet:** README sa at låste filer «are never edited» (ADDENDUM-10 og -11 fikk tillegg
etter låsen); portstatusens filkart, manusrad og portrad var fra et tidligere bygg (tre funn); sakregisterets sha for
SAK-11 var foreldet; og koder 2-sammenligningen bar 16 ordrette passasjeutdrag (§ 6).
**Det viktigste bør-rettes-funnet er faglig:** de 104 referansetreffene i fase 3 ligger i 12 av 20 verk, 51 i ett.
Wilson over treffene er for smalt; følsomheten uten det verket (84,9 % og 71,7 %) står nå i RESULTAT § 1.2, FAKTA § 9,
METODE og release notes.
**Rettet:** alle 5 blokkerende og alle 36 bør-rettes-funn i rettbare filer (35 steder; to lesere fant det samme), med
datert markør; 14 bør-rettes og 28 merk i
låste filer ført i KORRIGENDUM, seksjon I–K; 6 bør-rettes og 3 merk i manus v2.7 ført som kjent rest, ingen ny runde.
**Ikke rettet:** de 83 merk-funnene i rettbare filer (register på Vault), bortsett fra de få som ble rettet sammen med
et bør-rettes-funn på samme sted.

## 4 Scrub — og ett valg som er eierens

Over trærne til alle refs (`main`, `offentlig`, `v0.3`, `origin/main`), over alle 525 blobs i historikken,
over commit-metadata og over hver fil i utkastet, også inni zip-filene:

* **HEAD-treet og utkastet:** forretnings-e-post i ADDENDUM-03 (låst; kontaktadressen i OpenAlex-kallet); et
  engelsk ord som scrubben flagger (mønster 11), i B5-PORTSTATUS og ADR-0012, der ordet selv drøftes;
  absolutte hjemmestier i de fire oppdragsfilene som deponeres ordrett (inndata til låste målinger — en
  redigert kopi ville hatt en annen sha enn den som ble lest).
* **Historikken:** en privat e-postadresse i en tidligere versjon av `harvest/recallset2.py`, fjernet i
  `44c8235` (25.09). **Den er alt publisert** i git-bundlene i v0.1.0–v0.3.0.

**Valget:** `gjenopptak-git-history.bundle` er `git bundle --all`. Utover e-postadressen bærer historikken
etter v0.3.0 **commit `37d7187` (27.09), der SAK-09c har fullt navn og institusjon** for forfatteren av
verket saken gjelder — fjernet fra filene i `0b4c979`, men ikke fra historikken. v0.3.0-bundlen ble laget
26.09 og har den ikke; **v0.4.0 ville publisert den for første gang.** Alternativene er eierens: deponere
`--all` slik byggeren gjør nå; deponere bundlen for v0.3.0 uendret og la historikken etter den ligge bare på
Vault; eller noe tredje. Byggeren er ikke endret.

**Avgjort 29.09.2026: historikkbundlen er med** (`--all`), med setningen om revisjonen 28.–29.09 under
navnepolicyen i `docs/RELEASE-NOTES-v0.4.0.md`. Bundlen bærer også det ordrette sitatet av fotnote 83 i Heron v2
(fra `0eaff6b`, 26.09, etter v0.3.0), som i filene er erstattet med parafrase 29.09; sitatet er alt publisert
gjennom `offentlig` (`5fcb353`). Navnekontrollen: `docs/NAVNEKONTROLL-2026-09-29.md`.

**Kjørt på nytt 30.09.2026 over det endelige bygget** — trærne til alle fire refs (`main`, `offentlig`,
`origin/main`, `v0.3`), alle blobs i historikken, commit-metadata og hver fil i utkastet, også inni zip-filene og
kildetarballen: **ingen nøkler, tokens, passord eller PEM-blokker.** Samme treff som over, og to til å redegjøre for:
(1) **forretnings-e-posten står som author og committer i commit-metadataen** (i alle commits, 213 ved skanningen) — det er attribusjon
(INSTRUKSER § 12, F2), og den er publisert i alle tidligere bundler og på GitHub; (2) hjemmestien står også i
`fase3-oppdrag-presisjon.md` (i `oppdrag.zip`), som deponeres ordrett av samme grunn som de fire andre oppdragene. Bundlen bærer i
tillegg worktree-refen til låsecommiten `f19a3e3`.

## 5 sha-referanser

Alle heksstrenger på 12–64 tegn i dokumentsettet er slått opp mot sha256 av hver blob i git-historikken,
hver fil på Vault utenom fulltekstene, hver rad i MANIFEST-VAULT og hver commit. I runde 1 traff 145 av 172;
av de 27 var 13 ikke sha-er. Resten: **fem mellomtilstander av registeret** i REGISTER-SAKER er ikke bevart
(bare sluttilstanden `c6895202…` finnes); eksempelhodet i UTGANG svarte ikke til noen fil *(rettet 30.09: byttet til fase 3-hodet ordrett, runde 3)*; kildepakken
`blockmodeling_1.1.8.tar.gz` i SAK-09b er ikke sikret. De foreldede tabellene regnes om sist (§ 3.2).

## 6 G3 og manifestet

Sammenlignet på sha256 av innhold, ikke på filnavn. **Sikret 28.09:**

| hva | hvor på Vault | antall |
|---|---|---|
| lokale filer i repoets `data/` som ikke fantes på Vault — bl.a. `kandidat432/3-dommer.jsonl` og `1-hentet.jsonl` (inndata til 432-lista), SAK-14s Perseus- og Scaife-hentinger (inndata til 87,8 %), testkjøringene | `lokal-sikret-2026-09-28/` | 151 |
| sju blindfiler som bare lå i `data/arbeidsliste/` | `arbeidsliste/blind/` | 7 |
| tre oppdrag med sperreliste, gjenvunnet ordrett fra underinstansenes utskrifter, + opphav | `oppdrag-gjenvunnet/` | 4 |
| kildeutskriftene de tre er gjenvunnet fra | `oppdrag-gjenvunnet/utskrifter/` | 3 |
| den innsendte preprint-PDF-en (sha `5e0cf29b…`), som bare lå på Desktop | `manuskript/preprint-innsendt/` | 1 |

**Manifestet, runde 2:** 408 filer på Vault hadde ingen rad for sitt innhold — fase 3s trekk-, hente- og
referansefiler, `presisjonssett/`, `logs/port/` (der de 22 243 tekstbitene ligger, som LICENSE-DATA sier står i
manifestet), `logs/l3-poc/` og falsifiseringen. Alle er ført. **Speilet (`gjenopptak.speil`) oppdaterer
`resultat/` uten å føre manifestet**; åtte speilede filer manglet rad for gjeldende innhold og er ført. Kopien
av faktafila i `manuskript/` er foreldet (verken morgenens eller dagens versjon); den er ikke overskrevet.

**Fortsatt bare utenfor git og utenfor Vault:** koder 4s oppdrag (Fable 5.1 i chat — finnes ikke som fil);
kildepakken i SAK-09b; registerets mellomtilstander (tapt). **Utenfor git, på Vault, og bevisst utenfor
depositumet:** fulltekster, tekstbiter, dommer- og ekstraksjonslogger, blindfilenes tekst. *(Sto til 30.09.2026:
«… blindfilenes tekst, nøklene.»)*

**Nøkkelregelen, omformulert 30.09.2026 (eierens avgjørelse):** **en nøkkel holdes utenfor depositumet til
målingen den blinder er ferdig og rapportert; deretter deponeres den.** Anvendt på nøklene til blindfilene
depositumet bærer som indeks:

| nøkkel på Vault | blinder | ferdig og rapportert? | i v0.4.0 |
|---|---|---|---|
| `presisjonssett/port-presisjonssett-nokkel.jsonl` (og kopien fra 20.09, samme sha) | de 320 — koder 1, 2, 4 **og ADDENDUM-21 (koder 3)** | **nei: ADDENDUM-21 er preregistrert og ukjørt på samme blindfil** | **holdes ute** |
| `arbeidsliste/nokkel.jsonl` | leserøktene over de 2 844 (ADDENDUM-22) | ja, ADDENDUM-22 § 9–10 | `arbeidsliste-nokkel.jsonl` |
| `arbeidsliste/presisjon-100-nokkel.json` | den post hoc presisjonsporten (ADDENDUM-23) | ja, ADDENDUM-23 § 7 | `arbeidsliste-presisjon-100-nokkel.json` |
| `fase3-kjede/nokkel.jsonl` | fase 3s leserøkter | ja, RESULTAT-ADDENDUM-25 § 1 | `fase3-kjede-nokkel.jsonl` |
| `fase3/presisjon/nokkel-presisjon.jsonl` | fase 3s presisjonsport | ja, RESULTAT-ADDENDUM-25 § 1.1 | `fase3-presisjon-nokkel.jsonl` |
| `fase3/referanse/NOKKEL-referansesett.jsonl` | fasiten for recall (sil og leser) | ja, RESULTAT-ADDENDUM-25 § 1.2 | `fase3-referanse-nokkel.jsonl` |

Nøkler til blindinger som ikke selv er i depositumet — verksnivå-blindverket, ekstraksjonens Q-100 (ADDENDUM-16)
og testkjøringene `royk`, `b6-test`, `readme-test` — er ikke vurdert her; de følger regelen når blindingen
deponeres. Ingen av nøklene bærer passasjetekst.

**G3 på det endelige bygget, 30.09.2026:** hver fil i utkastet har sha256 i MANIFEST-VAULT eller kommer fra git ved
byggets HEAD, og sha-en i utkastet er den byggmanifestet fører. **Ett blokkerende funn:** `koder2-sammenlikning.json`
bar 16 ordrette passasjeutdrag (inntil 400 tegn) fra de 320 — i strid med avgjørelsen om ingen passasjetekst i
depositumet (§ 7). Depositumet bærer nå `koder2-sammenlikning-uten-tekst.json`, med sha256 og tegnantall i stedet;
originalen står på volumet. **Originalen er alt publisert** — identisk (md5 `e634fa99…`) i v0.2.0, v0.2.1 og v0.3.0 —
og en publisert post kan ikke bytte fil. v0.4.0 slutter å bære teksten; de tidligere versjonene står. Utdragene er
korte sitater i en vitenskapelig sammenligning, og hviler der på sitatretten (LISENSAUDIT § 2). Etter det har **ingen JSON- eller JSONL-fil i depositumet passasjetekst** (maskinelt: felt
som `tekst`, `passasje`, `utdata_raa` over 40 tegn, og alle strenger over 600 tegn, også inni zip-filene).
**Manifestet à jour:** en skanning av hele volumet på innholds-sha fant filer uten rad, bl.a. inndata til ADDENDUM-17
(`a17-2p-mot-2d.json`) og 2′-loggen; de er ført (seksjonene «Frys-lesning 4» og «G3 før v0.4.0» i manifestet).
Fulltekstkatalogene med eget `MANIFEST.md` føres der, ikke rad for rad. *(Påstanden over om at «alle er ført», gjaldt
de 408 filene fra runde 2.)*
**Kanalene:** Zenodo v0.1.0–v0.3.0 (uendret), GitHub `offentlig` (`967254a`, uendret til utgivelsescommiten),
MetaArXiv (preprint, pending), volumet (privat).

## 7 Lisens — blindfilene som indeks (avgjort 28.09.2026)

**Blindfilene er tekstbiter**, så de deponeres som **indeks**: id, verk-id, setningsspenn, sha256 av teksten, og
hele blindfilens sha256. **Eieren avgjorde 28.09.2026: indeks, med regenereringssetning i README; ingen
passasjetekst i depositumet.** Kontrollert: 16 indeksfiler, 3 642 rader, ingen tekstfelt, alle sha-er stemmer
mot blindfilene. Regenerering etter README-oppskriften traff `tekst_sha256` for **6 av 6** trukne W-rader
(PDF og JATS) og **16 av 16** ankerrader (PMC- og DOAJ-id-er fra recall-settene; 12 fra
`logs/recall-sett-2-setninger.jsonl`, 4 fra `logs/pipeline-test/sentences-REPARSE-ADDENDUM07.jsonl`).
Punktet om `W2974992769` (NC-ND, sitert én gang) i LISENSAUDIT § 4 F står uendret.

*(Tillegg 30.09.2026: 15 fase 3-blindfiler er lagt til som indeks — 4 592 rader; i alt 31 indeksfiler og
8 234 rader, **0 med tekstfelt**, kontrollert i det bygde utkastet.)*

## 8 Hva som mangler før eieren kan autorisere

1. ~~Eierens valg om historikkbundlen~~ **avgjort 29.09: med** (§ 4).
2. ~~Stedene som navngir personer~~ **kontrollert maskinelt 29.09** (`docs/NAVNEKONTROLL-2026-09-29.md`): 0
   evaluerende i rettbare filer, 4 i låste; navn står bare i sitering og nøytral omtale. Fotnote 83 i Heron v2
   § 11 er erstattet med parafrase etter eierens avgjørelse; tredjepersonens navn, datoen og meddelelsens
   ordlyd forekommer ikke i noen sporet fil. Historikken bærer det opprinnelige (§ 4).
3. ~~ADDENDUM-25-utfallet, og en tredje lesning av avsnittene merket «leses etter ADDENDUM-25-utfall»~~ **målt og
   lest 30.09** (§ 1, § 3.3). Åpent etter runden: skanneren i NAVNEKONTROLL skal flyttes til `src/`; kandidatlista
   på 432 er ikke deponert (§ 3.3). ~~De to fase 3-nøklene er eierens valg~~ **avgjort 30.09: nøkkelregelen, § 6.**
4. sha-tabellene i MANUSKRIPT-FAKTA § 0 og REGISTER-SAKER: regnet om 28.09 etter runde 2; **regnes om igjen** ved hver senere endring av en fil de fører.
5. `docs/ZENODO.md` med v0.4.0-seksjonen og versjons-DOI når den finnes. **30.09: seksjonen står; DOI-en fylles inn
   etter publisering, sammen med `CITATION.cff`.**
6. ~~Manus v2.6: 9 rader rest~~ **v2.7/v2.8: 2 rader kjent rest** fra sjuende sjekk, pluss 9 fra frys-lesning 4 og 2 fra
   faktafila, alle ført som kjent rest uten ny runde (`FAKTASJEKK-MANUSKRIPT-v2.7-2026-09-30.md`). `silrecall`-setningen
   er omskrevet i v2.7: skjemaet skal utvides før feltet bærer et tall.
7. **Åpne poster som ikke hindrer publisering:** skriveren i ledd 7c setter `status: "målt"` når bare totalen er målt
   (UTGANG); `steg_les` fører seg ferdig uten fullt antall (LAERDOM § 45); `CCLeser` fører ikke `modelUsage`;
   navnekontrollens skanner til `src/`; kandidatlista på 432 er ikke deponert.
