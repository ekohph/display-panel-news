"""Retrieval backend factory.

The default backend is an on-disk scikit-learn BM25 index.  Keep this module's
public functions stable so graph code does not change when a future dense
vector backend is introduced.
"""

from __future__ import annotations

from config import settings
from rag.bm25 import BM25Index, get_retrievers as get_bm25_retrievers
from rag.loader import load_documents

INDEX_FILE = settings.index_dir / "bm25_store.joblib"


def rebuild_vectorstore() -> BM25Index:
    """Rebuild the persisted BM25 index from all current summary chunks."""
    if settings.retrieval_backend != "bm25":
        raise ValueError(
            f"Unsupported retrieval backend: {settings.retrieval_backend}. "
            "Only 'bm25' is configured in this version."
        )
    index = BM25Index.from_documents(load_documents())
    settings.index_dir.mkdir(parents=True, exist_ok=True)
    index.save(INDEX_FILE)
    return index


def build_or_load_vectorstore() -> BM25Index:
    """Load the persisted BM25 index, or build it on first use."""
    if settings.retrieval_backend != "bm25":
        raise ValueError(
            f"Unsupported retrieval backend: {settings.retrieval_backend}. "
            "Set RETRIEVAL_BACKEND=bm25."
        )
    if INDEX_FILE.exists():
        return BM25Index.load(INDEX_FILE)
    return rebuild_vectorstore()


def get_retrievers(index: BM25Index, k: int | None = None):
    return get_bm25_retrievers(index, k)
