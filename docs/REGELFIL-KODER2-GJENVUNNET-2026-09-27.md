# Regelfilen koder 2 leste — gjenvunnet 2026-09-27

**Opphav:** gjenvunnet fra øktutskrift
`~/.claude/projects/-Users-eirikbottennicolaysen-avalyset/1024847e-ef08-48fa-bd0a-2b2d9235bb89/subagents/agent-abf6e3798610fb9c1.jsonl`,
linje 13, felt `message.content[0].content` — Read-verktøyets resultat da koder 2 åpnet filen
25.09.2026 kl. 17:14:55 UTC (19:14:55 CEST; utskriftens tidsstempel på linje 13). Originalen het
`scratchpad/koderegler.md`, lå aldri i git og finnes ikke lenger på disk.

**Status:** dette er **innholdet slik koder 2 leste det**, ikke originalens bytes. Read-verktøyets
linjeprefiks (`N<TAB>`) er fjernet; ellers er ingenting endret. Avsluttende blanktegn og siste
linjeskift kan ikke verifiseres. Innholdet er 167 linjer, 9 805 B,
**sha256 `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449`** — regnet på innholdet nedenfor, uten denne headeren.

**Koder 2 var ikke et menneske.** Den var en CC-instans (Opus 5, agentisk, seks regelkilder), kjørt
som underøkt av den samme økten som var koder 1s orkestrator. ADDENDUM-11 førte opprinnelig ingen modell-ID;
den er gjenvunnet og ført i ADDENDUM-11 § 8 (`claude-opus-5`, alle 61 API-svar).
*(Rettet 28.09.2026, frys-lesningen: sto «kl. 19:35», som er øktens siste linje/filens mtime i CEST, ikke
lesetidspunktet, og «ingen modell-ID … står ikke i repoet», som § 8 har foreldet.)*

## Hvorfor dette er den ekte filen, og ikke en rekonstruksjon

1. **Rekkefølgen stemmer.** De seks kildene ligger i nøyaktig den rekkefølgen ADDENDUM-11 §2 lister:
   PREREG-v1 §2, PREREG-v1 §5, ADDENDUM-03 §1.2, ADDENDUM-05, ADDENDUM-04 §4, ADDENDUM-10 §1–3.
2. **Den forutsagte defekten er der, med riktig antall.** ADDENDUM-11 §3.3 sier at utdraget fra
   ADDENDUM-05 «avkuttet tabellen, slik at bare `H1/H7-uavklart` sto eksplisitt navngitt», og at
   koder 2 «derfor ikke brukte de tre øvrige uavklarte parene». Den gjenvunnede filen slutter
   ADDENDUM-05-blokken på **linje 72, tabellhodet**, og de **tre** dataradene (H2/H7, H3/H7, H5/H7)
   mangler. Et dokument som beskriver en feil i en fil vi ikke hadde, og filen viser feilen med
   samme mekanisme og samme antall.
3. **Lekkasjepåstanden reproduserer.** ADDENDUM-11 §2 påstår null treff på presisjonstall, M1, M2,
   klassefordeling, PS-identifikatorer og ADDENDUM-10s utfallstabell. Målt på den gjenvunnede filen:
   0 treff på «16,7», «22 243», «2 173», «0,93», «88,0», «31,6», «PS-», «presisjon», «treffrate»,
   «forventet», «kappa», «κ», «M1-rå», «fasit». Påstanden er nå verifisert, ikke bare hevdet.
4. **Innholdet er ordrett.** Hver blokk er sjekket linje for linje mot den låste kilden:
   PREREG-v1 §2 4/4, PREREG-v1 §5 19/19, ADDENDUM-03 §1.2 10/10, ADDENDUM-04 §4 16/16,
   ADDENDUM-10 §1–3 27/27 — og ADDENDUM-05 40/40 etter at grep-prefikset er trukket fra, se under.

## En defekt mer, som ikke står noe sted

ADDENDUM-05-blokken er ikke limt inn som tekst. Den er limt inn som **`grep -n`-utdata**: hver linje
bærer sitt linjenummer i kilden og et skilletegn som sier om linjen var et treff (`29:`) eller
kontekst (`30-`), og seks linjer inne i spennet 29–72 er utelatt (50, 65, 66, 67, 68, 69). Innholdet
er ordrett, men **formen fortalte koder 2 hvilke linjer et søk hadde truffet på**. Det lekker
ingenting om svarene, og det endrer ingen κ-verdi — men det er en kanal ADDENDUM-11 ikke nevner, og
de fem andre blokkene har den ikke. Den avkuttede tabellen er sannsynligvis samme årsak:
`grep`-vinduet nådde tabellhodet og stoppet.

