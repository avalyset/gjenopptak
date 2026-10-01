"""Fase 3 (ADDENDUM-25): referansesett, nøkkelsikring, presisjonsport og recall.

    PYTHONPATH=src python -m gjenopptak.classify.fase3 referansetekst
    PYTHONPATH=src python -m gjenopptak.classify.fase3 referanseoppdrag
    PYTHONPATH=src python -m gjenopptak.classify.fase3 sikre-nokkel
    PYTHONPATH=src python -m gjenopptak.classify.fase3 presisjon-bygg --kjoring fase3-kjede
    PYTHONPATH=src python -m gjenopptak.classify.fase3 maal --kjoring fase3-kjede

**Referansesettet bygges før silen og leseren kjøres.** Hvert av de 20 verkene skrives ut som
nummererte setninger med *samme parser* som kjeden (``parse.sentences_from_jats`` /
``pdfroute.sentences_from_pdf``), slik at setningsnummeret er det samme som tekstbitenes
``start_index``/``end_index``. En CC-underinstans med tom kontekst leser hele verket og noterer hvert
treff som setningsnumrene treffet består av.

**Beholdt og bekreftet, låst i ADDENDUM-25 § 5:** et referansetreff er *beholdt* av silen hvis en
tekstbit i unionen fra samme verk dekker **alle** setningsnumrene treffet består av; *bekreftet* hvis
minst én slik tekstbit fikk ``treff: true`` av leseren.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from ..vault import require_vault, sha256_file

REPO = Path(__file__).resolve().parents[3]
UT = "fase3"
FRØ = 734248
N_PRESISJON = 100
REGELFIL = "koder2/koderegler-gjenvunnet.md"
REGELFIL_SHA256 = "234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449"
MAKS_SPENN = 5                      # ±2 setninger: passasjeenheten (ADDENDUM-03 § 1.2)


def nå() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def setninger(v: Path, rad: dict, tmp: Path) -> list[dict]:
    from ..parse import sentences_from_jats
    from ..parse.pdfroute import sentences_from_pdf
    b = (v / rad["fil"]).read_bytes()
    if hashlib.sha256(b).hexdigest() != rad["sha256"]:
        raise SystemExit(f"{rad['work_id']}: sha256 avviker fra utvalget")
    return (sentences_from_jats(b, doc_id=rad["work_id"]) if rad["port_ledd"] == "P1-JATS"
            else sentences_from_pdf(b, doc_id=rad["work_id"], tmp_dir=tmp))


def referansetekst() -> int:
    v = require_vault()
    ut = v / UT
    ref = json.loads((ut / "referanse-verk.json").read_text(encoding="utf-8"))["verk"]
    utv = {r["work_id"]: r for r in _jsonl(ut / "utvalg-fase3-arkeologi.jsonl")}
    td = ut / "referanse" / "tekst"
    td.mkdir(parents=True, exist_ok=True)
    tmp = REPO / "data" / "tmp-fase3"
    tmp.mkdir(parents=True, exist_ok=True)
    rader = []
    for i, wid in enumerate(ref, 1):
        rows = setninger(v, utv[wid], tmp)
        f = td / f"R{i:02d}.txt"
        f.write_text("\n".join(f"S{r['sentence_index']}: {r['text']}" for r in rows) + "\n",
                     encoding="utf-8")
        rader.append({"ref": f"R{i:02d}", "work_id": wid, "setninger": len(rows),
                      "tegn": sum(len(r["text"]) for r in rows), "fil": f.name, "sha256": sha256_file(f)})
        print(f"R{i:02d} {wid}: {len(rows)} setninger")
    (ut / "referanse" / "tekster.json").write_text(json.dumps(rader, ensure_ascii=False, indent=1) + "\n",
                                                   encoding="utf-8")
    return 0


OPPDRAG = """# Oppdrag: les ett verk fra perm til perm, og noter hvert treff

Du er en uavhengig koder i en preregistrert studie. **Alt du skriver skal være på norsk (bokmål).**

**Din egen kladdekatalog**, som ingen annen instans bruker — legg alle hjelpefiler der og ingen andre steder:
`{KLADD}`

## Oppgaven

