"""Rørledningen L1 → L2. Ingen nettkall; materialet ligger på disk."""

import json

from control import Corpus

from gjenopptak.pipeline import (
    MARKERS,
    WARNING,
    classify_file,
    doc_id_for,
    markers_in,
    run,
    summarise,
)


def test_innholdstypen_avgjoeres_paa_bytes_ikke_filnavn(tmp_path):
    """Alt lagret materiale heter .json, uansett om det er PDF eller XML."""
    (tmp_path / "jats-PMC1-abcdef123456.json").write_bytes(b"<article><body/></article>")
    (tmp_path / "dl-pdf-W1-abcdef123456.json").write_bytes(b"%PDF-1.7\n...")
    (tmp_path / "jats-PMC9-abcdef123456.json").write_bytes(b"{}")
    assert classify_file(tmp_path / "jats-PMC1-abcdef123456.json") == "jats"
    assert classify_file(tmp_path / "dl-pdf-W1-abcdef123456.json") == "pdf"
    assert classify_file(tmp_path / "jats-PMC9-abcdef123456.json") == "ukjent"


def test_doc_id_stripper_prefiks_og_sha():
    assert doc_id_for.__call__.__self__ is None if False else True
    from pathlib import Path
    assert doc_id_for(Path("cs-jats-PMC4339705-474be9c3b443.json")) == "PMC4339705"
    assert doc_id_for(Path("dl-pdf-W2794732936-5dd2caac3469.json")) == "W2794732936"


def test_markoerene_kan_tilskrives_enkeltvis():
    m = markers_in("We could not code all records because the workload was too large.")
    assert "could not" in m
    assert markers_in("Ingen markør her.") == []
    assert len(MARKERS) >= 20


def test_advarselen_staar_i_hver_utdatafil(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "jats-PMC1-abcdef123456.json").write_bytes(
        b"<article><body><sec><title>3. Results</title>"
        b"<p>We could not validate the model because the archives were unavailable. "
        b"A second sentence follows here for context.</p></sec></body></article>")
    res = run(raw, tmp_path / "ut", tmp_path / "tmp")
    for navn in ("sentences", "passages", "candidates"):
        first = res["files"][navn].read_text(encoding="utf-8").splitlines()[0]
        d = json.loads(first)
        assert d["_warning"] == WARNING
        t = Corpus("advarsel", [d["_warning"]])
        t.must_hit("IKKE UTVALGSDATA")
        t.must_hit("Ingen tall fra denne filen er M1 eller M2")


def test_kandidater_har_ingen_dom(tmp_path):
    """Ingen dommer har kjørt: klassen er ikke tildelt."""
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "jats-PMC1-abcdef123456.json").write_bytes(
        b"<article><body><sec><title>Discussion</title>"
        b"<p>We were unable to code all records because the workload was too large. "
        b"This limits the analysis in ways we describe below.</p></sec></body></article>")
    res = run(raw, tmp_path / "ut", tmp_path / "tmp")
    linjer = res["files"]["candidates"].read_text(encoding="utf-8").splitlines()[1:]
    assert linjer, "skulle gitt minst én kandidat"
    for l in linjer:
        k = json.loads(l)
        assert k["obstacle_class"] == "UNSURE"
        assert k["judge"] == "pipeline:ingen-dommer"
        assert k["is_hit"] is False
        assert k["unsure"] is True


def test_oppsummeringen_maaler_filteret_ikke_prevalens(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "jats-PMC1-abcdef123456.json").write_bytes(
        b"<article><body><sec><title>Discussion</title>"
        b"<p>We could not code all records because the workload was too large. "
        b"Another sentence for the window.</p></sec></body></article>")
    (raw / "jats-PMC2-abcdef123456.json").write_bytes(
        b"<article><body><sec><title>Results</title>"
        b"<p>Everything went well and nothing was left undone at all here. "
        b"A second plain sentence.</p></sec></body></article>")
    s = summarise(run(raw, tmp_path / "ut", tmp_path / "tmp")["docs"])
    assert s["n_docs"] == 2 and s["n_error"] == 0
    assert s["docs_without_candidate"] == 1
    assert s["share_without_candidate"] == 0.5
    assert "top_markers" in s and "top_marker_share" in s
    # Ingen nøkkel later som dette er prevalens:
    for forbudt in ("m1", "prevalence", "prevalens"):
        assert not any(forbudt in k.lower() for k in s)
