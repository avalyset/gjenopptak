# LAERDOM — slutninger i gjenopptak

**Ikke låst.** Filen redigeres fritt og er ingen del av preregistreringen. Den er kronologisk, med én seksjon per funn: hva som ble målt, hvilket tall det ga, hvilken slutning som ble trukket, og hva som ble gjort. Den er ikke en logg over slynger, men over slutninger.

Den eldre lærdommen om sikringssteg står for seg i `docs/laerdom-sikring.md`.

## Fast steg

**Hver slynge som produserer en måling, føyer til en seksjon her i samme commit som målingen.**

* Seksjonen har leddene *Målt*, *Tall*, *Slutning*, *Gjort* og *Filer*.
* En slutning som ikke er fulgt opp, føres som ikke gjort. Den skrives aldri som om den var gjennomført.
* Tall kopieres fra filen de står i, ikke fra hukommelse eller oppdragstekst.

---

## 1 Markørfilteret finner ikke det ugjorte når det står som tilstand (2026-09-12)

* **Målt:** recall og presisjon for markørfilteret (L2) mot manuell fasit.
  * v1 er målt på sett 1: 30 dokumenter og 28 treff.
  * v2 er målt på sett 1 og deretter på sett 2: 40 dokumenter og 27 treff. v2 ble frosset før sett 2 ble hentet.
* **Tall:**
  * **v1: 0/28.** Presisjon 0/6, og 0/7 på full tekst.
  * **v2 på sett 1: 28/28.** Tallet er en øvre grense: de 36 tilleggene er lest ut av de samme 28 setningene.
  * **v2 på sett 2: recall 7/27 = 25,9 %** (95 % 13,2–44,7), **presisjon 6/43 = 14,0 %** (6,6–27,3).
* **Slutning:**
  * Listen er bygget på mislykkede handlinger («could not», «were unable to»). Fasiten uttrykker det ugjorte som en tilstand («remains unknown», «no way of determining», «do not reflect») eller som det som ble gjort i stedet.
  * Et leksikalsk filter som førsteledd bærer ikke recall. **Leksikalsk førsteledd er forkastet** (eier, 2026-09-14).
* **Gjort:**
  * ADDENDUM-06 innførte v2 og merket 28/28 som sirkulært.
  * ADDENDUM-07 målte v2, la ikke til markører og satte krav til sett 3.
  * Forkastelsen av førsteleddet er en beslutning. Ingen kode og intet addendum er endret av den ennå.
* **Filer:** ADDENDUM-06 §1.2, §1.4; ADDENDUM-07 §4.1, §4.2, §5; `data/recall-sett.jsonl`, `data/recall-sett-2.jsonl`, `data/recall-sett-2-maaling.json`; `src/gjenopptak/extract/passage.py`.

## 2 Den kvotefrie ruten kan søke i 28,8 % av siteringene (2026-09-12)

* **Målt:** dekningsgrad for falsifiseringstesten i PREREG §8 via Europe PMC og Crossref, på 20 verk trukket med målefrøet 734 248.
* **Tall:**
  * Crossref kjenner 1 156 siteringer.
  * Europe PMC kjenner 617 av dem, 53,4 %.
  * 333 har fulltekst i Europe PMC. **Det gir 28,8 % søkbare av alle kjente siteringer.**
  * Per verk varierer forholdet mellom 0,14 og 1,08.
* **Slutning:** en overlevelsesrate regnet på den kvotefrie ruten ville målt Europe PMCs dekning like mye som litteraturens oppfølging. Falsifiseringstesten må kjøres mot OpenAlex. Den kvotefrie ruten brukes bare til kryssjekk og armering.
* **Gjort:**
  * ADDENDUM-06 §4 fester OpenAlex som målerute.
  * Overlevelsesrate rapporteres aldri uten dekningsgrad.
* **Filer:** ADDENDUM-06 §4; `data/pipeline-test/l4-dekning-PIPELINETEST.json`; `src/gjenopptak/falsify/citations.py`.

## 3 Rammen følger levering, ikke forretningsmodell (2026-09-13)

* **Målt:** hentingsprøve på hele energimodelleringsrammen (30 362 verk), med vertstabeller rå mot hentbar.
* **Tall:**
  * 9 713 verk er hentbare, 32,0 %.
  * ScienceDirect falt fra 1 994 til 30 (1 964 svarte 403).
  * IOP falt fra 1 221 til 4 (1 217 svarte med en HTML-side i stedet for PDF).
  * Wiley falt fra 698 til 2, Hindawi fra 185 til 4, E3S fra 378 til 0 og MATEC fra 90 til 0.
  * arXiv steg fra 4,7 til 14,5 % av rammen, MDPI fra 6,8 til 17,4 %.
  * IEEE Xplore og Springer Link beholdt 89 %. hdl.handle.net falt fra 763 til 0.
* **Slutning:**
  * Rammen er ikke energilitteraturen med tilfeldig bortfall. M1 i feltet er prevalens blant verk hos forleggere og arkiver som leverer PDF til skript.
  * Skillet følger leveringen, ikke forretningsmodellen: Hindawi, E3S og MATEC er rent åpne og svarte 403, mens IEEE og Springer, som også selger abonnement, leverte.
  * Om publiseringskanal samvarierer med hvordan forfattere skriver om det ugjorte, er et åpent forbehold, ikke et funn.
* **Gjort:**
  * Forbeholdet står i sammendraget av enhver rapportering (ADDENDUM-08 §3.3).
  * Energikontrollen i PREREG §7 svarte 403 og står utenfor den hentbare rammen. Det er ført som åpen post.
* **Filer:** ADDENDUM-08 §3; `data/rammeprove-energimodellering-sammendrag.json`; `data/frames/frame-energimodellering-RAW.jsonl` og `-HENTBAR.jsonl`.

## 4 Et fulltekstsøk koster ti kreditter (2026-09-13)

* **Målt:** `x-ratelimit-remaining` før og etter hvert OpenAlex-kall på kvotedøgnet.
* **Tall:**
  * Et filterkall koster 1 kreditt (`x-ratelimit-cost-usd` 0.0001). `fulltext.search` koster **10 kreditter** (0.001).
  * Sju vellykkede fulltekstsøk senket remaining fra 842 til 772.
  * Tolv avviste kall (429) ble ikke belastet.
  * Dagsbudsjettet på 1 000 kreditter gir 100 fulltekstsøk hvis ingenting annet gjøres samme døgn.
* **Slutning:** falsifiseringstesten i L4 er fulltekstsøk i siterende arbeider på OpenAlex (seksjon 2). **L4 er derfor en kvoteskranke, ikke en dagsnotis:** kostnaden må budsjetteres før porten kodes.
* **Gjort:**
  * Kvotemodellen er presisert i ADDENDUM-08 §6.
  * Budsjettet for L4 er ikke laget.
* **Filer:** ADDENDUM-08 §6; `data/kvotedogn-2026-09-13-punkt4-logg.jsonl`; `data/kvotesjekk-2026-09-13.json`.

## 5 Rammene er tynnere enn navnene lover (2026-09-13)

* **Målt:** andelen verk i hver frosset ramme der ingen av feltets emne-ID-er er primærtopic.
* **Tall:**
  * Energimodellering: **54,4 %** (16 506 av 30 362).
  * Arkeologi: **61,9 %** (23 204 av 37 510).
  * Klinisk epidemiologi: **62,7 %** (27 571 av 43 986).
  * Tekstvitenskapskontrollen W3000588547 har feltets T10165 bare som tredje topic.
  * Tekstvitenskap er ikke målt, fordi listen ikke er frosset.
* **Slutning:** i hver ramme har over halvparten av verkene feltet bare som sekundært eller tertiært topic. Feltnavnene lover mer enn rammene inneholder. **Faktisk fag skal kodes per verk under porten** (eier, 2026-09-14).
* **Gjort:**
  * Målt og ført i ADDENDUM-09 §9. Valget av `topics.id` står etter ADDENDUM-02 §7.
  * Kodingen av faktisk fag per verk er en beslutning og er ikke gjennomført.
* **Filer:** ADDENDUM-09 §9; `data/frames/frame-*-RAW.jsonl`; `src/gjenopptak/harvest/coverage.py` (`TOPIC_IDS`).

## 6 L3-POC variant A: deteksjon virker, klassifisering ikke (2026-09-14)

* **Målt:** lokal dommer på 110 blindede passasjer: 55 fasittreff fra sett 1 og 2, og 55 negative passasjer fra leste setninger.
  * Modell: `gemma2:9b`, Q4_0, vekt-sha256 `ff1d1fc7…0373`, temperatur 0, frø 734 248, `keep_alive=0`.
  * Ledetekst A: `de9f8229…`.
* **Tall:**
  * **Recall 81,8 %** (45/55) og **presisjon 95,7 %** (45/47).
  * Negative dømt treff: 3,6 % (2/55).
  * **Eksakt klasse 45,5 %** (25/55). Med H1 og H7 slått sammen: 54,5 %.
  * Dømt uavklart: 2,7 %.
* **Slutning:** modellen finner de parkerte spørsmålene, men plasserer dem ikke i riktig klasse.
* **Gjort:**
  * Resultatene og de ti verste bommene er skrevet og sikret.
  * Frontier-dommeren er ikke målt: Gemini-nøkkelen er på gratisnivå, med null kvote for Pro og 20 kall per døgn for Flash.
* **Filer:** `data/l3-poc/resultater.json`, `dommer-lokal.jsonl`, `bommer-lokal.md`, `spesifikasjon.json`; `src/gjenopptak/classify/l3poc.py`, `l3poc_run.py`, `prompts/l3-poc-v1-system.txt`.

## 7 Feilretningen: modellen kollapser mot ikke-løftbart (2026-09-14)

* **Målt:** fordelingen av variant As dommer mot fasitklassen.
* **Tall:**
  * **11 av 20 klassefeil** blant dømte treff ble dømt H7: H2→H7 4, H1/H7-uavklart→H7 3, H2/H7-uavklart→H7 2, H1→H7 1 og H4→H7 1.
  * **9 av 10 misser** ble dømt INGEN. Den tiende ble dømt N3.
  * Ingen av de sju uavklarte i fasiten fikk riktig klasse.
  * Det var fire dommer med falsk løftbarhet.
* **Slutning:** modellen kollapser mot ikke-løftbart. Det er bort fra det hypotesen hviler på: PREREG §1 punkt 2 sier at en del av hindringene i dag er opphevet, en andel av dem av AI. En ukorrigert lokal klassifisering ville undervurdert den løftbare andelen.
* **Gjort:** variant B ble laget for å prøve om et eksplisitt skille mellom H7 og H1/H2 retter feilen (seksjon 8).
* **Filer:** `data/l3-poc/dommer-lokal.jsonl`, `fasit.jsonl`, `resultater.json`.

## 8 Variant B: terskeleffekt, ikke begrepsavklaring (2026-09-14)

* **Målt:** samme 110 elementer, samme modell og samme innstillinger som variant A.
  * Ledetekst B er A med ett innskutt avsnitt: dataene finnes ikke eller ble aldri samlet inn → H7; arbeidet med data som finnes → H1 eller H2.
  * Det står ett fasiteksempel per side, trukket med målefrøet. Ledetekst B har sha256 `4fe2fb59…06cc73`.
  * Sammenligningen er lekkasjefri på 108 elementer: L3-022 og L3-087 inneholder eksempelsetningene og er holdt utenfor.
* **Tall (A → B, 108 elementer):**
  * **Recall 83,0 → 90,6 %**, **presisjon 95,7 → 90,6 %**.
  * Eksakt klasse 47,2 → 47,2 %. H1 og H7 slått sammen 56,6 → 64,2 %.
  * **Dømt H7 28,7 → 28,7 %.** Dømt INGEN 51,9 → 50,0 %.
  * Falsk løftbarhet 4 → 7. Alle sju B-tilfellene er dømt H1, og de tre nye ligger i biomed.
  * **H2→H7 består:** tre av fem er fortsatt dømt H7.
