# AGENTS.md

## Project Rules

CL Maverick KB is a local Obsidian-compatible knowledge base and LLM Wiki scaffold for the Maverick ecosystem.

Do not build or scaffold Hermes, Telegram bot, web UI, PostgreSQL, Qdrant, or any LLM API integration unless the user explicitly asks for that work.

Do not change the project structure without an explicit user command.

## Knowledge Base Scope

`Maverick_KB/` is a local Obsidian vault. It must not be committed to GitHub at this stage.

`Maverick_KB/raw_normalized/` is generated locally from inbox materials and must not be committed to GitHub.

GitHub currently stores only the project scaffold, scripts placeholders, documentation, and repository rules:

- `README.md`
- `AGENTS.md`
- `docs/`
- `scripts/`
- `inbox/README.md`
- `exports/README.md`
- `.gitignore`

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

- `docs/WIKI_DIGESTION_RULES.md`
- `docs/MAVERICK_KB_PROJECT_BRIEF.md`
- `docs/MAVERICK_KB_TZ.md`
- `docs/MAVERICK_KB_PROCESS.md`
- `docs/MAVERICK_KB_AGENT_PROMPT.md`
- `docs/MAVERICK_KB_CHECKLIST.md`

## Autonomous processing prompt

For autonomous one-message starts, use:

```text
docs/MAVERICK_KB_INITIAL_MESSAGE.md
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
