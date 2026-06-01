"""Normalize extracted Amazon ads strategy records.

Input path: data/processed/amazon_ads_skill/extracted_records.jsonl

Output paths:
  data/processed/amazon_ads_skill/normalized_records.jsonl
  data/processed/amazon_ads_skill/merged_rules.jsonl
  data/processed/amazon_ads_skill/case_library.jsonl
  data/processed/amazon_ads_skill/normalization_report.md

CLI arguments:
  --input-file: JSONL extracted records path.
  --normalized-output: JSONL normalized records path.
  --rules-output: JSONL merged rules path.
  --cases-output: JSONL case library path.
  --report-output: Markdown normalization report path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DEFAULT_INPUT_FILE = Path("data/processed/amazon_ads_skill/extracted_records.jsonl")
DEFAULT_NORMALIZED_OUTPUT = Path("data/processed/amazon_ads_skill/normalized_records.jsonl")
DEFAULT_RULES_OUTPUT = Path("data/processed/amazon_ads_skill/merged_rules.jsonl")
DEFAULT_CASES_OUTPUT = Path("data/processed/amazon_ads_skill/case_library.jsonl")
DEFAULT_REPORT_OUTPUT = Path("data/processed/amazon_ads_skill/normalization_report.md")


RULE_SOURCE_TYPES = {"executable_rule", "diagnostic_hypothesis"}
CASE_SOURCE_TYPES = {"case_observation"}
NOISE_SOURCE_TYPES = {"irrelevant_noise"}


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", type=Path, default=DEFAULT_INPUT_FILE)
    parser.add_argument("--normalized-output", type=Path, default=DEFAULT_NORMALIZED_OUTPUT)
    parser.add_argument("--rules-output", type=Path, default=DEFAULT_RULES_OUTPUT)
    parser.add_argument("--cases-output", type=Path, default=DEFAULT_CASES_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load JSONL records."""
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on {path}:{line_number}: {exc}") from exc
    return rows


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write JSONL records."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def compact_text(text: str) -> str:
    """Normalize text for grouping without changing source-facing values."""
    text = re.sub(r"\s+", "", text or "").lower()
    text = re.sub(r"[，。；：、,.!:;?？（）()【】\[\]\"'“”‘’]", "", text)
    return text


def stable_hash(text: str, length: int = 12) -> str:
    """Return a short stable hash."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:length]


def unique_list(values: list[Any]) -> list[Any]:
    """Return values deduplicated by JSON representation."""
    seen: set[str] = set()
    result: list[Any] = []
    for value in values:
        key = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def source_ref(record: dict[str, Any]) -> dict[str, Any]:
    """Build a compact source reference for merged outputs."""
    return {
        "record_id": record["record_id"],
        "source_id": record["source_id"],
        "section_id": record["section_id"],
        "section_role": record["section_role"],
        "record_type": record["record_type"],
        "confidence": record["confidence"],
        "evidence_quote": record["evidence_quote"],
    }


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Create a normalized record while preserving the extracted record."""
    normalized_type = record["record_type"]
    if record["record_type"] == "diagnostic_hypothesis":
        normalized_type = "diagnostic_rule_candidate"
    elif record["record_type"] == "irrelevant_noise":
        normalized_type = "noise_record"

    normalized = dict(record)
    normalized.update(
        {
            "normalized_type": normalized_type,
            "normalized_topic": record.get("topic") or "unknown",
            "source_ref": source_ref(record),
        }
    )
    return normalized


def rule_group_key(record: dict[str, Any]) -> str:
    """Group semantically close rules without merging different thresholds."""
    threshold = compact_text(record.get("metric_threshold", ""))
    condition = compact_text(record.get("condition", ""))[:80]
    action = compact_text(record.get("action", ""))[:80]
    topic = record.get("topic") or "unknown"
    stage = record.get("product_stage") or "unknown"
    ad_type = record.get("ad_type") or "unknown"
    match_type = record.get("match_type") or "unknown"
    return "|".join([topic, stage, ad_type, match_type, threshold, condition, action])


def confidence_for_group(records: list[dict[str, Any]]) -> str:
    """Infer group confidence from source confidence and source roles."""
    if any(record["confidence"] == "high" for record in records) and len(records) >= 2:
        return "high"
    if any(record["confidence"] == "medium" for record in records):
        return "medium"
    return "low"


