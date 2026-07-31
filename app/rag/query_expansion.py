"""Alias-driven query expansion for lexical retrieval."""

from __future__ import annotations

from pathlib import Path

import yaml

ALIASES_FILE = Path(__file__).with_name("query_aliases.yml")


def _load_groups() -> list[list[str]]:
    """Load valid alias groups; a missing file simply means no expansion."""
    if not ALIASES_FILE.exists():
        return []
    with ALIASES_FILE.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    groups: list[list[str]] = []
    for group in raw.get("groups", []):
        aliases = group.get("aliases", []) if isinstance(group, dict) else []
        cleaned = [alias.strip() for alias in aliases if isinstance(alias, str) and alias.strip()]
        if cleaned:
            groups.append(cleaned)
    return groups


def expand_query(query: str) -> str:
    """Add equivalent aliases for every term group matched by ``query``.

    The original wording remains first, preserving its lexical BM25 signal.
    Additions are deduplicated case-insensitively, so a user can write both
    ``inkjet`` and ``잉크젯`` without repeatedly expanding the same terms.
    """
    normalized = query.casefold()
    additions: list[str] = []
    seen: set[str] = set()

    for aliases in _load_groups():
        if not any(alias.casefold() in normalized for alias in aliases):
            continue
        for alias in aliases:
            folded = alias.casefold()
            if folded in normalized or folded in seen:
                continue
            additions.append(alias)
            seen.add(folded)

    return " ".join([query, *additions]) if additions else query
