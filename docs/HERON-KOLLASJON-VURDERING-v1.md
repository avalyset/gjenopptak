# Heron-kollasjonen — kan den gjøres? (v1, 2026-09-25)

> **SUPERSEDED 2026-09-26 av `docs/HERON-KOLLASJON-VURDERING-v2.md`.** Dette notatet står uendret
> som det ble skrevet. Det konkluderte på BLs status alene, og førte kartleggingen utenfor BL som
> åpen post. v2 gjennomførte den kartleggingen og snudde begrunnelsen: hindringen er tilgang til
> filer som finnes, ikke fravær av materiale. Klassen H8 står i begge.

Verket: W3000588547, 10.5525/gla.thesis.76774, Glasgow 2019, kritisk utgave av Herons *Automata*.
Det ugjorte står i setning 944 med fotnote 83: forfatteren fikk se bilder av Bd, Ha og Hb, men
«these manuscripts came to my attention too late to be examined and collated». Hindringen er
uttrykkelig tidsrammen: «Because of the tight timescale for the completion of the thesis … it was
decided to postpone collating Bd, Ha and Hb until I should be able to revise the thesis for
publication.» Klassen er H1 — menneskelig lesning i skala.

Vurdering, ikke forsøk. Ingen bilder lastet ned. Avhandlingens sigla-liste (§3.1) er lest fra
PDF-en på Vault; tilgjengelighet og modeller er slått opp på nett.

## 1–4. Håndskriftene

| | **Bd** | **Ha** | **Hb** |
|---|---|---|---|
| **signatur** | British Library, **Burney MS 108** | British Library, **Harley MS 5589** | British Library, **Harley MS 5605** |
| **datering** | saec. XVI¹ᐟ⁴ | saec. XVI³ᐟ⁴ | saec. XVI²⁻³ᐟ⁴ |
| **folioer med *Automata*** | ff. 81v–100r | ff. 19r–27r | ff. 50v–69r |
| **omfang i sider** | 38 | 17 | 38 |
| **digitalisert?** | Ja, men **«Images currently unavailable»** i BLs katalog | Samme | Samme |
| **åpen tilgang i dag?** | **Nei.** BL har ikke gjenopprettet bildene etter cyberangrepet i oktober 2023 | **Nei** | **Nei** |
| **oppløsning** | ukjent — viseren svarer ikke | ukjent | ukjent |
| **lisens** | katalogteksten er CC-BY (British Library Board); bildene har ingen oppgitt lisens så lenge de er utilgjengelige | samme | samme |
| **stemma** | β-grenen | γ-grenen | γ-grenen |

**Samlet omfang: 93 manuskriptsider.** Alle tre er i samme bibliotek, noe som gjør et
reproduksjonsbestillingsspor mulig i prinsippet, men BLs bildetjenester er den samme tjenesten som
falt ut i 2023.

## 3. HTR-modeller for gresk minuskel i Kraken

| modell | kilde | lisens | rapportert feilrate |
|---|---|---|---|
| **Greek HTR (9.–12. årh. minuskel)**, NFC- og NFD-normalisert | Zenodo 15838142 / 15837901, PatristicTextArchive/GreekHTR | CC-BY-SA 4.0 | **ingen oppgitt** — forhåndsutgivelse, datasettet ennå ikke publisert |
| **Vat. gr. 2228 – Medieval Greek HTR** (Kraken 7.1.1) | Zenodo 22856948 | CC-BY-SA 4.0 | 99,33 % **tegnnøyaktighet i eget materiale**; posten sier selv at dette «is not an independent performance estimate» |
| nærmeste publiserte overføringstall (Transkribus, ikke Kraken) | LT4HALA 2026, «From Manuscript to Model» | — | **5,13 % CER** på håndskriftet modellen er trent på, **27,13 % CER** på et annet 1300-tallshåndskrift |

To ting følger av tabellen. Det finnes åpne Kraken-modeller for gresk minuskel, men **ingen av dem
rapporterer en uavhengig feilrate**, og det nærmeste publiserte overføringstallet viser at en
gresk HTR-modell femdobler feilraten når den møter en annen hånd. Modellene er dessuten trent på
9.–12. og 14. århundres bokhender; våre tre er humanistiske 1500-tallshender.

## 5. Innsats og gjennomførbarhet

| | |
|---|---|
| **skaffe bilder** | Blokkert i åpen kanal. Eneste rute er bestilt reproduksjon fra BL, med ukjent leveringstid og kostnad så lenge tjenesten er delvis nede |
| **HTR med eksisterende modell** | ~93 sider, men ved forventet 25–30 % CER på ukjent hånd er utskriften ubrukelig til kollasjon: en kollasjon krever ordnøyaktige lesninger, ikke omtrentlige |
| **realistisk rute** | 20–30 sider transkribert for hånd av noen som leser 1500-talls gresk minuskel, finjustering av en åpen modell på det, så HTR på resten og kollasjon med CollateX mot utgavens tekst |
| **innsats** | 2–4 ukers spesialistarbeid *etter* at bildene foreligger |
| **gjennomførbart nå?** | **Nei** |

## Anbefaling

**Ikke forsøk kollasjonen nå.** Den faller på materialet, ikke på metoden: alle tre håndskriftene
ligger i det ene biblioteket som ikke har fått bildene sine tilbake på nesten tre år. Det som
stanser forsøket i dag, er altså ikke den hindringen forfatteren oppga — tidsrammen — men en ny
hindring som oppsto etter at avhandlingen ble levert.

Det er verdt å merke seg som funn i seg selv: et parkert spørsmål kodet H1 (menneskelig lesning i
skala, løftbar) er i praksis blitt H8 (tilgang) siden 2023. **Løftbarhetstabellen i ADR-0004 er
datert i det øyeblikket den skrives.**

Hvis bildene kommer tilbake, er dette likevel den beste kandidaten i materialet: omfanget er lite
(93 sider), teksten finnes i en moderne kritisk utgave å kollasjonere mot, stemmaposisjonene er
kjent (β mot γ), og verdien er entydig — forfatteren har selv skrevet at kollasjonen skal gjøres
før publisering.
