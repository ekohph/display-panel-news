# Codex Setup Pack for Display Panel News Briefings

This directory is a public setup pack for creating public display-panel news briefings with Codex, and for configuring recurring automation when needed.

This setup pack is written to be company-neutral. It does not infer or imply that the user belongs to any specific company, and it does not give special treatment to any one panel maker. If you need company-specific official newsroom URLs or sensitive tracking priorities, keep them in a local private file rather than in the public repository.

## What This Pack Does

When these files are given to another Codex session, Codex can handle the following tasks.

- Search public display panel, supply chain, buyer, platform ecosystem, market research, and research sources
- Write Korean Markdown briefings
- Separate industry news from paper and research trends
- Avoid duplicates by DOI, URL, and normalized title
- Conservatively include only research sources with clear display relevance
- Generate output files in a form suitable for public repository commits
- Guide recurring automation setup if the user wants it

## Token Usage Estimate

This workflow tends to use a large amount of source-search context. A single briefing may involve public web searches, local configuration reads, previous-summary checks, duplicate review, and Markdown writing.

Based on local run history where a public summary was actually generated or updated, a typical successful briefing run was roughly in this range.

- Reported total tokens: about `1.8M~4.1M` per run, with an average of about `2.9M`
- Approximate token count excluding cached input: about `250k~670k` per run, with an average of about `430k`

Across all 7 detected runs, the reported total token count averaged about `3.5M`, with a minimum of `63k` and a maximum of `10.3M`. However, that full range includes short continuation runs and larger manual investigation/rule-editing runs, so it should not be treated as representative of the cost of one normal automated briefing.

These numbers are not an exact prediction of billing or credit usage. They are a rough scale estimate based on token usage recorded in Codex session logs. Actual usage can vary significantly depending on the number of searched sources, skipped dates, whether Sunday research coverage is enabled, page length, cache reuse, and whether automated commit/push is enabled.

## Quick Start

1. Download this repository, or copy the `codex-setup/` directory into a public display-news repository.
2. Open a Codex session in that repository.
3. Paste the automation setup prompt below into Codex.

### Copy-Paste Prompt: Recurring Automation Setup

Use this when a user who is not familiar with Codex automation wants guided setup.

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

User notes:

- If the computer is turned off, or if the Codex app, permissions, or network are not ready, automatic execution may not run.
- Users can describe the schedule in natural language. It is usually easier to manage the automation if users do not write raw automation files directly.
- The default output is Markdown, meaning a formatted text file. If you need another format such as HTML or PDF, describe that to Codex in natural language.

### One-Time Daily Briefing

If you want to create only one daily briefing without automation, ask Codex like this.

```text
Follow codex-setup/prompts/daily_briefing_ko.md.
Use codex-setup/config/*.yml and codex-setup/reference/source_urls.yml.
Use codex-setup/reference/search_queries.md for Google News RSS discovery queries.
Create the output Markdown under summaries/<month_ko>/YYYY-MM-DD.md.
Do not send email. Do not push until I approve.
```

### Include Sunday Research Trends

If you want to include papers and research trends on Sunday, add this request.

```text
Today is Sunday. Follow codex-setup/prompts/sunday_research_ko.md as an additional pass.
Include a 기술 논문 / 연구 동향 section only when the paper has explicit display relevance.
```

### Monthly Trends

If you want to create a monthly trend summary, ask Codex like this.

```text
Follow codex-setup/prompts/monthly_trend_ko.md.
Create or update trends/monthly/YYYY-MM.md.
Separate industrial trends from research and technology trends.
```

## Directory Structure

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

## Privacy and Affiliation Protection Rules

- Do not include personal email addresses, tokens, API keys, local paths, browser profiles, cookies, or internal documents.
- Do not mention or imply the user's employer, affiliation, or employment relationship.
- Do not create a fixed section for any specific panel maker. Treat every company by the same standard, and cover it only when that day's public sources are sufficiently meaningful.
- If a list of official URLs for specific companies is made public, it may reveal tracking priorities or interests. Keep company-specific URLs that may be sensitive in a local private extension file rather than in public files.

Recommended private extension path:

```text
codex-local/private_sources.yml
```

Do not commit `codex-local/`.

## Public Source Principles

Use only public web sources, official public announcements, public paper metadata, public abstracts, and reliable industry media. For paid articles or access-restricted papers, summarize only information confirmed through public snippets, public abstracts, public metadata, or reliable secondary reporting.

## Output Format Rules

Daily summary files should be written in Korean Markdown and generally use the following structure.

1. `핵심 요약`
2. `패널 메이커 및 공급망 동향`
3. `Panel buyers 동향`
4. `Platform ecosystem`
5. Regulatory, market, or equipment-related sections when needed
6. `기술 논문 / 연구 동향`: include only on Sundays or long-term trend-summary days when meaningful research sources are available

Omit sections with no content. Put source links directly below each bullet.

```md
- 요약 문장.
  원문: https://...
  교차 확인: https://...
```

Show `교차 확인` only when there is a genuinely useful secondary source.

## Git Workflow

After generating files, proceed in this order.

1. Check changed files with `git status --short`.
2. Stage only the intended files that are safe to publish.
3. Commit with a clear message.
4. Push only after the user explicitly approves it.

Do not include private configuration files, personal logs, local caches, or credentials in public commits.
