"""Stemplingen skal være idempotent, og den skal aldri kunne stoppe en lås."""
from pathlib import Path

from gjenopptak import tidsstempel as T


def test_fire_kalendere_og_terskel_er_oppgitt():
    assert len(T.KALENDERE) == 4
    assert T.MIN_ATTESTASJONER == 2


def test_eksisterende_kvittering_gjenbrukes(tmp_path):
    """Idempotens: en bundle som alt er stemplet, skal ikke stemples på nytt."""
    f = tmp_path / "x.bundle"
    f.write_bytes(b"innhold")
    ut = tmp_path / "ots"
    ut.mkdir()
    (ut / "x.bundle.ots").write_bytes(b"kvittering")
    s = T.stamp(f, ut_dir=ut)
    assert s.ok and s.bytes == len(b"kvittering")
    assert s.feil is None


def test_feil_returneres_og_kastes_ikke(tmp_path, monkeypatch):
    """En lås som ikke kan føres fordi et eksternt nettverk er nede, er verre enn en
    lås uten tidsstempel. stamp() skal melde feil, ikke kaste."""
    monkeypatch.setattr(T, "_ots_kjørbar", lambda: None)
    s = T.stamp(tmp_path / "finnes-ikke.bundle")
    assert not s.ok
    assert "ots ikke installert" in (s.feil or "")
