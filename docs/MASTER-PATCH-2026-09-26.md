# MASTER-PATCH 2026-09-26 — ferdig tekst til MASTER_GJENOPPTAK

**PÅFØRT 27.09.2026 i MASTER v0.2.** Hele patchen står nå i
`/Volumes/Vault/gjenopptak-kilder/master/arkiv/MASTER_GJENOPPTAK_v0_2_2026-09-27.md`
(sha256 `dd59ded0ce481c71…`), med statusblokk og changelog i ny § 0. Filen beholdes som
etterprøvbar kilde til hva som ble satt inn hvor.

**To poster var stale ved påføringen og ble rettet der, ikke her:** korrigendum-notatet heter
`docs/INNHENTET-2026-09-26-en-koder.md` (ikke `KORRIGENDUM-…`), og ekstraksjonstesten er **avgjort**,
ikke «i gang» — ADDENDUM-16 er målt og død som enhet. Setningen under om at MASTER ligger på Desktop
gjaldt 26.09; kanon ligger nå på Vault, jf. ADR-0009.

*Opprinnelig innledning, 26.09:* «MASTER redigeres ikke i denne slyngen (ligger på Desktop,
Bitdefender sperrer periodisk, bump gjøres ved øktslutt). Teksten under er ferdig til innsetting, med
målseksjon angitt per blokk.»

---

## → § 4 og § 8: grunnraten, regnet tre veier

**Erstatter ethvert sted der grunnraten står som «ett per 900».** Det tallet er 25/22 243 og måler
utvalget, ikke materialet.

> **Grunnraten, tre tall som ikke er det samme** (kilde: `data/port/spesifikasjon.json`,
> `data/port/presisjon-resultater.json`, `data/port-presisjonssett-ADDENDUM10.jsonl`,
> `data/port-presisjonssett-verdikter-koder2.jsonl`; utregningen står i `docs/METODE.md` § 1):
>
> | | koder 1 | koder 2 | hva tallet er |
> |---|---|---|---|
> | a) bekreftede treff / alle tekstbiter | ett per **890** (0,112 %) | ett per **1 171** (0,085 %) | måler **utvalget**, ikke materialet — skal ikke brukes som prevalens |
> | b) presisjon × flaggede / alle | ett per **61** (1,63 % [1,13–2,29]) | ett per **81** (1,24 % [0,81–1,85]) | et **gulv**: bare sanne blant flaggede |
> | c) b / implisert recall | ett per **29** (3,43 % [2,12–7,95]) | ett per **33** (3,04 % [1,73–7,55]) | **beste anslag**, korrigert for tapte |
>
> Implisert recall 47,5 % (koder 1) og 40,7 % (koder 2), regnet mot **400 tapte [110–1 405]** —
> bomraten blant de 100 leste ikke-flaggede (2/100, Wilson 0,55–7,00 %) × 20 070 ikke-flaggede.
> Intervallet i c er dominert av usikkerheten i tapte, ikke i presisjonen.

## → § 4: fasitens avgrensning

> **Fasiten er 25 sanne blant 150 leste dommer-flaggede tekstbiter.** De 320 leste bar i tillegg **2
> sanne blant de 150 ikke-flaggede** (én i INGEN, én i N3) og **12 ankertreff** med kjent fasit fra
> recall-sett 1 og 2 (koder 1, `data/port-presisjonssett-ADDENDUM10.jsonl`). Koder 2 fant 19, 2 og 11.
> De 12 ankerne er frøsettets egne passasjer og skal aldri inn i en recall-måling av en ny metode; de 2
> ikke-flaggede er dommerens tapte treff og rapporteres for seg, utenfor kriteriet.

## → § 4: nevneren og hva N inneholder

