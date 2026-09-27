"""L4: siteringsgrafen uten OpenAlex (ADDENDUM-03 krever dekningsgrad per felt).

PREREG §8 krever at hver kandidat sjekkes mot om noen alt har svart, og at
**dekningsgraden rapporteres per felt** — andelen siterende arbeider med
tilgjengelig fulltekst. Lav dekning svekker kandidaten og styrker den aldri.

OpenAlex' ``cites:``-filter er den enkleste veien, men koster kvote: 1 000 kall i
døgnet, ingen polite pool. To ruter finnes uten kvote:

* **Europe PMC** ``citedby``-endepunktet. Gir siterende arbeider *som Europe PMC
  kjenner*, altså i hovedsak biomedisin, og bare for verk med PMCID.
* **Crossref** ``is-referenced-by-count`` og referanselister. Gir et antall som
  dekker alle forlag som deponerer referanser, men ikke selve listen av siterende
  verk med mindre man søker baklengs.

De to måler ulike ting, og forskjellen er selve poenget: Europe PMC-dekningen er
et **nedre** anslag, Crossref-tellingen et **øvre**. Rapporteres bare den ene,
blir overlevelsesraten i PREREG §8 systematisk feil i én retning.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
CROSSREF = "https://api.crossref.org/works"
UA = "gjenopptak/0.1.0 (research; contact via repo)"
HJ = {"User-Agent": UA, "Accept": "application/json"}


@dataclass
class CitationCoverage:
    """Dekningsgrad for ett verk, målt begge veier."""

    doi: str
    epmc_source: str | None = None
    epmc_id: str | None = None
    pmcid: str | None = None
    epmc_citing: int | None = None        # siterende verk EPMC kjenner
    epmc_citing_ft: int | None = None     # av dem: med fulltekst i EPMC
    epmc_citing_oa: int | None = None     # av dem: åpen tilgang
    crossref_count: int | None = None     # is-referenced-by-count
    error: str | None = None

    @property
    def epmc_share_of_crossref(self) -> float | None:
        """Hvor stor del av Crossrefs telling Europe PMC ser i det hele tatt."""
        if not self.crossref_count or self.epmc_citing is None:
            return None
        return self.epmc_citing / self.crossref_count

    @property
    def fulltext_share(self) -> float | None:
        """PREREG §8s dekningsgrad: andel siterende med tilgjengelig fulltekst.

        Nevneren er de siterende EPMC kjenner, ikke Crossrefs telling. Begge
        oppgis, fordi de svarer på ulike spørsmål: «hvor mange av dem vi kan se
        kan vi lese» mot «hvor mange finnes det».
        """
        if not self.epmc_citing or self.epmc_citing_ft is None:
            return None
        return self.epmc_citing_ft / self.epmc_citing

    @property
    def searchable_share_of_all(self) -> float | None:
        """Andel av alle kjente siteringer som faktisk kan søkes i fulltekst."""
        if not self.crossref_count or self.epmc_citing_ft is None:
            return None
        return self.epmc_citing_ft / self.crossref_count


def _get(c: httpx.Client, url: str, *, params: dict | None = None, retries: int = 3):
    last = None
    for a in range(retries):
        r = c.get(url, headers=HJ, params=params)
        if r.status_code == 200:
            return r
        last = r
        time.sleep(1.2 * (a + 1))
    return last


def _hits(c: httpx.Client, query: str) -> int | None:
    r = _get(c, f"{EPMC}/search", params={"query": query, "resultType": "lite",
                                          "format": "json", "pageSize": "1"})
    if not r or r.status_code != 200:
        return None
    return int(json.loads(r.content).get("hitCount") or 0)


def epmc_ids(c: httpx.Client, doi: str) -> tuple[str | None, str | None, str | None]:
    """(source, id, pmcid) for en DOI. Citations-endepunktet krever source+id.

    Merk: ``MED/{PMCID}`` gir hitCount 0 uten å feile — en stille nullverdi som
    ser ut som «ingen siteringer». Derfor brukes source og id slik søket gir dem.
    """
    r = _get(c, f"{EPMC}/search", params={"query": f'DOI:"{doi}"', "resultType": "lite",
                                          "format": "json", "pageSize": "5"})
    if not r or r.status_code != 200:
        return (None, None, None)
    for x in json.loads(r.content).get("resultList", {}).get("result", []):
        if (x.get("doi") or "").lower() == doi:
            return (x.get("source"), x.get("id"), x.get("pmcid"))
    return (None, None, None)


def epmc_citations(c: httpx.Client, source: str, ident: str) -> tuple[int | None, int | None, int | None]:
    """(kjente siterende, med fulltekst, åpne) via CITES-søk — tre kall."""
    nøkkel = f"{ident}_{source}"
    alle = _hits(c, f"CITES:{nøkkel}")
    ft = _hits(c, f"CITES:{nøkkel} AND HAS_FT:Y")
    oa = _hits(c, f"CITES:{nøkkel} AND OPEN_ACCESS:Y")
    return (alle, ft, oa)


def crossref_count(c: httpx.Client, doi: str) -> int | None:
    """is-referenced-by-count. Uten ``select``: den gir 400 på enkelt-work."""
    r = _get(c, f"{CROSSREF}/{doi}")
    if not r or r.status_code != 200:
        return None
    return int(json.loads(r.content).get("message", {}).get("is-referenced-by-count") or 0)


#: Armering. Et verk vi vet er mye sitert. Gir målingen 0 her, er den ødelagt.
ARM_DOI = "10.7554/elife.09560"
ARM_MIN_CROSSREF = 50
ARM_MIN_EPMC = 20


class ArmingFailed(AssertionError):
    """Målingen ga null for et verk som er kjent mye sitert."""


def arm(c: httpx.Client) -> dict:
    """Kjør målingen mot et kjent sitert verk før den brukes på noe annet."""
    cr = crossref_count(c, ARM_DOI)
    src, ident, pmcid = epmc_ids(c, ARM_DOI)
    alle = ft = oa = None
    if src and ident:
        alle, ft, oa = epmc_citations(c, src, ident)
    if not cr or cr < ARM_MIN_CROSSREF:
        raise ArmingFailed(f"Crossref ga {cr} for {ARM_DOI}; ventet >= {ARM_MIN_CROSSREF}. "
                           "Målingen er ødelagt, og nullresultater fra den er ikke gyldige.")
    if not alle or alle < ARM_MIN_EPMC:
        raise ArmingFailed(f"Europe PMC ga {alle} siterende for {ARM_DOI}; "
                           f"ventet >= {ARM_MIN_EPMC}. Målingen er ødelagt.")
    return {"doi": ARM_DOI, "crossref": cr, "epmc_citing": alle,
            "epmc_ft": ft, "epmc_oa": oa, "source": src, "id": ident}


def measure(dois: list[str], *, pause: float = 0.25, armed: bool = True) -> list[CitationCoverage]:
    """Mål dekningsgrad begge veier. Ingen OpenAlex-kall.

    Armeres først: et nullresultat teller ikke før målingen har truffet på et
    verk vi vet er sitert.
    """
    ut: list[CitationCoverage] = []
    with httpx.Client(timeout=60, follow_redirects=True) as c:
        if armed:
            arm(c)
        for doi in dois:
            cc = CitationCoverage(doi=doi)
            try:
                cc.crossref_count = crossref_count(c, doi)
                cc.epmc_source, cc.epmc_id, cc.pmcid = epmc_ids(c, doi)
                if cc.epmc_source and cc.epmc_id:
                    cc.epmc_citing, cc.epmc_citing_ft, cc.epmc_citing_oa = \
                        epmc_citations(c, cc.epmc_source, cc.epmc_id)
            except Exception as e:                     # noqa: BLE001
                cc.error = f"{type(e).__name__}: {str(e)[:60]}"
            ut.append(cc)
            time.sleep(pause)
    return ut


def summarise(rows: list[CitationCoverage]) -> dict:
    ok = [r for r in rows if r.error is None]
    cr_tot = sum(r.crossref_count or 0 for r in ok)
    ep_tot = sum(r.epmc_citing or 0 for r in ok)
    ft_tot = sum(r.epmc_citing_ft or 0 for r in ok)
    oa_tot = sum(r.epmc_citing_oa or 0 for r in ok)
    andeler = sorted(r.epmc_share_of_crossref for r in ok
                     if r.epmc_share_of_crossref is not None)
    ft_andeler = sorted(r.fulltext_share for r in ok if r.fulltext_share is not None)
    def median(xs):
        return xs[len(xs) // 2] if xs else None
    return {
        "n": len(rows), "n_ok": len(ok),
        "n_in_epmc": sum(1 for r in ok if r.epmc_id),
        "crossref_citations_total": cr_tot,
        "epmc_citations_total": ep_tot,
        "epmc_citations_with_fulltext": ft_tot,
        "epmc_citations_open_access": oa_tot,
        "epmc_share_of_crossref": (ep_tot / cr_tot) if cr_tot else None,
        "fulltext_share_of_epmc": (ft_tot / ep_tot) if ep_tot else None,
        "searchable_share_of_all": (ft_tot / cr_tot) if cr_tot else None,
        "median_epmc_share_per_work": median(andeler),
        "median_fulltext_share_per_work": median(ft_andeler),
        "n_cited_but_absent_from_epmc": sum(1 for r in ok if r.crossref_count and not r.epmc_citing),
    }
