"""Løftbarhet med uavklarte naboklasser (ADDENDUM-05, ADR-0004)."""

import pytest
from control import Corpus

from gjenopptak.classify import (
    NON_HITS,
    PREREG_TABLE,
    UNRESOLVED,
    UnknownClass,
    format_liftable,
    is_unresolved,
    liftability,
    liftable_share,
)
from gjenopptak.schemas import errors, load_schema, validate


def test_tabellen_er_prereg_5_ordrett():
    assert PREREG_TABLE == {
        "H1": "ja", "H2": "ja", "H3": "ja_med_forbehold", "H4": "ja",
        "H5": "delvis", "H6": "ja", "H7": "nei", "H8": "nei", "H9": "nei",
    }


def test_uavklart_gir_uavklart_ikke_ja():
    """PREREG §5 gir H1 «ja», og det anslaget er kjent for høyt."""
    for klasse in UNRESOLVED:
        assert liftability(klasse) == "uavklart", klasse
        assert liftability(klasse) != "ja"


def test_de_fire_naboparene_mot_h7():
    assert set(UNRESOLVED) == {"H1/H7-uavklart", "H2/H7-uavklart",
                               "H3/H7-uavklart", "H5/H7-uavklart"}
    for klasse, (loftbar, ikke) in UNRESOLVED.items():
        assert ikke == "H7"
        assert PREREG_TABLE[ikke] == "nei"
        assert PREREG_TABLE[loftbar] != "nei", f"{loftbar} skal være den løftbare siden"


def test_ikke_treff_har_ingen_loftbarhet():
    for n in NON_HITS:
        with pytest.raises(UnknownClass):
            liftability(n)


def test_ukjent_klasse_feiler():
    with pytest.raises(UnknownClass):
        liftability("H10")


def test_uavklarte_regnes_ikke_inn_i_loftbar_andel():
    """Nevneren for løftbar andel er avklarte treff, ikke alle treff."""
    r = liftable_share(["H1", "H1", "H7", "H8", "H1/H7-uavklart", "H1/H7-uavklart", "N3"])
    assert r["n_hits"] == 6           # N3 er ikke et treff
    assert r["n_resolved"] == 4
    assert r["n_unresolved"] == 2
    assert r["n_liftable"] == 2       # to H1
    assert r["share_liftable_of_resolved"] == 0.5
    assert r["share_unresolved_of_hits"] == pytest.approx(2 / 6)


def test_begge_tall_rapporteres_sammen():
    linje = format_liftable(["H1", "H7", "H5/H7-uavklart"])
    t = Corpus("rapport", [linje])
    t.must_hit("løftbar")
    t.must_hit("uavklart")
    t.must_hit("av avklarte")


def test_modulen_tilbyr_ingen_loftbar_andel_alene():
    import gjenopptak.classify as c

    for navn in dir(c):
        assert navn not in ("liftable_only", "share_liftable", "loftbar_andel")


def test_skjemaene_kjenner_de_nye_klassene():
    for navn in ("candidates", "claims"):
        s = load_schema(navn)
        enum = s["properties"]["obstacle_class"]["enum"]
        for k in UNRESOLVED:
            assert k in enum, (navn, k)
        felt = (s["properties"]["loftbarhet"]["items"]["properties"]["verdi"]
                if navn == "claims" else s["properties"]["liftable"])  # ADR-0010
        assert "uavklart" in felt["enum"], navn


def test_uavklart_kandidat_validerer_og_gal_kombinasjon_fanges():
    rec = {
        "schema_version": "candidates-1", "candidate_id": "W1:12", "sentence_id": "W1:12",
        "doc_id": "W1", "field_key": "klinisk_epidemiologi", "section_raw": "Potential confounders",
        "section_label_provenance": "source", "is_hit": True,
        "obstacle_class": "H1/H7-uavklart", "liftable": "uavklart",
        "liftability_table_version": "PREREG-v1-§5 + ADDENDUM-05",
        "judge": "owner", "judged_at": "2026-09-12T10:00:00+00:00",
        "unit": "sentence",
        "passage_span": {"start_index": 236, "end_index": 240, "n_sentences": 5, "window": 2},
    }
    validate("candidates", rec)
    rec["liftable"] = "kanskje"
    assert errors("candidates", rec)


def test_addendum05_forer_det_utloesende_funnet():
    from pathlib import Path

    add = Path(__file__).resolve().parent.parent / "ADDENDUM-05.md"
    t = Corpus("ADDENDUM-05", add.read_text(encoding="utf-8").splitlines())
    t.must_hit("10.1080/20008198.2017.1380470")
    t.must_hit("H1/H7-uavklart")
    t.must_hit("H2 / H7")
    t.must_hit("H3 / H7")
    t.must_hit("H5 / H7")
    t.must_hit("kjent for høyt")
    t.must_hit("regnes ikke inn i løftbar andel")
