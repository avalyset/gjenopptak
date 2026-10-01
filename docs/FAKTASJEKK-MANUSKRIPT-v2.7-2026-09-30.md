# Faktasjekk av MANUSKRIPT-v2.7-UTKAST — sjuende runde, bare de ni stedene — 30.09.2026

**Manuskript:** `docs/MANUSKRIPT-v2.7-UTKAST.md`, sha256 `dcc2c45b23e6218f2d22d7a44fd745706b57e9b3384128e5dc060ff026b6e52d`.
**Fasit:** radene i `FAKTASJEKK-MANUSKRIPT-v2.6-2026-09-30.md` og kildene de peker på. **Ingen prosa er omskrevet.**

**Mandat (eierens avgjørelse 30.09.2026):** bare de ni stedene fra sjette runde. Det som står igjen, føres som
**kjent rest; ingen ny runde.** Diffen mot v2.6 berører nøyaktig de ni stedene (l. 3–6, 36–37, 433–442, 447–450,
466–468, 475–485) og ingenting annet. Radfil på Vault: `manuskript/faktasjekk-v2.7/rest.jsonl` (sha256 `88fadb87e4603be7…`).

## De ni stedene

| v2.6-rad | v2.7 | status |
|---|---|---|
| 37, 434 «chain unchanged» | «chain as locked before the draw» / «the code of §3.2 with one extension made before the lock» (`--utvalg`); registerrettingen etter låsen står i l. 479–481 | **rettet** |
| 437 «an agentic Opus instance» | «twenty agentic Opus instances, one per work» | **rettet** |
| 439–440 referanseporten | 10:20:05 UTC og 29 sekunder til silen stemmer (MANIFEST-VAULT, `tilstand.json`); «enforced by procedure» stemmer; «in the resume routine's code since 13:04 UTC» — se rest | **rettet, med rest** |
| 445 «interrupted once» | fire avbrudd, oppregnet; 1 357 byte-identiske vinduer | **rettet, med rest** («write path») |
| 462–463 registerhodet | «recorded in the outcome document … the register schema still admits only "not measured"» — stemmer med RESULTAT § 1.7; «is to be extended» er en plan, ført som åpen post i MASTER-patchen | **rettet** |
| 470 nevneren | «per 1 000 passages of the corpus» | **rettet** |
| 471–472 kostnaden | «118 185 per reader hit, against 164 805 … and 139 053 per hit confirmed» — samme enhet | **rettet** |
| 472–477 «Three deviations» | «include … The full list is in the outcome document, §0»; fem avvik nevnt, alle i RESULTAT § 0–1 | **rettet** |
| 5–7 header | «revised after the sixth fact-check (`d118f50`) … as at commit `f4fb54a`, whose §9 carries the phase 3 numbers» — § 9 står i `f4fb54a` | **rettet** |

## Kjent rest — 2 rader

| linje | manuskriptet sier | riktig | kilde | status |
|---|---|---|---|---|
| 439–441 | «it has been enforced in the resume routine's code since 13:04 UTC the same day» | 13:04 UTC er referanseporten i kjedens `cli.py` (`6d905cd`); i gjenopptaksrutinen fra 13:09 UTC (`f6a2452`, da rutinen ble til) | `git log 6d905cd`, `git log f6a2452` | **upresist — kjent rest** |
| 448, 484 | «a blocked write path that stopped twelve reader sessions» / «blocked by the write path» | instansene ble stengt ute fra både blindfilene (lesing) og verdiktfila (skriving): `data` i worktreet pekte utenfor sandkassen | RESULTAT-ADDENDUM-25 § 0.6 | **upresist — kjent rest** |

Begge er upresise, ingen er feil i tall, og ingen snur en slutning.

**Observert utenfor mandatet** (uendret linje): l. 592 sier fortsatt «revised four times against fact-check
reports»; utkastet er nå kontrollert i sju runder.

## Tillegg 30.09.2026 — kjent rest fra frys-lesning 4 (ingen ny runde)

Frys-lesningen av det endelige v0.4.0-bygget leste hele manuskriptet, ikke bare de ni stedene, og fant
9 steder til. De føres her som **kjent rest** etter eierens avgjørelse; ingen prosa er omskrevet. Register:
Vault `zenodo/v0.4.0-bygg/frys4/leser-3.jsonl`.

