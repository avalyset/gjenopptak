# Depositumskravet 10.10.2026 — hva en låst måling leste, og hva v0.5.0 mangler

**Kravet** (INSTRUKSER § 12, frys-regelen pkt. d): alt en låst måling leste, skal med i depositumet — blindfiler,
regelfiler, sperrelister — og en måling skal ikke stå uten deponert grunnlag. Dette dokumentet fører hva Zenodo
v0.5.0 (10.5281/zenodo.23120143) bærer og ikke bærer, og hva v0.6.0 legger til.

## 1 Hvordan det er slått opp

* **v0.5.0 slik den er publisert:** fillisten hentet fra Zenodo 10.10.2026 (98 filer). Alle 98 er like utkastet på
  Vault (`zenodo/v0.5.0-utkast/`) på navn og md5. Sammenlikningen under er gjort på sha256 mot de 98 filene og mot
  hvert medlem i zip-filene og kildetarballen: 347 sha256 i alt.
* **Hva målingene leste og ga:** hver fulle sha256 som `PREREG-v1.md`, `ADDENDUM-01` til `-28`, `docs/RESULTAT-*.md`
  og `docs/METODE.md` navngir (63), slått opp i `MANIFEST-VAULT.md`; og utfallsfilene for hvert addendum slik de står i
  `docs/GJENOPPTAK_ADDENDUMSTATUS_v1_2026-10-10.md`. I alt 148 navngitte stier; noen få er samme fil under to navn
  (den lokale kopien i `data/` og Vault-kopien).
* **Andres tekst:** pakkingen søker hvert vindu på 50 tegn i hver strengverdi mot de 6 213 unike
  passasjene på minst 50 tegn i de 32 blindfilene, blanktegn regnet som like, og feiler om et ordrett
  utdrag står igjen (§ 7). Et første søk prøvde bare ett utdrag per passasje og fant ni; frys-lesningen før
  utgivelsen viste at det var en stikkprøve.

## 2 Det oppdraget spurte om: regelfilen bak κ = 0,812

**Den mangler ikke.** `koder2/koderegler-gjenvunnet.md` (sha256 `234695dd…8449`) ligger i v0.4.0, v0.4.1 og v0.5.0 som
`koder2-koderegler-gjenvunnet.md`, sammen med `REGELFIL-KODER2-GJENVUNNET-2026-09-27.md`, koder 2s oppdrag med
sperrelisten (`oppdrag.zip`) og koder 2s verdikter. v0.1.0–v0.3.0 mangler den, som INSTRUKSER § 12 sier.

**Det som mangler bak κ = 0,812, er koder 1s verdikter.** Koder 2s fil er deponert; koder 1s er det ikke. Uten den kan
ingen κ mot koder 1 regnes fra depositumet — verken 0,812, 0,636, 0,248 eller noen av de andre.

## 3 Funnet

v0.5.0 bærer dokumentene, fase 3 og koder 2. **Den bærer ikke utfallsfilene for målingene i ADDENDUM-01 til -24.**
Tallene står i addenda og resultatnotater, og hver fil har sha256 i det deponerte manifestet, men filene selv ligger
bare på Vault.

| | stier |
|---|---|
| navngitt i addenda, resultatnotater og addendumstatusen | 148 |
| ligger alt i v0.5.0, eller følger git (medregnet lokale kopier av slike) | 17 |
| inn i v0.6.0 i `maalefiler.zip` | 107 byte for byte eller med utdrag tatt ut, 9 uten tekstfelt, og koder 1s verdikter |
| holdes ute med grunn | 7 |
| for store for zip-filen, ligger på Vault | 6 |
| finnes ikke lenger | 1 (fase 4-dommeren: tatt ut 03.10.2026, slettet per 07.10.2026) |

Radene summerer ikke til 148: to av filene i zip-filen er Vault-kopier av stier som står med `data/`-navn i
addendumstatusen, og kilden til koder 1s verdikter står også blant dem som holdes ute.

## 4 Inn i v0.6.0 uten tekstfelt

Tekstfeltene (`passage_text`, `sentence_text`, `passasjetekst`, `passasje`, `setning`, `text`, `tekst`, `datatilgang_seksjon`, `utdata_raa`) er byttet med sha256 og lengde. Navnet får `-uten-tekst`.

