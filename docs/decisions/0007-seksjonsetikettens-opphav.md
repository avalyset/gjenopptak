# ADR-0007 — Seksjonsetikettens opphav: source eller parser

**Repo:** gjenopptak
**Status:** Accepted
**Dato:** 2026-09-12

## Kontekst

ADR-0002 festet at rå seksjonsetikett følger hver setning gjennom hele kjeden, og
begrunnet det med den positive kontrollen: den avgjørende setningen står i en
resultatseksjon, ikke under limitations. Det er selve metodefunnet — at et
seksjonsfilter på limitations ville mistet den — og hele kjeden er bygget rundt
å kunne vise det.

ADR-0002 forutsatte samtidig at etiketten kom fra kilden. Hentbarhetsmålingen i
ADDENDUM-01 §5 viste at forutsetningen ikke holder i to av fire felt. Europe PMC,
som leverer forlagets egen JATS, ga null treff i historisk tekstvitenskap (0 av 25
kontrollerte) og null i energisystemmodellering (0 av 48). Begge nullresultatene
ble armert med en kjent Europe PMC-artikkel som traff i samme forespørselssett, så
de er reelle: JATS-ruten finnes ikke i de feltene. *(Rettet 30.09.2026, frys-lesning 4: nullene er utvalgsnull,
ikke påvist fravær — KORRIGENDUM-2026-09-28 § D.)*

Der må teksten hentes som PDF og parses med GROBID. En GROBID-seksjon er ikke
kildens merking. Den er en parsers slutning fra sidelayout, skriftstørrelse og
posisjon — en gjetning som kan være god, men som er en gjetning. OpenAlex oppgir
selv at «a meaningful share of files will contain errors», og at skannede eller
rene bilde-PDF-er ikke kan parses i det hele tatt.

Uten et skille ville påstanden «setningen sto i en resultatseksjon» blitt
rapportert med samme vekt enten etiketten kom fra forlagets `<sec sec-type>`
eller fra en layoutgjetning. Det ville gjort hovedfunnet uetterprøvbart, og en
leser kunne ikke sett forskjellen.

## Beslutning

1. **`section_label_provenance` er et påkrevd felt** på hver setning, og følger
   setningen videre gjennom `candidates.jsonl` til `claims.jsonl`. Verdimengden er
   lukket: `source` eller `parser`. Det finnes ingen tredje verdi, ingen tom verdi,
   ingen standardverdi.

2. **`source` brukes kun når kilden selv merker seksjonen.** Det vil si strukturell
   merking i leverandørens eget format: JATS `<sec>` med `sec-type` og/eller
   `<title>`, TEI som er forlagslevert, eller tilsvarende. Kriteriet er at
   inndelingen er skrevet av den som utgav teksten, ikke utledet av oss.
   En seksjon uten tittel i JATS er fortsatt `source`: kilden har merket at her
   er en seksjon, og at den er uten tittel. Fraværet av tittel er kildens
   opplysning, ikke vår gjetning.

3. **`parser` brukes for alt GROBID-utledet** og for enhver annen etikett vi selv
   slutter oss til fra layout, skrift, posisjon eller regler. Når verdien er
   `parser`, er `parser_version` og `parser_model_version` påkrevde og ikke-tomme:
   GROBID-versjon og den konkrete modellversjonen som ga inndelingen. Mangler ett
   av dem, er oppføringen ugyldig og telles ikke — samme regel som for
   modellsignaturen i ADR-0003.

4. **Enhver påstand om hvor i teksten en setning sto, rapporteres delt på
   provenance.** Andeler, tellinger, tabeller og figurer over seksjonsfordeling
   oppgis med én kolonne for `source` og én for `parser`. **De to slås aldri
   sammen til ett tall.** Det gjelder også sammendraget: finnes bare ett samlet
   tall, er rapporten feil.

5. **Rute og opphav loggføres sammen.** `fulltext_source` og `fulltext_format`
   (ADDENDUM-01 §3.2: P1 JATS, P2 TEI, P3 PDF) står i dokumentposten, og
   provenance i setningsposten. En leser skal kunne gå fra et tall til hvilken
   rute som frambrakte det.

## Konsekvens

- Hovedfunnet blir svakere der det er svakest, og det er hensikten. Er
  `parser`-kolonnen den som bærer påstanden om resultatseksjoner, står påstanden
  og faller med GROBID, og det er synlig for enhver leser uten forklaring.
- Feltene blir ikke sammenlignbare på seksjonsfordeling. Klinisk epidemiologi vil
  ha overvekt av `source`, historisk tekstvitenskap nesten bare `parser`. En
  forskjell mellom feltene i hvor treffene står, kan derfor være en forskjell i
  parsere og ikke i skrivemåte. Det skal sies hver gang tallene stilles opp.
- Delingen kan gjøre et tall for tynt å rapportere: 4 av 25 fordelt på to
  provenance-kolonner er to tall som hver er nær støy. Da rapporteres de likevel
  delt, med n oppgitt, og ikke slått sammen for å se sterkere ut.
- Kjeden må feile på manglende provenance. En eldre `sentences.jsonl` uten feltet
  er ugyldig mot skjemaet og skal kjøres om, ikke migreres med en antatt verdi.
- ADR-0002 står uendret. Denne beslutningen legger til et felt og en
  rapporteringsregel; den fjerner ingenting, og normaliseringen er fortsatt
  additiv.