Les **hele** verket i tekstfilen under, fra første til siste setning, og noter **hver passasje** som inneholder
et **parkert spørsmål** slik studiens regler definerer det. Tekstfilen har én setning per linje, på formen
`S<nummer>: <tekst>`.

Du får ingen opplysning om hvor mange treff verket har, om hvordan det er valgt, eller om hva noen andre har
ment om det. Ikke forsøk å utlede det.

## De eneste to filene du får lese

1. **Reglene:** `{REGLER}`
2. **Verket:** `{TEKST}` — {N} setninger

Reglene er den eneste kilden. Står svaret ikke der, skal du ikke gjette deg til det fra annet materiale.

**Les verket i biter på høyst 200 linjer**, i rekkefølge (Read med `offset` og `limit`), til og med siste
linje. Ikke søk i teksten etter ord for å finne kandidater — les den.

**Merk om regelfilen:** utdraget fra ADDENDUM-05 i den er limt inn som `grep -n`-utdata, så noen linjer
bærer linjenummer og skilletegn, og tabellen over uavklarte naboparer er avkuttet etter tabellhodet. Det
er kjent og skal ikke rettes. Bruk bare de uavklart-verdiene reglene faktisk navngir.

## STRENGT FORBUDT å åpne, grep-e, cat-e eller på annen måte inspisere

Alt i repoet `{REPO}` og alt på `{VAULT}` **unntatt de to filene over** — særlig andre tekstfiler under
`{UT}/referanse/`, alt annet under `{UT}/`, `data/kjede/`, alle ADDENDUM-filer, `PREREG-v1.md`, `docs/`, og
alle verdikt-, nøkkel- og blindfiler. `git log`, `git show`, `git diff` og `git blame` er forbudt. Ingen
nettverkstilgang.

## Hva et treff er her

Et treff er et parkert spørsmål etter reglene: noe som ikke ble gjort **og** en navngitt hindring, knyttet
til hverandre, og det ugjorte tilhører undersøkelsen verket rapporterer. **Begge delene må ligge innenfor
{MAKS} påfølgende setninger** — det er studiens passasjeenhet (±2 setninger). Et ugjort og en hindring som står
lenger fra hverandre, er ikke ett treff.

## Utdata

Skriv **én JSON-linje per treff**, i den rekkefølgen du finner dem, til `{UTFIL}`:

```json
{{"work_id": "{WID}", "ref": "{REF}", "setninger": [412, 413], "klasse": "H7", "tvil": false,
 "begrunnelse": "én setning som navngir det ugjorte og hindringen"}}
```

* `setninger` — **numrene på setningene treffet består av**: setningen(e) med det ugjorte og setningen(e)
  med hindringen. Høyeste minus laveste skal være høyst {MAKS1}.
* `klasse` — H1–H9, eller `H1/H7-uavklart` der reglene gir den verdien.
* `tvil` — `true` hvis du var i reell tvil om at det er et treff.

Skriv linjene fortløpende og flush underveis. Har verket ingen treff, skriv filen tom (0 linjer) — **filen
skal finnes uansett**. Ikke skriv noe annet til den filen.

## Sluttrapport

