# INNHENTET 2026-10-10 — «differansen 0,812 − 0,636 er ikke statistisk etablert»

**De låste og publiserte filene under er uendret.** De sier at forskjellen mellom Opus i én sammenhengende økt
(κ = 0,812) og Opus i ett kall per passasje (κ = 0,636) ikke er statistisk etablert, og at øktformens bidrag
er «mulig og umålt». Det var slutningen som lot seg trekke 27.09.2026 fra to separate intervaller som overlappet.
Den er **innhentet** av den parede testen i reanalysen 03.10.2026. Utsagnene rettes ikke i filene; de føres her
(samme regel som `INNHENTET-2026-09-26-en-koder.md`).

## 1 Hva som gjelder

**Differansen er 0,177, paret passasjebootstrap [0,044–0,323], paret verksklynget bootstrap [0,057–0,318].**
0,177 er regnet av de uavrundede κ-verdiene (0,8124 og 0,6356); ADDENDUM-19 § 7.2 oppga 0,176 av de avrundede.
Begge intervallene utelukker 0 (andel replikater ≤ 0: 0,42 % og 0,31 %). 10 000 replikater, frø 734248, begge
κ mot koder 1 på de samme 320 passasjene. Kilde: `docs/REANALYSE-2026-10-03.md` b), tall i
`revisjon-2026-10/reanalyse.json` på Vault (`differanse_koder2_minus_opus`), kode
`src/gjenopptak/classify/reanalyse_fagfelle.py`.

Feilen i den gamle slutningen var metoden, ikke tallene: to intervaller som overlapper, viser ikke at differansen
kan være null når de to målingene er gjort på de samme passasjene. Den parede testen er den som gjelder.

**Det differansen ikke viser:** den er målt mellom én økt (koder 2, kjørt én gang) og 320 enkeltkall, med samme
modell og samme regelfil. Om økten gjentatt ville gitt 0,812 igjen, er ikke målt — ADDENDUM-21 arm A er
preregistrert og ukjørt.

## 2 Utsagn som er innhentet

| fil | linje | står | status |
|---|---|---|---|
| `ADDENDUM-19.md` (låst) | 196–200 | «Men differansen mot koder 2 er ikke statistisk etablert … en eventuell resteffekt av øktformen er mulig og umålt.» | innhentet 03.10.2026. Klassifiseringen i § 4 (båndet 0,30–0,70) står. |
| `ADDENDUM-24.md` (låst) | 15–17 | gjengir ADDENDUM-19: resteffekten av øktformen er «mulig og umålt» | innhentet 03.10.2026. Kriteriet og utfallet i ADDENDUM-24 berøres ikke. |
| `docs/INSTRUKSER-v1.3.md` (publisert i GitHub-utgivelsen v0.4.1) | 325–326 | «Differansen 0,636 mot 0,812 er **ikke** statistisk etablert … øktformens bidrag er ikke påvist.» | innhentet 03.10.2026. Rettet i INSTRUKSER v1.4. |
| `docs/INSTRUKSER-v1.3.md` | 323–324 | leserstigen «samme regelfil, ett kall»: «Sonnet 0,297» | **feil tall for denne raden.** Med koder 2s fulle regelfil er Sonnet 5 **0,294** [0,126–0,455], n = 319 (ADDENDUM-19 § 7.1; `ekstraksjon/2026-09-26/a19-a20-full-regelfil.json`). 0,297 er Sonnet med det tynne utdraget (ADDENDUM-18 § 9). Rettet i INSTRUKSER v1.4. |
| `docs/MANUSKRIPT-v2.9.md` og `docs/PREPRINT-v2.md` / `PREPRINT-v2.pdf` | 278 og 514 / 272 og 505 | «The difference between 0.636 and 0.812 is **not statistically established**» og «a difference that is not statistically established here» | innhentet 03.10.2026; rettet i manuskript v3.1 og senere («The paired difference, 0.177, has a work-clustered interval of 0.057–0.318», `docs/MANUSKRIPT-v3.3.md` linje 243). |

`docs/LAERDOM.md` § 42 (linje 880) siterer «mulig og umålt» i en datert rettelse fra 28.09.2026; den er en logg og
rettes ikke, og § 50 fører det nye tallet. `ADDENDUM-28.md` § 2 pkt. 1 siterer begge deler og er ikke innhentet.

**Rettet i filene selv 10.10.2026**, fordi de er levende dokumenter og ikke låst: `docs/METODE.md` (avsnittet etter
leserstigen) og `docs/MANUSKRIPT-FAKTA-2026-09-28.md` (avsnittet etter leserstigen), begge med datert merknad om
hva som sto.

## 3 Beslektet, og ført fra før

Tersklene i `ADDENDUM-21.md` § 5 («innenfor 0,712–0,917», «≥ 0,70 men under 0,712») er satt på intervallet til
κ = 0,826, ikke til 0,812 [0,697–0,906]. Det står i `docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md` § A, sammen med
samme avskriftsfeil i ADDENDUM-19 linje 116, 184 og 196–197. Koder 3 er ukjørt, så ingen klassifisering er gjort
på de tersklene.

## 4 Zenodo

Versjonene til og med v0.5.0 (10.5281/zenodo.23120143) bærer `ADDENDUM-19.md`, `ADDENDUM-24.md`, `METODE.md` og
`MANUSKRIPT-FAKTA-2026-09-28.md` med de innhentede utsagnene; v0.4.1 bærer i tillegg `MANUSKRIPT-v2.9.md`.
`PREPRINT-v2.pdf` ligger i v0.4.1, v0.5.0 og v0.6.0 og bærer utsagnet i alle tre. **En deponert fil endres ikke.**
Denne fila er rettelsen ved siden av. Den deponeres første gang i v0.6.0, der `METODE.md` og faktafila også er rettet.
