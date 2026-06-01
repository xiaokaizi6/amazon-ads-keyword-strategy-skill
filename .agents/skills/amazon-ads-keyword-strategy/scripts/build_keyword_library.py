"""Build a structured Amazon keyword library.

Output paths:
  data/processed/amazon_ads_skill/keyword_library.jsonl
  data/processed/amazon_ads_skill/keyword_library.csv
  data/processed/amazon_ads_skill/keyword_library_report.md

CLI arguments:
  --source-file: JSONL or CSV source file; can be passed multiple times.
  --seed-keyword: manual seed keyword; can be passed multiple times.
  --product-stage: product stage context for classification.
  --output-jsonl: JSONL keyword library output path.
  --output-csv: CSV keyword library output path.
  --report-output: Markdown report output path.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from classify_keywords import (
    METRIC_FIELDS,
    classify_record,
    coerce_list,
    extract_keyword,
    extract_metrics,
    load_records,
    normalize_keyword,
)


DEFAULT_OUTPUT_JSONL = Path("data/processed/amazon_ads_skill/keyword_library.jsonl")
DEFAULT_OUTPUT_CSV = Path("data/processed/amazon_ads_skill/keyword_library.csv")
DEFAULT_REPORT_OUTPUT = Path("data/processed/amazon_ads_skill/keyword_library_report.md")

TEXT_FIELDS_FOR_EXTRACTION = [
    "keyword",
    "search_term",
    "customer_search_term",
    "condition",
    "action",
    "evidence_quote",
    "case_title",
    "problem",
]
ASIN_RE = re.compile(r"\bB0[A-Z0-9]{8}\b", re.I)
ENGLISH_PHRASE_RE = re.compile(r"\b[a-zA-Z][a-zA-Z0-9-]*(?:\s+[a-zA-Z][a-zA-Z0-9-]*){1,5}\b")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-file", action="append", type=Path, default=[])
    parser.add_argument("--seed-keyword", action="append", default=[])
    parser.add_argument("--product-stage", default="unknown")
    parser.add_argument("--output-jsonl", type=Path, default=DEFAULT_OUTPUT_JSONL)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def extract_phrases(text: str) -> list[str]:
    """Extract simple English keyword-like phrases from a text field."""
    phrases: list[str] = []
    for match in ENGLISH_PHRASE_RE.findall(text or ""):
        normalized = normalize_keyword(match)
        token_count = len(normalized.split())
        if token_count < 2 or token_count > 6:
            continue
        if normalized in {"search term", "keyword report", "amazon ads"}:
            continue
        phrases.append(match.strip())
    return phrases


def source_type_from_path(path: Path) -> str:
    """Infer source type from a source file name."""
    name = path.name.lower()
    if "search" in name or "广告" in name:
        return "advertising_search_term_report"
    if "competitor" in name or "asin" in name or "竞品" in name:
        return "competitor_reverse_lookup"
    if "case" in name:
        return "case_observation"
    if "comment" in name:
        return "comment_signal"
    return "unknown"


def candidate_from_row(row: dict[str, Any], source_file: Path | None) -> list[dict[str, Any]]:
    """Convert one source row to one or more candidate keyword records."""
    keyword = extract_keyword(row)
    source_type = str(row.get("source_type") or (source_type_from_path(source_file) if source_file else "manual_seed"))
    source_detail = str(row.get("source_detail") or (source_file.as_posix() if source_file else "manual_seed"))
    phrases = [keyword] if keyword else []
    if not phrases:
        for field in TEXT_FIELDS_FOR_EXTRACTION:
            value = row.get(field)
            if isinstance(value, str):
                phrases.extend(extract_phrases(value))

    candidates = []
    related_asins = sorted(
        set(coerce_list(row.get("related_asins")) + ASIN_RE.findall(json.dumps(row, ensure_ascii=False)))
    )
    metrics = extract_metrics(row)
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase:
            continue
        candidates.append(
            {
                "keyword": phrase,
                "source_type": source_type,
                "source_detail": source_detail,
                "related_asins": related_asins,
                "metrics": metrics,
            }
        )
    return candidates


def merge_metrics(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    """Merge metrics conservatively without inventing unavailable data."""
    merged = dict(existing)
    for field in METRIC_FIELDS:
        left = merged.get(field)
        right = incoming.get(field)
        if right is None:
            continue
        if left is None:
            merged[field] = right
        elif field in {"impressions", "clicks", "orders", "spend", "sales"}:
            merged[field] = left + right
        else:
            merged[field] = right
    return merged


def merge_candidates(candidates: list[dict[str, Any]], product_stage: str) -> list[dict[str, Any]]:
    """Deduplicate, classify, and assign keyword IDs."""
    merged: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        normalized = normalize_keyword(candidate["keyword"])
        if not normalized:
            continue
        if normalized not in merged:
            merged[normalized] = candidate
            merged[normalized]["normalized_keyword"] = normalized
            continue
        current = merged[normalized]
        current["source_detail"] = " | ".join(
            sorted(set([current.get("source_detail", ""), candidate.get("source_detail", "")]) - {""})
        )
        current["related_asins"] = sorted(
            set(coerce_list(current.get("related_asins")) + coerce_list(candidate.get("related_asins")))
        )
        current["metrics"] = merge_metrics(current.get("metrics", {}), candidate.get("metrics", {}))

    records: list[dict[str, Any]] = []
    for index, candidate in enumerate(sorted(merged.values(), key=lambda item: item["normalized_keyword"]), start=1):
        candidate["keyword_id"] = f"KW{index:06d}"
        records.append(classify_record(candidate, product_stage=product_stage))
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write records to JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def csv_value(value: Any) -> Any:
    """Format nested fields for CSV."""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    """Write keyword library records to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "keyword_id",
        "keyword",
        "normalized_keyword",
        "keyword_type",
        "source_type",
        "source_detail",
        "related_asins",
        "product_stage",
        "search_intent",
        "relevance_score",
        "traffic_level",
        "competition_level",
        "cpc_level",
        "conversion_potential",
        "ranking_priority",
        "ad_priority",
        "match_type_recommendation",
        "campaign_recommendation",
        "negative_match_recommendation",
        "risk_flags",
        "metrics",
        "status",
        "last_updated",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: csv_value(record.get(field, "")) for field in fields})


