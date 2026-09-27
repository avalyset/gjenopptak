# ADDENDUM-09 — Sekvensiell trekking i frørekkefølge

**Skrevet:** 2026-09-13
**Hører til:** PREREG-v1.md `05988b238d9f22f9e7506524a7f3f29201d0c64e0db788237188f1ef652ba23a`,
ADDENDUM-01.md `aa78d1be50ac17f8e26a92513aa115b3d504bdde3556e43b4f2317ea47cc255f`,
ADDENDUM-02.md `7c0542c92c54a586e3b387794272bed171ee285b75c8ebe4ee8fe1fa16f6f713`,
ADDENDUM-03.md `0b577ae6c3d0278e811e674c78e4e2948be46252e5aca9c94e94466c1f985c4e`,
ADDENDUM-04.md `7f7d067b80468a7016e398d1120930c98eb8a705b0e1c0102ad97e9db42f8a9c`,
ADDENDUM-05.md `b12c85b2a731517f9d0c5742194b2b8a900177cb82d662f8bf20e7d67fef5e9d`,
ADDENDUM-06.md `0f0e9a8126804f8a8fdf185864e80612c76816c2a536cf696df29e65d8c05687`,
ADDENDUM-07.md `06eb4fb365413d089601d592bf273b08fa96d25b94390d771ad38a45b9c2a3c3`,
ADDENDUM-08.md `6888efb33a6bba03545d6891f78936c6c15006d0a148a6da414f24c165ae3a26`
**Status:** operasjonalisering etter lås. Erstatter hentingsprøven på hele rammelisten (ADDENDUM-04 §1.3) med hentbarhetstest i trekkrekkefølge for arkeologi, klinisk epidemiologi og tekstvitenskap. Rammedefinisjonen i ADDENDUM-04 §1.1 står. Endrer ingen markør, ingen klasse, ingen terskel og ingen enhet. Skrevet før trekking: ingen trekkrekkefølge er beregnet for noen rammeliste, og ingen verk er testet i trekkrekkefølge. Ingen av de ni låste filene er endret.

---

## 1 Beslutningen

* **Trekkingen skjer sekvensielt nedover den frosne listen, i frørekkefølge.** Frøet er prereg-frøet `05988b23` = 93 883 171, med lokal `random.Random` og stokkingen i ADDENDUM-01 §6.1.
* **Hentbarheten testes i trekkrekkefølge.** Trekkingen stopper ved 25 hentbare verk per felt.
* **Dette erstatter hentingsprøven på hele listen** for de tre feltene som ikke har den. Energimodellering har den (ADDENDUM-08 §4) og bruker den (§6).
* **Substitusjon bortfaller per konstruksjon.** Et verk som ikke er hentbart, er ikke i rammen og blir aldri trukket. Det finnes ingen avstand mellom rammeprøve og innsamling som et frafall kan oppstå i.

---

## 2 Begrunnelse: metodisk identisk

**Rekkefølgen gir samme fordeling.** I en jevnt tilfeldig stokking av rålisten kommer de hentbare verkene i en jevnt tilfeldig innbyrdes rekkefølge. De 25 første hentbare er derfor et enkelt tilfeldig utvalg av 25 fra den hentbare rammen. Det er samme fordeling som å teste hele listen først og så trekke 25 av de hentbare.

**Likheten hviler på tre forutsetninger:**

1. porten er den samme (ADDENDUM-04 §1.1, samme kode som rammeprøven);
2. portens utfall for et verk avhenger ikke av posisjonen;
3. rekkefølgen er fastlagt før noe verk testes.

**Kostnaden:** ventet antall forsøk er 54–75 per felt (ADDENDUM-03 §2.3: 58, 54 og 75), mot 37 510, 43 986 og 66 830 forsøk for prøve på hele listen.

---

## 3 Hva som går tapt

**Rammestørrelsen blir et anslag.** For de tre feltene telles den hentbare rammen ikke, men anslås med intervall fra karakteriseringen (§7). ADDENDUM-04 §1.3 krevde prøven på hele listen med begrunnelsen «Det er arbeidet som gjør nevneren kjent». Den begrunnelsen faller for de tre feltene:

* M1 er en andel i utvalget, og utvalget trenger ikke N.
* Rammestørrelsen rapporteres som anslag med intervall.
* Energimodellering beholder den telte rammen på 9 713 verk.

**Vertssammensetningen karakteriseres på 200 forsøk per felt,** ikke på hele listen. Tabellene for energimodellering i ADDENDUM-08 §3 er tellinger.

---

## 4 Trekkrekkefølgen

For hvert felt:

1. **Utgangspunktet** er den frosne rålisten, leksikografisk sortert på work-ID, med sha256 (ADDENDUM-08 §5).
2. **Stokkingen:** en ny `random.Random(93883171)` per felt stokker listen med `shuffle` (ADDENDUM-01 §1 og §6.1). Posisjon 1 er første element etter stokkingen.
3. **Før noe verk testes, føres:**
   * listens sha256 og N;
   * Python-versjon og kodens commit;
   * sha256 av rekkefølgen (work-ID-ene skilt med linjeskift);
   * sha256 av leseloggen.

