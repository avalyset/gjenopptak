"""Saxton & Rawls (2006): implementasjonen reproduserer artikkelens egen tabell 3.

Verifikasjonen kjøres som test, ikke bare én gang: endres likningene, faller denne.
"""

from gjenopptak.falsify import saxton_rawls as SR

# Tabell 3, «Example estimated water characteristic values for texture classes at 2.5%w organic
# matter, no salinity, gravel or density adjustment». Kolonnene er Sand %w, Clay %w, WP, FC, SAT
# (%v, heltall) og matrisk tetthet (g cm⁻³).
TABELL_3 = [
    ("Sa", 88, 5, 5, 10, 46, 1.43), ("LSa", 80, 5, 5, 12, 46, 1.43),
    ("SaL", 65, 10, 8, 18, 45, 1.46), ("L", 40, 20, 14, 28, 46, 1.43),
    ("SiL", 20, 15, 11, 31, 48, 1.38), ("Si", 10, 5, 6, 30, 48, 1.38),
    ("SaCL", 60, 25, 17, 27, 43, 1.50), ("CL", 30, 35, 22, 36, 48, 1.39),
    ("SiCL", 10, 35, 22, 38, 51, 1.30), ("SiC", 10, 45, 27, 41, 52, 1.26),
    ("SaC", 50, 40, 25, 36, 44, 1.47), ("C", 25, 50, 30, 42, 50, 1.33),
]


def test_tabell_3_reproduseres_eksakt():
    for navn, S, C, wp, fc, sat, rho in TABELL_3:
        s, c, om = S / 100, C / 100, 2.5
        assert round(SR.theta_1500(s, c, om) * 100) == wp, navn
        assert round(SR.theta_33(s, c, om) * 100) == fc, navn
        assert round(SR.theta_S(s, c, om) * 100) == sat, navn
        assert round(SR.rho_N(s, c, om), 2) == rho, navn


def test_fast_partikkeltetthet_kan_gi_FC_over_metning():
    """Kjernen i PS-246: likning [8] deler på 2,65, [9] senker FC bare 0,2 så mye."""
    # CQF Clay 1 i avhandlingen: C 0,48, S 0,19, OM 1,3 %, målt matrisk tetthet 1,64
    fast = SR.med_tetthet(0.19, 0.48, 1.3, rho=1.64)
    assert fast["theta_33_DF"] > fast["theta_S_DF"], "inkonsistensen avhandlingen beskriver"
    assert fast["fysisk_mulig"] is False
