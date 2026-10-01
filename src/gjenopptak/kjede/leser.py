"""Leseren bak ett grensesnitt, som silen (``sil.py``).

    leser(regler, parti) -> Lesning

En leser får **regelfilen og et parti tekstbiter i samme kontekst** og gir én dom per tekstbit.
Det er det som skiller den fra dommeren i silen, som ser én tekstbit per kall uten reglene
(ADR-0012: ett-kall-modeller er sil-klasse).

To implementasjoner:

===============  ==========================================================  ==================
leser            hvordan                                                     målt mot koder 1
===============  ==========================================================  ==================
``CCLeser``      Claude Code-instans, agentisk, leser filene selv (``claude   κ = 0,812 (koder 2,
                 -p`` eller underinstans); partiet er hele økten                ADDENDUM-11)
``LokalLeser``   ollama-modell, regelfil + parti på 20 i én melding, JSON-     ADDENDUM-24
                 skjema, temp 0, frø; ingen filtilgang, ingen verktøy
===============  ==========================================================  ==================

Klassen en leser havner i, avgjøres av en preregistrert port mot koder 1 over de 320 i portens
blindfil, ikke av implementasjonen: κ ≥ 0,70 gir godkjent leser, under gir sil-klasse.

Dommene bærer samme felter som koder 1 og koder 2 (ADDENDUM-11 §2): ``id``, ``ekte_treff``,
``min_klasse``, ``min_bedømbar``, ``tvil``, ``begrunnelse``.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

#: Klasseverdiene reglene navngir. Uavklart bare som ``H1/H7-uavklart``: regelfilens utdrag fra
#: ADDENDUM-05 er avkuttet etter tabellhodet, og koderne ble bedt om å bruke bare det reglene
#: faktisk navngir (arbeidsliste/oppdrag-koder-c.md). Samme skranke her, for paritet.
KLASSER = ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H1/H7-uavklart",
           "N1", "N2", "N3", "INGEN")

#: JSON-skjemaet ollama tvinger utdata inn i. Rekkefølgen på feltene er koder 2s.
SKJEMA = {
    "type": "object",
    "properties": {"dommer": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "ekte_treff": {"type": "boolean"},
            "min_klasse": {"type": "string", "enum": list(KLASSER)},
            "min_bedømbar": {"type": ["boolean", "null"]},
            "tvil": {"type": "boolean"},
            "begrunnelse": {"type": "string"},
        },
        "required": ["id", "ekte_treff", "min_klasse", "min_bedømbar", "tvil", "begrunnelse"],
    }}},
    "required": ["dommer"],
}


class LeserFeil(RuntimeError):
    pass


@dataclass
class Lesning:
    """Det én leserkjøring over ett parti gir: dommene, og hva den kostet."""

    dommer: list[dict]
    ugyldige: list[str]                 # id-er uten gyldig dom
    bruk: dict = field(default_factory=dict)


class Leser(Protocol):
    """``leser(regler, parti) -> Lesning``. En ny leser trenger bare denne formen."""

    navn: str

    def signatur(self) -> dict:
        ...

    def __call__(self, regler: str, parti: list[dict]) -> Lesning:
        ...


def sha256_tekst(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_blob(sti: Path) -> str:
    h = hashlib.sha256()
    with sti.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def partimelding(parti: list[dict], nr: int, av: int) -> str:
    """Brukermeldingen: partiet, i blindfilens rekkefølge, med id som overskrift."""
    deler = [f"Parti {nr} av {av}. {len(parti)} tekstbiter. Gi nøyaktig én dom per id, i denne "
             f"rekkefølgen: {', '.join(r['id'] for r in parti)}.\n"]
    for r in parti:
        deler.append(f"### {r['id']}\n{r['tekst']}\n")
    return "\n".join(deler)


def valider(rå: list[dict], parti: list[dict]) -> tuple[list[dict], list[str]]:
    """Behold første gyldige dom per ventet id. Alt annet er ugyldig — ingenting fylles ut."""
    ventet = [r["id"] for r in parti]
    fikk: dict[str, dict] = {}
    for d in rå:
        if not isinstance(d, dict) or d.get("id") not in ventet or d["id"] in fikk:
            continue
        if not isinstance(d.get("ekte_treff"), bool) or d.get("min_klasse") not in KLASSER \
                or not isinstance(d.get("tvil"), bool):
            continue
        fikk[d["id"]] = {k: d.get(k) for k in
                         ("id", "ekte_treff", "min_klasse", "min_bedømbar", "tvil", "begrunnelse")}
    return [fikk[i] for i in ventet if i in fikk], [i for i in ventet if i not in fikk]


@dataclass
class LokalLeser:
    """ollama-modell som leser: regelfil i systemmeldingen, partiet i brukermeldingen.

    Ingen filtilgang og ingen verktøy — derfor trenger den ingen sperreliste: den ser bare
    det som sendes. ``num_predict`` settes høyt og ``done_reason`` føres, fordi et tak som
    binder halen er et utvalgsfilter og ikke en kostnadsinnstilling (LAERDOM § 34).
    """

    modell: str
    vekt_sha256: str
    instruks: str
    num_ctx: int = 32768
    temperatur: float = 0.0
    frø: int = 734248
    num_predict: int = 8192
    vert: str = "http://localhost:11434"
    keep_alive: str = "30m"
    navn: str = "lokal"

    def signatur(self) -> dict:
        return {"leser": self.navn, "modell": self.modell, "vekt_sha256": self.vekt_sha256,
                "instruks_sha256": sha256_tekst(self.instruks), "num_ctx": self.num_ctx,
                "temperatur": self.temperatur, "frø": self.frø, "num_predict": self.num_predict}

    def _kall(self, system: str, bruker: str) -> dict:
        import httpx
        kropp = {"model": self.modell, "stream": False, "keep_alive": self.keep_alive,
                 "format": SKJEMA,
                 "options": {"temperature": self.temperatur, "seed": self.frø,
                             "num_ctx": self.num_ctx, "num_predict": self.num_predict},
                 "messages": [{"role": "system", "content": system},
                              {"role": "user", "content": bruker}]}
        with httpx.Client(timeout=3600) as c:
            r = c.post(f"{self.vert}/api/chat", json=kropp)
            r.raise_for_status()
            return r.json()

    def __call__(self, regler: str, parti: list[dict], *, nr: int = 1, av: int = 1) -> Lesning:
        system = f"{self.instruks}\n\n# REGLENE\n\n{regler}"
        bruker = partimelding(parti, nr, av)
        t0 = time.time()
        svar = self._kall(system, bruker)
        rå_tekst = (svar.get("message") or {}).get("content", "")
        bruk = {"prompt_eval_count": svar.get("prompt_eval_count"),
                "eval_count": svar.get("eval_count"), "done_reason": svar.get("done_reason"),
                "sekunder": round(time.time() - t0, 1),
                "total_duration_s": round((svar.get("total_duration") or 0) / 1e9, 1),
                "råsvar_sha256": sha256_tekst(rå_tekst), "råsvar": rå_tekst}
        if (bruk["prompt_eval_count"] or 0) >= self.num_ctx:
            bruk["avkuttet_inn"] = True
        try:
            rå = json.loads(rå_tekst).get("dommer", [])
        except (ValueError, AttributeError):
            rå = []
            bruk["parsefeil"] = True
        if svar.get("done_reason") == "length":
            # Avkuttet utdata: JSON-en kan likevel parse (skjemaet lukker den), men halen mangler.
            bruk["avkuttet_ut"] = True
        dommer, ugyldige = valider(rå, parti)
        return Lesning(dommer=dommer, ugyldige=ugyldige, bruk=bruk)


@dataclass
class CCLeser:
    """Claude Code-instans som leser, hodeløst med ``claude -p``; oppdraget går på stdin.

    Instansen leser regelfilen og blindfilen selv og skriver dommene til ``utfil``. Partiet er
    hele økten (≤ 356 tekstbiter, ADDENDUM-22 §3). Forbruket føres fra kommandoens eget
    JSON-svar. Aldri parallelt (LAERDOM § 32).
    """

    modell: str
    rot: Path
    ekstra_kataloger: tuple[Path, ...] = ()
    navn: str = "cc"

    def signatur(self) -> dict:
        return {"leser": self.navn, "modell": self.modell, "form": "claude -p, agentisk"}

    def kjør_økt(self, oppdrag: str, utfil: Path) -> dict:
        t0 = time.time()
        arg = ["claude", "-p", "--model", self.modell, "--output-format", "json",
               "--permission-mode", "acceptEdits"]
        for k in self.ekstra_kataloger:
            arg += ["--add-dir", str(k)]
        r = subprocess.run(arg, cwd=self.rot, capture_output=True, text=True, timeout=7200,
                           input=oppdrag)
        try:
            svar = json.loads(r.stdout)
        except ValueError:
            return {"feil": "kunne ikke lese JSON fra claude -p", "stderr": r.stderr[-400:],
                    "minutter": round((time.time() - t0) / 60, 1)}
        if svar.get("is_error") and "authenticate" in str(svar.get("result", "")).lower():
            raise LeserFeil(
                f"claude-CLI-en kunne ikke autentisere ({svar.get('result')}). Kjør «claude "
                f"login» i en terminal og start på nytt.")
        return {"usage": svar.get("usage"), "total_cost_usd": svar.get("total_cost_usd"),
                "num_turns": svar.get("num_turns"), "is_error": svar.get("is_error"),
                "resultat": str(svar.get("result"))[:400],
                "minutter": round((time.time() - t0) / 60, 1)}

    def __call__(self, regler: str, parti: list[dict], *, oppdrag: str = "",
                 utfil: Path | None = None) -> Lesning:
        if not oppdrag or utfil is None:
            raise LeserFeil("CCLeser trenger oppdraget og utfilen; instansen leser filene selv")
        bruk = self.kjør_økt(oppdrag, utfil)
        rå = [json.loads(l) for l in utfil.read_text(encoding="utf-8").splitlines() if l.strip()] \
            if utfil.is_file() else []
        # Arbeidslistens felter heter treff/klasse; portens heter ekte_treff/min_klasse.
        for d in rå:
            if "treff" in d and "ekte_treff" not in d:
                d["ekte_treff"] = d["treff"]
            if "klasse" in d and "min_klasse" not in d:
                d["min_klasse"] = d["klasse"]
            d.setdefault("min_bedømbar", None)
        dommer, ugyldige = valider(rå, parti)
        return Lesning(dommer=dommer, ugyldige=ugyldige, bruk=bruk)


#: Registeret over lesere, som ``sil.SILER``.
LESERE = {"lokal": LokalLeser, "cc": CCLeser}