| fil på Vault | addendum | sha256 (kilden) |
|---|---|---|
| `ekstraksjon/2026-09-26/ekstraksjon2-logg.jsonl` | A17 | `1ef06b1c1e9c674356c010213977fe48d9c695c62d9cbb90c2aff96c600eae37` |
| `logs/anker-setninger.json` | A02 | `6efea9404f6569b5d0e479d1033d729ee96b238ebdebb8dcdc564337571b4c06` |
| `logs/h1h4-funn.json` | A03 | `826df190d5c5c61b14d3513ec7dbe92f60da628c3621e5c101255ce2f6c59e00` |
| `logs/recall-sett-2-maaling.json` | A07 | `9683655272d2945e5631edeaab4249e1980c92de7a17bdb931695d705146e4ba` |
| `logs/recall-sett-2.jsonl` | A07 | `40b3776ecb34c9e1748f086c20fd1adaf10f40412d1de10e334f00039cdfcefc` |
| `logs/recall-sett.jsonl` | A06 | `f2c9bf80040c9ad96b064b4399961bf927fd77a58b088132add2a981d7dcbe27` |
| `presisjonssett/port-tvil.jsonl` | A10 | `a37aa3f34d70d5faeaf0f8a3a661ac08fdb912bd7186d84d1faa574796adca1a` |
| `verksniva-2026-09-26-v2.json` | A13 | `6bb4efbdcfe2d810293369587b15787dc75fa175971736c4b3aa9e6373bd666e` |
| `verksniva-2026-09-26.json` | A13 | `56534f6ffc32c1c3906a6ae1ffe00f488cccf52ed255cabdfb2085a0e1b40828` |
| `presisjonssett/port-presisjonssett-ADDENDUM10.jsonl` → `port-presisjonssett-verdikter-koder1-ADDENDUM10.jsonl` | A10, A11 og alle κ mot koder 1 | `6a04079c31fbbc60a8a189232a7ef37f55756ce18c74545d10bf062fcea70c36` |

Koder 1s verdikter deponeres med feltene `id`, `ekte_treff`, `min_klasse`, `min_bedømbar`, `tvil`, `min_begrunnelse` — samme form som koder 2s deponerte fil.
Tekstfeltet, verk-ID, spenn, dommerens klasse og utvalgstype følger ikke med; de er nøkkelen (§ 5). Begrunnelsesfeltet
siterte passasjen tolv steder; de utdragene er tatt ut (§ 7). *(Rettet 10.10.2026: sto «elleve»; tabellen i § 7 og filen har tolv.)*

## 5 Holdes ute

| fil på Vault | grunn |
|---|---|
| `kandidat432/8-register.jsonl` | deponert som register-v2-indeks.jsonl |
| `presisjonssett/koder2-sammenlikning.json` | 16 ordrette utdrag; versjonen uten tekst er deponert |
| `presisjonssett/port-presisjonssett-ADDENDUM10.jsonl` | tekst og nøkkelfelt; koder 1s verdikter deponeres avledet uten tekst og uten nøkkelfelt |
| `presisjonssett/port-presisjonssett-blind.jsonl` | tekst (lisensbeslutningen); deponert som indeks |
| `presisjonssett/port-presisjonssett-nokkel.jsonl` | nøkkelregelen: port-320 er blindfil for ADDENDUM-21 og -28, som er låst og ukjørt, og kilde for A-strata i ADDENDUM-27 |
| `revisjon-2026-10/menneskevalidering/blind.jsonl` | tekst (lisensbeslutningen); utvalgsfila er deponert |
| `revisjon-2026-10/menneskevalidering/nokkel.jsonl` | nøkkelregelen: ADDENDUM-27 er ukjørt |

Blindfilene er deponert som indeks (`blindfiler-indeks.zip`), som før. **Nøkkelen til port-320 er eierens
avgjørelse:** den holdes ute fordi ADDENDUM-21 og ADDENDUM-28 er låst og ukjørt på samme blindfil. Skal ingen av dem
kjøres, kan nøkkelen deponeres — det er ikke gjort her.

## 6 For store for zip-filen

Rammelistene og verdiktene fra hentingsprøven. De ligger på Vault med sha256 i `MANIFEST-VAULT.md`.

| fil på Vault | sha256 |
|---|---|
| `frames/frame-tekstvitenskap-RAW.jsonl` | `3a9389959ba3ea6cd3cf11ac05fb3d7604738a1514171248c36a706e7a4f852c` |
| `frames/frame-energimodellering-HENTBAR.jsonl` | `7df1b27a44ba939b3dde4cf11c72199e3a8134be5b06b99ccbaf39bc186c381e` |
| `logs/hentingsprove-energimodellering-verdikter.jsonl` | `4ef5f1cfc8fd5a41ea57d73245d81ef8e201a0a1de19e1b43e6f2c72d8697a2c` |
| `frames/frame-energimodellering-RAW.jsonl` | `56d80195d2df726fe49961269a2a4b2f215c6534cb9783c7dc66a1d725048209` |
| `frames/frame-arkeologi-RAW.jsonl` | `1050450fc774e56affc21c99e0ffc3c59682ff391c1e46163c69a50d5cdf241a` |
| `frames/frame-klinisk_epidemiologi-RAW.jsonl` | `ee783f99b184761b64a95a51603cc48910331628d2a3bd15d0e17240e5929ac5` |

## 7 Ordrette utdrag

