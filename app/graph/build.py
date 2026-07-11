"""Assemble the LangGraph pipeline.

    START -> router -> (panel_maker | buyer | vendor)* -> synthesize -> END

The router picks which category nodes run; selected nodes retrieve their
category's news in parallel; synthesize grounds the final answer.
"""

from __future__ import annotations

from functools import partial

from langgraph.graph import END, START, StateGraph

from config import CATEGORIES
from graph import nodes
from graph.state import GraphState
from llm import get_LLM
from rag.vectorstore import build_or_load_vectorstore, get_retrievers


def build_graph():
    llm = get_LLM()                       # answer generation
    router_llm = get_LLM(temperature=0)   # deterministic routing

    vectorstore = build_or_load_vectorstore()
    retrievers = get_retrievers(vectorstore)

    g = StateGraph(GraphState)
    g.add_node("router", partial(nodes.router_node, llm=router_llm))
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
