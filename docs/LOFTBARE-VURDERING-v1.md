# De fire løftbare treffene — kan de løses? (v1, 2026-09-21)

Vurdering, ikke forsøk. Passasjene og materialbeskrivelsene er lest i `data/port/passasjer-arkeologi.jsonl`;
metadata fra `data/port/spesifikasjon.json`. Ingen nye kall.

| | **PS-202** (H2) | **PS-266** (H2) | **PS-119** (H5) | **PS-246** (H5) |
|---|---|---|---|---|
| **verk** | W2936215896, PLOS ONE 2019, blyholdige kar fra Pietrele/Blejeşti | W3217588367, Acta Musei Napocensis 54/I 2017, graffito fra Ocnița | W2551114598, avhandling, Birmingham 2016 (DART) | samme avhandling |
| **hva ble latt ugjort** | Påvise blyspor (Pb) i to kar med p-XRF | Lese eiermerket `CEN( )` på bunnen av en liten kopp | Sammenlikne seksjonene ut fra sug beregnet fra VWC | Bruke målt matrisk tetthet som inndata i SPAW |
| **hindringen** | Fragmentert, erodert overflate på P13F723CER53.4 og et tykt gipslag på Blejeşti-2 | Usikre kursive bokstavformer og et krussedull over de to siste tegnene | Modellens nøyaktighet (0,04) er for grov til at sug kan skille seksjonene | SPAWs faste partikkeltetthet tar ikke imot målt matrisk tetthet; gir FC > mettet VWC |
| **materiale et forsøk trenger** | Gjenstandene selv, eller rå p-XRF-spektre / nye SEM-snitt | Høyoppløst bilde av Pl. II/4–5, helst strøklys eller 3D-skann av gjenstanden | Daglige TDR-VWC-serier per seksjon og horisont | Jordinndata per horisont (leire, sand, grus, org., matrisk tetthet) + Saxton–Rawls-likningene |
| **tilgjengelig?** | **Nei.** Data Availability sier «all relevant data … in the paper and Supporting Information»; S1 er metodediskusjon og SEM/p-XRF-tabeller, ikke rå spektre. Karene ligger i rumenske samlinger | **Delvis.** Plansjen ligger i den åpne PDF-en (vi hentet teksten, ikke bildene). Gjenstanden er i Râmnicu-Vâlcea **uten inv.nr.**, bokstavhøyde 1,2–1,5 cm | **Nei.** Rådataene er Boddice (2014)/DART-konsortiets, ikke trykt i avhandlingen | **Ja.** Tabell 5.1, 6.1, 6.3 og 6.4 i avhandlingen gir inndataene; Saxton & Rawls (2006) er publisert |
| **hva forsøket ville være** | Ny måling på objektet etter rensing, eller reanalyse av spektre | Bildeforbedring (CLAHE, flerskala) + paleografisk sammenlikning med parallellene artikkelen selv nevner | Reimplementere SWCC-omregningen og kjøre den på rådataene | Reimplementere Saxton–Rawls med målt tetthet som fri parameter, kjøre samme horisonter, og se om FC > mettet-inkonsistensen og korreksjonsfaktoren 2,22 forsvinner |
| **verktøy** | p-XRF/SEM i laboratorium | Bildebehandling + epigrafisk oppslagsverk | Python + rådataserier | Python, ~30 linjer pedotransfer |
| **innsats** | Uker, reise, laboratorietid | 2–4 t, men konklusjonen hviler på ett trykt fotografi | 1–2 dager *etter* at data er skaffet | **3–6 t, alt materiale i hånden** |
| **utfall hvis forsøkt** | Ikke gjennomførbart eksternt | Forslag til lesning, ikke verifiserbart uten autopsi | Blokkert til data foreligger | Testbart ja/nei på et uttalt kriterium |

## Anbefaling

**Forsøk PS-246.** Det er det eneste av de fire der hindringen er en programvareskranke og ikke fravær av
fysisk materiale: SPAW låser partikkeltettheten til standardverdien, og nettopp derfor måtte forfatteren
innføre korreksjonsfaktoren 2,22. Inndataene står i avhandlingens egne tabeller, likningene er publisert,
og forsøket har et skarpt kriterium: **faller FC under mettet VWC når målt matrisk tetthet tillates, er det
ugjorte gjort — ellers ikke.** Det krever ingen tilgang til noe som ikke allerede er åpent.

PS-119 er samme avhandling, men venter på rådata som ikke er publisert. PS-266 kan gi et lesningsforslag,
men et forslag fra ett trykt fotografi er svakere bevis enn porten krever. PS-202 lar seg ikke gjøre uten
gjenstandene.

Merk hva dette sier om løftbarheten i stort: av 24 ekte treff er fire løftbare i klasse, og **ett** av dem
er løftbart i praksis her og nå. Klassen sier hva slags hindring det er, ikke om materialet finnes.
