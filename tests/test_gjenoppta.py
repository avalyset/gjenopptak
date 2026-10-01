"""Gjenopptak fra låsecommiten: § 9-tabellen leses fra addendumet, og en endret cli.py stopper."""
import hashlib
import subprocess

import pytest

from gjenopptak.kjede.gjenoppta import GjenopptakNekt, låst_tabell, sjekk_sha

CLI = "src/gjenopptak/kjede/cli.py"


def _tabell(**rader):
    linjer = ["# ADDENDUM", "", "## 8 Noe", "| `src/feil.py` | `" + "0" * 64 + "` |", "", "## 9 Filer låst", "",
              "| fil | sha256 |", "|---|---|"]
    linjer += [f"| `{sti}` | `{h}` |" for sti, h in rader.items()]
    linjer += ["| regelfil `koder2/koderegler-gjenvunnet.md` | `" + "a" * 64 + "` |"]
    return "\n".join(linjer) + "\n"


LÅST = "print('låst')\n".encode()


def _wt(tmp_path, innhold=LÅST):
    p = tmp_path / CLI
    p.parent.mkdir(parents=True)
    p.write_bytes(innhold)
    return hashlib.sha256(LÅST).hexdigest()


def test_tabellen_leses_bare_fra_paragraf_9_og_bare_repofiler():
    t = låst_tabell(_tabell(**{CLI: "b" * 64, "kjede.toml": "c" * 64}))
    assert t == {CLI: "b" * 64, "kjede.toml": "c" * 64}    # ikke § 8-raden, ikke Vault-regelfilen


def test_uendret_cli_slipper(tmp_path):
    h = _wt(tmp_path)
    assert sjekk_sha(tmp_path, {CLI: h}) == []


def test_endret_cli_stopper(tmp_path):
    h = _wt(tmp_path, "print('arbeidstreet med referanseport')\n".encode())
    avvik = sjekk_sha(tmp_path, {CLI: h})
    assert len(avvik) == 1 and avvik[0].startswith(CLI) and "≠ låst" in avvik[0]


def test_cli_må_stå_i_tabellen(tmp_path):
    _wt(tmp_path)
    assert any("står ikke i § 9-tabellen" in a for a in sjekk_sha(tmp_path, {"kjede.toml": "0" * 64}))


def test_tom_paragraf_9_nekter():
    with pytest.raises(GjenopptakNekt):
        låst_tabell("# ADDENDUM\n\n## 9 Filer\n\ningen tabell\n")


def test_ekte_addendum_25_gir_cli_sha_fra_låsen():
    tekst = subprocess.run(["git", "show", "f19a3e3:ADDENDUM-25.md"], capture_output=True, text=True).stdout
    if not tekst:
        pytest.skip("låsecommiten finnes ikke i denne klonen")
    t = låst_tabell(tekst)
    assert t[CLI] == "c2eb33bc361557371a2ed86d6d3530fcd090865ca9cdc0e9fe8ae6a108731e0b"
    assert set(t) >= {CLI, "kjede.toml", "src/gjenopptak/kjede/ledd.py", "src/gjenopptak/kjede/leser.py"}


def test_vakten_ser_kjøring_startet_av_rutinen_selv():
    from gjenopptak.kjede.gjenoppta import kjører_allerede
    ps = ("  1550 /x/Python -m gjenopptak.kjede.cli --konfig /v/kjede.toml run --verk v.txt --navn fase3-kjede --leser cli\n"
          "  1540 /x/Python -m gjenopptak.kjede.gjenoppta\n"
          "  1542 /usr/bin/caffeinate -is env PYTHONPATH=src python -m gjenopptak.kjede.gjenoppta\n"
          "  1600 /x/Python -m gjenopptak.kjede.gjenoppta --sjekk\n"
          "  1700 /x/Python -m gjenopptak.kjede.cli run --navn annen-kjoring\n")
    treff = kjører_allerede("fase3-kjede", ps_utdata=ps, egen={1600})
    assert any(l.startswith("1550") for l in treff)       # --konfig før run: ble ikke sett før rettingen
    assert any(l.startswith("1540") for l in treff)       # en annen gjenopptaksrutine
    assert not any(l.startswith(("1600", "1700", "1542")) for l in treff)


