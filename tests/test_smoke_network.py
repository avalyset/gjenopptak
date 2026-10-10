"""Røyktest mot det levende API-et. Markert `network`; ikke med i standardkjøring.

    .venv/bin/python -m pytest -m network

Ett kall, maks 10 works, ett felt. Fulltekst hentes ikke.
"""

import json
from pathlib import Path

import pytest
from control import Corpus

from gjenopptak.harvest import MANIFEST_NAME
from gjenopptak.harvest.smoketest import main
from gjenopptak.schemas import validate

pytestmark = pytest.mark.network


@pytest.fixture(autouse=True)
def _adr0009_port(tmp_path, monkeypatch):
    """ADR-0009-porten slippes forbi her, som i test_fetchtest.py; Vault-nektelsen testes i
    test_vault_standard.py. Røyktesten skriver til tmp_path, som med vilje ikke ligger på Vault."""
    from gjenopptak.harvest import smoketest as _st
    monkeypatch.setattr(_st, "krev", lambda d=None, **kw: Path(d) if d else tmp_path)


def test_roykttest_ende_til_ende(tmp_path, capsys):
    kode = main(["--field", "energimodellering", "--limit", "10", "--data-dir", str(tmp_path)])
    assert kode == 0
    ut = capsys.readouterr().out

    rader = [json.loads(l) for l in (tmp_path / "documents.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert 0 < len(rader) <= 10
    for r in rader:
        validate("documents", r)
    assert all(r["has_fulltext"] for r in rader)
    assert all(2015 <= r["publication_year"] <= 2020 for r in rader)
    assert all(r["fulltext_format"] == "none" for r in rader), "L0 skal ikke hente fulltekst"

    manifest = Corpus("manifest", (tmp_path / "raw" / MANIFEST_NAME).read_text(encoding="utf-8").splitlines())
    manifest.must_hit("works-energimodellering")
    manifest.must_hit("https://api.openalex.org/works")
    for r in rader:
        assert r["raw_sha256"] and len(r["raw_sha256"]) == 64
    manifest.must_hit(rader[0]["raw_sha256"])

    logg = Corpus("stdout", ut.splitlines())
    logg.must_hit("ADDENDUM-01 mangler")
    logg.must_hit("fulltekst   : ikke hentet")
