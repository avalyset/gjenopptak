# ADDENDUM-03 — observasjonsenhet, nedlastbarhet, løftbar kontroll

**Skrevet:** 2026-09-12
**Hører til:** PREREG-v1.md `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`,
ADDENDUM-01.md `aa78d1be50ac17f8e26a92513aa115b3d504bdde3556e43b4f2317ea47cc255f`,
ADDENDUM-02.md `7c0542c92c54a586e3b387794272bed171ee285b75c8ebe4ee8fe1fa16f6f713`
**Status:** operasjonalisering etter lås, med **én korreksjon av observasjonsenheten** (§1). Skrevet før trekking. Ingen av de tre låste filene er endret.

---

## 1 Observasjonsenheten er passasjen

### 1.1 Defekten

PREREG §2 definerer et treff som **én setning** der forfatteren navngir noe de ikke fikk gjort **og** oppgir hindringen. Kjeden bærer samtidig et kontekstvindu på ±2 setninger i `candidates.jsonl`. Uttrekket var altså definert på passasje og målingen på setning — to enheter i samme kjede, uten at noen av dem var valgt framfor den andre.

Kostnaden ble målt i ADDENDUM-02 §2.5. To nærtreff i historisk tekstvitenskap ble forkastet fordi hindringen sto i nabosetningen, ikke i treffsetningen:

* 10.5282/journalipp/4841 — «we were unable to consult the work», med utilgjengeligheten forklart i setningen etter.
* 10.1515/sm-2017-0003 — «we were unable to reach an exact official number of Assyrians», hindringen likeså.

Feltet endte uten positiv kontroll. Det var ikke fordi parkerte spørsmål manglet, men fordi kriteriet krevde at to opplysninger sto i samme setning.

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

### 1.3 Felter

`candidates.jsonl` og `claims.jsonl` bærer:

* `unit` ∈ {`sentence`, `passage`} — hvor snevert kriteriet ble oppfylt. Påkrevd, lukket sett, ingen standardverdi.
* `passage_span` — `start_index`, `end_index`, `n_sentences`, `window`, i setningsindekser fra `sentences.jsonl`. Påkrevd.

`unit` ligger i `candidates` og ikke bare i `claims`, fordi M1-streng og M1-passasje regnes på kandidatnivå. Skjemaene og testene er oppdatert; en post uten `unit` er ugyldig og telles ikke.

Uttrekket er implementert i `src/gjenopptak/extract/passage.py`. Modulen gir `split_counts` og `format_m1`, som alltid returnerer begge tallene. **Den tilbyr ingen funksjon som returnerer ett samlet M1** — samme håndhevingsform som ADR-0007 punkt 4.

---

## 2 Faktisk nedlastbarhet

R3 i ADDENDUM-01 §5 teller registrerte PDF-lenker. ADDENDUM-02 §2.4 viste at den positive kontrollens lenke svarer 403. Her er det ekte tallet målt.

**Framgangsmåte.** 30 verk per felt, trukket med målefrøet 734 248 (ikke prereg-frøet) fra det lagrede R0-utsnittet og lokalt begrenset til `open_access.is_oa` og vinduet — altså et tilfeldig utsnitt av rammen i ADDENDUM-01 §3.1. Utsnittet er hentet fra rådata som alt lå på disk, fordi OpenAlex-kvoten var oppbrukt (§5); regelen ved flere lagrede filer er leksikografisk minste filnavn. Hvert verk ble forsøkt hentet gjennom porten JATS → TEI → PDF, med egen ærlig User-Agent. **Ingen blokkering er omgått**, ingen user-agent-spoofing, ingen alternative kilder. En 403 er et måleresultat.

«Lesbar tekst» betyr: JATS som gir minst 20 setninger gjennom parseren, eller PDF som gir minst 2 000 tegn.

### 2.1 Hva porten ga

| felt | lesbar tekst | via P1 JATS | via P3 PDF | ingen PDF-lenke |
|---|---|---|---|---|
| tekstvitenskap | **13/30 = 43 %** | 0 | 13 | 10 |
| klinisk epidemiologi | **14/30 = 47 %** | 7 | 7 | 8 |
| arkeologi | **10/30 = 33 %** | 1 | 9 | 15 |
| energimodellering | **5/30 = 17 %** | 0 | 5 | 11 |

**P2 ble ikke forsøkt.** OpenAlex' fulltekstarkiv krever API-nøkkel, og ingen er opprettet (ADDENDUM-02 §8.1). Tallene er altså hva den offentlige ruten gir.

