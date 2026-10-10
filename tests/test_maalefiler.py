"""maalefiler.zip: andres tekst følger ikke med, nøkler for ukjørte målinger holdes ute, og zip-filen er reproduserbar."""
import hashlib
import json
import zipfile

from gjenopptak import maalefiler as M


def test_tekstfelt_byttes_paa_alle_nivaaer_og_alt_annet_staar():
    inn = {"id": "PS-001", "passage_text": "Vi kunne ikke datere laget.", "begrunnelse": "egen tekst",
           "rader": [{"text": "kort", "n": 3}, {"setning": "", "ok": True}], "tekst": 7}
    ut = M.uten_tekst(inn)
    assert ut["passage_text"] == {"sha256": hashlib.sha256("Vi kunne ikke datere laget.".encode()).hexdigest(), "tegn": 27}
    assert ut["rader"][0] == {"text": {"sha256": hashlib.sha256(b"kort").hexdigest(), "tegn": 4}, "n": 3}
    assert ut["rader"][1]["setning"]["tegn"] == 0 and ut["rader"][1]["ok"] is True
    assert ut["begrunnelse"] == "egen tekst" and ut["id"] == "PS-001" and ut["tekst"] == 7     # ikke-streng røres ikke
    assert "datere" not in json.dumps(ut, ensure_ascii=False)


def test_koder1_beholder_bare_verdiktfeltene():
    rad = {"id": "PS-001", "tekst": "andres tekst", "doc_id": "W1", "start_index": 3, "utvalgstype": "treff",
           "dømt_klasse": "H7", "ekte_treff": False, "min_klasse": "INGEN", "min_bedømbar": None, "tvil": False,
           "min_begrunnelse": "ingen hindring"}
    ut = [json.loads(l) for l in M.koder1((json.dumps(rad, ensure_ascii=False) + "\n").encode()).decode().splitlines()]
    assert ut == [{"id": "PS-001", "ekte_treff": False, "min_klasse": "INGEN", "min_bedømbar": None, "tvil": False,
                   "min_begrunnelse": "ingen hindring"}]


def test_listene_er_ryddige_og_holder_fra_hverandre():
    for xs in (M.SOM_DE_ER, M.UTEN_TEKST):
        assert list(xs) == sorted(set(xs))
    alle = set(M.SOM_DE_ER) | set(M.UTEN_TEKST)
    assert not alle & set(M.HOLDT_UTE) and not alle & set(M.FOR_STORE) and not set(M.SOM_DE_ER) & set(M.UTEN_TEKST)
    assert M.KODER1[0] in M.HOLDT_UTE and M.KODER1[1] not in alle
    # blindfiler og nøkler for ukjørte målinger er aldri med
    assert not [s for s in alle if "blind.jsonl" in s or s.endswith("port-presisjonssett-blind.jsonl")]
    assert "presisjonssett/port-presisjonssett-nokkel.jsonl" in M.HOLDT_UTE
    assert "revisjon-2026-10/menneskevalidering/nokkel.jsonl" in M.HOLDT_UTE


