# Faktasjekk av MANUSKRIPT-v2.3-UTKAST — fjerde runde, bare endrede linjer — 28.09.2026

**Manuskript:** `docs/MANUSKRIPT-v2.3-UTKAST.md`, sha256 `a6c551ec8462acef0c8959834d987b40014edb42131ab72c5275d3c1e787d3be`.
**Fasit:** faktafila fra `acfd915` (sha256 `685d6ea0…`, frosset på Vault) og kildene. **Ingen prosa er omskrevet.**

Kontrollert: de 56 linjene som er endret fra v2.2 (18 blokker), og hver av de 16 radene fra v2.2-kontrollen
(`FAKTASJEKK-MANUSKRIPT-v2.2-2026-09-28.md`). Uendrede linjer er ikke kontrollert på nytt. Radfil på Vault:
`manuskript/faktasjekk-v2.3/rest.jsonl` (sha256 `2c8cc942a0050c4f…`). Nettkall bare til doi.org og api.crossref.org.

## Utfall

| | antall |
|---|---|
| rader fra v2.2 | 16 (12 avvik, 4 venter) |
| **riktig rettet i v2.3** | **11** |
| **fortsatt avvikende** | **2** (l. 6, l. 343) |
| **nye avvik i v2.3** | **3** (l. 5, 127, 442), alle i omskrevne linjer |
| venter på fase 3 | 3 |

## Resten

| linje | manuskriptet sier | riktig | kilde | status |
|---|---|---|---|---|
| 5 | taken from the source documents named in §7 (LAERDOM, ADR-0012/-0014, REGEL-N3-v1, METODE, the case files) | § 7 (l. 498–516) navngir verken METODE, REGEL-N3-v1, ADR-0012 eller ADR-0014, bare «decision records», «the lessons log» og «the case files». (source)-merkene viser dessuten til ADDENDUM-16, ADDENDUM-22 og «repository history», som ikke står i lista | docs/MANUSKRIPT-v2.3-UTKAST.md § 7 (`a6c551ec`) | uklart · **ny** |
| 6 | Numbers the fact file does not carry are taken from the source documents named in §7 … and are marked *(source)* where they first occur. | Delvis rettet: l. 95, 112, 127, 161, 171 og 260 er nå merket. Fortsatt umerket og ikke i FAKTA: Zenodo «25 September 2026» (l. 149; ZENODO.md), OTS «28 September 2026» (l. 150), «12 September 2026» (l. 14), `e92620b` med to filer (l. 146), eksponeringsfordelingen 1/4/2 (l. 131–133), «88 % and 32 %» (l. 479–480) | Vault: manuskript/faktasjekk-v2.2/FAKTA-acfd915.md + docs/ZENODO.md (8e726f64) (`685d6ea0`) | overclaim |
| 127 | its identity was established on three independent grounds *(source: LAERDOM §30)* | Feil kildemerke. «Tre uavhengige kontroller» (rekkefølge, forutsagt defekt, ordrett innhold) står i ADDENDUM-11 § 8. LAERDOM § 30 har ingen tre grunnlag for identiteten: «tre ting» der er gevinstene av gjenvinningen. REGELFIL-KODER2-GJENVUNNET fører fire. Tallet tre stemmer mot ADDENDUM-11 | ADDENDUM-11.md § 8 + docs/LAERDOM.md § 30 (f8fe0772) + docs/REGELFIL-KODER2-GJENVUNNET-2026-09-27.md (7cef264d) (`1b64d884`) | feil · **ny** |
| 343 | the case file records the retrieval step at 100 % under that rule, while the lessons log and ADR-0013 hold that … the case would not have been lifted | Kildenes posisjoner er feil gjengitt. RESULTAT.md l. 163–164 sier «saken ville stått som opphevet på 100 %», ikke bare hentesteget; LAERDOM § 35 sier det samme, og § 37 sier «porten ville ikke hatt noe svar». Bare ADR-0013 (vilkår 3, l. 46–47) sier «ikke opphevet» | docs/saker/SAK-14/RESULTAT.md + docs/LAERDOM.md § 35/§ 37 (f8fe0772) + docs/decisions/0013-opphevelse-definisjon.md (867f3038) (`cbb92c56`) | uklart |
| 442 | Of the six attempts in liftable classes, three stopped on input we could not obtain | Fem av seks var i løftbar klasse (H3/H5). SAK-09c var H1/H7-uavklart, og løftbarheten for uavklarte er «uavklart», ikke «ja» (ADDENDUM-05 § 3; REGISTER-SAKER; manus l. 221–222 holder uavklart utenfor løftbar andel) | ADDENDUM-05.md § 3 + docs/saker/REGISTER-SAKER.md (70e1ac9c) (`b12c85b2`) | feil · **ny** |

**Venter på ADDENDUM-25-utfall:** l. 168, 417, 487.
