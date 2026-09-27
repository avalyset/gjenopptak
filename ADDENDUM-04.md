# ADDENDUM-04 — hentbar tekst i rammen

**Skrevet:** 2026-09-12
**Hører til:** PREREG-v1.md `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`,
ADDENDUM-01.md `aa78d1be50ac17f8e26a92513aa115b3d504bdde3556e43b4f2317ea47cc255f`,
ADDENDUM-02.md `7c0542c92c54a586e3b387794272bed171ee285b75c8ebe4ee8fe1fa16f6f713`,
ADDENDUM-03.md `0b577ae6c3d0278e811e674c78e4e2948be46252e5aca9c94e94466c1f985c4e`
**Status:** operasjonalisering etter lås, med **redefinert utvalgsramme** (§1) og **to innsnevringer** (§3, §4). Skrevet før trekking. Ingen av de fire låste filene er endret.

---

## 1 Rammen er hentbar tekst, ikke OA-status

### 1.1 Beslutningen

Utvalgsrammen er ikke lenger åpen tilgang alene. **Et verk er i rammen når den tredelte porten faktisk gir en fil med uttrekkbar tekst.** Rammen er to ledd:

```
LEDD 1 (tellbart filter, OpenAlex)
  topics.id:<feltets ID-er>,publication_year:2015-2020,open_access.is_oa:true

LEDD 2 (hentingsprøve, bestått/ikke bestått)
  P1  Europe PMC har pmcid, inEPMC=Y, isOpenAccess=Y
        -> JATS fra /{pmcid}/fullTextXML gir >= 20 setninger
  P3  best_oa_location.pdf_url svarer 200 med en PDF
        -> uttrekk gir >= 2 000 tegn
  bestått = P1 eller P3 lykkes. Ellers: utenfor rammen.
```

