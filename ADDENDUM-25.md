# ADDENDUM-25 — fase 3: nytt materiale, referansesett bygget først, prospektiv port

**Skrevet:** 2026-09-28, **før trekking og før kjøring.** **Status: LÅST ved commit, før noe verk er trukket.**
**Gjelder:** ADDENDUM-22 §6, ADDENDUM-23 §5 og silens recall (METODE, «silrecall: ikke målt»).
**Ingen Anthropic-API.** Modellene er lokal ollama og Claude Code-instanser på abonnementet.

## 1 Hvorfor

Kandidatlista på 432 har bestått en **post hoc** port (ADDENDUM-23). Silens recall er **aldri målt**: de 27
kjente treffene var silens egen utgang, så «27 av 27 i unionen» sier at silen gjenfinner det den selv har
funnet, ikke hvor mye den mister. Dette addendumet er den første **prospektive** testen: nytt materiale,
et referansesett bygget og sikret **før** silen og leseren kjøres, og porter satt her, før noe er trukket.

## 2 Materialet, låst

| | verdi |
|---|---|
| ramme | den frosne arkeologi-rammen, `frames/frame-arkeologi-RAW.jsonl` på Vault, 37 510 rader, sha256 **`1050450fc774e56affc21c99e0ffc3c59682ff391c1e46163c69a50d5cdf241a`** (`felt/arkeologi.yaml`) |
| rekkefølge | `random.Random(734248).shuffle` av den leksikografisk sorterte rammelisten (`draw.draw_order`, frø **734248**). Rekkefølgens sha256 føres i trekkspesifikasjonen |
| ekskludert | **de 100 verkene som alt er brukt** (`data/utvalg/utvalg-*.jsonl`, alle fire felt) som `brukt`; de positive kontrollene og de leste (`logs/leste-kontrollkandidater.json`) som i ADDENDUM-09 |
| vilkår | uendret fra ADDENDUM-09 (`draw.decide`): typefilteret, feltets emne blant verkets tre høyeste topics (T10087, T10421), hentingsporten P1/P3 (ADDENDUM-04 §1.1) og identitetsporten på P3 (ADDENDUM-07 §8) |
| antall | **100**, sekvensielt; trekkingen stopper ved 100. Ingen substitusjon |
| kode | `src/gjenopptak/harvest/draw_fase3.py` (sha256 i §9) |
| utdata | Vault `fase3/`: trekkspesifikasjon, trekklogg, `utvalg-fase3-arkeologi.jsonl`, `verk-fase3.txt`, filene i `fase3/utvalg/` |

**Hvorfor ny rekkefølge og ikke fortsettelse av den gamle.** Den gamle rekkefølgen (prereg-frøet) er brukt til
posisjon 94 og karakterisert på de 200 første. Oppdraget for fase 3 angir frø 734248; en ny stokking med
målefrøet gir et utvalg som ikke arver noe fra hvor den første trekkingen stoppet.

## 3 Referansesettet — bygget FØR silen og leseren

1. **20 av de 100**, `random.Random(734248).sample(sorted(work_id), 20)` (`draw_fase3 referanseutvalg`).
2. Hvert av de 20 skrives ut som **nummererte setninger med kjedens egen parser** (`classify/fase3.py
   referansetekst`), slik at setningsnummeret er det samme som tekstbitenes `start_index`/`end_index`.
3. **Én CC-instans per verk**, hodeløst med `claude -p --model claude-opus-5` (samme modell-ID som koder 2 og
   koder c), **tom kontekst, serielt, egen kladdekatalog**. Instansen startes med **arbeidskatalog på Vault,
   utenfor repoet**, og uten MCP-servere (`--strict-mcp-config`): en instans startet i repoet får git-status og
   ferske commit-emner i systemprompten (`classify/fase3.py referanse-les`). Instansen får nøyaktig to filer: regelfilen
   `koder2/koderegler-gjenvunnet.md` (sha256 **`234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449`**)
   og sitt eget verk. **Sperreliste** i oppdraget: alt i repoet og på Vault utenom de to filene, særlig de andre
   verkenes tekster, alt annet under `fase3/`, kjedens kjøringer, alle addenda, `docs/`, og alle verdikt-,
   nøkkel- og blindfiler; `git log/show/diff/blame` forbudt. Oppdraget er malen `OPPDRAG` i `classify/fase3.py`.
4. Instansen leser **hele verket** og noterer hvert treff som **setningsnumrene treffet består av** (det ugjorte
   og hindringen), med klasse, `tvil` og én setnings begrunnelse. Begge deler må ligge innenfor **5 påfølgende
   setninger** — passasjeenheten (ADDENDUM-03 §1.2). Et notert treff med større spenn føres, merkes
   `gyldig_spenn: false`, og teller i nevneren.
5. **Nøkkelen sikres før neste steg:** alle treff samles til `fase3/referanse/NOKKEL-referansesett.jsonl`, sha256
   føres i `MANIFEST-VAULT.md`, og filen stemples med OpenTimestamps (`sikre-nokkel`). **Ingen del av kjeden kjøres
   før den raden står i manifestet.** Nøkkelen redigeres aldri etterpå.

## 4 Kjeden, uendret

