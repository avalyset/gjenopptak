# Faktasjekk av MANUSKRIPT-v2-UTKAST — 28.09.2026

**Manuskript:** `docs/MANUSKRIPT-v2-UTKAST.md`, sha256 `5d11574a02a7d90f1301f2c1120e97bb3ff272045227cd474188eb3b0e80051d`,
472 linjer, uendret gjennom hele kontrollen. **Fasit:** `docs/MANUSKRIPT-FAKTA-2026-09-28.md` (sha256 `99b3094d…`)
og kildene den peker til. **Ingen prosa er omskrevet** — verken i manuskriptet eller i faktafila.

## Metode

Tre kontrollører, hver med sin del (l. 1–186, 187–289, 290–472), kontrollerte **hvert tall, hver DOI, hvert
sitat, hver sha, hver identifikator og hver dato**. Tall som ikke står i FAKTA, ble regnet om fra kildefilene
(koderfiler, registeret, Vault); κ med `classify/reliabilitet.py` (frø 734248), intervaller med Wilson. DOI-er
slått opp på doi.org (302) og i Crossref; referanser uten DOI søkt i Crossref. Sitater kontrollert ordrett mot
kilden (dokument i repoet, eller fulltekst på Vault). Hver påstand er ført med kildesti og sha256 i
delrapportene på Vault, `manuskript/faktasjekk-v2/`:

| del | linjer | påstander | sha256 |
|---|---|---|---|
| 1 | 1–186 | 83 | `bac85a0abce4c5247e0e377a40e8755380c861e59290d89e2946d9d16e395b29` |
| 2 | 187–289 | 68 | `9d550ff225449d2a999645110339db45c73b8cd44e934309fcfd36f1e7b99f60` |
| 3 | 290–472 | 118 | `a65e28062914c2dc6988c5b1852f9de8761d20f9860757038716f201b83885b9` |

## Utfall

| status | antall | hva det betyr |
|---|---|---|
| samsvar | **209** | verdien stemmer med FAKTA eller kilden |
| feil | **12** | verdien er gal |
| overclaim | **20** | sterkere enn målingen eller kilden bærer |
| uklart | **19** | kan ikke avgjøres, eller manus og kilde sier noe litt annet |
| uten kilde | **3** | ingen sti eller sha finnes |
| foreldet | **2** | var riktig før en rettelse 28.09 |
| venter | **4** | venter på ADDENDUM-25-utfall |
| **sum** | **269** | |

**Mønstre i avvikene** (for lesing, ikke omskriving):
* **Deponeringsstatus i framtid som om den var fortid** (l. 120, 447, 450, 453, 456): manus skriver som om v0.4.0
  er deponert og bærer historikk, blindfilindeks og ots-kvitteringer. v0.4.0 er forberedt, ikke publisert, og
  valget om historikkbundlen er ikke tatt (`UTGIVELSE-v0.4.0-PORTSTATUS.md` § 4).
* **Gjenåpningsprosedyren omtales som låst for alle seks saker** (l. 30, 67, 181): tre av seks har ingen
  kriteriefil, og ADR-0013 er skrevet etter sakene.
* **Sterkere slutninger enn sakfilene** (l. 294, 298, 397, 400, 403–405): «kriteriet oppfylt for 2 av 4» der
  kilden sier nei; «optimal», «vist unødvendig», «enhver studie», «målbart dårligere» der kildene er forsiktigere.
* **Enkelttall** (l. 87, 104, 135, 280, 328, 329, 369, 387, 403, 436): se tabellen.

## Avvik, sortert på linje

