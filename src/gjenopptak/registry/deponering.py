"""Deponering etter fagfellevurderingen (03.10.2026): registerindeksen for kandidatlista og tallmanifestet.

    PYTHONPATH=src python -m gjenopptak.registry.deponering registerindeks
    PYTHONPATH=src python -m gjenopptak.registry.deponering tallmanifest

**Registerindeksen** er register v2 (de 432 radene bak kandidatlista, `kandidat432/8-register.jsonl`) uten tredjepartstekst:
hver rad med alle analysefeltene og `tekst_sha256` for passasjen leseren dømte (teksten hentes fra arbeidslistas
blindfiler på Vault og hashes; den skrives ikke ut). Leserens begrunnelse (`notes`) er tatt ut, fordi den gjengir innholdet
i passasjen. Skrives til Vault `revisjon-2026-10/register-v2-indeks.jsonl`.

**Tallmanifestet** kobler tall i manuskriptet (v2.9) til fil, deponert filnavn, sha256 og genererende skript, og
**kontrollerer hver verdi maskinelt** ved å lese den ut av fila. Skrives til `docs/TALLMANIFEST.md`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from ..vault import require_vault, sha256_file

REPO = Path(__file__).resolve().parents[3]


def _jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def registerindeks() -> int:
    v = require_vault()
    reg = _jl(v / "kandidat432" / "8-register.jsonl")
    tekst = {r["id"]: r["tekst"] for f in sorted((v / "arbeidsliste" / "blind").glob("blind-okt-*.jsonl")) for r in _jl(f)}
    ut, mangler = [], []
    for r in reg:
        t = tekst.get(r["candidate_id"])
        if t is None:
            mangler.append(r["candidate_id"])
        rad = {k: v_ for k, v_ in r.items() if k != "notes"}
        rad["tekst_sha256"] = hashlib.sha256(t.encode("utf-8")).hexdigest() if t is not None else None
        rad["tekst_tegn"] = len(t) if t is not None else None
        ut.append(rad)
    f = v / "revisjon-2026-10" / "register-v2-indeks.jsonl"
    f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ut), encoding="utf-8")
    print(json.dumps({"rader": len(ut), "uten_tekst": mangler, "fil": str(f), "sha256": sha256_file(f),
                      "kilde_sha256": sha256_file(v / "kandidat432" / "8-register.jsonl")}, ensure_ascii=False))
    return 0 if not mangler else 1


#: (id, sted i manus v2.9, påstand, verdi i manus, kilde, deponert som, uttrekk, skript)
#: kilde: "V:<sti>" (Vault) eller "R:<sti>" (repo). uttrekk: ("json", sti-liste) | ("antall",) | ("tekst", regex).
R = "V:revisjon-2026-10/reanalyse.json"
RS = "classify/reanalyse_fagfelle.py"
P = ("a_c_kappa", "par")
TALL = [
    # Tallene i manus v3.1 (docs/MANUSKRIPT-v3.1.md). Alle 144 tallpunktene er kontrollert mot kilde i
    # docs/FAKTASJEKK-MANUSKRIPT-v3-2026-10-03.md; her står de som kan leses maskinelt ut av en deponert fil.
    ("T01", "§3.4", "tekstbiter i fase 1", 22243, R, "revisjon-reanalyse.json", ("json", ["e_prevalens", "N_tekstbiter"]), RS),
    ("T02", "§5.6", "tekstbiter flagget av dommeren", 2173, R, "revisjon-reanalyse.json", ("json", ["e_prevalens", "N_flagget"]), RS),
    ("T03", "Abstract, §5.2", "κ koder 1 mot koder 2", 0.812, R, "revisjon-reanalyse.json", ("json", [*P, "koder 1 mot koder 2", "kappa"]), RS),
    ("T04", "§5.2", "κ koder 4 mot koder 2", 0.899, R, "revisjon-reanalyse.json", ("json", [*P, "koder 4 mot koder 2", "kappa"]), RS),
    ("T05", "§5.2", "κ koder 4 mot koder 1", 0.781, R, "revisjon-reanalyse.json", ("json", [*P, "koder 4 mot koder 1", "kappa"]), RS),
    ("T06", "§5.3", "κ Opus ett kall mot koder 1", 0.636, R, "revisjon-reanalyse.json", ("json", [*P, "Opus ett kall mot koder 1", "kappa"]), RS),
    ("T07", "Abstract, §5.1", "rader i kandidatlista", 432, "V:revisjon-2026-10/register-v2-indeks.jsonl", "register-v2-indeks.jsonl", ("antall",), "registry/deponering.py"),
    ("T08", "§5.1", "verk med minst én rad", 60, R, "revisjon-reanalyse.json", ("json", ["a_klasser", 0, "H7_av_alle", "fordeling", "verk"]), RS),
    ("T09", "§5.1", "H7 per rad", "289/432", R, "revisjon-reanalyse.json", ("brøk", ["a_klasser", 0, "H7_av_alle"]), RS),
    ("T10", "§5.1", "løftbar H1–H6 per avklart rad", "77/406", R, "revisjon-reanalyse.json", ("brøk", ["a_klasser", 0, "H1_H6_av_avklarte"]), RS),
    ("T11", "§5.4", "post hoc port", "85/100", R, "revisjon-reanalyse.json", ("brøk", ["a_porter_recall", "post_hoc_port_85_100"]), RS),
    ("T12", "§5.4", "preregistrert port: kjente treff funnet", "21 av 27", "R:ADDENDUM-22.md", "ADDENDUM-22.md", ("tekst", r"21 av 27"), "—"),
    ("T13", "Abstract, §5.5", "fase 2: bekreftelsesrate", "85/100", R, "revisjon-reanalyse.json", ("brøk", ["a_porter_recall", "fase3_port_85_100"]), RS),
    ("T14", "Abstract, §5.5", "fase 2: silens retention", "95/104", R, "revisjon-reanalyse.json", ("brøk", ["a_porter_recall", "fase3_beholdt"]), RS),
    ("T15", "§5.5", "fase 2: leserens enighet med referansen", "85/104", R, "revisjon-reanalyse.json", ("brøk", ["a_porter_recall", "fase3_bekreftet"]), RS),
    ("T16", "§5.5", "referansetreff i det største verket", 51, R, "revisjon-reanalyse.json", ("json", ["a_porter_recall", "fase3_beholdt", "fordeling", "største_verk"]), RS),
    ("T17", "§5.5", "retention uten største verk", "45/53", "V:fase3/rapport-fase3.json", "fase3-rapport.json", ("brøk", ["recall_klynger", "uten_største", "beholdt"]), "classify/fase3_rapport.py"),
    ("T18", "§5.5", "leserenighet uten største verk", "38/53", "V:fase3/rapport-fase3.json", "fase3-rapport.json", ("brøk", ["recall_klynger", "uten_største", "bekreftet"]), "classify/fase3_rapport.py"),
    ("T19", "§5.5", "leserens rader i fase 2", 673, "V:fase3-kjede/8-register.jsonl", "fase3-register.jsonl", ("antall",), "kjede/ledd.py steg_register"),
    ("T20", "§5.5", "fase 2: unike erklæringer", 424, R, "revisjon-reanalyse.json", ("json", ["f_duplikater", 1, "unike_erklæringer"]), RS),
    ("T21", "§5.5", "fase 2: H7 av erklæringer med én flertallsklasse", "265/402", R, "revisjon-reanalyse.json", ("brøk", ["f_duplikater", 1, "H7_av_unike"]), RS),
    ("T22", "§5.5", "fase 2: løftbar av avklarte erklæringer", "53/375", R, "revisjon-reanalyse.json", ("brøk", ["f_duplikater", 1, "H1_H6_av_avklarte_unike"]), RS),
    ("T23", "§5.1", "arkeologi: leser-positive blant silkandidater", "274/990", R, "revisjon-reanalyse.json", ("felt", "arkeologi"), RS),
    ("T24", "§5.1", "klinisk epidemiologi", "53/347", R, "revisjon-reanalyse.json", ("felt", "klinisk_epidemiologi"), RS),
    ("T25", "§5.1", "tekstvitenskap", "37/378", R, "revisjon-reanalyse.json", ("felt", "tekstvitenskap"), RS),
    ("T26", "§5.1", "energimodellering", "68/1129", R, "revisjon-reanalyse.json", ("felt", "energimodellering"), RS),
    ("T27", "§5.6", "grunnrate, prosent", 3.42, R, "revisjon-reanalyse.json", ("prosent2", ["e_prevalens", "punkt", "prevalens"]), RS),
    ("T28", "§5.6", "grunnrate, verksklynget intervall (prosent)", "1.3–7.5", R, "revisjon-reanalyse.json", ("iv1", ["e_prevalens", "verksklynget_bootstrap95"]), RS),
    ("T29", "§5.7 tabell 3", "case B: greske sitatsteder løst", "79 av 90", "R:docs/saker/SAK-14/RESULTAT.md", "saker.zip: saker/SAK-14/RESULTAT.md", ("tekst", r"79 av 90"), "—"),
    ("T30", "§5.7", "case F: C(41,7)", "22 481 940", "R:docs/saker/SAK-11/LUKKET.md", "saker.zip: saker/SAK-11/LUKKET.md", ("tekst", r"22 481 940"), "—"),
    ("T31", "Abstract, §5.1", "fase 1: unike erklæringer", 276, R, "revisjon-reanalyse.json", ("json", ["f_duplikater", 0, "unike_erklæringer"]), RS),
    ("T32", "§5.1", "fase 1: rader som deler setning", 269, R, "revisjon-reanalyse.json", ("json", ["f_duplikater", 0, "rader_som_deler_setning"]), RS),
    ("T33", "Abstract, §5.1", "fase 1: H7 av erklæringer med én flertallsklasse", "183/257", R, "revisjon-reanalyse.json", ("brøk", ["f_duplikater", 0, "H7_av_unike"]), RS),
    ("T34", "§5.1", "fase 1: løftbar av avklarte erklæringer", "42/245", R, "revisjon-reanalyse.json", ("brøk", ["f_duplikater", 0, "H1_H6_av_avklarte_unike"]), RS),
    ("T35", "§5.1", "fase 1: erklæringer med delt klasse", 19, R, "revisjon-reanalyse.json", ("json", ["f_duplikater", 0, "blandet_klasse"]), RS),
    ("T36", "Abstract, §5.3", "paret differanse κ", 0.177, R, "revisjon-reanalyse.json", ("json", ["a_c_kappa", "differanse_koder2_minus_opus", "punkt"]), RS),
    ("T37", "Abstract, §5.3", "paret differanse, verksklynget intervall", "0.057–0.318", R, "revisjon-reanalyse.json", ("iv3", ["a_c_kappa", "differanse_koder2_minus_opus", "klynge_paret95"]), RS),
    ("T38", "§5.2 tabell 1", "κ koder 1–2, verksklynget intervall", "0.711–0.909", R, "revisjon-reanalyse.json", ("iv3", [*P, "koder 1 mot koder 2", "klynge_bootstrap95"]), RS),
    ("T39", "Abstract, §5.5", "bekreftelsesrate, verksklynget (prosent)", "76.2–93.8", R, "revisjon-reanalyse.json", ("iv1", ["a_porter_recall", "fase3_port_85_100", "klynge_bootstrap95"]), RS),
    ("T40", "Abstract, §5.5", "retention, verksklynget (prosent)", "76.9–96.7", R, "revisjon-reanalyse.json", ("iv1", ["a_porter_recall", "fase3_beholdt", "klynge_bootstrap95"]), RS),
    ("T41", "§5.5 tabell 2", "leserenighet, verksklynget (prosent)", "60.9–89.7", R, "revisjon-reanalyse.json", ("iv1", ["a_porter_recall", "fase3_bekreftet", "klynge_bootstrap95"]), RS),
    ("T42", "§5.4", "post hoc port, verksklynget (prosent)", "75.7–92.3", R, "revisjon-reanalyse.json", ("iv1", ["a_porter_recall", "post_hoc_port_85_100", "klynge_bootstrap95"]), RS),
    ("T43", "§5.1", "H7 per rad, verksklynget (prosent)", "58.2–79.7", R, "revisjon-reanalyse.json", ("iv1", ["a_klasser", 0, "H7_av_alle", "klynge_bootstrap95"]), RS),
    ("T44", "§5.1", "løftbar per rad, verksklynget (prosent)", "9.0–26.5", R, "revisjon-reanalyse.json", ("iv1", ["a_klasser", 0, "H1_H6_av_avklarte", "klynge_bootstrap95"]), RS),
    ("T45", "§4", "valideringsprøven, passasjer", 149, "V:revisjon-2026-10/menneskevalidering/utvalg.json", "menneskevalidering-utvalg.json", ("json", ["n"]), "classify/menneskevalidering.py"),
]


def _hent(o, sti):
    for s in sti:
        o = o[s]
    return o


def tallmanifest() -> int:
    v = require_vault()
    rader, avvik = [], 0
    for tid, sted, påstand, verdi, kilde, dep, (art, *arg), skript in TALL:
        p = (v / kilde[2:]) if kilde.startswith("V:") else (REPO / kilde[2:])
        funnet = None
        if art == "json":
            funnet = _hent(json.loads(p.read_text(encoding="utf-8")), arg[0])
            if isinstance(verdi, float) and isinstance(funnet, float):
                funnet = round(funnet, len(str(verdi).split(".")[1]))
        elif art == "brøk":
            x = _hent(json.loads(p.read_text(encoding="utf-8")), arg[0])
            funnet = f"{x['k']}/{x['n']}"
        elif art in ("iv1", "iv3"):
            x = _hent(json.loads(p.read_text(encoding="utf-8")), arg[0])
            funnet = (f"{100 * x[0]:.1f}–{100 * x[1]:.1f}" if art == "iv1" else f"{x[0]:.3f}–{x[1]:.3f}")
        elif art == "prosent2":
            funnet = round(100 * _hent(json.loads(p.read_text(encoding="utf-8")), arg[0]), 2)
        elif art == "felt":
            x = json.loads(p.read_text(encoding="utf-8"))["d_felt"][arg[0]]
            funnet = f"{x['leser_positive']}/{x['silkandidater']}"
        elif art == "antall":
            funnet = sum(1 for l in p.read_text(encoding="utf-8").splitlines() if l.strip())
        elif art == "tekst":
            funnet = verdi if re.search(arg[0], p.read_text(encoding="utf-8")) else None
        ok = funnet == verdi
        avvik += not ok
        rader.append((tid, sted, påstand, verdi, funnet, ok, kilde, dep, sha256_file(p), skript))
    L = ["# Tallmanifest — manuskript v3.1 → fil, sha256 og skript", "",
         "**Generert** av `src/gjenopptak/registry/deponering.py tallmanifest`. Hver verdi er **lest ut av fila maskinelt** og "
         "sammenliknet med tallet i manuskriptet; ✓ betyr likt, ✗ betyr avvik. «Deponert som» er filnavnet i Zenodo v0.5.0 "
         "(utkast, ikke publisert). Skriptet er det som skrev fila; «—» betyr et dokument skrevet for hånd.", "",
         f"**{len(rader) - avvik} av {len(rader)} stemmer.** Alle 144 tallpunkter i manuset er kontrollert mot kilde i "
         "`FAKTASJEKK-MANUSKRIPT-v3-2026-10-03.md` (i `faktasjekk-manuskript.zip`); tabellen her er de som leses maskinelt.", "",
         "| id | manus | påstand | i manus | i fila | | kilde | deponert som | sha256 | skript |", "|---|---|---|---|---|---|---|---|---|---|"]
    for tid, sted, påstand, verdi, funnet, ok, kilde, dep, sha, skript in rader:
        L.append(f"| {tid} | {sted} | {påstand} | {verdi} | {funnet} | {'✓' if ok else '✗'} | `{kilde}` | `{dep}` | `{sha[:16]}…` | `{skript}` |")
    L += ["", "**Avvik, forklart:**", ""]
    for r in rader:
        if not r[5]:
            if True:
                L.append(f"* **{r[0]}** — i manus {r[3]}, i fila {r[4]}.")
    if not avvik:
        L.append("ingen.")
    f = REPO / "docs" / "TALLMANIFEST.md"
    f.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{len(rader) - avvik} av {len(rader)} stemmer; {f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("kommando", choices=("registerindeks", "tallmanifest"))
    a = p.parse_args(argv)
    return registerindeks() if a.kommando == "registerindeks" else tallmanifest()


if __name__ == "__main__":
    sys.exit(main())