def test_pakk_er_reproduserbar_og_avleder_tekstfilene(tmp_path, monkeypatch):
    v = tmp_path / "vault"
    (v / "a").mkdir(parents=True)
    (v / "a/tall.json").write_text('{"kappa": 0.636}\n', encoding="utf-8")
    (v / "a/fasit.jsonl").write_text('{"id": 1, "sentence_text": "hemmelig setning"}\n', encoding="utf-8")
    (v / "a/k1.jsonl").write_text(json.dumps({"id": "PS-001", "tekst": "x", "ekte_treff": True, "min_klasse": "H7",
                                              "min_bedømbar": True, "tvil": False, "min_begrunnelse": "b"}) + "\n", encoding="utf-8")
    monkeypatch.setattr(M, "SOM_DE_ER", ("a/tall.json",))
    monkeypatch.setattr(M, "UTEN_TEKST", ("a/fasit.jsonl",))
    monkeypatch.setattr(M, "KODER1", ("a/k1.jsonl", "a/k1-verdikter.jsonl", M.KODER1[2]))
    innhold = M.pakk(v, tmp_path / "en.zip")
    M.pakk(v, tmp_path / "to.zip")
    assert (tmp_path / "en.zip").read_bytes() == (tmp_path / "to.zip").read_bytes()
    with zipfile.ZipFile(tmp_path / "en.zip") as z:
        assert sorted(z.namelist()) == ["maalefiler/a/fasit-uten-tekst.jsonl", "maalefiler/a/k1-verdikter.jsonl", "maalefiler/a/tall.json"]
        alt = b"".join(z.read(n) for n in z.namelist()).decode()
    assert "hemmelig" not in alt and '"tekst"' not in alt and "0.636" in alt
    assert [i["form"] for i in innhold] == ["uten tekst", "uten tekst og nøkkelfelt", "som den er"]
    assert all(i["utdrag_utelatt"] == 0 for i in innhold)
    assert all(len(i["sha256"]) == 64 and len(i["kilde_sha256"]) == 64 for i in innhold)


PASSASJE = ("We could not date the lower layer,   because no suitable sample was preserved in the trench;\n"
            "the upper layer was dated to the early Iron Age on the basis of three charcoal samples.")


def _indeks(tmp_path):
    b = tmp_path / "blind.jsonl"
    b.write_text(json.dumps({"id": "P1", "tekst": PASSASJE}) + "\n" + json.dumps({"id": "P2", "tekst": "kort"}) + "\n", encoding="utf-8")
    return M.passasjeindeks([b])


def test_ordrett_utdrag_finnes_ogsaa_med_andre_blanktegn_og_korte_sitater_staar(tmp_path):
    passasjer, indeks = _indeks(tmp_path)
    langt = "Begrunnelse: «because no suitable sample was preserved in the trench; the upper layer was dated» — altså H7."
    (a, b), = M.utdrag(langt, passasjer, indeks)
    assert langt[a:b] == "because no suitable sample was preserved in the trench; the upper layer was dated"
    ny, n = M.ta_ut(langt, passasjer, indeks)
    assert n == 1 and "suitable sample" not in ny and ny.startswith("Begrunnelse: «[utdrag utelatt: 81 tegn, sha256 ")
    assert ny.endswith("]» — altså H7.")
    kort = "Forfatterne sier «no suitable sample was preserved» og oppgir det som grunn."      # 33 tegn: under grensen
    assert M.utdrag(kort, passasjer, indeks) == [] and M.ta_ut(kort, passasjer, indeks) == (kort, 0)
    egen = "Forfatterne daterte ikke det nedre laget fordi ingen egnet prøve var bevart i sjakten, og det øvre på trekull."
    assert M.utdrag(egen, passasjer, indeks) == []                                              # parafrase er ikke utdrag


def test_titler_roeres_ikke_og_rens_lar_rene_filer_staa_byte_for_byte(tmp_path):
    passasjer, indeks = _indeks(tmp_path)
    sitat = "the upper layer was dated to the early Iron Age on the basis of three charcoal samples."
    rad = {"id": 1, "tittel": sitat, "begrunnelse": f"Sitat: {sitat}"}
    b, n = M.rens("x.jsonl", (json.dumps(rad) + "\n").encode(), passasjer, indeks)
    ut = json.loads(b)
    assert n == 1 and ut["tittel"] == sitat and "charcoal" not in ut["begrunnelse"]
    ren = b'{"kappa": 0.636,   "n": 320}\n'
    assert M.rens("y.json", ren, passasjer, indeks) == (ren, 0)                                 # ingen omskriving uten grunn
    tekst, n = M.rens("z.md", f"Oppdrag.\n\n{sitat}\n".encode(), passasjer, indeks)
    assert n == 1 and b"charcoal" not in tekst


