"""L0: avledning og manifest. Offline; nettkallet ligger i røyktesten."""

import json

import pytest
from control import Corpus
from fixtures import OPENALEX_RESPONSE

from gjenopptak.harvest import (
    MANIFEST_NAME,
    build_document,
    build_filter,
    sha256_bytes,
    write_documents,
    write_raw,
)
from gjenopptak.schemas import validate


def test_filteret_baerer_de_laaste_rammebetingelsene():
    f = build_filter(["https://openalex.org/T10159"])
    assert "has_fulltext:true" in f
    assert "publication_year:2015-2020" in f
    with pytest.raises(ValueError):
        build_filter([])


def test_raadata_lagres_urort_og_fores_i_manifest(tmp_path):
    blob = json.dumps(OPENALEX_RESPONSE, ensure_ascii=False).encode("utf-8")
    rec = write_raw(blob, "https://api.openalex.org/works?filter=x", tmp_path / "raw", stem="openalex-proeve")

    assert rec.path.read_bytes() == blob, "rådata ble endret ved lagring"
    assert rec.sha256 == sha256_bytes(blob)
    assert rec.bytes_len == len(blob)

    manifest = (tmp_path / "raw" / MANIFEST_NAME).read_text(encoding="utf-8")
    rader = Corpus("manifest", manifest.splitlines())
    rader.must_hit(rec.path.name)
    rader.must_hit(rec.sha256)
    rader.must_hit(str(len(blob)))
    rader.must_hit("https://api.openalex.org/works?filter=x")
    rader.must_hit(rec.harvested_at)


def test_manifest_er_append_only(tmp_path):
    raw = tmp_path / "raw"
    a = write_raw(b'{"a":1}', "https://example.invalid/a", raw, stem="a")
    b = write_raw(b'{"b":2}', "https://example.invalid/b", raw, stem="b")
    linjer = (raw / MANIFEST_NAME).read_text(encoding="utf-8").splitlines()
    rader = Corpus("manifest", linjer)
    rader.must_hit(a.sha256)
    rader.must_hit(b.sha256)
    assert sum(1 for line in linjer if line.startswith("| ") and "sha256" not in line) == 2


def test_dokumenter_avledes_og_validerer(tmp_path):
    blob = json.dumps(OPENALEX_RESPONSE, ensure_ascii=False).encode("utf-8")
    rec = write_raw(blob, "https://api.openalex.org/works?filter=x", tmp_path / "raw", stem="openalex")
    docs = [build_document(w, field_key="energimodellering", raw=rec)
            for w in OPENALEX_RESPONSE["results"]]
    for d in docs:
        validate("documents", d)

    doi = Corpus.from_records("doi", docs, lambda r: r["doi"] or "")
    doi.must_hit("10.1016/j.apenergy.2018.04.048")  # den positive kontrollen, PREREG-v1 §7

    lisens = Corpus.from_records("license", docs, lambda r: r["license"] or "")
    lisens.must_hit("cc-by")

    assert all(d["raw_sha256"] == rec.sha256 for d in docs)
    assert all(d["has_fulltext"] for d in docs)
    assert all(2015 <= d["publication_year"] <= 2020 for d in docs)
    assert all(d["fulltext_format"] == "none" for d in docs), "L0 henter ikke fulltekst"


def test_ukjent_felt_avvises(tmp_path):
    rec = write_raw(b"{}", "https://example.invalid", tmp_path / "raw", stem="x")
    with pytest.raises(ValueError):
        build_document(OPENALEX_RESPONSE["results"][0], field_key="fysikk", raw=rec)


def test_documents_jsonl_radantall(tmp_path):
    rec = write_raw(b"{}", "https://example.invalid", tmp_path / "raw", stem="x")
    docs = [build_document(w, field_key="energimodellering", raw=rec)
            for w in OPENALEX_RESPONSE["results"]]
    ut = tmp_path / "documents.jsonl"
    assert write_documents(docs, ut) == 2
    linjer = ut.read_text(encoding="utf-8").splitlines()
    assert len(linjer) == 2
    ider = Corpus("jsonl", linjer)
    ider.must_hit("W2799011080")
    ider.expect_none("W0000000000")
