"""ADDENDUM-26 § 8: kandidatene i H1–H6 med ``tvil: false`` til ``docs/SAKBEHANDLING-<dato>-haandskrift.md``.

    PYTHONPATH=src python -m gjenopptak.classify.fase4_sakbehandling --dato 2026-10-03

Samme form som ``docs/SAKBEHANDLING-2026-09-27-kandidater.md``: per kandidat verk-ID, år, setningsspenn, silens kilde,
tittel, DOI og kilde-URL, **ordrett sitat ±2 setninger** (tekstbiten leseren dømte — passasjeenheten, ADDENDUM-03
§ 1.2) og leserens begrunnelse. Sitatene hviler på sitatretten med kildeangivelse (LISENSAUDIT-2026-09-28).
Titlene kommer fra OpenAlex-metadataene trekkingen lagret (``fase4/raw/fase4-meta-*.json``), ikke fra teksten.
Lista får navnet porten ga den (``maaling-fase4.json``).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from ..vault import require_vault, sha256_file
from . import fase4 as F4
from .fase3 import _jsonl
from .liftability import is_unresolved

LØFTBARE = ("H1", "H2", "H3", "H4", "H5", "H6")


def titler(raw: Path) -> dict[str, dict]:
    ut: dict[str, dict] = {}
    for f in sorted(raw.glob("fase4-meta-*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for w in d.get("results", []):
            ut[w["id"].rsplit("/", 1)[-1]] = {"tittel": w.get("title") or w.get("display_name"),
                                               "år": w.get("publication_year")}
    return ut


def kandidater(v: Path, navn: str = F4.KJØRING) -> list[dict]:
    kd = F4.kjøringsdir(v, navn)
    tekst = {r["id"]: r["tekst"] for f in sorted((kd / "blind").glob("blind-okt-*.jsonl")) for r in _jsonl(f)}
    return [{**d, "tekst": tekst[d["id"]]} for d in F4._leserdommer(kd, v, navn)
            if d.get("treff") is True and d.get("tvil") is False
            and d.get("klasse") in LØFTBARE and not is_unresolved(d["klasse"])]


def skriv(dato: str, navn: str = F4.KJØRING) -> Path:
    v = require_vault()
    ut = v / F4.UT
    m = json.loads((ut / "maaling-fase4.json").read_text(encoding="utf-8"))
    listenavn = m.get("navn") or "kandidatliste"
    p1 = m.get("port1_presisjon") or {}
    ramme = {json.loads(l)["work_id"]: json.loads(l) for l in (v / "frames/frame-haandskrift-RAW.jsonl").open(encoding="utf-8")}
    ti = titler(ut / "raw")
    kand = kandidater(v, navn)
    per = defaultdict(list)
    for d in sorted(kand, key=lambda d: (d["klasse"], d["doc_id"], d["start_index"])):
        per[d["klasse"]].append(d)
    L = [f"# Kandidater til saksbehandling — fase 4, håndskriftstudier — {dato}", "",
         f"**{len(kand)} kandidater** fra leserens treff i fase 4 (ADDENDUM-26). Utvalgskriteriet er **løftbar klasse "
         f"(H1–H6) og `tvil: false`** hos leseren; uavklarte er ikke med (ADDENDUM-26 § 8).", "",
         f"**Lista heter «{listenavn}».** Den prospektive porten ga blind presisjon **{p1.get('k')} av {p1.get('n')}** "
         f"(terskel 0,70; `maaling-fase4.json`). Presisjonen er målt over alle leserens treff, ikke over denne delgruppen.", "",
         f"**Titlene er hentet fra OpenAlex** (metadataene trekkingen lagret i `fase4/raw/`), ikke lest ut av teksten. "
         f"Sitatene er tekstbiten leseren dømte, ordrett, og hviler på sitatretten med kildeangivelse.", ""]
    for kl in LØFTBARE:
        if not per.get(kl):
            continue
        L += [f"## {kl}", ""]
        for d in per[kl]:
            r = ramme.get(d["doc_id"], {})
            bol = r.get("best_oa_location") or {}
            t = ti.get(d["doc_id"], {})
            L += [f"**{d['id']}** · `{d['doc_id']}` · {t.get('år') or r.get('publication_year') or '—'} · "
                  f"setning {d['start_index']}–{d['end_index']} · sil: {d.get('kilde', '—')}", "",
                  f"> {t.get('tittel') or '(tittel mangler i metadataene)'}", "",
                  f"* **DOI:** {r.get('doi') or '—'} · **kilde:** {bol.get('pdf_url') or bol.get('landing_page_url') or '—'}",
                  f"* **lisens (OpenAlex):** {bol.get('license') or 'ikke oppgitt'}", "",
                  "**Sitat, ordrett ±2 setninger:**", "", "> " + " ".join(d["tekst"].split()), "",
                  f"**Leserens begrunnelse:** {d.get('begrunnelse', '').strip()}", ""]
    f = Path(__file__).resolve().parents[3] / "docs" / f"SAKBEHANDLING-{dato}-haandskrift.md"
    f.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(json.dumps({"fil": str(f), "kandidater": len(kand), "per_klasse": {k: len(v_) for k, v_ in per.items()},
                      "sha256": sha256_file(f)}, ensure_ascii=False))
    return f


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--dato", required=True)
    p.add_argument("--kjoring", default=F4.KJØRING)
    a = p.parse_args(argv)
    skriv(a.dato, a.kjoring)
    return 0


if __name__ == "__main__":
    sys.exit(main())
