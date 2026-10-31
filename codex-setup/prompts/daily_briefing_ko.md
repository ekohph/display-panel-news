# Daily Display Panel Briefing Prompt

## Recurring tracking topics

Check these four topics on every industrial-news pass and in Sunday/monthly research searches. Search touch separately within display sensors. Use `display-panel-news/codex-setup/reference/search_queries.md` from the workflow root.

1. Display sensors: sensors integrated into or used with display panels, including optical/fingerprint, proximity, ambient-light and NIR sensing when a display application is established. Touch is a separate search subtopic covering in-cell/on-cell, capacitive/optical touch, stylus/pen input and touch integration across product segments. General NIR sensor research alone is outside this topic.
2. Stretchable display: emitters, TFTs, electrodes/interconnects, substrates, encapsulation, strain/image compensation, manufacturing and reliability.
3. Neuromorphic TFT: synaptic transistors, oxide/organic TFTs, optoelectronic synapses, plasticity, learning and device/array integration. Track independently; direct display application is not required.
4. Glass packaging: glass substrates/core substrates/interposers, through-glass vias (TGV), redistribution layers, panel-level packaging, equipment, processes and reliability. Track independently, including semiconductor packaging; direct display application is not required.

These definitions govern topic eligibility alongside the general display scope, including oxide/IGZO research, and take precedence over general display-anchor and non-display-application filters. Check every topic and touch separately even when the company-news scan has no candidates. Daily checks cover industrial news; broad paper searches follow Sunday/monthly research cadence. Include substantive, verifiable, non-duplicate findings only; omit empty sections and avoid quotas. State demonstrated applications accurately without assuming display use. Public briefings describe technology and findings without editorial-policy history.

Use this prompt after reading `codex-setup/README.md`, `codex-setup/config/*.yml`, and `codex-setup/reference/source_urls.yml`.

## Task

Create today's Korean Markdown briefing for public display-panel news.

## Scope

Cover meaningful public developments related to:

- display panel makers and panel manufacturing;
- panel buyers and display product strategy;
- platform ecosystem requirements that affect display specs or adoption;
- display supply chain, materials, equipment, regulation, and market data;
- research only when the cadence rules allow it.

Keep the writing company-neutral. Do not imply that the user belongs to any specific company. Do not create a special recurring section for one company.

## Process

1. Determine today's local date and reference time.
2. Review the latest existing summary and the dedupe index to avoid duplicates.
3. Start with the core source groups in `config/sources.yml` and `reference/source_urls.yml`; do not re-read the full workspace.
4. Use Google News RSS queries from `reference/search_queries.md` only as a broad discovery layer, then follow original publisher URLs.
5. Expand to broader web search only when the first-pass scan finds one or more candidate items or when the gap since the last summary is significant.
6. Deduplicate by URL, DOI, official source, and normalized headline.
7. Include only items with clear display relevance or a recurring tracking topic match.
8. Keep the output compact: use the minimum necessary sections and one source link per item unless a second source adds clear value.
9. Write the output under the path defined in `config/output_paths.yml`.
10. If `app/build_index.py` exists in this repository, run `python app/build_index.py`
    after saving the briefing so the local RAG chat index includes the new file.
    Skip silently if the script or its dependencies are not present.

## Output Format

Use Korean Markdown:

```md
# Display Panel News Summary - YYYY-MM-DD

YYYY년 M월 D일 HH:mm KST 기준으로 정리한 공개 디스플레이 패널 뉴스 브리핑입니다.

## 핵심 요약

- ...

## 패널 메이커 및 공급망 동향

- ...
  원문: https://...

## Panel buyers 동향

- ...
  원문: https://...

## Platform ecosystem

- ...
  원문: https://...
```

Omit sections with no meaningful content.

## Source Link Rules

- Put `원문` directly under the relevant bullet.
- Add `교차 확인` only when the second source adds useful verification.
- Do not add a standalone source list section.

## Safety Rules

- Do not use private sources.
- Do not cite Google News wrapper URLs; cite the original publisher URL.
- Exclude `wikileaks-kr.org` unless the user explicitly asks to inspect it. If it appears in broad search, treat it only as a weak lead and require stronger primary, official, or major-media corroboration before inclusion.
- Do not mention internal assumptions, private automation state, or personal context.
- Do not send email.
- Do not push unless the user explicitly approves.
