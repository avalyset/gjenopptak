# Release notes — v0.6.0 (oktober 2026)

En opprydning. **Ingen ny måling, ingen endrede tall, ingen låst fil endret.** Versjons-DOI
**10.5281/zenodo.23279145**, publisert 2026-10-10. Konsept-DOI 10.5281/zenodo.22959326 er den som siteres.

## Nytt

* **`maalefiler.zip` — måleinndata og utfallsfiler.** Depositumet til og med v0.5.0 bar dokumentene og fase 3, men
  ikke filene tallene i ADDENDUM-01 til -24 er regnet fra, og ikke koder 1s verdikter. Nå er de med: 107 filer,
  9 til med tekstfeltene byttet med sha256 og lengde, og koder 1s verdikter etter ADDENDUM-10 uten tekst og
  nøkkelfelt. Modellenes og kodernes begrunnelser siterer passasjene; 101 ordrette utdrag på 50 tegn eller mer er
  tatt ut av 17 av filene og byttet med et merke med lengde og sha256. Sammenlikningen ser bort fra blanktegn,
  bokstavstørrelse og Unicode-form. Kortere sitater står.
  `DEPOSITUMSKRAV-2026-10-10.md` fører hver fil som legges til eller holdes ute, og hvorfor.
* **`gjenvunnet-kode.zip` — skriptene bak ADDENDUM-19, 19b og 20.** De lå i øktens scratchpad og ble aldri
  committet. `a20.py`, analysekoden og avledningskommandoene er ordrett fra øktutskriften; `a19.py` og `a19b.py` er
  regenerert ved å kjøre de ordrette snuttene på `a20.py`. `README.md` i zip-filen sier det først: den regenererte
  `a19.py` har samme tegnantall som utskriften rapporterte, men er **ikke byte-verifisert mot originalen**, som ikke
  finnes. Opphav og autentisitetsgrunnlag står i `OPPHAV.md`.
* **Manuskript v3.3** (`MANUSKRIPT-v3.3.md`) og `MANUSKRIPT-v3.3.docx` slik det ble sendt til *Scientometrics*
  03.10.2026. v3.2, som ble preprinten 10.20944/preprints202610.0368.v1, ligger i `manuskript-tidligere.zip`.
* **`GJENOPPTAK_ADDENDUMSTATUS_v1_2026-10-10.md`:** PREREG-v1 og hvert addendum med låsecommit, status, utfall, filer
  med sha256 og hvilken Zenodo-versjon som bærer det.
* **ADDENDUM-28** (tredje koder fra en annen modellfamilie, lokal gemma2): låst 10.10.2026, **ikke kjørt**.
  ADDENDUM-27 (menneskelig validering) er fortsatt låst og ikke kjørt.
* **Fire INNHENTET-filer.** To fra landingen: `INNHENTET-2026-10-07-fase4-data.md` og `INNHENTET-2026-10-10-differansen-0812-0636.md`.
  Den siste fører at ADDENDUM-19 § 7.2 og ADDENDUM-24 § 1 sier differansen 0,812 − 0,636 ikke er statistisk
  etablert, og at den parede testen 03.10.2026 innhentet det: 0,177, paret bootstrap [0,044–0,323], verksklynget
  [0,057–0,318].
  De to andre kom av kontrollen før publisering; se neste avsnitt.

## Uavhengig kontroll før publisering

Utkastet ble kontrollert 10.10.2026 i en egen økt uten kjennskap til byggeøkten. Kontrollen fant 25 avvik: 8 som
blokkerte, 11 som burde rettes og 6 kosmetiske. De 19 første er rettet eller ført i INNHENTET-filer; av de kosmetiske
er ett løst (foreldet status i historiske filer), og fem står.

* **`INNHENTET-2026-10-10-manuskript-v3.3.md`:** tre steder i det innsendte manuskriptet, som ikke rettes i filen.
  Klasse-κ 0,722 er regnet over alle 320 passasjer, ikke «among passages both coders call hits». Sitatet i innledningen
  mangler kilde (Takeuchi m.fl. 2019, 10.1002/ams2.395). Tallmanifestet dekker 45 maskinleste verdier, ikke «each
  number». Filen fører rettet ordlyd for revisjonen. De samme stedene står i v3.1 og v3.2.
* **`INNHENTET-2026-10-10-ekstern-vurdering-spraakmodell.md`:** «ekstern fagfellevurdering 03.10.2026» var en
  vurdering gjort av en språkmodell (GPT). Ingen menneskelig fagfelle har lest manuskriptet. Rettet i filene som ikke
  er låst; ADDENDUM-27, ADDENDUM-28, release notes for v0.5.0 og svarbrevet for v3.1 står og føres i filen.
* **`README-HISTORISK.md`** i `manuskript-tidligere.zip` og `utgivelser-tidligere.zip`: filene der er historiske, og
  status i dem er status den dagen de ble skrevet (blant annet «pending» om en preprint som siden ble avvist, og
  «utkast» om v0.4.0).
