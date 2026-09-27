# Gjenopptak — preregistrering v1

**Låst:** 2026-09-12
**Eier:** Eirik Botten Nicolaysen, EcoDeco AS (org.nr. 936 320 856)
**Repo:** gjenopptak
**Denne filen redigeres aldri.** Operasjonaliseringer etter lås føres som ADDENDUM-NN med egen sha256.

## 1 Hypotese

1. Det finnes forskningsspor der forfatteren selv skrev ned hva de ikke fikk gjort og navnga hindringen.
2. En del av disse hindringene er i dag opphevet, en andel av dem av AI.
3. Den delmengden lar seg finne systematisk, på tvers av felt.

## 2 Hva som måles

**M1 — prevalens.** Andel artikler med minst ett parkert spørsmål: en setning der forfatteren navngir noe de ikke fikk gjort OG oppgir en hindring.

**M2 — bedømbarhet.** Andel av treffene der spørsmålet «er hindringen opphevet i dag» lar seg avgjøre uten domeneekspert i faget.

Begge oppgis rått, per felt og samlet, med usikre i egen kolonne.

## 3 Hva som IKKE måles

- om spørsmålet er verdt å svare på
- om forfatteren hadde rett i at det var umulig
- om noen burde ha fulgt opp
- hvor mye tid en gjenopptakelse ville spart

## 4 Utvalg

**Formålsvalgt, ikke representativt.** Fire felt valgt fordi de har ulik hindringstype. Dette er designets nest største begrensning etter én-koder-svakheten og står i sammendraget av enhver rapport.

| Felt | Begrunnelse |
|---|---|
| historisk tekstvitenskap / diplomatisk kildeutgivelse | H1–H2; eier kan bedømme opphevelse uten å spørre noen |
| klinisk epidemiologi / journalgjennomgang | H8 dominerer; felt der AI ofte IKKE løfter |
| arkeologi | H4, bilde- og signalmønster |
| energisystemmodellering | H5; bærer den positive kontrollen |

- Ramme: OpenAlex, `has_fulltext: true`, publiseringsår 2015–2020.
- n = 25 per felt, 100 totalt. Trukket tilfeldig innen felt.
- Presisjonen per felt (±14 prosentpoeng) er utilstrekkelig per felt og tilstrekkelig for spørsmålet om klassen finnes på tvers av fag. Det er tilsiktet.

**Frø.** Frøet er de første åtte heksadesimale tegnene i sha256 av denne filen. Verdien kan ikke stå her og føres i ADDENDUM-01 sammen med de oppløste OpenAlex-emne-ID-ene per felt. Trekking skjer først etter at ADDENDUM-01 er skrevet.

**Korpusgrense.** Fulltekst finnes for 52 249 064 av 326 944 662 works i OpenAlex (16 %), skjevt mot nyere, engelskspråklig og open access. Humaniora publiserer i monografi og er tynnest dekket. Verktøyet sveiper åpen fulltekst, ikke litteraturen. Oppgis i all rapportering.

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

## 6 Terskler, tallfestet før data

| Måling | Terskel | Konsekvens |
|---|---|---|
| M1 prevalens | < 5 % | sporet parkeres |
| M1 prevalens | 5–20 % | analyseverktøy, ikke tjeneste |
| M1 prevalens | > 20 % | bygges og skrives opp |
| M2 bedømbarhet | < 30 % | kandidatgenerator med menneskelig lesning, og det sies |
| M2 bedømbarhet | > 60 % | detektor |
| Overlevelse i falsifiseringstesten | < 50 % | klassifiseringen er ikke pålitelig nok; stopp |
| Lokal modells enighet med eiers koding | < 70 % | arkitektur B: lokal filtrering, ekstern adjudikasjon, dommer oppgis per oppføring |

## 7 Kontroller

**Positiv kontroll:** Hirth, Mühlenpfordt & Bulkeley 2018 (10.1016/j.apenergy.2018.04.048) legges inn i energiutvalget som kjent treff. Koder rubrikken den ikke som treff, er rubrikken feil og alt stopper. Én positiv kontroll til per øvrig felt velges og føres i ADDENDUM-02 før lesing.

**Negativ kontroll:** ti artikler kodes blindt i andre runde, minst sju dager senere eller av annen instans. Uenighet rapporteres som rå prosent. Dette er ikke κ og skal ikke presenteres som det.

## 8 Falsifiseringstest

For hver kandidat merket «hindringen er opphevet, spørsmålet står åpent»: søk siteringsgrafen (OpenAlex `cites:`) etter om noen alt har svart. Treff ⇒ kandidaten er gal.

**Dekningsgrad rapporteres per felt** som andel siterende arbeider med tilgjengelig fulltekst. Lav dekning svekker kandidaten og styrker den aldri. Uten dette rapporteres høyest overlevelsesrate der grunnlaget er dårligst.

Måltallet er hvor mange kandidater som overlever, ikke hvor mange som ble foreslått.

## 9 Kjente svakheter

1. **Én koder.** Designets hovedsvakhet. Hører i sammendraget, ikke i vedlegg.
2. Formålsvalgt utvalg, se §4.
3. Korpusgrensen på 16 %, se §4.
4. **Terskelfølsomhet.** Enhver inaktivitets- eller aldersgrense oppgis med følsomhetsanalyse. Referanse: en grense flyttet fra 1 til 36 måneder endret antall «forlatte» i SciCat fra 18 030 til 8 010, faktor 2,25 på ett metodevalg.

## 10 Avgrensning mot eksisterende arbeid

- **Stent 1972 / Hook 2002 (prematuritet):** hindringen der er konseptuell (H9); vår er ressurs- og evnemessig (H1–H6). Motsatt ende av samme akse.
- **Sleeping beauties (van Raan 2004 m.fl.):** måler siteringsbaner, altså resepsjon. Vår klasse er forfatterens nedskrevne innrømmelse. Rammen lånes ikke.
- **Self-admitted technical debt:** nærmeste metodiske analog, fra kodekommentar til artikkeltekst.
- **Uttrekk av limitations/future work:** tatt. Vårt tillegg er klassifisering av hvorfor, og kryssing mot tidsaksen. Metodekrav som følger: hele teksten skannes, ikke bare limitations-seksjonen.
- **LLM-agenter for gap- og idégenerering:** peker framover. Vi peker bakover på en datert innrømmelse og tester om hindringen falt bort.
