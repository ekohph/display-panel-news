# Display Panel News — Chat App

`summaries/` 의 공개 뉴스 브리핑을 근거로 대화하는 Streamlit 챗봇입니다.
채팅 LLM은 **LMStudio**(OpenAI 호환 서버), 검색은 **scikit-learn BM25 RAG**,
파이프라인은 **LangGraph**(노드: `panel_maker` · `buyer` · `vendor`)로 구성됩니다.

## 구조

```
app/
├── app.py            # Streamlit 채팅 UI (엔트리포인트)
├── engine.py         # 그래프 호출 래퍼 (build_chat_app / run_turn)
├── config.py         # 환경변수 → Settings
├── embeddings.py     # get_LLM() / get_embedding() ← 모델 공급자 팩토리
├── rag/
│   ├── loader.py       # summaries 파싱 + panel_maker/buyer/vendor 분류
│   └── vectorstore.py  # BM25 인덱스 build/load + 카테고리별 retriever
└── graph/
    ├── state.py        # LangGraph 상태
    ├── nodes.py        # router + 카테고리 노드 + synthesize
    └── build.py        # build_graph()
```

파이프라인: `router` → (`panel_maker` | `buyer` | `vendor`)\* → `synthesize`.
라우터가 질문에 필요한 뉴스 소스를 고르고, 선택된 노드가 자기 카테고리 뉴스만
RAG로 검색한 뒤, 마지막에 근거 기반으로 답을 생성합니다.

## 사전 준비: LMStudio

1. LMStudio에서 채팅 모델을 하나 로드합니다.
2. **Local Server**를 시작합니다 (기본 `http://localhost:1234`).

## 설치 & 실행

```powershell
# 리포 루트에서
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt

# (선택) 설정 커스터마이즈
copy app\.env.example app\.env   # 필요 시 편집

streamlit run app/app.py
```

최초 실행 시 BM25 인덱스를 빌드합니다. 임베딩 모델 다운로드는 없습니다.
인덱스는 `app/.rag_index/bm25_store.joblib` 에 저장되고 이후 재사용됩니다.

## 모델 공급자 교체

그래프는 `embeddings.py`의 `get_LLM()`만 사용합니다. 현재는 LMStudio를 반환하며,
향후 다른 LLM 공급자를 적용할 때도 이 함수만 교체하면 됩니다. BM25를 쓰는 동안
`get_embedding()`은 `None`을 반환합니다.

## BM25 기본 검색

기본 검색기는 scikit-learn `CountVectorizer` 기반의 BM25입니다. 한국어 형태소
분석기 없이도 회사명·제품명·공정명을 검색할 수 있도록 2~4자 character n-gram을
사용하며, 인덱스는 `app/.rag_index/bm25_store.joblib`에 저장됩니다.

`rag/query_aliases.yml`의 동의어 그룹은 질의에 자동 확장됩니다. 예를 들어
`inkjet`을 검색하면 `잉크젯`, `ink-jet`, `IJP`도 함께 검색합니다.

현재 BM25 모드에서는 임베딩 모델이나 API 호출이 없습니다. 향후 dense-vector
저장소(예: Chroma)를 사용할 때에는 `embeddings.py`의 `get_embedding()`에
공급자 구현을 추가하면 됩니다.

## ChromaDB 동기화

`update_chroma_index.py`는 `summaries/`를 bullet 단위로 chunking하고, 설정된
dense embedding provider로 벡터를 만든 뒤 ChromaDB에 upsert합니다. 동일한
chunk는 안정적인 ID를 사용하며, 삭제되거나 수정된 Markdown chunk도 다음 실행에서
동기화됩니다.

```powershell
# app/embeddings.py의 get_embedding()을 구현한 뒤
.\app\update_chroma_index.ps1

# 컬렉션 전체를 다시 만들고 싶을 때만 사용
.\app\update_chroma_index.ps1 -Reset
```

실행 전 `langchain-chroma`, `chromadb`와 선택한 embedding provider 의존성을
설치해야 합니다.
