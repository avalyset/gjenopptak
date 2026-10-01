# Lisensaudit — hva depositumet redistribuerer, og mot hvilken lisens

**28.09.2026, før v0.4.0.** Grunnlag: `best_oa_location.license` fra rammens OpenAlex-svar, ført per
verk i [`LISENS-PER-VERK.md`](LISENS-PER-VERK.md). **Dette er en kartlegging, ikke juridisk råd.**

## 1 Lisensbildet

**Populasjonen er de 60 verkene i register v2**, alle med minst én kandidatrad; de 14 verkene som siteres
ordrett i kandidatfila, er blant dem. Verk som siteres ordrett i andre filer uten å stå i registeret, er
**ikke** med i tallene under. Kjent er ett: `W3000588547` (Heron-avhandlingen, sitert ordrett i
`HERON-KOLLASJON-VURDERING-v2.md` § 11), lisens `—`, grønn OA, ført for seg i `LISENS-PER-VERK.md`. Om
det finnes flere, er ikke talt. *(Rettet 28.09.2026, frys-lesning 2: sto «60 verk har minst én kandidatrad
eller ett ordrett sitat i det publiserte treet».)*

| lisens | verk | hva den begrenser |
|---|---|---|
| `cc-by` | 22 | ingenting utover navngivelse |
| **`—` ingen oppgitt** | **17** | **ukjent** — se under |
| `cc-by-nc-nd` | 7 | ikke-kommersiell **og** ingen bearbeiding |
| `other-oa` | 4 | ukjent, tilgang uten lisensangivelse |
| `cc-by-sa` | 3 | del på samme vilkår |
| `cc-by-nc` | 3 | ikke-kommersiell |
| `cc-by-nc-sa` | 3 | ikke-kommersiell, del på samme vilkår |
| `public-domain` | 1 | ingenting |

**13 av 60 bærer NC- eller ND-vilkår. 17 av 60 har ingen oppgitt lisens** — og `—` betyr ikke fritt.
De 17 er gjennomgående **grønn og bronse OA**: forfatterversjoner i institusjonsarkiv, der
utgangspunktet er at alle rettigheter er forbeholdt med mindre noe annet står. Det tyngst siterte
verket, `W2551114598` med 28 sitatblokker, er **public domain**, og det er flaks, ikke design.

## 2 Hva depositumet faktisk redistribuerer

| artefakt | i depositumet? | tredjepartsinnhold | vurdering |
|---|---|---|---|
| PREREG, addenda, ADR-er, LAERDOM, METODE | ja | **korte ordrette sitater** i ankereksempler | sitatrett |
| `register/claims.jsonl` (v1) | ja | **ingen** — kontrollert: id, span, klasse, metadata, **ingen `tekst`** | ren |
| `MANIFEST-VAULT.md` | ja | **ingen** — sti, bytes, sha256 | ren |
| kildekode som tarball | ja | ingen | Apache-2.0, vår |
| git-bundle med hele historikken | ja | alt i treet, altså sitatene | som treet |
| **fulltekster** | **nei** — på volumet, bare sha256 i manifestet | — | **dette er det som holder auditen enkel** |
| **tekstbiter (22 243)** | **nei** — på volumet | — | se § 4 |
| dommer- og ekstraksjonslogger | nei — på volumet | inneholder passasjetekst | se § 4 |

**Det avgjørende:** depositumet inneholder **ingen fulltekst og ingen tekstbitsamling**. Eksponeringen
er begrenset til **korte ordrette sitater** i prosadokumentene.

**Sitatmengden i det publiserte treet:** den tyngste enkeltfilen er
`docs/SAKBEHANDLING-2026-09-27-kandidater.md`, med **50 ordrette sitater fra 14 verk**, ett ±2-setningers
sitat per kandidat (50 `**Sitat, ordrett**`-blokker; de andre 50 `>`-linjene er tittellinjer), talt per
verk i `docs/LISENS-PER-VERK.md`. Et samlet antall tredjepartssitater over alle filer er **ikke talt**.
*(Rettet 28.09.2026, frys-lesningen: her sto «422 sitatforekomster i 37 filer», med «120 blokksitater» i
`MASTER-PATCH-2026-09-26.md` og «69» i kandidatfila. Blokkene i MASTER-PATCH er sporets egen prosa, ikke
sitater; 69 stemmer med ingen telling av kandidatfila; og tellemetoden var ikke oppgitt. Tallet er
trukket, ikke erstattet.)*

**Kort ordrett sitat for kritikk og vitenskapelig drøfting hviler på sitatretten** (i Norge
åndsverkloven, tilsvarende andre steder), som gjelder **uavhengig av lisensen**. NC begrenser
kommersiell bruk og ND begrenser bearbeiding; ingen av dem opphever retten til å sitere. **Det
lisensen styrer, er redistribusjon av verket eller en vesentlig del av det** — og det er nettopp det
depositumet ikke gjør.

