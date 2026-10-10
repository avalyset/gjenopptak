"""Kryssdokumentsjekken skal fange en foreldet verdi som står umerket — og bare da."""

from gjenopptak import kryssjekk as K


def skriv(tmp_path, navn, tekst):
    p = tmp_path / navn
    p.write_text(tekst, encoding="utf-8")
    return p


def test_fanger_umerket_foreldet_verdi(tmp_path):
    f = skriv(tmp_path, "a.md", "Hovedfunnet: 17 av 24 leste ekte treff (71 %) er H7.\n")
    avvik = K.sjekk([f])
    assert [a[0] for a in avvik] == ["H7-andel av ekte treff"]


def test_merket_verdi_er_ikke_avvik(tmp_path):
    f = skriv(tmp_path, "b.md", "*Før ADDENDUM-10: 17 av 24 (71 %).*\n")
    assert K.sjekk([f]) == []


def test_sammenstilling_er_ikke_avvik(tmp_path):
    f = skriv(tmp_path, "c.md", "| M1-korrigert | 0,652 | **0,671** |\n")
    assert K.sjekk([f]) == []


def test_seksjonspeker_dekker_hele_seksjonen(tmp_path):
    f = skriv(tmp_path, "d.md",
              "## 16 Porten målt (2026-09-20)\n"
              "> **Foreldet av ADDENDUM-10.** Gjeldende tall står i resultatnotatet.\n"
              "\n" * 1 + "* Presisjon 16,0 % (24 av 150).\n"
              "* M1-korrigert: 0,652.\n")
    assert K.sjekk([f]) == []


def test_manglende_fil_rapporteres(tmp_path):
    avvik = K.sjekk([tmp_path / "finnes-ikke.md"])
    assert avvik and avvik[0][0] == "FIL MANGLER"


def test_de_ekte_dokumentene_er_rene():
    """Selve repoet skal stå grønt — dette er porten mot at et tall blir stale igjen."""
    assert K.main([]) == 0


def test_bar_prosentsats_er_ikke_signatur_for_en_paastand():
    """28.09.2026: «83,3 %» sto som foreldet-signatur for løftbar andel uten emneord, og
    flagget SAK-14s Perseus-rate «75/90 = 83,3 %». En vokter som matcher på et tall alene,
    vokter tallet og ikke påstanden. Kravet er at emnet står på samme linje."""
    gamle = next(g for navn, _, g, _ in K.STØRRELSER if navn == "løftbar andel")
    import re
    uskyldig = "**75/90 = 83,3 %** [74,3–89,6]. **Utfallet er det samme under begge.**"
    assert not any(re.search(m, uskyldig) for m in gamle), "falsk positiv på en ærlig 83,3 %"
    skyldig = "20 av 24 løftbare = 83,3 % av de leste treffene"
    assert any(re.search(m, skyldig) for m in gamle), "den ekte foreldede verdien slipper unna"


def test_kappa_intervallet_for_0812_fanges(tmp_path):
    """28.09.2026: 0,812 sto med intervallet til 0,826 i seks filer. Signaturen krever 0,812 på
    samme linje, så 0,826-raden i ADDENDUM-11 er ikke et avvik."""
    feil = skriv(tmp_path, "e.md", "| koder 2 | 0,812 | 0,712–0,917 | leser |\n")
    assert [a[0] for a in K.sjekk([feil])] == ["κ-intervall for 0,812"]
    riktig = skriv(tmp_path, "f.md", "| første lesning | 320 | 96,6 % | 0,826 | 0,712–0,917 |\n")
    assert K.sjekk([riktig]) == []


def test_alle_addenda_er_laast(tmp_path):
    """INSTRUKSER-v1.2: hvert ADDENDUM-*.md er låst når det er committet, ikke bare 01..09."""
    f = skriv(tmp_path, "ADDENDUM-21.md", "Koder 2 fikk κ = 0,812, intervall 0,712–0,917.\n")
    avvik = K.sjekk([f])
    assert avvik and avvik[0][0].startswith("LÅST")