def write_report(path: Path, records: list[dict[str, Any]], source_files: list[Path]) -> None:
    """Write a Markdown build report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    type_counts = Counter(record["keyword_type"] for record in records)
    status_counts = Counter(record["status"] for record in records)
    source_counts = Counter(record["source_type"] for record in records)
    risk_counts = Counter(flag for record in records for flag in record.get("risk_flags", []))

    lines = [
        "# Keyword Library Report",
        "",
        f"- Total keywords: {len(records)}",
        f"- Source files: {len(source_files)}",
        "",
        "## Source Files",
        "",
    ]
    if source_files:
        lines.extend(f"- `{path.as_posix()}`" for path in source_files)
    else:
        lines.append("- Manual seed keywords only.")

    for title, counter in (
        ("Keyword Types", type_counts),
        ("Statuses", status_counts),
        ("Source Types", source_counts),
        ("Risk Flags", risk_counts),
    ):
        lines.extend(["", f"## {title}", "", "| Value | Count |", "| --- | --- |"])
        if counter:
            lines.extend(f"| {key} | {value} |" for key, value in sorted(counter.items()))
        else:
            lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- Validate comment-sourced terms before treating them as rules.",
            "- Separate converting terms from natural ranking target terms.",
            "- Review negative candidates by sample size before applying negative phrase.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run keyword library building."""
    args = parse_args()
    candidates: list[dict[str, Any]] = []
    for keyword in args.seed_keyword:
        candidates.append(
            {
                "keyword": keyword,
                "source_type": "manual_seed",
                "source_detail": "manual seed",
                "related_asins": [],
                "metrics": {field: None for field in METRIC_FIELDS},
            }
        )
    for source_file in args.source_file:
        rows = load_records(source_file)
        if args.limit is not None:
            rows = rows[: args.limit]
        for row in rows:
            candidates.extend(candidate_from_row(row, source_file))

    records = merge_candidates(candidates, product_stage=args.product_stage)
    write_jsonl(args.output_jsonl, records)
    write_csv(args.output_csv, records)
    write_report(args.report_output, records, args.source_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
