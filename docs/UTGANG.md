# Utgangen — én rad, forklart

`8-register.jsonl` har **én linje per treff leseren meldte**; bekreftelsen er målt på et blindutvalg
(presisjonsporten), ikke per rad. *(Rettet 30.09.2026, frys-lesning 4: sto «én linje per bekreftet treff».)* Hver linje bærer sin egen usikkerhet, så
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

**Kjent feil i eksempelraden, ført 28.09.2026 (frys-lesningen).** `cites_coverage` sier `status: "målt"`
med `fulltext_total: 0` og `fulltext_available: null`. Nullen er Crossrefs antall siterende arbeider, men
dekningen er ikke målt (`fulltext_available` er tom, og 0/0 er udefinert) — det er nettopp det umålte
nulltallet regelen under forbyr. Skriveren i kjedens ledd 7c (`_dekning` i `src/gjenopptak/kjede/ledd.py`)
gjør fortsatt dette når en DOI har null siterende, og `royk/8-register.jsonl` på Vault bærer samme
verdier. **Omfanget er større enn det:** skriveren setter `status: "målt"` når bare totalen er målt, også når
`fulltext_available` er tom — i fase 3-registeret gjelder det **538 av 673 rader** (491 med `fulltext_total` over
null, 47 med null). «målt» betyr der at antallet siterende er målt, ikke dekningen. *(Rettet 30.09.2026, frys-lesning 4.)*
 LAERDOM § 36 rettet bare `kandidat432`. **Rettelsen av skriveren og en ny røykkjøring står
igjen** og er ikke gjort her. Eksempelraden er beholdt som kjeden skriver den.

## Hva hvert felt betyr

| felt | hva det sier | hvorfor det står der |
|---|---|---|
| `obstacle_class` | hindringsklassen, `H1`–`H9` eller `<klasse>/H7-uavklart` | fra PREREG-v1 § 5. **Avledes av en tabell, aldri av en modell** (ADR-0004) |
| `tvil` | leserens eget tvilsflagg | skiller presisjonen sterkt i en post hoc delgruppe (ADDENDUM-23 § 7.2): **97,6 %** [87,7–99,6] der den er `false`, **75,9 %** [63,5–85,0] der den er `true`; andre prediktorer er ikke sammenlignet, og forskjellen er ikke testet *(rettet 28.09.2026: sto «den enkeltopplysningen som forutsier presisjon best»)* |
| `unit` | `sentence` eller `passage` | `sentence` når det ugjorte og hindringen står i **samme** setning (M1-streng), `passage` når de er spredt over ±2 (ADDENDUM-03 § 1.2) |
| `sil.kilde` | hvilket silledd fanget raden | `begge` = både dommeren og ekstraksjonen. Det er det presiseste leddet |
| `sil.presisjon` + `_ki` | **målt** presisjon for det leddet, med Wilson-intervall | begge 34,5 % [29,8–39,6] · dommer 14,3 % [12,8–16,0] · ekstraksjon 7,2 % [5,4–9,4]. Per **klasse** er presisjonen ikke målt; per kilde er den |
| `sil.ikke_prosa` | om tekstbiten er tall-, tabell- eller referanserester | **merket, aldri fjernet.** 18,1 % av dømt materiale er ikke prosa, men bare 2,5 % av treffene |
| `leser.modell` | hvem som avgjorde | agentisk Opus. Ett-kall-modeller er sil-klasse, ikke lesere (ADR-0012) |
| `leser.presisjon_ved_tvil` | presisjonen som gjelder **denne** radens tvilsverdi | ikke et gjennomsnitt: 0,976 eller 0,759 — konstantene i `kjede.toml`, målt i den post hoc porten (ADDENDUM-23 § 7.2), og de står også på fase 3-radene. Fase 3s egen, prospektive måling er **97,4 %** og **77,4 %** (`docs/RESULTAT-ADDENDUM-25.md` § 1.1) *(Rettet 30.09.2026, frys-lesning 4.)* |
| `verksniva.materialtilgang` | `ÅPEN` / `DELVIS` / `LUKKET` for verkets eget materiale | kriteriet er låst før tallene, portert ordrett |
| `verksniva.ser_ikke` | **hva vurderingen ikke ser** | H8 utenfor verket: tilgangssituasjonen endrer seg utenfor materialet. Heron gikk fra H1 til H8 uten at teksten endret seg |
| `cites_coverage` | falsifiseringens dekningsgrad | `status: "ikke målt"` når den ikke er målt — **aldri 0**. Et umålt nulltall var én av ti grønn-og-feil-tilfeller |
| `loftbarhet` | vurdering **med dato** og tabellversjon | løftbarhet er ikke en egenskap ved teksten (ADR-0010). En vurdering uten dato er ubrukelig |
| `section_label_provenance` | `source` eller `parser` | `parser` betyr at seksjonsetiketten er parserens **gjetning**, ikke kildens merking (ADR-0007) |

