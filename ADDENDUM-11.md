# ADDENDUM-11 — uavhengig koding av presisjonssettet, og hva κ ble

**Skrevet:** 2026-09-25. **Gjelder:** reliabiliteten til fasiten i PREREG-v1 §2 og §5.

## 1 Hvorfor

Fasiten i portmaterialet var lest av én instans, som også hadde bygget dommeren og
ledeteksten. Ankerne viste at den lesningen ikke hadde flyttet seg binært, men en anker­kontroll
måler drift hos én leser; den måler ikke om reglene gir samme utfall hos en annen. Manuskriptet
oppga dette som den største enkeltsvakheten, med κ uttrykkelig ikke målt. Dette addendumet måler det.

## 2 Metode

**Koder 2 er en separat instans med tom kontekst.** Den fikk nøyaktig to filer: blindfilen
(320 rader, bare `id` og `tekst`, stokket) og en regelfil bygget av ordrette utdrag fra
PREREG-v1 §2, PREREG-v1 §5, ADDENDUM-03 §1.2, ADDENDUM-05, ADDENDUM-04 §4 og ADDENDUM-10 §1–3.

**Sperret, med filnavn i oppdraget:** koder 1s verdiktfil, nøkkelfilen, den sammenstilte fasiten,
tvilsfilen, dommerfilene, `presisjon-resultater.json`, LAERDOM, resultatnotatet, manuskriptet,
PS-246-filene, ADDENDUM-10 i sin helhet og alt på Vault. `git log` og `git show` var forbudt.
Koder 2 bekrefter i sin sluttrapport at ingen av dem ble åpnet.

**Regelfilen er sjekket for lekkasje:** null treff på presisjonstall, M1, M2, klassefordeling,
PS-identifikatorer eller ADDENDUM-10s utfallstabell. Koder 2 fikk ingen forventet treffrate.

**Kodingen** gikk gjennom alle 320 i blindfilens rekkefølge, i én sammenhengende økt, med samme
felter som koder 1: `id`, `ekte_treff`, `min_klasse`, `min_bedømbar`, `tvil`, `begrunnelse`.

## 3 Hvor uavhengigheten ikke rekker

1. **Samme modellfamilie.** Begge kodere er LLM-baserte, av samme familie, med samme
   treningsfordeling. Dette måler om regelsettet gir samme utfall i to uavhengige lesninger —
   ikke om et menneske ville lest likt. **Ingen menneskelig annotør har vurdert materialet.**
2. **Samme orkestrator.** Oppdraget til koder 2 er formulert av den samme instansen som var koder 1.
   Sperrelisten er verifiserbar, formuleringen er det ikke.
3. **En feil i regelfilen, som er vår og ikke koder 2s.** Utdraget fra ADDENDUM-05 avkuttet tabellen,
   slik at bare `H1/H7-uavklart` sto eksplisitt navngitt. Koder 2 rapporterte dette selv og brukte
   derfor ikke de tre øvrige uavklarte parene. Klasseenigheten under er målt med den begrensningen
   på koder 2s side.
4. **Tre tolkningslinjer koder 2 måtte feste selv**, fordi reglene ikke avgjør dem: at «ugjort uten
   navngitt hindring» kodes N3 og ikke uavklart; at feltgap og nyhetspåstander samles i N2 mens
   tredjeparts hindringer havner i INGEN eller N3; og hva `min_bedømbar` skal bety. Den siste viser
   seg å være avgjørende, se §5.

## 4 κ

Hovedsammenlikningen er mot koder 1 **etter ADDENDUM-10**, fordi begge kodere da hadde samme
regelsett. Intervallene er paret bootstrap, 10 000 gjentak, frø 734248.

| sammenlikning | n | rå enighet | κ | 95 % KI |
|---|---|---|---|---|
| treff / ikke-treff, alle 320 | 320 | 96,2 % | **0,812** | 0,697–0,906 |
| treff / ikke-treff, kun portmaterialet | 300 | 96,7 % | **0,774** | 0,623–0,898 |
| klasse blant passasjer begge kodet som treff | 30 | 86,7 % | **0,732** | 0,481–0,936 |
| klasse, uavklarte par slått sammen med naboen | 30 | 90,0 % | **0,734** | 0,371–1,000 |
| mot koder 1s **første** lesning (før ADDENDUM-10) | 320 | 96,6 % | 0,826 | 0,712–0,917 |

