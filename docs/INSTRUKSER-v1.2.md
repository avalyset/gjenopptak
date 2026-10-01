# INSTRUKSER — Gjenopptak-sporet

**Versjon:** 1.2
**Sist oppdatert:** 28.09.2026

## Hva som endret seg i v1.2

**Kanon-linjen er rettet.** v1.1 pekte MASTER til et annet sted enn der den ligger. Den ligger på
**Vault**, ikke i repoet og ikke i `~/Desktop/Master Dok.` som de andre sporene:

```
/Volumes/Vault/gjenopptak-kilder/master/arkiv/
```

`POINTER.txt` i den mappen navngir gjeldende fil. **POINTER er kanon, ikke filnavnet du husker.**
Per 28.09.2026: `MASTER_GJENOPPTAK_v0_3_2026-09-28.md`.

**Hygienelisten fra MASTER § 9 er påført her** (se nederst). Fire poster sto som åpne poster i MASTER,
men er filarbeid uten måling. De hører i en instruksfil, ikke i et strategidokument.

> **Ærlig om utgangspunktet:** v1.1 finnes ikke på disk. Søkt i `~/dev/gjenopptak`, på Vault og i
> `~/Desktop` — ingen fil. v1.1 er instruksfila i Claude-prosjektet, som ikke er versjonert her. v1.2
> er derfor **skrevet på nytt** med den rettede kanon-linjen, ikke diffet mot v1.1. Det står her i
> stedet for å late som om en diff er gjort.

---

## 1 Hvor ting ligger

| hva | hvor | merk |
|---|---|---|
| **MASTER** | `/Volumes/Vault/gjenopptak-kilder/master/arkiv/`, navngitt av `POINTER.txt` | **committes aldri til git** |
| versjonsbump | `~/bin/bump-master.sh bump gjenopptak --minor` | leser versjonen fra headeren, aldri fra kalleren; gjør alle tre stegene i én operasjon og selvverifiserer |
| repo | `~/dev/gjenopptak`, offentlig på `https://github.com/avalyset/gjenopptak` | offentlig gren = rotcommit `5fcb353` + én utgivelsescommit per MASTER-versjon (`967254a` = v0.3); `main` pushes aldri (ADR-0012, datert tillegg); full historikk ligger i Zenodo-bundlene |
| materiale | `/Volumes/Vault/gjenopptak-kilder/` | 25 GB, 20 000+ filer; **`data/` er gitignorert** (ADR-0001) |
| manifest | `Vault: MANIFEST-VAULT.md` | sti, bytes, sha256, tidspunkt og opphav per sikret fil; **3 010 rader** per 28.09 |
| kanon-bundler | `Vault: repo/kanon/` | `git bundle --all` per låsecommit; antallet står i katalogen (41 per 28.09.2026) |
| Zenodo | konsept-DOI `10.5281/zenodo.22959326` | **siter konsept-DOI-en**, ikke en versjons-DOI |
| patcher til MASTER | `docs/patch/` | skrives som fil, påføres ved bump — aldri rett inn i MASTER mellom bumper |

**Sjekk alltid POINTER på disk.** Prosjektfiler og chat er speil som er ukers gamle.

## 2 Faste betingelser

Disse gjelder uten at de gjentas i hvert oppdrag.

**Hemmeligheter.** Aldri `cat`/`print`/`echo`/`grep` på innholdet i credential-filer — bare `len()`,
`wc -c` eller `startswith()`. En nøkkel verifiseres med lengde og prefiks, aldri skrives ut. `401`
eller `403` betyr at nøkkelen er død eller uten kreditt: **stopp, rapporter, ikke prøv en annen nøkkel.**
Lag ikke nøkler, og bruk aldri én tjenestes nøkkel som erstatning for en annens.

**Ingen Anthropics API i verktøyet.** Fjernet, ikke slått av (ADR-0012, datert tillegg). En
`kjede.toml` som inneholder `[api]`, avvises av `konfig.last()`. Kvoteporten nekter enhver fase med
`api_kall`. Leseren er **bare** underinstans eller `claude`-CLI på Max-abonnementet. Skal en ekstern
modell noen gang inn, er den **Gemini** — og det krever en ny datert beslutning.

**Ingen e-post til noen.** Ikke til forfattere, ikke til redaksjoner, ikke til arkiv. Gjelder også når
det er den åpenbare veien videre; det er eierens valg.

**Låste filer røres ikke.** `PREREG-v1.md`, `ADDENDUM-*.md`, register v1, fasiten, og
`docs/saker/SAK-*/KRITERIUM.md`. Rettelser bor i **daterte korrigenda i egne filer**, med peker fra
README. En låst fil som er feil, forblir feil og får et korrigendum ved siden av.

**Git.** Eksplisitte stier, aldri `-A` og aldri `.`. **Ingen push før «go».** Låsecommiter utløser
kanon-bundle automatisk via `TRIGGER_PATTERN`.

**Ingen parallelle Opus-instanser.** Sju samtidige ga leverandørens øktgrense ved 87 % dekning og
tapte fem av åtte økter (LAERDOM § 32). Underinstanser kjøres serielt, med egen kladdekatalog.

