"""Måleinndata og måleutfall som deponeres samlet i ``maalefiler.zip`` (fra v0.6.0).

Bakgrunnen står i ``docs/DEPOSITUMSKRAV-2026-10-10.md``: depositumet til og med v0.5.0 bar dokumentene og
fase 3, men ikke filene de fleste publiserte tallene er regnet fra. Listen under er hver fil et låst addendum
navngir med sha256, og hver fil som bærer et utfall, slik de ble slått opp 10.10.2026.

Fire regler avgjør hva som går inn:

* **Tekstfelt deponeres ikke** (LISENSAUDIT-2026-09-28 § 4 C). I en fil som bærer passasjer eller setninger i
  egne felt, byttes verdien i hvert slikt felt med sha256 og lengde.
* **Ordrette utdrag tas ut.** Begrunnelsene til modeller og kodere siterer passasjene. Hvert ordrett utdrag på
  ``MIN_UTDRAG`` tegn eller mer fra en blindfilpassasje byttes med et merke som bærer lengde og sha256 av
  utdraget, så filen kan etterprøves mot Vault-kopien. Titler er metadata og røres ikke. Etter pakking søkes hvert
  medlem på nytt, og byggingen feiler om et utdrag står igjen.
* **Nøkkelregelen** (eierens avgjørelse 30.09.2026): en nøkkel holdes utenfor til målingen den blinder er ferdig
  og rapportert.
* **Koder 1s verdikter** deponeres uten tekst og uten nøkkelfelt, i samme form som koder 2s.

Filene er altså ikke fri for andres ord: utdrag under ``MIN_UTDRAG`` tegn står, og søket kjenner bare passasjene i
blindfilene. Zip-filen bygges med faste tidsstempler, så samme inndata gir samme bytes.
"""
from __future__ import annotations

import hashlib
import json
import unicodedata
import zipfile
from array import array
from bisect import bisect_left
from pathlib import Path

ZIPNAVN = "maalefiler.zip"

#: Korteste ordrette utdrag fra en blindfilpassasje som tas ut. Søket prøver hvert vindu på ``MIN_UTDRAG`` tegn,
#: fra hver posisjon, og utvider treffet til hele det sammenfallende spennet; blanktegn regnes som like.
MIN_UTDRAG = 50
#: Felt som er bibliografiske metadata. En tittel som også står i en passasje, er ikke et utdrag av den.
METADATAFELT = ("tittel", "title")

#: Felt som bærer andres tekst. Verdien byttes med {"sha256": …, "tegn": …} uansett lengde.
TEKSTFELT = ("passage_text", "sentence_text", "passasjetekst", "passasje", "setning", "text", "tekst",
             "datatilgang_seksjon", "utdata_raa")

