# PS-246 — resultat

**Kriteriet ble låst før beregning:** `docs/PS-246-KRITERIUM.md`,
sha256 `137bde5040404b2d0e27e23222c44238cc70423418011aa9ca1f9bbb67a43802`, commit `59d4221`.

**Det ugjorte:** å bruke målt matrisk tetthet — og dermed målt partikkeltetthet — i Saxton–Rawls
i stedet for SPAWs faste standardverdi 2,65 Mg/m³.
**Kriteriet:** FC faller under mettet VWC for de målte seksjonene.

## Kilde og verifikasjon

Likningene er hentet fra originalartikkelen: Saxton, K.E. og Rawls, W.J. (2006), *Soil Water
Characteristic Estimates by Texture and Organic Matter for Hydrologic Solutions*, Soil Sci. Soc.
Am. J. 70(5):1569–1578, doi:10.2136/sssaj2005.0117. Artikkelen er lukket hos forlaget; kopien som
er brukt, er arkivert (sha256 `f092918b61806ccdfaee9f6f7bcc2775982a86c78c605fd33bb5b80887d3a902`).
Likninger brukt: **[1]** θ1500, **[2]** θ33, **[3]** θ(S−33), **[5]** θS, **[6]** ρN, **[7]** ρDF,
**[8]** θS−DF, **[9]** θ33−DF, **[10]** θ(S−33)DF.

**Verifikasjon før avhandlingens data ble rørt:** implementasjonen reproduserer **alle tolv rader i
artikkelens tabell 3** eksakt — visnegrense, markkapasitet, metning og normal tetthet, avrundet til
samme heltall og to desimaler som publisert (f.eks. SiL: WP 11, FC 31, SAT 48, ρN 1,38). Sjekken
ligger som test, `tests/test_saxton_rawls.py`.

## Inndata

Fra avhandlingens **tabell 6.1** («The SPAW model soil data inputs», s. 164–165): per horisont
leirandel C og sandandel S som desimalbrøk, organisk materiale OM i %w, og målt matrisk tetthet ρm
i Mg/m³. 29 horisonter lot seg lese entydig.

**Én verdi måtte leses av figur, og det er resultatets svakeste ledd:** de målte
partikkeltetthetene står i **tabell 5.1 og figur 5.2–5.4**, som ligger som bilder uten tekstlag i
PDF-en. Verdiene under er lest av figur 5.2(a) med usikkerhet **±0,02 Mg/m³**, og utfallet er regnet
både med den avleste verdien og med ±0,02.

## Resultat

De fire horisontene forfatteren navngir som FC > θS (avhandlingen s. 190), volumprosent:

| horisont | ρm | ρs lest | FC @2,65 | θS @2,65 | diff | FC @målt | θS @målt | diff | ρs som kreves | utfall |
|---|---|---|---|---|---|---|---|---|---|---|
| CQF AS Clay 1 | 1,64 | 2,72 | 39,3 | 38,1 | **−1,2** | 39,6 | 39,7 | **+0,1** | 2,71 | ja, men innenfor lesefeilen (−0,2 … +0,5) |
| CQF AS Clay 2 (øvre) | 1,73 | 2,72 | 35,7 | 34,7 | **−1,0** | 36,1 | 36,4 | **+0,3** | 2,70 | ja, men innenfor lesefeilen (−0,1 … +0,7) |
| CQF AS Clay 2 (nedre) | 1,84 | 2,72 | 36,7 | 30,6 | **−6,1** | 37,1 | 32,4 | **−4,7** | 2,98 | **nei** |
| CQF DS Ditchfill 1 | 1,68 | 2,62 | 37,6 | 36,6 | **−1,0** | 37,5 | 35,9 | **−1,6** | 2,70 | **nei** |

Negativ differanse = FC over metning, altså fysisk umulig.

**Kontroll mot avhandlingen:** med den faste 2,65 og avhandlingens egne inndata gir beregningen
FC > θS for nøyaktig de fire horisontene forfatteren navngir — inkonsistensen er reprodusert, ikke
bare beskrevet. Over alle 29 horisonter gjelder FC > θS for åtte (de fire over, pluss CQF DS Clay 2,
DCF AS Clay 1, DCF AS Clay 2 og DCF DS Clay 2).

