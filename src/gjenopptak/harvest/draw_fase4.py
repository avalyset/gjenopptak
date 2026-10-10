"""Fase 4: håndskriftstudier, prospektiv port (ADDENDUM-26).

    PYTHONPATH=src python -m gjenopptak.harvest.draw_fase4 trekk
    PYTHONPATH=src python -m gjenopptak.harvest.draw_fase4 referanseutvalg

Samme vilkår som ADDENDUM-09 og fase 3 (``draw.decide``): kontroll/lest, typefilteret, feltets emne blant
verkets tre høyeste topics, hentingsporten P1/P3 og identitetsporten på P3. Forskjellene, låst i
ADDENDUM-26 § 2:

* **Rammen** er den frosne håndskriftrammen (topics T10595|T14210 med ordfilter på tittelen).
* **Ekskludert som brukt:** de 100 verkene fra første runde og de 100 fra fase 3.
* **Rekker rammen ikke til 100**, stopper trekkingen ved rammens slutt; ingen substitusjon, ingen utvidelse.
* **OpenAlex-kvoten føres før og etter** (fase 3 førte bare etter, RESULTAT-ADDENDUM-25 § 1.5).

Rekkefølgen er ``random.Random(734248).shuffle`` av den sorterte rammelisten, som i fase 3.
Utdata til Vault under ``fase4/``.
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from ..vault import copy_verified, require_vault, sha256_file
from .draw import (DrawRefused, Exclusions, MetaFetcher, decide, draw_order, order_sha256,
                   pdf_text, utvalg_rows, write_jsonl)
from .fetchtest import read_verdicts, run_frame

FELT = "haandskrift"
FRØ = 734248
N = 100
N_REFERANSE = 20
RAMME = "frames/frame-haandskrift-RAW.jsonl"
RAMME_SHA256 = "6e444a0837d6559906096b15ff6371ee6b630391d387702cc4171410225eaf75"
BRUKT_REPO = tuple(f"utvalg/utvalg-{f}.jsonl" for f in
                   ("energimodellering", "arkeologi", "klinisk_epidemiologi", "tekstvitenskap"))
BRUKT_VAULT = ("fase3/utvalg-fase3-arkeologi.jsonl",)
N_BRUKT = 200
LESELOGG = "logs/leste-kontrollkandidater.json"
UT = "fase4"
UTVALG = f"utvalg-fase4-{FELT}.jsonl"


def brukte_verk(repo_data: Path, vault: Path) -> set[str]:
    ids: set[str] = set()
    for p in [repo_data / r for r in BRUKT_REPO] + [vault / r for r in BRUKT_VAULT]:
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip():
                ids.add(json.loads(l)["work_id"])
    if len(ids) != N_BRUKT:
        raise DrawRefused(f"forventet {N_BRUKT} brukte verk, fant {len(ids)}")
    return ids


def _remaining(c) -> int | None:
    """Ett billig kall for å lese kvoten før trekkingen."""
    from .coverage import OPENALEX, year_filter
    from .freeze import _limits
    r = c.get(f"{OPENALEX}/works", params={"filter": year_filter(), "per-page": "1", "select": "id"})
    return _limits(r)[0]


def trekk(repo_data: Path = Path("data"), workers: int = 16) -> int:
    from .coverage import client, felt_topics

    v = require_vault()
    ut = v / UT
    if (ut / UTVALG).exists():
        print("IKKE STARTET: fase 4 er alt trukket", file=sys.stderr)
        return 2
    ut.mkdir(parents=True, exist_ok=True)
    liste = v / RAMME
    if sha256_file(liste) != RAMME_SHA256:
        print("IKKE STARTET: rammelisten har endret sha256", file=sys.stderr)
        return 2
    rows = [json.loads(l) for l in liste.open(encoding="utf-8")]
    by_id = {r["work_id"]: r for r in rows}
    order = draw_order(sorted(by_id), seed=FRØ)
    brukt = brukte_verk(repo_data, v)
    excl = Exclusions.from_log(v / LESELOGG)
    spes = {"felt": FELT, "fase": 4, "addendum": "ADDENDUM-26",
            "tid": datetime.now(timezone.utc).isoformat(timespec="seconds"), "frø": FRØ,
            "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                                     text=True).stdout.strip(),
            "rammeliste": RAMME, "rammeliste_sha256": RAMME_SHA256, "N": len(rows),
            "rekkefolge_sha256": order_sha256(order), "leselogg_sha256": excl.log_sha256,
            "brukt_ekskludert": len(brukt), "brukt_i_rammen": len(brukt & set(by_id)), "n": N}
    write_jsonl([spes], ut / f"trekkspesifikasjon-fase4-{FELT}.jsonl")

    filer = ut / "hentet"
    vfil = filer / "verdikter-fase4.jsonl"
    filer.mkdir(parents=True, exist_ok=True)
    tmp = repo_data / "tmp-fase4"
    verdikter = read_verdicts(vfil) if vfil.is_file() else {}
    tekster: dict[str, str] = {}

    def verdict_for(pos: int, row: dict):
        nonlocal verdikter
        if row["work_id"] not in verdikter:
            neste = [by_id[w] for w in order[pos - 1:pos - 1 + 50]
                     if w not in verdikter and w not in brukt]
            s = run_frame(neste, filer, tmp, vfil, workers=workers)
            if s.stopped:
                raise RuntimeError(f"hentingen stoppet: {s.stopped}")
            verdikter = read_verdicts(vfil)
        return verdikter[row["work_id"]]

    def text_for(vd) -> str:
        if vd.sha256 not in tekster:
            tekster[vd.sha256] = pdf_text((filer / vd.file).read_bytes(), tmp, vd.work_id)
        return tekster[vd.sha256]

    with client() as c:
        før = _remaining(c)
        meta = MetaFetcher(c, order, ut / "raw", stem="fase4-meta")
        beslutninger = decide(order, by_id, field_ids=felt_topics(FELT), exclusions=excl,
                              drawn_elsewhere=brukt, meta_for=meta, verdict_for=verdict_for,
                              text_for=text_for, n=N, n_char=0)
    for d in beslutninger:
        if d.grunn == "dobbeltramme":
            d.grunn = "brukt"
    logg_n, logg_sha = write_jsonl((d.as_row() for d in beslutninger), ut / f"trekklogg-fase4-{FELT}.jsonl")
    utv = [dict(r, felt=FELT, fil=f"{UT}/utvalg/{d.fil}") for r, d in zip(
        utvalg_rows(beslutninger),
        sorted((d for d in beslutninger if d.utfall == "trukket"), key=lambda d: d.trekkposisjon))]
    utv_n, utv_sha = write_jsonl(utv, ut / UTVALG)
    (ut / "verk-fase4.txt").write_text("\n".join(r["work_id"] for r in utv) + "\n", encoding="utf-8")
    for d in beslutninger:
        if d.utfall == "trukket":
            r = copy_verified(filer / d.fil, ut / "utvalg")
            if r.mismatch or r.sha256 != d.sha256:
                print(f"AVVIK ved kopiering av {d.fil}", file=sys.stderr)
                return 1
    uttømt = len(beslutninger) == len(order) and utv_n < N
    res = {"trukket": utv_n, "utvalg_sha256": utv_sha, "trekklogg_rader": logg_n,
           "trekklogg_sha256": logg_sha, "posisjoner_besøkt": len(beslutninger), "rammen_uttømt": uttømt,
           "hoppet": dict(Counter((d.grunn or "").split(":")[0] for d in beslutninger
                                  if d.utfall == "hoppet")),
           "port_testet": sum(d.port_testet for d in beslutninger),
           "port_inne": sum(bool(d.port_inne) for d in beslutninger),
           "openalex_kall": meta.calls + 1, "openalex_remaining_før": før,
           "openalex_remaining": meta.remaining,
           "ledd": dict(Counter(d.port_ledd for d in beslutninger if d.utfall == "trukket"))}
    (ut / "trekkresultat-fase4.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                                                 encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0 if (utv_n == N or uttømt) else 1


def referanseutvalg() -> int:
    """20 av de trukne, med frøet over den sorterte listen. Skrives før silen kjøres. Er færre enn 100
    trukket, er det fortsatt 20 (eller alle, om det er færre enn 20)."""
    v = require_vault()
    ut = v / UT
    f = ut / "referanse-verk.json"
    if f.exists():
        print("finnes alt — trekkes ikke om", file=sys.stderr)
        return 2
    utv = [json.loads(l) for l in (ut / UTVALG).read_text(encoding="utf-8").splitlines() if l.strip()]
    ids = sorted(r["work_id"] for r in utv)
    n = min(N_REFERANSE, len(ids))
    valgt = sorted(random.Random(FRØ).sample(ids, n))
    f.write_text(json.dumps({"frø": FRØ, "fra": UTVALG, "fra_sha256": sha256_file(ut / UTVALG),
                             "metode": f"random.Random({FRØ}).sample(sorted(ids), {n})",
                             "verk": valgt}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("\n".join(valgt))
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("kommando", choices=("trekk", "referanseutvalg"))
    p.add_argument("--workers", type=int, default=16)
    a = p.parse_args(argv)
    try:
        return trekk(workers=a.workers) if a.kommando == "trekk" else referanseutvalg()
    except DrawRefused as e:
        print(f"IKKE STARTET: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
