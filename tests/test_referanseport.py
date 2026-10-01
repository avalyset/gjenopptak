"""Referanseporten (ADR-0014, tillegg 28.09.2026): nekter sil og leser før referansesettet er
komplett og nøkkelens sha står i manifestet. Testene prøver hvert tilfelle den skal feile på."""
import hashlib
import json

import pytest

from gjenopptak.kjede.referanseport import ReferansePortFeil, SPERRET, sjekk


def _materiale(tmp_path, *, verk=("W1", "W2"), treff=("R01", "R02"), bruk=("R01", "R02"),
               feil=(), nøkkel=True, i_manifest=True):
    rot = tmp_path / "fase3"
    (rot / "referanse" / "treff").mkdir(parents=True)
    (rot / "referanse" / "bruk").mkdir(parents=True)
    utvalg = rot / "utvalg.jsonl"
    utvalg.write_text("")
    (rot / "referanse-verk.json").write_text(json.dumps({"verk": list(verk)}))
    (rot / "referanse" / "tekster.json").write_text(json.dumps(
        [{"ref": f"R{i:02d}", "work_id": w} for i, w in enumerate(verk, 1)]))
    for r in treff:
        (rot / "referanse" / "treff" / f"{r}.jsonl").write_text("")
    for r in bruk:
        (rot / "referanse" / "bruk" / f"{r}.json").write_text(json.dumps({"is_error": r in feil}))
    manifest = tmp_path / "MANIFEST-VAULT.md"
    manifest.write_text("# manifest\n")
    if nøkkel:
        n = rot / "referanse" / "NOKKEL-referansesett.jsonl"
        n.write_text('{"work_id": "W1", "setninger": [3, 4]}\n')
        if i_manifest:
            manifest.write_text(f"| fase3/referanse/{n.name} | 1 | {hashlib.sha256(n.read_bytes()).hexdigest()} |\n")
    return utvalg, manifest


def test_uten_erklært_referansesett_gjelder_ikke_porten(tmp_path):
    u = tmp_path / "utvalg.jsonl"
    u.write_text("")
    assert sjekk(u, tmp_path / "MANIFEST-VAULT.md") is None


def test_komplett_og_sikret_slipper(tmp_path):
    u, m = _materiale(tmp_path)
    r = sjekk(u, m)
    assert r["verk"] == 2 and len(r["nøkkel_sha256"]) == 64


@pytest.mark.parametrize("avvik,forventet", [
    ({"treff": ("R01",)}, "R02 (W2): treffil mangler"),
    ({"bruk": ("R01",)}, "R02 (W2): brukslogg mangler"),
    ({"feil": ("R02",)}, "R02 (W2): økten endte med feil"),
    ({"nøkkel": False}, "NOKKEL-referansesett.jsonl mangler"),
    ({"i_manifest": False}, "står ikke i MANIFEST-VAULT.md"),
])
def test_ufullstendig_eller_usikret_nekter(tmp_path, avvik, forventet):
    u, m = _materiale(tmp_path, **avvik)
    with pytest.raises(ReferansePortFeil, match=forventet.replace("(", r"\(").replace(")", r"\)")):
        sjekk(u, m)


def test_endret_nøkkel_etter_sikring_nekter(tmp_path):
    # Nøkkelen redigeres aldri etter at raden står i manifestet (ADDENDUM-25 § 8).
    u, m = _materiale(tmp_path)
    (u.parent / "referanse" / "NOKKEL-referansesett.jsonl").write_text('{"work_id": "W1", "setninger": [9]}\n')
    with pytest.raises(ReferansePortFeil, match="står ikke i"):
        sjekk(u, m)


def test_sil_og_leser_er_sperret_hent_er_ikke():
    assert {"dommer", "ekstraksjon", "union", "les"} <= set(SPERRET)
    assert "hent" not in SPERRET and "tekstbiter" not in SPERRET
