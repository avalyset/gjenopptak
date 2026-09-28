# SAK-09c — lukket på `[V]`. Klasse **H8**: inndataen finnes ikke utenfor samtykket.

**27.09.2026. Ingen terskel er beregnet, og ingen kriteriefil er låst** — saken nådde aldri dit.
`[V]`-sjekken i [triagen](../SAKBEHANDLING-2026-09-27-triage.md) skulle avgjøre om kildetekstene var
hentbare, og den falt. Etter oppdragets regel lukkes saken med grunn og neste sak tas.

**Sak:** `W7133020405`, passasje AL-2606, feltet energimodellering.
**Verket:** `W7133020405`, doktoravhandling 2018-11 (Aragao 2018), *Using Network Theory to Manage
Knowledge from Unstructured Data in Construction Projects: Application to a Collaborative Analysis of
the Energy Consumption in the Construction of Oil and Gas Facilities*.

## Det ugjorte, ordrett fra avhandlingen

> «Even the network of concepts suggested in this work can possibly be generated automatically (for
> instance, using Google's knowledge graph philosophy). However, this task is not trivial in
> implementing the construction phase, given the limited number of text resources and the
> significant effort it takes to integrate diverse research works from the field of AI, which is not
> entirely mature yet. As such, instead of an automated generation of networks, this research
> proposes a semi-automated method due to scope limitations, even though the authors are aware of
> several AI techniques to generate networks of cases automatically in the future.»

Passasjen navngir to grunner — få tekstressurser og stor arbeidsinnsats — og avgjør ikke hvilken av
dem hindringen var. Derfor sto den kodet **H1/H7-uavklart** etter ADDENDUM-05.

## `[V]`-sjekken, med URL og dato

**Slått opp 27.09.2026.** Posten ligger åpent i det institusjonelle arkivet Scholaris/TSpace:
`http://hdl.handle.net/1807/92034`, post-uuid `51478950-54be-4205-a8d0-b4f368a7e883`,
`inArchive: true`, `withdrawn: false`.

**Posten har én innholdsfil.** `ORIGINAL`-bunten inneholder avhandlingens PDF, **7 387 793 B**. De øvrige buntene er `LICENSE`
(arkivets eget lisensskjema), `TEXT` (arkivets egen tekstutvinning) og `THUMBNAIL`. **Ingen
datafil, ingen tilleggsmateriale, ingen transkripsjoner.**

Filen ble lastet ned og sammenlignet med kopien på Vault:
**sha256 `3765e308632490403a97961781635cf641c8d41eba45d1ed46b24d846e5dc5cb` på begge — identisk.**
Det som er hentbart, er altså nøyaktig det som alt er målt på, og ikke mer.

### (a) Det manuelle nettverket står i avhandlingen — **holder**

Nodesettet er de **34 begrepene** i AFSYS-kartet (13 aktiviteter, 9 systemer, 12 faktorer,
figur 5.3), og kantsettet står som **nabomatriser** for hver av de tre casene, i vedlegg A, B og C,
med et supplement i vedlegg D. Dette leddet av `[V]` er verifisert og står.

### (b) Kildetekstene må være hentbare — **faller**

Avhandlingen svarer selv, ordrett:

> «The adjacency matrices and the tables with the excerpts of each case study are found in
> Appendices A, B, and C. **The interviewees' profiles are not included in this thesis due to
> ethical considerations, as the participants may be identified by their responses, and their
> anonymity was guaranteed as one of the requirements of the formal consent.**»

Kildeteksten er intervjuprofilene, og de er **holdt tilbake av etiske grunner**, ikke av en
betalingsmur. Triagen antok en betalingsmur som den mulige feilmodusen; den virkelige er strengere.
En betalingsmur kan falle. Et samtykke som garanterer anonymitet, faller ikke, og skal ikke falle.

Avhandlingen navngir dessuten selv hva inndataen til det ugjorte ville vært:

> «future works can attempt to integrate automated knowledge retrieval tools to collect and
> represent the concept networks directly from the transcripts or even from the audio files»

**Transkripsjonene og lydfilene.** Ingen av dem er i posten, og ingen av dem kan bli det.

## Hvorfor utdragstabellene ikke kan erstatte kildeteksten

Vedlegg A, B og C har tabeller med **utdrag** fra profilene (A.7/Table A.1 og tilsvarende).
De er hentbare. De kan likevel ikke brukes som inndata til å prøve det ugjorte, og grunnen står i
avhandlingen selv:

> «The excerpts were selected according to their impact on the energy use during the construction.»

Utdragene **er resultatet av det manuelle steget** som automatikken skulle erstatte: de er alt lest,
valgt ut og klassifisert etter virkning på energibruken. Å kjøre begreps- og relasjonsekstraksjon på
dem ville måle hvor godt en modell gjenfinner et nettverk i en tekst som alt er destillert mot det
nettverket. Det er en sirkel, og en recall på 0,70 eller 0,50
målt slik ville ikke si noe om det ugjorte. **Vi gjør det ikke, og vi gjør det ikke med et forbehold
heller.**

## Klassifisering

| | før | nå |
|---|---|---|
| kodet klasse fra teksten | `H1/H7-uavklart` | uendret — teksten har ikke endret seg |
| datert vurdering (ADR-0010) | — | **H8**, `loftbar: nei`, 27.09.2026 |

Dette er samme form som Heron: verket gikk fra løftbar klasse til H8 **uten at teksten endret seg**,
fordi tilgangssituasjonen ligger utenfor materialet. Her ligger den utenfor for godt.
`cites_coverage` står som `«ikke målt»`, ikke 0 — ingen falsifisering er kjørt for denne saken.

## Hva som ikke ble gjort, og bevisst ikke ble gjort

* **Ingen e-post til noen.** Ingen forespørsel til verkets opphav eller til arkivet. Samtykket er
  ikke vårt å utfordre.
* **Ingen kriteriefil låst.** Et kriterium som ikke kan kjøres, skal ikke låses — en låsecommit og en
  kanon-bundle ville gitt saken et revisjonsspor den ikke har fortjent.
* **Ingen delvis kjøring på utdragene**, av grunnen over.
* **Ingen ny måling.** `[V]`-sjekken er ett arkivoppslag og én nedlasting, ingen OpenAlex-kreditter.

## Konsekvens for sporet

**Ledd 2 har ingen sak på AI-aksen der inndataen er offentlig.** SAK-14 var den ene som kunne kjøres,
og den falt på porten. SAK-09c faller før porten. Det er et eget funn om utvalget: de ugjorte
oppgavene som en språkmodell *kunne* løse, ligger ofte i arbeider der inndataen er primærdata samlet
under samtykke — og da er hindringen ikke teknologisk, men rettslig og etisk, og den er ikke løftbar
uansett hvor god modellen blir.

**SAK-09b ligger i samme verk og rammes ikke av dette.** Den trenger nabomatrisene, som står i
vedlegg A–C, og blokkmodelleringsbeskrankningene i vedlegg H — alt i den hentbare filen. Den står
fortsatt i køen, etter SAK-08.
