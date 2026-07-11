"""FAISS vector store: build/persist the index and expose per-category retrievers.

The index is persisted as a single serialized blob under ``app/.rag_index``
(git-ignored) and reused across runs. Delete that folder (or use the sidebar
"재생성" button) to rebuild — required whenever the embedding model or the
summaries change materially.

NOTE (Windows): we persist via ``serialize_to_bytes`` + Python file I/O rather
than ``FAISS.save_local``. ``save_local`` calls faiss' C++ ``write_index``,
which cannot open non-ASCII paths (e.g. a repo under ``...\\문서\\...``).
Serializing to bytes and writing with Python avoids that entirely.
"""

from __future__ import annotations

from langchain_community.vectorstores import FAISS

from config import CATEGORIES, settings
from embeddings import get_embeddings

from rag.loader import load_documents

# Single-file persisted index (Python writes it, so Unicode paths are fine).
INDEX_FILE = settings.index_dir / "faiss_store.bin"


def rebuild_vectorstore(embeddings=None):
    """Re-embed every summary chunk and overwrite the persisted index.

    Called by ``app/build_index.py`` (e.g. as the last step of the Codex
    briefing automation) and by the first-run path below.
    """
    embeddings = embeddings or get_embeddings()
    docs = load_documents()
    if not docs:
        raise RuntimeError(f"No chunks parsed from {settings.summaries_dir}")
    vs = FAISS.from_documents(docs, embeddings)

    settings.index_dir.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_bytes(vs.serialize_to_bytes())
    return vs


def build_or_load_vectorstore(embeddings=None):
    """Load the persisted FAISS index, or build it from the summaries."""
    embeddings = embeddings or get_embeddings()

    if INDEX_FILE.exists():
        data = INDEX_FILE.read_bytes()
        return FAISS.deserialize_from_bytes(
            serialized=data,
            embeddings=embeddings,
            allow_dangerous_deserialization=True,  # our own local index
        )

    return rebuild_vectorstore(embeddings)


def get_retrievers(vs, k: int | None = None) -> dict:
    """One retriever per category, filtered to that category's chunks.

    FAISS applies the metadata ``filter`` *after* fetching ``fetch_k`` nearest
    vectors. A small category (e.g. ``buyer``) would be starved if fetch_k were
    small, so we set fetch_k to the whole index (capped) — cheap for this
    corpus and guarantees each node gets its category's true top-k.
    """
    k = k or settings.top_k
    total = getattr(getattr(vs, "index", None), "ntotal", 0) or 0
    fetch_k = min(max(total, k * 20), 10000)
    retrievers = {}
    for cat in CATEGORIES:
        retrievers[cat] = vs.as_retriever(
            search_kwargs={
                "k": k,
                "fetch_k": fetch_k,
                "filter": {"category": cat},
            }
        )
    return retrievers