## Headeren

Hodet fra fase 3-kjøringen (`fase3-kjede`, 30.09.2026), ordrett:

```json
{
 "kjøring": "fase3-kjede",
 "tid": "2026-09-30T17:43:55+00:00",
 "port": "arbeidsliste (prospektiv port)",
 "bekreftet": true,
 "n_rader": 673,
 "n_dømt": 4107,
 "forbehold": {
  "stabil_kjerne": "3 av 27",
  "n3_spredning": "5,8–13,6 % mellom kodere",
  "ikke_prosa": "merket, aldri fjernet",
  "leser_datert": "datert 30.09.2026, claude-opus-5, regelfil 234695dd4e1777a9; lesningen er ikke gjentakbar (METODE §9)",
  "silrecall": "ikke målt",
  "verksnivaa": "n_doemte_treff, n_loftbare og klasser i 7b-verksniva.jsonl teller silens flagg (dommeren, 3-dommer.jsonl), ikke leserens verdikter; materialtilgang, eier, tilgang og forsok_mulig gjelder verket"
 },
 "adr": "ADR-0012",
 "register_sha256": "b7d9230c93970c2614a8c4c6b26f3d6dfa94ad4e81ec0883e8924ae9e0e919be",
 "register_innhold_sha256": "f590f25afcd33ab79cd43cd8056513fd15c5a2cd22dbf0da6ef1db77dabac4ae",
 "navnepolicy": "verk, ikke person"
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
* **`leser_datert`** — leseren er datert: dato, modell og regelfil. En agentisk økt kan ikke spilles av på
  nytt, så samme kommando gir ikke nødvendigvis samme register (METODE § 9).
* **`silrecall: "ikke målt"`** — skjemaet tillater bare den verdien. For fase 3 er recall likevel målt mot et
  referansesett lest før silen (95 av 104 beholdt, `docs/RESULTAT-ADDENDUM-25.md` § 1.2); tallet står der, ikke
  i hodet, til skjemaet eventuelt endres.
* **`verksnivaa`** — **verksnivåets tellinger er silens, ikke leserens.** `n_doemte_treff`, `n_loftbare` og
  `klasser` i `7b-verksniva.jsonl` teller dommerens flagg fra `3-dommer.jsonl`, ikke leserens verdikter. En
  linje med `n_doemte_treff: 12` sier altså at silen flagget tolv tekstbiter i verket, ikke at leseren bekreftet
  tolv. Registerradens `verksniva` bærer bare det som gjelder verket — materialtilgang, eier, tilgang,
  `forsok_mulig` — og ingen av tellingene.

`navnepolicy: "verk, ikke person"` er påkrevd: en rad viser til et verk ved `doc_id`, og vurderinger i prosa
adresseres til verket, aldri til forfatteren.

*(Rettet 30.09.2026: eksempelet var hodet fra røyktesten 27.09 med tre forbehold, som ikke består dagens skjema
og ikke svarer til noen deponert fil; forklaringene av `leser_datert`, `silrecall`, `verksnivaa` og
`navnepolicy` manglet.)*

`register_innhold_sha256` er sha256 uten de daterte feltene. Det er den sha-en en røyktest kan
bruke; `register_sha256` endrer seg for hver kjøring fordi `tested_at` gjør det.
