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

## Sunday Publisher and Metadata AI Discovery

Search publisher pages, Crossref and OpenAlex every Sunday, alongside arXiv. These are discovery routes, not just fallbacks. Use each combination as a separate query, adapting it to the week's trends:

```text
OLED "graph neural network"
"organic light-emitting diode" "deep learning" "device prediction"
OLED "machine learning" "device design"
OLED "Bayesian optimization"
"oxide TFT" "large language model"
"oxide semiconductor" "literature extraction" display
"thin-film transistor" "machine learning" backplane
"mobility stability" "AI" "thin-film transistor"
"display manufacturing" "process optimization" "machine learning"
microLED "machine learning" yield
"OLED materials" "machine learning" lifetime
```

Check relevant publisher results, including Wiley Advanced Intelligent Systems and Journal of SID, Springer Nature/Nano Convergence, ACS and IEEE. Use Crossref/OpenAlex bibliographic or title/abstract search; do not assume a search engine has indexed every metadata API record. Resolve candidate DOIs to publisher abstracts/full text before summarizing.

For new-paper coverage verify first online publication in the weekly window. For `이번 주 트렌드와 연결한 주요 논문 리뷰`, also search without a date restriction and compare against known papers. Select one or two papers with the strongest connection to an actual weekly trend; older and covered papers are eligible. Read `operations-local/known_papers.json` and `research_coverage.md` when present in the workflow root, and honor exclusions. Treat title-only matches as leads; display relevance can be established in the abstract/full text.

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

For display-backplane searches outside the recurring tracking topics, use co-occurrence style queries. Do not use standalone `IGZO`.

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

Outside the recurring tracking topics, exclude results that only mention:

```text
DRAM
3D NAND
embedded memory
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

## Recurring Tracking Topics

Run every group on each industrial-news pass, including touch separately. Use news/release variants daily and paper/DOI/abstract variants on Sunday/monthly research dates. Search Korean and English. Neuromorphic TFT and glass packaging do not require a display keyword. Sensor results require a demonstrated display application; NIR alone is insufficient.

### 1. Display sensors

```text
디스플레이 센서 패널 통합
under display sensor optical fingerprint
OLED integrated photodetector sensor
in-panel sensor ambient light proximity
near infrared sensor display integration
```

### Touch: separate sensor search

```text
디스플레이 터치 센서 인셀 온셀
in-cell on-cell touch display sensor
capacitive optical touch display sensor
OLED touch stylus pen input
large area automotive wearable touch display
```

### 2. Stretchable display

```text
스트레처블 디스플레이 신축성 소자 봉지 신뢰성
stretchable display OLED microLED TFT
stretchable display interconnect electrode encapsulation
stretchable display strain image compensation reliability
```

### 3. Neuromorphic TFT

```text
뉴로모픽 TFT 시냅스 트랜지스터
neuromorphic thin film transistor
synaptic transistor oxide organic TFT
optoelectronic synaptic transistor plasticity array
IGZO neuromorphic synaptic transistor
```

### 4. Glass packaging

```text
유리 패키징 유리기판 유리 인터포저 TGV
glass packaging glass core substrate
glass interposer through glass via TGV
panel level glass packaging redistribution layer
glass substrate packaging equipment reliability
```

Check every group before deciding that there are no candidates. Select by significance and public evidence; do not force an item per topic. State actual applications without assuming display use.
