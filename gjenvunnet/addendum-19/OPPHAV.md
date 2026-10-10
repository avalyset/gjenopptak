# Koden bak ADDENDUM-19 og ADDENDUM-20 — gjenvunnet fra øktutskriften

**Gjenvunnet 10.10.2026.** Skriptene som kjørte ADDENDUM-19, 19b og 20 lå i øktens scratchpad og ble aldri
committet. Scratchpad-katalogen finnes ikke lenger. Det som finnes, er øktutskriften, der hvert verktøykall
står ordrett.

## Hva som er ordrett, og hva som er regenerert

**`a19.py` og `a19b.py` ble aldri skrevet som tekst i utskriften.** De ble laget ved å kjøre en kort
Python-snutt på `a20.py`. Utskriften bærer `a20.py` ordrett og begge snuttene ordrett. Filene her er derfor av
to slag, og de holdes fra hverandre:

| fil | slag | kilde i utskriften |
|---|---|---|
| `a20.py` | **ordrett** | linje 12478, 2026-09-27T07:36:11Z — heredoc `cat > $SP/a20.py <<'PY'` |
| `analyse-a19-a20.py` | **ordrett** | linje 13346, 2026-09-27T11:26:20Z — heredoc til `.venv/bin/python -`; skrev `a19-a20-full-regelfil.json` |
| `analyse-a19b.py` | **ordrett** | linje 13559, 2026-09-27T12:50:56Z — heredoc til `.venv/bin/python -`; skrev `a19b-utfall.json` (κ = 0,636) |
| `avledning-a19.txt` | **ordrett** | linje 13278, 2026-09-27T10:50:39Z — hele kommandoen som laget `a19.py` av `a20.py` |
| `avledning-a19b.txt` | **ordrett** | linje 13433, 2026-09-27T12:24:05Z — hele kommandoen som laget `a19b.py` (og `a18_rekjor.py`) |
| `a19.py` | **regenerert** | snutten i `avledning-a19.txt` kjørt på `a20.py` |
| `a19b.py` | **regenerert** | snutten i `avledning-a19b.txt` kjørt på `a20.py` |

«Ordrett» betyr: tegn for tegn fra `input.command` i verktøykallet, JSON-dekodet. Heredocene er sitert
(`<<'PY'`), så skallet endret ingenting. «Regenerert» betyr: snutten leser `a20.py` og `ADDENDUM-19.md`,
erstatter docstring, katalognavn, addendumnavn, addendum-sha og (for 19b) `max_tokens`, og skriver resultatet.
Ingen linje er skrevet etter hukommelsen.

`a19b.py` er skriptet som ga den gyldige kjøringen og κ = 0,636. `a19.py` ga den ugyldige første kjøringen
(`max_tokens` 300, κ = 0,390).

## Autentisitetsgrunnlag

1. **Utskriften:** `~/.claude/projects/-Users-eirikbottennicolaysen-avalyset/1024847e-ef08-48fa-bd0a-2b2d9235bb89.jsonl`,
   48 483 717 B, sha256 `aecdf1aa80b023004d548067cf6b3a30a1b3a71fde11446e1cf592ae32dd6684`. Samme økt som koder 2s
   oppdrag ble gjenvunnet fra (`oppdrag-gjenvunnet/OPPHAV.md` på Vault). Kopi sikret på Vault:
   `oppdrag-gjenvunnet/utskrifter/okt-1024847e-ef08-48fa-bd0a-2b2d9235bb89.jsonl`, samme sha256.
2. **Lengden på `a19.py`:** snutten skrev ut `a19.py parser OK · 4473 B` da den ble kjørt 27.09. Den regenererte
   filen er 4 473 tegn. (Snutten telte tegn, ikke bytes; filen er 4 491 B.)
3. **Addendum-sha i `a19.py`:** `0dbd59cc…abbd`. Det er sha256 av `ADDENDUM-19.md` i commit `5e8bb6f`, og det er
   verdien som står i `signatur.addendum_sha256` i hver rad i `addendum-19/opus5-dommer.jsonl`.
4. **Addendum-sha i `a19b.py`:** `fb0410e3…0223`. Det er sha256 av `ADDENDUM-19.md` i commit `7a384c1`, og det er
   verdien som står i hver rad i `addendum-19/opus5-b-dommer.jsonl`, sammen med `max_tokens: 2000` og
   `addendum: "ADDENDUM-19b"`.
5. **`max_tokens`-linjene i `a19b.py`:** snutten skrev dem ut 27.09; de tre linjene er like i den regenererte filen.
6. **`a20.py`:** addendum-sha `8118dd54…489f` er sha256 av `ADDENDUM-20.md` slik den ble låst, og står i hver rad i
   `addendum-20/haiku45-dommer.jsonl`.

**Det som ikke er kontrollert:** `a19b.py` har ingen lengde i utskriften å måle mot, bare de tre linjene i pkt. 5
og signaturen i pkt. 4. Skriptene er ikke kjørt på nytt; de kaller et betalt API. At κ = 0,6356 følger av
`opus5-b-dommer.jsonl`, er vist uavhengig i `docs/REANALYSE-2026-10-03.md`.

`tests/test_gjenvunnet_a19.py` kjører avledningen på nytt og feiler om en fil her ikke lenger stemmer.

## sha256

| fil | bytes | sha256 |
|---|---|---|
| `a20.py` | 4 488 | `7f132d878306b24c2da8afe67167504d6258a088c1a609d574ebef1bc76448f3` |
| `a19.py` | 4 491 | `d5c572d83056ad13a28a35e6abb2e54b6ff5c3c30b48a9b7adde912e0a296bf5` |
| `a19b.py` | 4 405 | `82c610764f5bf3ae55e27b9467a446ab070c6c065e8c7352bb95944001b596f8` |
| `analyse-a19-a20.py` | 4 534 | `eaf967b91e87bd6648a18086ffb3eb62c5e908fb34fb560cb3881489127636d0` |
| `analyse-a19b.py` | 4 274 | `38429d739815576a34c80fb198a000ce26121887509992794dac065d5effaccb` |
| `avledning-a19.txt` | 1 694 | `8bb64873c8e83e15749e3a6019601a2b465365604b31a60f0bd4be8274630ab3` |
| `avledning-a19b.txt` | 5 286 | `2640921b7e283f11c886009806b48a6ff76d721500e4970d6bb4f3c2a4822fae` |

## Det som ikke er gjenvunnet

* **Første forsøk på `a19.py`** (linje 12911, 08:28Z) brukte `sed` og ga en fil med syntaksfeil; den kjørte aldri.
  Kommandoen står i utskriften og er ikke tatt med.
* **`a18_rekjor.py`** (de 13 avkuttede passasjene i ADDENDUM-18) står som strengliteral i `avledning-a19b.txt`, ikke
  som egen fil.
* **`kredittsjekk.py` og `ko.sh`** (køen som ventet på API-kreditt) er ikke tatt med. `ko2.sh` står som heredoc i
  `avledning-a19.txt`, ikke som egen fil.

## Merk ved lesing

Skriptene har absolutte stier til øktens scratchpad og til Vault, og `nokkel()` leser en API-nøkkel fra en lokal
fil ved navn. Ingen nøkkelverdi står i noen av filene. De er arkivmateriale, ikke kjørbar del av pakken.
