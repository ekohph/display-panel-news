"""Rebuild the RAG index from summaries/ — standalone CLI.

Intended to run as the LAST step of the Codex briefing automation, right after
a new daily briefing markdown is saved, so the chat app's index always matches
the latest content:

    python app/build_index.py

Notes:
- Always rebuilds from scratch (the corpus is small; takes well under a minute
  plus the one-time embedding-model load).
- A Streamlit app that is already running keeps its in-memory index until the
  sidebar "🔄 모델 새로고침" button is clicked or the app is restarted.
"""

from __future__ import annotations

import sys
import time
from collections import Counter
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def main() -> int:
    from config import settings
    from rag.loader import load_documents
    from rag.vectorstore import rebuild_vectorstore

    t0 = time.time()
    docs = load_documents()
    cats = Counter(d.metadata["category"] for d in docs)
    dates = sorted({d.metadata["date"] for d in docs})
    print("corpus:")
    for name, path in settings.corpus_dirs:
        print(f"  {name}: {path}")
    print(f"chunks   : {len(docs)}  {dict(cats)}")
    if dates:
        print(f"dates    : {dates[0]} .. {dates[-1]} ({len(dates)} days)")

    vs = rebuild_vectorstore()
    print(f"index    : {vs.document_count} BM25 chunks -> {settings.index_dir}")
    print(f"done in {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