* **Slutning:** B flyttet terskelen for treff (flere treff, flere falske treff, mer falsk løftbarhet via H1) uten å skjerpe skillet mellom klassene. **Deteksjon og klassifisering skilles i to kall** (eier, 2026-09-14).
* **Gjort:** to-kall-arkitekturen er en beslutning og ikke bygget.
* **Filer:** `data/l3-poc/sammenligning-AB.json`, `dommer-lokal-B.jsonl`, `spesifikasjon-B.json`; `src/gjenopptak/classify/prompts/l3-poc-B-system.txt`.

## 9 Humaniora svikter i begge komponenter (2026-09-14)

* **Målt:** humaniora mot biomed i markørfilteret (sett 2) og i L3-POC-en.
* **Tall:**
  * **Markørfilteret:** v2 har recall 1/8 = **12,5 %** i humaniora (presisjon 1/20 = 5,0 %), mot 6/19 = 31,6 % i biomed.
  * **L3, variant A:** humaniora har **recall 72,0 %** (18/25) og **eksakt klasse 28,0 %** (7/25), mot 90,0 % og 60,0 % i biomed.
  * **L3, variant B:** recall i humaniora steg til 87,5 %, men eksakt klasse ble stående på 33,3 % (lekkasjefritt).
* **Slutning:**
  * Feltet som sannsynligvis er rikest på klassen, er det dårligst dekkede. Historisk tekstvitenskap ble valgt for H1–H2 (PREREG §4).
  * Feltet har tynnest fulltekst: 14,5 % av verkene har PDF-lenke, og ingen har forlagsmerket JATS (ADDENDUM-01 §7).
  * Feltet er svakest i begge komponentene som skal finne klassen.
* **Gjort:** kravet i ADDENDUM-07 §7 om minst én kildeutgivelse i sett 3 står. Utover det er det ikke satt inn noe særskilt tiltak for humaniora.
* **Filer:** ADDENDUM-07 §4.1; ADDENDUM-01 §7; `data/l3-poc/resultater.json`, `sammenligning-AB.json`.

## 10 Åtte ganger meldte en komponent grønt og var feil (2026-09-14)

* **Målt:** gjennomgang av tilfellene fram til nå der en komponent signaliserte suksess mens tilstanden var en annen.

| nr | komponent | grønt signal | faktisk tilstand | fanget av | fil |
|---|---|---|---|---|---|
| 1 | markørfilter v1 | rørledningstesten ga 217 kandidater | recall 0/28 mot fasiten | manuell fasit, lest uten filteret | ADDENDUM-06 §1.2, §3 |
| 2 | markørfilter v2 | 28/28 på sett 1 | 7/27 på sett 2 | ny fasit fra dokumenter ingen markør er hentet fra | ADDENDUM-06 §1.4; ADDENDUM-07 §5 |
| 3 | lenketellingen R3 som hentbarhet | PDF-lenke registrert for 50–73 % | lesbar tekst for 17–47 %; overdrevet 1,5–3,8× | faktisk nedlasting av 30 verk per felt | ADDENDUM-03 §2, §4 |
| 4 | JATS-parseren | setninger returnert uten feil; 147 675 lagret | 143 av 341 filer avkortet; 39 519 setninger manglet | ny parse av de samme bytene ga 537 og 20 setninger | ADDENDUM-07 §2.2 |
| 5 | språk-, lengde- og årsporten ved høsting | posten besto, og Crossref bekreftet året | 2 av 15 humanistiske tekster var en annen artikkel | lesing av teksten mot posten | ADDENDUM-07 §2.3 |
| 6 | henting fra Acervo | HTTP 200 | F5-robotsperre på 224 tegn i stedet for artikkelen; 66 av 127 vurderinger | innholdet sjekket mot posten | ADDENDUM-07 §1.2, §2.3 |
| 7 | siteringsoppslaget i L4 | kallene gikk uten feil | null siteringer for alle 20 verk: Crossref-`select` ga 400, og `MED/{PMCID}` gir stille 0 | armering mot 10.7554/elife.09560 (391 i Crossref, 194 i Europe PMC) | commit `066b92e`; `src/gjenopptak/falsify/citations.py` |
| 8 | repo-sikringen | bundle skrevet, suksess meldt | den ekte bundelen overskrevet (sha256 `468ddbca…` → `327fb3ce…`) | kjøring mot ekte arkivtilstand, med sha256 før og etter | `docs/laerdom-sikring.md` |

* **Slutning:** fellesnevneren er at hvert tilfelle ble **fanget av en uavhengig måling mot ekte tilstand, aldri av selvsjekk.** Uavhengige målinger her er manuell fasit, et usett sett, faktisk nedlasting, ny parse av de samme bytene, lesing mot posten, innholdskontroll, armering mot et kjent verk og sha256 av det ekte arkivet. Ingen av komponentene oppdaget sin egen feil.
* **Gjort:** hver sak fikk sin egen motvekt:
  * ny fasit før et filtertall regnes som måling (ADDENDUM-07 §7);
  * hentbarhet definert ved faktisk henting (ADDENDUM-04 §1);
  * rettet parser med armert test (`296ea2e`);
  * identitetsport per lenke (`3dc08ad`), også i trekkingen (ADDENDUM-09 §5);
  * robotsperre ført som nektelse, ikke som «for kort»;
  * `ArmingFailed` i L4;
  * bundelnavn med HEAD, og sikring testet mot ekte tilstand.
  * En generell regel om uavhengig måling for alle komponenter er ikke innført.
* **Filer:** se tabellen.

## 11 Tekstvitenskap er tynnest også i hentbarhet (2026-09-16)

* **Målt:** frysing av tekstvitenskapsrammen, karakterisering på de første 200 posisjonene i trekkrekkefølgen med samme port som de tre andre feltene, sekundærtopic-andel fra den frosne listen, og overlapp mot de tre andre listene.
* **Tall:**
  * Rammen har **66 440 verk** (333 sider, 334 kall), sha256 `3a938995…f852c`.
  * **Hentbar andel 49/200 = 24,5 %** (95 % 19,1–30,9). Anslått ramme **16 278 verk** (12 661–20 533).
  * Det er lavest av de fire feltene: klinisk epidemiologi 37,0 %, energimodellering 32,0 % (talt på hele listen), arkeologi 31,0 %.
  * ADDENDUM-04 §1.3 anslo om lag 29 000 verk, altså 43 %, fra 30 verk i ADDENDUM-03 §2.3 med intervall 27–61 %. **Målingen ligger under den nedre grensen i det anslaget.**
  * Alle 49 kom på ledd P3. **Ingen kom via Europe PMC:** feltet har ingen JATS-rute (ADDENDUM-01 §7).
  * Største frafall er fravær, ikke blokkering: **93 av 200 (46,5 %) har ingen PDF-lenke**. Deretter HTML i stedet for PDF 18, annen HTTP-status 12, 403 11, nettverksfeil 9.
  * Ingen vert dominerer. De største er de Gruyter 8 → 0 og hdl.handle.net 6 → 0, mens dergipark 5 → 5 og OpenEdition 5 → 5 leverer alt.
  * **Sekundærtopic: 35 547 av 66 440 = 53,5 %** har ikke feltets emne som primærtopic.
  * Overlappet mot arkeologi er **140 verk** — nøyaktig tallet ADDENDUM-02 §7 regnet fram ved inklusjon–eksklusjon. Mot energimodellering og klinisk epidemiologi er det 0.
* **Slutning:**
  * Feltet som ble valgt fordi det ventes å være rikest på H1–H2 (PREREG §4), er tynnest i hvert ledd: lavest hentbarhet, ingen JATS-rute, svakest markørfilter (12,5 %) og svakest klassifisering i L3 (28 %). Det forsterker seksjon 9.
  * Frafallet her er fravær av lenke, ikke utgiverblokkering. Det er en annen mekanisme enn forleggerskjevheten i seksjon 3, og den kan ikke rettes med en annen rute.
  * Et anslag fra 30 verk er ikke presist nok til å dimensjonere et felt: målingen på 200 falt utenfor intervallet fra 30.
* **Gjort:**
  * Rammen er frosset og sikret, og 25 verk er trukket etter ADDENDUM-09 (siste trukne posisjon 118).
  * Den åpne raden for tekstvitenskap i ADDENDUM-09 §9 er fylt.
  * Ingen terskel og ingen regel er endret.
* **Filer:** `data/frames/frame-tekstvitenskap-RAW.jsonl`; `data/utvalg/karakterisering-tekstvitenskap.json`, `utvalg-tekstvitenskap.jsonl`, `trekklogg-tekstvitenskap.jsonl`; ADDENDUM-01 §7; ADDENDUM-02 §7; ADDENDUM-04 §1.3; ADDENDUM-09 §9.

## 12 Porten uten leksikalsk førsteledd koster snaut tre døgn lokal inferens (2026-09-16)

* **Målt:** L1 og L2 på de 100 trukne verkene, og faktisk dømmetakt for dommer A på ekte passasjer fra utvalget.
* **Tall:**
  * **66 833 setninger** i de 100 verkene. Median 389 per verk, største 7 257, minste 22.
  * Hele teksten i passasjer gir **22 243 passasjer med steg 3**, som er det minste steget som bevarer ±2-paringen i ADDENDUM-03 §1.2. Ikke-overlappende vinduer gir 13 405, og ett vindu per setning gir 66 833.
  * Dømmetakten er målt på 12 ekte passasjer: **10,4 sekunder per passasje** med `keep_alive=0`, som ADR-0003 krever. Modellen lastes på nytt for hver dom.
  * Det gir **omtrent 64 timer** for de 22 243 passasjene. Ikke-overlappende vinduer ville kostet 39 timer, ett vindu per setning 193 timer. Hvert treff koster i tillegg ett oppfølgingskall for enhet og bedømbarhet.
* **Slutning:**
  * Å sende hele teksten gjennom en 9B-dommer uten førsteledd er en flerdøgnskjøring allerede for 100 verk. Det er gjennomførbart for utvalget, og det er prisen for at det leksikalske førsteleddet er forkastet (seksjon 1).
  * Kostnaden er lineær i tekstmengde. Et sveip over en hel ramme — 16 000 til 44 000 hentbare verk per felt — ville med samme arkitektur kostet i størrelsesorden ti tusen timer. Verktøyet kan altså kode et utvalg, men ikke sveipe en ramme, med mindre førsteleddet erstattes av noe raskere enn dommeren selv.
  * `keep_alive=0` er en stor del av prisen. Kravet står likevel: det er det som hindrer at en passasje dømmes i skyggen av den forrige (ADR-0003).
* **Gjort:**
  * L1 og L2 er kjørt og lagret for alle 100 verkene, med seksjonsetikett og proveniens per setning.
  * Dømmingen er startet med steg 3 og er gjenopptakbar: hver passasje skrives fortløpende, og en ny kjøring tar bare dem som mangler.
  * Ingen terskel og ingen regel er endret. To-kall-arkitekturen fra seksjon 8 er fortsatt ikke bygget; oppfølgingskallet for enhet og bedømbarhet er et første skritt i den retningen.
* **Filer:** `src/gjenopptak/classify/port.py`, `port_run.py`; `data/port/spesifikasjon.json`, `passasjer-*.jsonl`, `setninger-*.jsonl`.

## 13 Lastingen var ikke kostnaden — ledeteksten var det (2026-09-16)

* **Målt:** takten for dommer A på ekte passasjer, med og uten at modellen holdes lastet, og determinismen mellom de to måtene.
* **Tall:**
  * Med `keep_alive=0`, som ADR-0003 krever: **11,6 sekunder per passasje** (median over 47 dommer). Første anslag fra 12 passasjer var 10,4 s.
  * **Median `load_duration` er 1,5 s av de 11,6.** Lastingen er altså 13 % av kostnaden, ikke hoveddelen. Resten er prefill av ledeteksten på om lag 1 400 tokens, som er identisk for hver passasje.
  * Med modellen lastet: **3,96 sekunder per passasje**, altså 2,9 ganger raskere. Gevinsten kommer av at prefiksen gjenbrukes, ikke av spart lasting.
  * **Determinismen holdt: 47 av 47 identiske råsvar og klasser**, og vektfilen var uendret før og etter.
  * Gjenstående tid for porten faller fra om lag 64 til om lag 24 timer.
