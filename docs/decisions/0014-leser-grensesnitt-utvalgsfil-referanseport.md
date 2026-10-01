# ADR-0014 — Leseren bak ett grensesnitt, utvalgsfil for nytt materiale, og referanseporten

**Dato:** 2026-09-28. **Status:** vedtatt. **Skrevet etter koden.**

**Hvorfor etter.** Koden kom i `f38bd74` som verktøy for ADDENDUM-24 og -25, og addendaene låste den
med sha256. Beslutningene som koden inneholder, ble tatt i addendatekstene og i commit-meldingen, men
ingen ADR ble skrevet. Det ble funnet i en disiplinkontroll samme dag. Denne ADR-en er skrevet fra koden
og addendaene slik de står, og **dokumenterer beslutninger som alt var tatt**; den er ikke grunnlaget de
ble tatt på. Nummeret er kontrollert ledig mot alle refs og hele historikken (0005/0006 er brent, jf.
README).

## Kontekst

ADR-0012 gjør kjeden til én sti — ramme → henting → tekstbiter → sil → leser → register — og sier at
leseren er en agentisk Opus-instans og at ett-kall-modeller er sil-klasse. Tre ting manglet:

1. Silen hadde et grensesnitt (`kjede/sil.py`, `Sil`), leseren hadde ikke. En ny leser kunne ikke
   prøves uten å skrive om leddet.
2. `hent` kjente bare portens 100 verk (`data/port/spesifikasjon.json`). Nytt materiale kunne ikke
   kjøres gjennom kjeden uendret.
3. Et referansesett som skal bygges **før** silen, var en regel i prosa (ADDENDUM-25 § 3.5), ikke i
   koden.

## Beslutning

**1 Leser-protokollen** (`src/gjenopptak/kjede/leser.py`): `leser(regler, parti) -> Lesning`, med
`signatur()`. To implementasjoner:

* `CCLeser` — Claude Code-instans med `claude -p`, agentisk, leser filene selv. `steg_les` bruker den;
  oppførselen er uendret fra ADR-0012.
* `LokalLeser` — ollama-modell med regelfil og et parti tekstbiter i samme kontekst, JSON-skjema med
  kodernes felter, `done_reason` ført.

**Klassen en leser havner i, avgjøres av en preregistrert port mot koder 1, ikke av implementasjonen.**
`LokalLeser` med `qwen2.5:7b` er målt til κ = 0,248 og er sil-klasse (ADDENDUM-24,
`docs/RESULTAT-ADDENDUM-24.md`). `valider()` fyller aldri ut en manglende dom.

**2 Utvalgsfil** (`gjenopptak run --utvalg <fil>`): `hent` finner verk utenfor porten i en utvalgsfil med
`work_id`, `felt`, `fil` (relativ til Vault-målet), `sha256`, `port_ledd`, `doi`, med samme sha256-kontroll
som for portens verk. Et verk som står både i porten og i utvalgsfilen, er en feil — da er det ikke nytt
materiale. For kjente verk endres ingenting.

## Konsekvenser

* En ny leser kan **måles** mot porten uten å røre leddene (`classify/leser_port.py`). Å sette den inn i
  `les` krever kodeendring: `steg_les` instansierer `CCLeser` direkte (`kjede/ledd.py`), og `--leser`
  godtar bare `subagent` og `cli` (`kjede/cli.py`). At en leser ikke får lese for et register før den har
  bestått porten sin, er en regel i prosa; den håndheves ikke i kode. *(Rettet 28.09.2026, frys-lesning 2:
  sto «En ny leser settes inn uten å røre leddene, men den får ikke lese for et register før den har
  bestått porten sin».)*
* Nytt materiale kan kjøres uten kodeendring i kjeden, så lenge det har en utvalgsfil på Vault.
* Kjedeinstansene startes i repoet (som i ADDENDUM-22) og ser git-status i systemprompten. Referanse- og
  presisjonsinstansene i fase 3 startes utenfor repoet (`classify/fase3.py`). Forskjellen er bevisst og
  står i ADDENDUM-25 § 4. *(Merknad 30.09.2026: etter gjenopptakene 29.–30.09 ble fase 3s leserinstanser startet
  i worktreet på låsecommiten `f19a3e3` på Vault, ikke i arbeidstreet — RESULTAT-ADDENDUM-25 § 0.3 og § 0.6.)*

## Forkastet

* **Leseren som konfigurasjonsvalg uten port** — ville latt en billigere modell gli inn i leserleddet
  uten måling. ADR-0012 forbyr det for ett-kall-modeller; protokollen utvider forbudet til alle.
* **En ny spesifikasjonsfil per materiale i stedet for `--utvalg`** — ville krevd endring i
  `kjede.toml` for hver kjøring, og `kjede.toml` er låst med sha256 i ADDENDUM-25.

## Tillegg 28.09.2026 — referanseporten i koden

**Funnet:** ADDENDUM-25 § 3.5 sa at ingen del av kjeden kjøres før nøkkelens rad står i manifestet, men
kjeden håndhevet det ikke. I den første fase 3-kjøringen holdt rekkefølgen **fordi kommandoene ble kjørt i
riktig rekkefølge**: nøkkelen skrevet 10:20:02Z, manifestraden 10:20:05Z, kjeden startet 10:20:33Z. En regel
som bare finnes som prosa, er ikke en regel (LAERDOM § 31).

**Beslutning:** `src/gjenopptak/kjede/referanseport.py`. Et materiale **erklærer** et referansesett ved at
katalogen utvalgsfilen ligger i, har `referanse-verk.json`. Da nekter `gjenopptak run` å starte
`dommer`, `ekstraksjon`, `union`, `blind`, `les`, `verksniva`, `falsify` og `register` (exit 2) før
**alle** erklærte verk har treffil og feilfri brukslogg, og før `NOKKEL-referansesett.jsonl` finnes med en
sha256 som står i `MANIFEST-VAULT.md`. En nøkkel som er endret etter at raden ble skrevet, feiler dermed
også. Porten har **ikke noe flagg av**; tørrkjøring (`--torr`) starter ingenting og sjekkes ikke. Uten
erklært referansesett gjelder den ikke.

**Testet** med hvert tilfelle den skal feile på (`tests/test_referanseport.py`): manglende treffil,
manglende brukslogg, økt med feil, manglende nøkkel, nøkkel utenfor manifestet, nøkkel endret etter
sikring. Mot det ekte fase 3-materialet slipper den: 20 verk, nøkkel `6e38c3a7…` i manifestet.

**Avvik fra låsen, ført:** koblingen står i `kjede/cli.py`, som ADDENDUM-25 § 9 låser med sha256
`c2eb33bc…`. Fase 3-kjøringen som går, startet 10:20:33Z og lastet den låste versjonen; tillegget endrer
ikke den kjøringen. *(Merknad 30.09.2026: kjøringen er ferdig og ble gjenopptatt fra den låste `cli.py`; bare
det rettede registerleddet ble kjørt fra arbeidstreet, der referanseporten står og bestås — § 0.8.)* Avviket står i `docs/RESULTAT-ADDENDUM-25.md` § 0, ikke i den låste teksten.