Kort: antall setninger lest (første og siste nummer), antall treff, fordeling på klasse, og **en uttrykkelig
bekreftelse på at ingen av de forbudte filene ble åpnet**. Les hele verket. Ikke stopp før siste setning.
"""


def referanseoppdrag() -> int:
    v = require_vault()
    ut = v / UT
    tekster = json.loads((ut / "referanse" / "tekster.json").read_text(encoding="utf-8"))
    od = ut / "referanse" / "oppdrag"
    od.mkdir(parents=True, exist_ok=True)
    (ut / "referanse" / "treff").mkdir(parents=True, exist_ok=True)
    for t in tekster:
        o = OPPDRAG.format(
            KLADD=ut / "referanse" / "kladd" / t["ref"], REGLER=v / REGELFIL,
            TEKST=ut / "referanse" / "tekst" / t["fil"], N=t["setninger"], REPO=REPO, VAULT=v, UT=UT,
            MAKS=MAKS_SPENN, MAKS1=MAKS_SPENN - 1, WID=t["work_id"], REF=t["ref"],
            UTFIL=ut / "referanse" / "treff" / f"{t['ref']}.jsonl")
        (od / f"oppdrag-{t['ref']}.md").write_text(o, encoding="utf-8")
    print(f"{len(tekster)} oppdrag i {od}")
    return 0


MODELL = "claude-opus-5"


def referanse_les() -> int:
    """Én ``claude -p``-instans per verk, serielt. Arbeidskatalogen er kladden på Vault, **utenfor
    repoet**: en instans startet i repoet får git-status og ferske commit-emner i systemprompten.
    Ingen MCP-servere. Ferdige verk (treffil + bruk uten feil) leses ikke om."""
    import subprocess
    import time
    v = require_vault()
    ut = v / UT
    tekster = json.loads((ut / "referanse" / "tekster.json").read_text(encoding="utf-8"))
    bd = ut / "referanse" / "bruk"
    bd.mkdir(parents=True, exist_ok=True)
    for t in tekster:
        ref = t["ref"]
        treff, bruk = ut / "referanse" / "treff" / f"{ref}.jsonl", bd / f"{ref}.json"
        if treff.is_file() and bruk.is_file() and not json.loads(bruk.read_text()).get("is_error"):
            print(f"{ref}: ferdig, hopper over")
            continue
        kladd = ut / "referanse" / "kladd" / ref
        kladd.mkdir(parents=True, exist_ok=True)
        oppdrag = (ut / "referanse" / "oppdrag" / f"oppdrag-{ref}.md").read_text(encoding="utf-8")
        t0 = time.time()
        r = subprocess.run(["claude", "-p", "--model", MODELL, "--output-format", "json",
                            "--permission-mode", "acceptEdits", "--strict-mcp-config",
                            "--add-dir", str(v)], cwd=kladd, capture_output=True, text=True,
                           timeout=7200, input=oppdrag)
        try:
            svar = json.loads(r.stdout)
        except ValueError:
            svar = {"is_error": True, "result": "kunne ikke lese JSON", "stderr": r.stderr[-400:]}
        rad = {"ref": ref, "work_id": t["work_id"], "modell": MODELL, "start": nå(),
               "minutter": round((time.time() - t0) / 60, 1), "is_error": svar.get("is_error"),
               "usage": svar.get("usage"), "modelUsage": svar.get("modelUsage"),
               "num_turns": svar.get("num_turns"), "total_cost_usd": svar.get("total_cost_usd"),
               "resultat": str(svar.get("result"))[:1500],
               "treffil_finnes": treff.is_file(),
               "treff": len(_jsonl(treff)) if treff.is_file() else None}
        bruk.write_text(json.dumps(rad, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{ref} {t['work_id']}: {rad['treff']} treff, {rad['minutter']} min, feil={rad['is_error']}",
              flush=True)
        if rad["is_error"] or not treff.is_file():
            print(f"STOPP ved {ref}: økten feilet eller skrev ingen treffil", file=sys.stderr)
            return 2
    return 0


def sikre_nokkel() -> int:
    """Samle referansetreffene til én nøkkel, sha256 i manifestet, ots-stempel. Før silen."""
    from ..tidsstempel import stamp
    v = require_vault()
    ut = v / UT
    tekster = json.loads((ut / "referanse" / "tekster.json").read_text(encoding="utf-8"))
    rader, mangler = [], []
    for t in tekster:
        f = ut / "referanse" / "treff" / f"{t['ref']}.jsonl"
        if not f.is_file():
            mangler.append(t["ref"])
            continue
        for r in _jsonl(f):
            s = sorted(int(x) for x in r["setninger"])
            rader.append({**r, "work_id": t["work_id"], "ref": t["ref"], "setninger": s,
                          "gyldig_spenn": (s[-1] - s[0]) <= MAKS_SPENN - 1 if s else False})
    if mangler:
        raise SystemExit(f"STOPP — mangler treffil for {mangler}; nøkkelen sikres ikke ufullstendig")
    nf = ut / "referanse" / "NOKKEL-referansesett.jsonl"
    if nf.exists():
        raise SystemExit("nøkkelen finnes alt — skrives ikke om")
    nf.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rader), encoding="utf-8")
    sha = sha256_file(nf)
    st = stamp(nf, ut_dir=ut / "referanse" / "ots")
    with (v / "MANIFEST-VAULT.md").open("a", encoding="utf-8") as fh:
        fh.write(f"\n## Fase 3: referansenøkkel sikret før silen, {nå()}\n\n"
                 f"| sti | bytes | sha256 | sikret | kilde-URL | merknad |\n|---|---|---|---|---|---|\n"
                 f"| {UT}/referanse/{nf.name} | {nf.stat().st_size} | {sha} | {nå()} | — | "
                 f"{len(rader)} referansetreff fra {len(tekster)} verk (ADDENDUM-25 § 4); "
                 f"ots: {'ok' if st.ok else st.feil} |\n")
    print(json.dumps({"treff": len(rader), "verk": len(tekster), "sha256": sha,
                      "ugyldig_spenn": sum(not r["gyldig_spenn"] for r in rader),
                      "ots": str(st.kvittering) if st.ok else st.feil}, ensure_ascii=False))
    return 0


def _kjøring(navn: str) -> Path:
    return REPO / "data" / "kjede" / navn


def _leserdommer(kd: Path, v: Path, navn: str) -> list[dict]:
    """Leserens dommer koblet til tekstbitene gjennom nøkkelen på Vault."""
    nøkkel = {r["id"]: r for r in _jsonl(v / navn / "nokkel.jsonl")}
    ut = []
    for f in sorted(kd.glob("7-verdikter-okt-*.jsonl")):
        for r in _jsonl(f):
            ut.append({**nøkkel[r["id"]], **r})
    return ut


def presisjon_bygg(navn: str) -> int:
    v = require_vault()
    kd = _kjøring(navn)
    treff = [d for d in _leserdommer(kd, v, navn) if d.get("treff") is True]
    n = min(N_PRESISJON, len(treff))
    utvalg = random.Random(FRØ).sample(sorted(treff, key=lambda d: d["id"]), n)
    tekst = {}
    for f in sorted((kd / "blind").glob("blind-okt-*.jsonl")):
        for r in _jsonl(f):
            tekst[r["id"]] = r["tekst"]
    pd = v / UT / "presisjon"
    pd.mkdir(parents=True, exist_ok=True)
    blind = [{"id": f"P3-{i:03d}", "tekst": tekst[d["id"]]} for i, d in enumerate(utvalg, 1)]
    nøkkel = [{"id": f"P3-{i:03d}", "leser_id": d["id"], "doc_id": d["doc_id"],
               "start_index": d["start_index"], "end_index": d["end_index"]}
              for i, d in enumerate(utvalg, 1)]
    (pd / "blind-presisjon.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in blind),
                                              encoding="utf-8")
    (pd / "nokkel-presisjon.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in nøkkel),
                                               encoding="utf-8")
    print(json.dumps({"leser_treff": len(treff), "trukket": n, "frø": FRØ,
                      "blind_sha256": sha256_file(pd / "blind-presisjon.jsonl"),
                      "nokkel_sha256": sha256_file(pd / "nokkel-presisjon.jsonl")}, ensure_ascii=False))
    return 0


#: Presisjonsporten i samme form som ADDENDUM-23 §4 (oppdraget ordrett i
#: ``oppdrag-gjenvunnet/oppdrag-presisjon-100-ADDENDUM-23.md``), med fase 3s stier.
PRESISJON_OPPDRAG = """# Oppdrag: uavhengig koding av {N} blindede tekstbiter

