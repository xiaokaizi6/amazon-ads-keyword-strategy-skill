"""Update keyword-library statuses from an advertising search-term report.

Input paths:
  data/processed/amazon_ads_skill/keyword_library.jsonl
  an advertising search-term report in JSONL or CSV

Output paths:
  data/processed/amazon_ads_skill/keyword_library.jsonl
  data/processed/amazon_ads_skill/keyword_library_report.md

CLI arguments:
  --library-file: existing keyword library JSONL path.
  --ads-file: advertising search-term report JSONL or CSV path.
  --output-file: updated keyword library JSONL path.
  --report-output: Markdown update report path.
  --target-acos: acceptable ACOS threshold for converting terms.
  --negative-click-threshold: clicks with zero orders before negative candidate.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from classify_keywords import (
    METRIC_FIELDS,
    classify_record,
    extract_keyword,
    extract_metrics,
    load_records,
    normalize_keyword,
)


DEFAULT_LIBRARY_FILE = Path("data/processed/amazon_ads_skill/keyword_library.jsonl")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/keyword_library.jsonl")
DEFAULT_REPORT_OUTPUT = Path("data/processed/amazon_ads_skill/keyword_library_report.md")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library-file", type=Path, default=DEFAULT_LIBRARY_FILE)
    parser.add_argument("--ads-file", type=Path, required=True)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_FILE)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    parser.add_argument("--target-acos", type=float, default=0.35)
    parser.add_argument("--negative-click-threshold", type=int, default=20)
    parser.add_argument("--high-spend-threshold", type=float, default=50.0)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load JSONL records."""
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on {path}:{line_number}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write JSONL records."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def infer_updated_status(
    record: dict[str, Any],
    metrics: dict[str, float | None],
    target_acos: float,
    negative_click_threshold: int,
    high_spend_threshold: float,
) -> tuple[str, list[str]]:
    """Infer updated keyword status and update notes."""
    notes: list[str] = []
    orders = metrics.get("orders") or 0
    clicks = metrics.get("clicks") or 0
    acos = metrics.get("acos")
    spend = metrics.get("spend") or 0
    current_status = str(record.get("status") or "unverified")

    if orders > 0 and (acos is None or acos <= target_acos):
        notes.append("orders with acceptable ACOS")
        if record.get("ranking_priority") == "high" or record.get("keyword_type") == "ranking_target_keyword":
            return "ranking_target", notes
        return "validated_converting", notes
    if orders > 0:
        notes.append("orders exist but ACOS needs review")
        return current_status if current_status != "unverified" else "testing", notes
    if clicks >= negative_click_threshold:
        notes.append("high clicks with zero orders")
        return "negative_candidate", notes
    if spend >= high_spend_threshold and orders == 0:
        notes.append("high spend with zero orders")
        return "negative_candidate", notes
    return current_status if current_status != "unverified" else "testing", notes


def merge_metrics(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    """Merge ad report metrics into library metrics."""
    merged = dict(existing)
    for field in METRIC_FIELDS:
        value = incoming.get(field)
        if value is not None:
            merged[field] = value
    return merged


def write_report(
    path: Path,
    records: list[dict[str, Any]],
    changes: list[dict[str, Any]],
    ads_file: Path,
) -> None:
    """Write a Markdown update report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    status_counts = Counter(record.get("status", "unknown") for record in records)
    lines = [
        "# Keyword Library Report",
        "",
        f"- Updated from ads file: `{ads_file.as_posix()}`",
        f"- Total keywords: {len(records)}",
        f"- Changed keywords: {len(changes)}",
        "",
        "## Status Distribution",
        "",
        "| Status | Count |",
        "| --- | --- |",
    ]
    lines.extend(f"| {status} | {count} |" for status, count in sorted(status_counts.items()))
    lines.extend(["", "## Changes", "", "| Keyword | Old status | New status | Reason |", "| --- | --- | --- | --- |"])
    if changes:
        lines.extend(
            "| {keyword} | {old} | {new} | {reason} |".format(
                keyword=change["keyword"],
                old=change["old_status"],
                new=change["new_status"],
                reason=", ".join(change["notes"]),
            )
            for change in changes
        )
    else:
        lines.append("| none | - | - | No status changes. |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run keyword library update from ads data."""
    args = parse_args()
    library = load_jsonl(args.library_file)
    by_normalized = {record["normalized_keyword"]: dict(record) for record in library}
    changes: list[dict[str, Any]] = []

    for row in load_records(args.ads_file):
        keyword = extract_keyword(row)
        if not keyword:
            continue
        normalized = normalize_keyword(keyword)
        metrics = extract_metrics(row)
        record = by_normalized.get(
            normalized,
            classify_record(
                {
                    "keyword": keyword,
                    "normalized_keyword": normalized,
                    "source_type": "advertising_search_term_report",
                    "source_detail": args.ads_file.as_posix(),
                    "metrics": metrics,
                }
            ),
        )
        old_status = str(record.get("status") or "unverified")
        record["metrics"] = merge_metrics(record.get("metrics", {}), metrics)
        new_status, notes = infer_updated_status(
            record,
            record["metrics"],
            args.target_acos,
            args.negative_click_threshold,
            args.high_spend_threshold,
        )
        record["status"] = new_status
        if new_status == "negative_candidate":
            record["negative_match_recommendation"] = "negative_candidate"
            record["ad_priority"] = "low"
        if new_status == "validated_converting":
            record["keyword_type"] = "converting_keyword"
            record["ad_priority"] = "high"
            record["match_type_recommendation"] = ["exact", "phrase"]
        if new_status == "ranking_target":
            record["ranking_priority"] = "high"
        if notes:
            record["source_detail"] = " | ".join(
                sorted(set([str(record.get("source_detail") or ""), args.ads_file.as_posix()]) - {""})
            )
        if old_status != new_status:
            changes.append(
                {
                    "keyword": record["keyword"],
                    "old_status": old_status,
                    "new_status": new_status,
                    "notes": notes,
                }
            )
        by_normalized[normalized] = record

    records = sorted(by_normalized.values(), key=lambda item: item["normalized_keyword"])
    for index, record in enumerate(records, start=1):
        if not record.get("keyword_id"):
            record["keyword_id"] = f"KW{index:06d}"
    write_jsonl(args.output_file, records)
    write_report(args.report_output, records, changes, args.ads_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
