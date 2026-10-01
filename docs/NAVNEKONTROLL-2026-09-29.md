# Navnekontroll før v0.4.0 — 29.09.2026

**Policy:** «verk, ikke person» (registerhode-skjemaet, ADR-0012 datert tillegg 28.09.2026): evaluerende setninger
adresseres til verket, ikke personen; navn beholdes i sitering.

## Metode

**Enkel egennavn-heuristikk, ikke spaCy** — spaCy er ikke installert i miljøet, og å hente det er en nedlasting.
Personnavnlisten er bygd fra (a) forfatterne i OpenAlex-svaret for verkene i sakene, L5-verkene, PS-246 og
H1-kontrollen (ett kall 29.09.2026), (b) forfatterlinjene i sakfilene, og (c) en manuell gjennomgang av 489
egennavn-kandidater (store forbokstaver midt i setning) i de 22 primærfilene: saksfilene, triagen,
sakregisteret, Heron-notatene, manuskriptene og patchene. Hvert kandidatord er klassifisert som nålevende
person, historisk person (antikke forfattere og kopister, som er kilder og ikke forfattere av verk i studien)
eller ikke-person. Eieren, som er manuskriptets forfatter, er holdt utenfor. I tillegg regnes personord som
subjekt: «forfatteren», «forfatterne», «the author(s)» og pronomen.

**Klassifisering per treff:** *evaluerende* = personnavn eller personord før et evaluerende verb i samme ledd
(≤ 8 ord, ingen preposisjon rett foran; verbliste på norsk og engelsk: fant, mistet, feilet, oppgir feil,
kunne ikke, unnlot, glemte, overså, utelot, manglet … / failed, missed, omitted, could not, overlooked,
neglected, mistakenly …); *sitering* = navnet innen 25 tegn fra årstall, «m.fl.», «et al.», W-id eller DOI;
*nøytral* = resten. Evaluerende treff er gjennomgått manuelt før omskriving. **Grensen:** heuristikken fanger
bare verb i lista og bare subjekter den kjenner; en evaluerende setning med et verb utenfor lista eller med et
navn som ikke står i personlisten, fanges ikke. Skanneren og alle treff ligger på Vault, `navnekontroll/`
(`navnekontroll.py` sha256 `d03b06819652bb9b…`); den flyttes til `src/` når fase 3 er ferdig.

**Filstatus:** *låst* = `PREREG-v1.md`, alle `ADDENDUM-*.md`, `PS-246-KRITERIUM.md` og `docs/saker/*/KRITERIUM.md`
(kriteriefilene ble gjenopprettet til låst sha i `ced7f47`); *eierfil* = manuskriptutkastene v2–v2.5 og
INSTRUKSER-v1.3, som er eierens sha-verifiserte filer og ikke skrives om her; *rettbar* = resten.

## Utfall

| klasse | rettbar | låst | eierfil | sum |
|---|---|---|---|---|
| evaluerende | 0 | 4 | 0 | 4 |
| sitering | 79 | 5 | 103 | 187 |
| nøytral | 73 | 4 | 0 | 77 |

Talt 29.09.2026 over alle sporede `.md`-filer etter omskrivingen og parafrasen i Heron-notatet; denne rapporten er
holdt utenfor tellingen, fordi tabellene under gjengir treffene.

**Evaluerende i rettbare filer: 0** (seks før omskrivingen 29.09: fem koderbegrunnelser i
`SAKBEHANDLING-2026-09-27-kandidater.md` og ett avsnitt i `PS-246-RESULTAT.md`). **I låste filer: 4.**
**I historikken som skal i bundlen:** 11 evaluerende tillegg i
7 commits på `main` (`git log -p offentlig..main`, bare `+`-linjer i `.md`;
`offentlig` og `main` har ingen felles forfar, så det er hele main-historikken). `offentlig`-grenens to commits, som
alt er publisert, bærer 10 av de samme setningene. Historikken skrives ikke om; release notes fører revisjonen.

### Omskrevet 29.09.2026 (diff)

| fil | linje | endring (subjekt før → etter) |
|---|---|---|
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 53 (AL-0021) | personord i flertall → «Studien» |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 341 (AL-2541) | personord i flertall → «Simuleringen i avhandlingen» |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 367 (AL-2594) | personord i flertall → «Avhandlingen» |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 460 (AL-1440) | personord i flertall → «Studien» |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 557 (AL-2516) | personord i flertall → «Artikkelens stokastiske formulering» |
| `docs/PS-246-RESULTAT.md` | 82–84 | personord i entall (to steder) → «Avhandlingen» |

Den gamle ordlyden gjengis ikke her, fordi den er det policyen tar ut; den står i commitens diff og i historikken.

Hver omskrevet linje bærer merket «Omformulert til verket 29.09.2026, navnepolicyen i `0b4c979`». Registerets
`notes`-felt (i `data/`) er uendret; det røres ikke mens fase 3 går.

### Fotnote 83 i Heron-notatet (`docs/HERON-KOLLASJON-VURDERING-v2.md` § 11)

Fila er ikke låst. Fotnoten sto som **ordrett sitat** fra avhandlingen, med en navngitt tredjeperson og en datert
personlig meddelelse. **Eieren avgjorde 29.09.2026** at sitatet erstattes med parafrase — «avhandlingen (fotnote
83) tilskriver utsettelsen av kollasjonen råd fra veiledningen, ikke materialets tilstand» — uten navn, dato eller
ordlyd fra meddelelsen; henvisningen til avhandlingen og fotnotenummeret står. Gjort, med datert merke.
Navnekontrollen på fila etterpå: 7 treff, 6 sitering og 1 nøytral (et navn i en boktittel), **0 evaluerende**, og
verken tredjepersonens navn, datoen eller meddelelsens ordlyd forekommer i noen sporet fil.

**Historikken bærer det ordrette sitatet.** Heron v2 ble lagt til i `0eaff6b` (26.09.2026, 13:11Z), etter at v0.3.0
ble laget; sitatet står i hver versjon av fila fram til parafrasen. Det er alt publisert gjennom `offentlig`-grenen
(`5fcb353`, `967254a`), og git-bundlen i v0.4.0 — som eieren har valgt å ta med — bærer det. Historikken skrives
ikke om.

## Alle treff etter klassifisering

### Evaluerende (alle i låste filer)

Fil, linje, subjekt og verb; setningen gjengis ikke. Filene er låst og røres ikke.