def test_fase4_stoerrelsene_er_i_tabellen_og_en_annen_verdi_fanges(tmp_path):
    """07.10.2026: fase 4 (ADDENDUM-26) ble avbrutt; størrelsene fra RESULTAT-ADDENDUM-26 § 0 er dekket."""
    navn = {s[0] for s in K.STØRRELSER}
    assert {"fase 4: rammerader", "fase 4: overlapp med tekstvitenskap-rammen", "fase 4: trukne verk",
            "fase 4: tekstbiter", "fase 4: dømte tekstbiter"} <= navn
    riktig = skriv(tmp_path, "ok.md", "Håndskriftrammen har 807 rader; 799 av 807 overlapper. Fase 4 trakk 100 verk, "
                   "31 031 tekstbiter; 830 av 31 031 dømt.\n")
    assert K.sjekk([riktig]) == []
    galt = skriv(tmp_path, "galt.md", "Håndskriftrammen har 806 rader.\n799 av 807 er riktig.\n800 av 807 er ikke riktig.\n"
                 "Fase 4 trakk 90 verk.\nFase 4 ga 30 031 tekstbiter.\nFase 4 dømte 831 av 31 031.\n")
    assert sorted(a[0] for a in K.sjekk([galt])) == ["fase 4: dømte tekstbiter", "fase 4: overlapp med tekstvitenskap-rammen",
                                                     "fase 4: rammerader", "fase 4: tekstbiter", "fase 4: trukne verk"]


def test_differansen_0812_0636_fanges_og_rettelsen_slipper(tmp_path):
    gammel = skriv(tmp_path, "g.md", "Differansen 0,636 mot 0,812 er **ikke** statistisk etablert.\n")
    engelsk = skriv(tmp_path, "e.md", "a difference that is not statistically established here.\n")
    ny = skriv(tmp_path, "n.md", "Differansen er 0,177, paret bootstrap [0,044–0,323].\n"
                                 "*(Rettet 10.10.2026: sto at øktformens bidrag er mulig og umålt.)*\n")
    assert [a[0] for a in K.sjekk([gammel, engelsk])] == ["differansen 0,812 − 0,636"] * 2
    assert K.sjekk([ny]) == []


def test_sonnet_i_leserstigen_og_preprintens_status(tmp_path):
    f = skriv(tmp_path, "s.md", "Leserstigen: Haiku 0,031,\n  Sonnet 0,297, Opus 0,636.\n"
                                "Preprint: osf.io/preprints/metaarxiv/zvc34_v1 — pending.\n")
    assert [a[0] for a in K.sjekk([f])] == ["Sonnet 5 med full regelfil", "preprintens status"]
    ok = skriv(tmp_path, "t.md", "Sonnet med tynt utdrag: 0,297. MetaArXiv zvc34 ble avvist 30.09.2026.\n")
    assert K.sjekk([ok]) == []


def test_erstattet_instruksversjon_og_versjonert_manus_er_laast(tmp_path):
    gammel = skriv(tmp_path, "INSTRUKSER-v1.3.md", "x")
    assert not K.er_laast(gammel)                          # høyeste versjon er levende
    ny = skriv(tmp_path, "GJENOPPTAK_INSTRUKSER_v1.4_2026-10-10.md", "x")
    assert K.er_laast(gammel) and not K.er_laast(ny)
    for navn in ("MANUSKRIPT-v3.3.md", "MANUSKRIPT-v2.8-UTKAST.md", "PREPRINT-v2.md", "RELEASE-NOTES-v0.5.0.md"):
        assert K.er_laast(skriv(tmp_path, navn, "x")), navn
    assert not K.er_laast(skriv(tmp_path, "METODE.md", "x"))


def test_mappe_og_frosset_leses_og_en_ulesbar_mappe_er_feil(tmp_path, capsys):
    rot = tmp_path / "repo"; rot.mkdir()
    levende = tmp_path / "plan"; levende.mkdir()
    sendt = tmp_path / "sendt" / "v1"; sendt.mkdir(parents=True)
    skriv(levende, "PLAN.md", "MetaArXiv zvc34_v1: pending.\n")
    skriv(sendt, "BREV.txt", "a difference that is not statistically established here.\n")
    assert K.main(["--rot", str(rot), "--mappe", str(levende), "--frosset", str(sendt.parent)]) == 1
    ut = capsys.readouterr().out
    assert "AVVIK  preprintens status" in ut and "BREV.txt:1  differansen" in ut
    assert "1 umerkede foreldede verdier i rettbare filer · 1 i låste filer" in ut
    assert K.main(["--rot", str(rot), "--mappe", str(tmp_path / "finnes-ikke")]) == 1
    tom = tmp_path / "tom"; tom.mkdir()
    assert K.main(["--rot", str(rot), "--frosset", str(tom)]) == 1
    K.FROSNE_RØTTER.clear()


def test_grunnratens_gamle_intervall_fanges(tmp_path):
    gammel = skriv(tmp_path, "g.md", "| c) | 3,43 % = ett per 29 [2,12–7,95 %] | beste anslag |\n")
    ny = skriv(tmp_path, "n.md", "| c) | 3,42 %, verksklynget [1,3–7,5 %] (sto [2,12–7,95 %]) | sekundær størrelse |\n")
    assert [a[0] for a in K.sjekk([gammel])] == ["grunnrate c), intervall"] and K.sjekk([ny]) == []