* **Slutning:**
  * Antakelsen om hvor tiden går, var feil, og den ville gitt feil tiltak. Hadde lastingen vært hovedkostnaden, ville en raskere disk hjulpet; den virkelige kostnaden er en lang ledetekst som sendes på nytt for hver passasje.
  * Det peker videre: en kortere ledetekst, eller en arkitektur der rubrikken ligger i prefiksen og bare passasjen varierer, er den neste innsparingen. To-kall-arkitekturen fra seksjon 8 bør bygges med det for øye.
  * Kravet i ADR-0003 kunne ikke bare oppheves. Det ble byttet mot en måling: identisk utfall på alt som alt var dømt, og ny sjekk etter kjøringen.
* **Gjort:**
  * ADR-0008 skrevet og akseptert, med determinismesjekk før og etter batchen som betingelse.
  * `judge.py` godtar `keep_alive ≠ 0` bare med `batch: true` i signaturen.
  * Kjøringen gjenopptatt med lastet modell.
* **Filer:** `docs/decisions/0008-keepalive-ved-batch.md`; `data/port/determinisme-ADR0008.json`; `src/gjenopptak/classify/port_run.py`, `l3poc_run.py`, `judge.py`.

## 14 Ankerne røpet seg på lengden — signalet ble funnet før lesningen (2026-09-17)

* **Målt:** tegnlengden på de 20 ankerpassasjene mot de 200 portpassasjene i prøvebygget av presisjonssettet, før og etter at lengdekvartil ble lagt inn som tredje stratifiseringsakse.
* **Tall:**
  * **Før:** median 602 tegn for portradene mot **768** for ankerne — **166 tegns avstand**. Kvartilbredden var 500 tegn for portradene mot 188 for ankerne.
  * **Etter:** median **754 mot 768 — 14 tegns avstand**, kvartilbredde 216 mot 188. Portradenes fordeling over ankernes fire lengdekvartiler ble 56/52/49/43 mot måltettheten 50/50/50/50.
  * Strataene på felt og dømt klasse er **bit for bit identiske før og etter** (samme 16 celler, samme kvoter; INGEN-radene 23/27 per felt begge ganger). Lengdeaksen fordeler bare innenfor cellene.
  * **Halene står igjen:** portradene har fortsatt korte passasjer helt ned i 9 tegn (P10 = 320), mens ankerne starter på 485 (P10 = 523). Over 1 930 tegn finnes bare ankere.
* **Slutning:**
  * Ankerne er hentet fra humanistiske og biomedisinske recall-dokumenter, portradene fra fire andre felt. Setningslengden i kildene skilte dem, uten at noe felt i blindfilen gjorde det. Blinding er ikke bare et spørsmål om hvilke felter filen har — materialets egen form kan være merkelappen.
  * Medianavstanden er lukket uten å røre de to overordnede aksene, men **en passasje under ~485 tegn er fortsatt sikkert en portrad**. Det er en rest som ikke kan fjernes uten å endre selve materialet, og som derfor blir et forbehold i stedet for et tiltak.
  * **Signalet ble funnet før lesningen, ikke etter.** Det betyr at leseren — samme instans som skal avgjøre om de 220 passasjene er ekte treff — kjente signalet da lesningen begynte. Det er i seg selv en del av forbeholdet: ankerne kan i prinsippet gjenkjennes på lengde i halene, og et anker som gjenkjennes måler ikke lenger om lesningen har flyttet seg. Ankertallene skal leses med det, ikke som en ren kalibrering.
* **Gjort:**
  * `stratifisert` fikk en underordnet akse som fordeler *innenfor* hvert stratum mot en måltetthet, uten å endre stratumkvotene. Rekkefølgen er felt, dømt klasse, lengde; lengden kan aldri bryte de to første.
  * Kvartilgrensene (669/768/856 tegn i prøvebygget) regnes på ankernes egen fordeling, og krav en tom lengdebøtte ikke kan dekke, flyttes til nærmeste bøtte som har rader.
  * Restsignalet i halene er ført her i stedet for å bli dempet bort.
* **Filer:** `src/gjenopptak/classify/port.py`, `port_run.py`, `tests/test_port.py`.

## 15 To skjevheter i presisjonssettet: N3-bunken og det tynne feltet (2026-09-17)

* **Målt:** klassefordelingen i portmaterialet etter 18 964 dømte passasjer, og hva den gjør med presisjonssettets sammensetning.
* **Tall:**
  * Ikke-treffene er ikke én bunke: **INGEN 15 380 (81,1 %), N3 1 478, N1 37, N2 8**. N3 er **97,0 % av N-klassene** og 8,8 % av alle ikke-treff.
  * Treffraten per felt: energimodellering 14,2 %, arkeologi 11,7 %, klinisk epidemiologi 8,3 %, **tekstvitenskap 3,0 %**. Proporsjonal trekking ville gitt tekstvitenskap **5 av de 150** leste treffene.
  * Med gulv på 25 ble feltfordelingen i treffstratumet 57 energimodellering / 50 arkeologi / 25 tekstvitenskap / 18 klinisk epidemiologi.
  * N1 og N2 er 45 passasjer til sammen og leses i sin helhet. De er korte av natur: **median 280 tegn mot 731–760 i de tre trukne stratene**. 39 av 45 ligger i ankernes nederste lengdekvartil.
* **Slutning:**
  * **N3 måtte bli eget stratum.** Skillet mellom N3 og H-klassene er «navngitt hindring eller ikke» — finere enn skillet mot INGEN, og dermed der en falsk negativ er mest sannsynlig. Trekkes de 50 ikke-treffene bare fra INGEN, måler recall-tallet INGEN-bunken og kaller det materialet. Derfor rapporteres bom tredelt — INGEN, N3, N1/N2 — og aldri slått sammen; den vektede raten står ved siden av med vektene fra materialets egen fordeling, ikke i stedet for delene.
  * **Gulvet på tekstvitenskap er en måleskranke, ikke en vekting.** 3,0 % kan være ekte sjeldenhet i humanistisk prosa, eller en dommer som er dårligere på den prosaen: POC-en målte 72 % recall i humaniora mot 90 % i biomed. De to forklaringene skilles bare hvis feltet har nok leste treff til at presisjon kan måles separat der. Fem hadde ikke vært nok til noe som helst.
  * **Sensus kan ikke lengdedempes.** N1/N2 leses i sin helhet, så det finnes ingen trekkefrihet å forme fordelingen med. Det trekker medianen for portradene samlet ned fra 737 til 709 tegn. Blant radene under 361 tegn er 56 % N1/N2 — kortheten er altså et halvt signal, ikke et helt. Det er ført som forbehold; å jevne det ut ville krevd at de andre stratene ble trukket skjevt bort fra sitt eget materiale, og da måler presisjonen noe annet enn materialet.
* **Gjort:**
  * `feltkvoter()` med gulv, kjørt før klassestratifiseringen, så rekkefølgen er felt → klasse → lengde.
  * N3 som eget stratum på 50, stratifisert på felt; N1/N2 lest i sin helhet og rapportert rått uten ekstrapolering.
  * `presisjon()` tar vekter fra materialet og rapporterer de tre bomratene hver for seg.
* **Filer:** `src/gjenopptak/classify/port.py`, `port_run.py`, `tests/test_port.py`.

## 16 Porten målt: 16 % presisjon, og dommeren mister omtrent like mange som den finner (2026-09-20)

> **Foreldet av ADDENDUM-10 og ADDENDUM-11 (se § 20 og § 21).** Tallene under er som de sto
> 2026-09-20 og er ikke rettet — loggen er datert, ikke gjeldende. Gjeldende tall: presisjon
> 16,7 % (koder 1) og 12,7 % (koder 2), M1-korrigert 0,671 / 0,604, M2 88,0 % / 31,6 %.
> Kilde: `docs/RESULTAT-PORT-v1.md`.

* **Målt:** 320 blindede passasjer lest mot PREREG §2 og passasjekravet i ADDENDUM-03 §1.2 — 150 dømte treff, 50 dømt INGEN, 50 dømt N3, alle 50 N1/N2, og 20 ankere fra recall-settenes fasit. Nøkkelen ble åpnet først etter at alle 320 verdikter var skrevet.
* **Tall:**
  * **Presisjon 16,0 % (24 av 150), Wilson 11,0–22,7 %.** Per felt: arkeologi 26,0 %, klinisk epidemiologi 22,2 %, tekstvitenskap 16,0 %, **energimodellering 5,3 %** (3 av 57).
  * Per dømt klasse er **H7 den eneste med signal: 33,3 % (21 av 63)**. De uavklarte er tomme: **H5/H7-uavklart 0 av 27, H1/H7-uavklart 0 av 13**. H8 1 av 18, H9 1 av 14, H1 0 av 7, H5 0 av 6.
  * Av de 126 falske treffene er **46,8 % dømt H7 eller H8** — den største enkeltandelen, men under halvparten. De uavklarte klassene tar 31,7 % til.
  * **Bom blant ikke-treffene, tredelt: INGEN 2,0 % (1 av 50), N3 2,0 % (1 av 50), N1 0 av 37 og N2 0 av 13 rått.** Vektet med materialets egen fordeling (INGEN 91,7 %, N3 8,1 %, N1+N2 0,25 %): **2,0 %**.
  * Regnet om på materialet: om lag **348 ekte treff [239–493]** blant de 2 173 dømte, mot **om lag 401 tapte [110–1405]** blant de 20 070 ikke-treffene. **Implisert recall ≈ 46 %.**
  * **Ankerne: 12 av 12 kjente treff lest som treff, 8 av 8 kjente ikke-treff lest som ikke-treff. Eksakt klasseenighet 75 % (9 av 12)**, med tre avvik, alle mot H7 eller H1.
  * **M1-rå ≥1 treff: 0,93. ≥2: 0,85. ≥3: 0,83. M1-korrigert: 0,652.** Uten de tre atypiske: 0,94 / 0,88 / 0,86 / 0,668. Per felt korrigert: arkeologi 0,87, klinisk 0,75, energimodellering 0,59, tekstvitenskap 0,40.
  * **M1-streng og M1-passasje er praktisk talt identiske (0,93 mot 0,93)**, fordi dommeren merket **2 128 av 2 173 treff (97,9 %) som samme setning**.
  * **M2: dommerens egne merker gir 10,5 %** (1 688 av 2 173 er «usikker»). **På mine 24 leste ekte treff er den 87,5 %** (21 av 24).
  * Primær- mot sekundærtopic: 50 verk hver vei, presisjon **16,7 % mot 15,5 %** — ingen forskjell.
  * 48 tvilstilfeller ført til `data/port-tvil.jsonl`, uavgjort.
* **Slutning:**
  * **M1-rå er en grunnrate, ikke en prevalens.** 93 av 100 verk har minst ett dømt treff; etter måling står om lag to tredeler igjen, og korreksjonen hviler på en presisjon med bredt intervall. Tallet som skal rapporteres er M1-korrigert med intervallet, aldri M1-rå alene.
  * **De uavklarte klassene er støy, ikke usikkerhet.** Null av 40 leste treff i H5/H7- og H1/H7-uavklart holdt. Dommeren bruker dem som oppsamling når passasjen nevner en begrensning uten at noe er ugjort. De bør ikke telle med i noe M1-tall før mekanismen er endret.
  * **Feilmønsteret er én ting: dommeren leser enhver omtale av en mangel som et parkert spørsmål.** Feltgapene («little is known about…»), prosjektenes egne vansker i case-studier, metodebegrensninger og ekskluderingskriterier utgjør nesten hele falskmassen. Energimodellering er verst fordi litteraturen der er full av modellbegrensninger.
  * **Ankerne holder.** At lesningen traff 12 av 12 og 8 av 8 mot en fasit skrevet før dommeren fantes, betyr at 16 % ikke er en artefakt av en strengere leser. Klasseavvikene går mot H7 — samme retning som dommerens, verdt å merke seg.
  * **Enhetsmålingen er mettet og måler ingenting.** Når 97,9 % av treffene merkes «samme setning», er ikke M1-streng en følsomhetsanalyse lenger. Enheten må avgjøres av spennet i teksten, ikke av modellens eget svar.
  * **Recall er like dårlig som presisjonen, og verre målt.** To prosent bom på 20 070 ikke-treff er flere tapte enn funnede treff, med et intervall som spenner fra 110 til 1 405. Uten flere leste ikke-treff kan ikke dette strammes inn.
  * Frykten fra ADDENDUM-09 §9 om sekundærtopic slo ikke til: presisjonen er den samme uansett om feltet er verkets primærtopic.
