"""L1: JATS → setninger. Kontrollstrengen står i en resultatseksjon.

Ingen påstand om at noe *mangler* gjøres i denne filen før kontrollstrengen
har truffet. Se control.py.
"""

import pytest
from control import Corpus
from fixtures import CONTROL_SENTENCE, JATS_CONTROL, LIMITATIONS_SENTENCE, UNTITLED_SENTENCE

from gjenopptak.parse import normalize_section, sentences_from_jats, write_sentences
from gjenopptak.schemas import validate


@pytest.fixture(scope="module")
def rows() -> list[dict]:
    return sentences_from_jats(JATS_CONTROL.encode("utf-8"), doc_id="WTEST")


@pytest.fixture()
def tekst(rows) -> Corpus:
    return Corpus.from_records("sentences.text", rows, "text")


def test_kontrollstrengen_traff(tekst):
    """MÅ treffe. Traff den ikke, er parseren ødelagt og alt annet er verdiløst."""
    assert tekst.must_hit(CONTROL_SENTENCE) == 1


def test_kontrollsetningen_bar_raa_resultatseksjon(rows, tekst):
    tekst.must_hit(CONTROL_SENTENCE)
    treff = [r for r in rows if CONTROL_SENTENCE in r["text"]]
    assert len(treff) == 1
    r = treff[0]
    # ADR-0002: rå etikett, med nummerering, uendret.
    assert r["section_raw"] == "3. Results"
    assert r["section_id_raw"] == "s3"
    assert r["section_type_raw"] == "results"
    assert r["section_path_raw"] == ["3. Results"]
    # Normaliseringen er additiv og står ved siden av originalen.
    assert r["section_norm"] == "results"
    assert r["section_norm_rule"] == "substring:results"


def test_hele_teksten_skannes_ikke_bare_limitations(rows, tekst):
    """Kontrollen ligger utenfor limitations; begge skal være med."""
    tekst.must_hit(CONTROL_SENTENCE)
    tekst.must_hit(LIMITATIONS_SENTENCE)
    seksjoner = {r["section_raw"] for r in rows}
    for ventet in ("Abstract", "1. Introduction", "2. MATERIALS AND METHODS", "3. Results",
                   "3.1 Sub-hourly behaviour", "4. Discussion and limitations", "Data availability"):
        assert ventet in seksjoner, (ventet, sorted(seksjoner))


def test_versaler_og_nummerering_bevares_raa(rows, tekst):
    tekst.must_hit(CONTROL_SENTENCE)
    seksjon = Corpus.from_records("section_raw", rows, "section_raw")
    assert seksjon.must_hit("2. MATERIALS AND METHODS", exact=True) >= 1
    # Normaliseringen har gjort sitt, men har ikke rørt originalen:
    assert normalize_section("2. MATERIALS AND METHODS")[0] == "methods"
    seksjon.expect_none("2. Materials and methods", exact=True)


def test_seksjon_uten_tittel_gir_tom_raa_etikett(rows, tekst):
    tekst.must_hit(UNTITLED_SENTENCE)
    treff = [r for r in rows if UNTITLED_SENTENCE in r["text"]]
    assert len(treff) == 1
    assert treff[0]["section_raw"] == ""
    assert treff[0]["section_norm"] == "unknown"
    assert treff[0]["section_norm_rule"] == "empty_label"


def test_figurtekst_og_abstract_er_med(rows, tekst):
    tekst.must_hit(CONTROL_SENTENCE)
    assert tekst.must_hit("Load duration curve") == 1
    assert tekst.must_hit("We document an open data platform") == 1
    typer = {r["block_kind"] for r in rows}
    assert {"p", "title", "caption"} <= typer, sorted(typer)


def test_forkortelse_splitter_ikke_setningen(tekst):
    """«e.g.» og «Fig. 2» skal ikke gi tre setninger."""
    assert tekst.must_hit("Open data has grown, e.g. in the power sector.") == 1
    tekst.expect_none("in the power sector. Fig")


def test_ingen_setning_er_tom_og_indeks_er_sammenhengende(rows, tekst):
    tekst.must_hit(CONTROL_SENTENCE)
    assert rows, "ingen setninger — armeringen over skulle ha fanget dette"
    assert [r["sentence_index"] for r in rows] == list(range(len(rows)))
    assert all(r["text"].strip() for r in rows)
    assert all(r["char_end"] > r["char_start"] for r in rows)
    assert len({r["sentence_id"] for r in rows}) == len(rows)


def test_alle_rader_validerer_mot_skjemaet(rows):
    for r in rows:
        validate("sentences", r)


def test_skriving_til_jsonl_er_radvis_og_utf8(rows, tekst, tmp_path):
    tekst.must_hit(CONTROL_SENTENCE)
    ut = tmp_path / "sentences.jsonl"
    n = write_sentences(rows, ut)
    assert n == len(rows)
    linjer = ut.read_text(encoding="utf-8").splitlines()
    assert len(linjer) == n
    fra_fil = Corpus("jsonl", linjer)
    fra_fil.must_hit(CONTROL_SENTENCE)
    fra_fil.must_hit('"section_raw":"3. Results"'.replace('":"', '": "'))


