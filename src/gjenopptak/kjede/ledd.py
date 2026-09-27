"""Kjedens åtte ledd. Hvert ledd kan kjøres alene og gjenopptas.

ADR-0012, og byggeplanen B1 (``docs/BYGGEPLAN.md``):

===  ====================  =================================================================
nr   ledd                  gjør
===  ====================  =================================================================
1    ``hent``              fulltekst til Vault, manifest-rad per fil, ``require_vault()``
2    ``tekstbiter``        samme deler og vindusregel som porten
3    ``dommer``            ``gemma2:9b``, ``num_ctx`` eksplisitt, signatur per dom, kanari først
4    ``ekstraksjon``       ledeteksten fra ADDENDUM-16, ``num_ctx`` 8192, alle-treff-kobling
5    ``union``             A ∪ B, ikke-prosa merket, aldri fjernet
6    ``blind``             blindfiler, leseroppdrag fra mal, sperreliste, nøkkel til Vault
7    ``les``               serielle CC-økter à ≤ øktstørrelse, egen kladdekatalog, forbruk ført
8    ``register``          claims-2 med tvil-felt, header med port, sha, manifest
===  ====================  =================================================================

Hvert ledd skriver tilstand til ``tilstand.json`` i kjøringens katalog, og hopper over det
som alt er gjort. Et avbrudd koster tid, ikke arbeid.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import shutil
import subprocess
import time
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from ..classify import port as PO
from ..classify.ikkeprosa import er_ikke_prosa
from ..vault import require_vault, sha256_file
from .konfig import Konfig, sha256_fil

LEDD = ("hent", "tekstbiter", "dommer", "ekstraksjon", "union", "blind", "les",
        "verksniva", "falsify", "register")


class LeddFeil(RuntimeError):
    """Leddet kan ikke fullføres. Meldingen sier hva som mangler."""


def nå() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def norm(s: str) -> str:
    """ADDENDUM-16 §3: NFC, samlet mellomrom, uten tegnsetting i endene. Ingen fuzzy."""
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip().strip(".,;:!?\"»«'()[]").lower()


@dataclass
class Kjøring:
    """Én kjøring av kjeden: katalogen, verkene, og tilstanden."""

    k: Konfig
    navn: str
    verk: list[str] = field(default_factory=list)
    felt: str | None = None

    @property
    def dir(self) -> Path:
        return self.k.kjøring(self.navn)

    @property
    def tilstandsfil(self) -> Path:
        return self.dir / "tilstand.json"

    def les_tilstand(self) -> dict:
        if self.tilstandsfil.is_file():
            return json.loads(self.tilstandsfil.read_text(encoding="utf-8"))
        return {"navn": self.navn, "opprettet": nå(), "ledd": {}}

    def skriv_tilstand(self, t: dict) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        self.tilstandsfil.write_text(json.dumps(t, ensure_ascii=False, indent=1) + "\n",
                                     encoding="utf-8")

    def før(self, ledd: str, ut: dict) -> None:
        t = self.les_tilstand()
        t["ledd"][ledd] = {"tid": nå(), **ut}
        self.skriv_tilstand(t)

    def gjort(self, ledd: str) -> dict | None:
        return self.les_tilstand()["ledd"].get(ledd)

    def fil(self, navn: str) -> Path:
        self.dir.mkdir(parents=True, exist_ok=True)
        return self.dir / navn


def _les_jsonl(p: Path) -> list[dict]:
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def _skriv_jsonl(rader: list[dict], p: Path) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rader), encoding="utf-8")
    return sha256_fil(p)


# ============================================================= 1 hent
def steg_hent(kj: Kjøring) -> dict:
    """Finn eller hent fulltekst for verkene, og før en manifest-rad per fil.

    De 100 verkene i porten ligger alt på Vault; de finnes gjennom
    ``spesifikasjon.json`` og gjenhentes ikke. Ukjente verk hentes med
    ``harvest.fetchtest``, som har den ærlige UA-en og vertsporten.
    """
    v = require_vault(kj.k.vault_rot)
    spes = json.loads(kj.k.sti("tekstbiter", "fasit_spesifikasjon").read_text(encoding="utf-8"))
    kjent = {r["work_id"]: r for r in spes["verk"]}
    rader, mangler = [], []
    for wid in kj.verk:
        r = kjent.get(wid)
        if r is None:
            mangler.append(wid)
            continue
        f = v / "utvalg" / r["felt"] / r["fil"]
        if not f.is_file():
            raise LeddFeil(f"{wid}: filen mangler på Vault: {f}")
        sha = sha256_file(f)
        if sha != r["sha256"]:
            raise LeddFeil(f"{wid}: sha256 stemmer ikke med spesifikasjonen ({sha[:16]}…)")
        rader.append({"work_id": wid, "felt": r["felt"], "fil": str(f.relative_to(v)),
                      "bytes": f.stat().st_size, "sha256": sha, "port_ledd": r["port_ledd"],
                      "doi": r.get("doi"), "opphav": "frosset i porten", "sett": nå()})
    ut = kj.fil("1-hentet.jsonl")
    s = _skriv_jsonl(rader, ut)
    # Radene bærer et tidsstempel, så filens sha endrer seg for hver kjøring. Innholds-sha
    # utelater tidsstempelet, slik at leddet også har en identitet som KAN reproduseres.
    innhold = hashlib.sha256("".join(
        json.dumps({n_: r[n_] for n_ in sorted(r) if n_ != "sett"},
                   ensure_ascii=False, sort_keys=True) + "\n"
        for r in sorted(rader, key=lambda r: r["work_id"])).encode()).hexdigest()
    res = {"verk": len(rader), "ikke_funnet": mangler, "fil": str(ut), "sha256": s,
           "innhold_sha256": innhold, "vault": str(v)}
    if mangler:
        res["merknad"] = ("disse verkene er ikke i den frosne rammen og må hentes med "
                          "harvest.fetchtest før kjeden kan bruke dem")
    kj.før("hent", res)
    return res


# ============================================================= 2 tekstbiter
def steg_tekstbiter(kj: Kjøring) -> dict:
    """Bygg tekstbiter med samme deler og vindusregel som porten.

    ``spesifikasjon.json`` er fasit for formatet: feltene i utdataet må være de samme som
    i ``data/port/passasjer-*.jsonl``, og hver setning må dekkes.
    """
    from ..parse import sentences_from_jats
    from ..parse.pdfroute import sentences_from_pdf

    v = require_vault(kj.k.vault_rot)
    hentet = _les_jsonl(kj.fil("1-hentet.jsonl"))
    if not hentet:
        raise LeddFeil("ledd 1 (hent) har ikke kjørt")
    window = int(kj.k.verdi("tekstbiter", "window"))
    stride = int(kj.k.verdi("tekstbiter", "stride"))
    tmp = kj.dir / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    # Formatfasit: feltnavnene porten skrev.
    fasit_fil = kj.k.sti("tekstbiter", "fasit_spesifikasjon").parent / "passasjer-arkeologi.jsonl"
    ventede_felt = set(_les_jsonl(fasit_fil)[0]) if fasit_fil.is_file() else set()

    pas: list[dict] = []
    per_verk = {}
    for r in hentet:
        b = (v / r["fil"]).read_bytes()
        rows = (sentences_from_jats(b, doc_id=r["work_id"]) if r["port_ledd"] == "P1-JATS"
                else sentences_from_pdf(b, doc_id=r["work_id"], tmp_dir=tmp))
        ps = PO.passasjer(rows, r["felt"], stride=stride, window=window)
        if not PO.dekker_alle_setninger(ps, len(rows)):
            raise LeddFeil(f"{r['work_id']}: tekstbitene dekker ikke alle {len(rows)} setningene")
        for p in ps:
            d = {"doc_id": p.doc_id, "felt": p.felt, "start_index": p.start_index,
                 "end_index": p.end_index, "senter_index": p.senter_index,
                 "section_raw": p.section_raw,
                 "section_label_provenance": p.section_label_provenance,
                 "seksjoner_i_vindu": list(p.seksjoner_i_vindu), "tekst": p.tekst}
            if ventede_felt and set(d) != ventede_felt:
                raise LeddFeil(f"formatet avviker fra fasit: {set(d) ^ ventede_felt}")
            pas.append(d)
        per_verk[r["work_id"]] = {"setninger": len(rows), "tekstbiter": len(ps)}
    ut = kj.fil("2-tekstbiter.jsonl")
    s = _skriv_jsonl(pas, ut)
    res = {"tekstbiter": len(pas), "verk": len(per_verk), "window": window, "stride": stride,
           "per_verk": per_verk, "fil": str(ut), "sha256": s,
           "formatfasit": str(fasit_fil) if ventede_felt else "ingen"}
    kj.før("tekstbiter", res)
    return res


# ============================================================= 3 dommer
def _ollama(k: Konfig, seksjon: str, ledetekst: str, bruker: str, *, skjema: dict | None = None) -> dict:
    """Ett kall til ollama med eksplisitt ``num_ctx``, temperatur og frø."""
    import httpx

    vert = str(k.verdi("dommer", "vert"))
    kropp = {"model": str(k.verdi(seksjon, "modell")), "stream": False,
             "keep_alive": k.verdi("dommer", "keep_alive"),
             "options": {"temperature": k.verdi(seksjon, "temperatur"),
                         "seed": k.verdi(seksjon, "fro"),
                         "num_ctx": k.verdi(seksjon, "num_ctx")},
             "prompt": f"{ledetekst}\n\n{bruker}"}
    if skjema:
        kropp["format"] = skjema
    with httpx.Client(timeout=900) as c:
        r = c.post(f"{vert}/api/generate", json=kropp)
        r.raise_for_status()
        return r.json()


def kanari(kj: Kjøring, seksjon: str) -> dict:
    """Kanari før kjøring: setningen legges sist i et vindu fylt mot ``num_ctx``.

    ADDENDUM-16 §4: en kanari som ikke siteres tilbake, betyr stille avkutting. Tomt sitat
    diskvalifiserer — «tomt er ikke bekreftelse».
    """
    k = kj.k
    setning = str(k.verdi("dommer", "kanari"))
    num_ctx = int(k.verdi(seksjon, "num_ctx"))
    # Kanarien må prøve den inndataen leddet faktisk får i drift, med EKTE tekst
    # (ADDENDUM-16 §4). Dommerens enhet er ÉN tekstbit på ±2 setninger; den ser aldri et
    # maksvindu, så et maksvindu ville testet noe som ikke skjer — og dommeren svarer
    # UGYLDIG på det, korrekt. Ekstraksjonens enhet ER et dokumentvindu, så der er
    # maksvinduet den riktige prøven.
    biter = _les_jsonl(kj.fil("2-tekstbiter.jsonl"))
    if not biter:
        raise LeddFeil("kanarien trenger ledd 2 (tekstbiter) for å bygge et ekte vindu")
    uttømt = False
    if seksjon == "dommer":
        lengste = max(biter, key=lambda b: len(b["tekst"]))
        tekst = lengste["tekst"] + " " + setning
    else:
        # Nøyaktig det vinduet steg 4 sender: ``vindu_tegn`` tegn. Da prøver kanarien
        # produksjonsvinduet, ikke et gjettet et — og fyllkravet blir unødvendig.
        mål_tegn = int(k.verdi("ekstraksjon", "vindu_tegn"))
        stykker, n = [], 0
        for b in biter:
            if n >= mål_tegn:
                break
            stykker.append(b["tekst"])
            n += len(b["tekst"]) + 1
        uttømt = n < mål_tegn
        tekst = "\n".join(stykker)[:mål_tegn - len(setning) - 1] + "\n" + setning
    ledetekst = kj.k.sti(seksjon, "ledetekst").read_text(encoding="utf-8")
    # Kanarien må bruke LEDDETS EGET kall. Dommeren kjører /api/chat med JSON-skjema
    # (l3poc.RESPONSE_SCHEMA); uten skjemaet svarer modellen fritt og parseren gir UGYLDIG,
    # så en kanari uten skjema ville målt sitt eget oppsett og ikke dommeren.
    if seksjon == "dommer":
        from ..classify import l3poc as P
        from ..classify.l3poc_run import Lokal
        d = Lokal(keep_alive=k.verdi("dommer", "keep_alive"))
        s = d(ledetekst, P.user_prompt(tekst))
        rå = s["råsvar"]
        inn = (s.get("bruk") or {}).get("prompt_eval_count", 0)
    else:
        svar = _ollama(k, seksjon, ledetekst, tekst)
        rå = svar.get("response", "")
        inn = svar.get("prompt_eval_count", 0)
    ut = {"seksjon": seksjon, "num_ctx": num_ctx, "prompt_eval_count": inn,
          "vindusfylling": round(inn / num_ctx, 3), "enhet":
          "lengste tekstbit" if seksjon == "dommer" else "maksvindu",
          "teksten_uttømt": bool(seksjon != "dommer" and uttømt),
          "vindu_tegn": len(tekst),
          "avkuttet": inn >= num_ctx, "svarlengde": len(rå)}
    if inn >= num_ctx:
        raise LeddFeil(f"kanari: prompt_eval_count {inn} ≥ num_ctx {num_ctx} — stille avkutting")
    # Ingen minstefylling: kanarien SKAL være like stor som produksjonsvinduet, verken
    # mer eller mindre. Er produksjonsvinduet lite, er det ikke en feil i kanarien.
    # Kanarien må prøve det modellen faktisk skriver. Ekstraksjonen siterer setninger i
    # «Q:»-linjer, så der er sitat-tilbake den riktige testen (ADDENDUM-16 §4). Dommeren
    # svarer JSON og siterer ingenting; der er testen at et helt verdikt kom ut av et
    # maksvindu. Å kreve sitat av dommeren ville vært en test den ikke kan bestå.
    if seksjon == "ekstraksjon":
        q = [l.strip()[2:] for l in rå.splitlines() if l.strip().startswith("Q:")]
        ut["q_linjer"] = len(q)
        ut["kanari_sitert"] = any(norm(setning)[:40] in norm(x) for x in q if norm(x))
        if not ut["kanari_sitert"]:
            raise LeddFeil(f"kanari: setningen sto ikke i noen Q-linje ({len(q)} Q-linjer, "
                           f"svar {len(rå)} tegn) — vinduet kan være stille avkuttet")
    else:
        from ..classify import l3poc as P
        try:
            v = P.parse_response(rå)
        except Exception as e:
            raise LeddFeil(f"kanari: dommeren ga ikke et gyldig verdikt fra et maksvindu "
                           f"({type(e).__name__}: {e}); svar {len(rå)} tegn") from e
        ut["kanari_klasse"] = v.klasse
        ut["kanari_treff"] = v.treff
        # «UGYLDIG» er l3poc-parserens verdi når svaret ikke lot seg lese (l3poc.py:183).
        # Å godta den ville vært en falsk grønn — jf. LAERDOM §29.
        if v.klasse in (None, "", "UGYLDIG", "UNSURE"):
            raise LeddFeil(f"kanari: dommeren svarte {v.klasse!r} på et maksvindu — "
                           f"UGYLDIG betyr at svaret ikke lot seg parse")
    return ut


def steg_dommer(kj: Kjøring, *, cache: Path | None = None) -> dict:
    """Døm hver tekstbit. Gjenopptakbar: bare de som mangler dømmes.

    ``cache`` er en katalog med ferdige ``dommer-<felt>.jsonl`` fra porten. Tekstbiter som
    finnes der, dømmes ikke om — de er samme modell, samme ledetekst, samme frø.
    """
    from ..classify import l3poc as P
    from ..classify.l3poc_run import Lokal

    pas = _les_jsonl(kj.fil("2-tekstbiter.jsonl"))
    if not pas:
        raise LeddFeil("ledd 2 (tekstbiter) har ikke kjørt")
    utfil = kj.fil("3-dommer.jsonl")
    ferdige = {(r["doc_id"], r["start_index"]) for r in _les_jsonl(utfil)}
    fra_cache = 0
    if cache and not ferdige:
        rader = []
        for f in sorted(cache.glob("dommer-*.jsonl")):
            for r in _les_jsonl(f):
                rader.append(r)
        hurtig = {(r["doc_id"], r["start_index"]): r for r in rader}
        traff = [hurtig[(p["doc_id"], p["start_index"])] for p in pas
                 if (p["doc_id"], p["start_index"]) in hurtig]
        if traff:
            _skriv_jsonl(traff, utfil)
            ferdige = {(r["doc_id"], r["start_index"]) for r in traff}
            fra_cache = len(traff)
    todo = [p for p in pas if (p["doc_id"], p["start_index"]) not in ferdige]
    kan = None
    if todo:
        kan = kanari(kj, "dommer")
        ledetekst = kj.k.sti("dommer", "ledetekst").read_text(encoding="utf-8")
        dommer = Lokal(keep_alive=kj.k.verdi("dommer", "keep_alive"))
        with utfil.open("a", encoding="utf-8") as fh:
            for p in todo:
                svar = dommer(ledetekst, P.user_prompt(p["tekst"]))
                verdikt = P.parse_response(svar["råsvar"])
                rad = {
                    **{n: p[n] for n in ("doc_id", "felt", "start_index", "end_index",
                                         "senter_index", "section_raw",
                                         "section_label_provenance", "seksjoner_i_vindu")},
                    "klasse": verdikt.klasse, "treff": verdikt.treff,
                    "inkonsistent": verdikt.inkonsistent, "råsvar": svar["råsvar"],
                    "bruk": svar["bruk"], "signatur": svar["signatur"],
                }
                # Oppfølgingen porten gjør for treff (port_run.døm): ``samme_setning`` skiller
                # M1-streng fra M1-passasje (ADDENDUM-03 §1.2) og er det registerets ``unit``
                # er avledet av. Uten den kan ikke kjeden si hvilken enhet raden gjelder.
                if verdikt.treff:
                    o = dommer(PO.OPPF_PROMPT, P.user_prompt(p["tekst"]), format=PO.OPPF_SCHEMA)
                    try:
                        d_ = json.loads(o["råsvar"])
                        rad["samme_setning"] = bool(d_["samme_setning"])
                        rad["bedømbar"] = d_.get("bedømbar")
                    except (ValueError, KeyError, TypeError):
                        rad["samme_setning"] = None
                        rad["bedømbar"] = None
                    rad["oppf_signatur"] = o["signatur"]
                fh.write(json.dumps(rad, ensure_ascii=False) + "\n")
                fh.flush()
    alle = _les_jsonl(utfil)
    res = {"dømt": len(alle), "fra_cache": fra_cache, "nye": len(todo),
           "flagget": sum(1 for r in alle if r.get("treff")), "kanari": kan,
           "fil": str(utfil), "sha256": sha256_fil(utfil)}
    kj.før("dommer", res)
    return res


# ============================================================= 4 ekstraksjon
def steg_ekstraksjon(kj: Kjøring, *, cache: Path | None = None) -> dict:
    """Kjør ekstraksjonen per dokumentvindu og hent ut Q-linjene.

    ``cache`` er en ferdig ``ekstraksjon-logg.jsonl``. Verk som finnes der, kjøres ikke om.
    """
    pas = _les_jsonl(kj.fil("2-tekstbiter.jsonl"))
    if not pas:
        raise LeddFeil("ledd 2 (tekstbiter) har ikke kjørt")
    utfil = kj.fil("4-ekstraksjon.jsonl")
    verk = sorted({p["doc_id"] for p in pas})
    gjort = {(r["work_id"], r["vindu"]) for r in _les_jsonl(utfil)}
    fra_cache = 0
    if cache and cache.is_file() and not gjort:
        rader = [r for r in _les_jsonl(cache) if r.get("work_id") in set(verk)]
        if rader:
            _skriv_jsonl(rader, utfil)
            gjort = {(r["work_id"], r["vindu"]) for r in rader}
            fra_cache = len(rader)
    kan = None
    vt = int(kj.k.verdi("ekstraksjon", "vindu_tegn"))
    if not gjort:
        kan = kanari(kj, "ekstraksjon")
        ledetekst = kj.k.sti("ekstraksjon", "ledetekst").read_text(encoding="utf-8")
        per_verk: dict[str, list[dict]] = {}
        for p in pas:
            per_verk.setdefault(p["doc_id"], []).append(p)
        with utfil.open("a", encoding="utf-8") as fh:
            for wid in verk:
                biter = sorted(per_verk[wid], key=lambda d: d["start_index"])
                # Vindu = sammenhengende tekst per verk, delt så num_ctx ikke bindes.
                tekst = "\n".join(b["tekst"] for b in biter)
                deler = [tekst[i:i + vt] for i in range(0, len(tekst), vt)] or [""]
                for nr, del_ in enumerate(deler, 1):
                    t0 = time.time()
                    svar = _ollama(kj.k, "ekstraksjon", ledetekst, del_)
                    fh.write(json.dumps({
                        "work_id": wid, "vindu": nr,
                        "tokens_inn": svar.get("prompt_eval_count"),
                        "veggtid": round(time.time() - t0, 2),
                        "utdata_raa": svar.get("response", ""),
                        "signatur": {"model_id": str(kj.k.verdi("ekstraksjon", "modell")),
                                     "temperature": kj.k.verdi("ekstraksjon", "temperatur"),
                                     "seed": kj.k.verdi("ekstraksjon", "fro"),
                                     "num_ctx": kj.k.verdi("ekstraksjon", "num_ctx"),
                                     "prompt_sha256": str(kj.k.verdi("ekstraksjon",
                                                                     "ledetekst_sha256"))},
                    }, ensure_ascii=False) + "\n")
                    fh.flush()
    rader = _les_jsonl(utfil)
    q = [l[2:].strip() for r in rader for l in r["utdata_raa"].splitlines()
         if l.strip().startswith("Q:") and norm(l.strip()[2:])]
    res = {"vinduer": len(rader), "fra_cache": fra_cache, "q_linjer": len(q), "kanari": kan,
           "fil": str(utfil), "sha256": sha256_fil(utfil)}
    kj.før("ekstraksjon", res)
    return res


# ============================================================= 5 union
def steg_union(kj: Kjøring) -> dict:
    """L3: silen. Går gjennom grensesnittet ``sil(tekstbiter) -> kandidater`` (B4).

    Implementasjonen er ``dommer ∪ ekstraksjon``, den eneste som fanget alle 27 kjente treff.
    Ikke-prosa merkes av den versjonerte regelen og fjernes aldri.
    """
    from . import sil as S

    pas = _les_jsonl(kj.fil("2-tekstbiter.jsonl"))
    dom = _les_jsonl(kj.fil("3-dommer.jsonl"))
    eks = _les_jsonl(kj.fil("4-ekstraksjon.jsonl"))
    if not (pas and dom):
        raise LeddFeil("ledd 2–3 må ha kjørt før unionen")
    biter = [S.Tekstbit(doc_id=p["doc_id"], start_index=p["start_index"],
                        end_index=p["end_index"], felt=p["felt"], tekst=p["tekst"],
                        section_raw=p.get("section_raw", ""),
                        section_label_provenance=p.get("section_label_provenance", "parser"))
             for p in pas]
    flagget = {(r["doc_id"], r["start_index"], r["end_index"]) for r in dom if r.get("treff")}
    q = [(r["work_id"], l.strip()[2:]) for r in eks for l in r["utdata_raa"].splitlines()
         if l.strip().startswith("Q:")]
    impl = S.velg("dommer_union_ekstraksjon")
    kandidater, stat = impl(biter, flagget=flagget, q_linjer=q,
                            alle_treff=str(kj.k.verdi("ekstraksjon", "kobling")) == "alle-treff")
    ut = kj.fil("5-union.jsonl")
    s = _skriv_jsonl([k.som_rad() for k in kandidater], ut)
    im = kj.k.seksjon("sil").get("implementasjon", {})
    res = {**stat, "sil": impl.navn,
           "andel_av_korpus_pst": round(100 * stat["andel_av_korpus"], 2),
           "målt_recall": im.get("recall_kjente"),
           "målt_kostnad": f"{im.get('leserpassasjer_per_bekreftet_treff')} leserpassasjer per "
                           f"bekreftet treff ({im.get('kostnad_kilde')})",
           "ikke_prosa_regel_sha256": str(kj.k.verdi("sil", "ikke_prosa_sha256")),
           "fil": str(ut), "sha256": s}
    kj.før("union", res)
    return res


# ============================================================= 6 blind
SPERRELISTE = (
    "data/port-presisjonssett*.jsonl", "data/port-tvil.jsonl",
    "data/koder2-sammenlikning.json", "data/recall-sett*",
    "data/falsifisering-*.json", "data/port/dommer-*.jsonl",
    "presisjon-resultater.json", "docs/LAERDOM.md", "docs/RESULTAT-PORT-v1.md",
    "docs/MANUSKRIPT-v0.1.md", "docs/METODE.md", "docs/MASTER-PATCH-*.md",
    "docs/PS-246-*", "PREREG-v1.md", "alle ADDENDUM-filer",
    "docs/REGELFIL-KODER2-GJENVUNNET-*.md", "alle andre blindfiler enn din egen",
)


def steg_blind(kj: Kjøring) -> dict:
    """Blindfiler, leseroppdrag fra mal, generert sperreliste, nøkkel til Vault.

    Blindfilene bærer bare ``id`` og ``tekst``, stokket med frøet fra konfigurasjonen.
    Oppdraget bygges fra malen med ``rute``-feltet tatt ut (det feltet kunne ikke oppstå:
    ADDENDUM-22 §9.4). Nøkkelen som binder ``id`` til verk og posisjon, ligger på Vault og
    står navngitt blant de forbudte filene.
    """
    v = require_vault(kj.k.vault_rot)
    union = _les_jsonl(kj.fil("5-union.jsonl"))
    if not union:
        raise LeddFeil("ledd 5 (union) har ikke kjørt")
    frø = int(kj.k.verdi("leser", "fro"))
    st = int(kj.k.verdi("leser", "okt_storrelse"))
    stokket = list(union)
    random.Random(frø).shuffle(stokket)
    n = len(stokket)
    antall = max(1, -(-n // st))
    grunn, rest = divmod(n, antall)
    størrelser = [grunn + 1] * rest + [grunn] * (antall - rest)

    blinddir = kj.dir / "blind"
    blinddir.mkdir(parents=True, exist_ok=True)
    mal = kj.k.vault_sti("leser", "oppdrag_mal").read_text(encoding="utf-8")
    # Ta ut rute-feltet: blokken som definerer det, og linjen i JSON-eksempelet.
    # Rute-feltet ut av kontrakten OG ut av prosaen: ADDENDUM-22 §9.4 viste at ruten ikke kan
    # oppstå så lenge selvpålagt forenkling diskvalifiserer treffet. Et oppdrag som ber om et
    # felt kontrakten ikke har, er selvmotsigende.
    mal = re.sub(r"\n\* `rute` — én av nøyaktig tre verdier:.*?\n(?=\* `begrunnelse`)", "\n",
                 mal, flags=re.S)
    mal = mal.replace(' "rute": "ekstern ressurs manglet",\n', "")
    mal = mal.replace('{"id": "AL-0001", "treff": true, "klasse": "H7",\n',
                      '{"id": "AL-0001", "treff": true, "klasse": "H7", ')
    mal = mal.replace(" og hvilken rute hindringen hører\ntil", "")
    mal = mal.replace("fordeling på klasse og på rute", "fordeling på klasse")
    mal = mal.replace("koding av arbeidslisten", f"koding, kjøring {kj.navn}")
    mal = mal.replace("av 8\n", f"av {antall}\n")
    sperre = "`" + "`, `".join(SPERRELISTE) + "`"
    nøkkel, økter, i = [], [], 0
    for o, s in enumerate(størrelser, 1):
        del_ = stokket[i:i + s]
        i += s
        blind = []
        for j, r in enumerate(del_, 1):
            aid = f"{kj.navn.upper()}-{len(nøkkel) + 1:05d}"
            blind.append({"id": aid, "tekst": r["tekst"]})
            nøkkel.append({"id": aid, "okt": o, **{n_: r[n_] for n_ in
                           ("doc_id", "start_index", "end_index", "felt", "kilde", "ikke_prosa")}})
        bf = blinddir / f"blind-okt-{o}.jsonl"
        bsha = _skriv_jsonl(blind, bf)
        opp = (mal.replace("{OKT}", str(o)).replace("{N}", str(s))
                  .replace("blind-okt-{OKT}.jsonl", bf.name))
        opp = opp.replace("data/arbeidsliste/", str(blinddir.relative_to(kj.k.rot)) + "/")
        # Malen bærer sin egen utdatasti. Bytt den ut på MØNSTER, ikke på en literal sti:
        # en hardkodet sti her ville gjort kjeden ukjørbar på en annen maskin (B1).
        opp = re.sub(r"^\s*`?/\S*okt-\d+-verdikter\.jsonl`?\s*:?\s*$",
                     f"`{kj.dir / f'7-verdikter-okt-{o}.jsonl'}`:", opp, flags=re.M)
        opp = re.sub(r"/\S*/okt-\d+-verdikter\.jsonl",
                     str(kj.dir / f"7-verdikter-okt-{o}.jsonl"), opp)
        opp += (f"\n\n## Sperreliste, generert av kjeden\n\nForbudt å åpne: {sperre}, "
                f"nøkkelfilen `{v.name}/{kj.navn}/nokkel.jsonl`, og alt annet på "
                f"`{v}` enn regelfilen. `git log`, `git show`, `git diff`, `git blame` "
                f"er forbudt.\n\n**Din egen kladdekatalog:** "
                f"`{kj.k.sti('leser', 'kladd_rot')}/okt-{o}/`\n")
        of = blinddir / f"oppdrag-okt-{o}.md"
        of.write_text(opp, encoding="utf-8")
        økter.append({"okt": o, "n": s, "blind": str(bf), "blind_sha256": bsha,
                      "oppdrag": str(of), "oppdrag_sha256": sha256_fil(of)})
    nd = v / kj.navn
    nd.mkdir(parents=True, exist_ok=True)
    nf = nd / "nokkel.jsonl"
    nsha = _skriv_jsonl(nøkkel, nf)
    res = {"union": n, "økter": len(økter), "størrelser": størrelser, "frø": frø,
           "blindfelt": ["id", "tekst"], "okt_storrelse_tak": st,
           "nøkkel": str(nf), "nøkkel_sha256": nsha, "per_okt": økter,
           "rute_felt": "tatt ut av malen"}
    kj.før("blind", res)
    return res


# ============================================================= 7 les
def steg_les(kj: Kjøring, *, tørr: bool = False, cache: Path | None = None,
             modus: str = "cli") -> dict:
    """Start leserøktene **serielt**, én instans om gangen, og verifiser hver.

    Byggeplanen B1: «Aldri parallelle Opus-instanser — sju parallelle falt på øktgrensen ved
    87 %. Egen kladdekatalog per instans.» Økten startes hodeløst med ``claude -p``; forbruket
    føres fra kommandoens eget JSON-svar.
    """
    t = kj.les_tilstand()
    blind = t["ledd"].get("blind")
    if not blind:
        raise LeddFeil("ledd 6 (blind) har ikke kjørt")
    kladd = kj.k.sti("leser", "kladd_rot")
    modell = str(kj.k.verdi("leser", "modell"))
    # Uten Claude Code finnes ingen leser. Si det rent og avslutt, i stedet for å feile inne i
    # subprocess med en melding om et manglende program.
    if modus == "cli" and not tørr and shutil.which("claude") is None:
        raise LeddFeil(
            "leddet «les» krever Claude Code med Opus, og `claude` finnes ikke på PATH. "
            "Kjeden har ingen annen leser: ett-kall-modeller er sil-klasse (ADR-0012), og "
            "verktøyet holder ingen API-nøkkel. Installer Claude Code og kjør «claude auth login», "
            "eller kjør leddet med --leser subagent fra en Claude Code-økt.")
    # Cache: ferdige verdikter fra en tidligere lesning av de samme passasjene, koblet på
    # (doc_id, start_index, end_index) gjennom nøkkelen. Brukes av røyktesten, slik at
    # kjeden kan verifiseres uten å bruke Opus-økter på nytt.
    hurtig: dict[tuple, dict] = {}
    if cache:
        nøkkel_gml = {}
        for kf in ([cache / "nokkel.jsonl"] if cache.is_dir() else []):
            for r in _les_jsonl(kf):
                nøkkel_gml[r["id"]] = r
        filer = sorted(cache.glob("*verdikter*.jsonl")) if cache.is_dir() else [cache]
        for f in filer:
            for r in _les_jsonl(f):
                n = nøkkel_gml.get(r["id"])
                if n:
                    hurtig[(n["doc_id"], n["start_index"], n["end_index"])] = r
        print(f"    leser-cache: {len(hurtig)} verdikter fra {cache}")
    ferdig, forbruk = [], []
    for ø in blind["per_okt"]:
        utfil = kj.dir / f"7-verdikter-okt-{ø['okt']}.jsonl"
        ventede = [r["id"] for r in _les_jsonl(Path(ø["blind"]))]
        if utfil.is_file() and [r["id"] for r in _les_jsonl(utfil)] == ventede:
            ferdig.append({"okt": ø["okt"], "status": "alt ferdig", "n": len(ventede)})
            continue
        if hurtig:
            nøkkel = {r["id"]: r for r in _les_jsonl(Path(blind["nøkkel"]))}
            rader, mangler = [], 0
            for aid in ventede:
                n = nøkkel[aid]
                v = hurtig.get((n["doc_id"], n["start_index"], n["end_index"]))
                if v is None:
                    mangler += 1
                    continue
                rader.append({"id": aid, **{x: v[x] for x in
                              ("treff", "klasse", "begrunnelse", "tvil") if x in v}})
            if mangler == 0:
                _skriv_jsonl(rader, utfil)
                ferdig.append({"okt": ø["okt"], "status": "fra cache", "n": len(rader)})
                continue
            ferdig.append({"okt": ø["okt"], "status": "cache dekker ikke alt",
                           "mangler": mangler, "av": len(ventede)})
            if not tørr:
                raise LeddFeil(f"økt {ø['okt']}: leser-cachen mangler {mangler} av "
                               f"{len(ventede)} passasjer; kjør uten --cache-leser")
            continue
        if tørr:
            ferdig.append({"okt": ø["okt"], "status": "tørrkjøring", "n": len(ventede)})
            continue
        (kladd / f"okt-{ø['okt']}").mkdir(parents=True, exist_ok=True)
        oppdrag = Path(ø["oppdrag"]).read_text(encoding="utf-8")
        if modus == "subagent":
            # CCs egen underinstans, som i ADDENDUM-22. Kjeden kan ikke starte en subagent selv —
            # det er orkestratorens verktøy — så den legger fram oppdraget og venter på
            # verdiktfilen. Kontrakten er stien: orkestratoren skriver dit oppdraget sier.
            ferdig.append({"okt": ø["okt"], "status": "venter på subagent",
                           "oppdrag": ø["oppdrag"], "utfil": str(utfil), "n": len(ventede)})
            continue
        t0 = time.time()
        # Oppdraget går på stdin, ikke som argument: ``--add-dir`` tar flere kataloger og
        # sluker et etterfølgende posisjonsargument. Stdin tar også lange oppdrag trygt.
        r = subprocess.run(
            ["claude", "-p", "--model", modell, "--output-format", "json",
             "--permission-mode", "acceptEdits", "--add-dir", str(kj.k.vault_mål)],
            cwd=kj.k.rot, capture_output=True, text=True, timeout=7200, input=oppdrag)
        bruk = {}
        try:
            svar = json.loads(r.stdout)
            bruk = {"usage": svar.get("usage"), "total_cost_usd": svar.get("total_cost_usd"),
                    "num_turns": svar.get("num_turns"), "is_error": svar.get("is_error"),
                    "resultat": str(svar.get("result"))[:400]}
            # En utløpt OAuth-økt ser ut som en tom kjøring. Si hva det er, og hva som retter det.
            if svar.get("is_error") and "authenticate" in str(svar.get("result", "")).lower():
                raise LeddFeil(
                    f"leserøkt {ø['okt']}: claude-CLI-en kunne ikke autentisere "
                    f"({svar.get('result')}). Kjeden kan ikke logge inn for deg: kjør "
                    f"«claude login» i en terminal og start leddet på nytt med --from les.")
        except ValueError:
            bruk = {"feil": "kunne ikke lese JSON fra claude -p",
                    "stderr": r.stderr[-400:]}
        bruk |= {"okt": ø["okt"], "minutter": round((time.time() - t0) / 60, 1)}
        forbruk.append(bruk)
        fikk = [r_["id"] for r_ in _les_jsonl(utfil)]
        if fikk != ventede:
            ferdig.append({"okt": ø["okt"], "status": "AVVIK",
                           "dømt": len(fikk), "ventet": len(ventede),
                           "rekkefølge_ok": fikk == ventede[:len(fikk)]})
        else:
            ferdig.append({"okt": ø["okt"], "status": "ferdig", "n": len(fikk)})
    # feltkontroll
    gyldige_treffklasser = set(PO.__dict__.get("PREREG_KLASSER", ())) or None
    avvik = []
    for ø in blind["per_okt"]:
        for r in _les_jsonl(kj.dir / f"7-verdikter-okt-{ø['okt']}.jsonl"):
            if not isinstance(r.get("treff"), bool) or not r.get("klasse") or not r.get("begrunnelse"):
                avvik.append(r.get("id"))
            if "tvil" not in r:
                avvik.append(r.get("id"))
    res = {"økter": ferdig, "forbruk": forbruk, "serielt": True, "modus": modus,
           "cache": str(cache) if cache else None,
           "feltavvik": sorted(set(a for a in avvik if a))[:20],
           "n_feltavvik": len(set(a for a in avvik if a))}
    kj.før("les", res)
    return res


#: PREREG-v1 §5 gir H1–H6 løftbar, H7–H9 ikke; ADDENDUM-05 §3 gir uavklart til de uavklarte.
#: Oppslag, aldri en modell (ADR-0004).
_LOFTBAR_TABELL = {"H1": "ja", "H2": "ja", "H3": "ja", "H4": "ja", "H5": "ja", "H6": "ja",
                   "H7": "nei", "H8": "nei", "H9": "nei"}


def _loftbar(klasse: str) -> str:
    if "uavklart" in klasse:
        return "uavklart"
    return _LOFTBAR_TABELL.get(klasse, "uavklart")


def _dekning(fals: dict, doi: str | None) -> dict:
    """``cites_coverage`` fra 7c. Uten måling er den **ikke** null — den er ukjent."""
    r = fals.get(str(doi).lower()) if doi else None
    if r is None:
        return {"fulltext_available": None, "fulltext_total": None, "coverage_ratio": None,
                "status": "ikke målt"}
    tot = r.get("epmc_citing") if r.get("epmc_citing") is not None else r.get("crossref_count")
    ft = r.get("epmc_citing_ft")
    return {"fulltext_available": ft, "fulltext_total": tot,
            "coverage_ratio": (round(ft / tot, 4) if (ft is not None and tot) else None),
            "status": "målt", "kilde": "EPMC + Crossref"}


# ============================================================= 8 register
def steg_register(kj: Kjøring, *, port: str | None = None) -> dict:
    """Skriv registeret i claims-2 med ``tvil``-felt og en header som sier hvilken port som er bestått."""
    v = require_vault(kj.k.vault_rot)
    t = kj.les_tilstand()
    blind = t["ledd"].get("blind")
    if not blind:
        raise LeddFeil("ledd 6 (blind) har ikke kjørt")
    nøkkel = {r["id"]: r for r in _les_jsonl(Path(blind["nøkkel"]))}
    verdikter = {}
    for ø in blind["per_okt"]:
        for r in _les_jsonl(kj.dir / f"7-verdikter-okt-{ø['okt']}.jsonl"):
            verdikter[r["id"]] = r
    if not verdikter:
        raise LeddFeil("ledd 7 (les) har ikke gitt verdikter")
    # Parseropphavet per verk, fra ledd 1: claims-2 fører hvilken parser setningene kom fra.
    from ..parse.jats import PARSER_ID as JATS_ID
    from ..parse.pdfroute import pdftotext_version
    ledd_per_verk = {r["work_id"]: r["port_ledd"] for r in _les_jsonl(kj.fil("1-hentet.jsonl"))}
    samme_setning = {(r["doc_id"], r["start_index"]): r.get("samme_setning")
                     for r in _les_jsonl(kj.fil("3-dommer.jsonl")) if r.get("treff")}
    # 7b og 7c om de har kjørt: verksnivået og siteringsdekningen hører på raden (B3).
    vn = {r["work_id"]: r for r in _les_jsonl(kj.fil("7b-verksniva.jsonl"))}
    fals = {}
    ff = kj.fil("7c-falsifisering.json")
    if ff.is_file():
        d_ = json.loads(ff.read_text(encoding="utf-8"))
        for r in d_.get("rader", []):
            if r.get("doi"):
                fals[str(r["doi"]).lower()] = r
    pres = {"begge": float(kj.k.verdi("sil", "presisjon_begge")),
            "dommer": float(kj.k.verdi("sil", "presisjon_dommer")),
            "ekstraksjon": float(kj.k.verdi("sil", "presisjon_ekstraksjon"))}
    rader = []
    for aid, vd in sorted(verdikter.items()):
        if not vd.get("treff"):
            continue
        n = nøkkel[aid]
        rader.append({
            "schema_version": str(kj.k.verdi("register", "skjema")),
            "claim_id": f"CLAIM-{aid}", "candidate_id": aid,
            "doc_id": n["doc_id"], "field_key": n["felt"],
            "obstacle_class": vd["klasse"],
            "tvil": bool(vd.get("tvil")),
            "loftbarhet": [{"vurdert_dato": nå()[:10], "datopresisjon": "dag",
                            "tabellversjon": "PREREG-v1-§5 + ADDENDUM-05",
                            "obstacle_class": vd["klasse"],
                            "loftbar": _loftbar(vd["klasse"])}],
            "falsified": False,
            "cites_coverage": _dekning(fals, vn.get(n["doc_id"], {}).get("doi")),
            "tested_at": nå(), "section_raw": n.get("section_raw", ""),
            "section_label_provenance": n.get("section_label_provenance", "parser"),
            # ADDENDUM-03 §1.2: «sentence» når det ugjorte og hindringen står i samme
            # setning, ellers «passage». Verifisert mot register v2: 27 av 27 rader følger
            # denne regelen. Er oppfølgingen ukjent, er «passage» det konservative svaret —
            # det er også det v2 bruker der samme_setning mangler.
            "unit": "sentence" if samme_setning.get(
                (n["doc_id"], n["start_index"])) is True else "passage",
            "parser_version": (JATS_ID if ledd_per_verk.get(n["doc_id"]) == "P1-JATS"
                               else "pdftotext/poppler"),
            "parser_model_version": (JATS_ID if ledd_per_verk.get(n["doc_id"]) == "P1-JATS"
                                     else pdftotext_version()),
            "passage_span": {"start_index": n["start_index"], "end_index": n["end_index"],
                             "n_sentences": n["end_index"] - n["start_index"] + 1,
                             "window": int(kj.k.verdi("tekstbiter", "window"))},
            "sil": {"kilde": n["kilde"], "presisjon": pres[n["kilde"]],
                    "presisjon_ki": list(kj.k.verdi("sil", f"presisjon_{n['kilde']}_ki")),
                    "presisjon_kilde": str(kj.k.verdi("sil", "presisjon_kilde")),
                    "ikke_prosa": bool(n["ikke_prosa"]),
                    "ikke_prosa_regel_sha256": str(kj.k.verdi("sil", "ikke_prosa_sha256"))},
            "verksniva": ({"materialtilgang": vn[n["doc_id"]]["materialtilgang"],
                           "maskinlesbar": vn[n["doc_id"]]["maskinlesbar"],
                           "eier": vn[n["doc_id"]]["eier"],
                           "tilgang": vn[n["doc_id"]]["tilgang"],
                           "forsok_mulig": vn[n["doc_id"]]["forsok_mulig"],
                           "ser_ikke": "H8 utenfor verket — tilgangssituasjonen endrer seg "
                                       "utenfor materialet (ADR-0010)"}
                          if n["doc_id"] in vn else None),
            "leser": {"modell": str(kj.k.verdi("leser", "modell")),
                      "regelfil_sha256": str(kj.k.verdi("leser", "regelfil_sha256")),
                      "presisjon_ved_tvil": float(kj.k.verdi("leser", "presisjon_med_tvil"))
                      if vd.get("tvil") else float(kj.k.verdi("leser", "presisjon_uten_tvil")),
                      "modus": (kj.les_tilstand()["ledd"].get("les") or {}).get("modus", "cli")},
            "notes": vd.get("begrunnelse", ""),
        })
    # B3: hver rad valideres mot utgangsskjemaet før den skrives. En rad som ikke kan leses av
    # en utenforstående, er ikke en leveranse.
    from ..schemas import validate as _valider
    feil = []
    for r in rader:
        try:
            _valider("kandidat", r)
        except Exception as e:
            feil.append(f"{r['candidate_id']}: {type(e).__name__}: {str(e)[:140]}")
    if feil:
        raise LeddFeil(f"{len(feil)} rader bryter kandidat-skjemaet; første: {feil[0]}")
    ut = kj.fil("8-register.jsonl")
    s = _skriv_jsonl(rader, ut)
    # ``tested_at`` og ``loftbarhet.vurdert_dato`` er daterte (ADR-0010), så filens sha endrer
    # seg for hver kjøring. Innholds-sha utelater dem, og er den sha en røyktest kan bruke.
    DATERT = {"tested_at", "loftbarhet"}
    innhold = hashlib.sha256("".join(
        json.dumps({n_: r[n_] for n_ in sorted(r) if n_ not in DATERT},
                   ensure_ascii=False, sort_keys=True) + "\n"
        for r in rader).encode()).hexdigest()
    hode = {
        "kjøring": kj.navn, "tid": nå(),
        "port": port or str(kj.k.verdi("register", "uten_port")),
        "bekreftet": bool(port),
        "n_rader": len(rader), "n_dømt": len(verdikter),
        "forbehold": {"stabil_kjerne": str(kj.k.verdi("register", "stabil_kjerne")),
                      "n3_spredning": str(kj.k.verdi("register", "n3_spredning")),
                      "ikke_prosa": "merket, aldri fjernet"},
        "adr": "ADR-0012", "register_sha256": s, "register_innhold_sha256": innhold,
    }
    _valider("registerhode", hode)
    hf = kj.fil("8-register-header.json")
    hf.write_text(json.dumps(hode, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md = v / kj.navn
    md.mkdir(parents=True, exist_ok=True)
    for f in (ut, hf):
        (md / f.name).write_bytes(f.read_bytes())
    res = {"rader": len(rader), "port": hode["port"], "fil": str(ut), "sha256": s,
           "innhold_sha256": innhold, "header": str(hf), "vault": str(md)}
    kj.før("register", res)
    return res


# ============================================================= 7b verksnivå
def steg_verksniva(kj: Kjøring) -> dict:
    """Materialtilgang per verk, med kriteriet portert ordrett fra Vault-skriptet.

    Kriteriet leser verkets **råtekst**: JATS-XML som den er, PDF gjennom ``pdftotext``. Det er
    samme inndata som da tallene ble målt 26.09.2026, og regexene er uendret
    (:mod:`gjenopptak.kjede.verksniva`, ``KILDE_SHA256``).
    """
    from ..parse.pdfroute import pdf_to_text
    from . import verksniva as VN

    v = require_vault(kj.k.vault_rot)
    hentet = _les_jsonl(kj.fil("1-hentet.jsonl"))
    if not hentet:
        raise LeddFeil("ledd 1 (hent) har ikke kjørt")
    dom = _les_jsonl(kj.fil("3-dommer.jsonl"))
    from collections import Counter, defaultdict
    treff: dict[str, Counter] = defaultdict(Counter)
    for r in dom:
        if r.get("treff"):
            treff[r["doc_id"]][r["klasse"]] += 1
    tmp = kj.dir / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    rader = []
    for h in hentet:
        b = (v / h["fil"]).read_bytes()
        if h["port_ledd"] == "P1-JATS":
            txt = b.decode("utf-8", "replace")
        else:
            txt = pdf_to_text(b, tmp, h["work_id"])
        er_jats = txt.lstrip().startswith("<?xml")
        a = VN.analyser(h["work_id"], txt, er_jats)
        lb = sum(n for k, n in treff[h["work_id"]].items() if k in VN.LOFTBAR)
        a.update(work_id=h["work_id"], felt=h["felt"], doi=h.get("doi"),
                 port_ledd=h["port_ledd"],
                 kilde=("JATS" if er_jats else ("HTML" if txt.lstrip().startswith("<") else "PDF")),
                 n_doemte_treff=sum(treff[h["work_id"]].values()), n_loftbare=lb,
                 klasser=dict(treff[h["work_id"]].most_common()))
        a["forsok_mulig"] = (a["materialtilgang"] != "LUKKET") and lb > 0
        rader.append(a)
    rang = {"ÅPEN": 0, "DELVIS": 1, "LUKKET": 2}
    rader.sort(key=lambda r: (rang[r["materialtilgang"]], -r["n_loftbare"], r["work_id"]))
    ut = kj.fil("7b-verksniva.jsonl")
    s = _skriv_jsonl(rader, ut)
    res = {"verk": len(rader), "kriterium_sha256": VN.KILDE_SHA256,
           "per_nivaa": dict(Counter(r["materialtilgang"] for r in rader).most_common()),
           "forsok_mulig": sum(1 for r in rader if r["forsok_mulig"]),
           "fil": str(ut), "sha256": s}
    kj.før("verksniva", res)
    return res


# ============================================================= 7c L5 falsifisering
def steg_falsify(kj: Kjøring, *, tørr: bool = False) -> dict:
    """Falsifisering mot siteringer, for verkene med minst ett dømt treff.

    Bruker :mod:`gjenopptak.falsify.citations`, som armer seg selv først: uten en armert klient er
    et nulltall ikke et svar (LAERDOM — stille nulltall i siteringsoppslag var ett av de ti
    grønn-og-feil-tilfellene). Armeringen feiler høyt i stedet for å returnere 0.
    """
    from ..falsify import citations as C

    vn = _les_jsonl(kj.fil("7b-verksniva.jsonl"))
    if not vn:
        raise LeddFeil("ledd 7b (verksniva) har ikke kjørt")
    dois = [r["doi"] for r in vn if r["n_doemte_treff"] > 0 and r.get("doi")]
    uten_doi = [r["work_id"] for r in vn if r["n_doemte_treff"] > 0 and not r.get("doi")]
    ut = kj.fil("7c-falsifisering.json")
    if tørr:
        res = {"status": "tørrkjøring", "dois": len(dois), "uten_doi": len(uten_doi)}
        kj.før("falsify", res)
        return res
    if ut.is_file():
        d = json.loads(ut.read_text(encoding="utf-8"))
        res = {"status": "alt gjort", "rader": len(d.get("rader", [])), "fil": str(ut),
               "sha256": sha256_fil(ut)}
        kj.før("falsify", res)
        return res
    try:
        rader = C.measure(dois)
        armert = True
        feil = None
    except Exception as e:                       # armering eller nett feiler høyt
        rader, armert, feil = [], False, f"{type(e).__name__}: {e}"
    d = {"tid": nå(), "armert": armert, "feil": feil, "n_dois": len(dois),
         "uten_doi": uten_doi,
         "rader": [r.__dict__ if hasattr(r, "__dict__") else r for r in rader]}
    if rader:
        d["sammendrag"] = C.summarise(rader)
    ut.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    res = {"armert": armert, "feil": feil, "dois": len(dois), "uten_doi": len(uten_doi),
           "rader": len(rader), "fil": str(ut), "sha256": sha256_fil(ut)}
    kj.før("falsify", res)
    return res