## Er kriteriet oppfylt?

**Nei, ikke for de målte seksjonene som gruppe.** To av fire flagget horisonter flipper til FC < θS
med målt partikkeltetthet, og begge ligger innenfor ±0,02 av terskelen — lesefeilen fra figuren
alene avgjør fortegnet. To flipper ikke: Clay 2 (nedre) krever en partikkeltetthet på **2,98
Mg/m³**, langt over det noen av kurvene i figur 5.2 viser og over vanlige mineraltettheter, og
Ditchfill 1 har en avlest partikkeltetthet (2,62) **under** terskelen sin (2,70).

Forfatteren skrev at «using these measured values, Equations 6.8 and 6.9 return θ33(DF) as lower
than θs(DF), which would allow FC to be reached» (s. 190). Den analysen ble ikke gjennomført i
avhandlingen. Gjennomført nå holder den for to av de fire horisontene forfatteren navnga, og ikke
for de to andre.

## Sammenligning med korreksjonsfaktoren 2,22

Korreksjonsfaktoren virker et annet sted enn tetthetsfiksen: den ganger **modellert SMD** (δj) etter
at modellen har kjørt, og brakte det testede tilfellet (CQF 2011) innenfor 18 mm av målt SMD.
Tetthetsfiksen endrer i stedet **inndata til likning [8]**, og virker per horisont.

Avhandlingen oppgir selv at et annet tilfelle krevde faktor **0,50** i stedet for 2,22. En faktor
som skifter med tilfellet, kompenserer for utfallet, ikke for årsaken. Tetthetsfiksen fjerner
årsaken der partikkeltettheten er høy nok — men, som tabellen viser, ikke overalt: for Clay 2
(nedre) er det ikke partikkeltettheten som er problemet, og der vil en korreksjonsfaktor fortsatt
være det eneste som bringer modellen i nærheten av måledataene.

## Hva dette er og ikke er

* **Den ugjorte analysen er gjennomført.** Det som manglet i avhandlingen, var utregningen med målt
  tetthet; den foreligger nå, med tall per horisont og med terskelen som kreves.
* **Avhandlingen tok ikke feil.** Forfatteren fant årsaken, beskrev den presist, oppga at SPAW ikke
  lot parameteren endres, og valgte en dokumentert omgåelse innenfor sin tidsramme. Det som her er
  lagt til, er utregningen forfatteren selv utsatte.
* **Saxton–Rawls ble publisert i 2006, ti år før avhandlingen.** Likningene var tilgjengelige hele
  tiden, og ingen hindring er opphevet siden publisering. Dette er derfor **ikke** et
  tidsakse-tilfelle etter ADR-0010, og **ikke** et AI-løftbart tilfelle: det som manglet, var tid og
  et verktøy som tok imot målt tetthet.
* **Kjeden er demonstrert, ikke AI-aksen.** Funn → klassifisering → falsifisering → gjennomføring
  har gått hele veien på ett tilfelle. Det sier ingenting om hvor ofte den gjør det, og ingenting om
  hva en modell kan løfte.

## Reproduksjonssteg

1. Hent avhandlingen (W2551114598) og les tabell 6.1: C, S, OM og ρm per horisont.
2. Les partikkeltetthetene av figur 5.2 — de finnes ikke som tekst i PDF-en. Noter din egen
   leseusikkerhet.
3. Hent Saxton & Rawls (2006) og bruk likning [1], [2], [3], [5], [6], [8] og [9].
4. Kjør `src/gjenopptak/falsify/saxton_rawls.py`: `theta_33`, `theta_S` og `med_tetthet(...)`.
   Verifiser først mot artikkelens tabell 3 med `pytest tests/test_saxton_rawls.py`.
5. For hver horisont: regn θS−DF = 1 − ρm/ρs og θ33−DF = θ33 − 0,2(θS − θS−DF), med ρs = 2,65 og med
   målt ρs. Terskelen er ρs* = ρm / (1 − (θ33 − 0,2·θS)/0,8).
6. Sammenlign fortegnet på θS−DF − θ33−DF.
