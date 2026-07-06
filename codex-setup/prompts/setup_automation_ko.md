# Automation Setup Prompt

Copy this into a new Codex session when you want Codex to set up a recurring briefing automation.

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

## Notes

- Local automations depend on the user's Codex app, computer, permissions, and network being available.
- Do not promise catch-up behavior for missed local runs unless the active Codex surface explicitly states that behavior.
- Keep schedules in plain language for users; Codex should translate them through its automation capability.
- Markdown is the safest default output for Git. Treat HTML, PDF, and other formats as optional add-ons.