> **N = 22 243 står låst, og N inneholder 27,4 % ikke-prosa.** Etter en fast regel — under 50 %
> bokstaver eller treff på referansemønster (årstall + sidespenn, nummerrekke, initialrekke, `pp. n–m`)
> — er **6 098 av 22 243 tekstbiter og 490 av de 2 173 flaggede ikke prosa**
> (`ekstraksjon/2026-09-26/g3-ikke-prosa.json`). **Ett av de 25 fasit-treffene treffer regelen.**
> Nevneren er ikke endret og skal ikke endres: den er materialet slik porten så det. Men grunnraten i
> `docs/METODE.md` § 1 er regnet på en N som til godt over en fjerdedel ikke er løpende tekst, og et
> hvilket som helst κ- eller presisjonstall bærer den forurensningen.
>
> **Trekkingen av de 150 var ikke uniform** (gulv 25 på tekstvitenskap, `port.py`; LAERDOM § 15).
> **16,7 % gjelder utvalget.** Vektet mot feltfordelingen i de 2 173 blir det 16,69 %, vektet mot
> prosa/ikke-prosa 15,38 % — begge innenfor [11,6–23,4]. Datert note i ADDENDUM-10 § 7.
>
> **Rettelse 27.09.2026: 27,4 % reproduserer ikke.** Implementasjonen som produserte tallet lå i en
> kladdefil som ikke ble bevart; bare regelteksten står i utdatafilen. Regelen er reimplementert fra den
> teksten (`src/gjenopptak/classify/ikkeprosa.py`, sha256 `63ed734555a8bc95…`) og **avviker på alle fire
> kontrolltallene**: alle passasjer 5 455 mot 6 098 (−643), flaggede 453 mot 490 (−37), de 25 fasit-treff
> 3 mot 1 (+2), de leste portpassasjene 47 mot 19 (+28). Avvikene går i **begge** retninger, så det er en
> annen regel, ikke en skalert. **Hvilken av de to som er den formulerte, kan ikke avgjøres** — originalen
> finnes ikke. Tallet skal oppgis som «27,4 % etter regelen slik den ble kjørt 26.09, ikke reprodusert»,
> og den versjonerte regelen i `ikkeprosa.py` gir **24,5 %**. Nevneren står uansett låst; poenget — at N
> inneholder en stor andel ikke-prosa — står i begge versjoner.
>
> **Den stabile kjernen i fasiten er tre av 27.** Bare PS-044, PS-205 og PS-266 har enighet mellom koder 1
> og 2 *og* ingen tvil hos noen av dem (ADDENDUM-23 §1). Enige er 19 av 27; uten tvil hos koder 1 er
> **7**, hos koder 2 **4**. Koder 1 merket **20 av 27** med tvil. Det er grunnen til at ADDENDUM-22s port
> på 22 av 27 falt med 21: alle seks tapene var tvilsmerket, fire var allerede blant koder 2s uenigheter.
> **En terskel nær referansesettets ytterkant måler settet, ikke leseren.**

## → til neste Zenodo-versjon: (d) regelfilen

> **(d) Koder 2s regelfil, gjenvunnet 27.09.2026 — må med i neste deponering.** Deponerte versjoner
> v0.2.1 og v0.3.0 bærer κ = 0,812 uten at inndataen bak tallet finnes i pakken. Tre ting skal inn:
>
> 1. **Regelfilen selv:** `docs/REGELFIL-KODER2-GJENVUNNET-2026-09-27.md` med det gjenvunnede
>    innholdet, 167 linjer, 9 805 bytes, sha256
>    `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449`. Vault-kopi:
>    `koder2/koderegler-gjenvunnet.md`. Ført i `MANIFEST-VAULT.md`, seksjon «Koder 2-gjenvinning —
>    2026-09-27», med sti, bytes, sha256, opphav og autentisitetsgrunnlag.
> 2. **Sti og sha i ADDENDUM-11-utfallet:** §8 fører opphavet (øktutskrift, linje 13, 25.09 kl. 19:35),
>    de fire autentisitetskontrollene, den verifiserte lekkasjesjekken, `grep -n`-defekten som ikke sto
>    noe sted, og koder 2s modellsignatur `claude-opus-5` med målt kostnad.
> 3. **Gjenvinningsnoten:** at originalen lå i scratchpad og er borte, at sha-en gjelder det
>    gjenvunnede innholdet og ikke originalens bytes, og at avsluttende blanktegn og siste linjeskift
>    ikke kan verifiseres. Uten den setningen leser en bruker sha-en som en bit-identitet den ikke er.
>
> Ingen tall endres av dette. Det som endres, er at κ = 0,812 blir etterprøvbart for andre enn oss.

## → svaret på del D, i fire linjer