def test_pakk_tar_ut_utdrag_og_feiler_om_noe_staar_igjen(tmp_path, monkeypatch):
    v = tmp_path / "vault"; (v / "a").mkdir(parents=True)
    blind = v / "a/blind.jsonl"
    blind.write_text(json.dumps({"id": "P1", "tekst": PASSASJE}) + "\n", encoding="utf-8")
    sitat = "because no suitable sample was preserved in the trench; the upper layer was dated"
    (v / "a/dommer.jsonl").write_text(json.dumps({"id": "P1", "raasvar": f"treff: {sitat}"}) + "\n", encoding="utf-8")
    (v / "a/k1.jsonl").write_text(json.dumps({"id": "P1", "tekst": PASSASJE, "ekte_treff": True, "min_klasse": "H7",
                                              "min_bedømbar": True, "tvil": False, "min_begrunnelse": sitat}) + "\n", encoding="utf-8")
    monkeypatch.setattr(M, "SOM_DE_ER", ("a/dommer.jsonl",))
    monkeypatch.setattr(M, "UTEN_TEKST", ())
    monkeypatch.setattr(M, "KODER1", ("a/k1.jsonl", "a/k1-verdikter.jsonl", M.KODER1[2]))
    innhold = M.pakk(v, tmp_path / "ut.zip", [blind])
    assert {i["navn"]: (i["form"], i["utdrag_utelatt"]) for i in innhold} == {
        "a/dommer.jsonl": ("utdrag utelatt", 1), "a/k1-verdikter.jsonl": ("uten tekst og nøkkelfelt, utdrag utelatt", 1)}
    with zipfile.ZipFile(tmp_path / "ut.zip") as z:
        assert "suitable sample" not in b"".join(z.read(n) for n in z.namelist()).decode()
    monkeypatch.setattr(M, "rens", lambda navn, b, p, i: (b, 0))                                # rensingen satt ut av spill
    import pytest
    with pytest.raises(RuntimeError, match="står igjen"):
        M.pakk(v, tmp_path / "ut2.zip", [blind])


def test_stor_forbokstav_og_unicode_form_skjuler_ikke_et_utdrag(tmp_path):
    """Funnet 10.10.2026: et sitat på nøyaktig 50 tegn slapp gjennom i tre filer, fordi koderen hadde gitt det stor
    forbokstav og sammenlikningen skilte mellom store og små bokstaver. Setningene her er oppdiktet."""
    import json
    from gjenopptak import maalefiler as M
    passasje = ("it was unworkable to tell apart which hedges had been cut, and the eﬃcient café-owner’s naïve "
                "record could not be dated either.")
    blind = tmp_path / "blind.jsonl"
    blind.write_text(json.dumps({"id": "P1", "tekst": passasje}) + "\n", encoding="utf-8")
    idx = M.passasjeindeks([blind])
    for sitat in ("Unworkable to tell apart which hedges had been cut",                    # stor forbokstav, nøyaktig 50 tegn
                  "UNWORKABLE TO TELL APART WHICH HEDGES HAD BEEN CUT, and the",          # versaler
                  "and the efficient cafe\u0301-owner’s nai\u0308ve record could not be dated either",   # ligatur løst opp, aksenter dekomponert
                  "which hedges\u00a0had been cut, and the eﬃcient café-owner’s"):          # hardt mellomrom
        assert len(sitat) >= 50
        ut, n = M.ta_ut(f"Koderen skriver: «{sitat}» og går videre.", *idx)
        assert n == 1 and sitat not in ut and ut.startswith("Koderen skriver: «[utdrag utelatt: ") and ut.endswith("» og går videre."), sitat
    assert len("Unworkable to tell apart which hedges had been cut") == 50
    kort = "Unworkable to tell apart which hedges had been cu"                             # 49 tegn står
    assert M.ta_ut(f"«{kort}»", *idx) == (f"«{kort}»", 0)
    ut, n = M.ta_ut("Æ" * 10 + " Unworkable to tell apart which hedges had been cut " + "ø" * 10, *idx)
    assert n == 1 and ut.startswith("Æ" * 10) and ut.endswith("ø" * 10)                    # posisjonene peker i originalen