* **Gjort:**
  * 320 verdikter i `data/port-presisjonssett-verdikter.jsonl`, sammenstilt til `data/port-presisjonssett.jsonl`.
  * `m1_varianter` tar nå `streng`, og målingen rapporterer M1 i fire varianter × streng/passasje × per felt × med og uten atypiske.
  * `topicdeling()` lagt til; M2 regnes på mine verdikter, ikke på dommerens merker.
  * 48 tvilstilfeller ført uavgjort til `data/port-tvil.jsonl`.
* **Filer:** `data/port-presisjonssett-{blind,nokkel,verdikter}.jsonl`, `data/port-presisjonssett.jsonl`, `data/port/presisjon-resultater.json`, `data/port-tvil.jsonl`; `src/gjenopptak/classify/port.py`, `port_run.py`.

## 17 Løftbar andel og første falsifisering (2026-09-21)

> **Foreldet av ADDENDUM-10 (se § 20).** Gjeldende løftbar andel: 5 av 25 = 20,0 % (koder 1),
> 2 av 19 = 10,5 % (koder 2). Falsifiseringen dekker fire av de fem — PS-031 kom til med
> ADDENDUM-10 og er ikke prøvd. Kilde: `docs/RESULTAT-PORT-v1.md`.

* **Løftbar andel:** bare **4 av 24 ekte treff (16,7 %) er i en løftbar klasse (H1–H6)** etter ADR-0004-tabellen; 20 av 24 (83,3 %) er H7–H9. Ankerne ligger likt (2 av 12). Verktøyet kan altså love noe for om lag en sjettedel av det porten faktisk finner.
* **Falsifisering, 36 kreditter:** alle fire løftbare treff **overlever** — ingen siterende arbeid har tatt opp det ugjorte (12 siterende med 58 % fulltekstdekning for W2936215896, 1 med 100 % for W2551114598, og W3217588367 har ingen siterende i det hele tatt). Testen er svak der siteringsgrunnlaget er tynt: «overlever» betyr her «ingen har svart», ikke «ingen kunne ha svart».

## 18 Den beste kandidaten faller på materialet, ikke på metoden (2026-09-25)

* **Målt:** om det beste løftbare treffet i materialet lar seg forsøke. W3000588547 (Glasgow 2019, kritisk utgave av Herons *Automata*) lot tre håndskrifter stå ukollasjonert og oppga tidsrammen som hindring — H1, løftbar. Sigla-listen er lest fra avhandlingen, tilgjengelighet og modeller er slått opp.
* **Tall:**
  * De tre er **Burney MS 108** (ff. 81v–100r), **Harley MS 5589** (ff. 19r–27r) og **Harley MS 5605** (ff. 50v–69r) — alle i British Library, til sammen **93 manuskriptsider**, fordelt på β- og γ-grenen av stemmaet.
  * Alle tre står som digitalisert i BLs katalog, men med **«Images currently unavailable»**: bildene har ikke vært i åpen kanal siden cyberangrepet i oktober 2023, snart tre år.
  * Åpne Kraken-modeller for gresk minuskel finnes (PatristicTextArchive, Vat. gr. 2228, begge CC-BY-SA 4.0), men **ingen rapporterer en uavhengig feilrate**. Nærmeste publiserte overføringstall: **5,13 % CER på håndskriftet modellen er trent på, 27,13 % på et annet** (LT4HALA 2026). Femdobling ved ny hånd — og de tre er 1500-tallshender mot modellenes 9.–14. århundre.
  * Realistisk rute hvis bildene fantes: 20–30 sider transkribert for hånd, finjustering, så HTR og kollasjon med CollateX — **2–4 ukers spesialistarbeid**.
* **Slutning:**
  * **Forsøket faller på materialet, ikke på metoden.** Det er ikke lesekapasiteten som stanser kollasjonen i 2026; det er at bildene ikke finnes i åpen kanal. En kollasjon krever ordnøyaktige lesninger, og 27 % CER gir ikke det — men det spørsmålet blir aldri aktuelt uten bilder.
  * **Hindringen har skiftet klasse siden publisering: H1 i 2019, H8 fra oktober 2023.** Begge kodingene er riktige for hvert sitt tidspunkt. Det er grunnlaget for ADR-0010: løftbarhet er datert, og hver oppføring bærer vurderingsdato.
  * Kandidaten avvises ikke — den **parkeres med en utløser**: BL-bildene tilbake i åpen kanal. Omfanget er lite, det finnes en moderne kritisk utgave å kollasjonere mot, stemmaposisjonene er kjent, og forfatteren har selv skrevet at kollasjonen skal gjøres før publisering.
* **Gjort:** `docs/HERON-KOLLASJON-VURDERING-v1.md` skrevet; ADR-0010 vedtatt; ADR-0004 merket som endret; én linje føyd til `docs/RESULTAT-PORT-v1.md`.
* **Filer:** `docs/HERON-KOLLASJON-VURDERING-v1.md`, `docs/decisions/0010-loftbarhet-er-datert.md`, `docs/decisions/0004-loftbarhet-fra-tabell.md`, `docs/RESULTAT-PORT-v1.md`.

## 19 Den ugjorte analysen ble gjennomført — og forfatterens anslag holdt for to av fire (2026-09-25)

* **Målt:** PS-246, et ekte treff i klasse H5: avhandlingen W2551114598 lot være å bruke målt matrisk tetthet i Saxton–Rawls, fordi SPAW låser partikkeltettheten til 2,65 Mg/m³ og markkapasiteten dermed kom ut over metningen. Kriteriet ble låst før beregning (`docs/PS-246-KRITERIUM.md`, commit `59d4221`).
* **Tall:**
  * Implementasjonen ble verifisert mot artikkelens egen tabell 3 **før** avhandlingens data ble rørt: **alle tolv teksturklasser reprodusert eksakt** (WP, FC, SAT, ρN).
  * Med SPAWs faste 2,65 og avhandlingens egne inndata gir beregningen FC > θS for **nøyaktig de fire horisontene forfatteren navngir** — og for åtte av 29 horisonter i alt. Inkonsistensen er dermed reprodusert, ikke bare gjenfortalt.
  * Med målt partikkeltetthet, lest av figur 5.2 med **±0,02 Mg/m³**: Clay 1 **+0,1 %v** og Clay 2 (øvre) **+0,3 %v** flipper til fysisk mulig, begge innenfor lesefeilen. Clay 2 (nedre) gjør det ikke — den krever **2,98 Mg/m³**. Ditchfill 1 heller ikke: avlest 2,62 mot terskel 2,70.
  * **Kriteriet er ikke oppfylt** for de målte seksjonene som gruppe: to av fire, begge marginale.
* **Slutning:**
  * **Å gjennomføre er ikke det samme som å slutte seg til.** Forfatteren skrev at målte verdier «would allow FC to be reached». Utregningen viser at det holder for to av de fire horisontene forfatteren selv navnga. Påstanden var rimelig og delvis riktig; bare utregningen kunne skille.
  * **Det avgjørende leddet lå ikke i likningene, men i lesbarheten.** Tabell 5.1 og figur 5.2–5.4 er bilder uten tekstlag, så partikkeltetthetene måtte leses av en kurve. Den lesefeilen alene bestemmer fortegnet for to av fire horisonter. Et datavedlegg ville avgjort saken; en PDF-figur gjør det ikke.
  * **Korreksjonsfaktoren og tetthetsfiksen virker på hver sin side av modellen.** 2,22 ganger modellert SMD etter kjøring, og avhandlingen måtte bruke 0,50 i et annet tilfelle. En faktor som skifter med tilfellet, kompenserer for utfallet; tetthetsfiksen fjerner årsaken — men bare der partikkeltettheten er høy nok.
  * **Ingen AI-akse og ingen tidsakse.** Saxton & Rawls er fra 2006, ti år før avhandlingen. Det som manglet, var tid og et verktøy som tok imot målt tetthet. Kjeden funn → klassifisering → falsifisering → gjennomføring er demonstrert på ett tilfelle; hvor ofte den går hele veien, er ikke målt.
* **Gjort:** `src/gjenopptak/falsify/saxton_rawls.py` med likning [1]–[10] fra originalartikkelen; `tests/test_saxton_rawls.py` som holder tabell 3 som permanent kontroll; resultatet i `docs/PS-246-RESULTAT.md`; datert vurdering føyd til PS-246 i registeret etter ADR-0010.
* **Filer:** `docs/PS-246-KRITERIUM.md`, `docs/PS-246-RESULTAT.md`, `src/gjenopptak/falsify/saxton_rawls.py`, `tests/test_saxton_rawls.py`, `register/claims.jsonl` (Vault).

## 20 Tre presiseringer skrevet etter data flyttet én av 48 saker (2026-09-25)

* **Målt:** de 48 tvilstilfellene fra lesningen av presisjonssettet, avgjort etter tre presiseringer av treffkravet i ADDENDUM-10 — og hva avgjørelsene gjør med tallene.
* **Tall:**
  * Fordeling: **7** saker under §1 (feltgap tilhører feltet → ikke treff), **2** under §2 (oversiktsarbeid har sitt eget ugjorte → treff H7), **10** under §3 (modellbegrensning: regnekraft/løser → H5, manglende metode/teori → H9, selvpålagt forenkling → N3), og **29** utenfor alle tre, avgjort på passasjen som før.
  * **Én verdikt endret seg: PS-031.** Presisjonen går fra 24/150 = 16,0 % til **25/150 = 16,7 %**, energimodellering fra 5,3 % til 7,0 %, M1-korrigert fra 0,652 til **0,671**, løftbar andel fra 16,7 % til **20,0 %**, M2 fra 87,5 % til 88,0 %.
  * M1-rå er uendret ved alle tre tersklene (0,93 / 0,85 / 0,83): ADDENDUM-10 rører ikke dommerens utdata.
  * Tre nye oppføringer i registeret (PS-031, PS-257, PS-300 — de to siste er ekte treff funnet i N3- og INGEN-stratene), 16 bekreftende daterte vurderinger føyd til eksisterende, og én sak (PS-246) sto allerede med en vurdering datert samme dag og ble ikke rørt.
* **Slutning:**
  * **En regel skrevet etter data må måles på hvor mye den flytter.** Tre presiseringer som flyttet én av 48 saker, presiserer; tre som hadde flyttet tjue, ville vært en ny rubrikk med gammelt navn. Tallet er derfor ført i addendumet selv, ikke bare her.
  * **Tvilen lå i passasjene, ikke i regelverket.** 29 av 48 saker faller utenfor alle tre reglene og måtte avgjøres på teksten alene. Det er grensen for hva en presisering kan gjøre: den rydder i tilbakevendende former, ikke i enkelttilfeller.
  * **Retningen på endringen er verdt å merke seg.** Den ene saken som flyttet seg, gikk fra ikke-treff til treff — altså oppover for presisjonen. Samtidig ligger alle nye tall innenfor konfidensintervallet fra før, så ingen konklusjon endres.
  * **ADR-0010 gjorde omregningen billig.** Fordi løftbarhet er en datert tilføyelseslogg, kunne 16 saker få en bekreftende vurdering og tre nye oppføringer komme til uten at noe eldre ble skrevet om. Sperren slo også inn der den skulle: PS-246 hadde alt en vurdering datert i dag, og den ble stående.
* **Gjort:** ADDENDUM-10 skrevet og commitet alene (med rettelse i §6 samme dag), de 48 avgjort i `data/port-tvil.jsonl` med regelhenvisning per sak, tallene regnet om, `docs/RESULTAT-PORT-v1.md` utvidet med før/etter-tabell uten å overskrive de gamle tallene, registeret oppdatert.
* **Filer:** `ADDENDUM-10.md`, `data/port-tvil.jsonl`, `data/port-presisjonssett-ADDENDUM10.jsonl`, `docs/RESULTAT-PORT-v1.md`, `register/claims.jsonl` (Vault).