P1 bekrefter ADDENDUM-01 §5.2 på nytt, nå på et uavhengig utsnitt: null JATS i tekstvitenskap og energimodellering, én i arkeologi.

### 2.2 Hvorfor de 78 feilet

| feilklasse | antall (av 120) |
|---|---|
| ingen PDF-lenke registrert i det hele tatt | **44 (37 %)** |
| HTTP 403 — blokkert | **18 (15 %)** |
| HTTP 200, men HTML-landingsside i stedet for PDF | 9 (8 %) |
| nettverksfeil (timeout, connect) | 3 (2 %) |
| HTTP 200, PDF uten uttrekkbar tekst | 2 (2 %) |
| HTTP 404 | 1 |
| HTTP 500 | 1 |
| **sum feilet** | **78 (65 %)** |

Den største enkeltårsaken er ikke blokkering, men at **verket er registrert som åpent uten at noen PDF-lenke finnes**: 37 % av de 120. I arkeologi gjelder det halvparten av utsnittet.

**403 etter vert:** sciencedirect.com 5, escholarship.org 2, og én hver fra brill.com, persee.fr, publish.csiro.au, scholarworks.waldenu.edu, adc.bmj.com, academic.oup.com, clinicalradiologyonline.net, bmjopen.bmj.com, science.org, epj-conferences.org, rees-journal.org. Blokkeringen er altså ikke ett forlags særtrekk, men spredt over store forlag, tidsskriftplattformer og institusjonelle arkiv. De fem ScienceDirect-403-ene ligger alle i energimodellering, som er det feltet den positive kontrollen tilhører.

**200-med-HTML** er verter som svarer på PDF-URL-en med en landingsside: cambridge.org, doi.org, zora.uzh.ch, urn.nb.no, mdpi.com (2), aimspress.com, iopscience.iop.org, lup.lub.lu.se. Teknisk sett ikke en blokkering, men like utilgjengelig for kjeden.

### 2.3 Substitusjonsrate

Med `p` = andel som gir lesbar tekst, trengs `n/p` trekk for å fylle n = 25 plasser, og `n(1−p)/p` substitusjoner. Wilson-intervall på p, 95 %:

| felt | p (95 %-int.) | forventet antall trekk | intervall | forventede substitusjoner | trekk for 95 % sikkerhet | flagget |
|---|---|---|---|---|---|---|
| tekstvitenskap | 43 % (27–61 %) | **58** | 41–91 | 33 | 73 | nei |
| klinisk epidemiologi | 47 % (30–64 %) | **54** | 39–83 | 29 | 67 | nei |
| arkeologi | 33 % (19–51 %) | **75** | 49–130 | 50 | 96 | **JA** |
| energimodellering | 17 % (7–34 %) | **150** | 74–341 | 125 | 198 | **JA** |

**Arkeologi og energimodellering flagges**: forventet antall trekk overstiger 60. Energimodellering trenger seks trekk per plass, og den øvre enden av intervallet er 341 trekk for 25 verk.

**To forbehold som ikke skal skilles fra tallene.**

1. `n/p` er et punktanslag som holder om lag halvparten av gangene. Kolonnen «trekk for 95 % sikkerhet» er tallet reservelisten faktisk må ha, og **den er over 60 for alle fire felt** — også for de to som ikke flagges på punktanslaget.
2. p er målt på 30 forsøk per felt. Intervallene er brede, og for energimodellering (5 av 30) er nedre grense 7 %, som ville betydd 341 trekk.

**Konsekvens for designet.** Substitusjonsregelen i ADDENDUM-01 §6 har en stoppregel: overstiger antall substitusjoner antall plasser (>25), stopper feltet. Med de målte ratene vil **alle fire felt utløse den stoppregelen** — forventede substitusjoner er 29–125 mot 25 plasser. Stoppregelen er altså for stram til å være brukbar slik den er skrevet, og eier må velge:

* heve stoppgrensen til et tall som følger av de målte ratene, oppgitt i et nytt addendum, eller
* redusere n per felt, eller
* ta P2 i bruk og oppgi det som rute, med tilgangsbetingelsen synlig (ADDENDUM-02 §8.1).

Valget kan ikke tas av den som måler. Tallene over er grunnlaget.

De 120 verkene er loggført i `data/leste-kontrollkandidater.json` og utelates fra trekkingen. **Ingen av de 120 er lest** — bare nedlastingsstatus og om filen inneholder tekst er registrert. Loggen har nå 199 oppføringer i alt: 56 fra kontroll- og ankersøket i ADDENDUM-02, disse 120, og 23 fra H1/H4-søket i §3 — 180 unike DOI-er.

