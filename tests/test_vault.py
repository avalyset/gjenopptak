"""Sikring til Vault. Ingen avhengighet av at volumet er montert."""

from pathlib import Path

import pytest
from control import Corpus

from gjenopptak import vault as v


def test_ingen_fallback_naar_volumet_mangler(tmp_path):
    """En kopi på systemdisken ser ut som en sikring og er ikke det."""
    with pytest.raises(v.VaultUnavailable) as e:
        v.require_vault(tmp_path / "finnes-ikke")
    assert "ikke montert" in str(e.value)


def test_katalog_som_ikke_er_montert_avvises(tmp_path):
    """Katalogen finnes, men er ikke et volum — det er den farlige varianten."""
    (tmp_path / "Vault").mkdir()
    with pytest.raises(v.VaultUnavailable) as e:
        v.require_vault(tmp_path / "Vault")
    assert "ikke et montert volum" in str(e.value)


def test_ruting_skiller_fulltekst_fra_api_svar(tmp_path):
    data = tmp_path / "data"
    for sub in ("raw", "frames"):
        (data / sub).mkdir(parents=True)
    assert v.route(data / "raw" / "jats-PMC1-abc.json", data) == "fulltext"
    assert v.route(data / "raw" / "dl-pdf-W1-abc.json", data) == "fulltext"
    assert v.route(data / "raw" / "epmc-kand-arkeologi-x.json", data) == "raw"
    assert v.route(data / "raw" / "MANIFEST.md", data) == "raw"
    assert v.route(data / "frames" / "frame-x-RAW.jsonl", data) == "frames"
    assert v.route(data / "nedlastbarhet.json", data) == "logs"


def test_fulltekstprefiksene_dekker_alle_hentemaater():
    p = Corpus("prefikser", list(v.FULLTEXT_PREFIXES))
    for s in ("jats-", "pdf-", "ft-jats-", "cs-jats-", "dl-pdf-"):
        p.must_hit(s)


def test_kopiering_verifiserer_paa_innhold(tmp_path):
    src = tmp_path / "kilde.txt"
    src.write_text("æøå innhold\n", encoding="utf-8")
    res = v.copy_verified(src, tmp_path / "ut")
    assert not res.mismatch
    assert res.sha256 == res.dst_sha256 == v.sha256_file(res.dst)
    assert res.bytes == src.stat().st_size


def test_manifestet_leses_til_oppslag_med_url_og_dato(tmp_path):
    man = tmp_path / "MANIFEST.md"
    man.write_text(
        "| filnavn | bytes | sha256 | kilde-URL | hentetidspunkt |\n|---|---|---|---|---|\n"
        f"| jats-PMC1-abc.json | 120 | {'a'*64} | https://ex.invalid/PMC1/fullTextXML | 2026-09-12T10:00:00+00:00 |\n",
        encoding="utf-8")
    d = v.parse_source_manifest(man)
    assert d["jats-PMC1-abc.json"]["source_url"] == "https://ex.invalid/PMC1/fullTextXML"
    assert d["jats-PMC1-abc.json"]["fetched_at"] == "2026-09-12T10:00:00+00:00"


def test_siste_rad_vinner_naar_samme_fil_er_hentet_flere_ganger(tmp_path):
    man = tmp_path / "MANIFEST.md"
    man.write_text(
        f"| f.json | 1 | {'a'*64} | https://ex.invalid/1 | 2026-09-12T10:00:00+00:00 |\n"
        f"| f.json | 1 | {'a'*64} | https://ex.invalid/2 | 2026-09-12T11:00:00+00:00 |\n",
        encoding="utf-8")
    assert v.parse_source_manifest(man)["f.json"]["source_url"] == "https://ex.invalid/2"


def test_navneoppslag_normaliseres_til_nfc():
    """diff -r gir falske avvik; oppslag må tåle begge formene."""
    import unicodedata
    nfd = unicodedata.normalize("NFD", "tekstvitenskap-æøå.json")
    assert v.nfc(nfd) == unicodedata.normalize("NFC", nfd)
    assert v.nfc(nfd) != nfd