**Implementasjonen** er `src/gjenopptak/harvest/draw.py`, commit `396812a`. Testene fester stokkingsvektoren på en testliste. Python 3.12.0 og 3.14.7 gir samme rekkefølge.

**Feltrekkefølgen** er frysingsrekkefølgen: energimodellering, arkeologi, klinisk epidemiologi, tekstvitenskap. Den avgjør bare `dobbeltramme`.

---

## 5 Vilkårene i trekkrekkefølge

**Et verk trekkes når alle vilkårene holder.** Faller det på ett, hoppes det over, grunnen føres, og neste posisjon vurderes.

| nr | vilkår | kilde | avgjøres av |
|---|---|---|---|
| 1 | ikke positiv kontroll, ikke i leseloggen | ADDENDUM-02 §1 | work-ID, DOI og PMCID; tittel bare for loggrader uten ID |
| 2 | ikke trukket i et tidligere felt | ADDENDUM-02 §7 (`dobbeltramme`) | work-ID |
| 3 | OpenAlex-typen er ikke `erratum`, `paratext`, `retraction` eller `peer-review` | ADDENDUM-01 §6 (`ikke_artikkel`) | OpenAlex-metadata |
| 4 | minst én av feltets emne-ID-er blant verkets tre høyest rangerte topics | ADDENDUM-02 §7 (`utenfor_felt`) | OpenAlex-metadata |
| 5 | porten gir tekst på P1 eller P3 | ADDENDUM-04 §1.1 | samme kode som rammeprøven (`fetchtest.run_frame`) |
| 6 | teksten fra P3 består identitetsporten | ADDENDUM-07 §8 | `identity_verdict` mot OpenAlex-tittelen; P1 er matchet på DOI i Europe PMC |

**Kontrollene** er de fire i ADDENDUM-08 §1.7:

* H1: W3000588547;
* H7: 10.1038/s41467-019-11357-9;
* H8: 10.1016/s2468-2667(17)30217-7;
* energimodelleringens kontroll i PREREG §7: 10.1016/j.apenergy.2018.04.048. Den står ikke i leseloggen og er ført særskilt.

**Leseloggen** tas som et øyeblikksbilde når trekkingen starter, og sha256 føres.

* Kravet i ADDENDUM-02 §1 om at kontroller og leste verk fjernes fra rammelisten før trekking, gjennomføres ved at verket hoppes over i trekkrekkefølgen.
* Rekkefølgen er dermed bestemt av den frosne listen, ikke av en liste som endrer seg med leseloggen. Fordelingen er den samme.
* Antallet fjernede verk oppgis sammen med M1 (ADDENDUM-02 §1, punkt 2).

**Metadataene** hentes fra OpenAlex under trekkingen, 50 work-ID-er per kall, én kreditt per kall (ADDENDUM-08 §6). Et verk som OpenAlex ikke returnerer metadata for på trekketidspunktet, kan ikke prøves mot vilkår 3, 4 og 6. Det hoppes over med grunnen `mangler-metadata`.

**`utenfor_felt`** utløses bare om verkets topics er endret etter frysingen. Rammefilteret krever feltets ID blant verkets topics, og OpenAlex fører høyst tre topics per verk. Vilkåret håndheves likevel, slik ADDENDUM-02 §7 krever.

**`ikke_artikkel` fanges bare delvis av typen.** Anmeldelser og lignende som OpenAlex fører som vanlige artikler, blir stående i utvalget. De kodes, rapporteres som eget tall og erstattes ikke.

**Identitetsporten** er regelen i ADDENDUM-07 §2.3: DOI-en står i teksten, eller minst 60 % av tittelens ord gjør det. Tittelen er OpenAlex-tittelen på trekketidspunktet.

**Testene kan kjøres parallelt.** Beslutningene tas i posisjonsrekkefølge.

---

## 6 Energimodellering

* **Feltet har hentingsprøve på hele listen** (ADDENDUM-08 §4).
* **Trekkingen går nedover den samme typen rekkefølge** over den frosne rålisten.
* **Portens utfall** for hvert verk tas fra verdiktet i prøven.
* **Teksten** er den lagrede filen på Vault, med kjent sha256. Ingenting hentes på nytt.
* **Vilkår 1–4 og 6** gjelder på samme måte.

---

## 7 Karakterisering av de tre feltene

* **Utsnittet:** de første 200 posisjonene i trekkrekkefølgen testes med porten uansett vilkår 1–4. Det er et enkelt tilfeldig utvalg av rålisten.
* **Det som rapporteres:**
  * hentbar andel på porten, med Wilson-intervall (95 %), sammenlignbar med 32,0 % i energimodellering;
  * andelen P3-treff som består identitetsporten;
  * de ti største vertene, rå mot hentbar;
  * frafallskategoriene.
* **Anslått rammestørrelse** er andelen ganger N, med intervall.
* **Forholdet til trekkingen:** trekkingens forsøk er de første posisjonene i de samme 200. Er 25 ikke nådd innen 200, fortsetter trekkingen nedover rekkefølgen, mens karakteriseringen blir stående på 200.

