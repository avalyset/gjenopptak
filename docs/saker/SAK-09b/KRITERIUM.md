# SAK-09b — kriterium, låst før beregning

**Sak:** Aragao 2018, `W7133020405`, passasje **AL-0852**, klasse **H5 verktøygrense**.
**Skrevet:** 2026-09-27, **før noe er beregnet.** Kriteriet er ordrett fra
`docs/SAKBEHANDLING-2026-09-27-triage.md`; tersklene er uendret.
Samme verk som SAK-09c, som ble lukket på `[V]` — denne saken rammes ikke av det, fordi den trenger
matrisene, og de står i avhandlingen.

## Det ugjorte, ordrett fra avhandlingen

> «The way EUCONNs are represented in 𝑀 makes it quite difficult to guarantee that the blockmodeling
> algorithm in Pajek will create an equal number of partitions for the nodes of the intermediate mode
> (construction activities), which should be ambiguously represented in rows and columns.
> **In addition, Pajek does not offer a practical option to force that to happen.** To avoid the
> problem above with the restricted matrix 𝑀 and to guarantee that the blockmodeling algorithm in
> Pajek will not combine the nodes of different categories in the same clusters, we propose using the
> augmented one-mode adjacency matrix, and to establish appropriate constraints.»

Hindringen er navngitt i samme setning: **verktøyet**. Forfatteren omgikk den ved å bruke den
utvidede én-modus-matrisen i stedet for den begrensede 𝑀. Det ugjorte er å gjøre det på 𝑀 med tvungen
lik partisjonering av mellomnivået.

## Kriteriet, ordrett fra triagen

> Kriterium: **reproduser avhandlingens Pajek-resultat først; kjør med tvungen partisjonering;
> opphevet hvis kjøringen gir like partisjoner; resultat: endres blokkstrukturen, rapportert.**

## Presiseringer som trengs for å kunne kjøre det, fastsatt nå

1. **«Avhandlingens Pajek-resultat»** er den generaliserte blokkmodelleringen av grunnlinje-nettverket
   (spørreundersøkelsen) i § 8.6 og figur 8.2: **12 klynger, 109 beskrankninger, total feil 14**, og
   Pajek ga **10 løsninger med samme sluttfeil**, der forfatterne valgte én manuelt. **Reprodusert
   betyr: samme total feil, 14.** Den valgte partisjonen er *ikke* reproduksjonsmål, siden valget
   blant de ti var manuelt og ikke er en egenskap ved algoritmen.
2. **To delkontroller må bestå før (1) i det hele tatt prøves**, og de er begge mot tall
   avhandlingen selv oppgir:
   * **matriseparsingen:** de fem nabomatrisene (prosjekt A, B, C, samlet case, undersøkelsen) leses
     fra tekstlaget og må reprodusere **tabell D.1 eksakt** — antall bånd, gjennomsnittsgrad og
     tetthet for hver av de fire case-nettverkene.
   * **beskrankningssettet:** det rekonstrueres fra reglene i vedlegg H, som er avkuttet med
     ellipser, og **antallet må bli 109.**
   Feiler én av dem, **stopper saken** etter oppdragets steg 3, og grunnen føres. Det er ikke et
   negativt resultat; det er en manglende forutsetning.
3. **«Tvungen partisjonering»** betyr: generalisert blokkmodellering av den **begrensede** matrisen 𝑀
   (ligning 8.2), der mellomnivåets 13 noder — byggeaktivitetene, som står både i rader og kolonner —
   tvinges til **samme** partisjon på begge akser. Operasjonelt: én klyngevektor for mellomnivået
   brukes på både rad- og kolonneaksen, i stedet for at algoritmen finner én for hver.
4. **«Like partisjoner» måles eksakt, ikke i antall.** Rad- og kolonnepartisjonen av mellomnivået må
   være **identiske som mengdepartisjoner** over de 13 aktivitetene, sammenlignet
   medlemskapsvektor mot medlemskapsvektor. Lik *klyngetall* uten lik *inndeling* er ikke oppfylt.
