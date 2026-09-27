"""ADR-0010: løftbarhet er datert, og vurderingshistorikken er tilføyelsesbasert."""

import importlib

import pytest
from jsonschema import ValidationError

from gjenopptak.schemas import errors, validate

L = importlib.import_module("gjenopptak.classify.liftability")


def _claim(**over) -> dict:
    rec = {
        "schema_version": "claims-2",
        "claim_id": "CLAIM-T-1",
        "candidate_id": "CAND-T-1",
        "doc_id": "W1",
        "field_key": "arkeologi",
        "obstacle_class": "H2",
        "loftbarhet": [L.vurdering("H2", "2026-09-20", vurdert_av=L.OSS)],
        "falsified": False,
        "cites_coverage": {"fulltext_available": 1, "fulltext_total": 2, "coverage_ratio": 0.5},
        "tested_at": "2026-09-21T00:00:00+00:00",
        "section_raw": "Results",
        "section_label_provenance": "source",
        "unit": "passage",
        "passage_span": {"start_index": 10, "end_index": 14, "n_sentences": 5, "window": 2},
    }
    rec.update(over)
    return rec


def test_gyldig_oppfoering_slipper_gjennom():
    validate("claims", _claim())


def test_uten_vurdert_dato_avvises():
    v = L.vurdering("H2", "2026-09-20", vurdert_av=L.OSS)
    del v["vurdert_dato"]
    with pytest.raises(ValidationError):
        validate("claims", _claim(loftbarhet=[v]))
    with pytest.raises(ValueError):
        L.vurdering("H2", "20. september", vurdert_av=L.OSS)


def test_uten_tabellversjon_avvises():
    v = L.vurdering("H2", "2026-09-20", vurdert_av=L.OSS)
    del v["tabellversjon"]
    with pytest.raises(ValidationError):
        validate("claims", _claim(loftbarhet=[v]))
    with pytest.raises(ValueError):
        L.vurdering("H2", "2026-09-20", vurdert_av=L.OSS, tabellversjon="")


def test_tom_loftbarhetsliste_avvises():
    assert errors("claims", _claim(loftbarhet=[]))


def test_endring_av_eksisterende_vurdering_avvises():
    c = _claim()
    with pytest.raises(L.VurderingLaast):
        L.foey_til(c, L.vurdering("H8", "2026-09-20", vurdert_av=L.OSS, grunn="omkoding"))
    with pytest.raises(L.VurderingLaast):
        L.foey_til(c, L.vurdering("H8", "2019-01-01", vurdert_av=L.OSS))


def test_tilfoeyelse_beholder_den_gamle():
    c = _claim()
    ny = L.foey_til(c, L.vurdering("H8", "2026-09-25", vurdert_av=L.OSS, grunn="tilgangen falt bort",
                                   kilde="BL: Images currently unavailable"))
    assert len(ny["loftbarhet"]) == 2
    assert ny["loftbarhet"][0] == c["loftbarhet"][0], "den gamle vurderingen står urørt"
    assert len(c["loftbarhet"]) == 1, "den opprinnelige posten er ikke endret"
    assert L.gjeldende(ny["loftbarhet"])["obstacle_class"] == "H8"
    assert L.gjeldende(ny["loftbarhet"])["verdi"] == "nei"
    validate("claims", ny)


def test_parkert_kandidat_baerer_utloser():
    c = _claim(parkert={"utloser": "BL-bildene tilbake i åpen kanal",
                        "parkert_dato": "2026-09-25", "begrunnelse": "93 sider utilgjengelige"})
    validate("claims", c)
    assert errors("claims", _claim(parkert={"parkert_dato": "2026-09-25"})), "utløser er påkrevd"


def test_datoen_er_aldri_finere_enn_kilden(tmp_path):
    """ADR-0010 tillegg: ÅÅÅÅ og ÅÅÅÅ-MM er gyldige; en oppdiktet dag er ikke."""
    for dato, presisjon in (("2019", "år"), ("2019-11", "måned"), ("2026-09-25", "dag")):
        v = L.vurdering("H1", dato, vurdert_av=L.FORFATTERENS)
        assert v["datopresisjon"] == presisjon
        validate("claims", _claim(obstacle_class="H1", loftbarhet=[v]))
    feil = L.vurdering("H1", "2019-11", vurdert_av=L.OSS)
    feil["datopresisjon"] = "dag"
    assert errors("claims", _claim(loftbarhet=[feil])), "presisjonen må stemme med datoformen"


def test_vurdering_uten_eier_avvises():
    with pytest.raises(TypeError):
        L.vurdering("H2", "2026-09-20")          # vurdert_av er påkrevd argument
    with pytest.raises(ValueError):
        L.vurdering("H2", "2026-09-20", vurdert_av="")
    v = L.vurdering("H2", "2026-09-20", vurdert_av=L.OSS)
    del v["vurdert_av"]
    assert errors("claims", _claim(loftbarhet=[v]))