> **Deteksjon: ja, og prisen er kjent.** Kjeden finner parkerte spørsmål i skala — 432 av 2 844
> silte tekstbiter i de 100 verkene, med blind presisjon **85 % [76,7–90,7]**, og **98 % på de
> radene leseren ikke er i tvil om**. Målt pris: **164 805 kontekst-tokens per bekreftet treff**
> (`arbeidsliste/koder-c-komplett.json`).
> **Leseren er Opus, agentisk.** Ett-kall-modeller er sil-klasse: κ 0,031 (Haiku) og 0,294 (Sonnet)
> mot 0,636 for Opus per kall og 0,812 for Opus i én sammenhengende økt (ADR-0012, ADDENDUM-19 §7.1).
> **Løftbarhet er snevret inn til klassen.** Den avledes av en tabell, aldri av en modell (ADR-0004),
> og er datert (ADR-0010): 17,8 % [14,5–21,7] av treffene har løftbar klasse H1–H6, 76,2 % har ikke.
> **Fasitens stabile kjerne er tre av 27.** Bare PS-044, PS-205 og PS-266 har enighet mellom koder 1
> og 2 *og* ingen tvil hos noen av dem (ADDENDUM-23 §1), og det er grunnen til at en port på 22 av 27
> falt med 21.

## → § 9 åpne poster: legg til

> * **Koder 2s regelfil er gjenvunnet, og var aldri versjonert.** ADDENDUM-11 § 2 beskriver en regelfil
>   bygget av ordrette utdrag fra seks kilder. Filen (`scratchpad/koderegler.md`) lå aldri i git og
>   finnes ikke lenger på disk, men **hele innholdet er gjenvunnet fra koder 2s egen øktutskrift**
>   27.09.2026: 167 linjer, sha256 `234695dd4e1777a9`, ført i `docs/METODE.md` § 4 og
>   `docs/REGELFIL-KODER2-GJENVUNNET-2026-09-27.md`. **κ = 0,812 kan dermed reproduseres på sin egen
>   inndata**, og ADDENDUM-11s lekkasjepåstand er verifisert i stedet for hevdet. **Modell-ID er også
>   gjenvunnet fra samme utskrift: `claude-opus-5`**, 61 API-svar, 20 minutter, 9 019 781 tokens inn /
>   103 373 ut. Koder 2 var en CC-instans på Opus 5, agentisk, seks regelkilder — **ikke et menneske**.
>   Begge kodere er LLM-baserte; ingen menneskelig annotør finnes. ADR-0003-bruddet er dermed reparert
>   i ettertid, men det var reelt: signaturen sto ikke i addendumet.
> * **Fasiten er dommerbetinget.** De 25 måler recall-tap relativt til dommeren, ikke presisjon og
>   ikke absolutt recall, for enhver ny metode (`docs/METODE.md` § 2).
> * **«Én koder» står i PREREG-v1 § 4 og ADDENDUM-06**, innhentet av ADDENDUM-11 siden 25.09.2026.
>   Begge filene er låst; rettelsen hører i et datert korrigendum i egen fil, ikke inn i dem.
> * **OPPGAVEN-v2 finnes ikke på maskinen.** Søkt i repoet over alle refs, i `~/Desktop`, i
>   `~/Desktop/Master Dok./Gjenopptak/` og i `~/Documents` — ingen fil. B3-rettelsen kan derfor ikke
>   føres der; tallene står i `docs/METODE.md` § 1 i mellomtiden.
> * **Nevneren i utvalgstesen ble rettet før 2d.** «Treff per verk» målte lengde: avhandlingene har
>   1 301 tekstbiter hver mot artiklenes 169. Per 1 000 tekstbiter er avhandlinger **glisnest** (0,923)
>   og preprint tettest (2,049) — funnet står, retningen snudde. Gjeldende kriterium er ≥ 2× på fasit
>   per 1 000 tekstbiter: type 2,22× lever, felt 3,10× lever, leveringsform 1,55× dør
>   (`ekstraksjon/2026-09-26/b2-nevner.json`, ADR-0011 rettelsesseksjon).
> * **Duplikatraten i den sammensatte teksten er 12,92 %** (alle regex-fragmenter) mot **2,96 %** når
>   bare fragmenter med minst tre ord telles. Forskjellen er punktledere i innholdsfortegnelser. Den
>   låste terskelen sier «setninger», så 12,92 % gjelder, og **test 2′ er preregistrert som
>   ADDENDUM-17** (`ekstraksjon/2026-09-26/b1-duplikatrate.json`).
> * **«Én koder» i PREREG-v1 § 9 er innhentet;** korrigendum i
>   `docs/KORRIGENDUM-2026-09-26-en-koder.md`, pekt til fra README. Samme frase i ADDENDUM-06 § 1.6 er
>   fortsatt sann, men gjelder bare recall-fasiten.
> * **Ekstraksjonstesten (ADR-0011, ADDENDUM-16) er i gang, ikke avgjort.** 598 vinduer, målt rate
>   20,9 s/vindu → projeksjon 3,10 timer mot nærsøk-rutens 4,48 timer. Recall, blind presisjon og
>   samlet tid måles når kjøringen er ferdig.

