"""Recall-sett 2: dokumenter den utvidede markørlisten aldri har sett.

Sett 1 (ADDENDUM-06) ga v1-filteret 0/28 recall. Listen ble deretter utvidet med
36 tillegg, hvert lest ut av en av de 28 bommene. Recall etter utvidelsen er
28/28 mot **samme** fasit — en øvre grense, ikke en måling. Sett 2 måler den
utvidede listen på materiale som ikke har bidratt med en eneste markør.

Sett 1 hadde også et sjangerhull: ingen av de 30 dokumentene var en diplomatisk
kildeutgivelse eller humanistisk kildearbeid, og de ti døde markørene
(``remains unread`` og de ni andre) ble beholdt nettopp fordi nullresultatet
deres kom fra et materiale som mangler sjangeren. Sett 2 henter derfor 15 av 40
fra humaniora via DOAJ. Europe PMC dekker ikke feltet.

**Kravene håndheves før lesing, ikke etter.** Sett 1 mistet tid på at spansk,
gresk og italiensk materiale ble oppdaget midt i lesingen. Her er språk avgjort
med en språkdetektor på den faktisk uttrukne teksten, ikke med stoppord og ikke
fra metadata: DOAJ-artikkelposter har oftest ``bibjson.language: null``, og
EPMC-feltet ``language`` er forlagets påstand.

Rekkefølgen er fastsatt av målefrøet (734248, ADDENDUM-01). Kandidatene
behandles i frørekkefølge, og de første som oppfyller alle krav utgjør settet.
Hver forkastelse føres med grunn, slik at frafallet kan rapporteres per
kriterium.
"""

from __future__ import annotations

import json
import os
import random
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable, Mapping, Sequence

#: Målefrøet fra ADDENDUM-01. Ikke prereg-frøet: dette er et måleinstrument.
SEED = 734248

YEAR_FROM, YEAR_TO = 2015, 2020

#: Kvoter. Fylles ikke opp på tvers: får vi ikke 15 humanistiske, rapporteres
#: tallet, og biomedisin utvides ikke for å nå 40.
QUOTA = {"biomed": 25, "humaniora": 15}

#: Fagkvoter innenfor humaniora. **Nødvendig, ikke pynt.** Et ustratifisert
#: trekk over hele DOAJ-puljen ga 0 historie og 0 arkeologi: teologiske
#: tidsskrifter serverer lang HTML-fulltekst som passerer portene, mens
#: historie- og arkeologikandidatene oftest er landingssider eller ikke
#: engelskspråklige. Trekket ble derfor gjort om per fag, før lesing.
#: Et fag som ikke fyller kvoten fylles ikke opp av et annet.
QUOTA_FAG = {
    "historie": 3,
    "arkeologi": 3,
    "filologi": 2,
    "klassiske-fag": 2,
    "religionsvitenskap": 2,
    "bibelvitenskap": 2,
    "diplomatikk-arkiv": 1,
}

#: LCC-koder i DOAJ for de fagene oppdraget nevner, pluss de tre som bærer
#: kildearbeidssjangeren sett 1 manglet: CD diplomatikk og arkiv, CN epigrafi,
#: Z paleografi og håndskrifter.
LCC_HUMANIORA: tuple[tuple[str, str], ...] = (
    ("D", "historie"),
    ("CC", "arkeologi"),
    ("CD", "diplomatikk, arkiv, segl"),
    ("CN", "epigrafi"),
    ("P", "filologi og lingvistikk"),
    ("PA", "klassisk filologi"),
    ("BL", "religionsvitenskap"),
    ("BR", "kristendomshistorie"),
    ("BS", "bibelvitenskap"),
    ("Z", "paleografi, bok- og skrifthistorie"),
)

#: Minste uttrukne tekst for at et dokument skal kunne leses i sin helhet.
#: Under dette er det et sammendrag eller en landingsside, ikke en artikkel.
MIN_CHARS = 6_000

#: Tegngrensen alene holder ikke. En OJS-landingsside med tysk sammendrag,
#: nøkkelord, forfatteropplysninger og sitatforslag kom over 6 000 tegn på 42
#: setninger, uten en eneste setning fra artikkelen. Setningstallet skiller
#: metadata fra løpende prosa.
#:
#: Gulvet gjelder **bare HTML-ruten**. Der er landingssiden feilmodusen: lenken
#: fra DOAJ peker på den, og galleyen finnes ikke alltid. JATS-endepunktet
#: svarer fulltekst eller 404, og en kort JATS-artikkel er en kort artikkel —
#: en kommentar på 43 setninger løpende prosa er et ekte dokument, ikke en
#: landingsside. Å bruke gulvet der ville kastet dokumenter på feil grunnlag.
MIN_SENTENCES = 60
ROUTES_WITH_SENTENCE_FLOOR = frozenset({"html"})


