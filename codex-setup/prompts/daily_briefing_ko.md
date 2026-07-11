# Daily Display Panel Briefing Prompt

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
2. Review the latest existing summary to avoid duplicates.
3. Search the source groups in `config/sources.yml` and `reference/source_urls.yml`.
4. Use Google News RSS queries from `reference/search_queries.md` as a broad discovery layer, then follow original publisher URLs.
5. Use broader web search for missing public developments.
6. Deduplicate by URL, DOI, official source, and normalized headline.
7. Include only items with clear display relevance.
8. Write the output under the path defined in `config/output_paths.yml`.
9. If `app/build_index.py` exists in this repository, run `python app/build_index.py`
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
