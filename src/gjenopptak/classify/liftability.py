"""Løftbarhet fra tabell, med uavklarte naboklasser (ADR-0004, ADDENDUM-05).

ADR-0004 slår fast at løftbarhet er en ren oppslagsfunksjon fra hindringsklasse
til den låste verdien i PREREG §5, og at ingen modell får sette den.

ADDENDUM-05 legger til fire klasser for tilfellene der passasjen ikke avgjør om
hindringen var arbeidsmengde eller manglende data. De får ``uavklart``, ikke
``ja``: PREREG §5 gir H1 «ja», og målingen i ADDENDUM-05 viser at det anslaget er
kjent for høyt.
"""

from __future__ import annotations

#: PREREG §5, ordrett. Endres bare ved nytt addendum med egen sha256.
PREREG_TABLE: dict[str, str] = {
    "H1": "ja",
    "H2": "ja",
    "H3": "ja_med_forbehold",
    "H4": "ja",
    "H5": "delvis",
    "H6": "ja",
    "H7": "nei",
    "H8": "nei",
    "H9": "nei",
}

#: ADDENDUM-05: naboparene der datamangel er fellesnevneren. H7 er ikke-løftbar,
#: så en uavklart koding kan ikke arve den løftbare naboens verdi.
UNRESOLVED: dict[str, tuple[str, str]] = {
    "H1/H7-uavklart": ("H1", "H7"),
    "H2/H7-uavklart": ("H2", "H7"),
    "H3/H7-uavklart": ("H3", "H7"),
    "H5/H7-uavklart": ("H5", "H7"),
}

#: Ikke-treff. Har ingen løftbarhet.
NON_HITS = ("N1", "N2", "N3")

TABLE_VERSION = "PREREG-v1-§5 + ADDENDUM-05"


class UnknownClass(KeyError):
    """Klassen finnes ikke i tabellen. Kjeden skal feile, ikke gjette."""


def liftability(obstacle_class: str) -> str:
    """Slå opp løftbarhet. Aldri avledet fra en modell (ADR-0004)."""
    if obstacle_class in PREREG_TABLE:
        return PREREG_TABLE[obstacle_class]
    if obstacle_class in UNRESOLVED:
        return "uavklart"
    if obstacle_class == "UNSURE":
        return "usikker"
    if obstacle_class in NON_HITS:
        raise UnknownClass(f"{obstacle_class} er et ikke-treff og har ingen løftbarhet")
    raise UnknownClass(f"ukjent hindringsklasse: {obstacle_class!r}")


def is_unresolved(obstacle_class: str) -> bool:
    return obstacle_class in UNRESOLVED


def liftable_share(classes: list[str]) -> dict:
    """Andel løftbare, med uavklarte som eget tall utenfor brøken.

    ADDENDUM-05: uavklarte regnes **ikke** inn i løftbar andel. De står for seg,
    fordi å fordele dem ville gjenskape nøyaktig den overvurderingen tabellen nå
    er kjent for.
    """
    treff = [c for c in classes if c not in NON_HITS]
    uavklart = [c for c in treff if is_unresolved(c)]
    avklart = [c for c in treff if not is_unresolved(c)]
    loftbare = [c for c in avklart if liftability(c) in ("ja", "ja_med_forbehold", "delvis")]
    return {
        "n_hits": len(treff),
        "n_resolved": len(avklart),
        "n_unresolved": len(uavklart),
        "n_liftable": len(loftbare),
        "share_liftable_of_resolved": (len(loftbare) / len(avklart)) if avklart else None,
        "share_unresolved_of_hits": (len(uavklart) / len(treff)) if treff else None,
        "table_version": TABLE_VERSION,
    }


def format_liftable(classes: list[str]) -> str:
    """Den eneste rapporteringsformen: løftbar andel og uavklart andel sammen."""
    r = liftable_share(classes)
    if not r["n_hits"]:
        return "ingen treff"
    lo = r["share_liftable_of_resolved"]
    uo = r["share_unresolved_of_hits"]
    return (f"løftbar {r['n_liftable']}/{r['n_resolved']} av avklarte "
            f"= {lo:.0%}; uavklart {r['n_unresolved']}/{r['n_hits']} = {uo:.0%} "
            f"(tabell: {r['table_version']})")