---

# Kodereglene — eneste tillatte kilde

## PREREG-v1 §2 (hva som måles)
## 2 Hva som måles

**M1 — prevalens.** Andel artikler med minst ett parkert spørsmål: en setning der forfatteren navngir noe de ikke fikk gjort OG oppgir en hindring.

**M2 — bedømbarhet.** Andel av treffene der spørsmålet «er hindringen opphevet i dag» lar seg avgjøre uten domeneekspert i faget.

Begge oppgis rått, per felt og samlet, med usikre i egen kolonne.


## PREREG-v1 §5 (hindringstypologi)
## 5 Hindringstypologi

Hver treffsetning kodes i én klasse. Løftbarhet er fastsatt her, før data, og avledes aldri fra en modell.

| Klasse | Hindring | Løftbar av AI i dag |
|---|---|---|
| H1 | menneskelig lesning eller koding i skala | ja |
| H2 | lesbarhet: håndskrift, skadet kilde, lyd | ja |
| H3 | språkbarriere | ja, med forbehold |
| H4 | mønster i bilder eller signaler i volum | ja |
| H5 | simulering og regnekraft | delvis |
| H6 | strukturslutning fra sekvens | ja |
| H7 | dataene fantes ikke | nei |
| H8 | tilgang, juss, etikk, samtykke | nei |
| H9 | begrepet eller teorien manglet | nei |

Ikke-treff, som telles og rapporteres separat:
- **N1 besvart i samme artikkel**
- **N2 nyhetspåstand** («to the best of our knowledge, this is the first…»)
- **N3 omfangsvalg** uten navngitt hindring

Andelen N1–N3 måler hvor mye et rent nøkkelordfilter ville tatt feil. Andelen H7–H9 måler hva verktøyet ikke kan love.

**To eksempelsetninger per klasse føres i ADDENDUM-02, skrevet før første artikkel leses.** De hentes fra kjente tilfeller, ikke fra utvalget.


## ADDENDUM-03 §1.2 (passasjekravet)
### 1.2 Beslutningen

**Observasjonsenheten er passasjen: treffsetningen pluss ±2 setninger.** Et treff krever at det ugjorte og hindringen begge står innenfor passasjen, **og at de er knyttet til hverandre** — hindringen må være oppgitt som grunn for det ugjorte, ikke bare befinne seg i nærheten. Den koblingen avgjøres av koderen; ingen regel eller modell kan avgjøre den.

**M1 rapporteres som to tall på samme koding:**

| tall | krav |
|---|---|
| **M1-streng** | det ugjorte og hindringen i **samme setning** |
| **M1-passasje** | begge innenfor **±2 setninger**, og knyttet til hverandre |

**Ingen av dem er hovedtallet.** Begge oppgis, alltid sammen, som følsomhet på ett metodevalg. En rapport som oppgir ett M1-tall er feil, uansett hvilket av de to den oppgir.

**Terskelen på 5 % i PREREG §6 anvendes på M1-passasje.** Begrunnelsen skal stå der terskelen brukes: *setningskravet måler en retorisk form, ikke klassen.* Om en forfatter skriver «vi fikk ikke gjort X fordi Y» eller «vi fikk ikke gjort X. Y sto i veien» er et valg om setningsbygning. Klassen — at et spørsmål ble parkert og hindringen navngitt — er den samme. Å la terskelen henge på tegnsettingen ville gjort porten til en måling av skrivestil.

De øvrige tersklene i PREREG §6 følger samme enhet: M2 og overlevelsesraten regnes på de samme passasjene, og oppgis med hvilken enhet som ligger under.


