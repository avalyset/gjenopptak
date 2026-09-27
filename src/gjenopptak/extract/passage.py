"""Passasjen som observasjonsenhet (ADDENDUM-03 §1).

PREREG §2 definerer et treff som én setning der forfatteren navngir noe de ikke
fikk gjort **og** oppgir hindringen. Uttrekket bærer samtidig et kontekstvindu på
±2 setninger. Uttrekket var altså definert på passasje og målingen på setning.

ADDENDUM-03 §1 løser det: observasjonsenheten er passasjen — treffsetningen pluss
±2 setninger — og et treff krever at det ugjorte og hindringen begge står innenfor
passasjen og er knyttet til hverandre. Hvor snevert kriteriet ble oppfylt, bæres i
feltet ``unit``:

* ``sentence`` — begge deler i samme setning (det gamle, strengere kravet)
* ``passage`` — begge deler innenfor vinduet

Begge tall rapporteres alltid, aldri ett alene: M1-streng og M1-passasje er
følsomhet på ett metodevalg. Modulen gir derfor ingen funksjon som returnerer
«antall treff» uten å skille de to.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

WINDOW = 2

#: Forfatteren navngir noe som ikke ble gjort. Utvides i ADDENDUM-02 §3-ankrene.
UNDONE = re.compile(
    r"(were unable to|was not possible|could not\b|did not (have|attempt|allow|assess)"
    r"|prevented (us|me) from|was not feasible|no attempt was made|too time[- ]consuming"
    r"|prohibitivel|only a subset|we manually reviewed|we coded a random sample"
    r"|remains? (unread|untranscribed)|have not been (read|transcribed|collated|digiti))",
    re.I,
)

#: Hindringen oppgis. Klassen avgjøres av koderen, ikke av dette mønsteret.
#:
#: Mønsteret er bevisst romslig. Det er en kandidatgenerator med høy recall —
#: koderen forkaster, mønsteret skal ikke gjøre det. Presisjonen måles som
#: andelen N1-N3 blant kandidatene (PREREG §5).
OBSTACLE = re.compile(
    r"(because|due to|owing to|as a result of|since|lack(ing|ed|s)? of|absence of|unavailab"
    r"|not available|accessib|restrict|consent|ethical|confidential|resources?|workload"
    r"|time[- ]consuming|effort|cost|manual|illegib|inaudible|fragmentary|damaged"
    r"|language barrier|computationally|insufficient material|not enough"
    r"|no (copy|copies|surviving|extant|record|material|data)\b"
    r"|not (held|obtainable|preserved)|could not be (found|located|obtained|accessed))",
    re.I,
)


#: ADDENDUM-06 §1 — utvidelser målt fram fra bommene mot recall-fasiten, ikke
#: fra fantasi. Hver rad er (mønster, doc_id, setningsindeks, sitatfragment).
#: Fragmentet er kontrollstrengen: testen krever at mønsteret treffer den.
#: Fasiten ligger i data/recall-sett.jsonl; ingen av disse er hentet fra det
#: sirkulære frasesøkmaterialet.
UNDONE_ADDITIONS: tuple[tuple[str, str, int, str], ...] = (
    (r"has not been possible", "W2768163024", 95,
     "it has not been possible to characterize them"),
    (r"is not always possible", "W2505978088", 254,
     "it is not always possible to assign specific items to one or the other individual"),
    (r"cannot\b", "PMC4342813", 698,
     "we cannot favour a northern or southern route through Wallacea"),
    (r"lack(ed|s) sufficient", "W246600566", 137,
     "our data lacked sufficient power to detect small differences"),
    (r"we lack\b", "W2505978088", 505,
     "For the inland regions we lack quantitative data for comparison"),
    (r"limiting our ability", "PMC5020840", 27,
     "limiting our ability to understand evaluations by those with low English language proficiency"),
    (r"have not been (\w+ )?quantified", "W2225860453", 111,
     "they have not been individually quantified for this study"),
    (r"not been taken into (consideration|account)", "W2225860453", 141,
     "Length has not been taken into consideration here"),
    (r"hamper(s|ed)?\b", "W2225860453", 191,
     "sample size of nonlocal cores hampers statistical comparisons"),
    (r"would not consider", "PMC4342813", 653,
     "we would not consider a more detailed dating of the westward movement reliable"),
    (r"not assigned to", "PMC4342813", 798,
     "P and Q mtDNAs not assigned to a specific lineage due to lack of information"),
    (r"for another occasion", "W2505978088", 44,
     "We leave for another occasion the treatment of the forms of violence"),
    (r"need(s)? yet to be", "W2505978088", 44,
     "involves new empirical findings that need yet to be investigated"),
    (r"still waiting for", "W2505978088", 137,
     "While we are still waiting for DNA analyses capable of testing this proposal"),
    (r"to be explored", "W2505978088", 249,
     "Another venue to be explored is the analysis of craniodental epigenetic traits"),
    (r"remains desirable", "W2505978088", 346,
     "A systematic approach to the deposition of dead bodies of both sexes"
     " in the Iberian groups contemporaneous with the Argaric society remains desirable"),
    (r"(is|are) needed\b", "W2505978088", 528,
     "Various taphonomic and analytical problems have affected the dates"
     " of several double burials recently excavated at La Bastida, so that redating is needed"),
    (r"unfruitful", "W2505978088", 538,
     "The results have so far been unfruitful"),
    (r"not yet reliable", "W2505978088", 544,
     "Sex estimation of inmature individuals from morphometric traits"
     " in the skeleton is not yet reliable enough"),
    (r"with the exception of", "W2505978088", 573,
     "with the exception of those that contained at least one infant"),
    (r"not produced reliable", "W2505978088", 635,
     "The C14 analysis of bone samples has not produced reliable results"),
    (r"we grouped", "W2225860453", 93,
     "we grouped all local varieties together for this study"),
    (r"have been assigned to the", "W2225860453", 105,
     "in this paper all flint artefacts have been assigned to the erratic flint variety"),
    (r"labo(u)?r[- ]intensive", "W246600566", 160,
     "Measuring these outcomes will likely require time and labor-intensive methods"),
    # Denne er den svakeste av tilleggene: den markerer sjangeren
    # «begrensningsavsnitt», ikke det ugjorte. Setningen oppgir det ugjorte bare
    # indirekte («the lack of information about women who...»), og ingen
    # verbfrase bærer det. Den koster ingenting i presisjon på de 30, men
    # klinisk sjanger er tynt representert der. Se ADDENDUM-06 §1.
    (r"limitation of (this|our) study", "PMC5454651", 193,
     "The main limitation of this study was the lack of information about women"),
)

#: ADDENDUM-06 §1 — samme regime for hindringssiden. Tre av bommene traff på
#: UNDONE og falt på OBSTACLE: hindringen er ikke alltid en av de ni klassenes
#: stikkord, den står i fagets eget ordforråd.
OBSTACLE_ADDITIONS: tuple[tuple[str, str, int, str], ...] = (
    (r"no (\w+ )?(cop(y|ies)|surviving|extant|record|records|material|data)\b",
     "W2342080206", 131,
     "There were no similar data available from public hospitals elsewhere in Hong Kong"),
    (r"(lack|absence|no|without|missing|not have|had no) (\w+ )?information",
     "PMC5454651", 183,
     "we did not have information about age at time of CBE"),
    (r"lack(ing|ed|s)?\b", "W2505978088", 573,
     "data on the composition of the grave goods is lacking, doubtful or incomplete"),
    (r"(other|another) language", "PMC5020840", 379,
     "it was not possible to produce equivalent vignettes in other languages"),
    (r"language (barrier|proficiency)", "PMC5020840", 27,
     "those with low English language proficiency"),
    (r"(sample size|statistical power|sufficient power|underpowered)",
     "W246600566", 137,
     "which might have been detected with a larger sample size"),
    (r"difficult", "W2225860453", 112,
     "hence the difficulty to always distinguishing MJC from flint"),
    (r"(similarly|too) small", "PMC4342813", 698,
     "From the similarly small proportions of autochthonous haplogroups along both"),
    (r"waiting for", "W2505978088", 137,
     "we are still waiting for DNA analyses"),
    (r"will be available", "W2505978088", 348,
     "we cannot discard the possibility of interesting patterns"
     " when more detailed data will be available"),
    (r"taphonom", "W2505978088", 528,
     "Various taphonomic and analytical problems have affected the dates"),
)


def _utvid(base: re.Pattern, tillegg: tuple[tuple[str, str, int, str], ...]) -> re.Pattern:
    """v1-mønsteret pluss tilleggene, som ett alternativ-uttrykk."""
    deler = [base.pattern] + [t[0] for t in tillegg]
    return re.compile("|".join(f"(?:{d})" for d in deler), re.I)


#: v2 brukes på utvalget. v1 står urørt: den produserte rørledningstestens tall,
#: og de tallene skal kunne reproduseres etterpå.
UNDONE_V2 = _utvid(UNDONE, UNDONE_ADDITIONS)
OBSTACLE_V2 = _utvid(OBSTACLE, OBSTACLE_ADDITIONS)


class NotSplit(ValueError):
    """Tallene for sentence og passage kan ikke slås sammen (ADDENDUM-03 §1)."""


@dataclass(frozen=True)
class Passage:
    """Passasjen ett treff ble avgjort på."""

    doc_id: str
    hit_index: int
    start_index: int
    end_index: int
    window: int
    unit: str
    text: str
    sentence_text: str
    section_raw: str
    section_label_provenance: str

    @property
    def n_sentences(self) -> int:
        return self.end_index - self.start_index + 1

    def span(self) -> dict:
        """``passage_span`` slik skjemaet krever det."""
        return {
            "start_index": self.start_index,
            "end_index": self.end_index,
            "n_sentences": self.n_sentences,
            "window": self.window,
        }


def passages(
    rows: Sequence[Mapping],
    *,
    window: int = WINDOW,
    undone: re.Pattern = UNDONE,
    obstacle: re.Pattern = OBSTACLE,
) -> list[Passage]:
    """Finn kandidatpassasjer i setningene fra ett dokument.

    Setningene må komme fra samme dokument og i rekkefølge. En setning som
    navngir noe ugjort gir en passasje når hindringen står i samme setning
    (``unit="sentence"``) eller innenfor vinduet (``unit="passage"``).
    """
    if not rows:
        return []
    doc_ids = {r["doc_id"] for r in rows}
    if len(doc_ids) != 1:
        raise ValueError(f"passages() tar setninger fra ett dokument, fikk {len(doc_ids)}")

    ut: list[Passage] = []
    for i, row in enumerate(rows):
        if not undone.search(row["text"]):
            continue
        lo = max(0, i - window)
        hi = min(len(rows) - 1, i + window)
        i_sentence = bool(obstacle.search(row["text"]))
        vindu = " ".join(rows[j]["text"] for j in range(lo, hi + 1))
        if not (i_sentence or obstacle.search(vindu)):
            continue
        ut.append(
            Passage(
                doc_id=row["doc_id"],
                hit_index=row["sentence_index"],
                start_index=rows[lo]["sentence_index"],
                end_index=rows[hi]["sentence_index"],
                window=window,
                unit="sentence" if i_sentence else "passage",
                text=vindu,
                sentence_text=row["text"],
                section_raw=row.get("section_raw", ""),
                section_label_provenance=row["section_label_provenance"],
            )
        )
    return ut


def split_counts(hits: Iterable[Passage]) -> dict[str, int]:
    """{"sentence": n, "passage": m} — m teller dem som *bare* nådde passasjekravet.

    M1-streng = sentence. M1-passasje = sentence + passage. Begge oppgis; se
    ``format_m1`` for den eneste rapporteringsformen modulen tilbyr.
    """
    ut = {"sentence": 0, "passage": 0}
    for h in hits:
        ut[h.unit] += 1
    return ut


def format_m1(hits: Iterable[Passage], n_documents: int) -> str:
    """Begge tallene, i én streng. Det finnes ingen enkelttalls-variant."""
    if n_documents <= 0:
        raise NotSplit("M1 krever et nevnerantall > 0")
    c = split_counts(hits)
    streng = c["sentence"]
    passasje = c["sentence"] + c["passage"]
    return (
        f"M1-streng {streng}/{n_documents} = {streng / n_documents:.1%}; "
        f"M1-passasje {passasje}/{n_documents} = {passasje / n_documents:.1%} "
        f"(±{WINDOW} setninger)"
    )