def test_vault_manifest_faar_fulltekstkolonner(tmp_path):
    data = tmp_path / "data"
    (data / "raw").mkdir(parents=True)
    (data / "raw" / "jats-PMC1-abc.json").write_text("<article/>", encoding="utf-8")
    (data / "logg.json").write_text("{}", encoding="utf-8")
    (data / "raw" / "MANIFEST.md").write_text(
        f"| jats-PMC1-abc.json | 10 | {'b'*64} | https://ex.invalid/x | 2026-09-12T09:00:00+00:00 |\n",
        encoding="utf-8")
    dest = tmp_path / "vault" / "gjenopptak-kilder"
    rep = v.secure_tree(data, dest)
    assert rep.n_files == 3 and not rep.mismatches
    path, digest = v.write_vault_manifest(rep)
    m = Corpus("manifest", path.read_text(encoding="utf-8").splitlines())
    m.must_hit("kilde-URL")
    m.must_hit("https://ex.invalid/x")           # fulltekst har URL
    m.must_hit("2026-09-12T09:00:00+00:00")      # og hentedato
    m.must_hit("RAMMEPRØVE-IKKE-LEST")           # skillet mot leste filer
    assert len(digest) == 64


def test_frysingen_kaller_sikringen():
    """En frossen liste som bare finnes ett sted er et kvotedøgn i risiko."""
    import inspect

    from gjenopptak.harvest import freeze as fz

    kode = inspect.getsource(fz.main)
    k = Corpus("freeze.main", kode.splitlines())
    k.must_hit("secure_frame_file")
    k.must_hit("IKKE SIKRET")
    k.must_hit("--no-vault") if "--no-vault" in kode else k.must_hit("no_vault")


# --------------------------------------------------------------------------- #
# Repo-sikring: bundelen bærer historikken
# --------------------------------------------------------------------------- #

def test_bundle_navnet_baerer_head_ikke_bare_dato(tmp_path):
    """Dato alene lot en dummy-commit overskrive den ekte bundelen."""
    import subprocess

    repo = tmp_path / "r"
    repo.mkdir()
    for a in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "T"]):
        subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True)
    (repo / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "f.txt"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "en"], check=True, capture_output=True)
    n1 = v.bundle_name(repo, date="2026-09-12")
    (repo / "g.txt").write_text("y", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "g.txt"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "to"], check=True, capture_output=True)
    n2 = v.bundle_name(repo, date="2026-09-12")
    assert n1 != n2, "to commits samme dag må gi to filnavn"
    assert n1.startswith("gjenopptak-2026-09-12-") and n1.endswith(".bundle")
    # samme commit gir samme navn: idempotent, ikke destruktivt
    assert v.bundle_name(repo, date="2026-09-12") == n2


def test_de_laaste_filene_har_kjent_sha256():
    """Én rad per låst fil, og sha256 må stemme med den faktiske filen i repoet."""
    import hashlib
    from pathlib import Path

    assert len(v.LOCKED_FILES) == 10
    assert set(v.LOCKED_SHA256) == set(v.LOCKED_FILES)
    assert v.LOCKED_SHA256["PREREG-v1.md"].startswith("05988b23")
    assert v.LOCKED_SHA256["ADDENDUM-05.md"].startswith("b12c85b2")
    assert v.LOCKED_SHA256["ADDENDUM-06.md"].startswith("0f0e9a81")
    assert v.LOCKED_SHA256["ADDENDUM-07.md"].startswith("06eb4fb3")
    assert v.LOCKED_SHA256["ADDENDUM-08.md"].startswith("6888efb3")
    assert v.LOCKED_SHA256["ADDENDUM-09.md"].startswith("79f1baf5")

    rot = Path(__file__).resolve().parents[1]
    for navn, ventet in v.LOCKED_SHA256.items():
        fil = rot / navn
        assert fil.exists(), navn
        assert hashlib.sha256(fil.read_bytes()).hexdigest() == ventet, navn