def passes_length(rows: Sequence[Mapping], text: str, rute: str) -> str | None:
    """Lengdekravene. Returnerer frafallsgrunn eller None."""
    if len(text) < MIN_CHARS:
        return "for-kort"
    if rute in ROUTES_WITH_SENTENCE_FLOOR and len(rows) < MIN_SENTENCES:
        return "for-kort"
    return None

#: Språkkravet. Detektoren må gi engelsk som topp med minst denne sannsynligheten.
MIN_EN_PROB = 0.90

#: Andel tegn utenfor latinsk skrift som tvinger forkastelse. Sett 1 slapp
#: gjennom et dokument med 69 % greske tegn på en stoppordheuristikk.
MAX_NONLATIN = 0.10

#: Andel kontroll- og erstatningstegn som tvinger forkastelse. En DOAJ-lenke
#: pekte på et Word-dokument, og uttrekket ble 67 % binærsøppel — blant annet
#: metadata fra en printerdriver — med leselig engelsk imellom. Språkporten
#: slapp det gjennom fordi den leselige delen var engelsk. Målt over settet
#: ligger alle andre dokumenter under 1 %, så grensen skiller uten skjønn.
MAX_GARBAGE = 0.05


def garbage_share(text: str) -> float:
    """Andel kontroll-, erstatnings- og uassignerte tegn."""
    if not text:
        return 0.0
    d = sum(1 for c in text
            if c == "\ufffd" or unicodedata.category(c) in ("Cc", "Cf", "Co", "Cs", "Cn"))
    return d / len(text)

SJANGRE = ("forskningsartikkel", "oversiktsartikkel", "kildeutgivelse",
           "avhandling", "konferansebidrag")


# --------------------------------------------------------------------------- #
# Frø og rekkefølge
# --------------------------------------------------------------------------- #

def seeded_dates(n: int, *, seed: int = SEED,
                 year_from: int = YEAR_FROM, year_to: int = YEAR_TO) -> list[str]:
    """n datoer i vinduet, trukket med frøet, sortert og uten duplikater.

    Europe PMC ignorerer ``page`` for et filter-bare-søk (målt: side 1 og side
    97 ga identiske treff). Datostratifisering er derfor måten å nå forbi de
    første 25 postene på, og den er reproduserbar fra frøet alene.
    """
    start = date(year_from, 1, 1)
    span = (date(year_to, 12, 31) - start).days
    rng = random.Random(seed)
    ut: set[str] = set()
    while len(ut) < n:
        ut.add((start + timedelta(days=rng.randint(0, span))).isoformat())
    return sorted(ut)


def seeded_order(items: Sequence, *, seed: int = SEED) -> list:
    """Kandidatene i frørekkefølge. Stokkingen skjer på en kopi."""
    ut = list(items)
    random.Random(seed).shuffle(ut)
    return ut


# --------------------------------------------------------------------------- #
# Utelukkelse
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Exclusions:
    """Alt som er sett før: lest, hentet, eller funnet ved frasesøk."""

    work: frozenset[str] = frozenset()
    pmcid: frozenset[str] = frozenset()
    doi: frozenset[str] = frozenset()
    pmid: frozenset[str] = frozenset()

    @classmethod
    def from_json(cls, path: Path) -> "Exclusions":
        d = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            work=frozenset(d.get("work", [])),
            pmcid=frozenset(d.get("pmcid", [])),
            doi=frozenset(norm_doi(x) for x in d.get("doi", []) if x),
            pmid=frozenset(d.get("pmid", [])),
        )

    def hit(self, *, work: str | None = None, pmcid: str | None = None,
            doi: str | None = None, pmid: str | None = None) -> str | None:
        """Hvilken identifikator som er sett før, eller None."""
        if work and work in self.work:
            return f"work:{work}"
        if pmcid and pmcid in self.pmcid:
            return f"pmcid:{pmcid}"
        if doi and norm_doi(doi) in self.doi:
            return f"doi:{norm_doi(doi)}"
        if pmid and pmid in self.pmid:
            return f"pmid:{pmid}"
        return None


