# PS-246 — kriteriet, låst før noe regnes

**Skrevet:** 2026-09-25, før første beregning. **Redigeres ikke etter dette.**

## Treffet

PS-246 er et ekte treff fra porten, klasse **H5**, i verk **W2551114598** (trekkposisjon 88), en
avhandling om vekstmerker (University of Birmingham 2016, DART-prosjektet).

**Det ugjorte:** å bruke **målt matrisk tetthet** som inndata i Saxton–Rawls i stedet for SPAWs
faste standardverdi for partikkeltetthet.

**Hindringen forfatteren oppga:** SPAW låser partikkeltettheten, slik at markkapasitet (FC) kom ut
høyere enn mettet vanninnhold (θS) — fysisk umulig — og forholdet ble rettet med en
**korreksjonsfaktor på 2,22**.

## Suksesskriterium

**FC faller under mettet VWC for de målte seksjonene** når målt matrisk tetthet brukes i stedet for
standardverdien.

Kriteriet avgjøres per seksjon og oppsummeres som antall seksjoner der FC < θS med målt tetthet,
mot antall der det gjelder med standardverdien.

## Hvordan utfallet behandles

* **Utfallet rapporteres uansett retning.** Faller FC ikke under θS, står det i resultatfilen med
  samme tyngde som et positivt utfall. Kriteriet er skrevet før tallene finnes nettopp for at
  retningen ikke skal kunne velges etterpå.
* Resultatet **sammenlignes mot avhandlingens egen korreksjonsfaktor 2,22**: hvilken justering av
  θS eller FC den tilsvarer, og om den er nødvendig når tettheten kan settes fritt.
* Likninger hentes fra **Saxton & Rawls (2006)**, originalartikkelen, med likningsnummer per
  likning. Implementasjonen verifiseres mot minst én av artikkelens egne publiserte verdier **før**
  avhandlingens data brukes. Treffer den ikke, stoppes forsøket og feilen rapporteres som vår egen.
* Inndata hentes fra avhandlingens tabell 5.1, 6.1, 6.3 og 6.4, med tabell, rad og enhet per verdi.
  Er en verdi tvetydig i PDF-en, føres den som usikker og regnes **med og uten**.

## Hva som ikke påstås

1. **Ikke at avhandlingen tok feil.** Forfatteren beskrev inkonsistensen selv, oppga hvorfor den
   oppsto, og valgte en dokumentert omgåelse under en gitt tidsramme. Det som prøves her, er den
   analysen forfatteren selv utsatte — ikke en korreksjon av arbeidet.
2. **Ikke at dette er en AI-løftbar hindring.** Saxton & Rawls ble publisert i **2006**, ti år før
   avhandlingen. Likningene var tilgjengelige hele tiden. Det som manglet, var tid og et verktøy
   som tok imot målt tetthet — ikke en metode som ikke fantes. Dette er dermed heller ikke et
   tidsakse-tilfelle etter ADR-0010: ingen hindring er opphevet siden publisering.
3. **Ikke at kjeden er validert av ett tilfelle.** Ett gjennomført forsøk viser at kjeden funn →
   klassifisering → falsifisering → gjennomføring kan gå hele veien. Det er ikke et mål på hvor
   ofte den gjør det.
