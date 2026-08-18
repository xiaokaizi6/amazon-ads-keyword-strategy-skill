"""Export a DOCX body as source-faithful, searchable JSONL records.

This uses only the DOCX Open XML package so it can retain every body
paragraph and table without altering the original binary source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--reviewed-at", default=date.today().isoformat())
    return parser.parse_args()


def node_text(node: ET.Element) -> str:
    return "".join(text for text in node.itertext() if text).strip()


def table_rows(table: ET.Element) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in table.findall(f"{W_NS}tr"):
        rows.append([node_text(cell) for cell in row.findall(f"{W_NS}tc")])
    return rows


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    args = parse_args()
    with zipfile.ZipFile(args.source) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find(f"{W_NS}body")
    if body is None:
        raise ValueError("DOCX has no word/document.xml body")

    records: list[dict[str, object]] = []
    for index, node in enumerate(body, start=1):
        if node.tag == f"{W_NS}p":
            text = node_text(node)
            if not text:
                continue
            content_type = "paragraph"
            content: object = text
        elif node.tag == f"{W_NS}tbl":
            rows = table_rows(node)
            if not rows:
                continue
            content_type = "table"
            content = rows
        else:
            continue
        records.append(
            {
                "record_id": f"{args.source_id}-DOCX-N{index:03d}",
                "source_id": args.source_id,
                "source_location": f"DOCX body node {index:03d} ({content_type})",
                "content_type": content_type,
                "content": content,
                "source_sha256": sha256(args.source),
                "reviewed_at": args.reviewed_at,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"Exported {len(records)} source-faithful DOCX records to {args.output}")


if __name__ == "__main__":
    main()