## → § 8 lærdom: legg til

> **En vokter med håndskrevet filliste vokter listen, ikke dokumentsettet.** Kryssjekken meldte null
> avvik over tolv håndplukkede filer; utvidet til å oppdage settet fra disk leste den 40 filer og
> fant fire foreldede verdier med én gang. Det som ikke er i settet, kan ikke feile — og en grønn
> kjøring blir da en påstand om utvalget, ikke om materialet (LAERDOM § 28).

## → ny beslutning, med begrunnelse

> **Besluttet 26.09.2026: Verktøyet leverer en datert arbeidsliste med hindringsrute. Vurdering av
> opphevelse er sakbehandling per kandidat (ADR-0010), ikke et pipelinesteg.**
>
> Begrunnelsen er målt, ikke antatt. Fire siler er forkastet (ADDENDUM-06/07, -14, -15), og de to
> hypotesene i denne slyngen delte seg: utvalgstesen lever på **dokumenttype** (avhandling 1,200
> fasit-treff/verk mot artikkel 0,208 = **5,77×**, 5 og 77 verk) og på **felt** (arkeologi 0,520 mot
> 0,160 = **3,25×**), men dør på leveringsform (1,53×) og port-ledd (1,41×).
> **Seksjonsplassering er død for godt:** alle merkede treff krever 54,6 % av de merkede tekstbitene,
> over terskelen på 50 %. Og løftbarheten er datert per kandidat (ADR-0010): Heron gikk fra H1 til H8
> uten at teksten endret seg. En rørledning som skal avgjøre opphevelse, må da avgjøre en
> tilgangssituasjon som endrer seg utenfor materialet — det er sakbehandling, ikke et steg.

## → § 1 status på ledd 3

> **Ledd 3 står uendret. Ekstraksjon per dokumentvindu er målt og død** (ADR-0011, ADDENDUM-16):
> recall **9 av 25 = 36,0 %** mot kravet 21/25, og blind presisjon **17,0 % [10,9–25,5]** mot kravet
> over 23,4 %. Bare tidsvilkåret holdt: **4,28 t** (ekstraksjon 3,45 + dømming 0,83) mot komparatorens
> 4,48 t. **Fire siler og én enhetsendring er nå prøvd og forkastet.**
>
> **Statusen ledd 3 skal bære:** *den lokale modellen er en sil, ikke en detektor.* Kostnadsenheten er
> **frontier-lesninger per bekreftet treff**, og for dommeren er den **≈ 6** (2 173 flaggede / 362
> forventet sanne, avledet av presisjon 16,7 %).
>
> Ekstraksjonen gir **færre kandidater, samme presisjon, lavere recall**: 884 mot 2 173, 17,0 %
> [10,9–25,5] mot 16,7 % [11,6–23,4], 9 av 25 mot 25 av 25. Den fant likevel **begge treffene dommeren
> mistet** og to av de fire uten markørord.
>
> **Kaskaden er det eneste som slår leddene:** dommeren på ekstraksjonens Q-linjer gir presisjon
> **31,4 % [20,3–45,0]** med **94,1 %** bevaring av de sanne, og unionen dekker **27 av 27** kjente
> treff. Kilder: `ekstraksjon/2026-09-26/2d-recall.json`, `2d-tid.json`, `2d-blind-presisjon.json`,
> `d1-2x2.json`, `d2-tokenvolum.json`.