def test_vakten_ser_bort_fra_skall_som_bare_nevner_modulen():
    # 30.09: en overvåkingsløkke med «pgrep -f gjenopptak.kjede.gjenoppta» nektet gjenopptaket.
    from gjenopptak.kjede.gjenoppta import kjører_allerede
    ps = ("  16921 /bin/zsh -c until ! pgrep -f 'gjenopptak.kjede.gjenoppta' >/dev/null; do sleep 30; done\n"
          "  16768 /bin/sh -c cd /r && python -m gjenopptak.kjede.gjenoppta --fullfor-okt 3 && python -m "
          "gjenopptak.kjede.gjenoppta --fra les --om\n"
          "  16800 /usr/bin/grep gjenopptak.kjede.cli --navn fase3-kjede\n"
          "  16771 /x/Python -m gjenopptak.kjede.gjenoppta --fullfor-okt 3\n")
    treff = kjører_allerede("fase3-kjede", ps_utdata=ps, egen=set())
    assert [l.split()[0] for l in treff] == ["16771"]


def test_nekter_når_ollama_er_nede():
    # Port 9 (discard) har ingen lytter lokalt; tilkoblingen avvises straks.
    from gjenopptak.kjede.gjenoppta import krev_ollama
    with pytest.raises(GjenopptakNekt, match="ollama svarer ikke"):
        krev_ollama("http://127.0.0.1:9", tidsavbrudd=2)


def test_slipper_når_ollama_svarer(tmp_path):
    import json as _json
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from gjenopptak.kjede.gjenoppta import krev_ollama

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            b = _json.dumps({"models": [{"name": "gemma2:9b"}]}).encode()
            self.send_response(200 if self.path == "/api/tags" else 404)
            self.end_headers()
            self.wfile.write(b)

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        assert krev_ollama(f"http://127.0.0.1:{srv.server_port}")["modeller"] == 1
    finally:
        srv.shutdown()


def test_sandkassen_nekter_symlenke_ut_av_vault(tmp_path):
    from gjenopptak.kjede.gjenoppta import sjekk_sandkasse
    vault, ute = tmp_path / "vault", tmp_path / "hjemme" / "data"
    wt = vault / "fase3" / "wt"
    (ute / "kjede" / "fase3-kjede").mkdir(parents=True)
    wt.mkdir(parents=True)
    (wt / "data").symlink_to(ute)
    with pytest.raises(GjenopptakNekt, match="symlenke"):
        sjekk_sandkasse(wt, vault)
    (wt / "data").unlink()
    (wt / "data" / "kjede" / "fase3-kjede").mkdir(parents=True)
    assert sjekk_sandkasse(wt, vault).endswith("data")
    # kjøringens katalog som lenke ut av Vault stoppes også
    import shutil
    shutil.rmtree(wt / "data" / "kjede" / "fase3-kjede")
    (wt / "data" / "kjede" / "fase3-kjede").symlink_to(ute / "kjede" / "fase3-kjede")
    with pytest.raises(GjenopptakNekt, match="utenfor Vault"):
        sjekk_sandkasse(wt, vault)


# --- 30.09.2026: etterkontroll, tvungen --om etter les, og fullføring uten overskriving ------------------

import json as _json

from gjenopptak.kjede.gjenoppta import (etterkontroll, fotavtrykk, fullfør_økt, overskrevet, planlegg,
                                        rest_oppdrag, ugyldige_dommer, verdiktstatus)

OPPDRAG = ("# Oppdrag: økt {n}\n\nLes {t} blindede tekstbiter.\n\n2. **Materialet:** "
           "`data/kjede/fase3-kjede/blind/blind-okt-{n}.jsonl` — {t} linjer\n\nSkriv til\n"
           "`/V/data/kjede/fase3-kjede/7-verdikter-okt-{n}.jsonl`:\n\nNår alle {t} er kodet, rapporter.\n\n"
           "Gå gjennom alle {t} i rekkefølge.\n\n**Din egen kladdekatalog:** `/V/data/kjede/kladd/okt-{n}/`\n")