* **Rettet i dokumentene:** `ZENODO.md` og `CITATION.cff` beskriver nå v0.6.0 som publisert (`CITATION.cff` manglet
  dessuten `authors` i referansen og validerte ikke mot CFF 1.2.0; feilen var arvet minst fra v0.4.1);
  `TALLMANIFEST.md` sa at v0.5.0 var et utkast; addendumstatusen hadde én feil sha256, feil forsøkstall for
  ADDENDUM-09, tre foreldede eller upresise tall og en indre motsigelse om eierens beslutning; `README.md`,
  `METODE.md` og faktaarket kalte koder 4 «en annen modellfamilie» der manuskriptet sier «a different model from the
  same vendor»; `README.md` oppga Wilson-intervaller uten å si det og kobler nå repoets fasenumre til
  manuskriptets; `DEPOSITUMSKRAV-2026-10-10.md` sa «elleve» der tabellen har tolv; og `MANIFEST-VAULT.md` bar ett
  foreldet tall umerket og manglet én rad.

## Endret

* `METODE.md` og `MANUSKRIPT-FAKTA-2026-09-28.md`: avsnittet om differansen rettet, med datert merknad om hva som
  sto; ADR-0012 (i `decisions.zip`) likeså, og `LAERDOM.md` § 50 fører tallet. Samme to filer: grunnratens intervall
  [2,12–7,95] er byttet med det verksklyngede [1,3–7,5] fra reanalysen, og størrelsen heter ikke lenger «beste anslag».
* `CITATION.cff`: versjon 0.6.0 og preprintens DOI. `README.md`, `ZENODO.md`, `MANIFEST-VAULT.md`.
* Koden (i `gjenopptak-src-0.6.0.tar.gz`): `classify/tredje_koder.py` (ADDENDUM-28, ikke kjørt), `maalefiler.py`,
  `kryssjekk.py` (tre nye størrelser; versjonerte og sendte dokumenter regnes som låst; kataloger utenfor repoet),
  `utgivelse.py`, og `zenodo.py`, som laster opp og publiserer et bygget utkast (testet mot en falsk Zenodo, uten
  nettverk). `langdetect` står nå i `pyproject.toml`.
* **Testsettet er grønt i repoet, ikke fra depositumet alene.** I arbeidskopien: 515 tester, alle grønne, pluss én
  nettverkstest som ikke kjøres som standard. Fra `gjenopptak-src-0.6.0.tar.gz` alene feiler 34, fordi de leser
  filer som ikke ligger i tarballen: dokumentene i `docs/`, de låste filene i roten, `gjenvunnet/` og git selv. Fra
  en klone av git-bundelen feiler 10: ni trenger filer under `data/` som er git-ignorert og ligger på Vault
  (`data/l3-poc/fasit.jsonl` med flere), og én trenger OpenTimestamps-klienten i repoets `.venv`. Målt 10.10.2026.

## Endret form

Zenodo tar høyst 100 filer per post. For å få plass ligger disse nå i zip:

* `manuskript-tidligere.zip`: `MANUSKRIPT-v0.1.md`, `MANUSKRIPT-v3.1.md`, `MANUSKRIPT-v3.2.md`, `SVARBREV-v3.1.md`,
  `PREPRINT.md`.
* `utgivelser-tidligere.zip`: release notes for v0.4.0, v0.4.1 og v0.5.0, `UTGIVELSE-v0.4.0-PORTSTATUS.md`,
  `B5-PORTSTATUS.md`.
* `saker.zip`: også `SAKBEHANDLING-2026-09-27-kandidater.md` og `-triage.md`, under `sakbehandling/`.
* De to første har en `README-HISTORISK.md` som sier at status i filene er status den dagen de ble skrevet.
* `innhentet.zip`: de fem INNHENTET-filene, `INNHENTET-2026-09-26-en-koder.md` (som før lå for seg) og de fire nye.
  Med de to fra kontrollen ville posten ellers hatt 101 filer.

Filene er de samme som i v0.5.0 (v3.2 er ny), med ett unntak: **kandidatlista er renset.**
`SAKBEHANDLING-2026-09-27-kandidater.md` siterte passasjene den lister; de 83 ordrette utdragene på 50 tegn eller mer
(det lengste 1 039 tegn) er byttet med samme merke som i `maalefiler.zip`. Rettingen er gjort i filen i repoet
10.10.2026, med en datert merknad, og byggingen feiler om et utdrag står i den. Kopiene i v0.4.0–v0.5.0 står som de
ble publisert, og git-bundelen bærer lista slik den sto, i historikken. Posten har 97 filer. `maalefiler.zip` er bygget med faste tidsstempler, så
samme inndata gir samme bytes.

## Holdt utenfor

* **Ekskluderingsliste versjon 5 (10.10.2026):** som versjon 4, pluss `GJENOPPTAK_INSTRUKSER_*.md` og
  `GJENOPPTAK_FILKART_*.md` — arbeidsregler og lokale stier, ikke studiens dokumentasjon. De ligger i git-bundelen.
