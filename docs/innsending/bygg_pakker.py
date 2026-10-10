"""Bygg innsendingspakkene fra manus v2.9 — bare formatering, ingen innholdsendring i brødteksten.

    python docs/innsending/bygg_pakker.py

Det eneste som skjer med v2.9 (docs/MANUSKRIPT-v2.9.md):

1. **Tittelside:** hodet står ordrett; nøkkelord (CITATION.cff) og korresponderende forfatter føyes til, med
   e-post som plassholder — eieren fyller den inn i skjemaet.
2. **KI-erklæringen flyttes, ordrett,** fra § 8 til Methods som § 3.6: begge kanalene krever at bruk av
   språkmodeller dokumenteres i Methods (Preprints.org «Instructions for Authors», lest levende 02.10.2026;
   Scientometrics «Submission guidelines»).
3. **Referanselista:** v2.9 har en plassholder som lister kildene med identifikator; den byttes med den samme
   lista satt i APA og kontrollert mot Crossref, fra docs/PREPRINT-v2.md.
4. **Kanalens erklæringsblokk** settes rett foran referansene (Preprints.org: «Conflicts of Interest» sist;
   Scientometrics: «Statements and Declarations»).

Word-fil med pandoc. sha256 for inndata og utdata skrives til PAKKE.json i hver pakke.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
V29 = REPO / "docs" / "MANUSKRIPT-v2.9.md"
PRE = REPO / "docs" / "PREPRINT-v2.md"
UT = REPO / "docs" / "innsending"
NØKKELORD = ("metascience; preregistration; research limitations; self-admitted technical debt; open access; "
             "text classification")
KORR = ("**Corresponding author:** Eirik Botten Nicolaysen, EcoDeco AS, Lillehammer, Norway; "
        "e-mail: [entered at submission].")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def blokk(tekst: str, start: str, slutt: str) -> str:
    a = tekst.index(start)
    return tekst[a:tekst.index(slutt, a)]


def grunnlag() -> str:
    t = V29.read_text(encoding="utf-8")
    hode, kropp = t.split("\n---\n", 1)
    hode = hode.rstrip() + f"\n{KORR}\n**Keywords:** {NØKKELORD}\n"
    ki = blokk(kropp, "## 8 Use of AI tools\n", "## References")
    kropp = kropp.replace(ki, "")
    ki_tekst = ki.split("\n", 1)[1].strip()
    assert kropp.count("## 4 Results") == 1
    kropp = kropp.replace("## 4 Results", f"### 3.6 Use of AI tools\n\n{ki_tekst}\n\n## 4 Results")
    ref_v29 = kropp[kropp.index("## References"):]
    ref_apa = PRE.read_text(encoding="utf-8")
    ref_apa = ref_apa[ref_apa.index("## References"):]
    kropp = kropp.replace(ref_v29, "@@ERKLÆRINGER@@\n\n" + ref_apa.rstrip() + "\n")
    return hode + "\n---\n" + kropp


DATA = ("Code (Apache-2.0) and the author's own data (CC BY 4.0) are openly available at Zenodo, concept DOI "
        "https://doi.org/10.5281/zenodo.22959326 (all versions); the version holding this manuscript is 0.4.1, "
        "https://doi.org/10.5281/zenodo.23096158. Source repository: https://github.com/avalyset/gjenopptak. "
        "Third-party full texts and passages are not redistributed; the blind files are deposited as indices "
        "from which the text is regenerated from the open sources and verified by sha256 (Section 7).")
PREREG = ("The protocol (PREREG-v1) was locked internally on 12 September 2026, before data were read "
          "(sha256 05988b23…), and corrected only through dated, separately committed addenda. It was not "
          "timestamped by a third party before data were read; the first third-party guarantee of any lock is "
          "the Zenodo deposit of 25 September 2026 (Sections 3.1 and 6).")
KI = ("Language models were used as research instruments and as writing tools under the author's direction; "
      "the declaration is in Section 3.6.")

ERKL = {
    "preprints-org": (
        "## Funding\n\nThis research received no external funding.\n\n"
        f"## Data Availability Statement\n\n{DATA}\n\n"
        f"## Preregistration\n\n{PREREG}\n\n"
        f"## Use of AI Tools\n\n{KI}\n\n"
        "## Conflicts of Interest\n\nThe author declares no conflicts of interest."),
    "scientometrics": (
        "## Statements and Declarations\n\n"
        "**Funding.** No funding was received for conducting this study.\n\n"
        "**Competing interests.** The author has no relevant financial or non-financial interests to disclose.\n\n"
        "**Ethics approval and consent.** Not applicable: the study analyses published open-access texts and "
        "involves no human participants.\n\n"
        f"**Data availability.** {DATA}\n\n"
        "**Code availability.** The pipeline is open source (Apache-2.0) in the same deposit and repository.\n\n"
        f"**Preregistration.** {PREREG}\n\n"
        f"**Use of AI tools.** {KI}\n\n"
        "**Author contributions.** Eirik Botten Nicolaysen: conceptualization, methodology, software, "
        "validation, formal analysis, investigation, data curation, writing — original draft, writing — "
        "review and editing, visualization, project administration (sole author)."),
}


def bygg(kanal: str, g: str) -> dict:
    d = UT / kanal
    d.mkdir(parents=True, exist_ok=True)
    md = d / f"MANUSKRIPT-{kanal}.md"
    md.write_text(g.replace("@@ERKLÆRINGER@@", ERKL[kanal]), encoding="utf-8")
    docx = md.with_suffix(".docx")
    subprocess.run(["pandoc", "-f", "markdown+autolink_bare_uris", str(md), "-o", str(docx)], check=True)
    ut = {"kanal": kanal, "inndata": {"MANUSKRIPT-v2.9.md": sha(V29), "PREPRINT-v2.md (bare referanselista)": sha(PRE)},
          "utdata": {}}
    for f in sorted(d.glob("*")):
        if f.suffix in (".md", ".docx") and f.name != "PAKKE.json":
            ut["utdata"][f.name] = sha(f)
    for brev in sorted(d.glob("FOLGEBREV-*.md")):
        b = brev.with_suffix(".docx")
        subprocess.run(["pandoc", str(brev), "-o", str(b)], check=True)
        ut["utdata"][b.name] = sha(b)
    (d / "PAKKE.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return ut


if __name__ == "__main__":
    g = grunnlag()
    for k in ERKL:
        print(json.dumps(bygg(k, g), ensure_ascii=False, indent=1))
