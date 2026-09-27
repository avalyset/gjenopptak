"""JSON-skjemaer for kjeden. Alle poster bærer schema_version."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).resolve().parent
NAMES = ("documents", "sentences", "candidates", "claims", "kandidat", "registerhode")


@lru_cache(maxsize=None)
def load_schema(name: str) -> dict:
    """Les ett skjema. Navn uten suffiks, f.eks. load_schema("sentences")."""
    if name not in NAMES:
        raise ValueError(f"ukjent skjema: {name!r}; kjente: {NAMES}")
    return json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def validator(name: str) -> Draft202012Validator:
    schema = load_schema(name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate(name: str, record: dict) -> None:
    """Kast ved første feil. Kjeden skal feile på ugyldig post, ikke gjette."""
    validator(name).validate(record)


def errors(name: str, record: dict) -> list[str]:
    """Alle feil som tekst, i stabil rekkefølge. Til testbruk."""
    return [
        f"{'/'.join(str(p) for p in e.absolute_path) or '<rot>'}: {e.message}"
        for e in sorted(validator(name).iter_errors(record), key=lambda e: list(e.absolute_path))
    ]
