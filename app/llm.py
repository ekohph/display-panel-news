"""Chat LLM factory.

`get_LLM()` is the single place the rest of the app obtains a chat model.
Everything downstream depends only on the LangChain `BaseChatModel` interface,
so swapping the backend (a different LMStudio machine, Ollama, a hosted API,
etc.) is a config change here — no other file changes.
"""

from __future__ import annotations

import functools

from langchain_openai import ChatOpenAI

from config import settings

# Values that mean "figure out the model id from the server" rather than a
# real, pinned model identifier.
_AUTO_MODEL_SENTINELS = {"", "auto", "local-model", "local"}


@functools.lru_cache(maxsize=1)
def _autodetect_model() -> str | None:
    """Ask the OpenAI-compatible server which model is loaded.

    Newer LMStudio rejects a placeholder model id and requires the real one
    (e.g. ``google/gemma-4-e4b``). We query ``/v1/models`` and pick the first
    non-embedding model. Cached so we only hit the server once.
    """
    try:
        from openai import OpenAI

        client = OpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            timeout=8,
        )
        ids = [m.id for m in client.models.list().data]
    except Exception:
        return None
    chat_ids = [i for i in ids if "embed" not in i.lower()]  # skip embedders
    pool = chat_ids or ids
    return pool[0] if pool else None


def clear_model_cache() -> None:
    """Forget the auto-detected model (call after loading a different model)."""
    _autodetect_model.cache_clear()


def resolve_model() -> str:
    """The model id to send: explicit config wins, else auto-detect."""
    configured = (settings.llm_model or "").strip()
    if configured.lower() not in _AUTO_MODEL_SENTINELS:
        return configured  # user pinned a specific model — respect it
    return _autodetect_model() or configured or "local-model"


def get_LLM(**overrides):
    """Return the chat LLM (a LangChain chat model).

    Default target is a local LMStudio server exposing an OpenAI-compatible
    API at ``settings.llm_base_url`` (``http://localhost:1234/v1``).

    Swap the LLM without touching call sites:
      * Move it to another PC:  set ``LLM_BASE_URL=http://<host>:1234/v1``
      * Pin a specific model:   set ``LLM_MODEL=google/gemma-4-e4b``
      * Auto-detect (default):  leave ``LLM_MODEL=auto`` and the loaded model
                                is read from the server.

    ``overrides`` lets callers tweak per-call params, e.g.
    ``get_LLM(temperature=0)`` for the deterministic router.

    # ---- To use a non-OpenAI-compatible backend on another PC ----
    # Return any LangChain chat model here instead of ChatOpenAI, e.g.:
    #   from langchain_ollama import ChatOllama
    #   return ChatOllama(base_url=..., model=...)
    # The rest of the code is unaffected as long as it is a BaseChatModel.
    """
    params = dict(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        model=resolve_model(),
        temperature=settings.llm_temperature,
        timeout=120,
    )
    params.update(overrides)
    return ChatOpenAI(**params)
