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
