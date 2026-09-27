# ADDENDUM-10 — tre presiseringer av treffkravet, anvendt på tvilstilfellene

**Skrevet:** 2026-09-25. **Gjelder:** PREREG-v1 §2 og ADDENDUM-04 §4.

## 0 Når dette er skrevet, og hva det ikke gjør

**Disse presiseringene er gjort etter at data er sett.** De ble utløst av 48 tvilstilfeller fra
lesningen av presisjonssettet 2026-09-20, ført uavgjort i `data/port-tvil.jsonl` nettopp fordi
reglene ikke avgjorde dem. Det står her fordi rekkefølgen er en del av beviset: en regel skrevet
etter data er svakere enn en skrevet før, og leseren skal kunne vekte den deretter.

**De presiserer eksisterende regler og endrer ikke rubrikken.** Hindringstypologien i PREREG-v1 §5
er uendret: ingen klasse er lagt til, fjernet eller omdefinert. Løftbarhetstabellen er uendret.
Treffkravet — noe ugjort, en navngitt hindring, de to knyttet sammen, og det ugjorte tilhørende
arbeidet som rapporteres — er uendret. Det som presiseres, er hvordan kravet leses i tre
tilbakevendende former som PREREG-v1 §2 ikke skiller eksplisitt.

En presisering som hadde flyttet mange saker, ville vært en regelendring i forkledning. Utfallet
står i §4: av 48 tvilstilfeller endrer én verdikt.

## 1 Feltgap tilhører feltet, ikke arbeidet

Når passasjen sier at *feltet* mangler noe — «little is known about…», «no study has…», «the
literature is lagging» — og hindringen forklarer hvorfor litteraturen står der den står, er det
**ikke et treff**, selv når hindringen er tydelig navngitt og H-formet.

Kravet i PREREG-v1 §2 er at forfatteren navngir noe **de** ikke fikk gjort. Et kunnskapshull i
feltet er en begrunnelse for at arbeidet er verdt å gjøre, ikke et spørsmål arbeidet parkerte.
Det samme gjelder når det ugjorte tilhører en annen organisasjons arbeid, for eksempel et råd om
hvordan en tredjepart bør modellere.

## 2 Oversiktsarbeid har sitt eget ugjorte

Et oversiktsarbeid har egne analyser: sammenslåing, subgruppeanalyse, tallfesting på tvers av
primærstudier. Når passasjen sier at **oversikten selv** ikke kan gjennomføre en slik analyse fordi
primærstudiene ikke rapporterer det som trengs, er det **et treff, klasse H7**.

Skillet mot §1 er hvem det ugjorte tilhører, ikke hvor hindringen ligger. «Ingen av studiene
undersøkte X» alene er et feltgap. «Vi kan ikke avgjøre X fordi studiene ikke rapporterer det» er
oversiktens eget parkerte spørsmål, og dataene finnes ikke — derav H7.

## 3 Modellbegrensninger deles i tre

Passasjer der hindringen er en egenskap ved en modell, en metode eller et verktøy, kodes slik:

| formen | klasse |
|---|---|
| navngitt **regnekraft eller løser** — kjøretid, minne, en parameter verktøyet ikke tar imot | **H5** |
| **manglende metode eller teori** — kategorien lar seg ikke skille, begrepet finnes ikke | **H9** |
| **forenkling uten navngitt hindring** — en antakelse forfatteren selv innfører | **N3**, ikke treff |

Den tredje raden er den viktigste. En selvpålagt forenkling ser ut som en hindring i teksten
(«kan ikke vurderes gitt antakelsen om…»), men hindringen er forfatterens eget valg. Da er det et
omfangsvalg, og N3 er riktig.

Presiseringen gjelder bare **klassen** for saker som allerede oppfyller treffkravet. Den gjør
ingen passasje til et treff som mangler et ugjort.

## 4 Utfallet på de 48

| regel | saker | verdikt endret |
|---|---|---|
| §1 feltgap → ikke treff | 7 | 0 |
| §2 oversiktsarbeid → treff, H7 | 2 | 0 |
| §3 modellbegrensning | 10 | 1 |
| utenfor alle tre, avgjort på lesningen som før | 29 | 0 |
| **sum** | **48** | **1** |

Den ene endringen er PS-031 (energimodellering, dømt H5): regnekraft er navngitt som grunn til at
etterspørselen grupperes i klasser i stedet for å bruke alle 8 760 timeverdiene. Lest som feltgap
var den ikke et treff; lest etter §3 er den et treff i klasse H5.

De 29 utenfor reglene er avgjort som før, på passasjen alene. At tre presiseringer bare flytter én
av 48 saker, er i seg selv et tall: tvilen i dette materialet ligger ikke i regelverket, men i
passasjene.

## 5 Følger for tallene

