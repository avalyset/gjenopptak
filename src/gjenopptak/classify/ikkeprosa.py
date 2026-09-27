"""G3-regelen: er en tekstbit prosa, eller referanseliste/tabellrester?

Regelen ble formulert 2026-09-26 og produserte tallene i
`ekstraksjon/2026-09-26/g3-ikke-prosa.json`, men implementasjonen lå i en kladdefil som
ikke ble bevart. Den er reimplementert 2026-09-27 fra regelteksten i utdatafilen og
kryssjekket mot de fire kontrolltallene der (6 098/22 243, 490/2 173, 1/25, 19/150).
Jf. LAERDOM §30: alt en låst måling leser, låses med den.

Regelteksten, ordrett fra utdatafilen:
    «under 50 % bokstaver ELLER referansemønster (årstall+sidespenn, nummerrekke
     «50. 51. 52.», initialrekke, pp. n–m)»
"""
import re

#: Årstall i parentes eller alene, fulgt av sidespenn: «(2015) 12–34», «2015, 12-34».
_AARSTALL_SIDESPENN = re.compile(r'\(?(19|20)\d{2}\)?[^\n]{0,20}?\d{1,4}\s*[–—-]\s*\d{1,4}')
#: Nummerrekke: «50. 51. 52.» — tre eller flere tall med punktum etter hverandre.
_NUMMERREKKE = re.compile(r'(?:\b\d{1,4}\.\s+){3,}')
#: Initialrekke: «A. B. Cohen», «J. R. R.» — tre eller flere enkeltbokstav-initialer.
_INITIALREKKE = re.compile(r'(?:\b[A-ZÆØÅ]\.\s*){3,}')
#: Eksplisitt sidespenn.
_PP = re.compile(r'\bpp?\.\s*\d{1,4}\s*[–—-]\s*\d{1,4}')

def bokstavandel(tekst: str) -> float:
    """Andel tegn som er bokstaver, av alle ikke-blanke tegn."""
    t = [c for c in tekst if not c.isspace()]
    if not t:
        return 0.0
    return sum(1 for c in t if c.isalpha()) / len(t)

def referansemonster(tekst: str) -> bool:
    """Treffer tekstbiten et av de fire referansemønstrene?"""
    return bool(_AARSTALL_SIDESPENN.search(tekst) or _NUMMERREKKE.search(tekst)
                or _INITIALREKKE.search(tekst) or _PP.search(tekst))

def er_ikke_prosa(tekst: str) -> bool:
    """G3: under 50 % bokstaver ELLER referansemønster."""
    return bokstavandel(tekst) < 0.50 or referansemonster(tekst)