P2 (OpenAlex' TEI-arkiv) inngår ikke i rammekriteriet. Ruten krever API-nøkkel, og den offentlige ruten er valgt nettopp for at sveipet skal kunne kjøres uten nøkkel og uten budsjett (ADDENDUM-02 §8.1). Tas P2 i bruk senere, utvider den rammen og skal da føres som en ny rammeversjon, ikke som en stille forbedring.

### 1.2 Begrunnelse

ADDENDUM-03 §2 målte faktisk nedlastbarhet på 30 verk per felt: **43 % / 47 % / 33 % / 17 %** for tekstvitenskap, klinisk epidemiologi, arkeologi og energimodellering. To tredeler av forsøkene feilet.

**Frafallet er ikke tilfeldig.** Det fordeler seg etter forlegger og plattform:

* Alle fem ScienceDirect-treffene i energimodellering ga 403. Den positive kontrollen i PREREG §7 ligger på samme vert og gir samme svar.
* Arkeologi manglet registrert PDF-lenke i halvparten av utsnittet (15 av 30).
* Den største enkeltårsaken samlet er verk registrert som åpne uten noen PDF-lenke: 44 av 120, altså 37 %.

Substitusjon forutsetter at frafallet er tilfeldig. Er det systematisk, gjør substitusjon noe annet enn å reparere: den fyller plassene med verk fra de *hentbare* forleggerne og skjuler seleksjonen i et substitusjonstall, mens nevneren later som om den gjelder rammen. Med hentbarhet i rammen er nevneren kjent, og seleksjonen står i metoden der en leser ser den.

Valget er altså mellom en ærlig, smalere ramme og en bredere ramme med skjult skjevhet. Denne beslutningen velger det første.

### 1.3 Hva det koster

Rammen blir mindre, og hvor mye vet vi ikke før hentingsprøven er kjørt på hele listen. Anslag fra ADDENDUM-03, med brede intervaller: energimodellering faller fra 30 362 til i størrelsesorden 5 000 verk (17 %, 95 %-intervall 7–34 %), arkeologi fra 37 510 til om lag 12 500, klinisk epidemiologi fra 43 986 til om lag 20 500, tekstvitenskap fra 66 830 til om lag 29 000. Alle fire er fortsatt langt over n = 25.

Prøven må kjøres på hele rammelisten, ikke bare på de trukne. Det er arbeidet som gjør nevneren kjent, og det er prisen for §1.

---

## 2 Konsekvens for tolkningen

**M1 er prevalens av parkerte spørsmål blant verk som er både åpne og hentbare, i fire formålsvalgte emnerammer, 2015–2020.** Det er en sterkere seleksjon enn OA-betingelsen alene, fordi den i tillegg velger bort forleggere som blokkerer maskinell nedlasting, og verk der ingen PDF-lenke er registrert.

**Formuleringen som skal stå i sammendraget av enhver rapportering**, ved siden av én-koder-svakheten (PREREG §9) og OA-forbeholdet (ADDENDUM-02 §5):

> Rammen er verk som er åpent tilgjengelige **og** hentbare på den offentlige ruten. Verk hos forleggere som blokkerer maskinell nedlasting, og verk uten registrert PDF-lenke, er utenfor rammen — ikke substituert bort, men aldri inne. Målt på 30 verk per felt gjaldt dette 53–83 % av de åpne verkene.

**Utelatte verter, målt i ADDENDUM-03 §2.2.** Listen er ikke uttømmende — den er hva 120 forsøk traff — og den skal oppgis som eksempler, ikke som en komplett ekskluderingsliste:

* **HTTP 403, blokkert maskinell nedlasting:** sciencedirect.com (5 forsøk), escholarship.org (2), academic.oup.com, adc.bmj.com, bmjopen.bmj.com, brill.com, clinicalradiologyonline.net, epj-conferences.org, persee.fr, publish.csiro.au, rees-journal.org, scholarworks.waldenu.edu, science.org.
* **HTTP 200 med HTML-landingsside i stedet for PDF:** mdpi.com (2), aimspress.com, cambridge.org, doi.org, iopscience.iop.org, lup.lub.lu.se, urn.nb.no, zora.uzh.ch.
* **Nettverksfeil ved gjentatte forsøk:** bcps.journals.ekb.eg, periodicos.unb.br, repositorio.inesctec.pt.
* **Annet:** eap-iea.org (404), hdl.handle.net (500), eprints.ums.edu.my og paediatricaindonesiana.org (PDF uten uttrekkbar tekst).

Fagprofilen til disse vertene er ikke tilfeldig fordelt. Brill og Persée bærer humaniora; ScienceDirect og IOP bærer ingeniørfag; BMJ og OUP bærer medisin. Rammen velger derfor ikke bare bort forleggere, men også deler av fagene, og en forskjell mellom feltene i målt M1 kan være en forskjell i hvem som blokkerer. Det skal sies hver gang feltene stilles opp mot hverandre.

---

## 3 ADDENDUM-01 §6 innsnevres

Substitusjonsregelen gjaldt verk som viser seg uhentbare. Med §1 er uhentbare verk ikke i rammen, og kan derfor ikke trekkes.

**Substitusjon gjelder nå bare ekte enkeltfrafall:** et verk som besto hentingsprøven ved frysing, men ikke lar seg hente ved innsamling. Lenker som råtner, verter som endrer tilgang, filer som forsvinner. Årsakskategoriene i ADDENDUM-01 §6 beholdes, men `ingen_rute` og `lisens` skal ikke forekomme lenger — de er rammekriterier nå — og opptrer de likevel, er det et tegn på at hentingsprøven og innsamlingen ikke bruker samme port.

**Forventet rate er nær null**, og **stoppregelen på >25 substitusjoner blir meningsfull igjen**: utløses den, er noe galt med listen eller porten, ikke med litteraturen.

**Flaggene i ADDENDUM-03 §2.3 bortfaller.** Arkeologi (75 trekk for 25 plasser) og energimodellering (150) var flagget fordi frafallet lå inne i rammen. Det frafallet ligger nå utenfor. Tallene i ADDENDUM-03 står som måling av hva den offentlige ruten gir, og de er grunnlaget for §1 — men de er ikke lenger anslag på hvor mange trekk innsamlingen krever.

Merk hva som ikke forsvinner: arbeidet. Hentingsprøven må gjøres på hele rammelisten, så nedlastingsforsøkene er de samme. Forskjellen er at de nå gjøres én gang, i lys, som en del av rammedefinisjonen — ikke løpende, som reparasjon av et utvalg.

---

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

## 5 Kvotemodellen

Verifisert i **ADDENDUM-03 §5** (ikke §0; kvotemålingen står i §5):

| | |
|---|---|
| tak | **1 000 kall per døgn** |
| modell | $0,10 gratiskreditt à $0,0001 per kall |
| polite pool | **finnes ikke** — `mailto` gir samme tak, målt i tre varianter |
| nullstilling | om lag 11 timer fra taket nås |

**Frysing av fire rammelister er fire døgn**, ett felt per døgn: 335 + 220 + 188 + 152 = 895 kall i alt (ADDENDUM-03 §5.2). Listene lagres med sha256 og fryses én gang.

Rekkefølgen er energimodellering først: feltet har lavest hentbarhet og bærer den positive kontrollen. Går frysingen og hentingsprøven der, går de overalt.

**Hentingsprøven i §1 bruker ikke OpenAlex.** Den går mot Europe PMC og PDF-verter, og kan derfor kjøres samme døgn som en frysing, eller mellom døgnene.

---

## 6 Erklæring

* **Ingen trekking av utvalg er utført.** En rå rammeliste er ikke et utvalg.
* Ingen fulltekst er hentet under arbeidet med dette addendumet.
* **PREREG-v1.md og ADDENDUM-01/02/03.md er uendret**, sha256 `05988b23…ba23a`, `aa78d1be…c255f`, `7c0542c9…f713`, `0b577ae6…5c4e`.
* Ingen remote, ingen push, ingen nøkkel opprettet.
* Åpne poster: hentingsprøven på hele rammelisten (§1.3); positiv kontroll i H1 eller H4 (§4); frysing av de tre øvrige feltene (§5); energikontrollens seksjon; tekstvitenskapskontrollen; og postene i ADDENDUM-02 §9 som fortsatt står.
