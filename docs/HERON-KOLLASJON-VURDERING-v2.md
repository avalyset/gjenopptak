# Heron-kollasjonen — kan den gjøres? (v2, 2026-09-26)

**Erstatter v1** (`docs/HERON-KOLLASJON-VURDERING-v1.md`, 2026-09-25), som blir stående merket
superseded. v1 konkluderte på BLs status alene. v2 legger til kartleggingen utenfor BL, som v1 selv
førte som åpen post, og **snur begrunnelsen: hindringen er ikke at materialet mangler, men at de
filene som finnes, er utenfor rekkevidde.**

Verket: W3000588547 = 10.5525/gla.thesis.76774, **Francesco Grillo**, *Hero of Alexandria's
Automata: a critical edition and translation*, PhD, Glasgow 2019. Klassen sto H1 i 2019 (tidsrammen),
H8 fra oktober 2023 (tilgang). Ingen bilder lastet ned. Ingen bestilling gjort.

## 1 Håndskriftene, nå med Pinakes-identitet

| | **Bd** | **Ha** | **Hb** |
|---|---|---|---|
| signatur | British Library, **Burney MS 108** | **Harley MS 5589** | **Harley MS 5605** |
| **Diktyon / Pinakes** | **39371** | **39548** | **39564** |
| Pinakes-URL | `pinakes.irht.cnrs.fr/notices/cote/39371/` | `…/39548/` | `…/39564/` |
| *Automata* i Pinakes | ff. 081v–100 | ff. 019–32v* | ff. 50v–69 |
| *Automata* i avhandlingen | ff. 81v–100r | ff. 19r–27r | ff. 50v–69r |
| datering (avhandlingen) | saec. XVI¹ᐟ⁴ | saec. XVI³ᐟ⁴ | saec. XVI²⁻³ᐟ⁴ |
| sider | 38 | 17 | 38 |
| kopist | — | — | **Ioannes Mauromates** (Pinakes; RGK I 171 iflg. BLs post) |

**Foliotallene stemmer mellom Pinakes og avhandlingen.** Pinakes oppgir hele *Automata*-delen i
Harley 5589 (ff. 19–32v) mot avhandlingens ff. 19r–27r; avhandlingen angir teksten fram til der den
slutter, Pinakes hele avsnittet. Ingen motsigelse.

Avhandlingens sigla-liste, ordrett: `Burneianus gr. 108, saec. XVI¹ᐟ⁴, ff. 81v-100r = Bd*` ·
`Harleianus 5589, saec. XVI3/4, ff. 19r-27r = Ha**` · `Harleianus 5605, saec. XVI2-3/4, ff. 50v-69r
= Hb**`. Asteriskene angir **tittelform**, ikke tilgangsmåte (`*` = Περὶ αὐτοματοποιητικῆς,
`**` = Περὶ αὐτοματοποιητικῶν).

## 2 De tre hadde aldri et IIIF-manifest

De arkiverte BL-katalogsidene for alle tre inneholder **0 forekomster** av `IIIF`, `manifest`,
`ark:` og `vdc_`, og **1 forekomst** av `Proxy.ashx?src=…_files/…jpg`. Bildene lå på BLs **gamle
DeepZoom-flisrute**, ikke på IIIF-API-et `api.bl.uk` (som i dag ikke engang har DNS-oppslag).

To følger av dette, og de er begge nye i v2:

1. **Ingen IIIF-aggregator kan noensinne ha speilet dem.** Biblissima, StruViMan og liknende
   indekserer manifester; her fantes ingen.
2. **De står utenfor den IIIF-baserte gjenopprettingen.** BL har lagt over 2 000 digitaliserte
   håndskrifter tilbake i en IIIF-viser (`iiif.bl.uk/uv/` svarer 200). Våre tre kan ikke komme
   tilbake den veien uten at materialet først publiseres på nytt som IIIF.

## 3 Wayback: åtte hjørnefliser

| håndskrift | fangster | folier | nivå/flis |
|---|---|---|---|
| Burney 108 | 8 | f001r, f024v, f027r, **f081v** | 7 / 0_0 |
| Harley 5589 | 2 | f001r, **f019r** | 7 / 0_0 |
| Harley 5605 | 2 | f003r, **f050v** | 7 / 0_0 |

De arkiverte foliene er nøyaktig de som sto som lenker på katalogsiden — seksjonsstartene, inkludert
starten på *Automata* i alle tre. Crawleren tok **én flis** per foli: nivå 7, flis 0_0, altså
øverste venstre hjørne. **Det beviser at digitaliseringen fantes, og kan ikke leses.** Ingen fangst
av selve visersidene.

## 4 ARCA (IRHT): poster finnes, men reproduksjonen er BLs egen

ARCA er etterfølgeren til Médium, IRHTs reproduksjonskatalog. Fritekstsøket er nede; **cote-søket
virker**, og det er der funnene kom.

