"""Persistent BM25 retrieval using scikit-learn sparse term matrices.

The corpus is Korean-heavy and contains many product/process names.  Character
n-grams avoid a mandatory Korean morphological analyser while keeping exact
company and technology terms searchable.
"""

from __future__ import annotations

from dataclasses import dataclass

import joblib
import numpy as np
from langchain_core.documents import Document
from sklearn.feature_extraction.text import CountVectorizer

from config import CATEGORIES, settings
from rag.query_expansion import expand_query


@dataclass
class BM25Index:
    documents: list[Document]
    vectorizer: CountVectorizer
    term_frequencies: object
    doc_lengths: np.ndarray
    idf: np.ndarray
    average_doc_length: float

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @classmethod
    def from_documents(cls, documents: list[Document]) -> "BM25Index":
        if not documents:
            raise RuntimeError("No documents available to build the BM25 index")

        vectorizer = CountVectorizer(
            analyzer="char_wb",
            ngram_range=(settings.bm25_ngram_min, settings.bm25_ngram_max),
            lowercase=True,
            dtype=np.float32,
        )
        term_frequencies = vectorizer.fit_transform([doc.page_content for doc in documents])
        doc_lengths = np.asarray(term_frequencies.sum(axis=1)).ravel().astype(np.float32)
        average_doc_length = float(doc_lengths.mean()) or 1.0
        document_frequency = np.diff(term_frequencies.tocsc().indptr)
        total = len(documents)
        idf = np.log1p((total - document_frequency + 0.5) / (document_frequency + 0.5)).astype(np.float32)
        return cls(documents, vectorizer, term_frequencies, doc_lengths, idf, average_doc_length)

    def search_with_scores(
        self, query: str, *, category: str | None, k: int
    ) -> list[tuple[Document, float]]:
        """Return the highest-scoring chunks with their BM25 scores."""
        query_vector = self.vectorizer.transform([query])
        terms = query_vector.indices
        if not len(terms):
            return []

        candidates = np.array(
            [i for i, doc in enumerate(self.documents) if category is None or doc.metadata.get("category") == category],
            dtype=np.int32,
        )
        if not len(candidates):
            return []

        tf = self.term_frequencies[candidates][:, terms].toarray()
        denominator = tf + settings.bm25_k1 * (
            1 - settings.bm25_b + settings.bm25_b * self.doc_lengths[candidates, None] / self.average_doc_length
        )
        scores = (tf * (settings.bm25_k1 + 1) / np.maximum(denominator, 1e-12) * self.idf[terms]).sum(axis=1)
        order = np.argsort(-scores, kind="stable")
        return [
            (self.documents[candidates[pos]], float(scores[pos]))
            for pos in order[:k]
            if scores[pos] > 0
        ]

    def search(self, query: str, *, category: str | None, k: int) -> list[Document]:
        """Return only documents for LangChain-compatible retrievers."""
        return [document for document, _ in self.search_with_scores(query, category=category, k=k)]

    def save(self, path) -> None:
        joblib.dump(self, path)

    @classmethod
    def load(cls, path) -> "BM25Index":
        return joblib.load(path)


class BM25Retriever:
    """Small LangChain-compatible adapter used by the existing graph nodes."""

    def __init__(self, index: BM25Index, category: str, k: int):
        self.index = index
        self.category = category
        self.k = k

    def invoke(self, query: str) -> list[Document]:
        return self.index.search(expand_query(query), category=self.category, k=self.k)


def get_retrievers(index: BM25Index, k: int | None = None) -> dict[str, BM25Retriever]:
    k = k or settings.top_k
    return {category: BM25Retriever(index, category, k) for category in CATEGORIES}