| fil | linje | subjekt | verb |
|---|---|---|---|
| `ADDENDUM-02.md` | 39 | personord (flertall) | «kunne ikke» |
| `ADDENDUM-08.md` | 105 | personord (entall) | «fant» |
| `ADDENDUM-16.md` | 40 | personord (flertall) | «were unable» |
| `docs/saker/SAK-09b/KRITERIUM.md` | 19 | personord (entall) | «omgikk» |

### Sitering (187)

| fil | linje | navn | status | setning |
|---|---|---|---|---|
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 129 | Haouachi | rettbar | Haouachi 2016 har en Crossref-DOI (`10.70675/8513d3c9ze385z4b4bz910cz221c7718984d`, 302 til theses.fr) selv om |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 130 | Bynum | rettbar | Bynum m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 132 | Karatas | rettbar | Crossref gir Karatas 2018, Mecking, Hohle & Wolfram 2017 og Hansen m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 132 | Mecking | rettbar | Crossref gir Karatas 2018, Mecking, Hohle & Wolfram 2017 og Hansen m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 132 | Hohle | rettbar | Crossref gir Karatas 2018, Mecking, Hohle & Wolfram 2017 og Hansen m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 132 | Wolfram | rettbar | Crossref gir Karatas 2018, Mecking, Hohle & Wolfram 2017 og Hansen m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 132 | Hansen | rettbar | Crossref gir Karatas 2018, Mecking, Hohle & Wolfram 2017 og Hansen m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 132 | Pring | rettbar | Pring 2016 og |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 133 | Aragao | rettbar | Aragao 2018 finnes ikke i Crossref. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.1-2026-09-28.md` | 87 | Bynum | rettbar | Bynum 7 forfattere, 2021), handle 1807/92034 løser; |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.1-2026-09-28.md` | 87 | Haouachi | rettbar | Haouachi har Crossref-DOI 10.70675/8513d3c9ze385z4b4bz910cz221c7718984d (→ theses.fr/2016STRAC019) \| |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.1-2026-09-28.md` | 110 | Haouachi | rettbar | * Haouachi 2016 har en Crossref-DOI som kan brukes i referanselista: |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.2-2026-09-28.md` | 58 | Haouachi | rettbar | \| 519 \| Haouachi 2016 (W2474595476, thesis; |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.2-2026-09-28.md` | 58 | Riris | rettbar | Kontrollert 28.09: fem DOI-er gir 302 og stemmer med Crossref (Riris 2018, 1 forf.; |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.2-2026-09-28.md` | 58 | Bynum | rettbar | Bynum m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.2-2026-09-28.md` | 58 | Karatas | rettbar | Karatas 2018; |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.2-2026-09-28.md` | 58 | Mecking | rettbar | Mecking m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.2-2026-09-28.md` | 58 | Hansen | rettbar | Hansen m.fl. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.2-2026-09-28.md` | 58 | Haouachi | rettbar | Haouachi har Crossref-DOI 10.70675/8513d3c9ze385z4b4bz910cz221c7718984d (302 → theses.fr/2016STRAC019); |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.4-2026-09-28.md` | 24 | Haouachi | rettbar | Haouachi-DOI-en.) |
| `docs/HERON-KOLLASJON-VURDERING-v2.md` | 8 | Grillo | rettbar | Verket: W3000588547 = 10.5525/gla.thesis.76774, doktoravhandling 2019 (Grillo 2019), *Hero of |
| `docs/HERON-KOLLASJON-VURDERING-v2.md` | 111 | Schmidt | rettbar | ## 7 Schmidt 1899 kollasjonerte ingen av dem |
| `docs/HERON-KOLLASJON-VURDERING-v2.md` | 141 | Cataldi | rettbar | \| **Cataldi Palau 2000**, «Il copista Ioannes Mauromates», Atti del V Colloquio (Cremona 1998), Firenze 2000, s. |
| `docs/HERON-KOLLASJON-VURDERING-v2.md` | 142 | Giacomelli | rettbar | \| **Giacomelli 2019**, «I libri greci di Matteo Macigni», s. |
| `docs/HERON-KOLLASJON-VURDERING-v2.md` | 197 | Cataldi | rettbar | **De tre utestede plansjesporene:** RGK 1c, Cataldi Palau 2000, Giacomelli 2019. |
| `docs/HERON-KOLLASJON-VURDERING-v2.md` | 197 | Giacomelli | rettbar | **De tre utestede plansjesporene:** RGK 1c, Cataldi Palau 2000, Giacomelli 2019. |
| `docs/LAERDOM.md` | 350 | Saxton | rettbar | * **Ingen AI-akse og ingen tidsakse.** Saxton & Rawls er fra 2006, ti år før avhandlingen. |
| `docs/LAERDOM.md` | 350 | Rawls | rettbar | * **Ingen AI-akse og ingen tidsakse.** Saxton & Rawls er fra 2006, ti år før avhandlingen. |
| `docs/LOFTBARE-VURDERING-v1.md` | 12 | Saxton | rettbar | Saxton & Rawls (2006) er publisert \| |
| `docs/LOFTBARE-VURDERING-v1.md` | 12 | Rawls | rettbar | Saxton & Rawls (2006) er publisert \| |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 293 | Haouachi | rettbar | \| **SAK-14** \| Haouachi 2016 `W2474595476` \| H3 språk \| **ikke opphevet** \| **79 av 90 = 87,8 %** [79,4–93,0] mot terskel **90 %** \| |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 294 | Aragao | rettbar | \| **SAK-09b** \| Aragao 2018 `W7133020405` \| H5 verktøygrense \| **ikke opphevet av det navngitte middelet** \| `blockmodeling` 1.1.8 har **ingen mekanisme**; |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 295 | Aragao | rettbar | \| **SAK-09c** \| Aragao 2018 `W7133020405` \| H1/H7 → **H8 varig** \| **lukket på `[V]`** \| arkivposten har **én** innholdsfil; |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 296 | Riris | rettbar | \| **SAK-08** \| Riris 2018 `W2784603861` \| H5 → **H8 utløser** \| **lukket på `[V]`** \| **seks** ruter sjekket, ingen modellkode \| |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 297 | Bynum | rettbar | \| **SAK-11** \| Bynum m.fl. |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 374 | Stäuble | rettbar | Bredere Eythra-søk: **81 treff**, og de to som gjelder boplassen, er **anmeldelser** (`10.11588/ai.2017.1.42531`, `10.11588/ger.2019.78651`) av Stäuble & Veits  |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 374 | Veits | rettbar | Bredere Eythra-søk: **81 treff**, og de to som gjelder boplassen, er **anmeldelser** (`10.11588/ai.2017.1.42531`, `10.11588/ger.2019.78651`) av Stäuble & Veits  |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 376 | Pring | rettbar | \| PS-246-utvidelsen \| Pring 2016 `W2551114598` \| — \| — \| **nei** — avhandlingen **har** EC-instrumentering (TDR), men EC-en rapporteres aldri som data; |
| `docs/MANUSKRIPT-v0.1.md` | 46 | Sutoyo | rettbar | Sutoyo and Capiluppi (2024) review a decade of |
| `docs/MANUSKRIPT-v0.1.md` | 46 | Capiluppi | rettbar | Sutoyo and Capiluppi (2024) review a decade of |
| `docs/MANUSKRIPT-v0.1.md` | 47 | Melin | rettbar | detection approaches, and Melin et al. |
| `docs/MANUSKRIPT-v0.1.md` | 53 | Azhar | rettbar | LimTopic models the topics of stated limitations (Al Azhar et al. |
| `docs/MANUSKRIPT-v0.1.md` | 54 | Azher | rettbar | generates future-work sections by retrieval (Al Azher et al. |
| `docs/MANUSKRIPT-v0.1.md` | 213 | Saxton | rettbar | **Neither an AI axis nor a time axis.** Saxton and Rawls (2006) appeared ten years before the |
| `docs/MANUSKRIPT-v0.1.md` | 213 | Rawls | rettbar | **Neither an AI axis nor a time axis.** Saxton and Rawls (2006) appeared ten years before the |
| `docs/MANUSKRIPT-v2-UTKAST.md` | 294 | Pring | eierfil | \| PS-246 \| Pring 2016, W2551114598 \| H5 \| criterion met for 2 of 4 horizons (25 Sept.) \| soil-model inconsistency reproduced for the four horizons named \| |
| `docs/MANUSKRIPT-v2-UTKAST.md` | 295 | Haouachi | eierfil | \| SAK-14 \| Haouachi 2016, W2474595476 \| H3 language \| **not lifted** \| 79 of 90 = 87.8 % [79.4–93.0] vs 90 % \| |
| `docs/MANUSKRIPT-v2-UTKAST.md` | 296 | Aragao | eierfil | \| SAK-09b \| Aragao 2018, W7133020405 \| H5 tool limit \| **not lifted by the named means** \| `blockmodeling` 1.1.8 has no mechanism; |
| `docs/MANUSKRIPT-v2-UTKAST.md` | 297 | Aragao | eierfil | \| SAK-09c \| Aragao 2018, W7133020405 \| H1/H7 → **H8, permanent** \| closed at condition (i) \| one content file in the archive; |
| `docs/MANUSKRIPT-v2-UTKAST.md` | 298 | Riris | eierfil | \| SAK-08 \| Riris 2018, W2784603861 \| H5 → **H8, trigger** \| closed at condition (i) \| six routes checked, no model code deposited \| |
| `docs/MANUSKRIPT-v2-UTKAST.md` | 299 | Bynum | eierfil | \| SAK-11 \| Bynum et al. |
| `docs/MANUSKRIPT-v2-UTKAST.md` | 364 | Pring | eierfil | soil-water model of Pring 2016 — the answer from the citation graph is no in all four, at a cost of |
| `docs/MANUSKRIPT-v2-UTKAST.md` | 367 | Pring | eierfil | For Pring 2016 the parked term cannot be supplied from the thesis: electrical |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 301 | Pring | eierfil | \| PS-246 \| Pring 2016, W2551114598 \| H5 \| **not lifted** (25 Sept.) \| the model inconsistency (FC > θS) reproduced for exactly the four horizons the thesis name |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 302 | Haouachi | eierfil | \| SAK-14 \| Haouachi 2016, W2474595476 \| H3 language \| **not lifted** \| 79 of 90 = 87.8 % [79.4–93.0] vs 90 % \| |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 303 | Aragao | eierfil | \| SAK-09b \| Aragao 2018, W7133020405 \| H5 tool limit \| **not lifted by the named means** \| `blockmodeling` 1.1.8 has no mechanism to bind the two partitions; |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 304 | Aragao | eierfil | \| SAK-09c \| Aragao 2018, W7133020405 \| H1/H7 → **H8, permanent** \| closed at condition (i) \| one content file in the archive; |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 305 | Riris | eierfil | \| SAK-08 \| Riris 2018, W2784603861 \| H5 → **H8, trigger** \| closed at condition (i) \| six routes checked, no model code deposited \| |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 306 | Bynum | eierfil | \| SAK-11 \| Bynum et al. |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 370 | Karatas | eierfil | sanctuary at Knossos (Karatas 2018, W2974992769, 3 citing works), the joint evaluation of pottery, |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 371 | Mecking | eierfil | artefacts and houses at Eythra (Mecking et al. |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 372 | Hansen | eierfil | of lead-processing crucibles from the fifth-millennium Lower Danube (Hansen et al. |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 373 | Pring | eierfil | W2936215896, 12 citing works), and the salinity term in the soil-water model of Pring 2016 — the |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 376 | Pring | eierfil | For Pring 2016 the parked term cannot be supplied from the thesis: electrical |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 485 | Pring | eierfil | DOI where one exists: Pring 2016 (W2551114598, thesis, no DOI); |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 485 | Haouachi | eierfil | Haouachi 2016 (W2474595476, thesis; |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 486 | Aragao | eierfil | Aragao 2018 (W7133020405, thesis, handle 1807/92034); |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 486 | Riris | eierfil | Riris 2018 |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 487 | Bynum | eierfil | Bynum et al. |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 488 | Karatas | eierfil | Karatas 2018 (W2974992769, 10.4000/mythos.297); |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 488 | Mecking | eierfil | Mecking et al. |
| `docs/MANUSKRIPT-v2.1-UTKAST.md` | 489 | Hansen | eierfil | Hansen et al. |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 315 | Pring | eierfil | \| PS-246 \| Pring 2016, W2551114598 \| H5 \| **not lifted** (25 Sept.) \| the model inconsistency (FC > θS) reproduced for exactly the four horizons the thesis name |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 316 | Haouachi | eierfil | \| SAK-14 \| Haouachi 2016, W2474595476 \| H3 language \| **not lifted** \| 79 of 90 = 87.8 % [79.4–93.0] vs 90 % \| |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 317 | Aragao | eierfil | \| SAK-09b \| Aragao 2018, W7133020405 \| H5 tool limit \| **not lifted by the named means** \| `blockmodeling` 1.1.8 has no mechanism to bind the two partitions; |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 318 | Aragao | eierfil | \| SAK-09c \| Aragao 2018, W7133020405 \| H1/H7 → **H8, permanent** \| closed at condition (i) \| one content file in the archive; |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 319 | Riris | eierfil | \| SAK-08 \| Riris 2018, W2784603861 \| H5 → **H8, trigger** \| closed at condition (i) \| model code not found in six checked routes; |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 320 | Bynum | eierfil | \| SAK-11 \| Bynum et al. |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 395 | Karatas | eierfil | sanctuary at Knossos (Karatas 2018, W2974992769, 3 citing works), the joint evaluation of pottery, |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 396 | Mecking | eierfil | artefacts and houses at Eythra (Mecking et al. |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 397 | Hansen | eierfil | of lead-processing crucibles from the fifth-millennium Lower Danube (Hansen et al. |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 399 | Pring | eierfil | for the fourth, the salinity term in the soil-water model of Pring 2016, the |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 402 | Pring | eierfil | For Pring 2016 the parked term cannot be supplied from the thesis: electrical |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 519 | Pring | eierfil | DOI where one exists: Pring 2016 (W2551114598, thesis, no DOI); |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 519 | Haouachi | eierfil | Haouachi 2016 (W2474595476, thesis; |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 520 | Aragao | eierfil | Aragao 2018 (W7133020405, thesis, handle 1807/92034); |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 520 | Riris | eierfil | Riris 2018 |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 521 | Bynum | eierfil | Bynum et al. |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 522 | Karatas | eierfil | Karatas 2018 (W2974992769, 10.4000/mythos.297); |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 522 | Mecking | eierfil | Mecking et al. |
| `docs/MANUSKRIPT-v2.2-UTKAST.md` | 523 | Hansen | eierfil | Hansen et al. |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 320 | Pring | eierfil | \| PS-246 \| Pring 2016, W2551114598 \| H5 \| **not lifted** (25 Sept.) \| the model inconsistency (FC > θS) reproduced for exactly the four horizons the thesis name |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 321 | Haouachi | eierfil | \| SAK-14 \| Haouachi 2016, W2474595476 \| H3 language \| **not lifted** \| 79 of 90 = 87.8 % [79.4–93.0] vs 90 % \| |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 322 | Aragao | eierfil | \| SAK-09b \| Aragao 2018, W7133020405 \| H5 tool limit \| **not lifted by the named means** \| `blockmodeling` 1.1.8 has no mechanism to bind the two partitions; |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 323 | Aragao | eierfil | \| SAK-09c \| Aragao 2018, W7133020405 \| H1/H7 → **H8, permanent** \| closed at condition (i) \| one content file in the archive; |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 324 | Riris | eierfil | \| SAK-08 \| Riris 2018, W2784603861 \| H5 → **H8, trigger** \| closed at condition (i) \| model code not found in six checked routes; |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 325 | Bynum | eierfil | \| SAK-11 \| Bynum et al. |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 405 | Karatas | eierfil | sanctuary at Knossos (Karatas 2018, W2974992769, 3 citing works), the joint evaluation of pottery, |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 406 | Mecking | eierfil | artefacts and houses at Eythra (Mecking et al. |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 407 | Hansen | eierfil | of lead-processing crucibles from the fifth-millennium Lower Danube (Hansen et al. |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 409 | Pring | eierfil | for the fourth, the salinity term in the soil-water model of Pring 2016, the |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 412 | Pring | eierfil | For Pring 2016 the parked term cannot be supplied from the thesis: electrical |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 535 | Pring | eierfil | DOI where one exists: Pring 2016 (W2551114598, thesis, no DOI); |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 535 | Haouachi | eierfil | Haouachi 2016 (W2474595476, thesis, |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 536 | Aragao | eierfil | Aragao 2018 (W7133020405, thesis, handle |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 537 | Riris | eierfil | Riris 2018 |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 538 | Bynum | eierfil | Bynum et al. |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 539 | Karatas | eierfil | Karatas 2018 (W2974992769, 10.4000/mythos.297); |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 539 | Mecking | eierfil | Mecking et al. |
| `docs/MANUSKRIPT-v2.3-UTKAST.md` | 540 | Hansen | eierfil | Hansen et al. |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 325 | Pring | eierfil | \| PS-246 \| Pring 2016, W2551114598 \| H5 \| **not lifted** (25 Sept.) \| the model inconsistency (FC > θS) reproduced for exactly the four horizons the thesis name |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 326 | Haouachi | eierfil | \| SAK-14 \| Haouachi 2016, W2474595476 \| H3 language \| **not lifted** \| 79 of 90 = 87.8 % [79.4–93.0] vs 90 % \| |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 327 | Aragao | eierfil | \| SAK-09b \| Aragao 2018, W7133020405 \| H5 tool limit \| **not lifted by the named means** \| `blockmodeling` 1.1.8 has no mechanism to bind the two partitions; |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 328 | Aragao | eierfil | \| SAK-09c \| Aragao 2018, W7133020405 \| H1/H7 → **H8, permanent** \| closed at condition (i) \| one content file in the archive; |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 329 | Riris | eierfil | \| SAK-08 \| Riris 2018, W2784603861 \| H5 → **H8, trigger** \| closed at condition (i) \| model code not found in six checked routes; |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 330 | Bynum | eierfil | \| SAK-11 \| Bynum et al. |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 411 | Karatas | eierfil | sanctuary at Knossos (Karatas 2018, W2974992769, 3 citing works), the joint evaluation of pottery, |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 412 | Mecking | eierfil | artefacts and houses at Eythra (Mecking et al. |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 413 | Hansen | eierfil | of lead-processing crucibles from the fifth-millennium Lower Danube (Hansen et al. |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 415 | Pring | eierfil | for the fourth, the salinity term in the soil-water model of Pring 2016, the |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 418 | Pring | eierfil | For Pring 2016 the parked term cannot be supplied from the thesis: electrical |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 543 | Pring | eierfil | DOI where one exists: Pring 2016 (W2551114598, thesis, no DOI); |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 543 | Haouachi | eierfil | Haouachi 2016 (W2474595476, thesis, |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 544 | Aragao | eierfil | Aragao 2018 (W7133020405, thesis, handle |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 545 | Riris | eierfil | Riris 2018 |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 546 | Bynum | eierfil | Bynum et al. |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 547 | Karatas | eierfil | Karatas 2018 (W2974992769, 10.4000/mythos.297); |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 547 | Mecking | eierfil | Mecking et al. |
| `docs/MANUSKRIPT-v2.4-UTKAST.md` | 548 | Hansen | eierfil | Hansen et al. |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 326 | Pring | eierfil | \| PS-246 \| Pring 2016, W2551114598 \| H5 \| **not lifted** (25 Sept.) \| the model inconsistency (FC > θS) reproduced for exactly the four horizons the thesis name |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 327 | Haouachi | eierfil | \| SAK-14 \| Haouachi 2016, W2474595476 \| H3 language \| **not lifted** \| 79 of 90 = 87.8 % [79.4–93.0] vs 90 % \| |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 328 | Aragao | eierfil | \| SAK-09b \| Aragao 2018, W7133020405 \| H5 tool limit \| **not lifted by the named means** \| `blockmodeling` 1.1.8 has no mechanism to bind the two partitions; |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 329 | Aragao | eierfil | \| SAK-09c \| Aragao 2018, W7133020405 \| H1/H7 → **H8, permanent** \| closed at condition (i) \| one content file in the archive; |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 330 | Riris | eierfil | \| SAK-08 \| Riris 2018, W2784603861 \| H5 → **H8, trigger** \| closed at condition (i) \| model code not found in six checked routes; |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 331 | Bynum | eierfil | \| SAK-11 \| Bynum et al. |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 412 | Karatas | eierfil | sanctuary at Knossos (Karatas 2018, W2974992769, 3 citing works), the joint evaluation of pottery, |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 413 | Mecking | eierfil | artefacts and houses at Eythra (Mecking et al. |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 414 | Hansen | eierfil | of lead-processing crucibles from the fifth-millennium Lower Danube (Hansen et al. |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 416 | Pring | eierfil | for the fourth, the salinity term in the soil-water model of Pring 2016, the |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 419 | Pring | eierfil | For Pring 2016 the parked term cannot be supplied from the thesis: electrical |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 545 | Pring | eierfil | DOI where one exists: Pring 2016 (W2551114598, thesis, no DOI); |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 545 | Haouachi | eierfil | Haouachi 2016 (W2474595476, thesis, |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 546 | Aragao | eierfil | Aragao 2018 (W7133020405, thesis, handle |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 547 | Riris | eierfil | Riris 2018 |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 548 | Bynum | eierfil | Bynum et al. |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 549 | Karatas | eierfil | Karatas 2018 (W2974992769, 10.4000/mythos.297); |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 549 | Mecking | eierfil | Mecking et al. |
| `docs/MANUSKRIPT-v2.5-UTKAST.md` | 550 | Hansen | eierfil | Hansen et al. |
| `docs/PS-246-KRITERIUM.md` | 32 | Saxton | låst | * Likninger hentes fra **Saxton & Rawls (2006)**, originalartikkelen, med likningsnummer per |
| `docs/PS-246-KRITERIUM.md` | 32 | Rawls | låst | * Likninger hentes fra **Saxton & Rawls (2006)**, originalartikkelen, med likningsnummer per |
| `docs/PS-246-KRITERIUM.md` | 43 | Rawls | låst | **Ikke at dette er en AI-løftbar hindring.** Saxton & Rawls ble publisert i **2006**, ti år før |
| `docs/PS-246-RESULTAT.md` | 86 | Rawls | rettbar | * **Saxton–Rawls ble publisert i 2006, ti år før avhandlingen.** Likningene var tilgjengelige hele |
| `docs/PS-246-RESULTAT.md` | 99 | Saxton | rettbar | Hent Saxton & Rawls (2006) og bruk likning [1], [2], [3], [5], [6], [8] og [9]. |
| `docs/PS-246-RESULTAT.md` | 99 | Rawls | rettbar | Hent Saxton & Rawls (2006) og bruk likning [1], [2], [3], [5], [6], [8] og [9]. |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 131 | Saxton | rettbar | > Saxton and Rawls (2006) provide a number of additional equations for hydraulic conductivity, and adjustments for density, gravel and salinity, which are used  |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 131 | Rawls | rettbar | > Saxton and Rawls (2006) provide a number of additional equations for hydraulic conductivity, and adjustments for density, gravel and salinity, which are used  |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 131 | Saxton | rettbar | The saturated, Ks, and unsaturated, Kθ, hydraulic conductivity can be estimated using the following equations (Saxton and Rawls, 2006). |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 131 | Rawls | rettbar | The saturated, Ks, and unsaturated, Kθ, hydraulic conductivity can be estimated using the following equations (Saxton and Rawls, 2006). |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 313 | Saxton | rettbar | Saxton and Rawls (2006) also give adjustments for gravel content, R, although the SWCC is not dependent on this parameter. |
| `docs/SAKBEHANDLING-2026-09-27-kandidater.md` | 313 | Rawls | rettbar | Saxton and Rawls (2006) also give adjustments for gravel content, R, although the SWCC is not dependent on this parameter. |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 14 | Pring | rettbar | enheten er verk × hindring.)* 23 passasjer er ett ugjort (Pring 2016, SPAW/partikkeltetthet); |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 21 | Haouachi | rettbar | ### SAK-14 · Haouachi 2016 (W2474595476) · H3 språk · **AI-aksen** |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 34 | Aragao | rettbar | ### SAK-09c · Aragao 2018 (W7133020405) · H1/H7-uavklart · **AI-aksen** |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 44 | Riris | rettbar | ### SAK-08 · Riris 2018 (W2784603861) · H5 regnekraft |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 52 | Aragao | rettbar | ### SAK-09b · Aragao 2018 (W7133020405) · H5 verktøygrense |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 80 | Pring | rettbar | - **PS-246-utvidelse** Pring 2016, AL-0110/AL-2127: saltholdighet satt til null fordi |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 81 | Saxton | rettbar | Saxton–Rawls 2006 har termen; |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 81 | Rawls | rettbar | Saxton–Rawls 2006 har termen; |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 142 | Veits | rettbar | gjelder boplassen, er **anmeldelser** av Stäuble & Veits bind — `10.11588/ai.2017.1.42531` (2017) og |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 164 | Pring | rettbar | ### PS-246-utvidelsen · Pring 2016 (`W2551114598`), AL-0110/AL-2127 — **nei, og grunnen er skarpere enn ventet** |
| `docs/patch/MASTER-2026-09-27-SAK-14.md` | 17 | Haouachi | rettbar | Ekte treff, klasse **H3 språkbarriere**, verk `W2474595476` (Haouachi 2016). |
| `docs/patch/MASTER-2026-09-28-fase1-2.md` | 62 | Aragao | rettbar | Ekte treff, klasse **H5 verktøygrense**, verk `W7133020405` (Aragao 2018). |
| `docs/patch/MASTER-2026-09-28-fase1-2.md` | 94 | Riris | rettbar | `W2784603861` (Riris 2018), H5 regnekraft. |
| `docs/patch/MASTER-2026-09-28-fase1-2.md` | 104 | Bynum | rettbar | `W4206850274` (Bynum m.fl. |
| `docs/patch/MASTER-2026-09-28-fase1-2.md` | 129 | Pring | rettbar | \| PS-246-utvidelsen \| Pring 2016 `W2551114598` \| — \| **nei** — EC finnes som TDR-signal, men rapporteres aldri; |
| `docs/saker/REGISTER-SAKER.md` | 10 | Haouachi | rettbar | \| **SAK-14** \| Haouachi 2016 `W2474595476` \| H3 språk \| AL-0738, AL-2370 \| **ikke opphevet** — 87,8 % mot terskel 90 % \| [`SAK-14/KRITERIUM.md`](SAK-14/KRITERIU |
| `docs/saker/REGISTER-SAKER.md` | 11 | Aragao | rettbar | \| **SAK-09c** \| Aragao 2018 `W7133020405` \| H1/H7-uavklart → **H8** \| AL-2606 \| **lukket på `[V]`** — kildeteksten finnes ikke utenfor samtykket \| *ingen — sake |
| `docs/saker/REGISTER-SAKER.md` | 12 | Riris | rettbar | \| **SAK-08** \| Riris 2018 `W2784603861` \| H5 → **H8** (utløser) \| AL-1280 \| **lukket på `[V]`** — modellkoden ikke funnet i seks ruter; |
| `docs/saker/REGISTER-SAKER.md` | 13 | Aragao | rettbar | \| **SAK-09b** \| Aragao 2018 `W7133020405` \| H5 verktøygrense \| AL-0852 \| **ikke opphevet av det navngitte middelet** — `blockmodeling` 1.1.8 mangler mekanismen  |
| `docs/saker/REGISTER-SAKER.md` | 14 | Bynum | rettbar | \| **SAK-11** \| Bynum m.fl. |
| `docs/saker/REGISTER-SAKER.md` | 16 | Pring | rettbar | \| SAK-01 \| Pring 2016 `W2551114598` \| H5 verktøygrense \| 23 passasjer \| **gjennomført 25.09 som PS-246**; |
| `docs/saker/SAK-08/LUKKET.md` | 14 | Riris | rettbar | **Verket:** `W2784603861`, artikkel 2018 (Riris 2018), «Assessing the impact and legacy of swidden |
| `docs/saker/SAK-09b/KRITERIUM.md` | 3 | Aragao | låst | **Sak:** Aragao 2018, `W7133020405`, passasje **AL-0852**, klasse **H5 verktøygrense**. |
| `docs/saker/SAK-09b/RESULTAT.md` | 3 | Aragao | rettbar | **Gjennomført 27.09.2026.** Sak: Aragao 2018, `W7133020405`, passasje **AL-0852**, klasse |
| `docs/saker/SAK-09c/LUKKET.md` | 8 | Aragao | rettbar | **Verket:** `W7133020405`, doktoravhandling 2018-11 (Aragao 2018), *Using Network Theory to Manage |
| `docs/saker/SAK-14/KRITERIUM.md` | 3 | Haouachi | låst | **Sak:** Haouachi 2016, `W2474595476`, klasse **H3 språkbarriere**, AI-aksen. |
| `docs/saker/SAK-14/RESULTAT.md` | 3 | Haouachi | rettbar | **Gjennomført 27.09.2026.** Sak: Haouachi 2016, `W2474595476`, klasse **H3 språkbarriere**, |

### Nøytral (77)

| fil | linje | navn | status | setning |
|---|---|---|---|---|
| `README.md` | 337 | Saxton | rettbar | the reproduction of Saxton & Rawls Table 3 and the mirror check |
| `README.md` | 337 | Rawls | rettbar | the reproduction of Saxton & Rawls Table 3 and the mirror check |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 123 | Pring | rettbar | * **«581 864 tegn»** (Pring-teksten) er bytes; |
| `docs/FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md` | 131 | Riris | rettbar | Riris-tittelen i SAK-08 avviker fra Crossref. |
| `docs/FAKTASJEKK-MANUSKRIPT-v2.1-2026-09-28.md` | 98 | Pring | rettbar | **Pring:** 581 864 er bytes; |
| `docs/HERON-KOLLASJON-VURDERING-v2.md` | 142 | Macigni | rettbar | \| **Giacomelli 2019**, «I libri greci di Matteo Macigni», s. |
| `docs/LAERDOM.md` | 340 | Saxton | rettbar | * **Målt:** PS-246, et ekte treff i klasse H5: avhandlingen W2551114598 lot være å bruke målt matrisk tetthet i Saxton–Rawls, fordi SPAW låser partikkeltetthete |
| `docs/LAERDOM.md` | 340 | Rawls | rettbar | * **Målt:** PS-246, et ekte treff i klasse H5: avhandlingen W2551114598 lot være å bruke målt matrisk tetthet i Saxton–Rawls, fordi SPAW låser partikkeltetthete |
| `docs/LOFTBARE-VURDERING-v1.md` | 11 | Saxton | rettbar | II/4–5, helst strøklys eller 3D-skann av gjenstanden \| Daglige TDR-VWC-serier per seksjon og horisont \| Jordinndata per horisont (leire, sand, grus, org., matri |
| `docs/LOFTBARE-VURDERING-v1.md` | 11 | Rawls | rettbar | II/4–5, helst strøklys eller 3D-skann av gjenstanden \| Daglige TDR-VWC-serier per seksjon og horisont \| Jordinndata per horisont (leire, sand, grus, org., matri |
| `docs/LOFTBARE-VURDERING-v1.md` | 13 | Saxton | rettbar | \| **hva forsøket ville være** \| Ny måling på objektet etter rensing, eller reanalyse av spektre \| Bildeforbedring (CLAHE, flerskala) + paleografisk sammenliknin |
| `docs/LOFTBARE-VURDERING-v1.md` | 13 | Rawls | rettbar | \| **hva forsøket ville være** \| Ny måling på objektet etter rensing, eller reanalyse av spektre \| Bildeforbedring (CLAHE, flerskala) + paleografisk sammenliknin |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 376 | Saxton | rettbar | Bulk-TDR-EC er dessuten den gale størrelsen: Saxton–Rawls krever `ECe` i dS/m fra mettet pastautdrag \| |
| `docs/MANUSKRIPT-FAKTA-2026-09-28.md` | 376 | Rawls | rettbar | Bulk-TDR-EC er dessuten den gale størrelsen: Saxton–Rawls krever `ECe` i dS/m fra mettet pastautdrag \| |
| `docs/MANUSKRIPT-v0.1.md` | 197 | Saxton | rettbar | density** into the Saxton–Rawls soil-water equations, because the SPAW tool fixes particle density at |
| `docs/MANUSKRIPT-v0.1.md` | 197 | Rawls | rettbar | density** into the Saxton–Rawls soil-water equations, because the SPAW tool fixes particle density at |
| `docs/MANUSKRIPT-v0.1.md` | 330 | Ferrara | rettbar | \| 4 \| Ke, Q., Ferrara, E., Radicchi, F. |
| `docs/MANUSKRIPT-v0.1.md` | 330 | Radicchi | rettbar | \| 4 \| Ke, Q., Ferrara, E., Radicchi, F. |
| `docs/MANUSKRIPT-v0.1.md` | 330 | Flammini | rettbar | & Flammini, A. |
| `docs/MANUSKRIPT-v0.1.md` | 331 | Sutoyo | rettbar | \| 5 \| Sutoyo, E. |
| `docs/MANUSKRIPT-v0.1.md` | 331 | Capiluppi | rettbar | & Capiluppi, A. |
| `docs/MANUSKRIPT-v0.1.md` | 332 | Melin | rettbar | \| 6 \| Melin, E.L., Eisty, N.U., Watson, G.R. |
| `docs/MANUSKRIPT-v0.1.md` | 332 | Eisty | rettbar | \| 6 \| Melin, E.L., Eisty, N.U., Watson, G.R. |
| `docs/MANUSKRIPT-v0.1.md` | 332 | Watson | rettbar | \| 6 \| Melin, E.L., Eisty, N.U., Watson, G.R. |
| `docs/MANUSKRIPT-v0.1.md` | 333 | Azhar | rettbar | \| 7 \| Al Azhar, I., Reddy, V.D., Alhoori, H. |
| `docs/MANUSKRIPT-v0.1.md` | 333 | Reddy | rettbar | \| 7 \| Al Azhar, I., Reddy, V.D., Alhoori, H. |
| `docs/MANUSKRIPT-v0.1.md` | 333 | Alhoori | rettbar | \| 7 \| Al Azhar, I., Reddy, V.D., Alhoori, H. |
| `docs/MANUSKRIPT-v0.1.md` | 334 | Azher | rettbar | \| 8 \| Al Azher, I., Mokarrama, M.J., Guo, Z. |
| `docs/MANUSKRIPT-v0.1.md` | 334 | Mokarrama | rettbar | \| 8 \| Al Azher, I., Mokarrama, M.J., Guo, Z. |
| `docs/MANUSKRIPT-v0.1.md` | 334 | Guo | rettbar | \| 8 \| Al Azher, I., Mokarrama, M.J., Guo, Z. |
| `docs/MANUSKRIPT-v0.1.md` | 335 | Zhao | rettbar | \| 9 \| Xu, Z., Zhao, Y., Patwardhan, M., Vig, L. |
| `docs/MANUSKRIPT-v0.1.md` | 335 | Patwardhan | rettbar | \| 9 \| Xu, Z., Zhao, Y., Patwardhan, M., Vig, L. |
| `docs/MANUSKRIPT-v0.1.md` | 335 | Vig | rettbar | \| 9 \| Xu, Z., Zhao, Y., Patwardhan, M., Vig, L. |
| `docs/MANUSKRIPT-v0.1.md` | 335 | Cohan | rettbar | & Cohan, A. |
| `docs/MANUSKRIPT-v0.1.md` | 336 | Amershi | rettbar | \| 10 \| Smith, J.J., Amershi, S., Barocas, S., Wallach, H. |
| `docs/MANUSKRIPT-v0.1.md` | 336 | Barocas | rettbar | \| 10 \| Smith, J.J., Amershi, S., Barocas, S., Wallach, H. |
| `docs/MANUSKRIPT-v0.1.md` | 336 | Wallach | rettbar | \| 10 \| Smith, J.J., Amershi, S., Barocas, S., Wallach, H. |
| `docs/MANUSKRIPT-v0.1.md` | 336 | Wortman | rettbar | & Wortman Vaughan, J. |
| `docs/MANUSKRIPT-v0.1.md` | 336 | Vaughan | rettbar | & Wortman Vaughan, J. |
| `docs/MANUSKRIPT-v0.1.md` | 342 | Yin | rettbar | \| 16 \| Tian, Q., Yin, H., Xia, Y., Kong, Y. |
| `docs/MANUSKRIPT-v0.1.md` | 342 | Xia | rettbar | \| 16 \| Tian, Q., Yin, H., Xia, Y., Kong, Y. |
| `docs/MANUSKRIPT-v0.1.md` | 342 | Kong | rettbar | \| 16 \| Tian, Q., Yin, H., Xia, Y., Kong, Y. |
| `docs/MANUSKRIPT-v0.1.md` | 342 | Liu | rettbar | & Liu, Z. |
| `docs/MANUSKRIPT-v0.1.md` | 343 | Saxton | rettbar | \| 17 \| Saxton, K.E. |
| `docs/MANUSKRIPT-v0.1.md` | 343 | Rawls | rettbar | & Rawls, W.J. |
| `docs/PS-246-KRITERIUM.md` | 10 | Saxton | låst | **Det ugjorte:** å bruke **målt matrisk tetthet** som inndata i Saxton–Rawls i stedet for SPAWs |
| `docs/PS-246-KRITERIUM.md` | 10 | Rawls | låst | **Det ugjorte:** å bruke **målt matrisk tetthet** som inndata i Saxton–Rawls i stedet for SPAWs |
| `docs/PS-246-KRITERIUM.md` | 43 | Saxton | låst | **Ikke at dette er en AI-løftbar hindring.** Saxton & Rawls ble publisert i **2006**, ti år før |
| `docs/PS-246-RESULTAT.md` | 6 | Saxton | rettbar | **Det ugjorte:** å bruke målt matrisk tetthet — og dermed målt partikkeltetthet — i Saxton–Rawls |
| `docs/PS-246-RESULTAT.md` | 6 | Rawls | rettbar | **Det ugjorte:** å bruke målt matrisk tetthet — og dermed målt partikkeltetthet — i Saxton–Rawls |
| `docs/PS-246-RESULTAT.md` | 12 | Saxton | rettbar | Likningene er hentet fra originalartikkelen: Saxton, K.E. |
| `docs/PS-246-RESULTAT.md` | 12 | Rawls | rettbar | og Rawls, W.J. |
| `docs/PS-246-RESULTAT.md` | 86 | Saxton | rettbar | * **Saxton–Rawls ble publisert i 2006, ti år før avhandlingen.** Likningene var tilgjengelige hele |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 142 | Stäuble | rettbar | gjelder boplassen, er **anmeldelser** av Stäuble & Veits bind — `10.11588/ai.2017.1.42531` (2017) og |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 180 | Saxton | rettbar | **Og det er dessuten den gale EC-en.** Saxton & Rawls' saltholdighetsledd tar `ECe` i dS/m fra en |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 180 | Rawls | rettbar | **Og det er dessuten den gale EC-en.** Saxton & Rawls' saltholdighetsledd tar `ECe` i dS/m fra en |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 183 | Saxton | rettbar | termen mangler i Saxton–Rawls, men fordi avhandlingen ikke har inndataen termen krever. |
| `docs/SAKBEHANDLING-2026-09-27-triage.md` | 183 | Rawls | rettbar | termen mangler i Saxton–Rawls, men fordi avhandlingen ikke har inndataen termen krever. |
| `docs/decisions/0013-opphevelse-definisjon.md` | 64 | Saxton | rettbar | \| **PS-246** `W2551114598` \| **ja** \| **ja** — avhandlingens FC > θS i nøyaktig de fire navngitte horisontene reprodusert (implementasjonen først verifisert mot |
| `docs/decisions/0013-opphevelse-definisjon.md` | 64 | Rawls | rettbar | \| **PS-246** `W2551114598` \| **ja** \| **ja** — avhandlingens FC > θS i nøyaktig de fire navngitte horisontene reprodusert (implementasjonen først verifisert mot |
| `docs/decisions/0013-opphevelse-definisjon.md` | 97 | Saxton | rettbar | Saxton & Rawls, ikke reproduksjon av kildens (avhandlingens) egne tall.* |
| `docs/decisions/0013-opphevelse-definisjon.md` | 97 | Rawls | rettbar | Saxton & Rawls, ikke reproduksjon av kildens (avhandlingens) egne tall.* |
| `docs/patch/MASTER-2026-09-28-fase1-2.md` | 129 | Saxton | rettbar | eneste verdi er `0.0μS/cm`, som ble *satt*, og bulk-TDR-EC er den gale størrelsen for Saxton–Rawls \| |
| `docs/patch/MASTER-2026-09-28-fase1-2.md` | 129 | Rawls | rettbar | eneste verdi er `0.0μS/cm`, som ble *satt*, og bulk-TDR-EC er den gale størrelsen for Saxton–Rawls \| |
| `docs/saker/REGISTER-SAKER.md` | 128 | Saxton | rettbar | Saxton–Rawls krever `ECe` i dS/m fra mettet pastautdrag. |
| `docs/saker/REGISTER-SAKER.md` | 128 | Rawls | rettbar | Saxton–Rawls krever `ECe` i dS/m fra mettet pastautdrag. |
| `docs/saker/SAK-08/LUKKET.md` | 50 | Riris | rettbar | \| **CoMSES Computational Model Library, i tillegg** \| **ingen modell** av Riris. |
| `docs/saker/SAK-11/LUKKET.md` | 8 | Bynum | rettbar | **Verket:** Michael Bynum, Andrea Staid, Bryan Arguello, Anya Castillo, Bernard Knueven, Carl D. |
| `docs/saker/SAK-11/LUKKET.md` | 8 | Staid | rettbar | **Verket:** Michael Bynum, Andrea Staid, Bryan Arguello, Anya Castillo, Bernard Knueven, Carl D. |
| `docs/saker/SAK-11/LUKKET.md` | 8 | Arguello | rettbar | **Verket:** Michael Bynum, Andrea Staid, Bryan Arguello, Anya Castillo, Bernard Knueven, Carl D. |
| `docs/saker/SAK-11/LUKKET.md` | 8 | Castillo | rettbar | **Verket:** Michael Bynum, Andrea Staid, Bryan Arguello, Anya Castillo, Bernard Knueven, Carl D. |
| `docs/saker/SAK-11/LUKKET.md` | 8 | Knueven | rettbar | **Verket:** Michael Bynum, Andrea Staid, Bryan Arguello, Anya Castillo, Bernard Knueven, Carl D. |
| `docs/saker/SAK-11/LUKKET.md` | 9 | Laird | rettbar | Laird, «Proactive Operations and Investment Planning via Stochastic Optimization to Enhance Power |
| `docs/saker/SAK-11/LUKKET.md` | 14 | Watson | rettbar | Watson, etter Laird; |
| `docs/saker/SAK-11/LUKKET.md` | 14 | Laird | rettbar | Watson, etter Laird; |
| `docs/saker/SAK-14/KRITERIUM.md` | 45 | Jacoby | låst | Karl Jacoby, |
| `docs/saker/SAK-14/RESULTAT.md` | 21 | Jacoby | rettbar | \| avhandlingens franske gjengivelse \| gresk hos Perseus (Jacoby) \| |

### Historikk: evaluerende tillegg per commit (skrives ikke om)

| commit | antall | fil |
|---|---|---|
| `8bd9be3` | 5 | `docs/SAKBEHANDLING-2026-09-27-kandidater.md` |
| `ced7f47` | 1 | `docs/saker/SAK-09b/KRITERIUM.md` |
| `feb0c31` | 1 | `docs/saker/SAK-09b/KRITERIUM.md` |
| `e92620b` | 1 | `ADDENDUM-16.md` |
| `d862982` | 1 | `docs/PS-246-RESULTAT.md` |
| `b737b45` | 1 | `ADDENDUM-08.md` |
| `742ae17` | 1 | `ADDENDUM-02.md` |
