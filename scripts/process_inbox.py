"""Normalize local inbox materials into Obsidian-friendly markdown files.

Supported input formats: TXT, MD, DOCX, PDF.
Source files are moved from inbox/_new to inbox/_processed or inbox/_failed.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET


SUPPORTED_EXTENSIONS = {".txt", ".md", ".docx", ".pdf"}
TEXT_EXTENSIONS = {".txt", ".md"}
ENCODINGS = ("utf-8-sig", "utf-8", "cp1251")
WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def normalize_whitespace(value: str) -> str:
    value = value.replace("\xa0", " ")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def read_text_file(path: Path) -> str:
    last_error: Exception | None = None
    for encoding in ENCODINGS:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    raise ValueError(f"could not decode text file: {last_error}")


def extract_word_text(element: ET.Element) -> str:
    parts: list[str] = []

    for node in element.iter():
        tag = node.tag
        if tag.endswith("}t") and node.text:
            parts.append(node.text)
        elif tag.endswith("}tab"):
            parts.append("\t")
        elif tag.endswith("}br") or tag.endswith("}cr"):
            parts.append("\n")

    return normalize_whitespace("".join(parts))


def extract_docx_paragraph(paragraph: ET.Element) -> str:
    return extract_word_text(paragraph)


def extract_docx_table(table: ET.Element) -> str:
    rows: list[str] = []

    for row in table.findall(".//w:tr", WORD_NS):
        cells: list[str] = []
        for cell in row.findall("./w:tc", WORD_NS):
            cell_text = extract_word_text(cell)
            if cell_text:
                cells.append(cell_text)
        if cells:
            rows.append(" | ".join(cells))

    return "\n".join(rows)


def extract_docx_text(path: Path) -> str:
    """Extract DOCX text directly from word/document.xml."""
    try:
        with zipfile.ZipFile(path) as archive:
            document_xml = archive.read("word/document.xml")
    except KeyError as exc:
        raise ValueError("DOCX has no word/document.xml") from exc
    except zipfile.BadZipFile as exc:
        raise ValueError("invalid DOCX file") from exc

    root = ET.fromstring(document_xml)
    body = root.find("w:body", WORD_NS)
    if body is None:
        raise ValueError("DOCX has no document body")

    parts: list[str] = []

    for child in list(body):
        if child.tag.endswith("}p"):
            text = extract_docx_paragraph(child)
            if text:
                parts.append(text)
        elif child.tag.endswith("}tbl"):
            text = extract_docx_table(child)
            if text:
                parts.append(text)

    return "\n\n".join(parts)


def extract_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("missing dependency: pypdf") from exc

    reader = PdfReader(str(path))
    pages: list[str] = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"<!-- page: {index} -->\n{text.strip()}")

    return "\n\n".join(pages)


def extract_text(path: Path) -> str:
    extension = path.suffix.lower()
    if extension in TEXT_EXTENSIONS:
        return read_text_file(path)
    if extension == ".docx":
        return extract_docx_text(path)
    if extension == ".pdf":
        return extract_pdf_text(path)
    raise ValueError(f"unsupported file type: {extension or '<none>'}")


def build_output_markdown(
    source_path: Path,
    source_type: str,
    processed_at: str,
    extracted_text: str,
) -> str:
    return "\n".join(
        [
            "---",
            f"source_file: {yaml_quote(source_path.name)}",
            f"source_type: {yaml_quote(source_type)}",
            f"processed_at: {yaml_quote(processed_at)}",
            "status: raw_normalized",
            "---",
            "",
            f"# Raw normalized: {source_path.name}",
            "",
            "## Extracted text",
            "",
            extracted_text.rstrip(),
            "",
        ]
    )


def unique_path(path: Path, timestamp: str) -> Path:
    if not path.exists():
        return path

    candidate = path.with_name(f"{path.stem}__{timestamp}{path.suffix}")
    if not candidate.exists():
        return candidate

    counter = 2
    while True:
        numbered = path.with_name(f"{path.stem}__{timestamp}_{counter}{path.suffix}")
        if not numbered.exists():
            return numbered
        counter += 1


def output_path_for(source_path: Path, output_dir: Path, date_prefix: str, timestamp: str) -> Path:
    raw_path = output_dir / f"{date_prefix}__{source_path.name}.md"
    return unique_path(raw_path, timestamp)


def move_original(source_path: Path, target_dir: Path, timestamp: str) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = unique_path(target_dir / source_path.name, timestamp)
    source_path.replace(target_path)
    return target_path


def append_log(
    log_path: Path,
    processed_at: str,
    source_path: Path,
    source_type: str,
    raw_normalized_path: Path | None,
    original_moved_to: Path | None,
    status: str,
    error: str = "",
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.write_text("# Processing Log\n\n", encoding="utf-8")

    raw_value = str(raw_normalized_path) if raw_normalized_path else "-"
    moved_value = str(original_moved_to) if original_moved_to else "-"
    error_value = error if error else "-"

    entry = "\n".join(
        [
            f"## {processed_at}",
            "",
            f"- source_path: {source_path}",
            f"- source_type: {source_type}",
            f"- raw_normalized_path: {raw_value}",
            f"- original_moved_to: {moved_value}",
            f"- status: {status}",
            f"- error: {error_value}",
            "",
        ]
    )

    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)


def process_file(
    source_path: Path,
    output_dir: Path,
    processed_dir: Path,
    failed_dir: Path,
    log_path: Path,
    root: Path,
) -> str:
    now = datetime.now().astimezone()
    processed_at = now.isoformat(timespec="seconds")
    date_prefix = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    source_type = source_path.suffix.lower().lstrip(".") or "unknown"
    result_path: Path | None = None
    moved_path: Path | None = None

    print(f"[PROCESS] {relative_to_root(source_path, root)}")

    try:
        if source_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"unsupported file type: {source_path.suffix or '<none>'}")

        extracted_text = extract_text(source_path)
        if not extracted_text.strip():
            raise ValueError("no text extracted")

        output_dir.mkdir(parents=True, exist_ok=True)
        result_path = output_path_for(source_path, output_dir, date_prefix, timestamp)
        result_path.write_text(
            build_output_markdown(
                source_path=source_path,
                source_type=source_type,
                processed_at=processed_at,
                extracted_text=extracted_text,
            ),
            encoding="utf-8",
            newline="\n",
        )

        moved_path = move_original(source_path, processed_dir, timestamp)
        append_log(
            log_path=log_path,
            processed_at=processed_at,
            source_path=source_path,
            source_type=source_type,
            raw_normalized_path=result_path,
            original_moved_to=moved_path,
            status="success",
        )

        print(f"[OK]      raw: {relative_to_root(result_path, root)}")
        print(f"[MOVED]   original: {relative_to_root(moved_path, root)}")
        return "success"

    except Exception as exc:  # Keep processing the rest of the inbox.
        try:
            moved_path = move_original(source_path, failed_dir, timestamp)
        except Exception as move_exc:
            moved_path = None
            error = f"{exc}; failed to move original: {move_exc}"
        else:
            error = str(exc)

        append_log(
            log_path=log_path,
            processed_at=processed_at,
            source_path=source_path,
            source_type=source_type,
            raw_normalized_path=result_path,
            original_moved_to=moved_path,
            status="error",
            error=error,
        )

        print(f"[ERROR]   {error}")
        if moved_path:
            print(f"[MOVED]   original: {relative_to_root(moved_path, root)}")
        return "error"


def main() -> int:
    root = project_root()
    inbox_dir = root / "inbox"
    new_dir = inbox_dir / "_new"
    processed_dir = inbox_dir / "_processed"
    failed_dir = inbox_dir / "_failed"
    output_dir = root / "Maverick_KB" / "raw_normalized"
    log_path = root / "Maverick_KB" / "PROCESSING_LOG.md"

    new_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    failed_dir.mkdir(parents=True, exist_ok=True)

    print("CL Maverick KB - inbox processor v0.2")
    print(f"Project root:    {root}")
    print(f"Inbox _new:      {new_dir}")
    print(f"Processed:       {processed_dir}")
    print(f"Failed:          {failed_dir}")
    print(f"Raw normalized:  {output_dir}")
    print(f"Processing log:  {log_path}")
    print("-")

    source_files = [
        source_path
        for source_path in sorted(new_dir.iterdir(), key=lambda item: item.name.lower())
        if source_path.is_file()
    ]

    print(f"Found files in inbox/_new: {len(source_files)}")
    if not source_files:
        print("No files to process. Put PDF/DOCX/TXT/MD files into inbox/_new and run again.")
        return 0

    print("-")

    success_count = 0
    error_count = 0

    for index, source_path in enumerate(source_files, start=1):
        print(f"[{index}/{len(source_files)}]")
        status = process_file(
            source_path=source_path,
            output_dir=output_dir,
            processed_dir=processed_dir,
            failed_dir=failed_dir,
            log_path=log_path,
            root=root,
        )
        if status == "success":
            success_count += 1
        else:
            error_count += 1
        print("-")

    print("Done.")
    print(f"Success: {success_count}")
    print(f"Errors:  {error_count}")
    print(f"Open in Obsidian: {relative_to_root(output_dir, root)}")
    print(f"Log: {relative_to_root(log_path, root)}")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