#: Deponeres byte for byte. Stier relative til gjenopptak-kilder/ på Vault.
SOM_DE_ER: tuple[str, ...] = (
    "arbeidsliste/koder-c-komplett.json",
    "arbeidsliste/okt-1-verdikter.jsonl",
    "arbeidsliste/okt-2-rest-verdikter.jsonl",
    "arbeidsliste/okt-2-verdikter.jsonl",
    "arbeidsliste/okt-3-rest-verdikter.jsonl",
    "arbeidsliste/okt-3-verdikter.jsonl",
    "arbeidsliste/okt-4-rest-verdikter.jsonl",
    "arbeidsliste/okt-4-verdikter.jsonl",
    "arbeidsliste/okt-5-verdikter.jsonl",
    "arbeidsliste/okt-6-rest-verdikter.jsonl",
    "arbeidsliste/okt-6-verdikter.jsonl",
    "arbeidsliste/okt-7-rest-verdikter.jsonl",
    "arbeidsliste/okt-7-verdikter.jsonl",
    "arbeidsliste/okt-8-verdikter.jsonl",
    "arbeidsliste/presisjon-100-maal.json",
    "arbeidsliste/presisjon-100-verdikter.jsonl",
    "arbeidsliste/presisjon-rest-verdikter.jsonl",
    "ekstraksjon/2026-09-26/2d-blind-presisjon.json",
    "ekstraksjon/2026-09-26/2d-blind-q-100-NOKKEL.json",
    "ekstraksjon/2026-09-26/2d-blind-q-100-VERDIKTER.json",
    "ekstraksjon/2026-09-26/2d-blind-q-regler.md",
    "ekstraksjon/2026-09-26/2d-recall.json",
    "ekstraksjon/2026-09-26/2d-tid.json",
    "ekstraksjon/2026-09-26/a17-2p-mot-2d.json",
    "ekstraksjon/2026-09-26/a19-a20-full-regelfil.json",
    "ekstraksjon/2026-09-26/a19b-utfall.json",
    "ekstraksjon/2026-09-26/addendum-18/a18-kappa.json",
    "ekstraksjon/2026-09-26/addendum-18/haiku45-avkuttet-rekjort.jsonl",
    "ekstraksjon/2026-09-26/addendum-18/haiku45-dommer.jsonl",
    "ekstraksjon/2026-09-26/addendum-18/sonnet5-pass1-avkuttet-rekjort.jsonl",
    "ekstraksjon/2026-09-26/addendum-18/sonnet5-pass1-dommer.jsonl",
    "ekstraksjon/2026-09-26/addendum-18/sonnet5-pass2-dommer.jsonl",
    "ekstraksjon/2026-09-26/addendum-19/opus5-b-dommer.jsonl",
    "ekstraksjon/2026-09-26/addendum-19/opus5-dommer.jsonl",
    "ekstraksjon/2026-09-26/addendum-20/a20-partiell.json",
    "ekstraksjon/2026-09-26/addendum-20/haiku45-dommer.jsonl",
    "ekstraksjon/2026-09-26/addendum-20/sonnet5-dommer.jsonl",
    "ekstraksjon/2026-09-26/b1-duplikatrate.json",
    "ekstraksjon/2026-09-26/b2-nevner.json",
    "ekstraksjon/2026-09-26/d1-2x2.json",
    "ekstraksjon/2026-09-26/h2-trekking.json",
    "ekstraksjon/2026-09-26/k1-de-27.json",
    "ekstraksjon/2026-09-26/k1-union-v2.json",
    "embeddings/kjoring.json",
    "embeddings/maaling.json",
    "falsifisering-2026-09-21/falsifisering-2026-09-21.json",
    "fase3/avbrudd-2026-09-29/determinisme.json",
    "fase3/lisens-per-verk-fase3.json",
    "fase3/presisjon/oppdrag-presisjon-MAL.md",
    "fase3/presisjon/sperreliste-presisjon.md",
    "fase4/trekkresultat-fase4.json",
    "form-ruter/a1-seksjon-2026-09-26.json",
    "form-ruter/a2-kombinasjon-2026-09-26.json",
    "form-ruter/a2-naersok-2026-09-26.json",
    "frames/frame-haandskrift-RAW.jsonl",
    "koder4/eksponerte-rader.json",
    "koder4/folsomhet-eksponering.json",
    "koder4/koder4-fable51-verdikter.jsonl",
    "koder4/koder4-resultat.json",
    "leser-lokal-ADDENDUM-24/kanari.json",
    "leser-lokal-ADDENDUM-24/kjoring.log",
    "leser-lokal-ADDENDUM-24/maaling.json",
    "leser-lokal-ADDENDUM-24/parti-01.json",
    "leser-lokal-ADDENDUM-24/parti-02.json",
    "leser-lokal-ADDENDUM-24/parti-03.json",
    "leser-lokal-ADDENDUM-24/parti-04.json",
    "leser-lokal-ADDENDUM-24/parti-05.json",
    "leser-lokal-ADDENDUM-24/parti-06.json",
    "leser-lokal-ADDENDUM-24/parti-07.json",
    "leser-lokal-ADDENDUM-24/parti-08.json",
    "leser-lokal-ADDENDUM-24/parti-09.json",
    "leser-lokal-ADDENDUM-24/parti-10.json",
    "leser-lokal-ADDENDUM-24/parti-11.json",
    "leser-lokal-ADDENDUM-24/parti-12.json",
    "leser-lokal-ADDENDUM-24/parti-13.json",
    "leser-lokal-ADDENDUM-24/parti-14.json",
    "leser-lokal-ADDENDUM-24/parti-15.json",
    "leser-lokal-ADDENDUM-24/parti-16.json",
    "logs/coverage-addendum01.json",
    "logs/frame-diagnostics.json",
    "logs/has_fulltext-per-aar.json",
    "logs/kontroll-tekstvitenskap-H1-2026-09-13.json",
    "logs/kontrollkandidater.json",
    "logs/kvotedogn-2026-09-13-punkt4-logg.jsonl",
    "logs/leste-kontrollkandidater.json",
    "logs/nedlastbarhet.json",
    "logs/pipeline-test/l4-dekning-PIPELINETEST.json",
    "logs/pipeline-test/reparse-tall-ADDENDUM07.json",
    "logs/pipeline-test/summary-PIPELINETEST.json",
    "logs/rammeprove-energimodellering-sammendrag.json",
    "logs/recall-sett-meta.json",
    "logs/substitusjon.json",
    "presisjonssett-2026-09-20/presisjon-resultater.json",
    "presisjonssett/port-presisjonssett-verdikter.jsonl",
    "raw/kand-tv3-H1-gruppe1del0-9c8d4820ed97.json",
    "triage-loftbare-2026-09-26-kriterium.py",
    "triage-loftbare-2026-09-26.json",
    "utvalg/karakterisering-tekstvitenskap.json",
    "utvalg/trekkspesifikasjon-energimodellering.jsonl",
    "utvalg/utvalg-arkeologi.jsonl",
    "utvalg/utvalg-energimodellering.jsonl",
    "utvalg/utvalg-klinisk_epidemiologi.jsonl",
    "utvalg/utvalg-tekstvitenskap.jsonl",
    "verksniva-2026-09-26-kriterium-v2.py",
    "verksniva-2026-09-26-kriterium.py",
    "verksniva-blindverk-NOKKEL.json",
    "verksniva-blindverk-VERDIKTER.json",
)

