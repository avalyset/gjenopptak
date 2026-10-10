# INNHENTET 2026-10-10 — «ekstern fagfellevurdering 03.10.2026» var en vurdering gjort av en språkmodell

**De låste og publiserte filene under er uendret.** De omtaler vurderingen av manuskript v2.9 den 03.10.2026 som
«ekstern fagfellevurdering», «the review» og «the reviewer», uten å si hvem som leste. **Leseren var en
språkmodell (GPT). Ingen menneskelig fagfelle har lest manuskriptet.** Ordet
«fagfellevurdering» gir inntrykk av noe annet, og det rettes ikke i låste filer; det føres her.

## 1 Hva som gjelder

* **Hva vurderingen var:** én lesning av manuskript v2.9 gjort av en språkmodell (GPT) 03.10.2026. Instruksen ba
  modellen opptre som uavhengig fagfelle for *Scientometrics* og ga den manuskriptet som PDF og lenkene til det
  offentlige depositumet og repoet. Rapporten anbefalte «major revision». Rapporten og instruksen ligger på Vault,
  `fagfellevurdering/gpt-2026-10-03/`, med sha256 i `MANIFEST-VAULT.md`. De deponeres ikke.
* **Hva den førte til:** reanalysen med verket som klyngeenhet (`REANALYSE-2026-10-03.md`), den parede testen av
  differansen 0,812 − 0,636, caseutvalget som skjønn (`CASEUTVALG-2026-10-03.md`), ADDENDUM-27 og manuskript v3.1.
  Rettelsene står. Det er kilden som er feil benevnt.
* **Hva som ikke finnes:** ingen fagfellevurdering fra et tidsskrift. Manuskript v3.3 ble sendt til *Scientometrics*
  03.10.2026; repoet fører per 10.10.2026 ingen redaktør- eller fagfellerapport derfra.
* **Alle koderne i studien er også språkmodeller.** Vurderingen 03.10.2026 er dermed ikke en menneskelig kontroll
  av noe ledd; den menneskelige valideringen er preregistrert i ADDENDUM-27 og ikke kjørt.

## 2 Utsagn som er innhentet

| fil | linje | står | status |
|---|---|---|---|
| `ADDENDUM-27.md` (låst 03.10.2026) | 4 | «**Gjelder:** ekstern fagfellevurdering 03.10.2026, hovedinnvending 1 …» | innhentet: vurderingen var gjort av en språkmodell. Preregistreringen berøres ikke |
| `ADDENDUM-28.md` (låst 10.10.2026) | 5 | «… og ekstern fagfellevurdering 03.10.2026, hovedinnvending 1.» | samme. Preregistreringen berøres ikke |
| `RELEASE-NOTES-v0.5.0.md` (publisert i v0.5.0; i `utgivelser-tidligere.zip`) | 3 | «Revisjon etter ekstern fagfellevurdering 03.10.2026.» | innhentet |
| `SVARBREV-v3.1.md` (publisert i v0.5.0; i `manuskript-tidligere.zip`) | 1, 7 | «Response to the review» … «We thank the reviewer for a detailed and accurate report.» | innhentet: «the reviewer» er en språkmodell |
| `src/gjenopptak/classify/reanalyse_fagfelle.py` (låst med sha256 i ADDENDUM-28) | 1, 402, 485 | modulnavnet, docstringen og de to overskriftene skriptet skriver («Reanalyse etter ekstern fagfellevurdering», «Revisjon etter ekstern fagfellevurdering») | innhentet. Koden endres ikke; overskriften i `MANUSKRIPT-FAKTA-2026-09-28.md` § 10 står fordi skriptet finner seksjonen på den |

## 3 Rettet i filer som ikke er låst (10.10.2026)

`CASEUTVALG-2026-10-03.md`, `REANALYSE-2026-10-03.md`, `REVISJON-2026-10-03-REFERANSER.md`, `LAERDOM.md` § 50,
`ZENODO.md` og `MANUSKRIPT-FAKTA-2026-09-28.md` § 10 (presisering under overskriften). Hvert sted har en datert
merknad som sier hva som sto. `README.md` sa det riktig fra før: «an external review by a language model».

## 4 Regelen framover

En lesning gjort av en språkmodell kalles «ekstern vurdering gjort av en språkmodell», ikke fagfellevurdering.
«Fagfellevurdering» brukes bare om en vurdering fra et tidsskrift eller en navngitt menneskelig leser.