def test_fil_paa_disk_gir_samme_resultat(tmp_path):
    """Fixturen skrives til disk fordi *.xml aldri committes (.gitignore)."""
    p = tmp_path / "kontroll.xml"
    p.write_text(JATS_CONTROL, encoding="utf-8")
    rows = sentences_from_jats(p.read_bytes(), doc_id="WTEST")
    Corpus.from_records("fra_disk", rows, "text").must_hit(CONTROL_SENTENCE)


def test_jats_gir_provenance_source(rows, tekst):
    """JATS-seksjonen er kildens egen merking (ADR-0007)."""
    tekst.must_hit(CONTROL_SENTENCE)
    prov = Corpus.from_records("provenance", rows, "section_label_provenance")
    assert prov.must_hit("source", exact=True) == len(rows)
    prov.expect_none("parser", exact=True)
    assert all(r["parser_version"] is None for r in rows)
    assert all(r["parser_model_version"] is None for r in rows)


def test_seksjon_uten_tittel_er_ogsaa_source(rows, tekst):
    """At en seksjon mangler tittel, er kildens opplysning — ikke vår gjetning."""
    tekst.must_hit(UNTITLED_SENTENCE)
    treff = [r for r in rows if UNTITLED_SENTENCE in r["text"]]
    assert treff[0]["section_raw"] == ""
    assert treff[0]["section_label_provenance"] == "source"


# ---------------------------------------------------------------------------
# Determinisme: ADDENDUM-07. `seen` holdt id(el) for lxml-proxyer; en frigjort
# proxy-id kunne gå til et annet element, og hele <body> ble tatt for et
# <front> som alt var gått gjennom. Samme XML ga 537 setninger fire ganger og
# 20 den femte.
# ---------------------------------------------------------------------------

def _jats_med_stor_front(n_forfattere: int = 40, n_avsnitt: int = 300) -> bytes:
    forf = "".join(
        f'<contrib contrib-type="author"><name><surname>S{i}</surname>'
        f'<given-names>G{i}</given-names></name><xref ref-type="aff" rid="a{i}"/></contrib>'
        for i in range(n_forfattere))
    aff = "".join(f'<aff id="a{i}"><institution>Inst {i}</institution>'
                  f'<country>X</country></aff>' for i in range(n_forfattere))
    avs = "".join(f"<p>Paragraph {i} reports the work in some detail. "
                  f"It has two sentences.</p>" for i in range(n_avsnitt))
    return (
        '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
        f'<front><journal-meta><journal-id>j</journal-id></journal-meta><article-meta>'
        f'<contrib-group>{forf}</contrib-group>{aff}'
        '<abstract><p>This is the abstract. It is short.</p></abstract>'
        '</article-meta></front>'
        f'<body><sec><title>Methods</title>{avs}</sec></body>'
        '<back><ref-list><ref><mixed-citation>R.</mixed-citation></ref></ref-list></back>'
        '</article>').encode()


def _gammel_blocks_from_jats(xml: bytes):
    """Den gamle algoritmen, ordrett, som kontroll. Skal ikke brukes i koden."""
    from lxml import etree
    from gjenopptak.parse import jats as J
    parser = etree.XMLParser(recover=False, resolve_entities=False,
                             no_network=True, load_dtd=False)
    root = etree.fromstring(xml, parser=parser)
    blocks, seen = [], set()
    for want in ("front", "body", "back"):
        for el in root.iter():
            if isinstance(el.tag, str) and J._localname(el) == want and id(el) not in seen:
                seen.add(id(el))
                J._walk(el, [], blocks)
    return blocks


def test_armering_den_gamle_algoritmen_mister_kroppen():
    """Kontrollen må vise feilen, ellers beviser den nye testen ingenting."""
    xml = _jats_med_stor_front()
    antall = set()
    for _ in range(200):
        _ = [object() for _ in range(300)]
        antall.add(len(_gammel_blocks_from_jats(xml)))
    assert min(antall) < 300, (
        "kontrollen fyrte ikke: den gamle id()-algoritmen mistet ikke <body> "
        f"på fiksturen (så {sorted(antall)}). Testen under er da ikke armert.")


def test_blocks_from_jats_er_deterministisk_og_komplett():
    from gjenopptak.parse import jats as J
    xml = _jats_med_stor_front()
    antall = set()
    for i in range(200):
        _ = [object() for _ in range(300)]
        if i % 50 == 0:
            import gc
            gc.collect()
        antall.add(len(J.blocks_from_jats(xml)))
    assert antall == {302}, f"ventet 302 blokker hver gang, fikk {sorted(antall)}"


def test_samme_xml_gir_samme_setninger():
    from gjenopptak.parse.jats import sentences_from_jats
    xml = _jats_med_stor_front()
    forste = [r["text"] for r in sentences_from_jats(xml, doc_id="D")]
    for _ in range(50):
        _ = [object() for _ in range(300)]
        assert [r["text"] for r in sentences_from_jats(xml, doc_id="D")] == forste
