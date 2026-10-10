"""ADDENDUM-28: tredje koder på lokal ollama (``gemma2:9b``) over portens 320.

    PYTHONPATH=src python -m gjenopptak.classify.tredje_koder kanari
    PYTHONPATH=src python -m gjenopptak.classify.tredje_koder kjør
    PYTHONPATH=src python -m gjenopptak.classify.tredje_koder mål

Alt som styrer kjøringen står i ``OPPSETT`` og er låst av ADDENDUM-28 med sha256. Alle datafiler
leses fra Vault, og utdata går til Vault (``tredje-koder-ADDENDUM-28/``).

**Sperrelisten er bygget inn i rekkefølgen.** ``kanari`` og ``kjør`` åpner bare blindfilen,
regelfilen, instruksen og vekten. Koder 1 og koder 2 åpnes først av ``mål``, og ``mål`` nekter før
``kjør`` har skrevet ``dommer.jsonl`` og forseglet den med sha256 i ``SEGL.json``.

**Hva som ikke gjøres:** ingen omkjøring av et parti (temp 0 og fast frø gir samme svar), ingen
utfylling av ugyldige dommer, ingen ny instruks eller partistørrelse etter første parti.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from ..kjede.leser import LokalLeser, partimelding, sha256_blob, sha256_tekst
from ..vault import require_vault, sha256_file
from .reanalyse_fagfelle import B, FRØ, _pct, boot_kappa, enighet

REPO = Path(__file__).resolve().parents[3]

OPPSETT = {
    "addendum": 28,
    "modell": "gemma2:9b",
    "vekt_sha256": "ff1d1fc78170d787ee1201778e2dd65ea211654ca5fb7d69b5a2e7b123a50373",
    "instruks": "prompts/leser-lokal-v1.txt",                           # relativ til repoet
    "instruks_sha256": "6dc74bbca307a24186b49b257210df58e06c19e9e9b6e70d8c437111d02a6137",
    # Alt under er relativt til Vault (gjenopptak-kilder/).
    "regelfil": "koder2/koderegler-gjenvunnet.md",
    "regelfil_sha256": "234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449",
    "blindfil": "presisjonssett/port-presisjonssett-blind.jsonl",
    "blindfil_sha256": "15ce72a7687cea57ac1e7f774aa0303f0bedfc3c2867244d24173a1ec211d4a5",
    "koder1": "presisjonssett/port-presisjonssett-ADDENDUM10.jsonl",
    "koder1_sha256": "6a04079c31fbbc60a8a189232a7ef37f55756ce18c74545d10bf062fcea70c36",
    "koder2": "presisjonssett/port-presisjonssett-verdikter-koder2.jsonl",
    "koder2_sha256": "7852f8623134709987a499edf142e3a87ce9c300fea861369a7917cce9d1bd0f",
    "parti": 5,
    "num_ctx": 8192,
    "num_predict": 2048,
    "temperatur": 0,
    "frø": FRØ,
    "keep_alive": 0,            # modellen lastes ut etter hvert kall: ingen hurtigbuffer mellom partier
    "kanari_id": "KANARI",
    "kanari_tekst": "We could not date the layer, because no suitable sample was preserved.",
    "utdir": "tredje-koder-ADDENDUM-28",
    "kontroll_kappa_k1_k2_320": 0.8124,     # revisjon-2026-10/reanalyse.json
}

#: Filene ``kanari`` og ``kjør`` aldri åpner (relativt til Vault). Datafilene i koder 2s sperreliste
#: (oppdrag-gjenvunnet/oppdrag-koder2-ADDENDUM-11.md) slik de ligger på Vault, pluss alt som er
#: kodet på de samme 320 siden. Modellen selv har ingen filtilgang; listen binder koden og den som kjører.
SPERRET = (
    "presisjonssett/port-presisjonssett-ADDENDUM10.jsonl",
    "presisjonssett/port-presisjonssett-verdikter-koder2.jsonl",
    "presisjonssett/port-presisjonssett-verdikter.jsonl",
    "presisjonssett/port-presisjonssett-nokkel.jsonl",
    "presisjonssett/port-presisjonssett.jsonl",
    "presisjonssett/port-tvil.jsonl",
    "presisjonssett/koder2-sammenlikning.json",
    "presisjonssett/koder2-sammenlikning-uten-tekst.json",
    "presisjonssett-2026-09-20/",
    "koder4/",
    "leser-lokal-ADDENDUM-24/",
    "ekstraksjon/2026-09-26/addendum-18/",
    "ekstraksjon/2026-09-26/addendum-19/",
    "ekstraksjon/2026-09-26/addendum-20/",
    "revisjon-2026-10/menneskevalidering/nokkel.jsonl",
    "revisjon-2026-10/reanalyse.json",
)

FLAGGET = ("treff",)                       # utvalgstype: dommeren (samme vekt) flagget passasjen
IKKE_FLAGGET = ("ingen", "n1n2", "n3")
ANKRE = ("anker-treff", "anker-ikke-treff")


def _vekt_blob(digest: str) -> Path:
    return Path.home() / ".ollama" / "models" / "blobs" / f"sha256-{digest}"


def _jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def _nå() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _skriv(p: Path, obj) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _ollama(leser: LokalLeser) -> dict:
    """Versjon og lastede modeller. En annen lastet modell stopper kjøringen: 16 GB samlet minne."""
    import httpx
    with httpx.Client(timeout=30) as c:
        versjon = c.get(f"{leser.vert}/api/version").json().get("version")
        lastet = [m.get("name") for m in c.get(f"{leser.vert}/api/ps").json().get("models", [])]
    andre = [m for m in lastet if m != OPPSETT["modell"]]
    if andre:
        raise SystemExit(f"STOPP — andre modeller er lastet i ollama: {', '.join(andre)}")
    return {"ollama_versjon": versjon}


def forutsetninger() -> tuple[Path, str, list[dict], LokalLeser]:
    """Verifiser alt som er låst før noe kjøres. Ett avvik stopper. Åpner ingen sperret fil."""
    v = require_vault()
    avvik = []
    blob = _vekt_blob(OPPSETT["vekt_sha256"])
    if not blob.is_file() or sha256_blob(blob) != OPPSETT["vekt_sha256"]:
        avvik.append(f"vekten {OPPSETT['modell']} stemmer ikke med {OPPSETT['vekt_sha256'][:16]}…")
    rf, bf, inf = v / OPPSETT["regelfil"], v / OPPSETT["blindfil"], REPO / OPPSETT["instruks"]
    for navn, sti in (("regelfil", rf), ("blindfil", bf), ("instruks", inf)):
        if not sti.is_file() or sha256_file(sti) != OPPSETT[f"{navn}_sha256"]:
            avvik.append(f"{navn}en har endret sha256 eller mangler")
    if avvik:
        raise SystemExit("STOPP — " + "; ".join(avvik))
    leser = LokalLeser(modell=OPPSETT["modell"], vekt_sha256=OPPSETT["vekt_sha256"],
                       instruks=inf.read_text(encoding="utf-8"), num_ctx=OPPSETT["num_ctx"],
                       temperatur=OPPSETT["temperatur"], frø=OPPSETT["frø"],
                       num_predict=OPPSETT["num_predict"], keep_alive=OPPSETT["keep_alive"])
    return v, rf.read_text(encoding="utf-8"), _jsonl(bf), leser


def partier(blind: list[dict]) -> list[list[dict]]:
    n = OPPSETT["parti"]
    return [blind[i:i + n] for i in range(0, len(blind), n)]


def vindusbrudd(bruk: dict) -> list[str]:
    """Grunnene til at et helt parti er ugyldig. Tom liste = partiet fikk plass og ble ferdig.

    Vinduet rommer ledetekst *og* svar. Når summen når ``num_ctx``, kan ollama ha kastet starten av
    ledeteksten — der reglene står — og fortsatt å skrive; da er dommene avsagt uten regelfilen.
    """
    grunner = []
    inn, ut = bruk.get("prompt_eval_count"), bruk.get("eval_count")
    if inn is None or ut is None:
        grunner.append("tokentall mangler i svaret")
    elif inn + ut >= OPPSETT["num_ctx"]:
        grunner.append(f"vinduet fullt: {inn} inn + {ut} ut >= {OPPSETT['num_ctx']}")
    if bruk.get("done_reason") != "stop":
        grunner.append(f"done_reason = {bruk.get('done_reason')}")
    if bruk.get("parsefeil"):
        grunner.append("svaret parser ikke")
    return grunner


def signatur(leser: LokalLeser, regler: str, parti: list[dict], nr: int, av: int, bruk: dict,
             miljø: dict) -> dict:
    """Alt som skal til for å gjenta nøyaktig dette kallet. Bæres av hver dom i ``dommer.jsonl``."""
    return {"addendum": OPPSETT["addendum"], **leser.signatur(), "keep_alive": OPPSETT["keep_alive"],
            "regelfil_sha256": OPPSETT["regelfil_sha256"], "blindfil_sha256": OPPSETT["blindfil_sha256"],
            "kode_sha256": sha256_file(Path(__file__)), **miljø,
            "parti": nr, "partier": av, "parti_ids": [r["id"] for r in parti],
            "system_sha256": sha256_tekst(f"{leser.instruks}\n\n# REGLENE\n\n{regler}"),
            "bruker_sha256": sha256_tekst(partimelding(parti, nr, av)),
            "råsvar_sha256": bruk.get("råsvar_sha256"), "prompt_eval_count": bruk.get("prompt_eval_count"),
            "eval_count": bruk.get("eval_count"), "done_reason": bruk.get("done_reason")}


def kanari() -> int:
    """Største parti + kanarisetningen sist. Bestått: vinduet rommet ledetekst og svar, og kanarien
    har en gyldig dom. Kanariens klasse kreves ikke — det ville målt koderens kvalitet."""
    v, regler, blind, leser = forutsetninger()
    miljø = _ollama(leser)
    største = max(partier(blind), key=lambda p: sum(len(r["tekst"]) for r in p))
    prøve = største + [{"id": OPPSETT["kanari_id"], "tekst": OPPSETT["kanari_tekst"]}]
    sist = partimelding(prøve, 0, 0).rstrip().endswith(OPPSETT["kanari_tekst"])
    l = leser(regler, prøve, nr=0, av=0)
    brudd = vindusbrudd(l.bruk)
    ok = sist and not brudd and OPPSETT["kanari_id"] not in l.ugyldige
    b = l.bruk
    ut = {"bestått": ok, "tid": _nå(), "kanari_sist_i_vinduet": sist, "vindusbrudd": brudd,
          "parti_ids": [r["id"] for r in største], "parti_tegn": sum(len(r["tekst"]) for r in største),
          "prompt_eval_count": b.get("prompt_eval_count"), "eval_count": b.get("eval_count"),
          "num_ctx": OPPSETT["num_ctx"],
          "vindusfylling": round(((b.get("prompt_eval_count") or 0) + (b.get("eval_count") or 0))
                                 / OPPSETT["num_ctx"], 3),
          "done_reason": b.get("done_reason"), "gyldige": len(l.dommer), "ugyldige": l.ugyldige,
          "kanari_dom": next((d for d in l.dommer if d["id"] == OPPSETT["kanari_id"]), None),
          "sekunder": b.get("sekunder"), "råsvar": b.get("råsvar"),
          "signatur": signatur(leser, regler, prøve, 0, 0, b, miljø)}
    d = v / OPPSETT["utdir"]
    d.mkdir(parents=True, exist_ok=True)
    _skriv(d / "kanari.json", ut)
    print(json.dumps({k: ut[k] for k in ut if k not in ("parti_ids", "signatur", "råsvar")}, ensure_ascii=False))
    return 0 if ok else 2


def kjør() -> int:
    v, regler, blind, leser = forutsetninger()
    d = v / OPPSETT["utdir"]
    if (d / "SEGL.json").is_file():
        raise SystemExit("STOPP — kjøringen er alt forseglet (SEGL.json finnes); ingen omkjøring")
    if not (d / "kanari.json").is_file() or not json.loads((d / "kanari.json").read_text())["bestått"]:
        raise SystemExit("STOPP — kanarien er ikke bestått")
    miljø = _ollama(leser)
    ps = partier(blind)
    t0 = time.time()
    for i, p in enumerate(ps, 1):
        f = d / f"parti-{i:02d}.json"
        if f.is_file():
            print(f"parti {i}: finnes, hopper over (ingen omkjøring)")
            continue
        l = leser(regler, p, nr=i, av=len(ps))
        brudd = vindusbrudd(l.bruk)
        _skriv(f, {"parti": i, "ids": [r["id"] for r in p], "dommer": l.dommer, "ugyldige": l.ugyldige,
                   "vindusbrudd": brudd, "bruk": l.bruk, "tid": _nå(),
                   "signatur": signatur(leser, regler, p, i, len(ps), l.bruk, miljø)})
        print(f"parti {i}/{len(ps)}: {len(l.dommer)} gyldige, {len(l.ugyldige)} ugyldige, "
              f"inn {l.bruk.get('prompt_eval_count')}, ut {l.bruk.get('eval_count')}, "
              f"{l.bruk.get('done_reason')}, {l.bruk.get('sekunder')} s"
              + (f" — PARTIET UGYLDIG: {'; '.join(brudd)}" if brudd else ""), flush=True)
    if sha256_blob(_vekt_blob(OPPSETT["vekt_sha256"])) != OPPSETT["vekt_sha256"]:
        raise SystemExit("STOPP — vekten endret seg under kjøringen")
    forsegl(d, blind)
    print(f"ferdig og forseglet, {round((time.time() - t0) / 60, 1)} min")
    return 0


def forsegl(d: Path, blind: list[dict]) -> dict:
    """Én rad per passasje, i blindfilens rekkefølge, med signatur per dom. Deretter sha256 i SEGL.json.

    En passasje er gyldig bare når partiet er uten vindusbrudd og dommen selv er gyldig.
    """
    rader = []
    for i, p in enumerate(partier(blind), 1):
        parti = json.loads((d / f"parti-{i:02d}.json").read_text(encoding="utf-8"))
        dom = {x["id"]: x for x in parti["dommer"]}
        for r in p:
            grunn = "; ".join(parti["vindusbrudd"]) or (None if r["id"] in dom else "ingen gyldig dom i svaret")
            rader.append({"id": r["id"], "gyldig": grunn is None, "ugyldig_grunn": grunn,
                          "dom": dom.get(r["id"]) if grunn is None else None,
                          "dom_forkastet": dom.get(r["id"]) if grunn is not None else None,
                          "tekst_sha256": sha256_tekst(r["tekst"]), "tid": parti["tid"],
                          "signatur": parti["signatur"]})
    f = d / "dommer.jsonl"
    f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rader), encoding="utf-8")
    segl = {"fil": "dommer.jsonl", "sha256": sha256_file(f), "rader": len(rader),
            "gyldige": sum(r["gyldig"] for r in rader), "forseglet": _nå(),
            "vekt_verifisert_etter": OPPSETT["vekt_sha256"]}
    _skriv(d / "SEGL.json", segl)
    return segl


# ------------------------------------------------------------------ måling
def _par(a: dict, b: dict, ids: list[str], verk: dict) -> dict:
    """κ med rå enighet, PABAK og Gwets AC1, og verksklynget intervall (passasjenivå ved siden av)."""
    if not ids:
        return {"n": 0}
    rader = [(verk[i], a[i], b[i]) for i in ids]
    return {**enighet([r[1] for r in rader], [r[2] for r in rader]), "verk": len({r[0] for r in rader}),
            "klynge_bootstrap95": _pct(boot_kappa(rader, klynge=True, rng=random.Random(FRØ))),
            "passasje_bootstrap95": _pct(boot_kappa(rader, klynge=False, rng=random.Random(FRØ)))}


def _differanse(p: tuple[dict, dict], q: tuple[dict, dict], ids: list[str], verk: dict) -> dict:
    """κ(p) − κ(q) på de samme passasjene, paret verksklynget bootstrap: samme verk i begge ledd."""
    if not ids:
        return {"n": 0}
    per = defaultdict(list)
    for i in ids:
        per[verk[i]].append(i)
    navn = sorted(per)

    def diff(utvalg: list[str]) -> float:
        return (enighet([p[0][i] for i in utvalg], [p[1][i] for i in utvalg])["kappa"]
                - enighet([q[0][i] for i in utvalg], [q[1][i] for i in utvalg])["kappa"])
    rng = random.Random(FRØ)
    kly = [diff([i for w in (rng.choice(navn) for _ in navn) for i in per[w]]) for _ in range(B)]
    return {"n": len(ids), "punkt": round(diff(ids), 4), "klynge_paret95": _pct(kly),
            "andel_≤0_klynge": round(sum(x <= 0 for x in kly) / len(kly), 4)}


def _tre(g: dict, k1: dict, k2: dict, ids: list[str], verk: dict) -> dict:
    """De tre låste utfallene på samme delmengde, og de to differansene."""
    return {"n": len(ids),
            "gemma2_mot_koder1": _par(g, k1, ids, verk),
            "gemma2_mot_koder2": _par(g, k2, ids, verk),
            "koder1_mot_koder2": _par(k1, k2, ids, verk),
            "differanse_k1k2_minus_gemma2k1": _differanse((k1, k2), (g, k1), ids, verk),
            "differanse_k1k2_minus_gemma2k2": _differanse((k1, k2), (g, k2), ids, verk)}


def mål() -> int:
    v = require_vault()
    d = v / OPPSETT["utdir"]
    if not (d / "SEGL.json").is_file():
        raise SystemExit("STOPP — kjøringen er ikke forseglet; koder 1 og koder 2 åpnes ikke før den er det")
    segl = json.loads((d / "SEGL.json").read_text(encoding="utf-8"))
    if sha256_file(d / "dommer.jsonl") != segl["sha256"]:
        raise SystemExit("STOPP — dommer.jsonl stemmer ikke med seglet")
    for navn in ("koder1", "koder2"):
        if sha256_file(v / OPPSETT[navn]) != OPPSETT[f"{navn}_sha256"]:
            raise SystemExit(f"STOPP — {navn} har endret sha256")
    rader = _jsonl(d / "dommer.jsonl")
    r1 = {r["id"]: r for r in _jsonl(v / OPPSETT["koder1"])}
    ids = [r["id"] for r in rader]
    if set(ids) != set(r1) or len(ids) != len(r1):
        raise SystemExit("STOPP — dommer.jsonl og koder 1 dekker ikke de samme id-ene")
    k1 = {i: bool(r1[i]["ekte_treff"]) for i in ids}
    k2 = {r["id"]: bool(r["ekte_treff"]) for r in _jsonl(v / OPPSETT["koder2"])}
    verk = {i: r1[i]["doc_id"] for i in ids}
    type_ = {i: r1[i]["utvalgstype"] for i in ids}
    dom = {r["id"]: r["dom"] for r in rader if r["gyldig"]}
    g = {i: bool(x["ekte_treff"]) for i, x in dom.items()}
    D = [i for i in ids if i in g]                         # delmengden: gyldig dom fra gemma2
    if not D:
        raise SystemExit("STOPP — ingen gyldige dommer; det finnes ingen delmengde å måle på")
    alle = _par(k1, k2, ids, verk)
    res = {
        "addendum": OPPSETT["addendum"], "tid": _nå(), "frø": FRØ, "B": B, "klyngeenhet": "verk (doc_id)",
        "innfiler": {"dommer.jsonl": segl["sha256"], OPPSETT["koder1"]: OPPSETT["koder1_sha256"],
                     OPPSETT["koder2"]: OPPSETT["koder2_sha256"]},
        "kode_sha256": sha256_file(Path(__file__)),
        "gyldige": len(D), "ugyldige": [r["id"] for r in rader if not r["gyldig"]],
        "ugyldig_grunner": dict(Counter(r["ugyldig_grunn"] for r in rader if not r["gyldig"])),
        "utfall": _tre(g, k1, k2, D, verk),
        "kontroll_koder1_mot_koder2_alle_320": {
            **alle, "ventet_kappa": OPPSETT["kontroll_kappa_k1_k2_320"],
            "stemmer": alle["kappa"] == OPPSETT["kontroll_kappa_k1_k2_320"]},
        # Ugyldige dommer satt til én og samme verdi, begge veier — ingen koder er favorisert.
        "følsomhet_ugyldige": {
            navn: {"gemma2_mot_koder1": _par({**{i: verdi for i in ids}, **g}, k1, ids, verk),
                   "gemma2_mot_koder2": _par({**{i: verdi for i in ids}, **g}, k2, ids, verk)}
            for navn, verdi in (("alle_treff", True), ("ingen_treff", False))} if len(D) < len(ids) else None,
        # Utvalget er stratifisert på dommerens dommer, og dommeren er samme vekt som koder 3.
        "etter_dommerens_flagg": {
            "flagget": _tre(g, k1, k2, [i for i in D if type_[i] in FLAGGET], verk),
            "ikke_flagget": _tre(g, k1, k2, [i for i in D if type_[i] in IKKE_FLAGGET], verk),
            "treff_per_utvalgstype": {
                t: {"n": sum(type_[i] == t for i in D), "gemma2": sum(g[i] for i in D if type_[i] == t),
                    "koder1": sum(k1[i] for i in D if type_[i] == t),
                    "koder2": sum(k2[i] for i in D if type_[i] == t)}
                for t in FLAGGET + IKKE_FLAGGET + ANKRE}},
        "mønster_gemma2_koder1_koder2": dict(sorted(Counter(
            f"{int(g[i])}{int(k1[i])}{int(k2[i])}" for i in D).items())),
        "klasser_gemma2": dict(Counter(x["min_klasse"] for x in dom.values()).most_common()),
        "inkonsistente": sorted(i for i, x in dom.items() if x["ekte_treff"] != x["min_klasse"].startswith("H")),
        "tokens_inn": 0, "tokens_ut": 0, "sekunder": 0.0, "done_reason": [],
    }
    bruk = [json.loads(f.read_text(encoding="utf-8"))["bruk"] for f in sorted(d.glob("parti-*.json"))]
    res["tokens_inn"] = sum(b.get("prompt_eval_count") or 0 for b in bruk)
    res["tokens_ut"] = sum(b.get("eval_count") or 0 for b in bruk)
    res["sekunder"] = round(sum(b.get("sekunder") or 0 for b in bruk), 1)
    res["done_reason"] = sorted({str(b.get("done_reason")) for b in bruk})
    _skriv(d / "maaling.json", res)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("kommando", choices=("kanari", "kjør", "mål"))
    a = p.parse_args(argv)
    return {"kanari": kanari, "kjør": kjør, "mål": mål}[a.kommando]()


if __name__ == "__main__":
    sys.exit(main())
