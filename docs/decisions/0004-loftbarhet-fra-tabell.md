# ADR-0004 — Løftbarhet avledes fra tabellen, aldri fra en modell

**Repo:** gjenopptak
**Status:** Accepted (endret av ADR-0010: løftbarhet er datert)
**Dato:** 2026-09-12

## Kontekst

To spørsmål lot seg lett blande sammen i implementasjonen:

1. Hvilken hindring navngir forfatteren? (H1–H9, N1–N3)
2. Er den hindringen løftbar av AI i dag?

Spørsmål 1 er en lesning av en setning. Spørsmål 2 er en påstand om verden i 2026. Ble begge
overlatt til samme modell, ville modellen både lese teksten og avgjøre sin egen relevans — og et
funn om at «AI kan løfte dette» ville da delvis være modellens vurdering av seg selv. Terskelen i
PREREG-v1 §6 og hele falsifiseringstesten i §8 ville hvilt på et sirkulært ledd.

PREREG-v1 §5 låser derfor løftbarhet i en tabell, fastsatt før data: ja / ja, med forbehold /
delvis / nei, per klasse.

## Beslutning

- Løftbarhet er en **ren oppslagsfunksjon** fra hindringsklasse til den låste verdien i
  PREREG-v1 §5. Tabellen ligger som data i `src/gjenopptak/classify/`, med en test som sammenligner
  den mot teksten i PREREG-v1 §5 og feiler ved avvik.
- En modell kan foreslå **klasse** (H1–H9, N1–N3). En modell kan aldri sette, overstyre, nyansere
  eller kommentere løftbarhetsverdien. Feltet `liftable` skrives kun av oppslaget.
- Ingen ledetekst nevner løftbarhet, slik at klassevalget ikke kan dras mot en ønsket konklusjon.
- Endres tabellen etter lås, skjer det som ADDENDUM-NN med egen sha256, og alle berørte
  oppføringer merkes med hvilken tabellversjon som gjaldt (`liftability_table_version`).
- Er klassen usikker, er løftbarheten usikker. Usikre føres i egen kolonne, jf. PREREG-v1 §2, og
  tvinges ikke til en verdi.

## Konsekvens

- Uenighet om løftbarhet blir uenighet om tabellen — en diskusjon om et dokument som er datert og
  hashet — ikke en diskusjon om hva en modell svarte en gitt dag.
- Tallet «andel treff som er løftbare» er fullt determinert av klassefordelingen. Det er
  hensikten: det som måles er lesningen, ikke en modellvurdering av AI-evner.
- H7–H9 er `nei` ved konstruksjon. Andelen H7–H9 er dermed det direkte tallet på hva verktøyet
  ikke kan love, jf. PREREG-v1 §5.
- Blir en hindring reelt løftbar senere (f.eks. H5 fra `delvis` til `ja`), er det et ADDENDUM og et
  nytt tabellversjonsnummer, ikke en stille endring i kode.
