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
                            "docs/patch/MASTER-x.md", "docs/ROADMAP.md", "docs/BYGGEPLAN.md",
                            "docs/MASTER-PATCH-2026-09-26.md"}          # versjon 3 (03.10.2026)
    assert {"docs/MANUSKRIPT-v0.1.md", "docs/METODE.md"} <= set(beholdt)


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
    # v0.5.0 (03.10.2026): ADR-ene pakkes i én zip for å holde posten under taket; addendaene står alene
    assert _i_zip("git:abc:docs/decisions/0001-korpusgrense-aapen-fulltekst.md", "decisions-0001-x.md") == (
        "decisions.zip", "0001-korpusgrense-aapen-fulltekst.md")
    assert _i_zip("git:abc:ADDENDUM-25.md", "ADDENDUM-25.md") is None


def test_ekskluderingslisten_v4_v3_fortrenger_alle_v2_og_v01_star():
    from gjenopptak.utgivelse import utelat
    stier = ["docs/MANUSKRIPT-v0.1.md", "docs/MANUSKRIPT-v2.8-UTKAST.md", "docs/MANUSKRIPT-v2.9.md",
             "docs/MANUSKRIPT-v3.md", "docs/MANUSKRIPT-FAKTA-2026-09-28.md", "docs/SVARBREV-v3.md"]
    beholdt, utelatt = utelat(stier)
    assert set(utelatt) == {"docs/MANUSKRIPT-v2.8-UTKAST.md", "docs/MANUSKRIPT-v2.9.md"}
    assert set(beholdt) == {"docs/MANUSKRIPT-v0.1.md", "docs/MANUSKRIPT-v3.md", "docs/MANUSKRIPT-FAKTA-2026-09-28.md",
                            "docs/SVARBREV-v3.md"}


def test_case_dokumentene_utenfor_saker_pakkes_i_saker_zip():
    from gjenopptak.utgivelse import _i_zip
    assert _i_zip("git:abc:docs/PS-246-RESULTAT.md", "PS-246-RESULTAT.md") == ("saker.zip", "sakbehandling/PS-246-RESULTAT.md")
    assert _i_zip("git:abc:docs/HERON-KOLLASJON-VURDERING-v2.md", "x")[0] == "saker.zip"
    assert _i_zip("git:abc:docs/RESULTAT-ADDENDUM-25.md", "RESULTAT-ADDENDUM-25.md") is None


def test_v060_gruppene_og_ekskluderingsliste_5():
    from gjenopptak.utgivelse import UTELATT_VERSJON, _i_zip, utelat
    assert UTELATT_VERSJON.startswith("5 ")
    assert _i_zip("git:abc:gjenvunnet/addendum-19/a19b.py", "x") == ("gjenvunnet-kode.zip", "addendum-19/a19b.py")
    assert _i_zip("git:abc:docs/MANUSKRIPT-v3.2.md", "x") == ("manuskript-tidligere.zip", "MANUSKRIPT-v3.2.md")
    assert _i_zip("git:abc:docs/MANUSKRIPT-v3.3.md", "MANUSKRIPT-v3.3.md") is None          # gjeldende står på toppnivå
    assert _i_zip("git:abc:docs/PREPRINT.md", "PREPRINT.md") == ("manuskript-tidligere.zip", "PREPRINT.md")
    assert _i_zip("git:abc:docs/RELEASE-NOTES-v0.5.0.md", "x")[0] == "utgivelser-tidligere.zip"
    assert _i_zip("git:abc:docs/RELEASE-NOTES-v0.6.0.md", "RELEASE-NOTES-v0.6.0.md") is None
    assert _i_zip("git:abc:docs/SAKBEHANDLING-2026-09-27-triage.md", "x") == ("saker.zip", "sakbehandling/SAKBEHANDLING-2026-09-27-triage.md")
    beholdt, utelatt = utelat(["docs/GJENOPPTAK_ADDENDUMSTATUS_v1_2026-10-10.md", "docs/GJENOPPTAK_INSTRUKSER_v1.4_2026-10-10.md",
                               "docs/GJENOPPTAK_FILKART_v1_2026-10-10.md", "docs/MANUSKRIPT-v3.3.md", "docs/MANUSKRIPT-v3.1.md"])
    assert utelatt == ["docs/GJENOPPTAK_INSTRUKSER_v1.4_2026-10-10.md", "docs/GJENOPPTAK_FILKART_v1_2026-10-10.md"]
    assert "docs/GJENOPPTAK_ADDENDUMSTATUS_v1_2026-10-10.md" in beholdt and "docs/MANUSKRIPT-v3.1.md" in beholdt