| linje | påstand (ordrett fra manus) | manus sier | kilde sier | kilde | status |
|---|---|---|---|---|---|
| 3 | every number below is anchored there with a path and a sha256 | alle tall i utkastet er forankret i FAKTA | FAKTA fører ikke 356 (øktstørrelse), ~3 000 tokens (vindu), 70 %-terskelen, «eight steps», «three independent grounds», XML/PDF-andelene l. 81–83; FAKTA § 0: tall som ikke står der, er ikke belagt | docs/MANUSKRIPT-FAKTA-2026-09-28.md (`99b3094d`) | **overclaim** |
| 26 | Among confirmed hits, roughly two thirds name an obstacle of the kind that cannot be lifted by anyone | «confirmed hits»; H7 «cannot be lifted by anyone» | De 432 er leserens (koder c) treff i en kandidatliste; bare en post hoc blindprøve på 100 er bekreftet (85 %). PREREG § 5 fører H7 som «løftbar av AI i dag: nei», og ADR-0010 gjør løftbarhet datert; FAKTA § 7: «bekreftet» krever presisering i samme avsnitt | data/kjede/kandidat432/8-register.jsonl + ADDENDUM-23.md + PREREG-v1.md + docs/MANUSKRIPT-FAKTA-2026-09-28.md | **overclaim** |
| 30 | We then took six candidates through a locked reopening procedure | seks saker, «locked procedure» | Seks saker (FAKTA § 4). ADR-0013 (datert 28.09) ble skrevet etter sakene: «Vilkårene … er de tre stedene de seks sakene faktisk stanset». SAK-08, SAK-09c og SAK-11: «ingen kriteriefil låst» | docs/MANUSKRIPT-FAKTA-2026-09-28.md + docs/decisions/0013-opphevelse-definisjon.md + docs/saker/SAK-08/LUKKET.md + docs/saker/SAK-09c/LUKKET.md + docs/saker/SA… | **overclaim** |
| 34 | cited only in translation could be retrieved and read against the original | 79 steder hentet «and read against the original» | 79 = referansen oppløst til gresk tekst (steg 2). Bare 11 av 90 steder bærer avhandlingens franske gjengivelse; portens andre ledd var umålbart for de øvrige 79; termsammenligningen gjelder 8 steder | docs/saker/SAK-14/RESULTAT.md + docs/MANUSKRIPT-FAKTA-2026-09-28.md | **overclaim** |
| 66 | We report (i) the class distribution on 100 works | klassefordeling «on 100 works» | De 432 radene dekker 60 verk, ikke 100; FAKTA § 8: «Ikke at de 432 radene dekker 100 verk» | docs/MANUSKRIPT-FAKTA-2026-09-28.md + data/kjede/kandidat432/8-register.jsonl | **uklart** |
| 67 | (iv) six reopening attempts under a locked procedure | seks, «locked procedure» | Seks saker; ADR-0013-vilkårene skrevet 28.09 etter sakene; tre av seks uten låst kriteriefil | docs/MANUSKRIPT-FAKTA-2026-09-28.md + docs/decisions/0013-opphevelse-definisjon.md + docs/saker/SAK-08/LUKKET.md + docs/saker/SAK-09c/LUKKET.md + docs/saker/SA… | **overclaim** |
| 81 | works delivered as structured XML are almost always retrievable, works delivered as PDF in about half | XML «nesten alltid», PDF «om lag halvparten» | Ingen kilde fører disse andelene. Delvis regnbart: P3-suksess blant verk med PDF-lenke 49/107 = 45,8 % (arkeologi, tekstvitenskap, karakterisering-*.json) og 9 559/19 004 = 50,3 % (energimodellering, ADDENDUM-08 § 3). JATS-hentbarhet er ikke målt som andel | data/utvalg/karakterisering-arkeologi.json + ADDENDUM-08.md | **uten kilde** |
| 87 | at a stride of three sentences (ADDENDUM-03) | stride 3, hjemlet i ADDENDUM-03 | stride 3 stemmer (spesifikasjon.json «stride»: 3; kjede.toml; ADR-0012), men ADDENDUM-03 nevner ikke stride; STRIDE = 3 kom i kode, commit 630f861 (16.09.2026) | ADDENDUM-03.md + data/port/spesifikasjon.json | **feil** |
| 104 | 12 anchor passages with known status from earlier recall sets | 12 ankerpassasjer | 20 ankerpassasjer i de 320 (anker-treff 12, anker-ikke-treff 8); 12 er ankertreffene (FAKTA: «12 ankertreff»). Manus l. 168 bruker selv 300 ikke-anker = 320 − 20 | data/port-presisjonssett-ADDENDUM10.jsonl + docs/MANUSKRIPT-FAKTA-2026-09-28.md + docs/METODE.md | **feil** |
| 120 | it is deposited with v0.4.0 | deponert med v0.4.0 | v0.4.0 «Forberedt, IKKE publisert»; UTGIVELSE-0.4.0.json «publisert»: false; regelfila ligger i utkastet | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md + Vault: zenodo/v0.4.0-bygg/UTGIVELSE-0.4.0.json | **overclaim** |
| 120 | **Coder 4** (28 September) is Claude Fable 5.1 in a chat interface — a different model family | 28.09; «Claude Fable 5.1»; annen modellfamilie | Kildene skriver «Fable 5.1 i chat, en annen modellfamilie» (METODE «Koder 4», FAKTA § 1); ingen kilde bruker «Claude Fable»; ingen modell-ID er ført, og oppdraget «finnes ikke som fil» (PORTSTATUS) | docs/METODE.md + docs/MANUSKRIPT-FAKTA-2026-09-28.md + docs/UTGIVELSE-v0.4.0-PORTSTATUS.md | **uklart** |
| 122 | Seven of the 320 rows had been seen by coder 4 with the reader's class labels the day before | 7 rader, sett med leserens klasser dagen før | 7 eksponerte: PS-266 eksakt tekstmatch; PS-246, -288, -289, -319 «2 felles setninger» med rader i kandidatfila; PS-257 og PS-300 bare «kjent på id fra sporets dokumenter» | Vault: koder4/eksponerte-rader.json + docs/METODE.md + docs/SAKBEHANDLING-2026-09-27-kandidater.md | **overclaim** |
| 134 | each locked as a single-file commit that triggers an archived bundle of the full git history | hvert addendum: én-fils-commit + kanon-bundle | ADDENDUM-16s låsecommit e92620b har 2 filer (ADDENDUM-16.md + prompts/ekstraksjon-v1.txt). Bundle-utløseren (securerepo, 9e58a4e 12.09 16:23) kom etter PREREG og ADDENDUM-01–04; ingen kanon-bundle for 471e854, 8de9a76, 742ae17, 3a004bf, 16b484b (Vault repo/kanon/). ADDENDUM-10 og -11 har fått tillegg etter lås (PORTST… | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md (`03aab10d`) | **overclaim** |
| 135 | Two rule clarifications were written after data (ADDENDUM-10) | to presiseringer | ADDENDUM-10 «tre presiseringer av treffkravet» (§ 1 feltgap, § 2 oversiktsarbeid, § 3 modellbegrensninger); regelfila bærer «ADDENDUM-10 §1–3» | ADDENDUM-10.md + ADDENDUM-11.md | **feil** |
| 137 | OpenTimestamps receipts on the bundles (complete from 28 September 2026) | 28.09.2026 | 42 av 42 bundler stemplet og oppgradert 28.09.2026; «For de 40 eldre bundlene … attesterer beviset bare at innholdet fantes 28.09, ikke at PREREG (12.09) … var låst før beregningen» | docs/TIDSSTEMPEL.md (`9bad243f`) | **uklart** |
| 142 | The tool runs as one command in eight steps | åtte ledd (ADR-0012) | MASTER-patch 28.09: «Kjeden er ti ledd, ikke åtte: hent, tekstbiter, dommer, ekstraksjon, union, blind, les, verksniva, falsify, register»; ledd.py LEDD = 10; METODE § 9 «Ledd 1–6 og ledd 8–10»; ADR-0012 lister ikke åtte ledd | docs/patch/MASTER-2026-09-28-fase1-2.md + src/gjenopptak/kjede/ledd.py + docs/METODE.md + docs/decisions/0012-kjeden-er-en-sti.md | **foreldet** |
| 160 | work-level assessment, citation-falsification coverage | registerraden bærer verksnivå og siteringsdekning | Registerradene i kandidat432 har ingen verksnivå-felt (nøkler: … sil, tvil, loftbarhet, cites_coverage …; 7b-verksniva.jsonl mangler for kjøringen); cites_coverage er «ikke målt» på alle 432 | data/kjede/kandidat432/8-register.jsonl + src/gjenopptak/kjede/ledd.py | **overclaim** |
| 181 | Each case has its criterion in a file whose sha256 is fixed before any computation. | alle saker har låst kriteriefil | SAK-08, SAK-09c og SAK-11: «Ingen kriteriefil låst». ADR-0013 følge 3: «Et kriterium låses ikke for en sak som kan stanse på vilkår 1». Låst kriterium bare for PS-246, SAK-14 (5330c701…) og SAK-09b (2fa587a0…) | docs/saker/SAK-08/LUKKET.md + docs/saker/SAK-09c/LUKKET.md + docs/saker/SAK-11/LUKKET.md + docs/decisions/0013-opphevelse-definisjon.md | **feil** |
| 203 | ADDENDUM-22 reports 69/374 = 18.4 % for the liftable share | ADDENDUM-22: 69/374 = 18,4 % løftbar | ADDENDUM-22 § 9.3 (l. 251): «løftbar klasse H1–H6 69 av 374 = 18,4 % [14,8–22,7]» — nevner alle treff. KORRIGENDUM B: riktig partiell verdi med avklarte som nevner er 69/353 = 19,5 % [15,7–24,0]; ADDENDUM-22 § 10 (l. 321) gir den komplette 77/432 = 17,8 %. | docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md (`e42d44d3`) | **uklart** |
| 204 | those are the partial state at the time the addendum was locked, mid-run, not a contradiction. | ADDENDUM-22 bærer bare partiell tilstand fra da det ble låst, midt i kjøringen | ADDENDUM-22 l. 3: «Skrevet: 2026-09-27, før kjøring. Status: LÅST» (låst før kjøringen, commit 09e3d0c 10:14). 374-tallene står i § 9 (utfall, commit 4d77be2 12:15, 2 481 av 2 844 dømt). § 10 i samme addendum (commit fa94c5b 14:42) gir de komplette tallene: H7 289/432 = 66,9 %, løftbar 77/432 = 17,8 %, H7–H9 76,2 %. | ADDENDUM-22.md (`fc11ff06`) | **feil** |
| 222 | Seven of the 320 rows had been seen by coder 4 with labels before coding | 7 av 320 sett av koder 4 med etiketter før kodingen | METODE, datert note: «7 av 320 rader er derfor ikke blindt kodet»: PS-266 eksakt tekstmatch; PS-246, PS-288, PS-289, PS-319 2 felles setninger med en AL-rad i kandidatdokumentet; PS-257 og PS-300 kjent på id fra sporets dokumenter. | docs/METODE.md (`94c6ad68`) | **uklart** |
| 239 | The boundary is now an explicit, versioned decision rule with anchor examples (REGEL-N3-v1). | REGEL-N3-v1 er nå grensens regel | docs/REGEL-N3-v1.md finnes (versjon 1, 28.09.2026, ni ankere). KORRIGENDUM H: «Regelen er ikke i bruk i fase 3» og gjelder først fra første koding som får den som inndata. | docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md (`e42d44d3`) | **uklart** |
| 261 | Two earlier runs (κ 0.390 for Opus, 0.321 for Sonnet) were invalidated by output truncation at 300 tokens | Opus 0,390 og Sonnet 0,321 ugyldige, avkuttet ved 300 | § 2: Opus 0,390 ugyldig (max_tokens 300). ADDENDUM-18s Sonnet 0,321 (n 307) er rammet av samme tak og «erstattet av 0,297 [0,125–0,456], n = 319 … det er tallet som siteres». ADDENDUM-19 § 7.3: rettet fra 0,321 til 0,297; kjøringen brukte det tynne utdraget (00d69c09ed8b9045). | ADDENDUM-19.md (`41a2f0cb`) | **uklart** |
| 280 | coder 2 confirmed 19 of coder 1's 25 hits, 76 % | 19 av 25 = 76 % | ADDENDUM-23 § 2 (l. 43): «koder 2 bekreftet 19 av 27 = 70,4 % på hele settet»; FAKTA § 1: enige om treffstatus 19 av 27. Av koder 1s 25 treff i treff-stratumet bekreftet koder 2 17 (68,0 %). | ADDENDUM-23.md (`d0eb2ca4`) | **feil** |
| 287 | One deviation from the gate's text must stand: "one separate instance" became two | "one separate instance" | ADDENDUM-23 § 4 (l. 65): «én separat instans med tom kontekst»; § 7.3 (l. 127): «§4 sa «én separat instans».» | ADDENDUM-23.md (`d0eb2ca4`) | **uklart** |
| 294 | criterion met for 2 of 4 horizons (25 Sept.) | kriteriet oppfylt for 2 av 4 horisonter | «Er kriteriet oppfylt? Nei, ikke for de målte seksjonene som gruppe. To av fire flagget horisonter flipper … begge ligger innenfor ±0,02 av terskelen — lesefeilen fra figuren alene avgjør fortegnet.» ADR-0013: vilkår 3 «nei — 2 av 4 horisonter, begge innenfor ±0,02». | docs/PS-246-RESULTAT.md (`3a6ea9d1`) | **overclaim** |
| 298 | six routes checked, no model code deposited | 6 ruter; ingen modellkode deponert | Overskrift: «modellkoden er ikke funnet i seks sjekkede ruter; forlagets tilleggsmateriale er uavklart (HTTP 403)». «(Overskriften rettet 28.09.2026 …: sto «modellkoden er ikke deponert noe sted», som teksten selv sier ikke er målt for forlagets rute.)» | docs/saker/SAK-08/LUKKET.md (`704155d2`) | **overclaim** |
| 302 | 76 unique references: Dionysius 57, Plutarch 22, Appian 5, Cassius Dio 3, Moralia 2, Aristotle 1 | 57/22/5/3/2/1 knyttet til «76 unique references» | Per sitatsted: 57/22/5/3/2/1 = 90. Per unik referanse (tabell.json, «nokkel»): Dionysios 48, Plutark (biografier) 19, Appian 4, Cassius Dio 3, Moralia 1, Aristoteles 1 = 76. | Vault: saker/SAK-14/tabell.json (`caa70e01`) | **uklart** |
| 314 | all eleven would have been recorded as hits and the case would stand as lifted at 100 % | 11 av 11 ville blitt treff; 100 % | RESULTAT: «Uten den kontrollen ville alle elleve blitt ført som treff, og saken ville stått som opphevet på 100 %.» Men oppslag.log viser for de Perseus-tilbakefallene «TILBAKEFALL n_ord= 0 … fikk={}», og RESULTAT selv oppgir at «Rom. 19, 9 ga «No document found»». | Vault: saker/SAK-14/oppslag.log (`5de8c3e2`) | **uklart** |
| 328 | blockmodeling 1.1.8, published in June 2018, before submission | 1.1.8 publisert juni 2018 | «blockmodeling står på CRAN, nåværende versjon 1.1.8 (2025-07-25) … Arkivet viser 0.3.1, publisert 2018-06-05 — før avhandlingen ble levert (2018-11).» | docs/saker/SAK-09b/KRITERIUM.md (`2fa587a0`) | **feil** |
| 329 | unconstrained, its partitions were equal 0 of 120 times | pakken: 0 av 120 like | RESULTAT: pakken kjørt med «50 tilfeldige starter» (r-kjoring.R: rep = 50) og ga ulike partisjoner. «over 120 tilfeldige starter ble mellomnivåets to partisjoner like av seg selv i 0 av 120 tilfeller» gjelder «min egen implementasjon»; kjoring3.json: utvungen n=120, like=0. | Vault: saker/SAK-09b/kjoring3.json (`2a2480ad`) | **feil** |
| 335 | "total error 14" counts only the 32 three-mode blocks without saying so | «total error 14»; 32 blokker | Avhandlingen ordrett: «(the total error is 14)». RESULTAT: «teller bare de 32 tre-modus-blokkene». | Vault: utvalg/energimodellering/ft-pdf-W7133020405-3765e3086324.json (`3765e308`) | **uklart** |
| 352 | Only SAK-14 reached a threshold | bare SAK-14 nådde en terskel | REGISTER: «Bare SAK-14 kom helt fram til en terskel» (om de fem). ADR-0013: vilkår 3 heter «terskel», og PS-246, SAK-14 og SAK-09b kom til vilkår 3. | docs/saker/REGISTER-SAKER.md (`4b7601fa`) | **uklart** |
| 364 | the answer from the citation graph is no in all four | 4 av 4 nei fra siteringsgrafen | Triagen: PS-246-utvidelsen ble besvart ved søk i avhandlingen selv («Søk i hele avhandlingen (581 864 tegn) …»), ikke i siteringsgrafen. De tre andre ble besvart fra siteringer og bredere søk. | docs/SAKBEHANDLING-2026-09-27-triage.md (`29445995`) | **uklart** |
| 369 | in 581 864 characters | 581 864 tegn | pdftotext -layout av samme PDF gir 581 864 BYTES (UTF-8) = 579 109 tegn. Triagen og FAKTA oppgir «581 864 tegn». | Vault: utvalg/arkeologi/ft-pdf-W2551114598-2ca87c62f14f.json (`2ca87c62`) | **feil** |
| 387 | the six attempts above took days each | dager per sak | SAK-14, SAK-09c, SAK-08 og SAK-09b er alle «gjennomført/lukket 27.09.2026», SAK-11 28.09.2026 og PS-246 25.09. FAKTA § 4: «Fase 2, gjennomført 27.–28.09.2026.» | docs/saker/REGISTER-SAKER.md (`4b7601fa`) | **feil** |
| 388 | the best AI-liftable candidate in the material, a critical edition parked for want of time | Heron = beste AI-løftbare kandidat i materialet | RESULTAT-PORT-v1: «Heron-kollasjonen i W3000588547 … er kontrollen, utenfor de 100 verkene og utenfor nevneren (ADDENDUM-08 § 1), ikke et av de løftbare treffene i utvalget … (Rettet 28.09.2026: sto «Beste AI-kandidat … den sterkeste av de fire løftbare»; kontrollen er ikke blant de 100.)» | docs/RESULTAT-PORT-v1.md (`2d1e24ac`) | **foreldet** |
| 395 | The claim that "some obstacles have since been lifted, some by AI" has no support | «some obstacles have since been lifted, some by AI» | PREREG-v1 § 1.2 ordrett: «En del av disse hindringene er i dag opphevet, en andel av dem av AI.» Manus § 1 gjengir det som «some fraction of the named obstacles have since been removed … including language models». | PREREG-v1.md (`05988b23`) | **uklart** |
| 397 | an author's workaround shown to be optimal | omgåelsen er optimal | SAK-09b RESULTAT: «Avhandlingens løsning er altså et lokalt optimum også under tvang»; 14 mot 18 (beste av 120 tvungne starter), og ingen forbedring fra avhandlingens partisjon. | docs/saker/SAK-09b/RESULTAT.md (`0ff7a732`) | **overclaim** |
| 397 | an undone computation shown by the authors' own arithmetic to be unnecessary | unødvendig, vist ved aritmetikk | SAK-11 LUKKET: «forfatterne argumenterer for at full enumerering er unødvendig, og de gir belegg … her kan vi ikke etterprøve belegget, bare påstandens aritmetikk.» REGISTER: «artikkelen selv kan ha målt». | docs/saker/SAK-11/LUKKET.md (`bd93b73d`) | **overclaim** |
| 400 | The reliability results are transferable to any study that uses LLM annotation. | overførbare til enhver studie | FAKTA § 6.3: «Formålsvalgte felt — tallene gjelder disse fire.» ADDENDUM-11/RESULTAT-PORT: κ per felt spriker fra 0,390 (energimodellering) til 1,000. | docs/MANUSKRIPT-FAKTA-2026-09-28.md (`99b3094d`) | **overclaim** |
| 403 | collapses at one boundary (N3, 0.530) | N3 0,530, én grense | METODE: «De to svakeste grensene er ikke-treff-klassene. N3 og N2 ligger på 0,53» (N2 0,535). Regnet om: N3 0,5296, N2 0,5349. | docs/METODE.md (`94c6ad68`) | **feil** |
| 404 | until the boundary is written as a decision rule | κ-kollaps løst av beslutningsregel | REGEL-N3-v1: «Regelen er ikke brukt på de 320 … κ = 0,530 er derfor før-tallet» og «en ny κ-måling etter fase 3 vil vise hvor mye den var verdt». | docs/REGEL-N3-v1.md (`96cd8372`) | **overclaim** |
| 405 | a reader in one call per item is measurably worse than the same model reading a batch | målbart dårligere (0,636 mot 0,812) | FAKTA § 2: «differansen mellom 0,636 og 0,812 er ikke statistisk etablert. Intervallene overlapper i 0,697–0,768 … Øktformens bidrag er derfor ikke påvist.» § 8: «Ikke at øktformen forklarer κ-forskjellen.» | docs/MANUSKRIPT-FAKTA-2026-09-28.md (`99b3094d`) | **overclaim** |
| 406 | Two of these results were reached only because the gates were locked before the runs | to resultater | Ingen kilde sier hvilke to resultater dette er, eller at de avhang av låsingen. | docs/MANUSKRIPT-v2-UTKAST.md (`5d11574a`) | **uten kilde** |
| 426 | the protocol never defined "without a domain expert" | «without a domain expert» | PREREG-v1 § 2 ordrett: «lar seg avgjøre uten domeneekspert i faget». | PREREG-v1.md (`05988b23`) | **uklart** |
| 436 | Register v2 did not validate against its own schema until 28 September 2026 | 28.09.2026 | REGISTER-SAKER: «To feil i register v2, funnet og rettet 27.09.2026». Registerhodet, rettet-linjen: «2026-09-27: sil.presisjon_ki fylt fra kjede.toml (432 rader); cites_coverage 0/0 … erstattet med «ikke målt»». | data/kjede/kandidat432/8-register-header.json (`38366d7c`) | **feil** |
| 438 | (register sha256 aa8f7c2e… → c6895202…) | aa8f7c2e → c6895202 | sha256 av 8-register.jsonl regnet om = c6895202b76199aa… (stemmer). REGISTER-SAKER: rettingen alene ga aa8f7c2e → 6caabaff; c6895202 er tilstanden etter fire senere sak- og vurderingsoppdateringer (siste SAK-11, 28.09). aa8f7c2e er ikke bevart (UTGIVELSE-v0.4.0 § 5). | data/kjede/kandidat432/8-register.jsonl (`c6895202`) | **uklart** |
| 447 | the full working history is in the deposited git bundles | hele historikken i deponerte bundler | UTGIVELSE-v0.4.0 § 4: «v0.3.0-bundlen ble laget 26.09» og historikken etter den (bl.a. 37d7187, 27.09) er ikke deponert, «Alternativene er eierens». ZENODO.md: gjeldende versjon 0.3.0. | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md (`03aab10d`) | **overclaim** |
| 450 | blind files are deposited as indices (identifier, work, sentence span, sha256 of the text) | blindfiler deponert som indeks | UTGIVELSE-v0.4.0 § 7: indeks avgjort 28.09, «16 indeksfiler, 3 642 rader», og filen blindfiler-indeks.zip er ny i v0.4.0, som er «Forberedt, IKKE publisert». ZENODO.md: gjeldende 0.3.0 har ingen blindfilindeks. | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md (`03aab10d`) | **overclaim** |
| 452 | Licence per work is recorded in the manifest | lisens per verk i manifestet | LICENSE-DATA: «The licence of each source work is listed per work in docs/LISENS-PER-VERK.md». INSTRUKSER-v1.3 § 12 sier «føres i manifestet». | LICENSE-DATA (`7b731235`) | **uklart** |
| 453 | The deposit (concept DOI …) carries the protocol, all addenda and decision records, … OpenTimestamps receipts, and a bundle | depositumet bærer alle addenda, ADR-er, METODE, regelfil, oppdrag, ots-kvitteringer | ZENODO.md: gjeldende versjon 0.3.0 (26.09, 38 filer). UTGIVELSE-v0.4.0 § 1: ADDENDUM-12–25, ADR-0011–0014, METODE, regelfilen, oppdrag med sperreliste og ots-kvitteringer.zip er NYE i v0.4.0, «Forberedt, IKKE publisert». INSTRUKSER-v1.3 § 12 lister dette som hva depositumet «skal bære». | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md (`03aab10d`) | **overclaim** |
| 456 | v0.4.0 carries it | v0.4.0 bærer regelfilen | UTGIVELSE-v0.4.0: «Forberedt, IKKE publisert … det finnes ikke noe utkast hos Zenodo». | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md (`03aab10d`) | **uklart** |
| 461 | as described in §2.4 and §3.2, with model identity recorded per verdict | § 2.4, § 3.2; modell-ID per verdikt | § 2.4 «Coders» og § 3.2 «The pipeline» finnes (manus l. 113 og 140). Koder 2-fila har feltene id, ekte_treff, min_klasse, min_bedømbar, tvil, begrunnelse, og koder 4-fila id, treff, klasse, samme_setning, bedombar, tvil, begrunnelse — ingen modell-ID. Koder 2s modell-ID ble gjenvunnet fra øktutskrift 27.09 (FAKTA § 1)… | docs/RESULTAT-ADDENDUM-25.md (`52fdf5b6`) | **overclaim** |
| 462 | This draft was written by Claude Fable 5.1 | Claude Fable 5.1 | Intet dokument i repoet eller på Vault fører hvilken modell som skrev utkastet. INSTRUKSER-v1.3 § 2 gir «chat-Claude» rollen «narrativ», og koder 4 er «Fable 5.1 i chat». | docs/INSTRUKSER-v1.3.md (`ececde4b`) | **uten kilde** |
| 463 | every number was then checked against that file by a separate pass | kontroll gjennomført | Manus l. 5–6: «Not for circulation until the fact-check pass (CC) has been run against this file.» Kontrollen pågår 28.09 (denne fila). | docs/MANUSKRIPT-v2-UTKAST.md (`5d11574a`) | **uklart** |

## Venter på ADDENDUM-25-utfall

| linje | påstand | merknad |
|---|---|---|
| 155 | The first measured recall will come from phase 3 [pending]. | RESULTAT-ADDENDUM-25: «kjøringen pågår» |
| 372 | Phase 3 — prospective gate and first measured recall [pending] | RESULTAT-ADDENDUM-25: «Status 28.09.2026: kjøringen pågår … § 1 Utfall: Ikke målt ennå.» |
| 434 | Phase 3 supplies the first measured value [pending] | RESULTAT-ADDENDUM-25 § 1: «Ikke målt ennå.» |
| 469 | [To be assembled from the register and case files | W-id-ene nedenfor er kontrollert hver for seg. |

Tallene § 4.7 oppgir om oppsettet (100 verk, 20 referanseverk, 100 treff mot 0,70, recall uten terskel) stemmer
med `ADDENDUM-25.md`.

## Feil i MANUSKRIPT-FAKTA selv — funnet under kontrollen, ikke rettet her

* **l. 206** sier at ADDENDUM-22s tall er «partiell tilstand da addendumet ble låst midt i kjøringen». ADDENDUM-22
  ble låst før kjøring; 374-tallene står i § 9.3, de komplette i § 10.
* **§ 6.9** daterer valideringsrettingen av registeret til 28.09; REGISTER-SAKER og registerhodet sier 27.09.
* **«581 864 tegn»** (Pring-teksten) er bytes; teksten har 579 109 tegn. Samme feil i triagen.
* **SAK-08:** «ingen modellkode deponert» står fortsatt i REGISTER-SAKERs «Mønsteret» og i registerhodet, selv om
  `SAK-08/LUKKET.md` er rettet til «ikke funnet i seks sjekkede ruter».

## Til referanselista (når den skrives)

Haouachi 2016 har en Crossref-DOI (`10.70675/8513d3c9ze385z4b4bz910cz221c7718984d`, 302 til theses.fr) selv om
OpenAlex mangler den. Bynum m.fl. har sju forfattere og år 2021 i Crossref (2020 i OpenAlex og triagen).
Riris-tittelen i SAK-08 avviker fra Crossref. «Mythos 2018», «Eythra 2017» og «Pietrele 2019» er ikke
forfatter–år; Crossref gir Karatas 2018, Mecking, Hohle & Wolfram 2017 og Hansen m.fl. 2019. Pring 2016 og
Aragao 2018 finnes ikke i Crossref. Konsept-DOI-en 10.5281/zenodo.22959326 gir 302 (DataCite, ikke Crossref).