---

## 3 Løftbar positiv kontroll

Begge kontrollene i ADDENDUM-02 er H7/H8, altså ikke-løftbare. Rubrikkens løftbare ende var uprøvd, og det er den ende verktøyet hviler på.

### 3.1 H1 — funnet

| felt | DOI | klasse | seksjon | `section_label_provenance` | `unit` |
|---|---|---|---|---|---|
| klinisk epidemiologi | **10.4073/cmdp.2018.2** | **H1** | `Critical appraisal of included studies` | `source` | `sentence` |

Passasjen (setning 265 av 711, PMC8428058): forfatterne beskriver at kritisk vurdering av primærstudier **ikke** gjøres i deres kartleggingsarbeid, og oppgir hvorfor i samme setning — arbeidet «**does not conduct critical appraisal … too time consuming**» gitt tidsrammen på 3–6 måneder som kartene lages innenfor.

* **Det ugjorte:** kritisk vurdering av primærstudiene.
* **Hindringen:** menneskelig gjennomgang i skala tar for lang tid innenfor tidsrammen.
* **Klasse H1**, løftbar `ja` ved oppslag i PREREG §5. Kontrollen prøver dermed rubrikken i den løftbare enden.
* Innenfor rammen per konstruksjon: kandidaten er hentet fra et lagret rammesøk med feltets filterstreng. Publiseringsår 2018. Hentbar som JATS via Europe PMC.

**Nyanse som skal stå:** setningen er skrevet i tredjeperson om forfatternes egen organisasjon, ikke som «vi». Det er fortsatt forfatternes beskrivelse av eget arbeidstrinn og eget grunnlag for å utelate det, og rubrikken skal kode den som treff. En koder som krever førsteperson vil kode den som ikke-treff, og det er da rubrikken som er uklar, ikke kontrollen.

### 3.2 H4 — armert nullresultat

**Ingen H4-kontroll er funnet.** Nullresultatet er armert på to måter:

1. **Kontrollstreng:** passasjesøket ble kjørt mot en kjent Europe PMC-artikkel (PMC4875724) før feltsøket. Den ga 291 setninger og én kandidatpassasje — søket virker.
2. **Ikke-tomt nabolag:** 104 lagrede JATS-filer fra rammesøkene ble gjennomsøkt, og 7 passasjer med både bilde-/signalord og skalaord ble funnet. Ingen av dem er H4: de handler om sekvensdata, registerdata og manglende kliniske opplysninger, ikke om mønstergjenkjenning i bilder eller signaler i volum.

**Begrensning som gjør nullresultatet svakere enn det ser ut.** Søket var bundet til kandidatlister som alt lå på disk, fordi OpenAlex-kvoten var 0 (§5). Et fritt H4-søk i rammene — `fulltext.search` på «manual segmentation», «visual inspection of all images» og liknende, innenfor hver feltramme — **ble ikke gjort**. Nullresultatet gjelder det materialet som var tilgjengelig uten kvote, ikke rammene. Det bør gjentas når kvoten er tilbake, og posten står åpen til da.

### 3.3 Kontrollstatus etter denne slyngen

| klasse | kontroll | løftbar |
|---|---|---|
| H1 | 10.4073/cmdp.2018.2 | ja |
| H7 | 10.1038/s41467-019-11357-9 | nei |
| H8 | 10.1016/s2468-2667(17)30217-7 | nei |
| H4 | **mangler** (armert nullresultat) | ja |
| energifeltets kontroll | 10.1016/j.apenergy.2018.04.048 — seksjon fortsatt uverifisert (§4) | — |
| tekstvitenskapsfeltet | **mangler** — men §1 endrer forutsetningen, se under | — |

**§1 gjenåpner tekstvitenskapsposten.** De to nærtreffene i ADDENDUM-02 §2.5 ble forkastet på setningskravet. Under passasjekravet kan de kvalifisere, og de bør vurderes på nytt av eier. Vurderingen krever at koblingen mellom det ugjorte og hindringen bedømmes — det er koderens arbeid, ikke målingens, og den er ikke gjort her.

---

## 4 R3 i ADDENDUM-01 er en øvre grense

Dette er en **presisering, ikke en retting**. R3 er beregnet og rapportert korrekt for det den måler: andelen verk med en registrert PDF-lenke. Den ble aldri presentert som nedlastbarhet, men den kan leses slik, og §2 viser hvor langt de to ligger fra hverandre.