#: Deponeres avledet, med tekstfeltene byttet ut. Navnet i zip-filen får «-uten-tekst» før endelsen.
UTEN_TEKST: tuple[str, ...] = (
    "ekstraksjon/2026-09-26/ekstraksjon2-logg.jsonl",
    "logs/anker-setninger.json",
    "logs/h1h4-funn.json",
    "logs/recall-sett-2-maaling.json",
    "logs/recall-sett-2.jsonl",
    "logs/recall-sett.jsonl",
    "presisjonssett/port-tvil.jsonl",
    "verksniva-2026-09-26-v2.json",
    "verksniva-2026-09-26.json",
)

#: Koder 1s verdikter etter ADDENDUM-10: (kilde, navn i zip, feltene som beholdes).
KODER1 = ("presisjonssett/port-presisjonssett-ADDENDUM10.jsonl",
          "presisjonssett/port-presisjonssett-verdikter-koder1-ADDENDUM10.jsonl",
          ("id", "ekte_treff", "min_klasse", "min_bedømbar", "tvil", "min_begrunnelse"))

#: Holdes utenfor, med grunn. Ført her for at fraværet skal være en beslutning og ikke en forglemmelse.
HOLDT_UTE: dict[str, str] = {
    "kandidat432/8-register.jsonl":
        "deponert som register-v2-indeks.jsonl",
    "presisjonssett/koder2-sammenlikning.json":
        "16 ordrette utdrag; versjonen uten tekst er deponert",
    "presisjonssett/port-presisjonssett-ADDENDUM10.jsonl":
        "tekst og nøkkelfelt; koder 1s verdikter deponeres avledet uten tekst og uten nøkkelfelt",
    "presisjonssett/port-presisjonssett-blind.jsonl":
        "tekst (lisensbeslutningen); deponert som indeks",
    "presisjonssett/port-presisjonssett-nokkel.jsonl":
        "nøkkelregelen: port-320 er blindfil for ADDENDUM-21 og -28, som er låst og ukjørt, og kilde for A-strata i ADDENDUM-27",
    "revisjon-2026-10/menneskevalidering/blind.jsonl":
        "tekst (lisensbeslutningen); utvalgsfila er deponert",
    "revisjon-2026-10/menneskevalidering/nokkel.jsonl":
        "nøkkelregelen: ADDENDUM-27 er ukjørt",
}

