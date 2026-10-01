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
