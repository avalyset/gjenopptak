"""Skjemaene: gyldige poster slipper gjennom, ugyldige stoppes."""

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from gjenopptak.schemas import NAMES, errors, load_schema, validate

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "src" / "gjenopptak" / "schemas"


#: Poster som bærer sin egen schema_version. Utvidet 27.09.2026 med «kandidat», som er
#: registerraden i claims-2 med usikkerheten på raden (byggeplanen B3).
POSTER = {"documents", "sentences", "candidates", "claims", "kandidat"}
#: «registerhode» er ikke en post men et hode: det beskriver en liste, og bærer ingen
#: schema_version. Det er derfor skilt ut her og ikke unntatt inne i løkken.
HODER = {"registerhode"}


def test_alle_skjemaer_er_dekket_av_en_av_gruppene():
    assert set(NAMES) == POSTER | HODER


def test_postskjemaene_har_schema_version_og_er_strenge():
    for name in sorted(POSTER):
        s = load_schema(name)
        forventet = {"claims": "claims-2", "kandidat": "claims-2"}.get(name, f"{name}-1")
        assert s["properties"]["schema_version"]["const"] == forventet, name
        assert "schema_version" in s["required"], name
        assert s["additionalProperties"] is False, name


def test_hodeskjemaene_er_strenge_uten_schema_version():
    for name in sorted(HODER):
        s = load_schema(name)
        assert "schema_version" not in s["properties"], name
        assert s["additionalProperties"] is False, name


def _candidate(**over) -> dict:
    rec = {
        "schema_version": "candidates-1",
        "candidate_id": "W1:12",
        "sentence_id": "W1:12",
        "doc_id": "W1",
        "field_key": "energimodellering",
        "section_raw": "3. Results",
        "is_hit": True,
        "obstacle_class": "H1",
        "liftable": "ja",
        "liftability_table_version": "PREREG-v1-§5",
        "judge": "owner",
        "judged_at": "2026-09-12T10:00:00+00:00",
        "section_label_provenance": "source",
        "unit": "sentence",
        "passage_span": {"start_index": 10, "end_index": 14, "n_sentences": 5, "window": 2},
    }
    rec.update(over)
    return rec


def test_gyldig_kandidat_validerer():
    validate("candidates", _candidate())


def test_loftbarhet_utenfor_tabellen_avvises():
    """ADR-0004: liftable er et lukket sett hentet fra PREREG-v1 §5."""
    with pytest.raises(ValidationError):
        validate("candidates", _candidate(liftable="kanskje"))


def test_ukjent_hindringsklasse_avvises():
    with pytest.raises(ValidationError):
        validate("candidates", _candidate(obstacle_class="H10"))


def test_modellsignatur_krever_keep_alive_null():
    """ADR-0003: keep_alive=0 er et krav, ikke en innstilling."""
    sig = {
        "model_id": "lokalmodell:8b",
        "weights_sha256": "a" * 64,
        "temperature": 0.0,
        "seed": 7,
        "keep_alive": 0,
        "runtime": "ollama-0.0.0",
        "prompt_sha256": "b" * 64,
        "judged_at": "2026-09-12T10:00:00+00:00",
    }
    validate("candidates", _candidate(judge="local:lokalmodell:8b", model_signature=sig))

    dårlig = dict(sig, keep_alive=300)
    with pytest.raises(ValidationError):
        validate("candidates", _candidate(judge="local:lokalmodell:8b", model_signature=dårlig))


def test_modellsignatur_med_manglende_felt_er_ugyldig():
    """Mangler ett felt, er oppføringen ugyldig og telles ikke."""
    ufullstendig = {
        "model_id": "lokalmodell:8b",
        "weights_sha256": "a" * 64,
        "temperature": 0.0,
        "seed": 7,
        "keep_alive": 0,
        "runtime": "ollama-0.0.0",
        # prompt_sha256 mangler
        "judged_at": "2026-09-12T10:00:00+00:00",
    }
    feil = errors("candidates", _candidate(model_signature=ufullstendig))
    assert any("prompt_sha256" in f for f in feil), feil


