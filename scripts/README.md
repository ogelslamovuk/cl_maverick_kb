# Scripts

This directory contains local processing scripts for CL Maverick KB.

## Inbox Processing v0.1

`process_inbox.py` reads local source files from `inbox/` and writes normalized markdown files to `Maverick_KB/raw_normalized/`.

Supported formats:

- `.txt`
- `.md`
- `.docx`
- `.pdf`

The processor does not delete source files from `inbox/` and does not create wiki pages.

## Add Source Files

Place source files in:

```powershell
inbox/
```

Files in `inbox/` are local-only, except `inbox/README.md`.

The tracked placeholder `inbox/README.md` is ignored by the processor.

## Install Dependencies

From the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r scripts\requirements.txt
```

## Run

From the project root:

```powershell
.\.venv\Scripts\python scripts\process_inbox.py
```

## Result

Open the local Obsidian vault at `Maverick_KB/`.

Normalized files are created in:

```powershell
Maverick_KB/raw_normalized/
```

Processing history is appended to:

```powershell
Maverick_KB/PROCESSING_LOG.md
```
