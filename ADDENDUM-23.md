# ADDENDUM-23 — POST HOC reanalyse etter at den preregistrerte porten falt

**Skrevet:** 2026-09-27. **Status: LÅST før koder c-kjøringen er ferdig.**
**Dette er ikke en preregistrering. Det er en POST HOC reanalyse av samme data.**

## 0 Hva som gikk galt, og hvorfor dette ikke kan kalles en port

Den preregistrerte porten i ADDENDUM-22 §6.1 krevde at leseren bekreftet **≥ 22 av 27** kjente treff. Den
bekreftet 17, og med fire ennå udømte er taket 21. **Porten falt, og den står som falt.** Dette
addendumet endrer ikke det utfallet, senker ikke terskelen og gjenoppliver ikke listen som arbeidsliste.

Alt under er **merket POST HOC** fordi kriteriene er valgt *etter* at fallet var kjent. Det gir dem
svakere bevisverdi enn en preregistrert port, uansett hvor rimelige de er.

## 1 (a) Den stabile kjernen — definert fra ADDENDUM-10/11-filene alene

**Definisjon, fastsatt uten å se på koder c:** et av de 27 kjente treffene er i den stabile kjernen hvis
**koder 1 og koder 2 er enige om treffstatus** *og* **ingen av dem har merket `tvil`**. Kildene er
`data/port-presisjonssett-ADDENDUM10.jsonl` (koder 1) og
`data/port-presisjonssett-verdikter-koder2.jsonl` (koder 2), ingenting annet.

**n = 3 av 27: PS-044, PS-205, PS-266.**

Delkriteriene, for at tallet skal kunne etterprøves:

| kriterium | antall av 27 |
|---|---|
| koder 1 og 2 enige om treffstatus | 19 |
| koder 1 har **ikke** merket tvil | 7 |
| koder 2 har **ikke** merket tvil | 4 |
| **alle tre samtidig — kjernen** | **3** |

**Dette er i seg selv hovedfunnet i addendumet.** Referansesettet på 27 inneholder **tre** passasjer der to
uavhengige kodere er enige uten at noen av dem er i tvil. Koder 1 merket **20 av 27** med tvil. Et
referansesett med den egenskapen kan ikke bære en port på 22 av 27 — terskelen forutsatte en stabilitet
settet ikke har. Jf. LAERDOM §33.

## 2 (b) Terskelen: koder 2s egen bekreftelsesrate på kjernen

Koder 2 bekreftet **3 av 3** i kjernen = **100 %**. Terskelen for koder c er derfor **100 % på kjernen, det
vil si 3 av 3.**

Til sammenlikning bekreftet koder 2 **19 av 27 = 70,4 %** på hele settet.

**Terskelen har nesten ingen styrke, og det skal stå.** En port på n = 3 med krav om perfekt bekreftelse
kan bare feile på én måte: at leseren mister én av tre. Den skiller ikke en god leser fra en middels.
Den kan bare avdekke et sammenbrudd.

## 3 Opplysning som må stå: (a) og (b) er allerede kjent oppfylt

**Da dette addendumet ble skrevet, visste orkestratoren allerede at koder c bekreftet alle tre i
kjernen.** Alle tre ble dømt i de komplette øktene, og utfallet står i ADDENDUM-22 §9.3s
registersammenlikning: PS-044 (AL-1726) treff, PS-205 (AL-1902) treff, PS-266 (AL-0925) treff — alle med
samme hindringsklasse som registeret.

**Kriterium (a) + (b) er altså oppfylt, 3 av 3, og det var kjent før kriteriet ble skrevet.** Det er ikke
en blind test, og det skal ikke rapporteres som om det var. Orkestratoren kjente på skrivetidspunktet også
koder c-verdiktene for 23 av de 27 kjente, inkludert alle seks tapene. **Det eneste genuint uavgjorte er
(c).**

## 4 (c) Blind presisjon — den delen som faktisk ikke er avgjort

* **Utvalg:** **100 tilfeldige passasjer** som koder c kalte treff, trukket fra den **ferdige** kjøringen
  (alle 2 844 dømt, inkludert de 363 som fullføres serielt etter 429-avbruddet), med **frø 734248**.
* **Leser:** én **separat instans med tom kontekst**, som får passasjeteksten og regelfilen
  `koder2/koderegler-gjenvunnet.md` (sha256 `234695dd4e1777a9…`) og **ingenting annet**. Sperrelisten er
  den samme som i `arbeidsliste/oppdrag-koder-c.md` (sha256 `0025f3e1e9a74869…`), utvidet med koder c-s
  verdiktfiler, nøkkelfilen og dette addendumet. Instansen får **ikke** vite at passasjene er kalt treff.
