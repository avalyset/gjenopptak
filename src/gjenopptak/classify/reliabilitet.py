"""Enighet mellom to kodere: rå enighet og Cohens κ med intervall.

κ korrigerer for enighet som ville oppstått ved tilfeldighet gitt hver koders egen
marginalfordeling. På skjevt materiale — der det ene utfallet dominerer — er κ strengere
enn rå enighet, og forskjellen mellom dem er selve poenget: to kodere som begge sier «nei»
til nesten alt, er enige uten å bevise noe.

Intervallet regnes både asymptotisk (Fleiss, Cohen & Everitt 1969) og som
persentilintervall fra bootstrapping. Bootstrap er hovedtallet: den asymptotiske formelen
er upålitelig når en celle er nær null, og det er den vanlige situasjonen her.
"""

from __future__ import annotations

import random
from collections import Counter
from typing import Sequence


def ra_enighet(a: Sequence, b: Sequence) -> float:
    if len(a) != len(b):
        raise ValueError("koderne må ha like mange vurderinger")
    if not a:
        raise ValueError("ingen vurderinger")
    return sum(1 for x, y in zip(a, b) if x == y) / len(a)


def cohen_kappa(a: Sequence, b: Sequence) -> float:
    """Cohens κ. Returnerer 0.0 når begge kodere er helt uten variasjon og enige."""
    n = len(a)
    if n != len(b) or n == 0:
        raise ValueError("koderne må ha like mange, minst én, vurdering")
    po = ra_enighet(a, b)
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[k] / n) * (cb.get(k, 0) / n) for k in ca)
    if pe == 1.0:
        return 0.0
    return (po - pe) / (1 - pe)


def kappa_se(a: Sequence, b: Sequence) -> float:
    """Asymptotisk standardfeil (Fleiss, Cohen & Everitt 1969), for to kategorier og flere."""
    n = len(a)
    po, k = ra_enighet(a, b), cohen_kappa(a, b)
    ca, cb = Counter(a), Counter(b)
    kat = sorted(set(ca) | set(cb), key=str)
    pi = {c: ca.get(c, 0) / n for c in kat}
    pj = {c: cb.get(c, 0) / n for c in kat}
    pe = sum(pi[c] * pj[c] for c in kat)
    if pe >= 1.0:
        return float("nan")
    par = Counter(zip(a, b))
    ledd1 = sum(par[(c, c)] / n * (1 - (pi[c] + pj[c]) * (1 - k)) ** 2 for c in kat)
    ledd2 = (1 - k) ** 2 * sum(par[(i, j)] / n * (pj[i] + pi[j]) ** 2
                               for i in kat for j in kat if i != j)
    ledd3 = (k - pe * (1 - k)) ** 2
    var = (ledd1 + ledd2 - ledd3) / (n * (1 - pe) ** 2)
    return var ** 0.5 if var > 0 else 0.0


def kappa_bootstrap(a: Sequence, b: Sequence, *, n_rep: int = 10_000, seed: int = 734248,
                    alfa: float = 0.05) -> tuple[float, float]:
    """Persentilintervall for κ. Paret resampling: enheten er passasjen, ikke vurderingen."""
    rng = random.Random(seed)
    n = len(a)
    par = list(zip(a, b))
    ut = []
    for _ in range(n_rep):
        s = [par[rng.randrange(n)] for _ in range(n)]
        x, y = [p[0] for p in s], [p[1] for p in s]
        try:
            ut.append(cohen_kappa(x, y))
        except ValueError:
            continue
    ut.sort()
    lo = ut[int((alfa / 2) * len(ut))]
    hi = ut[min(len(ut) - 1, int((1 - alfa / 2) * len(ut)))]
    return lo, hi


def enighet(a: Sequence, b: Sequence, *, navn: str = "") -> dict:
    """Rå enighet, κ, asymptotisk SE og bootstrapintervall i én post."""
    k = cohen_kappa(a, b)
    se = kappa_se(a, b)
    lo, hi = kappa_bootstrap(a, b)
    return {"navn": navn, "n": len(a), "ra_enighet": ra_enighet(a, b), "kappa": k,
            "se_asymptotisk": se, "ki_asymptotisk": [k - 1.96 * se, k + 1.96 * se] if se == se else None,
            "ki_bootstrap": [lo, hi],
            "marginaler": {"koder1": dict(Counter(a).most_common()), "koder2": dict(Counter(b).most_common())}}


#: Uavklarte par slås sammen med naboen de deler datamangel med (ADDENDUM-05).
SAMMENSLAA = {"H1/H7-uavklart": "H1~H7", "H2/H7-uavklart": "H2~H7",
              "H3/H7-uavklart": "H3~H7", "H5/H7-uavklart": "H5~H7",
              "H1": "H1~H7", "H7": "H1~H7", "H2": "H2~H7", "H3": "H3~H7", "H5": "H5~H7"}


def slaa_sammen(klasse: str | None) -> str | None:
    """H1/H7-paret og de øvrige uavklarte slås sammen med sin nabo."""
    return SAMMENSLAA.get(klasse, klasse)
