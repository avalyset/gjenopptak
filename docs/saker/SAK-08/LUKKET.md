# SAK-08 — lukket på `[V]`. Klasse **H8**: modellkoden er ikke deponert noe sted.

**27.09.2026. Ingen terskel beregnet, ingen kriteriefil låst** — `[V]`-sjekken avgjorde saken først,
slik triagen forutsatte: «Uten kode: H8/H7, lukket.»

**Sak:** `W2784603861`, passasje AL-1280, feltet arkeologi, klasse **H5 regnekraft**.
**Verket:** Philip Riris, «Assessing the impact and legacy of swidden farming in neotropical
interfluvial environments through exploratory modelling of post-contact land use change»,
*The Holocene* **28**(6), 945–954, 2018. DOI `10.1177/0959683617752857`. Grønn OA: den aksepterte
versjonen ligger åpent i Bournemouth University Research Online.

## Det ugjorte, ordrett fra artikkelen

> «Two sets of runs were carried out separately due to prohibitively long processing times for large
> numbers of continuously measured runs. The first set measured the end state of the landscape and
> isodes over 100 repetitions of each parameter combination (4500 runs), while the second set
> measured model outputs diachronically over just 30 repetitions of each parameter combination
> (1350 runs).»

Hindringen er navngitt i samme setning: **prosesseringstiden**. Klassen er H5, og aksen er regnekraft,
ikke AI.

**Hva som ville opphevet den, presist.** Begge settene dekker de samme **45 parameterkombinasjoner**
(4500 / 100 = 45, og 1350 / 30 = 45 — en indre kontroll som holder). Det ugjorte er altså ikke flere
kombinasjoner, men å måle **alle 4500 kjøringene diakront** i stedet for bare 1350, det vil si
**3,33 ganger flere kontinuerlig målte kjøringer**. Modellen er en koplet agentbasert modell og
cellulær automat i **NetLogo 6.0.1** over en terrengmodell på **609 × 426 celler** av Cuao-nedbørfeltet
(3 568 km², nedskalert fra 90 m), 800 tidssteg = 400 år per kjøring.

## `[V]`-sjekken: kode og data for modellen. **Faller.**

Slått opp **27.09.2026**. Triagen navnga fire ruter; jeg sjekket dem og to til.

| rute | utfall |
|---|---|
| artikkelens egen datatilgang (akseptert versjon, 59 634 tegn) | **ingen** datatilgjengelighetserklæring. 0 treff på «data availab*», 0 på «model code», 0 på github/osf.io/comses/zenodo/figshare/dryad. `NetLogo` nevnes 3 ganger, alle som programvarereferanse (Wilensky 1999), aldri som deponert fil |
| Bournemouth eprints, post `33470` | **én fil**: `/33470/7/Riris_2018_accepted.pdf`. Ingen tilleggsmateriale, ingen `.nlogo` |
| CoMSES Computational Model Library | **ingen modell** av Riris. Søket ga seks urelaterte kodebaser |
| GitHub | ingen forfatterkonto med repoer (`priris`, `philipriris` finnes ikke; `riris` har 0 repoer). Emnesøk på `Piaroa` og `Cuao` gir bare urelaterte treff |
| **Crossref, i tillegg** | DOI-en har **ingen registrerte relasjoner** — ingen komponent-DOI, ingen datasett-relasjon, intet tilleggsmateriale |
| **ORCID, i tillegg** | `0000-0003-4244-7495` (Philip Riris), 18 verk, **ingen `DATA_SET` og ingen `SOFTWARE`**. Artikkelen er registrert som `journal-article` alene |

### Den ene ruten jeg ikke fikk lest, ført som uavklart

Forlagets egen side, `journals.sagepub.com/doi/10.1177/0959683617752857` og `/doi/suppl/…`, svarte
**HTTP 403** med en botport («Just a moment…»). **Jeg omgikk den ikke.** Om den publiserte versjonen
har tilleggsmateriale, er derfor ikke avklart av meg. Det svekker `[V]`-konklusjonen på ett punkt, og
det står her i stedet for å bli utelatt. To ting taler for at det ikke finnes: Crossref registrerer
ingen komponenter for DOI-en, og OpenAlex kjenner ingen annen lokasjon enn Bournemouth-PDF-en
(`best_oa_location`, `oa_status: green`, fra rammelisten, ingen nye kreditter brukt).

## Saken feiler også sin egen forutsetning — uavhengig av 403-en

Kriteriet i triagen har et steg (1) før alt annet: **«reproduser artikkelens rapporterte tall for de
to separate settene før noe nytt kjøres (PS-246-mønsteret)».** Det steget kan ikke utføres uten
modellen. Å bygge en koplet ABM/CA på nytt fra en tisiders artikkel gir **en annen modell**, og dens
tall ville ikke reprodusere forfatterens — de ville erstatte dem. Da måler man ikke om hindringen
kunne løftes; man måler en nyskrevet modell mot en publisert tabell.

Det er nettopp skillet PS-246 holdt: der ble kildens tabell 3 reprodusert ledd for ledd **før**
avhandlingens data ble rørt. Uten den muligheten er det ingen sak, bare en ny studie.

**Derfor stopper saken selv om 403-en skulle skjule en `.nlogo`-fil:** en modellfil uten
terrengmodellen (609 × 426 celler, avledet av 90 m-data) og uten parametersveipets oppsett ville
fortsatt ikke la steg (1) kjøres. Begge deler måtte finnes, og ingen av dem er funnet.

## Klassifisering

| | før | nå |
|---|---|---|
| kodet klasse fra teksten | `H5` | uendret — teksten har ikke endret seg |
| datert vurdering (ADR-0010) | — | **H8**, `loftbar: nei`, 27.09.2026 |

Grunnen er den samme formen som Heron og SAK-09c: **tilgangssituasjonen ligger utenfor materialet.**
Her er den ikke permanent slik samtykket i SAK-09c er — en forfatter kan deponere kode i morgen, og
da er saken løftbar igjen. Derfor er dette en **utløser**, ikke en endelig lukking: dukker modellen
opp på CoMSES, GitHub, Zenodo eller i ORCID-posten, kan saken gjenåpnes med kriteriet uendret.

`cites_coverage` står som `«ikke målt»`, ikke 0.

## Hva som ikke ble gjort, og bevisst ikke ble gjort

* **Ingen e-post til noen.** Ingen forespørsel til forfatteren om modellfilen, selv om det er den
  åpenbare veien videre. Det er eierens valg, ikke mitt.
* **Ingen omgåelse av botporten** hos forlaget. 403 er ført som 403.
* **Ingen reimplementering** av modellen, av grunnen over.
* **Ingen kriteriefil låst**, og ingen kanon-bundle utløst.
* **Ingen nye OpenAlex-kreditter.** Lokasjonsopplysningen er lest av den frosne rammelisten.