| linje | alvor | manuskriptet sier | riktig |
|---|---|---|---|
| 430 | bør rettes | «*(Numbers in this section are from the ADDENDUM-25 run report of 30 September 2026 and are to be anchored in the fact file's phase 3 section before circulation | Tallene er forankret: MANUSKRIPT-FAKTA § 9 (l. 443–569) fører hvert fase 3-tall med sti og sha, og headeren l. 4–5 sier selv at § 9 i `f4fb54a` bærer dem. FAKTASJEKK-v2.6 l. 13–18 og l. 36 fant § 4.7 kontrollert mot § 9. Merknaden er foreldet og motsier header |
| 480 | merk | «so the register for this run is written by the corrected step, the one code change after the lock, with the row content unchanged hash for hash» | RESULTAT-ADDENDUM-25 § 0.3 (l. 52–56) fører også `kjede/cli.py` som «Avvik fra låsen» (c2eb33bc → 40ebef04, referanseporten), og § 0.8 (l. 294–295) sier at både `ledd.py` og `cli.py` skilte seg fra låsen i registerkallet. Presist: «the one change to the chain' |
| 485 | merk | «The full list is in the outcome document, §0.» | Flere av avvikene som nevnes, står i § 1, ikke § 0: OpenAlex-før-verdien i § 1.5 (RESULTAT-ADDENDUM-25.md:155–156) og feltnavnet i § 1.1 (l. 102–103). Den andre øktgrensen (økt 7) er ikke beskrevet i § 0; § 0.7 beskriver bare økt 3, og økt 7 går bare indirekte |
| 491 | merk | «**What the tool delivers.** On this material a field enters and a candidate list leaves» | Etter fase 3 leverer verktøyet også en «worklist (prospective gate)» (l. 470; MANUSKRIPT-FAKTA § 9 l. 465). Enten «a candidate list or, where a prospective gate has been passed, a worklist», eller avgrens «this material» til de første 100. |
| 517 | bør rettes | «class agreement is lower (0.722) and weakest at two non-hit boundaries (N3 0.530, N2 0.535)» (også l. 267–268 «the weakest boundary is a non-hit class: N3») | Kildetabellen i METODE.md:77–89 har lavere per-klasse-κ for H8 0,395, H9 0,498 og H1/H7-uavklart 0,498; N2 0,535 og N3 0,530 er de svakeste bare blant klasser med mer enn et par tilfeller (n ≤ 3 for de tre). Bør stå «weakest among classes with more than a hand |
| 527 | bør rettes | «*Reference set* is judge-conditioned and measures recall loss relative to the judge, not precision, absolute recall or prevalence.» | § 4.7 (l. 436–444, 462–468) bruker «reference set» om fase 3s referansesett: 20 verk lest i sin helhet før silen, ikke dommerbetinget, og det gir «the first measured recall» (95/104, 85/104; MANUSKRIPT-FAKTA § 9 l. 482–497). Definisjonen gjelder bare 25-settet |
| 529 | bør rettes | «*Confirmed* means a post hoc gate at 85 of 100, not the preregistered one, and 15 of the 100 were coded by a second instance.» | Gjelder bare kandidatlista. For fase 3 er «confirmed» en prospektiv port, 85/100 [76,7–90,7], én instans uten avbrudd (MANUSKRIPT-FAKTA § 9 l. 465–480; RESULTAT-ADDENDUM-25 § 1.1). § 4.7 bruker også ordet om recall («the reader confirmed 85 of the 104», l. 463 |
| 580 | bør rettes | «whether a bundle of the history after the v0.3.0 lock is included is a decision of the author, open at the time of this draft.» | Avgjort 29.09.2026, før utkastets dato 30.09: historikkbundlen er med (`--all`) (UTGIVELSE-v0.4.0-PORTSTATUS.md:183, :251; RELEASE-NOTES-v0.4.0). `gjenopptak-git-history.bundle` ligger i det bygde utkastet. Setningen var feil allerede da utkastet ble datert. |
| 592 | bør rettes | «and revised four times against fact-check reports produced by separate instances (`136d025`, `b084ba2`, `faaaddc`, `c4d645c`); a fifth check (`ffeaccf`) record | Headeren l. 3–6 sier at utkastet er revidert etter `ffeaccf` også, og etter en sjette (`d118f50`); en sjuende runde (FAKTASJEKK-v2.7) har kontrollert v2.7. AI-erklæringen motsier headeren. Observert utenfor mandatet i FAKTASJEKK-MANUSKRIPT-v2.7-2026-09-30.md:3 |

**To til fra frys-lesning 4, i andre lesere og i faktafila** (også kjent rest, ingen ny runde):

| linje | manuskriptet sier | riktig |
|---|---|---|
| 39–40, 463–464, 551–552 | recall 95/104 = 91,3 % [84,4–95,4] og 85/104 = 81,7 % [73,2–88,0], uten forbehold om klynger | treffene ligger i 12 av 20 verk, 51 i ett (R08); Wilson antar uavhengighet og er for smalt. Uten R08: 45/53 = 84,9 % [72,9–92,1] og 38/53 = 71,7 % [58,4–82,0] (FAKTA § 9, RESULTAT § 1.2) |
| 480 | «the corrected step, the one code change after the lock» | den eneste endringen i et **ledd**; `kjede/cli.py` ble endret 28.09 med referanseporten (RESULTAT § 0.3), som ikke rører noe ledd |

