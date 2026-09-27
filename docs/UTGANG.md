# Utgangen — én rad, forklart

`8-register.jsonl` har **én linje per bekreftet treff**. Hver linje bærer sin egen usikkerhet, så
tallet ikke kan leses uten forbeholdene som gjelder akkurat den raden. Skjemaet er
[`kandidat.schema.json`](../src/gjenopptak/schemas/kandidat.schema.json), og **hver rad valideres mot
det før den skrives** — en rad en utenforstående ikke kan lese, er ikke en leveranse.

## En ekte rad

```json
{
  "schema_version": "claims-2",
  "claim_id": "CLAIM-ROYK-00045",
  "candidate_id": "ROYK-00045",
  "doc_id": "W3217588367",
  "field_key": "arkeologi",
  "obstacle_class": "H2",
  "tvil": false,
  "loftbarhet": [
    {
      "vurdert_dato": "2026-09-27",
      "datopresisjon": "dag",
      "tabellversjon": "PREREG-v1-§5 + ADDENDUM-05",
      "obstacle_class": "H2",
      "loftbar": "ja"
    }
  ],
  "falsified": false,
  "cites_coverage": {
    "fulltext_available": null,
    "fulltext_total": 0,
    "coverage_ratio": null,
    "status": "målt",
    "kilde": "EPMC + Crossref"
  },
  "tested_at": "2026-09-27T15:56:44+00:00",
  "section_raw": "",
  "section_label_provenance": "parser",
  "unit": "sentence",
  "parser_version": "pdftotext/poppler",
  "parser_model_version": "pdftotext version 26.08.0",
  "passage_span": {
    "start_index": 3951,
    "end_index": 3955,
    "n_sentences": 5,
    "window": 2
  },
  "sil": {
    "kilde": "dommer",
    "presisjon": 0.143,
    "presisjon_ki": [
      0.128,
      0.16
    ],
    "presisjon_kilde": "ADDENDUM-22 §10; teller/nevner 124/359, 260/1814, 48/671",
    "ikke_prosa": false,
    "ikke_prosa_regel_sha256": "63ed734555a8bc95efd0d86c782805627032fdfeed7430635170ed6bff488aff"
  },
  "verksniva": {
    "materialtilgang": "DELVIS",
    "maskinlesbar": true,
    "eier": "ingen erklæring",
    "tilgang": "ikke nevnt",
    "forsok_mulig": true,
    "ser_ikke": "H8 utenfor verket — tilgangssituasjonen endrer seg utenfor materialet (ADR-0010)"
  },
  "leser": {
    "modell": "claude-opus-5",
    "regelfil_sha256": "234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449",
    "presisjon_ved_tvil": 0.976,
    "modus": "cli"
  },
  "notes": "Om folketribunat og pretur sto i linje 7 lar seg ikke avgjøre fordi steinen er brukket nettopp der, altså en skadet kilde."
}
```

## Hva hvert felt betyr

| felt | hva det sier | hvorfor det står der |
|---|---|---|
| `obstacle_class` | hindringsklassen, `H1`–`H9` eller `<klasse>/H7-uavklart` | fra PREREG-v1 § 5. **Avledes av en tabell, aldri av en modell** (ADR-0004) |
| `tvil` | leserens eget tvilsflagg | den enkeltopplysningen som forutsier presisjon best: **97,6 %** der den er `false`, **75,9 %** der den er `true` |
| `unit` | `sentence` eller `passage` | `sentence` når det ugjorte og hindringen står i **samme** setning (M1-streng), `passage` når de er spredt over ±2 (ADDENDUM-03 § 1.2) |
| `sil.kilde` | hvilket silledd fanget raden | `begge` = både dommeren og ekstraksjonen. Det er det presiseste leddet |
| `sil.presisjon` + `_ki` | **målt** presisjon for det leddet, med Wilson-intervall | begge 34,5 % [29,8–39,6] · dommer 14,3 % [12,8–16,0] · ekstraksjon 7,2 % [5,4–9,4]. Per **klasse** er presisjonen ikke målt; per kilde er den |
| `sil.ikke_prosa` | om tekstbiten er tall-, tabell- eller referanserester | **merket, aldri fjernet.** 18,1 % av dømt materiale er ikke prosa, men bare 2,5 % av treffene |
| `leser.modell` | hvem som avgjorde | agentisk Opus. Ett-kall-modeller er sil-klasse, ikke lesere (ADR-0012) |
| `leser.presisjon_ved_tvil` | presisjonen som gjelder **denne** radens tvilsverdi | ikke et gjennomsnitt: 0,976 eller 0,759 |
| `verksniva.materialtilgang` | `ÅPEN` / `DELVIS` / `LUKKET` for verkets eget materiale | kriteriet er låst før tallene, portert ordrett |
| `verksniva.ser_ikke` | **hva vurderingen ikke ser** | H8 utenfor verket: tilgangssituasjonen endrer seg utenfor materialet. Heron gikk fra H1 til H8 uten at teksten endret seg |
| `cites_coverage` | falsifiseringens dekningsgrad | `status: "ikke målt"` når den ikke er målt — **aldri 0**. Et umålt nulltall var én av ti grønn-og-feil-tilfeller |
| `loftbarhet` | vurdering **med dato** og tabellversjon | løftbarhet er ikke en egenskap ved teksten (ADR-0010). En vurdering uten dato er ubrukelig |
| `section_label_provenance` | `source` eller `parser` | `parser` betyr at seksjonsetiketten er parserens **gjetning**, ikke kildens merking (ADR-0007) |

## Headeren

```json
{
  "kjøring": "royk",
  "tid": "2026-09-27T15:56:45+00:00",
  "port": "ubekreftet kandidatliste",
  "bekreftet": false,
  "n_rader": 65,
  "n_dømt": 334,
  "forbehold": {
    "stabil_kjerne": "3 av 27",
    "n3_spredning": "5,8–13,6 % mellom kodere",
    "ikke_prosa": "merket, aldri fjernet"
  },
  "adr": "ADR-0012",
  "register_sha256": "0d1330a54475a718e8930610bda24cdad7e7bae23e5a306a69415316a596517c",
  "register_innhold_sha256": "854a890d4657be943298d04302c23b28549200a843865377db474fc7fdbec77c"
}
```

`port` sier hvilken port lista har bestått. **Uten en bestått port står det `ubekreftet
kandidatliste`, og det er ikke en feil** — en arbeidsliste kan bare komme fra en **prospektiv** port
på nytt materiale. `forbehold` er de globale, og de følger lista uansett hvilken rad man leser:

* **`stabil_kjerne: "3 av 27"`** — bare tre av fasitens 27 treff har enighet mellom to kodere *og*
  ingen tvil hos noen av dem. En terskel nær referansesettets ytterkant måler settet, ikke leseren.
* **`n3_spredning: "5,8–13,6 % mellom kodere"`** — grensen mellom `N3` og ikke-treff bærer
  koderidentitet. Åtte uavhengige kodere på tilfeldig delt materiale spredte seg over det spennet.
* **`ikke_prosa: "merket, aldri fjernet"`** — nevneren er materialet slik porten så det.

`register_innhold_sha256` er sha256 uten de daterte feltene. Det er den sha-en en røyktest kan
bruke; `register_sha256` endrer seg for hver kjøring fordi `tested_at` gjør det.