| | post | reproduksjonsrad |
|---|---|---|
| Burney 108 | `ark:/63955/md88cf95nc41`, Medium 100062805 | «Facsimilé (London-BL)»: objet **intégral** · procédé **numérique** · avancement **FAIT (site externe)** |
| Harley 5605 | `ark:/63955/md88cf95nc5m`, Medium 100063014, «HERON ALEXANDRINUS» | samme |
| Harley 5589 | **ingen post** | — |

**Kontroll som gjør raden meningsfull:** BnF Latin 5605 (`ark:/63955/md52w3766w1z`) har **ingen
reproduksjonsblokk i det hele tatt**. ARCA fører altså reproduksjonssett når de finnes — og for våre
to fører den ett, nemlig **BLs egen, komplette, digitale, hostet eksternt**. IRHT har ingen
uavhengig film. Posten sier dessuten: «Images non libres de droit. Demandes de reproduction à
adresser à l'institution de conservation.»

**Armering:** cote-søket på «5605» ga BnF Latin 5605 (kontroll) **og** BL Harley 5605; London + «108»
ga to treff (Burney 108, Harley 108) mens London + «5589» ga null. Nullen på 5589 er ekte.

## 5 Dumbarton Oaks: ekte nullresultat

Manuscripts-on-Microfilm Database, ~2 000 filmruller.

| søk | mmdb-poster |
|---|---|
| **kontroll** «Add. 36749» | 1 (`/resources/mmdb/manuscripts/1240`) |
| **kontroll** «Harley» | 10, blant dem Harley 3318, 5624, 6295, 6299 |
| **kontroll** «Burney» | 2 (Burney 75, Burney 92) |
| «Harley 5605» | **0** |
| «Harley 5589» | **0** |
| «Burney 108» | **0** |

Kontrollene traff, og de traff på **samme fonds** som våre tre. Dette er et ekte nullresultat:
Dumbarton Oaks har ingen film av noen av de tre.

## 6 RGK: null i tekstbindene, plansjebindet utestet

Repertorium der griechischen Kopisten 800–1600, søkt inne i `archive.org/details/rgk_20211230`.

| bind | kontroll | søk på våre |
|---|---|---|
| **1a** Großbritannien | «Harl» 104 · «Burn» 36 · «Kopisten» 91 | «5605» 0 · «5589» 0 · «Mauro» 0 · «Μαυρομάτης» 0 |
| **2a** Frankreich + *Nachträge GB* | «Paris» 59 (navnesøk armert); «Harl» 0 (signatursøk upålitelig) | «Mauro» 0 · «5605» 0 |
| **3a** Rom/Vatikan | «Vat» 1578 · «Kopisten» 35 | «Mauro» 0 |
| **1c Tafeln (plansjer)** | «Kopist» 0 · «Lond» 0 · «Tafel» 0 → **indeksen virker ikke** | **UTESTET** |

Nullene i 1a, 2a og 3a er armerte. **1c er stedet der en plansje av Mauromates' hånd ville ligget,
og det er nettopp der søket ikke kan brukes.** Det er en åpen tråd, ikke et fravær.

## 7 Schmidt 1899 kollasjonerte ingen av dem

Sigla for *Automata* (s. 412): **A** = Marcianus 516 · **G** = Gudianus 19 · **M** = Magliabecchianus
I.II.36 · **T** = Taurinensis B.V.20 (1541) · a = consensus AGT. (For *Pneumatica*, s. 76, også
**P** = Parisinus 2515.)

Søk inne i utgaven: **«Harleianus» 0 treff · «Musei Britannici» 0 treff · «Burneianus» 2 treff**, og
det ene er en apparatnote på s. 292 som leser «… κάτω **Burneianus** 81 in …» — altså **Burney 81 i
*Pneumatica*-apparatet, ikke Burney 108**.

**Ingen trykt kollasjon finnes å bruke i stedet for håndskriftene.** Det er samtidig grunnen til at
kollasjonen ville vært ny. **Senere utgaver er ikke kontrollert — utestet.**

## 8 Biblissima: utenfor omfanget, og frasesøket duger ikke

Biblissimas IIIF Collections (~144 000 manifester) indekserer **én** BL-samling: **«The British
Library, Polonsky Pre-1200 Project»**. Den dekker håndskrifter før 1200; våre tre er 1500-talls og
kan ikke ligge der.

**Frasesøket er ubrukelig og nullene derfra teller ikke:** `"Harley 5605"` gir 0, men **kontrollene
`"Harley 603"`, `"Harley 2506"` og `"Burney 19"` gir også 0.** Konklusjonen over hviler på
samlingsomfanget, ikke på frasesøket.

## 9 Utestet fordi kilden svarte feil — ikke fravær

