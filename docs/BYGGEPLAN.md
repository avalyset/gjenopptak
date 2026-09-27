# Gjenopptak — byggeplan

**27.09.2026, v4. Erstatter v3 (26.09).** Byggeplan, ikke avslutningsplan. Ingenting her venter
på en måling. Er ROADMAP.md fase 1; ROADMAP fase 2 (sakbehandling) går parallelt og bruker
registeret fra B1 — den venter ikke på B5–B7.

**Endringer fra v3:** førsteleddet er avgjort (B4) — silen er dommer ∪ ekstraksjon, embeddings
er død · detektoren er ikke den lokale dommeren men en agentisk Opus-leser (B1) · kvoteporten
dekker Opus-økter og API-kreditt, ikke bare OpenAlex (B1) · utgangen bærer tvil-felt og
fasitens stabile kjerne (B3) · depositumet bærer alt en låst måling leste (B5).

---

## Målet, konkret

```
gjenopptak kjør --felt energimodellering --ar 2015-2020 --n 25
```

gir en fil med kandidater. Hver rad: verk, passasje, hindringsklasse, **tvil**, løftbarhet med
dato, materialtilgang, falsifiseringsstatus — og feilratene som gjelder for akkurat den raden.

Det finnes ikke i dag. I dag er det ni moduler kjørt for hånd med håndskrevne prompter mellom,
og leseren startes manuelt som CC-økt.

---

## B1 — Én kommando

Kjeden som én kjørbar: L0 ramme → L1 henting → L2 tekstbiter → **L3 sil** (dommer gemma2:9b ∪
ekstraksjon per dokument) → **L4 leser** (agentisk Opus-instans, regelfil `234695dd…`,
sperreliste, serielle økter ≤ 356) → verksnivå → L5 falsifisering mot siteringer → L6 register.
Verksnivået inn i kjeden, ikke som sideskript.

Krav som følger av det vi har lært, ikke av teori:

- **Gjenopptakbar.** Hver fase skriver tilstand; avbrudd koster tid, ikke arbeid. Leserøkter
  som faller på 429 gjenopptas der de stoppet.
- **Kvotebudsjett som port, ikke som advarsel.** Kommandoen nekter å starte en fase den ikke
  har kreditt eller kvote til å fullføre, og sier hvor mye den trenger: OpenAlex-kreditter,
  API-kreditt (stopp på «credit balance too low»), Opus-økter (målt 25 034 kontekst-tokens per
  passasje, 287 533 harness-tokens per økt à 356).
- **Serielt.** Aldri parallelle Opus-instanser — sju parallelle falt på øktgrensen ved 87 %.
  Egen kladdekatalog per instans.
- **Vault som standard**, `require_vault` ved start, ingen fallback (ADR-0009). `data/` er
  gitignorert (ADR-0001).
- **Signatur per dom** (ADR-0003), determinismesjekk før og etter batch (ADR-0008). For
  API-kall: `stop_reason` og `usage` logges per kall; `max_tokens` satt så det ikke kan binde;
  parametere modellen avviser føres per kall, ikke utelates stille.
- **Kanari før hver ollama-kjøring**: `num_ctx` eksplisitt, kanarisetning sist i et maksvindu.
- **Tørrkjøring** som rapporterer kostnad i kreditter, økter og timer før noe hentes.

**Leveranse:** kommandoen kjører på et felt fra ende til ende uten manuell inngripen; røyktest
på 3 av de 100 verkene gir register sha-identisk med register v2.

---

## B2 — Felt som konfigurasjon

Emne-ID-er, år og terskler er spredt i kode og addenda. Et felt skal være en fil:

```yaml
felt: energimodellering
topics: [T10424, T11185, T11941]
ar: [2015, 2020]
ramme: hentbar
```

Med den filen kan hvem som helst legge til et felt uten å røre kode.

**Leveranse:** de fire eksisterende feltene som konfigurasjonsfiler, og ett nytt felt lagt til
uten kodeendring.

---

## B3 — Utgangen bærer sin egen usikkerhet

