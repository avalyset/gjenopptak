"""Kvoteporten: en fase nektes hvis budsjettet ikke rekker til å fullføre den.

Byggeplanen B1: «Kvotebudsjett som port, ikke som advarsel. Kommandoen nekter å starte en
fase den ikke har kreditt eller kvote til å fullføre, og sier hvor mye den trenger.»

Tre kvoter, målt og ikke anslått:

* **OpenAlex** — restkreditter fra svarhodene, gulv fra ``[kvote] openalex_gulv``.
* **Anthropics API** — ingen. Verktøyet kaller den ikke, og porten nekter enhver fase som ville
  gjort det (ADR-0012, datert tillegg 27.09.2026).
* **Opus-økter** — regnet fra målt forbruk: 25 034 kontekst-tokens per passasje, 287 533
  harness-tokens og 29,5 minutter per økt à 356. Harness-ens ukesgrense kan ikke leses fra
  kode, så den leses fra en fil operatøren skriver; mangler den, nektes leserfasen.

Ingen nøkkel leses, og ingen nøkkel skrives ut — det finnes ingen nøkkelsti i verktøyet.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from .konfig import Konfig

HARNESS_FIL = "kvote-harness.json"


class KvoteAvslag(RuntimeError):
    """Fasen ble nektet fordi budsjettet ikke rekker. Meldingen sier hvor mye som mangler."""


@dataclass
class Behov:
    """Hva en fase kommer til å koste, regnet fra målt forbruk."""

    passasjer: int = 0
    okter: int = 0
    kontekst_tokens: int = 0
    harness_tokens: int = 0
    minutter: float = 0.0
    openalex_kall: int = 0
    api_kall: int = 0

    def linjer(self) -> list[str]:
        ut = []
        if self.openalex_kall:
            ut.append(f"OpenAlex-kall:      {self.openalex_kall:>12,}")
        if self.passasjer:
            ut.append(f"passasjer:          {self.passasjer:>12,}")
        if self.okter:
            ut.append(f"Opus-økter:         {self.okter:>12,}")
            ut.append(f"kontekst-tokens:    {self.kontekst_tokens:>12,}")
            ut.append(f"harness-tokens:     {self.harness_tokens:>12,}")
            ut.append(f"tid:                {self.minutter/60:>12.1f} timer")
        if self.api_kall:
            ut.append(f"API-kall:           {self.api_kall:>12,}")
        return ut or ["ingen kvote brukt"]


def behov_for_leser(k: Konfig, n_passasjer: int) -> Behov:
    """Leserfasens kostnad, fra de målte tallene i ``[leser]``."""
    st = int(k.verdi("leser", "okt_storrelse"))
    okter = max(1, math.ceil(n_passasjer / st)) if n_passasjer else 0
    return Behov(
        passasjer=n_passasjer,
        okter=okter,
        kontekst_tokens=n_passasjer * int(k.verdi("leser", "kontekst_tokens_per_passasje")),
        harness_tokens=okter * int(k.verdi("leser", "harness_tokens_per_okt")),
        minutter=okter * float(k.verdi("leser", "minutter_per_okt")),
    )


# --------------------------------------------------------- Anthropics API: ikke i verktøyet
#: ADR-0012, datert tillegg 27.09.2026. Verktøyet kaller ikke Anthropics API. Det finnes ingen
#: nøkkelsjekk og ingen kredittsjekk her, fordi det ikke finnes noe kall å sjekke for. Leseren er
#: en CC-instans på Max-abonnementet (underinstans eller ``claude -p``). Skal en ekstern modell
#: noen gang inn, er den Gemini, og da med sin egen port — ikke denne.
API_FORBUDT = ("verktøyet kaller ikke Anthropics API (ADR-0012, datert tillegg 27.09.2026); "
               "leseren er en CC-instans på Max-abonnementet")


def harness_kvote(k: Konfig) -> dict | None:
    """Harness-ens ukesgrense, lest fra filen operatøren skriver. ``None`` om den mangler.

    Kode kan ikke lese Claude Codes egen kvotevisning. Filen skrives med
    ``gjenopptak run kvote --skriv-harness <prosent>`` eller av operatøren, og gjelder
    bare så lenge tidsstempelet er ferskt.
    """
    f = k.arbeid / HARNESS_FIL
    if not f.is_file():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError:
        return None


# --------------------------------------------------------------------------- porten
@dataclass
class Portsvar:
    fase: str
    slipper: bool
    behov: Behov
    grunner: list[str] = field(default_factory=list)

    def tekst(self) -> str:
        hode = f"kvoteport {self.fase}: {'SLIPPER' if self.slipper else 'NEKTER'}"
        return "\n".join([hode, *[f"  {l}" for l in self.behov.linjer()],
                          *[f"  ← {g}" for g in self.grunner]])


def port(k: Konfig, fase: str, behov: Behov, *, sjekk_api: bool = True) -> Portsvar:
    """Avgjør om fasen får starte. Nekter heller enn å advare."""
    grunner: list[str] = []
    slipper = True

    if behov.api_kall:
        # Ikke «mangler kreditt», men «finnes ikke som vei». En fase som ville kalt Anthropics
        # API, nektes uansett kvote.
        slipper = False
        grunner.append(f"fasen ville gjort {behov.api_kall:,} kall til Anthropics API — {API_FORBUDT}")

    if behov.okter:
        h = harness_kvote(k)
        tak = float(k.verdi("kvote", "harness_ukesgrense_tak"))
        if h is None:
            slipper = False
            grunner.append(
                f"harness-kvoten er ukjent: skriv {k.arbeid / HARNESS_FIL} med "
                f"{{\"ukesgrense_prosent\": <tall>, \"lest\": \"<tidspunkt>\"}} — "
                f"fasen trenger {behov.okter} Opus-økter à "
                f"{int(k.verdi('leser', 'harness_tokens_per_okt')):,} harness-tokens")
        else:
            brukt = float(h.get("ukesgrense_prosent", 100))
            if brukt >= tak:
                slipper = False
                grunner.append(f"harness-ukesgrensen står på {brukt:.0f} %, taket er {tak:.0f} % — "
                               f"fasen trenger {behov.okter} økter og "
                               f"{behov.minutter/60:.1f} timer")
            else:
                grunner.append(f"harness-ukesgrense {brukt:.0f} % av tak {tak:.0f} % (fra "
                               f"{h.get('lest', 'ukjent tidspunkt')})")

    if slipper and not grunner:
        grunner.append("ingen kvote å sjekke for denne fasen")
    return Portsvar(fase=fase, slipper=slipper, behov=behov, grunner=grunner)