| kilde | hva som skjedde |
|---|---|
| **ARCAs fritekstsøk** | «INTERNAL ERROR» på målsøk **og** kontroll («Marcianus 516») |
| **BL-katalogens `Surrogates`-fasett** | **HTTP 500 også på kontrollen** (fasetten alene, uten spørring) — **andre gang** |
| **RGK 1c (plansjer)** | indeksen svarer 0 på ord som må finnes |
| **Cataldi Palau 2000**, «Il copista Ioannes Mauromates», Atti del V Colloquio (Cremona 1998), Firenze 2000, s. 335–399 | plansjelisten lot seg ikke se; verket er ikke på Internet Archive. Pinakes siterer s. 376 for Harley 5605 |
| **Giacomelli 2019**, «I libri greci di Matteo Macigni», s. 403 | Pinakes' referanse for Burney 108; plansjer ikke undersøkt |

## 10 Ikke søkt — sagt rett ut

München (Institut für Griechische und Lateinische Philologie / Kommission für Byzantinistik), Hill
Museum & Manuscript Library, Institute for Advanced Study, italienske klassiske institutter, og
britiske bibliotek som kan ha bestilt BL-film. **Ingen søk gjort.** At HMMLs partnere er østlige og
europeiske samlinger framfor BL, er en antakelse, ikke en måling. Cambridge (CUDL) har et eget
Heron-håndskrift, Trinity O.4.9 — et annet vitne, ikke et surrogat av våre.

## 11 Grillo/Ruffell-sporet: noen har hatt filene

Avhandlingens egen formulering skiller skarpt mellom leverte reproduksjoner og konsulterte bilder:

> «I have thus seen manuscripts La, Lb, Lc, Ld, Pa, Ph, Pg and Pf, and **photographic or microfilm
> reproductions** of manuscripts A, Aa, Ab, Ac, Ad, Ba, Bb, Bc, Ea, Eb, F, G, M, Mb, O, Pb, Pc, Pd,
> Pe, T, Ta, Tb and Vd. **I have also been able to consult images of Bd, Ha and Hb**, but these
> manuscripts came to my attention too late to be examined and collated for the purposes of the
> constitutio textus and the stemmatic analysis.»

**Takkeseksjonen lister tolv bibliotek som ga ham reproduksjoner, og British Library er ikke blant
dem** (0 forekomster av «British Library» i takkeblokken): Biblioteca Angelica Roma, BNC Firenze,
BNE Madrid, Marciana Venezia, BNU Torino, **Bodleian Oxford**, Det Kongelige Bibliotek København,
HAB Wolfenbüttel, ÖNB Wien, El Escorial, UB Amsterdam, Ambrosiana Milano — pluss tilgang på lesesal
ved Leiden UB og BnF.

**Slutning, og den er en slutning:** bildene av Bd, Ha og Hb var etter alt å dømme **BLs egne
Digitised Manuscripts, konsultert på nett** mens viseren var oppe. Ordvalget i avhandlingen skiller
nettopp mellom «provided me with reproductions» og «able to consult images», og BL mangler i
leverandørlisten. Dette er ikke belagt av et dokument som sier det rett ut.

**Fotnote 83, ordrett:**

> «These three manuscripts first came to my attention after my primary supervisor learned about them
> (see Ruffell 2016). Because of the tight timescale for the completion of the thesis, and because
> other in situ collations had yet to be carried out, it was decided to postpone collating Bd, Ha and
> Hb until I should be able to revise the thesis for publication (Prof. Costas Panayotakis, personal
> communication, June 14, 2017).»

Personene: forfatter **Francesco Grillo**; hovedveileder **prof. Isabel Ruffell**; prosjektet «Hero
of Alexandria and his theatrical automata» med **dr. Euan McGookin**, 2014–2017; **prof. Costas
Panayotakis** tok beslutningen om å utsette.

## 12 Konklusjon

**H8 står per 2026-09-26.** Men begrunnelsen er ny, og skarpere enn i v1:

**Hindringen er tilgang til filer som finnes, ikke fravær av materiale.** Alle tre er komplett
digitalisert — ARCA fører BLs digitalisering som «intégral … FAIT», Wayback beviser at flisene lå
ute, og avhandlingens forfatter har sett bildene. Ingen uavhengig film eksisterer noe sted som lot
seg sjekke, men det er ikke lenger det avgjørende: det avgjørende er at ferdige filer ligger hos BL
og hos minst én forsker.

**Ruter, i rekkefølge etter pris:**

1. **Forespørsel til Grillo/Ruffell.** Koster ingenting. Avhandlingen sier selv at kollasjonen skal
   gjøres «when I revise the thesis for publication», så interessen er sammenfallende.
2. **De tre utestede plansjesporene:** RGK 1c, Cataldi Palau 2000, Giacomelli 2019. Gir i beste fall
   én foli hver — nok til håndidentifikasjon, ikke til kollasjon.
3. **Bestilt digitalisering hos BL.** «Imaging services and digitisation» er oppført som tilgjengelig.
   Omfang: ~93 folier / **~186 sider**. Sikker, men koster.
4. **Lesesal med Reader Pass.** Postene finnes i interimkatalogen; bestillingsskjemaet er live.

**For registeret:** utløseren bør ikke lenger være «bildene tilbake i åpen kanal» — det er bare én
av fire ruter, og ikke den billigste.
