# ADR-0011 — Enheten for søk er setningen, ekstrahert per dokumentvindu

**Status:** besluttet 2026-09-26, **forkastet 2026-09-28** (se tillegget nederst). **Gjelder:** L2-rørledningen.
**Erstatter ikke:** ADR-0002 (seksjonsbevaring), ADR-0003 (modellsignatur), ADR-0007
(seksjonsetikettens opphav). **Nummer:** kontrollert mot alle refs
(`git for-each-ref` + `git ls-tree -r --name-only` over `refs/heads` og `refs/tags`);
0005 og 0006 er brent under en tidligere konvensjon og gjenbrukes ikke.

## Beslutningen

**Enheten for søk er setningen, ekstrahert per dokumentvindu; enheten for klassifisering er den
ekstraherte setningen med ±2. Tekstbiten som søkeenhet ga 22 243 dommer for ~222 setninger per verk,
fem gjennomganger per setning. Ekstraksjon leser hver setning én gang.**

## Hvorfor beslutningen ble tatt

Fire siler er prøvd som førsteledd mot tekstbiten som enhet, og alle fire er forkastet:
markørlisten (ADDENDUM-06/07), embeddinger (ADDENDUM-14), seksjonsfordeling og nærsøk
(ADDENDUM-15). Ingen av dem holder 90 % av fasit-treffene for under to tredeler av materialet, og
for to av dem er taket strukturelt.

Kostnaden ligger i enheten, ikke i silen. Med steg 3 og vindu ±2 blir hver setning dømt om lag fem
ganger; 22 243 dommer dekker om lag 4 400 setninger per fire verk. En ekstraksjon som leser et vindu
og siterer de setningene som oppfyller kravet, leser hver setning én gang, og flytter arbeidet fra
«klassifiser alt» til «hent det som finnes».

## Påstander som kan falsifiseres

1. Ekstraksjon per dokumentvindu finner minst 21 av de 25 fasit-treffene etter matchdefinisjonen i
   ADDENDUM-16.
2. Samlet tid for ekstraksjon pluss dømming av de siterte linjene er lavere enn nærsøk-rutens samlede
   tid (ADDENDUM-15).
3. Blind presisjon på de siterte linjene er høyere enn dommerens øvre intervallgrense, 23,4 %.

## Dødsbetingelser, ordrett som låst før kjøring

> Utvalgstesen (steg 1): lever bare hvis treff per verk i den tetteste typen eller
> leveringsformen er ≥ 2 × den glisneste, med minst 5 verk i hver gruppe. Færre enn 5:
> «ikke avgjørbar», ikke «død».
> Seksjonsplassering: dødt for godt hvis alle merkede treff krever > 50 % av de merkede
> tekstbitene.
> Ekstraksjon (steg 2): død hvis ETT av disse inntreffer — recall < 21/25; samlet tid
> ikke under nærsøk-rutens samlede tid; blind presisjon ≤ 23,4 % (dommerens øvre
> intervallgrense). Ingen promptrevisjon i denne slyngen. En revidert prompt er en ny
> preregistrert test med eget addendum, og resultatet rapporteres ved siden av det
> første, ikke i stedet for.

## Rettelse 2026-09-26, før 2d ble målt: nevneren

**Utvalgstesens nevner var verk; den er rettet til tekstbiter før ekstraksjonsresultatet forelå.**
«Treff per verk» måler lengde så snart gruppene har ulik dokumentlengde, og det har de: de fem
avhandlingene har 1 301 tekstbiter hver mot artiklenes 169. Med verk som nevner var avhandlinger
tettest (1,200 fasit-treff/verk mot artikkel 0,208 = 5,77×); med tekstbiter som nevner er de
**glisnest** (0,923 per 1 000 mot preprintens 2,049 = 2,22×). Funnet står, men retningen snudde.

**Gjeldende kriterium er ≥ 2× på fasit-treff per 1 000 tekstbiter, minst 5 verk i hver gruppe.**
Tallene per verk beholdes i tabellen, merket «lengdeavhengig». Utfall etter rettingen:
OpenAlex-type 2,22× **lever**, felt 3,10× **lever**, leveringsform 1,55× **dør**.
Kilde: `ekstraksjon/2026-09-26/b2-nevner.json` på Vault.

Rettingen ble gjort før 2d fordi en nevner som måler lengde, ville gjort utvalgstesen til en
måling av dokumentlengde, og fordi rekkefølgen ellers ville vært å velge nevner etter å ha sett
hvilken som ga ønsket utfall.

