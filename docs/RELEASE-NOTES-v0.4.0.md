# Release notes — v0.4.0 (utkast, ikke publisert)

**Status 01.10.2026:** bygget på nytt med manus v2.8 og MASTER v0.4; publiseres 01.10.2026. Portstatus:
`docs/UTGIVELSE-v0.4.0-PORTSTATUS.md`. *(Sto 29.09.2026: «forberedt, ikke publisert».)*

**MASTER:** v0.4.0 svarer til **MASTER v0.4** (01.10.2026, `MASTER_GJENOPPTAK_v0_4_2026-10-01.md` på volumet,
sha256 `de770544fb4f7928…`), med utgivelsescommit og tag `v0.4` på `offentlig`. MASTER selv deponeres ikke.

## Navnepolicy

**Revisjon 28.–29. september 2026 under navnepolicyen «verk, ikke person».** Evaluerende setninger i dokumentene
er adressert til verket, ikke til forfatteren; navn står bare i sitering og nøytral omtale (commits `0b4c979`,
28.09, og navnekontrollen 29.09, `docs/NAVNEKONTROLL-2026-09-29.md`). Låste filer — protokollen, addendaene og
kriteriefilene — er ikke endret og bærer fire slike setninger. Historikken i git-bundlen er ikke skrevet om:
den bærer de opprinnelige formuleringene, talt maskinelt til 11 evaluerende tillegg i 7 commits på `main`.

## Hva som ikke er med — ekskluderingsliste versjon 1 (29.09.2026)

Byggeren (`src/gjenopptak/utgivelse.py`, `UTELATT`) holder disse sporede filene utenfor depositumet, etter eierens
avgjørelse. De finnes i git-historikken i bundlen.

| mønster | hvorfor |
|---|---|
| `docs/INSTRUKSER-*.md` | arbeidsinstrukser til språkmodellinstansene, ikke studiens dokumentasjon |
| `docs/patch/**` | patcher til den interne MASTER-fila |
| `ROADMAP.md`, `docs/ROADMAP.md` | intern planlegging |
| `docs/BYGGEPLAN.md` | intern planlegging |
| `docs/MANUSKRIPT-v2*-UTKAST.md`, **unntatt den nyeste** | bare siste manuskriptutkast deponeres |

## Tre grupper i zip — Zenodos tak på 100 filer

Zenodo tillater høyst **100 filer per post**. Tre grupper som alle er nye i v0.4.0, deponeres derfor som zip, med
innholdet byte-identisk og sha256 per fil ført i byggmanifestet (`zipinnhold`):

| zip | innhold |
|---|---|
| `saker.zip` | `docs/saker/**` — sakregisteret og de sju sakfilene, med katalogstrukturen `saker/SAK-…/…` bevart |
| `faktasjekk-manuskript.zip` | de sju faktasjekkrapportene for manuskriptutkastene |
| `oppdrag.zip` | de seks leseroppdragene med sperreliste, ordrett slik de ble lest |

Filer som alt var deponert i v0.3.0, er ikke flyttet inn i zip.

## Historikkbundlen

`gjenopptak-git-history.bundle` er `git bundle --all` (eierens avgjørelse 29.09.2026). Den bærer hele
arbeidshistorikken, også formuleringer som senere er revidert under navnepolicyen, og det ordrette sitatet av en
fotnote i Heron-notatet (§ 11) som i filene er erstattet med parafrase 29.09.2026.

## Fase 3 (ADDENDUM-25) — utfallet er med

**Port (1) bestått:** blind presisjon 85 av 100 [76,7–90,7] mot terskel 0,70 på 100 nye arkeologiverk, med
porter, regelfil og kjede låst før trekkingen. Lista fra denne kjøringen heter **«arbeidsliste (prospektiv
port)»** — den eneste i prosjektet som bærer det navnet. Kandidatlista fra de første 100 verkene er uendret
kandidatliste. **Port (2), første målte recall:** silen beholdt 95 av 104 referansetreff (91,3 % [84,4–95,4]),
leseren bekreftet 85 av 104 (81,7 % [73,2–88,0]), mot en LLM-referanselesning av 20 verk. Treffene er klynget (51
av de 104 i ett verk), så intervallene er for smale; uten det verket er tallene 84,9 % og 71,7 % (RESULTAT § 1.2). Tall og avvik:
`docs/RESULTAT-ADDENDUM-25.md`; hvert tall med sti og sha: `docs/MANUSKRIPT-FAKTA-2026-09-28.md` § 9.

**Én endring i et ledd etter låsen:** registerleddet (`kjede/ledd.py`, sha `07fc3a77…` → `39f8b9de…`) skrev et
hode som brøt sitt eget skjema. Det er rettet, radene er uendret, og hodet bærer nå også merknaden om at
verksnivåets tellinger er silens, ikke leserens (`docs/UTGANG.md`). `silrecall` står som «ikke målt» i hodet,
fordi skjemaet bare tillater den verdien. Referanseporten i `kjede/cli.py`
(28.09, RESULTAT-ADDENDUM-25 § 0.3) er også en endring etter låsen, men rører ikke noe ledd.

**Nye filer for fase 3:** `fase3-maaling.json`, `fase3-rapport.json`, `fase3-register.jsonl` med hode,
`fase3-referanse-nokkel.jsonl`, presisjonsportens oppdrag, nøkkel og verdikter, `fase3-modell-fra-utskrifter.json`,
`fase3-leser-verdikter.zip` og 15 nye blindfiler i `blindfiler-indeks.zip`. Ingen tekstbiter.

## Nøklene

**Nøkkelregelen (30.09.2026):** en nøkkel holdes utenfor depositumet til målingen den blinder er ferdig og
rapportert, og deponeres deretter. v0.4.0 bærer derfor nøklene til leserøktene og presisjonsporten for de første
100 verkene (ADDENDUM-22/23) og for fase 3 (ADDENDUM-25), og fase 3s referansenøkkel. **Nøkkelen til de 320
(port-presisjonssettet) holdes ute:** ADDENDUM-21 (koder 3) er preregistrert og ikke kjørt på samme blindfil.
Tabellen står i portstatusen, § 6.

## Koder 2-sammenligningen uten passasjetekst

`koder2-sammenlikning.json` deponeres som **`koder2-sammenlikning-uten-tekst.json`**: feltet `passasje` i de 16
største uenighetene (ordrette utdrag på inntil 400 tegn fra verkene) er erstattet av `passasje_sha256` og
`passasje_tegn`, etter avgjørelsen om ingen passasjetekst i depositumet (portstatus § 7). Alle andre felt, også
`hovedtall` som dokumentene viser til, er uendret. Originalen ligger på volumet med sha256 i manifestet. Den er
publisert uendret i v0.2.0, v0.2.1 og v0.3.0; de postene kan ikke bytte fil og står.

## Erstattet (superseded)

**`MANUSKRIPT-v0.1.md` er erstattet av `MANUSKRIPT-v2.8-UTKAST.md`.** v0.1 er utkastet som ble deponert i
v0.1.0–v0.3.0; det følger med i v0.4.0 fordi det er deponert før og skal kunne sammenlignes, men tallene og
slutningene i det er ikke gjeldende. Gjeldende tall står i `MANUSKRIPT-FAKTA-2026-09-28.md`, og siste utkast er
v2.8: v2.7 kontrollert i sju faktasjekkrunder (`FAKTASJEKK-MANUSKRIPT-*.md`), og v2.8 legger bare til
klyngefølsomheten i § 4.7 og forbehold 7. Kjent rest står i `FAKTASJEKK-MANUSKRIPT-v2.7-2026-09-30.md`.

