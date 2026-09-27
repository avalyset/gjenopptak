"""Kontrollsøk uten OpenAlex-kvote, og kravene fra ADDENDUM-04 §4."""

import pytest
from control import Corpus

from gjenopptak.harvest import controlsearch as cs
from gjenopptak.harvest import fetchtest as ft


def test_soekeformene_dekker_begge_klassene():
    assert len(cs.PHRASES_H1) >= 8 and len(cs.PHRASES_H4) >= 6
    h1 = Corpus("H1", list(cs.PHRASES_H1))
    h1.must_hit("coded")           # manuell koding
    h1.must_hit("manual review")
    h4 = Corpus("H4", list(cs.PHRASES_H4))
    h4.must_hit("images")
    h4.must_hit("segment")


def test_eget_arbeid_kreves():
    """ADDENDUM-04 §4: det ugjorte må tilhøre arbeidet som rapporteres."""
    ja = "We manually coded 500 of the 4000 records because coding all was infeasible."
    assert cs.OWN_WORK.search(ja) and not cs.THIRD_PARTY.search(ja)


def test_organisasjonens_praksis_avvises():
    """Setningen som felte H1-kontrollen i ADDENDUM-04 §4."""
    nei = ("3ie does not conduct critical appraisal of primary studies on the grounds "
           "that it would be too time consuming.")
    assert not cs.OWN_WORK.search(nei), "ingen førsteperson — skal falle på OWN_WORK"


def test_andres_studier_avvises_selv_med_we():
    nei = "Most studies did not code all records, as we note above."
    assert cs.OWN_WORK.search(nei) and cs.THIRD_PARTY.search(nei)


def test_armeringsfrasen_peker_paa_et_kjent_verk():
    assert cs.ARMING_DOI.startswith("10.")
    assert "not feasible" in cs.ARMING_PHRASE


def test_vinduet_er_prereg_vinduet():
    assert cs.YEARS == (2015, 2020)


def test_manifestskillet_er_to_ulike_merker():
    """En fil hentet av rammeprøven er ikke en observasjon."""
    assert ft.FRAME_PROBE_TAG != ft.READ_TAG
    note = Corpus("note", ft.MANIFEST_NOTE.splitlines())
    note.must_hit("ikke lest")
    note.must_hit("fortsatt trekkbare")
    note.must_hit("gjensidig utelukkende")


def test_manifestnoten_skrives_bare_en_gang(tmp_path):
    raw = tmp_path / "raw"
    assert ft.ensure_manifest_note(raw) is True
    assert ft.ensure_manifest_note(raw) is False
    tekst = (raw / "MANIFEST.md").read_text(encoding="utf-8")
    assert tekst.count(ft.FRAME_PROBE_TAG) == 1


def test_hentbar_rammefil_bare_bestatte_sortert(tmp_path):
    vs = [
        ft.FetchVerdict("W3", "10.1/c", in_frame=True, gate="P3-PDF", chars=5000),
        ft.FetchVerdict("W1", "10.1/a", in_frame=True, gate="P1-JATS", chars=9000),
        ft.FetchVerdict("W2", "10.1/b", in_frame=False, gate="P3-PDF", status=403),
    ]
    n, digest = ft.write_frame_file(vs, tmp_path / "frame-HENTBAR.jsonl")
    assert n == 2
    linjer = (tmp_path / "frame-HENTBAR.jsonl").read_text(encoding="utf-8").splitlines()
    import json as _json
    assert [_json.loads(l)["work_id"] for l in linjer] == ["W1", "W3"]
    assert len(digest) == 64


def test_armeringen_kaster_naar_soeket_er_tomt(monkeypatch, tmp_path):
    """Et nullresultat uten arming er ikke et funn."""
    monkeypatch.setattr(cs, "search_phrase", lambda *a, **k: [])
    with pytest.raises(cs.ArmingFailed) as e:
        cs.arm(None, tmp_path)
    assert "ikke gyldig" in str(e.value)
