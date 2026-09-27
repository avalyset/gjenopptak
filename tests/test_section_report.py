"""ADR-0007 punkt 4: seksjonsfordeling rapporteres delt, aldri som ett tall."""

import pytest
from control import Corpus

from gjenopptak.registry import (
    ProvenanceMissing,
    format_table,
    rows_for_report,
    split_by_provenance,
)


def rad(section, prov, **over):
    r = {"section_raw": section, "section_label_provenance": prov}
    if prov == "parser":
        r.setdefault("parser_version", "grobid-0.8.1")
        r.setdefault("parser_model_version", "BidLSTM_CRF-2024-04")
    r.update(over)
    return r


ROWS = [
    rad("3. Results", "source"),
    rad("3. Results", "source"),
    rad("4. Discussion and limitations", "source"),
    rad("Results", "parser"),
    rad("", "parser"),
]


def test_tellingen_er_delt_i_to():
    split = split_by_provenance(ROWS)
    assert set(split) == {"source", "parser"}
    assert split["source"]["3. Results"] == 2
    assert split["parser"]["Results"] == 1
    assert split["parser"][""] == 1


def test_modulen_tilbyr_ingen_sammenslaatt_telling():
    """Regelen håndheves ved at funksjonen ikke finnes."""
    import gjenopptak.registry as reg

    for navn in dir(reg):
        assert "combined" not in navn and "samlet" not in navn and "total_count" not in navn


def test_post_uten_opphav_avvises():
    with pytest.raises(ProvenanceMissing):
        split_by_provenance([{"section_raw": "3. Results"}])
    with pytest.raises(ProvenanceMissing):
        split_by_provenance([rad("x", "grobid")])


def test_parser_uten_versjon_telles_ikke():
    with pytest.raises(ProvenanceMissing):
        split_by_provenance([rad("Results", "parser", parser_version=None)])
    with pytest.raises(ProvenanceMissing):
        split_by_provenance([rad("Results", "parser", parser_model_version="")])


def test_tabellen_har_to_kolonner_og_ingen_totalkolonne():
    tabell = Corpus("tabell", format_table(ROWS).splitlines())
    tabell.must_hit("n source")
    tabell.must_hit("n parser")
    tabell.must_hit("(uten tittel)")
    tabell.expect_none("n totalt")
    tabell.expect_none("| total |")


def test_raden_bevarer_begge_tallene_hver_for_seg():
    rader = {sc.section: sc for sc in rows_for_report(ROWS)}
    assert rader["3. Results"].as_row() == ("3. Results", 2, 0)
    assert rader["Results"].as_row() == ("Results", 0, 1)
    # De to «Results»-variantene er ikke samme rad: rå etikett bevares (ADR-0002).
    assert "3. Results" in rader and "Results" in rader


def test_adr0007_finnes_og_krever_deling():
    from pathlib import Path

    adr = Path(__file__).resolve().parent.parent / "docs/decisions/0007-seksjonsetikettens-opphav.md"
    tekst = Corpus("ADR-0007", adr.read_text(encoding="utf-8").splitlines())
    tekst.must_hit("section_label_provenance")
    tekst.must_hit("slås aldri")
    tekst.must_hit("parser_model_version")
    tekst.must_hit("Status:** Accepted")
