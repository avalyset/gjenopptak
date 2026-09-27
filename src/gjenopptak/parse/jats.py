"""JATS-XML → sentences.jsonl. Rå seksjonsetikett bevares (ADR-0002).

Hele teksten skannes: sammendrag, alle seksjoner, seksjoner uten tittel,
seksjonstitler, figurtekster og tabellceller. Ingen seksjonsbasert
forhåndsfiltrering finnes i dette leddet, og det skal heller ikke legges til
senere — den avgjørende setningen i den positive kontrollen (PREREG-v1 §7) står
i en resultatseksjon.

``section_raw`` er strengen slik den sto i kilden: nummerering, versaler og tom
verdi beholdes. ``section_norm`` er additiv og erstatter aldri originalen.

Hver setning bærer ``section_label_provenance = "source"``: JATS-seksjonen er
kildens egen merking. En seksjon uten tittel er fortsatt ``source`` — at den er
uten tittel er kildens opplysning, ikke vår gjetning (ADR-0007).

Offsetene ``char_start``/``char_end`` peker inn i den rekonstruerte
dokumentteksten: blokktekstene føyd sammen med ``\\n`` i dokumentets rekkefølge.
Rekonstruksjonen er determinert av parseren, ikke av kilden.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Sequence

from lxml import etree

PARSER_ID = f"gjenopptak.parse.jats/lxml-{etree.__version__}"

#: JATS-inndelingen er skrevet av den som utgav teksten, ikke utledet av oss.
#: Derfor er opphavet «source» for alt som kommer ut av denne modulen. GROBID-TEI
#: gir «parser» og hører i et annet ledd (ADR-0007).
SECTION_LABEL_PROVENANCE = "source"

#: Blokker som bærer tekst. Dokumentrekkefølgen styrer, ikke denne listen.
_BLOCK_TAGS = {
    "p": "p",
    "title": "title",
    "td": "table_cell",
    "th": "table_cell",
    "list-item": "list_item",
}

#: Containere som ikke er blokker selv, men som setter blokktypen for barna.
_KIND_CONTAINERS = {"caption": "caption"}

#: Additive normaliseringsregler (ADR-0002). Første treff vinner; regelnavnet
#: loggføres i section_norm_rule slik at valget kan spores og kjøres om.
_NORM_RULES: tuple[tuple[str, str, str], ...] = (
    ("abstract", r"^\s*(abstract|summary|sammendrag)\b", "prefix:abstract"),
    ("limitations", r"\blimitation", "substring:limitation"),
    ("future_work", r"\b(future work|further work|future research|outlook)\b", "substring:future_work"),
    ("related_work", r"\b(related work|previous work|background)\b", "substring:related_work"),
    ("data_availability", r"\b(data availability|availability of data|code availability)\b", "substring:data_availability"),
    ("methods", r"\b(method|materials and methods|methodology|data and methods)\b", "substring:methods"),
    ("results", r"\bresult", "substring:results"),
    ("discussion", r"\bdiscussion\b", "substring:discussion"),
    ("conclusion", r"\b(conclusion|concluding remarks)\b", "substring:conclusion"),
    ("intro", r"\bintroduction\b", "substring:intro"),
)

#: Forkortelser som ikke avslutter en setning.
_ABBREV = (
    "e.g", "i.e", "cf", "vs", "etc", "al", "fig", "figs", "eq", "eqs", "ref",
    "refs", "no", "nos", "approx", "ca", "resp", "dr", "prof", "mr", "mrs",
    "ms", "st", "vol", "pp", "ed", "eds", "sec", "tab",
)
_ABBREV_RE = re.compile(r"(?:\b(?:" + "|".join(re.escape(a) for a in _ABBREV) + r")|\b[A-Z])\.$", re.I)
_SPLIT_RE = re.compile(r"(?<=[.!?])[\)\]\"'»”’]*\s+")
_WS_RE = re.compile(r"\s+")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _localname(el: etree._Element) -> str:
    return etree.QName(el).localname


def normalize_section(section_raw: str) -> tuple[str, str | None]:
    """Additiv avledning. Returnerer (section_norm, section_norm_rule)."""
    if not section_raw.strip():
        return "unknown", "empty_label"
    low = section_raw.lower()
    for norm, pattern, rule in _NORM_RULES:
        if re.search(pattern, low):
            return norm, rule
    return "other", "no_rule_matched"


def _emit(text: str, s: int, e: int, out: list[tuple[int, int, str]]) -> None:
    """Legg til én setning med offsets som peker på selve teksten, uten kantrom."""
    seg = text[s:e]
    lead = len(seg) - len(seg.lstrip())
    frag = seg.strip()
    if frag:
        start = s + lead
        out.append((start, start + len(frag), frag))


def split_sentences(text: str) -> list[tuple[int, int, str]]:
    """Setningssplitt. Returnerer (start, slutt, tekst) i tekstens egne offsets.

    Regelbasert med vilje: en modell i dette leddet ville gjort splitten
    avhengig av en dommer, jf. ADR-0003, uten at det er nødvendig.
    """
    out: list[tuple[int, int, str]] = []
    pos = 0
    pending: list[tuple[int, int]] = []
    for piece in _SPLIT_RE.split(text):
        if not piece:
            continue
        start = text.index(piece, pos)
        end = start + len(piece)
        pos = end
        pending.append((start, end))
        if _ABBREV_RE.search(piece.rstrip()):
            continue  # forkortelse: slå sammen med neste
        _emit(text, pending[0][0], pending[-1][1], out)
        pending = []
    if pending:
        _emit(text, pending[0][0], pending[-1][1], out)
    return out


@dataclass
class _Block:
    text: str
    kind: str
    section_raw: str
    section_path_raw: list[str] = field(default_factory=list)
    section_id_raw: str | None = None
    section_type_raw: str | None = None


def _text_of(el: etree._Element) -> str:
    """All tekst under elementet, med mellomrom normalisert. Kursiv og
    referanselenker flates ut; ingen tekst kastes."""
    return _WS_RE.sub(" ", "".join(el.itertext())).strip()


def _own_title(sec: etree._Element) -> str:
    for child in sec:
        if isinstance(child.tag, str) and _localname(child) == "title":
            return _text_of(child)
    return ""


def _enclosing_sec(el: etree._Element) -> etree._Element | None:
    node = el.getparent()
    while node is not None and _localname(node) != "sec":
        node = node.getparent()
    return node


def _add_block(child: etree._Element, path: list[str], kind: str, blocks: list[_Block]) -> None:
    text = _text_of(child)
    if not text:
        return
    sec = _enclosing_sec(child)
    blocks.append(
        _Block(
            text=text,
            kind=kind,
            section_raw=path[-1] if path else "",
            section_path_raw=list(path),
            section_id_raw=sec.get("id") if sec is not None else None,
            section_type_raw=sec.get("sec-type") if sec is not None else None,
        )
    )


def _walk(el: etree._Element, path: list[str], blocks: list[_Block], kind: str | None = None) -> None:
    for child in el:
        if not isinstance(child.tag, str):
            continue  # kommentarer, prosesseringsinstruksjoner
        name = _localname(child)

        if name == "sec":
            _walk(child, path + [_own_title(child)], blocks, kind)
            continue

        if name in ("abstract", "trans-abstract"):
            label = _own_title(child) or child.get("abstract-type") or "Abstract"
            _walk(child, path + [label], blocks, kind)
            continue

        if name in _KIND_CONTAINERS:
            # Containeren er ikke en blokk selv. Har den blokk-barn, arver de
            # typen; ellers blir containerens egen tekst én blokk. Slik telles
            # figurteksten én gang, ikke to.
            inner = _KIND_CONTAINERS[name]
            has_blocks = any(
                isinstance(g.tag, str) and _localname(g) in _BLOCK_TAGS
                for g in child.iter()
                if g is not child
            )
            if has_blocks:
                _walk(child, path, blocks, inner)
            else:
                _add_block(child, path, inner, blocks)
            continue

        if name in _BLOCK_TAGS:
            # Nøstet tekst er alt med i _text_of; ingen videre nedstigning,
            # ellers dobbelttelles den.
            _add_block(child, path, kind or _BLOCK_TAGS[name], blocks)
            continue

        _walk(child, path, blocks, kind)


def blocks_from_jats(xml: bytes) -> list[_Block]:
    """Alle tekstblokker i dokumentrekkefølge: front (abstract), body, back.

    Elementer som alt er gått gjennom, spores med **XPath-stien**, ikke med
    ``id(el)``. lxml lager Python-proxyer for elementer ved behov og kaster dem
    når ingen referanse holder dem. Da frigjøres id-en, og en proxy for et
    *annet* element kan få den samme. Med ``id()`` i ``seen`` ble et
    ``<body>`` av og til tatt for et ``<front>`` som alt var gått gjennom, og
    hele artikkelkroppen hoppet over: samme 122 KB-XML ga 537 setninger fire
    ganger og 20 den femte (ADDENDUM-07). Stien er stabil og unik per element.
    """
    parser = etree.XMLParser(recover=False, resolve_entities=False, no_network=True, load_dtd=False)
    root = etree.fromstring(xml, parser=parser)
    tree = root.getroottree()
    blocks: list[_Block] = []
    seen: set[str] = set()
    for want in ("front", "body", "back"):
        for el in root.iter():
            if not (isinstance(el.tag, str) and _localname(el) == want):
                continue
            sti = tree.getpath(el)
            if sti in seen:
                continue
            seen.add(sti)
            _walk(el, [], blocks)
    if not blocks and not seen:  # fragment uten front/body/back
        _walk(root, [], blocks)
    return blocks


def sentences_from_jats(xml: bytes, *, doc_id: str, parsed_at: str | None = None) -> list[dict]:
    """JATS → liste av sentences-poster. Hele teksten, rå seksjon bevart."""
    parsed_at = parsed_at or _now()
    rows: list[dict] = []
    offset = 0
    index = 0
    for block in blocks_from_jats(xml):
        norm, rule = normalize_section(block.section_raw)
        for start, end, text in split_sentences(block.text):
            rows.append(
                {
                    "schema_version": "sentences-1",
                    "sentence_id": f"{doc_id}:{index}",
                    "doc_id": doc_id,
                    "text": text,
                    "char_start": offset + start,
                    "char_end": offset + end,
                    "sentence_index": index,
                    "section_raw": block.section_raw,
                    "section_path_raw": block.section_path_raw,
                    "section_id_raw": block.section_id_raw,
                    "section_type_raw": block.section_type_raw,
                    "section_norm": norm,
                    "section_norm_rule": rule,
                    "section_label_provenance": SECTION_LABEL_PROVENANCE,
                    "parser_version": None,
                    "parser_model_version": None,
                    "block_kind": block.kind,
                    "parser": PARSER_ID,
                    "parsed_at": parsed_at,
                }
            )
            index += 1
        offset += len(block.text) + 1  # blokkene føyes sammen med "\n"
    return rows


def write_sentences(rows: Sequence[dict], out_path: Path, *, validate_each: bool = True) -> int:
    """Skriv sentences.jsonl. Returnerer radantall."""
    from ..schemas import validate

    if validate_each:
        for row in rows:
            validate("sentences", row)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return len(rows)


def iter_jsonl(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)