def norm_doi(s: str) -> str:
    s = (s or "").strip().lower()
    for pre in ("https://doi.org/", "http://doi.org/", "doi:"):
        if s.startswith(pre):
            s = s[len(pre):]
    return s


# --------------------------------------------------------------------------- #
# Språk, avgjort på teksten
# --------------------------------------------------------------------------- #

_LATIN_OK = re.compile(r"[\s\d\W]", re.UNICODE)


def nonlatin_share(text: str) -> float:
    """Andel bokstaver som ikke er latinsk skrift."""
    bokstaver = [c for c in text if c.isalpha()]
    if not bokstaver:
        return 0.0
    ikke = sum(1 for c in bokstaver if "LATIN" not in unicodedata.name(c, ""))
    return ikke / len(bokstaver)


@dataclass(frozen=True)
class LangVerdict:
    ok: bool
    top: str
    prob: float
    nonlatin: float
    grunn: str = ""
    fordeling: tuple[tuple[str, float], ...] = ()


def body_text(rows: Sequence[Mapping], *, drop_head: int = 5,
              keep: float = 0.75) -> str:
    """Kroppsteksten: uten tittelblokk og uten litteraturlisten.

    Språk på hele teksten er ikke nok i noen retning. En spanskspråklig artikkel
    med langt engelsk sammendrag kan gi engelsk på helheten, og en
    engelskspråklig artikkel med spansk litteraturliste kan gi spansk på siste
    tredjedel. Begge ble målt: obsidian-artikkelen i sett 2 hadde spansk
    referanseliste og engelsk kropp, Cicero-landingssiden hadde tysk
    sammendrag og ingen kropp.
    """
    n = len(rows)
    stop = max(drop_head + 1, int(n * keep))
    return " ".join(r["text"] for r in list(rows)[drop_head:stop])


def language_verdict(text: str, *, min_prob: float = MIN_EN_PROB,
                     max_nonlatin: float = MAX_NONLATIN) -> LangVerdict:
    """Engelsk avgjort med detektor, ikke med stoppord.

    Detektoren er ``langdetect`` med fast frø. Den kalles på den uttrukne
    teksten, og begge tallene føres: en kildeutgivelse kan ha latinsk eller
    gammelnorsk kildetekst med engelsk apparat rundt, og da skal andelen sees.
    """
    from langdetect import DetectorFactory, detect_langs
    from langdetect.lang_detect_exception import LangDetectException

    DetectorFactory.seed = 0
    ikke_latin = nonlatin_share(text)
    try:
        fordeling = tuple((str(x.lang), float(x.prob)) for x in detect_langs(text))
    except LangDetectException as e:
        return LangVerdict(False, "?", 0.0, ikke_latin, f"detektor feilet: {e}")
    top, prob = fordeling[0]
    if ikke_latin > max_nonlatin:
        return LangVerdict(False, top, prob, ikke_latin,
                           f"ikke-latinsk skrift {ikke_latin:.0%}", fordeling)
    if top != "en":
        return LangVerdict(False, top, prob, ikke_latin,
                           f"språk {top} ({prob:.2f})", fordeling)
    if prob < min_prob:
        return LangVerdict(False, top, prob, ikke_latin,
                           f"engelsk bare {prob:.2f}", fordeling)
    return LangVerdict(True, top, prob, ikke_latin, "", fordeling)


# --------------------------------------------------------------------------- #
# Identitet: er uttrekket dokumentet posten beskriver?
# --------------------------------------------------------------------------- #

#: Andel av tittelens ord (minst fire tegn) som må finnes blant ordene i
#: uttrekket når DOI-en ikke står der. Satt før identitetsrevisjonen ble kjørt
#: på kandidatene, ikke kalibrert mot dem.
MIN_TITLE_SHARE = 0.6


@dataclass(frozen=True)
class IdentityVerdict:
    ok: bool
    andel: float
    doi_funnet: bool
    grunn: str = ""


def _fold(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).casefold()


def title_tokens(title: str) -> list[str]:
    """Tittelens ord på minst fire tegn, foldet, i rekkefølge, uten duplikater."""
    return list(dict.fromkeys(re.findall(r"\w{4,}", _fold(title))))


