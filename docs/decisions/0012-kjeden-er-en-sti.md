# ADR-0012 — kjeden er én sti, og leseren er en agentisk instans

**Dato:** 2026-09-27. **Status:** vedtatt. **Gjelder:** `gjenopptak run` og alt som produserer et register.

**Numrene 0005 og 0006 har aldri vært i bruk.** De finnes ikke på noen ref i dette repoet og er ikke
nevnt i noen fil; hullet er ikke en manglende beslutning.

## Vedtaket

**Kjeden var ramme → henting → tekstbiter → sil (dommer ∪ ekstraksjon) → leser → register. Leseren var en
agentisk Opus-instans med regelfil `234695dd4e1777a9…` og sperreliste; ett-kall-modeller var
sil-klasse.**

I byggeplanens leddnavn (`docs/BYGGEPLAN.md` B1): **L0 ramme → L1 henting → L2 tekstbiter → L3 sil →
L4 leser → verksnivå → L5 falsifisering → L6 register.** Denne beslutningen fester tre av dem: kjeden
som sti (L0–L6), leservalget (L4) og silen (L3).

Det er formulert i fortid fordi det ikke er en plan. Hvert ledd er kjørt, målt og dokumentert, og
beslutningen fester hva målingene viste at kjeden *er* — ikke hva den burde være.

## Hva hvert ledd ble målt til

Alle tall er hentet fra `docs/METODE.md` med de seksjonene som er oppgitt der, og gjelder de samme 100
verkene.

| ledd | hva det gjorde | målt |
|---|---|---|
| **ramme + henting** | åpen fulltekst, JATS før PDF | 100 verk, `data/port/spesifikasjon.json` |
| **tekstbiter** | setning ± 2, stride 3, dekker hver setning | **22 243 tekstbiter** (METODE §1) |
| **sil A — dommer** | `gemma2:9b`, temp 0, frø 734248 | flagget **2 173** av 22 243 (METODE §1) |
| **sil B — ekstraksjon** | prompt `c8c276df…` (ADDENDUM-16, sha `20e777e4…`), num_ctx 8192 | 884 Q-linjer → 1 030 tekstbiter |
| **A ∪ B** | unionen, ikke-prosa merket og beholdt | **2 844**, dekker alle 27 kjente treff |
| **leser** | agentisk Opus-instans, regelfil + sperreliste | κ = **0,812** mot koder 1 (ADDENDUM-11) |
| **register** | claims-2, én rad per bekreftet treff | `register/claims.jsonl` |

**Grunnraten som leddene skal bære** (METODE §1, tre regnemåter på samme materiale): **ett treff per 890**
tekstbiter måler utvalget og skal ikke brukes som prevalens; **ett per 61** er et gulv som bare teller
sanne blant de flaggede; **ett per 29** er beste anslag med de tapte inkludert.

## Hvorfor silen er en union, ikke ett ledd

Dommeren alene og ekstraksjonen alene mistet hver sine treff. Snittet av dem er det presiseste enkeltleddet
— presisjon **31,4 % [20,3–45,0]** ved **94,1 % bevaring** av de sanne (METODE §5) — men **unionen** er den
eneste silen som fanget **alle 27 kjente treff**. Kjeden bruker derfor unionen som inndata til leseren, og
snittet som sorteringsnøkkel, ikke som filter.

**Ikke-prosa merkes og fjernes aldri.** Regelen ligger i `src/gjenopptak/classify/ikkeprosa.py`
(sha256 `63ed734555a8bc95…`). 18,1 % av det dømte materialet er ikke prosa, men bare 2,5 % av treffene —
merkingen holder søppelet ute av treffmassen uten å endre nevneren.

## Hvorfor leseren er agentisk, og ett-kall-modeller er sil-klasse

Målt med **samme regelfil og samme kallstruktur**, ett kall per passasje, mot koder 1:

| leser | κ | klasse |
|---|---|---|
| Haiku 4.5 | 0,031 [−0,024–0,129] | **sil** |
| Sonnet 5 | 0,294 [0,126–0,455] | **sil** |
| Opus 5, ett kall per passasje | 0,636 [0,478–0,768] | grensetilfelle |
| Opus 5, **agentisk, én sammenhengende økt** | **0,812** [0,712–0,917] | **leser** |