def test_claims_krever_dekningsgrad():
    """PREREG-v1 §8: dekningsgrad kan ikke utelates."""
    claim = {
        "schema_version": "claims-2",
        "claim_id": "C1",
        "candidate_id": "W1:12",
        "doc_id": "W1",
        "field_key": "energimodellering",
        "obstacle_class": "H1",
        "loftbarhet": [
            {"vurdert_dato": "2026-09-20", "datopresisjon": "dag",
             "tabellversjon": "PREREG-v1-§5 + ADDENDUM-05", "obstacle_class": "H1",
             "verdi": "ja", "vurdert_av": "oss"}
        ],
        "falsified": False,
        "tested_at": "2026-09-12T10:00:00+00:00",
        "section_raw": "3. Results",
        "section_label_provenance": "source",
        "unit": "passage",
        "passage_span": {"start_index": 10, "end_index": 14, "n_sentences": 5, "window": 2},
    }
    feil = errors("claims", claim)
    assert any("cites_coverage" in f for f in feil), feil
    claim["cites_coverage"] = {"fulltext_available": 3, "fulltext_total": 11, "coverage_ratio": 3 / 11}
    validate("claims", claim)


def test_skjemafiler_er_gyldig_json_og_utf8():
    for name in NAMES:
        raw = (SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8")
        json.loads(raw)


# --------------------------------------------------------------------------- #
# ADR-0007: seksjonsetikettens opphav
# --------------------------------------------------------------------------- #

def test_provenance_er_paakrevd_i_alle_tre_leddene():
    """Kjeden skal feile på manglende opphav, ikke anta en verdi."""
    for navn in ("sentences", "candidates", "claims"):
        assert "section_label_provenance" in load_schema(navn)["required"], navn


def test_kandidat_uten_provenance_avvises():
    rec = _candidate()
    del rec["section_label_provenance"]
    feil = errors("candidates", rec)
    assert any("section_label_provenance" in f for f in feil), feil


def test_provenance_er_et_lukket_sett():
    for ugyldig in ("SOURCE", "grobid", "ukjent", "", None):
        with pytest.raises(ValidationError):
            validate("candidates", _candidate(section_label_provenance=ugyldig))


def test_parser_krever_begge_versjonsfeltene():
    """ADR-0007: mangler ett av dem, er oppføringen ugyldig og telles ikke."""
    validate("candidates", _candidate(
        section_label_provenance="parser",
        parser_version="grobid-0.8.1",
        parser_model_version="BidLSTM_CRF-2024-04",
    ))
    for mangler in ({"parser_version": "grobid-0.8.1"},
                    {"parser_model_version": "BidLSTM_CRF-2024-04"},
                    {}):
        feil = errors("candidates", _candidate(section_label_provenance="parser", **mangler))
        assert feil, mangler


def test_parser_avviser_tom_versjonsstreng():
    feil = errors("candidates", _candidate(
        section_label_provenance="parser", parser_version="", parser_model_version="x"))
    assert any("parser_version" in f or "minLength" in f or "short" in f for f in feil), feil


def test_source_krever_ikke_versjonsfelt():
    """En kildemerket seksjon har ingen parser å versjonere."""
    validate("candidates", _candidate(section_label_provenance="source"))


def test_unit_er_et_lukket_sett():
    """ADDENDUM-03 §1: bare sentence og passage finnes."""
    for ugyldig in ("paragraph", "document", "SENTENCE", None):
        with pytest.raises(ValidationError):
            validate("candidates", _candidate(unit=ugyldig))


def test_passage_span_krever_alle_fire_feltene():
    for mangler in ("start_index", "end_index", "n_sentences", "window"):
        span = {"start_index": 10, "end_index": 14, "n_sentences": 5, "window": 2}
        del span[mangler]
        feil = errors("candidates", _candidate(passage_span=span))
        assert any(mangler in f for f in feil), (mangler, feil)