* **Andres tekst:** blindfilene deponeres som indeks, som før. Fulltekster og tekstbiter deponeres ikke.
* **Innsendingspapirene:** `docs/innsending/` (følgebrev og skjemasvar til tidsskriftet, og pakkebyggeren) er tatt ut
  av git 10.10.2026 og er ikke i depositumet. Se «Git-bundelen» under for hva historikken bærer.
* **Nøkler for ukjørte målinger:** nøkkelen til portens 320 passasjer (ADDENDUM-21 og -28 er låst og ukjørt på samme
  blindfil) og nøkkelen til den menneskelige valideringen (ADDENDUM-27).
* **Seks store filer** (rammelistene og verdiktene fra hentingsprøven) ligger på Vault med sha256 i manifestet.

## Scrub

Scrub over utgivelsestreet i git (elleve mønstre): ingen nøkkel, token, privat e-post eller absolutt hjemmesti. De
samme mønstrene er kjørt over hele utkastet, også filene som kommer fra Vault og innholdet i zip-filene: ingen
nøkkel, token eller privat e-post der heller. To mønstre har treff i git-treet, og ett til i Vault-filene; hvert er
redegjort for:

* **Forretnings-e-post, 5 linjer:** OpenAlex' polite-pool-parameter i det låste ADDENDUM-03; «Corresponding author»
  i manuskript v3.1, v3.2 og v3.3; og regelen i instruksfila om at e-post sendes fra forretningsadressen. Adressen er
  forfatterens offentlige kontaktadresse.
* **Ordet «sealed», 6 linjer:** prosaomtaler av scrub-mønsteret selv, i `B5-PORTSTATUS.md` (to), ADR-0012, de to
  instruksversjonene og denne linjen.
* **Absolutt hjemmesti, 7 filer fra Vault:** de ordrett gjenvunne oppdragene og sperrelistene sier hvilken katalog
  leseren skulle arbeide i. Fem av dem har ligget i `oppdrag.zip` siden v0.4.0; to er nye i `maalefiler.zip`
  (`fase3/presisjon/oppdrag-presisjon-MAL.md` og `sperreliste-presisjon.md`). Stien bærer forfatterens navn og ingen
  hemmelighet, og filene deponeres ordrett fordi de er måleinndata.

### Git-bundelen

Git-bundelen bærer hele historikken, som i de tidligere versjonene (eierens avgjørelse 10.10.2026). Tre ting ligger i
historikken og ikke i treet:

* Én privat e-postadresse som `mailto=`-parameter i `harvest/recallset2.py`, lagt til 12.09.2026 og fjernet
  25.09.2026. Bundlene i alle tidligere versjoner bærer den.
* Én absolutt hjemmesti i to filer, lagt til og rettet 02.–03.10.2026.
* **`docs/innsending/`:** katalogen er ute av treet fra 10.10.2026, men commitene der filene lå, følger historikken.
  14 av de 19 filene ligger alt i bundelen i v0.5.0. Fem kom senere og er ikke offentlige før denne versjonen: to
  følgebrev og to skjemasvar til *Scientometrics* og ett skjemasvar til Preprints.org.

Ingen nøkkel eller token finnes i historikken.

## Kjent

* Fem kosmetiske avvik fra kontrollen står: linjehenvisninger i addendumstatusen som ligger én linje for lavt eller
  gjelder Vault-originalen; at dette notatet ikke nevner at `blindfiler-indeks.zip` og `ots-kvitteringer.zip` er
  bygget på nytt; at én `pdf_url` fra OpenAlex i `maalefiler.zip` (`frames/frame-haandskrift-RAW.jsonl`) bærer et
  signert tredjeparts-token; og at `README.md` oppgir et annet filnavn for bundelen enn det den har i depositumet.
* Sakdokumentene, triagelista og noen andre filer som har ligget i depositumet før, siterer kildene ordrett med
  kildeangivelse: 56 utdrag på 50 tegn eller mer i 16 filer, det lengste på 158 tegn. `DEPOSITUMSKRAV-2026-10-10.md`
  § 7 teller dem. De er ikke endret; bare kandidatlista er renset.
* `zenodo.py` er testet mot en falsk Zenodo, uten nettverk. Denne versjonen er den første som deponeres med det.
* `ADDENDUM-20.md` § 7 sier fortsatt at kjøringen ble avbrutt. Den ble fullført samme dag; utfallet står i
  ADDENDUM-19 § 7.1 og i `maalefiler.zip` (`a19-a20-full-regelfil.json`).
* To bitall som ADDENDUM-19 § 4 varslet, er ikke regnet: κ over de 300 portpassasjene uten ankere, og paret
  differanse mellom Opus og Haiku. Dommerfilene de kan regnes fra, er med.
* Statuslinjen i `ADDENDUM-18.md` sier «ukjørt»; filen fører selv utfallet i § 7.
