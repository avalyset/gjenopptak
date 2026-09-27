"""Kontrollstreng-rammeverk.

Regelen: **et nullresultat teller ikke før en streng som MÅ treffe har
truffet.** En test som bare viser at noe ikke finnes, viser like gjerne at
søket er ødelagt — tom liste, feil felt, feil fil, parser som ga opp. Derfor
må hver telling først armeres av en positiv kontroll i samme korpus.

Alt telles i Python over datastrukturene selv, aldri ved å sende tekst til
grep. Tellingen skal se de samme postene som kjeden ser.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence


class ControlNotArmed(AssertionError):
    """Et nullresultat ble hevdet før en kontrollstreng hadde truffet."""


class ControlMissed(AssertionError):
    """En streng som MÅTTE treffe, traff ikke. Søket er ødelagt, ikke tomt."""


@dataclass
class Corpus:
    """Et navngitt korpus av strenger som kan telles med kontroll."""

    name: str
    items: Sequence[str]
    armed_by: list[str] = field(default_factory=list)

    @classmethod
    def from_records(cls, name: str, records: Iterable[dict], key: str | Callable[[dict], str]) -> "Corpus":
        getter = (lambda r: r[key]) if isinstance(key, str) else key
        return cls(name=name, items=[getter(r) for r in records])

    @property
    def armed(self) -> bool:
        return bool(self.armed_by)

    def count(self, needle: str, *, exact: bool = False) -> int:
        """Antall elementer som treffer. Ren Python, ingen subprocess."""
        if exact:
            return sum(1 for item in self.items if item == needle)
        return sum(1 for item in self.items if needle in item)

    def must_hit(self, needle: str, *, at_least: int = 1, exact: bool = False) -> int:
        """Krev treff, og armer korpuset for nullpåstander."""
        n = self.count(needle, exact=exact)
        if n < at_least:
            raise ControlMissed(
                f"kontrollstreng traff ikke i korpus {self.name!r}: {needle!r} "
                f"(fant {n}, krevde >= {at_least}; korpuset har {len(self.items)} elementer). "
                "Nullresultater fra dette korpuset er ikke gyldige."
            )
        self.armed_by.append(needle)
        return n

    def expect_none(self, needle: str, *, exact: bool = False) -> int:
        """Hevd at noe ikke finnes. Krever at korpuset er armert."""
        if not self.armed:
            raise ControlNotArmed(
                f"korpus {self.name!r}: expect_none({needle!r}) ble kalt før noen "
                "kontrollstreng hadde truffet. Et nullresultat teller ikke her."
            )
        n = self.count(needle, exact=exact)
        if n:
            raise AssertionError(f"korpus {self.name!r}: {needle!r} fantes {n} ganger, ventet 0")
        return 0

    def expect_count(self, needle: str, expected: int, *, exact: bool = False) -> int:
        if expected == 0:
            return self.expect_none(needle, exact=exact)
        n = self.count(needle, exact=exact)
        if n != expected:
            raise AssertionError(f"korpus {self.name!r}: {needle!r} fantes {n} ganger, ventet {expected}")
        self.armed_by.append(needle)
        return n
