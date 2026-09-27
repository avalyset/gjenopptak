"""Hvor mange trekk som må til for å fylle n hentbare verk (ADDENDUM-03 §2).

Rammen i ADDENDUM-01 §3.1 er tellbar; hentbarhet avgjøres først når verket
forsøkes hentet. Andelen som gir lesbar tekst, kalles her ``p`` og er målt, ikke
antatt. Alt under følger av p, og p har en konfidensintervall som må bæres med:
et punktanslag på antall nødvendige trekk skjuler at p er målt på 30 forsøk.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from ..harvest.coverage import wilson


@dataclass(frozen=True)
class Substitution:
    """Substitusjonsregnskap for ett felt."""

    field_key: str
    n_wanted: int
    readable: int
    attempted: int

    @property
    def p(self) -> float:
        return self.readable / self.attempted if self.attempted else 0.0

    @property
    def p_interval(self) -> tuple[float, float]:
        _, lo, hi = wilson(self.readable, self.attempted)
        return (lo, hi)

    @property
    def expected_draws(self) -> float:
        """Forventet antall trekk for å fylle n_wanted. n/p."""
        if self.p <= 0:
            return math.inf
        return self.n_wanted / self.p

    @property
    def draws_interval(self) -> tuple[float, float]:
        """Trekk-intervall som følger av p-intervallet. Merk rekkefølgen:
        lav p gir mange trekk, så øvre p-grense gir nedre trekk-grense."""
        lo, hi = self.p_interval
        return (self.n_wanted / hi if hi > 0 else math.inf,
                self.n_wanted / lo if lo > 0 else math.inf)

    @property
    def expected_substitutions(self) -> float:
        """Forventet antall substitusjoner for n_wanted plasser: n(1-p)/p."""
        if self.p <= 0:
            return math.inf
        return self.n_wanted * (1 - self.p) / self.p

    def draws_for_confidence(self, conf: float = 0.95, cap: int = 100_000) -> int:
        """Minste K der P(minst n_wanted hentbare av K trekk) >= conf.

        Punktanslaget n/p holder bare halvparten av gangene. Dette er tallet
        man faktisk må ha i reservelisten.
        """
        if self.p <= 0:
            return cap
        K = self.n_wanted
        while K <= cap:
            # P(X >= n) der X ~ Bin(K, p)
            hale = sum(
                math.comb(K, i) * self.p**i * (1 - self.p) ** (K - i)
                for i in range(self.n_wanted, K + 1)
            )
            if hale >= conf:
                return K
            K += 1
        return cap

    @property
    def flagged(self, grense: int = 60) -> bool:
        """Feltet flagges når forventet antall trekk overstiger grensen."""
        return self.expected_draws > grense