5. **Verktøyet er R-pakken `blockmodeling`**, versjon ≥ 0.3.1. **Kan den ikke kjøres på maskinen, er
   saken ikke kjørt — ikke ikke-opphevet.** En verktøysvikt skal ikke kunne opptre som et resultat.
   Det føres som «ikke kjørt, grunn: …», og saken blir stående med utløser.
6. **Nodenummereringen er avhandlingens:** 1–13 byggeaktiviteter, 14–22 systemer, 23–34 faktorer.
   De fire faste aktivitetsklyngene er forfatterens funksjonelle inndeling: logistikk (6, 12, 13),
   tungt utstyr (1, 5, 9), bygningstekniske arbeider (2, 7, 11), elektromekanisk montasje
   (3, 4, 8, 10). Klynge 1–4 er aktiviteter, 5–8 systemer, 9–12 faktorer.
7. **Forskningsresultatet** er om blokkstrukturen endres, og det har **ingen terskel**: total feil for
   den tvungne løsningen, og antall av de 34 begrepene som skifter klynge sammenlignet med figur 8.2.
   **Rapporteres uansett retning, også når ingenting endres.**

## Hva som var kjent da dette ble låst

Åpenhet om utgangspunktet, slik at ingen kan tro tersklene er satt etter tallene:

* **Begge `[V]` er verifisert 27.09.2026.**
  * Matrisene: alle fem 34 × 34-binærmatriser ligger i PDF-ens **tekstlag** med nodenavn — figur
    D.1–D.4 (s. 241–243) og figur E.1 (s. 251) — og er hentbare med `pdftotext -layout`. De er
    altså ikke bilder, som jeg først antok da et søk i vedlegg A ga null treff.
  * Verktøyet: `blockmodeling` står på CRAN, nåværende versjon **1.1.8** (2025-07-25), vedlikeholdt av
    Aleš Žiberna. Arkivet viser **0.3.1, publisert 2018-06-05** — **før avhandlingen ble levert
    (2018-11)**. Triagens merknad står: dette er **verktøyvalg, ikke tidsakse.**
* **Tre tall fra avhandlingen er lest før låsingen, og de er reproduksjonsmål, ikke terskler:**
  tabell D.1 (bånd 148/146/133/249, gjennomsnittsgrad 4,353/4,294/3,912/7,324, tetthet
  0,132/0,130/0,119/0,222), **109 beskrankninger**, **total feil 14**.
* **Én beregning er gjort før låsingen, og den føres her:** beskrankningsreglene i vedlegg H ble
  summert til 13 + 36 + 48 + 12 = **109**, som stemmer med avhandlingens tall. Det var nødvendig for
  å avgjøre om vedlegg H er tilstrekkelig når listen er avkuttet — altså en del av `[V]`. Ingen
  matrise er parset, og ingen blokkmodell er kjørt.
* **Ett avvik i avhandlingen er sett og ikke ryddet bort:** prosaen i vedlegg H sier klyngene ikke
  skal ha «more than four nodes», mens de oppførte beskrankningene er `6 50 3 z`, altså **høyst tre**.
  Hvilken som gjelder, avgjøres av reproduksjonen: den varianten som gir total feil 14, er den
  forfatteren kjørte. **Begge prøves, og utfallet føres** — dette er ikke en frihet til å velge det
  som passer, men en test med ett riktig svar.
* **R er ikke installert på maskinen.** Det er kjent før låsingen og er grunnen til presisering 5.

## Dødsbetingelser

* **Tersklene flyttes ikke.** «Like partisjoner» er eksakt likhet, ikke likt antall.
* **Negativt utfall føres likt.** Presisering 7 har ingen terskel og rapporteres også når
  blokkstrukturen er uendret.
* **Ingen e-post til noen**, og ingen forespørsel om materiale.
* **Ingen Anthropics API.** Bare lokal ollama og underinstans på Max.
* **Klarer jeg ikke å reprodusere avhandlingens egne tall, stopper saken** og grunnen føres.
* **Ingen verktøysvikt forkledd som resultat**, jf. presisering 5.
