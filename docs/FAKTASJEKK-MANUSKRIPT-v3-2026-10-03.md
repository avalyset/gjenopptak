# Faktasjekk av MANUSKRIPT-v3.md — 03.10.2026

Kontrollert fil: `docs/MANUSKRIPT-v3.md` (439 linjer), lest i sin helhet.
Kilder (forkortelser brukt i tabellen):

| kort | fil |
|---|---|
| FAKTA | `docs/MANUSKRIPT-FAKTA-2026-09-28.md` |
| REAN | `docs/REANALYSE-2026-10-03.md` |
| JSON | `Vault:revisjon-2026-10/reanalyse.json` (sha256 `ac782709d90ada77…`, kontrollert lik REAN l. 3) |
| CASE | `docs/CASEUTVALG-2026-10-03.md` |
| REF | `docs/REVISJON-2026-10-03-REFERANSER.md` + råsvar i Vault `revisjon-2026-10/referanser/` (Crossref/arXiv) |
| PP2 | `docs/PREPRINT-v2.md` |
| andre | ADDENDUM-11, -15, -22, -27, `docs/METODE.md`, `docs/LAERDOM.md`, `docs/RESULTAT-ADDENDUM-25.md`, `docs/RESULTAT-ADDENDUM-27.md`, `docs/saker/SAK-09b/RESULTAT.md`, `docs/PS-246-RESULTAT.md`, `docs/LOFTBARE-VURDERING-v1.md`, `docs/SAKBEHANDLING-2026-09-27-triage.md`; Vault `presisjonssett/port-presisjonssett-ADDENDUM10.jsonl`, `revisjon-2026-10/menneskevalidering/nokkel.jsonl` |

Merk om navn: v3s «phase 1» = de første 100 verkene; v3s «phase 2» = kildenes **fase 3 / ADDENDUM-25**. (PP2 brukte «phase 2» om casearbeidet.) Ikke et avvik, men tallmanifestet må bære koblingen.

---

## (a) Alle kontrollerte punkter

Avledede tall er regnet om her (kolonnen «kontroll»).

