"""Søk etter positive kontroller i H1 og H4 uten å bruke OpenAlex-kvote.

ADDENDUM-04 §4 felte H1-kontrollen, og H4 sto allerede uten. Begge klassene er
løftbare, og det er den enden verktøyet hviler på.

**Hvorfor Europe PMC og ikke OpenAlex.** Kandidatsøk med ``fulltext.search``
koster ett kall per frase per ramme — 60 kall for en runde. Europe PMC har eget
frasesøk i åpen fulltekst, gratis, og gir PMCID direkte. Rammetilhørighet kan
etterpå avgjøres for hele kandidatlisten med **ett** OpenAlex-kall per ramme, ved
å filtrere på en DOI-liste. Kvotekostnaden faller fra ~60 til ~4.

**Prisen:** Europe PMC dekker biomedisin og grenseområder. Kandidater i
historisk tekstvitenskap vil ikke dukke opp her. Det skal stå i nullresultatet.

Kravene fra ADDENDUM-02 §2 og ADDENDUM-04 §4, i rekkefølge:

1. passasjen (±2 setninger) bærer både det ugjorte og hindringen
2. det ugjorte tilhører **arbeidet som rapporteres**, ikke organisasjonens praksis
3. verket ligger i en av de fire rammene, i vinduet, og er hentbart
4. sitat under femten ord, ett per kilde

Punkt 1, 2 og 4 avgjøres her. Punkt 3 krever OpenAlex og gjøres når kvoten er fri.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx

from ..extract import passages
from ..parse import sentences_from_jats
from .openalex import write_raw

EPMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
EPMC_XML = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
UA = "gjenopptak/0.1.0 (research; contact via repo)"
HJ = {"User-Agent": UA, "Accept": "application/json"}
HX = {"User-Agent": UA, "Accept": "application/xml"}

#: PREREG-vinduet. Kandidater utenfor det kan ikke være kontroller.
YEARS = (2015, 2020)

#: H1 — menneskelig lesning eller koding i skala.
PHRASES_H1 = (
    '"we manually coded"',
    '"manually coded a random sample"',
    '"we hand-coded"',
    '"coded by hand"',
    '"we were unable to code all"',
    '"manual coding of all"',
    '"manual review of all"',
    '"we coded a random sample"',
    '"too time-consuming to code"',
    '"a subset of records was reviewed manually"',
)

#: H4 — mønster i bilder eller signaler i volum.
PHRASES_H4 = (
    '"manual annotation of all images"',
    '"visual inspection of all images"',
    '"we visually inspected a random sample"',
    '"we annotated a subset of images"',
    '"manually segmented a subset"',
    '"only a subset of the images"',
    '"manual delineation of all"',
    '"too time-consuming to segment"',
)

#: Armering. Denne setningen finnes i en kjent artikkel og MÅ komme ut av søket.
#: Uten treff her er et nullresultat fra søkeformene over uten verdi.
ARMING_PHRASE = '"manual review of all records was not feasible"'
ARMING_DOI = "10.1136/bmjopen-2026-121412"

#: Forfatterens eget arbeid, ikke organisasjonens praksis (ADDENDUM-04 §4).
#: Hovedfilteret: uten førsteperson er det ikke arbeidet som rapporteres.
OWN_WORK = re.compile(r"\b(we|our|us)\b", re.I)

#: Sikkerhetsnett for tredjepersonsformer som likevel nevner «we» et sted i
#: setningen — en beskrivelse av andres eller organisasjonens praksis.
#: 10.4073/cmdp.2018.2 («3ie does not conduct …») faller alt på OWN_WORK.
THIRD_PARTY = re.compile(
    r"^\s*(the\s+\w+\s+(does not|did not|do not)"
    r"|[0-9A-Za-z]{1,6}ie\s+(does|did|do)\s+not"
    r"|(most|many|other|previous|earlier)\s+(studies|authors|reviews|papers)\b)",
    re.I,
)


class ArmingFailed(AssertionError):
    """Kontrollstrengen traff ikke. Nullresultatet er da ikke gyldig."""


@dataclass
class Candidate:
    """En kandidatpassasje som har bestått punkt 1, 2 og 4."""

    klass: str
    phrase: str
    doi: str
    pmcid: str
    year: int
    journal: str
    unit: str
    sentence: str
    words: int
    passage: str
    section_raw: str
    provenance: str
    span: dict = field(default_factory=dict)

    def as_row(self) -> dict:
        d = self.__dict__.copy()
        return d


def _get(c: httpx.Client, url: str, headers: dict, *, retries: int = 4, **kw) -> httpx.Response:
    last = None
    for attempt in range(retries):
        r = c.get(url, headers=headers, **kw)
        if r.status_code == 200:
            return r
        last = r
        time.sleep(2 * (attempt + 1))
    return last if last is not None else r


def search_phrase(c: httpx.Client, phrase: str, raw_dir: Path, *, stem: str,
                  years: tuple[int, int] | None = YEARS, page_size: int = 10) -> list[dict]:
    """Frasesøk i åpen fulltekst. Returnerer treff med DOI og PMCID."""
    q = f"{phrase} AND OPEN_ACCESS:Y"
    if years:
        q += f" AND (FIRST_PDATE:[{years[0]} TO {years[1]}])"
    r = _get(c, EPMC_SEARCH, HJ, params={"query": q, "resultType": "lite",
                                         "format": "json", "pageSize": str(page_size)})
    if r.status_code != 200:
        return []
    write_raw(r.content, str(r.url), raw_dir, stem=stem)
    ut = []
    for x in json.loads(r.content).get("resultList", {}).get("result", []):
        if x.get("pmcid") and x.get("doi"):
            ut.append({"doi": x["doi"].lower(), "pmcid": x["pmcid"],
                       "year": int(x.get("pubYear") or 0),
                       "journal": (x.get("journalTitle") or "")[:40]})
    return ut


def verify(c: httpx.Client, hit: dict, phrase: str, klass: str, raw_dir: Path,
           *, max_words: int = 34) -> list[Candidate]:
    """Hent fulltekst og behold passasjer som oppfyller punkt 1, 2 og 4."""
    url = EPMC_XML.format(pmcid=hit["pmcid"])
    r = _get(c, url, HX, retries=2)
    if r.status_code != 200 or not r.content.strip():
        return []
    write_raw(r.content, url, raw_dir, stem=f"cs-jats-{hit['pmcid']}")
    try:
        rows = sentences_from_jats(r.content, doc_id=hit["pmcid"])
    except Exception:                                        # noqa: BLE001
        return []
    kjerne = phrase.strip('"').lower()
    ut: list[Candidate] = []
    for p in passages(rows):
        if kjerne not in p.text.lower():
            continue
        s = p.sentence_text
        if not (8 <= len(s.split()) <= max_words):
            continue
        if not OWN_WORK.search(s):          # punkt 2: arbeidet som rapporteres
            continue
        if THIRD_PARTY.search(s):           # punkt 2: ikke organisasjonens praksis
            continue
        ut.append(Candidate(
            klass=klass, phrase=kjerne, doi=hit["doi"], pmcid=hit["pmcid"],
            year=hit["year"], journal=hit["journal"], unit=p.unit, sentence=s,
            words=len(s.split()), passage=p.text[:600], section_raw=p.section_raw,
            provenance=p.section_label_provenance, span=p.span(),
        ))
    return ut


def arm(c: httpx.Client, raw_dir: Path) -> dict:
    """Bekreft at søkeformen virker. Kaster ArmingFailed hvis ikke."""
    treff = search_phrase(c, ARMING_PHRASE, raw_dir, stem="cs-arming", years=None, page_size=10)
    if not treff:
        raise ArmingFailed(
            f"armeringsfrasen {ARMING_PHRASE} ga ingen treff i Europe PMC. "
            "Et nullresultat fra de øvrige søkeformene er da ikke gyldig."
        )
    return {"n": len(treff), "dois": [t["doi"] for t in treff][:5],
            "fant_forventet": any(t["doi"] == ARMING_DOI for t in treff)}
