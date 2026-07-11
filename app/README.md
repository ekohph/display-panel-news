# Display Panel News — Chat App

`summaries/` 의 공개 뉴스 브리핑을 근거로 대화하는 Streamlit 챗봇입니다.
채팅 LLM은 **LMStudio**(OpenAI 호환 서버), 검색은 **로컬 임베딩 + FAISS RAG**,
파이프라인은 **LangGraph**(노드: `panel_maker` · `buyer` · `vendor`)로 구성됩니다.

## 구조

```
app/
├── app.py            # Streamlit 채팅 UI (엔트리포인트)
├── engine.py         # 그래프 호출 래퍼 (build_chat_app / run_turn)
├── config.py         # 환경변수 → Settings
├── llm.py            # get_LLM()        ← 채팅 LLM 교체 지점
├── embeddings.py     # get_embeddings() ← 임베딩 교체 지점
├── rag/
│   ├── loader.py       # summaries 파싱 + panel_maker/buyer/vendor 분류
│   └── vectorstore.py  # FAISS 인덱스 build/load + 카테고리별 retriever
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
2. **Local Server** 를 시작합니다 (기본 `http://localhost:1234`).
   OpenAI 호환 엔드포인트 `/v1/chat/completions` 가 열립니다.

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

최초 실행 시 임베딩 모델 다운로드 + 인덱스 빌드로 잠깐 느릴 수 있습니다.
인덱스는 `app/.rag_index/` 에 저장되고 이후 재사용됩니다.

## 다른 PC / 다른 모델로 교체

- **채팅 LLM 위치 변경**: `app/.env` 의 `LLM_BASE_URL` 을 그 PC 주소로
  (`http://192.168.0.42:1234/v1`). 코드 변경 없음. → `app/llm.py`
- **채팅 모델 변경**: `LLM_MODEL` 수정.
- **임베딩 변경**: `EMBED_MODEL` 수정하거나 `app/embeddings.py` 에서 백엔드 교체.
  임베딩을 바꾸면 사이드바 **"RAG 인덱스 재생성"** 으로 인덱스를 다시 만듭니다.

모든 downstream 코드는 LangChain 인터페이스(`BaseChatModel` / `Embeddings`)에만
의존하므로, `get_LLM()` / `get_embeddings()` 만 바꾸면 나머지는 그대로 동작합니다.
