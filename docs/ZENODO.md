# Zenodo-deponeringen

**Deponert:** 2026-09-25. **Gjeldende versjon:** 0.4.0 (2026-10-01). *(Sto til v0.4.0: «0.3.0 (2026-09-26)».)*

| | |
|---|---|
| **Konsept-DOI** (siter denne) | **10.5281/zenodo.22959326** |
| **Versjons-DOI** (v0.4.0, gjeldende) | **10.5281/zenodo.23073893** |
| Versjons-DOI (v0.3.0) | 10.5281/zenodo.22976464 |
| Versjons-DOI (v0.2.1) | 10.5281/zenodo.22975301 |
| Versjons-DOI (v0.2.0) | 10.5281/zenodo.22965761 |
| Versjons-DOI (v0.1.0) | 10.5281/zenodo.22959327 |
| Post | https://zenodo.org/records/23073893 (v0.3.0: https://zenodo.org/records/22976464) |
| Lisens på depositumet | CC BY 4.0 (koden inni er Apache-2.0, jf. `LICENSE`) |
| Filer | 98 (v0.3.0: 38, v0.2.0: 38, v0.1.0: 35) |

## Hva som ligger der

Protokollen (PREREG-v1) med addendaene og beslutningsnotatene slik de sto ved hver versjon (v0.1.0:
ADDENDUM-01–10; ADR-numrene 0005 og 0006 er brent og har aldri eksistert), lærdomsloggen,
resultatnotatet, manuskriptutkastet, kriteriet og resultatet for det ene gjennomførte tilfellet
(PS-246), vurderingene av løftbare kandidater, registeret (`claims.jsonl`), README og lisensfilene,
kildekoden som tarball, `MANIFEST-VAULT.md` med sha256 for alt datamateriale, og **en bundle av hele
git-historikken** (alle refs).

Dataene selv — frosne rammelister, utvalg, fulltekster, dommer — ligger utenfor depositumet, på
eksternt volum, oppført med sha256 i manifestet som er med.

## Tidsstemplingen

Preregistreringen ble låst **internt** før data, 12. september 2026, og rettet gjennom daterte addenda
(ti ved v0.1.0, ADDENDUM-01–25 per 28.09.2026) som hver er commitet alene med egen sha256. Den ble **ikke tidsstemplet hos tredjepart før denne
deponeringen**. De interne låsedatoene er belagt av git-historikken alene — den ligger i depositumet
som bundle, slik at rekkefølgen kan etterprøves, men en uavhengig garanti for at protokollen kom før
dataene, finnes først fra 25. september 2026.

Dette står også i selve postens beskrivelse på Zenodo, ikke bare her.

## DOI-oppslag

Ved publisering av v0.1.0 svarte `https://doi.org/10.5281/zenodo.22959327` med **HTTP 404**:
DataCite hadde ennå ikke registrert håndtaket. **Det er nå løst.** Ved kontroll senere samme dag
svarte både versjons-DOI-en og konsept-DOI-en **HTTP 302** til Zenodo. DOI-ene kan oppgis videre.
Forbeholdet fra v0.1.0 er dermed innfridd, ikke fjernet: registrering hos DataCite tar tid, og et
ferskt oppslag bør gjentas før en DOI siteres.

**Samme mønster gjentok seg ved v0.2.1 (2026-09-26).** Rett etter publisering svarte
`https://doi.org/10.5281/zenodo.22975301` **HTTP 404**, mens konsept-DOI-en svarte **302**. Den nye
versjons-DOI-en skal derfor ikke oppgis videre før et ferskt oppslag gir 302. Konsept-DOI-en er
uansett den som siteres, og den peker alltid til nyeste versjon.

## Neste versjon

En ny versjon deponeres mot samme konsept-DOI. Versjons-DOI-en endres, konsept-DOI-en gjør det
ikke — det er den som skal siteres i CITATION.cff og i manuskriptet.

## Versjon 0.2.0 (2026-09-25)

Lagt til: ADDENDUM-11 (uavhengig omkoding og κ), oppdatert manuskript, resultatnotat og lærdomslogg,
koder 2s verdiktfil, sammenlikningsfilen og ny git-bundle. Kildetarballen er byttet til 0.2.0.
De 35 filene fra v0.1.0 følger med, uendret der de ikke er nevnt.

Hovedtallet som kom til: κ = 0,81 [0,70–0,91] på treff/ikke-treff mellom to uavhengige kodinger.
Hovedfunnet står i begge lesninger. M2 bærer koderidentitet og er ikke operasjonalisert.

## Versjon 0.2.1 (2026-09-26)

**Bare metadata. Ingen data, kode, dokument eller resultat skiller seg fra 0.2.0.**

`CITATION.cff` i 0.2.0-posten var foreldet: den sa `version: "0.1.0"` og førte bare konsept-DOI-en,
fordi filen ikke ble lastet opp på nytt da 0.2.0 ble laget. Funnet kom av et søk etter navneformen
«Bottenvik» i publisert materiale — feilen var en annen enn den som ble søkt etter.

Denne versjonen bytter den ene filen. Zenodo tillater ikke filbytte i en publisert post, så en ny
versjon var eneste vei; det er derfor versjonsnummeret på *posten* er 0.2.1 mens filen fortsatt
beskriver utgivelsen **0.2.0** — innholdet er 0.2.0s, og de tre DOI-ene som var tildelt fram til den.
Versjons-DOI-en for 0.2.1 står bevisst ikke i filen.

