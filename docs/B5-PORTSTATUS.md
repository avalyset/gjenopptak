# B5 — portstatus før push. Ingen push er gjort.

**Skrevet:** 2026-09-27. **Status: STOPPET FØR PUSH.** Push er irreversibel og autoriseres av eieren
på grønne porter. Denne filen er portstatusen, ikke en anbefaling om å pushe.

## Portene

| port | status | grunnlag |
|---|---|---|
| Apache-2.0 på kode | **grønn** | `LICENSE`, 12 155 B, Apache License 2.0 |
| CC BY 4.0 på data | **grønn** | `LICENSE-DATA`, 1 511 B; delingen står i README «Licensing» |
| `CITATION.cff` med konsept-DOI | **grønn** | konsept-DOI `10.5281/zenodo.22959326`, tre DOI-er i `identifiers` |
| scrub: nøkler og tokens over alle refs | **grønn** | 686 objekter, 139 commits, én ref: **null treff** på Anthropic-, Google-, OpenAI-, GitHub-, AWS-nøkler, PEM-privatnøkler, Bearer-tokens og «sealed» |
| scrub: e-post over alle refs | **RØD** | se under |
| G3: hvor materialet finnes utenfor git | **grønn** | se under |
| argumentet mot push | **skrevet** | se under |

## Den røde porten: privat e-post i historikken

Scrubben gikk over **alle blober på alle refs**, ikke bare HEAD, og fant:

* **`ADDENDUM-03.md:197` i HEAD** — en **forretningsadresse** (`…@ecodeco.no`) ført som
  `mailto=`-query-parameter i en måletabell. Det er OpenAlex' egen polite-pool-konvensjon, og
  adressen er prosjektets kontaktpunkt. **Filen er låst**, så den kan ikke redigeres — bare
  korrigeres i et datert korrigendum.
* **`src/gjenopptak/harvest/recallset2.py` i tre historiske revisjoner** (`3dc08ad`, `82df4e0`,
  `9459884`) — en **privat** adresse (`…@gmail.com`), hardkodet før den ble parameterisert.
  **HEAD har 0 treff:** koden leser den nå fra `OPENALEX_MAILTO` i miljøet.

**En push av denne historikken publiserer den private adressen.** Det er ikke et stort tap i seg
selv, men det er irreversibelt, og det er ikke min avgjørelse.

**Tre veier, med hva hver koster:**

1. **Skriv om historikken** (`git filter-repo`). Fjerner adressen, men **endrer hver commit-sha**.
   Det bryter alt som er festet til dem: de 35 kanon-bundlene, hver `sha256` i
   `MANIFEST-VAULT.md`, og påstanden i addendaene om at hver låsecommit bar nøyaktig én fil.
   **Revisjonssporet er hele poenget med de bundlene.** Denne veien anbefales ikke.
2. **Publiser med historikken.** Ett øyeblikks arbeid, og den private adressen ligger ute for godt.
3. **Publiser fra én ny rotcommit** av HEAD, og la den fulle historikken bli liggende privat på
   Vault, der den alt er sikret i 35 bundler med sha256 i manifestet. Koden og dokumentene blir
   offentlige og verifiserbare; revisjonssporet blir like intakt som i dag, bare ikke offentlig.
   **Dette er den veien som taper minst.** Prisen er at en utenforstående ikke kan se
   commit-for-commit-historikken — men den kan heller ikke i dag, siden repoet ikke har remote.

## G3 — hvor materialet finnes utenfor git

`data/` er gitignorert (ADR-0001), og alt tungt ligger på Vault med sha256 i manifestet. Det som
**ville blitt publisert**, er 150 filer: `src/`, `tests/`, `docs/`, `felt/`, de 23 addendaene,
`PREREG-v1.md`, `README.md`, `kjede.toml` og lisensene.

| hvor | omfang | hva |
|---|---|---|
| `/Volumes/Vault/gjenopptak-kilder/` | **25 GB, 20 186 filer** | rådata, rammer, fulltekster, dommer- og ekstraksjonslogger, blindfiler, nøkler til blindingen, verdikter, registre |
| `MANIFEST-VAULT.md` | 545 562 B, **2 843 rader** | sti, bytes, sha256, tidspunkt og opphav for hver sikrede fil |
| `repo/kanon/` på Vault | **35 bundler** | `git bundle --all` per låsecommit, med sha256 |
| `master/arkiv/` på Vault | v0.1 + v0.2 + POINTER | MASTER, som aldri committes til git |
| Zenodo | **8 DOI-referanser** i `docs/ZENODO.md` | konsept-DOI + versjons-DOI-er |
| lokal `data/` | 87 MB, 138 filer | regenererbar, eller kopi av Vault |

**Ingenting av dette forsvinner ved en push, og ingenting av det blir offentlig av en push.** Det er
poenget med skillet: koden og protokollen er offentlige, materialet er sikret og sitert.

## Argumentet MOT push

Skrevet fordi en port som bare ser etter grunner til å slippe gjennom, ikke er en port.

1. **Den private e-posten i historikken er irreversibel når den er ute.** Ingen av de tre veiene over
   er gratis: én ødelegger revisjonssporet, én publiserer adressen, én gir opp offentlig historikk.
2. **Porten som skulle bære verktøyet, falt.** ADDENDUM-22s prospektive port ga 21 av 27 mot terskel
   22. Det som publiseres, er derfor et verktøy med en **kandidatliste**, ikke en arbeidsliste, og et
   κ på 0,812 hvis stabile kjerne er **tre av 27**. En utenforstående som finner repoet, kan lese
   tallene som mer avgjort enn de er — særlig om README leses uten `docs/UTGANG.md`.
3. **Leseren krever et Max-abonnement.** Verktøyet er «åpent» i lisens, men ikke i praksis: uten
   Claude Code med Opus er silen alt man får, og silen er 14 % presis. Det kan skuffe noen som
   klonet det i god tro, og det står i README — men det står ikke i en overskrift.
4. **Ingen ekstern har lest koden.** 139 commits, én forfatter, ingen review. Feilene som er funnet i
   denne planen alene — fem i kanarien, én i malsubstitusjonen, én i `sed`-en — ble funnet ved å
   kjøre, ikke ved å lese. Det er sannsynlig at flere står.
5. **CITATION.cff sier 0.3.0.** Kjeden, ADR-0012, B1–B4 og registerformatet er nyere enn den
   versjonen. En push uten bump siterer feil tilstand.
6. **Push er ikke reversibel i praksis.** Et slettet GitHub-repo er indeksert, klonet og speilet i
   mellomtiden.

**Motargumentet, kort:** ingenting av dette er hemmelig, tallene er ført med sine forbehold, og et
verktøy ingen kan hente er ikke et verktøy. Men avveiningen er eierens.

## Hva et «go» vil autorisere

Ingenting skjer før eieren sier «go», og da bare dette:

1. Valgt vei for e-posten i historikken (1, 2 eller 3 over) — **må velges først**.
2. `gh repo create avalyset/gjenopptak --public`, push av `main`.
3. `CITATION.cff` bumpet, og en release som peker på Zenodo-versjonen.

Uten et valg i punkt 1 gjøres ingenting.