---

## 8 Filer

* **`data/utvalg/utvalg-<felt>.jsonl`:** work-ID, DOI, år, trekkposisjon, portledd og sha256 av fulltekstfilen, sortert på trekkposisjon.
* **`data/utvalg/trekklogg-<felt>.jsonl`:** hver besøkte posisjon, med beslutning, grunn, portutfall, identitet, OpenAlex-type og de tre høyest rangerte topics.
* **`data/utvalg/trekkspesifikasjon-<felt>.jsonl`** (§4) og **`data/utvalg/karakterisering-<felt>.json`** (§7).
* **Fulltekst:**
  * alt hentes til Vault `trekking-<felt>/`, med hentemanifest;
  * de trukne kopieres til `utvalg/<felt>/` med `MANIFEST-UTVALG.md` og merket `UTVALG-IKKE-LEST`;
  * ingen fil leses;
  * filene i `data/utvalg/` kopieres til Vault `utvalg/`.
* **Et utvalg trekkes én gang og overskrives aldri.** Koden nekter.

---

## 9 Sekundærtopic-andelen, målt før trekking

ADDENDUM-02 §7 sa at andelen verk der ingen av feltets ID-er er `primary_topic`, «bør gjøres før trekking». Andelen er regnet fra de frosne listene, uten kall:

| felt | N | primærtopic i feltet | ikke i feltet | andel ikke |
|---|---|---|---|---|
| energimodellering | 30 362 | 13 856 | 16 506 | 54,4 % |
| arkeologi | 37 510 | 14 306 | 23 204 | 61,9 % |
| klinisk epidemiologi | 43 986 | 16 415 | 27 571 | 62,7 % |
| tekstvitenskap | — | — | — | måles når listen er frosset |

**I hver ramme har over halvparten av verkene feltet bare som sekundært eller tertiært topic.**

* ADDENDUM-02 §7 avgjorde at valget av `topics.id` står, fordi `primary_topic.id` ville utelatt den positive kontrollen.
* Tekstvitenskapskontrollen W3000588547 har også feltets T10165 som tredje topic, ikke som primærtopic.
* Andelen er ikke et trekkvilkår. Den rapporteres, og utvalgets egen andel kan leses av trekkloggen.

---

## 10 Hva endres, og hva endres ikke

**Endres:**

* **ADDENDUM-04 §1.3** (prøve på hele listen) erstattes for arkeologi, klinisk epidemiologi og tekstvitenskap av test i trekkrekkefølge og karakterisering på 200 forsøk.
* **ADDENDUM-01 §6.2–6** (utløsende årsaker, erstatning, substitusjonslogg, rapportering og stoppregel) og **ADDENDUM-04 §3** bortfaller for alle fire feltene. Ingenting erstattes. Stokkingen i §6.1 står som trekkrekkefølgen.
* **I stedet for antall substitusjoner** rapporteres antall hoppede posisjoner per grunn, fra trekkloggen.
* **`ikke_artikkel`, `utenfor_felt` og `dobbeltramme`** går fra substitusjonskategorier til vilkår i trekkrekkefølge.

**Endres ikke:**

* rammedefinisjonen i ADDENDUM-04 §1.1;
* frøet og stokkingen (ADDENDUM-01 §1 og §6.1);
* n = 25 per felt (PREREG §4);
* at kontrollene ligger utenfor nevneren (ADDENDUM-02 §1);
* klassene, markørene, tersklene og enheten.

---

## 11 Erklæring

* **Skrevet før trekking.** Ingen trekkrekkefølge er beregnet for noen rammeliste, og ingen verk er testet i trekkrekkefølge.
* **Ett OpenAlex-kall er brukt i arbeidet med dette addendumet:** ett metadatakall på tre verk som ikke kan trekkes, for å bekrefte syntaksen for metadatabolkene: kontrollene W3000588547 og W2804095963 og det leste armeringsverket W2114973577. Sekundærtopic-andelen i §9 er regnet uten kall.
* **Tekstvitenskap er ikke frosset.** Remaining var 361 kl. 06:43 UTC, under kvotevaktens 385. Trekking og karakterisering av feltet kommer etter frysingen.
* **Ingen artikler er lest.**
* **PREREG-v1.md og ADDENDUM-01/02/03/04/05/06/07/08.md er uendret**, sha256 `05988b23…ba23a`, `aa78d1be…c255f`, `7c0542c9…f713`, `0b577ae6…5c4e`, `7f7d067b…8a9c`, `b12c85b2…5e9d`, `0f0e9a81…5687`, `06eb4fb3…a3c3`, `6888efb3…3a26`.
* **Ingen remote, ingen push.**
* **Åpne poster:**
  * frysing, trekking og karakterisering av tekstvitenskap, og feltets sekundærtopic-andel;
  * restposten for `ikke_artikkel` (§5), som rapporteres ved koding;
  * postene som står fra ADDENDUM-08 §8.
