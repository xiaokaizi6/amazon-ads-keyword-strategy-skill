"""Index raw Amazon ads Markdown articles.

Input path: data/raw/amazon_ads_articles
Output path: data/processed/amazon_ads_skill/articles_index.jsonl

CLI arguments:
  --input-dir: raw Markdown article directory.
  --output-file: JSONL article index path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_INPUT_DIR = Path("data/raw/amazon_ads_articles")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/articles_index.jsonl")
PROJECT_ROOT = Path.cwd()
METADATA_KEYS = {
    "文章链接": "article_url",
    "发布人名称": "publisher_name",
    "发布时间": "publish_date",
    "站内元信息": "site_meta",
    "圈子/标签": "tags",
    "爬取到的公开回复数": "raw_reply_count",
    "爬取到的评论数": "raw_comment_count",
}


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_FILE)
    return parser.parse_args()


def decode_markdown(raw_bytes: bytes) -> str:
    """Decode Markdown bytes using common encodings for Chinese exports."""
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def relative_path(path: Path) -> str:
    """Return a stable project-relative path."""
    try:
        return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def parse_int(value: str) -> int | None:
    """Parse the first integer from a metadata value."""
    match = re.search(r"\d+", value)
    return int(match.group(0)) if match else None


def parse_tags(value: str) -> list[str]:
    """Split tag metadata into a clean list."""
    return [part.strip() for part in re.split(r"[,，/、]", value) if part.strip()]


def extract_metadata(text: str) -> dict[str, Any]:
    """Extract title, top metadata, headings, and structural flags."""
    metadata: dict[str, Any] = {
        "title": "",
        "article_url": "",
        "publisher_name": "",
        "publish_date": "",
        "site_meta": "",
        "tags": [],
        "raw_reply_count": None,
        "raw_comment_count": None,
        "has_author_body": False,
        "has_comments": False,
        "detected_headings": [],
    }

    lines = text.splitlines()
    for line in lines:
        title_match = re.match(r"^#\s+(.+?)\s*$", line)
        if title_match:
            metadata["title"] = title_match.group(1).strip()
            break

    headings: list[str] = []
    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading_match:
            heading = heading_match.group(2).strip()
            headings.append(heading)
            if heading == "发布人正文":
                metadata["has_author_body"] = True
            elif heading == "评论区" or heading.startswith("评论 "):
                metadata["has_comments"] = True

        meta_match = re.match(r"^-\s*([^:：]+)\s*[:：]\s*(.*?)\s*$", line)
        if not meta_match:
            continue

        key = meta_match.group(1).strip()
        value = meta_match.group(2).strip()
        field = METADATA_KEYS.get(key)
        if field == "tags":
            metadata[field] = parse_tags(value)
        elif field in {"raw_reply_count", "raw_comment_count"}:
            metadata[field] = parse_int(value)
        elif field:
            metadata[field] = value

    metadata["detected_headings"] = headings
    if metadata["raw_comment_count"] and metadata["raw_comment_count"] > 0:
        metadata["has_comments"] = True
    return metadata


def build_record(path: Path, source_id: str, seen_hashes: dict[str, str]) -> dict[str, Any]:
    """Build one article index record."""
    base_record: dict[str, Any] = {
        "source_id": source_id,
        "file_name": path.name,
        "file_path": relative_path(path),
        "title": "",
        "article_url": "",
        "publisher_name": "",
        "publish_date": "",
        "site_meta": "",
        "tags": [],
        "raw_reply_count": None,
        "raw_comment_count": None,
        "char_count": 0,
        "has_author_body": False,
        "has_comments": False,
        "detected_headings": [],
        "content_hash": "",
        "status": "ok",
        "error_message": "",
    }

    try:
        raw_bytes = path.read_bytes()
        content_hash = hashlib.sha256(raw_bytes).hexdigest()
        text = decode_markdown(raw_bytes)
        base_record["content_hash"] = content_hash
        base_record["char_count"] = len(text)

        if not text.strip():
            base_record["status"] = "empty"
            base_record["error_message"] = "file is empty"
            return base_record

        base_record.update(extract_metadata(text))
        if content_hash in seen_hashes:
            base_record["status"] = "duplicate"
            base_record["error_message"] = f"duplicate of {seen_hashes[content_hash]}"
        else:
            seen_hashes[content_hash] = source_id
    except Exception as exc:  # noqa: BLE001 - keep indexing other files.
        base_record["status"] = "error"
        base_record["error_message"] = f"{type(exc).__name__}: {exc}"

    return base_record


def iter_markdown_files(input_dir: Path) -> list[Path]:
    """Return Markdown files in deterministic order."""
    return sorted(input_dir.rglob("*.md"), key=lambda path: relative_path(path).lower())


def write_jsonl(records: list[dict[str, Any]], output_file: Path) -> None:
    """Write records as UTF-8 JSONL."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    """Run article indexing."""
    args = parse_args()
    if not args.input_dir.exists():
        raise FileNotFoundError(f"input directory not found: {args.input_dir}")

    seen_hashes: dict[str, str] = {}
    records = [
        build_record(path, f"A{index:03d}", seen_hashes)
        for index, path in enumerate(iter_markdown_files(args.input_dir), start=1)
    ]
    write_jsonl(records, args.output_file)
    print(f"indexed {len(records)} files -> {args.output_file.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
