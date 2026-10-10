# Utfall av ADDENDUM-26 — fase 4, håndskriftstudier

**Status 03.10.2026: avbrutt og ryddet etter eierens beslutning, før noen port var målt. Data slettet; ramme og protokoll bevart.**

## 0 Avbrutt 03.10.2026, før noe ledd etter dommeren var kjørt og før noen port var målt

**Grunn:** ressursbruk; delstudien ligger utenfor manuskriptets omfang. Eierens avgjørelse 03.10.2026.

**Hvor langt kjøringen kom:**

| steg | status |
|---|---|
| trekking (02.10) | ferdig: 100 verk fra 431 posisjoner; OpenAlex-kvote 813 før, 804 etter |
| referansesett | ferdig: 20 verk lest til siste setning (R14 lest på nytt etter et avbrudd, forsøket satt til side i `fase4/referanse/avbrutt/R14-1`) |
| referansenøkkel | sikret 03.10 10:03 UTC: `NOKKEL-referansesett.jsonl`, sha256 `60439c6a61d22cb6…`, rad i manifestet; OpenTimestamps-stempelet kom etter manifestraden (ots-kjørbaren ble ikke funnet fra worktreet), men før noe kjedeledd |
| `hent`, `tekstbiter` | ferdig: 100 verk, **31 031** tekstbiter |
| `dommer` | **delvis: 830 av 31 031** dømt (`3-dommer.jsonl`, sha256 `6c9468c2a7bf7aad96b4dda39441f1e9d136fe3980ba98c8e6fb4f904db1d0d9`, 856489 B, 830 gyldige linjer, siste linje hel); ikke ført som ferdig i `tilstand.json` |
| ekstraksjon, union, blind, les, etterledd | ikke kjørt |
| porter (1) og (2), tilleggsmålet | **ikke målt** |

**Stoppet** med SIGTERM til driverens prosessgruppe og deretter til `ollama serve`, 03.10.2026 kl. 11:04 UTC.
Ingenting er slettet.

**Ryddet samme dag (eierens beslutning).** Fase 4-dataene er tatt ut: hentede og trukne fulltekster (`fase4/hentet`, `fase4/utvalg`),
referanselesingene med nøkkel og ots-stempel (`fase4/referanse`), og worktreet med tekstbiter, de 830 dommene og tilstanden
(`fase4/worktree-7ebf7aa`; registreringen fjernet med `git worktree prune`) — 366 MB på Vault, pluss 11 MB øktutskrifter fra
referanseinstansene på systemdisken. Alt er flyttet til papirkurven og er borte når den tømmes. **Kjøringen kan ikke lenger
gjenopptas.**

**Bevart:** protokollen (`ADDENDUM-26.md`, låst `7ebf7aa`), den frosne rammelista (`frames/frame-haandskrift-RAW.jsonl`, 807 rader,
sha256 `6e444a08…`), denne fila, manifestradene for alt som ble skrevet, og de små sporfilene i `fase4/` (trekkspesifikasjon,
trekklogg, utvalgslista med verk-ID og sha256 uten tekst, OpenAlex-svarene i `raw/`, logger, driveren).

**Hva som kan regenereres:** trekkingen er deterministisk gitt rammen, frøet og hentingsporten — men hentbarheten avhenger av
utgivernes nettsteder den dagen, så et nytt utvalg kan avvike. Tekstbitene og dommerens utdata er deterministiske gitt de samme
fulltekstene. **Referanselesingene og nøkkelen kan ikke gjenskapes byte for byte:** de var ikke-deterministiske modellesninger,
og en ny kjøring er en ny referanse.

**Hva det betyr:** fase 4 har ikke gitt noe resultat. Hypotesen i ADDENDUM-26 § 1 er verken støttet eller svekket.
Referansesettets tall rapporteres ikke (ADDENDUM-26 § 4), og grunnlaget for dem er ryddet.
