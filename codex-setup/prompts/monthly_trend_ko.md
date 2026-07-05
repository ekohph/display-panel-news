# Monthly Trend Prompt

Use this prompt for monthly display-panel trend synthesis.

## Task

Create or update `trends/monthly/YYYY-MM.md` using public daily summaries, source articles, market data, and research metadata.

## Process

1. Read all daily summaries for the target month.
2. Identify repeated themes, turning points, and meaningful changes.
3. Separate industrial trends from research and technology trends.
4. Avoid repeating every daily item; synthesize instead.
5. Cite the most representative public sources.

## Recommended Structure

```md
# Display Panel Monthly Trends - YYYY-MM

## 핵심 요약

- ...

## 산업 동향

### Panel makers and manufacturing

- ...

### Buyers and product strategy

- ...

### Supply chain, equipment, and regulation

- ...

## 기술 논문 / 연구 동향

- ...

## 다음 달 관찰 포인트

- ...
```

## Research Rules

Apply `config/research_rules.yml`. Do not include semiconductor, memory, sensor, or general materials papers unless the public source explicitly connects the item to display devices, display backplanes, panel architecture, display manufacturing, or display materials.

## Neutrality Rules

Keep the tone balanced. Do not write from the perspective of any one company, and do not single out a company as the default reference point.