## Tillegg 2026-09-27: to påstander i teksten over er falsifisert av egne målinger

Den opprinnelige teksten står uendret. Dette tillegget retter mekanismen og grunnlaget, ikke
beslutningen.

### C1 — «~222 setninger per verk, fem gjennomganger per setning» er feil

Regnet om fra fil (`data/port/spesifikasjon.json` → `sum_setninger`, `sum_passasjer`, `stride`,
`window`; `ekstraksjon/2026-09-26/b1-duplikatrate.json`):

| størrelse | verdi |
|---|---|
| setninger i alt | **66 833** |
| tekstbiter i alt | 22 243 |
| **setninger per verk** | **668** — ikke 222 |
| tekstbiter per verk | **222** — dette er tallet den opprinnelige teksten kalte «setninger per verk» |
| steg · vindu | 3 · ±2, altså 5 setninger per tekstbit |
| **gjennomganger per setning** | **1,67** — ikke 5 |

Med steg 3 og vindu 5 leses hver setning i gjennomsnitt 1,67 ganger, ikke fem. Femtallet var
vindusbredden, ikke redundansen.

**Følgen for begrunnelsen:** kostnadsgevinsten ved ekstraksjon kan ikke tilskrives at redundansen
fjernes — det er lite redundans å fjerne. **Gevinsten, om den finnes, ligger i færre kall og kortere
utdata:** 598 vinduer mot 22 243 dommer, og ett svar per vindu framfor ett per tekstbit.
**Beslutningen står; mekanismen var feil beskrevet.** *(Foreldet av tillegget 2026-09-28 nedenfor:
beslutningen står ikke.)*

### C2 — type-forholdet 2,22× hviler på to fasit-treff

Etter nevnerrettingen (seksjonen over) er tetteste type **preprint med 2,049 fasit-treff per 1 000
tekstbiter** — og telleren er **2 treff i 976 tekstbiter** (`ekstraksjon/2026-09-26/b2-nevner.json`).
Glisneste med minst fem verk er dissertation, 6 treff i 6 503.

Dødsbetingelsen krevde **minst 5 verk** i hver gruppe, ikke minst et antall treff. Den ble oppfylt
(7 og 5 verk), og **utfallet «lever» står som kriteriets utfall — merket «ikke handlingsgrunnlag —
2 treff».** Et forholdstall der telleren er 2, flytter seg med ett treff.

**Ingen ny terskel innføres nå.** En framtidig test på dokumenttype preregistreres med et **treffgulv**
i tillegg til verkgulvet, og det gulvet fastsettes før tallene ses.

Felt-forholdet 3,10× hviler på 13 treff mot 4 (arkeologi mot energimodellering) og er ikke berørt av
denne innvendingen.

## Konsekvenser

* Ekstraksjonsprompten lagres som fil med sha256, føres i ADDENDUM-16 og i hver utdatalinje, og
  endres ikke etter at addendumet er committet.
* `num_ctx` settes eksplisitt til minst 4096 i `options`, fordi ollama ellers trunkerer stille til
  2048. Vindu verifiseres med en kanarisetning før kjøring.
* Dommeren kjøres **uendret** på de siterte linjene, så den ene endringen som måles, er enheten.
* **Ingen ADR for ruting nå.** Ruting skrives når det finnes kode den styrer.

## Tillegg 2026-09-28: påstand 1 og 3 er falsifisert — beslutningen er forkastet

**Status: forkastet.** Ekstraksjon per dokumentvindu er målt og død etter ADR-ens egne
dødsbetingelser (`docs/METODE.md` § 5, ADDENDUM-16 § 6):

| påstand | målt | kilde | utfall |
|---|---|---|---|
| 1 recall ≥ 21/25 | **9 av 25 = 36,0 %** | `ekstraksjon/2026-09-26/2d-recall.json` | **falsifisert** |
| 2 samlet tid under nærsøk-ruten | 4,28 t | `2d-tid.json` | står |
| 3 blind presisjon > 23,4 % | **17 av 100 = 17,0 %** [10,9–25,5] | `2d-blind-presisjon.json` | **falsifisert** |

Én død betingelse var nok. Ekstraksjonen lever videre bare som det ene leddet i silen dommer ∪
ekstraksjon (ADR-0012), ikke som søkeenhet. Setningen «Beslutningen står» i C1 over sa det
uten å nevne utfallet; utfallet er ført her.
