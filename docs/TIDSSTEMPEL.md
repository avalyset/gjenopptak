# Tidsstempling av kanon-bundlene

**28.09.2026.** Hver kanon-bundle er forankret i Bitcoins blokkjede gjennom **OpenTimestamps** —
gratis, uten konto, gjennom fire offentlige kalendere.

## Hvorfor

En kanon-bundle beviser at en låst fil hadde et gitt innhold **i vår egen historikk**. Den beviser
ikke **når**. «Kriteriet ble låst før beregningen» har til nå vært en påstand en leser måtte ta på
tro, eller etterprøve mot filsystemets tidsstempler, som vi kontrollerer selv.

Et ots-bevis gjør påstanden etterprøvbar mot en **tredjepart** — **for låser fra og med 28.09.2026**. Det
er den billigste integritetsforbedringen sporet kan få: null kroner, null konto. For de 40 eldre bundlene,
som alle ble stemplet 28.09.2026, attesterer beviset bare at innholdet fantes 28.09, ikke at PREREG (12.09)
eller kriteriene (25.–27.09) var låst før beregningen; forbeholdet om ekstern tidsstempling står for dem.
*(Rettet 28.09.2026, frys-lesningen: sto at stemplingen «fjerner et helt argument mot preregistreringen».)*

## Hva som er stemplet

**40 av 40 bundler, 0 feil**, 28.09.2026. Kvitteringene ligger i
`repo/kanon/ots/<bundle>.ots` på Vault, med sha256 i `MANIFEST-VAULT.md`. *(Tillegg 28.09.2026: **42 av
42** med bundlene som ble skrevet senere samme dag, alle oppgradert; se «Verifisering».)*

**Bundlen selv stemples**, ikke en fil som inneholder hashen. Den attesterte hashen er da nøyaktig de
bytene manifestet fører sha256 for, og de to stemmer ved konstruksjon. Å stemple en fil som *inneholder*
hashen ville attestert at en tekststreng fantes — et svakere utsagn.

## Kalenderne

`a.pool.opentimestamps.org` · `b.pool.opentimestamps.org` · `a.pool.eternitywall.com` ·
`ots.btc.catallaxy.com`. ots krever **minst to attestasjoner**; under det skrives ingen kvittering.

## Ved hver ny lås

`write_bundle()` stempler automatisk og legger kvitteringen i `repo/kanon/ots/`.
`BundleResult.ots` bærer stien, eller feilmeldingen.

**Stemplingen er ikke en forutsetning for å skrive bundlen.** En lås som ikke kan føres fordi
kalenderne er nede, mister revisjonssporet; en lås uten tidsstempel mister bare
tredjepartsbekreftelsen, og den kan settes i ettertid på samme fil. `stamp()` returnerer derfor en
feil i stedet for å kaste.

## Verifisering

```
ots verify repo/kanon/ots/<bundle>.ots
```

Nye kvitteringer er **ufullstendige** til kalenderen har fått hashen inn i en blokk — typisk noen
timer. `ots upgrade <fil>.ots` henter det fullstendige beviset når det finnes. **Kvitteringene
skrevet 28.09.2026 er oppgradert** til fullstendige Bitcoin-bevis, **42 av 42**, 28.09.2026 kl. 13:49
(`MANIFEST-VAULT.md`, «OpenTimestamps oppgradert til fullstendige bevis»; de uoppgraderte er bevart i
`repo/kanon/ots-for-oppgradering-2026-09-28/`). v0.4.0-utkastet bærer de oppgraderte
(`ots-kvitteringer.zip`, 42 filer, byte-like med `repo/kanon/ots/`). *(Rettet 28.09.2026: sto «er ikke
oppgradert ennå, og det skal gjøres før v0.4.0 deponeres».)*

**Status før oppgraderingen, samme dag:** hashen lå alt i en Bitcoin-transaksjon —
`09bf0b5e97d2845e1a91ac8dc2cdc8ff15377f334c6a15ddd542b2ee5c4880de` hos
`alice.btc.calendar.opentimestamps.org` — og ventet på seks bekreftelser. Forankringen er altså i
gang innen minutter; det som gjenstår, er å hente det fullstendige beviset når blokken er bekreftet.

## Feilen som kostet en feilsøkingsrunde

Første forsøk ga «need at least 2 attestations but received 0 within timeout» mens alle fire
kalenderne svarte HTTP 200 på under 1,3 sekunder. Årsaken var **ikke** nettverket:
venv-Pythonen har ikke systemets CA-lager, så hver kalendersubmisjon feilet stille på SSL. Samme rot
som en tidligere feil mot Perseus. `tidsstempel.py` setter `SSL_CERT_FILE` fra `certifi`.
