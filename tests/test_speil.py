"""Speilet skal melde fra når det ligger bak repoet.

Den ekte feilen speilingen er bygd mot: `7fb32fc` rettet navneformen i LICENSE,
LICENSE-DATA og README.md. Ingen av dem er en låst fil, så securerepo svarte
«ingen bundle nødvendig» og returnerte før noe ble kopiert. Speilet sto med gal
navneform i et døgn. Testene under holder den ruten åpen.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from gjenopptak import speil as S


@pytest.fixture
def rigg(tmp_path, monkeypatch):
    """Lite repo + falsk Vault. PLIKT snevres inn til tre filer."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "LICENSE").write_text("Copyright 2026 Eirik Botten Nicolaysen\n", encoding="utf-8")
    (repo / "README.md").write_text("# gjenopptak\n", encoding="utf-8")
    (repo / "docs" / "ZENODO.md").write_text("DOI 10.5281/zenodo.1\n", encoding="utf-8")

    dest = tmp_path / "vault" / "gjenopptak-kilder"
    (dest / S.SPEILKATALOG).mkdir(parents=True)
    monkeypatch.setattr(S, "require_vault", lambda *a, **kw: dest)
    monkeypatch.setattr(S, "PLIKT", ("LICENSE", "README.md", "docs/ZENODO.md"))
    return repo, dest / S.SPEILKATALOG


def status(rader: list[S.Avvik]) -> dict[str, str]:
    return {a.navn: a.status for a in rader}


def test_fanger_utdatert_speilkopi(rigg):
    """Kjernekravet: en kopi med gammelt innhold skal meldes, ikke passere."""
    repo, speilsti = rigg
    # Speilet får den gale navneformen — slik den faktisk sto på Vault.
    (speilsti / "LICENSE").write_text("Copyright 2026 Eirik Bottenvik-Nicolaysen\n",
                                      encoding="utf-8")
    subprocess.run(["cp", "-p", str(repo / "README.md"), str(speilsti)], check=True)
    subprocess.run(["cp", "-p", str(repo / "docs" / "ZENODO.md"), str(speilsti)], check=True)

    rader = S.avvik(repo, Path("/ignorert"))
    assert status(rader) == {"LICENSE": S.UTDATERT, "README.md": S.LIK, "ZENODO.md": S.LIK}
    bak = S.etterslep(rader)
    assert [a.navn for a in bak] == ["LICENSE"]
    # Og avviket er sha256, ikke tidsstempel: kopien er nyere enn kilden her.
    assert bak[0].kilde_sha != bak[0].speil_sha

    S.speil(repo, Path("/ignorert"))
    assert (speilsti / "LICENSE").read_text(encoding="utf-8") == \
        (repo / "LICENSE").read_text(encoding="utf-8")
    assert S.etterslep(S.avvik(repo, Path("/ignorert"))) == []


def test_fanger_manglende_speilkopi(rigg):
    repo, speilsti = rigg
    rader = S.avvik(repo, Path("/ignorert"))
    assert set(status(rader).values()) == {S.MANGLER}
    assert len(S.speil(repo, Path("/ignorert"))) == 3
    assert S.etterslep(S.avvik(repo, Path("/ignorert"))) == []


def test_byggeartefakt_meldes_men_roeres_ikke(rigg):
    """PDF og abstrakt har ingen kilde i repoet. De skal ses, ikke slettes."""
    repo, speilsti = rigg
    artefakt = speilsti / "abstract.txt"
    artefakt.write_text("bygget, ikke sporet\n", encoding="utf-8")
    rader = S.avvik(repo, Path("/ignorert"))
    assert status(rader)["abstract.txt"] == S.FORELDRELOES
    assert not any(a.navn == "abstract.txt" for a in S.etterslep(rader))
    S.speil(repo, Path("/ignorert"))
    assert artefakt.exists() and artefakt.read_text(encoding="utf-8") == "bygget, ikke sporet\n"


def test_fil_utenfor_plikt_men_med_kilde_fanges_ogsaa(rigg):
    """Ligger noe i speilet som finnes i repoet, gjelder innholdskravet det også."""
    repo, speilsti = rigg
    (repo / "docs" / "LAERDOM.md").write_text("ny tekst\n", encoding="utf-8")
    (speilsti / "LAERDOM.md").write_text("gammel tekst\n", encoding="utf-8")
    rader = S.avvik(repo, Path("/ignorert"))
    assert status(rader)["LAERDOM.md"] == S.UTDATERT
    S.speil(repo, Path("/ignorert"))
    assert (speilsti / "LAERDOM.md").read_text(encoding="utf-8") == "ny tekst\n"


def test_check_gir_exit_1_ved_etterslep_og_0_naar_ajour(rigg, capsys):
    repo, speilsti = rigg
    argv = ["--repo", str(repo), "--vault-root", "/ignorert", "--check"]
    assert S.main(argv) == 1
    assert S.main(["--repo", str(repo), "--vault-root", "/ignorert"]) == 0
    assert S.main(argv) == 0


def test_securerepo_speiler_selv_naar_ingen_laast_fil_er_roert(tmp_path, monkeypatch):
    """Regresjonen: ruten som returnerte 0 uten å røre speilet."""
    from gjenopptak import securerepo as R

    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True)
    (repo / "LICENSE").write_text("Copyright 2026 Eirik Botten Nicolaysen\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "rettet navneform"], cwd=repo, check=True)

    dest = tmp_path / "vault" / "gjenopptak-kilder"
    (dest / S.SPEILKATALOG).mkdir(parents=True)
    (dest / S.SPEILKATALOG / "LICENSE").write_text(
        "Copyright 2026 Eirik Bottenvik-Nicolaysen\n", encoding="utf-8")
    monkeypatch.setattr(S, "require_vault", lambda *a, **kw: dest)
    monkeypatch.setattr(S, "PLIKT", ("LICENSE",))

    # Commiten rører ingen låst fil: securerepo skriver ingen bundle ...
    kode = R.main(["--repo", str(repo), "--vault-root", str(tmp_path / "vault")])
    assert kode == 0
    # ... men speilet er likevel friskmeldt.
    assert (dest / S.SPEILKATALOG / "LICENSE").read_text(encoding="utf-8") == \
        "Copyright 2026 Eirik Botten Nicolaysen\n"


def test_plikt_peker_paa_filer_som_finnes():
    """PLIKT skal ikke drifte fra repoet."""
    rot = Path(__file__).resolve().parent.parent
    mangler = [rel for rel in S.PLIKT if not (rot / rel).is_file()]
    assert mangler == []