| | |
|---|---|
| Fil byttet | `CITATION.cff`, 1 735 B |
| sha256 | `b723f9d9d9bfc0061629a381d1f721383a4e0f9db4e83d413e090dc3f59dd37d` |
| md5 (Zenodos eget) | `682642b40b884764bb125ea21af7cc62` (før: `49f4fcd2ab8ea53d94139c87e9bad33e`) |
| Port før publisering | filkartet mot 0.2.0 viste **én** endret fil av 38 |
| Frys-lesning | versjon, tre DOI-linjer, navneform og ORCID lest i filen slik den lå i utkastet |
| HTTP | newversion 201 · fil-DELETE 204 · fil-PUT 201 · metadata-PUT 200 · publish 202 |

Filen ble hentet tilbake fra den publiserte posten og er byte-identisk med repoets `CITATION.cff`.

## Versjon 0.3.0 (2026-09-26)

**Elleve foreldede tall rettet i resultatnotatet.** Seksjonene over oppdateringstabellen i
`RESULTAT-PORT-v1.md` bar tall fra før ADDENDUM-10 uten at det gikk fram av seksjonen selv — blant
dem hovedfunnet **71 %**, der abstract, manuskript og preprint sa **68 %**. Alle er oppdatert, det
gamle står merket «før ADDENDUM-10» i samme setning eller rad, og hvert tall som bærer
koderidentitet står nå med begge kodere. Ingen måling er gjort om; ingen verdi er slettet.

| tall | før | nå |
|---|---|---|
| H7-andel av ekte treff | 17 av 24 = 71 % | koder 1 17 av 25 = 68 % · koder 2 12 av 19 = 63 % |
| M1-passasje korrigert | 0,652 | 0,671 · 0,604 |
| M1-streng korrigert | 0,649 | 0,667 · 0,599 |
| M2 | 87,5 % (21/24) | 88,0 % (22/25) · 31,6 % (6/19) |
| presisjon | 16,0 % (24/150) | 16,7 % (25/150) · 12,7 % (19/150) |
| presisjon energimodellering | 5,3 % | 7,0 % · 1,8 % |
| løftbar andel | 4 av 24 = 16,7 % | 5 av 25 = 20,0 % · 2 av 19 = 10,5 % *(koder 2 rettet 28.09.2026: løftbar 2 av 17 avklarte = 11,8 %, uavklart 2 av 19 = 10,5 %)* |
| H7–H9-andel | 20 av 24 = 83,3 % | 20 av 25 = 80,0 % |
| letekostnad | ~37 dømte treff per løftbart | ~30 · ~75 |
| skalert løftbare | ~58 | ~72 · ~29 |
| de 48 tvilstilfellene | «uavgjort» | avgjort av ADDENDUM-10 |
| falsifiseringens dekning | «alle fire løftbare prøvd» | fire av fem; PS-031 ikke prøvd |
| forbehold 1 | «Én koder» | to kodere, κ = 0,81 |

Endrede filer: `RESULTAT-PORT-v1.md`, `LAERDOM.md` (pekere i § 16 og § 17, ny § 24),
`CITATION.cff` (0.3.0, fem DOI-linjer), ny kildetarball `0.3.0` og ny git-bundle. De øvrige 33
filene følger uendret med.

**Ny kontroll:** `python -m gjenopptak.kryssjekk` leser filene **mot hverandre** — samme størrelse
skal ha samme verdi i alle filer som deponeres, eller være merket med hvilken versjon den tilhører.
Frys-lesningen før v0.2.0 leste hver fil for seg; hver fil var konsistent med seg selv, og derfor
bestod alle. Kjørt på utkastets egne nedlastede filer før publisering: **0 umerkede foreldede
verdier over 13 filer.** Bakgrunnen står i LAERDOM § 24.

**DOI-oppslag:** `10.5281/zenodo.22976464` svarte **HTTP 404** rett etter publisering, som ved
v0.1.0 og v0.2.1. Konsept-DOI-en svarte **302**. Vent på 302 før versjons-DOI-en oppgis videre.

## Versjon 0.4.0 (2026-10-01)

**Versjons-DOI:** **10.5281/zenodo.23073893**. **Post:** https://zenodo.org/records/23073893 (98 filer). Konsept-DOI-en
**10.5281/zenodo.22959326** er uendret og er den som siteres.

**Hva som er nytt:** fase 2 (seks saker, ingen opphevet hindring), fase 3 (ADDENDUM-25: prospektiv port på 100 nye
arkeologiverk, port (1) bestått med 85 av 100 [76,7–90,7], lista heter «arbeidsliste (prospektiv port)», og første
målte silrecall, 95 av 104), ADDENDUM-12–25, ADR-0011–0014, METODE, manuskriptutkast v2.8 med sju
faktasjekkrapporter, regelfilen bak κ = 0,812, leseroppdragene med sperreliste, blindfilene som indeks, nøklene til
de ferdige målingene (nøkkelregelen i portstatusen § 6), ots-kvitteringer og en git-bundle av hele historikken.
Hva som er utelatt og hvorfor: `docs/RELEASE-NOTES-v0.4.0.md`. Filkart mot v0.3.0 og portene:
`docs/UTGIVELSE-v0.4.0-PORTSTATUS.md`.

**DOI-oppslag:** ved hver tidligere versjon svarte en fersk versjons-DOI **HTTP 404** i timene etter publisering.
Den oppgis ikke videre før et oppslag gir **302**. **v0.4.0 svarte 302 med en gang** (01.10.2026), og konsept-DOI-en
likeså. Versjons-DOI-en ble reservert i utkastet før publisering.

**Zenodo tillater høyst 100 filer per post.** v0.4.0 har 98: sakfilene, faktasjekkrapportene og leseroppdragene
ligger i hver sin zip (`RELEASE-NOTES-v0.4.0.md`).