def test_bare_prereg_og_addendum_utloeser_bundle():
    for ja in ("PREREG-v1.md", "ADDENDUM-01.md", "ADDENDUM-06.md", "ADDENDUM-99.md"):
        assert v.TRIGGER_PATTERN.match(ja), ja
    for nei in ("src/gjenopptak/vault.py", "docs/decisions/0007-x.md",
                "tests/test_vault.py", "ADDENDUM-01.md.bak", "README.md"):
        assert not v.TRIGGER_PATTERN.match(nei), nei


def test_bundelen_er_merket_autoritativ():
    note = Corpus("note", v.BUNDLE_NOTE.splitlines())
    note.must_hit("autoritative")
    note.must_hit("historikken")
    note.must_hit("én fil")


def test_securerepo_gir_exit_3_naar_vault_mangler(tmp_path, monkeypatch):
    """Samme mønster som frame-sikringen: advarsel og exit-kode, ikke stillhet."""
    from gjenopptak import securerepo as sr

    monkeypatch.setattr(sr, "commit_touches_locked", lambda *a, **k: ["ADDENDUM-01.md"])
    monkeypatch.setattr(sr, "_git", lambda *a, **k: "deadbeefcafe\n")
    kode = sr.main(["--repo", str(tmp_path), "--vault-root", str(tmp_path / "ingen-vault")])
    assert kode == 3


def test_securerepo_skriver_ingen_bundle_men_speiler_naar_ingen_laast_fil_er_roert(
        tmp_path, monkeypatch):
    """Ruten som før returnerte 0 uten å røre noe. Nå går speilingen først.

    Endret kontrakt: tidligere svarte denne ruten 0 også når Vault var borte —
    den «hoppet over». Det er nøyaktig hullet LICENSE falt gjennom (se
    `gjenopptak.speil`), så uten Vault er svaret nå 3, etter samme norm som
    testen over: advarsel og exit-kode, ikke stillhet.
    """
    from gjenopptak import securerepo as sr
    from gjenopptak import speil as sp

    monkeypatch.setattr(sr, "commit_touches_locked", lambda *a, **k: [])
    monkeypatch.setattr(sr, "_git", lambda *a, **k: "deadbeefcafe\n")
    assert sr.main(["--repo", str(tmp_path), "--vault-root", str(tmp_path / "ingen")]) == 3

    # Med speilet på plass og à jour: ingen bundle, exit 0.
    dest = tmp_path / "dest"
    (dest / sp.SPEILKATALOG).mkdir(parents=True)
    monkeypatch.setattr(sp, "require_vault", lambda *a, **k: dest)
    monkeypatch.setattr(sp, "PLIKT", ())
    assert sr.main(["--repo", str(tmp_path), "--vault-root", str(tmp_path / "ingen")]) == 0


def test_laast_fil_med_endret_sha256_stopper_sikringen(tmp_path, monkeypatch):
    """En låst fil som er endret skal avbryte, ikke kopieres videre."""
    repo = tmp_path / "repo"
    repo.mkdir()
    for n in v.LOCKED_FILES:
        (repo / n).write_text("endret innhold\n", encoding="utf-8")
    monkeypatch.setattr(v, "require_vault", lambda root=None: tmp_path / "dest")
    with pytest.raises(OSError) as e:
        v.copy_locked_files(repo, root=tmp_path)
    assert "En låst fil er endret" in str(e.value)


# --------------------------------------------------------------------------- #
# To arkivspor: kanon og kode
# --------------------------------------------------------------------------- #

def _repo(tmp_path, filnavn="ADDENDUM-01.md"):
    import subprocess

    repo = tmp_path / "r"
    repo.mkdir()
    for a in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "T"]):
        subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True)
    (repo / filnavn).write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", filnavn], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "en"], check=True, capture_output=True)
    return repo