Du er en uavhengig koder i en preregistrert studie. **Alt du skriver skal være på norsk (bokmål).**

**Din egen kladdekatalog**, som ingen annen instans bruker — legg alle hjelpefiler der og ingen andre steder:
`{KLADD}`

## Oppgaven

Les {N} blindede tekstbiter og avgjør for hver om den inneholder et **parkert spørsmål** slik studiens
regler definerer det, og i så fall hvilken hindringsklasse den faller i.

**Du får ingen opplysning om hva utvalget er, hvordan det er trukket, eller hva noen andre har ment om
det. Ikke forsøk å utlede det. Avgjør hver tekstbit på reglene alene.**

## De eneste to filene du får lese

1. **Reglene:** `{REGLER}`
2. **Materialet:** `{BLIND}` — {N} linjer, feltene `id` og `tekst`

Reglene er den eneste kilden. Står svaret ikke der, skal du ikke gjette deg til det fra annet materiale.

**Merk om regelfilen:** utdraget fra ADDENDUM-05 i den er limt inn som `grep -n`-utdata, så noen linjer
bærer linjenummer og skilletegn, og tabellen over uavklarte naboparer er avkuttet etter tabellhodet. Det
er kjent og skal ikke rettes. Bruk bare de uavklart-verdiene reglene faktisk navngir.

