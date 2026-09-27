# ADDENDUM-17 — test 2′: samme ekstraksjon på deduplisert tekst

**Skrevet:** 2026-09-26, **før** kjøringen og **før** resultatet av test 2 (ADDENDUM-16) var målt.
**Utløst av en terskel låst før 2d:** duplikatraten i den sammensatte teksten overstiger 10 %.

## 1 Hvorfor 2′ finnes

Teksten som test 2 leser, er satt sammen fra tekstbit-filene ved overlappkirurgi: for hver etterfølgende
tekstbit beholdes bare halen som ikke alt står i teksten. Tekstbit-filene dekker **hver setning i hvert
verk** — 66 833 dekkede setningsindekser mot 66 833 i `data/port/spesifikasjon.json`, for alle 100 verk —
så sammensetningen mister ingenting.

Den fjerner likevel ikke gjentakelser som står i **verket selv**. Målt på den sammensatte teksten
(`ekstraksjon/2026-09-26/b1-duplikatrate.json`):

| måling | fragmenter | unike | dupliserte |
|---|---|---|---|
| **A — alle regex-fragmenter** | 65 146 | 56 731 | **12,92 %** (31 av 100 verk over 10 %) |
| B — bare fragmenter med ≥ 3 ord | 50 004 | 48 523 | 2,96 % (3 av 100 verk over 10 %) |

Forskjellen er tegnsettingsrester: punktledere i innholdsfortegnelser og sidetall. Verste verk,
W2811446991, har fragmentet «.» **1 622 ganger**.

**Den låste terskelen sier «> 10 % dupliserte setninger i sammensatt tekst», ikke «prosasetninger».
Måling A gjelder, og 12,92 % > 10 %. 2′ preregistreres derfor**, selv om måling B viser at den reelle
prosagjentakelsen er lav. At det låste kriteriet slår til på et grunnlag som er svakere enn det ser ut,
står her framfor å bli tolket bort.

## 2 Hva som er likt, og hva som er det eneste som endres

| | |
|---|---|
| prompt | **uendret**: `prompts/ekstraksjon-v1.txt`, sha256 `c8c276df9ffe62c906db566c24abcf6f415746a8271f737928f426f94dbeb534` |
| modell · temp · frø · num_ctx | **uendret**: gemma2:9b (vekt `ff1d1fc7…0373`), 0, 734248, 8192 |
| vindusregel | **uendret**: ca. 3 000 tokens, overlapp 200, kuttet på setningsgrense |
| matchdefinisjon | **uendret**, ADDENDUM-16 § 5 |
| dødsbetingelser | **uendret**, ADDENDUM-16 § 6 |
| **det eneste som endres** | **teksten dedupliseres før vinduene bygges**: identiske fragmenter etter NFC-normalisering og samlet mellomrom beholdes bare ved første forekomst, i rekkefølge |

## 3 Rekkefølge og rapportering

2′ **kjøres etter** at 2d er målt, slik at 2 ikke kan påvirkes av 2′ og omvendt.
**Begge rapporteres, ved siden av hverandre, aldri i stedet for hverandre.** Det gjelder også hvis 2′
gir bedre tall: 2 er resultatet av den preregistrerte testen, 2′ er resultatet av en test med én endret
inndatabehandling.

## 4 Hva 2′ kan vise, og hva den ikke kan

**Kan vise:** om dupliserte fragmenter kostet tid uten å gi treff — altså om samme recall oppnås med
færre vinduer og lavere veggtid.

**Kan ikke vise:** om dedupliseringen er *riktig*. Et fragment som står to ganger i et verk, kan stå to
ganger med mening (en gjentatt tabelltittel over to sider er støy; en gjentatt konklusjonssetning i
sammendrag og konklusjon er ikke). Dedupliseringen beholder første forekomst og er dermed blind for
hvilken av dem som hadde konteksten.

**Grensen på matchdefinisjonen:** et fasit-treff som bare finnes i en dublett som ble fjernet, kan
fortsatt gjenfinnes, fordi første forekomst beholdes. Men rekkefølgen i vinduene endres, og et treff kan
havne i et annet vindu enn i test 2. Det er en reell forskjell mellom testene, ikke en feil i noen av dem.

## Utfall 2026-09-27 — 2′ gir ingen bedring, og terskelen som utløste den målte feil ting

Kjørt ferdig: **585 vinduer, 9 tekniske feil, 219,1 min** dommertid. Tall i
`ekstraksjon/2026-09-26/a17-2p-mot-2d.json`. Begge står ved siden av hverandre, som §3 krever; **2d er
resultatet av den preregistrerte testen.**

| | 2d (ADDENDUM-16) | 2′ (ADDENDUM-17) | endring |
|---|---|---|---|
| vinduer | 595 | 585 | −10 |
| Q-linjer | 884 | 867 | **−17** |
| unike Q-linjer | 882 | 863 | −19 |
| passasjer truffet | 1 030 | 987 | **−43** |
| Q-linjer uten passasjetreff | 99 | 109 | +10 |
| **de 27 kjente dekket** | **11** | **9** | **−2** |
| tokens inn | 2 019 953 | 1 972 893 | −47 060 |
| dommertid | 206,9 min | 208,8 min | +1,9 |

**2′ er dårligere på hver akse som betyr noe.** Den finner færre Q-linjer, treffer færre passasjer, mister
to av de kjente treffene, og sparer 2,3 % tokens mot 1 % mer veggtid. Ingen bedring å veie mot noe.

**Og terskelen som utløste 2′, målte feil størrelse.** §1 førte 12,92 % duplisering på *alle*
regex-fragmenter, mot 2,96 % på fragmenter med ≥ 3 ord. Målt nå på det som faktisk er utdataet —
**Q-linjene selv er 0,2 % dupliserte i 2d.** Det var ingenting å fjerne. Dedupliseringen kortet teksten og
tok med seg innhold ekstraksjonen ville brukt: tre vinduer forsvant, og med dem to kjente treff.

**Slutningen står uendret:** duplisering i den sammensatte teksten er ikke en feilkilde i ekstraksjonens
utdata. Terskelen var satt på et mål (fragmentduplisering) som ikke er årsakskjeden til det man var redd
for (dupliserte Q-linjer). **En terskel skal settes på den størrelsen den skal beskytte**, ikke på en
nabostørrelse som er lettere å regne. 2′ preregistrerte og kjørte likevel, og det var riktig — nå er det
målt og ikke antatt.