def test_de_to_sporene_har_hver_sin_katalog_og_prefiks():
    assert v.BUNDLE_CLASSES["kanon"]["dir"] == "kanon"
    assert v.BUNDLE_CLASSES["kode"]["dir"] == "kode"
    assert v.BUNDLE_CLASSES["kanon"]["prefix"] == "gjenopptak-"
    assert v.BUNDLE_CLASSES["kode"]["prefix"] == "gjenopptak-kode-"
    assert v.BUNDLE_CLASSES["kanon"]["authoritative"] is True
    assert v.BUNDLE_CLASSES["kode"]["authoritative"] is False


def test_navnene_kan_ikke_forveksles(tmp_path):
    repo = _repo(tmp_path)
    kanon = v.bundle_name(repo, date="2026-09-12", bundle_class="kanon")
    kode = v.bundle_name(repo, date="2026-09-12", bundle_class="kode")
    assert kanon != kode
    assert kode.startswith("gjenopptak-kode-")
    assert not kanon.startswith("gjenopptak-kode-")


def test_kodebundle_kan_ikke_skrives_til_kanon(tmp_path, monkeypatch):
    """Invarianten: kanon tar bare commits som fører inn en låst fil."""
    repo = _repo(tmp_path, filnavn="src.py")          # ingen låst fil
    monkeypatch.setattr(v, "require_vault", lambda root=None: tmp_path / "dest")
    with pytest.raises(v.WrongBundleClass) as e:
        v.write_bundle(repo, root=tmp_path, bundle_class="kanon")
    assert "kan ikke skrives til kanon" in str(e.value)
    assert not (tmp_path / "dest" / "repo" / "kanon").exists(), "ingenting skal være skrevet"


def test_laasecommit_kan_skrives_til_kanon(tmp_path, monkeypatch):
    repo = _repo(tmp_path, filnavn="ADDENDUM-01.md")
    monkeypatch.setattr(v, "require_vault", lambda root=None: tmp_path / "dest")
    res = v.write_bundle(repo, root=tmp_path, bundle_class="kanon", date="2026-09-12")
    assert res.bundle_class == "kanon" and res.authoritative
    assert res.covers == ("ADDENDUM-01.md",)
    assert res.path.parent.name == "kanon"


def test_force_gir_alltid_kode_aldri_kanon():
    """Ingen flaggkombinasjon skal kunne løfte kodearbeid inn i kanon."""
    import inspect

    from gjenopptak import securerepo as sr

    kode = inspect.getsource(sr.main)
    assert 'klasse = "kanon" if (utloest and not args.force) else "kode"' in kode
    # --force er dokumentert som kode-only i hjelpeteksten
    assert "ALLTID til kode/" in kode
    # og write_bundle håndhever det uavhengig av hvem som kaller
    assert "kan ikke skrives til kanon/" in inspect.getsource(v.write_bundle)


def test_nyeste_i_kanon_er_autoritativ(tmp_path, monkeypatch):
    repo = _repo(tmp_path, filnavn="ADDENDUM-01.md")
    monkeypatch.setattr(v, "require_vault", lambda root=None: tmp_path / "dest")
    a = v.write_bundle(repo, root=tmp_path, bundle_class="kanon", date="2026-09-11")
    assert v.latest_canon(tmp_path / "dest") == a.path


def test_laerdommen_er_skrevet_ned():
    from pathlib import Path

    doc = Path(__file__).resolve().parent.parent / "docs" / "laerdom-sikring.md"
    t = Corpus("lærdom", doc.read_text(encoding="utf-8").splitlines())
    t.must_hit("kan skade det det skal beskytte")
    t.must_hit("468ddbca")           # den ekte sha256
    t.must_hit("327fb3ce")           # dummy-versjonen som overskrev
    t.must_hit("ekte tilstand")
    t.must_hit("UFULLSTENDIG")       # hvor samme feil ellers kunne oppstå


# ------------------------------------------------- manifestet kan ikke krympe