**`require_vault()` ved start** av alt som leser materiale. **Ingen tall uten sti.**

**Nettbruk.** Ærlig User-Agent, ingen omgåelse av botporter. Et `403` føres som `403`, ikke som fravær.
Gjelder også underinstanser — prompten **må** si det, for de arver ikke normen (LAERDOM-post om
underagent-UA).

**OpenAlex.** Kreditter budsjetteres per oppdrag og telles i rapporten. `mailto` er valgfritt;
fellespoolen holder for titalls kall, og da sendes ingen adresse til tjenesten.

## 3 Arbeidsformen

1. **Kriteriet låses før beregning.** Egen fil, sha256 ført, låsecommit, kanon-bundle. Et kriterium som
   ikke kan kjøres, **låses ikke** — da ville revisjonssporet late som om saken ble prøvd.
2. **Kildens egne tall reproduseres først** (PS-246-mønsteret). Klarer du det ikke, **stopp saken og før
   hvorfor.** Å trekke egne data i stedet bytter ut kildens tall med dine.
3. **Terskler flyttes ikke.** 89 % mot en terskel på 90 % er ikke opphevet. Intervallet oppgis, men
   avgjørelsen følger det målte forholdet.
4. **Negativt utfall føres likt.** Et resultat uten terskel rapporteres også når N = 0.
5. **Post hoc merkes post hoc.** Funn kriteriet ikke ba om, er verdifulle og skal ikke gjemmes — men de
   er ikke porten.
6. **Hver måling føyer en seksjon til `docs/LAERDOM.md` i samme commit**, med Målt / Tall / Slutning /
   Gjort / Filer.
7. **Alt materiale til Vault med sha i manifestet**, i samme arbeidsøkt.
8. **Én rapport per fullført enhet**, ikke underveis.

## 4 Hygienelisten — poster som bare er filer

Flyttet hit fra MASTER § 9 den 28.09.2026. Ingen av dem er en måling; alle er filtilstand.

1. **OPPGAVEN-v2 finnes ikke på maskinen.** Søkt i repoet over alle refs, i `~/Desktop` og i
   `~/Documents`. B3-rettelsen kan derfor ikke føres der. **Tallene står i `docs/METODE.md` § 1, og det
   er kanon** til filen eventuelt dukker opp. Ingen handling kreves.
2. **«Én koder» i `PREREG-v1.md` § 4 og `ADDENDUM-06.md`**, innhentet av ADDENDUM-11. Begge filene er
   låst. Rettelsen bor i `docs/INNHENTET-2026-09-26-en-koder.md`, pekt til fra README. **Skal aldri
   redigeres inn i de låste filene.** Samme frase i ADDENDUM-06 § 1.6 er fortsatt sann, men gjelder bare
   recall-fasiten. Samme innhenting gjelder ADDENDUM-02 § 5 og ADDENDUM-08 (INNHENTET § 3, 28.09.2026); øvrige
   funn i låste filer fra frys-lesningen står i `docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md`.
3. **Forretningsadressen i `ADDENDUM-03.md` linje 197** — OpenAlex' polite-pool-konvensjon ført som
   `mailto=`-parameter i en måletabell. Låst fil. Skal den bort, hører det i et datert korrigendum, ikke
   i en redigering. Ingen hemmelighet; adressen er prosjektets kontaktpunkt.
4. ~~**`CITATION.cff` sier 0.3.0**~~ — **utført:** `CITATION.cff` er bumpet til 0.4.0 (28.09.2026) sammen
   med v0.4.0-utgivelsen. Regelen står for neste gang: bumpes sammen med Zenodo-versjonen, ikke før.

**Det som *ikke* er hygiene, og derfor står igjen i MASTER § 9:** eierens valg om den private e-posten i
de fire Zenodo-postene, de tre utløserne fra fase 2, ADDENDUM-21 arm A, og at ingen ekstern har lest
koden. Alle fire krever en beslutning eller en hendelse, ikke en filendring.

## 5 Der det har gått galt før

Kort liste, fordi den er kortere enn LAERDOM og fanger det som gjentar seg.

* **En oppslagstjeneste som svarer 200 med en annen passasje** gjør bom til treff. Les den oppløste
  adressen ut av svaret (LAERDOM § 35).
* **En skjemastramming som ikke valideres bakover** fanger bare framtidige rader (§ 36).
* **`sed` på en docstring** ødela `a19.py` og fikk en kø til å hoppe over et ledd. Bruk Python-redigering
  på Python-filer.
* **Ikke-ASCII variabelnavn** i zsh feiler. Bruk ASCII.
* **`mv` til iCloud-synkede mapper** gir 0-byte placeholders. Bruk `cp` og verifiser størrelsen.
* **En blokkert TCC-katalog ser ut som en tom katalog.** Aldri `2>/dev/null` på eksistenssøk.
* **`MASTER` speilet i en prosjektfil** er ukers gammelt. Les POINTER på disk.
