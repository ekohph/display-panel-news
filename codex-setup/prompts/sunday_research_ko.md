# Sunday Research Coverage Prompt

Use this as an additional pass for Sunday briefings.

## Task

Search for meaningful display-related papers, preprints, university releases, research-lab releases, and public journal metadata from the previous Monday through Sunday. Also review arXiv computer-science categories `cs.AI`, `cs.CV`, `cs.LG`, `cs.CL`, and `cs.RO` for AI papers relevant to display devices, display manufacturing/inspection, or display materials.

## Required Inputs

- `config/research_rules.yml`
- `config/sources.yml`
- `reference/search_queries.md`
- `reference/source_urls.yml`

## Search Strategy

1. Search journal and metadata sources for display-specific terms.
2. Search arXiv and Crossref/OpenAlex/PubMed for newly published or newly indexed items. The arXiv CS category pass is required on Sundays, not optional.
3. Use publisher ASAP pages when accessible.
4. If publisher pages are blocked or not indexed, verify via DOI metadata or public abstract records.
5. Exclude weakly related papers.

## Weekly AI Top 1

From the prior week's AI papers, select exactly one Top 1 item across these three buckets:

1. AI directly applied to displays or display quality;
2. AI for manufacturing, process control, yield, defect detection, or inspection;
3. AI for materials discovery, formulation, or reliability relevant to display materials.

Rank first by direct display or panel-production relevance, then by technical significance and evidence quality. Explain the selection, the display connection, and the main limitation. If the best AI paper is only weakly connected to displays, keep it in a separate `## AI 관련 논문` section rather than presenting it as a display paper.

## Include Only When

The public record explicitly connects the work to at least one of:

- display devices;
- panel architecture;
- display backplanes;
- OLED, LCD, AMOLED, QD, microLED, Micro-OLED, or microdisplay;
- display manufacturing;
- active matrix or pixel circuits;
- display materials with clear device relevance.

## Oxide TFT and IGZO Rule

Do not include standalone IGZO results.

For IGZO or oxide-semiconductor papers, require both:

1. a device term, such as `IGZO TFT`, `a-IGZO TFT`, `In-Ga-O TFT`, `IGO TFT`, `polycrystalline oxide TFT`, `oxide semiconductor TFT`, `thin-film transistor`, `oxygen diffusion`, `metal capping`, or `gate dielectric`; and
2. a display anchor, such as `display`, `panel`, `backplane`, `pixel`, `OLED`, `LCD`, `AMOLED`, `microdisplay`, or `active matrix`.

Exclude items whose only application is memory, BEOL logic, sensors, power electronics, or general semiconductor integration.

## Output

Add this section only when there is at least one meaningful item:

```md
## 기술 논문 / 연구 동향

최근 일주일(YYYY년 M월 D일~M월 D일)에 공개된 자료 중, 디스플레이 응용이 명확한 논문과 연구 자료만 포함했습니다.

- ...
  원문: https://...
  교차 확인: https://...
```

When an AI paper is selected, add the following separate block after the display research section:

```md
## AI 관련 논문

### 주간 AI Top 1

- 논문명 — arXiv category: `cs.AI` / `cs.CV` / `cs.LG` / `cs.CL` / `cs.RO`
  Top 1 선정 이유: ...
  디스플레이 연결 관점: ...
  한계/주의점: ...
  원문: https://...
```

Use careful language. Do not imply near-term commercialization unless the public source supports it.