#: For store for zip-filen (over 1 MB hver). Ligger på Vault; sha256 her og i MANIFEST-VAULT.md.
FOR_STORE: dict[str, str] = {
    "frames/frame-tekstvitenskap-RAW.jsonl": "3a9389959ba3ea6cd3cf11ac05fb3d7604738a1514171248c36a706e7a4f852c",
    "frames/frame-energimodellering-HENTBAR.jsonl": "7df1b27a44ba939b3dde4cf11c72199e3a8134be5b06b99ccbaf39bc186c381e",
    "logs/hentingsprove-energimodellering-verdikter.jsonl": "4ef5f1cfc8fd5a41ea57d73245d81ef8e201a0a1de19e1b43e6f2c72d8697a2c",
    "frames/frame-energimodellering-RAW.jsonl": "56d80195d2df726fe49961269a2a4b2f215c6534cb9783c7dc66a1d725048209",
    "frames/frame-arkeologi-RAW.jsonl": "1050450fc774e56affc21c99e0ffc3c59682ff391c1e46163c69a50d5cdf241a",
    "frames/frame-klinisk_epidemiologi-RAW.jsonl": "ee783f99b184761b64a95a51603cc48910331628d2a3bd15d0e17240e5929ac5",
}


_FORM: dict[str, str] = {}


def _form(c: str) -> str:
    """Tegnet slik det sammenliknes: Unicode-form NFKD og uten skille mellom store og små bokstaver. «ﬁ» blir «fi»,
    «É» blir «e» fulgt av aksenttegnet, og et hardt mellomrom blir et mellomrom."""
    f = _FORM.get(c)
    if f is None:
        f = _FORM[c] = unicodedata.normalize("NFKD", unicodedata.normalize("NFKD", c).casefold())
    return f


def _norm(s: str) -> tuple[str, list[int]]:
    """Teksten slik den sammenliknes, og posisjonen i originalen for hvert tegn. Blanktegnsrekker er slått sammen til
    ett mellomrom; bokstavstørrelse og Unicode-form er jevnet ut (``_form``). Et sitat som bare har fått stor
    forbokstav, eller en ligatur løst opp, er fortsatt et ordrett utdrag."""
    ut, pos, forrige_blank = [], [], False
    for i, c in enumerate(s):
        for d in (c.lower() if c < "\x80" else _form(c)):
            if d.isspace():
                if not forrige_blank:
                    ut.append(" "); pos.append(i)
                forrige_blank = True
            else:
                ut.append(d); pos.append(i); forrige_blank = False
    return "".join(ut), pos


def passasjeindeks(blindfiler: list[Path]) -> tuple[str, array]:
    """Alle passasjene i blindfilene, normalisert og skjøtt med NUL, og en sortert tabell over hashen av hvert
    vindu på ``MIN_UTDRAG`` tegn i dem. Tabellen sier om et vindu kan være et utdrag; teksten avgjør det."""
    sett: dict[str, None] = {}
    for b in blindfiler:
        for l in b.read_text(encoding="utf-8").splitlines():
            if l.strip():
                t = _norm(json.loads(l)["tekst"])[0]
                if len(t) >= MIN_UTDRAG:
                    sett.setdefault(t)
    alt = "\x00".join(sett)
    tabell = array("q", sorted({hash(t[i:i + MIN_UTDRAG]) for t in sett for i in range(len(t) - MIN_UTDRAG + 1)}))
    return alt, tabell