`gjenopptak run --verk fase3/verk-fase3.txt --utvalg fase3/utvalg-fase3-arkeologi.jsonl --navn fase3-kjede`,
med `kjede.toml` slik den står i låsecommiten: dommer `gemma2:9b` (ledetekst `de9f8229…`), ekstraksjon
(`c8c276df…`), unionen med alle-treff-kobling, G3-merking (`63ed7345…`), blindfiler stokket med frø 734248, og
leseren **CC-instans `claude-opus-5`, serielt, ≤ 356 tekstbiter per økt, egen kladdekatalog per økt** (`--leser
cli`). Leserøktene startes i repoet, som i ADDENDUM-22, og ser derfor git-status og ferske commit-emner i
systemprompten; tekstbitene har nye blinde id-er og ingen verdikter står i commit-emnene. **Ingen commit-melding
nevner referansesettets innhold eller tall før målingen i §5 er gjort.** Eneste kodeendring i kjeden er `--utvalg`, som lar `hent` finne verk utenfor portens 100 på samme
sha256-kontroll; den endrer ingenting for kjente verk.

## 5 Portene, låst nå

**(1) Blind presisjon.** **100 tilfeldige** av leserens treff (alle, om det er færre), `random.Random(734248)
.sample` over treffene sortert på id, til **en separat CC-instans** med regelfilen og sperreliste, i samme form
som presisjonsporten i ADDENDUM-23 §4 (oppdraget ordrett i `oppdrag-gjenvunnet/oppdrag-presisjon-100-ADDENDUM-23.md`).
Presisjon = andel instansen kaller `ekte_treff: true`, med Wilson 95 %.
**≥ 0,70 → lista heter «arbeidsliste (prospektiv port)». Under → «kandidatliste».** Navnet endres ikke i ettertid.

**(2) Recall — rapporteres uten terskel.** For hvert referansetreff i nøkkelen:
* **beholdt av silen** = en tekstbit i unionen (`5-union.jsonl`) fra samme verk dekker **alle** setningsnumrene
  treffet består av;
* **bekreftet av leseren** = minst én slik tekstbit fikk `treff: true` av leseren.

Rapporteres: andel beholdt og andel bekreftet av alle referansetreff, med Wilson 95 %, og andel bekreftet blant de
beholdte. **Dette er det første målte recall-tallet for silen.** Som følsomhet, merket slik: de samme to andelene
uten referansetreff merket `tvil`, og uten treff med `gyldig_spenn: false`.

**Hva recall her er og ikke er.** Referanseleseren er samme modellfamilie og samme regelfil som kjedens leser.
«Bekreftet» måler derfor enighet mellom to lesninger av samme type, ikke mot et menneske. «Beholdt» er det
renere tallet: det avhenger bare av om silen slapp passasjen gjennom.

## 6 Kostnad, målt

OpenAlex: `x-ratelimit-remaining` før og etter trekkingen, og antall kall (`MetaFetcher.calls`). Lokal tid per
ledd fra kjedens tilstandsfil. Max-økter: antall `claude -p`-økter og `usage` fra hver (referansesett, leser,
presisjonsport). **Pris per bekreftet treff** = hver av de tre, delt på antall treff presisjonsporten bekreftet,
skalert til hele lista (leserens treff × presisjon).

## 7 Rapporteres i tillegg

Klassefordeling blant leserens treff; H7-andel; løftbar andel og uavklart andel hver for seg (ADDENDUM-05 §4);
og **felt-tetthet mot de 100 første**: treff per verk og treff per 1 000 tekstbiter, mot arkeologi i ADDENDUM-22
§10 (274 treff, 25 verk) og mot alle 100.

## 8 Dødsbetingelser

* **Referansenøkkelen er fasit og røres ikke** etter at raden står i manifestet — uansett hva silen eller leseren
  viser. En referanseinstans som avbrytes, gjenopptas fra første ulest setning i en **ny** instans med samme
  oppdrag; ferdige verk leses ikke om.
* **Ingen leserøkt kjøres om.** Blir en økt avbrutt av leverandørens grense, fullføres de udømte tekstbitene
  serielt, som i ADDENDUM-22 §10. Aldri parallelle instanser (LAERDOM §32).
* **Regelfilen rettes ikke.** Portene flyttes ikke.
* **OpenAlex-gulvet står:** trekkingen stopper hvis `remaining` < 50 (`draw.REMAINING_FLOOR`), og fortsettes neste
  kvotedøgn fra samme posisjon.
* **Ingen publisering, ingen push, ingen MASTER-redigering.**

## 9 Filer låst med dette addendumet

Regnet på filene slik de står i commit `7972867`, commiten før låsen.

| fil | sha256 |
|---|---|
| `src/gjenopptak/harvest/draw_fase3.py` | `6f5b3c8613852e5eb644e41acbbbb7aa3ed3824579cd0fa80d256b81f75139dc` |
| `src/gjenopptak/harvest/draw.py` | `b36fdcf059df5bd1b126e8457ea9183ed69be8ec0fb4510ffab43b97eb95d0fa` |
| `src/gjenopptak/classify/fase3.py` | `28cd7717f7a1161c419964e4a2c411df844e4f3e1819ac4d992c18f6d3d65e59` |
| `src/gjenopptak/kjede/ledd.py` | `07fc3a77f5bdef3b91fa7b5ce444b01219e04e60b46a15af39264598d4906db8` |
| `src/gjenopptak/kjede/cli.py` | `c2eb33bc361557371a2ed86d6d3530fcd090865ca9cdc0e9fe8ae6a108731e0b` |
| `src/gjenopptak/kjede/leser.py` | `957310f746b7a9a0f8effc561fa592f2d2b2d744c2c7aa8ad5f9e300d9113a6d` |
| `kjede.toml` | `65620200fb2a3ca7bc45273cd12e408cd5b42285d1d1415af0a3a3d15cea77db` |
| regelfil `koder2/koderegler-gjenvunnet.md` | `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449` |
| ramme `frames/frame-arkeologi-RAW.jsonl` | `1050450fc774e56affc21c99e0ffc3c59682ff391c1e46163c69a50d5cdf241a` |