## 21 Reglene reproduserer der hindringen er konkret, og svikter der den er et modellvalg (2026-09-25)

* **Målt:** enigheten mellom to uavhengige kodinger av de samme 320 passasjene. Koder 2 var en separat instans med tom kontekst, som bare fikk blindfilen og et ordrett regelutdrag; koder 1s verdikter, nøkkelfilen, dommerens utdata, LAERDOM, resultatnotatet og manuskriptet var sperret (ADDENDUM-11).
* **Tall:**
  * Treffbeslutningen: **κ = 0,812 [0,697–0,906]** over alle 320, **κ = 0,774 [0,623–0,898]** på portmaterialet alene. Rå enighet 96,2 % og 96,7 %.
  * Klasse blant de 30 passasjene begge kodet som treff: **κ = 0,732 [0,481–0,936]**.
  * **Per felt spriker det kraftig:** klinisk epidemiologi **1,000** (n = 52) · tekstvitenskap 0,847 (53) · arkeologi 0,748 (94) · **energimodellering 0,390** (101).
  * De tolv uenighetene om treffstatus fordeler seg **6 / 3 / 3**: seks der koder 2 kodet N3 (selvpålagt forenkling, metode- eller omfangsvalg), tre der koder 2 kodet N1 (besvart i samme passasje), og tre der koder 2 fant et treff koder 1 ikke fant.
  * Hovedfunnet står i begge lesninger: H7 er 17 av 25 (68 %) hos koder 1 og 12 av 19 (63 %) hos koder 2, og presisjonsintervallene 16,7 % [11,6–23,4] og 12,7 % [8,3–18,9] overlapper i hele sin bredde.
  * **M2 gjør det ikke: 88,0 % mot 31,6 %** på hver sin fasit.
* **Slutning:**
  * **Rubrikken er skarp der hindringen er konkret og uskarp der den er et modellvalg.** En kilde som ikke er bevart, en tillatelse som ble nektet, et utvalg som aldri ble samlet — det leser to kodere likt. Om en forenklingsantakelse forfatteren selv innførte, teller som navngitt hindring, leser de ulikt, og κ faller fra 1,00 til 0,39 mellom de to ytterpunktene. Prevalenstall for regnetunge felt arver den uskarpheten.
  * **ADDENDUM-10 §3 avgjør ikke det den ble skrevet for å avgjøre.** Den ble laget nettopp for modellbegrensninger, og halvparten av uenighetene ligger fortsatt der. En presisering som ikke flytter uenigheten, har ikke løst problemet — den har bare gitt det et navn.
  * **M2 er ikke operasjonalisert.** PREREG §2 sier «uten domeneekspert» uten å definere det. Koder 1 leste hindringens art, koder 2 fagets nåværende metodelandskap; begge er forenlige med ordlyden. Et mål som tåler to lesninger med faktor tre mellom seg, er ikke et mål ennå.
  * **Høy rå enighet beviser lite på skjevt materiale.** 96 % rå enighet ser sterkt ut helt til κ korrigerer for at begge kodere sier «nei» til det meste. Forskjellen mellom de to tallene er selve grunnen til å regne κ.
* **Gjort:** ADDENDUM-11 skrevet og commitet alene; `reliabilitet.py` med κ, asymptotisk SE og paret bootstrap, med test som viser fallgruven over; κ ført inn i manuskriptets metode, resultater og begrensninger; koder 2-kolonnen lagt til i resultatnotatet uten å erstatte koder 1.
* **Filer:** `ADDENDUM-11.md`, `data/port-presisjonssett-verdikter-koder2.jsonl`, `data/koder2-sammenlikning.json`, `src/gjenopptak/classify/reliabilitet.py`, `docs/MANUSKRIPT-v0.1.md`, `docs/RESULTAT-PORT-v1.md`.

## 22 Grønt som ikke alltid er grønt: en rekkefølgeavhengig test (2026-09-25)

* **Målt:** testsuiten feilet én gang på `test_armering_den_gamle_algoritmen_mister_kroppen` (JATS-parsing), og var grønn i tre påfølgende kjøringer etterpå og grønn når testen kjøres alene.
* **Tall:** 1 feil av 4 fulle kjøringer, 0 feil av 1 isolert kjøring. Suiten kjører med `pytest-randomly`, altså ny rekkefølge hver gang.
* **Slutning:**
  * **Feilen er testforurensning, ikke et funn i materialet** — men den hører hjemme i samme familie som de ti tilfellene i seksjon 10: en komponent som melder grønt uten at grønt betyr det samme hver gang.
  * En suite med tilfeldig rekkefølge og delt tilstand gir et *stokastisk* kvalitetssignal. «336 grønne» er da ikke én påstand, men én trekning. Det er greit så lenge det sies, og villedende så lenge det ikke gjør det.
  * Tiltaket er ikke å slå av tilfeldig rekkefølge. Det er å finne den delte tilstanden — å skru av randomiseringen ville skjult nøyaktig det signalet som avdekket den.
* **Gjort:** feilen er ført her i stedet for å bli rapportert bort. Den delte tilstanden er ikke funnet ennå; testen er ikke markert eller deaktivert.
* **Filer:** `tests/test_jats_parse.py`, `pyproject.toml` (`addopts = "-q -m 'not network'"`, `pytest-randomly` aktiv).

## 23 En indikator er ikke tilstanden: seks avledningsfeil (2026-09-26)

* **Målt:** seks tilfeller i dette sporet der noe utledet ble ført som et faktum, og hva som felte dem. Ingen ble felt av selvsjekk; alle seks av et uavhengig oppslag mot kilden.

| # | påstanden | indikatoren den ble utledet av | kilden som felte den | hva kilden sa |
|---|---|---|---|---|
| 1 | **BAGELS** som referanse for uttrekk av limitations | navnet sto i oppdraget og ble gitt videre gjennom flere slynger | arXiv- og Crossref-søk | ingen slik publikasjon finnes; treffene er akseleratorfysikk og agent-bootstrapping |
| 2 | forfatternavnet **«Bottenvik-Nicolaysen»** i CITATION.cff og lisensfilene | brukernavnet `eirikbottennicolaysen` | ORCIDs offentlige API | «Eirik Botten Nicolaysen» |
| 3 | Heron-vurderingens dato **2019-01-01** | publiseringsåret 2019 i metadata | avhandlingens tittelblad; OpenAlex har ingen `publication_date` | «November 2019» — måned, ikke dag |
| 4 | presisjon i arkeologi **18,0 %** for koder 2 | hukommelse fra en tidligere tabell | `koder2-sammenlikning.json` | 22,0 % |
| 5 | **«åtte av tolv»** uenigheter gjelder samme strid | inntrykk av mønsteret, aldri talt | opptelling i samme fil | 6 / 3 / 3 |
| 6 | ORCID **«ikke koblet»** til OSF-kontoen | API-feltet `social.orcid` var tomt, og API-et avviste verdien | nettleseren, Settings → Account | koblingen lå i Connected Identities hele tiden |

* **Tall:** **fem av seks sto i et dokument før de ble felt.** BAGELS i det commitede manuskriptet (`ee64211`), navneformen i tre filer over to commits, den oppdiktede datoen i registeret over to commits, «åtte av tolv» i fire dokumenter over tre commits — og to av dem var alt bundlet til Vault. Bare arkeologiprosenten ble tatt før den nådde en commit. Ingen av de seks nådde en ekstern publisering, men to ble felt først i frys-lesningen rett før innsending.
* **Slutning:**
  * **Fellesnevneren er én bevegelse: en indikator ble lest, og tilstanden bak den ble sluttet.** Et tomt API-felt ble til «ikke koblet». Et publiseringsår ble til en dag. Et brukernavn ble til et etternavn. Et mønster i en liste ble til et forholdstall. I hvert tilfelle var indikatoren riktig lest — det var slutningen fra den til verden som ikke holdt.
  * **Dette er motsatt kant av seksjon 10 og 22.** Der meldte en komponent grønt og var feil: systemet løy. Her meldte systemet sant, og vi leste meldingen som noe mer enn den var. Begge feilklasser gir samme utfall — en påstand i et dokument som ikke svarer til verden — men de krever ulike mottiltak. Mot det første hjelper uavhengig måling. Mot dette hjelper bare å slå opp.
  * **Regelen: en indikator er ikke tilstanden.** Før en avledet verdi føres i et dokument, slås den opp i kilden som faktisk bærer den. Et tomt felt betyr at feltet er tomt. Et årstall betyr at året er kjent. Et navn i en sti betyr at stien heter det.
  * **Kostnaden ved å ta feil er ikke symmetrisk.** En oppdiktet presis dato er verre enn en grov, fordi den ser etterprøvbar ut; «åtte av tolv» er verre enn «de fleste», av samme grunn. Avledningen gjør påstanden skarpere enn grunnlaget, og skarpheten er det leseren stoler på.
  * **Frys-lesning før utadvendt tekst er der dette faktisk tas.** To av seks ble felt der, etter å ha stått i commitede dokumenter i dager. Uten det steget ville begge gått ut.
* **Gjort:** alle seks er rettet i kilden, og de som sto i låste eller deponerte dokumenter, er rettet som daterte tillegg (ADDENDUM-10 §6, ADDENDUM-11 §7) framfor stille redigering.
* **Filer:** `docs/MANUSKRIPT-v0.1.md`, `CITATION.cff`, `register/claims.jsonl` (Vault), `docs/RESULTAT-PORT-v1.md`, `ADDENDUM-11.md`, `docs/PREPRINT.md`.

## 24 Frys-lesning per fil fanger ikke tall som er foreldet på tvers (2026-09-26)

* **Målt:** om dokumentsettet var internt konsistent etter ADDENDUM-10 og ADDENDUM-11. Det var det
  ikke, og feilen lå ikke i noen enkelt fil.
* **Tall:** `docs/RESULTAT-PORT-v1.md` bar **elleve** foreldede størrelser i seksjonene over
  oppdateringstabellen: hovedfunnet 17 av 24 (71 %) mot gjeldende 17 av 25 (68 %), M1-korrigert
  0,652 mot 0,671, M2 87,5 % mot 88,0 %, presisjon 16,0 % mot 16,7 %, løftbar andel 4 av 24 (16,7 %)
  mot 5 av 25 (20,0 %), letekostnad ~37 mot ~30 dømte treff per løftbart, «48 tvilstilfeller
  uavgjort» etter at de var avgjort, «alle fire løftbare prøvd» etter at det femte var kommet til,
  og forbehold 1 «Én koder» etter at det var to. Abstract, manuskript og faktaark sa 68 % samtidig.
  Ingen av tallene var gale da de ble skrevet; alle var gale som gjeldende.
* **Slutning:**
  * **Feilen er en oppdateringsform, ikke en regnefeil.** ADDENDUM-10 §5 lovet at avledede tall
    «regnes om i `docs/RESULTAT-PORT-v1.md`, der tallene før ADDENDUM-10 blir stående ved siden av
    de nye». Det ble gjort — men **bare i en ny tabell nederst**, ikke i seksjonene som hadde
    tallene. En leser som starter øverst, møter aldri tabellen.
  * **Frys-lesningen før deponering leste hver fil for seg.** Hver fil var konsistent med seg selv,
    og derfor bestod alle. Det som ikke ble lest, var samme størrelse *på tvers* av filer — og det
    er der avviket lå. Kontrollen må være: samme størrelse, samme verdi i alle filer som deponeres,
    eller merket med hvilken versjon den tilhører.
  * **Et tillegg som bare legger til, etterlater motsigelsen.** ADDENDUM-10 og -11 er begge
    append-only av gode grunner. Men når et tillegg endrer et tall, må hvert sted tallet står,
    enten oppdateres eller merkes. Ellers er dokumentet sant i deler og usant som helhet.
  * **Daterte logger er unntaket, og må si det selv.** § 16 og § 17 her er ikke rettet — de er
    referat fra 20. og 21. september. De har fått en peker til gjeldende tall i stedet, fordi en
    logg som rettes i ettertid slutter å være en logg.
