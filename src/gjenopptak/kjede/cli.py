"""``gjenopptak run`` — kjeden som én kjørbar sti.

    gjenopptak run --verk verk.txt --navn min-kjoring
    gjenopptak run --felt energimodellering --from dommer --to union
    gjenopptak run --verk verk.txt --torr          # kostnad før noe hentes

Hvert ledd kan kjøres alene med ``--from``/``--to`` og gjenopptas. Kvoteporten nekter å
starte en fase budsjettet ikke rekker til. ADR-0012 og ``docs/BYGGEPLAN.md`` B1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import ledd as L
from .felt import last_felt, navn_liste, ramme_status
from .konfig import KonfigFeil, last
from .kvote import API_FORBUDT, Behov, behov_for_leser, harness_kvote, port


def _verksliste(a: argparse.Namespace, k) -> tuple[list[str], str | None]:
    """Verkene kjøringen gjelder, fra ``--verk`` (fil med W-id-er) eller ``--felt``."""
    if a.verk:
        p = Path(a.verk)
        if not p.is_file():
            raise SystemExit(f"finner ikke verksfilen: {p}")
        ids = [l.strip() for l in p.read_text(encoding="utf-8").splitlines()
               if l.strip() and not l.startswith("#")]
        return ids, None
    # B2: feltet er en fil. Den avgjør topics, år, ramme og terskler — ingenting i kode.
    f = last_felt(k, a.felt)
    st, hvorfor = ramme_status(k, f)
    print(f"felt {f.navn}: topics {', '.join(f.topics)} · år {f.ar[0]}–{f.ar[1]} · "
          f"{f.n_verk} verk · gulv {f.gulv} · fra {f.kilde.relative_to(k.rot)}")
    print(f"  ramme: {st} — {hvorfor}")
    if st == "avvik":
        raise SystemExit(2)
    spes = json.loads(k.sti("tekstbiter", "fasit_spesifikasjon").read_text(encoding="utf-8"))
    ids = [r["work_id"] for r in spes["verk"] if r["felt"] == a.felt]
    if not ids and st == "mangler":
        print(f"  ingen trukne verk ennå — feltet kan planlegges (--torr), ikke kjøres")
        return [], a.felt
    if not ids:
        raise SystemExit(f"rammen finnes, men ingen verk er trukket for {a.felt!r} ennå")
    return ids, a.felt


def _spenn(a: argparse.Namespace) -> list[str]:
    fra = a.fra or L.LEDD[0]
    til = a.til or L.LEDD[-1]
    for n in (fra, til):
        if n not in L.LEDD:
            raise SystemExit(f"ukjent ledd {n!r}; gyldige er {', '.join(L.LEDD)}")
    i, j = L.LEDD.index(fra), L.LEDD.index(til)
    if i > j:
        raise SystemExit(f"--from {fra} kommer etter --to {til}")
    return list(L.LEDD[i:j + 1])


def _kvoteport(kj: L.Kjøring, spenn: list[str], *, tørr: bool) -> None:
    """Nekt fasene budsjettet ikke rekker til. Skriver behovet uansett."""
    if "les" in spenn:
        union = L._les_jsonl(kj.fil("5-union.jsonl"))
        if union:
            n = len(union)
        elif kj.verk:
            n = len(kj.verk) * 222              # målt snitt tekstbiter per verk
        elif kj.felt:
            # Feltet har ingen trukne verk ennå: regn på det feltfilen sier det skal ha.
            n = last_felt(kj.k, kj.felt).n_verk * 222
        else:
            n = 0
        b = behov_for_leser(kj.k, n)
        svar = port(kj.k, "les", b, sjekk_api=False)
        print(svar.tekst())
        if not svar.slipper and not tørr:
            raise SystemExit(2)
    print(f"kvoteport: {API_FORBUDT}")


def kjør(a: argparse.Namespace) -> int:
    k = last(Path(a.konfig) if a.konfig else None)
    avvik = k.sjekk_sha(k.laaste_filer())
    if avvik:
        print("LÅSTE FILER AVVIKER — kjeden stoppes:", file=sys.stderr)
        for x in avvik:
            print(f"  {x}", file=sys.stderr)
        return 2
    verk, felt = _verksliste(a, k)
    kj = L.Kjøring(k=k, navn=a.navn, verk=verk, felt=felt)
    spenn = _spenn(a)
    print(f"kjøring {kj.navn}: {len(verk)} verk"
          f"{f' (felt {felt})' if felt else ''} · ledd {spenn[0]} → {spenn[-1]}")
    print(f"konfig {k.fil} · rot {k.rot} · vault {k.vault_mål}")
    print(f"låste filer: {len(k.laaste_filer())} verifisert på sha256")
    _kvoteport(kj, spenn, tørr=a.torr)
    if a.torr:
        print("\nTØRRKJØRING — ingenting hentes, dømmes eller leses.")
        if not verk and felt:
            f = last_felt(k, felt)
            print(f"  feltet har ingen frosset ramme ennå. Å bygge den koster:")
            print(f"    OpenAlex-kall:      {f.ramme_rader // 200 + 1:>12,}  (200 per side)")
            print(f"    verk å trekke:      {f.n_verk:>12,}")
            b = behov_for_leser(k, f.n_verk * 222)
        else:
            b = behov_for_leser(k, len(verk) * 222)
        for l in b.linjer():
            print(f"  {l}")
        return 0
    cache_dom = Path(a.cache_dommer) if a.cache_dommer else None
    cache_eks = Path(a.cache_ekstraksjon) if a.cache_ekstraksjon else None
    for navn in spenn:
        if kj.gjort(navn) and not a.om:
            print(f"\n— {navn}: alt gjort, hopper over (--om for å kjøre om)")
            continue
        print(f"\n— {navn}")
        if navn == "hent":
            r = L.steg_hent(kj)
        elif navn == "tekstbiter":
            r = L.steg_tekstbiter(kj)
        elif navn == "dommer":
            r = L.steg_dommer(kj, cache=cache_dom)
        elif navn == "ekstraksjon":
            r = L.steg_ekstraksjon(kj, cache=cache_eks)
        elif navn == "union":
            r = L.steg_union(kj)
        elif navn == "blind":
            r = L.steg_blind(kj)
        elif navn == "les":
            r = L.steg_les(kj, tørr=a.torr, modus=a.leser,
                           cache=Path(a.cache_leser) if a.cache_leser else None)
        elif navn == "verksniva":
            r = L.steg_verksniva(kj)
        elif navn == "falsify":
            r = L.steg_falsify(kj, tørr=a.torr)
        else:
            r = L.steg_register(kj, port=a.port)
        for nøkkel, verdi in r.items():
            if isinstance(verdi, (str, int, float, bool)) or verdi is None:
                print(f"    {nøkkel}: {verdi}")
            else:
                print(f"    {nøkkel}: {json.dumps(verdi, ensure_ascii=False)[:160]}")
    print(f"\ntilstand: {kj.tilstandsfil}")
    return 0


def kvote(a: argparse.Namespace) -> int:
    k = last(Path(a.konfig) if a.konfig else None)
    if a.skriv_harness is not None:
        f = k.arbeid / "kvote-harness.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps({"ukesgrense_prosent": a.skriv_harness,
                                 "lest": L.nå()}, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
        print(f"skrevet {f}: ukesgrense {a.skriv_harness} %")
        return 0
    print(f"Anthropics API: brukes ikke — {API_FORBUDT}")
    h = harness_kvote(k)
    print(f"harness-kvote:  {h if h else 'ukjent — skriv den med --skriv-harness <prosent>'}")
    print(f"Vault:          {k.vault_mål} ({'finnes' if k.vault_mål.is_dir() else 'MANGLER'})")
    for x in k.sjekk_sha(k.laaste_filer()) or ["låste filer: alle sha256 stemmer"]:
        print(f"  {x}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="gjenopptak",
        description="Kjeden ramme → henting → tekstbiter → sil → leser → register (ADR-0012).")
    p.add_argument("--konfig", help="sti til kjede.toml; ellers søkes den oppover fra cwd")
    sub = p.add_subparsers(dest="kommando", required=True)

    r = sub.add_parser("run", help="kjør kjeden eller et spenn av ledd")
    g = r.add_mutually_exclusive_group(required=True)
    g.add_argument("--verk", help="fil med én W-id per linje")
    g.add_argument("--felt", help="feltnavn; leses fra felt/<navn>.yaml (B2)")
    r.add_argument("--navn", default="kjoring", help="navn på kjøringen (katalog under [kjede] arbeid)")
    r.add_argument("--from", dest="fra", help=f"første ledd ({', '.join(L.LEDD)})")
    r.add_argument("--to", dest="til", help="siste ledd")
    r.add_argument("--torr", action="store_true", help="tørrkjøring: rapporter kostnad, gjør ingenting")
    r.add_argument("--om", action="store_true", help="kjør ledd om selv om de er gjort")
    r.add_argument("--port", help="navnet på porten lista har bestått; uten den blir den ubekreftet")
    r.add_argument("--cache-dommer", help="katalog med ferdige dommer-<felt>.jsonl")
    r.add_argument("--cache-ekstraksjon", help="ferdig ekstraksjon-logg.jsonl")
    r.add_argument("--leser", choices=("subagent", "cli"), default="cli",
                   help="subagent = CCs egen underinstans (kjeden legger fram oppdraget og venter "
                        "på verdiktfilen); cli = claude -p på stdin")
    r.add_argument("--cache-leser", help="katalog med nokkel.jsonl og *verdikter*.jsonl fra en "
                                        "tidligere lesning av de samme passasjene")
    r.set_defaults(f=kjør)

    q = sub.add_parser("kvote", help="vis kvotene kjeden kan lese, eller skriv harness-kvoten")
    q.add_argument("--skriv-harness", type=float, metavar="PROSENT",
                   help="skriv harness-ens ukesgrense i prosent, som kjeden ikke kan lese selv")
    q.set_defaults(f=kvote)

    a = p.parse_args(argv)
    try:
        return a.f(a)
    except (KonfigFeil, L.LeddFeil) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
