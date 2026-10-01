"""Leser-protokollen: validering fyller aldri ut, og partimeldingen bærer id-rekkefølgen."""
from gjenopptak.kjede.leser import KLASSER, SKJEMA, CCLeser, LokalLeser, partimelding, valider


def _dom(i, treff=False, klasse="INGEN"):
    return {"id": i, "ekte_treff": treff, "min_klasse": klasse, "min_bedømbar": None,
            "tvil": False, "begrunnelse": "x"}


def test_valider_beholder_første_gyldige_og_fyller_ikke_ut():
    parti = [{"id": "PS-001", "tekst": "a"}, {"id": "PS-002", "tekst": "b"}, {"id": "PS-003", "tekst": "c"}]
    rå = [_dom("PS-002", True, "H7"), _dom("PS-002"), _dom("PS-999"), _dom("PS-001", klasse="UKJENT")]
    dommer, ugyldige = valider(rå, parti)
    assert [d["id"] for d in dommer] == ["PS-002"]
    assert dommer[0]["ekte_treff"] is True          # første dom vinner, dubletten ignoreres
    assert ugyldige == ["PS-001", "PS-003"]          # ukjent klasse og manglende id er ugyldige


def test_partimelding_navngir_rekkefolgen():
    m = partimelding([{"id": "PS-001", "tekst": "t1"}, {"id": "PS-002", "tekst": "t2"}], 3, 16)
    assert "Parti 3 av 16" in m and "PS-001, PS-002" in m and "### PS-002\nt2" in m


def test_skjemaet_tvinger_kodernes_felter_og_klasser():
    item = SKJEMA["properties"]["dommer"]["items"]
    assert item["required"] == ["id", "ekte_treff", "min_klasse", "min_bedømbar", "tvil", "begrunnelse"]
    assert item["properties"]["min_klasse"]["enum"] == list(KLASSER)
    assert "H1/H7-uavklart" in KLASSER and "H2/H7-uavklart" not in KLASSER


def test_to_implementasjoner_samme_form():
    lok = LokalLeser(modell="m", vekt_sha256="0" * 64, instruks="i")
    cc = CCLeser(modell="claude-opus-5", rot=__import__("pathlib").Path("."))
    for l in (lok, cc):
        assert callable(l) and isinstance(l.signatur(), dict) and l.navn
