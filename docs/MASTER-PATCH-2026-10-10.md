# MASTER-patch 2026-10-10 — landingen: hver åpen post ført, og hva v0.5 bærer

**§ 1 og § 2 er påført i `MASTER_GJENOPPTAK_v0_5_2026-10-10.md`** (bumpet 10.10.2026 med `bump-master.sh`), sammen
med `docs/MASTER-PATCH-2026-10-07.md`. **§ 3 er påført i `MASTER_GJENOPPTAK_v0_6_2026-10-10.md`** (bumpet samme dag;
POINTER peker dit). MASTER ligger på Vault og i `00-KONTEKST/`, ikke i git. Finansieringsstatus
føres bare i MASTER.

## 1 Endringer i MASTER v0.5

* **§ 0:** ny statusblokk. Zenodo v0.4.0, v0.4.1 og v0.5.0 er publisert; manuskript v3.3 er sendt til Scientometrics
  03.10.2026; preprinten er publisert på Preprints.org 07.10.2026 (10.20944/preprints202610.0368.v1); MetaArXiv avviste
  zvc34. Preprints.org brukes ikke videre — Zenodo er preprintkanalen.
* **§ 0:** ADDENDUM-19 er besvart for valget av leser: leseren er en agentisk Opus-instans, lokale modeller er sil
  (eierens beslutning 10.10.2026). Ingen nye målinger av leseren. Hva som bærer differansen, er ikke skilt. Differansen 0,812 − 0,636 er 0,177, paret bootstrap [0,044–0,323], verksklynget [0,057–0,318].
* **§ 0:** fase 4 er lukket (avbrutt 03.10.2026, data slettet). ADDENDUM-27 og ADDENDUM-28 er låst og ukjørt.
* **§ 2:** skrevet om: alle sju Zenodo-versjoner med DOI, dato og filtall; preprint; innsending; GitHub. Avsnittet om
  at regelfilen «må med i neste deponering» er erstattet: den har vært med siden v0.4.0, og det som mangler i v0.5.0,
  står i `docs/DEPOSITUMSKRAV-2026-10-10.md`.
* **§ 9:** tabellen under.

## 2 Hver åpen post fra MASTER v0.4 § 9 og patchene siden

Status for hver post over, slått opp 10.10.2026. **Rettet** = gjort. **Gjeldende** = står åpen. **Utgått** = ikke
lenger aktuell. Samme liste står i MASTER v0.5 § 9.

| post | status | grunnlag |
|---|---|---|
| Preprintens moderering (MetaArXiv) | **utgått** | avvist 30.09.2026; Preprints.org-DOI 10.20944/preprints202610.0368.v1 inn i `CITATION.cff` med v0.6.0 |
| Kronikk til forskning.no | **gjeldende** | utløseren er innfridd (preprint publisert 07.10); ingen kronikk er skrevet |
| DOI 22976464 mot doi.org | **rettet** | svarer 302 (10.10.2026) |
| Heron utenfor BL | **gjeldende** | kartlagt 26.09.2026 (elleve kilder, § 6); åpent er RGK 1c, de to paleografiske studiene, institusjonene som ikke er søkt, og at ingen forespørsel er sendt |
| Frontier-dommer | **utgått** | ingen betalte modell-API-er; leseren er avgjort |
| L2 med embeddings | **utgått** | målt og forkastet: ADDENDUM-14 (embeddings) og ADDENDUM-15 (seksjon og nærsøk) |
| Uavhengig menneskelig annotør | **gjeldende** | ADDENDUM-27 låst 03.10.2026, prøven trukket, ingen annotatør rekruttert |
| Koder 2s regelfil inn i depositumet | **rettet** | i v0.4.0, v0.4.1 og v0.5.0 |
| «Én koder» i låste filer | **rettet** | `docs/INNHENTET-2026-09-26-en-koder.md` |
| Den preregistrerte porten falt, lista heter kandidatliste | **gjeldende** (faktum) | fase 3 ga «arbeidsliste (prospektiv port)» for 673 rader; de 432 er uendret kandidatliste |
| E-posten i Zenodo-bundlene | **gjeldende — eierens valg** | gjelder alle sju versjoner; valget for v0.6.0 står under «Nye åpne poster» |
| `CITATION.cff` sier 0.3.0 | **rettet** | 0.5.0 i v0.5.0; 0.6.0 i utkastet |
| Ti commits er ikke pushet | **utgått** | publiseringspolicyen: `main` pushes aldri, `offentlig` får én utgivelsescommit per versjon |
| ADDENDUM-21 arm A | **utgått som plan** | låst og ukjørt; ingen nye målinger av leseren. Tersklene i § 5 er dessuten satt på feil intervall (KORRIGENDUM § A) |
| Tre utløsere fra fase 2 (SAK-08, -11, -17) | **gjeldende** | ikke sjekket på nytt 10.10 |
| Ingen ekstern har lest koden | **gjeldende** | vurderingen 03.10 gjaldt manuskriptet, og leseren var en språkmodell |
| Manuskript v2 skrives fra faktafila | **utgått** | manuskript v3.3 er sendt |
| `tvil`-flaggets nivå på tvers av kodere | **gjeldende, ikke planlagt** | umålt |
| Klasse-κ 0,501 måles om på nytt materiale | **gjeldende, ikke planlagt** | umålt |
| Zenodo v0.4.0 publiseres | **rettet** | publisert 01.10.2026; v0.4.1 og v0.5.0 etter |
| `silrecall` i registerhodet | **gjeldende** | skjemaet tillater fortsatt bare «ikke målt» |
| Manus v2.8: kjent rest | **utgått** | erstattet av v3.x og faktasjekk v3 |
| Kjedegjeld: `steg_les`, ekstraksjonen, `CCLeser` | **rettet** 02.10.2026 | commits `07dc97f` og `f70e794` |
| Kjedegjeld: ledd-ferdig nøkles på inndata-sha; 7c-skriveren | **gjeldende** | ikke gjort |
| Trekkingen fører ikke OpenAlex-kvoten før | **rettet for fase 4** | 813 før, 804 etter (RESULTAT-ADDENDUM-26 § 0) |
| Kandidatlista på 432 er ikke deponert | **rettet** | `register-v2-indeks.jsonl` i v0.5.0 |
| Navnekontrollens skanner til `src/` | **gjeldende** | ligger på Vault, `navnekontroll/navnekontroll.py` |
| Fase 3 for de tre andre feltene | **gjeldende, ikke planlagt** | fase 4 var ett nytt felt og ble avbrutt |
| Fase 3 hadde ingen sakbehandling | **gjeldende** | utvalg gjort 10.10: 53 løftbare erklæringer, 16 vurdert som konkrete, fem foreslått som saker; ingen sak opprettet. Vault `saker/fase3-utvalg-2026-10-10/` |
| Recall-klyngene: nytt referansesett med tak per verk | **gjeldende, ikke planlagt** | — |

