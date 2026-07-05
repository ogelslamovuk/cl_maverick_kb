# CL Maverick KB

CL Maverick KB is a local Obsidian-compatible knowledge base and future LLM Wiki for the Maverick ecosystem.

The project is intended for onboarding a new client, training cinema staff, documenting Maverick operational processes, and later generating FAQ entries, instructions, training scenarios, and assistant answers.

## Start here for AI agents

Use these documents to give another AI agent the full context for creating Maverick KB instructions:

1. `docs/MAVERICK_KB_INITIAL_MESSAGE.md` — ready initial message for autonomous processing; replace only the source folder path.
2. `docs/MAVERICK_KB_PROJECT_BRIEF.md` — project description, folders, repositories, existing skills.
3. `docs/MAVERICK_KB_TZ.md` — technical assignment for creating instructions from source materials.
4. `docs/MAVERICK_KB_PROCESS.md` — end-to-end procedure: source analysis, transcription, wiki update, Pages publish, verification.
5. `docs/MAVERICK_KB_AGENT_PROMPT.md` — full reusable prompt for another AI agent.
6. `docs/MAVERICK_KB_CHECKLIST.md` — acceptance checklist before saying the task is done.
7. `docs/WIKI_DIGESTION_RULES.md` — rules for converting raw material into clean wiki pages.

Reusable local skill-pack:

```text
D:\JetBrains\ai-skills\skills\maverick-kb-content-pipeline
```

Public MkDocs/GitHub Pages copy:

```text
D:\JetBrains\cl_maverick_kb_pages
```

## Local Vault

`Maverick_KB/` is the local Obsidian vault. It contains working knowledge pages, taxonomy, templates, media notes, gaps, and normalized raw materials.

At this stage, `Maverick_KB/` is not synchronized with GitHub and must remain local.

## GitHub Scope

GitHub currently stores only the project scaffold:

- repository documentation
- agent/project rules
- script placeholders
- inbox/export placeholders
- ignore rules

No raw source files, vault contents, PDFs, DOCX files, videos, archives, or local environment files should be committed.
