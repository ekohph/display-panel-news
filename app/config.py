"""Central configuration for the display-panel news chat app.

All tunables come from environment variables (optionally an app/.env file),
so the app can be re-pointed at a different LLM / embedding model / machine
without code changes.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# app/ directory and repo root (summaries / trends live in <repo>/...)
APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent
WORKSPACE_ROOT = REPO_ROOT.parent

# Load app/.env if present (does not override already-set env vars).
load_dotenv(APP_DIR / ".env")


def _get(key: str, default: str) -> str:
    val = os.getenv(key)
    return val if val not in (None, "") else default


def _get_bool(key: str, default: bool = False) -> bool:
    return _get(key, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    # --- Chat LLM (LMStudio / OpenAI-compatible) ---
    llm_base_url: str = _get("LLM_BASE_URL", "http://localhost:1234/v1")
    llm_api_key: str = _get("LLM_API_KEY", "lm-studio")
    llm_model: str = _get("LLM_MODEL", "auto")
    llm_temperature: float = float(_get("LLM_TEMPERATURE", "0.3"))

    # --- Retrieval ---
    # ``bm25`` is deliberately the default: it has no model download or
    # embedding endpoint dependency.  ``chroma`` can be added later with an
    # embedding provider from embeddings.py.
    retrieval_backend: str = _get("RETRIEVAL_BACKEND", "bm25").lower()
    bm25_k1: float = float(_get("BM25_K1", "1.5"))
    bm25_b: float = float(_get("BM25_B", "0.75"))
    bm25_ngram_min: int = int(_get("BM25_NGRAM_MIN", "2"))
    bm25_ngram_max: int = int(_get("BM25_NGRAM_MAX", "4"))
    # For the current small corpus, searching every category is cheaper and
    # more reliable than making an additional LLM routing request.
    router_enabled: bool = _get_bool("RAG_ROUTER_ENABLED", False)

    # --- Optional dense-vector storage ---
    # The current BM25 path does not create embeddings.  A future provider is
    # implemented only in embeddings.get_embedding().
    chroma_dir: Path = APP_DIR / _get("CHROMA_DIR", ".chroma")
    chroma_collection: str = _get("CHROMA_COLLECTION", "display_panel_news")

    top_k: int = int(_get("RAG_TOP_K", "3"))
    # Cap the total context sent to the LLM. Keeps the synthesize prompt small,
    # which matters for weak/unstable local GPUs.
    max_context_chars: int = int(_get("MAX_CONTEXT_CHARS", "2500"))

    # --- RAG corpus paths ---
    summaries_dir: Path = REPO_ROOT / "summaries"
    trends_dir: Path = REPO_ROOT / "trends"
    pricing_research_dir: Path = WORKSPACE_ROOT / "panel-pricing-research"
    # Bump this when the chunk metadata or corpus scope changes. Existing
    # joblib indexes then rebuild automatically on their next use.
    rag_index_version: str = "corpus-v2"
    index_dir: Path = APP_DIR / ".rag_index"

    @property
    def corpus_dirs(self) -> tuple[tuple[str, Path], ...]:
        """Named Markdown roots included in the BM25 RAG corpus."""
        return (
            ("summaries", self.summaries_dir),
            ("trends", self.trends_dir),
            ("panel-pricing-research", self.pricing_research_dir),
        )


settings = Settings()

# Category identifiers used by both RAG metadata and graph nodes.
CATEGORIES = ("panel_maker", "buyer", "vendor")
