# Faktasjekk av MANUSKRIPT-v2.4-UTKAST — femte runde og kjent rest — 28.09.2026

**Manuskript:** `docs/MANUSKRIPT-v2.4-UTKAST.md`, sha256 `e18ea6ec30f3697dfc7ae51c98b386186072ac21b84902e797de6626d93ebd5d`.
**Fasit:** faktafila fra `acfd915` (sha256 `685d6ea0…`, frosset på Vault) og kildene. **Ingen prosa er omskrevet.**

**Dette er siste runde før ADDENDUM-25-utfallet** (eierens avgjørelse 28.09.2026). Det som står igjen under, er
**kjent rest** og kontrolleres ikke på nytt før fase 3 er målt; da leses de omskrevne avsnittene og § 4.7.

Kontrollert: de 32 linjene som er endret fra v2.3, og hver av de 8 radene fra v2.3-kontrollen
(`FAKTASJEKK-MANUSKRIPT-v2.3-2026-09-28.md`). Radfil på Vault: `manuskript/faktasjekk-v2.4/rest.jsonl`
(sha256 `4dfe573ade9e5e00…`). Ingen nettkall (ingen DOI i de endrede linjene).

## Løpet over fem runder

| runde | versjon | avvik inn | rettet | står | nye | avvik ut |
|---|---|---|---|---|---|---|
| 1 | v2 | — | — | — | — | 56 |
| 2 | v2.1 | 56 | 20 | 36 | 9 | 45 |
| 3 | v2.2 | 45 | 37 | 8 | 4 | 12 |
| 4 | v2.3 | 12 | 10 | 2 | 3 | 5 |
| 5 | v2.4 | 5 | 4 | 1 | 1 | **2** |

(Runde 4: av 16 rader var 12 avvik og 4 «venter»; 11 rettet, hvorav én var en venter-rad — plassholderen for
Haouachi-DOI-en.)

## Kjent rest

| linje | manuskriptet sier | riktig | kilde | status |
|---|---|---|---|---|
| 5 | tallene utenfor faktafila er merket med prosjektdokumentet de kommer fra — «the method document (METODE), … the case files, or the repository history» | lista er ikke uttømmende: merkene viser også til MASTER § 4 (l. 488), ZENODO.md (l. 153), TIDSSTEMPEL.md (l. 154), PREREG-v1-hodet (l. 15), bundlekatalogen (l. 150) og `koder4/eksponerte-rader.json` (l. 134) | kildemerkene i manus | uklart |
| 7 | «all of which are in the repository and the deposit» | gjeldende deponerte versjon er v0.3.0 (26.09), som mangler bl.a. saksfilene, ADDENDUM-11 § 8, LAERDOM § 35/§ 37, METODEs koder 4-note, REGEL-N3-v1, TIDSSTEMPEL og ADR-0013; v0.4.0 er ikke publisert. Historikken etter v0.3.0 (bl.a. `e92620b`) ligger i ingen deponert bundle. MASTER og `koder4/eksponerte-rader.json` finnes bare på Vault | `docs/UTGIVELSE-v0.4.0-PORTSTATUS.md`, Vault `zenodo/v0.4.0-bygg/UTGIVELSE-0.4.0.json` | **feil** (ny i v2.4) |

**Venter på ADDENDUM-25-utfall:** l. 173, 423 (§ 4.7) og 495.

**Observert utenfor mandatet** (uendret linje, ikke kontrollert som del av runden): l. 535–536 sier at utkastet er
revidert tre ganger (`136d025`, `b084ba2`, `faaaddc`), mens l. 3–4 nå nevner fire faktasjekker med `c4d645c` som
den fjerde.
