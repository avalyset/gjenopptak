"""Opplasting og publisering av et bygget utkast til Zenodo.

``utgivelse.py`` bygger utkastet på Vault og rører ikke Zenodo. Denne modulen gjør resten, i fire steg
som kjøres hver for seg, og som hver kan kjøres på nytt uten å gjøre skade:

1. ``reserver``  – oppretter et utkast til ny versjon mot forrige post og skriver utkastets id, bucket og
   reserverte DOI til ``zenodo/zenodo-v<versjon>-tilstand.json`` på Vault. Finnes tilstandsfilen, gjenbrukes
   utkastet. Deretter setter ``fyll`` DOI-en og publiseringsdatoen inn for plassholderne i ``docs/ZENODO.md``,
   ``CITATION.cff`` og release notes (ingen nettkall), endringen committes, og utkastet bygges på nytt før steg 2.
2. ``last-opp``  – gjør fillisten i Zenodo-utkastet lik byggemanifestet: sletter arvede filer som er endret
   eller fjernet, laster opp nye og endrede, lar uendrede stå. Setter versjon og dato i metadata.
3. ``verifiser`` – leser fillisten tilbake og krever samme navn og samme md5 som manifestet, fil for fil.
4. ``publiser``  – **irreversibelt.** Kjører bare når verifiseringen er uten avvik, utkastet på disk fortsatt
   er det manifestet beskriver, og eierens ja er gitt ordrett på kommandolinjen (``--ja "publiser v0.6.0"``).

``plan`` regner ut hva steg 2 vil gjøre, fra byggemanifestets filkart, uten nettkall. Et utkast som fortsatt bærer en
plassholder, eller som ikke fører den reserverte DOI-en, lastes ikke opp og publiseres ikke.

Hvert steg som skriver til Zenodo krever ``--ja``. Nøkkelen leses fra ``~/.config/zenodo.env``
(``ZENODO_TOKEN``); den sendes bare som ``Authorization``-hode, aldri i en URL, og skrives aldri ut, heller
ikke i feilmeldinger. Zenodo tillater 100 filer per post og om lag 133 kall i minuttet; klienten venter
mellom kallene.

All nettferdsel går gjennom ``Klient.send``, som testene bytter med en falsk Zenodo. Modulen er testet uten
nettverk (``tests/test_zenodo.py``).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .utgivelse import MAKS_FILER, UTKAST_KATALOG
from .vault import VaultUnavailable, require_vault, sha256_file

API = "https://zenodo.org/api"
NØKKELFIL = Path.home() / ".config" / "zenodo.env"
NØKKELNAVN = "ZENODO_TOKEN"
#: Zenodo tillater om lag 133 kall i minuttet. 0,6 s mellom kallene gir høyst 100.
PAUSE = 0.6
FORSØK = 4


#: Plassholdere for versjons-DOI og publiseringsdato i dokumentene som beskriver versjonen som bygges. Begge er
#: gyldige etter CFF 1.2.0-skjemaet, så ``CITATION.cff`` validerer også før de er fylt. ``fyll`` setter inn verdiene.
PLASSHOLDER_DOI = "10.5281/zenodo.VERSJONS-DOI-SETTES-VED-PUBLISERING"
PLASSHOLDER_DATO = "9999-12-31"
#: Filene ``fyll`` skriver i, relativt til repoet.
FYLLES = ("docs/ZENODO.md", "CITATION.cff", "docs/RELEASE-NOTES-v{versjon}.md")


class ZenodoFeil(RuntimeError):
    pass


def les_nøkkel(sti: Path = NØKKELFIL) -> str:
    """Verdien av ``ZENODO_TOKEN`` i nøkkelfilen. Verdien skrives aldri ut; feilmeldingen navngir bare filen."""
    if not sti.is_file():
        raise ZenodoFeil(f"nøkkelfilen finnes ikke: {sti}")
    for linje in sti.read_text(encoding="utf-8").splitlines():
        linje = linje.strip().removeprefix("export ").strip()
        if linje.startswith(NØKKELNAVN + "="):
            verdi = linje.split("=", 1)[1].strip().strip("'\"")
            if verdi:
                return verdi
    raise ZenodoFeil(f"{NØKKELNAVN} står ikke i {sti}")


def _urllib_send(metode: str, url: str, hoder: dict[str, str], kropp, lengde: int | None) -> tuple[int, bytes, dict]:
    """Ett HTTP-kall. ``kropp`` er bytes, en åpen fil eller None. Returnerer (status, svar, svarhoder)."""
    h = dict(hoder)
    if lengde is not None:
        h["Content-Length"] = str(lengde)
    forespørsel = urllib.request.Request(url, data=kropp, method=metode, headers=h)
    try:
        with urllib.request.urlopen(forespørsel, timeout=900) as svar:
            return svar.status, svar.read(), dict(svar.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers or {})


@dataclass
class Klient:
    """Zenodos deponerings-API. ``send`` og ``sov`` kan byttes; testene bytter begge."""
    nøkkel: str = field(repr=False)
    api: str = API
    send: Callable = field(default=_urllib_send, repr=False)
    sov: Callable[[float], None] = field(default=time.sleep, repr=False)
    pause: float = PAUSE
    kall_gjort: int = 0

    def kall(self, metode: str, url: str, *, data: dict | None = None, fil: Path | None = None,
             ok: tuple[int, ...] = (200,)) -> dict | list | None:
        if not url.startswith(self.api + "/"):
            raise ZenodoFeil(f"kallet går ikke til {self.api}: {url.split('?')[0]}")
        if "access_token" in url or self.nøkkel in url:
            raise ZenodoFeil("nøkkelen sendes aldri i en URL")
        hoder = {"Authorization": f"Bearer {self.nøkkel}", "Accept": "application/json",
                 "User-Agent": "gjenopptak-zenodo/1 (https://github.com/avalyset/gjenopptak)"}
        for forsøk in range(1, FORSØK + 1):
            self.sov(self.pause)
            self.kall_gjort += 1
            if fil is not None:
                with fil.open("rb") as f:
                    status, svar, svarhoder = self.send(metode, url, hoder | {"Content-Type": "application/octet-stream"},
                                                        f, fil.stat().st_size)
            elif data is not None:
                b = json.dumps(data).encode("utf-8")
                status, svar, svarhoder = self.send(metode, url, hoder | {"Content-Type": "application/json"}, b, len(b))
            else:
                status, svar, svarhoder = self.send(metode, url, hoder, None, None)
            if status in ok:
                return json.loads(svar) if svar.strip() else None
            # 429 og 5xx på lesekall og fil-PUT prøves igjen; POST gjentas aldri (newversion og publish er ikke idempotente)
            if (status == 429 or status >= 500) and metode in ("GET", "PUT", "DELETE") and forsøk < FORSØK:
                self.sov(float({k.lower(): v for k, v in svarhoder.items()}.get("retry-after", 5 * forsøk)))
                continue
            melding = svar[:300].decode("utf-8", "replace").replace(self.nøkkel, "[nøkkel]")
            raise ZenodoFeil(f"{metode} {url.removeprefix(self.api)} ga {status}: {melding}")
        raise ZenodoFeil(f"{metode} {url.removeprefix(self.api)}: ga opp etter {FORSØK} forsøk")


# --- det bygde utkastet -------------------------------------------------------------------------------------------

def manifeststi(vault: Path, versjon: str) -> Path:
    return vault / UTKAST_KATALOG / f"v{versjon}-bygg" / f"UTGIVELSE-{versjon}.json"


def tilstandssti(vault: Path, versjon: str) -> Path:
    return vault / UTKAST_KATALOG / f"zenodo-v{versjon}-tilstand.json"


def les_manifest(vault: Path, versjon: str) -> dict:
    sti = manifeststi(vault, versjon)
    if not sti.is_file():
        raise ZenodoFeil(f"byggemanifestet finnes ikke: {sti}")
    m = json.loads(sti.read_text(encoding="utf-8"))
    if m.get("versjon") != versjon:
        raise ZenodoFeil(f"manifestet er for versjon {m.get('versjon')}, ikke {versjon}")
    navn = [f["navn"] for f in m["filer"]]
    if len(navn) != len(set(navn)):
        raise ZenodoFeil("manifestet har to filer med samme navn")
    if len(navn) > MAKS_FILER:
        raise ZenodoFeil(f"manifestet har {len(navn)} filer; Zenodo tar høyst {MAKS_FILER}")
    return m


def _md5(sti: Path) -> str:
    h = hashlib.md5()  # noqa: S324 – Zenodos egen sjekksum, ikke sikkerhet
    with sti.open("rb") as f:
        for bit in iter(lambda: f.read(1 << 20), b""):
            h.update(bit)
    return h.hexdigest()


def kontroller_utkast(m: dict, utkast: Path | None = None) -> list[str]:
    """Avvik mellom manifestet og filene på disk: mangler, overskytende, feil størrelse, feil md5 eller sha256."""
    ut = utkast or Path(m["utkast"])
    avvik = []
    ventet = {f["navn"]: f for f in m["filer"]}
    finnes = {p.name for p in ut.iterdir() if p.is_file()} if ut.is_dir() else set()
    avvik += [f"mangler på disk: {n}" for n in sorted(set(ventet) - finnes)]
    avvik += [f"på disk, ikke i manifestet: {n}" for n in sorted(finnes - set(ventet))]
    for n in sorted(set(ventet) & finnes):
        p, f = ut / n, ventet[n]
        if p.stat().st_size != f["bytes"]:
            avvik.append(f"feil størrelse: {n}")
        elif _md5(p) != f["md5"] or sha256_file(p) != f["sha256"]:
            avvik.append(f"feil sjekksum: {n}")
    return avvik


def plassholdere(m: dict, utkast: Path | None = None) -> list[str]:
    """Dokumenter i utkastet som fortsatt bærer en plassholder for DOI eller dato. Skal være tom før opplasting."""
    ut = utkast or Path(m["utkast"])
    funn = []
    for f in sorted(m["filer"], key=lambda f: f["navn"]):
        p = ut / f["navn"]
        if p.suffix in (".md", ".cff") and p.is_file():
            t = p.read_text(encoding="utf-8", errors="replace")
            if PLASSHOLDER_DOI in t or PLASSHOLDER_DATO in t:
                funn.append(f"plassholder ikke fylt: {f['navn']}")
    return funn


def doi_ført(m: dict, t: dict, utkast: Path | None = None) -> list[str]:
    """``ZENODO.md`` i utkastet skal føre DOI-en Zenodo reserverte. Har utkastet ingen ``ZENODO.md``, er det ikke et avvik."""
    p = (utkast or Path(m["utkast"])) / "ZENODO.md"
    if not p.is_file() or t["doi"] in p.read_text(encoding="utf-8", errors="replace"):
        return []
    return [f"ZENODO.md fører ikke den reserverte DOI-en {t['doi']}"]


def fyll(repo: Path, versjon: str, doi: str, dato: str) -> dict[str, int]:
    """Sett versjons-DOI og publiseringsdato inn for plassholderne i repoet. Ingen nettkall. Returnerer antall per fil."""
    if not re.fullmatch(r"10\.5281/zenodo\.\d+", doi):
        raise ZenodoFeil(f"ikke en Zenodo-DOI: {doi}")
    if not re.fullmatch(r"20\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])", dato):
        raise ZenodoFeil(f"datoen skal være ÅÅÅÅ-MM-DD: {dato}")
    fylt = {}
    for mønster in FYLLES:
        p = repo / mønster.format(versjon=versjon)
        if not p.is_file():
            raise ZenodoFeil(f"finnes ikke: {p}")
        t = p.read_text(encoding="utf-8")
        n = t.count(PLASSHOLDER_DOI) + t.count(PLASSHOLDER_DATO)
        if n:
            p.write_text(t.replace(PLASSHOLDER_DOI, doi).replace(PLASSHOLDER_DATO, dato), encoding="utf-8")
        fylt[str(p.relative_to(repo))] = n
    if not any(fylt.values()):
        raise ZenodoFeil("ingen plassholder igjen i " + ", ".join(fylt))
    return fylt


def utkast_sha256(m: dict) -> str:
    """Én sha256 for hele utkastet: over linjene «sha256  navn», sortert på navn. Samme filer gir samme verdi."""
    linjer = "".join(f"{f['sha256']}  {f['navn']}\n" for f in sorted(m["filer"], key=lambda f: f["navn"]))
    return hashlib.sha256(linjer.encode("utf-8")).hexdigest()


# --- planen -------------------------------------------------------------------------------------------------------

def _md5_av(sjekksum: str | None) -> str:
    return (sjekksum or "").removeprefix("md5:")


def plan(m: dict, fjernfiler: list[dict]) -> dict[str, list]:
    """Hva som må til for at fillisten i Zenodo-utkastet skal bli lik manifestet.

    ``fjernfiler`` er svaret fra ``GET …/files``: ``filename``, ``checksum`` (md5) og ``id``. En fil med samme navn
    og samme md5 står. En fil med samme navn og annen md5 slettes og lastes opp. En fil som ikke er i manifestet,
    slettes.
    """
    ventet = {f["navn"]: f["md5"] for f in m["filer"]}
    der: dict[str, list[dict]] = {}
    for f in fjernfiler:
        der.setdefault(f["filename"], []).append(f)
    slett, behold = [], []
    for navn, forekomster in sorted(der.items()):
        like = [f for f in forekomster if navn in ventet and _md5_av(f.get("checksum")) == ventet[navn]]
        if like:
            behold.append(navn)
        slett += [{"navn": navn, "id": f["id"]} for f in forekomster if f is not (like[0] if like else None)]
    last_opp = sorted(n for n in ventet if n not in behold)
    return {"slett": slett, "last_opp": last_opp, "behold": behold}


def plan_fra_filkart(m: dict) -> dict[str, list]:
    """Samme plan regnet fra byggemanifestets filkart mot forrige publiserte versjon. Ingen nettkall."""
    k = m.get("filkart")
    if not k:
        raise ZenodoFeil("manifestet har ikke filkart; bygg med --forrige")
    return {"slett": sorted(k["endret"] + k["fjernet"]), "last_opp": sorted(k["endret"] + k["ny"]),
            "behold": sorted(k["uendret"])}


# --- stegene ------------------------------------------------------------------------------------------------------

def les_tilstand(vault: Path, versjon: str) -> dict | None:
    sti = tilstandssti(vault, versjon)
    return json.loads(sti.read_text(encoding="utf-8")) if sti.is_file() else None


def _skriv_tilstand(vault: Path, versjon: str, t: dict) -> None:
    sti = tilstandssti(vault, versjon)
    kladd = sti.with_suffix(".json.kladd")
    kladd.write_text(json.dumps(t, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    kladd.replace(sti)


def reserver(k: Klient, vault: Path, versjon: str, forrige: str) -> dict:
    """Opprett utkast til ny versjon og skriv tilstandsfilen. Finnes den, gjenbrukes utkastet uten nytt kall."""
    t = les_tilstand(vault, versjon)
    if t:
        return t
    forrige_post = k.kall("POST", f"{k.api}/deposit/depositions/{forrige}/actions/newversion", ok=(201,))
    utkast_url = forrige_post["links"]["latest_draft"]
    u = k.kall("GET", utkast_url)
    if u.get("submitted"):
        raise ZenodoFeil(f"utkastet {u['id']} er alt publisert")
    t = {"versjon": versjon, "forrige": str(forrige), "utkast_id": u["id"], "utkast_url": utkast_url,
         "bucket": u["links"]["bucket"], "doi": u["metadata"]["prereserve_doi"]["doi"], "publisert": False}
    _skriv_tilstand(vault, versjon, t)
    return t


def _tilstand(vault: Path, versjon: str) -> dict:
    t = les_tilstand(vault, versjon)
    if not t:
        raise ZenodoFeil(f"ingen tilstandsfil for v{versjon}; kjør reserver først")
    if t.get("publisert"):
        raise ZenodoFeil(f"v{versjon} er alt publisert ({t.get('doi')}); en publisert post kan ikke endres")
    return t


def fjernfiler(k: Klient, t: dict) -> list[dict]:
    return k.kall("GET", f"{k.api}/deposit/depositions/{t['utkast_id']}/files") or []


def last_opp(k: Klient, vault: Path, versjon: str, *, dato: str | None = None) -> dict:
    """Gjør Zenodo-utkastet likt det bygde utkastet. Kan kjøres på nytt: det som alt er likt, står."""
    m, t = les_manifest(vault, versjon), _tilstand(vault, versjon)
    avvik = kontroller_utkast(m)
    if avvik:
        raise ZenodoFeil("utkastet på disk er ikke det manifestet beskriver: " + "; ".join(avvik[:5]))
    avvik = plassholdere(m) + doi_ført(m, t)
    if avvik:
        raise ZenodoFeil("utkastet er ikke klart for opplasting (kjør fyll og bygg på nytt): " + "; ".join(avvik[:5]))
    p = plan(m, fjernfiler(k, t))
    for f in p["slett"]:
        k.kall("DELETE", f"{k.api}/deposit/depositions/{t['utkast_id']}/files/{f['id']}", ok=(204,))
    ut = Path(m["utkast"])
    for navn in p["last_opp"]:
        k.kall("PUT", f"{t['bucket']}/{urllib.parse.quote(navn)}", fil=ut / navn, ok=(200, 201))
    u = k.kall("GET", t["utkast_url"])
    md = dict(u["metadata"])
    md.pop("prereserve_doi", None)
    md["version"] = versjon
    if dato:
        md["publication_date"] = dato
    k.kall("PUT", t["utkast_url"], data={"metadata": md})
    return {"slettet": len(p["slett"]), "lastet_opp": len(p["last_opp"]), "sto": len(p["behold"])}


def verifiser(k: Klient, vault: Path, versjon: str) -> list[str]:
    """Avvik mellom fillisten i Zenodo-utkastet og manifestet. Tom liste betyr likt, fil for fil, på navn og md5."""
    m, t = les_manifest(vault, versjon), _tilstand(vault, versjon)
    p = plan(m, fjernfiler(k, t))
    avvik = [f"i Zenodo-utkastet, ikke i manifestet eller med annen md5: {f['navn']}" for f in p["slett"]]
    avvik += [f"mangler i Zenodo-utkastet: {n}" for n in p["last_opp"]]
    u = k.kall("GET", t["utkast_url"])
    if u["metadata"].get("version") != versjon:
        avvik.append(f"metadata sier versjon {u['metadata'].get('version')}, ikke {versjon}")
    return avvik


def jaord(versjon: str) -> str:
    return f"publiser v{versjon}"


def publiser(k: Klient, vault: Path, versjon: str, ja: str) -> dict:
    """Publiser utkastet. Irreversibelt: en publisert post kan verken endres eller trekkes."""
    if ja != jaord(versjon):
        raise ZenodoFeil(f"publisering krever eierens ja ordrett: --ja \"{jaord(versjon)}\"")
    m, t = les_manifest(vault, versjon), _tilstand(vault, versjon)
    avvik = kontroller_utkast(m) + plassholdere(m) + doi_ført(m, t) + verifiser(k, vault, versjon)
    if avvik:
        raise ZenodoFeil(f"{len(avvik)} avvik, ingenting publisert: " + "; ".join(avvik[:5]))
    svar = k.kall("POST", f"{k.api}/deposit/depositions/{t['utkast_id']}/actions/publish", ok=(202,))
    t |= {"publisert": True, "doi": svar.get("doi") or t["doi"], "konsept_doi": svar.get("conceptdoi"),
          "post": (svar.get("links") or {}).get("record_html") or (svar.get("links") or {}).get("html"),
          "head": m.get("head"), "utkast_sha256": utkast_sha256(m), "antall_filer": len(m["filer"])}
    _skriv_tilstand(vault, versjon, t)
    return t


# --- kommandolinjen -----------------------------------------------------------------------------------------------

SKRIVER = ("reserver", "last-opp", "publiser")


def main(argv=None, *, klient: Klient | None = None, vault: Path | None = None, repo: Path | None = None) -> int:
    p = argparse.ArgumentParser(prog="gjenopptak.zenodo", description="Last opp og publiser et bygget utkast.")
    p.add_argument("steg", choices=("plan", "reserver", "fyll", "last-opp", "verifiser", "publiser"))
    p.add_argument("--versjon", required=True)
    p.add_argument("--forrige", help="forrige publiserte post (record-id); kreves av reserver")
    p.add_argument("--dato", help="publiseringsdato (ÅÅÅÅ-MM-DD); brukes av fyll og last-opp")
    p.add_argument("--doi", help="versjons-DOI for fyll; standard er den reserverte i tilstandsfilen")
    p.add_argument("--ja", nargs="?", const="ja", default=None,
                   help="eierens ja. Kreves av hvert steg som skriver til Zenodo; publiser krever «publiser v<versjon>»")
    a = p.parse_args(argv)
    try:
        vault = vault or require_vault()
        if a.steg == "plan":
            m = les_manifest(vault, a.versjon)
            pl, avvik = plan_fra_filkart(m), kontroller_utkast(m)
            print(f"v{a.versjon}: {len(m['filer'])} filer · utkast-sha256 {utkast_sha256(m)}")
            print(f"mot forrige versjon: slett {len(pl['slett'])} · last opp {len(pl['last_opp'])} · står {len(pl['behold'])}")
            print("utkastet på disk: " + ("likt manifestet" if not avvik else f"{len(avvik)} avvik"))
            for linje in avvik:
                print("  " + linje)
            ufylt = plassholdere(m)
            print("plassholdere for DOI og dato: " + ("ingen" if not ufylt else f"{len(ufylt)} filer — fylles etter reserver, før opplasting"))
            for linje in ufylt:
                print("  " + linje)
            return 1 if avvik else 0
        if a.steg == "fyll":
            if not a.dato:
                raise ZenodoFeil("fyll krever --dato")
            doi = a.doi or (les_tilstand(vault, a.versjon) or {}).get("doi")
            if not doi:
                raise ZenodoFeil("fyll krever --doi, eller en tilstandsfil fra reserver")
            for fil, n in fyll(repo or Path(__file__).resolve().parents[2], a.versjon, doi, a.dato).items():
                print(f"{fil}: {n} plassholdere fylt")
            return 0
        if a.steg in SKRIVER and not a.ja:
            raise ZenodoFeil(f"{a.steg} skriver til Zenodo og krever --ja")
        if a.steg == "reserver" and not a.forrige:
            raise ZenodoFeil("reserver krever --forrige")
        k = klient or Klient(les_nøkkel())
        if a.steg == "reserver":
            t = reserver(k, vault, a.versjon, a.forrige)
            print(f"utkast {t['utkast_id']} · reservert DOI {t['doi']} · {tilstandssti(vault, a.versjon)}")
        elif a.steg == "last-opp":
            r = last_opp(k, vault, a.versjon, dato=a.dato)
            print(f"slettet {r['slettet']} · lastet opp {r['lastet_opp']} · sto {r['sto']}")
        elif a.steg == "verifiser":
            avvik = verifiser(k, vault, a.versjon)
            print("ingen avvik" if not avvik else f"{len(avvik)} avvik")
            for linje in avvik:
                print("  " + linje)
            return 1 if avvik else 0
        else:
            t = publiser(k, vault, a.versjon, a.ja)
            print(f"PUBLISERT v{a.versjon} · {t['doi']} · {t['antall_filer']} filer")
    except (ZenodoFeil, VaultUnavailable) as e:
        print(f"FEIL: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
