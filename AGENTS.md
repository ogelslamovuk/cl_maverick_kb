# AGENTS.md

## Project Rules

CL Maverick KB is a local Obsidian-compatible knowledge base and LLM Wiki scaffold for the Maverick ecosystem.

Do not build or scaffold Hermes, Telegram bot, web UI, PostgreSQL, Qdrant, or any LLM API integration unless the user explicitly asks for that work.

Do not change the project structure without an explicit user command.

## Knowledge Base Scope

`Maverick_KB/` is a local Obsidian vault. It must not be committed to GitHub at this stage.

`Maverick_KB/raw_normalized/` is generated locally from inbox materials and must not be committed to GitHub.

GitHub currently stores only the project scaffold, scripts placeholders, public documentation, and repository rules:

- `README.md`
- `AGENTS.md`
- `docs/`
- `scripts/`
- `inbox/README.md`
- `exports/README.md`
- `.gitignore`

## Publication Boundary

Internal KB process materials may exist locally in Obsidian, but must never be committed to GitHub or published to the user-facing GitHub Pages site, frontend navigation, direct public URLs, or search index.

Internal materials include agent prompts, initial messages, digestion rules, project briefs, technical assignments, processing procedures, readiness checklists, gaps/open questions, raw transcripts, source-processing notes, and any file whose purpose is to instruct Codex/LLM/agents rather than Maverick end users.

Store internal process documents under local-only Obsidian paths such as `Maverick_KB/internal/`. When updating Pages, explicitly exclude internal materials from MkDocs with `exclude_docs`, keep them out of `nav`, and verify the built `site/` and `site/search/search_index.json` do not contain them.

## Navigation Model

The main knowledge base navigation is organized by user tasks and operational processes, not by applications.

Products are used as metadata tags:

- Manager/Portal
- Seller
- Kiosk
- Site
- Widget
- Waiter
- Media Maker

Channels:

- `mooon.by` = site
- `go2.by` = widget

## Roles

- cashier
- cash zone administrator
- cinema hall administrator
- accountant
- tax specialist
- technical specialist
- system administrator
- ticket controller

Russian display names:

- кассир
- администратор кассовой зоны
- администратор кинозала
- бухгалтер
- налоговик
- технический специалист
- системный администратор
- контролёр

## Statuses

- `draft`
- `needs_review`
- `verified`
- `outdated`
- `conflict`
- `gap`
- `high_risk`

High-risk knowledge includes money, VAT, payments, refunds, certificates, accounting, and technical setup.

High-risk materials must not be marked `verified` without explicit user confirmation.

## Knowledge Integrity

Do not invent facts. If source data is missing or unclear, create a gap instead.

Use gaps to record missing facts, conflicts, questions, or places where user confirmation is required.

Before any LLM-digestion or wiki-digestion work, Codex must read and follow:

- `Maverick_KB/internal/WIKI_DIGESTION_RULES.md`
- `Maverick_KB/internal/MAVERICK_KB_PROJECT_BRIEF.md`
- `Maverick_KB/internal/MAVERICK_KB_TZ.md`
- `Maverick_KB/internal/MAVERICK_KB_PROCESS.md`
- `Maverick_KB/internal/MAVERICK_KB_AGENT_PROMPT.md`
- `Maverick_KB/internal/MAVERICK_KB_CHECKLIST.md`

## Autonomous processing prompt

For autonomous one-message starts, use:

```text
Maverick_KB/internal/MAVERICK_KB_INITIAL_MESSAGE.md
```

If the user starts with that message, it already counts as approval for the full processing cycle. Do not stop after a plan waiting for another `approve`.

## Transcription on this Windows machine

Do not stop just because `whisper` is not in PATH, PowerShell cannot run `whisper`, `OPENAI_API_KEY` is not set, or Python `openai` / `whisper` packages are missing.

Use the local executable directly:

```text
D:\soft\Whisper\whisper-cli.exe
```

From Git Bash/MSYS:

```bash
/d/soft/Whisper/whisper-cli.exe
```

Models live in:

```text
D:\soft\Whisper\models\
```

If full transcription fails, continue with segmented audio, contact sheets, screenshots, partial transcript, and `Maverick_KB/QUESTIONS.md` instead of stopping the entire KB task.
