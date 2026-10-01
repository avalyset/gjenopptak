"""Referanseporten: silen og leseren startes ikke før referansesettet er komplett og sikret.

ADR-0014, datert tillegg 28.09.2026. ADDENDUM-25 § 3.5 sa «ingen del av kjeden kjøres før den raden
står i manifestet», men kjeden håndhevet det ikke: rekkefølgen i den første fase 3-kjøringen holdt
fordi kommandoene ble kjørt i riktig rekkefølge (nøkkel 10:20:02Z, manifestrad 10:20:05Z, kjede
10:20:33Z), ikke fordi noe nektet. En port som bare finnes i prosa, er ikke en port (LAERDOM § 31).

**Når porten gjelder.** Et materiale erklærer et referansesett ved at katalogen utvalgsfilen ligger i,
har ``referanse-verk.json``. Da gjelder porten for leddene i ``SPERRET`` og kan ikke slås av med et
flagg. Uten den fila finnes ikke noe referansesett å vente på, og porten svarer ``None``.

**Hva «komplett og sikret» er:**

1. hvert verk i ``referanse-verk.json`` står i ``referanse/tekster.json``;
2. hvert av dem har en treffil ``referanse/treff/<ref>.jsonl`` (tom er gyldig: null treff) og en
   brukslogg ``referanse/bruk/<ref>.json`` uten ``is_error``;
3. ``referanse/NOKKEL-referansesett.jsonl`` finnes, og **dens sha256 står i ``MANIFEST-VAULT.md``**.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

#: Leddene som ikke får starte før porten er bestått. ``hent`` og ``tekstbiter`` leser ingenting
#: som kan påvirke referanseleserne, og kan kjøres før.
SPERRET = ("dommer", "ekstraksjon", "union", "blind", "les", "verksniva", "falsify", "register")


class ReferansePortFeil(RuntimeError):
    pass


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sjekk(utvalg: Path, manifest: Path) -> dict | None:
    """``None`` hvis materialet ikke erklærer et referansesett. Ellers en oppsummering, eller
    ``ReferansePortFeil`` med alt som mangler."""
    rot = utvalg.parent
    erkl = rot / "referanse-verk.json"
    if not erkl.is_file():
        return None
    verk = json.loads(erkl.read_text(encoding="utf-8"))["verk"]
    mangler: list[str] = []
    tf = rot / "referanse" / "tekster.json"
    tekster = json.loads(tf.read_text(encoding="utf-8")) if tf.is_file() else []
    per_verk = {t["work_id"]: t["ref"] for t in tekster}
    for w in verk:
        ref = per_verk.get(w)
        if ref is None:
            mangler.append(f"{w}: ikke i referanse/tekster.json")
            continue
        if not (rot / "referanse" / "treff" / f"{ref}.jsonl").is_file():
            mangler.append(f"{ref} ({w}): treffil mangler")
        b = rot / "referanse" / "bruk" / f"{ref}.json"
        if not b.is_file():
            mangler.append(f"{ref} ({w}): brukslogg mangler")
        elif json.loads(b.read_text(encoding="utf-8")).get("is_error"):
            mangler.append(f"{ref} ({w}): økten endte med feil")
    nøkkel = rot / "referanse" / "NOKKEL-referansesett.jsonl"
    sha = None
    if not nøkkel.is_file():
        mangler.append("NOKKEL-referansesett.jsonl mangler")
    else:
        sha = _sha(nøkkel)
        if not manifest.is_file() or sha not in manifest.read_text(encoding="utf-8"):
            mangler.append(f"nøkkelens sha256 {sha[:16]}… står ikke i {manifest.name}")
    if mangler:
        raise ReferansePortFeil(
            f"referansesettet i {rot} er ikke komplett og sikret ({len(mangler)} mangler): "
            + "; ".join(mangler[:8]) + (" …" if len(mangler) > 8 else ""))
    return {"verk": len(verk), "nøkkel_sha256": sha, "rot": str(rot)}