## STRENGT FORBUDT å åpne, grep-e, cat-e eller på annen måte inspisere

Alt i repoet `{REPO}`, og **alt på `{VAULT}` unntatt de to filene over** — særlig nøkkelfilen
`{UT}/presisjon/nokkel-presisjon.jsonl`, alt under `{UT}/referanse/`, kjedens kjøringer og nøkler, og alle
verdiktfiler. **Ikke list katalogen `{UT}/presisjon/`** — skriv rett til filnavnet under.
**`git log`, `git show`, `git diff` og `git blame` er forbudt.**

## Utdata

Skriv **én JSON-linje per tekstbit**, i blindfilens rekkefølge, til
`{UTFIL}`:

```json
{{"id": "P3-001", "treff": true, "klasse": "H7", "begrunnelse": "én setning", "tvil": false}}
```

* `treff` — `true`/`false` etter reglenes definisjon av et treff.
* `klasse` — ved treff: `H1`–`H9`, eller `<klasse>/H7-uavklart` der reglene gir den verdien. Ved
  ikke-treff: `N1`, `N2`, `N3`, eller `INGEN` når ingen ikke-treff-kategori passer.
* `begrunnelse` — **én setning**, på norsk.
* `tvil` — `true` hvis du var i reell tvil om `treff`.

Skriv linjene fortløpende og flush underveis. Ikke skriv noe annet til den filen.

## Sluttrapport

Når alle {N} er kodet, skriv en kort rapport i svaret ditt med:

1. antall kodede tekstbiter, og antall `treff`
2. fordeling på klasse
3. **en uttrykkelig bekreftelse på at ingen av de forbudte filene ble åpnet**
4. hvilke tolkningsvalg du måtte gjøre selv fordi reglene ikke avgjorde dem
5. om defekten i ADDENDUM-05-utdraget påvirket noen koding, og i så fall hvilke