Begrunnelsene til modeller og kodere siterer passasjene de dømmer. **101 ordrette utdrag på 50 tegn eller mer er tatt
ut av 17 av filene i `maalefiler.zip`**, det lengste på 424 tegn. Sammenlikningen ser bort fra blanktegn, bokstavstørrelse
og Unicode-form: et sitat som bare har fått stor forbokstav, er fortsatt et utdrag. Hvert er byttet med et merke som bærer lengde og
sha256 av utdraget, så filen kan etterprøves mot Vault-kopien. Kortere sitater står, og titler er ikke rørt.

| fil | utdrag tatt ut | lengste (tegn) |
|---|---|---|
| `ekstraksjon/2026-09-26/addendum-18/haiku45-dommer.jsonl` | 18 | 166 |
| `leser-lokal-ADDENDUM-24/parti-06.json` | 18 | 229 |
| `presisjonssett/port-presisjonssett-verdikter-koder1-ADDENDUM10.jsonl` | 12 | 77 |
| `presisjonssett/port-presisjonssett-verdikter.jsonl` | 12 | 77 |
| `triage-loftbare-2026-09-26.json` | 10 | 424 |
| `ekstraksjon/2026-09-26/addendum-20/haiku45-dommer.jsonl` | 7 | 77 |
| `presisjonssett/port-tvil-uten-tekst.jsonl` | 6 | 77 |
| `ekstraksjon/2026-09-26/addendum-19/opus5-dommer.jsonl` | 4 | 60 |
| `arbeidsliste/okt-5-verdikter.jsonl` | 3 | 106 |
| `ekstraksjon/2026-09-26/addendum-19/opus5-b-dommer.jsonl` | 2 | 59 |
| `ekstraksjon/2026-09-26/addendum-20/sonnet5-dommer.jsonl` | 2 | 60 |
| `logs/recall-sett-2-uten-tekst.jsonl` | 2 | 77 |
| `arbeidsliste/okt-2-verdikter.jsonl` | 1 | 93 |
| `arbeidsliste/okt-7-verdikter.jsonl` | 1 | 59 |
| `koder4/koder4-fable51-verdikter.jsonl` | 1 | 52 |
| `verksniva-2026-09-26-uten-tekst.json` | 1 | 57 |
| `verksniva-blindverk-VERDIKTER.json` | 1 | 57 |

Kontrollen er gjort to ganger med to metoder: pakkingen selv, som feiler om et utdrag står igjen, og et uavhengig
søk over den ferdige zip-filen. Søket kjenner bare passasjene i blindfilene; setninger fra kontrollartiklene er tatt på
feltnavn (§ 4).

**De to metodene var først ikke uavhengige der det gjaldt.** Begge skilte mellom store og små bokstaver. Et nytt søk
10.10.2026, uten det skillet, fant ett sitat på nøyaktig 50 tegn som sto igjen i tre filer fordi koderen hadde gitt
det stor forbokstav. Sammenlikningen er rettet (`_norm` i `maalefiler.py`, med test), tallet gikk fra 98 til 101, og
det uavhengige søket finner nå bare én streng igjen i zip-filen: en verktittel i et tittelfelt, som ikke regnes
som utdrag (§ 4).

**Kandidatlista er renset, i repoet og dermed i v0.6.0.** `SAKBEHANDLING-2026-09-27-kandidater.md` siterte
passasjene den lister: 83 ordrette utdrag på 50 tegn eller mer, det lengste på 1 039 tegn. Eieren avgjorde 10.10.2026
at lista får samme uttak som `maalefiler.zip`. Filen i repoet er rettet (64 548 B før, 32 939 B etter, med en datert
merknad under tittelen), og `saker.zip`, utgivelsestreet og kildene fra og med v0.6.0 bærer den rensede. Byggingen
kontrollerer at ingen utdrag står i den, og feiler ellers (`UTEN_UTDRAG` og `kontroller_uten_utdrag` i
`utgivelse.py`). Et uavhengig søk finner ingen 50-tegnsvinduer fra passasjene. **Lista slik den sto, er ikke borte:**
den ligger i git-historikken, som bundelen bærer, på GitHub i utgivelsene v0.4 og v0.4.1, og i Zenodo
v0.4.0–v0.5.0. Publiserte poster kan ikke endres, og historikken skrives ikke om. En kopi er sikret på Vault,
`saker/kandidatliste-original-2026-09-27/`.

**Resten er ikke rørt.** Samme søk over resten av v0.6.0-utkastet finner 59 sammenfall på 50 tegn eller mer i 19
filer utenfor `maalefiler.zip`, det lengste på 158 tegn: sakdokumentene og triagelista, som siterer med
kildeangivelse (31 i åtte filer i `saker.zip`), koder 2s verdikter (9, lengste 72 tegn),
`NAVNEKONTROLL-2026-09-29.md` (6), eksempelstrenger i `extract/passage.py` i kildearkivet (5), og enkeltsitater i fem
andre filer. Tre av de 59 er ikke sitat: det er tittelen på et verk i referanselista i manuskript v3.1, v3.2 og
v3.3, som en passasje også nevner. Alle filene unntatt manuskript v3.2 og v3.3 har ligget i depositumet før.
Sitatene hviler på sitatretten slik lisensauditen sier.

