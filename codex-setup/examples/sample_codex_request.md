# Sample Codex Request

Use this text in a new Codex session.

```text
Read the public setup pack under codex-setup/.

Generate today's Korean display panel news briefing using only public sources.

Rules:
- Keep the output company-neutral.
- Do not imply my employer or affiliation.
- Do not use private data.
- Do not send email.
- Do not push until I approve.
- Use Google News RSS queries from codex-setup/reference/search_queries.md as a broad discovery layer, but cite original publisher URLs.
- Exclude wikileaks-kr.org unless I explicitly ask you to inspect it; treat it only as a weak lead requiring stronger corroboration.
- For research papers, follow codex-setup/config/research_rules.yml.
- Save the daily Markdown file under summaries/<month_ko>/YYYY-MM-DD.md.
```

For Sunday:

```text
Today is Sunday. After the daily industrial news pass, run the Sunday research pass using codex-setup/prompts/sunday_research_ko.md.
Only include research items with explicit display relevance.
```