def first_non_empty(records: list[dict[str, Any]], field: str) -> str:
    """Return the first non-empty field value."""
    for record in records:
        value = record.get(field, "")
        if value:
            return value
    return ""


def merged_threshold(records: list[dict[str, Any]]) -> str:
    """Preserve distinct thresholds without forcing one canonical threshold."""
    thresholds = unique_list([record.get("metric_threshold", "") for record in records if record.get("metric_threshold")])
    return " | ".join(thresholds)


def build_rule_groups(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build merged rules from executable rules and diagnostic candidates."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record["record_type"] in RULE_SOURCE_TYPES:
            groups[rule_group_key(record)].append(record)

    merged_rules: list[dict[str, Any]] = []
    for index, group_records in enumerate(groups.values(), start=1):
        primary = group_records[0]
        supporting = [source_ref(record) for record in group_records]
        comment_signals = [
            source_ref(record)
            for record in group_records
            if record["section_role"] == "comment" or record.get("comment_signal") not in {"", "none"}
        ]
        tags = sorted({tag for record in group_records for tag in record.get("tags", [])})
        if any(record["record_type"] == "diagnostic_hypothesis" for record in group_records):
            tags = sorted(set(tags + ["diagnostic_candidate"]))
        minority_view = []
        if len(group_records) == 1 and primary["section_role"] == "comment":
            minority_view = [source_ref(primary)]

        merged_rules.append(
            {
                "rule_id": f"R{index:03d}",
                "topic": primary.get("topic", ""),
                "product_stage": primary.get("product_stage", "unknown"),
                "ad_type": primary.get("ad_type", "unknown"),
                "match_type": primary.get("match_type", "unknown"),
                "condition": first_non_empty(group_records, "condition"),
                "recommended_action": first_non_empty(group_records, "action"),
                "metric_threshold": merged_threshold(group_records),
                "reasoning": first_non_empty(group_records, "reasoning"),
                "supporting_sources": unique_list(supporting),
                "opposing_sources": [],
                "case_sources": [],
                "comment_signals": unique_list(comment_signals),
                "confidence": confidence_for_group(group_records),
                "limitations": first_non_empty(group_records, "limitations")
                or "需要结合产品阶段、毛利、预算、样本量和广告目标验证。",
                "tags": tags,
                "minority_view": minority_view,
            }
        )
    return merged_rules


def attach_counterexamples(
    merged_rules: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
) -> None:
    """Attach counterexamples as opposing sources instead of rules."""
    for counterexample in counterexamples:
        attached = False
        counter_tags = set(counterexample.get("tags", []))
        for rule in merged_rules:
            if counterexample.get("topic") == rule.get("topic") or counter_tags.intersection(rule.get("tags", [])):
                rule["opposing_sources"].append(source_ref(counterexample))
                attached = True
        if not attached and merged_rules:
            nearest = min(
                merged_rules,
                key=lambda rule: 0 if rule.get("topic") == counterexample.get("topic") else 1,
            )
            nearest["opposing_sources"].append(source_ref(counterexample))

    for rule in merged_rules:
        rule["opposing_sources"] = unique_list(rule["opposing_sources"])


def build_case_library(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build case library entries from case observations."""
    cases: list[dict[str, Any]] = []
    for index, record in enumerate(
        [record for record in records if record["record_type"] in CASE_SOURCE_TYPES],
        start=1,
    ):
        metrics = record.get("case_metrics", {})
        title = record.get("condition") or record.get("evidence_quote") or record["record_id"]
        cases.append(
            {
                "case_id": f"CASE{index:03d}",
                "source_id": record["source_id"],
                "case_title": title[:120],
                "case_topic": record.get("topic", ""),
                "category": metrics.get("category", ""),
                "case_metrics": metrics,
                "problem": metrics.get("ranking_problem") or record.get("condition", ""),
                "diagnostic_points": [],
                "related_rules": [],
                "evidence_quote": record.get("evidence_quote", ""),
                "confidence": "case_data",
            }
        )
    return cases


def attach_cases_and_diagnostics(
    merged_rules: list[dict[str, Any]],
    cases: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> None:
    """Attach related rules to cases and case sources to rules."""
    diagnostic_by_source: dict[str, list[str]] = defaultdict(list)
    for record in records:
        if record["record_type"] in {"diagnostic_hypothesis", "diagnostic_question"}:
            point = record.get("action") or record.get("condition") or record.get("reasoning")
            if point:
                diagnostic_by_source[record["source_id"]].append(point)

    for case in cases:
        case["diagnostic_points"] = unique_list(diagnostic_by_source.get(case["source_id"], []))[:10]
        related_rule_ids = []
        for rule in merged_rules:
            topic_match = rule["topic"] and rule["topic"] == case["case_topic"]
            metric_text = json.dumps(case.get("case_metrics", {}), ensure_ascii=False)
            tag_match = any(tag and tag in metric_text for tag in rule.get("tags", []))
            if topic_match or tag_match:
                related_rule_ids.append(rule["rule_id"])
                rule["case_sources"].append(
                    {
                        "case_id": case["case_id"],
                        "source_id": case["source_id"],
                        "evidence_quote": case["evidence_quote"],
                    }
                )
        case["related_rules"] = related_rule_ids[:20]

    for rule in merged_rules:
        rule["case_sources"] = unique_list(rule["case_sources"])


def markdown_counter(counter: Counter[str]) -> str:
    """Render a counter as Markdown bullets."""
    if not counter:
        return "- 无"
    return "\n".join(f"- {key}: {value}" for key, value in counter.most_common())


def write_report(
    path: Path,
    records: list[dict[str, Any]],
    normalized_records: list[dict[str, Any]],
    merged_rules: list[dict[str, Any]],
    cases: list[dict[str, Any]],
) -> None:
    """Write normalization report."""
    source_type_counts = Counter(record["record_type"] for record in records)
    topic_counts = Counter(rule["topic"] for rule in merged_rules if rule["topic"])
    confidence_counts = Counter(rule["confidence"] for rule in merged_rules)
    minority_views = sum(1 for rule in merged_rules if rule.get("minority_view"))
    comment_rule_sources = sum(1 for rule in merged_rules if rule.get("comment_signals"))
    lines = [
        "# Normalization Report",
        "",
        "## Summary",
        "",
        f"- input record 数: {len(records)}",
        f"- normalized record 数: {len(normalized_records)}",
        f"- merged rule 数: {len(merged_rules)}",
        f"- case_library 数: {len(cases)}",
        f"- executable_rule 输入数: {source_type_counts.get('executable_rule', 0)}",
        f"- diagnostic_hypothesis 输入数: {source_type_counts.get('diagnostic_hypothesis', 0)}",
        f"- case_observation 输入数: {source_type_counts.get('case_observation', 0)}",
        f"- irrelevant_noise 输入数: {source_type_counts.get('irrelevant_noise', 0)}",
        f"- comment-derived rule/candidate 数: {comment_rule_sources}",
        f"- minority_view 数: {minority_views}",
        "",
        "## Rule Topic Distribution",
        "",
        markdown_counter(topic_counts),
        "",
        "## Rule Confidence Distribution",
        "",
        markdown_counter(confidence_counts),
        "",
        "## Noise Handling",
        "",
        "- irrelevant_noise 未进入 merged_rules。",
        "- comment_signal 仅作为弱信号保留在 normalized_records，不进入规则库。",
        "- counterexample 进入 opposing_sources，不直接变成绝对规则。",
        "- 不同 metric_threshold 以原文阈值保留，不强行折叠成固定阈值。",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """Run record normalization."""
    args = parse_args()
    records = load_jsonl(args.input_file)
    normalized_records = [normalize_record(record) for record in records]
    merged_rules = build_rule_groups(records)
    attach_counterexamples(
        merged_rules,
        [record for record in records if record["record_type"] == "counterexample"],
    )
    cases = build_case_library(records)
    attach_cases_and_diagnostics(merged_rules, cases, records)

    write_jsonl(args.normalized_output, normalized_records)
    write_jsonl(args.rules_output, merged_rules)
    write_jsonl(args.cases_output, cases)
    write_report(args.report_output, records, normalized_records, merged_rules, cases)
    print(f"Wrote {len(normalized_records)} normalized records to {args.normalized_output}")
    print(f"Wrote {len(merged_rules)} merged rules to {args.rules_output}")
    print(f"Wrote {len(cases)} cases to {args.cases_output}")
    print(f"Wrote report to {args.report_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
