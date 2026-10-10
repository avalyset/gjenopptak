"""gjenvunnet/addendum-19: a19.py og a19b.py er avledet av a20.py, og OPPHAV.md fører riktige sha256."""
import ast
import hashlib
import re
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "gjenvunnet" / "addendum-19"
ASHA_19 = "0dbd59cce64f4ce97d324807c74d46cb6a1abd002a417b09ed11a4c75162abbd"    # ADDENDUM-19.md i 5e8bb6f
ASHA_19B = "fb0410e3b1225b60613cb430376f927f22d3bbb896d4f5e718c6a7d369890223"   # ADDENDUM-19.md i 7a384c1


def _les(navn):
    return (D / navn).read_text(encoding="utf-8")


def _a19(src):
    """Snutten i avledning-a19.txt, med addendum-sha som konstant i stedet for lest fra disk."""
    ny = re.sub(r'^""".*?"""', '"""ADDENDUM-19: Opus 5, koder 2s gjenvunnede regelfil, ett kall per passasje, samme 320.\n'
                'Fyller cellen som skiller modell fra øktform. Identisk ADDENDUM-20 bortsett fra modell og addendum-sha."""',
                src, count=1, flags=re.S)
    ny = ny.replace("addendum-20", "addendum-19").replace('addendum="ADDENDUM-20"', 'addendum="ADDENDUM-19"')
    return re.sub(r'ASHA="[0-9a-f]{64}"', f'ASHA="{ASHA_19}"', ny, count=1)


def _a19b(src):
    ny = re.sub(r'^""".*?"""', '"""ADDENDUM-19b: identisk ADDENDUM-19, men max_tokens 2 000. Første kjøring var ugyldig på avkutting."""',
                src, count=1, flags=re.S)
    ny = ny.replace("addendum-20", "addendum-19").replace('addendum="ADDENDUM-20"', 'addendum="ADDENDUM-19b"')
    ny = re.sub(r'ASHA="[0-9a-f]{64}"', f'ASHA="{ASHA_19B}"', ny, count=1)
    return ny.replace('"max_tokens":300', '"max_tokens":2000').replace('max_tokens=300', 'max_tokens=2000')


def test_a19_er_avledningen_av_a20_og_har_utskriftens_lengde():
    a19 = _les("a19.py")
    assert a19 == _a19(_les("a20.py"))
    assert len(a19) == 4473                       # «a19.py parser OK · 4473 B» i utskriften 27.09.2026
    ast.parse(a19)


def test_a19b_er_avledningen_av_a20_med_taket_2000():
    a19b = _les("a19b.py")
    assert a19b == _a19b(_les("a20.py"))
    assert [l.strip()[:70] for l in a19b.splitlines() if "max_tokens" in l] == [
        '"""ADDENDUM-19b: identisk ADDENDUM-19, men max_tokens 2 000. Første kj',
        'base={"model":modell,"max_tokens":2000,"system":SYSTEM,"messages":[{"r',
        'temperature_utelatt=utelatt, max_tokens=2000,']


def test_snuttene_i_avledningsfilene_er_de_testen_kjorer():
    for navn, biter in (("avledning-a19.txt", ('ny.replace("addendum-20","addendum-19")', "ADDENDUM-19: Opus 5")),
                        ("avledning-a19b.txt", ("ny.replace('\"max_tokens\":300','\"max_tokens\":2000')", "ADDENDUM-19b: identisk"))):
        t = _les(navn)
        assert all(b in t for b in biter), navn


def test_opphav_foerer_sha256_for_hver_fil():
    opphav = _les("OPPHAV.md")
    ført = dict(re.findall(r"\| `([^`]+)` \| [\d  ]+ \| `([0-9a-f]{64})` \|", opphav))
    filer = sorted(p.name for p in D.iterdir() if p.name not in ("OPPHAV.md", "README.md"))
    assert sorted(ført) == filer
    for navn in filer:
        assert hashlib.sha256((D / navn).read_bytes()).hexdigest() == ført[navn], navn


def test_ingen_noekkelverdi_i_filene():
    hem = re.compile(r"(sk-ant-[A-Za-z0-9_\-]{8,}|sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,})")
    for p in D.iterdir():
        assert not hem.search(p.read_text(encoding="utf-8")), p.name


def test_readme_sier_regenerert_og_ikke_byte_verifisert():
    r = _les("README.md")
    assert "regenerert, ikke gjenfunnet" in r and "ikke byte-verifisert mot originalen" in r
    for linje in ("12478", "13278", "13433", "13346", "13559"):
        assert linje in r, linje
    assert "aecdf1aa80b023004d548067cf6b3a30a1b3a71fde11446e1cf592ae32dd6684" in r and "4 473 tegn" in r