## ADDENDUM-05 (de uavklarte naboparene)
29:## 2 Ny kodeverdi: uavklart
30-
31:**Er passasjen ikke tilstrekkelig til å avgjøre om hindringen var arbeidsmengde eller manglende data, kodes treffet som uavklart.** Verdien er `<klasse>/H7-uavklart` — for det utløsende paret: **`H1/H7-uavklart`**.
32-
33:Regelen er en kodingsregel, ikke en tolkningsfrihet: koderen skal ikke gjette. Står det ikke i passasjen hvorfor noe ikke lot seg gjøre, er klassen uavklart — også når konteksten gjør én lesning sannsynlig.
34-
35:Det utløsende funnet i §1 er **ikke** uavklart: der står hindringen eksplisitt («these details … are missing»), og klassen er H7. Uavklart er for tilfellene der teksten tier.
36-
37----
38-
39:## 3 Løftbarhet for uavklarte er «uavklart», ikke «ja»
40-
41-PREREG §5 gir H1 verdien `ja`. **Det anslaget er nå kjent for høyt**, fordi en del av det som koder som H1 på formen, i virkeligheten er H7.
42-
43:Løftbarhet for de uavklarte klassene settes derfor til `uavklart`. Den arver ikke den løftbare naboens verdi.
44-
45:Begrunnelsen er retningen på feilen. Å gi uavklarte `ja` ville gjenskapt overvurderingen som gjorde dette addendumet nødvendig. Å gi dem `nei` ville undervurdert på samme vis. `uavklart` er den eneste verdien som ikke later som spørsmålet er avgjort.
46-
47-Oppslaget ligger i `src/gjenopptak/classify/liftability.py` og er fortsatt en ren tabell — ADR-0004 står: ingen modell setter løftbarhet.
48-
49----
--
51:## 4 Andelen uavklarte er et eget tall
52-
53:**Andelen uavklarte rapporteres som eget tall og regnes ikke inn i løftbar andel.**
54-
55-| tall | nevner |
56-|---|---|
57-| løftbar andel | **avklarte treff** |
58:| uavklart andel | **alle treff** |
59-
60:De to oppgis alltid sammen. En rapport som oppgir løftbar andel uten uavklart andel er feil, fordi den skjuler hvor stor del av grunnlaget som ikke er avgjort.
61-
62-Uavklarte fordeles ikke proporsjonalt, og de tilordnes ikke en klasse ved skjønn. Begge grep ville flyttet et ukjent tall inn i et kjent, og feilen ville pekt samme vei som den opprinnelige.
63-
64-`classify.format_liftable` gir begge tallene i én streng, og modulen tilbyr ingen funksjon som returnerer løftbar andel alene — samme håndheving som for M1-tallene i ADDENDUM-03 §1 og seksjonsopphavet i ADR-0007 punkt 4.
--
70:**Datamangel er fellesnevneren, og H7 er ikke-løftbar.** Tre andre klasser i PREREG §5 har samme forvekslingsfare, og de får samme uavklart-verdi:
71-
72-| par | hva som ser likt ut | løftbar / ikke-løftbar |

## ADDENDUM-04 §4 (det ugjorte må tilhøre arbeidet som rapporteres)
## 4 PREREG §2 presiseres: det ugjorte må tilhøre arbeidet som rapporteres

**Et treff krever at det ugjorte tilhører den undersøkelsen artikkelen rapporterer.** Utsagn om organisasjonens generelle praksis, om fagets vanlige framgangsmåte, eller om hva andre ikke har gjort, er ikke treff — selv når hindringen er navngitt og selv når den er løftbar.

Grunnen er hva M1 skal måle: et parkert spørsmål er noe forfatterne ville gjort i dette arbeidet og ikke rakk. En beskrivelse av at et arbeidstrinn rutinemessig utelates, er en policy, ikke et parkert spørsmål. Blandes de to, måler M1 dels forskningsspor, dels metodekonvensjoner.

**Konsekvens: H1-kontrollen i ADDENDUM-03 §3.1 faller.** `10.4073/cmdp.2018.2` beskriver at 3ie ikke utfører kritisk vurdering av primærstudier fordi det ville være for tidkrevende innenfor tidsrammen. Det er organisasjonens praksis, i tredjeperson, ikke en undersøkelse forfatterne ønsket å gjøre i dette arbeidet. Nyansen sto i ADDENDUM-03 §3.1 som et forbehold; her avgjøres den mot kontrollen.

**H1 står dermed fortsatt uprøvd.** Det gjelder også H4 (ADDENDUM-03 §3.2, armert nullresultat). Rubrikkens løftbare ende — H1–H6, den enden verktøyet hviler på — har ingen positiv kontroll.

**Dette lappes ikke.** Kontrollstatus etter denne presiseringen:

| klasse | kontroll | løftbar |
|---|---|---|
| H7 | 10.1038/s41467-019-11357-9 (arkeologi) | nei |
| H8 | 10.1016/s2468-2667(17)30217-7 (klinisk epidemiologi) | nei |
| H1 | **mangler** — kandidaten falt på §4 | ja |
| H4 | **mangler** — armert nullresultat | ja |
| energifeltets kontroll | 10.1016/j.apenergy.2018.04.048, seksjon fortsatt uverifisert | — |
| tekstvitenskapsfeltet | **mangler**, gjenåpnet av ADDENDUM-03 §1 | — |

En positiv kontroll i H1 eller H4 er en forutsetning for å kode, ikke en forbedring. Uten den kan rubrikken ikke vise at den finner den typen treff verktøyet er bygget for.

---


## ADDENDUM-10 §1–3 (tre presiseringer)
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

