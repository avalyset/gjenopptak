# Faktasjekk av MANUSKRIPT-v2.2-UTKAST — tredje runde, bare det som fortsatt avviker — 28.09.2026

**Manuskript:** `docs/MANUSKRIPT-v2.2-UTKAST.md`, sha256 `6018f7087d95e705385209afc2b5044590a5f696c2817eeea682829c422206f5`.
**Fasit:** `docs/MANUSKRIPT-FAKTA-2026-09-28.md` slik den sto i commit `acfd915` (sha256 `685d6ea0335bd0e8…`),
frosset som `manuskript/faktasjekk-v2.2/FAKTA-acfd915.md` på Vault, og kildene den peker til. SAK-08-tillegget i
triagen og REGISTER-SAKER (`d491df7`) kom under kontrollen og er ikke brukt som kilde. **Ingen prosa er omskrevet.**
Forrige runder: `FAKTASJEKK-MANUSKRIPT-v2-2026-09-28.md`, `FAKTASJEKK-MANUSKRIPT-v2.1-2026-09-28.md`.

## Metode

Kontrollert: de 173 linjene i v2.2 som er endret fra v2.1 (125), eller som ble endret fra v2 til v2.1 og står
uendret (48), og hver av de 45 avvikene og 4 venter-radene fra v2.1-kontrollen, slått opp i v2.2 og vurdert på
nytt også i ny ordlyd. Tall, DOI, sitat, sha, id og dato mot fasiten og kildene; κ regnet om med
`reliabilitet.py` (frø 734248), Wilson-intervaller regnet om, DOI-er mot doi.org og Crossref. Delrapporter på
Vault, `manuskript/faktasjekk-v2.2/`: del A (l. 1–263) sha256 `32903aa9ac7b08e3…`, del B (l. 264–526) sha256
`8b7cd40c6908218e…`; kart `kart-v2.1-til-v2.2.json`. Tekstkartet bommet der en påstand bryter over linjeskift;
kontrollørene fant stedene selv.

**Ett regelavvik i kontrollen, ført:** del A sendte ett GET-kall til `api.datacite.org` for konsept-DOI-en, som
ligger utenfor de tillatte vertene (doi.org, api.crossref.org). Bare den offentlige DOI-en ble sendt; svaret er
ikke brukt i vurderingen.

## Utfall

| | antall |
|---|---|
| avvik i v2.1 | 45 |
| **riktig rettet i v2.2** | **37** |
| **fortsatt avvikende** | **8** |
| **nye avvik i v2.2** | **4** |
| **avvik i v2.2 i alt** | **12** — 2 feil, 3 overclaim, 5 uklart, 2 uten kilde |
| venter på ADDENDUM-25-utfall eller plassholder | 4 |

## Avvik i v2.2, sortert på linje