Asymptotisk intervall for hovedtallet (Fleiss, Cohen & Everitt): 0,710–0,915. Bootstrap er oppgitt
som hovedtall fordi cellene er små.

**Per felt** (treff/ikke-treff): klinisk epidemiologi κ 1,000 (n = 52) · tekstvitenskap 0,847 (53) ·
arkeologi 0,748 (94) · **energimodellering 0,390 (101)** · ankerne 0,792 (20).
Gruppert: biomed 0,943 · humaniora 0,796 · teknisk 0,390. Grupperingen er laget her, ikke
preregistrert: humaniora = tekstvitenskap og arkeologi, biomed = klinisk epidemiologi,
teknisk = energimodellering.

**Uenighetene er få og konsentrerte:** 12 av 320 på treffstatus, 4 på klasse. Alle 16 er ført i
`data/koder2-sammenlikning.json` med passasje og begge lesninger.

## 5 Hvordan hovedtallene flytter seg

| tall | koder 1 | koder 2 |
|---|---|---|
| presisjon | 25/150 = **16,7 %** [11,6–23,4] | 19/150 = **12,7 %** [8,3–18,9] |
| M1-passasje korrigert | **0,671** | **0,604** |
| M1-streng korrigert | 0,667 | 0,599 |
| M1-rå, minst ett treff | 0,930 | 0,930 |
| **M2 på leste ekte treff** | **22/25 = 88,0 %** | **6/19 = 31,6 %** |
| løftbar andel (H1–H6) | 5/25 = 20,0 % | 2/19 = 10,5 % |
| klassefordeling | H7 17, H5 3, H8 2, H2 2, H9 1 | H7 12, H1/H7-uavklart 2, H9 2, H5 1, H2 1, H8 1 |
| bom blant INGEN / N3 | 2,0 % / 2,0 % | 2,0 % / 2,0 % |

**Hovedfunnet står i begge lesninger.** H7 dominerer: 17 av 25 (68 %) hos koder 1, 12 av 19 (63 %)
hos koder 2. Presisjonsintervallene overlapper i hele sin bredde, og M1-rå er identisk fordi
ADDENDUM-11 ikke rører dommerens utdata.

**M2 overlever ikke.** 88,0 % mot 31,6 % er ikke støy, det er to ulike spørsmål: koder 1 leste
«lar bedømbarheten seg avgjøre uten domeneekspert» som et spørsmål om hindringens *art*, koder 2
som et spørsmål om fagets *nåværende metode- og datalandskap*. Begge lesninger er forenlige med
PREREG-v1 §2, som ikke definerer «domeneekspert». **M2 skal derfor ikke rapporteres som ett tall
uten koderidentitet**, og definisjonen må skjerpes før M2 brukes videre. Det er denne målingens
tydeligste enkeltresultat.

**Energimodellering er den svake sømmen.** κ 0,390 mot 0,943 i biomed. **Seks av de tolv**
uenighetene om treffstatus gjelder samme strid: en modell-, metode- eller omfangsbegrensning som
koder 1 leser som navngitt hindring og koder 2 som selvpålagt forenkling (PS-027, PS-031, PS-119,
PS-133, PS-202, PS-226 — alle kodet N3 av koder 2). Av de seks øvrige leser koder 2 tre som besvart
i samme passasje (N1: PS-010, PS-292, PS-315), og i tre finner koder 2 et treff koder 1 ikke fant
(PS-134, PS-258, PS-288). ADDENDUM-10 §3 skulle avgjøre den første gruppen, og gjør det ikke godt nok.

## 6 Hva som ikke endres

Ingen av koder 1s verdikter er endret. De to fasitene står ved siden av hverandre, og alle tall i
§5 oppgis parvis. Ingen sammenslått fasit er laget, og ingen tredje koder er brukt til å bryte
uenigheter — en slik «avgjørende stemme» ville vært den samme instansen som var koder 1.

## 7 Rettelse 2026-09-25, samme dag