def identity_verdict(text: str, *, title: str, doi: str | None = None,
                     min_share: float = MIN_TITLE_SHARE) -> IdentityVerdict:
    """Hører teksten til posten? DOI i teksten, ellers tittelens ord.

    Uten denne porten kunne en landingsside gi fra seg feil PDF: en lenke til
    en annen artikkel, eller til et annet nettsted. Språk- og
    lengdeportene målte da et annet dokument enn det som sto i utvalget. To av
    de 15 humanistiske i første versjon av sett 2 var slike (ADDENDUM-07).

    DOI-en søkes med mellomrom fjernet, fordi PDF-uttrekk bryter lange lenker
    over linjer. En tittel med færre enn to ord avgjøres ikke uten DOI.
    """
    flat = _fold(text)
    doi_funnet = bool(doi) and norm_doi(doi) in re.sub(r"\s+", "", flat)
    tok = title_tokens(title)
    ord_i_tekst = set(re.findall(r"\w{4,}", flat))
    andel = sum(t in ord_i_tekst for t in tok) / len(tok) if tok else 0.0
    if doi_funnet:
        return IdentityVerdict(True, andel, True)
    if len(tok) < 2:
        return IdentityVerdict(False, andel, False,
                               "tittelen for kort til å avgjøre uten DOI")
    if andel >= min_share:
        return IdentityVerdict(True, andel, False)
    return IdentityVerdict(False, andel, False,
                           f"tittelandel {andel:.2f} under {min_share}")


# --------------------------------------------------------------------------- #
# Sjanger
# --------------------------------------------------------------------------- #

_REVIEW = re.compile(r"\b(systematic review|meta[- ]analysis|scoping review|"
                     r"narrative review|a review|literature review|review of)\b", re.I)
_EDITION = re.compile(r"\b(edition|edited (text|by)|critical apparatus|cartulary|"
                      r"charters?|diplomatari|transcription of|catalogue of|"
                      r"inscriptions? (of|from)|codex|manuscript)\b", re.I)
_THESIS = re.compile(r"\b(thesis|dissertation)\b", re.I)
_CONF = re.compile(r"\b(proceedings|conference|symposium|workshop)\b", re.I)


def genre_from_metadata(*, title: str = "", pub_types: Iterable[str] = (),
                        journal: str = "") -> str:
    """Første anslag på sjanger, før lesing. Rettes om lesingen viser noe annet.

    Rekkefølgen er bevisst: avhandling og konferansebidrag avgjøres av typen,
    kildeutgivelse og oversiktsartikkel av tittelen. Et anslag er et anslag, og
    fasiten bærer den verdien lesingen ga.
    """
    typer = " ".join(str(t) for t in pub_types).lower()
    tekst = f"{title} {journal}"
    if _THESIS.search(typer) or _THESIS.search(tekst):
        return "avhandling"
    if _CONF.search(typer) or _CONF.search(journal):
        return "konferansebidrag"
    if "review" in typer or _REVIEW.search(title):
        return "oversiktsartikkel"
    if _EDITION.search(title):
        return "kildeutgivelse"
    return "forskningsartikkel"


# --------------------------------------------------------------------------- #
# Kravene, håndhevet før lesing
# --------------------------------------------------------------------------- #

@dataclass
class Candidate:
    """Én kandidat med alt som trengs for å avgjøre den før lesing."""

    kilde: str                      # epmc | doaj
    delsett: str                    # biomed | humaniora
    doc_id: str
    doi: str | None = None
    pmcid: str | None = None
    pmid: str | None = None
    work: str | None = None
    year: int | None = None
    title: str = ""
    journal: str = ""
    pub_types: tuple[str, ...] = ()
    lcc: tuple[str, ...] = ()
    fag: str = ""
    url: str | None = None
    sjanger: str = ""
    chars: int = 0
    lang: LangVerdict | None = None
    forkastet: str | None = None    # grunn, eller None om den står


REASONS = ("aar", "utelukket", "ingen-tekst", "identitet", "for-kort", "sprak",
           "sprak-kropp", "soppel", "hentefeil")


def year_ok(year: int | None, *, lo: int = YEAR_FROM, hi: int = YEAR_TO) -> bool:
    return year is not None and lo <= year <= hi


