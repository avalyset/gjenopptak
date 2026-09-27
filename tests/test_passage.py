"""ADDENDUM-03 §1: observasjonsenheten er passasjen, og begge tall rapporteres."""

import pytest
from control import Corpus

from gjenopptak.extract import NotSplit, Passage, format_m1, passages, split_counts, WINDOW


def rows(*setninger, doc_id="W1", section="3. Results", prov="source"):
    return [
        {"doc_id": doc_id, "sentence_index": i, "text": t,
         "section_raw": section, "section_label_provenance": prov}
        for i, t in enumerate(setninger)
    ]


# Tekstvitenskapstilfellet fra ADDENDUM-02 §2.5: hindringen står i nabosetningen.
NABO = rows(
    "We analysed the corpus.",
    "The standard work is Dottin (1894), but we were unable to consult the work.",
    "No copy was available in any accessible library.",
    "We therefore relied on later citations.",
)

# Energikontrollens form: begge deler i samme setning.
SAMME = rows(
    "Aggregate load matches published totals.",
    "We could not validate the model because manually transcribing the archives was beyond our resources.",
    "Ramp rates were checked for two zones.",
)


def test_vinduet_er_to_setninger():
    assert WINDOW == 2


def test_hindring_i_nabosetning_gir_passage_ikke_sentence():
    """Det gamle setningskravet ville forkastet dette treffet."""
    h = passages(NABO)
    assert len(h) == 1
    assert h[0].unit == "passage"
    assert h[0].span() == {"start_index": 0, "end_index": 3, "n_sentences": 4, "window": 2}


def test_hindring_i_samme_setning_gir_sentence():
    h = passages(SAMME)
    assert len(h) == 1 and h[0].unit == "sentence"


def test_begge_tall_rapporteres_alltid():
    linje = format_m1(passages(NABO), 1)
    tekst = Corpus("m1", [linje])
    tekst.must_hit("M1-streng 0/1")
    tekst.must_hit("M1-passasje 1/1")
    # Setningskravet alene ville gitt 0 %. Passasjekravet gir 100 %.
    assert "0.0%" in linje and "100.0%" in linje


def test_split_counts_skiller_de_to():
    c = split_counts(passages(NABO) + passages(SAMME))
    assert c == {"sentence": 1, "passage": 1}


def test_modulen_tilbyr_ingen_enkelttalls_m1():
    """Regelen håndheves ved at det ikke finnes en funksjon som slår dem sammen."""
    import gjenopptak.extract as ex

    for navn in dir(ex):
        assert navn not in ("m1", "prevalence", "hit_rate", "count_hits")


def test_omfangsvalg_uten_hindring_er_ikke_treff():
    """N3 (PREREG §5): sier hva teksten ikke handler om, uten å navngi en hindring."""
    n3 = rows("A detailed discussion is beyond the scope of this paper.",
              "We instead focus on the main mechanism.")
    assert passages(n3) == []


def test_passasjen_bærer_seksjon_og_opphav():
    """ADR-0002 og ADR-0007 følger passasjen."""
    h = passages(rows(
        "We could not code every record because the workload was too large.",
        section="4. Discussion and limitations", prov="parser"))
    assert h[0].section_raw == "4. Discussion and limitations"
    assert h[0].section_label_provenance == "parser"


def test_vinduet_klippes_ved_dokumentgrensene():
    h = passages(rows("We were unable to transcribe the tape because it was inaudible.",
                      "Next sentence."))
    assert h[0].start_index == 0 and h[0].end_index == 1


def test_setninger_fra_flere_dokumenter_avvises():
    blandet = rows("We could not do X because of Y.") + rows("Another.", doc_id="W2")
    with pytest.raises(ValueError):
        passages(blandet)


def test_m1_krever_nevner():
    with pytest.raises(NotSplit):
        format_m1(passages(SAMME), 0)


def test_skjemaet_krever_unit_og_passage_span():
    from gjenopptak.schemas import errors, load_schema, validate

    for navn in ("candidates", "claims"):
        req = load_schema(navn)["required"]
        assert "unit" in req and "passage_span" in req, navn

    claim = {
        "schema_version": "claims-2", "claim_id": "C1", "candidate_id": "W1:12",
        "doc_id": "W1", "field_key": "energimodellering", "section_raw": "3. Results",
        "section_label_provenance": "source", "obstacle_class": "H1",
        "loftbarhet": [{"vurdert_dato": "2026-09-20", "datopresisjon": "dag",
             "tabellversjon": "PREREG-v1-§5 + ADDENDUM-05", "obstacle_class": "H1",
             "verdi": "ja", "vurdert_av": "oss"}],
        "falsified": False, "tested_at": "2026-09-12T10:00:00+00:00",
        "cites_coverage": {"fulltext_available": 3, "fulltext_total": 11, "coverage_ratio": 0.27},
    }
    assert any("unit" in f for f in errors("claims", claim))
    claim["unit"] = "passage"
    claim["passage_span"] = passages(NABO)[0].span()
    validate("claims", claim)
    # Ukjent enhet avvises.
    claim["unit"] = "paragraph"
    assert errors("claims", claim)
