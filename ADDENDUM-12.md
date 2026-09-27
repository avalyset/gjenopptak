# ADDENDUM-12 — triage av de dømte løftbare treffene, og hvorfor den ikke sorterte

**Skrevet:** 2026-09-26. **Gjelder:** PREREG-v1 §5 (løftbarhet) og §8 (hva verktøyet kan love).
**Utfall: negativt.** Kriteriet rangerte ikke bedre enn tilfeldig, og to av fire signaler viste seg
å være ubrukelige som bygget. Addendumet føres fordi et negativt resultat om egen metode er et
resultat, og fordi grensen det avdekker gjelder verktøyklassen, ikke denne implementasjonen.

## 1 Hvorfor

Porten ga 2 173 dømte treff, hvorav 243 i en løftbar klasse (H1–H6). Bare 14 av dem lå i de 320
leste passasjene. Spørsmålet var om de resterende kunne **rangeres maskinelt** på gjennomførbarhet,
slik at lesing kunne rettes mot de beste — altså om et verktøy kan si *hvilke* parkerte spørsmål det
er verdt å forsøke, uten at et menneske leser dem først.

## 2 Materialet

**229 uleste dømte treff i klasse H1–H6.**

| | arkeologi | energimodellering | klinisk epi. | tekstvitenskap | sum |
|---|---|---|---|---|---|
| H1 | 15 | 67 | 21 | 5 | **108** |
| H2 | 4 | 1 | — | 1 | **6** |
| H3 | 1 | — | 3 | 2 | **6** |
| H4 | 3 | 1 | — | — | **4** |
| H5 | 22 | 49 | 19 | 1 | **91** |
| H6 | 5 | 8 | 1 | — | **14** |
| **sum** | **50** | **126** | **44** | **9** | **229** |

Energimodellering bærer 55,0 % av kandidatene og har samtidig portens dårligste presisjon (7,0 %).

## 3 Kriteriet, låst før tallene

Fire signaler, hvert 0–2, regnet uten å lese passasjen:

* **a — datatilgjengelighet i verket:** 2 ved datatilgangserklæring, datasett-DOI eller arkivlenke;
  1 ved supplement eller appendiks; 0 ellers. Regnet på verkets egen tekst.
* **b — materialtype etter dømt klasse:** H5/H6 = 2 (likninger og tabeller, lett) · H1/H3 = 1
  (korpus, middels) · H2/H4 = 0 (bilder og signaler, tungt).
* **c — selvinneholdt:** antall henvisninger til tabell, figur eller likning i passasjevinduet;
  ≥3 = 2, 1–2 = 1, 0 = 0.
* **d — siteringsgrunnlag:** antall siterende arbeider. Null eller én gjør falsifisering verdiløs.

Kriteriefilen er `triage-loftbare-2026-09-26-kriterium.py` på Vault, sha256
`6c33d498c8f62bb85d7f540d8c5ed1202275bd9c74d3e84b872f477f486bd9c0`. Den ble skrevet og lagret
**før** noen fordeling var regnet. Resultatene ligger i `triage-loftbare-2026-09-26.json`, sha256
`1b58c4bed2f169fe294460f0b3094e7828eebfed228e64e22adf7b922a31cd61`.

## 4 Fordelingen

| sum (a+b+c) | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|
| antall | **1** | 4 | 56 | 72 | 60 | 34 | 2 |

| signal | faller på det |
|---|---|
| **c = 0** — ingen henvisning til materiale i passasjen | **205 av 229 = 89,5 %** |
| a = 0 | 70 = 30,6 % |
| b = 0 | 10 = 4,4 % |
| minst ett signal = 0 | 212 = 92,6 % |
| alle tre ≥ 1 | **17 = 7,4 %** |
| alle tre = 2 | **1 = 0,4 %** |

**Signal c avgjør nesten alt alene.** Ni av ti dømte løftbare treff sier hva som ikke ble gjort uten
å si hvor materialet ligger.

## 5 Lesningen: 15 av 229

