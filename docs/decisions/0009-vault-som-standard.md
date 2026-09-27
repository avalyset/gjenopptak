# ADR-0009 — Vault er standard for alt som skrives

**Status:** Accepted (2026-09-21)

## Bakgrunn

Systemdisken gikk full under portkjøringen. Ryddingen 2026-09-20 fjernet 1 085 MB fra `data/`,
og hver eneste fil som ble slettet, fantes alt på Vault — materialet var altså skrevet to ganger,
først til systemdisken og deretter sikret. Det er feil vei: en frossen rammeliste koster et
kvotedøgn, dommene over 22 243 passasjer kostet 24 timers inferens, og begge deler lå i
utgangspunktet på den disken som fylles først.

## Beslutning

1. **Alle skrivende moduler skriver til Vault.** `krev()` og `utkatalog()` i `vault.py` er eneste
   vei til en utdatakatalog. Systemdisken brukes bare til det som kan regenereres på minutter:
   `data/tmp-port`, `__pycache__`, og småting en kjøring selv lager om igjen.
2. **`require_vault()` ved start i hver av dem, ingen fallback.** Uten montert og skrivbart volum
   kastes `VaultUnavailable` før modulen gjør noe som helst. En katalog som er oppgitt eksplisitt,
   godtas bare når den ligger under Vault-roten — ellers ville kjøringen se ut som en sikring og
   likevel havne på systemdisken.
3. **Diskvakt med gulv.** `diskvakt()` stopper *før* disken fylles, ikke etter: er det mindre enn
   `GJENOPPTAK_DISK_GULV_GB` (standard 5 GB) igjen, startes ikke kjøringen. Gulvet gjelder
   systemdisken, siden logger, midlertidige filer og modelltilstand fortsatt lander der.
4. **Testene håndhever det.** `tests/test_vault_standard.py` kjører hver skrivende modul med
   `require_vault` slått av og krever at den nekter å starte.

## Endrede moduler

| modul | utdata før | utdata nå |
|---|---|---|
| `harvest/freeze.py` | `data/` | Vault-roten (`frames/`, `raw/`) |
| `harvest/draw.py` | `data/` | Vault-roten (`utvalg/`, `raw/`) |
| `harvest/fetchtest.py` | `data/` | Vault-roten |
| `harvest/smoketest.py` | `data/` | Vault-roten |
| `classify/l3poc_run.py` | `data/l3-poc` | `logs/l3-poc` på Vault |
| `classify/port_run.py` | `data/port`, `data/port-presisjonssett-*` | `logs/port` og `presisjonssett/` på Vault |

## Følger

* Kjøringer uten Vault stopper. Det er meningen: alternativet er at de lykkes og legger igjen
  materialet på feil disk.
* Store testfikstur leses fra Vault og hoppes over når volumet ikke er montert
  (`tests/test_recall.py`), i stedet for å ligge i 104 MB på systemdisken.
* `data/` beholder de fredede filene fra ryddingen (presisjonssett, tvil, passasjer, utvalg) som
  lokale arbeidskopier; de finnes også på Vault.