Presisjonen på portmaterialet går fra 24 av 150 til **25 av 150**. Alle avledede tall — presisjon
per felt, M1 i fire varianter, M2 og løftbar andel — regnes om i `docs/RESULTAT-PORT-v1.md`, der
tallene før ADDENDUM-10 blir stående ved siden av de nye.

De 48 avgjørelsene ligger i `data/port-tvil.jsonl` med regelhenvisning per sak. Tvilsmarkeringen
fjernes ikke: en avgjort tvil er fortsatt en sak der to lesninger var mulige.

## 6 Rettelse samme dag

Tabellen i §4 sa først 11 saker under §3 og 28 utenfor. Ved gjennomgangen av hver enkelt sak ble PS-014 flyttet ut av §3: passasjen er ikke en selvpålagt forenkling, men en svakhet forfatterne løser i samme artikkel, altså N1. Fordelingen er 7 / 2 / 10 / 29. Tallet som betyr noe — én endret verdikt — står uendret. Rettelsen er ført her framfor å endres bort, fordi et addendum som stilltiende korrigeres, ikke kan etterprøves.

## 7 Datert note 2026-09-27: trekkingen av de 150 var ikke uniform, og hva det gjør med 16,7 %

Presisjonen **25/150 = 16,7 %** i § 5 er regnet på et **stratifisert, ikke uniformt** utvalg av de
2 173 flaggede. Ordlyden som styrer det, står i `src/gjenopptak/classify/port.py`
(`N_TREFF = 150`, `GULV = {"tekstvitenskap": 25}`, `feltkvoter()` kjørt **før** klassestratifiseringen)
og i LAERDOM § 15, ordrett: «**Proporsjonal trekking ville gitt tekstvitenskap 5 av de 150 leste
treffene**» og «Gulvet på tekstvitenskap er en **måleskranke, ikke en vekting**».

**Sammensetningen, de 150 mot de 2 173** (`ekstraksjon/2026-09-26/h2-trekking.json`):

| akse | de 2 173 | de 150 |
|---|---|---|
| energimodellering | 42,1 % | 38,0 % |
| arkeologi | 36,4 % | 33,3 % |
| klinisk epidemiologi | 13,3 % | 12,0 % |
| **tekstvitenskap** | **8,2 %** | **16,7 %** |
| PDF / JATS / HTML | 81,4 / 11,5 / 7,1 % | 80,7 / 11,3 / 8,0 % |
| **ikke-prosa** (G3-regelen) | **22,5 %** | **12,7 %** |

**To vektede anslag, begge innenfor det oppgitte Wilson-intervallet [11,6–23,4]:**

* **Vektet mot feltfordelingen i de 2 173: 16,69 %** — altså **+0,02 pp** mot det uvektede. Gulvet på
  tekstvitenskap er harmløst for hovedtallet, fordi feltets egen presisjon (16,0 %) ligger tett på
  gjennomsnittet, og fordi klinisk epidemiologis underrepresentasjon trekker motsatt vei.
* **Vektet mot prosa/ikke-prosa: 15,38 %** — altså **−1,28 pp**. Delene: prosa **24/131 = 18,3 %**
  [12,6–25,8], ikke-prosa **1/19 = 5,3 %** [0,9–24,6]. De 150 inneholder mindre søppel enn de 2 173,
  og 16,7 % er i den forstand et **optimistisk** anslag for materialet.

**Tilføyd 27.09.2026: regnet med to G3-regler, samme konklusjon.** Implementasjonen bak 26.09-regelen
er tapt og reproduserer ikke (LAERDOM §31), så begge føres, merket:

| G3-regel | prosa | ikke-prosa | vekt ikke-prosa | vektet estimat | mot 16,67 % |
|---|---|---|---|---|---|
| 26.09, **ikke reprodusert** | 24/131 = 18,32 % | 1/19 = 5,26 % | 22,5 % | **15,38 %** | −1,29 pp |
| `ikkeprosa.py` sha `63ed734555a8bc95`, **versjonert** | 24/136 = 17,65 % [12,2–24,9] | 1/14 = 7,14 % [1,3–31,5] | 20,8 % | **15,46 %** | −1,21 pp |

De to reglene er uenige om *hvilke* tekstbiter som er prosa — 19 mot 14 av de 150 — men enige om
retningen og størrelsen på korreksjonen. **Slutningen er robust mot regelvalget**, og tallene er ført i
`ekstraksjon/2026-09-26/k1-union-v2.json`.

**Hva som gjelder: 16,7 % er presisjonen i utvalget.** Tallet er ikke regnet om, terskelen er ikke
rørt, og ingen avledet størrelse i resultatnotatet er endret — differansene er mindre enn
intervallbredden. Men en leser som vil ha presisjonen i de 2 173, skal bruke **15,4–16,7 %** og vite
hvorfor spennet finnes.
