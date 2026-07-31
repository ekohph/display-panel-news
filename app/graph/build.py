"""Assemble the LangGraph pipeline.

    START -> router -> (panel_maker | buyer | vendor)* -> synthesize -> END

The optional router picks which category nodes run. When disabled, every
category runs without an additional LLM call; synthesize grounds the answer.
"""

from __future__ import annotations

from functools import partial

from langgraph.graph import END, START, StateGraph

from config import CATEGORIES, settings
from graph import nodes
from graph.state import GraphState
from embeddings import get_LLM
from rag.vectorstore import build_or_load_vectorstore, get_retrievers


def build_graph():
    llm = get_LLM()  # answer generation

    vectorstore = build_or_load_vectorstore()
    retrievers = get_retrievers(vectorstore)

    g = StateGraph(GraphState)
    if settings.router_enabled:
        router_llm = get_LLM(temperature=0)
        g.add_node("router", partial(nodes.router_node, llm=router_llm))
    else:
        g.add_node("router", nodes.all_categories_node)
    for cat in CATEGORIES:
        g.add_node(cat, nodes.make_category_node(cat, retrievers[cat]))
    g.add_node("synthesize", partial(nodes.synthesize_node, llm=llm))

    g.add_edge(START, "router")
    # Fan out from the router to whichever category nodes it selected.
    g.add_conditional_edges("router", nodes.route_selector, {c: c for c in CATEGORIES})
    # Fan in: every category node feeds the single synthesis node.
    for cat in CATEGORIES:
        g.add_edge(cat, "synthesize")
    g.add_edge("synthesize", END)

    return g.compile()