@dataclass
class Attrition:
    """Frafall per kriterium, i den rekkefølgen kriteriene ble prøvd.

    Telleren teller **forkastelser**, ikke vurderinger: en kandidat som står,
    får ingen rad her. Antall vurderte er forkastede pluss valgte, og det tallet
    må komme utenfra — ellers ville «vurdert» sett ut som om alle falt.
    """

    counts: dict[str, int] = field(default_factory=lambda: {r: 0 for r in REASONS})
    forkastet: int = 0

    def note(self, grunn: str) -> None:
        if grunn not in self.counts:
            raise KeyError(f"ukjent frafallsgrunn: {grunn}")
        self.forkastet += 1
        self.counts[grunn] += 1

    def as_dict(self, *, valgt: int | None = None) -> dict:
        ut = {"forkastet": self.forkastet, "per_kriterium": dict(self.counts)}
        if valgt is not None:
            ut["valgt"] = valgt
            ut["vurdert"] = valgt + self.forkastet
        return ut


# --------------------------------------------------------------------------- #
# Nettlaget. Ingen OpenAlex-kall: Europe PMC, Crossref og DOAJ.
# --------------------------------------------------------------------------- #

EPMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
EPMC_FT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
CROSSREF = "https://api.crossref.org/works/{doi}"
DOAJ_ARTICLES = "https://doaj.org/api/search/articles/{query}"

#: Kontaktadressen sendes bare når OPENALEX_MAILTO er satt i miljøet, som i
#: harvest/openalex.py. Ingen adresse ligger i koden (deponeringskrav).
UA = "gjenopptak/0.1 (forskningsprosjekt, recall-sett 2)" + (
    f" mailto:{os.environ['OPENALEX_MAILTO'].strip()}" if os.environ.get("OPENALEX_MAILTO", "").strip() else ""
)


def headers(accept: str = "application/json") -> dict[str, str]:
    """Accept settes eksplisitt. JATS-endepunktet svarer 406 på application/json
    — det var en falsk negativ i ADDENDUM-01 før den ble rettet."""
    return {"User-Agent": UA, "Accept": accept}


def epmc_day(client, dato: str, *, raw_dir: Path | None = None,
             page_size: int = 25) -> list[dict]:
    """Åpne engelskspråklige poster med fulltekst i EPMC, publisert én dag.

    Datostratifisering fordi ``page`` ikke virker for et filter-bare-søk: side 1
    og side 97 ga identiske treff i samme sekund. Dagene kommer fra frøet.
    """
    q = (f'(FIRST_PDATE:[{dato} TO {dato}]) AND OPEN_ACCESS:Y AND IN_EPMC:Y '
         f'AND LANG:eng')
    r = client.get(EPMC_SEARCH, params={"query": q, "format": "json",
                                       "pageSize": page_size, "resultType": "core"},
                   headers=headers(), timeout=90)
    r.raise_for_status()
    if raw_dir is not None:
        from .openalex import write_raw
        write_raw(r.content, str(r.url), raw_dir, stem=f"r2-epmc-{dato}")
    return r.json().get("resultList", {}).get("result", [])


def epmc_jats(client, pmcid: str) -> bytes:
    """JATS-XML for ett PMC-id. Accept må være XML."""
    r = client.get(EPMC_FT.format(pmcid=pmcid), headers=headers("application/xml"),
                   timeout=120)
    r.raise_for_status()
    return r.content


def crossref_work(client, doi: str) -> dict:
    """Uavhengig metadatasjekk: år, type, språk, emne, lenker."""
    r = client.get(CROSSREF.format(doi=doi), headers=headers(), timeout=60)
    r.raise_for_status()
    return r.json().get("message", {})


def doaj_search(client, query: str, *, page: int = 1, page_size: int = 100) -> dict:
    import urllib.parse
    url = DOAJ_ARTICLES.format(query=urllib.parse.quote(query, safe=""))
    r = client.get(url, params={"pageSize": page_size, "page": page},
                   headers=headers(), timeout=90)
    r.raise_for_status()
    return r.json()


#: Lenker som peker på en fulltekstgalley i OJS og liknende. PDF foretrekkes:
#: en landingsside gir sammendraget, ikke artikkelen.
_GALLEY = re.compile(
    r'href="([^"]*(?:/article/(?:view|download)/[^"]*|\.pdf(?:\?[^"]*)?))"', re.I)


_OJS_VIEW_GALLEY = re.compile(r"/article/view/([^/?#]+)/([^/?#]+)")


