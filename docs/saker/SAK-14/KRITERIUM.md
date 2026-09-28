# SAK-14 — kriterium, låst før beregning

**Sak:** Haouachi 2016, `W2474595476`, klasse **H3 språkbarriere**, AI-aksen.
**Passasjer:** AL-0738, AL-2370 (samme setning i to overlappende vindu).
**Skrevet:** 2026-09-27, **før noe er beregnet.** Kriteriet er ordrett fra
`docs/SAKBEHANDLING-2026-09-27-triage.md`; tersklene er uendret.

## Det ugjorte, ordrett fra avhandlingen

> «Pour les textes grecs, nous ne donnerons que la traduction des textes grecs en raison de notre
> méconnaissance du grec.»

Det ugjorte er å lese de greske kildene i original. Hindringen er navngitt i samme setning:
forfatterens manglende gresk. Klassen er H3, løftbar «ja, med forbehold» etter PREREG-v1 §5.

## Kriteriet, ordrett fra triagen

> Kriterium til låsing: (1) alle steder i avhandlingen der en gresk kilde siteres bare i
> oversettelse listes opp med referanse; (2) for hvert sted hentes den greske teksten fra åpen kilde
> og verifiseres ved eksakt strengmatch mot kildeutgaven; (3) hindringen regnes **opphevet hvis
> ≥ 90 %** av stedene får gresk tekst med de bærende termene identifisert; (4) forskningsresultatet
> er antall steder der LSJ-glossen for den bærende termen avviker fra den franske gjengivelsen på
> den aksen avhandlingen argumenterer (kjønn, etnisitet, status) — **rapportert som N uten terskel,
> negativt utfall likt.**

## Presiseringer som trengs for å kunne kjøre det, fastsatt nå

1. **Hva «en gresk kilde» er, operasjonelt.** Avhandlingen bruker latinske forkortelser i
   versaler, ikke forfatternavn. Et sted teller når det bærer en henvisning på formen
   `<FORKORTELSE>., <VERK> <bok>, <kapittel>, <seksjon>` der forfatteren skrev på gresk. Listen over
   greske forfattere hentes fra avhandlingens egne forkortelser, ikke fra en liste jeg lager.
2. **«Eksakt strengmatch mot kildeutgaven»** betyr: den greske teksten for den oppgitte
   bok/kapittel/seksjon hentes fra Perseus, og stedet regnes truffet når referansen oppløses til en
   eksisterende passasje i utgaven. Feilslått oppløsning teller som ikke truffet.
3. **«De bærende termene»** er de greske ordene som svarer til det franske uttrykket avhandlingen
   bygger sin påstand på i den setningen. De identifiseres av en lokal modell eller en
   underinstans, aldri av Anthropics API, og listen skrives før LSJ slås opp.
4. **Nevneren i (3)** er antall steder funnet i (1). Blir den 0, er saken ikke opphevet og ikke
   falt — den er **uten grunnlag**, og det føres som det.

## Hva som var kjent da dette ble låst

Åpenhet om utgangspunktet, slik at ingen kan tro tersklene er satt etter tallene:

* **[V] er verifisert.** Den greske teksten av *Antiquitates Romanae*, Books I–XX, ed. Karl Jacoby,
  er åpent hentbar på Perseus: `https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:2008.01.0572`
  (slått opp 2026-09-27; 264 greske ordformer på bok 1, kapittel 1, med Dionysios' åpningssetning
  τοὺς εἰωθότας ἀποδίδοσθαι …). **LSJ** er åpent via Logeion, `https://logeion.uchicago.edu/γυνή`
  (slått opp 2026-09-27); Perseus' eget `morph`-endepunkt svarte HTTP 503 samme dag.
* **Avhandlingen inneholder 12 greske ordformer i 964 723 tegn**, 8 unike. Det er i seg selv et
  belegg for utsagnet: greskkunnskapen mangler, og teksten bærer nesten ingen gresk.
* **Ti forekomster av «Antiquités romaines»** og ti av «traduction» er tellet. Ingen andre
  størrelser i kriteriet er beregnet.
* Avhandlingen er i portkorpuset og ligger på Vault med sha256 i manifestet, hentet frosset.

## Dødsbetingelser

* **Tersklene flyttes ikke.** 90 % i (3) står. Blir resultatet 89 %, er hindringen ikke opphevet.
* **Negativt utfall føres likt.** (4) har ingen terskel og skal rapporteres også når N = 0.
* **Ingen e-post til noen**, og ingen forespørsel om materiale.
* **Ingen Anthropics API.** Bare lokal ollama og underinstans på Max.
* Klarer jeg ikke å reprodusere det avhandlingen selv oppgir, **stopper saken** og grunnen føres.
