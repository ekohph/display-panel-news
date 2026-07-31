"""Load and apply the canonical company vocabulary."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import yaml

ALIASES_FILE = Path(__file__).with_name("company_aliases.yml")


@dataclass(frozen=True)
class Company:
    """Canonical company identity and the accepted forms used to find it."""

    id: str
    name: str
    category: str
    aliases: tuple[str, ...]


@cache
def load_companies() -> tuple[Company, ...]:
    """Return well-formed company records from the YAML vocabulary."""
    if not ALIASES_FILE.exists():
        return ()
    with ALIASES_FILE.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    companies: list[Company] = []
    for item in raw.get("companies", []):
        if not isinstance(item, dict):
            continue
        company_id = item.get("id")
        name = item.get("name")
        category = item.get("category")
        aliases = item.get("aliases", [])
        if not isinstance(aliases, list):
            aliases = []
        if not all(isinstance(value, str) and value.strip() for value in (company_id, name, category)):
            continue
        cleaned = list(dict.fromkeys(
            alias.strip() for alias in [name, *aliases] if isinstance(alias, str) and alias.strip()
        ))
        if cleaned:
            companies.append(
                Company(company_id.strip(), name.strip(), category.strip(), tuple(cleaned))
            )
    return tuple(companies)


def company_alias_groups() -> list[list[str]]:
    """Expose company aliases in the same shape as generic query alias groups."""
    return [list(company.aliases) for company in load_companies()]


def _matches_alias(text: str, alias: str) -> bool:
    """Match Latin abbreviations as tokens and Korean/CJK aliases as substrings."""
    if alias.isascii():
        return re.search(
            rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])",
            text,
            flags=re.IGNORECASE,
        ) is not None
    return alias.casefold() in text.casefold()


def tag_companies(text: str) -> list[Company]:
    """Find every canonical company mentioned in a Markdown chunk."""
    tagged: list[Company] = []
    for company in load_companies():
        if any(_matches_alias(text, alias) for alias in company.aliases):
            tagged.append(company)
    return tagged
