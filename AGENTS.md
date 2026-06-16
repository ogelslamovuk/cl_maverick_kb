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