**Nye åpne poster 10.10.2026:**

* **Zenodo v0.6.0 og push av `offentlig`** venter på eierens «ja».
* **E-posten i git-bundelen.** En privat adresse står i historikken som `mailto=`-parameter i
  `harvest/recallset2.py`, lagt til 12.09.2026 og fjernet 25.09.2026. Bundlene i alle sju publiserte versjoner bærer
  den, og de kan ikke endres. v0.6.0-utkastet er bygget med hele historikken, som før. Alternativet er en bundle med
  bare `offentlig`-historikken, uten adressen og uten commit-for-commit-historikk. Eierens valg før publisering.
* **Nøkkelen til port-320 og koder 1s verdikter:** v0.6.0-utkastet bærer koder 1s verdikter uten tekst og nøkkelfelt;
  selve nøkkelen holdes ute så lenge ADDENDUM-21 og -28 står ukjørt. Eierens avgjørelse.
* **MASTER i git:** kontekstsettet ligger i `00-KONTEKST/`; MASTER er ikke lagt i `docs/`, fordi alt der følger
  git-bundelen og GitHub ut. Eierens avgjørelse.
* **Planlagte bitall i ADDENDUM-19 som ikke er regnet:** κ over de 300 portpassasjene og paret differanse Opus mot
  Haiku. Kan regnes fra dommerfilene uten ny kjøring.

## 3 Endringer i MASTER v0.6 — eierens avgjørelser i landingens runde 2 og 3 (10.10.2026)

v0.5 står urørt i arkivet. *(Rettet 10.10.2026: avgjørelsene fra runde 2 ble først skrevet inn i v0.5 på stedet, og
denne patchen speilet det. Eier ba om bump i stedet; v0.5 er gjenopprettet byte for byte, sha256 `3a751cb8…`, og
§ 1–2 over står igjen slik de var.)*

* **§ 0:** ny statusblokk for v0.6 over den fra v0.5; ny rad i changeloggen.
* **§ 2:** GitHub-raden sier at taggen `v0.5.0` står på `cd7c032`, treet Zenodo v0.5.0 ble bygget fra.
* **§ 9, tabellen:** «E-posten i Zenodo-bundlene» er avgjort: v0.6.0 bærer hele historikken.
* **§ 9, «Nye åpne poster»:** publisering og push venter på uavhengig kontroll i ny økt og eierens «ja»;
  bundlevalget er ikke lenger åpent; nytt punkt om det historikken bærer og treet ikke har (den private
  e-postadressen, `docs/innsending/`, kandidatlista slik den sto).

Avgjørelsene:

| avgjørelse | runde | hvor det er gjort |
|---|---|---|
| Git-bundelen i v0.6.0 bærer hele historikken | 2, bekreftet i 3 | `--bundle alle` i `utgivelse.py` (`0309650`) |
| `docs/innsending/` ut av git; følgebrev og skjemasvar publiseres ikke som filer | 2 | `ac8225c`; Vault `innsending/fra-repo-docs-innsending-2026-10-10/` |
| Kandidatlista: 83 ordrette utdrag ut, i depositumet og i repoet | 2 og 3 | `f4727c3`, `a3c8f65`; original på Vault `saker/kandidatliste-original-2026-09-27/` |
| Opplasting og publisering skrives i repoet, testet uten nettverk | 2 | `src/gjenopptak/zenodo.py` (`ec15bb3`) |
| `gjenvunnet/addendum-19/README.md`: regenerert, ikke byte-verifisert | 2 | `d21624b` |
| Taggen `v0.5.0` på treet Zenodo v0.5.0 ble bygget fra, med de 14 innsendingsfilene | 3 | `cd7c032`, tre lik `f0bc64b`; verifisert mot bundelens HEAD og kildetarballen i depositumet |
| MASTER bumpes, endres ikke på stedet | 3 | v0.6; v0.5 gjenopprettet |
