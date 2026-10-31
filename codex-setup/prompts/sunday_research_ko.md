# Sunday Research Coverage Prompt

## Recurring tracking topics

Check these four topics on every industrial-news pass and in Sunday/monthly research searches. Search touch separately within display sensors. Use `display-panel-news/codex-setup/reference/search_queries.md` from the workflow root.

1. Display sensors: sensors integrated into or used with display panels, including optical/fingerprint, proximity, ambient-light and NIR sensing when a display application is established. Touch is a separate search subtopic covering in-cell/on-cell, capacitive/optical touch, stylus/pen input and touch integration across product segments. General NIR sensor research alone is outside this topic.
2. Stretchable display: emitters, TFTs, electrodes/interconnects, substrates, encapsulation, strain/image compensation, manufacturing and reliability.
3. Neuromorphic TFT: synaptic transistors, oxide/organic TFTs, optoelectronic synapses, plasticity, learning and device/array integration. Track independently; direct display application is not required.
4. Glass packaging: glass substrates/core substrates/interposers, through-glass vias (TGV), redistribution layers, panel-level packaging, equipment, processes and reliability. Track independently, including semiconductor packaging; direct display application is not required.

These definitions govern topic eligibility alongside the general display scope, including oxide/IGZO research, and take precedence over general display-anchor and non-display-application filters. Check every topic and touch separately even when the company-news scan has no candidates. Daily checks cover industrial news; broad paper searches follow Sunday/monthly research cadence. Include substantive, verifiable, non-duplicate findings only; omit empty sections and avoid quotas. State demonstrated applications accurately without assuming display use. Public briefings describe technology and findings without editorial-policy history.

Use this as an additional pass for Sunday briefings.

## Task

Search for meaningful display-related papers, preprints, university releases, research-lab releases, and public journal metadata from the previous Monday through Sunday. Also review arXiv computer-science categories `cs.AI`, `cs.CV`, `cs.LG`, `cs.CL`, and `cs.RO` for AI papers relevant to display devices, display manufacturing/inspection, or display materials.

## Required Inputs

- `config/research_rules.yml`
- `config/sources.yml`
- `reference/search_queries.md`
- `reference/source_urls.yml`
- Workflow state: `operations-local/known_papers.json`, `operations-local/seen_articles.json`, and `operations-local/research_coverage.md` when available in the workflow root.

## Search Strategy

1. Search publisher pages, Crossref and OpenAlex for the AI/display combinations in `reference/search_queries.md`, adapting them to the week's trends. Use these as discovery sources alongside arXiv, not merely as fallbacks.
2. Search arXiv and Crossref/OpenAlex/PubMed for newly published or newly indexed items. The arXiv CS category pass is required on Sundays, not optional.
3. Use publisher ASAP pages when accessible.
4. If publisher pages are blocked or not indexed, verify via DOI metadata or public abstract records.
5. Exclude weakly related papers.

## Papers explaining the week's trends

Add `## 이번 주 트렌드와 연결한 주요 논문 리뷰` after the new research and AI sections. Review one or two important papers tied to a concrete industrial or technical trend in this week's briefing. Search beyond the weekly publication window and compare new discoveries with known papers. Older and previously reported papers are allowed here; label them `첫 소개` or `재검토`, show original publication dates, and explain why they matter this week. Link earlier briefing coverage when available. Omit the section if no substantive connection exists.

If a newly found paper is more relevant than a known candidate, select it and tell the reader why its connection is stronger. Include the contribution, evidence, limitations and DOI/source. Do not duplicate a full summary across sections or label an older paper as new weekly research.

Persist relevant finds in the local known-paper register. Mark papers discussed with the user or included in a briefing as covered, keeping user acknowledgment separate from actual briefing history. Honor edition exclusions and no-reminder preferences. Already-covered status does not block a justified trend-linked revisit. Keep private correspondence out of public output.

## Weekly AI Top 1

From the prior week's AI papers, select exactly one Top 1 item across these three buckets:

1. AI directly applied to displays or display quality;
2. AI for manufacturing, process control, yield, defect detection, or inspection;
3. AI for materials discovery, formulation, or reliability relevant to display materials.

Rank first by direct display or panel-production relevance, then by technical significance and evidence quality. Explain the selection, the display connection, and the main limitation. If the best AI paper is only weakly connected to displays, keep it in a separate `## AI 관련 논문` section rather than presenting it as a display paper.

## Include Only When

The public record establishes a recurring tracking topic match, or explicitly connects the work to at least one of:

- display devices;
- panel architecture;
- display backplanes;
- OLED, LCD, AMOLED, QD, microLED, Micro-OLED, or microdisplay;
- display manufacturing;
- active matrix or pixel circuits;
- display materials with clear device relevance.

## Oxide TFT and IGZO Rule

Do not include standalone IGZO results.

For display-backplane IGZO or oxide-semiconductor papers outside the recurring tracking topics, require both:

1. a device term, such as `IGZO TFT`, `a-IGZO TFT`, `In-Ga-O TFT`, `IGO TFT`, `polycrystalline oxide TFT`, `oxide semiconductor TFT`, `thin-film transistor`, `oxygen diffusion`, `metal capping`, or `gate dielectric`; and
2. a display anchor, such as `display`, `panel`, `backplane`, `pixel`, `OLED`, `LCD`, `AMOLED`, `microdisplay`, or `active matrix`.

Outside the recurring tracking topics, exclude items whose only application is memory, BEOL logic, sensors, power electronics, or general semiconductor integration.

## Output

Add this section only when there is at least one meaningful item:

```md
## 기술 논문 / 연구 동향

최근 일주일(YYYY년 M월 D일~M월 D일)에 공개된 자료 중, 디스플레이 및 지속 추적 토픽에 해당하는 논문과 연구 자료를 정리했습니다.

- ...
  원문: https://...
  교차 확인: https://...
```

When an AI paper is selected, add the following separate block after the display research section:

```md
## AI 관련 논문

### 주간 AI Top 1

- 논문명 — 저널명 / DOI 또는 arXiv category와 ID, 최초 공개일
  Top 1 선정 이유: ...
  디스플레이 연결 관점: ...
  한계/주의점: ...
  원문: https://...
```

Use careful language. Do not imply near-term commercialization unless the public source supports it.