* **Terskel: ≥ 0,70** bekreftet.
* Wilson-intervall oppgis. Uparsede svar telles og fylles ikke inn.

## 5 Hva utfallet får hete

* **(a)+(b) oppfylt OG (c) ≥ 0,70:** lista heter **«kandidatliste (post hoc port)»** — aldri
  «arbeidsliste». Navnet bærer at porten var valgt etter fallet.
* **(c) < 0,70:** **ingen liste.** Verken kandidatliste eller arbeidsliste.
* **«Arbeidsliste» kan bare komme fra en prospektiv port på nytt materiale.** Ingen reanalyse av disse
  2 844 passasjene kan gi det navnet, uansett tall.

## 6 Dødsbetingelser

* **Kjernen utvides ikke.** n = 3 står. Å legge til passasjer der bare én koder var i tvil, ville vært å
  velge kriterium etter resultat en gang til.
* **(c) kjøres én gang**, med frø 734248. Ingen ny trekning, ingen ny ledetekst.
* Terskelen 0,70 flyttes ikke.
* Faller (c), skrives ingen liste, og tallet rapporteres.
* Ingen offentliggjøring, ingen MASTER-redigering.

## 7 Utfall 2026-09-27

### 7.1 (a) og (b): oppfylt, men **ikke informative**

Koder c bekreftet **3 av 3** i den stabile kjernen — PS-044 (H7), PS-205 (H7), PS-266 (H2) — mot terskelen
100 %. Kriteriet er dermed oppfylt.

**Det betyr nesten ingenting, og skal føres slik: «oppfylt, ikke informativ, n = 3».** Tre passasjer med
krav om perfekt bekreftelse kan bare avdekke et sammenbrudd, ikke skille en god leser fra en middels. Og
§3 opplyste at utfallet var kjent før kriteriet ble skrevet. **Merkelappen på lista avgjøres derfor av (c)
alene.**

### 7.2 (c) Blind presisjon: **85 av 100 = 85,0 %**

| | verdi |
|---|---|
| utvalg | 100 treff fra den ferdige koder c-kjøringen, frø 734248 |
| bekreftet av uavhengig instans | **85** |
| rate | **85,0 %**, Wilson 95 % **[76,7–90,7]** |
| terskel | 0,70 |
| **utfall** | **BESTÅTT** — hele intervallet ligger over terskelen |
| klasseenighet blant de bekreftede | 74 av 85 = 87,1 % |
| de 15 avviste ble kodet | `INGEN` 8, `N3` 6, `N1` 1 |

**`tvil`-feltet er informativt, og det er det mest brukbare funnet her.** Delt på koder c-s egen tvil:

* der koder c **ikke** var i tvil: **41 av 42 bekreftet = 97,6 %**
* der koder c **var** i tvil: **44 av 58 bekreftet = 75,9 %**

Tvilsmerket forutsier altså hvor to lesere skiller lag. En liste sortert på `tvil: false` ville hatt
presisjon nær 98 % på dette utvalget.

**Og et forbehold som må stå:** av de to kjente treffene som havnet i utvalget, avviste den uavhengige
instansen **PS-151**. Referansesettets egne treff overlever ikke alltid en tredje lesning heller — samme
mønster som porten i ADDENDUM-22 §9.2.

### 7.3 Avvik fra §4: to instanser, ikke én

**§4 sa «én separat instans». Det ble to: 85 + 15.** Den første ble avbrutt etter 85 passasjer, og de 15
siste ble kodet av en ny instans med tom kontekst, egen kladdekatalog og identisk oppdrag. De 85 er et
prefiks av blindfilen og de 15 er halen; ingen passasje er dømt to ganger, ingen mangler. Avviket er ført i
`arbeidsliste/presisjon-100-maal.json`. Det svekker «én lesning»-egenskapen og skal ikke skjules: de to
instansene kan ha festet tolkningslinjer ulikt, og 15 av 100 er nok til å flytte raten et par prosentpoeng.

### 7.4 Merkelappen

**Lista heter «kandidatliste (post hoc port)».** (c) er bestått med hele intervallet over terskelen, og
(a)+(b) er oppfylt men ikke informative.

**Hva navnet ikke betyr:**

* Det betyr **ikke** at den preregistrerte porten ble bestått. Den falt: 21 av 27 mot terskel 22.
* Det betyr **ikke** at lista er en arbeidsliste. Arbeidsliste kan bare komme fra en prospektiv port på
  nytt materiale, jf. §5.
* Det betyr at **85 % av det koder c kaller treff, holder for en uavhengig leser på samme regler** — og at
  tallet er målt etter at kriteriet ble valgt, med den svekkelsen det gir.