Topp 15 etter rang ble lest. **To ekte treff = 13,3 %**, mot portens målte presisjon **16,7 %
[11,6–23,4]** på et tilfeldig stratifisert utvalg. **Rangeringen ga ingen forbedring**; punktanslaget
ligger under det usorterte, og innenfor intervallet.

* **7 av 15 er parserstøy:** passasjen er tallkolonner fra en tabell («0.16 0.09 0.11 0.20 0.18»),
  og dommeren har begrunnet dem med «begrenset regnekraft» — en begrunnelse uten dekning i teksten.
* **4 av 15 er N1:** hindringen er navngitt *og* løst i samme verk («Fortunately, the simple affine
  policy … enables significant reduction»; «An additional computational model was created to …»).
* **2 av 15 er N3:** selvpålagt forenkling med uttalt antakelse.
* **2 av 15 er ekte treff**, begge i **W2551114598**, samme verk som PS-119 og PS-246. Det verket har
  **ett** siterende arbeid.

**Null ÅPNE. To DELVIS. Ingen LUKKEDE.** Materialtilgangen er verifisert mot verkets egen tekst:
borehullsdataene er «openly available from the BGS website», men de daglige seriene er modellutdata
som ikke er publisert, og «Historical SMD data are available **on request** from both the Met Office
and the EA».

## 6 To av fire signaler er ubrukelige som bygget

**Signal a er ugyldig.** Det kan ikke skille forfatterens egen datatilgang fra tredjeparts data
*nevnt* i teksten. I W2551114598 fyrte det på «openly available from the BGS website» og «data are
available on request from both the Met Office and the EA» — begge om andres data, om stedets
geologi og værhistorikk, ikke om verkets egne utdata. Verket har **null** datatilgangserklæringer.
**7 av de 15 arvet full score på a feilaktig.** Signalet måler at ordet «tilgjengelig» finnes i et
verk, ikke at materialet som trengs, er tilgjengelig.

**Signal d kunne ikke regnes.** `cited_by_count` finnes ikke i `spesifikasjon.json`, og ikke noe annet
sted på disk — heller ikke i de frosne rammelistene, trekkloggene eller utvalgsfilene. Bare de fire
alt falsifiserte kandidatene har siteringstall. Å fylle inn feltet koster ett `cites:`-oppslag per
kandidat, **om lag 2 060 kreditter** for alle 229. **Ført som ukjent, ikke gjettet.** Hadde det vært
regnbart, ville det nullet begge de to treffene: verket de ligger i, har ett siterende arbeid.

## 7 Konklusjonen som står

**Passasjen navngir hindringen, ikke ressursen.** Et parkert forskningsspørsmål blir formulert som en
grunn til at noe ikke ble gjort — ikke som en oppskrift på hva som skulle til. Derfor:

**Et verktøy kan ikke rangere kandidater på gjennomførbarhet fra treffpassasjen alene. Det må åpne
verket.** 89,5 % av passasjene mangler enhver henvisning til materialet, og der en henvisning finnes,
peker den like gjerne til andres data som til forfatterens.

**Dette er en grense for klassen av verktøy, ikke for denne implementasjonen.** Grensen følger av hva
en forfatter skriver når hun parkerer et spørsmål, og den flyttes ikke av en bedre modell, en bedre
ledetekst eller flere signaler av samme slag. Den flyttes bare av å hente verket og lese det — altså
av nøyaktig det arbeidet rangeringen skulle spare.

## 8 Hva dette ikke er

Ikke en måling av prevalens, ikke en ny presisjonsmåling, og ikke en revisjon av portens tall. De 15
leste er **ikke** et tilfeldig utvalg og skal aldri regnes inn i presisjonen; de er de høyest
rangerte etter et kriterium som viste seg ikke å rangere. De 214 uleste står uleste. De to nye
treffene er ført i registeret med DELVIS materialtilgang, og #15 med klassen rettet fra dømt H6 til
H5, fordi H6 er strukturslutning fra sekvens (PREREG-v1 §5) og hindringen er en simuleringsgrense.
