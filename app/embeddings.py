"""Embedding model factory for the RAG index.

`get_embeddings()` mirrors `get_LLM()`: it is the one place the app builds an
embedding model, so the RAG backend can be swapped without touching the
vector store or graph code.

Default: a local sentence-transformers model (runs fully offline on this PC,
no LMStudio embedding model required). The default is multilingual so Korean
summaries embed well.
"""

from __future__ import annotations

from config import settings


def get_embeddings():
    """Return a LangChain `Embeddings` instance.

    Default backend: local sentence-transformers via langchain-huggingface.
    Change the model with the ``EMBED_MODEL`` env var, or switch backend
    entirely below.

    # ================= SWAP EMBEDDINGS ON ANOTHER PC =================
    # The RAG code only depends on the LangChain Embeddings interface, so any
    # of these can be returned instead without changing vectorstore.py/graph.
    #
    # (A) LMStudio / OpenAI-compatible embeddings (needs an embedding model
    #     loaded in LMStudio, e.g. nomic-embed-text):
    #       from langchain_openai import OpenAIEmbeddings
    #       return OpenAIEmbeddings(
    #           base_url=settings.llm_base_url,   # or a dedicated EMBED_BASE_URL
    #           api_key=settings.llm_api_key,
    #           model="text-embedding-nomic-embed-text-v1.5",
    #           check_embedding_ctx_length=False,  # LMStudio needs this False
    #       )
    #
    # (B) A different local sentence-transformers model:
    #       just set EMBED_MODEL, e.g. jhgan/ko-sroberta-multitask
    #
    # NOTE: if you change the embedding model, delete app/.rag_index (or click
    # "RAG 인덱스 재생성" in the sidebar) so the index is rebuilt to match.
    # =================================================================
    """
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=settings.embed_model,
        encode_kwargs={"normalize_embeddings": True},
    )