def utdrag(s: str, passasjer: str, indeks: array) -> list[tuple[int, int]]:
    """Spennene i ``s`` (posisjoner i originalen) som gjengir en passasje ordrett over minst ``MIN_UTDRAG`` tegn."""
    if len(s) < MIN_UTDRAG or not len(indeks):
        return []
    n, pos = _norm(s)
    funn, i = [], 0
    while i <= len(n) - MIN_UTDRAG:
        vindu = n[i:i + MIN_UTDRAG]
        h = hash(vindu)
        k = bisect_left(indeks, h)
        j = passasjer.find(vindu) if k < len(indeks) and indeks[k] == h and "\x00" not in vindu else -1
        if j < 0:
            i += 1
            continue
        b = i + MIN_UTDRAG                                      # utvid mot høyre til spennet slutter
        while b < len(n) and j + (b - i) < len(passasjer) and n[b] == passasjer[j + (b - i)] != "\x00":
            b += 1
        funn.append((pos[i], pos[b - 1] + 1))
        i = b
    return funn


def ta_ut(s: str, passasjer: list[str], indeks: dict[str, tuple[int, int]]) -> tuple[str, int]:
    """``s`` med hvert ordrett utdrag byttet med et merke. Returnerer også antallet."""
    spenn = utdrag(s, passasjer, indeks)
    for a, b in reversed(spenn):
        u = s[a:b]
        s = s[:a] + f"[utdrag utelatt: {len(u)} tegn, sha256 {hashlib.sha256(u.encode('utf-8')).hexdigest()[:16]}]" + s[b:]
    return s, len(spenn)


def uten_utdrag(o, passasjer, indeks, teller: list[int], felt: str = ""):
    """Samme struktur, med ordrette utdrag tatt ut av hver strengverdi utenfor metadatafeltene."""
    if isinstance(o, dict):
        return {k: uten_utdrag(v, passasjer, indeks, teller, k) for k, v in o.items()}
    if isinstance(o, list):
        return [uten_utdrag(v, passasjer, indeks, teller, felt) for v in o]
    if isinstance(o, str) and felt not in METADATAFELT:
        ny, n = ta_ut(o, passasjer, indeks)
        teller[0] += n
        return ny
    return o


def utdrag_i_fil(navn: str, t: str, passasjer, indeks) -> int:
    """Antall ordrette utdrag i en fil, lest slik en leser ser den: JSON-strenger dekodet, annen tekst som den er."""
    def gå(o, felt=""):
        if isinstance(o, dict):
            return sum(gå(v, k) for k, v in o.items())
        if isinstance(o, list):
            return sum(gå(v, felt) for v in o)
        return len(utdrag(o, passasjer, indeks)) if isinstance(o, str) and felt not in METADATAFELT else 0
    try:
        if navn.endswith(".jsonl"):
            return sum(gå(json.loads(l)) for l in t.splitlines() if l.strip())
        if navn.endswith(".json"):
            return gå(json.loads(t))
    except ValueError:
        pass
    return len(utdrag(t, passasjer, indeks))


def rens(navn: str, b: bytes, passasjer, indeks) -> tuple[bytes, int]:
    """Bytene som deponeres, med ordrette utdrag tatt ut, og antallet. En fil uten utdrag kommer uendret tilbake."""
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        return b, 0
    if not utdrag_i_fil(navn, t, passasjer, indeks):
        return b, 0
    teller = [0]
    if navn.endswith(".jsonl"):
        ut = "".join(json.dumps(uten_utdrag(json.loads(l), passasjer, indeks, teller), ensure_ascii=False) + "\n"
                     for l in t.splitlines() if l.strip())
    elif navn.endswith(".json"):
        ut = json.dumps(uten_utdrag(json.loads(t), passasjer, indeks, teller), ensure_ascii=False, indent=1) + "\n"
    else:
        ut, teller[0] = ta_ut(t, passasjer, indeks)
    return ut.encode("utf-8"), teller[0]


