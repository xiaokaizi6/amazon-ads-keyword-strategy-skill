"""Split raw Amazon ads Markdown articles into metadata, body, updates, and comments.

Input paths:
  data/raw/amazon_ads_articles
  data/processed/amazon_ads_skill/articles_index.jsonl

Output path: data/processed/amazon_ads_skill/article_sections.jsonl

CLI arguments:
  --input-dir: raw Markdown article directory.
  --index-file: JSONL article index path.
  --output-file: JSONL section output path.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_INPUT_DIR = Path("data/raw/amazon_ads_articles")
DEFAULT_INDEX_FILE = Path("data/processed/amazon_ads_skill/articles_index.jsonl")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/article_sections.jsonl")
PROJECT_ROOT = Path.cwd()


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--index-file", type=Path, default=DEFAULT_INDEX_FILE)
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


def load_index(index_file: Path) -> list[dict[str, Any]]:
    """Load article index records in source order."""
    records: list[dict[str, Any]] = []
    with index_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def resolve_article_path(record: dict[str, Any], input_dir: Path) -> Path:
    """Resolve a raw article path from the index record."""
    indexed_path = Path(record.get("file_path", ""))
    if indexed_path.exists():
        return indexed_path
    return input_dir / record["file_name"]


def join_lines(lines: list[str]) -> str:
    """Join original lines without trimming internal content."""
    return "\n".join(lines).strip("\n")


def first_title(lines: list[str], fallback: str = "") -> str:
    """Extract the first Markdown heading title from a line block."""
    for line in lines:
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def is_separator(line: str) -> bool:
    """Return true for Markdown-like separator lines."""
    stripped = line.strip()
    return bool(stripped) and len(stripped) >= 3 and set(stripped) <= {"-", "_", "*"}


def is_update_start(line: str) -> bool:
    """Detect author additions such as date-stamped image or text supplements."""
    stripped = line.strip()
    if not stripped:
        return False
    if re.match(r"^\d{1,2}[./-]\d{1,2}\s*日?[，,、:：\s].*", stripped):
        return True
    return bool(re.match(r"^(补充|更新|新增|追加|图片补充|图补|update)\b", stripped, flags=re.I))


def split_body_updates(lines: list[str]) -> tuple[list[str], list[tuple[str, list[str]]]]:
    """Split author body lines into the main body and one or more author updates."""
    update_starts = [index for index, line in enumerate(lines) if is_update_start(line)]
    if not update_starts:
        return lines, []

    starts: list[int] = []
    for index in update_starts:
        start = index
        previous = index - 1
        if previous >= 0 and is_separator(lines[previous]):
            start = previous
        if start not in starts:
            starts.append(start)

    body_end = starts[0]
    updates: list[tuple[str, list[str]]] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        update_lines = lines[start:end]
        heading = next((line.strip() for line in update_lines if is_update_start(line)), "作者补充")
        updates.append((heading, update_lines))
    return lines[:body_end], updates


def comment_index_from_heading(heading: str) -> int | None:
    """Extract numeric comment index from a comment heading."""
    match = re.search(r"评论\s*(\d+)", heading)
    return int(match.group(1)) if match else None


def parse_comment_meta(lines: list[str]) -> tuple[str, str]:
    """Extract comment author and timestamp from a comment block."""
    author = ""
    comment_time = ""
    for line in lines:
        author_match = re.match(r"^-\s*评论人名称\s*[:：]\s*(.*?)\s*$", line)
        time_match = re.match(r"^-\s*评论时间\s*[:：]\s*(.*?)\s*$", line)
        if author_match:
            author = author_match.group(1).strip()
        elif time_match:
            comment_time = time_match.group(1).strip()
    return author, comment_time


def make_section(
    record: dict[str, Any],
    section_number: int,
    role: str,
    heading: str,
    text: str,
    *,
    comment_index: int | None = None,
    comment_author: str = "",
    comment_time: str = "",
    notes: str = "",
) -> dict[str, Any]:
    """Build one section output record."""
    return {
        "source_id": record["source_id"],
        "file_name": record["file_name"],
        "section_id": f"{record['source_id']}-S{section_number:03d}",
        "section_type": role,
        "section_role": role,
        "comment_index": comment_index,
        "comment_author": comment_author,
        "comment_time": comment_time,
        "heading": heading,
        "text": text,
        "char_count": len(text),
        "extraction_notes": notes,
    }


def split_comment_region(lines: list[str]) -> tuple[list[str], list[tuple[str, list[str]]]]:
    """Split a comment region into preface lines and explicit comment blocks."""
    preface: list[str] = []
    comments: list[tuple[str, list[str]]] = []
    current_heading = ""
    current_lines: list[str] = []

    for line in lines:
        heading_match = re.match(r"^###\s+(评论\s*\d+)\s*$", line.strip())
        if heading_match:
            if current_heading:
                comments.append((current_heading, current_lines))
            else:
                preface = current_lines
            current_heading = heading_match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_heading:
        comments.append((current_heading, current_lines))
    else:
        preface = current_lines
    return preface, comments


def split_article(record: dict[str, Any], article_path: Path) -> list[dict[str, Any]]:
    """Split one indexed article into structured sections."""
    text = decode_markdown(article_path.read_bytes())
    lines = text.splitlines()

    body_heading_index = next((index for index, line in enumerate(lines) if line.strip() == "## 发布人正文"), None)
    comment_heading_index = next((index for index, line in enumerate(lines) if line.strip() == "## 评论区"), None)

    sections: list[dict[str, Any]] = []

    def add_section(role: str, heading: str, section_text: str, **kwargs: Any) -> None:
        if section_text.strip() or role == "metadata":
            sections.append(make_section(record, len(sections) + 1, role, heading, section_text, **kwargs))

    if body_heading_index is not None:
        metadata_lines = lines[:body_heading_index]
        body_start = body_heading_index + 1
    else:
        metadata_lines = lines[: comment_heading_index if comment_heading_index is not None else 0]
        body_start = len(metadata_lines)

    add_section("metadata", first_title(metadata_lines, record.get("title", "")), join_lines(metadata_lines))

    body_end = comment_heading_index if comment_heading_index is not None else len(lines)
    if body_heading_index is not None:
        body_lines = lines[body_start:body_end]
        main_body_lines, update_blocks = split_body_updates(body_lines)
        if join_lines(main_body_lines).strip():
            add_section("author_body", "发布人正文", join_lines(main_body_lines))
        for heading, update_lines in update_blocks:
            add_section(
                "author_update",
                heading,
                join_lines(update_lines),
                notes="detected date-stamped or explicit author supplement",
            )
    elif body_end > body_start:
        add_section("unknown", "unknown", join_lines(lines[body_start:body_end]), notes="body heading not found")

    if comment_heading_index is not None:
        comment_lines = lines[comment_heading_index + 1 :]
        preface_lines, comments = split_comment_region(comment_lines)
        preface_text = join_lines(preface_lines)
        if preface_text.strip():
            notes = "comment area without explicit comment items"
            add_section("unknown", "评论区", preface_text, notes=notes)

        for heading, comment_lines_block in comments:
            comment_text = join_lines(comment_lines_block)
            comment_author, comment_time = parse_comment_meta(comment_lines_block)
            add_section(
                "comment",
                heading,
                comment_text,
                comment_index=comment_index_from_heading(heading),
                comment_author=comment_author,
                comment_time=comment_time,
            )

    return sections


def write_jsonl(records: list[dict[str, Any]], output_file: Path) -> None:
    """Write records as UTF-8 JSONL."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    """Run section splitting."""
    args = parse_args()
    if not args.input_dir.exists():
        raise FileNotFoundError(f"input directory not found: {args.input_dir}")
    if not args.index_file.exists():
        raise FileNotFoundError(f"index file not found: {args.index_file}")

    sections: list[dict[str, Any]] = []
    for record in load_index(args.index_file):
        if record.get("status") in {"empty", "error"}:
            continue
        article_path = resolve_article_path(record, args.input_dir)
        sections.extend(split_article(record, article_path))

    write_jsonl(sections, args.output_file)
    print(f"split {len(sections)} sections -> {args.output_file.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
