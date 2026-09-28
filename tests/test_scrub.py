"""Scrubben skal finne det den skal, og aldri skrive ut verdien den fant."""
from gjenopptak import scrub


def test_alle_elleve_monstre_er_der():
    assert len(scrub.MØNSTRE) == 11
    navn = [n for n, _ in scrub.MØNSTRE]
    assert len(set(navn)) == 11, "duplikate mønsternavn gjør rapporten uleselig"


def test_verdien_skrives_aldri_ut():
    """Et scrub-verktøy som logger hemmeligheten, har lekket den til hver logg."""
    hemmelig = "sk-ant-" + "A" * 40
    linje = f"nokkel = {hemmelig}"
    ut = scrub.redigert(linje, dict(scrub.MØNSTRE)["Anthropic-nøkkel"])
    assert hemmelig not in ut
    assert "REDIGERT" in ut
    assert ut.startswith("nokkel = sk-a"), "formen skal være lesbar, innholdet ikke"


def test_hvert_monster_treffer_sitt_eget_eksempel():
    eksempler = {
        "Anthropic-nøkkel": "sk-ant-" + "x" * 30,
        "OpenAI-nøkkel": "sk-" + "y" * 40,
        "Google-nøkkel": "AIza" + "z" * 35,
        "GitHub-token": "ghp_" + "q" * 36,
        "AWS-nøkkel": "AKIAIOSFODNN7EXAMPLE",
        "PEM-privatnøkkel": "-----BEGIN RSA PRIVATE KEY-----",
        "Bearer-token": "Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
        "privat e-post": "noen@gmail.com",
        "forretnings-e-post": "noen@ecodeco.no",
        "absolutt hjemmesti": "/Users/noen/dev",
        "ordet «sealed»": "the archive is sealed",
    }
    import re
    for navn, m in scrub.MØNSTRE:
        assert re.search(m, eksempler[navn]), f"{navn} traff ikke sitt eget eksempel"


def test_uskyldig_tekst_gir_ingen_treff():
    import re
    ren = "Presisjonen er 0,345 [0,298-0,396] og porten falt paa 21 av 27."
    for navn, m in scrub.MØNSTRE:
        assert not re.search(m, ren), f"{navn} ga falsk positiv"


def test_selvunntaket_er_laast_til_noyaktig_to_filer():
    """Filunntak er måten en scrub settes ut av spill. Listen skal ikke kunne vokse stille:
    den er scrubbens egen kilde og dens egen test, og ingenting annet."""
    assert scrub.SELVUNNTAK == ("src/gjenopptak/scrub.py", "tests/test_scrub.py")