def _dom(i: str, treff: bool = False) -> dict:
    return {"id": i, "treff": treff, "klasse": "H7" if treff else "INGEN", "begrunnelse": "én setning", "tvil": False}


def _skriv(p, rader):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(_json.dumps(r, ensure_ascii=False) + "\n" for r in rader), encoding="utf-8")


def _kjøring(tmp_path, dømt: dict[int, int], størrelse: int = 343):
    """En kjøringskatalog med blindfiler, oppdrag og verdiktfiler: ``dømt[okt]`` dommer i økt ``okt``."""
    kd = tmp_path / "fase3-kjede"
    per_okt = []
    for n, k in dømt.items():
        ids = [f"FASE3-KJEDE-{n:02d}{i:03d}" for i in range(størrelse)]
        _skriv(kd / "blind" / f"blind-okt-{n}.jsonl", [{"id": i, "tekst": f"tekst {i}"} for i in ids])
        (kd / "blind" / f"oppdrag-okt-{n}.md").write_text(OPPDRAG.format(n=n, t=størrelse), encoding="utf-8")
        if k:
            _skriv(kd / f"7-verdikter-okt-{n}.jsonl", [_dom(i, treff=j % 5 == 0) for j, i in enumerate(ids[:k])])
        per_okt.append({"okt": n, "blind": str(kd / "blind" / f"blind-okt-{n}.jsonl")})
    t = {"ledd": {"blind": {"tid": "2026-09-30T03:02:24+00:00", "union": størrelse * len(dømt), "per_okt": per_okt},
                  "les": {"tid": "2026-09-30T05:50:20+00:00"}}}
    (kd / "tilstand.json").write_text(_json.dumps(t), encoding="utf-8")
    return kd


def test_etterkontrollen_stopper_på_en_økt_med_30_av_343(tmp_path):
    # Tilfellet fra 30.09: leserleddet førte seg ferdig med økt 3 på 30 av 343.
    kd = _kjøring(tmp_path, {1: 343, 3: 30})
    assert etterkontroll(kd, ["les"]) == ["les: økt 3 delvis: 30 av 343"]


def test_etterkontrollen_slipper_komplette_økter(tmp_path):
    assert etterkontroll(_kjøring(tmp_path, {1: 343, 2: 343}), ["les"]) == []


def test_etterkontrollen_ser_tomme_utdata_ugyldige_dommer_og_foreldede_ledd(tmp_path):
    kd = _kjøring(tmp_path, {1: 343})
    f = kd / "7-verdikter-okt-1.jsonl"
    rader = [_json.loads(l) for l in f.read_text().splitlines()]
    rader[5]["klasse"] = "N1"                        # treff: true med en ikke-treffklasse
    rader[5]["treff"] = True
    _skriv(f, rader)
    (kd / "7b-verksniva.jsonl").write_text("")
    t = _json.loads((kd / "tilstand.json").read_text())
    t["ledd"]["hent"] = {"tid": "2026-09-28T10:20:34+00:00", "verk": 100}
    t["ledd"]["verksniva"] = {"tid": "2026-09-30T05:25:33+00:00"}      # før les: regnet på gamle verdikter
    (kd / "tilstand.json").write_text(_json.dumps(t))
    m = etterkontroll(kd, ["les", "verksniva"])
    assert "les: økt 1: 1 ugyldige dommer, første FASE3-KJEDE-01005" in m
    assert "verksniva: 7b-verksniva.jsonl er tom" in m
    assert any(x.startswith("verksniva: ført 2026-09-30T05:25:33") and "foreldet" in x for x in m)


def test_ugyldige_dommer_krever_skjemaets_felt():
    ok = _dom("A", treff=True)
    assert ugyldige_dommer([ok, {**ok, "id": "B", "klasse": "H1/H7-uavklart"}]) == []
    assert ugyldige_dommer([{**ok, "id": "C", "tvil": None}, {**ok, "id": "D", "klasse": "H10"},
                            {**ok, "id": "E", "begrunnelse": " "}]) == ["C", "D", "E"]


