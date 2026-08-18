#!/usr/bin/env python3
"""Audit source-by-source retrieval coverage for the portable evidence pack."""

from __future__ import annotations

import argparse
import json
import zipfile
from collections import defaultdict
from pathlib import Path


def jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def office_media_count(path: Path) -> int:
    prefix = "word/media/" if path.suffix.lower() == ".docx" else "xl/media/"
    with zipfile.ZipFile(path) as archive:
        return sum(1 for entry in archive.infolist() if not entry.is_dir() and entry.filename.startswith(prefix))


def parse_artifact(value: str) -> tuple[str, str, Path]:
    try:
        source_id, kind, path = value.split("|", 2)
    except ValueError as error:
        raise ValueError("--artifact must be SOURCE_ID|KIND|PATH") from error
    return source_id, kind, Path(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--article-sections", type=Path, required=True)
    parser.add_argument("--asset-root", type=Path, required=True)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sections_by_file: dict[str, int] = defaultdict(int)
    for section in jsonl(args.article_sections):
        sections_by_file[str(section["file_name"])] += 1

    artifacts: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in args.artifact:
        source_id, kind, path = parse_artifact(item)
        rows = jsonl(path)
        row_ids = {str(row.get("source_id", "")) for row in rows}
        if rows and row_ids != {source_id}:
            raise ValueError(f"artifact {path} has unexpected source ids: {sorted(row_ids)}")
        try:
            portable_path = path.resolve().relative_to(args.asset_root.resolve()).as_posix()
        except ValueError:
            portable_path = path.as_posix()
        artifacts[source_id].append({"kind": kind, "path": portable_path, "record_count": len(rows)})

    rows: list[dict[str, object]] = []
    for source in jsonl(args.manifest):
        source_id = str(source["source_id"])
        file_name = str(source["file_name"])
        source_type = str(source["source_type"])
        original = args.asset_root / str(source["portable_asset_path"])
        issues: list[str] = []
        methods: list[dict[str, object]] = artifacts[source_id].copy()
        if not original.is_file():
            issues.append("portable_original_missing")

        if source_type == "project_corpus":
            section_count = sections_by_file.get(file_name, 0)
            methods.insert(
                0,
                {
                    "kind": "markdown_sections",
                    "path": "assets/knowledge/article_sections.jsonl",
                    "record_count": section_count,
                },
            )
            if section_count == 0:
                issues.append("article_has_no_searchable_sections")
        else:
            extension = original.suffix.lower()
            method_counts = {str(item["kind"]): int(item["record_count"]) for item in methods}
            if extension in {".docx", ".xlsx"}:
                media_expected = office_media_count(original)
                media_found = method_counts.get("embedded_media_ocr", 0)
                if media_expected != media_found:
                    issues.append(f"embedded_media_ocr_count_mismatch_expected_{media_expected}_found_{media_found}")
                body_found = method_counts.get("docx_body", 0) + method_counts.get("xlsx_cells", 0)
                if body_found == 0 and media_expected == 0:
                    issues.append("office_source_has_no_searchable_body_or_media")
            elif extension == ".pdf" and method_counts.get("pdf_page_ocr", 0) == 0:
                issues.append("pdf_has_no_page_ocr")
            elif not methods:
                issues.append("user_source_has_no_retrieval_derivative")

        rows.append(
            {
                "source_id": source_id,
                "file_name": file_name,
                "source_type": source_type,
                "original_asset": str(source["portable_asset_path"]),
                "original_integrity": source.get("portable_integrity"),
                "retrieval_methods": methods,
                "full_content_retrieval_status": "available_with_source_boundaries" if not issues else "incomplete",
                "validation_issues": issues,
                "source_authority": "original_uploaded_or_project_source",
                "boundary": "OCR is a retrieval aid only; verify tables, images, numbers and low-confidence text against the original asset.",
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    available = sum(row["full_content_retrieval_status"] == "available_with_source_boundaries" for row in rows)
    print(f"Audited {len(rows)} sources; retrieval available: {available}; incomplete: {len(rows) - available}")


if __name__ == "__main__":
    main()
