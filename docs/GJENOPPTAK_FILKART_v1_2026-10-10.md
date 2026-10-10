# GJENOPPTAK — filkart

**Versjon:** v1
**Dato:** 10.10.2026
**Filnavn:** `GJENOPPTAK_FILKART_v1_2026-10-10.md`

Hvor hovedstedene ligger. Én linje per sted. Stiene er slått opp på disk 10.10.2026. Filkartet sier hvor en fil bor,
ikke hva som står i den; tilstand slås opp i filen selv. Kartet er ikke uttømmende: `MANIFEST-VAULT.md` fører hver fil.

## 1 Kontekstsettet — leses først

`~/Desktop/Gjenopptak-samling/00-KONTEKST/`. Nyeste versjon og dato i filnavnet gjelder.

| fil | hva | også i |
|---|---|---|
| `GJENOPPTAK_ADDENDUMSTATUS_v1_2026-10-10.md` | PREREG-v1 og ADDENDUM-01–28: låst, kjørt, utfall, fil, Zenodo. Leses før noe addendum foreslås | `docs/` |
| `GJENOPPTAK_MASTER_v0.6_2026-10-10.md` | strategi, beslutninger, publiserings- og finansieringsstatus, åpne poster | Vault `master/arkiv/` (kanon, annet navn) |
| `GJENOPPTAK_INSTRUKSER_v1.4_2026-10-10.md` | arbeidsreglene for sporet | `docs/` |
| `GJENOPPTAK_FILKART_v1_2026-10-10.md` | denne filen | `docs/` |
| `repo-disiplin.md` | felles regelverk for alle repoer, versjon 2 (10.09.2026), uendret | Vault-roten |

## 2 Repoet — `~/dev/gjenopptak`

