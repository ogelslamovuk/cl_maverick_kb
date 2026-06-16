# Inbox

Place new source materials into:

```text
inbox/_new/
```

Run the processor from the project root:

```powershell
.\.venv\Scripts\python scripts\process_inbox.py
```

After processing:

- successful originals move to `inbox/_processed/`;
- failed or unsupported originals move to `inbox/_failed/`;
- normalized markdown files are written to `Maverick_KB/raw_normalized/`;
- processing history is appended to `Maverick_KB/PROCESSING_LOG.md`.

Only this placeholder README is intended to be committed. Files inside `_new`, `_processed`, and `_failed` are local-only and ignored by Git.
