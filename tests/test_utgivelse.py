"""Utgivelsesbyggeren: flate navn, filkart mot forrige versjon, og blindfiler uten tekst."""
import hashlib
import json

from gjenopptak.utgivelse import Fil, blindindeks, filkart, flatt


def test_flatt_navn_folger_forrige_versjon():
    # v0.3.0 bar «decisions-0001-…»; saker og toppnivå må ikke kollidere.
    assert flatt("docs/decisions/0001-korpusgrense-aapen-fulltekst.md") == \
        "decisions-0001-korpusgrense-aapen-fulltekst.md"
    assert flatt("docs/saker/SAK-08/LUKKET.md") == "saker-SAK-08-LUKKET.md"
    assert flatt("docs/LAERDOM.md") == "LAERDOM.md"
    assert flatt("ADDENDUM-01.md") == "ADDENDUM-01.md"


def test_filkart_skiller_uendret_endret_ny_fjernet():
    nye = [Fil("a.md", "x", 1, "s", "m1"), Fil("b.md", "x", 1, "s", "NY"), Fil("c.md", "x", 1, "s", "m3")]
    forrige = {"a.md": {"bytes": 1, "md5": "m1"}, "b.md": {"bytes": 1, "md5": "m2"},
               "d.md": {"bytes": 1, "md5": "m4"}, "__versjon__": {"bytes": 0, "md5": "0.3.0"}}
    k = filkart(nye, forrige)
    assert k["forrige_versjon"] == "0.3.0"
    assert (k["uendret"], k["endret"], k["ny"], k["fjernet"]) == (["a.md"], ["b.md"], ["c.md"], ["d.md"])


def test_blindindeks_bærer_ikke_tekst(tmp_path):
    (tmp_path / "b").mkdir()
    tekst = "We could not date the layer."
    (tmp_path / "b" / "blind.jsonl").write_text(json.dumps({"id": "PS-001", "tekst": tekst}) + "\n")
    (tmp_path / "b" / "nokkel.jsonl").write_text(json.dumps(
        {"id": "PS-001", "doc_id": "W1", "start_index": 3, "end_index": 7, "felt": "arkeologi"}) + "\n")
    ix = blindindeks(tmp_path, "t", "b/blind.jsonl", "b/nokkel.jsonl")
    assert ix["rader"] == 1
    rad = ix["indeks"][0]
    assert "tekst" not in rad
    assert rad["tekst_sha256"] == hashlib.sha256(tekst.encode()).hexdigest()
    assert tekst not in json.dumps(ix, ensure_ascii=False)


def test_ekskluderingslisten_beholder_bare_nyeste_utkast():
    from gjenopptak.utgivelse import utelat
    stier = ["docs/MANUSKRIPT-v2-UTKAST.md", "docs/MANUSKRIPT-v2.1-UTKAST.md", "docs/MANUSKRIPT-v2.10-UTKAST.md",
             "docs/MANUSKRIPT-v2.5-UTKAST.md", "docs/MANUSKRIPT-v0.1.md", "docs/INSTRUKSER-v1.3.md",
             "docs/patch/MASTER-x.md", "docs/ROADMAP.md", "docs/BYGGEPLAN.md", "docs/METODE.md",
             "docs/MASTER-PATCH-2026-09-26.md"]
    beholdt, utelatt = utelat(stier)
    # v2.10 er nyere enn v2.5: sammenligningen er numerisk, ikke leksikografisk
    assert "docs/MANUSKRIPT-v2.10-UTKAST.md" in beholdt
    assert set(utelatt) == {"docs/MANUSKRIPT-v2-UTKAST.md", "docs/MANUSKRIPT-v2.1-UTKAST.md",
                            "docs/MANUSKRIPT-v2.5-UTKAST.md", "docs/INSTRUKSER-v1.3.md",
                            "docs/patch/MASTER-x.md", "docs/ROADMAP.md", "docs/BYGGEPLAN.md"}
    assert {"docs/MANUSKRIPT-v0.1.md", "docs/METODE.md", "docs/MASTER-PATCH-2026-09-26.md"} <= set(beholdt)


def test_ekskluderingslisten_v2_ferdig_manus_fortrenger_utkastet_og_preprintkilden_holdes_ute():
    from gjenopptak.utgivelse import utelat
    stier = ["docs/MANUSKRIPT-v2.7-UTKAST.md", "docs/MANUSKRIPT-v2.8-UTKAST.md", "docs/MANUSKRIPT-v2.9.md",
             "docs/MANUSKRIPT-FAKTA-2026-09-28.md", "docs/PREPRINT.md", "docs/PREPRINT-v2.md"]
    beholdt, utelatt = utelat(stier)
    assert set(utelatt) == {"docs/MANUSKRIPT-v2.7-UTKAST.md", "docs/MANUSKRIPT-v2.8-UTKAST.md",
                            "docs/PREPRINT-v2.md"}
    assert set(beholdt) == {"docs/MANUSKRIPT-v2.9.md", "docs/MANUSKRIPT-FAKTA-2026-09-28.md", "docs/PREPRINT.md"}


def test_zipgruppene_er_bare_nye_grupper_og_taket_er_zenodos():
    from gjenopptak.utgivelse import MAKS_FILER, _i_zip
    assert MAKS_FILER == 100                     # Zenodo: «exceeding the max amount per record», 01.10.2026
    assert _i_zip("git:abc:docs/saker/SAK-08/LUKKET.md", "saker-SAK-08-LUKKET.md") == ("saker.zip", "saker/SAK-08/LUKKET.md")
    assert _i_zip("git:abc:docs/FAKTASJEKK-MANUSKRIPT-v2.7-2026-09-30.md", "x")[0] == "faktasjekk-manuskript.zip"
    assert _i_zip("vault:oppdrag-gjenvunnet/OPPHAV.md", "oppdrag-gjenvunnet-OPPHAV.md") == ("oppdrag.zip", "oppdrag-gjenvunnet-OPPHAV.md")
    # filer som alt er deponert i v0.3.0, holdes utenfor zip
    assert _i_zip("git:abc:docs/decisions/0001-korpusgrense-aapen-fulltekst.md", "decisions-0001-x.md") is None
    assert _i_zip("git:abc:ADDENDUM-25.md", "ADDENDUM-25.md") is None