* **Gjort:** elleve tall rettet i resultatnotatet med det gamle merket «før ADDENDUM-10» i samme
  setning eller rad; koderidentitet på alle tall som bærer den; pekere i § 16 og § 17;
  kryssdokumentsjekk kjørt over alle filer som deponeres; v0.3.0 deponert.
* **Filer:** `docs/RESULTAT-PORT-v1.md`, `docs/LAERDOM.md`, `CITATION.cff`, `docs/ZENODO.md`.

## 25 Et nullresultat teller bare der søket kunne ha truffet (2026-09-26)

* **Målt:** om de tre Heron-håndskriftene har et surrogat utenfor British Library. Elleve kilder ble
  prøvd. Det viktigste som kom ut av det, var ikke svaret, men **hvor ofte et «nei» ikke var et nei.**
* **Tall:**

| kilde | kontroll | utfall |
|---|---|---|
| Dumbarton Oaks MMDB | «Add. 36749» 1 post · «Harley» 10 · «Burney» 2 | **ekte null** — 0 av tre |
| RGK 1a/2a/3a | «Harl» 104 · «Burn» 36 · «Paris» 59 · «Vat» 1578 | **ekte null** — 0 på begge signaturer og på kopistnavnet |
| ARCAs cote-søk | «5605» ga BnF Latin 5605; London+«108» ga 2 | **ekte null** for Harley 5589, **treff** for de to andre |
| ARCAs fritekstsøk | «Marcianus 516» → INTERNAL ERROR | **utestet** |
| BL-katalogens `Surrogates`-fasett | fasetten alene → HTTP 500 | **utestet**, andre gang |
| RGK 1c (plansjebindet) | «Kopist», «Lond», «Tafel» alle 0 | **utestet** |
| Biblissimas frasesøk | `"Harley 603"`, `"Harley 2506"`, `"Burney 19"` alle 0 | **ubrukelig syntaks** — nullene forkastet |

* **Slutning:**
  * **Tre kilder svarte feil på både målsøket og kontrollen, og er ført som utestet — ikke som
    fravær.** Uten kontrollen ville alle tre blitt lest som «finnes ikke», og kartleggingen ville
    konkludert med at ingen surrogater eksisterer noe sted. Det er den samme feilformen som i § 23:
    en indikator (tomt søkeresultat) ble nesten lest som en tilstand (ingenting finnes).
  * **To ga ekte null, og de er verdt mer enn de ni andre til sammen.** Dumbarton Oaks-kontrollen
    traff på *samme fonds* — åtte Harley-filmer og to Burney-filmer — så et treff på våre ville vært
    synlig. Der nullen er armert på nabomaterialet, er den nesten like sterk som et treff.
  * **Kontrollen må ligge nær målet.** «Harley» generelt var en bedre kontroll enn «Add. 36749»,
    fordi den prøver samme signaturform. I RGK avslørte kontrollen dessuten at katalogen bruker
    «Lond. Harl. 5536»: uten den ville søket på «Harley 5605» gitt null av rene ortografiske grunner.
  * **Et søk som virker, men med gal syntaks, er farligst.** Biblissima svarte 200 og «0 results» på
    hver frase, også på kontrollene. Et ødelagt søk som *ser* ut som et tomt søk, gir null uten
    feilmelding — og konklusjonen måtte derfor bygges på samlingens omfang i stedet.
  * **En gjenåpning er ikke gratis, men den er billig.** ARCAs fritekstsøk var nede i forrige økt og
    er nede nå; men **cote-søket, som ikke var prøvd, virket** — og det var der de to postene lå. Da
    en kilde svarer feil, er neste steg å prøve dens *andre* inngang, ikke å føre den som tom.
* **Gjort:** hver kilde i `docs/HERON-KOLLASJON-VURDERING-v2.md` er ført med kontroll og utfall, og
  de utestede står i egen seksjon (§ 9) atskilt fra dem som ikke ble søkt i det hele tatt (§ 10).
  Registerets vurdering av 2026-09-26 siterer kartleggingen som kilde.
* **Filer:** `docs/HERON-KOLLASJON-VURDERING-v2.md`, `register/claims.jsonl` (Vault),
  `docs/HERON-KOLLASJON-VURDERING-v1.md` (superseded, uendret).

## 26 Et sorteringskriterium må testes mot om det sorterer, ikke mot at det kjører (2026-09-26)

* **Målt:** om 229 dømte løftbare treff kunne rangeres maskinelt på gjennomførbarhet. Kriteriet ble
  låst før tallene ble sett, kjørte uten feil, ga en pen fordeling — og **sorterte ikke.**
* **Tall:** topp 15 etter rang ga **2 ekte treff = 13,3 %**, mot **16,7 % [11,6–23,4]** målt på et
  tilfeldig stratifisert utvalg. Punktanslaget ligger *under* det usorterte. **89,5 %** (205 av 229)
  falt på ett enkelt signal: passasjen henviser ikke til materiale. Av de fire signalene var
  **to ubrukelige**: datatilgangssignalet kunne ikke skille forfatterens data fra tredjeparts data
  nevnt i teksten (7 av 15 arvet full score på fraser om British Geological Survey og Met Office), og
  siteringssignalet kunne ikke regnes i det hele tatt fra frosset materiale.
* **Slutning:**
  * **Kriteriet bestod alle testene jeg hadde skrevet, og ingen av dem målte det som skulle måles.**
    Det var låst før tallene, dokumentert, reproduserbart og kjørte på 229 rader uten en feil. Alt
    det er nødvendig og ingenting av det er tilstrekkelig. **Den ene testen som betyr noe, er om
    topp-*n* har høyere treffrate enn et tilfeldig utvalg** — og den kan bare kjøres ved å lese, altså
    ved å gjøre arbeidet rangeringen skulle spare. Det er en kostnad som må tas én gang, ikke unngås.
  * **Dette er en egen feilklasse, ved siden av § 10, § 22 og § 23.** Der handlet det om en komponent
    som meldte grønt uten å være det, en test som var rekkefølgeavhengig, og en indikator lest som en
    tilstand. Her er selve *målet* feil valgt: jeg validerte at kriteriet var etterprøvbart framfor at
    det var informativt. Et kriterium kan være fullstendig gjennomsiktig og fullstendig ubrukelig
    samtidig.
  * **Et signal må prøves mot sin egen motsats før det brukes.** «Finnes ordet *tilgjengelig* i
    verket» ser ut som datatilgang og er det ikke. Prøven som ville avslørt det, er å spørre: hvilken
    *annen* grunn kan få dette signalet til å fyre? Her var svaret at forfatteren omtaler andres data —
    og det er ikke et sjeldent unntak, det er normalen i metodeavsnitt.
  * **Et signal som ikke kan regnes, skal stå som ukjent og prises.** `cited_by_count` fantes ikke på
    disk. Alternativene var å gjette, å droppe signalet stille, eller å føre det som ukjent med prisen
    for å fylle det: ~2 060 kreditter. Det siste er det eneste som holder, fordi det lar den neste
    lesningen vite hva den mangler.
  * **Negativt resultat om egen metode er et resultat.** Triagen er ført som ADDENDUM-12 og i
    manuskriptets diskusjon med tallene, ikke som en mislykket kjøring som ble stille borte. Det den
    avdekker, er dessuten sterkere enn det den skulle vise: **passasjen navngir hindringen, ikke
    ressursen**, og det er en grense for klassen av verktøy, ikke for denne implementasjonen.
* **Gjort:** ADDENDUM-12 skrevet og committet alene; de to ekte treffene ført i registeret med DELVIS
  materialtilgang og klassen på det ene rettet fra dømt H6 til H5; de 214 uleste står uleste, og de 15
  leste er merket som ikke-tilfeldige og skal aldri regnes inn i presisjonen.
* **Filer:** `ADDENDUM-12.md`, `triage-loftbare-2026-09-26.json` og
  `triage-loftbare-2026-09-26-kriterium.py` (Vault), `register/claims.jsonl` (Vault),
  `docs/MANUSKRIPT-v0.1.md`.

## 27 Et førsteledd måles på halen, ikke på medianen (2026-09-26)

* **Målt:** om semantisk likhet mot 55 kjente treff kan kutte 22 243 passasjer ned til noe en dommer
  kan se på. Modellen er flerspråklig av nødvendighet, kjøringen gikk feilfritt, og signalet er ekte.
  **Førsteleddet finnes likevel ikke.**
* **Tall:** AUC **0,711** (maks mot enkeltfrø) og **0,750** (mot sentroiden), mot 0,50 for tilfeldig.
  Median persentil for de 25 ekte treffene: **11,8 %** for den beste varianten. Men **verste treff
  ligger på 85,7 %**, og derfor: for å beholde 90 % av treffene må dommeren se **62–72 %** av
  materialet — faktor **1,4–1,6**, **14,6–16,9 timer av 23,5**. Ved markørlistens eget driftspunkt
  (230 kandidater, 1,0 %) fanger embeddingene **2 av 25**, akkurat som markørlisten.
* **Slutning:**
  * **Medianen lovet noe halen ikke holdt.** En rangering der halvparten av treffene ligger i øverste
    tolvdel, ser ut som et brukbart filter. Den er det ikke, fordi et filter ikke måles på hvor de
    fleste treffene havner, men på **hvor det verste havner**. Recall er et minimumskrav, ikke et
    gjennomsnitt, og det er halens plassering som setter kuttpunktet.
  * **Spør etter kostnaden ved kravet, ikke etter tallet ved kuttpunktet.** «48 % recall i topp 10 %»
    høres ut som et resultat. «For 90 % recall må du lese to tredeler» er samme måling lest riktig.
    Den andre formen er den som avgjør om verktøyet skal bygges, og den var like billig å regne ut.
  * **Signal og nytte er to ting.** AUC 0,75 er ikke støy. Men avstanden fra «bedre enn tilfeldig» til
    «kan kutte 99 % av materialet uten å miste treff» er flere størrelsesordener, og et prosjekt som
    feirer det første, har ikke målt det andre.
  * **Modellvalget måtte måles, ikke antas.** Materialet er **27,7 % klart ikke-engelsk** (fransk
    13,1 %, spansk 12,0 %, tysk 2,7 %). En enspråklig embedding-modell ville vært blind på over en
    fjerdedel — nøyaktig samme feilform som de engelske bildetekstene i § 26s oppfølger. Tellingen tok
    ett minutt og avgjorde valget; antakelsen ville vært gratis og gal.
  * **Den negative målingen var billig, og det er hele poenget.** Embedding av alt kostet **16,5
    minutter** mot dommerens 23,5 timer — 1,2 %. Et førsteledd som skal spare mye, kan prøves for
    nesten ingenting, og da er det uforsvarlig å anta i stedet for å måle.
  * **To varianter, to målinger, ingen forbedring.** A og B står ved siden av hverandre. Å rapportere
    B som «forbedringen» ville gjort et aggregeringsvalg til et framskritt, og neste gang ville
    terskelen for hva som teller som framgang vært flyttet uten at noe var målt.
* **Gjort:** ADDENDUM-14 skrevet og committet alene, med modellsignatur, recall ved seks kuttpunkter,
  kostnadstabellen, sammenligningen mot markørlisten og hva målingen ikke viser. Embeddingene ligger på
  Vault og kan brukes til rangering *innenfor* en alt filtrert mengde — det de ikke kan, er å lage
  mengden.
* **Filer:** `ADDENDUM-14.md`, `embeddings/{port-bge-m3.npy, froesett-bge-m3.npy, port-index.json,
  kjoring.json, maaling.json}` (Vault).

## 28 Kryssjekken slapp gjennom fordi filen lå utenfor settet (2026-09-26)

* **Målt:** kryssjekken leste tolv håndplukkede filer og meldte null avvik. Utvidet til å oppdage
  filsettet fra disk leste den **40** filer og fant **fire** foreldede verdier med én gang — blant dem
  «Én koder» i PREREG-v1 §4 og ADDENDUM-06, innhentet av ADDENDUM-11 siden 25. september.
