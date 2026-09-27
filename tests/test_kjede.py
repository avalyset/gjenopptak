"""Testpakke for kjeden (byggeplanen B7). Kjører uten Vault, uten ollama, uten Claude Code.

Testene prøver det som kan gå galt stille: at en terskel er endret, at et skjema slipper gjennom en
rad det ikke skulle, at koblingsregelen mister en passasje, at ikke-prosa-regelen har flyttet seg.
De prøver **ikke** om modellene svarer — det krever ollama og et abonnement, og står i README.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gjenopptak.classify.ikkeprosa import bokstavandel, er_ikke_prosa, referansemonster
from gjenopptak.kjede import felt as F
from gjenopptak.kjede import konfig as K
from gjenopptak.kjede import sil as S
from gjenopptak.kjede.kvote import API_FORBUDT, Behov, behov_for_leser, port
from gjenopptak.schemas import validate, validator

ROT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def k() -> K.Konfig:
    return K.last(ROT / "kjede.toml")


# --------------------------------------------------------------------- konfigurasjon
def test_konfigen_finnes_og_har_alle_seksjoner(k):
    for s in ("kjede", "vault", "tekstbiter", "dommer", "ekstraksjon", "sil", "leser",
              "register", "kvote"):
        assert k.seksjon(s)


def test_api_seksjonen_avvises(tmp_path):
    """ADR-0012, datert tillegg: verktøyet kaller ikke Anthropics API."""
    f = tmp_path / "kjede.toml"
    f.write_text((ROT / "kjede.toml").read_text(encoding="utf-8") + '\n[api]\nnokkel = "x"\n',
                 encoding="utf-8")
    with pytest.raises(K.KonfigFeil, match="kaller ikke Anthropics API"):
        K.last(f)


def test_ingen_hardkodet_sti_i_kjeden():
    """Stier hører i kjede.toml. En absolutt sti i koden bryter B1."""
    for p in (ROT / "src/gjenopptak/kjede").glob("*.py"):
        tekst = p.read_text(encoding="utf-8")
        for linje in tekst.splitlines():
            if linje.lstrip().startswith("#") or '"""' in linje:
                continue
            assert "/Volumes/Vault/" not in linje, f"{p.name}: absolutt Vault-sti i kode"
            assert "/Users/" not in linje, f"{p.name}: absolutt hjemmesti i kode"


def test_tersklene_har_ikke_flyttet_seg(k):
    """De målte verdiene er låst til målingene. Endres én, er tallet ikke lenger målt."""
    assert k.verdi("tekstbiter", "window") == 2
    assert k.verdi("tekstbiter", "stride") == 3
    assert k.verdi("dommer", "fro") == 734248
    assert k.verdi("leser", "fro") == 734248
    assert k.verdi("dommer", "num_ctx") == 8192
    assert k.verdi("ekstraksjon", "num_ctx") == 8192
    assert k.verdi("leser", "okt_storrelse") == 356
    assert k.verdi("ekstraksjon", "kobling") == "alle-treff"
    assert k.verdi("leser", "presisjon_uten_tvil") == 0.976
    assert k.verdi("leser", "presisjon_med_tvil") == 0.759


def test_laaste_filer_stemmer_paa_sha(k):
    """Regelfil, ledetekster og ikke-prosa-regelen. Vault-filene hoppes over uten volum."""
    for navn, p, ventet in k.laaste_filer():
        if not p.is_file():
            pytest.skip(f"{navn} ikke tilgjengelig ({p})")
        assert K.sha256_fil(p) == ventet, navn


# ------------------------------------------------------------------------------ felt
def test_de_fire_feltene_finnes_og_leses(k):
    navn = F.navn_liste(k)
    for f in ("arkeologi", "energimodellering", "klinisk_epidemiologi", "tekstvitenskap"):
        assert f in navn
        d = F.last_felt(k, f)
        assert d.topics and all(t.startswith("T") for t in d.topics)
        assert d.ar[0] <= d.ar[1]
        assert len(d.ramme_sha256) == 64


def test_gulvet_staar_bare_paa_tekstvitenskap(k):
    """Måleskranken er ett felt, og det er en målt kjensgjerning, ikke en innstilling."""
    for f in F.navn_liste(k):
        d = F.last_felt(k, f)
        assert d.gulv == (25 if f == "tekstvitenskap" else 0), f


def test_ukjent_felt_lister_de_kjente(k):
    with pytest.raises(K.KonfigFeil, match="Kjente felt"):
        F.last_felt(k, "finnes-ikke")


# ------------------------------------------------------------------------------ silen
def _bit(doc, s, tekst):
    return S.Tekstbit(doc_id=doc, start_index=s, end_index=s + 4, felt="test", tekst=tekst)


def test_silen_forener_og_merker_kilden():
    biter = [_bit("W1", 0, "Vi kunne ikke måle X fordi data manglet."),
             _bit("W1", 3, "En helt annen setning uten noe ugjort."),
             _bit("W1", 6, "Tredje tekstbit her.")]
    kand, stat = S.dommer_union_ekstraksjon(
        biter, flagget={("W1", 0, 4)}, q_linjer=[("W1", "Tredje tekstbit her")])
    kilder = {k.bit.start_index: k.kilde for k in kand}
    assert kilder == {0: "dommer", 6: "ekstraksjon"}
    assert stat["union"] == 2 and stat["snitt"] == 0


