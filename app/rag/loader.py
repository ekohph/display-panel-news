"""Load the Korean news summaries into categorized LangChain documents.

Each markdown file under ``summaries/<month>/YYYY-MM-DD.md`` is split into
bullet-level chunks. Every chunk is tagged with one of the three graph
categories — ``panel_maker`` / ``buyer`` / ``vendor`` — using a keyword
lexicon over its section heading, subsection (company) heading and body.
The graph nodes later retrieve only the chunks that match their category.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from langchain_core.documents import Document

from config import REPO_ROOT, settings

# --------------------------------------------------------------------------
# Classification lexicon.  Keyword hits in the subsection heading count most,
# then the section heading, then the body.  Argmax picks the category.
# Extend these lists to tune routing (Korean + English forms both listed).
# --------------------------------------------------------------------------
PANEL_MAKER_KW = [
    "패널 메이커", "panel maker", "panel-maker",
    "samsung display", "삼성디스플레이", "sdc",
    "lg display", "lgd", "엘지디스플레이", "lg디스플레이",
    "boe", "csot", "tcl", "티안마", "tianma", "visionox", "비전옥스",
    "everdisplay", "edo", "joled", "auo", "innolux", "이노룩스",
    "sharp", "jdi", "hkc", "truly", "royole",
]
BUYER_KW = [
    "buyer", "바이어", "구매",
    "apple", "애플", "samsung electronics", "삼성전자",
    "lg electronics", "lg전자", "엘지전자",
    "hyundai", "현대차", "현대자동차", "kia", "기아",
    "meta", "메타", "valve", "밸브", "sony", "소니",
    "google", "구글", "microsoft", "마이크로소프트",
    "xiaomi", "샤오미", "huawei", "화웨이", "honor",
    "oppo", "오포", "vivo", "dell", "hp", "lenovo", "레노버",
    "asus", "even realities", "xreal", "rokid", "nintendo", "닌텐도",
]
VENDOR_KW = [
    # supply chain / equipment / materials
    "공급망", "supply chain", "supply-chain", "장비", "equipment",
    "소재", "materials", "증착", "deposition", "유리", "glass",
    "기판", "substrate", "driver ic", "ddi", "검사", "inspection",
    "encapsulation", "polarizer", "편광", "cover window", "규제", "regulation",
    "관세", "tariff",
    # named suppliers / equipment makers
    "sunic", "deviceeng", "hb solution", "agc", "corning", "코닝",
    "applied materials", "canon tokki", "ulvac", "jusung", "주성",
    "wonik", "원익", "ap시스템", "ap systems", "vesa", "jbd", "pixel-flo",
    # market / platform ecosystem (catch-all axis)
    "시장", "market", "수급", "pricing", "가격", "shipment", "출하",
    "microled", "micro-oled", "oledos", "platform", "ecosystem",
    "intel", "인텔", "nvidia", "엔비디아", "amd", "qualcomm", "퀄컴",
]

CATEGORY_KW = {
    "panel_maker": PANEL_MAKER_KW,
    "buyer": BUYER_KW,
    "vendor": VENDOR_KW,
}

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
# Source links inside a bullet: "원문: https://..." / "교차 확인: https://...".
# Bare URLs are matched too, as a fallback for less regular chunks.
URL_RE = re.compile(r"https?://[^\s)\]>]+")


@dataclass
class _Segment:
    section: str  # level-2 heading (## ...)
    sub: str      # level-3 heading (### ...) or ""
    body: str


def _iter_segments(text: str) -> list[_Segment]:
    """Split text into (section, sub, body) blocks on markdown headings."""
    segments: list[_Segment] = []
    section, sub = "", ""
    buf: list[str] = []

    def flush() -> None:
        body = "\n".join(buf).strip()
        if body and (section or sub):
            segments.append(_Segment(section, sub, body))

    for line in text.splitlines():
        if line.startswith("### "):
            flush()
            buf = []
            sub = line[4:].strip()
        elif line.startswith("## "):
            flush()
            buf = []
            section = line[3:].strip()
            sub = ""
        elif line.startswith("# "):
            flush()
            buf = []
            section, sub = "", ""  # H1 title / intro -> skip
        else:
            buf.append(line)
    flush()
    return segments


def _split_bullets(body: str) -> list[str]:
    """Split a segment body into per-top-level-bullet chunks."""
    chunks: list[str] = []
    cur: list[str] = []
    for line in body.splitlines():
        if line.startswith("- "):
            if cur:
                chunks.append("\n".join(cur).strip())
            cur = [line]
        else:
            cur.append(line)
    if cur:
        chunks.append("\n".join(cur).strip())
    return [c for c in chunks if c]


def classify(section: str, sub: str, body: str) -> str:
    """Assign one of panel_maker / buyer / vendor via weighted keyword hits."""
    hay_head = f"{sub} {section}".lower()
    hay_body = body.lower()
    scores = {"panel_maker": 0, "buyer": 0, "vendor": 0}
    for cat, kws in CATEGORY_KW.items():
        for kw in kws:
            if kw in hay_head:
                scores[cat] += 3  # heading match is a strong signal
            if kw in hay_body:
                scores[cat] += 1
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        # No signal at all -> vendor is the catch-all (supply/market/platform).
        return "vendor"
    return best


def load_documents() -> list[Document]:
    """Parse every summary file into categorized chunks."""
    docs: list[Document] = []
    summaries_dir: Path = settings.summaries_dir
    if not summaries_dir.exists():
        raise FileNotFoundError(f"summaries directory not found: {summaries_dir}")

    for md in sorted(summaries_dir.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        m = DATE_RE.search(md.stem)
        date = m.group(1) if m else md.stem
        rel = md.relative_to(REPO_ROOT).as_posix()

        for seg in _iter_segments(text):
            for chunk in _split_bullets(seg.body):
                category = classify(seg.section, seg.sub, chunk)
                title = seg.sub or seg.section
                # Prepend context so the LLM can ground and cite answers.
                content = (
                    f"[{date} | {category} | {title}]\n"
                    f"섹션: {seg.section}\n\n{chunk}"
                )
                # Original-article links (원문/교차 확인) for clickable sources.
                urls = list(dict.fromkeys(URL_RE.findall(chunk)))  # dedupe, keep order
                docs.append(
                    Document(
                        page_content=content,
                        metadata={
                            "date": date,
                            "category": category,
                            "title": title,
                            "section": seg.section,
                            "path": rel,
                            "urls": urls,
                        },
                    )
                )
    return docs
