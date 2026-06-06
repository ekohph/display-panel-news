# Display Panel News

디스플레이 패널 제조사, 패널 구매 기업, 플랫폼 생태계 기업, 주요 공급망, 그리고 디스플레이 관련 연구 동향을 정리하는 공개 뉴스 브리핑 저장소입니다.

브리핑은 공개 웹 자료를 기준으로 작성하며, 각 항목에는 원문 링크를 함께 남깁니다.

## 정리 범위

- 패널 제조사: LG Display, Samsung Display, BOE, TCL CSOT, Tianma, Everdisplay, Visionox 등
- 패널 구매 기업: Apple, Samsung Electronics, LG Electronics, Hyundai Motor Group / Kia, Meta, Valve 등
- 플랫폼 생태계: Intel, NVIDIA 등 디스플레이 사양이나 로드맵에 영향을 줄 수 있는 플랫폼 기업
- 공급망: DDI, Micro-OLED backplane, 소재, 장비, 규제, 관련 부품 및 업체
- 연구 동향: 논문, preprint, 대학 및 연구기관 발표 자료 중 디스플레이 응용이 명확한 자료

## 폴더 구조

- `summaries/<월>/`: 일간 뉴스 요약 파일
- `trends/weekly/`: 주간 경향 요약
- `trends/monthly/`: 월간 산업 및 연구 경향 요약

예시:

```text
summaries/5월/
summaries/6월/
trends/weekly/
trends/monthly/
```

## 작성 형식

일간 요약은 한국어 Markdown으로 작성하며, 일반적으로 다음 구조를 사용합니다.

1. `핵심 요약`
2. `패널 메이커 신규 기사`
3. `Panel buyers 동향`
4. `Platform ecosystem`
5. 공급망 또는 규제 관련 섹션
6. `기술 논문 / 연구 동향`

해당 날짜에 의미 있는 내용이 없는 섹션은 표시하지 않습니다. `기술 논문 / 연구 동향`은 매주 월요일 또는 월간/분기/반기/연간 경향 정리일에 필요한 경우에만 포함합니다.

기사 링크는 각 bullet 바로 아래에 둡니다.

```md
- Tianma는 Intel Client Ecosystem Symposium / Edge Solution Summit 2026 Shanghai에서 노트북용 IT display 2종을 공개했습니다. (TweakTown, 2026년 5월 23일)
  원문: https://...
  교차 확인: https://...
```

`교차 확인`은 유용한 2차 출처가 있을 때만 표시합니다.

## 운영 원칙

- 공개 웹 자료만 사용합니다.
- 중복 기사나 실질적으로 같은 내용은 반복해서 신규 항목으로 넣지 않습니다.
- 하루 이상 파일 생성이 누락된 경우, 다음 생성 파일에는 마지막 생성 기준 시각 이후부터 현재 기준 시각까지의 의미 있는 신규/비중복 항목을 포함할 수 있습니다.
- 누락된 날짜에 대해 빈 파일을 별도로 생성하지 않습니다.
- 회사별 섹션은 뉴스 가치가 있는 항목이 있을 때만 표시합니다.
- 연구 자료는 회사 뉴스와 구분해서 다루며, 디스플레이 응용이 명확한 경우에만 포함합니다.

## 참고

이 저장소의 내용은 공개 자료 기반의 개인 리서치 정리입니다. 특정 회사, 기관, 제품에 대한 투자 의견이나 공식 입장을 의미하지 않습니다.
