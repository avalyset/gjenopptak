"""ADR-0009: hver skrivende modul nekter å starte uten Vault, og diskvakten har et gulv."""

import pytest

from gjenopptak import vault as V
from gjenopptak.classify import l3poc_run, port_run
from gjenopptak.harvest import draw, fetchtest, freeze, smoketest

SKRIVENDE = [
    ("freeze", freeze, ["--field", "energimodellering"]),
    ("draw", draw, ["--field", "energimodellering"]),
    ("fetchtest", fetchtest, ["--field", "energimodellering"]),
    ("smoketest", smoketest, ["--field", "energimodellering"]),
    ("l3poc_run", l3poc_run, ["mål"]),
    ("port_run", port_run, ["mål"]),
]


@pytest.mark.parametrize("navn,modul,argv", SKRIVENDE, ids=[s[0] for s in SKRIVENDE])
def test_nekter_aa_starte_uten_vault(navn, modul, argv, monkeypatch):
    def nei(*a, **kw):
        raise V.VaultUnavailable("volumet er ikke montert")
    monkeypatch.setattr(V, "require_vault", nei)
    monkeypatch.setattr(modul, "krev", lambda *a, **kw: nei())
    if hasattr(modul, "utkatalog"):
        monkeypatch.setattr(modul, "utkatalog", lambda *a, **kw: nei())
    with pytest.raises(V.VaultUnavailable):
        modul.main(argv)


def test_diskvakten_stopper_foer_disken_fylles(tmp_path):
    with pytest.raises(V.DiskFull):
        V.diskvakt(tmp_path, gulv=10_000_000.0)
    assert V.diskvakt(tmp_path, gulv=0.0) > 0


def test_krev_avviser_katalog_utenfor_vault(tmp_path, monkeypatch):
    monkeypatch.setattr(V, "require_vault", lambda *a, **kw: tmp_path / "vault")
    monkeypatch.setattr(V, "VAULT_ROOT", tmp_path / "vault")
    monkeypatch.setattr(V, "diskvakt", lambda *a, **kw: 999.0)
    assert V.krev(tmp_path / "vault" / "raw").name == "raw"
    with pytest.raises(V.VaultUnavailable):
        V.krev(tmp_path / "systemdisk")
