"""Verksnivå (ledd 7b): materialtilgang per verk. Kriteriet er portert ORDRETT.

Kilde: ``verksniva-2026-09-26-kriterium-v2.py`` på Vault, sha256
``d410c73419406a739921aba63d08d25e32f59e6fe83ca033baafb36660978e13``.
Regexene, tersklene og beslutningstreet under er uendret fra den filen — bare innpakningen er ny,
slik at kjeden kan kalle kriteriet i stedet for å kjøre et kladdeskript. Endres én terskel her, er
det ikke lenger samme måling.

Regelen for materialtilgang, fastsatt før kjøring:

* **ÅPEN** — datatilgangserklæring som dekker **forfatterens egne** data og sier at de er
  tilgjengelige (arkiv, DOI, «within the paper», supplement) **og** materialet er maskinlesbart
  (JATS med strukturerte tabeller, eller minst halvparten av tabellene har tekstlag).
* **DELVIS** — nøyaktig én av de to holder · eller egne data bare «on request» · eller erklæringen
  dekker bare tredjeparts data.
* **LUKKET** — ingen erklæring som dekker egne data, og ingen tabeller med tekstlag.

Flerspråkligheten i ``TAB_ORD``/``FIG_ORD`` kom av en blindtest 26.09.2026: kriteriet talte bare
engelske bildetekster, og 7 av 100 verk falt i LUKKET av den grunn alene.
"""

from __future__ import annotations

import re

#: sha256 til kildeskriptet kriteriet er portert fra.
KILDE_SHA256 = "d410c73419406a739921aba63d08d25e32f59e6fe83ca033baafb36660978e13"

LOFTBAR = {"H1", "H2", "H3", "H4", "H5", "H6"}

H_DATA=re.compile(r"(?:^|\n)[^\S\n]*(?:\d+\.?\d*\s*)?((?:Data|Code|Data and code|Data and materials|"
                  r"Availability of data(?: and materials?)?|Data availability)\s*"
                  r"(?:availability|accessibility|statement|sharing|and code availability)?[^\n]{0,30})\n",
                  re.I)
S_DATA=re.compile(r"[^.\n]{0,120}\b(?:data (?:availability|are available|is available|can be (?:found|accessed))|"
                  r"all (?:relevant )?data are within|data supporting (?:the|these) (?:findings|results)|"
                  r"datasets? (?:generated|analysed|analyzed|used) (?:and analysed )?(?:during|in) th(?:is|e) (?:study|work)|"
                  r"deposited in|available (?:from|in|at) (?:the )?(?:repository|zenodo|figshare|dryad|osf|github)|"
                  r"underlying data)\b[^.\n]{0,400}\.", re.I)
EGNE=re.compile(r"\bour (?:data|dataset)|data (?:generated|produced|collected) (?:in|for|during) th(?:is|e)|"
                r"all (?:relevant )?data are within|data supporting (?:the|these)|"
                r"datasets? (?:generated|analysed|analyzed) (?:during|in) th(?:is|e)|"
                r"the authors? (?:confirm|declare) that|presented in this (?:paper|study|article)|"
                r"in the (?:supplementary|supporting) (?:information|material|file)", re.I)
TREDJE=re.compile(r"\b(?:obtained|acquired|received|provided|supplied|sourced|downloaded) (?:from|by)\b|"
                  r"available from the [A-Z][A-Za-z ]{2,40}(?:website|portal|service|Survey|Office|Agency)|"
                  r"third[- ]party|British Geological Survey|Met Office|Environment Agency|"
                  r"courtesy of|by permission of", re.I)
FORESP=re.compile(r"\b(?:up)?on (?:reasonable )?request\b|by request|contacting the (?:corresponding )?author|"
                  r"from the corresponding author", re.I)
AAPEN_D=re.compile(r"zenodo|figshare|dryad|osf\.io|github\.com|gitlab|10\.5281/|10\.6084/|"
                   r"accession (?:number|code)|within the (?:paper|article|manuscript)|"
                   r"(?:supplementary|supporting) (?:information|material|files?|tables?)|dataverse|pangaea", re.I)
