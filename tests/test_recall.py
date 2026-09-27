"""Recall-fasiten og v2-mønstrene.

Armeringskravet: et nullresultat teller ikke før en streng som MÅ treffe har
truffet. Her betyr det at hver ny markør må treffe den faktiske setningen den
ble lest ut av. En markør som ikke gjør det, er skrevet fra fantasi.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from gjenopptak.extract import (
    OBSTACLE,
    FasitTreff,
    OBSTACLE_ADDITIONS,
    OBSTACLE_V2,
    UNDONE,
    UNDONE_ADDITIONS,
    UNDONE_V2,
    dekker,
    foer_og_etter,
    les_fasit,
    maal,
)
from gjenopptak.extract.passage import Passage
from gjenopptak.pipeline import MARKERS

ROOT = Path(__file__).resolve().parents[1]
FASIT = ROOT / "data/recall-sett.jsonl"

# ADR-0009: det store setningsmaterialet ligger på Vault, ikke på systemdisken.
# Uten montert volum hoppes testene over — de leses ikke fra en kopi et annet sted.
_VAULT = Path("/Volumes/Vault/gjenopptak-kilder/logs/pipeline-test")
SETNINGER = _VAULT / "sentences-PIPELINETEST.jsonl"
pytestmark = pytest.mark.skipif(
    not SETNINGER.exists(), reason="ADR-0009: setningsmaterialet ligger på Vault, som ikke er montert"
)

DØDE_I_RØRLEDNINGSTESTEN = (
    "did not attempt",
    "prevented me from",
    "no attempt was made",
    "we coded a random sample",
    "remains unread",
    "remains untranscribed",
    "have not been read",
    "have not been transcribed",
    "have not been collated",
    "have not been digiti",
)


# ---------------------------------------------------------------- armering


@pytest.mark.parametrize("mønster,doc_id,indeks,sitat", UNDONE_ADDITIONS)
def test_undone_tillegg_treffer_kildesetningen(mønster, doc_id, indeks, sitat):
    """Kontrollstreng: markøren må treffe setningen den kom fra."""
    assert re.search(mønster, sitat, re.I), f"{mønster!r} treffer ikke {doc_id} #{indeks}"


@pytest.mark.parametrize("mønster,doc_id,indeks,sitat", OBSTACLE_ADDITIONS)
def test_obstacle_tillegg_treffer_kildesetningen(mønster, doc_id, indeks, sitat):
    assert re.search(mønster, sitat, re.I), f"{mønster!r} treffer ikke {doc_id} #{indeks}"


def test_v2_inneholder_v1():
    """v2 skal utvide, ikke erstatte: alt v1 traff må v2 fortsatt treffe."""
    for s in ("we were unable to read it", "it was not possible", "could not be obtained"):
        assert UNDONE.search(s) and UNDONE_V2.search(s)
    for s in ("because of the workload", "owing to restricted access"):
        assert OBSTACLE.search(s) and OBSTACLE_V2.search(s)


def test_v1_er_urort():
    """v1 produserte rørledningstestens tall og skal kunne reproduseres."""
    assert UNDONE.search("was not possible")
    assert not UNDONE.search("has not been possible")   # nettopp bommen i fasiten
    assert not UNDONE.search("we cannot favour")
    assert not OBSTACLE.search("there were no similar data available")


# ------------------------------------------------------------------ fasit


def test_fasiten_har_advarsel_paa_topplinjen():
    første = json.loads(FASIT.read_text(encoding="utf-8").splitlines()[0])
    assert "IKKE UTVALGSDATA" in første["_warning"]
    assert "M1" in første["_warning"]


def test_fasiten_er_lesbar_og_konsistent():
    fasit = les_fasit(FASIT)
    assert len(fasit) == 28
    for t in fasit:
        assert t.start_index <= t.hit_index <= t.end_index
        assert t.unit == ("sentence" if t.start_index == t.end_index else "passage")
        assert t.begrunnelse.strip()
        assert t.klasse.startswith("H")


def test_fasitsitatene_er_verbatim_fra_L1():
    """Sitatene må være setningene fra L1-utdataene, ikke omskrevet."""
    fasit = les_fasit(FASIT)
    ønsket = {(t.doc_id, t.hit_index): t.sentence_text for t in fasit}
    funnet: dict[tuple[str, int], str] = {}
    with SETNINGER.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if "_warning" in r:
                continue
            k = (r["doc_id"], r["sentence_index"])
            if k in ønsket:
                funnet[k] = r["text"]
    assert funnet == ønsket


# --------------------------------------------------------------- måling


@pytest.fixture(scope="module")
def setninger():
    fasit = les_fasit(FASIT)
    docs = {t.doc_id for t in fasit}
    ut = {d: [] for d in docs}
    with SETNINGER.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if "_warning" in r:
                continue
            if r["doc_id"] in ut:
                ut[r["doc_id"]].append(r)
    for d in ut:
        ut[d].sort(key=lambda r: r["sentence_index"])
    return ut


def test_v1_fanger_ingenting_v2_fanger_alt(setninger):
    """Selve funnet: filteret slik det sto, fant null i ikke-sirkulært stoff."""
    fasit = les_fasit(FASIT)
    res = foer_og_etter(setninger, fasit)
    assert len(res["v1"].fanget) == 0
    assert len(res["v2"].bom) == 0
    assert res["v2"].recall > res["v1"].recall


def test_presisjon_er_under_en(setninger):
    """v2 er en kandidatgenerator, ikke en dommer: falske positive skal finnes."""
    fasit = les_fasit(FASIT)
    m = foer_og_etter(setninger, fasit)["v2"]
    assert 0.0 < m.presisjon < 1.0


def test_maal_krever_setninger_for_alle_fasitdokumenter(setninger):
    fasit = les_fasit(FASIT)
    delvis = {k: v for k, v in list(setninger.items())[:3]}
    with pytest.raises(ValueError, match="mangler setninger"):
        maal(delvis, fasit)


def test_dekker_krever_samme_dokument():
    p = Passage(doc_id="A", hit_index=10, start_index=8, end_index=12, window=2,
                unit="sentence", text="", sentence_text="", section_raw="",
                section_label_provenance="source")
    fasit = les_fasit(FASIT)[0]
    assert not dekker(p, fasit)


# -------------------------------------------------- de ti døde markørene


def test_de_ti_dode_markorene_star_fortsatt_i_listen():
    """De er døde i dette stoffet, men stoffet mangler sjangeren de dekker.

    Ingen av de 30 dokumentene er en diplomatisk kildeutgivelse eller et
    katalogarbeid, og det er der «remains unread» og «have not been
    transcribed» hører hjemme. Null treff på 28 fasitpassasjer og 1,07 millioner
    tegn gir ikke grunnlag for å fjerne dem. Fjerning krever en fasit som
    inneholder sjangeren.
    """
    for m in DØDE_I_RØRLEDNINGSTESTEN:
        assert m in MARKERS
        assert UNDONE_V2.search(m), f"{m} skal fortsatt være dekket av mønsteret"


def test_dode_markorer_er_dode_ogsaa_mot_fasiten():
    fasit = les_fasit(FASIT)
    tekst = " ".join(t.passage_text for t in fasit)
    for m in DØDE_I_RØRLEDNINGSTESTEN:
        assert not re.search(re.escape(m), tekst, re.I)
    # armering: en markør som MÅ finnes i fasitteksten
    assert re.search("was not possible", tekst, re.I)


# ------------------------------------------------ hvilken side som sviktet


def _rader(*setninger):
    return [{"doc_id": "A", "sentence_index": i, "text": t,
             "section_label_provenance": "source"} for i, t in enumerate(setninger)]


def _treff(i):
    return FasitTreff(doc_id="A", hit_index=i, start_index=i, end_index=i,
                      klasse="H7", unit="sentence", sentence_text="",
                      passage_text="", begrunnelse="", grensetilfelle=False)


def test_bomfordeling_skiller_de_tre_tilfellene():
    from gjenopptak.extract import bomfordeling
    setn = {"A": _rader(
        "We were unable to do it, and the sky was blue.",        # 0 markør, ingen hindring
        "The work stopped because of the workload.",             # 1 hindring, ingen markør
        "Nothing of interest is stated in this sentence at all.",  # 2 ingen av dem
    )}
    b = bomfordeling(setn, [_treff(0), _treff(1), _treff(2)],
                     undone=UNDONE, obstacle=OBSTACLE, window=0)
    assert b.as_dict() == {"bare_ugjort": 1, "bare_hindring": 1, "begge": 1}
    assert b.bare_hindring[0].hit_index == 0
    assert b.bare_ugjort[0].hit_index == 1
    assert b.begge[0].hit_index == 2


def test_bomfordeling_bruker_vinduet_for_hindringen():
    from gjenopptak.extract import bomfordeling
    setn = {"A": _rader(
        "We were unable to complete the coding of every record.",
        "This was because of the workload in the department.",
    )}
    # med vindu 0 faller hindringen utenfor; med vindu 2 er den inne
    assert bomfordeling(setn, [_treff(0)], undone=UNDONE, obstacle=OBSTACLE,
                        window=0).as_dict()["bare_hindring"] == 1
    assert bomfordeling(setn, [_treff(0)], undone=UNDONE, obstacle=OBSTACLE,
                        window=2).as_dict() == {"bare_ugjort": 0, "bare_hindring": 0,
                                                "begge": 1}


def test_marker_hits_teller_i_python():
    from gjenopptak.extract import marker_hits
    setn = {"A": _rader("It remains unread in the archive.",
                        "The file remains unread, and unreadable.",
                        "Nothing here.")}
    t = marker_hits(setn, ["remains unread", "have not been transcribed"])
    assert t == {"remains unread": 2, "have not been transcribed": 0}
