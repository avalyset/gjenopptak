"""Kjøring av porten: bygg passasjer, døm dem, mål M1 og M2. Ingen OpenAlex-kall.

    python -m gjenopptak.classify.port_run bygg
    python -m gjenopptak.classify.port_run døm [--felt <felt>] [--maks-passasjer N]
    python -m gjenopptak.classify.port_run mål

Dommen er gjenopptakbar: hver passasje skrives fortløpende, og en ny kjøring tar bare dem
som mangler. Ledetekst A er uendret; oppfølgingen for treff har sin egen ledetekst.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from ..parse import sentences_from_jats
from ..parse.pdfroute import sentences_from_pdf
from ..vault import require_vault, sha256_file
from . import l3poc as P
from . import port as PO
from .l3poc_run import Lokal, les_jsonl, nå, skriv_jsonl


def _manifest(v: Path) -> dict[str, tuple[str, str, str]]:
    ut = {}
    for l in (v / "MANIFEST-UTVALG.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (\d+) \| (\S+) \| (\S+) \| (\S+) \| (\d+) \| ([0-9a-f]{64}) \|", l)
        if m:
            ut[m.group(6)] = (m.group(2), m.group(4), m.group(3))     # work_id, fil, ledd
    return ut


def bygg(stride: int = PO.STRIDE) -> int:
    V = require_vault()
    tmp = Path("data/tmp-port")  # regenererbar på minutter, blir på systemdisken
    PO.UT.mkdir(parents=True, exist_ok=True)
    spes = {"tid": nå(), "stride": stride, "window": PO.WINDOW,
            "prompt_A_sha256": sha256_file(PO.PROMPT_A),
            "prompt_oppfolging_sha256": hashlib.sha256(PO.OPPF_PROMPT.encode()).hexdigest(),
            "verk": [], "sum_setninger": 0, "sum_passasjer": 0}
    for felt in PO.FELT:
        rammen = {json.loads(l)["work_id"]: json.loads(l) for l in open(f"data/frames/frame-{felt}-RAW.jsonl")}
        # OpenAlex-typen fra trekkloggen: de atypiske (anmeldelse, konferanseabstrakt) skal kunne
        # trekkes ut av M1 etterpå, jf. ADDENDUM-09 §5 om resten av «ikke_artikkel».
        typer = {r["work_id"]: r.get("type") for r in
                 (json.loads(l) for l in open(f"data/utvalg/trekklogg-{felt}.jsonl")) if r["utfall"] == "trukket"}
        man = _manifest(V / "utvalg" / felt)
        setn, pas = [], []
        for u in [json.loads(l) for l in open(f"data/utvalg/utvalg-{felt}.jsonl")]:
            wid, fil, ledd = man[u["sha256"]]
            assert wid == u["work_id"], (wid, u["work_id"])
            b = (V / "utvalg" / felt / fil).read_bytes()
            rows = sentences_from_jats(b, doc_id=wid) if ledd == "P1-JATS" else \
                sentences_from_pdf(b, doc_id=wid, tmp_dir=tmp)
            ps = PO.passasjer(rows, felt, stride=stride)
            assert PO.dekker_alle_setninger(ps, len(rows)), wid
            setn += rows
            pas += [asdict(p) | {"seksjoner_i_vindu": list(p.seksjoner_i_vindu)} for p in ps]
            r = rammen[wid]
            spes["verk"].append({"felt": felt, "work_id": wid, "doi": u["doi"], "aar": u["aar"],
                                 "trekkposisjon": u["trekkposisjon"], "port_ledd": ledd, "fil": fil,
                                 "sha256": u["sha256"], "primary_topic_id": r["primary_topic_id"],
                                 "primary_topic_name": r["primary_topic_name"],
                                 "n_setninger": len(rows), "n_passasjer": len(ps),
                                 "type": typer.get(wid),
                                 "atypisk": typer.get(wid) in ("book-review", "conference-abstract")})
            spes["sum_setninger"] += len(rows)
            spes["sum_passasjer"] += len(ps)
        s1 = skriv_jsonl(setn, PO.UT / f"setninger-{felt}.jsonl")
        s2 = skriv_jsonl(pas, PO.UT / f"passasjer-{felt}.jsonl")
        print(f"{felt:22} setninger {len(setn):6} ({s1[:12]})  passasjer {len(pas):6} ({s2[:12]})", flush=True)
    (PO.UT / "spesifikasjon.json").write_text(json.dumps(spes, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("sum:", spes["sum_setninger"], "setninger,", spes["sum_passasjer"], "passasjer")
    return 0


def døm(felt_valg: str | None, maks: int | None, keep_alive: int | str = 0) -> int:
    system_a = PO.PROMPT_A.read_text(encoding="utf-8")
    spes = json.loads((PO.UT / "spesifikasjon.json").read_text())
    if hashlib.sha256(system_a.encode()).hexdigest() != spes["prompt_A_sha256"]:
        print("ledetekst A er endret: dom avbrytes", file=sys.stderr)
        return 2
    dommer = Lokal(keep_alive=keep_alive)
    gjort = 0
    for felt in ([felt_valg] if felt_valg else PO.FELT):
        pas = les_jsonl(PO.UT / f"passasjer-{felt}.jsonl")
        utfil = PO.UT / f"dommer-{felt}.jsonl"
        ferdige = {f"{r['doc_id']}:{r['start_index']}" for r in les_jsonl(utfil)}
        todo = [p for p in pas if f"{p['doc_id']}:{p['start_index']}" not in ferdige]
        print(f"{felt}: {len(todo)} av {len(pas)} passasjer igjen", flush=True)
        t0 = time.time()
        with utfil.open("a", encoding="utf-8") as fh:
            for i, p in enumerate(todo, 1):
                svar = dommer(system_a, P.user_prompt(p["tekst"]))
                v = P.parse_response(svar["råsvar"])
                rad = {**{k: p[k] for k in ("doc_id", "felt", "start_index", "end_index", "senter_index",
                                            "section_raw", "section_label_provenance", "seksjoner_i_vindu")},
                       "klasse": v.klasse, "treff": v.treff, "inkonsistent": v.inkonsistent,
                       "råsvar": svar["råsvar"], "bruk": svar["bruk"], "signatur": svar["signatur"]}
                if v.treff:
                    o = dommer(PO.OPPF_PROMPT, P.user_prompt(p["tekst"]), format=PO.OPPF_SCHEMA)
                    try:
                        d = json.loads(o["råsvar"])
                        rad["samme_setning"] = bool(d["samme_setning"])
                        rad["bedømbar"] = d["bedømbar"]
                        rad["oppf_begrunnelse"] = d.get("begrunnelse")
                    except (ValueError, KeyError, TypeError):
                        rad["samme_setning"] = None
                        rad["bedømbar"] = None
                        rad["oppf_begrunnelse"] = None
                    rad["oppf_signatur"] = o["signatur"]
                fh.write(json.dumps(rad, ensure_ascii=False) + "\n")
                fh.flush()
                gjort += 1
                if i % 20 == 0 or v.treff:
                    fart = (time.time() - t0) / i
                    print(f"  {felt} {i}/{len(todo)} {p['doc_id']}:{p['start_index']} {v.klasse} "
                          f"({fart:.1f} s/passasje, ~{fart*(len(todo)-i)/3600:.1f} t igjen)", flush=True)
                if maks and gjort >= maks:
                    print("maks nådd", flush=True)
                    _vekt_etter(dommer, gjort, keep_alive)
                    return 0
    _vekt_etter(dommer, gjort, keep_alive)
    return 0


def _vekt_etter(dommer: Lokal, gjort: int, keep_alive) -> None:
    """ADR-0008: vektfilen verifiseres også etter kjøringen, ikke bare før."""
    etter = "sha256:" + sha256_file(dommer.blob)
    (PO.UT / "vekter-etter.json").write_text(json.dumps(
        {"tid": nå(), "keep_alive": keep_alive, "passasjer_i_denne_kjøringen": gjort,
         "vekt_før": dommer.verifisert, "vekt_etter": etter,
         "uendret": etter == dommer.verifisert}, ensure_ascii=False) + "\n", encoding="utf-8")


def mål() -> int:
    spes = json.loads((PO.UT / "spesifikasjon.json").read_text())
    verk = spes["verk"]
    atypiske = {v["work_id"] for v in verk if v.get("atypisk")}
    alle_dommer, ferdige_verk = [], set()
    for felt in PO.FELT:
        rader = les_jsonl(PO.UT / f"dommer-{felt}.jsonl")
        alle_dommer += rader
        talt = Counter(r["doc_id"] for r in rader)
        for v in verk:
            if v["felt"] == felt and talt.get(v["work_id"], 0) >= v["n_passasjer"]:
                ferdige_verk.add(v["work_id"])
    treff = PO.treff_per_verk(alle_dommer)
    ut = {"tid": nå(), "ferdige_verk": len(ferdige_verk), "verk_i_alt": len(verk),
          "passasjer_dømt": len(alle_dommer), "passasjer_i_alt": spes["sum_passasjer"], "per_felt": {}}
    for felt in PO.FELT:
        f_verk = [v for v in verk if v["felt"] == felt and v["work_id"] in ferdige_verk]
        rader = [t for v in f_verk for t in treff.get(v["work_id"], [])]
        ut["per_felt"][felt] = {"ferdige_verk": len(f_verk), "treff": len(rader),
                                "M1_passasje": PO.m1(f_verk, treff, streng=False),
                                "M1_streng": PO.m1(f_verk, treff, streng=True),
                                "M2": PO.m2(rader),
                                "klasser": dict(Counter(t["klasse"] for t in rader).most_common())}
    f_alle = [v for v in verk if v["work_id"] in ferdige_verk]
    rader_alle = [t for v in f_alle for t in treff.get(v["work_id"], [])]
    ut["samlet"] = {"M1_passasje": PO.m1(f_alle, treff, streng=False),
                    "M1_streng": PO.m1(f_alle, treff, streng=True),
                    "M2": PO.m2(rader_alle),
                    "klasser": dict(Counter(t["klasse"] for t in rader_alle).most_common())}
    uten = [v for v in f_alle if v["work_id"] not in atypiske]
    ut["samlet_uten_atypiske"] = {"n_verk": len(uten),
                                  "M1_passasje": PO.m1(uten, treff, streng=False),
                                  "M1_streng": PO.m1(uten, treff, streng=True)}
    (PO.UT / "resultater.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(ut, ensure_ascii=False, indent=1)[:4000])
    return 0


def determinisme(keep_alive: str, utsnitt: int | None = None, bare_batch: bool = False) -> int:
    """ADR-0008: kjør alt dømte passasjer på nytt og krev identisk utfall.

    Før batchen: ``keep_alive`` satt, alle dommer fra ``keep_alive=0`` prøves på nytt (punkt 4).
    Etter batchen: ``--keep-alive 0 --utsnitt N --bare-batch`` prøver et frøtrukket utsnitt av de
    batch-dømte passasjene med utlastet modell (punkt 5).
    """
    system_a = PO.PROMPT_A.read_text(encoding="utf-8")
    alt: list[dict] = []
    for felt in PO.FELT:
        alt += les_jsonl(PO.UT / f"dommer-{felt}.jsonl")
    if bare_batch:
        alt = [r for r in alt if (r.get("signatur") or {}).get("batch")]
    if utsnitt and utsnitt < len(alt):
        import random
        alt = sorted(random.Random(P.MAALEFRO).sample(alt, utsnitt), key=lambda r: (r["doc_id"], r["start_index"]))
    pas = {}
    for felt in PO.FELT:
        for p in les_jsonl(PO.UT / f"passasjer-{felt}.jsonl"):
            pas[f"{p['doc_id']}:{p['start_index']}"] = p
    dommer = Lokal(keep_alive=keep_alive)
    vekt_før = dommer.verifisert
    ut = {"tid": nå(), "keep_alive": keep_alive, "utsnitt": utsnitt, "bare_batch": bare_batch,
          "n": len(alt), "identisk_råsvar": 0, "identisk_klasse": 0,
          "avvik": [], "vekt_før": vekt_før, "takt_s": None}
    t0 = time.time()
    for r in alt:
        p = pas[f"{r['doc_id']}:{r['start_index']}"]
        svar = dommer(system_a, P.user_prompt(p["tekst"]))
        lik_rå = svar["råsvar"] == r["råsvar"]
        lik_kl = P.parse_response(svar["råsvar"]).klasse == r["klasse"]
        ut["identisk_råsvar"] += lik_rå
        ut["identisk_klasse"] += lik_kl
        if not lik_rå:
            ut["avvik"].append({"passasje": f"{r['doc_id']}:{r['start_index']}", "før": r["råsvar"],
                                "nå": svar["råsvar"], "klasse_før": r["klasse"],
                                "klasse_nå": P.parse_response(svar["råsvar"]).klasse})
    ut["takt_s"] = (time.time() - t0) / len(alt) if alt else None
    ut["vekt_etter"] = "sha256:" + sha256_file(dommer.blob)
    ut["vekt_uendret"] = ut["vekt_etter"] == vekt_før
    ut["grønn"] = ut["identisk_råsvar"] == len(alt) and ut["vekt_uendret"]
    navn = "determinisme-ADR0008-etter.json" if bare_batch else "determinisme-ADR0008.json"
    (PO.UT / navn).write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in ut.items() if k != "avvik"}, ensure_ascii=False, indent=1))
    print("avvik:", len(ut["avvik"]))
    return 0 if ut["grønn"] else 1


def etterfyll(keep_alive: str | int) -> int:
    """Kjør oppfølgingskallet på nytt for treff som mangler enhet eller bedømbarhet.

    Treffene fra den første kjøringen fikk dommer A sitt JSON-skjema også i oppfølgingen, så
    ``samme_setning`` og ``bedømbar`` ble stående tomme. Dommen på treffet selv er uberørt.
    """
    pas = {}
    for felt in PO.FELT:
        for p in les_jsonl(PO.UT / f"passasjer-{felt}.jsonl"):
            pas[f"{p['doc_id']}:{p['start_index']}"] = p
    dommer = Lokal(keep_alive=keep_alive)
    n = 0
    for felt in PO.FELT:
        fil = PO.UT / f"dommer-{felt}.jsonl"
        rader = les_jsonl(fil)
        mangler = [r for r in rader if r.get("treff") and r.get("bedømbar") is None]
        if not mangler:
            continue
        print(f"{felt}: {len(mangler)} treff uten oppfølging", flush=True)
        for r in mangler:
            p = pas[f"{r['doc_id']}:{r['start_index']}"]
            o = dommer(PO.OPPF_PROMPT, P.user_prompt(p["tekst"]), format=PO.OPPF_SCHEMA)
            try:
                d = json.loads(o["råsvar"])
                r["samme_setning"] = bool(d["samme_setning"])
                r["bedømbar"] = d["bedømbar"]
                r["oppf_begrunnelse"] = d.get("begrunnelse")
            except (ValueError, KeyError, TypeError):
                r["samme_setning"] = r["bedømbar"] = r["oppf_begrunnelse"] = None
            r["oppf_signatur"] = o["signatur"]
            n += 1
            if n % 50 == 0:
                print(f"  etterfylt {n}", flush=True)
        skriv_jsonl(rader, fil)
    print("etterfylt i alt:", n)
    return 0


def PS_UT() -> Path:
    """Presisjonssettet ligger på Vault (ADR-0009)."""
    return utkatalog("presisjonssett")


def presisjonssett_bygg() -> int:
    """Trekk presisjonssettet: 150 dømte treff stratifisert på felt og klasse, 50 dømt INGEN, 20 ankere.

    Blindfilen har bare id og passasjetekst, og id-ene tildeles etter stokkingen, så de sier ingenting
    om hvor raden kom fra. Ankerne ligger der på lik linje med de 200. Nøkkelen med dømt klasse og
    ankernes fasitklasse ligger i egen fil og leses først når verdiktene er skrevet.
    """
    rader = []
    for felt in PO.FELT:
        rader += les_jsonl(PO.UT / f"dommer-{felt}.jsonl")
    treff = [r for r in rader if r["klasse"] in P.HIT_CLASSES]
    ingen = [r for r in rader if r["klasse"] == "INGEN"]
    n3 = [r for r in rader if r["klasse"] == "N3"]
    n1n2 = [r for r in rader if r["klasse"] in ("N1", "N2")]
    print(f"dømt: {len(rader)} | treff: {len(treff)} | INGEN: {len(ingen)} | N3: {len(n3)} | N1+N2: {len(n1n2)}")
    pas = {}
    for felt in PO.FELT:
        for x in les_jsonl(PO.UT / f"passasjer-{felt}.jsonl"):
            pas[f"{x['doc_id']}:{x['start_index']}"] = x
    ank = PO.ankere()
    grenser = PO.lengdegrenser(ank)
    mål = PO.lengdemål(ank, grenser)
    kv = lambda r: PO.kvartil(len(pas[f"{r['doc_id']}:{r['start_index']}"]["tekst"]), grenser)
    print(f"ankernes lengdekvartiler (tegn): {tuple(round(g) for g in grenser)} | måltetthet: {mål}")
    # treffene: felt med gulv først, klasse innenfor feltet, lengde innenfor klassen
    kvoter = PO.feltkvoter(treff, PO.N_TREFF, PO.GULV)
    print("feltkvoter treff:", dict(sorted(kvoter.items())), "| gulv:", PO.GULV)
    valgt_t = []
    for felt in sorted(kvoter):
        valgt_t += PO.stratifisert([r for r in treff if r["felt"] == felt], kvoter[felt],
                                   lambda r: r["klasse"], sekundær=kv, mål=mål)
    valgt_i = PO.stratifisert(ingen, PO.N_INGEN, lambda r: r["felt"], sekundær=kv, mål=mål)
    valgt_n3 = PO.stratifisert(n3, PO.N_N3, lambda r: r["felt"], sekundær=kv, mål=mål)
    poster = []
    for r, typ in ([(r, "treff") for r in valgt_t] + [(r, "ingen") for r in valgt_i]
                   + [(r, "n3") for r in valgt_n3] + [(r, "n1n2") for r in n1n2]):
        poster.append({"tekst": pas[f"{r['doc_id']}:{r['start_index']}"]["tekst"],
                       "nøkkel": {"utvalgstype": typ, "doc_id": r["doc_id"], "felt": r["felt"], "lag": None,
                                  "start_index": r["start_index"], "end_index": r["end_index"],
                                  "dømt_klasse": r["klasse"], "fasit_klasse": None, "kilde": None,
                                  "section_raw": r["section_raw"], "samme_setning": r.get("samme_setning"),
                                  "bedømbar": r.get("bedømbar")}})
    for a in ank:
        poster.append({"tekst": a["tekst"],
                       "nøkkel": {"utvalgstype": a["utvalgstype"], "doc_id": a["doc_id"], "felt": None,
                                  "lag": a["lag"], "start_index": a["start_index"], "end_index": a["end_index"],
                                  "dømt_klasse": None, "fasit_klasse": a["fasit_klasse"], "kilde": a["kilde"],
                                  "section_raw": None, "samme_setning": None, "bedømbar": None}})
    import random
    poster.sort(key=lambda x: (x["nøkkel"]["doc_id"], x["nøkkel"]["start_index"], x["nøkkel"]["utvalgstype"]))
    random.Random(P.MAALEFRO).shuffle(poster)
    blind, nøkkel = [], []
    for i, x in enumerate(poster, 1):
        pid = f"PS-{i:03d}"
        blind.append({"id": pid, "tekst": x["tekst"]})
        nøkkel.append({"id": pid, **x["nøkkel"]})
    s1 = skriv_jsonl(blind, (PS_UT() / "port-presisjonssett-blind.jsonl"))
    s2 = skriv_jsonl(nøkkel, (PS_UT() / "port-presisjonssett-nokkel.jsonl"))
    print(f"blind: {len(blind)} rader ({s1[:12]}) | nøkkel: {len(nøkkel)} rader ({s2[:12]})")
    print("blindfelter:", sorted({k for b in blind for k in b}))
    print("strata treff:", dict(Counter((r["felt"], r["klasse"]) for r in valgt_t).most_common()))
    print("felt i treffstratumet:", dict(sorted(Counter(r["felt"] for r in valgt_t).items())))
    print("felt i N3-stratumet:", dict(sorted(Counter(r["felt"] for r in valgt_n3).items())))
    print("N1/N2 lest i sin helhet:", dict(sorted(Counter(r["klasse"] for r in n1n2).items())))
    print("utvalgstyper:", dict(sorted(Counter(n["utvalgstype"] for n in nøkkel).items())))
    print("ankere:", dict(Counter(n["utvalgstype"] for n in nøkkel if n["utvalgstype"].startswith("anker"))))
    lp = sorted(len(x["tekst"]) for x in poster if not x["nøkkel"]["utvalgstype"].startswith("anker"))
    la = sorted(len(x["tekst"]) for x in poster if x["nøkkel"]["utvalgstype"].startswith("anker"))
    for navn, L in (("portrader", lp), ("ankere", la)):
        q = [round(PO._kvantil(L, q)) for q in (0.25, 0.5, 0.75)]
        print(f"lengde {navn}: n={len(L)} Q1={q[0]} median={q[1]} Q3={q[2]} min={L[0]} maks={L[-1]}")
    print("kvartilfordeling portrader:", dict(sorted(Counter(PO.kvartil(n, grenser) for n in lp).items())))
    return 0


def presisjonssett_mål() -> int:
    """Slå sammen mine verdikter med nøkkelen, og regn presisjon, recall, M1 og M2."""
    nøkkel = {r["id"]: r for r in les_jsonl((PS_UT() / "port-presisjonssett-nokkel.jsonl"))}
    mine = {r["id"]: r for r in les_jsonl((PS_UT() / "port-presisjonssett-verdikter.jsonl"))}
    tekst = {r["id"]: r["tekst"] for r in les_jsonl((PS_UT() / "port-presisjonssett-blind.jsonl"))}
    fasit = []
    for pid, k in nøkkel.items():
        m = mine.get(pid)
        if not m:
            continue
        fasit.append({**k, "tekst": tekst[pid], "ekte_treff": bool(m["ekte_treff"]),
                      "min_klasse": m.get("min_klasse"), "min_bedømbar": m.get("min_bedømbar"),
                      "tvil": bool(m.get("tvil")), "min_begrunnelse": m.get("begrunnelse")})
    skriv_jsonl(fasit, (PS_UT() / "port-presisjonssett.jsonl"))
    alle_dommer = []
    for felt in PO.FELT:
        alle_dommer += les_jsonl(PO.UT / f"dommer-{felt}.jsonl")
    vekter = Counter()
    for r in alle_dommer:
        if r["klasse"] == "INGEN":
            vekter["INGEN"] += 1
        elif r["klasse"] in ("N1", "N2"):
            vekter[r["klasse"]] += 1
        elif r["klasse"] == "N3":
            vekter["N3"] += 1
    pres = PO.presisjon(fasit, dict(vekter))
    spes = json.loads((PO.UT / "spesifikasjon.json").read_text())
    treff = PO.treff_per_verk(alle_dommer)
    verk = spes["verk"]
    atypiske = {v["work_id"] for v in verk if v["atypisk"]}
    uten = [v for v in verk if v["work_id"] not in atypiske]
    alle_treff = [t for ts in treff.values() for t in ts]
    lest = [f for f in fasit if f["utvalgstype"] == "treff" and f["ekte_treff"]]
    from ..harvest.coverage import TOPIC_IDS
    m1 = {}
    for enhet, streng in (("M1_passasje", False), ("M1_streng", True)):
        blokk = {}
        for omfang, vs in (("alle_100", verk), ("uten_atypiske", uten)):
            blokk[omfang] = {"samlet": PO.m1_varianter(vs, treff, pres["per_dømt_klasse"],
                                                       pres["presisjon"], streng=streng)}
            for felt in PO.FELT:
                vf = [v for v in vs if v["felt"] == felt]
                blokk[omfang][felt] = PO.m1_varianter(vf, treff, pres["per_dømt_klasse"],
                                                      pres["presisjon"], streng=streng)
        m1[enhet] = blokk
    bed = [f["min_bedømbar"] for f in lest if f["min_bedømbar"] is not None]
    ut = {"tid": nå(), "presisjon": pres, "ankere": PO.ankermål(fasit), "M1": m1,
          "topicdeling": PO.topicdeling(verk, fasit, TOPIC_IDS),
          "M2_dommerens": PO.m2(alle_treff),
          "M2_min_lesning": {"n_leste_ekte_treff": len(lest), "bedømbar": sum(1 for b in bed if b),
                             "ikke_bedømbar": sum(1 for b in bed if not b),
                             "M2": sum(1 for b in bed if b) / len(bed) if bed else None,
                             "merknad": "regnet på mine verdikter for de leste ekte treffene, ikke på dommerens merker"},
          "enhet_blant_leste_ekte_treff": dict(Counter(f["samme_setning"] for f in lest)),
          "tvilstilfeller": sum(1 for f in fasit if f["tvil"]),
          "n_treff_i_alt": len(alle_treff), "n_verk": len(verk)}
    (PO.UT / "presisjon-resultater.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(ut, ensure_ascii=False, indent=1)[:5000])
    return 0


from ..vault import krev, utkatalog  # ADR-0009


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Porten: L1+L2+dommer A på de hundre. Ingen OpenAlex-kall.")
    sub = ap.add_subparsers(dest="kommando", required=True)
    b = sub.add_parser("bygg"); b.add_argument("--stride", type=int, default=PO.STRIDE)
    d = sub.add_parser("døm"); d.add_argument("--felt", choices=PO.FELT); d.add_argument("--maks-passasjer", type=int)
    d.add_argument("--keep-alive", default="0", help="0 = ADR-0003 (last ut mellom dommer); ellers ADR-0008 batch, f.eks. 30m")
    k = sub.add_parser("determinisme"); k.add_argument("--keep-alive", default="30m")
    k.add_argument("--utsnitt", type=int, help="frøtrukket utsnitt (ADR-0008 punkt 5)")
    k.add_argument("--bare-batch", action="store_true", help="bare passasjer dømt i batch")
    sub.add_parser("mål")
    e = sub.add_parser("etterfyll"); e.add_argument("--keep-alive", default="30m")
    sub.add_parser("presisjonssett-bygg")
    sub.add_parser("presisjonssett-mål")
    a = ap.parse_args(argv)
    PO.UT = utkatalog("logs/port")  # ADR-0009: ingen fallback
    if a.kommando == "bygg":
        return bygg(a.stride)
    if a.kommando == "døm":
        ka = 0 if a.keep_alive in ("0", 0) else a.keep_alive
        return døm(a.felt, a.maks_passasjer, ka)
    if a.kommando == "presisjonssett-bygg":
        return presisjonssett_bygg()
    if a.kommando == "presisjonssett-mål":
        return presisjonssett_mål()
    if a.kommando == "etterfyll":
        return etterfyll(0 if a.keep_alive in ("0", 0) else a.keep_alive)
    if a.kommando == "determinisme":
        ka = 0 if a.keep_alive in ("0", 0) else a.keep_alive
        return determinisme(ka, a.utsnitt, a.bare_batch)
    return mål()

if __name__ == "__main__":
    raise SystemExit(main())