Første utgave av dette addendumet sa at uenighetene i energimodellering «gjelder alle samme form».
Ved opptelling mot `data/koder2-sammenlikning.json` fordeler de tolv uenighetene om treffstatus seg
**6 / 3 / 3**: seks der koder 2 kodet N3 (selvpålagt forenkling, metode- eller omfangsvalg), tre der
koder 2 kodet N1 (besvart i samme passasje), og tre der koder 2 fant et treff koder 1 ikke fant.
Formuleringen «alle samme form» var et inntrykk, ikke en telling.

Samme feil sto som «åtte av tolv» i resultatnotatet, LAERDOM og manuskriptet, og er rettet til seks
alle fire steder. Slutningen står: den største enkeltgruppen er striden om modellforenklinger, og
den utgjør halvparten av uenighetene — men halvparten er ikke to tredeler, og tallet skal være talt.

## 8 Datert note 2026-09-27: regelfilen er gjenvunnet, og lekkasjesjekken er nå verifisert

Regelfilen §2 beskriver — `scratchpad/koderegler.md` — lå aldri i git og finnes ikke lenger på disk.
**Hele innholdet er gjenvunnet fra koder 2s egen øktutskrift** 27.09.2026:
`…/subagents/agent-abf6e3798610fb9c1.jsonl` linje 13, Read-resultatet da koder 2 åpnet filen
25.09.2026 kl. 19:35. 167 linjer, 9 805 bytes, sha256
`234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449`. Ført i
`docs/REGELFIL-KODER2-GJENVUNNET-2026-09-27.md`, på Vault som `koder2/koderegler-gjenvunnet.md`, og i
`docs/METODE.md` §4. Ingenting er rekonstruert.

**Filen er ekte, ikke gjenskapt.** Tre uavhengige kontroller:

1. **Rekkefølgen** på de seks kildene er nøyaktig den §2 lister.
2. **Defekten §3.3 forutsier, er der — med riktig antall.** ADDENDUM-05-blokken slutter på kildens
   linje 72, tabellhodet, og de **tre** dataradene (H2/H7, H3/H7, H5/H7) mangler. §3.3 sier at koder 2
   «derfor ikke brukte de tre øvrige uavklarte parene».
3. **Innholdet er ordrett** mot de låste kildene: PREREG-v1 §2 4/4 linjer, §5 19/19, ADDENDUM-03 §1.2
   10/10, ADDENDUM-04 §4 16/16, ADDENDUM-10 §1–3 27/27, ADDENDUM-05 40/40 etter at grep-prefikset er
   trukket fra.

**Lekkasjepåstanden i §2 er nå målt, ikke bare hevdet.** Null treff på «16,7», «22 243», «2 173»,
«0,93», «88,0», «31,6», «PS-», «presisjon», «treffrate», «forventet», «kappa», «κ», «M1-rå», «fasit».

**En defekt mer, som ikke sto noe sted.** ADDENDUM-05-blokken er limt inn som `grep -n`-utdata: hver
linje bærer kildens linjenummer og et skilletegn som skiller treff (`29:`) fra kontekst (`30-`), og
seks linjer i spennet 29–72 er utelatt (50, 65–69). Innholdet er ordrett, men **formen fortalte koder
2 hvilke linjer et søk hadde truffet på.** De fem andre blokkene har det ikke. Det lekker ingenting
om svarene og endrer ingen κ-verdi, men det er en kanal §3 ikke fører — og den er sannsynligvis også
årsaken til den avkuttede tabellen: `grep`-vinduet nådde tabellhodet og stoppet.

**Hva som følger:** κ = 0,812 kan reproduseres på sin egen inndata.

**Lagt til samme dag: modell-ID og kostnad er også gjenvunnet.** Addendumet førte ingen
modellsignatur for koder 2, i strid med ADR-0003. Den står i utskriften: **`claude-opus-5`**, ført i
hvert av de 61 API-svarene i økten. Kjøringen tok **20 minutter** (25.09.2026 kl. 17:14:53–17:35:26)
og kostet **9 019 781 tokens inn** (122 ubufret, 457 398 buffer skrevet, 8 562 261 buffer lest) og
**103 373 tokens ut**. Koder 2 var altså en CC-instans på Opus 5, agentisk, med seks regelkilder —
**ikke et menneske.** §3.1s setning «Ingen menneskelig annotør har vurdert materialet» står og er
korrekt. Vekt-sha finnes ikke for en API-modell og kan ikke gjenvinnes.