def test_planen_tvinger_om_på_leddene_etter_les():
    første, andre = planlegg("les", om=False)
    assert første[0] == ["--from", "les", "--to", "les"]            # ingen --om uten at det er bedt om
    assert andre[0] == ["--from", "verksniva", "--om"]              # alltid --om etter les
    assert andre[1][-3:] == ["verksniva", "falsify", "register"]
    assert planlegg("falsify", om=False) == [(["--from", "falsify", "--om"], ["falsify", "register"])]


def test_fullføringen_rører_ikke_de_dømte_og_gjør_økta_komplett(tmp_path):
    kd = _kjøring(tmp_path, {3: 30})
    før = fotavtrykk(kd)
    sett = {}

    def kjør(oppdrag, utfil):
        sett["oppdrag"] = oppdrag
        blind = [_json.loads(l) for l in (utfil.parent / "blind.jsonl").read_text().splitlines()]
        _skriv(utfil, [_dom(r["id"]) for r in blind])
        return {"usage": {}, "minutter": 0.1}

    r = fullfør_økt(kd, 3, kjør=kjør)
    assert (r["dømt_før"], r["udømte"], r["føyd_til"], r["status"]) == (30, 313, 313, "komplett")
    assert overskrevet(kd, før) == []
    assert verdiktstatus(kd, [3])[3] == {"status": "komplett", "dømt": 343, "ventet": 343}
    assert "Les 313 blindede" in sett["oppdrag"] and "fullforing/okt-3-rest1/verdikter.jsonl" in sett["oppdrag"]
    # restfilene ligger utenfor mønstrene målingen globber, så ingen dom telles to ganger
    assert [p.name for p in kd.glob("7-verdikter-okt-*.jsonl")] == ["7-verdikter-okt-3.jsonl"]
    assert [p.name for p in (kd / "blind").glob("blind-okt-*.jsonl")] == ["blind-okt-3.jsonl"]


def test_en_ny_grense_midt_i_resten_gir_gyldig_prefiks_og_ny_rest(tmp_path):
    kd = _kjøring(tmp_path, {3: 30})

    def avbrutt(oppdrag, utfil):
        blind = [_json.loads(l) for l in (utfil.parent / "blind.jsonl").read_text().splitlines()]
        _skriv(utfil, [_dom(r["id"]) for r in blind[:100]] + [_dom("FEIL-ID")])
        return {"is_error": True}

    r = fullfør_økt(kd, 3, kjør=avbrutt)
    assert (r["føyd_til"], r["status"]) == (100, "delvis")
    assert etterkontroll(kd, ["les"]) == ["les: økt 3 delvis: 130 av 343"]
    r2 = fullfør_økt(kd, 3, kjør=lambda o, u: (_skriv(u, [_dom(x["id"]) for x in
                     (_json.loads(l) for l in (u.parent / "blind.jsonl").read_text().splitlines())]), {})[1])
    assert (r2["rest"], r2["dømt_før"], r2["status"]) == (2, 130, "komplett")


def test_fullføring_nekter_en_komplett_økt(tmp_path):
    with pytest.raises(GjenopptakNekt, match="komplett"):
        fullfør_økt(_kjøring(tmp_path, {1: 343}), 1, kjør=lambda o, u: {})


def test_omskriving_oppdages_men_forlengelse_er_lov(tmp_path):
    kd = _kjøring(tmp_path, {1: 30, 2: 343})
    før = fotavtrykk(kd)
    with (kd / "7-verdikter-okt-1.jsonl").open("a") as fh:
        fh.write(_json.dumps(_dom("X")) + "\n")
    assert overskrevet(kd, før) == []
    _skriv(kd / "7-verdikter-okt-2.jsonl", [_dom("NY")])            # leserleddet kjørte økta om
    n = før["7-verdikter-okt-2.jsonl"]["bytes"]
    assert overskrevet(kd, før) == [f"7-verdikter-okt-2.jsonl: de første {n} bytene er endret"]


def test_rest_oppdraget_nekter_når_malen_ikke_passer():
    with pytest.raises(GjenopptakNekt, match="inneholder ikke"):
        rest_oppdrag("et helt annet oppdrag", okt=3, ventet=343, rest=313, k=1)
