"""Synchronize summary chunks into a persistent ChromaDB collection.

The script reuses ``rag.loader.load_documents()``, which parses every briefing
Markdown file into the same bullet-level chunks used by the chat app.  It then
embeds those chunks through ``embeddings.get_embedding()`` and upserts them
into Chroma.  IDs are deterministic, so rerunning the script is safe and only
changes chunks whose source text or metadata changed.

The default BM25-only configuration has no dense embedding provider. Implement
``get_embedding()`` before using this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from config import settings  # noqa: E402
from embeddings import get_embedding  # noqa: E402
from rag.loader import load_documents  # noqa: E402


def _chunk_id(document) -> str:
    """Create a stable ID that changes whenever the indexed chunk changes."""
    metadata = document.metadata
    source = "\x1f".join(
        [
            str(metadata.get("path", "")),
            str(metadata.get("date", "")),
            str(metadata.get("section", "")),
            str(metadata.get("title", "")),
            document.page_content,
        ]
    )
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def _chroma_metadata(metadata: dict) -> dict:
    """Convert loader metadata to Chroma's scalar-only metadata format."""
    clean: dict[str, str | int | float | bool] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            clean[key] = value
        else:
            clean[key] = json.dumps(value, ensure_ascii=False)
    return clean


def _batches(values: list, size: int):
    for start in range(0, len(values), size):
        yield values[start : start + size]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the ChromaDB news index.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete all existing chunks in the configured collection before indexing.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Number of chunks per embedding/upsert request (default: 32).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.batch_size < 1:
        raise ValueError("--batch-size must be at least 1")

    try:
        from langchain_chroma import Chroma
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Install Chroma dependencies with: pip install langchain-chroma chromadb"
        ) from exc

    embeddings = get_embedding()
    if embeddings is None:
        raise RuntimeError(
            "Chroma indexing needs a dense embedding provider. "
            "Implement get_embedding() in app/embeddings.py first."
        )

    documents = load_documents()
    ids = [_chunk_id(document) for document in documents]
    for document in documents:
        document.metadata = _chroma_metadata(document.metadata)

    vectorstore = Chroma(
        collection_name=settings.chroma_collection,
        persist_directory=str(settings.chroma_dir),
        embedding_function=embeddings,
    )

    existing_ids = set(vectorstore.get(include=[]).get("ids", []))
    desired_ids = set(ids)
    if args.reset and existing_ids:
        vectorstore.delete(ids=list(existing_ids))
        existing_ids.clear()

    stale_ids = existing_ids - desired_ids
    if stale_ids:
        vectorstore.delete(ids=list(stale_ids))

    for docs_batch, ids_batch in zip(_batches(documents, args.batch_size), _batches(ids, args.batch_size)):
        # langchain-chroma uses Chroma's upsert operation, so unchanged IDs are
        # harmless and changed source chunks replace their old vectors.
        vectorstore.add_documents(documents=docs_batch, ids=ids_batch)

    print(f"collection : {settings.chroma_collection}")
    print(f"directory  : {settings.chroma_dir}")
    print(f"chunks     : {len(documents)}")
    print(f"upserted   : {len(documents)}")
    print(f"deleted    : {len(stale_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
