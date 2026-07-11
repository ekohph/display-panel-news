"""Streamlit chat web app over the display-panel news summaries.

Run from the repo root (or from app/):

    streamlit run app/app.py

The heavy lifting (RAG index + LangGraph pipeline) lives in engine.py /
graph/ / rag/. This file is UI only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# Make sibling modules importable whether launched from repo root or app/.
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from config import settings  # noqa: E402

st.set_page_config(page_title="Display Chat", page_icon="🖥️", layout="wide")


# --------------------------------------------------------------------------
# Cached backend (built once per session, survives Streamlit reruns)
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner="뉴스 인덱스와 그래프를 준비하는 중… (최초 1회는 임베딩 모델 다운로드로 느릴 수 있어요)")
def _load_engine():
    """Import + build the LangGraph chat app. Returns (module, graph)."""
    import engine  # imported lazily so the UI can show a helpful error

    graph = engine.build_chat_app()
    return engine, graph


def get_engine():
    try:
        return _load_engine()
    except ModuleNotFoundError as exc:  # missing pip deps
        st.error(
            f"필요한 패키지를 불러오지 못했습니다: `{exc.name}`.\n\n"
            "의존성을 설치하세요:\n\n"
            "```\npip install -r app/requirements.txt\n```"
        )
        st.stop()
    except Exception as exc:  # noqa: BLE001 - surface any build error to the user
        st.error(f"백엔드 초기화 실패: {exc}")
        st.stop()


# --------------------------------------------------------------------------
# Copy button (ChatGPT/Claude style) — small HTML/JS component.
# navigator.clipboard first, textarea+execCommand fallback for iframes.
# --------------------------------------------------------------------------
def copy_button(text: str, label: str = "📋 복사", key: str = "") -> None:
    payload = json.dumps(text)  # safely escape into a JS string literal
    btn_id = f"copybtn_{key}"
    components.html(
        f"""
        <button id="{btn_id}" style="
            font: 13px/1.2 system-ui, -apple-system, 'Segoe UI', sans-serif;
            padding: 4px 10px; border: 1px solid rgba(128,128,128,.4);
            border-radius: 6px; background: transparent; color: inherit;
            cursor: pointer;">{label}</button>
        <script>
        (function() {{
            const txt = {payload};
            const btn = document.getElementById("{btn_id}");
            btn.addEventListener("click", async function() {{
                try {{
                    await navigator.clipboard.writeText(txt);
                }} catch (e) {{
                    const ta = document.createElement("textarea");
                    ta.value = txt;
                    ta.style.position = "fixed"; ta.style.opacity = "0";
                    document.body.appendChild(ta); ta.focus(); ta.select();
                    try {{ document.execCommand("copy"); }} catch (e2) {{}}
                    document.body.removeChild(ta);
                }}
                const old = btn.innerText;
                btn.innerText = "✅ 복사됨";
                setTimeout(function() {{ btn.innerText = old; }}, 1200);
            }});
        }})();
        </script>
        """,
        height=40,
    )


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 설정")
    st.caption("Chat LLM (LMStudio / OpenAI 호환)")

    # Show the model that will actually be sent (auto-detected if LLM_MODEL=auto).
    try:
        import llm as _llm

        resolved_model = _llm.resolve_model()
    except Exception:  # noqa: BLE001
        resolved_model = settings.llm_model
    st.code(
        f"base_url = {settings.llm_base_url}\n"
        f"model    = {resolved_model}\n"
        f"temp     = {settings.llm_temperature}",
        language="text",
    )
    st.caption("임베딩 (로컬)")
    st.code(f"embed = {settings.embed_model}", language="text")

    if st.button("🔄 모델 새로고침", use_container_width=True,
                 help="LMStudio에서 모델을 바꾼 뒤 눌러 재감지 + 그래프 재빌드"):
        try:
            import llm as _llm

            _llm.clear_model_cache()
        except Exception:  # noqa: BLE001
            pass
        _load_engine.clear()
        st.rerun()

    st.divider()
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("♻️ RAG 인덱스 재생성", use_container_width=True):
        # Drop the persisted index and the cached graph, then rebuild.
        import shutil

        if settings.index_dir.exists():
            shutil.rmtree(settings.index_dir, ignore_errors=True)
        _load_engine.clear()
        st.success("인덱스를 지웠습니다. 다음 질문에서 다시 만듭니다.")

    st.divider()
    st.caption(
        "그래프 노드: `panel_maker` · `buyer` · `vendor`\n\n"
        "각 노드는 자기 카테고리 뉴스만 검색(RAG)합니다."
    )


# --------------------------------------------------------------------------
# Renderers
# --------------------------------------------------------------------------
def _render_meta(meta: dict) -> None:
    """Render which nodes ran and which sources were used."""
    route = meta.get("route") or []
    sources = meta.get("sources") or []
    if route:
        st.caption("🔀 사용한 노드: " + ", ".join(f"`{r}`" for r in route))
    if sources:
        with st.expander(f"📚 참고한 뉴스 {len(sources)}건"):
            for s in sources:
                urls = s.get("urls") or []
                if urls:
                    # Title links to the original article; extra URLs = 교차 확인.
                    label = f"**{s['date']}** · `{s['category']}` — [{s['title']}]({urls[0]})"
                    if len(urls) > 1:
                        label += " · " + " · ".join(
                            f"[교차 확인 {i}]({u})" for i, u in enumerate(urls[1:], 1)
                        )
                    st.markdown(f"- {label}")
                else:
                    # No source URL in this chunk (e.g. 핵심 요약 표) — show the file.
                    st.markdown(f"- **{s['date']}** · `{s['category']}` — {s['title']}\n\n  `{s['path']}`")


def _render_assistant(content: str, meta: dict | None, key) -> None:
    """Assistant answer + sources + a per-message copy button."""
    st.markdown(content)
    if meta:
        _render_meta(meta)
    copy_button(content, "📋 답변 복사", key=f"ans{key}")


def _render_llm_error(exc: Exception) -> None:
    """Friendly, actionable error instead of a raw traceback."""
    msg = str(exc)
    low = msg.lower()
    st.error("답변 생성 중 오류가 발생했습니다.")
    if "devicelost" in low or "getfencestatus" in low or "vk::" in low:
        st.warning(
            "**LMStudio GPU(Vulkan) 장치가 추론 중 다운됐습니다 (ErrorDeviceLost).** "
            "앱이 아니라 GPU/드라이버/VRAM 쪽 문제입니다. 아래를 시도해 보세요:\n\n"
            "- LMStudio 모델 로드 설정에서 **GPU Offload 레이어 수 낮추기** (또는 0 = CPU)\n"
            "- 더 **작은 모델 / 낮은 양자화(Q4_K_M 등)** 로 교체해 VRAM 확보\n"
            "- **Context length** 줄이기\n"
            "- Runtime 을 **Vulkan → CPU** (또는 CUDA/ROCm) 로 변경\n"
            "- GPU 드라이버 업데이트 후 **모델 다시 로드**"
        )
    elif any(k in low for k in ("connection", "refused", "getaddrinfo", "max retries", "timed out", "timeout")):
        st.warning(
            f"**LMStudio 서버에 연결하지 못했습니다.** `{settings.llm_base_url}` 에서 "
            "Local Server가 실행 중이고 모델이 로드됐는지 확인하세요."
        )
    st.caption("오류 상세 (아래 코드박스 우측 상단 아이콘으로 복사):")
    st.code(msg, language="text")


# --------------------------------------------------------------------------
# Main chat area
# --------------------------------------------------------------------------
st.title("🖥️ 기술 경향 챗봇")
st.caption("`summaries/` 의 공개 뉴스 브리핑을 근거로 답합니다. LMStudio LLM + LangGraph RAG.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            _render_assistant(msg["content"], msg.get("meta"), key=i)
        else:
            st.markdown(msg["content"])

# Copy the whole conversation
if st.session_state.messages:
    transcript = "\n\n".join(
        f"[{'나' if m['role'] == 'user' else '어시스턴트'}]\n{m['content']}"
        for m in st.session_state.messages
    )
    copy_button(transcript, "🗒️ 전체 대화 복사", key="all")

prompt = st.chat_input("예: 최근 TCL CSOT 8.6세대 장비 발주 상황 알려줘")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    engine, graph = get_engine()

    with st.chat_message("assistant"):
        try:
            with st.spinner("뉴스를 찾아 답변 생성 중…"):
                history = [(m["role"], m["content"]) for m in st.session_state.messages[:-1]]
                result = engine.run_turn(graph, prompt, history)
        except Exception as exc:  # noqa: BLE001 - show a clean error, no traceback
            _render_llm_error(exc)
        else:
            _render_assistant(result["answer"], result, key=len(st.session_state.messages))
            st.session_state.messages.append(
                {"role": "assistant", "content": result["answer"], "meta": result}
            )
