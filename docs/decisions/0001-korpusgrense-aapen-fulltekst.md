# ADR-0001 — Korpusgrense: åpen fulltekst

**Repo:** gjenopptak
**Status:** Accepted
**Dato:** 2026-09-12

## Kontekst

Prosjektet trengte maskinlesbar fulltekst for å kunne skanne hele artikkelteksten, ikke bare
sammendrag eller metadata. Tre veier forelå: lisensiert fulltekst fra forlag, PDF-skraping fra
vilkårlige kilder, og åpen fulltekst via aggregatorer. De to første ga hverken reproduserbarhet
for tredjepart eller en juridisk holdbar delingsvei for korpuslisten.

Målingen som ble preregistrert i PREREG-v1 §4 gjelder prevalens i et formålsvalgt utvalg, ikke
i litteraturen. Dekningen i OpenAlex ble målt til 52 249 064 av 326 944 662 works med
`has_fulltext: true`, altså 16 %. Skjevheten var kjent på forhånd: mot nyere arbeider, mot
engelsk, mot open access. Humaniora publiserer i monografi og var tynnest dekket — samtidig som
ett av de fire feltene i utvalget er historisk tekstvitenskap.

## Beslutning

Korpuset er åpen fulltekst, og bare åpen fulltekst.

- Rammekilde for utvalg og metadata: OpenAlex, felt `has_fulltext: true`.
- Fulltekst hentes bare der lisensen tillater maskinlesning og lokal lagring: JATS-XML og
  tilsvarende strukturert fulltekst fra åpne kilder (PMC OA-delmengden, Europe PMC, DOAJ-ledd,
  forlagsleverte OA-filer med CC-lisens). Lisensfeltet loggføres per dokument.
- Ingen forsering av betalingsmur, ingen skraping av kilder som forbyr det i vilkår eller
  robots-regler, ingen manuell nedlasting utenfor kjeden.
- Dokumenter uten lisens som tillater lagring, utelates og telles som utelatt med grunn. De blir
  ikke erstattet av et nytt trekk, fordi erstatning ville gjort trekket avhengig av lisens.
- Rådata lagres urørt under `data/raw/` med MANIFEST.md (filnavn, bytes, sha256, kilde-URL,
  hentetidspunkt) og committes aldri.

## Konsekvens

- 16 %-dekningen og dens skjevhet er en **oppgitt designgrense**, ikke et forbehold i en fotnote.
  Den står i all rapportering, sammen med formuleringen fra PREREG-v1 §4: verktøyet sveiper åpen
  fulltekst, ikke litteraturen.
- Dekningen oppgis per felt, ikke bare samlet. Et felt med dårlig dekning skal ikke kunne
  framstå som et felt med lav prevalens.
- Historisk tekstvitenskap vil sannsynligvis ha lavest dekning av de fire feltene. Det svekker
  utsagnskraften om det feltet og påvirker ikke hovedspørsmålet, som er om klassen finnes på
  tvers av fag.
- Falsifiseringstesten i PREREG-v1 §8 arver samme grense: siteringsgrafen kan bare sjekkes der
  siterende arbeid har tilgjengelig fulltekst. Dekningsgraden rapporteres derfor per felt der òg.
- Korpuslisten (ID-er, lisenser, sha256) kan deles fritt; fulltekstene kan ikke.

## Tillegg 2026-09-28: rammen og substitusjonsregelen er endret av ADDENDUM-01

Den opprinnelige teksten står uendret. To punkter i den gjelder ikke lenger:

* **Rammen er ikke `has_fulltext: true`.** ADDENDUM-01 § 2 forkaster `has_fulltext` som utvalgsramme
  (en indekseringsramme, ikke en hentbarhetsramme); rammen er åpen tilgang pluss hentbarhet
  (ADDENDUM-01, ADDENDUM-04, `docs/METODE.md` § 6).
* **Lisens utløser substitusjon.** ADDENDUM-01 § 6 punkt 2–3 gjør `lisens` til en av fem utløsende
  årsaker for erstatning fra reservelisten for samme felt — det motsatte av «blir ikke erstattet» over.
* **Lisensvilkåret er i praksis «åpen og hentbar».** 21 av de 60 verkene i kandidatregisteret har ingen
  brukbar lisensangivelse (17 uten oppgitt lisens, 4 `other-oa`), og fulltekstene deres er likevel lagret
  på volumet (`docs/LISENSAUDIT-2026-09-28.md` § 1). De deponeres ikke.
