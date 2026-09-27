"""L3-kontrakten. Dommeren er en fast stub — ingen modell kjøres."""

import pytest

from gjenopptak.classify import (
    SIGNATURE_FIELDS,
    VALID_CLASSES,
    JudgeError,
    Verdict,
    check_signature,
    check_verdict,
    judge_passage,
)
from gjenopptak.extract import Passage
from gjenopptak.schemas import validate


def passasje(unit="sentence", prov="source", section="3. Results") -> Passage:
    return Passage(doc_id="PMC1", hit_index=12, start_index=10, end_index=14,
                   window=2, unit=unit, text="… fordi arbeidet var for stort …",
                   sentence_text="We could not code all records because the workload was too large.",
                   section_raw=section, section_label_provenance=prov)


class Stub:
    """Fast dommer. Svarer det den er satt opp til, uten modell."""

    def __init__(self, verdict: Verdict, name: str = "owner"):
        self.verdict, self.name = verdict, name

    def __call__(self, passage: Passage) -> Verdict:
        return self.verdict


SIG = {"model_id": "stub:1", "weights_sha256": "a" * 64, "temperature": 0.0,
       "seed": 7, "keep_alive": 0, "runtime": "stub-0", "prompt_sha256": "b" * 64,
       "judged_at": "2026-09-12T10:00:00+00:00"}


def test_kontrakten_kjenner_alle_klassene_og_ingen_andre():
    assert len(VALID_CLASSES) == 17
    for k in ("H1", "H9", "H1/H7-uavklart", "H5/H7-uavklart", "N1", "N3", "UNSURE"):
        assert k in VALID_CLASSES
    assert "H10" not in VALID_CLASSES


def test_eieren_trenger_ingen_signatur():
    post = judge_passage(passasje(), Stub(Verdict("H1", True)), field_key="arkeologi")
    validate("candidates", post)
    assert post["judge"] == "owner" and post["liftable"] == "ja"


def test_modell_uten_signatur_avvises():
    """ADR-0003: mangler signaturen, telles ikke oppføringen."""
    with pytest.raises(JudgeError) as e:
        judge_passage(passasje(), Stub(Verdict("H1", True), name="local:m"),
                      field_key="arkeologi")
    assert "modellsignatur" in str(e.value)


def test_signatur_krever_keep_alive_null():
    d = dict(SIG, keep_alive=300)
    with pytest.raises(JudgeError):
        check_signature("local:m", d)
    check_signature("local:m", SIG)


def test_signatur_krever_alle_feltene():
    for f in SIGNATURE_FIELDS:
        d = {k: v for k, v in SIG.items() if k != f}
        with pytest.raises(JudgeError) as e:
            check_signature("local:m", d)
        assert f in str(e.value)


def test_loftbarhet_slaas_opp_ikke_av_dommeren():
    """ADR-0004: dommeren foreslår klasse, aldri løftbarhet."""
    for klasse, ventet in (("H1", "ja"), ("H5", "delvis"), ("H7", "nei"),
                           ("H3", "ja_med_forbehold")):
        post = judge_passage(passasje(), Stub(Verdict(klasse, True)), field_key="arkeologi")
        assert post["liftable"] == ventet, klasse


def test_uavklart_gir_uavklart_og_merkes_usikker():
    """ADDENDUM-05: uavklart arver ikke den løftbare naboens verdi."""
    post = judge_passage(passasje(), Stub(Verdict("H1/H7-uavklart", True)),
                         field_key="klinisk_epidemiologi")
    validate("candidates", post)
    assert post["liftable"] == "uavklart"
    assert post["unsure"] is True


def test_ikke_treff_har_ingen_loftbarhet():
    post = judge_passage(passasje(), Stub(Verdict("N3", False)), field_key="arkeologi")
    validate("candidates", post)
    assert post["is_hit"] is False and post["liftable"] == "usikker"


def test_selvmotsigende_svar_avvises():
    with pytest.raises(JudgeError):
        check_verdict(Verdict("N1", True))        # ikke-treff kan ikke være treff
    with pytest.raises(JudgeError):
        check_verdict(Verdict("H1", False))       # hindringsklasse må være treff
    with pytest.raises(JudgeError):
        check_verdict(Verdict("H10", True))       # ukjent klasse
    with pytest.raises(JudgeError):
        check_verdict(Verdict("H1", True, judgeable="kanskje"))


def test_passasjen_baerer_enhet_seksjon_og_opphav_videre():
    """ADR-0002, ADR-0007 og ADDENDUM-03 §1 følger posten."""
    post = judge_passage(passasje(unit="passage", prov="parser", section=""),
                         Stub(Verdict("H4", True)), field_key="arkeologi")
    post["parser_version"] = "grobid-0.8.1"
    post["parser_model_version"] = "BidLSTM_CRF-2024-04"
    validate("candidates", post)
    assert post["unit"] == "passage"
    assert post["section_label_provenance"] == "parser"
    assert post["passage_span"]["window"] == 2


def test_ingen_modell_og_ingen_nett_i_modulen():
    """L3-stillaset skal ikke kunne kjøre en modell ved uhell."""
    import inspect

    from gjenopptak.classify import judge as j

    kode = inspect.getsource(j)
    for forbudt in ("import httpx", "requests", "urllib", "ollama", "openai", "subprocess"):
        assert forbudt not in kode, forbudt


# --------------------------------------------------------------------------- #
# L4: siteringsdekning uten OpenAlex
# --------------------------------------------------------------------------- #

def test_l4_bruker_ikke_openalex():
    """Siteringssjekken skal ikke koste kvote."""
    import inspect

    from gjenopptak.falsify import citations as cit

    kode = inspect.getsource(cit)
    # Det som betyr noe er om modulen kan KALLE OpenAlex, ikke om den nevner det.
    assert "api.openalex.org" not in kode
    assert "openalex.org" not in kode.replace("OpenAlex' ``cites:``", "")
    assert "api.crossref.org" in kode
    assert "europepmc" in kode


def test_l4_armeres_mot_kjent_sitert_verk():
    from gjenopptak.falsify import ARM_DOI, ArmingFailed, citations as cit

    assert ARM_DOI.startswith("10.")
    assert cit.ARM_MIN_CROSSREF >= 50 and cit.ARM_MIN_EPMC >= 20
    assert issubclass(ArmingFailed, AssertionError)


def test_dekningsgraden_har_begge_nevnere():
    """PREREG §8 spør om andel siterende med fulltekst; Crossref gir totalen."""
    from gjenopptak.falsify import CitationCoverage

    r = CitationCoverage(doi="10.1/x", crossref_count=391, epmc_citing=194,
                         epmc_citing_ft=75, epmc_citing_oa=66)
    assert abs(r.epmc_share_of_crossref - 194 / 391) < 1e-9
    assert abs(r.fulltext_share - 75 / 194) < 1e-9
    assert abs(r.searchable_share_of_all - 75 / 391) < 1e-9


def test_manglende_tall_gir_none_ikke_null():
    """Et ukjent tall skal ikke se ut som en målt null."""
    from gjenopptak.falsify import CitationCoverage

    r = CitationCoverage(doi="10.1/x")
    assert r.epmc_share_of_crossref is None
    assert r.fulltext_share is None
