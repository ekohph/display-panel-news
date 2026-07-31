"""Streamlit chat web app over the display-panel news summaries.

Run from the repo root (or from app/):

    streamlit run app/app.py

The heavy lifting (RAG index + LangGraph pipeline) lives in engine.py /
graph/ / rag/. This file is UI only.
"""

from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# Make sibling modules importable whether launched from repo root or app/.
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from config import REPO_ROOT, settings  # noqa: E402

st.set_page_config(page_title="Display Chat", page_icon="🖥️", layout="wide")

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] div[data-testid="stExpander"] {
        border-color: transparent;
        box-shadow: none;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
        font-size: 0.8rem;
        line-height: 1.1;
        min-height: 0;
        padding: 0.08rem 0;
        white-space: nowrap;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] [data-testid="stHorizontalBlock"] {
        gap: 0.2rem;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #d9d9d9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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


@st.cache_resource(show_spinner=False)
def _load_bm25_index():
    """Load the persisted BM25 index for sidebar document search."""
    from rag.vectorstore import build_or_load_vectorstore

    return build_or_load_vectorstore()


def _search_chunks(query: str) -> list[tuple[str, str, float | None]]:
    """Return ranked chunks with their source Markdown paths."""
    from rag.query_expansion import expand_query

    index = _load_bm25_index()
    expanded_query = expand_query(query)
    search_with_scores = getattr(index, "search_with_scores", None)
    if callable(search_with_scores):
        ranked = search_with_scores(
            expanded_query, category=None, k=index.document_count
        )
    else:
        # A running Streamlit process can retain an index object created before
        # score-returning search was added.  Its document-only API is still
        # sufficient to select the matching Markdown files.
        ranked = [
            (document, None)
            for document in index.search(
                expanded_query, category=None, k=index.document_count
            )
        ]

    results: list[tuple[str, str, float | None]] = []
    for document, score in ranked:
        path = str(document.metadata.get("path", ""))
        if not path:
            continue
        results.append((path, document.page_content, score))
    return results


def _query_context(chunk: str, query: str) -> str:
    """Return the matching word plus up to five neighbouring words each side."""
    words = list(re.finditer(r"\S+", chunk))
    if not words:
        return ""
    match = re.search(re.escape(query), chunk, flags=re.IGNORECASE)
    index = next(
        (
            i
            for i, word in enumerate(words)
            if match is not None and word.start() <= match.start() < word.end()
        ),
        0,
    )
    return " ".join(word.group(0) for word in words[max(0, index - 5) : index + 6])


def _highlight_query(text: str, query: str) -> str:
    """Escape Markdown source and highlight the user-entered search phrase."""
    pattern = re.compile(re.escape(query), flags=re.IGNORECASE)
    return pattern.sub(lambda match: f"<mark>{escape(match.group(0))}</mark>", escape(text))


def _highlight_markdown(text: str, query: str) -> str:
    """Preserve Markdown while inserting a yellow highlight around the query."""
    pattern = re.compile(re.escape(query), flags=re.IGNORECASE)
    return pattern.sub(lambda match: f"<mark>{match.group(0)}</mark>", text)


def _read_markdown(relative_path: str) -> str | None:
    """Read a known repository-relative Markdown file without path traversal."""
    root = REPO_ROOT.resolve()
    path = (root / relative_path).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None
    if not path.is_file() or path.suffix.lower() != ".md":
        return None
    return path.read_text(encoding="utf-8")


def _select_document(relative_path: str) -> None:
    st.session_state["selected_document"] = relative_path


def _file_button_label(file: Path, *, weekly: bool = False) -> str:
    """Return a compact day label, or the ISO week label for weekly reports."""
    if weekly:
        week_match = re.fullmatch(r"\d{4}-(W\d{1,2})", file.stem, flags=re.IGNORECASE)
        if week_match:
            return week_match.group(1).upper()
    match = re.search(r"(?:^|[-_])(\d{1,2})$", file.stem)
    return match.group(1) if match else file.stem


def _render_file_tree(root: Path, label: str) -> None:
    """Render a collapsed folder with compact five-column file buttons."""
    with st.expander(f"📁 {label}", expanded=False):
        if not root.exists():
            st.caption("문서가 없습니다.")
            return
        for folder in sorted((item for item in root.iterdir() if item.is_dir()), key=lambda item: item.name):
            if label == "summaries":
                folder_key = f"folder-expanded:{folder.relative_to(REPO_ROOT).as_posix()}"
                is_expanded = st.session_state.get(folder_key, False)
                folder_icon = "📂" if is_expanded else "📁"
                if st.button(
                    f"{folder_icon} {folder.name}",
                    key=f"folder:{folder.relative_to(REPO_ROOT).as_posix()}",
                    use_container_width=True,
                ):
                    st.session_state[folder_key] = not is_expanded
                    st.rerun()
                if not is_expanded:
                    continue
            else:
                st.caption(f"📁 {folder.name}")
            files = sorted(folder.rglob("*.md"), key=lambda item: item.as_posix())
            is_weekly_folder = folder.name.casefold() == "weekly"
            column_count = 4 if is_weekly_folder else 5
            columns = st.columns(column_count)
            for index, file in enumerate(files):
                relative_path = file.relative_to(REPO_ROOT).as_posix()
                with columns[index % column_count]:
                    if st.button(
                        _file_button_label(file, weekly=is_weekly_folder),
                        key=f"file:{relative_path}",
                        help=file.name,
                        use_container_width=True,
                    ):
                        _select_document(relative_path)


def _render_document_preview(
    relative_path: str,
    score: float | None = None,
    *,
    full: bool = False,
    highlight: str | None = None,
) -> None:
    """Show a Markdown document or its opening portion in the main frame."""
    text = _read_markdown(relative_path)
    if text is None:
        st.warning(f"문서를 열 수 없습니다: `{relative_path}`")
        return
    path = Path(relative_path)
    heading = f"📄 {path.name}"
    if score is not None:
        heading += f"  ·  BM25 {score:.2f}"
    with st.container(border=True):
        st.subheader(heading)
        preview_chars = len(text) if full else 2800
        body = text[:preview_chars]
        st.markdown(
            _highlight_markdown(body, highlight) if highlight else body,
            unsafe_allow_html=highlight is not None,
        )
        if not full and len(text) > preview_chars:
            st.caption("문서 앞부분만 표시했습니다. 사이드바에서 파일을 선택하면 전체 내용을 볼 수 있습니다.")


def _render_search_results(
    query: str, results: list[tuple[str, str, float | None]]
) -> None:
    """Render paginated chunk search results as a two-column table."""
    page_size = 10
    if st.session_state.get("search_page_query") != query:
        st.session_state.search_page_query = query
        st.session_state.search_page = 0

    page_count = max(1, (len(results) + page_size - 1) // page_size)
    page = min(st.session_state.get("search_page", 0), page_count - 1)
    st.session_state.search_page = page
    start = page * page_size

    with st.container(border=True):
        date_header, content_header = st.columns([1, 6])
        date_header.markdown("**날짜**")
        content_header.markdown("**내용**")

    for offset, (path, chunk, _score) in enumerate(results[start : start + page_size]):
        with st.container(border=True):
            date_column, content_column = st.columns([1, 6])
            date = Path(path).stem
            with date_column:
                if st.button(date, key=f"result:{start + offset}:{path}"):
                    _select_document(path)
            with content_column:
                st.markdown(
                    _highlight_query(_query_context(chunk, query), query),
                    unsafe_allow_html=True,
                )

    if page_count > 1:
        previous, indicator, next_page = st.columns([1, 2, 1])
        with previous:
            if st.button("이전", disabled=page == 0, key="search_previous"):
                st.session_state.search_page = page - 1
                st.rerun()
        with indicator:
            st.caption(f"{page + 1} / {page_count} 페이지 · 총 {len(results)}건")
        with next_page:
            if st.button("다음", disabled=page >= page_count - 1, key="search_next"):
                st.session_state.search_page = page + 1
                st.rerun()


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
sidebar_query = ""
sidebar_matches: list[tuple[str, str, float | None]] = []
with st.sidebar:
    sidebar_query = st.text_input(
        "문서 검색",
        placeholder="BOE, CSOT, OLED ...",
        label_visibility="collapsed",
    ).strip()
    if sidebar_query:
        try:
            sidebar_matches = _search_chunks(sidebar_query)
        except Exception as exc:  # noqa: BLE001 - surface index/config issues in sidebar
            st.error(f"문서 검색을 준비하지 못했습니다: {exc}")

    _render_file_tree(settings.summaries_dir, "summaries")
    _render_file_tree(REPO_ROOT / "trends", "trends")


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
    if any(k in low for k in ("connection", "refused", "getaddrinfo", "max retries", "timed out", "timeout")):
        st.warning(
            f"**LMStudio 서버에 연결하지 못했습니다.** `{settings.llm_base_url}` 에서 "
            "Local Server가 실행 중이고 모델이 로드됐는지 확인하세요."
        )
    st.caption("오류 상세 (아래 코드박스 우측 상단 아이콘으로 복사):")
    st.code(msg, language="text")


# --------------------------------------------------------------------------
# Main chat area
# --------------------------------------------------------------------------
st.title("🖥️ 디스플레이 뉴스 Agent")

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

with st.container():
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

selected_document = st.session_state.get("selected_document")
if sidebar_query:
    st.subheader(f"문서 검색 결과: {sidebar_query}")
    st.caption("검색 결과의 날짜를 클릭하면 표 하단의 ‘선택한 문서’에서 해당 Markdown 파일 전체를 볼 수 있습니다.")
    if sidebar_matches:
        _render_search_results(sidebar_query, sidebar_matches)
    else:
        st.info("일치하는 BM25 chunk를 찾지 못했습니다.")
    st.divider()

    selected_document = st.session_state.get("selected_document")
    st.subheader("선택한 문서")
    if selected_document:
        _render_document_preview(selected_document, full=True, highlight=sidebar_query)
    else:
        st.info("검색 결과의 날짜를 선택하면 해당 Markdown 파일 전체를 표시합니다.")
    st.divider()
elif selected_document:
    st.subheader("선택한 문서")
    _render_document_preview(selected_document, full=True)
    st.divider()