| # | v3 l. | påstand | kilde | kontroll | status |
|---|---|---|---|---|---|
| 1 | 3 | ORCID 0009-0001-9188-6788, EcoDeco AS, Lillehammer | PP2:3 | | STEMMER |
| 2 | 5, 344 | konsept-DOI 10.5281/zenodo.22959326 | FAKTA:62; PP2:4 | | STEMMER |
| 3 | 6, 344 | versjon v0.5.0 følger manuskriptet | `docs/TALLMANIFEST.md`:3 («Zenodo v0.5.0 (utkast)») | men referanselista l. 370–371 bærer v0.4.0 → se A-1 | STEMMER (se A-1) |
| 4 | 17 | 100 OA-verk, fire formålsvalgte felt | PP2:15–16 | | STEMMER |
| 5 | 18 | 432 kandidatrader | FAKTA:184; JSON `f_duplikater[0].rader` | | STEMMER |
| 6 | 18–19 | deduplisert til 276 erklæringer | JSON `f_duplikater[0].unike_erklæringer`=276; REAN:69 | | STEMMER |
| 7 | 19 | «among decided declarations, 71.2 %» H7 | JSON `f_duplikater[0].H7_av_unike` 183/257=0,7121 | tallet stemmer; nevneren 257 er ikke «decided» → A-2 | AVVIK (ANNET) |
| 8 | 20 | 100 nye arkeologiverk | FAKTA:444; PP2:414 | | STEMMER |
| 9 | 20–21 | 85 av 100 bekreftet, klynget 76,2–93,8 | JSON `a_porter_recall.fase3_port_85_100` k=85, klynge [0.7619, 0.9375] | 76,19→76,2; 93,75→93,8 | STEMMER |
| 10 | 22 | 95 av 104 beholdt, 20 verk | JSON `fase3_beholdt` 95/104; FAKTA:485 | | STEMMER |
| 11 | 23 | klynget 76,9–96,7 | JSON `fase3_beholdt.klynge_bootstrap95` [0.7692, 0.9671] | | STEMMER |
| 12 | 26 | κ 0,812 mellom «two agentic instances» | JSON `a_c_kappa.par.koder 1 mot koder 2.kappa`=0.8124 | tallet stemmer; at koder 1 var *agentisk* er ikke belagt → C-1 | STEMMER (tall) |
| 13 | 27 | paret differanse 0,177 [0,057–0,318] | JSON `differanse_koder2_minus_opus` punkt 0.1768, klynge [0.0571, 0.3178] | | STEMMER |
| 14 | 28–29 | seks forsøk, ingen løftet, tre stoppet på manglende inndata | CASE:44; FAKTA:357–359; PP2:31–33 | | STEMMER |
| 15 | 38 | sitatet «we were unable to code all data about discharge diagnosis and insurance status» | PP2:49 | | STEMMER |
| 16 | 47, 117 | ni-klasse typologi, fastsatt før data | PP2:58–62 | | STEMMER |
| 17 | 56–57 | BAGELS: benchmark for automatisk uttrekk og generering av limitations (Al Azher et al., 2025) | REF:9; arXiv 2505.18207-sammendrag | | STEMMER |
| 18 | 57–58 | LimitGen, syntetiske og menneskeskrevne limitations (Xu et al., 2025) | REF:10; arXiv 2507.02694 («LimitGen-Syn … LimitGen-Human, a collection of real human-written limitations») | | STEMMER |
| 19 | 63 | 81,4 % av tekstbitene har ingen seksjonsmerking | ADDENDUM-15:19 (18 099 av 22 243) | 18 099/22 243 = 81,37 % | STEMMER (gjelder de første 100 verkene) |
| 20 | 67–68 | biorc800, manuelt annotert (Lan et al., 2024) | REF:11; arXiv 2411.15623 | | STEMMER |
| 21 | 68–69 | SemEval-2021 NLPContributionGraph (D'Souza et al., 2021) | REF:15 | | STEMMER |
| 22 | 73–74 | Gu et al. 2026: effektive assistenter, ikke pålitelige uavhengige annotører mot eksperter | REF:12 | | STEMMER |
| 23 | 76–77, 160 | klynget bootstrap beskrevet av Vanbelle (2019) | REF:13 (§ 4.2 i fulltekst) | | STEMMER |
| 24 | 86 | protokoll låst internt 12.09.2026, hash som første commit | PP2:5–6, 138 | | STEMMER |
| 25 | 87 | første tredjeparts tidsstempel = deponering 25.09.2026 | PP2:143 | | STEMMER |
| 26 | 88 | tre regelpresiseringer skrevet etter data | PP2:141; FAKTA:395 | | STEMMER |
| 27 | 94 | «Two deviations occurred and are reported in §5.5» | §5.5 l. 249–252 lister **tre**; RESULTAT-ADDENDUM-25 §0.2, 0.3, 0.5–0.8 og §1.5 fører flere | → A-3 | AVVIK (ANNET) |
| 28 | 96 | seks gjenåpningsforsøk valgt ved skjønn | CASE:7–9 | | STEMMER |
| 29 | 97–98 | «lifted»-kriteriet skrevet etter de seks | CASE:49; PP2:189 | | STEMMER |
| 30 | 102 | OpenAlex, 2015–2020, OA med hentbar fulltekst | PP2:79 | | STEMMER |
| 31 | 103 | 25 verk fra hvert av fire felt | PP2:81–82 | | STEMMER |
| 32 | 104–105 | fase 2 (kildenes fase 3): 100 verk fra den frosne arkeologirammen, ingen overlapp | PP2:414–415 | | STEMMER |
| 33 | 108–109 | setning ± 2, stride 3 | FAKTA:273; PP2:89–90 | | STEMMER |
| 34 | 123 | tre ikke-treff-former N1–N3 | PP2:62–64 | | STEMMER |
| 35 | 124 | H1–H6 løftbar, H7–H9 ikke | FAKTA:195–196 | | STEMMER |
| 36 | 132 | `gemma2:9b`, temp 0, fast frø | FAKTA:274 | | STEMMER |
| 37 | 134 | fase 1: 2 844 av 22 243 (12,8 %) | FAKTA:276, 533 | 2 844/22 243 = 12,79 % | STEMMER |
| 38 | 134 | fase 2: 4 107 av 21 361 (19,2 %) | FAKTA:533 | 4 107/21 361 = 19,23 % | STEMMER |
| 39 | 135 | leser `claude-opus-5` | FAKTA:131, 553 | | STEMMER |
| 40 | 136 | partier på høyst 356 | ADDENDUM-25:56; ADDENDUM-22:92; PP2:163 | | STEMMER |
| 41 | 138 | fase 2 modell-ID verifisert per økt fra utskrifter | FAKTA:553–556 | | STEMMER |
| 42 | 146–147 | koder 4 = Claude Fable 5.1 i chat, modell-ID ikke ført | FAKTA:136; PP2:124–125 | | STEMMER |
| 43 | 147–148 | 7 av 320 rader ikke blindkodet | FAKTA:139 | | STEMMER |
| 44 | 160 | 10 000 replikater, frø 734248 | JSON `B`=10000, `frø`=734248 | | STEMMER |
| 45 | 166 | 149 passasjer fra 75 verk | `docs/RESULTAT-ADDENDUM-27.md`:12; ADDENDUM-27:34; Vault `menneskevalidering/nokkel.jsonl` (149 rader, 75 unike `doc_id`, talt her) | strata 25+30+30+15+15+15+19 = 149 | STEMMER |
| 46 | 166–169 | strata: silpositive/-negative, tvil/ikke tvil, alle fire felt, fase 2 positive og bom; trukket etter låsen | RESULTAT-ADDENDUM-27:7–25 | | STEMMER |
| 47 | 177 | 432 rader fra 60 av 100 verk | FAKTA:187; JSON `a_klasser[0].H7_av_alle.fordeling.verk`=60 | | STEMMER |
| 48 | 177–178 | 269 deler setning; 276 erklæringer | JSON `f_duplikater[0]` 269 / 276 | | STEMMER |
| 49 | 179 | 183 av 257 (71,2 %, 65,4–76,4) «among decided declarations» | JSON `f_duplikater[0].H7_av_unike` k=183 n=257 andel 0.7121 **wilson95** [0.654, 0.764] | tall stemmer; intervallet er Wilson, ikke verksklynget (§3.6 sier klynget som standard); 257 = 276 − 19 blandet, inkluderer uavklarte → A-2, A-4 | AVVIK (ANNET) |
| 50 | 179–180 | 42 av 245 (17,1 %, 12,9–22,4) løftbar | JSON `f_duplikater[0].H1_H6_av_avklarte_unike` 42/245=0.1714, **wilson95** [0.129, 0.224] | tall stemmer; intervallet umerket Wilson → A-4 | AVVIK (ANNET) |
| 51 | 180 | 19 erklæringer med delt klasse holdt utenfor | JSON `f_duplikater[0].blandet_klasse`=19 | | STEMMER |
| 52 | 181 | per rad H7 289 av 432 (klynget 58,2–79,7) | JSON `a_klasser[0].H7_av_alle` k=289, klynge [0.582, 0.7968] | | STEMMER |
| 53 | 181–182 | løftbar 77 av 406 avklarte rader (9,0–26,5) | JSON `a_klasser[0].H1_H6_av_avklarte` 77/406, klynge [0.0901, 0.265] | 406 = 432 − 26 | STEMMER |
| 54 | 182–183 | ett verk bidrar 118 rader | JSON `a_klasser[0].H7_av_alle.fordeling.største_verk`=118 | | STEMMER |
| 55 | 183–184 | klassetall H7 289, H5 50, H9 29, uavklart 26, H2 14, H8 11, H1 10, H3 2, H4 1, H6 0 | FAKTA:203–204 | sum = 432; H1–H6 = 50+14+10+2+1+0 = 77 ✓ | STEMMER |
| 56 | 186–187 | arkeologi 274/990 (27,7 %) | JSON `d_felt.arkeologi` 0.2768; FAKTA:597 | | STEMMER |
| 57 | 187 | klin. epid. 53/347 (15,3 %) | JSON `d_felt.klinisk_epidemiologi` 0.1527 | | STEMMER |
| 58 | 187 | tekstvitenskap 37/378 (9,8 %) | JSON `d_felt.tekstvitenskap` 0.0979 | | STEMMER |
| 59 | 188 | energimodellering 68/1 129 (6,0 %) | JSON `d_felt.energimodellering` 0.0602 | | STEMMER |
| 60 | 188 | andel tekstbiter som «reach the sieve» 6,8–17,5 % | JSON `d_felt.*.silkandidatenes_andel_av_tekstbiter` 0.0677–0.1755 | tallene stemmer; «reach» skal være «pass/become candidates» → A-5 | AVVIK (ANNET) |
| 61 | 189–190 | silens retensjon per felt ikke målt i fase 1 | JSON `d_felt._merknad`; REAN:42 | | STEMMER |
| 62 | 194 | 320 passasjer, 92 verk, største 33 | JSON `a_c_kappa.fordeling_320` | | STEMMER |
| 63 | 198 | koder 1–2: κ 0,812, 0,711–0,909, 96,2 %, PABAK 0,925, AC1 0,953, 39/33 | JSON `par.koder 1 mot koder 2` (0.8124; [0.7108, 0.9094]; 0.9625; 0.925; 0.9531; 39/33) | | STEMMER |
| 64 | 199 | koder 4–2: 0,899, 0,833–0,974, 98,1 %, 0,963, 0,977, 33/33 | JSON `par.koder 4 mot koder 2` (0.8986; [0.8327, 0.9736]; 0.9812; 0.9625; 0.977) | | STEMMER |
| 65 | 200 | koder 4–1: 0,781, 0,675–0,877, 95,6 %, 0,912, 0,945, 33/39 | JSON `par.koder 4 mot koder 1` (0.7811; [0.6753, 0.8771]; 0.9563; 0.9125; 0.9453) | | STEMMER |
| 66 | 202 | fall 0,024–0,025 uten de sju | METODE:482–484; FAKTA:139 (0,874; 0,757) | 0,899−0,874=0,025; 0,781−0,757=0,024 | STEMMER |
| 67 | 202–203 | kontrollparet faller 0,018, aldri eksponert | METODE:484, 476 (0,812→0,794) | | STEMMER |
| 68 | 203–204 | fallet skyldes tap av referansepositive; rekkefølgen uendret | METODE:481–483, 487–488 (6 av 27 kjente i de sju) | | STEMMER |
| 69 | 205 | klasse-κ koder 1–2 0,722 | METODE:74–75 | | STEMMER |
| 70 | 205–206 | N3 κ 0,530, N2 κ 0,535 | METODE:84–85 | | STEMMER |
| 71 | 206 | N3 talt 54, 34 og 13 ganger | METODE:85 (54, 34), 407 (koder 4: 13) | | STEMMER |
| 72 | 206–207 | N3-beslutningsregel skrevet, effekt ikke målt | PP2:254–256 | | STEMMER |
| 73 | 207–208 | av 27 referansepositive er bare 3 treff hos begge uten tvil | FAKTA:101 | | STEMMER |
| 74 | 213 | Haiku 4.5 κ 0,031 | FAKTA:151 | | STEMMER |
| 75 | 213 | Sonnet 5 κ 0,294 | FAKTA:152 | | STEMMER |
| 76 | 213 | Opus 5 κ 0,636 (0,503–0,744) | JSON `par.Opus ett kall mot koder 1` 0.6356, klynge [0.5027, 0.7439] | | STEMMER |
| 77 | 214 | agentisk Opus κ 0,812 | JSON (som #63) | | STEMMER |
| 78 | 215 | differanse 0,177, klynget 0,057–0,318, utelukker 0 | JSON `differanse_koder2_minus_opus`; REAN:18 | | STEMMER |
| 79 | 216 | lokal 7B agentisk κ 0,248 | LAERDOM:870 (qwen2.5:7b, ADDENDUM-24); PP2:275 | | STEMMER |
| 80 | 220 | port: minst 22 av 27 | FAKTA:245; PP2:182–183 | | STEMMER |
| 81 | 221 | bekreftet 21, porten falt | FAKTA:245 | | STEMMER |
| 82 | 221–222 | alle seks tap tvilsmerket av referansekoderen | Vault `presisjonssett/port-presisjonssett-ADDENDUM10.jsonl`: PS-133, -148, -226, -292, -297, -315 har alle `tvil: true` (sjekket her); ADDENDUM-22:218 | | STEMMER |
| 83 | 222 | terskel 81 % | 22/27 = 81,5 % | | STEMMER |
| 84 | 223 | referansekodernes enighet 19 av 27, 70,4 % | FAKTA:98; PP2:298 | 19/27 = 70,37 % | STEMMER |
| 85 | 223–224 | post hoc port: 100 trukket | FAKTA:249 | | STEMMER |
| 86 | 224–225 | 85 av 100, klynget 75,7–92,3; 33 verk, største 21 | JSON `post_hoc_port_85_100` (klynge [0.7571, 0.9231]; verk 33; største 21) | | STEMMER |
| 87 | 229–230 | 20 av 100 lest fra perm til perm av tjue agentiske instanser, tom kontekst, regelfil, sperreliste | PP2:416–418 | | STEMMER |
| 88 | 230–231 | nøkkelen sikret med hash før silen startet | PP2:418–419 | | STEMMER |
| 89 | 231–232 | 104 referansepositive i 12 av 20 verk; ett verk har 51 | FAKTA:485, 494; JSON `fase3_beholdt.fordeling` (verk 12, største 51) | | STEMMER |
| 90 | 236 | bekreftelse 85/100, 38 verk, 76,2–93,8 | JSON `fase3_port_85_100` (verk 38) | | STEMMER |
| 91 | 237 | retensjon 95/104 (91,3 %), 76,9–96,7 | JSON `fase3_beholdt` andel 0.9135 | | STEMMER |
| 92 | 238 | leserenighet 85/104 (81,7 %), 60,9–89,7 | JSON `fase3_bekreftet` 0.8173, klynge [0.6094, 0.8966] | | STEMMER |
| 93 | 239 | uten 51-verket: 45/53 (84,9 %) | FAKTA:495 | 104−51=53; 95−50=45; 45/53=84,9 % | STEMMER |
| 94 | 240 | uten 51-verket: 38/53 (71,7 %) | FAKTA:496 | 85−47=38; 38/53=71,7 % | STEMMER |
| 95 | 242 | 37 av 38 uten tvil, 48 av 62 med tvil, post hoc | FAKTA:475–476; RESULTAT-ADDENDUM-25:105 («Følsomhet, ikke port»; ADDENDUM-25 forhåndsspesifiserer ikke leser-tvil) | 37+48=85, 38+62=100 | STEMMER |
| 96 | 243 | 673 rader fra 73 av 100 verk | FAKTA:510–511 | | STEMMER |
| 97 | 243–244 | 424 erklæringer | JSON `f_duplikater[1].unike_erklæringer`=424 | | STEMMER |
| 98 | 244 | H7 265 av 402 (65,9 %, 61,2–70,4) «among decided declarations» | JSON `f_duplikater[1].H7_av_unike` 265/402, **wilson95** [0.612, 0.704] | 402 = 424 − 22 blandet, inkl. uavklarte; Wilson umerket → A-2, A-4 | AVVIK (ANNET) |
| 99 | 244–245 | løftbar 53 av 375 (14,1 %, 11,0–18,0) | JSON `f_duplikater[1].H1_H6_av_avklarte_unike`, **wilson95** [0.11, 0.18] | Wilson umerket → A-4 | AVVIK (ANNET) |
| 100 | 245–246 | 118 185 kontekst-tokens per leser-positiv; fase 1 164 805 | FAKTA:548 | | STEMMER |
| 101 | 248 | portterskel ≥ 0,70, bestått; navnet «worklist» | FAKTA:466, 474 | | STEMMER |
| 102 | 250–251 | referanserekkefølgen håndhevet ved prosedyre, i kode senere samme dag | PP2:419–422 | | STEMMER |
| 103 | 251 | registerleddet rettet etter låsen, radinnhold uendret | FAKTA:459, 560–561; PP2:462–464 | | STEMMER |
| 104 | 251–252 | to leserøkter traff bruksgrensen, fullført i ny instans | PP2:465–467 | | STEMMER |
| 105 | 256–258 | cellevektet estimator; 760 forventede referansepositive | JSON `e_prevalens.punkt.T`=759.9 | | STEMMER |
| 106 | 258 | 3,42 % (klynget 1,3–7,5) | JSON `e_prevalens.punkt.prevalens`=0.03416; `verksklynget_bootstrap95` [0.013, 0.0753] | 760/22 243 = 3,42 % | STEMMER |
| 107 | 258–259 | 2 positive blant 100 leste ikke-flaggede | REAN:63; JSON `ikke_flaggede_strata` (INGEN 1/50, N3 1/50) | stemmer med kilden; N1 (37) og N2 (13) er også lest i sin helhet med 0 positive, så alle leste ikke-flaggede er 150 — «100» er de utvalgte stratumene | STEMMER (merknad) |
| 108 | 259 | én antakelse: celler uten leste rader får feltets rate | REAN:57, 63 (14 celler, 26 tekstbiter) | | STEMMER |
| 109 | 264–265 | case A valgt 21.09.2026 av fire referansepositive i løftbar klasse, eneste med tilgjengelig inndata | CASE:11–16; LOFTBARE-VURDERING-v1:10–11 | | STEMMER |
| 110 | 265–266 | case B–F valgt 27.09 fra 50 rader, løftbar/uavklart, uten tvil | CASE:21–25 | | STEMMER |
| 111 | 267 | 19 saker (verk × hindring) | CASE:26; triage:14 | | STEMMER |
| 112 | 267 | 10 forkastet som krevde fysisk materiale, feltarbeid eller mennesker | triage:84–97 (overskriften dekker alle 10); CASE:27 skiller ut SAK-01 (= PS-246, allerede gjennomført) | stemmer med triagens overskrift; strengt er 9 forkastet av den grunnen + SAK-01 | STEMMER (merknad) |
| 113 | 272–274 | «lifted» = tre vilkår, definert etterpå | PP2:189–192; CASE:49 | | STEMMER |
| 114 | 274 | kriterier låst før beregning for A, B, C (PS-246, SAK-14, SAK-09b) | CASE:49–50 | | STEMMER |
| 115 | 278 | A: Pring (2016), H5, modellen tok ikke imot målt tetthet; inkonsistens reprodusert for de fire navngitte horisontene | LOFTBARE-VURDERING-v1:9–10; PS-246-RESULTAT:37, 49; PP2:313 | | STEMMER |
| 116 | 279 | B: Haouachi (2016), H3; 79 av 90 (87,8 %, terskel 90 %) | FAKTA:293, 303 | 79/90 = 87,78 % | STEMMER |
| 117 | 280 | C: Aragao (2018), H5; ikke løftet med det navngitte middelet | FAKTA:294 | | STEMMER |
| 118 | 281 | D: Aragao (2018), intervjumateriale holdt tilbake under samtykke | FAKTA:295 | | STEMMER |
| 119 | 282 | E: Riris (2018), H5; kode ikke funnet i seks ruter; én rute uavklart | FAKTA:296, 359; PP2:317 | | STEMMER |
| 120 | 283 | F: Bynum et al. (2021), H5; scenariosett og fordelingsparametere ikke rapportert | FAKTA:297, 359 | | STEMMER |
| 121 | 285–286 | 90-nevneren brukt; 55 av 60 (91,7 %) post hoc følsomhet | FAKTA:307, 310–311 | 55/60 = 91,67 % | STEMMER |
| 122 | 286–287 | to av åtte kontrollerbare henvisninger peker på feil sted | FAKTA:320–321 | | STEMMER |
| 123 | 287–289 | begge teksttjenestene svarte HTTP 200 med annet sted; alle elleve bom ville vært ført som løst | FAKTA:318–319; PP2:332–335 | | STEMMER |
| 124 | 289–290 | case C: avhandlingens tall reprodusert eksakt (12 av 12) «in two implementations» | SAK-09b/RESULTAT:20 (12 av 12, D.1, lest med pdftotext), :50 («Total feil 14, reprodusert i to implementasjoner»); FAKTA:331, 334 | 12/12 stemmer; «to implementasjoner» hører til total feil 14 → A-6 | AVVIK (ANNET) |
| 125 | 290–291 | omgåelsen har feil 14 mot 18 for beste tvungne søk fra 120 starter | FAKTA:337 | | STEMMER |
| 126 | 292–293 | 100 scenarioer < 0,001 %; C(41,7) = 22 481 940; 0,000445 % | FAKTA:297, 345, 353 | regnet: C(41,7) = 22 481 940; 100/22 481 940 = 0,000445 % | STEMMER |
| 127 | 295–296 | tre videre parkerte poster: ingen senere arbeid i siteringsgrafen | FAKTA:367–375 (SAK-15, -16, -17) | | STEMMER |
| 128 | 301–302 | bekreftelse 85 av 100 i begge faser | JSON `post_hoc_port_85_100`, `fase3_port_85_100` | | STEMMER |
| 129 | 302 | retensjon over 90 % i fase 2 | 91,3 % (#91) | | STEMMER |
| 130 | 303–304 | «Among decided declarations in both phases, about two thirds name data that never existed — an obstacle no later tool can remove» | 71,2 % / 65,9 % (JSON `f_duplikater`) | «about two thirds» er grovt for 71,2 %; «decided» som A-2; «no later tool can remove» er sterkere enn kildenes «dated assessment» → A-7 | AVVIK (ANNET) |
| 131 | 304–305 | ingen hindring vist løftet | FAKTA:439 | | STEMMER |
| 132 | 308–309 | fase 2-referansen og leseren deler leverandør og regelfil | FAKTA:502, 573 | | STEMMER |
| 133 | 310–311 | fase 2-retensjonen domineres av ett verk, bredt klynget intervall | JSON `fase3_beholdt` (største 51; [76,9–96,7]) | | STEMMER |
| 134 | 311–313 | tre av seks stoppet på manglende inndata; ikke estimat; ingen sammenlikning med modellkapasitet | CASE:44–46 | | STEMMER |
| 135 | 327 | ingen menneskelig annotering ennå; studie forhåndsregistrert | RESULTAT-ADDENDUM-27:3 | | STEMMER |
| 136 | 328–329 | koder 4s modell-ID ikke ført; koder 1, 2 og fase 2-referanseleserne deler leverandør og regelfil | FAKTA:136, 388–389 (koder 1 og 2 Opus); PP2:118, 417 (koder 2 og referanselesere: koder 2-regelfilen) | at koder 1 brukte *samme regelfil* er ikke belagt → C-2 | IKKE FUNNET (delvis) |
| 137 | 330–331 | fase 1 ikke tredjeparts tidsstemplet før data; tre regelpresiseringer etter data | PP2:141–143 | | STEMMER |
| 138 | 333 | fire felt i fase 1, ett i fase 2 | PP2:79–81; FAKTA:570 | | STEMMER |
| 139 | 335–336 | retensjon målt bare i fase 2, på 20 verk, ett holder halvparten | FAKTA:494 (51 av 104 = 49 %) | | STEMMER |
| 140 | 337 | leserens verdikter daterte og ikke repeterbare | PP2:165–166 | | STEMMER |
| 141 | 338–339 | bedømbarhet: 88 % og 32 % | ADDENDUM-11:78 (22/25 = 88,0 %; 6/19 = 31,6 %) | 31,6 → 32 | STEMMER |
| 142 | 343 | Apache-2.0; egne data CC BY 4.0 | PP2:548–550 | | STEMMER |
| 143 | 345–349 | deponeringen inneholder «both registers as indices» | PP2:564–565 sier register v2 ikke er i noen deponert versjon; v0.5.0 er utkast (TALLMANIFEST:3) — gjelder framtidig deponering, kan ikke kontrolleres nå | IKKE FUNNET → C-3 |
| 144 | 356 | skriveverktøy Claude, Anthropic | PP2:572 | | STEMMER |

### Referanser: sitert i teksten mot referanselista

| # | sitat i v3 (linje) | oppføring i lista | mot REF / PP2 / Crossref | status |
|---|---|---|---|---|
| R1 | Al Azher et al., 2025 (57) | l. 365–368 | forfattere, tittel, Findings EMNLP 2025, s. 19279–19294, DOI `10.18653/v1/2025.findings-emnlp.1050` = REF:9 = Crossref | STEMMER |
| R2 | Xu et al., 2025 (58) | l. 426–429 | forfattere, ACL 2025 (63rd), s. 20652–20706, DOI `…acl-long.1009` = REF:10 = Crossref (Crossref-tittelen har «(Volume 1: Long Papers)», utelatt — ufarlig) | STEMMER |
| R3 | Lan et al., 2024 (68) | l. 397–399 | s. 16086–16104, DOI `…findings-emnlp.944` = REF:11 = Crossref | STEMMER |
| R4 | D'Souza et al., 2021 (69) | l. 378–380 | «Proceedings of the 15th International Workshop on Semantic Evaluation», s. 364–376, DOI `…semeval-1.44` = Crossref (REF:15 skriver «SemEval-2021», samme verk) | STEMMER |
| R5 | Gu et al., 2026 (74, 309) | l. 382–384 | seks forfattere, Findings ACL 2026, s. 71–89, DOI `…2026.findings-acl.4` = REF:12 = Crossref | STEMMER |
| R6 | Vanbelle (2019) (77, 160) | l. 423–424 | år 2019, bind 28, s. 3012–3026, DOI `10.1177/0962280218794733` = REF:13 = Crossref; hefte 10–11 mangler, og kursiveringen («*…Research, 28*») skiller seg fra de andre oppføringene | STEMMER (formmerknad, A-10) |
| R7 | Pring (2016) (278) | l. 408–409 | = PP2:607–608 | STEMMER |
| R8 | Haouachi (2016) (279) | l. 390–391 | = PP2:593–594 | STEMMER |
| R9 | Aragao (2018) (280, 281) | l. 415–418 «Rodrigues Aragao, R. (2018)» | oppføringen = PP2:614–617, men sitatnøkkelen «Aragao» matcher ikke førsteleddet «Rodrigues Aragao» | AVVIK (ANNET) A-8 |
| R10 | Riris (2018) (282) | l. 411–413 | = PP2:610–612 | STEMMER |
| R11 | Bynum et al. (2021) (283) | l. 373–376 | = PP2:584–587 | STEMMER |
| R12 | — | Botten Nicolaysen (2026) v0.4.0, l. 370–371 | = PP2:581–582, men **ikke sitert** i v3, og v3 l. 6/344 sier at v0.5.0 følger manuskriptet | AVVIK (ANNET) A-1 |
| R13 | — | Hansen et al. (2019), l. 386–388 | = PP2:589–591; **ikke sitert** (l. 295 omtaler «three further parked items» uten sitat) | AVVIK (ANNET) A-9 |
| R14 | — | Karatas (2018), l. 393–395 | = PP2:596–598; **ikke sitert** | AVVIK (ANNET) A-9 |
| R15 | — | Mecking et al. (2017), l. 404–406 | = PP2:603–605; **ikke sitert** | AVVIK (ANNET) A-9 |
| R16 | — | MATPOWER (n.d.), l. 401–402 | = PP2:600–601; **ikke sitert** (C(41,7) i l. 292 uten MATPOWER-kilde) | AVVIK (ANNET) A-9 |
| R17 | — | Zimmerman et al. (2011), l. 437–439 | = PP2:622–624; **ikke sitert** | AVVIK (ANNET) A-9 |
| R18 | — | Todd (2024), l. 420–421 | = PP2:619–620; **ikke sitert** (OpenTimestamps nevnt l. 345 uten sitat) | AVVIK (ANNET) A-9 |
| R19 | — | Žiberna (2018), l. 431–432 | = PP2:626–627; **ikke sitert** (pakken ikke navngitt i v3, l. 280 «the named package») | AVVIK (ANNET) A-9 |
| R20 | — | Žiberna (2025), l. 434–435 | = PP2:629–630; **ikke sitert** | AVVIK (ANNET) A-9 |

Alle seks referansene fra REF som går videre (BAGELS, LimitGen, LLM-SSC/biorc800, Gu et al., Vanbelle 2019, NLPContributionGraph) er med og stemmer med REF og Crossref-råsvarene. Vanbelle 2017 (REF:14) er riktig utelatt, som REF anbefaler. Alle 14 oppføringer overtatt fra PP2 er ordrett like PP2.

---

## (b) AVVIK

### REN TALLFEIL

**Ingen.** Alle tall i v3 som har en entydig kilde, stemmer med kilden etter avrunding, også de avledede (prosenter, differanser, summer).

### ANNET

| id | v3 l. | avvik | kilde | type |
|---|---|---|---|---|
| A-1 | 6, 344 mot 370–371 | Manuskriptet sier at v0.5.0 følger det, men referanselista har bare Botten Nicolaysen (2026) **v0.4.0** (`10.5281/zenodo.23073893`), og den oppføringen siteres ikke i teksten. | PP2:581–582; TALLMANIFEST:3 | referanseavvik |
| A-2 | 19, 179, 244, 303 | «Among decided declarations» brukes om H7-andelen, men H7-nevnerne 257 og 402 er erklæringer uten delt klasse (276−19, 424−22) og **inkluderer uavklarte** (H1/H7). De avklarte er 245 og 375, som er nevneren for den løftbare andelen. Tallene er riktig gjengitt, men etiketten er feil, og de to andelene i samme setning har ulik nevner. Rettingen må være en omformulering («among declarations with a single majority class») eller en ny beregning (H7 av avklarte), som ikke finnes i kilden. | JSON `f_duplikater[*].H7_av_unike` mot `.H1_H6_av_avklarte_unike`; REAN:69–72 | formulering/nevner |
| A-3 | 94 | «Two deviations occurred and are reported in §5.5», men §5.5 (l. 249–252) lister tre: referanserekkefølgen, registerleddet og to økter på bruksgrensen. Utfallsdokumentet fører flere: modell-ID fra konfigurasjonen (§0.2), referanseporten som prosa (§0.3), avbrudd i ekstraksjonen (§0.5), leserøkter uten verdikt (§0.6), økter på øktgrensen (§0.7), registerleddet (§0.8) og manglende OpenAlex før-verdi (§1.5). Å bytte til «Three» er ikke nok uten en avklaring av hva som telles. | `docs/RESULTAT-ADDENDUM-25.md` §0.2–0.8, §1.5; PP2:461–468 | telling/formulering |
| A-4 | 179–180, 244–245 | Intervallene for deduplisert H7 og løftbar andel (65,4–76,4; 12,9–22,4; 61,2–70,4; 11,0–18,0) er **Wilson-intervaller på erklæringsnivå**, ikke verksklyngede. §3.6 (l. 159–161) sier at alle intervaller er verksklynget bootstrap «unless stated otherwise», og her står ikke noe annet. JSON har ikke klyngede intervaller for disse andelene. | JSON `f_duplikater[*].H7_av_unike.wilson95`, `.H1_H6_av_avklarte_unike.wilson95` | merking av metode |
| A-5 | 188 | «the share of passages that reach the sieve» — alle tekstbiter når silen. Tallet (6,8–17,5 %) er andelen som **blir silkandidater**. | JSON `d_felt.*.silkandidatenes_andel_av_tekstbiter`; REAN:35 | formulering |
| A-6 | 289–290 | «reported values were reproduced exactly (12 of 12) in two implementations» blander to kontroller. 12 av 12 er tabell D.1 (bånd, snittgrad, tetthet, lest fra PDF). De «to implementasjonene» gjelder total feil 14 og blokkene (1,7)/(1,8). | SAK-09b/RESULTAT:20–31, 50–58; FAKTA:331, 334 | formulering |
| A-7 | 303–304 | «an obstacle no later tool can remove» er sterkere enn kildene. Løftbarhet er en klasseverdi fra protokolltabellen og en **datert vurdering** (PP2:22; FAKTA:425, ADR-0010, H1→H8-eksempelet i PP2:480–483). I tillegg er «about two thirds» grovt for 71,2 % (fase 1), og «decided» har samme feil som A-2. | PP2:22; FAKTA:425 | påstand uten full dekning |
| A-8 | 280–281 | Sitatnøkkelen «Aragao (2018)» matcher ikke oppføringen «Rodrigues Aragao, R. (2018)». | PP2:614 (samme uoverensstemmelse arvet fra PP2:315–316) | referanseavvik |
| A-9 | 386–439 | Åtte oppføringer siteres ikke i teksten: Hansen 2019, Karatas 2018, Mecking 2017, MATPOWER n.d., Zimmerman 2011, Todd 2024, Žiberna 2018 og Žiberna 2025 (Botten Nicolaysen 2026 står under A-1). De var sitert i PP2 (§4.5–4.6), men v3 har kortet ned avsnittene som brukte dem. Enten må sitatene inn igjen (l. 280, 292, 295, 345), eller oppføringene ut. | PP2:315, 356–357, 383, 399–401 | referanseavvik |
| A-10 | 423–424 | Vanbelle: heftet (10–11) mangler, og kursiveringen avviker fra resten av lista («*…Research, 28*»). Ellers riktig. | Crossref `crossref-10.1177_0962280218794733.json` (issue «10-11») | form (lav) |

---

## (c) IKKE FUNNET

| id | v3 l. | påstand | hva som er søkt | merknad |
|---|---|---|---|---|
| C-1 | 26 | κ 0,812 er enighet mellom «two **agentic** instances» | FAKTA, PP2, METODE, ADDENDUM-11, LAERDOM | Tallet er belagt (JSON). At koder 2 er agentisk er belagt (FAKTA:131). At **koder 1** er en agentisk instans står ingen steder; FAKTA:388 sier bare «Koder 1 og 2 er Opus-instanser». |
| C-2 | 328–329 | koder 1 deler regelfil med koder 2 og fase 2-referanseleserne | samme | Koder 2-regelfilen ble satt sammen ordrett fra protokollseksjoner (PP2:118–119). At koder 1 leste med den samme fila, er ikke belagt. |
| C-3 | 345–349 | deponeringen v0.5.0 inneholder blant annet «both registers as indices» | PP2:564–565, TALLMANIFEST:3 | Gjelder en framtidig deponering. PP2 sier at register v2 ikke er i noen deponert versjon. Kan ikke kontrolleres før v0.5.0 er publisert. |

---

## Oppsummering

* **Kontrollerte punkter:** 144 tall- og påstandspunkter + 20 referanser (11 sitater i teksten og 20 oppføringer i lista, kryssjekket begge veier) = **164**.
* **STEMMER:** 133 av 144 tallpunkter (9 er AVVIK/ANNET, 2 IKKE FUNNET: #136, #143); #107 og #112 har merknad. 10 av 20 referanser stemmer (R6 med formmerknad).
* **AVVIK, REN TALLFEIL:** **0**.
* **AVVIK, ANNET:** **10** (A-1 til A-10). De berører 9 tallpunkter (#7, 27, 49, 50, 60, 98, 99, 124, 130) og 10 referanser (R9, R12–R20).
* **IKKE FUNNET:** **3** (C-1 til C-3; #136 er delvis belagt). Ingen av dem er tall.