* **Slutning:** en vokter med håndskrevet filliste vokter listen, ikke dokumentsettet. **Det som ikke
  er i settet, kan ikke feile** — og en grønn kjøring blir da en påstand om utvalget, ikke om
  materialet. Settet globbes nå, og to regler fulgte av de første treffene: låste filer hoppes over,
  fordi de er daterte referat som skal rettes med korrigendum i egen fil framfor redigering, og en
  linje som daterer verdien selv med ISO-dato, regnes som merket.
* **Filer:** `src/gjenopptak/kryssjekk.py`, commit `42f8419`.

## 29 Fire kontroller som meldte grønt eller stille, og regelen som følger (2026-09-26)

* **Kanarisjekken godtok tom streng som delstreng**, og meldte grønt på en kjøring uten en eneste
  `Q:`-linje — den tomme strengen er delstreng av alt.
* **`prompt_eval_count == num_ctx` er stille trunkering, ikke «ryddig fullt».** Første kanarikjøring ga
  nøyaktig 4096 av 4096, og halen av vinduet — der kanarisetningen sto — var kuttet bort.
* **`pdftotext` manglet 7 av 25 fasit-tekstbiter.** Fanget av en forkontroll som lette etter fasiten i
  tekstkilden *før* kjøring; ruten ville ellers dødd på parseren framfor på hypotesen.
* **Speilet meldte «1 bak» fordi en ny fil ikke var i `PLIKT`.** Fanget ved å følge METODE.md sine egne
  kommandoer etter å ha skrevet dokumentet.