## 3 Hva som likevel må ryddes: datalisensen overrekker

`LICENSE-DATA` gir i dag **CC BY 4.0** på blant annet:

> «the frozen frame lists, samples, draw logs and judgment files held on the external volume»
> og «docs/**»

**Vi kan ikke gi CC BY på andres tekst.** Konkret overrekker den på tre punkter:

1. **`docs/**` inneholder korte ordrette sitater** — 50 fra 14 verk i kandidatfila alene; et samlet
   antall er ikke talt (§ 2) — fra verk der 13 av de 60 i registeret har NC/ND. Vi har sitatrett; vi har
   ikke rett til å viderelisensiere. *(Rettet 28.09.2026, frys-lesning 2: sto «422 ordrette sitater fra 60
   verk», et tall § 2 og `LICENSE-DATA` alt har trukket.)*
2. **«samples» og «judgment files»** på volumet inneholder passasjetekst fra verkene.
3. **Rammelistene** er avledet av OpenAlex, som er **CC0** — der er CC BY unødvendig strengt, ikke
   for løst, men det bør likevel stå riktig.

Hva vi **faktisk** kan lisensiere er **våre egne data**: klasser, spans, verdikter, κ-beregninger,
registeret, målinger, prosaen vi har skrevet selv.

## 4 Forslag til v0.4.0

**A. Datalisensen presiseres til egne data.** `LICENSE-DATA` skal si eksplisitt hva som **ikke**
dekkes: ordrette sitater fra tredjepartsverk står under sitatrett og videre­lisensieres ikke, og
opphavet til hvert verk står i `LISENS-PER-VERK.md`. Utført i denne slyngen.

**B. Lisenstabellen inn i depositumet.** `docs/LISENS-PER-VERK.md` legges ved, slik at en leser kan
se hvilket verk som har hvilken lisens uten å slå opp 60 DOI-er.

**C. Fulltekster og tekstbiter blir værende utenfor.** Det er ikke en innskrenkning å bevare —
det er **den ene avgjørelsen som holder hele auditen enkel**, og den skal stå skrevet som en
beslutning og ikke som en tilfeldighet. Skulle tekstbitene noen gang deponeres, ville 22 243 vinduer
fra 100 verk være **en vesentlig del** av hvert verk i avledet form, og da styrer lisensen: 13 verk
med NC/ND og 17 uten oppgitt lisens ville måttet holdes ute eller innhentes enkeltvis.

**D. Sitatomfanget beholdes som det er, men begrunnes.** ±2 setninger per passasje er det
preregistrerte vinduet (ADDENDUM-03 § 1.2), ikke et valg gjort for å sitere mest mulig. Det bør stå i
README at sitatlengden følger av måleenheten.

**E. ots-kvitteringene legges ved** (se `TIDSSTEMPEL.md`): 40 filer, til sammen under 40 kB. *(30.09.2026: v0.4.0 bærer
42 kvitteringer, `ots-kvitteringer.zip`, 76 kB.)*

**F. Ett åpent punkt som er eierens:** `W2974992769` er `cc-by-nc-nd` og siteres én gang i
kandidatfila. Sitatet er kort og drøftende, så det hviler på sitatrett — men det er det ene verket der
en leser kan stille spørsmålet, og eieren bør vite det før v0.4.0.

## 5 Det auditen ikke svarer på

* **`other-oa` og `—` er uavklarte, ikke frie.** 21 av 60 verk har ingen brukbar lisensangivelse i
  OpenAlex. Å avklare dem krever oppslag per verk hos utgiver eller arkiv, og det er ikke gjort.
* **OpenAlex' lisensfelt er ikke autoritativt.** Det gjenspeiler hva utgiveren har meldt, og kan være
  utdatert eller feil. Tabellen sier hva rammen så, ikke hva som gjelder.
* **Sitatretten er vurdert, ikke innhentet.** Ingen jurist har lest dette.

## Tillegg 30.09.2026 — fase 3 og v0.4.0

Auditen over ble skrevet 28.09 og dekker ikke fase 3 (ADDENDUM-25): av de 100 nye verkene har **26 NC/ND og 30
ingen oppgitt lisens** (`LISENS-PER-VERK.md`, «Fase 3»). Slutningen står: fase 3-filene i v0.4.0 — måling, rapport,
register, nøkler, verdikter og blindindeks — bærer **ingen passasjetekst** (kontrollert maskinelt i G3 før
publisering), bare id-er, setningsspenn, sha256 og egne begrunnelser. Ett tilfelle ble funnet og rettet samtidig:
`koder2-sammenlikning.json` bar 16 ordrette utdrag og deponeres uten dem (`RELEASE-NOTES-v0.4.0.md`); originalen er
publisert i v0.2.0–v0.3.0 og står der, som korte sitater under sitatretten (§ 2). Tellingene
13/17 i § 4 gjelder de 60 verkene med kandidatrader fra den første kjøringen, ikke alle 100.

