"""Recall-sett 2: kravene som håndheves før lesing.

Armeringskravet gjelder her også. Språkdetektoren prøves mot de tre språkene som
slapp gjennom stoppordheuristikken i sett 1 — spansk, gresk og italiensk — og mot
en engelsk setning som MÅ passere. Et krav som ikke er prøvd mot noe det skal
forkaste, er ikke et krav.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gjenopptak.harvest import recallset2 as r2


# ------------------------------------------------------------------ frø

def test_datoene_er_reproduserbare_og_i_vinduet():
    a = r2.seeded_dates(30)
    assert a == r2.seeded_dates(30), "samme frø må gi samme dager"
    assert len(a) == len(set(a)) == 30
    assert all(a[i] <= a[i + 1] for i in range(len(a) - 1)), "sortert"
    for d in a:
        assert f"{r2.YEAR_FROM}-01-01" <= d <= f"{r2.YEAR_TO}-12-31"


def test_annet_fro_gir_andre_dager():
    assert r2.seeded_dates(20) != r2.seeded_dates(20, seed=1)


def test_rekkefolgen_er_reproduserbar_og_ikke_identitet():
    xs = list(range(40))
    a = r2.seeded_order(xs)
    assert a == r2.seeded_order(xs)
    assert sorted(a) == xs, "ingen elementer tapt"
    assert a != xs, "frøet skal faktisk stokke"
    assert xs == list(range(40)), "originalen skal ikke røres"


# ----------------------------------------------------------- utelukkelse

def test_utelukkelse_treffer_paa_hver_identifikator(tmp_path):
    p = tmp_path / "u.json"
    p.write_text(json.dumps({"work": ["W1"], "pmcid": ["PMC9"],
                             "doi": ["https://doi.org/10.1/AB"], "pmid": ["7"]}))
    u = r2.Exclusions.from_json(p)
    assert u.hit(work="W1") == "work:W1"
    assert u.hit(pmcid="PMC9") == "pmcid:PMC9"
    assert u.hit(doi="10.1/ab") == "doi:10.1/ab"
    assert u.hit(doi="HTTPS://DOI.ORG/10.1/AB") == "doi:10.1/ab"
    assert u.hit(pmid="7") == "pmid:7"
    assert u.hit(pmcid="PMC8", doi="10.9/x") is None


def test_norm_doi():
    for inn in ("https://doi.org/10.1/A", "http://doi.org/10.1/A", "doi:10.1/A", " 10.1/a "):
        assert r2.norm_doi(inn) == "10.1/a"


# ----------------------------------------------------------------- språk

EN = ("The main limitation of this study was the lack of information about the "
      "women who chose to follow up in the private sector. We could not assess "
      "that group, and no comparable data were available from other structures.")
ES = ("El objetivo de este trabajo es analizar la estructura geometrica de la "
      "decoracion del mosaico de la antesala del oecus de la domus romana.")
IT = ("In questo lavoro si presentano i risultati delle indagini archeologiche "
      "condotte nel sito e si discutono le implicazioni per la cronologia.")
EL = ("Ο σκοπός της παρούσας εργασίας είναι να αναλύσει τη δομή των ευρημάτων "
      "και να παρουσιάσει τα αποτελέσματα της έρευνας στην περιοχή.")


def test_engelsk_passerer():
    v = r2.language_verdict(EN)
    assert v.ok and v.top == "en" and v.prob >= r2.MIN_EN_PROB
    assert v.nonlatin == 0.0


@pytest.mark.parametrize("tekst,ventet", [(ES, "es"), (IT, "it"), (EL, "el")])
def test_spraakene_sett_1_slapp_gjennom_forkastes(tekst, ventet):
    v = r2.language_verdict(tekst)
    assert not v.ok
    assert v.top == ventet
    assert v.grunn


def test_ikke_latinsk_skrift_forkastes_selv_om_detektoren_sier_engelsk():
    """Terskelen er uavhengig av detektoren: sett 1 slapp inn 69 % greske tegn."""
    v = r2.language_verdict(EL)
    assert v.nonlatin > 0.9
    assert "ikke-latinsk" in v.grunn


def test_kildeutgivelse_med_latinsk_kildetekst_og_engelsk_apparat_passerer():
    t = ("Ista carta testatur quod dominus rex concessit terram illam. " + EN +
         " The charter itself remains unread in a private archive.")
    v = r2.language_verdict(t)
    assert v.ok, "engelsk apparat rundt latinsk kildetekst skal stå"


def test_nonlatin_share_paa_tom_og_blandet_tekst():
    assert r2.nonlatin_share("") == 0.0
    assert r2.nonlatin_share("123 !!! ") == 0.0
    assert r2.nonlatin_share("abcd") == 0.0
    assert r2.nonlatin_share("abΑΒ") == 0.5


def test_detektorfeil_gir_forkastelse_ikke_unntak():
    v = r2.language_verdict("   \n  ")
    assert not v.ok and "detektor feilet" in v.grunn


# --------------------------------------------------------------- sjanger

@pytest.mark.parametrize("tittel,typer,ventet", [
    ("A systematic review of outcomes", (), "oversiktsartikkel"),
    ("Outcomes after surgery", ("Journal Article",), "forskningsartikkel"),
    ("The charters of Kirkwall: an edition", (), "kildeutgivelse"),
    ("Inscriptions of Roman Dacia", (), "kildeutgivelse"),
    ("Something", ("Dissertation",), "avhandling"),
])
def test_sjanger_fra_metadata(tittel, typer, ventet):
    assert r2.genre_from_metadata(title=tittel, pub_types=typer) == ventet


def test_sjanger_fra_konferansetidsskrift():
    assert r2.genre_from_metadata(title="X", journal="Proceedings of the ACM") == "konferansebidrag"


def test_alle_sjangre_er_kjente_verdier():
    for t in ("A review of X", "The charters: an edition", "Y", "A thesis"):
        assert r2.genre_from_metadata(title=t) in r2.SJANGRE


# ---------------------------------------------------------------- frafall

def test_frafall_teller_forkastelser_ikke_vurderinger():
    """«vurdert» uten valgt-tallet ville sett ut som om alle falt."""
    a = r2.Attrition()
    a.note("aar"); a.note("sprak"); a.note("sprak")
    d = a.as_dict()
    assert d["forkastet"] == 3 and d["per_kriterium"]["sprak"] == 2
    assert "vurdert" not in d, "antall vurderte kan ikke utledes av frafallet alene"
    assert a.as_dict(valgt=15) == {**d, "valgt": 15, "vurdert": 18}
    with pytest.raises(KeyError):
        a.note("noe-annet")


def test_aarskravet():
    assert r2.year_ok(2015) and r2.year_ok(2020)
    assert not r2.year_ok(2014) and not r2.year_ok(2021) and not r2.year_ok(None)


# ------------------------------------------------------------- uttrekk

def test_html_gir_avsnittsskille():
    """Uten skille smelter avsnitt sammen og setningsdeleren ser ett ord."""
    t = r2.html_to_text(b"<html><script>x</script><body><p>Hei der</p>"
                        b"<p>Du</p><div>Og</div></body></html>")
    assert "x" not in t
    assert t.split("\n\n") == ["Hei der", "Du", "Og"]


def test_html_paa_soppel_gir_tom_streng_ikke_unntak():
    assert r2.html_to_text(b"") == ""


def test_galley_pdf_foerst():
    html = ('<a href="/j/article/view/9">HTML</a>'
            '<a href="/j/article/view/9/77">PDF</a>'
            '<a href="/j/article/download/9/77">last ned</a>')
    lenker = r2.galley_links(html, "https://x.example/j/article/view/9")
    assert lenker, "skal finne galleyer"
    assert "/download/" in lenker[0], "nedlastingslenken skal komme først"


def test_sentences_from_text_har_parser_opphav_og_tom_seksjon():
    t = (EN + "\n\n" + "A second paragraph, long enough to pass the forty "
         "character floor in blocks_from_text.")
    rows = r2.sentences_from_text(t, doc_id="T1")
    assert len(rows) >= 3
    for r in rows:
        assert r["doc_id"] == "T1"
        assert r["section_raw"] == ""
        assert r["section_label_provenance"] == "parser"     # ADR-0007
        assert r["schema_version"] == "sentences-1"
    assert [r["sentence_index"] for r in rows] == list(range(len(rows)))


def test_kvotene_summerer_til_foerti():
    assert sum(r2.QUOTA.values()) == 40
    assert r2.QUOTA["humaniora"] == 15


def test_lcc_listen_dekker_sjangerhullet_fra_sett_1():
    koder = dict(r2.LCC_HUMANIORA)
    for kode in ("CD", "CN", "Z"):
        assert kode in koder, f"{kode} bærer kildearbeidssjangeren sett 1 manglet"


# --------------------------------- lengdekravet, rutespesifikt (ADDENDUM-07)

def test_setningsgulvet_gjelder_bare_html_ruten():
    """Landingssiden er HTML-rutens feilmodus, ikke JATS-rutens."""
    kort = [{}] * 40
    assert r2.passes_length(kort, "x" * 7000, "html") == "for-kort"
    assert r2.passes_length(kort, "x" * 7000, "jats") is None
    assert r2.passes_length(kort, "x" * 7000, "pdf") is None
    assert r2.passes_length([{}] * 80, "x" * 7000, "html") is None


def test_tegngulvet_gjelder_alle_ruter():
    for rute in ("html", "jats", "pdf"):
        assert r2.passes_length([{}] * 200, "x" * 500, rute) == "for-kort"


def test_body_text_dropper_tittelblokk_og_referanser():
    rader = [{"text": f"S{i}"} for i in range(100)]
    kropp = r2.body_text(rader)
    assert "S0" not in kropp.split() and "S4" not in kropp.split()
    assert "S5" in kropp.split() and "S74" in kropp.split()
    assert "S75" not in kropp.split(), "referansehalen skal være ute"


def test_body_text_paa_kort_dokument_gir_noe():
    rader = [{"text": f"S{i}"} for i in range(6)]
    assert r2.body_text(rader).strip(), "aldri tom for et dokument med innhold"


def test_kroppsspraak_fanger_det_helheten_slapp_gjennom():
    """En spanskspråklig kropp med engelsk sammendrag skal falle."""
    rader = ([{"text": EN}] * 6 +
             [{"text": ES}] * 40 +
             [{"text": EN}] * 10)
    hel = " ".join(r["text"] for r in rader)
    assert not r2.language_verdict(r2.body_text(rader)).ok, "kroppen er spansk"


def test_frafallsgrunnene_dekker_sprak_kropp():
    assert "sprak-kropp" in r2.REASONS
    a = r2.Attrition()
    a.note("sprak-kropp")
    assert a.as_dict()["per_kriterium"]["sprak-kropp"] == 1


def test_soppelandel_skiller_binaerforurensning():
    """En DOAJ-lenke til et Word-dokument ga 67 % binærsøppel med engelsk imellom."""
    assert r2.garbage_share("") == 0.0
    assert r2.garbage_share("Ren engelsk tekst uten noe rart.") == 0.0
    skitten = "Hei" + "�" * 60 + "\x00\x01"
    assert r2.garbage_share(skitten) > r2.MAX_GARBAGE
    assert "soppel" in r2.REASONS


def test_ojs_view_galley_skrives_om_til_download_foerst():
    """view/ID/GALLEY er en HTML-ramme; filen ligger på download/ID/GALLEY."""
    html = ('<a class="obj_galley_link pdf" '
            'href="https://j.example/index.php/DOCU/es/article/view/49745/46242">PDF</a>')
    lenker = r2.galley_links(html, "https://j.example/index.php/DOCU/es/article/view/49745")
    assert lenker[0] == "https://j.example/index.php/DOCU/es/article/download/49745/46242"
    assert "https://j.example/index.php/DOCU/es/article/view/49745/46242" in lenker


def test_landingsside_uten_galley_skrives_ikke_om():
    """view/ID uten galley-del er artikkelens landingsside, ikke en fil."""
    html = '<a href="https://j.example/j/article/view/68790">annen artikkel</a>'
    lenker = r2.galley_links(html, "https://j.example/j/article/view/1")
    assert not any("/download/" in u for u in lenker)


# ------------------------------------------------------------------ identitet

MOSUL = "Settlement Dynamics on the Banks of the Upper Tigris, Iraq: The Mosul Dam Reservoir Survey (1980)"


def test_identitet_riktig_dokument_passerer():
    tekst = ("Settlement dynamics on the banks of the Upper Tigris, Iraq. The Mosul Dam "
             "Reservoir Survey was carried out in 1980 by a joint team.")
    v = r2.identity_verdict(tekst, title=MOSUL, doi=None)
    assert v.ok and v.andel == 1.0 and not v.doi_funnet


def test_armering_feil_dokument_fra_samme_tidsskrift_forkastes():
    """Kontrollen: sidefeltets artikkel deler fagord med posten, men er en annen."""
    feil = ("This dataset presents a digital edition of a manuscript inventory of "
            "artefacts from excavations in Upper Egypt, with archaeological data.")
    v = r2.identity_verdict(feil, title=MOSUL, doi="10.5334/joad.63")
    assert not v.ok
    assert v.andel < r2.MIN_TITLE_SHARE and not v.doi_funnet


def test_armering_sitert_verk_forkastes():
    tittel = "Gestão da informação do estágio não obrigatório na coordenação de curso de pedagogia presencial da UFRN"
    feil = "The Value of an Internship Experience for Early Career Geographers. Introduction."
    assert not r2.identity_verdict(feil, title=tittel, doi=None).ok


def test_identitet_doi_brutt_over_linjer_teller():
    tekst = "Bulletin of the History of Archaeology, DOI: https://doi.\norg/10.5334/ bha-553"
    v = r2.identity_verdict(tekst, title="Helt annen tittel her", doi="https://doi.org/10.5334/bha-553")
    assert v.ok and v.doi_funnet


def test_identitet_diakritika_og_markup_foldes():
    tittel = "Política exterior ecuatoriana durante la <i>guerra</i> del Pacífico"
    tekst = "POLITICA EXTERIOR ECUATORIANA durante la guerra del Pacifico (1879-1884)"
    assert r2.identity_verdict(tekst, title=tittel).ok


def test_identitet_ordgrense_ikke_delstreng():
    """«data» i «database» skal ikke telle som tittelord."""
    v = r2.identity_verdict("database metadata", title="Open data survey", doi=None)
    assert v.andel == 0.0 and not v.ok


def test_identitet_kort_tittel_krever_doi():
    assert not r2.identity_verdict("Estadísticas anuales 2019", title="Estadísticas").ok
    assert r2.identity_verdict("Estadísticas doi:10.1/x", title="Estadísticas", doi="10.1/x").ok


def test_frafallsgrunnene_dekker_identitet():
    assert "identitet" in r2.REASONS
    a = r2.Attrition()
    a.note("identitet")
    assert a.as_dict()["per_kriterium"]["identitet"] == 1