def galley_links(html: str, base: str) -> list[str]:
    """Kandidatlenker til fulltekst, PDF først, absolutte og uten duplikater.

    I OJS 3 er ``article/view/ID/GALLEY`` en HTML-ramme med en innebygd
    PDF-viser; selve filen ligger på ``article/download/ID/GALLEY``, som er
    lenken rammen selv laster. Uten omskrivingen hentet høsteren rammen, fant
    et par hundre tegn, og forkastet artikkelen som for kort. Det rammet
    systematisk tidsskrifter som leverer PDF, og favoriserte dem som leverer
    HTML-fulltekst — en skjevhet i verktøyet, ikke i materialet (ADDENDUM-07).

    Sorteringen løfter **enhver** PDF-lenke på siden, også lenker til andre
    artikler og til andre nettsteder. Lenkelisten sier derfor ikke
    hvilken fil som er artikkelen; det avgjør bare ``identity_verdict`` på den
    uttrukne teksten, per lenke. Uten den porten fikk to av 15 humanistiske
    dokumenter i sett 2 feil tekst (ADDENDUM-07).
    """
    from urllib.parse import urljoin
    ut: list[str] = []

    def legg_til(u: str) -> None:
        if u not in ut:
            ut.append(u)

    for treff in _GALLEY.findall(html):
        u = urljoin(base, treff.replace("&amp;", "&"))
        m = _OJS_VIEW_GALLEY.search(u)
        if m:
            legg_til(u[:m.start()] + f"/article/download/{m.group(1)}/{m.group(2)}" + u[m.end():])
        legg_til(u)
    ut.sort(key=lambda u: (0 if ".pdf" in u.lower() or "/download/" in u.lower() else 1))
    return ut


#: Blokkelementer får linjeskift, ellers smelter avsnitt sammen til én setning
#: og setningsdeleren i L1 ser «…resultsMethods…» som ett ord.
_BLOCK = frozenset("p div br li h1 h2 h3 h4 h5 h6 tr td section article "
                   "blockquote figcaption caption dd dt".split())


def html_to_text(blob: bytes) -> str:
    """Tekst fra HTML med lxml. Skript, stil og navigasjon fjernes."""
    from lxml import html as lh
    try:
        tre = lh.fromstring(blob)
    except Exception:                                        # noqa: BLE001
        return ""
    for tag in ("script", "style", "nav", "header", "footer", "noscript", "form"):
        for el in list(tre.iter(tag)):
            if el.getparent() is not None:
                el.getparent().remove(el)
    for el in tre.iter():
        if isinstance(el.tag, str) and el.tag.lower() in _BLOCK:
            el.tail = "\n" + (el.tail or "")
            if el.text:
                el.text = "\n" + el.text
    tekst = tre.text_content()
    tekst = re.sub(r"[ \t]+", " ", tekst)
    return re.sub(r"\n{3,}", "\n\n", tekst).strip()


def sentences_from_text(text: str, *, doc_id: str, parsed_at: str | None = None,
                        parser: str = "html") -> list[dict]:
    """Tekst → sentences-poster med opphav ``parser`` og tom seksjonsetikett.

    Samme form som PDF-ruten (ADR-0007): en HTML-galley bærer ingen kildemerket
    seksjonsinndeling vi kan stole på, og den ærlige verdien er tom
    ``section_raw`` med opphav ``parser`` — ikke en gjetning fra klassenavn.
    """
    from datetime import datetime, timezone

    from ..parse.jats import split_sentences
    from ..parse.pdfroute import NO_SECTION_MODEL, blocks_from_text

    parsed_at = parsed_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows: list[dict] = []
    offset = index = 0
    for blokk in blocks_from_text(text):
        for start, end, setning in split_sentences(blokk):
            rows.append({
                "schema_version": "sentences-1",
                "sentence_id": f"{doc_id}:{index}",
                "doc_id": doc_id,
                "text": setning,
                "char_start": offset + start,
                "char_end": offset + end,
                "sentence_index": index,
                "section_raw": "",
                "section_path_raw": [],
                "section_id_raw": None,
                "section_type_raw": None,
                "section_norm": "unknown",
                "section_norm_rule": f"{parser}-ingen-seksjonsmodell",
                "section_label_provenance": "parser",
                "parser_version": parser,
                "parser_model_version": NO_SECTION_MODEL,
                "block_kind": "p",
                "parser": f"gjenopptak.harvest.recallset2/{parser}",
                "parsed_at": parsed_at,
            })
            index += 1
        offset += len(blokk) + 1
    return rows