* **```json-gjerder ga falsk «0 av 48».** Dommerens svar ligger i en kodegjerde, og min
  rapportkode testet `raasvar.startswith("{")`. Den meldte at dommeren flagget null av 48 Q-linjer; det
  riktige tallet var 22 av 55. Et parsefeil som gir et *rundt* tall, ser ut som et funn.
* **Regelen som følger av de tre første: en sjekk testes med et tilfelle den skal FEILE på, ikke bare
  ett den skal bestå.** En kanarisjekk som aldri er kjørt mot utdata uten kanarisetning, har ikke
  bevist at den kan se forskjellen. Det samme gjelder en trunkeringssjekk som aldri har møtt et vindu
  som faktisk er for langt.

## 30 Alt en låst måling leser, låses med den (2026-09-27)

Tre feil i samme sak, alle mine, på én dag.

**(a) Inndata til en låst måling lå bare i scratchpad.** κ = 0,812 er sporets eneste
reliabilitetsmåling — den står i manuskriptet, resultatnotatet, to Zenodo-versjoner og ADDENDUM-11.
Regelfilen koder 2 leste for å komme dit, `koderegler.md`, ble aldri committet. Den lå i en
tmp-katalog som siden ble tømt. Verdiktene var bevart, blindfilen var bevart, koden var bevart — men
*det koderen leste for å avgjøre* var ikke. Og ADDENDUM-11 oppgav verken sti eller sha, bare en
beskrivelse, så det fantes ikke engang noe å lete etter navnet på.

**(b) Filnavnsøket meldte tomt. Innholdssøket fant. Tomt er ikke fravær.** Jeg søkte i repoet over alle
refs, på Vault og i scratchpad, på filnavn med «regel», «regl», «rules» — null treff — og skrev at
**κ = 0,812 ikke kan reproduseres på sin egen inndata**. Det var galt. Filen fantes som *innhold* i
CCs øktutskrifter: to distinkte setninger som måtte opptre i samme fil — «avledes aldri fra en modell»
(PREREG-v1 §5) og «den undersøkelsen artikkelen rapporterer» (ADDENDUM-04 §4) — ga **ett treff blant
686 utskriftsfiler**, og det var koder 2s egen økt. Hele filen sto i Read-resultatet.
**Samme feil, samme dag, en gang til:** jeg slo fast at `MANIFEST-VAULT.md` «ikke finnes i dette
repoet» etter å ha kjørt `find` i repoet. Filen ligger på Vault, 493 083 B, og har alltid gjort det.
Begge gangene var søket riktig utført og stedet feil. **Et nullresultat teller bare hvis søket kunne
ha truffet** — og det gjelder ikke bare armerte kontroller i studien, det gjelder mine egne søk etter
filer.

**(c) «Koder 2 (menneske)» — en merkelapp fra ingenting.** Jeg satte ordet «menneske» i en tabell der
κ = 0,812 sto ved siden av modell-κ. Ingenting på disk sier det: ADDENDUM-11 §3.1 sier ordrett «Ingen
menneskelig annotør har vurdert materialet», og RESULTAT-PORT, ADDENDUM-18 §5, ADDENDUM-19 §5 og
INNHENTET-notatet sier det samme. Merkelappen kom fra at 0,812 var *høy* — jeg leste tallet som en
egenskap ved koderen og fylte inn hva koderen måtte være. **Den nådde ikke disk fordi eieren stoppet
den i samme omgang, ikke fordi noen sjekk fanget den.** Det er ikke en betryggende grunn. En
grep-runde over repoet og Vault viste etterpå at ikke én fil bar feilen; hele avviket var i
rapporten min.

**Regelen: alt en låst måling leser, låses med den.** Blindfil, regelfil, ledetekst, sperreliste,
modellsignatur — i samme commit som tallet, med sha256, på Vault og ikke i tmp. Verdiktfiler er ikke
nok; forutsetningen er også data. En sperreliste kan verifiseres i ettertid, en formulering kan ikke.

**Hva gjenvinningen ga, og hvorfor den ikke er en unnskyldning.** Den ga tre ting dokumentasjonen ikke
hadde: ADDENDUM-11s lekkasjepåstand er nå *verifisert* (0 treff på presisjonstall, PS-id-er, M1/M2, κ)
i stedet for hevdet; den forutsagte defekten i ADDENDUM-05-utdraget er bekreftet med riktig antall
(tre manglende tabellrader); og en defekt ingen visste om kom fram — blokken er limt inn som
`grep -n`-utdata, så **formen fortalte koder 2 hvilke linjer et søk hadde truffet på**. Modell-ID
(`claude-opus-5`) og kostnad (61 kall, 20 min, 9 019 781 tokens inn) kom med samme utskrift, og
reparerte et ADR-0003-brudd i ettertid. Men alt dette var flaks: tmp var tømt, og bare utskriften
overlevde. **Flaks er ikke en sikringsrutine.**

**Filer:** `docs/REGELFIL-KODER2-GJENVUNNET-2026-09-27.md`, `koder2/koderegler-gjenvunnet.md` og
`MANIFEST-VAULT.md` seksjon «Koder 2-gjenvinning» på Vault, `ADDENDUM-11.md` §8, `docs/METODE.md` §4.

## 31 En regel som bare finnes som prosa, er ikke en regel (2026-09-27)

* **Målt:** om G3-regelen kan reproduseres fra sin egen dokumentasjon. Utdatafilen
  `ekstraksjon/2026-09-26/g3-ikke-prosa.json` fører regelteksten ordrett — «under 50 % bokstaver ELLER
  referansemønster (årstall+sidespenn, nummerrekke «50. 51. 52.», initialrekke, pp. n–m)» — men
  implementasjonen lå i en kladdefil som ikke ble bevart.
* **Tall:** reimplementert fra regelteksten gir **5 455 mot 6 098** ikke-prosa av 22 243 passasjer
  (−643), **453 mot 490** av de flaggede (−37), **3 mot 1** av de 25 fasit-treffene (+2), og **47 mot
  19** av de leste portpassasjene (+28).
* **Slutning:** avvikene går i **begge retninger**, så reimplementasjonen er ikke en strammere eller
  slappere utgave av samme regel — den er **en annen regel**. Regelteksten er ikke presis nok til å bære
  tallet: «under 50 % bokstaver» sier ikke av hva (alle tegn, ikke-blanke tegn, tegn utenom tall), og
  «referansemønster» sier ikke hvilke uttrykk. **Hvilken av de to som er den formulerte, kan ikke
  avgjøres**, fordi originalen ikke finnes. Tallet 27,4 % står i patchen § 4 og ADDENDUM-19 § 5 og er nå
  merket som ikke reprodusert.
* **Gjort:** regelen ligger i repoet som `src/gjenopptak/classify/ikkeprosa.py` (sha256 `63ed734555a8bc95…`) med
  regeltekst og reproduksjonshistorie i modulhodet, slik at neste tall er låst til en implementasjon. En
  prosabeskrivelse er dokumentasjon; **kode er regelen.** Dette er tredje gang samme dag at noe som
  avgjorde et tall bare fantes utenfor versjonskontroll — jf. [[§30]].
* **Filer:** `src/gjenopptak/classify/ikkeprosa.py`, `ekstraksjon/2026-09-26/k-union.json`,
  `docs/MASTER-PATCH-2026-09-26.md` § 4.

## 32 Leverandørens øktgrense er en ressurs som må budsjetteres som tokens (2026-09-27)

* **Målt:** jeg startet sju Opus-instanser samtidig for å kode 2 488 passasjer parallelt i stedet for
  sekvensielt. Alle sju falt på **HTTP 429, «You've hit your session limit»**, etter til sammen 87,2 %
  dekning. Tre av åtte økter ble komplette; fem ble avbrutt midt i.
* **Og en feil til, i samme grep:** tre instanser rapporterte **filkollisjoner i delt kladdekatalog**, og
  én at visningen av postene 14–40 kom fra en **annen økts blindfil**. Kontrollen viste null fremmede
  id-er i utdata, og justeringstesten (95–98 % av ikke-prosa kodet `INGEN`, null korte tallrester som
  treff) viste at de komplette øktene leste sitt eget materiale. Men det var flaks at kollisjonene traff
  hjelpeskript og ikke verdikter. **Parallelle instanser må ha isolerte kladdekataloger, oppgitt i
  oppdraget.**
* **Slutning:** jeg budsjetterte tokens (73,7 M, målt) og glemte at kall/tid mot en **øktgrense** er en
  annen og hardere skranke. Sekvensielt ville åtte økter tatt ~4 timer og levert; parallelt tok det 20
  minutter og leverte 3 av 8. **Regelen: når arbeidet deles i n instanser, er n begrenset av
  leverandørgrensen, ikke av hva maskinen orker.** Ved usikkerhet: kjør sekvensielt, mål første enhet, og
  øk parallelliteten først når grensen er kjent.
* **Filer:** `ADDENDUM-22.md` §9.1, `arbeidsliste/okt-*-verdikter.jsonl`.

## 33 En port satt på kjente treff måler fasiten like mye som leseren (2026-09-27)

* **Målt:** porten i ADDENDUM-22 §6 krevde at leseren skulle bekrefte ≥ 22 av 27 kjente treff. Den
  bekreftet **17**, og med fire ennå ikke dømt er taket **21**. Porten falt.
* **Tall:** alle seks mistede er merket `tvil: true` av koderen selv. **Fire av seks var allerede blant
  koder 2s tolv uenigheter med koder 1.** Koder 1s egne notater sier «klassen er usikker», «derav tvil»
  eller `bedømbar: nei` på fem av de seks. To mønstre bærer alle seks: «hindringen tilhører feltet eller
  tredjepart, ikke arbeidet» (ADDENDUM-04 §4 anvendt i motsatt retning) og «besvart i samme passasje»
  kodet `N1`.
* **Slutning:** jeg leste porten som en test av leseren. Den er også en test av **fasiten**. Når 4 av de
  6 tapene er passasjer en tidligere uavhengig koder også var uenig om, og 5 av 6 er merket usikre av
  koder 1 selv, måler porten hvor stabile de kjente treffene er under gjenlesning — ikke bare hvor god
  leseren er. **En port bygget på et referansesett arver referansesettets ustabilitet**, og terskelen må
  settes med den i hånd: 22 av 27 forutsetter at 27 er stabile, og de er ikke det.
* **Hva som ikke ble gjort:** porten ble ikke senket, terskelen ikke flyttet, og ingen liste skrevet.
  Utfallet står som det ble målt. Det riktige neste spørsmålet er ikke «hvorfor fant leseren bare 17»,
  men «hvor mange av de 27 er stabile nok å være en port».
* **Filer:** `ADDENDUM-22.md` §9.2, `ADDENDUM-11.md` §7, `data/koder2-sammenlikning.json`.

## 34 `max_tokens` er en målegrense, ikke bare en kostnadsgrense (2026-09-27)

* **Målt:** ADDENDUM-19 kjørte Opus 5 med `max_tokens = 300`. Av 320 svar var 36 uparsebare, og **alle 36
  hadde `output_tokens` = 300** — nøyaktig taket. 23 av dem var helt tomme, fordi hele budsjettet gikk før
  noen tekst kom ut. Median utdata for de gyldige svarene var **95** tokens, 95-persentilen 239.
* **Tall som avgjør saken:** **27 av koder 1s 39 treff (69 %) ligger i det avkuttede settet.** Taket bandt
  bare halen, og halen var systematisk: de passasjene modellen skrev langt om, var treffene. κ = 0,390
  målt på de 284 parsebare er derfor målt på et delsett som mangler to tredeler av det som skulle måles.
* **Samme feil traff et tall som alt var rapportert.** ADDENDUM-18s Sonnet pass 1 hadde 13 uparsede, og
  **12 av dem var avkuttet**. κ = 0,321 var altså også målt uten dem. Det ble oppdaget først da jeg
  sjekket avkutting *på tvers av alle kjøringer* i stedet for bare i den som åpenbart feilet.
* **Hvorfor det var usynlig:** loggformatet lagret `usage`, men **ikke `stop_reason`**. En avkutting er
  synlig i API-svaret og ble ikke ført. Uten det måtte avkuttingen påvises indirekte, med
  `output_tokens` mot taket — som fungerer, men bare fordi taket er kjent.
* **Slutning:** et tak som binder halen er ikke en kostnadsinnstilling, det er et **utvalgsfilter på
  utdata**, og det filtrerer på nøyaktig den egenskapen som ofte korrelerer med utfallet — svarlengde.
  **Regelen: sett taket minst en størrelsesorden over målt 95-persentil, og loggfør `stop_reason` per
  kall.** Og når én kjøring viser avkutting, sjekk alle kjøringer med samme tak, ikke bare den som
  feilet.
* **Filer:** `ADDENDUM-19.md` §3b, `ekstraksjon/2026-09-26/addendum-19/opus5-dommer.jsonl` (ugyldig,
  beholdt), `addendum-18/*-avkuttet-rekjort.jsonl`.

## 35 En tjeneste som svarer 200 på et sted som ikke finnes, gjør bom til treff (2026-09-27)

* **Målt:** SAK-14 slo opp 76 unike greske referanser mot Perseus Hopper og Scaife Viewer. Begge
  tjenestene svarer **HTTP 200 med en annen passasje** når referansen ikke finnes: `Lib. 37` ga `20`,
  `Lib. 10.37` ga `10.67`, `Hann. 114` ga `9`, `AR 2.31.41` ga `2.31.3`. Ingen feilkode, ingen
  advarsel, gresk tekst i svaret.
* **Tall:** **11 av 90 steder** er tilbakefall eller utenfor utgaven. Uten en nivå-for-nivå-
  sammenligning av det forespurte mot det returnerte ville alle elleve blitt ført som treff, og
  saken stått som **opphevet på 100 %** i stedet for **ikke opphevet på 87,8 %**. Porten ville
  snudd på en feil ingen logg viste.
* **Slutning:** en oppslagstjeneste er ikke en orakel som sier «finnes ikke». Den er en funksjon som
  alltid svarer noe. **Regelen: les den oppløste adressen ut av svaret og sammenlign den med den
  forespurte, nivå for nivå, før innholdet brukes til noe.** Hopper oppgir den i
  `addDocument('…')`, Scaife i `urn`-feltet. Et svar uten oppløst adresse er et ikke-treff, ikke et
  tomt treff.
* **Gjort:** `hent.py`/`hent2.py` avgjør status som `opplost` bare når hvert nivå stemmer og det
  finnes minst én gresk ordform; alt annet er `tilbakefall`, `tom` eller `utenfor_verket`.
* **Filer:** `saker/SAK-14/hent.py`, `hent2.py`, `oppslag.json`, `tabell.json`,
  `docs/saker/SAK-14/RESULTAT.md`.

## 36 Et umålt nulltall overlever en skjemastramming (2026-09-27)

* **Målt:** register v2 (432 rader) ble validert mot `kandidat.schema.json` fordi `sak`-feltet skulle
  settes på to rader. **Registeret validerte ikke.** To felt manglet på **alle 432 rader**:
  `sil.presisjon_ki`, og `status` i `cites_coverage` — der tallene sto som
  `fulltext_available: 0, fulltext_total: 0`.
* **Tall:** `falsified` er `false` på alle 432. Falsifiseringsleddet ga aldri et tall for kjøringen,
  men registeret rapporterte **0 av 0** — som leses som «ingen siterende fulltekst fantes».
  Skjemaets egen beskrivelse advarer mot nøyaktig dette: «Uten måling er den «ikke målt», ALDRI 0 —
  et umålt nulltall var ett av de ti grønn-og-feil-tilfellene.»
* **Slutning:** skjemaet ble strammet i B3, men **materialet som alt var produsert, ble ikke kjørt
  gjennom det**. En stramming som ikke valideres bakover, fanger bare framtidige rader. **Regelen:
  når et skjema strammes, valider alt eksisterende materiale mot det i samme arbeidsøkt — ellers er
  strammingen en hensikt, ikke en kontroll.**
* **Gjort:** `presisjon_ki` fylt fra `kjede.toml` etter kontroll av at `presisjon` stemte eksakt for
  alle tre silkilder; `cites_coverage` satt til `status: "ikke målt"` med `null` på alle tre tallene.
  Ingen ny måling. `register_sha256` `aa8f7c2e…` → `6caabaff…`, hodet bærer en `rettet`-linje.
* **Filer:** `kandidat432/8-register.jsonl`, `8-register-header.json`,
  `docs/saker/REGISTER-SAKER.md`.

## 37 En port med to ledd må si hva som skjer når det andre ikke kan måles (2026-09-27)

* **Målt:** SAK-14s port krevde at «≥ 90 % av stedene får gresk tekst **med de bærende termene
  identifisert**». Presisering 3 definerte den bærende termen mot «det franske uttrykket
  avhandlingen bygger sin påstand på i den setningen».
* **Tall:** avhandlingen gjengir gresk ordrett bare på **11 av 90 steder** (12,2 % [7,0–20,6]). For
  de øvrige 79 fantes det ikke noe fransk uttrykk å måle termen mot, og **det andre leddet i porten
  var umålbart for 88 % av nevneren**.
* **Slutning:** porten falt på det *første* leddet (87,8 % < 90 %), så svakheten endret ikke
  utfallet — men det var flaks. Hadde det første leddet bestått, ville porten ikke hatt noe svar.
  **Regelen: en konjunktiv port må oppgi hva som skjer med et sted der ett av leddene ikke kan
  måles — teller det som ikke-treff, eller faller det ut av nevneren?** Sies det ikke før
  beregningen, blir det bestemt etter tallene.
* **Gjort:** ført i `RESULTAT.md` under *Dødsbetingelser* som en svakhet i kriteriet, ikke som en
  egenskap ved materialet. Kravet tas inn i malen for de neste sakskriteriene.
* **Filer:** `docs/saker/SAK-14/KRITERIUM.md` presisering 3, `docs/saker/SAK-14/RESULTAT.md`.

## 38 Fritt blokktypevalg gjør generalisert blokkmodellering meningsløs (2026-09-27)

* **Målt:** SAK-09b reproduserte en publisert blokkmodell. Da blokktypen fikk velges fritt per blokk
  blant `{null, com, reg, rre, cre}`, nådde **både** min egen implementasjon og R-pakken
  `blockmodeling` 1.1.8 **total feil 0** — R fant **11 løsninger med feil 0** fra 50 tilfeldige
  starter.
* **Tall:** forfatterens publiserte løsning har feil **14**. Med fritt typevalg falt den til **3** for
  samme partisjon, og til **0** for nesten hvilken som helst partisjon. Grunnen er `rre`: en
  radregulær blokk har null feil så snart hver rad har minst én 1-er, og det kan nesten alltid
  oppnås ved å flytte én node.
* **Slutning:** kriteriefunksjonen i generalisert blokkmodellering er bare meningsfull med en
  **forhåndsgitt** blokkmodell — enten typene låst per posisjon, eller prioriteter/vekter per type.
  **Regelen: en reprodusert blokkmodell må oppgi den forhåndsgitte strukturen, ellers er tallet ikke
  etterprøvbart.** Avhandlingen her oppgir at vekter *kan* settes, men ikke hvilke, så
  optimaliseringen kan ikke reproduseres — bare feilen for en gitt partisjon.
* **Gjort:** typene låst per posisjon til forfatterens egen bildematrise i alle søk, og betingelsen
  ført i `RESULTAT.md` som en betingelse på resultatet.
* **Filer:** `saker/SAK-09b/kjoring.py` (fritt valg, degenerert), `kjoring2.py`/`kjoring3.py` (låst),
  `r-kjoring.R`, `docs/saker/SAK-09b/RESULTAT.md`.

## 39 En feildefinisjon kan utledes av kildens egne delresultater (2026-09-27)

* **Målt:** avhandlingen oppgir total feil 14 uten å definere hvordan en regulær blokks feil telles.
  Fire varianter fra litteraturen (nullrader, nullkolonner, maks, min) gir alle **1** for blokk (1,7),
  men figur 8.2 oppgir **3**.
* **Tall:** blokken er 3 × 3 med **én nullrad**. Definisjonen som treffer, er at en nullrad koster
  blokkens **kolonnetall** og en nullkolonne **radtallet**: 1 × 3 = 3. Den definisjonen gir deretter
  **14** over de 32 tre-modus-blokkene og **163** over alle 144 — og `blockmodeling` 1.1.8 gir samme
  tall i **hver enkelt celle**.
* **Slutning:** en publisert **feilmatrise** er mye mer verdt enn en publisert total. Totalen alene
  kan nås av flere definisjoner; en enkelt blokkverdi utelukker tre av fire. **Regelen: når en
  størrelse skal reproduseres og definisjonen ikke er oppgitt, se etter kildens delresultater og la
  dem velge definisjonen — og bekreft med en uavhengig implementasjon før tallet føres.**
* **Filer:** `saker/SAK-09b/feil.py`, `r-kontroll.R`, `docs/saker/SAK-09b/RESULTAT.md`.

## 40 En verktøygrense kan sperre en representasjon uten å sperre et resultat (2026-09-27)

* **Målt:** AL-0852 sier at Pajek ikke kan tvinge mellomnivåets rad- og kolonnepartisjon like i den
  begrensede matrisen 𝑀, og at forfatteren derfor brukte en augmentert én-modus-matrise i stedet.
  `blockmodeling` 1.1.8 — det navngitte alternativet, publisert i 2018 **før** innleveringen — har
  **heller ikke** mekanismen: `fixClusters` fryser klynger, `exchageClusters` styrer flytting,
  `sameIM` gjelder bildet på tvers av relasjoner. Ingen binder en radpartisjon til en kolonnepartisjon.
* **Tall:** utvunget ble de to partisjonene like **0 av 120** ganger i min implementasjon, og ulike i
  R også. Men forfatterens omgåelse **er** en tvungen løsning — den augmenterte matrisen har bare én
  partisjon av de 34 nodene — og den har feil **14**, mot 18 for beste tvungne søk fra 120 tilfeldige
  starter. Et tvungent søk **startet fra** forfatterens partisjon finner ingen forbedring.
* **Slutning:** det ugjorte var ikke ugjort av mangel på verktøy. Det var **unødvendig**: omgåelsen
  oppnådde det samme og mer. **Regelen: før et ugjort arbeid klassifiseres som en verktøygrense, sjekk
  om forfatterens egen omgåelse allerede oppfyller kravet det ugjorte skulle oppfylle.** En hindring
  som er løftbar men konsekvensløs, er et annet funn enn en hindring som ikke er løftbar, og de skal
  ikke føres likt.
* **Filer:** `docs/saker/SAK-09b/RESULTAT.md`, `saker/SAK-09b/kjoring3.json`,
  `docs/saker/REGISTER-SAKER.md`.
