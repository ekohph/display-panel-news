# Search Query Guide

Use these query patterns as starting points. Adjust date filters and source domains for the current briefing window.

## Google News RSS Daily Discovery

Use Google News RSS for broad Korean/English discovery:

```text
https://news.google.com/rss/search?q=<URL-encoded query>&hl=ko&gl=KR&ceid=KR:ko
```

Follow and cite the original publisher URL rather than the Google News wrapper. Deduplicate every candidate against recent summaries and `seen_articles.json`.

Run at least these ordinary daily queries:

```text
삼성디스플레이 OLED
LG디스플레이 OLED
BOE OLED
CSOT OLED
디스플레이 장비 공급계약
OLED 패널 공급
폴더블 디스플레이 패널
마이크로디스플레이 스마트글라스
microdisplay smart glasses
foldable display panel
OLED equipment supply
microLED display
```

## Industrial News

```text
display panel OLED LCD panel maker news
OLED panel supply chain equipment materials latest
display panel utilization yield capacity OLED LCD
automotive display OLED panel supplier
notebook OLED panel roadmap
OLED monitor panel supply
XR microdisplay OLED panel supply
display driver IC OLED panel supply chain
```

## Buyer and Product Signals

```text
OLED TV review panel technology brightness refresh rate
OLED monitor new model panel technology
foldable phone OLED panel supply
notebook OLED display roadmap
automotive cockpit display OLED
XR headset microdisplay OLED
```

## Market and Analyst Signals

```text
OLED display demand forecast
display panel shipment forecast
OLED monitor shipment forecast
notebook OLED demand forecast
TV panel market share OLED LCD
display supply demand equipment intelligence
```

## Research and Journal Search

```text
OLED display research publication
QD-OLED quantum dot display paper
microLED display research
Micro-OLED microdisplay paper
perovskite LED display paper
tandem OLED lifetime efficiency display
oxide TFT display backplane paper
LTPO display backplane research
active matrix display TFT research
display encapsulation OLED paper
color conversion display quantum dot paper
stretchable display research
```

## Sunday arXiv CS AI Search

Sunday research coverage must include the following arXiv computer-science categories:

```text
site:arxiv.org/list/cs.AI new AI display manufacturing inspection materials
site:arxiv.org/list/cs.CV display inspection defect detection manufacturing
site:arxiv.org/list/cs.LG display materials discovery process control
site:arxiv.org/list/cs.CL multimodal display manufacturing inspection
site:arxiv.org/list/cs.RO robot display manufacturing inspection
```

Use the category pages or arXiv search filters for the prior Monday-Sunday window. Search terms should cover `display`, `panel`, `OLED`, `microLED`, `microdisplay`, `manufacturing`, `inspection`, `defect detection`, `yield`, `process control`, `materials`, `organic semiconductor`, `perovskite`, and `thin-film`.

## Oxide TFT and IGZO Search

Use co-occurrence style queries. Do not use standalone `IGZO`.

```text
"IGZO TFT" display backplane
"a-IGZO TFT" display backplane
"oxide semiconductor TFT" display backplane
"amorphous indium gallium zinc oxide" "thin-film transistor" display
"In-Ga-O TFT" display backplane
"IGO TFT" display backplane
"polycrystalline oxide TFT" display backplane
"polycrystalline In-Ga-O" "thin-film transistor" display
"Journal of SID" "TFT" display
site:sid.onlinelibrary.wiley.com/doi TFT display
"oxygen diffusion" "IGZO TFT" display
"metal capping" "IGZO TFT" backplane
"gate dielectric" "oxide TFT" display
"active matrix" "oxide semiconductor TFT"
```

Exclude results that only mention:

```text
DRAM
3D NAND
embedded memory
neuromorphic memory
BEOL logic
power electronics
sensor
```

## Metadata Fallback Queries

```text
site:api.crossref.org DOI title
site:pubmed.ncbi.nlm.nih.gov exact paper title
site:openalex.org exact paper title
"exact paper title" DOI
"exact paper title" abstract
```
