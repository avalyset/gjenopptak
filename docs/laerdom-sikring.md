# Lærdom: et sikringssteg testes mot om det kan skade det det skal beskytte

**Skrevet:** 2026-09-12
**Gjelder:** `src/gjenopptak/vault.py`, `src/gjenopptak/securerepo.py`, og
sikringssteget i `src/gjenopptak/harvest/freeze.py`.

## Regelen

Et sikringssteg skal testes mot **om det kan skade det det skal beskytte** — ikke
bare mot om det skriver en fil. «Filen ble skrevet» og «det som alt var sikret er
fortsatt intakt» er to påstander, og den andre er den som betyr noe.

Konkret, for enhver rutine som skriver til et arkiv:

1. Kjør den mot **ekte tilstand**, med ekte arkivinnhold til stede. En test mot en
   tom katalog kan ikke oppdage at rutinen overskriver.
2. Mål arkivet **før og etter** med sha256, og krev at det som ikke var testens
   objekt er byte-identisk.
3. Sjekk navnekollisjoner med vilje: to kjøringer samme dag, to grener, samme
   commit to ganger. Idempotens og destruksjon ser like ut i en logg.
4. Rydd testens spor, og verifiser at ryddingen ikke tok noe annet med seg.

## Saken som ga regelen

Repo-sikringen skrev `git bundle --all` til Vault med filnavnet
`gjenopptak-<dato>.bundle`. Navnet var datobasert, ikke commit-basert.

Sikringssteget ble testet som spesifisert: en dummy-commit på en throwaway-gren,
for å se at steget utløses. Det utløste, skrev en bundle, og meldte suksess.

**Men dummy-bundelen hadde samme filnavn som den ekte og overskrev den.** Arkivet
gikk fra sha256 `468ddbca…` til `327fb3ce…`, og bundelen inneholdt nå
throwaway-grenen og dummy-commiten. Rutinen som skulle beskytte de låste filenes
historikk hadde nettopp erstattet den med en test.

Feilen ble fanget fordi testen gikk mot **ekte tilstand** — den ekte bundelen lå
der da dummyen ble skrevet. Hadde testen kjørt mot en tom testkatalog, ville alt
sett riktig ut, og feilen ville ligget latent til første gang to bundler ble
skrevet samme dag. Det ville skjedd ved neste ADDENDUM, siden addenda og
kodearbeid ofte havner på samme dato.

## Hva som ble endret

* Filnavnet bærer nå **HEAD i tillegg til dato**: `gjenopptak-<dato>-<head12>.bundle`.
  En ny commit gir en ny fil; samme commit gir samme fil. Idempotent, ikke destruktivt.
* Arkivet er delt i to spor med hver sin katalog og hvert sitt navneprefiks —
  `repo/kanon/` for låsecommits, `repo/kode/` for alt annet. Sporene kan ikke
  forveksles, og `write_bundle` kaster `WrongBundleClass` hvis en commit uten
  låst fil forsøkes skrevet til kanon.
* Testen ble gjentatt etter rettingen, mot ekte tilstand, med krav om at den ekte
  bundelen var byte-identisk etterpå. Den var det.

## Hvor det gjelder ellers

Samme form for feil er mulig i alt som skriver til `data/` eller Vault:

* `write_frame` i `freeze.py` — filnavnet er feltnavnet, og en ny frysing av
  samme felt overskriver. Der er det **ønsket**: en frossen liste skal kunne
  kjøres om. Men det betyr at en prøvekjøring med `--max-pages` kan erstatte en
  komplett liste med en avkortet. Derfor merkes avkortede lister `-UFULLSTENDIG`
  i filnavnet, slik at de ikke kan overskrive den komplette.
* `write_raw` i `openalex.py` — filnavnet bærer sha256 av innholdet, så en
  kollisjon betyr identisk innhold. Trygt ved konstruksjon.
* `ensure_manifest_note` og `append_repo_manifest` — føyer til, skriver aldri om.
  Det er nettopp derfor manifestet kunne peke på en flyttet sti etter at bundelen
  ble lagt i `kanon/`. Rettet ved å regenerere seksjonen, ikke ved å redigere raden.
  **Men manifestet er ikke append-only:** `write_vault_manifest` skriver hele filen.
  Se saken under.

---

## Sak 2: manifestet var ikke append-only, og en delvis sikring kunne tømme det

**Skrevet:** 2026-09-12, samme dag som ADDENDUM-06.

`MANIFEST-VAULT.md` har to skrivere. `append_repo_manifest` føyer til en
repo-seksjon; `write_vault_manifest` skriver **hele filen** fra kildelisten.
Setningen «manifestet er append-only» over var feil, og den feilen var det som
gjorde neste steg farlig.

Ved sikringen av recall-fasiten ble `secure_tree` kalt med `only=[fire filer]`
og deretter `write_vault_manifest`. Det ville erstattet et manifest over **969
filer** med ett over **4** — uten feilmelding. Raden for hver av de 965 andre,
med sha256, kilde-URL og hentedato, ville vært borte. For hentet fulltekst er
nettopp de radene det som gjør rammemedlemskap etterprøvbart den dagen en lenke
svarer 403.

Det skjedde ikke, og grunnen er tilfeldig: `require_vault()` returnerer
`<rot>/gjenopptak-kilder`, og kallet la på `gjenopptak-kilder` en gang til.
Skrivingen gikk til en nøstet katalog i stedet for over det ekte manifestet.
**En tilfeldig stifeil, ikke en sperre, var det som holdt.** Overskrivingen
skjedde likevel senere, med riktig sti: repo-seksjonen forsvant, og den måtte
føres inn på nytt fra bundelen på disk.

### Hva som ble endret

* `write_vault_manifest` kaster nå `ManifestWouldShrink` når det eksisterende
  manifestet beskriver flere filer enn rapporten. Tilsiktet krymping må sies
  eksplisitt med `allow_shrink=True`.
* Overskrivingen **bærer repo-seksjonene over** (`split_repo_sections`). Den
  andre skriverens arbeid kan ikke lenger slettes av den første.
* Tre tester, alle mot ekte tilstand etter regelen over: at et stort manifest
  ikke kan erstattes av et lite, at filen er byte-identisk etter et nekt, og at
  repo-seksjonen står igjen etter en lovlig overskriving.
* Den lille tilføyelsen til regelen: **punkt 2 gjelder også filer som ikke er
  binære.** Et manifest er arkivets innholdsfortegnelse, og en innholdsfortegnelse
  som stille blir kortere, er verre enn en fil som forsvinner — for da ser arkivet
  fortsatt komplett ut.