| sted | hva |
|---|---|
| `PREREG-v1.md`, `ADDENDUM-01.md` … `ADDENDUM-28.md` | de låste dokumentene. Ligger i roten; bare der utløser de kanon-bundelen |
| `README.md`, `CITATION.cff`, `LICENSE`, `LICENSE-DATA` | forsiden, sitering, Apache-2.0 på kode, CC BY 4.0 på egne data |
| `docs/METODE.md` | metoden slik den gjelder nå |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md`, `docs/TALLMANIFEST.md` | hvert tall i manuskriptet med sti og sha256 |
| `docs/LAERDOM.md` | lærdomsloggen, én seksjon per funn |
| `docs/RESULTAT-PORT-v1.md`, `docs/RESULTAT-ADDENDUM-24.md` … `-27.md` | utfallsnotater |
| `docs/REANALYSE-2026-10-03.md` | verksklyngede intervaller og den parede testen etter den eksterne vurderingen (en språkmodell) |
| `docs/INNHENTET-*.md`, `docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md` | utsagn i låste filer som er innhentet, med peker fra README |
| `docs/DEPOSITUMSKRAV-2026-10-10.md` | hva hver måling leste, og hva depositumet bærer av det |
| `docs/MANUSKRIPT-v*.md`, `docs/SVARBREV-v3.1.md`, `docs/PREPRINT*.md` | manuskriptversjonene; v3.2 gikk til Preprints.org, v3.3 til Scientometrics |
| `docs/decisions/` | ADR-ene (0001–0014; 0005 og 0006 er brent) |
| `docs/saker/`, `docs/PS-246-*.md`, `docs/SAKBEHANDLING-*.md` | sakbehandlingen: kriterium låst før utførelse, resultat, saksregister |
| `docs/ZENODO.md`, `docs/RELEASE-NOTES-v*.md` | deponeringsrutinen og hva hver versjon bærer |
| `docs/MASTER-PATCH-*.md`, `docs/patch/` | patcher til MASTER og instruksfila; påføres ved bump |
| `docs/innsending/` | **ikke i git fra 10.10.2026** (står i `.gitignore`). Følgebrev og skjemasvar publiseres ikke; kildene ligger på Vault, se § 3. Historikken før 10.10. bærer dem fortsatt |
| `docs/GJENOPPTAK_*.md`, `docs/INSTRUKSER-v1.2.md`, `-v1.3.md` | kontekstsettet og de erstattede instruksversjonene |
| `src/gjenopptak/` | koden: `harvest/` (ramme, trekking), `parse/`, `classify/` (dommer, porter, reliabilitet, reanalyse), `kjede/` (sil, leser, register), `kryssjekk.py`, `scrub.py`, `utgivelse.py` (bygger utkastet), `zenodo.py` (laster opp og publiserer), `maalefiler.py`, `vault.py`, `speil.py`, `securerepo.py` |
| `tests/` | testsettet; `pytest` kjører alt unntatt nettverkstesten, `pytest -m network` den |
| `prompts/`, `kjede.toml`, `felt/` | ledetekster, kjedens konfigurasjon, feltdefinisjonene |
| `gjenvunnet/addendum-19/` | skriptene bak ADDENDUM-19, 19b og 20, gjenvunnet fra øktutskriften, med `OPPHAV.md` |
| `data/` | lokale arbeidskopier; ikke i git. Vault-kopien er den som gjelder |
| grenen `main` | arbeidsgrenen; pushes aldri |
| grenen `offentlig` | det som pushes til `main` på GitHub: rotcommit pluss én utgivelsescommit per utgivelse. Taggene `v0.3`, `v0.4`, `v0.4.1`, `v0.5.0`, `v0.6.0` peker hit |

## 3 Vault — `/Volumes/Vault/gjenopptak-kilder/`

Alt materiale. Ingenting her ligger i git.

| sted | hva |
|---|---|
| `MANIFEST-VAULT.md` | sti, bytes, sha256 og tidspunkt for hver fil som er sikret; opphav for gjenvunne filer. Føres etter hver økt |
| `repo/kanon/` | git-bundler utløst av PREREG- og ADDENDUM-commits; `ots/` har tidsstemplene. Nyeste er autoritativ |
| `repo/kode/` | git-bundler av koden, restaureringsmateriale |
| `repo/laste-filer/` | PREREG-v1 og ADDENDUM-01–09 som rene filer |
| `resultat/` | speil av dokumentene i pliktlisten (`PLIKT` i `speil.py`), holdt i sync på sha256 |
| `master/arkiv/` | MASTER-versjonene og `POINTER.txt`, som navngir den gjeldende |
| `frames/` | de frosne rammelistene per felt |
| `raw/`, `logs/` | OpenAlex-svarene og måleloggene fra rammearbeidet (ADDENDUM-01–09) |
| `utvalg/`, `trekking-*/` | trekkspesifikasjoner, utvalg og trekklogger for de 100 verkene |
| `fulltext/`, `fulltext-direkte/`, `fulltext-rammeprove-energimodellering/` | hentet fulltekst; deponeres aldri |
| `presisjonssett/`, `presisjonssett-2026-09-20/` | portens 320 passasjer: blindfil, nøkkel, koder 1s og koder 2s verdikter |
| `koder2/`, `koder4/`, `oppdrag-gjenvunnet/` | koder 2s regelfil, koder 4s verdikter, de gjenvunne oppdragene med sperrelister og øktutskriftene |
| `ekstraksjon/2026-09-26/` | ADDENDUM-16–20: ekstraksjonstestene og dommerfilene for Haiku, Sonnet og Opus; `addendum-19/kode-gjenvunnet/` |
| `embeddings/`, `form-ruter/` | ADDENDUM-14 og -15 |
| `triage-loftbare-*`, `verksniva-*` (i roten) | ADDENDUM-12 og -13 |
| `arbeidsliste/`, `kandidat432/` | ADDENDUM-22 og -23: de 2 844 passasjene, verdiktene, kandidatlista |
| `leser-lokal-ADDENDUM-24/` | qwen-kjøringen |
| `fase3/`, `fase3-kjede/` | ADDENDUM-25: kjeden, referansesettet, presisjonsporten, registeret, øktutskriftene |
| `fase4/` | ADDENDUM-26: det som er igjen etter avbruddet (ramme, trekklogg, sporfiler) |
| `revisjon-2026-10/` | reanalysen, register v2 som indeks, og den menneskelige valideringen (blindfil, nøkkel, skjema, utvalg) |
| `saker/`, `kilder-ps246/`, `falsifisering-2026-09-21/` | sakbehandlingens arbeidsfiler og kilder |
| `manuskript/` | rendret manuskript og preprint, faktasjekkene |
| `fagfellevurdering/gpt-2026-10-03/` | rapporten og instruksen fra den eksterne vurderingen 03.10.2026. Leseren var en språkmodell (GPT) |
| `fagfellevurdering/opus5-2026-10-03/` | et avbrutt forsøk på samme vurdering med Opus 5; ingen rapport |
| `innsending/`, `register/`, `kontrollsok-tekstvitenskap-2026-09-13/` | følgebrevet som ligger klart til revisjon; `claims.jsonl`; kontrollsøket fra ADDENDUM-08 |
| `innsending/fra-repo-docs-innsending-2026-10-10/` | de 19 filene som lå i `docs/innsending/` i repoet (følgebrev, skjemasvar, pakkebygger), flyttet ut 10.10.2026 med sha256 i manifestet |
| `saker/fase3-utvalg-2026-10-10/` | utvalget av løftbare erklæringer fra fase 3 (53, hvorav 16 vurdert som konkrete) |
| `saker/kandidatliste-original-2026-09-27/` | kandidatlista slik den sto før de 83 ordrette utdragene ble tatt ut av repo-filen 10.10.2026 |
| `navnekontroll/` | navnekontrollens skanner og treff |
| `zenodo/` | byggene: `v<versjon>-utkast/` er det som lastes opp, `v<versjon>-bygg/` har byggemanifestet og Zenodo-kvitteringen |
| `royk/`, `readme-test/`, `b6-test/`, `lokal-sikret-2026-09-28/` | røyktester og sikrede lokale kjøringer |

Lokale modeller: `/Volumes/Vault/ollama/` (lenket fra `~/.ollama/models`).

## 4 Samlemappa — `~/Desktop/Gjenopptak-samling/`

| sted | hva |
|---|---|
| `00-KONTEKST/` | kontekstsettet (§ 1) |
| `01-artikler/` … `08-fagfellevurdering/` | **øyeblikksbilde fra 03.10.2026**, kopier med eget manifest (`00-MANIFEST-SHA256.json`). Oppdateres ikke; `00-LESMEG.md` beskriver tilstanden den dagen. Rapporten i `08-fagfellevurdering/` står ikke i det manifestet; Vault-kopien gjør |
| `09-INNSENDING/` | eneste kilde for innsending. `00-PLAN.md` er eneste status; `00-MANIFEST.json` har sha256. Frosset til redaktøren svarer |
| `09-INNSENDING/01-preprints-org/`, `02-scientometrics/`, `03-kvitteringer/` | det som ble sendt, det som ligger klart til revisjon, og kvitteringene |
| `10-FINANSIERING/` | søknadene. `GJENOPPTAK_FINANSIERING_00-PLAN.md` er planen; undermapper per finansiør; stemmepass inn og ut |

## 5 Utenfor maskinen

| sted | hva |
|---|---|
| Zenodo, konsept-DOI 10.5281/zenodo.22959326 | depositumet, sju versjoner til og med v0.5.0 |
| `https://github.com/avalyset/gjenopptak` | grenen `main` der er lokal `offentlig`; siste pushede utgivelse er v0.4.1 |
| Preprints.org, 10.20944/preprints202610.0368.v1 | preprinten (manuskript v3.2) |
| Scientometrics | innsendingen 03.10.2026 (manuskript v3.3); status i `09-INNSENDING/00-PLAN.md` |

## 6 Verktøy og nøkler

| sted | hva |
|---|---|
| `~/bin/bump-master.sh` | versjonsbump av MASTER: header, filnavn og POINTER i én operasjon |
| `.git/hooks/post-commit` | kjører `securerepo`: speiler dokumentene til Vault og skriver kanon-bundle når en låst fil committes |
| `~/.config/` | nøkkelfilene for Zenodo og OSF. Leses av CC, nevnes aldri i chat. Repoet har ingen `.env` |