def uten_tekst(o):
    """Samme struktur, med verdien i hvert tekstfelt byttet med sha256 og lengde."""
    if isinstance(o, dict):
        return {k: ({"sha256": hashlib.sha256(v.encode("utf-8")).hexdigest(), "tegn": len(v)}
                    if k in TEKSTFELT and isinstance(v, str) else uten_tekst(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [uten_tekst(v) for v in o]
    return o


def _jsonl(b: bytes) -> list:
    return [json.loads(l) for l in b.decode("utf-8").splitlines() if l.strip()]


def avled(sti: str, b: bytes) -> bytes:
    """Bytene som deponeres for en fil i ``UTEN_TEKST``."""
    if sti.endswith(".jsonl"):
        return "".join(json.dumps(uten_tekst(r), ensure_ascii=False) + "\n" for r in _jsonl(b)).encode("utf-8")
    return (json.dumps(uten_tekst(json.loads(b)), ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def koder1(b: bytes) -> bytes:
    """Koder 1s verdikter: bare feltene i ``KODER1``, i filens rekkefølge."""
    return "".join(json.dumps({k: r[k] for k in KODER1[2]}, ensure_ascii=False) + "\n" for r in _jsonl(b)).encode("utf-8")


def navn_uten_tekst(sti: str) -> str:
    p = Path(sti)
    return str(p.with_name(p.stem + "-uten-tekst" + p.suffix))


def pakk(vault: Path, mål: Path, blindfiler: list[Path] | None = None, *, indeks: tuple | None = None) -> list[dict]:
    """Skriv zip-filen og returner innholdslisten. Mangler en kilde, eller står et utdrag igjen, feiler byggingen.
    ``indeks`` er et ferdig resultat fra ``passasjeindeks``, når byggeren alt har regnet det."""
    passasjer, indeks = indeks or passasjeindeks(blindfiler or [])
    medlemmer: list[tuple[str, bytes, str, str]] = []       # (navn i zip, bytes, kilde, form)
    for sti in SOM_DE_ER:
        medlemmer.append((sti, (vault / sti).read_bytes(), sti, "som den er"))
    for sti in UTEN_TEKST:
        medlemmer.append((navn_uten_tekst(sti), avled(sti, (vault / sti).read_bytes()), sti, "uten tekst"))
    medlemmer.append((KODER1[1], koder1((vault / KODER1[0]).read_bytes()), KODER1[0], "uten tekst og nøkkelfelt"))
    innhold = []
    with zipfile.ZipFile(mål, "w", zipfile.ZIP_DEFLATED) as z:
        for navn, b, kilde, form in sorted(medlemmer):
            b, n = rens(navn, b, passasjer, indeks)
            if n:
                form = ("utdrag utelatt" if form == "som den er" else form + ", utdrag utelatt")
            igjen = utdrag_i_fil(navn, b.decode("utf-8", "replace"), passasjer, indeks)
            if igjen:
                raise RuntimeError(f"{navn}: {igjen} ordrette utdrag på {MIN_UTDRAG} tegn eller mer står igjen")
            z.writestr(zipfile.ZipInfo(f"maalefiler/{navn}", date_time=(1980, 1, 1, 0, 0, 0)), b,
                       compress_type=zipfile.ZIP_DEFLATED)
            innhold.append({"navn": navn, "kilde": f"vault:{kilde}", "form": form, "utdrag_utelatt": n, "bytes": len(b),
                            "sha256": hashlib.sha256(b).hexdigest(),
                            "kilde_sha256": hashlib.sha256((vault / kilde).read_bytes()).hexdigest()})
    return innhold