Rekken er monoton, og Haiku/Opus-spennene overlapper ikke. Ett-kall-modeller under Opus er derfor
**sil-klasse**: de kan redusere en mengde, men ikke avgjøre et register. Mellom per-kall-Opus og agentisk
Opus overlapper intervallene i 0,712–0,768, så øktformens bidrag er **mulig og umålt** — kjeden bruker den
agentiske formen fordi den er den eneste som er målt over 0,70, ikke fordi forskjellen er bevist.

**Leseren får aldri mer enn to filer:** regelfilen og sin egen blindfil med `id` og `tekst`. Sperrelisten
navngir de forbudte filene i oppdraget, slik ADDENDUM-11 §2 gjorde, og genereres av kjeden.

## Konsekvenser

* **Et register kan bare komme fra leser-leddet.** Et tall fra en sil er en kandidatmengde, og lista skal
  hete kandidatliste til en port er bestått.
* **Hvert ledd kan kjøres alene og gjenopptas.** `--from`/`--to` er en del av kjeden, ikke en bekvemmelighet:
  et ledd som ikke kan kjøres om uten å kjøre de forrige om, kan ikke etterprøves.
* **Alt som avgjør et tall, låses med tallet.** Regelfil, ledetekst, blindfil, sperreliste og
  modellsignatur får sha i manifestet i samme steg som utdataet (LAERDOM §30, §31).
* **Ingen hardkodede stier.** Modell, frø, `num_ctx`, øktstørrelse og stier står i én konfigfil, slik at
  en kjøring kan gjentas på en annen maskin uten å redigere kode.

## Hva dette ikke avgjør

Kjeden sier ingenting om hvor terskelen for en port skal ligge. ADDENDUM-22s port på 22 av 27 falt med 21,
og ADDENDUM-23 §1 viste hvorfor: fasitens stabile kjerne er **tre av 27**. En port må settes mot
referansesettets målte stabilitet, ikke mot dets ytterkant — men det er en beslutning per studie, ikke en
egenskap ved kjeden.

## Datert tillegg 27.09.2026 — verktøyet kaller ikke Anthropics API

**Besluttet:** verktøyet gjør **ingen kall til Anthropics API**. Leseren er en Claude Code-instans på
Max-abonnementet, som underinstans (`--leser subagent`) eller hodeløst kall (`--leser cli`).
Kvoteporten **nekter** enhver fase som ville kalt API-et — det er ikke «mangler kreditt», det er «finnes
ikke som vei».

**Hva som er fjernet, ikke bare slått av:**

* `[api]`-seksjonen i `kjede.toml`. En konfigurasjon som prøver å legge den inn igjen, **avvises av
  `konfig.last()`** med melding, ikke først ved kallet.
* Nøkkellesing og kredittsjekk i `kvote.py`. Det finnes ingen nøkkelsti i verktøyet, så det finnes
  ingenting å lese ut ved uhell.
* Kredittlinjen i `gjenopptak kvote`, som nå sier at API-et ikke brukes.

**Hvorfor det er en beslutning og ikke en innstilling.** Målingene i ADDENDUM-18, -19 og -20 gikk over
API-et med en betalt nøkkel, og de viste at ett-kall-modeller er sil-klasse (κ 0,031 / 0,294 / 0,636 mot
0,812 for agentisk Opus). Verktøyet trenger derfor ikke API-et til leseren, og en API-sti som ikke
brukes er en sti som kan tas i bruk ved uhell — med en nøkkel i miljøet, en kostnad ingen har budsjettert,
og en kvotegrense kjeden ikke kan se. `falsify/citations.py` kaller EPMC og Crossref; det er ikke
Anthropic og står uendret.

**Hvis en ekstern modell noen gang skal inn, er den Gemini** (nøkkelen finnes i miljøet). Det er ikke i
denne byggeplanen, og det krever sin egen port og sin egen preregistrering. Ingen del av kjeden
forbereder det nå.
