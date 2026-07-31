# 디스플레이 패널 뉴스 브리핑용 Codex 설정 팩

이 디렉토리는 Codex로 공개 디스플레이 패널 뉴스 브리핑을 만들고, 필요하면 반복 자동화까지 설정할 수 있도록 준비한 공개 설정 팩입니다.

이 설정 팩은 회사 중립적으로 작성되어 있습니다. 사용자가 특정 회사에 소속되어 있다고 추정하거나 암시하지 않으며, 특정 패널 업체를 별도로 우대하지 않습니다. 회사별 공식 뉴스룸 URL이나 민감한 추적 우선순위가 필요하다면 공개 저장소가 아니라 로컬 비공개 파일에 따로 보관하세요.

## 이 설정 팩으로 할 수 있는 일

이 파일들을 다른 Codex 세션에 읽히면 다음 작업을 맡길 수 있습니다.

- 공개 디스플레이 패널, 공급망, 구매 기업, 플랫폼 생태계, 시장조사, 연구 자료 검색
- 한국어 Markdown 브리핑 작성
- 산업 뉴스와 논문/연구 동향 분리
- DOI, URL, 정규화된 제목 기준 중복 회피
- 디스플레이 연관성이 명확한 연구 자료만 보수적으로 포함
- 공개 저장소에 커밋 가능한 형태의 결과 파일 생성
- 사용자가 원하면 반복 자동화 루틴 설정 안내

## 토큰 사용량 추정

이 워크플로는 소스 검색량이 많은 편입니다. 한 번의 브리핑에서도 공개 웹페이지 검색, 로컬 설정 파일 읽기, 이전 요약 확인, 중복 검토, Markdown 작성이 함께 일어납니다.

로컬 실행 이력 중 실제 public summary 생성 또는 업데이트가 있었던 실행을 기준으로 보면, 일반적인 성공 브리핑 실행은 대략 다음 정도였습니다.

- reported total tokens: 회당 약 `1.8M~4.1M`, 평균 약 `2.9M`
- cached input을 제외한 근사 토큰량: 회당 약 `250k~670k`, 평균 약 `430k`

전체 감지 실행 7건을 모두 포함하면 reported total tokens 기준 평균 약 `3.5M`, 최소 `63k`, 최대 `10.3M`이었습니다. 다만 이 범위에는 짧은 이어쓰기 실행과 수동 조사/규칙 수정이 섞인 큰 실행이 포함되어 있어, 일반적인 자동 브리핑 1회 비용을 대표한다고 보기는 어렵습니다.

이 숫자는 요금 또는 크레딧 사용량을 정확히 예측하는 값이 아니라, Codex 세션 로그에 기록된 token usage 기반의 대략적인 규모 추정입니다. 실제 사용량은 검색한 소스 수, 건너뛴 날짜 수, 일요일 연구 조사 여부, 페이지 길이, 캐시 재사용 여부, 자동 커밋/푸시 여부에 따라 크게 달라질 수 있습니다.

## 빠른 시작

1. 이 저장소를 다운로드하거나 `codex-setup/` 디렉토리를 공개 디스플레이 뉴스 저장소에 복사합니다.
2. 해당 저장소에서 Codex 세션을 엽니다.
3. 아래 자동화 설정 프롬프트를 Codex에 붙여 넣습니다.

### 붙여 넣기용 프롬프트: 반복 자동화 설정

Codex 자동화에 익숙하지 않은 사용자가 자동화 설정을 안내받고 싶을 때 사용하세요.

```text
Read codex-setup/README.md and all files under codex-setup/config, codex-setup/prompts, codex-setup/templates, and codex-setup/reference.

Help me set up a recurring Codex automation for public display-panel news briefings.

Important rules:
- Use only public sources and the neutral rules in codex-setup/.
- Use Google News RSS from `reference/search_queries.md` as a broad discovery layer, then follow and cite original publisher URLs.
- Exclude `wikileaks-kr.org` unless the user explicitly asks to inspect it. Treat it only as a weak lead and require stronger corroboration before inclusion.
- Do not infer or mention my employer or affiliation.
- Do not give special treatment to any one panel maker.
- Do not send email unless I explicitly ask for it.
- Do not commit or push unless I explicitly ask for it.
- Do not write raw automation configuration by hand if Codex provides an automation tool. Use the Codex automation capability and show me a reviewable proposal or ask for confirmation before creating the automation.
- If this Codex surface cannot create automations, explain that limitation and give me a manual run prompt instead.

Before creating the automation, ask me only for missing choices:
1. Schedule and timezone, such as every weekday at 07:30 local time, every day, or every Sunday.
2. Execution environment, if Codex asks for one. Prefer local for a repository on my computer unless I choose otherwise.
3. Output format. Default is Markdown only. If I ask for HTML or another format, add a small converter script or instructions in this repository.
4. Whether the automation should only create files, or also commit and push after successful generation.
5. Whether Sunday research coverage should be enabled. Default is yes for Sunday runs.

Use this task prompt for the recurring automation:

Read codex-setup/README.md and the files under codex-setup/config, codex-setup/prompts, codex-setup/templates, and codex-setup/reference. Generate the public Korean display-panel news briefing for the current local date using only public sources. Use Google News RSS as a broad discovery layer but cite original publisher URLs. Exclude wikileaks-kr.org unless explicitly requested and strongly corroborated. Save the Markdown file under the configured summaries path. Keep the writing company-neutral and do not imply the user's affiliation. On Sundays, run the Sunday research pass and include 기술 논문 / 연구 동향 only when public sources show explicit display relevance. Do not send email. Commit and push only if the automation was explicitly configured to do so.
```

