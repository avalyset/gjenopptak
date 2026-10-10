"""ADDENDUM-26 § 7–8: det ``fase4 maal`` ikke regner ut — presisjonsfølsomhet, klasser, felt-tetthet, kostnad og
modell-ID fra svaret. Leser bare; skriver ``fase4/rapport-fase4.json`` på Vault.

    PYTHONPATH=src python -m gjenopptak.classify.fase4_rapport

Sammenligningstallene for tetthet: fase 3 og de første 100 fra RESULTAT-ADDENDUM-25 § 1.4; tekstvitenskap-delen
av første runde regnes her fra filene for kandidatlista (treff fra register v2, dømte fra nøkkelen, tekstbiter fra
dommerfila), og samme regning for alle fire felt kontrolleres mot 432 / 2 844 / 22 243.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from ..vault import require_vault, sha256_file
from . import fase4 as F4
from .fase3 import _jsonl
from .fase3_rapport import _sum, andel, klasser, presisjon_følsomhet, tetthet

FASE3 = {"treff": 673, "dømt": 4107, "tekstbiter": 21361, "verk": 100}
FØRSTE_100 = {"treff": 432, "dømt": 2844, "tekstbiter": 22243, "verk": 100}


def første_runde_per_felt(v: Path, repo: Path, felt: str) -> dict:
    reg = _jsonl(v / "kandidat432" / "8-register.jsonl")
    nøkkel = _jsonl(v / "kandidat432" / "nokkel.jsonl")
    dommer = _jsonl(repo / "data" / "kjede" / "kandidat432" / "3-dommer.jsonl")
    alle = {"treff": len(reg), "dømt": len(nøkkel), "tekstbiter": len(dommer)}
    if alle != {k: FØRSTE_100[k] for k in alle}:
        raise SystemExit(f"kandidatlistas filer gir {alle}, ikke {FØRSTE_100}")
    return {"treff": sum(1 for r in reg if r["field_key"] == felt),
            "dømt": sum(1 for r in nøkkel if r.get("felt") == felt),
            "tekstbiter": sum(1 for r in dommer if r.get("felt") == felt),
            "verk": len({r["doc_id"] for r in dommer if r.get("felt") == felt}),
            "kilder": {"register": sha256_file(v / "kandidat432" / "8-register.jsonl"),
                       "nøkkel": sha256_file(v / "kandidat432" / "nokkel.jsonl"),
                       "dommer": sha256_file(repo / "data" / "kjede" / "kandidat432" / "3-dommer.jsonl")}}


def hovedrepo() -> Path:
    """Hovedrepoet, også når modulen kjøres fra en worktree (der `data/kjede/kandidat432` ikke finnes)."""
    import subprocess
    if (F4.REPO / "data" / "kjede" / "kandidat432").is_dir():
        return F4.REPO
    felles = subprocess.run(["git", "-C", str(F4.REPO), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            capture_output=True, text=True, check=True).stdout.strip()
    return Path(felles).parent


def leserøkter(ut: Path, kd: Path) -> list[dict]:
    """Forbruket for hver leserøkt som ble startet: leserleddet overskriver forbrukslisten ved hver kjøring, så det
    samles fra kopiene ``gjenoppta`` tok før hvert kall, siste tilstand (``les`` og ``les_avbrutt``) og
    fullføringsloggene. Duplikater (samme økt, minutter og bruk) telles én gang."""
    kilder = sorted(ut.glob("tilstand-foer-gjenopptak-*.json")) + [kd / "tilstand.json"]
    sett, ut_ = set(), []
    for k in kilder:
        t = json.loads(k.read_text(encoding="utf-8"))
        for ledd in ("les", "les_avbrutt"):
            for r in (t["ledd"].get(ledd) or {}).get("forbruk", []):
                nøkkel = json.dumps([r.get("okt"), r.get("minutter"), r.get("usage")], sort_keys=True, default=str)
                if nøkkel not in sett:
                    sett.add(nøkkel)
                    ut_.append({**r, "kilde": k.name, "rest": None})
    for lg in sorted((kd / "fullforing").glob("okt-*-rest*/logg.json")):
        d = json.loads(lg.read_text(encoding="utf-8"))
        ut_.append({**(d.get("bruk") or {}), "okt": d.get("okt"), "rest": d.get("rest"), "kilde": lg.parent.name})
    return ut_


def rapport(navn: str = F4.KJØRING) -> dict:
    v = require_vault()
    ut = v / F4.UT
    kd = F4.kjøringsdir(v, navn)
    t = json.loads((kd / "tilstand.json").read_text(encoding="utf-8"))
    leser = F4._leserdommer(kd, v, navn)
    treff = [d for d in leser if d.get("treff") is True]
    tb = int(t["ledd"]["tekstbiter"]["tekstbiter"])
    verk = int(t["ledd"]["hent"]["verk"])
    tv = første_runde_per_felt(v, hovedrepo(), "tekstvitenskap")
    ref = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ut / "referanse" / "bruk").glob("R*.json"))]
    pres = json.loads((ut / "presisjon" / "bruk-presisjon.json").read_text(encoding="utf-8")) \
        if (ut / "presisjon" / "bruk-presisjon.json").is_file() else None
    økter = leserøkter(ut, kd)
    dømte_økter = [r for r in økter if r.get("modeller_i_svaret") or r.get("modelUsage")]
    m = json.loads((ut / "maaling-fase4.json").read_text(encoding="utf-8")) if (ut / "maaling-fase4.json").is_file() else {}
    presisjon = (m.get("port1_presisjon") or {}).get("andel")
    bekreftede = round(len(treff) * presisjon) if presisjon else None

    def per_bekreftet(s: dict) -> int | None:
        return round(s["kontekst_inn"] / bekreftede) if bekreftede else None
    sr, sl = _sum(ref), _sum(økter)
    sp = _sum([pres]) if pres else None
    modeller = {
        "referansesett": dict(Counter(k for r in ref for k in (r.get("modelUsage") or {}))),
        "leser": dict(Counter(k for r in økter for k in (r.get("modelUsage") or {}))),
        "presisjon": sorted((pres or {}).get("modelUsage") or {}),
    }
    res = {"tid": F4.nå(), "kjøring": navn,
           "presisjon_følsomhet": presisjon_følsomhet(ut, leser),
           "klasser_blant_treff": klasser(treff),
           "felt_tetthet": {"fase4_haandskrift": tetthet(len(treff), len(leser), tb, verk),
                            "fase3_arkeologi": tetthet(**FASE3), "første_100_alle": tetthet(**FØRSTE_100),
                            "første_runde_tekstvitenskap": {**tetthet(tv["treff"], tv["dømt"], tv["tekstbiter"], tv["verk"]),
                                                            "kilder": tv["kilder"]}},
           "silens_andel": andel(len(leser), tb),
           "leser": {"treff": len(treff), "dømt": len(leser), "verk_med_treff": len({d["doc_id"] for d in treff}),
                     "treff_andel": andel(len(treff), len(leser))},
           "kostnad": {"openalex": json.loads((ut / "trekkresultat-fase4.json").read_text(encoding="utf-8")),
                       "modelltid_dommer_t": round(sum((r.get("bruk") or {}).get("total_duration", 0)
                                                        for r in _jsonl(kd / "3-dommer.jsonl")) / 3.6e12, 1),
                       "veggtid_ekstraksjon_t": round(sum(float(r.get("veggtid") or 0)
                                                          for r in _jsonl(kd / "4-ekstraksjon.jsonl")) / 3600, 1),
                       "max_økter": {"referansesett": sr, "leser_alle_startet": sl,
                                     "leser_som_dømte": _sum(dømte_økter), "presisjonsport": sp},
                       "per_bekreftet_treff": {"bekreftede": bekreftede, "referansesett": per_bekreftet(sr),
                                               "leser": per_bekreftet(sl),
                                               "presisjonsport": per_bekreftet(sp) if sp else None}},
           "modell_fra_svaret": modeller}
    (ut / "rapport-fase4.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return res


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--kjoring", default=F4.KJØRING)
    a = p.parse_args(argv)
    print(json.dumps(rapport(a.kjoring), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
