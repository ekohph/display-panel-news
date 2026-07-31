"""Thin orchestration layer between the Streamlit UI and the LangGraph app."""

from __future__ import annotations

from graph.build import build_graph


def build_chat_app():
    """Build (and compile) the LangGraph chat pipeline. Heavy: called once."""
    return build_graph()


def _dedupe_sources(sources: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for s in sources:
        key = (s.get("path"), s.get("title"), s.get("date"))
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def run_turn(graph, question: str) -> dict:
    """Run one independent chat turn. Returns {answer, route, sources}."""
    initial = {
        "question": question,
        "route": [],
        "contexts": [],
        "sources": [],
        "answer": "",
    }
    result = graph.invoke(initial)
    return {
        "answer": result.get("answer", ""),
        "route": result.get("route", []),
        "sources": _dedupe_sources(result.get("sources", [])),
    }