# --------------------------------------------------------------------------- #
# ADR-0010: løftbarhet er datert. Vurderingene er en tilføyelseslogg.
# --------------------------------------------------------------------------- #

import re as _re

_ISO = _re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

#: Datoen skal aldri være finere enn kilden tillater (ADR-0010 tillegg).
_PRESISJON = {4: "år", 7: "måned", 10: "dag"}


class VurderingLaast(RuntimeError):
    """En skrevet vurdering endres ikke. Ny kunnskap føyes til, den overskriver ikke."""


#: Hvem vurderingen tilhører. Klassen kan være lest ut av forfatterens egen tekst, eller vurdert av oss.
FORFATTERENS = "forfatterens egen formulering, klassifisert av oss"
OSS = "oss"


def vurdering(obstacle_class: str, vurdert_dato: str, *, vurdert_av: str,
              tabellversjon: str = TABLE_VERSION, grunn: str | None = None,
              kilde: str | None = None) -> dict:
    """Én datert løftbarhetsvurdering. Verdien slås opp, aldri settes (ADR-0004).

    Datoen skrives så fin som kilden tillater og ikke finere: ``2019``, ``2019-11`` eller
    ``2019-11-05``. Presisjonen utledes av formen og føres med. ``vurdert_av`` er påkrevd —
    en vurdering uten eier kan ikke etterprøves.
    """
    if not _ISO.match(vurdert_dato or ""):
        raise ValueError(
            f"vurdert_dato må være ÅÅÅÅ, ÅÅÅÅ-MM eller ÅÅÅÅ-MM-DD, fikk {vurdert_dato!r}. "
            "Finn ikke på en dag kilden ikke gir."
        )
    if not tabellversjon:
        raise ValueError("tabellversjon er påkrevd: oppslaget er (klasse, tabellversjon, dato)")
    if not vurdert_av:
        raise ValueError("vurdert_av er påkrevd: en vurdering bærer alltid hvem som gjorde den")
    return {"vurdert_dato": vurdert_dato, "datopresisjon": _PRESISJON[len(vurdert_dato)],
            "tabellversjon": tabellversjon, "obstacle_class": obstacle_class,
            "verdi": liftability(obstacle_class), "grunn": grunn, "kilde": kilde,
            "vurdert_av": vurdert_av}


def gjeldende(vurderinger: list[dict]) -> dict:
    """Nyeste vurdering. Ved samme dato gjelder den sist tilføyde."""
    if not vurderinger:
        raise ValueError("ingen vurderinger: en oppføring uten dato er ufullstendig (ADR-0010)")
    return max(enumerate(vurderinger), key=lambda iv: (iv[1]["vurdert_dato"], iv[0]))[1]


def foey_til(claim: dict, ny: dict) -> dict:
    """Føy til en vurdering. Tidligere vurderinger blir stående, uendret.

    Returnerer en ny post; den gamle listen kopieres. Enhver operasjon som ville endret
    eller fjernet en eksisterende vurdering, avvises — en historikk som kan redigeres,
    er ikke en historikk.
    """
    gamle = list(claim.get("loftbarhet", []))
    for felt in ("vurdert_dato", "datopresisjon", "tabellversjon", "obstacle_class", "verdi", "vurdert_av"):
        if felt not in ny:
            raise ValueError(f"vurderingen mangler {felt}")
    if not _ISO.match(ny["vurdert_dato"]):
        raise ValueError(f"vurdert_dato må være ISO-dato, fikk {ny['vurdert_dato']!r}")
    for g in gamle:
        if g["vurdert_dato"] == ny["vurdert_dato"] and g != ny:
            raise VurderingLaast(
                f"det finnes alt en vurdering datert {ny['vurdert_dato']} med annet innhold. "
                "En vurdering endres ikke; datér den nye riktig."
            )
    if ny["vurdert_dato"] < gjeldende(gamle)["vurdert_dato"] if gamle else False:
        raise VurderingLaast("en ny vurdering kan ikke dateres før den gjeldende")
    ut = dict(claim)
    ut["loftbarhet"] = gamle + [dict(ny)]
    return ut
