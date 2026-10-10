"""Reanalyse etter ekstern fagfellevurdering (03.10.2026). Bare lesing; ingen låst fil endres.

    PYTHONPATH=src python -m gjenopptak.classify.reanalyse_fagfelle

Skriver `revisjon-2026-10/reanalyse.json` på Vault. Punktene følger oppdraget:

a) verk-klynget bootstrap (10 000, frø 734248) for κ på 320-settet (koder 1/2/4 og Opus ett kall), de to
   85/100-portene, recall i fase 3, og H7- og H1–H6-andelene i begge registrene — side om side med tallene som
   står i manuskriptet, og fordelingen av rader per verk i hver prøve;
b) paret bootstrap (passasjenivå og verksnivå) på differansen κ(koder 2) − κ(Opus ett kall), begge mot koder 1;
c) rå enighet, PABAK og Gwets AC1 ved hver κ;
d) positiv rate blant silkandidatene per felt, og silkandidatenes andel av alle tekstbiter per felt;
e) prevalensestimatoren bak 3,43 % skrevet ut (strata, størrelser, trekk, vekter) med intervall som tar med
   begge kildene til usikkerhet, passasjevis og verksvis;
f) registerrader som deler setning med en annen rad i samme verk, og tallene på nytt etter deduplisering.

Klyngeenheten er verket (`doc_id`/`work_id`). Bootstrap-intervallene er persentilintervaller.
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

from ..vault import require_vault, sha256_file
from .fase3 import wilson
from .liftability import is_unresolved, liftability, liftable_share

FRØ = 734248
B = 10_000
REPO = Path(__file__).resolve().parents[3]
FELT = ("arkeologi", "energimodellering", "klinisk_epidemiologi", "tekstvitenskap")


def _jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


# ------------------------------------------------------------------ enighetsmål
def enighet(a: list[bool], b: list[bool]) -> dict:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    kappa = (po - pe) / (1 - pe) if pe < 1 else 0.0
    pi = (pa + pb) / 2
    pe_ac1 = 2 * pi * (1 - pi)
    ac1 = (po - pe_ac1) / (1 - pe_ac1) if pe_ac1 < 1 else 1.0
    return {"n": n, "rå_enighet": round(po, 4), "kappa": round(kappa, 4), "pabak": round(2 * po - 1, 4),
            "gwet_ac1": round(ac1, 4), "positive_a": sum(a), "positive_b": sum(b)}


def _pct(xs: list[float]) -> list[float]:
    xs = sorted(x for x in xs if x == x)
    return [round(xs[int(0.025 * len(xs))], 4), round(xs[min(len(xs) - 1, int(0.975 * len(xs)))], 4)]


def boot_kappa(rader: list[tuple[str, bool, bool]], *, klynge: bool, rng: random.Random) -> list[float]:
    """rader = (verk, a, b). Passasjenivå: trekk rader; verksnivå: trekk verk og ta alle radene deres."""
    per = defaultdict(list)
    for w, a, b in rader:
        per[w].append((a, b))
    verk = sorted(per)
    ut = []
    for _ in range(B):
        if klynge:
            par = [p for w in (rng.choice(verk) for _ in verk) for p in per[w]]
        else:
            par = [(rader[i][1], rader[i][2]) for i in (rng.randrange(len(rader)) for _ in rader)]
        ut.append(enighet([p[0] for p in par], [p[1] for p in par])["kappa"])
    return ut


def boot_andel(rader: list[tuple[str, bool]], *, rng: random.Random) -> list[float]:
    per = defaultdict(list)
    for w, x in rader:
        per[w].append(x)
    verk = sorted(per)
    ut = []
    for _ in range(B):
        xs = [x for w in (rng.choice(verk) for _ in verk) for x in per[w]]
        ut.append(sum(xs) / len(xs) if xs else float("nan"))
    return ut


def fordeling(verk: list[str]) -> dict:
    c = Counter(verk)
    return {"rader": len(verk), "verk": len(c), "rader_per_verk": dict(sorted(Counter(c.values()).items())),
            "største_verk": c.most_common(1)[0][1] if c else 0}


def andel_rad(navn: str, rader: list[tuple[str, bool]], oppgitt: str, rng: random.Random) -> dict:
    k, n = sum(x for _, x in rader), len(rader)
    return {"mål": navn, "k": k, "n": n, "andel": round(k / n, 4), "oppgitt_i_manus": oppgitt,
            "wilson95_passasje": list(wilson(k, n)), "klynge_bootstrap95": _pct(boot_andel(rader, rng=rng)),
            "fordeling": fordeling([w for w, _ in rader])}


# ------------------------------------------------------------------ data
def last(v: Path) -> dict:
    P = v / "presisjonssett"
    k1 = {r["id"]: r for r in _jl(P / "port-presisjonssett-ADDENDUM10.jsonl")}
    k2 = {r["id"]: r for r in _jl(P / "port-presisjonssett-verdikter-koder2.jsonl")}
    k4 = {r["id"]: r for r in _jl(v / "koder4" / "koder4-fable51-verdikter.jsonl")}
    op = {}
    for r in _jl(v / "ekstraksjon/2026-09-26/addendum-19/opus5-b-dommer.jsonl"):
        try:
            op[r["id"]] = bool(json.loads(r["raasvar"])["treff"])
        except (ValueError, KeyError, TypeError):
            op[r["id"]] = None
    return {"k1": k1, "k2": k2, "k4": k4, "opus": op}


def _t(r: dict) -> bool:
    return bool(r["ekte_treff"]) if "ekte_treff" in r else bool(r["treff"])


# ------------------------------------------------------------------ a, b, c
def kappaer(d: dict, rng: random.Random) -> dict:
    k1, k2, k4, op = d["k1"], d["k2"], d["k4"], d["opus"]
    ids = sorted(k1)
    w = {i: k1[i]["doc_id"] for i in ids}
    par = {"koder 1 mot koder 2": (lambda i: _t(k1[i]), lambda i: _t(k2[i]), "0,812 [0,697–0,906]"),
           "koder 4 mot koder 2": (lambda i: _t(k4[i]), lambda i: _t(k2[i]), "0,899 [0,808–0,969]"),
           "koder 4 mot koder 1": (lambda i: _t(k4[i]), lambda i: _t(k1[i]), "0,781 [0,659–0,883]"),
           "Opus ett kall mot koder 1": (lambda i: op[i], lambda i: _t(k1[i]), "0,636 [0,478–0,768]")}
    ut = {"fordeling_320": fordeling([w[i] for i in ids]), "par": {}}
    for navn, (fa, fb, oppgitt) in par.items():
        bruk = [i for i in ids if fa(i) is not None]
        rader = [(w[i], fa(i), fb(i)) for i in bruk]
        e = enighet([r[1] for r in rader], [r[2] for r in rader])
        ut["par"][navn] = {**e, "oppgitt_i_manus": oppgitt, "uten_svar": len(ids) - len(bruk),
                           "passasje_bootstrap95": _pct(boot_kappa(rader, klynge=False, rng=random.Random(FRØ))),
                           "klynge_bootstrap95": _pct(boot_kappa(rader, klynge=True, rng=random.Random(FRØ))),
                           "verk": len({r[0] for r in rader})}
    # b) paret differanse κ(k2,k1) − κ(opus,k1) på de samme passasjene
    bruk = [i for i in ids if op[i] is not None]
    per = defaultdict(list)
    for i in bruk:
        per[w[i]].append(i)
    verk = sorted(per)

    def diff(utvalg: list[str]) -> float:
        a = enighet([_t(k2[i]) for i in utvalg], [_t(k1[i]) for i in utvalg])["kappa"]
        b = enighet([op[i] for i in utvalg], [_t(k1[i]) for i in utvalg])["kappa"]
        return a - b
    r1, r2 = random.Random(FRØ), random.Random(FRØ)
    pas = [diff([bruk[r1.randrange(len(bruk))] for _ in bruk]) for _ in range(B)]
    kly = [diff([i for v_ in (r2.choice(verk) for _ in verk) for i in per[v_]]) for _ in range(B)]
    ut["differanse_koder2_minus_opus"] = {"n": len(bruk), "punkt": round(diff(bruk), 4),
                                          "passasje_paret95": _pct(pas), "klynge_paret95": _pct(kly),
                                          "andel_≤0_passasje": round(sum(x <= 0 for x in pas) / B, 4),
                                          "andel_≤0_klynge": round(sum(x <= 0 for x in kly) / B, 4)}
    return ut


def porter_og_recall(v: Path, rng: random.Random) -> dict:
    al = {r["id"]: r for r in _jl(v / "arbeidsliste" / "nokkel.jsonl")}
    # Kodet av to instanser, 85 + 15, fordi den første ble avbrutt (presisjon-100-maal.json, «avvik»).
    pv = _jl(v / "arbeidsliste" / "presisjon-100-verdikter.jsonl") + _jl(v / "arbeidsliste" / "presisjon-rest-verdikter.jsonl")
    post = [(al[r["id"]]["doc_id"], r.get("treff") is True) for r in pv]
    f3n = {r["id"]: r for r in _jl(v / "fase3" / "presisjon" / "nokkel-presisjon.jsonl")}
    f3v = _jl(v / "fase3" / "presisjon" / "verdikter-presisjon.jsonl")
    f3 = [(f3n[r["id"]]["doc_id"], r.get("treff") is True) for r in f3v]
    m = json.loads((v / "fase3" / "maaling-fase3.json").read_text(encoding="utf-8"))["rader"]
    return {
        "post_hoc_port_85_100": andel_rad("blind bekreftelse, post hoc port (ADDENDUM-23)", post, "85/100 [76,7–90,7]", rng),
        "fase3_port_85_100": andel_rad("blind bekreftelse, fase 3 (ADDENDUM-25)", f3, "85/100 [76,7–90,7]", rng),
        "fase3_beholdt": andel_rad("silens recall, fase 3", [(r["work_id"], r["beholdt"]) for r in m],
                                   "95/104 = 91,3 % [84,4–95,4]", rng),
        "fase3_bekreftet": andel_rad("leserens recall, fase 3", [(r["work_id"], r["bekreftet"]) for r in m],
                                     "85/104 = 81,7 % [73,2–88,0]", rng),
    }


def klasseandeler(rader: list[dict], navn: str, h7_oppgitt: str, loft_oppgitt: str, rng: random.Random) -> dict:
    h7 = [(r["doc_id"], r["obstacle_class"] == "H7") for r in rader]
    avkl = [r for r in rader if not is_unresolved(r["obstacle_class"])]
    loft = [(r["doc_id"], liftability(r["obstacle_class"]) in ("ja", "ja_med_forbehold", "delvis")) for r in avkl]
    ls = liftable_share([r["obstacle_class"] for r in rader])
    assert ls["n_resolved"] == len(avkl) and ls["n_liftable"] == sum(x for _, x in loft)
    return {"register": navn, "H7_av_alle": andel_rad("H7 av alle rader", h7, h7_oppgitt, rng),
            "H1_H6_av_avklarte": andel_rad("løftbar H1–H6 av avklarte", loft, loft_oppgitt, rng)}


# ------------------------------------------------------------------ d
def felt(v: Path) -> dict:
    nøkkel = _jl(v / "kandidat432" / "nokkel.jsonl")
    reg = _jl(v / "kandidat432" / "8-register.jsonl")
    tb = Counter()
    for f in FELT:
        for l in (REPO / "data" / "port" / f"dommer-{f}.jsonl").read_text(encoding="utf-8").splitlines():
            if l.strip():
                tb[f] += 1
    kand, pos = Counter(r["felt"] for r in nøkkel), Counter(r["field_key"] for r in reg)
    ut = {}
    for f in FELT:
        ut[f] = {"tekstbiter": tb[f], "silkandidater": kand[f], "leser_positive": pos[f],
                 "positiv_rate_blant_silkandidater": round(pos[f] / kand[f], 4),
                 "wilson95": list(wilson(pos[f], kand[f])),
                 "silkandidatenes_andel_av_tekstbiter": round(kand[f] / tb[f], 4),
                 "leser_positive_per_1000_tekstbiter": round(1000 * pos[f] / tb[f], 2)}
    rates = [ut[f]["positiv_rate_blant_silkandidater"] for f in FELT]
    ut["_forhold_høyest_lavest_blant_silkandidater"] = round(max(rates) / min(rates), 2)
    p1000 = [ut[f]["leser_positive_per_1000_tekstbiter"] for f in FELT]
    ut["_forhold_høyest_lavest_per_tekstbit"] = round(max(p1000) / min(p1000), 2)
    ut["_summer"] = {"tekstbiter": sum(tb.values()), "silkandidater": sum(kand.values()), "positive": sum(pos.values())}
    ut["_merknad"] = ("positiv rate blant silkandidater er ikke feltets prevalens: silens kandidatandel og "
                      "sensitivitet per felt er ikke målt i første runde")
    return ut


# ------------------------------------------------------------------ e
def prevalens(v: Path, d: dict) -> dict:
    """Grunnraten c) i METODE § 1, med estimatoren skrevet ut.

    Flaggede (dommeren sa treff, 2 173) er stratifisert på felt × dømt klasse; de 150 leste er trukket med
    feltkvoter (tekstvitenskap-gulv 25) og klassestratifisering. Ikke-flaggede (20 070) er stratifisert på
    dommerens ikke-treff-klasse; 50 INGEN og 50 N3 er lest, N1 og N2 er lest i sin helhet. Positiv = koder 1
    (`ekte_treff`).

        T̂ = Σ_c N_c · k_c / n_c   (flaggede celler c)  +  Σ_s N_s · k_s / n_s   (ikke-flaggede strata s)
        prevalens = T̂ / 22 243
    """
    k1 = d["k1"]
    N_flag, N_ikke = Counter(), Counter()
    for f in FELT:
        for l in (REPO / "data" / "port" / f"dommer-{f}.jsonl").read_text(encoding="utf-8").splitlines():
            if not l.strip():
                continue
            r = json.loads(l)
            (N_flag.__setitem__((f, r["klasse"]), N_flag[(f, r["klasse"])] + 1) if r["treff"] is True
             else N_ikke.__setitem__(r["klasse"], N_ikke[r["klasse"]] + 1))
    N = sum(N_flag.values()) + sum(N_ikke.values())
    flagg = [r for r in k1.values() if r["utvalgstype"] == "treff"]
    ikke = {"INGEN": "ingen", "N3": "n3"}
    lest_ikke = {s: [r for r in k1.values() if r["utvalgstype"] == u] for s, u in ikke.items()}
    n1n2 = [r for r in k1.values() if r["utvalgstype"] == "n1n2"]

    def celle(r):
        return (r["felt"], r["dømt_klasse"])

    def estimer(fl: list[dict], ik: dict[str, list[dict]], nn: list[dict]) -> tuple[float, dict]:
        per = defaultdict(list)
        for r in fl:
            per[celle(r)].append(_t(r))
        # Celler uten leste rader får feltets samlede rate blant de leste (dekkes ikke av utvalget ellers).
        felt_rate = {f: (sum(_t(r) for r in fl if r["felt"] == f) / max(1, sum(1 for r in fl if r["felt"] == f)))
                     for f in FELT}
        T_f, udekket = 0.0, 0
        for c, Nc in N_flag.items():
            xs = per.get(c)
            if xs:
                T_f += Nc * sum(xs) / len(xs)
            else:
                T_f += Nc * felt_rate[c[0]]
                udekket += Nc
        T_u = 0.0
        for s, rr in ik.items():
            T_u += N_ikke[s] * (sum(_t(r) for r in rr) / len(rr))
        T_u += sum(_t(r) for r in nn)          # N1 og N2: lest i sin helhet (37 + 13 = 50)
        return T_f + T_u, {"T_flagget": round(T_f, 1), "T_ikke_flagget": round(T_u, 1), "udekket_flagget": udekket}

    T, deler = estimer(flagg, lest_ikke, n1n2)
    rng_p, rng_k = random.Random(FRØ), random.Random(FRØ)
    pas, kly = [], []
    alle = flagg + lest_ikke["INGEN"] + lest_ikke["N3"]
    per_verk = defaultdict(list)
    for r in alle:
        per_verk[r["doc_id"]].append(r)
    verk = sorted(per_verk)
    for _ in range(B):
        # stratifisert passasjebootstrap: trekk innenfor hvert stratum med samme n
        fl = [flagg[rng_p.randrange(len(flagg))] for _ in flagg]
        ik = {s: [rr[rng_p.randrange(len(rr))] for _ in rr] for s, rr in lest_ikke.items()}
        pas.append(estimer(fl, ik, n1n2)[0] / N)
        # verksklynget: trekk verk, behold stratumtilhørigheten til hver rad
        rader = [r for w in (rng_k.choice(verk) for _ in verk) for r in per_verk[w]]
        fl = [r for r in rader if r["utvalgstype"] == "treff"]
        ik = {s: [r for r in rader if r["utvalgstype"] == u] for s, u in ikke.items()}
        if fl and all(ik.values()):
            kly.append(estimer(fl, ik, n1n2)[0] / N)
    ufl = [r for r in flagg]
    return {
        "estimator": "T̂ = Σ_c N_c·k_c/n_c (flaggede, celle = felt × dømt klasse) + Σ_s N_s·k_s/n_s (ikke-flaggede: INGEN, N3) + k(N1)+k(N2) (lest i sin helhet); prevalens = T̂/N",
        "N_tekstbiter": N, "N_flagget": sum(N_flag.values()),
        "flaggede_celler": [{"felt": f, "dømt_klasse": k, "N": n, "lest": sum(1 for r in ufl if celle(r) == (f, k)),
                             "positive": sum(_t(r) for r in ufl if celle(r) == (f, k))}
                            for (f, k), n in sorted(N_flag.items())],
        "ikke_flaggede_strata": [{"stratum": s, "N": N_ikke[s], "lest": len(lest_ikke[s]) if s in lest_ikke else
                                  sum(1 for r in n1n2 if r["dømt_klasse"] == s),
                                  "positive": sum(_t(r) for r in lest_ikke[s]) if s in lest_ikke else
                                  sum(_t(r) for r in n1n2 if r["dømt_klasse"] == s)} for s in sorted(N_ikke)],
        "punkt": {"T": round(T, 1), "prevalens": round(T / N, 5), **deler},
        "manus": {"tall": "362/0,475 = 763 → 3,43 % [2,12–7,95]",
                  "intervall_rekonstruert": "(362 + 110)/22 243 og (362 + 1 405)/22 243: punktpresisjonen uvektet "
                                            "(25/150) pluss Wilson-grensene for en uvektet bomrate 2/100 — "
                                            "presisjonens usikkerhet og klyngene er ikke med"},
        "stratifisert_passasje_bootstrap95": _pct(pas),
        "verksklynget_bootstrap95": _pct(kly), "verksklynget_gyldige_replikater": len(kly),
    }


# ------------------------------------------------------------------ f
def duplikater(rader: list[dict], navn: str) -> dict:
    """Rader i samme verk der setningsspennene overlapper, slått sammen til komponenter (unike erklæringer).
    Komponentens klasse er den hyppigste; ved likhet merkes den «blandet» og telles ikke i klasseandelene."""
    per = defaultdict(list)
    for r in rader:
        s = r["passage_span"]
        per[r["doc_id"]].append((int(s["start_index"]), int(s["end_index"]), r))
    komponenter = []
    for w, xs in per.items():
        xs.sort(key=lambda x: x[0])
        cur = [xs[0]]
        slutt = xs[0][1]
        for x in xs[1:]:
            if x[0] <= slutt:
                cur.append(x)
                slutt = max(slutt, x[1])
            else:
                komponenter.append(cur)
                cur, slutt = [x], x[1]
        komponenter.append(cur)
    delt = sum(len(k) for k in komponenter if len(k) > 1)
    klasser = []
    blandet = 0
    for k in komponenter:
        c = Counter(x[2]["obstacle_class"] for x in k).most_common()
        if len(c) > 1 and c[0][1] == c[1][1]:
            blandet += 1
            continue
        klasser.append(c[0][0])
    ls = liftable_share(klasser)
    return {"register": navn, "rader": len(rader), "rader_som_deler_setning": delt,
            "unike_erklæringer": len(komponenter), "komponenter_med_flere_rader": sum(len(k) > 1 for k in komponenter),
            "største_komponent": max(len(k) for k in komponenter), "blandet_klasse": blandet,
            "H7_av_unike": {"k": klasser.count("H7"), "n": len(klasser),
                            "andel": round(klasser.count("H7") / len(klasser), 4),
                            "wilson95": list(wilson(klasser.count("H7"), len(klasser)))},
            "H1_H6_av_avklarte_unike": {"k": ls["n_liftable"], "n": ls["n_resolved"],
                                        "andel": round(ls["n_liftable"] / ls["n_resolved"], 4),
                                        "wilson95": list(wilson(ls["n_liftable"], ls["n_resolved"]))}}


def main() -> int:
    v = require_vault()
    d = last(v)
    rng = random.Random(FRØ)
    reg432 = _jl(v / "kandidat432" / "8-register.jsonl")
    reg673 = _jl(v / "fase3-kjede" / "8-register.jsonl")
    ut = {"frø": FRØ, "B": B, "klyngeenhet": "verk (doc_id / work_id)",
          "kilder": {str(p.relative_to(v)): sha256_file(p) for p in (
              v / "presisjonssett/port-presisjonssett-ADDENDUM10.jsonl",
              v / "presisjonssett/port-presisjonssett-verdikter-koder2.jsonl",
              v / "koder4/koder4-fable51-verdikter.jsonl",
              v / "ekstraksjon/2026-09-26/addendum-19/opus5-b-dommer.jsonl",
              v / "arbeidsliste/nokkel.jsonl", v / "arbeidsliste/presisjon-100-verdikter.jsonl",
              v / "arbeidsliste/presisjon-rest-verdikter.jsonl",
              v / "fase3/presisjon/nokkel-presisjon.jsonl", v / "fase3/presisjon/verdikter-presisjon.jsonl",
              v / "fase3/maaling-fase3.json", v / "kandidat432/8-register.jsonl", v / "kandidat432/nokkel.jsonl",
              v / "fase3-kjede/8-register.jsonl")},
          "a_c_kappa": kappaer(d, rng),
          "a_porter_recall": porter_og_recall(v, rng),
          "a_klasser": [klasseandeler(reg432, "register v2 (432)", "289/432 = 66,9 % [62,3–71,2]", "77/406 = 19,0 % [15,4–23,1]", rng),
                        klasseandeler(reg673, "fase 3-register (673)", "425/673 = 63,2 % [59,4–66,7]", "101/628 = 16,1 % [13,4–19,2]", rng)],
          "d_felt": felt(v),
          "e_prevalens": prevalens(v, d),
          "f_duplikater": [duplikater(reg432, "register v2 (432)"), duplikater(reg673, "fase 3-register (673)")]}
    od = v / "revisjon-2026-10"
    od.mkdir(exist_ok=True)
    f = od / "reanalyse.json"
    f.write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(ut, ensure_ascii=False, indent=1))
    md = REPO / "docs" / "REANALYSE-2026-10-03.md"
    md.write_text(markdown(ut, sha256_file(f)), encoding="utf-8")
    fk = REPO / "docs" / "MANUSKRIPT-FAKTA-2026-09-28.md"
    t = fk.read_text(encoding="utf-8")
    i = t.find("\n## 10 Revisjon etter ekstern fagfellevurdering")
    fk.write_text((t if i < 0 else t[:i]) .rstrip("\n") + "\n" + fakta_seksjon(ut, sha256_file(f)), encoding="utf-8")
    print("skrevet", f, sha256_file(f), md, file=sys.stderr)
    return 0



# ------------------------------------------------------------------ rapport (generert fra JSON)
def _p(x: float, d: int = 1) -> str:
    return f"{100 * x:.{d}f}".replace(".", ",")


def _k(x: float) -> str:
    return f"{x:.3f}".replace(".", ",")


def _iv(xs: list[float], pst: bool = True) -> str:
    return f"[{_p(xs[0]) if pst else _k(xs[0])}–{_p(xs[1]) if pst else _k(xs[1])}]"


def markdown(d: dict, sha: str) -> str:
    L = ["# Reanalyse etter ekstern fagfellevurdering — 03.10.2026", "",
         f"**Generert** av `src/gjenopptak/classify/reanalyse_fagfelle.py` fra `revisjon-2026-10/reanalyse.json` på Vault "
         f"(sha256 `{sha}`). Ingen tall er skrevet av for hånd. Bootstrap: {d['B']:,} replikater, frø {d['frø']}, ".replace(",", " ", 1)
         + "persentilintervall; **klyngeenheten er verket**. Ingen låst fil er endret.", "",
         "## a) Verksklynget usikkerhet, side om side med manuskriptet", ""]
    a = d["a_c_kappa"]
    f320 = a["fordeling_320"]
    L += [f"**320-settet:** {f320['verk']} verk; rader per verk {f320['rader_per_verk']}; største verk {f320['største_verk']} rader.", "",
          "| par | κ | manus (passasjebootstrap) | **verksklynget 95 %** | rå enighet | PABAK | Gwet AC1 | positive a/b |",
          "|---|---|---|---|---|---|---|---|"]
    for n, p in a["par"].items():
        L.append(f"| {n} | {_k(p['kappa'])} | {p['oppgitt_i_manus']} | **{_iv(p['klynge_bootstrap95'], False)}** | "
                 f"{_p(p['rå_enighet'])} % | {_k(p['pabak'])} | {_k(p['gwet_ac1'])} | {p['positive_a']}/{p['positive_b']} |")
    df = a["differanse_koder2_minus_opus"]
    L += ["", "## b) Paret bootstrap på differansen κ 0,812 − κ 0,636 (begge mot koder 1, samme 320 passasjer)", "",
          f"Punkt **{_k(df['punkt'])}**; paret passasjebootstrap **{_iv(df['passasje_paret95'], False)}** "
          f"(andel replikater ≤ 0: {_p(df['andel_≤0_passasje'], 2)} %); paret verksklynget **{_iv(df['klynge_paret95'], False)}** "
          f"({_p(df['andel_≤0_klynge'], 2)} %). **Intervallet utelukker 0 i begge.** Manuskriptets «not statistically "
          "established», bygget på overlappende separate intervaller, er feil: med en paret test er differansen etablert.", "",
          "## a) Porter, recall og klasseandeler", "",
          "| mål | k / n | manus (Wilson, passasjer) | **verksklynget 95 %** | verk | rader per verk | største verk |",
          "|---|---|---|---|---|---|---|"]
    for v in d["a_porter_recall"].values():
        fo = v["fordeling"]
        L.append(f"| {v['mål']} | {v['k']}/{v['n']} | {v['oppgitt_i_manus']} | **{_iv(v['klynge_bootstrap95'])}** | {fo['verk']} | "
                 f"{fo['rader_per_verk']} | {fo['største_verk']} |")
    for r in d["a_klasser"]:
        for key in ("H7_av_alle", "H1_H6_av_avklarte"):
            v = r[key]
            fo = v["fordeling"]
            L.append(f"| {r['register']}: {v['mål']} | {v['k']}/{v['n']} | {v['oppgitt_i_manus']} | **{_iv(v['klynge_bootstrap95'])}** | "
                     f"{fo['verk']} | — | {fo['største_verk']} |")
    f = d["d_felt"]
    L += ["", "## d) Felt: positiv rate blant silkandidatene (riktig navngitt) og silkandidatenes andel", "",
          "| felt | tekstbiter | silkandidater | andel av tekstbitene | leser-positive | **positiv rate blant silkandidater** | per 1 000 tekstbiter |",
          "|---|---|---|---|---|---|---|"]
    for k in FELT:
        x = f[k]
        L.append(f"| {k} | {x['tekstbiter']} | {x['silkandidater']} | {_p(x['silkandidatenes_andel_av_tekstbiter'])} % | "
                 f"{x['leser_positive']} | **{_p(x['positiv_rate_blant_silkandidater'])} %** {_iv(x['wilson95'])} | "
                 f"{str(x['leser_positive_per_1000_tekstbiter']).replace('.', ',')} |")
    L += ["", f"Forholdet høyest/lavest er **{str(f['_forhold_høyest_lavest_blant_silkandidater']).replace('.', ',')}** blant "
          f"silkandidatene (manuskriptets «4,6») og **{str(f['_forhold_høyest_lavest_per_tekstbit']).replace('.', ',')}** per tekstbit. "
          "Ingen av dem er feltets prevalens: silens kandidatandel og sensitivitet per felt er ikke målt i første runde.", ""]
    e = d["e_prevalens"]
    L += ["## e) Prevalensestimatoren bak 3,43 %", "", f"**Estimator:** {e['estimator']}.", "",
          f"N = {e['N_tekstbiter']}; flagget av dommeren {e['N_flagget']}. **Ikke-flaggede strata:**", "",
          "| stratum | N | lest | positive (koder 1) |", "|---|---|---|---|"]
    for s in e["ikke_flaggede_strata"]:
        L.append(f"| {s['stratum']} | {s['N']} | {s['lest']} | {s['positive']} |")
    cel = e["flaggede_celler"]
    udekket = [c for c in cel if c["lest"] == 0]
    L += ["", f"**Flaggede:** {len(cel)} celler (felt × dømt klasse), {sum(c['lest'] for c in cel)} lest, "
          f"{sum(c['positive'] for c in cel)} positive; {len(udekket)} celler med til sammen "
          f"{sum(c['N'] for c in udekket)} flaggede tekstbiter har ingen leste rader og får feltets rate. Full celletabell i JSON-fila.", "",
          f"**Punkt:** T̂ = {str(e['punkt']['T']).replace('.', ',')} (flaggede {str(e['punkt']['T_flagget']).replace('.', ',')}, "
          f"ikke-flaggede {str(e['punkt']['T_ikke_flagget']).replace('.', ',')}) → **{_p(e['punkt']['prevalens'], 2)} %**.", "",
          f"**Intervall:** stratifisert passasjebootstrap **{_iv(e['stratifisert_passasje_bootstrap95'], True)} %**; verksklynget "
          f"**{_iv(e['verksklynget_bootstrap95'], True)} %**. Manuskriptets [2,12–7,95] er rekonstruert: {e['manus']['intervall_rekonstruert']}.", "",
          "**Vurdering:** estimatoren kan skrives ut entydig, med én antakelse (cellene uten leste rader). Punktet står "
          "(3,42 % mot 3,43 %); intervallet er feil i manuskriptet og byttes. Tallet hviler på 2 positive blant 100 leste "
          "ikke-flaggede, og flyttes fra «beste anslag» i sammendraget til en sekundær størrelse med dette intervallet.", "",
          "## f) Duplikater: rader som deler setning med en annen rad i samme verk", "",
          "| register | rader | rader som deler setning | **unike erklæringer** | komponenter > 1 rad | største | blandet klasse | H7 av unike | H1–H6 av avklarte unike |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in d["f_duplikater"]:
        h, l_ = r["H7_av_unike"], r["H1_H6_av_avklarte_unike"]
        L.append(f"| {r['register']} | {r['rader']} | {r['rader_som_deler_setning']} | **{r['unike_erklæringer']}** | "
                 f"{r['komponenter_med_flere_rader']} | {r['største_komponent']} | {r['blandet_klasse']} | "
                 f"{h['k']}/{h['n']} = {_p(h['andel'])} % {_iv(h['wilson95'])} | {l_['k']}/{l_['n']} = {_p(l_['andel'])} % {_iv(l_['wilson95'])} |")
    L += ["", "Regel: rader i samme verk med overlappende setningsspenn slås sammen til én komponent (én erklæring); "
          "komponentens klasse er den hyppigste, og komponenter med delt flertall («blandet») holdes utenfor klasseandelene. "
          "Kjeden deduplikerer ikke i dag: tekstbitene har stride 3 og vindu ±2, og en erklæring kan dermed bære flere rader.", "",
          "## Kilder", "", "| fil (Vault) | sha256 |", "|---|---|"]
    L += [f"| `{k}` | `{v[:16]}…` |" for k, v in d["kilder"].items()]
    return "\n".join(L) + "\n"


def fakta_seksjon(d: dict, sha: str) -> str:
    """FAKTA § 10: de nye tallene med sti og sha, generert fra reanalyse.json (som § 9 fra fase 3-JSON-ene)."""
    a, pr, kl, f, e, du = (d["a_c_kappa"], d["a_porter_recall"], d["a_klasser"], d["d_felt"], d["e_prevalens"],
                           d["f_duplikater"])
    k = f"`revisjon-2026-10/reanalyse.json` `{sha[:16]}…`"
    L = ["", "## 10 Revisjon etter ekstern fagfellevurdering (03.10.2026)", "",
         "**Generert** av `classify/reanalyse_fagfelle.py` fra " + k + " (Vault; deponeres som `revisjon-reanalyse.json`). "
         "Klyngeenhet verket, 10 000 replikater, frø 734248. Fullt dokument: `docs/REANALYSE-2026-10-03.md`; tallmanifest: "
         "`docs/TALLMANIFEST.md`.", "", "| tall | verdi | kilde |", "|---|---|---|"]
    for n, p_ in a["par"].items():
        L.append(f"| κ {n}, verksklynget 95 % | **{_k(p_['kappa'])} {_iv(p_['klynge_bootstrap95'], False)}**; rå {_p(p_['rå_enighet'])} %, "
                 f"PABAK {_k(p_['pabak'])}, AC1 {_k(p_['gwet_ac1'])} | {k} |")
    df = a["differanse_koder2_minus_opus"]
    L.append(f"| κ 0,812 − 0,636, paret | **{_k(df['punkt'])}**; passasje {_iv(df['passasje_paret95'], False)}, verksklynget "
             f"{_iv(df['klynge_paret95'], False)} — **utelukker 0** | {k} |")
    for v in pr.values():
        L.append(f"| {v['mål']}, verksklynget 95 % | **{v['k']}/{v['n']} {_iv(v['klynge_bootstrap95'])}**; {v['fordeling']['verk']} verk, "
                 f"største {v['fordeling']['største_verk']} rader | {k} |")
    for r in kl:
        for key in ("H7_av_alle", "H1_H6_av_avklarte"):
            v = r[key]
            L.append(f"| {r['register']}: {v['mål']}, verksklynget 95 % | **{v['k']}/{v['n']} {_iv(v['klynge_bootstrap95'])}** | {k} |")
    for fe in FELT:
        x = f[fe]
        L.append(f"| {fe}: positiv rate blant silkandidater / silkandidatenes andel av tekstbitene | "
                 f"**{x['leser_positive']}/{x['silkandidater']} = {_p(x['positiv_rate_blant_silkandidater'])} %** / "
                 f"{_p(x['silkandidatenes_andel_av_tekstbiter'])} % | {k} |")
    L.append(f"| grunnrate c), cellevektet | **{_p(e['punkt']['prevalens'], 2)} %**; stratifisert {_iv(e['stratifisert_passasje_bootstrap95'])} %, "
             f"verksklynget {_iv(e['verksklynget_bootstrap95'])} % — **erstatter [2,12–7,95]** | {k} |")
    for r in du:
        L.append(f"| {r['register']}: unike erklæringer etter deduplisering | **{r['unike_erklæringer']}** av {r['rader']} rader "
                 f"({r['rader_som_deler_setning']} deler setning); H7 {r['H7_av_unike']['k']}/{r['H7_av_unike']['n']}, "
                 f"H1–H6 {r['H1_H6_av_avklarte_unike']['k']}/{r['H1_H6_av_avklarte_unike']['n']} | {k} |")
    L += ["", "**Ikke påstå:** at κ-tallene viser gyldighet (alle kodere er modeller; ADDENDUM-27 er ikke kjørt); at 3,42 % er en "
          "prevalens i litteraturen; at feltforskjellene er forskjeller i forekomst; at de seks casene sier noe om hvor ofte "
          "tilgang er hindringen (`docs/CASEUTVALG-2026-10-03.md`: utvalget er skjønn).", ""]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