## 8 Inn i v0.6.0 byte for byte, eller med utdrag tatt ut

| fil på Vault | addendum | bytes (kilden) | sha256 (kilden) | form i zip |
|---|---|---|---|---|
| `arbeidsliste/koder-c-komplett.json` | A22 | 991 | `a2d72d53033dc601f2159367e6eda11d10dd148a4c9498e228e8ae737e734b10` | som den er |
| `arbeidsliste/okt-1-verdikter.jsonl` | A22,A23 | 72208 | `fe3481c638d4439d29f5ba8d2e7d0213e741f50e4cb09f7c2a3402261d02becc` | som den er |
| `arbeidsliste/okt-2-rest-verdikter.jsonl` | A22,A23 | 16360 | `d7d6cde447d1e023c1655a9578550a9cd2f9f11ce4d489c231f32d61c60360c9` | som den er |
| `arbeidsliste/okt-2-verdikter.jsonl` | A22,A23 | 61042 | `9fbb8c6d4ecc872a8b4d0366b6da4f1c5fde105d56ff20c53590c77e9a0b4219` | utdrag utelatt |
| `arbeidsliste/okt-3-rest-verdikter.jsonl` | A22,A23 | 10299 | `4429166f9c5d635228379125b45ec93354bb674b50bb876a1b0234c8ba1a3329` | som den er |
| `arbeidsliste/okt-3-verdikter.jsonl` | A22,A23 | 64774 | `cb853503965fef400370e362450d9ce06f101457142b148f206c564057c9821b` | som den er |
| `arbeidsliste/okt-4-rest-verdikter.jsonl` | A22,A23 | 23424 | `2ba6faab5236cae4a80243c9fbb8c6fcac88c18203907c9b9b3b55d568ed8f22` | som den er |
| `arbeidsliste/okt-4-verdikter.jsonl` | A22,A23 | 52776 | `0ca53b87f8df6580c75762a4f9b86d0f79ac0e15180de4a7f1c3fc65d515cab4` | som den er |
| `arbeidsliste/okt-5-verdikter.jsonl` | A22,A23 | 77957 | `99252abd912557b67fd5bab42803f411dcaded9ed26bb8253ce8988164c40ee7` | utdrag utelatt |
| `arbeidsliste/okt-6-rest-verdikter.jsonl` | A22,A23 | 23790 | `3a8cda9d571dba5fcf95d1fa055dde09155e9930752b8bda4df228d49f6f36dc` | som den er |
| `arbeidsliste/okt-6-verdikter.jsonl` | A22,A23 | 55288 | `feac3a51818a469ffcd747a3ac00da0ed92699ffccd2cbe9bdb2cbfcbb692660` | som den er |
| `arbeidsliste/okt-7-rest-verdikter.jsonl` | A22,A23 | 7299 | `07be1786a201f0e04c5601d5fd594f1c1034cf278902bdf89c13efbbf491ef09` | som den er |
| `arbeidsliste/okt-7-verdikter.jsonl` | A22,A23 | 69735 | `a3f142782e4d8ad9650648e08ac29f7afa0cdf693628c3501bff99c951a6acb5` | utdrag utelatt |
| `arbeidsliste/okt-8-verdikter.jsonl` | A22,A23 | 75545 | `f34282881647f27803254ef15e0eabfcd4079a043f8a5ce8ce69fcda079f4962` | som den er |
| `arbeidsliste/presisjon-100-maal.json` | A23 | 457 | `515f0868146bede3ffb9e42aed24469533cc287250c4a19d956d1c95ec5579df` | som den er |
| `arbeidsliste/presisjon-100-verdikter.jsonl` | A22,A23, A23 | 21598 | `667dffc4a075405b68ce15a35653fb9d3cdc72258a8036cb0c47ba801831f0ac` | som den er |
| `arbeidsliste/presisjon-rest-verdikter.jsonl` | A22,A23, A23 | 4068 | `fcea39ce253be406704853a8834ba952605fe25ee7bc40002b15dd0b398822b9` | som den er |
| `ekstraksjon/2026-09-26/2d-blind-presisjon.json` | A16 | 357 | `b0197d4c9a690c47be3c676b715b2fd287107a288ea05ce7b4ef22a1a05ebc01` | som den er |
| `ekstraksjon/2026-09-26/2d-blind-q-100-NOKKEL.json` | A16 | 6032 | `5f5e5eef8bc8efd4a0ed43eae58fa09700c2dc9f5f1a91379601c86c3c4c7841` | som den er |
| `ekstraksjon/2026-09-26/2d-blind-q-100-VERDIKTER.json` | A16 | 13306 | `df11a23cd2db720386501f1fb7e8541901eabc534e215f6fecfc718d3f853324` | som den er |
| `ekstraksjon/2026-09-26/2d-blind-q-regler.md` | A18,A19 | 1346 | `00d69c09ed8b9045fd3cd5e3362b29c82df4b5f9a66dccc7a5476619304bf247` | som den er |
| `ekstraksjon/2026-09-26/2d-recall.json` | A16 | 1202 | `49de2dc55d162fbfdee647fdbaacc4f8f285344a46cc1be01d9d0be01958747b` | som den er |
| `ekstraksjon/2026-09-26/2d-tid.json` | A16 | 249 | `3dbcc86a0f2b02bba3b535c323f0c6c21976a9de3fc93785187d0ed00cd39308` | som den er |
| `ekstraksjon/2026-09-26/a17-2p-mot-2d.json` | A17 | 570 | `5724047eaaa2e56a90eb2283596c7ce541c23d5b42e0dfaa326120c66bc294cc` | som den er |
| `ekstraksjon/2026-09-26/a19-a20-full-regelfil.json` | A20 | 1056 | `cfa59cecf405c65f02138a86a689dced4190a50becbd5ac6b789ad63058ea857` | som den er |
| `ekstraksjon/2026-09-26/a19b-utfall.json` | A18, A19 | 1469 | `6987d599c045994da2a0d4d048e85b83d33557a8285247039d6da793df4c8df0` | som den er |
| `ekstraksjon/2026-09-26/addendum-18/a18-kappa.json` | A18 | 3177 | `9f6dee6d39aa33254aa6393f2fff9304eae2e05550068e9c08ac017c5ad19ecf` | som den er |
| `ekstraksjon/2026-09-26/addendum-18/haiku45-avkuttet-rekjort.jsonl` | A18 | 6659 | `da4930fbd8ed881f1738b106e0794e078522d7d39911680839ca25b2be1c97c8` | som den er |
| `ekstraksjon/2026-09-26/addendum-18/haiku45-dommer.jsonl` | A18 | 279095 | `41d2f62fc81442a3772d74ed6372cd1774bfd7e6e6d80af19beb77854d159a20` | utdrag utelatt |
| `ekstraksjon/2026-09-26/addendum-18/sonnet5-pass1-avkuttet-rekjort.jsonl` | A18 | 10613 | `d0baf4f4af0fb661cde5d755dbf4eae0fd91c73772aeca7c85d65895efa9ecc0` | som den er |
| `ekstraksjon/2026-09-26/addendum-18/sonnet5-pass1-dommer.jsonl` | A18 | 291432 | `c72cb0d367b3a23a1bb356d441f58439ec57346d268762dae11860d99d557a93` | som den er |
| `ekstraksjon/2026-09-26/addendum-18/sonnet5-pass2-dommer.jsonl` | A18 | 291271 | `cd452b2486d074e237fd5b4d343b226aa9dadb7d45ca53ea80a20e7434f6484c` | som den er |
| `ekstraksjon/2026-09-26/addendum-19/opus5-b-dommer.jsonl` | A19 | 337639 | `296fdb78ab459aa3347338c6e91e3fbf316a0e62dc7c17bb58907d5bdf854a01` | utdrag utelatt |
| `ekstraksjon/2026-09-26/addendum-19/opus5-dommer.jsonl` | A19 | 328669 | `8f4758a7f409f6d42a3d5eb644a46e8689afd7488953ea71df71071bec12b07b` | utdrag utelatt |
| `ekstraksjon/2026-09-26/addendum-20/a20-partiell.json` | A20 | 1264 | `f85beab91ed58189bf23fa37b1d5f108d76d3f04afe122049fa331e885412166` | som den er |
| `ekstraksjon/2026-09-26/addendum-20/haiku45-dommer.jsonl` | A20 | 322892 | `528248cfd314a9e8faf0370d330ee50d33021a17fa5820fb2dbade7b6fd3193b` | utdrag utelatt |
| `ekstraksjon/2026-09-26/addendum-20/sonnet5-dommer.jsonl` | A20 | 329779 | `29a1a5a653b94fa46959dd5ca46bec4ec30f2d770b192e7265135f50a1186e59` | utdrag utelatt |
| `ekstraksjon/2026-09-26/b1-duplikatrate.json` | A17 | 26360 | `11eb83d55b018fe9a7f0dd92154b24530c13527b967d8ebf281cfa0c5d6b9d52` | som den er |
| `ekstraksjon/2026-09-26/b2-nevner.json` | A16 | 4081 | `ebc4052e95c2c7c0ec256f36b9e845e62e3a26ba65b6f459f0fb2181724d139a` | som den er |
| `ekstraksjon/2026-09-26/d1-2x2.json` | A18 | 533 | `9ac22605120d176652c9f70b66cfb15a7255d4d858db76274bbd04b3872b9b58` | som den er |
| `ekstraksjon/2026-09-26/h2-trekking.json` | A10 | 1038 | `48c07b3083f77e1ae27e4e9f2969d990bd310a99141f19aaa59d8dff6743e9ce` | som den er |
| `ekstraksjon/2026-09-26/k1-de-27.json` | A22 | 784 | `d3c203ab34c9ec9b228047a3514fbf2d496b67df1e6ff8aecb9af39f7fb4306c` | som den er |
| `ekstraksjon/2026-09-26/k1-union-v2.json` | A10, A22 | 1325 | `86381d18560c252a9f84c7b0763ecdd727ad9beacc37e562d4015211bcd5430f` | som den er |
| `embeddings/kjoring.json` | A14 | 572 | `0f313b71b568f8a2490a8b18f55a34eee4842d5f66706f11ee55fa0fa7026d32` | som den er |
| `embeddings/maaling.json` | A14 | 933 | `e587157b4fb9eccfc6fc9ff719ad3f4b033011fa7085827966bfaaed8d76f70a` | som den er |
| `falsifisering-2026-09-21/falsifisering-2026-09-21.json` | PREREG-v1 | 1315 | `11aeb78942afb259194b3ea828e01943d3e84d691885eeb41ce552b1e6ef74fe` | som den er |
| `fase3/avbrudd-2026-09-29/determinisme.json` | R-A25 | 419 | `3b66fa5e1284b20f70e591abdeb2314adc0dc95e658f5b01c8bab6cd64e02591` | som den er |
| `fase3/lisens-per-verk-fase3.json` | R-A25 | 16109 | `c5e4157da2ec0b6356e7419e7e117b276eef54f7049330b41dc55c0fd5aa7218` | som den er |
| `fase3/presisjon/oppdrag-presisjon-MAL.md` | A25, R-A25 | 3077 | `aebd975593942f892252771e3048bdce5f04a8e0ce57a77036c0e3f1faaed4cd` | som den er |
| `fase3/presisjon/sperreliste-presisjon.md` | A25, R-A25 | 506 | `cc201ac2451ba86d9165fd104810d885de1c691a35091dddbae6a32b5fa4f133` | som den er |
| `fase4/trekkresultat-fase4.json` | A26 | 527 | `74bbb6dac1bf3587862f598eb5f1375f159e38bb58a8ec7adabaf7155eb876a2` | som den er |
| `form-ruter/a1-seksjon-2026-09-26.json` | A15 | 658 | `2e2410520cbe92a3f1d603831e6da1fcb3e01775db5aa8a542df77d3036000d2` | som den er |
| `form-ruter/a2-kombinasjon-2026-09-26.json` | A15 | 449 | `2470fd78b4de273afd1ee00ff5c9df6e66a3471e3e0bb5eb014bf9b49c4254a1` | som den er |
| `form-ruter/a2-naersok-2026-09-26.json` | A15 | 5182 | `cfce3ca8cc76fe149bddd5e206cf42e88e9f09f7d69e7d97c96836e4e5585dd9` | som den er |
| `frames/frame-haandskrift-RAW.jsonl` | A26 | 405927 | `6e444a0837d6559906096b15ff6371ee6b630391d387702cc4171410225eaf75` | som den er |
| `koder4/eksponerte-rader.json` | koder 4 | 616 | `3bfcfd7b5111a8e02bd56c72041936ebdfccc2c79538e98076b84aa446237f89` | som den er |
| `koder4/folsomhet-eksponering.json` | koder 4 | 2720 | `a532490d6ab5feb2bcc7b7aeeb243918b6974beda13c3281cb6d4bc4ecbe48f3` | som den er |
| `koder4/koder4-fable51-verdikter.jsonl` | koder 4 | 42896 | `36a3465acd195355c2ad0bf5fca9d4c305c04b8cd977f9ac043a9c34d26b1798` | utdrag utelatt |
| `koder4/koder4-resultat.json` | koder 4 | 7197 | `7d685939a8531b1ba860f0039404c9d8544dd1fcaf23892adc7042aa5bbb429a` | som den er |
| `leser-lokal-ADDENDUM-24/kanari.json` | A24 | 1037 | `9ccf8eaaeffae23f7fab541f4eb713b94445d619d593d2a65ce2d069ca50cf8c` | som den er |
| `leser-lokal-ADDENDUM-24/kjoring.log` | A24 | 1128 | `12611d843891239378c27b509cae9a80ea700142e5faac7a8885f62aaba0a14e` | som den er |
| `leser-lokal-ADDENDUM-24/maaling.json` | A24 | 3519 | `34a7f259a6275a63d5b7c17b37337a6c9908348cf1e54dd566fadd9b536583e9` | som den er |
| `leser-lokal-ADDENDUM-24/parti-01.json` | A24 | 10287 | `e63f9e7c9cf51b9b9b75b547be9485e794ba9513a34d062c03d87916312e00b0` | som den er |
| `leser-lokal-ADDENDUM-24/parti-02.json` | A24 | 11251 | `5809d700be6931af05d31a903cb105961011897dbfc8bf11963ee1b31dee7887` | som den er |
| `leser-lokal-ADDENDUM-24/parti-03.json` | A24 | 10691 | `86b558d08035c4dc3e121d7965d6d30c062c01af8cb55ebf66b1a3f3fe7a2c40` | som den er |
| `leser-lokal-ADDENDUM-24/parti-04.json` | A24 | 10199 | `f0c914178edc8297cf73b34a1c5cc62de9eebea6430659625040b4075f420dbb` | som den er |
| `leser-lokal-ADDENDUM-24/parti-05.json` | A24 | 10411 | `f1c97efc447108d6a58bf875bba4fe7cf611bfa6d2547ba4c3ae3e6914c53b1f` | som den er |
| `leser-lokal-ADDENDUM-24/parti-06.json` | A24 | 11159 | `78d66e492342f56d96baf7a9a124196ff1ec2955572ebc6ef90eba7271880612` | utdrag utelatt |
| `leser-lokal-ADDENDUM-24/parti-07.json` | A24 | 10247 | `9943bdf8a590f278a9f797bd05f72ad64a4b4b22ce79eaae25825e860ae2420d` | som den er |
| `leser-lokal-ADDENDUM-24/parti-08.json` | A24 | 9525 | `dc87c772b39fe62525e85659fe312ab9a90118e4829f49fb0af60f1aea72e42b` | som den er |
| `leser-lokal-ADDENDUM-24/parti-09.json` | A24 | 11163 | `47d95c37030279551a8ecea870c2c7e1d84cb84b73c69fa9d6d0ecfb27123770` | som den er |
| `leser-lokal-ADDENDUM-24/parti-10.json` | A24 | 11048 | `04fcb6e70aa343af52f46b01592f9560ace6efd6eafe25ff1b94bc0126afedc8` | som den er |
| `leser-lokal-ADDENDUM-24/parti-11.json` | A24 | 10048 | `99ccf91ab1c5d506539d88407d64980ced46c66ef3c2a8e607bf313f8559bb50` | som den er |
| `leser-lokal-ADDENDUM-24/parti-12.json` | A24 | 9430 | `3d83c078be5e6ed8649f5bfca41f1c566bf0c9a490c78e14a77b86e1f943aa47` | som den er |
| `leser-lokal-ADDENDUM-24/parti-13.json` | A24 | 10108 | `93a63cd1cdad3f8011503969a93b08c7e80cd92bace3f904f8be0a30bb3ebb4c` | som den er |
| `leser-lokal-ADDENDUM-24/parti-14.json` | A24 | 9582 | `f2b5d6fa8b5a05e54a8d8c6fb49d0d18c181bce9b037b3ecf5c661a769cb435e` | som den er |
| `leser-lokal-ADDENDUM-24/parti-15.json` | A24 | 10218 | `ed2a93cd329fe8234426adcdf774be611edf6f780e9b06a88437440fd5f9fabd` | som den er |
| `leser-lokal-ADDENDUM-24/parti-16.json` | A24 | 9734 | `bd5721f86d8a4274e906f417758dec5bad9cddf493e120e96384fcbd5763f711` | som den er |
| `logs/coverage-addendum01.json` | A01 | 1344 | `6c03aeb5a1b60e9c5bef3940e45618157b0b6df2f3aa099e5fabf2563dd4cc73` | som den er |
| `logs/frame-diagnostics.json` | A02 | 2178 | `0c8b8687348f95cee4c14f5ab3a9ed238ffb0aca1586f9831285f89d1ec7beb5` | som den er |
| `logs/has_fulltext-per-aar.json` | A01 | 2269 | `78ba0107ded9dafc1e376ae67e56c9e25a33e5f2d60cf8f505d691f6c0a55217` | som den er |
| `logs/kontroll-tekstvitenskap-H1-2026-09-13.json` | A08 | 3358 | `5075b278eae7c4d05850e9a3d66da2ec5ca4d6639853704fd9efe33d775c0372` | som den er |
| `logs/kontrollkandidater.json` | A02 | 48800 | `0976e0434c614197d8d4af64e63b446b2e1e25a240d3a1146191de5245adab6b` | som den er |
| `logs/kvotedogn-2026-09-13-punkt4-logg.jsonl` | A08 | 11421 | `78003747c758e0150b7b78bcfe5e6cc324bbd7b8fdc6116bab1b2dca7d483b8e` | som den er |
| `logs/leste-kontrollkandidater.json` | A02 | 121270 | `cdea66e6d3a5da693487904a24cd3c8c8b448341aa35d3118b1d0fa77308a768` | som den er |
| `logs/nedlastbarhet.json` | A03 | 32266 | `9307aabda1c138c19deae24d4bb9c56c90bf6c7439d2c0adb22bd0ee730e8f9c` | som den er |
| `logs/pipeline-test/l4-dekning-PIPELINETEST.json` | A06 | 6168 | `f73329b6f9c476dfe7d3aaa2a9ae6e1e80becc73bb1e124da182f390df10f909` | som den er |
| `logs/pipeline-test/reparse-tall-ADDENDUM07.json` | A07 | 2837 | `e667315d71f0bcf33721081cf96e2aaabf0a5b5993aa1522e55ac2ab0cc79856` | som den er |
| `logs/pipeline-test/summary-PIPELINETEST.json` | A06 | 1134 | `4983487d5f9dbfb28de490875ef433425cf2ffe6a40a8866faae918726e27c2a` | som den er |
| `logs/rammeprove-energimodellering-sammendrag.json` | A04, A08 | 5050 | `7e1b6b0e1799218d54ca49a835f6d9fde2a3e8b63bd04271be43d2fa42fd3fcd` | som den er |
| `logs/recall-sett-meta.json` | A06 | 5863 | `c9fbe5f4c99cc4fd1419fb650303b3d3dbd4cdd696d0d285d3db35f617aeda9d` | som den er |
| `logs/substitusjon.json` | A03 | 1705 | `2a303406c32086cd7acf5027323913557749f74bbbffc2bcb665f2f74f86b7f9` | som den er |
| `presisjonssett-2026-09-20/presisjon-resultater.json` | PREREG-v1 | 15631 | `be5d5e66085059e9e1445f3ad8aa7393d6eff52c776d655bdcfe402861b20447` | som den er |
| `presisjonssett/port-presisjonssett-verdikter.jsonl` | PREREG,A10 | 60440 | `5bc261953f5b9e3cfefac3c22f1182567e6f096ced6d25735eb9a7a5bfb1b5de` | utdrag utelatt |
| `raw/kand-tv3-H1-gruppe1del0-9c8d4820ed97.json` | A08 | 9042 | `9c8d4820ed97145575b5382019a880031cc315d3dcba2299a4360c968bc4b4dd` | som den er |
| `triage-loftbare-2026-09-26-kriterium.py` | A12 | 5633 | `6c33d498c8f62bb85d7f540d8c5ed1202275bd9c74d3e84b872f477f486bd9c0` | som den er |
| `triage-loftbare-2026-09-26.json` | A12 | 105180 | `1b58c4bed2f169fe294460f0b3094e7828eebfed228e64e22adf7b922a31cd61` | utdrag utelatt |
| `utvalg/karakterisering-tekstvitenskap.json` | A04 | 1085 | `cc68fabf61a3788a692a3c3b175e3c5cf72e2378a9edf122d44022527c830467` | som den er |
| `utvalg/trekkspesifikasjon-energimodellering.jsonl` | A01 | 564 | `8e11e28f234a17a30be4051d8aebf5904c66fc436dc804248f2256eaefd70af1` | som den er |
| `utvalg/utvalg-arkeologi.jsonl` | A09 | 4906 | `5e678d4d8a7e97ff0e56565fa0075f1051597512155fc3825f33de80f3fdcb29` | som den er |
| `utvalg/utvalg-energimodellering.jsonl` | A09 | 4830 | `ba8ed6eb18e55539fe64dff703f75e8308272b321e39e64b6e934d7405e083e0` | som den er |
| `utvalg/utvalg-klinisk_epidemiologi.jsonl` | A09 | 4961 | `ca7e7a935189950b521b3de81bc2bdb1b889af603f7c4c33dd80a13b12b27b15` | som den er |
| `utvalg/utvalg-tekstvitenskap.jsonl` | A09 | 4896 | `bcf7be79be241569082b5e7d331c6e28e8973faea2f8ce9c085072db3b95318b` | som den er |
| `verksniva-2026-09-26-kriterium-v2.py` | A13 | 9052 | `d410c73419406a739921aba63d08d25e32f59e6fe83ca033baafb36660978e13` | som den er |
| `verksniva-2026-09-26-kriterium.py` | A13 | 8475 | `af4fcc0ed06d5a221c293b779ba59354f290d96be807960ef0c57e45254f9f6e` | som den er |
| `verksniva-blindverk-NOKKEL.json` | A13 | 1609 | `52eadee74d8baade729e3a98c524d61c650e0a28543ffcc865e5cae300309019` | som den er |
| `verksniva-blindverk-VERDIKTER.json` | A13 | 1655 | `adb75c3491d75a64ead84f864560f0f1e2b71fbd634c5869233e27b20152814e` | utdrag utelatt |

## 9 Koden

Skriptene bak ADDENDUM-19, 19b og 20 lå aldri i git. De er gjenvunnet fra øktutskriften og ligger i
`gjenvunnet/addendum-19/` med opphav og autentisitetsgrunnlag (`OPPHAV.md`); v0.6.0 bærer dem i `gjenvunnet-kode.zip`.
Kriterieskriptene for ADDENDUM-12 og -13 lå bare på Vault og er med i `maalefiler.zip`.

## 10 Det som ikke er sjekket

* Listen bygger på filene addenda og resultatnotater selv navngir. En måling som leste en fil uten å navngi den, er
  ikke fanget.
* De 17 stiene som alt ligger i v0.5.0 eller følger git, er talt, ikke listet her; de står med «i v0.5.0 som …» i addendumstatusen.
* v0.1.0–v0.4.1 er ikke gått gjennom fil for fil; de bærer mindre enn v0.5.0.
