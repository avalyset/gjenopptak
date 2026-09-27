"""Saxton & Rawls (2006), likning [1]–[10]: jordvannkarakteristikk fra tekstur og organisk materiale.

Kilde: Saxton, K.E. og Rawls, W.J. (2006), «Soil Water Characteristic Estimates by Texture and
Organic Matter for Hydrologic Solutions», Soil Sci. Soc. Am. J. 70(5):1569–1578,
doi:10.2136/sssaj2005.0117. Likningsnumrene under er artikkelens egne (Table 1).

Enheter, som i artikkelen: ``S`` og ``C`` er desimalbrøk (0,20 = 20 %w), ``OM`` er %w (2,5 = 2,5 %w),
og vanninnholdene er volumbrøk (0,31 = 31 %v).

Tetthetsleddet er kjernen i PS-246: likning [8] deler på den **faste** partikkeltettheten 2,65,
og [9] senker markkapasiteten bare 0,2 så mye som metningen. Settes tettheten høyt nok, faller
θS-DF under θ33-DF — markkapasitet over metning, som er fysisk umulig.
"""

from __future__ import annotations

PARTIKKELTETTHET = 2.65  # g cm⁻³, fast i likning [6] og [8]


def theta_1500(S: float, C: float, OM: float) -> float:
    """Visnegrense, 1500 kPa. Likning [1]."""
    t = (-0.024 * S + 0.487 * C + 0.006 * OM + 0.005 * (S * OM)
         - 0.013 * (C * OM) + 0.068 * (S * C) + 0.031)
    return t + (0.14 * t - 0.02)


def theta_33(S: float, C: float, OM: float) -> float:
    """Markkapasitet (FC), 33 kPa, ved normal tetthet. Likning [2]."""
    t = (-0.251 * S + 0.195 * C + 0.011 * OM + 0.006 * (S * OM)
         - 0.027 * (C * OM) + 0.452 * (S * C) + 0.299)
    return t + (1.283 * t ** 2 - 0.374 * t - 0.015)


def theta_s33(S: float, C: float, OM: float) -> float:
    """Metning minus 33 kPa. Likning [3]."""
    t = (0.278 * S + 0.034 * C + 0.022 * OM - 0.018 * (S * OM)
         - 0.027 * (C * OM) - 0.584 * (S * C) + 0.078)
    return t + (0.636 * t - 0.107)


def theta_S(S: float, C: float, OM: float) -> float:
    """Mettet vanninnhold ved normal tetthet. Likning [5]."""
    return theta_33(S, C, OM) + theta_s33(S, C, OM) - 0.097 * S + 0.043


def rho_N(S: float, C: float, OM: float) -> float:
    """Normal tetthet, g cm⁻³. Likning [6]."""
    return (1 - theta_S(S, C, OM)) * PARTIKKELTETTHET


def med_tetthet(S: float, C: float, OM: float, *, rho: float | None = None,
                DF: float | None = None) -> dict:
    """Tetthetsjustering, likning [7]–[10].

    Oppgi enten en målt tetthet ``rho`` (g cm⁻³) eller justeringsfaktoren ``DF``.
    ``DF = rho / rho_N`` — det er den eneste veien inn for en målt tetthet, og den går gjennom
    den faste 2,65 i likning [8].
    """
    rn = rho_N(S, C, OM)
    if (rho is None) == (DF is None):
        raise ValueError("oppgi nøyaktig én av rho og DF")
    if DF is None:
        DF = rho / rn
    rdf = rn * DF                                             # [7]
    tS = theta_S(S, C, OM)
    tS_df = 1 - (rdf / PARTIKKELTETTHET)                      # [8]
    t33 = theta_33(S, C, OM)
    t33_df = t33 - 0.2 * (tS - tS_df)                         # [9]
    return {"rho_N": rn, "DF": DF, "rho_DF": rdf, "theta_33": t33, "theta_S": tS,
            "theta_33_DF": t33_df, "theta_S_DF": tS_df,
            "theta_S33_DF": tS_df - t33_df,                   # [10]
            "fysisk_mulig": t33_df <= tS_df}