Gå gjennom alle {N} i blindfilens rekkefølge. Ikke hopp over noen, og ikke stopp før du er ferdig.
"""


def presisjon_les() -> int:
    """Presisjonsporten: én separat instans, arbeidskatalog på Vault utenfor repoet."""
    import subprocess
    import time
    v = require_vault()
    pd = v / UT / "presisjon"
    blind = pd / "blind-presisjon.jsonl"
    n = len(_jsonl(blind))
    utfil = pd / "verdikter-presisjon.jsonl"
    if utfil.is_file():
        print("verdiktfilen finnes — kjøres ikke om", file=sys.stderr)
        return 2
    kladd = pd / "kladd"
    kladd.mkdir(parents=True, exist_ok=True)
    o = PRESISJON_OPPDRAG.format(N=n, KLADD=kladd, REGLER=v / REGELFIL, BLIND=blind, REPO=REPO,
                                 VAULT=v, UT=UT, UTFIL=utfil)
    (pd / "oppdrag-presisjon.md").write_text(o, encoding="utf-8")
    t0 = time.time()
    r = subprocess.run(["claude", "-p", "--model", MODELL, "--output-format", "json",
                        "--permission-mode", "acceptEdits", "--strict-mcp-config", "--add-dir", str(v)],
                       cwd=kladd, capture_output=True, text=True, timeout=7200, input=o)
    try:
        svar = json.loads(r.stdout)
    except ValueError:
        svar = {"is_error": True, "result": "kunne ikke lese JSON", "stderr": r.stderr[-400:]}
    rad = {"modell": MODELL, "minutter": round((time.time() - t0) / 60, 1),
           "is_error": svar.get("is_error"), "usage": svar.get("usage"),
           "modelUsage": svar.get("modelUsage"), "num_turns": svar.get("num_turns"),
           "total_cost_usd": svar.get("total_cost_usd"), "resultat": str(svar.get("result"))[:1500],
           "dømt": len(_jsonl(utfil)) if utfil.is_file() else 0, "av": n}
    (pd / "bruk-presisjon.json").write_text(json.dumps(rad, ensure_ascii=False, indent=1) + "\n",
                                            encoding="utf-8")
    print(json.dumps({k: rad[k] for k in ("minutter", "is_error", "dømt", "av")}, ensure_ascii=False))
    return 0 if rad["dømt"] == n else 2


def dekker(u: dict, s: list[int]) -> bool:
    return u["start_index"] <= s[0] and s[-1] <= u["end_index"]


def maal(navn: str) -> int:
    v = require_vault()
    kd = _kjøring(navn)
    ut = v / UT
    nøkkel = _jsonl(ut / "referanse" / "NOKKEL-referansesett.jsonl")
    ref_verk = {t["work_id"] for t in json.loads((ut / "referanse" / "tekster.json").read_text())}
    union = [u for u in _jsonl(kd / "5-union.jsonl")]
    dommer = {(d["doc_id"], d["start_index"], d["end_index"]): d for d in _leserdommer(kd, v, navn)}
    per_verk: dict[str, list[dict]] = {}
    for u in union:
        per_verk.setdefault(u["doc_id"], []).append(u)
    beholdt = bekreftet = 0
    ref_rader = []
    for h in nøkkel:
        s = h["setninger"]
        dek = [u for u in per_verk.get(h["work_id"], []) if dekker(u, s)]
        bk = [u for u in dek if (dommer.get((u["doc_id"], u["start_index"], u["end_index"])) or {}).get("treff") is True]
        beholdt += bool(dek)
        bekreftet += bool(bk)
        ref_rader.append({"ref": h["ref"], "work_id": h["work_id"], "setninger": s, "klasse": h.get("klasse"),
                          "tvil": h.get("tvil"), "beholdt": bool(dek), "bekreftet": bool(bk),
                          "kilder": sorted({u["kilde"] for u in dek})})
    nH = len(nøkkel)
    res = {"tid": nå(), "kjøring": navn,
           "referanse": {"verk": len(ref_verk), "treff": nH,
                         "treff_uten_tvil": sum(1 for h in nøkkel if not h.get("tvil")),
                         "ugyldig_spenn": sum(1 for h in nøkkel if not h.get("gyldig_spenn"))},
           "recall_sil": {"k": beholdt, "n": nH, "andel": round(beholdt / nH, 3) if nH else None,
                          "wilson95": wilson(beholdt, nH)},
           "recall_leser": {"k": bekreftet, "n": nH, "andel": round(bekreftet / nH, 3) if nH else None,
                            "wilson95": wilson(bekreftet, nH)},
           "leser_gitt_beholdt": {"k": bekreftet, "n": beholdt,
                                  "andel": round(bekreftet / beholdt, 3) if beholdt else None}}
    pv = ut / "presisjon" / "verdikter-presisjon.jsonl"
    if pv.is_file():
        vs = _jsonl(pv)
        k = sum(1 for r in vs if r.get("treff") is True)
        res["port1_presisjon"] = {"k": k, "n": len(vs), "andel": round(k / len(vs), 3),
                                  "wilson95": wilson(k, len(vs)), "terskel": 0.70,
                                  "bestått": k / len(vs) >= 0.70}
        res["navn"] = ("arbeidsliste (prospektiv port)" if res["port1_presisjon"]["bestått"]
                       else "kandidatliste")
    (ut / "maaling-fase3.json").write_text(json.dumps({**res, "rader": ref_rader}, ensure_ascii=False,
                                                      indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("kommando", choices=("referansetekst", "referanseoppdrag", "referanse-les", "sikre-nokkel",
                                        "presisjon-bygg", "presisjon-les", "maal"))
    p.add_argument("--kjoring", default="fase3-kjede")
    a = p.parse_args(argv)
    if a.kommando == "referansetekst":
        return referansetekst()
    if a.kommando == "referanseoppdrag":
        return referanseoppdrag()
    if a.kommando == "referanse-les":
        return referanse_les()
    if a.kommando == "sikre-nokkel":
        return sikre_nokkel()
    if a.kommando == "presisjon-les":
        return presisjon_les()
    if a.kommando == "presisjon-bygg":
        return presisjon_bygg(a.kjoring)
    return maal(a.kjoring)


if __name__ == "__main__":
    sys.exit(main())