def _rapport(dest, filer):
    """Liten SecureReport med ferdige CopyResult-er, uten å røre Vault."""
    rep = v.SecureReport(dest=dest)
    for navn, n in filer:
        (dest / "logs").mkdir(parents=True, exist_ok=True)
        dst = dest / "logs" / navn
        dst.write_bytes(b"x" * n)
        rep.results.append(v.CopyResult(
            src=Path(navn), dst=dst, bytes=n, sha256="0" * 64,
            copied_at="2026-09-12T00:00:00+00:00", source_url=None,
            fetched_at=None, mismatch=False))
    return rep


def test_manifest_file_count_leser_feltet(tmp_path):
    assert v.manifest_file_count(tmp_path / "finnes-ikke.md") is None
    p = tmp_path / "MANIFEST-VAULT.md"
    p.write_text("**Filer:** 969  **Bytes:** 1  \n", encoding="utf-8")
    assert v.manifest_file_count(p) == 969
    p.write_text("ingen felt her\n", encoding="utf-8")
    assert v.manifest_file_count(p) is None


def test_delvis_sikring_kan_ikke_krympe_manifestet(tmp_path):
    """Sperren testes mot det den skal beskytte: det store manifestet."""
    dest = tmp_path / "gjenopptak-kilder"
    stor = _rapport(dest, [(f"f{i}.json", 10) for i in range(5)])
    sti, _ = v.write_vault_manifest(stor)
    assert v.manifest_file_count(sti) == 5
    før = sti.read_bytes()

    liten = _rapport(dest, [("ny.json", 10)])
    with pytest.raises(v.ManifestWouldShrink, match="beskriver 5 filer"):
        v.write_vault_manifest(liten)
    assert sti.read_bytes() == før, "manifestet skal være uendret etter nekt"

    # tilsiktet krymping må sies eksplisitt
    sti2, _ = v.write_vault_manifest(liten, allow_shrink=True)
    assert v.manifest_file_count(sti2) == 1


def test_like_stort_eller_stoerre_manifest_skrives(tmp_path):
    dest = tmp_path / "gjenopptak-kilder"
    sti, _ = v.write_vault_manifest(_rapport(dest, [("a.json", 1), ("b.json", 1)]))
    assert v.manifest_file_count(sti) == 2
    sti, _ = v.write_vault_manifest(_rapport(dest, [("a.json", 1), ("b.json", 1)]))
    assert v.manifest_file_count(sti) == 2
    sti, _ = v.write_vault_manifest(
        _rapport(dest, [("a.json", 1), ("b.json", 1), ("c.json", 1)]))
    assert v.manifest_file_count(sti) == 3


def test_repo_seksjonene_baeres_over_en_overskriving(tmp_path):
    """securerepo appender, write_vault_manifest overskriver. Begge deler samme fil."""
    dest = tmp_path / "gjenopptak-kilder"
    sti, _ = v.write_vault_manifest(_rapport(dest, [("a.json", 1), ("b.json", 1)]))
    with sti.open("a", encoding="utf-8") as fh:
        fh.write("\n## Repo-sikring, kanon — 2026-09-12T00:00:00+00:00\n\n"
                 "| repo/kanon/x.bundle | 1 | " + "0" * 64 + " | nå | ADDENDUM-06.md | AUTORITATIV |\n")
    assert "Repo-sikring, kanon" in sti.read_text(encoding="utf-8")

    sti, _ = v.write_vault_manifest(_rapport(dest, [("a.json", 1), ("b.json", 1), ("c.json", 1)]))
    tekst = sti.read_text(encoding="utf-8")
    assert "Repo-sikring, kanon" in tekst, "repo-seksjonen forsvant i overskrivingen"
    assert "repo/kanon/x.bundle" in tekst
    assert tekst.count("Repo-sikring, kanon") == 1, "seksjonen skal ikke dupliseres"
    assert v.manifest_file_count(sti) == 3


def test_split_repo_sections():
    assert v.split_repo_sections("ingen seksjon her") == ""
    t = "kildeliste\n## Repo-sikring, kode — nå\n| rad |\n"
    assert v.split_repo_sections(t).startswith("## Repo-sikring, kode")