사용자 참고 사항:

- 컴퓨터가 꺼져 있거나 Codex 앱, 권한, 네트워크 상태가 준비되어 있지 않으면 자동 실행이 수행되지 않을 수 있습니다.
- 사용자는 일정을 자연어로 설명하면 됩니다. raw automation 파일을 직접 작성하지 않는 쪽이 관리에 유리합니다.
- 기본 출력은 Markdown, 즉 formatted text 파일입니다. HTML, PDF 등 다른 형식이 필요한 경우 Codex에게 자연어로 설명해 주세요.

### 1회성 일일 브리핑

자동화 없이 하루 브리핑만 만들고 싶다면 아래처럼 요청합니다.

```text
Follow codex-setup/prompts/daily_briefing_ko.md.
Use codex-setup/config/*.yml and codex-setup/reference/source_urls.yml.
Use codex-setup/reference/search_queries.md for Google News RSS discovery queries.
Create the output Markdown under summaries/<month_ko>/YYYY-MM-DD.md.
Do not send email. Do not push until I approve.
```

### 일요일 연구 동향 포함

일요일에 논문/연구 동향까지 확인하고 싶다면 아래처럼 추가 요청합니다.

```text
Today is Sunday. Follow codex-setup/prompts/sunday_research_ko.md as an additional pass.
Include a 기술 논문 / 연구 동향 section only when the paper has explicit display relevance.
```

### 월간 트렌드

월간 트렌드 정리를 만들고 싶다면 아래처럼 요청합니다.

```text
Follow codex-setup/prompts/monthly_trend_ko.md.
Create or update trends/monthly/YYYY-MM.md.
Separate industrial trends from research and technology trends.
```

## 디렉토리 구조

```text
codex-setup/
  README.md
  README.en.md
  config/
    automation_defaults.yml
    cadence.yml
    categories.yml
    companies.yml
    output_paths.yml
    research_rules.yml
    sources.yml
  prompts/
    daily_briefing_ko.md
    monthly_trend_ko.md
    setup_automation_ko.md
    sunday_research_ko.md
  reference/
    search_queries.md
    source_urls.md
    source_urls.yml
  templates/
    daily_summary.md
    monthly_trend.md
    seen_articles.example.json
    weekly_trend.md
  examples/
    sample_automation_setup_request.md
    sample_codex_request.md
    sample_daily_output.md
```

## 개인정보 및 소속 노출 방지 규칙

- 개인 이메일 주소, 토큰, API key, 로컬 경로, 브라우저 프로필, 쿠키, 내부 문서를 포함하지 마세요.
- 사용자의 소속 회사나 고용 관계를 언급하거나 암시하지 마세요.
- 특정 패널 업체를 위한 별도 고정 섹션을 만들지 마세요. 어떤 회사든 그날의 공개 자료 가치가 충분할 때만 같은 기준으로 다룹니다.
- 특정 회사의 공식 URL 목록이 공개되면 추적 우선순위나 관심사가 드러날 수 있습니다. 민감할 수 있는 회사별 URL은 공개 파일이 아니라 로컬 비공개 확장 파일에 보관하세요.

권장 비공개 확장 파일 경로:

```text
codex-local/private_sources.yml
```

`codex-local/`은 커밋하지 마세요.

## 공개 소스 사용 원칙

공개 웹 자료, 공식 공개 발표, 공개 논문 메타데이터, 공개 초록, 신뢰할 수 있는 산업 매체만 사용합니다. 유료 기사나 접근 제한이 있는 논문은 공개 snippet, 공개 초록, 공개 메타데이터, 신뢰할 수 있는 2차 보도에서 확인되는 내용만 요약합니다.

## 출력 형식 규칙

일일 요약 파일은 한국어 Markdown으로 작성하며, 일반적으로 다음 구조를 사용합니다.

1. `핵심 요약`
2. `패널 메이커 및 공급망 동향`
3. `Panel buyers 동향`
4. `Platform ecosystem`
5. 필요할 경우 규제, 시장, 장비 관련 섹션
6. `기술 논문 / 연구 동향`: 일요일 또는 장기 트렌드 정리일에 의미 있는 연구 자료가 있을 때만 포함

내용이 없는 섹션은 생략합니다. 출처 링크는 각 bullet 바로 아래에 둡니다.

```md
- 요약 문장.
  원문: https://...
  교차 확인: https://...
```

`교차 확인`은 실제로 유용한 2차 출처가 있을 때만 표시합니다.

## Git 작업 흐름

파일을 생성한 뒤에는 다음 순서로 진행합니다.

1. `git status --short`로 변경 파일을 확인합니다.
2. 공개해도 되는 의도한 파일만 stage합니다.
3. 명확한 메시지로 commit합니다.
4. 사용자가 명시적으로 승인한 뒤에만 push합니다.

비공개 설정 파일, 개인 로그, 로컬 캐시, 인증 정보는 공개 커밋에 포함하지 마세요.
