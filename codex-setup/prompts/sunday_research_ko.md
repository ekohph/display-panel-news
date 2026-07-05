# Sunday Research Coverage Prompt

Use this as an additional pass for Sunday briefings.

## Task

Search for meaningful display-related papers, preprints, university releases, research-lab releases, and public journal metadata from the previous Monday through Sunday.

## Required Inputs

- `config/research_rules.yml`
- `config/sources.yml`
- `reference/search_queries.md`
- `reference/source_urls.yml`

## Search Strategy

1. Search journal and metadata sources for display-specific terms.
2. Search arXiv and Crossref/OpenAlex/PubMed for newly published or newly indexed items.
3. Use publisher ASAP pages when accessible.
4. If publisher pages are blocked or not indexed, verify via DOI metadata or public abstract records.
5. Exclude weakly related papers.

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

Use careful language. Do not imply near-term commercialization unless the public source supports it.
