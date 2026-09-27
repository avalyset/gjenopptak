"""Kjeden som én kjørbar sti: ramme → henting → tekstbiter → sil → leser → register.

ADR-0012 fester rekkefølgen og leservalget. ``docs/BYGGEPLAN.md`` B1 er kravlisten.
Konfigurasjonen ligger i én fil (``kjede.toml``); ingen sti er hardkodet i koden.
"""

from .konfig import Konfig, KonfigFeil, last
from .kvote import Behov, KvoteAvslag, behov_for_leser, port
from .ledd import LEDD, Kjøring, LeddFeil

__all__ = ["Konfig", "KonfigFeil", "last", "Behov", "KvoteAvslag", "behov_for_leser",
           "port", "LEDD", "Kjøring", "LeddFeil"]
