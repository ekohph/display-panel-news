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

# app/ directory and repo root (summaries live in <repo>/summaries)
APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent

# Load app/.env if present (does not override already-set env vars).
load_dotenv(APP_DIR / ".env")


def _get(key: str, default: str) -> str:
    val = os.getenv(key)
    return val if val not in (None, "") else default


@dataclass(frozen=True)
class Settings:
    # --- Chat LLM (LMStudio / OpenAI-compatible) ---
    llm_base_url: str = _get("LLM_BASE_URL", "http://localhost:1234/v1")
    llm_api_key: str = _get("LLM_API_KEY", "lm-studio")  # LMStudio ignores it
    # "auto" = detect the loaded model from the server's /v1/models.
    # Pin a specific id (e.g. google/gemma-4-e4b) to override.
    llm_model: str = _get("LLM_MODEL", "auto")
    llm_temperature: float = float(_get("LLM_TEMPERATURE", "0.3"))

    # --- RAG embeddings (local by default) ---
    embed_model: str = _get("EMBED_MODEL", "intfloat/multilingual-e5-small")

    # --- Retrieval ---
    top_k: int = int(_get("RAG_TOP_K", "3"))
    # Cap the total context sent to the LLM. Keeps the synthesize prompt small,
    # which matters a lot for weak/unstable local GPUs (large prompts can crash
    # the LMStudio Vulkan backend with ErrorDeviceLost). Raise it if your model
    # and GPU are comfortable with longer prompts.
    max_context_chars: int = int(_get("MAX_CONTEXT_CHARS", "2500"))

    # --- Paths ---
    summaries_dir: Path = REPO_ROOT / "summaries"
    index_dir: Path = APP_DIR / ".rag_index"


settings = Settings()

# Category identifiers used by both RAG metadata and graph nodes.
CATEGORIES = ("panel_maker", "buyer", "vendor")
