# ADR-0002 — Seksjonsbevaring: rå seksjonsetikett følger setningen

**Repo:** gjenopptak
**Status:** Accepted
**Dato:** 2026-09-12

## Kontekst

Nærmeste metodiske naboer — uttrekk av limitations- og future-work-seksjoner — filtrerte på
seksjon før de filtrerte på innhold. Det var billig og det var feil for vårt formål.

Den avgjørende setningen i den positive kontrollen (Hirth, Mühlenpfordt & Bulkeley 2018,
PREREG-v1 §7) står i en resultatseksjon, ikke under limitations. Hadde kjeden filtrert på
seksjonsnavn først, ville den ene artikkelen rubrikken måler seg mot falt ut før klassifisering,
og hele kontrollen vært verdiløs.

Samtidig varierer seksjonsetiketter i JATS mellom forlag og tidsskrift: `Discussion`,
`4. Discussion`, `DISCUSSION AND CONCLUSIONS`, `sec-4`, og seksjoner uten tittel. Enhver
normalisering til et fast sett kategorier er et tolkningsvalg som kan vise seg galt, og som ikke
kan angres om originalen er kastet.

## Beslutning

1. **Hele teksten skannes.** Ingen seksjonsbasert forhåndsfiltrering i noe ledd av kjeden.
2. **Rå seksjonsetikett følger hver setning gjennom hele kjeden** — parse → extract → classify →
   falsify → registry. Feltet `section_raw` bærer strengen slik den sto i kilden, uendret, inkludert
   nummerering, versaler og tom verdi. Også `section_path` (nøstingen) og `section_id` bevares rå.
3. **Normalisering er additiv.** Avledede felt (`section_norm` med et lukket sett verdier, og
   `section_norm_rule` som navngir regelen som traff) legges ved siden av. De erstatter aldri
   `section_raw`, og ingen del av kjeden leser `section_norm` uten at `section_raw` er tilgjengelig.
4. Seksjonen er et **rapporteringsfelt, ikke et filter**: hvor treffene sto, er et resultat.

## Konsekvens

- Normaliseringsreglene kan endres etter at data er samlet, og alt kan kjøres om fra `section_raw`
  uten å hente korpuset på nytt.
- Fordelingen av treff over seksjoner blir et målbart funn. Er andelen treff utenfor
  limitations-seksjoner høy, er det samtidig et tall på hva de eksisterende arbeidene i §10 mister.
- Prisen er volum: hele teksten må setningssplittes og bæres videre, med større `sentences.jsonl`
  og mer arbeid i klassifiseringen. Det er akseptert.
- Setninger uten seksjonsetikett er gyldige og går videre med tom `section_raw`. De telles for seg,
  slik at «ukjent seksjon» ikke skjules i en samlekategori.

## Tillegg 2026-09-28: belegget for seksjonsplasseringen

Setningen om at energikontrollens avgjørende setning står i en resultatseksjon, er **uverifisert**:
ADDENDUM-02, -03, -04 og -08 fører seksjonen som «fortsatt uverifisert», og teksten er ikke hentbar på
den offentlige ruten (ADDENDUM-08 § 3.2). Eksempelet med belegg er arkeologikontrollen
(10.1038/s41467-019-11357-9), der den parkerte setningen står i en resultatseksjon om AMS-datering og er
hentet som JATS (ADDENDUM-02 § 2.2). Beslutningen hviler på det eksempelet.
