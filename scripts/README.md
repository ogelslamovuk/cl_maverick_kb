# Scripts

This directory contains local processing scripts for CL Maverick KB.

## Inbox Processing

`process_inbox.py` reads local source files from `inbox/_new/` and writes normalized markdown files to `Maverick_KB/raw_normalized/`.

Supported formats:

- `.txt`
- `.md`
- `.docx`
- `.pdf`

The processor does not create wiki pages.

After processing, original files are moved:

- success: `inbox/_processed/`
- error or unsupported format: `inbox/_failed/`

If a target folder already contains a file with the same name, the processor appends a timestamp to avoid overwriting it.

## Add Source Files

Place source files in:

```powershell
inbox\_new\
```

Files in `inbox/_new/`, `inbox/_processed/`, and `inbox/_failed/` are local-only.

The processor no longer reads files directly from `inbox/`.

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

The log records the original path, raw normalized path, moved original path, status, and error text when applicable.
