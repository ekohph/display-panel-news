"""Model-provider factory.

Only this module knows how to construct the chat LLM or an optional dense
embedding provider.  The rest of the app imports ``get_LLM()`` and
``get_embedding()`` so either provider can be replaced later without changing
the graph, retrievers, or Chroma update script.
"""

from __future__ import annotations

import functools

from config import settings

_AUTO_MODEL_SENTINELS = {"", "auto", "local-model", "local"}


@functools.lru_cache(maxsize=1)
def _resolve_lmstudio_model() -> str | None:
    """Detect the loaded LMStudio chat model when ``LLM_MODEL=auto``."""
    try:
        from openai import OpenAI

        client = OpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            timeout=8,
        )
        ids = [model.id for model in client.models.list().data]
    except Exception:
        return None
    chat_ids = [model_id for model_id in ids if "embed" not in model_id.lower()]
    return (chat_ids or ids or [None])[0]


def _model_id() -> str:
    configured = settings.llm_model.strip()
    if configured.lower() not in _AUTO_MODEL_SENTINELS:
        return configured
    return _resolve_lmstudio_model() or configured or "local-model"


def get_LLM(**overrides):
    """Return the LangChain chat model currently used by the application.

    The default implementation is LMStudio's OpenAI-compatible local server.
    Replace only this function when another provider becomes available; callers
    rely solely on the LangChain chat-model interface.
    """
    from langchain_openai import ChatOpenAI

    params = {
        "base_url": settings.llm_base_url,
        "api_key": settings.llm_api_key,
        "model": _model_id(),
        "temperature": settings.llm_temperature,
        "timeout": 120,
    }
    params.update(overrides)
    return ChatOpenAI(**params)


def get_embedding():
    """Return an optional dense embedding provider, or ``None`` by default.

    BM25 does not need embeddings. When a provider is ready, implement it here
    and return an object exposing ``embed_documents`` and
    ``embed_query``.  Chroma indexing code already calls this function.
    """
    return None