SUPP=re.compile(r"\b(?:S\d+\s+(?:Table|Fig|File|Text)|Supplementary (?:Table|Figure|File|Material|Data|Information)\s*\d*|"
                r"Supporting Information|Additional file\s*\d+|Online Resource\s*\d+|"
                r"Material(?:es)? (?:suplementario|complementario)s?|Anexo\s*\d+|Annexe\s*\d+|"
                r"Anhang\s*\d+|Suppl[e\u00e9]ment(?:aire)?\s*\d*|Tillegg\s*\d+|Vedlegg\s*\d+)\b", re.I)
#: Flersprakelig etter blindtesten 2026-09-26: kriteriet talte bare engelske bildetekster, og
#: 7 av 100 verk falt i LUKKET av den grunn alene (spansk x5, fransk x1, «Illus» x1).
FORMAT=re.compile(r"\.(xlsx|xls|csv|tsv|pdf|docx|doc|zip|txt|dat|nc|shp|json)\b", re.I)
TAB_ORD=("Table","Tabla","Tabelle","Tableau","Tabella","Tabell")
FIG_ORD=("Figure","Fig\\.","Figura","Abbildung","Abb\\.","Figur")
TAB=re.compile(r"\b(?:" + "|".join(TAB_ORD) + r")\s+(\d+|[IVX]+)\b")
FIG=re.compile(r"\b(?:" + "|".join(FIG_ORD) + r")\s+(\d+)\b")
LIS=re.compile(r"creativecommons\.org/licenses/([a-z\-]+)|\bCC[ -](BY(?:[- ]NC)?(?:[- ]SA)?(?:[- ]ND)?)\b|"
               r"(all rights reserved)|(open access)", re.I)
TALL=re.compile(r"(?<![A-Za-z])\d+[\.,]?\d*(?![A-Za-z])")

def analyser(w, txt, er_jats):
    h=H_DATA.search(txt)
    seksjon=None
    if h:
        i=h.end(); seksjon=re.sub(r"\s+"," ",txt[i:i+700]).strip()
        if len(seksjon)<25: seksjon=None
    if not seksjon:
        s=S_DATA.search(txt)
        if s: seksjon=re.sub(r"\s+"," ",s.group(0)).strip()
    egne = bool(seksjon and EGNE.search(seksjon))
    tredje = bool(seksjon and TREDJE.search(seksjon))
    if not seksjon:
        tredje = tredje or bool(TREDJE.search(txt))
    eier = "begge" if (egne and tredje) else ("forfatterens egne" if egne else ("tredjeparts" if tredje else "ingen erklæring"))
    if seksjon and AAPEN_D.search(seksjon) and not FORESP.search(seksjon): tilgang="åpne"
    elif seksjon and FORESP.search(seksjon): tilgang="på forespørsel"
    elif seksjon and AAPEN_D.search(seksjon): tilgang="åpne + på forespørsel"
    else: tilgang="ikke nevnt"
    supp=sorted(set(SUPP.findall(txt)))
    formater=sorted({m.group(1).lower() for m in FORMAT.finditer(txt)})
    tabeller=sorted(set(TAB.findall(txt)), key=str); figurer=sorted(set(FIG.findall(txt)), key=str)
    med_tekstlag=0
    for nr in tabeller:
        for m in re.finditer(r"\b(?:" + "|".join(TAB_ORD) + rf")\s+{re.escape(nr)}\b", txt):
            etter=txt[m.end():m.end()+900]
            if len(TALL.findall(etter))>=8: med_tekstlag+=1; break
    lis=LIS.search(txt)
    lisens = (lis.group(1) or lis.group(2) or lis.group(3) or lis.group(4)) if lis else "ikke oppgitt"
    maskinlesbar = er_jats or (len(tabeller)>0 and med_tekstlag >= len(tabeller)/2)
    egne_tilgjengelig = egne and tilgang.startswith("åpne")
    if egne_tilgjengelig and maskinlesbar: nivaa="ÅPEN"
    elif egne_tilgjengelig or maskinlesbar or (egne and tilgang=="på forespørsel") or (tredje and tilgang.startswith("åpne")): nivaa="DELVIS"
    else: nivaa="LUKKET"
    return dict(datatilgang_seksjon=seksjon, eier=eier, tilgang=tilgang,
                n_supplementer=len(supp), supplementer=supp[:8], formater=formater,
                n_tabeller=len(tabeller), n_tabeller_med_tekstlag=med_tekstlag,
                n_figurer=len(figurer), lisens=lisens, maskinlesbar=maskinlesbar,
                materialtilgang=nivaa)
