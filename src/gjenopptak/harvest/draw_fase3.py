"""Fase 3: nye verk fra den frosne arkeologi-rammen, med prospektiv port (ADDENDUM-25).

    PYTHONPATH=src python -m gjenopptak.harvest.draw_fase3 trekk
    PYTHONPATH=src python -m gjenopptak.harvest.draw_fase3 referanseutvalg

Samme vilkår som ADDENDUM-09 (``draw.decide``): kontroll/lest, typefilter, feltets emne blant
verkets tre høyeste topics, hentingsporten P1/P3 og identitetsporten på P3. To forskjeller, begge
låst i ADDENDUM-25 § 2:

* **Rekkefølgen** er en ny stokking av den frosne, sorterte rammelisten med **frø 734248**, ikke
  prereg-frøet. Den gamle rekkefølgen er alt brukt til posisjon 94.
* **De 100 verkene som alt er brukt** (alle fire felt, ``utvalg-*.jsonl``) er ekskludert som
  ``brukt``, i tillegg til kontrollene og de leste.

Trekkingen stopper ved 100. Ingen substitusjon. Utdata til Vault under ``fase3/``.
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

FELT = "arkeologi"
FRØ = 734248
N = 100
N_REFERANSE = 20
RAMME = "frames/frame-arkeologi-RAW.jsonl"
RAMME_SHA256 = "1050450fc774e56affc21c99e0ffc3c59682ff391c1e46163c69a50d5cdf241a"
BRUKT = tuple(f"utvalg/utvalg-{f}.jsonl" for f in
              ("energimodellering", "arkeologi", "klinisk_epidemiologi", "tekstvitenskap"))
LESELOGG = "logs/leste-kontrollkandidater.json"
UT = "fase3"


def brukte_verk(repo_data: Path) -> set[str]:
    ids: set[str] = set()
    for rel in BRUKT:
        for l in (repo_data / rel).read_text(encoding="utf-8").splitlines():
            if l.strip():
                ids.add(json.loads(l)["work_id"])
    if len(ids) != 100:
        raise DrawRefused(f"forventet 100 brukte verk, fant {len(ids)}")
    return ids


def trekk(repo_data: Path = Path("data"), workers: int = 16) -> int:
    from .coverage import TOPIC_IDS, client

    v = require_vault()
    ut = v / UT
    if (ut / "utvalg-fase3-arkeologi.jsonl").exists():
        print("IKKE STARTET: fase 3 er alt trukket", file=sys.stderr)
        return 2
    ut.mkdir(parents=True, exist_ok=True)
    liste = v / RAMME
    if sha256_file(liste) != RAMME_SHA256:
        print("IKKE STARTET: rammelisten har endret sha256", file=sys.stderr)
        return 2
    rows = [json.loads(l) for l in liste.open(encoding="utf-8")]
    by_id = {r["work_id"]: r for r in rows}
    order = draw_order(sorted(by_id), seed=FRØ)
    brukt = brukte_verk(repo_data)
    excl = Exclusions.from_log(v / LESELOGG)
    spes = {"felt": FELT, "fase": 3, "addendum": "ADDENDUM-25",
            "tid": datetime.now(timezone.utc).isoformat(timespec="seconds"), "frø": FRØ,
            "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                                     text=True).stdout.strip(),
            "rammeliste": RAMME, "rammeliste_sha256": RAMME_SHA256, "N": len(rows),
            "rekkefolge_sha256": order_sha256(order), "leselogg_sha256": excl.log_sha256,
            "brukt_ekskludert": len(brukt), "n": N}
    write_jsonl([spes], ut / "trekkspesifikasjon-fase3-arkeologi.jsonl")

    filer = ut / "hentet"
    vfil = filer / "verdikter-fase3.jsonl"
    filer.mkdir(parents=True, exist_ok=True)
    tmp = repo_data / "tmp-fase3"
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
        meta = MetaFetcher(c, order, ut / "raw", stem="fase3-meta")
        beslutninger = decide(order, by_id, field_ids=TOPIC_IDS[FELT], exclusions=excl,
                              drawn_elsewhere=brukt, meta_for=meta, verdict_for=verdict_for,
                              text_for=text_for, n=N, n_char=0)
    # «dobbeltramme» betyr her «brukt i de 100»; grunnen skrives om så loggen sier hva som skjedde.
    for d in beslutninger:
        if d.grunn == "dobbeltramme":
            d.grunn = "brukt"
    logg_n, logg_sha = write_jsonl((d.as_row() for d in beslutninger), ut / "trekklogg-fase3-arkeologi.jsonl")
    utv = [dict(r, felt=FELT, fil=f"{UT}/utvalg/{d.fil}") for r, d in zip(
        utvalg_rows(beslutninger),
        sorted((d for d in beslutninger if d.utfall == "trukket"), key=lambda d: d.trekkposisjon))]
    utv_n, utv_sha = write_jsonl(utv, ut / "utvalg-fase3-arkeologi.jsonl")
    (ut / "verk-fase3.txt").write_text("\n".join(r["work_id"] for r in utv) + "\n", encoding="utf-8")
    for d in beslutninger:
        if d.utfall == "trukket":
            r = copy_verified(filer / d.fil, ut / "utvalg")
            if r.mismatch or r.sha256 != d.sha256:
                print(f"AVVIK ved kopiering av {d.fil}", file=sys.stderr)
                return 1
    res = {"trukket": utv_n, "utvalg_sha256": utv_sha, "trekklogg_rader": logg_n,
           "trekklogg_sha256": logg_sha, "posisjoner_besøkt": len(beslutninger),
           "hoppet": dict(Counter((d.grunn or "").split(":")[0] for d in beslutninger
                                  if d.utfall == "hoppet")),
           "port_testet": sum(d.port_testet for d in beslutninger),
           "port_inne": sum(bool(d.port_inne) for d in beslutninger),
           "openalex_kall": meta.calls, "openalex_remaining": meta.remaining,
           "ledd": dict(Counter(d.port_ledd for d in beslutninger if d.utfall == "trukket"))}
    (ut / "trekkresultat-fase3.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                                                 encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0 if utv_n == N else 1


def referanseutvalg() -> int:
    """20 av de 100, trukket med frøet over den sorterte listen. Skrives før silen kjøres."""
    v = require_vault()
    ut = v / UT
    f = ut / "referanse-verk.json"
    if f.exists():
        print("finnes alt — trekkes ikke om", file=sys.stderr)
        return 2
    utv = [json.loads(l) for l in (ut / "utvalg-fase3-arkeologi.jsonl").read_text().splitlines() if l.strip()]
    ids = sorted(r["work_id"] for r in utv)
    if len(ids) != N:
        raise DrawRefused(f"utvalget har {len(ids)} verk, ikke {N}")
    valgt = sorted(random.Random(FRØ).sample(ids, N_REFERANSE))
    f.write_text(json.dumps({"frø": FRØ, "fra": "utvalg-fase3-arkeologi.jsonl",
                             "fra_sha256": sha256_file(ut / "utvalg-fase3-arkeologi.jsonl"),
                             "metode": "random.Random(734248).sample(sorted(ids), 20)",
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
