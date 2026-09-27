"""Testfixturer som Python-strenger.

`.gitignore` utelukker `*.xml` fordi rådata aldri committes. Fixturene ligger
derfor i kode og skrives til `tmp_path` av testen som trenger en fil på disk.

JATS-fixturen er konstruert, ikke hentet fra et verk. Den bærer én egenskap
som er hele poenget med ADR-0002: den avgjørende setningen står i en
**resultatseksjon**, slik den gjør i den positive kontrollen i PREREG-v1 §7.
Et seksjonsfilter på limitations ville mistet den.
"""

from __future__ import annotations

#: Setningen som MÅ komme ut av parseren, med rå seksjonsetikett "3. Results".
CONTROL_SENTENCE = (
    "We could not validate the model against hourly metered data, "
    "because manually transcribing the paper archives was beyond our resources."
)

#: Setning i en limitations-seksjon; skal også komme ut, men er ikke kontrollen.
LIMITATIONS_SENTENCE = (
    "A remaining limitation is that consent for the record linkage was never obtained."
)

#: Setning i en seksjon uten tittel; section_raw skal bli tom streng.
UNTITLED_SENTENCE = "The dataset is available on request from the corresponding author."

JATS_CONTROL = f"""<?xml version="1.0" encoding="UTF-8"?>
<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
  <front>
    <article-meta>
      <title-group><article-title>Open power system data</article-title></title-group>
      <abstract>
        <p>We document an open data platform. Coverage is uneven across countries.</p>
      </abstract>
    </article-meta>
  </front>
  <body>
    <sec id="s1" sec-type="intro">
      <title>1. Introduction</title>
      <p>Open data has grown, e.g. in the power sector. Fig. 2 shows the trend.</p>
    </sec>
    <sec id="s2" sec-type="methods">
      <title>2. MATERIALS AND METHODS</title>
      <p>Hourly series were collected from transmission operators.</p>
    </sec>
    <sec id="s3" sec-type="results">
      <title>3. Results</title>
      <p>Aggregate load matches published totals within 1.4 %. {CONTROL_SENTENCE}</p>
      <sec id="s3-1">
        <title>3.1 Sub-hourly behaviour</title>
        <p>Ramp rates were only checked for two zones.</p>
      </sec>
      <fig id="f1">
        <caption><p>Load duration curve for 2015-2020.</p></caption>
      </fig>
    </sec>
    <sec id="s4" sec-type="discussion">
      <title>4. Discussion and limitations</title>
      <p>{LIMITATIONS_SENTENCE}</p>
    </sec>
    <sec id="s5">
      <p>{UNTITLED_SENTENCE}</p>
    </sec>
  </body>
  <back>
    <sec id="s6">
      <title>Data availability</title>
      <p>All files are released under CC-BY 4.0.</p>
    </sec>
  </back>
</article>
"""

#: Minimal OpenAlex-respons, samme form som API-et gir. Brukt offline.
OPENALEX_RESPONSE = {
    "meta": {"count": 2, "page": 1, "per_page": 2},
    "results": [
        {
            "id": "https://openalex.org/W2799011080",
            "doi": "https://doi.org/10.1016/j.apenergy.2018.04.048",
            "title": "Open Power System Data",
            "publication_year": 2018,
            "language": "en",
            "type": "article",
            "has_fulltext": True,
            "open_access": {"is_oa": True},
            "best_oa_location": {"license": "cc-by"},
            "primary_location": {"license": None},
            "topics": [{"id": "https://openalex.org/T10159", "display_name": "Energy systems"}],
        },
        {
            "id": "https://openalex.org/W1234567890",
            "doi": None,
            "title": "A study without a DOI",
            "publication_year": 2016,
            "language": "en",
            "type": "article",
            "has_fulltext": True,
            "open_access": {"is_oa": False},
            "best_oa_location": None,
            "primary_location": {"license": None},
            "topics": [],
        },
    ],
}
