"""Shared state for the LangGraph chat pipeline."""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict


class GraphState(TypedDict, total=False):
    question: str
    route: list            # subset of {"panel_maker", "buyer", "vendor"}
    # Category nodes run in parallel and append; reducers merge their outputs.
    contexts: Annotated[list, operator.add]
    sources: Annotated[list, operator.add]
    answer: str