def test_gjenvunnet_katalogen_er_med_i_dokumentsettet():
    from gjenopptak.utgivelse import repo_dokumenter
    assert "gjenvunnet/addendum-19/OPPHAV.md" in repo_dokumenter() and "gjenvunnet/addendum-19/a19b.py" in repo_dokumenter()


def test_kandidatlista_er_renset_og_bygget_kontrollerer_det(tmp_path):
    import json
    import re
    import pytest
    from gjenopptak import maalefiler as M
    from gjenopptak import utgivelse as U
    assert U.UTEN_UTDRAG == ("docs/SAKBEHANDLING-2026-09-27-kandidater.md",)
    assert U._i_zip("git:abc:" + U.UTEN_UTDRAG[0], "x")[0] == "saker.zip"
    lista = (U.REPO / U.UTEN_UTDRAG[0]).read_text(encoding="utf-8")                     # filen i repoet er renset 10.10.2026
    assert len(re.findall(r"\[utdrag utelatt: \d+ tegn, sha256 [0-9a-f]{16}\]", lista)) == 83
    assert "*Rettet 10.10.2026: de 83 ordrette utdragene" in lista
    passasje = "We could not date the lower layer, because no suitable sample was preserved in the trench at all."
    blind = tmp_path / "blind.jsonl"
    blind.write_text(json.dumps({"id": "P1", "tekst": passasje}) + "\n", encoding="utf-8")
    indeks = M.passasjeindeks([blind])
    ren = tmp_path / "ren.md"
    ren.write_text("| AL-0001 | H7 | «[utdrag utelatt: 97 tegn, sha256 0123456789abcdef]» |\n| AL-0002 | H1 | egen omtale |\n", encoding="utf-8")
    assert U.kontroller_uten_utdrag("sakbehandling/kandidater.md", ren, indeks) == 1
    uren = tmp_path / "uren.md"
    uren.write_text(f"| AL-0001 | H7 | «{passasje.upper()}» |\n", encoding="utf-8")       # versaler skjuler ikke utdraget
    with pytest.raises(U.UtgivelseFeil, match="1 ordrette utdrag på 50 tegn eller mer står igjen"):
        U.kontroller_uten_utdrag("sakbehandling/kandidater.md", uren, indeks)


def test_bundlevalget_er_hele_historikken_som_standard():
    from gjenopptak import utgivelse as U
    assert U.BUNDLE_REFS["alle"] == ["--all"] and "offentlig" in U.BUNDLE_REFS["offentlig"]
    import inspect
    assert inspect.signature(U.bygg).parameters["bundle"].default == "alle"


def test_historiske_zipfiler_faar_en_les_foerst_fil():
    from gjenopptak import utgivelse as U
    assert set(U.HISTORISK) == {"manuskript-tidligere.zip", "utgivelser-tidligere.zip"}
    for znavn, sti in U.HISTORISK.items():
        t = (U.REPO / sti).read_text(encoding="utf-8")
        flat = " ".join(t.split())
        assert "status den dagen de ble skrevet" in flat and "`README.md` og `ZENODO.md`" in flat and znavn in t
    assert U._i_zip("git:abc:docs/PREPRINT.md", "x")[0] == "manuskript-tidligere.zip"           # filene README-en omtaler, ligger der
    assert U._i_zip("git:abc:docs/RELEASE-NOTES-v0.4.0.md", "x")[0] == "utgivelser-tidligere.zip"
    alle_mønstre = (*U.REPO_MØNSTRE, *U.REPO_KATALOGER)
    assert not any(U._treffer(sti, m) or sti.startswith(m) for sti in U.HISTORISK.values() for m in alle_mønstre)   # deponeres ikke som egen fil


def test_innhentet_filene_samles_i_en_zip():
    from gjenopptak import utgivelse as U
    for navn in ("INNHENTET-2026-09-26-en-koder.md", "INNHENTET-2026-10-10-manuskript-v3.3.md"):
        assert U._i_zip(f"git:abc:docs/{navn}", navn) == ("innhentet.zip", navn)
    assert U._i_zip("git:abc:docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md", "x") is None             # korrigendumet står for seg