| felt | verk med PDF-lenke i utsnittet | verk med lesbar tekst | lenketellingen overdriver med |
|---|---|---|---|
| tekstvitenskap | 20/30 = 67 % | 13/30 = 43 % | 1,54× |
| klinisk epidemiologi | 22/30 = 73 % | 14/30 = 47 % | 1,57× |
| arkeologi | 15/30 = 50 % | 10/30 = 33 % | 1,50× |
| energimodellering | 19/30 = 63 % | 5/30 = 17 % | **3,80×** |

Av de PDF-lenkene som faktisk ble forsøkt, ga 65 % / 47 % / 64 % / 26 % en lesbar fil.

**Setningen som skal følge R3 i all videre rapportering:**

> R3 teller registrerte PDF-lenker, ikke nedlastbare filer. Målt på 30 verk per felt gir den offentlige ruten lesbar tekst for 17–47 % av rammen, og lenketellingen overdriver hentbarheten med en faktor 1,5 til 3,8.

ADDENDUM-01 blir ikke endret. Tallene der står, med denne presiseringen ved siden av.

---

## 5 Kvotetaket

### 5.1 Polite pool gir ikke høyere tak

Målt 2026-09-12 med tre varianter av samme kall:

| variant | `x-ratelimit-limit` | `x-ratelimit-remaining` | `retry-after` |
|---|---|---|---|
| uten mailto | **1 000** | 0 | 39 178 s |
| `mailto=eirik@ecodeco.no` som query-parameter | **1 000** | 0 | 39 178 s |
| `mailto:` i User-Agent | **1 000** | 0 | 39 178 s |

**Taket er 1 000 kall i alle tre tilfeller.** Mailto endrer ingenting. Svarhodene viser en kostnadsmodell i stedet: `x-ratelimit-limit-usd: 0.1` og `x-ratelimit-cost-required-usd: 0.0001` per kall — 1 000 kall er $0,10 i gratiskreditt, ikke en høflighetsgrense. Den gamle polite-pool-modellen, der en kontaktadresse ga tilgang til en romsligere kø, er ikke i kraft på dette endepunktet. Ingen nøkkel er opprettet, og mailto er ikke en nøkkel.

Nullstillingen tok 39 178 sekunder, altså **10,9 timer**.

### 5.2 Hva frysingen krever

Rammelistene har 30 362–66 830 verk (ADDENDUM-02 §6). Med 200 verk per side:

| felt | verk | sider (kall) |
|---|---|---|
| tekstvitenskap | 66 830 | 335 |
| klinisk epidemiologi | 43 986 | 220 |
| arkeologi | 37 510 | 188 |
| energimodellering | 30 362 | 152 |
| **sum** | 178 688 | **895** |

895 kall mot et tak på 1 000, uten margin for feilede sider, uten plass til noe annet arbeid samme døgn — og denne slyngens diagnostikk brukte opp kvoten på under et døgn.

**Frysingen må derfor fordeles over døgn.** Ett felt per døgn er den enkleste formen: 152–335 kall, godt innenfor taket, med margin. Frysingen er et engangsarbeid når resultatet lagres med sha256, slik ADDENDUM-01 §1 krever, og skal derfor gjøres én gang, arkiveres og ikke gjentas.

Alternativet er å betale for kreditt. Det er eierens valg, og det endrer hva metoden krever av en leser som vil etterprøve den — jf. ADDENDUM-02 §8.1, der den offentlige ruten er valgt nettopp for at sveipet skal kunne kjøres uten nøkkel og uten budsjett.

---

## 6 Erklæring

* **Ingen trekking av utvalg er utført.** Ingen rammeliste er frosset, ingen work-ID er valgt til de 100.
* 120 verk er forsøkt nedlastet, ingen av dem lest. 23 verk er lest i H1/H4-søket (§3). Loggen `data/leste-kontrollkandidater.json` har 199 oppføringer og 180 unike DOI-er, og alle utelates fra trekkingen.
* Ingen blokkering er omgått. Ingen user-agent-spoofing, ingen alternative kilder, ingen nøkkel opprettet.
* **PREREG-v1.md, ADDENDUM-01.md og ADDENDUM-02.md er uendret**, sha256 `05988b23…ba23a`, `aa78d1be…c255f` og `7c0542c9…f713`.
* Ingen remote, ingen push.
* Åpne poster: H4-kontroll (§3.2, søket var kvotebundet); energikontrollens seksjon (§4 og ADDENDUM-02 §2.4); tekstvitenskapskontrollen, nå gjenåpnet av §1; eierens valg om stoppregelen i ADDENDUM-01 §6 (§2.3); frysingen fordelt over døgn (§5.2); og de fire postene som alt sto åpne i ADDENDUM-02 §9.
