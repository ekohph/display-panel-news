"""LangGraph nodes: router -> {panel_maker, buyer, vendor} -> synthesize.

- ``router_node`` decides which news-source nodes are relevant (LLM, with a
  keyword fallback).
- Each category node retrieves only its own category's news via RAG.
- ``synthesize_node`` grounds the final answer on the retrieved context.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from config import CATEGORIES, settings

# --------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------
ROUTER_SYSTEM = (
    "너는 디스플레이 패널 뉴스 질문을 분류하는 라우터야. "
    "질문에 답하려면 어떤 뉴스 소스가 필요한지 고른다.\n"
    "- panel_maker: 패널 제조사 (Samsung Display, LG Display, BOE, TCL CSOT, Tianma, Visionox 등)\n"
    "- buyer: 패널 구매/디바이스 기업 (Apple, 삼성전자, LG전자, 현대차·기아, Meta, Valve 등)\n"
    "- vendor: 공급망·장비·소재·시장·플랫폼 (장비/소재사, DDI, 유리, microLED, VESA, Intel, 가격·출하 등)\n"
    "필요한 카테고리만 쉼표로 구분해 출력해. 여러 개면 여러 개, 애매하면 셋 다 출력. "
    "라벨 외 다른 설명은 절대 쓰지 마."
)


def _keyword_route(question: str) -> list[str]:
    """Fallback routing from the loader's lexicon; defaults to all three."""
    from rag.loader import CATEGORY_KW

    q = question.lower()
    hits = [cat for cat, kws in CATEGORY_KW.items() if any(kw in q for kw in kws)]
    return hits or list(CATEGORIES)


def _parse_route(text: str) -> list[str]:
    found = [cat for cat in CATEGORIES if cat in text.lower()]
    # preserve canonical order, drop dups
    return [c for c in CATEGORIES if c in found]


def router_node(state, llm) -> dict:
    question = state["question"]
    try:
        resp = llm.invoke(
            [SystemMessage(content=ROUTER_SYSTEM), HumanMessage(content=question)]
        )
        route = _parse_route(resp.content)
    except Exception:
        route = []
    if not route:
        route = _keyword_route(question)
    return {"route": route}


def all_categories_node(_state) -> dict:
    """Bypass LLM routing and retrieve every category."""
    return {"route": list(CATEGORIES)}


def route_selector(state) -> list[str]:
    """Path function for conditional edges: fan out to the chosen nodes."""
    return state.get("route") or list(CATEGORIES)


# --------------------------------------------------------------------------
# Category (news-source) nodes
# --------------------------------------------------------------------------
def make_category_node(category: str, retriever):
    """Build a node that retrieves and formats this category's news."""

    def node(state) -> dict:
        docs = retriever.invoke(state["question"])
        if not docs:
            return {}
        body = "\n\n".join(d.page_content for d in docs)
        context = f"### [{category}] 관련 뉴스\n{body}"
        sources = [
            {
                "date": d.metadata.get("date", ""),
                "category": d.metadata.get("category", category),
                "title": d.metadata.get("title", ""),
                "path": d.metadata.get("path", ""),
                "urls": d.metadata.get("urls", []),
                "companies": d.metadata.get("companies", []),
            }
            for d in docs
        ]
        return {"contexts": [context], "sources": sources}

    node.__name__ = f"{category}_node"
    return node


# --------------------------------------------------------------------------
# Synthesis
# --------------------------------------------------------------------------
SYNTH_SYSTEM = (
    "너는 디스플레이 패널 산업 뉴스 어시스턴트야. "
    "아래 '뉴스 컨텍스트'에 있는 내용만 근거로 한국어로 답한다.\n"
    "규칙:\n"
    "- 컨텍스트에 없는 내용은 지어내지 말고, 모르면 모른다고 말한다.\n"
    "- 가능하면 날짜와 회사명을 함께 언급한다.\n"
    "- 답변 끝에 근거가 된 뉴스의 날짜와, 컨텍스트에 '원문:' URL이 있으면 그 URL을 간단히 표기한다.\n"
    "- 간결하고 사실 위주로 답한다."
)


def synthesize_node(state, llm) -> dict:
    contexts = state.get("contexts") or []
    context_block = "\n\n".join(contexts).strip() or "(관련 뉴스를 찾지 못했습니다.)"

    # Keep the prompt small to avoid overloading weak local GPU backends.
    budget = settings.max_context_chars
    if len(context_block) > budget:
        context_block = context_block[:budget].rstrip() + "\n\n…(컨텍스트 일부 생략)"

    user_prompt = (
        f"질문:\n{state['question']}\n\n"
        f"뉴스 컨텍스트:\n{context_block}"
    )
    # Deliberately stateless: each answer is grounded only in this question
    # and the newly retrieved news context.
    messages = [SystemMessage(content=SYNTH_SYSTEM), HumanMessage(content=user_prompt)]
    resp = llm.invoke(messages)
    return {"answer": resp.content}
