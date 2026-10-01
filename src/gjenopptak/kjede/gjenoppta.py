"""Gjenoppta en låst kjøring etter avbrudd — fra låsecommitens worktree, aldri fra arbeidstreet.

    python -m gjenopptak.kjede.gjenoppta --sjekk
    python -m gjenopptak.kjede.gjenoppta

Eierens regel 28.09.2026 (RESULTAT-ADDENDUM-25 § 0.3): en fase 3-kjøring som avbrytes, gjenopptas fra
låsecommiten `f19a3e3` i en git worktree på Vault, slik at alle ledd kjører med de sha256-ene
ADDENDUM-25 § 9 låser. Arbeidstreet kan ha gått videre (referanseporten i `cli.py`, ADR-0014), og en
gjenopptakelse derfra ville kjørt kode som ikke er den låste.

**Sjekkene, i rekkefølge — ett avvik stopper, ingenting startes:**

1. Vault er montert (ADR-0009).
2. Worktreets HEAD er låsecommiten, og ingen sporet fil i det er endret.
3. **Hver fil i sha-tabellen i addendumets § 9, lest fra låsecommiten selv** (`git show <lås>:<addendum>`),
   har den sha256-en i worktreet — `kjede/cli.py` eksplisitt, fordi det er fila arbeidstreet har endret.
4. `gjenopptak` importeres fra worktreet, ikke fra arbeidstreet eller den redigerbare installasjonen.
5. ollama svarer på ``/api/tags`` på verten i den låste ``kjede.toml`` (lagt til 29.09.2026).
5b. Referanseporten (ADR-0014) bestås. Den står ikke i den låste `cli.py`, så rutinen kjører den selv.
6. Ingen annen `kjede.cli run` for samme kjøring går allerede (to samtidige ville skrevet i samme
   tilstandsfil; LAERDOM § 43).

Så startes `gjenopptak run` i worktreet med de samme argumentene som den opprinnelige kjøringen. Hver
gjenopptakelse føres i `fase3/gjenopptak-logg.jsonl` på Vault.

**Lagt til 30.09.2026, etter at leserleddet to ganger ble ført ferdig uten utdata** (LAERDOM § 45):

7. **Ingen verdiktfil overskrives.** Før et spenn med `les` klassifiseres hver økts verdiktfil mot blindfila:
   mangler, komplett, delvis eller korrupt. Delvis eller korrupt nekter start — en delvis økt fullføres først
   serielt med ``--fullfor-okt N`` (ADDENDUM-25 § 8), og det låste leserleddet ville ellers kjørt hele økta
   om oppå de dømte. Hver eksisterende verdiktfils bytes og sha føres før start og kontrolleres etter: en fil
   kan forlenges, aldri skrives om.
8. **Etter `les` kjøres `verksniva`, `falsify` og `register` alltid om** (tvungen ``--om``), i et eget kall.
   Den låste kjeden fører et ledd ferdig uten å se på om inndataene har endret seg.
9. **Etterkontroll av hvert ledd** etter hvert kall: ikke-tomme, gyldige utdata i fullt antall — for `les` hver
   økt id for id mot blindfila — og ingen ledd ført ferdig før leddet det bygger på. Et avvik stopper med
   rc 3 og navnet på det som mangler; kallet etter startes ikke.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from ..vault import require_vault
from . import referanseport as RP

REPO = Path(__file__).resolve().parents[3]
LÅS = "f19a3e3"
ADDENDUM = "ADDENDUM-25.md"
VAULT_FASE3 = "fase3"
WORKTREE = "fase3/worktree-f19a3e3"          # relativ til Vault-målet
KJØRING = ["--verk", "{fase3}/verk-fase3.txt", "--utvalg", "{fase3}/utvalg-fase3-arkeologi.jsonl",
           "--navn", "fase3-kjede", "--leser", "cli"]
MÅ_FINNES = ("src/gjenopptak/kjede/cli.py",)


class GjenopptakNekt(RuntimeError):
    pass


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def låst_tabell(addendum_tekst: str) -> dict[str, str]:
    """Sha-tabellen i addendumets § 9: rader på formen | `sti` | `sha256` |, der stien er en fil i repoet
    (``src/…`` eller ``kjede.toml``). Rader om Vault-filer (regelfil, ramme) er med i tabellen, men
    sjekkes av kjeden selv og ikke her."""
    i = addendum_tekst.find("## 9 ")
    if i < 0:
        raise GjenopptakNekt("fant ikke § 9 i addendumet")
    ut = {}
    for sti, h in re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|", addendum_tekst[i:], re.M):
        if sti.startswith("src/") or sti == "kjede.toml":
            ut[sti] = h
    if not ut:
        raise GjenopptakNekt("sha-tabellen i § 9 er tom")
    return ut


def sjekk_sha(worktree: Path, tabell: dict[str, str]) -> list[str]:
    avvik = [f"{sti} står ikke i § 9-tabellen" for sti in MÅ_FINNES if sti not in tabell]
    for sti, ventet in sorted(tabell.items()):
        p = worktree / sti
        if not p.is_file():
            avvik.append(f"{sti}: finnes ikke i worktreet")
        elif (fikk := sha256(p)) != ventet:
            avvik.append(f"{sti}: sha256 {fikk[:16]}… ≠ låst {ventet[:16]}…")
    return avvik


def _git(*a: str, cwd: Path = REPO) -> str:
    return subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True, check=True).stdout.strip()


def kjører_allerede(navn: str, *, ps_utdata: str | None = None, egen: set[int] | None = None) -> list[str]:
    """Prosesser som allerede kjører denne kjøringen: ``gjenopptak.kjede.cli`` med ``--navn <navn>``
    (i hvilken som helst argumentrekkefølge — rutinen selv setter ``--konfig`` foran ``run``), eller en
    annen gjenopptaksrutine som ikke bare sjekker. Egen prosess og forelder regnes ikke med.

    Rettet 29.09.2026: mønsteret var «kjede.cli run», som ikke traff kjøringer startet av rutinen selv
    (``kjede.cli --konfig … run``), så vakten mot to samtidige kjøringer var blind for dem.

    Rettet 30.09.2026: bare en Python-prosess som kjører modulen (``python -m gjenopptak.kjede.…``) teller.
    Et skall som nevner modulnavnet — en overvåkingsløkke med ``pgrep -f gjenopptak.kjede.gjenoppta`` —
    slo vakten ut og nektet gjenopptaket etter fullføringen av økt 3."""
    egen = egen if egen is not None else {os.getpid(), os.getppid()}
    if ps_utdata is None:
        ps_utdata = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout
    ut = []
    for l in ps_utdata.splitlines():
        deler = l.strip().split(None, 1)
        if len(deler) < 2 or not deler[0].isdigit() or int(deler[0]) in egen:
            continue
        ord_ = deler[1].split()
        if not Path(ord_[0]).name.lower().startswith("python") or "-m" not in ord_:
            continue
        modul = ord_[ord_.index("-m") + 1] if ord_.index("-m") + 1 < len(ord_) else ""
        if modul == "gjenopptak.kjede.cli" and f"--navn {navn}" in deler[1]:
            ut.append(l.strip())
        elif modul == "gjenopptak.kjede.gjenoppta" and "--sjekk" not in ord_:
            ut.append(l.strip())
    return ut


def ollama_vert(worktree: Path) -> str:
    """Verten fra den låste ``kjede.toml`` i worktreet — samme vert kjeden selv kaller."""
    import tomllib
    with (worktree / "kjede.toml").open("rb") as fh:
        return str(tomllib.load(fh)["dommer"]["vert"])


def krev_ollama(vert: str, *, tidsavbrudd: float = 5.0) -> dict:
    """Startvilkår ved siden av sha-sjekken: ollama svarer på ``/api/tags``.

    Lagt til 29.09.2026 etter avbruddet: ollama-tjenesten kan stoppe uten kjeden, og da feiler
    kjeden først i kanarien etter at alle forutsetninger er sjekket. Bedre å nekte før start."""
    import urllib.error
    import urllib.request
    try:
        with urllib.request.urlopen(f"{vert.rstrip('/')}/api/tags", timeout=tidsavbrudd) as r:
            modeller = [m.get("name") for m in json.load(r).get("models", [])]
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise GjenopptakNekt(f"ollama svarer ikke på {vert}/api/tags ({e}); start `ollama serve` "
                             f"frikoblet før gjenopptak") from e
    return {"vert": vert, "modeller": len(modeller)}


def sjekk_sandkasse(worktree: Path, vault: Path, navn: str = "fase3-kjede") -> str:
    """``data`` i worktreet må være en ekte katalog innenfor Vault, og kjøringens katalog likeså.

    Lagt til 30.09.2026: ``data`` var en symlenke til repoets ``data/``, utenfor katalogene en
    ``claude -p``-instans får lese og skrive (arbeidskatalogen og ``--add-dir`` Vault). Alle 12
    leserøktene ble blokkert fra blindfilene og verdiktfilen, og leddet ble likevel ført som ferdig."""
    d = worktree / "data"
    if d.is_symlink() or not d.is_dir():
        raise GjenopptakNekt(f"{d} er {'en symlenke' if d.is_symlink() else 'ikke en katalog'}; "
                             f"leserinstansene når bare arbeidskatalogen og Vault")
    for sti in (d, d / "kjede" / navn):
        if not sti.resolve().is_relative_to(vault.resolve()):
            raise GjenopptakNekt(f"{sti} ligger utenfor Vault ({sti.resolve()})")
    return str(d)


#: Kjedens ledd i rekkefølge (``ledd.LEDD`` i låsecommiten; testen holder dem like).
LEDD = ("hent", "tekstbiter", "dommer", "ekstraksjon", "union", "blind", "les", "verksniva", "falsify", "register")
ETTER_LES = ("verksniva", "falsify", "register")
#: Klasseverdiene leseroppdraget tillater: H1–H9, <klasse>/H7-uavklart, N1–N3, INGEN.
_KLASSE = re.compile(r"^(H[1-9](/H7-uavklart)?|N[1-3]|INGEN)$")
RC_ETTERKONTROLL = 3


def _rader(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def _ventede(kd: Path, okt: int) -> list[str]:
    return [r["id"] for r in _rader(kd / "blind" / f"blind-okt-{okt}.jsonl")]


def ugyldige_dommer(rader: list[dict]) -> list[str]:
    """Id-er der en leserdom ikke har skjemaets felt, eller der `treff` og klassen sier hver sin ting."""
    ut = []
    for r in rader:
        k = r.get("klasse")
        ok = (isinstance(r.get("treff"), bool) and isinstance(r.get("tvil"), bool)
              and isinstance(r.get("begrunnelse"), str) and bool(r["begrunnelse"].strip())
              and isinstance(k, str) and bool(_KLASSE.match(k)) and r["treff"] == k.startswith("H"))
        if not ok:
            ut.append(str(r.get("id")))
    return ut


def verdiktstatus(kd: Path, okter: list[int]) -> dict[int, dict]:
    """Hver økts verdiktfil mot blindfila: ``mangler`` (ingen fil, eller tom), ``komplett`` (samme id-er i
    samme rekkefølge), ``delvis`` (et ekte prefiks) eller ``korrupt`` (alt annet)."""
    ut = {}
    for n in okter:
        ventede = _ventede(kd, n)
        f = kd / f"7-verdikter-okt-{n}.jsonl"
        fikk = [r.get("id") for r in _rader(f)] if f.is_file() else []
        if not fikk:
            s = "mangler"
        elif fikk == ventede:
            s = "komplett"
        elif fikk == ventede[:len(fikk)]:
            s = "delvis"
        else:
            s = "korrupt"
        ut[n] = {"status": s, "dømt": len(fikk), "ventet": len(ventede)}
    return ut


def fotavtrykk(kd: Path) -> dict[str, dict]:
    """Bytes og sha256 for hver eksisterende verdiktfil — det som ikke får skrives om."""
    ut = {}
    for f in sorted(kd.glob("7-verdikter-okt-*.jsonl")):
        b = f.read_bytes()
        ut[f.name] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    return ut


def overskrevet(kd: Path, før: dict[str, dict]) -> list[str]:
    """Verdiktfiler der de første bytene ikke lenger er de samme som før kallet. Forlenget er lov."""
    ut = []
    for navn, fa in før.items():
        f = kd / navn
        if not f.is_file():
            ut.append(f"{navn}: forsvant")
            continue
        b = f.read_bytes()
        if len(b) < fa["bytes"] or hashlib.sha256(b[:fa["bytes"]]).hexdigest() != fa["sha256"]:
            ut.append(f"{navn}: de første {fa['bytes']} bytene er endret")
    return ut


def _valider_mot(skjema: Path, rad: dict) -> str | None:
    from jsonschema import Draft202012Validator
    feil = sorted(Draft202012Validator(json.loads(skjema.read_text(encoding="utf-8"))).iter_errors(rad),
                  key=lambda e: list(e.absolute_path))
    return feil[0].message if feil else None


def etterkontroll(kd: Path, ledd: list[str] | tuple[str, ...], *, skjemaer: Path | None = None) -> list[str]:
    """Hvert ledd i ``ledd`` må ha ikke-tomme, gyldige utdata i fullt antall og være ført etter leddet det bygger
    på. Returnerer det som mangler, hver linje med leddets navn først; tom liste er bestått.

    ``skjemaer`` er katalogen med utgangsskjemaene; den låste commitens egne brukes for registeret."""
    t = json.loads((kd / "tilstand.json").read_text(encoding="utf-8"))
    L = t.get("ledd", {})
    mangler: list[str] = []

    def m(navn: str, tekst: str) -> None:
        mangler.append(f"{navn}: {tekst}")

    def antall(navn: str, fil: str, ventet) -> int | None:
        p = kd / fil
        if not p.is_file():
            m(navn, f"{fil} finnes ikke")
            return None
        n = sum(1 for l in p.read_text(encoding="utf-8").splitlines() if l.strip())
        if n == 0:
            m(navn, f"{fil} er tom")
        elif ventet is not None and n != int(ventet):
            m(navn, f"{fil} har {n} rader, ventet {ventet}")
        return n

    for navn in ledd:
        if navn not in L:
            m(navn, "ikke ført i tilstand.json")
            continue
        if navn == "hent":
            antall(navn, "1-hentet.jsonl", L["hent"].get("verk"))
        elif navn == "tekstbiter":
            antall(navn, "2-tekstbiter.jsonl", L["tekstbiter"].get("tekstbiter"))
        elif navn == "dommer":
            antall(navn, "3-dommer.jsonl", (L.get("tekstbiter") or {}).get("tekstbiter"))
        elif navn == "ekstraksjon":
            antall(navn, "4-ekstraksjon.jsonl", L["ekstraksjon"].get("vinduer"))
        elif navn == "union":
            antall(navn, "5-union.jsonl", L["union"].get("union"))
        elif navn == "blind":
            b = L["blind"]
            n = sum(antall(navn, f"blind/blind-okt-{ø['okt']}.jsonl", None) or 0 for ø in b["per_okt"])
            if n != int(b.get("union") or 0):
                m(navn, f"blindfilene har {n} tekstbiter, unionen {b.get('union')}")
        elif navn == "les":
            okter = [ø["okt"] for ø in L["blind"]["per_okt"]]
            for n, s in verdiktstatus(kd, okter).items():
                if s["status"] != "komplett":
                    m(navn, f"økt {n} {s['status']}: {s['dømt']} av {s['ventet']}")
                else:
                    ug = ugyldige_dommer(_rader(kd / f"7-verdikter-okt-{n}.jsonl"))
                    if ug:
                        m(navn, f"økt {n}: {len(ug)} ugyldige dommer, første {ug[0]}")
        elif navn == "verksniva":
            antall(navn, "7b-verksniva.jsonl", L["hent"].get("verk"))
        elif navn == "falsify":
            p = kd / "7c-falsifisering.json"
            if not p.is_file():
                m(navn, "7c-falsifisering.json finnes ikke")
            elif not (json.loads(p.read_text(encoding="utf-8")) or {}).get("rader"):
                m(navn, "7c-falsifisering.json har ingen rader")
        elif navn == "register":
            n = antall(navn, "8-register.jsonl", None)
            h = kd / "8-register-header.json"
            if not h.is_file():
                m(navn, "8-register-header.json finnes ikke")
            else:
                hode = json.loads(h.read_text(encoding="utf-8"))
                if n is not None and hode.get("n_rader") != n:
                    m(navn, f"hodet sier {hode.get('n_rader')} rader, fila har {n}")
                if skjemaer and (feil := _valider_mot(skjemaer / "registerhode.schema.json", hode)):
                    m(navn, f"hodet bryter registerhode-skjemaet: {feil}")
            if skjemaer and n:
                for r in _rader(kd / "8-register.jsonl"):
                    if feil := _valider_mot(skjemaer / "kandidat.schema.json", r):
                        m(navn, f"{r.get('candidate_id')} bryter kandidat-skjemaet: {feil}")
                        break
    # Ferskhet: et ledd ført ferdig før leddet det bygger på, er regnet på gamle inndata.
    for a, b in zip(LEDD, LEDD[1:]):
        ta, tb = (L.get(a) or {}).get("tid"), (L.get(b) or {}).get("tid")
        if b in ledd and ta and tb and tb < ta:
            m(b, f"ført {tb}, før inndataleddet {a} ({ta}) — foreldet")
    return mangler


def planlegg(fra: str | None, om: bool) -> list[tuple[list[str], list[str]]]:
    """Kallene en gjenopptakelse består av: (argumenter til ``run``, leddene etterkontrollen dekker).

    Et spenn som når ``les``, deles: først fram til og med ``les`` (``--om`` bare om det er bedt om), så
    ``verksniva``–``register`` med **tvungen** ``--om``, fordi de er regnet på leserens utdata."""
    fra = fra or LEDD[0]
    if fra not in LEDD:
        raise GjenopptakNekt(f"ukjent ledd {fra!r}; gyldige er {', '.join(LEDD)}")
    i, j = LEDD.index(fra), LEDD.index("les")
    if i > j:
        return [(["--from", fra, "--om"], list(LEDD[i:]))]
    første = ["--from", fra, "--to", "les"] + (["--om"] if om else [])
    return [(første, list(LEDD[:j + 1])), (["--from", ETTER_LES[0], "--om"], list(LEDD))]


def rest_oppdrag(oppdrag: str, *, okt: int, ventet: int, rest: int, k: int) -> str:
    """Oppdraget for økt ``okt`` omskrevet til de ``rest`` udømte: bare blindfil, utfil, kladdekatalog og
    antall byttes. Alt annet — regler, sperreliste, utdataform — står ordrett."""
    ut = oppdrag
    bytt = [(f"blind/blind-okt-{okt}.jsonl", f"fullforing/okt-{okt}-rest{k}/blind.jsonl"),
            (f"fase3-kjede/7-verdikter-okt-{okt}.jsonl", f"fase3-kjede/fullforing/okt-{okt}-rest{k}/verdikter.jsonl"),
            (f"kladd/okt-{okt}/", f"kladd/okt-{okt}-rest{k}/"),
            (f"Les {ventet} blindede", f"Les {rest} blindede"),
            (f"— {ventet} linjer", f"— {rest} linjer"),
            (f"Når alle {ventet} ", f"Når alle {rest} "),
            (f"Gå gjennom alle {ventet} ", f"Gå gjennom alle {rest} ")]
    for gml, ny in bytt:
        if gml not in ut:
            raise GjenopptakNekt(f"oppdraget for økt {okt} inneholder ikke «{gml}»; rest-oppdraget bygges ikke")
        ut = ut.replace(gml, ny)
    if re.search(rf"\b{ventet}\b", ut):
        raise GjenopptakNekt(f"rest-oppdraget nevner fortsatt {ventet}")
    return ut


def _cc_økt(wt: Path, vault: Path, oppdrag: str, utfil: Path) -> dict:
    """Én leserøkt med den låste ``CCLeser`` importert fra worktreet — samme kall som kjedens leserledd."""
    import tomllib
    with (wt / "kjede.toml").open("rb") as fh:
        modell = str(tomllib.load(fh)["leser"]["modell"])
    kode = ("import json,sys; from pathlib import Path; from gjenopptak.kjede.leser import CCLeser; "
            "a=json.load(sys.stdin); print(json.dumps(CCLeser(modell=a['m'], rot=Path(a['r']), "
            "ekstra_kataloger=(Path(a['v']),)).kjør_økt(a['o'], Path(a['u'])), ensure_ascii=False, default=str))")
    r = subprocess.run([sys.executable, "-c", kode], cwd=wt, env={**os.environ, "PYTHONPATH": str(wt / "src")},
                       input=json.dumps({"m": modell, "r": str(wt), "v": str(vault), "o": oppdrag, "u": str(utfil)}),
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise GjenopptakNekt(f"leserøkta feilet: {r.stderr[-400:]}")
    return {"modell": modell, **json.loads(r.stdout.strip().splitlines()[-1])}


def fullfør_økt(kd: Path, okt: int, *, kjør=None) -> dict:
    """Fullfør de udømte i en delvis økt i **én ny instans**, serielt (ADDENDUM-25 § 8, som ADDENDUM-22 § 10).

    Restinstansen får samme oppdrag med egen blindfil, utfil og kladdekatalog under ``fullforing/``, utenfor
    mønstrene ``7-verdikter-okt-*.jsonl`` og ``blind/blind-okt-*.jsonl`` som målingen leser. Den gyldige
    delen av restens dommer — et prefiks av de udømte, id for id — føyes til verdiktfila; de dømte står.
    ``kjør(oppdrag, utfil) -> bruk`` er selve økta (injiseres i testene)."""
    f = kd / f"7-verdikter-okt-{okt}.jsonl"
    s = verdiktstatus(kd, [okt])[okt]
    if s["status"] != "delvis":
        raise GjenopptakNekt(f"økt {okt} er {s['status']} ({s['dømt']} av {s['ventet']}); bare en delvis økt fullføres")
    dømte = _rader(f)
    if ug := ugyldige_dommer(dømte):
        raise GjenopptakNekt(f"økt {okt} har {len(ug)} ugyldige dommer blant de dømte; første {ug[0]}")
    blind = _rader(kd / "blind" / f"blind-okt-{okt}.jsonl")
    rest = blind[len(dømte):]
    k = 1 + len(list((kd / "fullforing").glob(f"okt-{okt}-rest*")))
    rd = kd / "fullforing" / f"okt-{okt}-rest{k}"
    rd.mkdir(parents=True)
    (rd / "blind.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rest), encoding="utf-8")
    oppdrag = rest_oppdrag((kd / "blind" / f"oppdrag-okt-{okt}.md").read_text(encoding="utf-8"),
                           okt=okt, ventet=len(blind), rest=len(rest), k=k)
    (rd / "oppdrag.md").write_text(oppdrag, encoding="utf-8")
    før = f.read_bytes()
    logg = {"tid": datetime.now(timezone.utc).isoformat(timespec="seconds"), "okt": okt, "rest": k,
            "dømt_før": len(dømte), "udømte": len(rest), "verdikter_før_sha256": hashlib.sha256(før).hexdigest(),
            "blind_sha256": sha256(rd / "blind.jsonl"), "oppdrag_sha256": sha256(rd / "oppdrag.md")}
    utfil = rd / "verdikter.jsonl"
    logg["bruk"] = kjør(oppdrag, utfil)
    nye = _rader(utfil) if utfil.is_file() else []
    gyldige = []
    for r, b in zip(nye, rest):
        if r.get("id") != b["id"] or ugyldige_dommer([r]):
            break
        gyldige.append(r)
    if f.read_bytes() != før:
        raise GjenopptakNekt(f"{f.name} ble endret mens restinstansen kjørte; ingenting føyes til")
    tmp = f.with_suffix(".jsonl.tmp")
    tmp.write_bytes(før + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in gyldige).encode("utf-8"))
    os.replace(tmp, f)
    etter = f.read_bytes()
    assert etter[:len(før)] == før
    logg |= {"skrevet_av_rest": len(nye), "føyd_til": len(gyldige), "dømt_etter": len(dømte) + len(gyldige),
             "ventet": len(blind), "verdikter_etter_sha256": hashlib.sha256(etter).hexdigest(),
             "status": verdiktstatus(kd, [okt])[okt]["status"]}
    (rd / "logg.json").write_text(json.dumps(logg, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    return logg


def sjekk(*, vault: Path | None = None) -> dict:
    vault = vault or require_vault()
    wt = vault / WORKTREE
    if not (wt / ".git").exists():
        raise GjenopptakNekt(f"worktreet finnes ikke: {wt} (git worktree add --detach {wt} {LÅS})")
    lås = _git("rev-parse", LÅS)
    head = _git("rev-parse", "HEAD", cwd=wt)
    if head != lås:
        raise GjenopptakNekt(f"worktreets HEAD {head[:12]} er ikke låsecommiten {lås[:12]}")
    endret = _git("status", "--porcelain", "--untracked-files=no", cwd=wt)
    if endret:
        raise GjenopptakNekt(f"sporede filer er endret i worktreet:\n{endret}")
    tabell = låst_tabell(_git("show", f"{lås}:{ADDENDUM}"))
    avvik = sjekk_sha(wt, tabell)
    if avvik:
        raise GjenopptakNekt("sha256 avviker fra ADDENDUM-25 § 9: " + "; ".join(avvik))
    imp = subprocess.run([sys.executable, "-c", "import gjenopptak; print(gjenopptak.__file__)"],
                         capture_output=True, text=True, env={**os.environ, "PYTHONPATH": str(wt / "src")},
                         cwd=wt).stdout.strip()
    if not imp.startswith(str(wt)):
        raise GjenopptakNekt(f"gjenopptak importeres fra {imp}, ikke fra worktreet")
    fase3 = vault / VAULT_FASE3
    sandkasse = sjekk_sandkasse(wt, vault)
    ollama = krev_ollama(ollama_vert(wt))
    rp = RP.sjekk(fase3 / "utvalg-fase3-arkeologi.jsonl", vault / "MANIFEST-VAULT.md")
    if rp is None:
        raise GjenopptakNekt("materialet erklærer ikke noe referansesett — feil utvalg?")
    return {"worktree": str(wt), "lås": lås, "filer_sjekket": len(tabell),
            "cli_sha256": tabell["src/gjenopptak/kjede/cli.py"], "import": imp,
            "referanseport": rp, "ollama": ollama, "sandkasse": sandkasse, "kjører_allerede": kjører_allerede("fase3-kjede")}


def _nå() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _logg(fase3: Path, rad: dict) -> None:
    with (fase3 / "gjenopptak-logg.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rad, ensure_ascii=False, default=str) + "\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--sjekk", action="store_true", help="bare sjekkene; start ingenting")
    p.add_argument("--fra", help="første ledd som kjøres (sendes som --from); ført i loggen")
    p.add_argument("--om", action="store_true", help="kjør ledd fram til og med les om selv om de er ført ferdige")
    p.add_argument("--fullfor-okt", type=int, metavar="N",
                   help="fullfør de udømte i den delvise leserøkta N i én ny instans, og stopp")
    a = p.parse_args(argv)
    try:
        s = sjekk()
    except (GjenopptakNekt, RP.ReferansePortFeil) as e:
        print(f"GJENOPPTAK NEKTET: {e}", file=sys.stderr)
        return 2
    print(json.dumps({k: v for k, v in s.items() if k != "referanseport"}, ensure_ascii=False, indent=1))
    if a.sjekk:
        return 0
    if s["kjører_allerede"]:
        print(f"GJENOPPTAK NEKTET: kjøringen går allerede: {s['kjører_allerede']}", file=sys.stderr)
        return 2
    wt = Path(s["worktree"])
    vault = wt.parents[1]
    fase3 = vault / VAULT_FASE3
    navn = KJØRING[KJØRING.index("--navn") + 1]
    kd = wt / "data" / "kjede" / navn
    skjemaer = wt / "src" / "gjenopptak" / "schemas"
    if a.fullfor_okt is not None:
        try:
            r = fullfør_økt(kd, a.fullfor_okt, kjør=lambda o, u: _cc_økt(wt, vault, o, u))
        except GjenopptakNekt as e:
            print(f"FULLFØRING NEKTET: {e}", file=sys.stderr)
            return 2
        _logg(fase3, {"fullføring": {k: v for k, v in r.items() if k != "bruk"}, "lås": s["lås"]})
        print(json.dumps({k: v for k, v in r.items() if k != "bruk"}, ensure_ascii=False, indent=1))
        return 0 if r["status"] == "komplett" else RC_ETTERKONTROLL
    try:
        plan = planlegg(a.fra, a.om)
    except GjenopptakNekt as e:
        print(f"GJENOPPTAK NEKTET: {e}", file=sys.stderr)
        return 2
    t = json.loads((kd / "tilstand.json").read_text(encoding="utf-8"))
    okter = [ø["okt"] for ø in ((t["ledd"].get("blind") or {}).get("per_okt") or [])]
    if any("--to" in args for args, _ in plan):
        stå = {n: x for n, x in verdiktstatus(kd, okter).items() if x["status"] in ("delvis", "korrupt")}
        if stå:
            print("GJENOPPTAK NEKTET: leserleddet ville skrevet over dømte tekstbiter — "
                  + "; ".join(f"økt {n} {x['status']} ({x['dømt']} av {x['ventet']})" for n, x in stå.items())
                  + ". Fullfør med --fullfor-okt N først.", file=sys.stderr)
            return 2
    før = fotavtrykk(kd)
    kopi = fase3 / f"tilstand-foer-gjenopptak-{_nå().replace(':', '')}.json"
    kopi.write_bytes((kd / "tilstand.json").read_bytes())
    _logg(fase3, {"tid": _nå(), "lås": s["lås"], "cli_sha256": s["cli_sha256"], "filer_sjekket": s["filer_sjekket"],
                  "nøkkel_sha256": s["referanseport"]["nøkkel_sha256"], "plan": [x for x, _ in plan],
                  "tilstand_før": {"fil": kopi.name, "sha256": sha256(kopi)}, "verdiktfiler_før": før})
    grunn = [x.format(fase3=fase3) for x in KJØRING]
    with (fase3 / "kjede.log").open("a", encoding="utf-8") as fh:
        fh.write(f"\ngjenopptatt {_nå()} fra worktree {wt} på {s['lås'][:12]}, cli.py {s['cli_sha256'][:16]}…\n")
        for args, dekker in plan:
            fh.write(f"kall: run {' '.join(args)}\n")
            fh.flush()
            r = subprocess.run([sys.executable, "-m", "gjenopptak.kjede.cli", "--konfig", str(wt / "kjede.toml"),
                                "run", *grunn, *args], cwd=wt, env={**os.environ, "PYTHONPATH": str(wt / "src")},
                               stdout=fh, stderr=subprocess.STDOUT)
            fh.write(f"slutt rc={r.returncode} {_nå()}\n")
            mangler = overskrevet(kd, før) + etterkontroll(kd, dekker, skjemaer=skjemaer)
            if mangler or r.returncode:
                fh.write("ETTERKONTROLL STOPPET:\n" + "".join(f"  {x}\n" for x in mangler))
                _logg(fase3, {"tid": _nå(), "kall": args, "rc": r.returncode, "etterkontroll": mangler})
                print(f"ETTERKONTROLL STOPPET etter run {' '.join(args)} (rc {r.returncode}):", file=sys.stderr)
                for x in mangler:
                    print(f"  {x}", file=sys.stderr)
                return r.returncode or RC_ETTERKONTROLL
            _logg(fase3, {"tid": _nå(), "kall": args, "rc": 0, "etterkontroll": "bestått", "ledd": dekker})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