| linje | manuskriptet sier | riktig | kilde | status |
|---|---|---|---|---|
| 4 | numbers that the fact file does not carry are marked in the text as taken from the named source document | Ikke gjennomført i l. 1–263: tall utenfor FAKTA står uten navngitt kilde — «16 September 2026» (l. 94; commit 630f861), «20 anchor passages … 8 non-hits» (l. 110), «three independent grounds» (l. 126; ADDENDUM-11 § 8), Zenodo «25 September 2026» (l. 147; ZENODO.md), «~3 000-token» (l. 158), «356» (l. 167; METODE § 9), N3 «54, 34 and 13», 0.530 og 0.722 (l. 254–255; METODE § 2/§ 9). Tallene stemmer mot kildene; merkingen mangler | Vault: manuskript/faktasjekk-v2.2/FAKTA-acfd915.md + docs/METODE.md + ADDENDUM-11.md (`685d6ea0`) | overclaim |
| 38 | for the 11 places where the thesis gives its own French rendering the original could be read against it, and two of eight checkable citations | Av de 11 stedene med fransk gjengivelse (10 unike) ble bare 9 oppløst, 8 unike; «PLVT., Rom. 19, 9» og «DION. HAL. AR. II 40, 5» har seksjon som ikke er adresserbar i den greske utgaven. Sammenligningen gjelder «de 8 unike stedene som både har avhandlingens egen gjengivelse og lot seg oppløse» | docs/saker/SAK-14/RESULTAT.md + Vault: saker/SAK-14/tabell.json (`cbb92c56`) | overclaim |
| 282 | whose corrected value after re-running the truncated items is 0.297 [0.125–0.456], n = 319. The invalid runs are kept, marked invalid, and not used. | 0,321→0,297 og «short rule excerpt» er rettet. Men Sonnet-kjøringen (ADDENDUM-18) ble ikke erklært ugyldig: de 12 avkuttede ble kjørt om, og 0,297 er «tallet som siteres». Bare 0,321 er foreldet («beholdes ved siden av»). «invalid … not used» passer bare Opus-kjøringen (0,390) | ADDENDUM-19.md § 3b og § 7.3 + ADDENDUM-18.md § 9 (`41a2f0cb`) | uklart |
| 336 | all eleven would have been recorded as hits and the case would stand as lifted at 100 % | HTTP 200-vilkåret er nå eksplisitt (v2.1-raden rettet). Men porten krevde gresk tekst «med de bærende termene identifisert», umålbart for 79 av 90. LAERDOM § 37: «Hadde det første leddet bestått, ville porten ikke hatt noe svar»; ADR-0013: slik port = ikke opphevet. RESULTAT.md sier «opphevet på 100 %» — kildene spriker | docs/LAERDOM.md § 37 + docs/decisions/0013-opphevelse-definisjon.md + docs/saker/SAK-14/RESULTAT.md (`f8fe0772`) | uklart · **ny** |
| 367 | with free block-type choice the objective is degenerate, so all searches here fixed the types per position to the thesis's own image matrix. | Bare de egne søkene låste typene. R-portkjøringen (blockmodeling 1.1.8, 50 starter) brukte blocks = nul/com/reg/rre fritt per blokk, som manus selv sier i l. 355–356. RESULTAT.md rettet nettopp dette 28.09: «i alle egne søk» (sto «i alle søk»); «Portkjøringen i R gjorde det ikke» | docs/saker/SAK-09b/RESULTAT.md (`0ff7a732`) | feil · **ny** |
| 422 | the five new attempts took about 5.5 hours of tool-assisted work in total, from 20 minutes (SAK-08) to 36 minutes (SAK-09b) by commit times | 5,5 t (19:10–00:39), SAK-08 ≈ 19–20 min og SAK-09b ≈ 36 min stemmer, men 36 min er ikke øvre grense: SAK-14 ≈ 2 t 10 min (19:10–21:20), SAK-11 ≈ 1 t 29 min (23:10–00:39), SAK-09c ≈ 55 min. Spennet er ≈ 20 min til ≈ 2 t | git log --date=iso --format='%h %ad %s' 59d4221^..704bbff -- docs/saker/ docs/PS-246-KRITERIUM.md docs/PS-246-RESULTAT.md docs/SAKBEHANDLING-2026-09-27-triage.md (`62c97e3e`) | feil |
| 430 | Where the class is liftable in principle, what stops the attempt is input we could not obtain — withheld under consent, not found where it would be expected, not reported. | Gjelder tre av seks (SAK-09c, SAK-08 på vilkår 1; SAK-11 på vilkår 2). PS-246, SAK-14 og SAK-09b — løftbar klasse — nådde vilkår 3 og stanset på terskel eller navngitt middel, ikke på inndata (ADR-0013: 2–1–3; FAKTA § 4 «I tre av fem»). Manus l. 384–387 sier det selv | docs/decisions/0013-opphevelse-definisjon.md + Vault: manuskript/faktasjekk-v2.2/FAKTA-acfd915.md § 4 (`867f3038`) | overclaim · **ny** |
| 432 | The claim that "some obstacles have since been lifted, some by AI" has no support in this material. | Står uendret (kartet bommet på linjeskiftet). PREREG-v1 § 1.2 ordrett: «En del av disse hindringene er i dag opphevet, en andel av dem av AI.» Anførselstegnene gjengir en egen oversettelse, som også avviker fra manus § 1 l. 57–58 («some fraction of the named obstacles have since been removed») | PREREG-v1.md (`05988b23`) | uklart |
| 441 | weakest at two non-hit boundaries (N3 0.530, N2 0.535), for which a decision rule now exists but is untested | «until» er rettet, og «untested» stemmer. Men regelen finnes bare for N3: REGEL-N3-v1 sier selv «N3 og N2 (κ 0,535) er de to klassene reglene ikke avgjør», og N2 har ingen regel | docs/REGEL-N3-v1.md (`96cd8372`) | uklart |
| 487 | the working history to 26 September 2026 is in the git bundles deposited with versions v0.1.0–v0.3.0 | v0.3.0 var deponert før 13:27 26.09 (dbd0bd1 «v0.3.0 deponert»). Resten av 26.09, bl.a. låsene av ADDENDUM-12–17 (15:43–21:32), ligger i ingen deponert bundle (ADDENDUM-12–25 er «nye» i v0.4.0). Med l. 500 («history after 26 September») faller ettermiddagen 26.09 mellom begge; skillet er v0.3.0, ikke datoen | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md § 1 og § 4 + docs/ZENODO.md + git log 2026-09-26 (dbd0bd1, 20f2c5e, 87df0e5) (`03aab10d`) | uklart · **ny** |
| 499 | whether it includes the candidate list and a bundle of the history after 26 September 2026 is undecided … and will be stated in the release notes | Bare historikkbundlen er et åpent valg (§ 4, § 8 pkt. 1 «Eierens valg om historikkbundlen»). At kandidatlista er uavgjort, står i ingen kilde; det forberedte v0.4.0-bygget (96 filer) har ikke register v2. At valget føres i release notes, har ingen kilde | docs/UTGIVELSE-v0.4.0-PORTSTATUS.md + Vault: zenodo/v0.4.0-bygg/UTGIVELSE-0.4.0.json (`03aab10d`) | uten kilde |
| 509 | This draft was written in a chat interface by a language model of the Fable 5.1 family | Ingen fil i repoet eller på Vault fører hvilken modell som skrev utkastet; Fable 5.1 er belagt bare som koder 4. INSTRUKSER-v1.3 gir chat-rollen «narrativ» uten modellnavn, og commitene som la inn v2–v2.2 (b07b9ee, 6392fad, 922cfb6) sier bare at fila er kopiert fra eierens skrivebord | docs/INSTRUKSER-v1.3.md (`ececde4b`) | uten kilde |