Hver kandidatrad får med:

- silens presisjon for kandidatens klasse, med intervall (A∩B 34 %, A alene 14 %, B alene 7 %)
- **leserens tvil-flagg** — blind presisjon 98 % ved `tvil: false`, 76 % ved `tvil: true`
- verksnivåets vurdering og hva den ikke ser (H8 utenfor verket)
- falsifiseringens dekningsgrad for det verket
- løftbarhet med vurderingsdato og tabellversjon (ADR-0010)
- seksjonsetikettens opphav: kildens egen merking eller parserens gjetning (ADR-0007)
- **ikke-prosa-merking** (`ikkeprosa.py`, versjonert) — merket, aldri fjernet

Registerets header bærer hvilken port lista har passert («kandidatliste (post hoc port)» /
«ubekreftet») og de globale forbeholdene: fasitens stabile kjerne 3 av 27; N3-grensen bærer
koderidentitet (5,8–13,6 % mellom kodere).

**Leveranse:** utgangsformatet definert i skjema, med et eksempel en utenforstående kan lese.

---

## B4 — Førsteleddet er avgjort; grensesnittet er utskiftbart

Målt 26.–27.09: embeddings 84 % ved 2,0× (død), seksjon 1,09× (død), nærsøk 84 % ved 5,25×,
ekstraksjon per dokument 36 % recall (død som enhet). **Silen er dommer ∪ ekstraksjon**: 12,8 %
av korpuset, dekker alle 27 kjente, ~6 leser-passasjer per bekreftet treff.

Silen implementeres bak ett grensesnitt (`sil(tekstbiter) -> kandidater`) med denne som eneste
implementasjon. En bedre sil settes inn senere uten å røre resten — men bare preregistrert, og
ikke i denne byggeplanen.

**Leveranse:** silen som plugg-inn, med målt recall og kostnad i konfigurasjonen.

---

## B5 — Offentlig repo

Verktøyet er lokalt uten remote. Ingen kan bruke det.

- GitHub, offentlig, Apache-2.0 på kode og CC BY 4.0 på data
- scrub over alle refs før push (E2), eksponeringssjekk utenfor git (G3)
- `CITATION.cff` med konsept-DOI
- releases som peker på Zenodo-versjonen
- depositumet bærer **alt en låst måling leste**: regelfil, blindfiler, sperrelister, leseroppdrag

**Leveranse:** repoet er offentlig og klonbart.

---

## B6 — Dokumentasjon som gjør det brukbart

- **README:** installer, kjør på ditt felt, les utgangen. Konkret, med faktiske kommandoer.
- **METODE.md:** rammen, enheten, typologien med ankersetninger, silen, leseren med regelfil og
  øktform, fasit og κ med stabil kjerne, korrigering for presisjon, falsifisering,
  reproduksjonssteg, kjente grenser. Stoppvilkår: en utenforstående kjører porten på et nytt
  felt fra dokumentet alene.
- **Feltguide:** hvordan legge til et felt, hva som kan gå galt, hva tallene betyr for feltet.

**Leveranse:** noen utenfor prosjektet kjører verktøyet uten å spørre oss.

---

## B7 — Installerbar

`pip install` fra repoet eller PyPI, pinnede avhengigheter, testpakke som kjører hos brukeren.
Ollama-modellen lastes ved første kjøring, vekt-sha256 verifisert. Leseren krever Claude Code
med Opus; kommandoen sier det ved start og avslutter rent uten.

**Leveranse:** installasjon på en ren maskin gir en kjørbar kommando.

---

## Rekkefølge

B1 og B2 først. B3 og B4 parallelt. B5, B6, B7 til slutt, i den rekkefølgen. ADR før B1-koden
(kjeden, leservalget, silen), nummer mot alle refs.

Ingen av dem venter på en måling.

## Biproduktene

Manuskript v2, Zenodo v0.4.0 og preprint-oppfølging skrives når verktøyet er bygget **og**
ROADMAP fase 2 har gitt saksmapper. De er resultater av arbeidet, ikke faser i det.
