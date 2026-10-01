"""Bygg en Zenodo-versjon som utkast på Vault — og stopp der.

    python -m gjenopptak.utgivelse --versjon 0.4.0 --forrige 22976464
    python -m gjenopptak.utgivelse --versjon 0.4.0 --forrige 22976464 --bare-filkart

Modulen **publiserer ikke** og kaller ikke Zenodos skrive-API. Publisering er irreversibel og
autoriseres av eieren på grønne porter (docs/ZENODO.md). Det eneste nettkallet er et lesekall
mot den publiserte forrige versjonen, for filkartet.

Bakgrunnen for filkartet står i docs/ZENODO.md (0.2.1): en publisert post kan ikke bytte fil, og
`CITATION.cff` i 0.2.0 var foreldet fordi den ikke ble lastet opp på nytt. Kartet mot forrige
versjon er porten som fanger det.

**Hva som holdes utenfor**, som beslutning og ikke som tilfeldighet (LISENSAUDIT-2026-09-28 § 4 C):
fulltekster og tekstbiter. Blindfilene er tekstbiter, så de deponeres som **indeks** — id, verk,
spenn, felt og sha256 av teksten — ikke som tekst. Hele blindfilens sha256 står i indeksen, slik at
den kan etterprøves mot Vault-kopien.

Zenodos fillister er flate. Kataloger flates til navn med bindestrek (``docs/decisions/0001-x.md``
blir ``decisions-0001-x.md``), og filgrupper som ikke gir mening enkeltvis, legges i zip.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .vault import VaultUnavailable, require_vault, sha256_file

REPO = Path(__file__).resolve().parents[2]
UTKAST_KATALOG = "zenodo"

#: Repo-sporede dokumenter i depositumet. Katalogene flates; ``docs/patch/`` holdes utenfor fordi
#: den bærer MASTER-interne instrukser, ikke studiens dokumentasjon.
REPO_MØNSTRE = ("PREREG-v1.md", "ADDENDUM-*.md", "README.md", "CITATION.cff", "LICENSE",
                "LICENSE-DATA", "docs/*.md", "docs/decisions/*.md", "docs/saker/**/*.md")
REPO_UTENFOR = ("docs/patch/",)

#: Ekskluderingslisten, versjonert. Oppgis i release notes for versjonen som bygges. Et mønster med
#: ``**`` dekker alle underkataloger. ``MANUSKRIPT-v2*-UTKAST.md`` er unntatt for den nyeste: bare det
#: siste utkastet (høyest versjonsnummer) deponeres.
UTELATT_VERSJON = "1 (29.09.2026, eierens avgjørelse)"
UTELATT = ("docs/INSTRUKSER-*.md", "docs/patch/**", "ROADMAP.md", "docs/ROADMAP.md",
           "docs/BYGGEPLAN.md", "docs/MANUSKRIPT-v2*-UTKAST.md")
NYESTE_UNNTATT = "docs/MANUSKRIPT-v2*-UTKAST.md"

#: Filer i repoet som ikke er dokumenter, men som en låst måling leste eller som depositumet
#: tidligere har båret.
REPO_EKSTRA = {
    "claims.jsonl": "data/register/claims.jsonl",
}

#: Inndata som bare finnes på Vault. (flatt navn, sti relativ til gjenopptak-kilder/)
VAULT_FILER = (
    ("koder2-koderegler-gjenvunnet.md", "koder2/koderegler-gjenvunnet.md"),
    ("arbeidsliste-oppdrag-koder-c.md", "arbeidsliste/oppdrag-koder-c.md"),
    ("oppdrag-koder2-ADDENDUM-11.md", "oppdrag-gjenvunnet/oppdrag-koder2-ADDENDUM-11.md"),
    ("oppdrag-presisjon-100-ADDENDUM-23.md", "oppdrag-gjenvunnet/oppdrag-presisjon-100-ADDENDUM-23.md"),
    ("oppdrag-presisjon-rest-ADDENDUM-23.md", "oppdrag-gjenvunnet/oppdrag-presisjon-rest-ADDENDUM-23.md"),
    ("oppdrag-gjenvunnet-OPPHAV.md", "oppdrag-gjenvunnet/OPPHAV.md"),
    ("MANIFEST-VAULT.md", "MANIFEST-VAULT.md"),
    # 30.09.2026: originalen bar 16 ordrette passasjeutdrag; depositumet får versjonen uten tekst (sha256 i stedet).
    ("koder2-sammenlikning-uten-tekst.json", "presisjonssett/koder2-sammenlikning-uten-tekst.json"),
    ("port-presisjonssett-verdikter-koder2.jsonl", "presisjonssett/port-presisjonssett-verdikter-koder2.jsonl"),
    # Fase 3 (ADDENDUM-25), lagt til 30.09.2026: utfallet og det som skal til for å regne det om — uten tekstbiter.
    ("fase3-maaling.json", "fase3/maaling-fase3.json"),
    ("fase3-rapport.json", "fase3/rapport-fase3.json"),
    ("fase3-register.jsonl", "fase3-kjede/8-register.jsonl"),
    ("fase3-register-header.json", "fase3-kjede/8-register-header.json"),
    ("fase3-referanse-nokkel.jsonl", "fase3/referanse/NOKKEL-referansesett.jsonl"),
    ("fase3-oppdrag-presisjon.md", "fase3/presisjon/oppdrag-presisjon.md"),
    ("fase3-presisjon-nokkel.jsonl", "fase3/presisjon/nokkel-presisjon.jsonl"),
    ("fase3-presisjon-verdikter.jsonl", "fase3/presisjon/verdikter-presisjon.jsonl"),
    ("fase3-modell-fra-utskrifter.json", "fase3/utskrifter/modell-fra-utskrifter.json"),
    # Nøkkelregelen (eierens avgjørelse 30.09.2026): en nøkkel holdes utenfor til målingen den blinder er ferdig
    # og rapportert, og deponeres deretter. Port-320-nøkkelen (presisjonssett/) holdes ute: ADDENDUM-21 (koder 3)
    # er preregistrert og ukjørt på samme blindfil.
    ("arbeidsliste-nokkel.jsonl", "arbeidsliste/nokkel.jsonl"),
    ("arbeidsliste-presisjon-100-nokkel.json", "arbeidsliste/presisjon-100-nokkel.json"),
    ("fase3-kjede-nokkel.jsonl", "fase3-kjede/nokkel.jsonl"),
)

#: Fase 3s kjøringskatalog på Vault (relativ til gjenopptak-kilder/): leserens verdikter pakkes som zip.
FASE3_KJØRING = "fase3/worktree-f19a3e3/data/kjede/fase3-kjede"

#: Blindfiler som deponeres som indeks. (navn i indeksen, blindfil, nøkkelfil, nøkkelformat)
BLINDFILER = (
    ("port-320", "presisjonssett/port-presisjonssett-blind.jsonl",
     "presisjonssett/port-presisjonssett-nokkel.jsonl"),
    *((f"arbeidsliste-okt-{i}", f"arbeidsliste/blind/blind-okt-{i}.jsonl", "arbeidsliste/nokkel.jsonl")
      for i in range(1, 9)),
    *((f"arbeidsliste-okt-{i}-rest", f"arbeidsliste/blind/blind-okt-{i}-rest.jsonl", "arbeidsliste/nokkel.jsonl")
      for i in (2, 3, 4, 6, 7)),
    ("arbeidsliste-presisjon-100", "arbeidsliste/blind/blind-presisjon-100.jsonl", "arbeidsliste/nokkel.jsonl"),
    ("arbeidsliste-presisjon-rest", "arbeidsliste/blind/blind-presisjon-rest.jsonl", "arbeidsliste/nokkel.jsonl"),
    *((f"fase3-okt-{i}", f"{FASE3_KJØRING}/blind/blind-okt-{i}.jsonl", "fase3-kjede/nokkel.jsonl")
      for i in range(1, 13)),
    *((f"fase3-okt-{i}-rest1", f"{FASE3_KJØRING}/fullforing/okt-{i}-rest1/blind.jsonl", "fase3-kjede/nokkel.jsonl")
      for i in (3, 7)),
    ("fase3-presisjon-100", "fase3/presisjon/blind-presisjon.jsonl", "fase3/presisjon/nokkel-presisjon.jsonl"),
)


#: Zenodo tillater høyst 100 filer per post (avvist ved opplasting av v0.4.0, 01.10.2026: «exceeding the max amount
#: per record»). Byggeren nekter derfor et utkast over grensen.
MAKS_FILER = 100

#: Grupper som deponeres som én zip med katalogstrukturen bevart, fordi Zenodos fillister er flate og har tak.
#: Bare grupper som er nye i v0.4.0, så filkartet mot v0.3.0 ikke endres for filer som alt er deponert.
#: (zip-navn, predikat over (kilde, flatt navn), navn inni zip)
def _i_zip(kilde: str, navn: str) -> tuple[str, str] | None:
    rel = kilde.split(":", 2)[2] if kilde.startswith("git:") else None
    if rel and rel.startswith("docs/saker/"):
        return "saker.zip", rel.removeprefix("docs/")
    if rel and Path(rel).match("docs/FAKTASJEKK-MANUSKRIPT-*.md"):
        return "faktasjekk-manuskript.zip", Path(rel).name
    if kilde.startswith("vault:") and (navn.startswith("oppdrag-") or navn in ("arbeidsliste-oppdrag-koder-c.md",
                                                                             "fase3-oppdrag-presisjon.md")):
        return "oppdrag.zip", navn
    return None


class UtgivelseFeil(RuntimeError):
    pass


@dataclass(frozen=True)
class Fil:
    navn: str          # flatt navn i depositumet
    kilde: str         # hvor den kom fra, for manifestet
    bytes: int
    sha256: str
    md5: str


def flatt(rel: str) -> str:
    """``docs/decisions/0001-x.md`` → ``decisions-0001-x.md``; ``docs/saker/SAK-08/LUKKET.md`` →
    ``saker-SAK-08-LUKKET.md``. Toppnivå og ``docs/`` beholder filnavnet."""
    p = Path(rel)
    deler = p.parts
    if deler[0] == "docs":
        deler = deler[1:]
    return "-".join(deler)


def _md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True,
                          check=True).stdout


def _treffer(rel: str, mønster: str) -> bool:
    if mønster.endswith("/**"):
        return rel.startswith(mønster[:-2])
    return fnmatch.fnmatchcase(rel, mønster)


def _versjon(rel: str) -> tuple[int, ...]:
    """``docs/MANUSKRIPT-v2.5-UTKAST.md`` → (2, 5); ``…-v2-UTKAST.md`` → (2,)."""
    m = re.search(r"-v(\d+(?:\.\d+)*)-UTKAST\.md$", rel)
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def utelat(stier: list[str]) -> tuple[list[str], list[str]]:
    """(beholdt, utelatt) etter ``UTELATT``. Det nyeste utkastet under ``NYESTE_UNNTATT`` beholdes."""
    utkast = [r for r in stier if _treffer(r, NYESTE_UNNTATT)]
    nyeste = max(utkast, key=_versjon) if utkast else None
    beholdt, utelatt = [], []
    for rel in stier:
        if rel != nyeste and any(_treffer(rel, m) for m in UTELATT):
            utelatt.append(rel)
        else:
            beholdt.append(rel)
    return beholdt, utelatt


def repo_dokumenter(*, med_utelatt: bool = False):
    """Sporede filer som matcher mønstrene, minus ekskluderingslisten. Fra git, ikke fra disken:
    en usporet fil i arbeidstreet skal ikke kunne gli inn i et depositum."""
    spores = set(_git("ls-files").split("\n")) - {""}
    ut = []
    for rel in sorted(spores):
        if any(rel.startswith(u) for u in REPO_UTENFOR):
            continue
        if any(Path(rel).match(m) or (m.endswith("**/*.md") and rel.startswith(m.split("**")[0])
                                      and rel.endswith(".md")) for m in REPO_MØNSTRE):
            ut.append(rel)
    beholdt, utelatt = utelat(ut)
    return (beholdt, utelatt) if med_utelatt else beholdt


def blindindeks(vault: Path, navn: str, blind_rel: str, nøkkel_rel: str) -> dict:
    """Én blindfil som indeks: ingen tekst, bare plassering og sha256 av teksten."""
    blind = vault / blind_rel
    if not blind.is_file():
        raise UtgivelseFeil(f"blindfilen finnes ikke på Vault: {blind}")
    nøkkel = {}
    for l in (vault / nøkkel_rel).read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            nøkkel[r["id"]] = r
    rader = []
    for l in blind.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        k = nøkkel.get(r["id"])
        if k is None:
            raise UtgivelseFeil(f"{r['id']} i {blind_rel} mangler i nøkkelen {nøkkel_rel}")
        rader.append({"id": r["id"], "doc_id": k["doc_id"], "start_index": k["start_index"],
                      "end_index": k["end_index"], "felt": k.get("felt"),
                      "tekst_sha256": hashlib.sha256(r["tekst"].encode("utf-8")).hexdigest(),
                      "tekst_tegn": len(r["tekst"])})
    return {"navn": navn, "blindfil": blind_rel, "blindfil_sha256": sha256_file(blind),
            "blindfil_bytes": blind.stat().st_size, "nøkkelfil": nøkkel_rel,
            "nøkkelfil_sha256": sha256_file(vault / nøkkel_rel), "rader": len(rader),
            "merk": "Teksten er holdt utenfor (LISENSAUDIT-2026-09-28 § 4 C). Blindfilen ligger "
                    "på Vault og kan etterprøves mot blindfil_sha256.", "indeks": rader}


def forrige_filer(record: str) -> dict[str, dict]:
    """Lesekall mot den publiserte forrige versjonen: {navn: {bytes, md5}}."""
    # venv-Pythonen har ikke systemets CA-lager (TIDSSTEMPEL.md) — samme rot som ots-feilen.
    import ssl
    import certifi
    ktx = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(f"https://zenodo.org/api/records/{record}", timeout=60,
                                context=ktx) as r:
        d = json.load(r)
    return {f["key"]: {"bytes": f["size"], "md5": f["checksum"].removeprefix("md5:")}
            for f in d["files"]} | {"__versjon__": {"bytes": 0, "md5": d["metadata"].get("version")}}


def filkart(nye: list[Fil], forrige: dict[str, dict]) -> dict:
    fv = forrige.pop("__versjon__", {}).get("md5")
    nye_map = {f.navn: f for f in nye}
    uendret = sorted(n for n, f in nye_map.items() if n in forrige and forrige[n]["md5"] == f.md5)
    endret = sorted(n for n, f in nye_map.items() if n in forrige and forrige[n]["md5"] != f.md5)
    ny = sorted(n for n in nye_map if n not in forrige)
    borte = sorted(n for n in forrige if n not in nye_map)
    return {"forrige_versjon": fv, "forrige_antall": len(forrige), "nye_antall": len(nye_map),
            "uendret": uendret, "endret": endret, "ny": ny, "fjernet": borte}


def bygg(versjon: str, forrige: str | None, *, bare_filkart: bool = False) -> dict:
    vault = require_vault()
    ut = vault / UTKAST_KATALOG / f"v{versjon}-utkast"
    if not bare_filkart:
        if ut.exists() and any(ut.iterdir()):
            raise UtgivelseFeil(f"{ut} finnes og er ikke tom — bygg aldri over et utkast. "
                                f"Flytt det bort først.")
        ut.mkdir(parents=True, exist_ok=True)
    status = _git("status", "--porcelain", "--untracked-files=no").strip()
    if status:
        raise UtgivelseFeil(f"arbeidstreet har usikrede endringer i sporede filer:\n{status}")
    head = _git("rev-parse", "HEAD").strip()
    filer: list[Fil] = []

    def legg(navn: str, kilde_sti: Path, kilde: str) -> None:
        if not kilde_sti.is_file():
            raise UtgivelseFeil(f"mangler: {kilde_sti}")
        if any(f.navn == navn for f in filer):
            raise UtgivelseFeil(f"to kilder gir samme flate navn {navn!r}")
        mål = ut / navn
        if not bare_filkart:
            subprocess.run(["cp", "-p", str(kilde_sti), str(mål)], check=True)
            if sha256_file(mål) != sha256_file(kilde_sti):
                raise UtgivelseFeil(f"sha256 avvek etter kopiering av {kilde_sti}")
        p = kilde_sti
        filer.append(Fil(navn, kilde, p.stat().st_size, sha256_file(p), _md5(p)))

    # 1 dokumentene fra git, lest fra HEAD-treet (arbeidstreet er verifisert rent over)
    for rel in repo_dokumenter():
        legg(flatt(rel), REPO / rel, f"git:{head[:12]}:{rel}")
    for navn, rel in REPO_EKSTRA.items():
        kilde = vault / "register" / "claims.jsonl" if not (REPO / rel).is_file() else REPO / rel
        legg(navn, kilde, str(kilde))
    # 2 Vault-inndata
    for navn, rel in VAULT_FILER:
        legg(navn, vault / rel, f"vault:{rel}")
    # 3 byggeartefakter i en egen kladd på Vault (aldri i /tmp: de skal kunne etterprøves)
    bygg_dir = vault / UTKAST_KATALOG / f"v{versjon}-bygg"
    bygg_dir.mkdir(parents=True, exist_ok=True)
    bundle = bygg_dir / "gjenopptak-git-history.bundle"
    if not bare_filkart:
        subprocess.run(["git", "-C", str(REPO), "bundle", "create", str(bundle), "--all"],
                       check=True, capture_output=True)
        tar = bygg_dir / f"gjenopptak-src-{versjon}.tar.gz"
        subprocess.run(["git", "-C", str(REPO), "archive", "--format=tar.gz",
                        f"--prefix=gjenopptak-{versjon}/", "-o", str(tar), "HEAD",
                        "src", "tests", "pyproject.toml", "requirements.txt", "kjede.toml",
                        "felt", "prompts"], check=True)
        otsz = bygg_dir / "ots-kvitteringer.zip"
        ots = sorted((vault / "repo" / "kanon" / "ots").glob("*.ots"))
        with zipfile.ZipFile(otsz, "w", zipfile.ZIP_DEFLATED) as z:
            for o in ots:
                z.write(o, f"ots/{o.name}")
        bi = bygg_dir / "blindfiler-indeks.zip"
        with zipfile.ZipFile(bi, "w", zipfile.ZIP_DEFLATED) as z:
            for navn, b, n in BLINDFILER:
                z.writestr(f"blindfiler-indeks/{navn}.json",
                           json.dumps(blindindeks(vault, navn, b, n), ensure_ascii=False, indent=1) + "\n")
        # Fase 3: leserens verdikter (id, treff, klasse, begrunnelse, tvil — ingen tekst) og fullføringsloggene.
        lv = bygg_dir / "fase3-leser-verdikter.zip"
        kd = vault / FASE3_KJØRING
        verdikter = sorted(kd.glob("7-verdikter-okt-*.jsonl"), key=lambda f: int(f.stem.rsplit("-", 1)[1]))
        with zipfile.ZipFile(lv, "w", zipfile.ZIP_DEFLATED) as z:
            for f in verdikter:
                z.write(f, f"fase3-leser-verdikter/{f.name}")
            for f in sorted((kd / "fullforing").glob("okt-*-rest*/logg.json")):
                z.write(f, f"fase3-leser-verdikter/fullforing-{f.parent.name}-logg.json")
        # Grupper i zip (Zenodos tak): tas ut av lista og pakkes, med innholdet ført i manifestet.
        grupper: dict[str, list[tuple[str, Fil]]] = {}
        for f in list(filer):
            g = _i_zip(f.kilde, f.navn)
            if g:
                grupper.setdefault(g[0], []).append((g[1], f))
                filer.remove(f)
                (ut / f.navn).unlink()
        zipinnhold = {}
        for znavn, medl in sorted(grupper.items()):
            zp = bygg_dir / znavn
            with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
                for arc, f in sorted(medl):
                    kilde = REPO / f.kilde.split(":", 2)[2] if f.kilde.startswith("git:") else vault / f.kilde[6:]
                    z.write(kilde, arc)
            zipinnhold[znavn] = [{"navn": arc, "kilde": f.kilde, "sha256": f.sha256, "bytes": f.bytes}
                                 for arc, f in sorted(medl)]
            legg(znavn, zp, f"bygget: {len(medl)} filer i zip")
        for p, k in ((bundle, "git bundle --all"), (tar, "git archive HEAD"),
                     (otsz, f"{len(ots)} ots-kvitteringer"), (bi, f"{len(BLINDFILER)} blindfiler som indeks"),
                     (lv, f"{len(verdikter)} verdiktfiler fra fase 3s leser")):
            legg(p.name, p, f"bygget: {k}")
    if len(filer) > MAKS_FILER:
        raise UtgivelseFeil(f"{len(filer)} filer, men Zenodo tillater høyst {MAKS_FILER} per post")
    kart = filkart(filer, forrige_filer(forrige)) if forrige else None
    _, utelatt = repo_dokumenter(med_utelatt=True)
    manifest = {"versjon": versjon, "bygget": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "head": head, "utkast": str(ut), "publisert": False,
                "utelatt": {"versjon": UTELATT_VERSJON, "mønstre": list(UTELATT),
                            "unntak": f"nyeste {NYESTE_UNNTATT}", "filer": utelatt},
                "filer": [f.__dict__ for f in filer], "filkart": kart,
                "zipinnhold": locals().get("zipinnhold", {})}
    if not bare_filkart:
        (bygg_dir / f"UTGIVELSE-{versjon}.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--versjon", required=True)
    p.add_argument("--forrige", help="Zenodo-record-ID for forrige versjon (for filkartet)")
    p.add_argument("--bare-filkart", action="store_true", help="ikke kopier, bare regn filkartet")
    a = p.parse_args(argv)
    try:
        m = bygg(a.versjon, a.forrige, bare_filkart=a.bare_filkart)
    except (UtgivelseFeil, VaultUnavailable) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return 3
    print(f"v{m['versjon']}: {len(m['filer'])} filer, HEAD {m['head'][:12]}, utkast {m['utkast']}")
    if m["filkart"]:
        k = m["filkart"]
        print(f"mot {k['forrige_versjon']} ({k['forrige_antall']} filer): "
              f"{len(k['uendret'])} uendret · {len(k['endret'])} endret · {len(k['ny'])} nye · "
              f"{len(k['fjernet'])} fjernet")
    print("IKKE PUBLISERT. Publisering autoriseres av eieren.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
