# Architecture

CL Maverick KB is organized as a local-first documentation project.

## Local Project

The repository root contains the public scaffold: documentation, scripts, inbox/export placeholders, ignore rules, and agent instructions.

GitHub currently stores only this scaffold. The working knowledge base remains local.

## Obsidian Vault

`Maverick_KB/` is the local Obsidian-compatible vault. It is used for manual knowledge editing, internal navigation, taxonomy maintenance, templates, gaps, and future generated wiki pages.

The vault is ignored by Git at this stage.

## Inbox

`inbox/` is reserved for incoming raw materials. Files placed there are local-only and ignored by Git, except `inbox/README.md`.

## Future Raw Processor

A future local processor may normalize raw inputs into structured intermediate materials. Planned sources include PDF, DOCX, video transcripts, keyframes, OCR text, and manually supplied notes.

## Future Wiki Generation

Generated wiki pages should follow the vault schema, use task/process navigation, preserve source references where available, and create gaps instead of inventing missing facts.

High-risk topics require explicit user confirmation before they can be marked as verified.