def test_alle_treff_mister_ikke_passasjen_foerste_treff_mistet():
    """Regresjonstest for PS-300: Q-linjen lå i to overlappende vindu."""
    felles = "Dateringen lot seg ikke fastslå."
    biter = [_bit("W1", 0, f"Innledning. {felles}"), _bit("W1", 3, f"{felles} Og mer tekst.")]
    q = [("W1", felles)]
    alle, s_alle = S.dommer_union_ekstraksjon(biter, flagget=set(), q_linjer=q, alle_treff=True)
    ett, s_ett = S.dommer_union_ekstraksjon(biter, flagget=set(), q_linjer=q, alle_treff=False)
    assert s_alle["union"] == 2, "alle-treff skal ta begge vinduene"
    assert s_ett["union"] == 1, "første-treff tar bare det første — og det var feilen"
    assert s_alle["q_i_flere_vindu"] == 1


def test_ukoblet_q_linje_telles_og_forsvinner_ikke():
    _, stat = S.dommer_union_ekstraksjon(
        [_bit("W1", 0, "Noe tekst.")], flagget=set(),
        q_linjer=[("W1", "en setning som ikke finnes i teksten")])
    assert stat["q_ukoblet"] == 1 and stat["union"] == 0


def test_silregisteret_har_en_implementasjon():
    assert list(S.SILER) == ["dommer_union_ekstraksjon"]
    with pytest.raises(ValueError, match="ukjent sil"):
        S.velg("embeddings")


# ----------------------------------------------------------------------- ikke-prosa
def test_ikke_prosa_regelen_har_ikke_flyttet_seg():
    assert er_ikke_prosa(". . . . . . . . . .")
    assert er_ikke_prosa("50. 51. 52. 53.")
    assert er_ikke_prosa("Smith, J. (2015) 12–34.")
    assert er_ikke_prosa("pp. 120–145")
    assert not er_ikke_prosa(
        "The authors could not date the layer because no suitable sample was preserved.")
    assert bokstavandel("abc") == 1.0
    assert bokstavandel("") == 0.0
    assert referansemonster("A. B. C. Smith")


# --------------------------------------------------------------------------- kvoten
def test_kvoteporten_nekter_api_faser(k):
    svar = port(k, "test", Behov(api_kall=5), sjekk_api=False)
    assert not svar.slipper
    assert any("Anthropics API" in g for g in svar.grunner)
    assert "Max-abonnementet" in API_FORBUDT


def test_kvoteporten_regner_okter_fra_maalt_forbruk(k):
    b = behov_for_leser(k, 712)
    assert b.okter == 2
    assert b.kontekst_tokens == 712 * 25034
    assert b.harness_tokens == 2 * 287533


def test_kvoteporten_nekter_uten_harness_kvote(k, tmp_path, monkeypatch):
    """Leserkvoten kan ikke leses av kode. Da skal fasen nektes, ikke gjettes på."""
    monkeypatch.setattr(K.Konfig, "arbeid", property(lambda self: tmp_path))
    svar = port(k, "les", behov_for_leser(k, 100))
    assert not svar.slipper
    assert any("harness-kvoten er ukjent" in g for g in svar.grunner)


# --------------------------------------------------------------------------- skjema
def _rad() -> dict:
    return {
        "schema_version": "claims-2", "claim_id": "CLAIM-T-1", "candidate_id": "T-1",
        "doc_id": "W1", "field_key": "test", "obstacle_class": "H5", "tvil": False,
        "unit": "sentence",
        "passage_span": {"start_index": 0, "end_index": 4, "n_sentences": 5, "window": 2},
        "section_raw": "", "section_label_provenance": "parser",
        "sil": {"kilde": "begge", "presisjon": 0.345, "presisjon_ki": [0.298, 0.396],
                "ikke_prosa": False},
        "leser": {"modell": "claude-opus-5", "regelfil_sha256": "a" * 64,
                  "presisjon_ved_tvil": 0.976},
        "cites_coverage": {"fulltext_available": None, "fulltext_total": None,
                           "coverage_ratio": None, "status": "ikke målt"},
        "loftbarhet": [{"vurdert_dato": "2026-09-27", "tabellversjon": "PREREG-v1-§5",
                        "obstacle_class": "H5", "loftbar": "ja"}],
        "falsified": False, "tested_at": "2026-09-27T00:00:00+00:00",
    }


def test_en_gyldig_rad_valideres():
    validate("kandidat", _rad())


@pytest.mark.parametrize("nøkkel", ["tvil", "sil", "leser", "cites_coverage", "loftbarhet", "unit"])
def test_raden_avvises_naar_usikkerheten_mangler(nøkkel):
    """B3: en rad uten sin egen usikkerhet er ikke en leveranse."""
    r = _rad()
    del r[nøkkel]
    with pytest.raises(Exception):
        validate("kandidat", r)


def test_ugyldig_klasse_avvises():
    r = _rad()
    r["obstacle_class"] = "H12"
    with pytest.raises(Exception):
        validate("kandidat", r)


def test_dekning_kan_ikke_vaere_null_uten_maling():
    """«ikke målt» er ikke 0. Et umålt nulltall var én av ti grønn-og-feil-tilfeller."""
    r = _rad()
    r["cites_coverage"] = {"fulltext_available": 0, "fulltext_total": 0, "coverage_ratio": None}
    with pytest.raises(Exception):
        validate("kandidat", r)          # status mangler


def test_registerhodet_krever_forbeholdene():
    hode = {"kjøring": "t", "tid": "2026-09-27T00:00:00+00:00", "port": "ubekreftet kandidatliste",
            "bekreftet": False, "n_rader": 0, "n_dømt": 0, "adr": "ADR-0012",
            "forbehold": {"stabil_kjerne": "3 av 27", "n3_spredning": "5,8–13,6 %",
                          "ikke_prosa": "merket, aldri fjernet"}}
    validate("registerhode", hode)
    del hode["forbehold"]["stabil_kjerne"]
    with pytest.raises(Exception):
        validate("registerhode", hode)


def test_begge_skjemaene_er_gyldige():
    for n in ("kandidat", "registerhode"):
        validator(n)