## Venter

| linje | manuskriptet sier | merknad |
|---|---|---|
| 165 | The first measured recall will come from phase 3 [pending]. | Venter: RESULTAT-ADDENDUM-25 «Status 28.09.2026: kjøringen pågår»; portene i ADDENDUM-25 § 5 er ikke målt. Fylles fra utfallsfila |
| 407 | ### 4.7 Phase 3 — prospective gate and first measured recall *[pending]* | Venter: «Status 28.09.2026: kjøringen pågår»; utfall «Ikke målt ennå». Plassholderen l. 409–413 fylles fra utfallsfila |
| 473 | Phase 3 supplies the first measured value *[pending]*. | Venter: RESULTAT-ADDENDUM-25 § 1 «Ikke målt ennå» |
| 519 | Haouachi 2016 (W2474595476, thesis; Crossref DOI to be inserted) | Plassholder. Kontrollert 28.09: fem DOI-er gir 302 og stemmer med Crossref (Riris 2018, 1 forf.; Bynum m.fl. 2021, 7 forf.; Karatas 2018; Mecking m.fl. 2017; Hansen m.fl. 2019). Haouachi har Crossref-DOI 10.70675/8513d3c9ze385z4b4bz910cz221c7718984d (302 → theses.fr/2016STRAC019); OpenAlex-utvalget har doi None |

## Utenfor manuskriptet, funnet underveis

* `docs/saker/SAK-11/LUKKET.md` fører seks forfattere; Crossref har sju. Manuskriptet sier riktig «seven».
