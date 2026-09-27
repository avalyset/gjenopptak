# ADR-0010 — Løftbarhet er datert

**Repo:** gjenopptak
**Status:** Accepted
**Dato:** 2026-09-25
**Endrer:** ADR-0004 (løftbarhet avledes fra tabellen, aldri fra en modell). Oppslagsregelen står.

## Kontekst

ADR-0004 låste løftbarhet som en oppslagsfunksjon fra hindringsklasse til en tabell fastsatt før
data, og forutså at *tabellen* kan endres ved ADDENDUM. Den forutså ikke at **klassen til en
enkelt oppføring kan skifte fordi verden skifter**.

Heron-kandidaten viser det konkret. W3000588547 (Glasgow 2019, kritisk utgave av Herons *Automata*)
lot tre håndskrifter stå ukollasjonert — Burney MS 108, Harley MS 5589 og Harley MS 5605 — og
oppga hindringen selv: avhandlingens tidsramme. Det er **H1**, menneskelig lesning i skala, løftbar.
Da vurderingen ble gjort 2026-09-25, var alle tre utilgjengelige: British Librarys digitaliserte
bilder har ikke vært i åpen kanal siden cyberangrepet i oktober 2023. Hindringen som faktisk står i
veien i dag, er **H8**, tilgang, ikke løftbar.

Ingen av de to kodingene er feil. De gjelder ulike tidspunkter.

## Beslutning

1. **Klassen gjelder tidspunktet vurderingen gjøres, ikke verket.** En oppføring uten dato er
   ufullstendig, ikke bare udokumentert.
2. **Hver oppføring i registeret bærer `vurdert_dato`** sammen med klasse, løftbarhetsverdi og
   tabellversjon. Løftbarhet er dermed et oppslag på *(klasse, tabellversjon, dato)*, ikke på
   klasse alene. Oppslagsregelen fra ADR-0004 er uendret: en modell setter aldri verdien.
3. **En hindring kan gjeninnføres og oppheves igjen.** Endringen skrives som en **ny datert
   vurdering føyd til oppføringen**, med grunn og kilde. Den forrige vurderingen blir stående.
   Oppføringen skrives aldri om: en historikk som kan redigeres, er ikke en historikk.
4. **Prevalenstall oppgis med vurderingsdato.** «4 av 24 er løftbare» er en påstand om 2026-09-20
   og skal leses slik. Uten dato er tallet ikke etterprøvbart, fordi grunnlaget kan ha flyttet seg.
5. **Gjeninnføring telles.** Andelen oppføringer der hindringen har skiftet klasse siden verket ble
   publisert, er et eget tall. Det måler hvor holdbart et løftbarhetsestimat er over tid.

## Følger

* Et treff kan være løftbart i teorien og blokkert i praksis samtidig. Registeret må kunne si begge
  deler uten å motsi seg selv: klassen forfatteren navnga, og klassen som gjelder nå.
* Falsifiseringstesten i PREREG-v1 §8 får en tidsakse. «Ingen har svart» og «ingen kan svare nå» er
  ulike utfall med ulik holdbarhet.
* Kandidater som er blokkert av noe som kan bli opphevet, **parkeres med en utløser** i stedet for å
  avvises. For Heron er utløseren: BL-bildene tilbake i åpen kanal.
* ADR-0004 står. Det som endres, er at oppslaget nå tar dato som argument, og at registeret bærer
  vurderingshistorikk per oppføring.

## Tillegg (2026-09-25): eier og datopresisjon

To krav kom ut av den første oppføringen som faktisk ble ført. Heron-posten fikk `2019-01-01`, en
dato ingen kilde gir: OpenAlex har bare `publication_year` for verket, og dagen var konstruert av
skjemaets eget format. Avhandlingens tittelblad sier «November 2019» — måned, ikke dag.

6. **En vurdering bærer alltid hvem som gjorde den.** `vurdert_av` er påkrevd og ikke-tomt.
   Verdien skiller to tilfeller som ellers ser like ut:
   * `forfatterens egen formulering, klassifisert av oss` — hindringen står i verkets egen tekst,
     klassen er vår lesning av den.
   * `oss` — vurderingen er vår, gjort mot en kilde utenfor verket.
7. **Datoen er aldri finere enn kilden tillater.** `vurdert_dato` godtar `ÅÅÅÅ`, `ÅÅÅÅ-MM` eller
   `ÅÅÅÅ-MM-DD`, og `datopresisjon` (`år` / `måned` / `dag`) føres ved siden av og må stemme med
   formen. Et skjema som bare godtar hele datoer, tvinger fram oppdiktede dager — og en oppdiktet
   dag er verre enn en grov dato, fordi den ser etterprøvbar ut.
