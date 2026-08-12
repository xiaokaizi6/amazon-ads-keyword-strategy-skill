"""Validate Amazon ads keyword strategy skill artifacts.

The script checks the skill folder, reference/example/eval artifacts, processed
JSONL outputs, and common quality constraints. It writes a Markdown report to:

  data/processed/amazon_ads_skill/validation_report.md
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_SKILL_DIR = Path(".agents/skills/amazon-ads-keyword-strategy")
DEFAULT_PROCESSED_DIR = Path("data/processed/amazon_ads_skill")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/validation_report.md")

MAX_EVIDENCE_QUOTE_CHARS = 240
MIN_EVAL_CASES = 35

REQUIRED_DIRS = [
    Path("."),
    Path("references"),
    Path("examples"),
    Path("evals"),
    Path("scripts"),
]

REQUIRED_SKILL_FILES = [
    Path("SKILL.md"),
    Path("references/01_taxonomy.md"),
    Path("references/02_extraction_schema.md"),
    Path("references/03_keyword_classification.md"),
    Path("references/04_campaign_structure.md"),
    Path("references/05_search_term_optimization.md"),
    Path("references/06_product_stage_strategy.md"),
    Path("references/07_conflict_register.md"),
    Path("references/08_metric_thresholds.md"),
    Path("references/09_case_library.md"),
    Path("references/10_noise_filter_rules.md"),
    Path("references/11_source_index.md"),
    Path("references/12_keyword_library_building.md"),
    Path("references/13_keyword_database_schema.md"),
    Path("references/14_source_validation_and_conflict_protocol.md"),
    Path("references/15_source_review_schema.md"),
    Path("examples/example_input_search_term_report.md"),
    Path("examples/example_output_ads_diagnosis.md"),
    Path("examples/example_output_keyword_strategy.md"),
    Path("examples/example_output_case_diagnosis.md"),
    Path("evals/test_cases.jsonl"),
    Path("evals/expected_outputs.md"),
    Path("scripts/build_keyword_library.py"),
    Path("scripts/build_rulebooks.py"),
    Path("scripts/build_case_library.py"),
    Path("scripts/classify_keywords.py"),
    Path("scripts/update_keyword_library_from_ads.py"),
    Path("scripts/validate_outputs.py"),
    Path("scripts/review_sources.py"),
]

REQUIRED_PROCESSED_FILES = [
    Path("extracted_records.jsonl"),
    Path("merged_rules.jsonl"),
    Path("case_library.jsonl"),
    Path("noise_comments.jsonl"),
    Path("conflict_candidates.jsonl"),
    Path("keyword_library.jsonl"),
    Path("keyword_library.csv"),
    Path("keyword_library_report.md"),
]

EXTRACTED_FIELDS = [
    "record_id",
    "source_id",
    "section_id",
    "post_type",
    "record_type",
    "section_role",
    "is_relevant",
    "noise_reason",
    "topic",
    "product_stage",
    "ad_type",
    "match_type",
    "condition",
    "action",
    "metric_threshold",
    "reasoning",
    "case_metrics",
    "evidence_quote",
    "comment_signal",
    "confidence",
    "limitations",
    "contradiction_key",
    "tags",
]

MERGED_RULE_FIELDS = [
    "rule_id",
    "topic",
    "product_stage",
    "ad_type",
    "match_type",
    "condition",
    "recommended_action",
    "metric_threshold",
    "reasoning",
    "supporting_sources",
    "opposing_sources",
    "case_sources",
    "comment_signals",
    "confidence",
    "limitations",
    "tags",
    "minority_view",
]

CASE_LIBRARY_FIELDS = [
    "case_id",
    "source_id",
    "case_title",
    "case_topic",
    "category",
    "case_metrics",
    "problem",
    "diagnostic_points",
    "related_rules",
    "evidence_quote",
    "confidence",
]

KEYWORD_LIBRARY_FIELDS = [
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

KEYWORD_METRIC_FIELDS = [
    "impressions",
    "clicks",
    "ctr",
    "cpc",
    "orders",
    "cvr",
    "acos",
    "tacos",
    "spend",
    "sales",
    "organic_rank",
    "ad_rank",
]

SOURCE_MANIFEST_FIELDS = [
    "source_id",
    "file_name",
    "file_path",
    "title",
    "author_or_org",
    "published_date",
    "acquired_date",
    "version",
    "source_type",
    "marketplace",
    "ad_products",
    "product_stages",
    "is_first_party",
    "evidence_cluster",
    "content_sha256",
    "byte_count",
    "extension",
    "readable",
    "readability_issues",
    "included_in_scope",
]

CLAIM_REVIEW_FIELDS = [
    "claim_id",
    "source_id",
    "source_location",
    "evidence_quote",
    "normalized_claim",
    "claim_type",
    "status",
    "confidence",
    "checked_source_ids",
    "supporting_evidence",
    "opposing_evidence",
    "missing_evidence",
    "verification_test",
    "reviewed_at",
    "validation_errors",
    "coverage",
]

CLAIM_STATUSES = {
    "supported",
    "confirmed_error",
    "outdated",
    "unsupported",
    "context_dependent",
    "disputed",
    "unresolved",
}

EVAL_FIELDS = [
    "case_id",
    "user_input",
    "expected_must_include",
    "expected_must_not_include",
    "related_reference_files",
    "difficulty",
]

OUTPUT_SECTIONS = [
    "当前诊断",
    "数据完整性检查",
    "产品阶段判断",
    "关键词分类",
    "广告结构诊断",
    "搜索词动作表",
    "竞价和预算调整",
    "自然排名与广告关系判断",
    "案例相似性提示",
    "风险和例外",
    "7 天 / 14 天 / 30 天行动计划",
]

EXAMPLE_COVERAGE_PHRASES = [
    "新品期广告结构规划",
    "搜索词报告优化",
    "ACOS 高但可能在推自然排名",
    "ACOS 低但自然排名不提升",
    "广告单占比高",
]

T009_REQUIRED_MUST_INCLUDE = [
    "不能只看 ACOS",
    "要检查 CPC 是否过低",
    "要检查广告位和 CTR",
    "要检查广告出单词和自然排名目标词是否一致",
    "要检查整体 CVR / Session / Unit Session Percentage",
    "要提示广告依赖风险",
]

T009_REQUIRED_MUST_NOT_INCLUDE = [
    "直接说广告效果很好不用调整",
    "直接说低 ACOS 一定能推自然排名",
    "直接建议关闭广告",
]


@dataclass(frozen=True)
class Issue:
    severity: str
    file: str
    line: int | str
    field: str
    reason: str
    suggestion: str


class Validator:
    def __init__(self, skill_dir: Path, processed_dir: Path, output_file: Path) -> None:
        self.skill_dir = skill_dir
        self.processed_dir = processed_dir
        self.output_file = output_file
        self.issues: list[Issue] = []
        self.checks: list[tuple[str, str]] = []
        self.jsonl_cache: dict[Path, list[tuple[int, dict[str, Any]]]] = {}

    def run(self) -> int:
        self.check_required_dirs()
        self.check_required_files()
        self.check_skill_frontmatter()
        self.check_jsonl_files()
        self.check_processed_schemas()
        self.check_keyword_library_schema()
        self.check_noise_and_comment_rules()
        self.check_eval_files()
        self.check_references()
        self.check_examples()
        self.check_source_review_artifacts()
        self.write_report()
        return 1 if self.has_errors else 0

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == "error" for issue in self.issues)

    def add_issue(
        self,
        severity: str,
        file: Path | str,
        line: int | str,
        field: str,
        reason: str,
        suggestion: str,
    ) -> None:
        self.issues.append(
            Issue(severity, self.display_path(file), line, field, reason, suggestion)
        )

    def add_check(self, name: str, status: str) -> None:
        self.checks.append((name, status))

    def display_path(self, path: Path | str) -> str:
        path_obj = Path(path)
        try:
            return path_obj.resolve().relative_to(Path.cwd().resolve()).as_posix()
        except ValueError:
            return path_obj.as_posix()

    def skill_path(self, relative: Path) -> Path:
        return self.skill_dir / relative

    def processed_path(self, relative: Path) -> Path:
        return self.processed_dir / relative

    def check_required_dirs(self) -> None:
        ok = True
        for relative in REQUIRED_DIRS:
            path = self.skill_path(relative)
            if not path.is_dir():
                ok = False
                self.add_issue(
                    "error",
                    path,
                    "-",
                    "__directory__",
                    "Required directory does not exist.",
                    "Create the directory with the expected skill artifact contents.",
                )
        if not self.processed_dir.is_dir():
            ok = False
            self.add_issue(
                "error",
                self.processed_dir,
                "-",
                "__directory__",
                "Processed output directory does not exist.",
                "Run the extraction/build scripts or create the processed output directory.",
            )
        self.add_check("required directories", "pass" if ok else "fail")

    def check_required_files(self) -> None:
        ok = True
        for relative in REQUIRED_SKILL_FILES:
            path = self.skill_path(relative)
            if not path.is_file():
                ok = False
                self.add_issue(
                    "error",
                    path,
                    "-",
                    "__file__",
                    "Required skill file does not exist.",
                    "Create the file or restore it in the expected location.",
                )
        for relative in REQUIRED_PROCESSED_FILES:
            path = self.processed_path(relative)
            if not path.is_file():
                ok = False
                self.add_issue(
                    "error",
                    path,
                    "-",
                    "__file__",
                    "Required processed JSONL file does not exist.",
                    "Run the upstream generation script that produces this JSONL file.",
                )
        self.add_check("required files", "pass" if ok else "fail")

    def check_skill_frontmatter(self) -> None:
        path = self.skill_path(Path("SKILL.md"))
        if not path.is_file():
            self.add_check("SKILL.md frontmatter", "fail")
            return

        text = path.read_text(encoding="utf-8")
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
        if not frontmatter_match:
            self.add_issue(
                "error",
                path,
                1,
                "frontmatter",
                "SKILL.md does not start with YAML frontmatter.",
                "Add frontmatter containing name and description.",
            )
            self.add_check("SKILL.md frontmatter", "fail")
            return

        frontmatter = frontmatter_match.group(1)
        parsed: dict[str, str] = {}
        for line_no, line in enumerate(frontmatter.splitlines(), start=2):
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            parsed[key.strip()] = value.strip()
            if key.strip() in {"name", "description"} and not value.strip():
                self.add_issue(
                    "error",
                    path,
                    line_no,
                    key.strip(),
                    "Required frontmatter field is empty.",
                    "Fill the field with a concise value.",
                )

        for field in ("name", "description"):
            if field not in parsed:
                self.add_issue(
                    "error",
                    path,
                    1,
                    field,
                    "Required frontmatter field is missing.",
                    "Add this field to SKILL.md frontmatter.",
                )
        self.add_check(
            "SKILL.md frontmatter",
            "pass" if not any(i.file == self.display_path(path) for i in self.issues) else "fail",
        )

    def check_jsonl_files(self) -> None:
        jsonl_files = list(self.processed_dir.glob("*.jsonl"))
        test_cases = self.skill_path(Path("evals/test_cases.jsonl"))
        if test_cases.is_file():
            jsonl_files.append(test_cases)

        ok = True
        for path in sorted(set(jsonl_files)):
            records = self.read_jsonl(path)
            if any(
                issue.file == self.display_path(path) and issue.field == "__json__"
                for issue in self.issues
            ):
                ok = False
            if path.is_file() and not records:
                ok = False
                self.add_issue(
                    "error",
                    path,
                    "-",
                    "__jsonl__",
                    "JSONL file contains no records.",
                    "Add valid JSON objects, one per line.",
                )
        self.add_check("JSONL legality", "pass" if ok else "fail")

    def read_jsonl(self, path: Path) -> list[tuple[int, dict[str, Any]]]:
        if path in self.jsonl_cache:
            return self.jsonl_cache[path]

        records: list[tuple[int, dict[str, Any]]] = []
        if not path.is_file():
            self.jsonl_cache[path] = records
            return records

        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    self.add_issue(
                        "warning",
                        path,
                        line_no,
                        "__jsonl__",
                        "Blank line in JSONL file.",
                        "Remove blank lines; JSONL should have one JSON object per line.",
                    )
                    continue
                try:
                    value = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        "__json__",
                        f"Invalid JSON: {exc.msg}.",
                        "Fix the line so it is a complete JSON object.",
                    )
                    continue
                if not isinstance(value, dict):
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        "__json__",
                        "JSONL record is not an object.",
                        "Use a JSON object for each line.",
                    )
                    continue
                records.append((line_no, value))
        self.jsonl_cache[path] = records
        return records

    def check_processed_schemas(self) -> None:
        checks = [
            (self.processed_path(Path("extracted_records.jsonl")), EXTRACTED_FIELDS),
            (self.processed_path(Path("noise_comments.jsonl")), EXTRACTED_FIELDS),
            (self.processed_path(Path("merged_rules.jsonl")), MERGED_RULE_FIELDS),
            (self.processed_path(Path("case_library.jsonl")), CASE_LIBRARY_FIELDS),
            (self.processed_path(Path("keyword_library.jsonl")), KEYWORD_LIBRARY_FIELDS),
        ]

        ok = True
        for path, required_fields in checks:
            for line_no, record in self.read_jsonl(path):
                missing = [field for field in required_fields if field not in record]
                for field in missing:
                    ok = False
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        field,
                        "Required field is missing.",
                        "Regenerate or patch the JSONL record with the required field.",
                    )
                self.check_evidence_quotes(path, line_no, record)
        self.add_check("processed schema fields", "pass" if ok else "fail")

    def check_keyword_library_schema(self) -> None:
        path = self.processed_path(Path("keyword_library.jsonl"))
        records = self.read_jsonl(path)
        ok = True
        seen_keywords: set[str] = set()
        for line_no, record in records:
            normalized = record.get("normalized_keyword")
            if not isinstance(normalized, str) or not normalized:
                ok = False
                self.add_issue(
                    "error",
                    path,
                    line_no,
                    "normalized_keyword",
                    "Keyword record has no normalized keyword.",
                    "Set normalized_keyword so dedupe and updates work.",
                )
            elif normalized in seen_keywords:
                ok = False
                self.add_issue(
                    "error",
                    path,
                    line_no,
                    "normalized_keyword",
                    "Duplicate normalized keyword.",
                    "Merge duplicate keyword rows into one library record.",
                )
            else:
                seen_keywords.add(normalized)

            metrics = record.get("metrics")
            if not isinstance(metrics, dict):
                ok = False
                self.add_issue(
                    "error",
                    path,
                    line_no,
                    "metrics",
                    "Keyword metrics field is not an object.",
                    "Store metrics as an object with required metric keys.",
                )
                continue
            for field in KEYWORD_METRIC_FIELDS:
                if field not in metrics:
                    ok = False
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        f"metrics.{field}",
                        "Required keyword metric field is missing.",
                        "Add the metric key and use null when data is unavailable.",
                    )
        self.add_check("keyword library schema", "pass" if ok else "fail")

    def check_evidence_quotes(
        self, path: Path, line_no: int, value: Any, field_path: str = ""
    ) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{field_path}.{key}" if field_path else key
                if key == "evidence_quote":
                    if not isinstance(child, str):
                        self.add_issue(
                            "error",
                            path,
                            line_no,
                            child_path,
                            "evidence_quote must be a string.",
                            "Store evidence_quote as a short source excerpt string.",
                        )
                    elif len(child) > MAX_EVIDENCE_QUOTE_CHARS:
                        self.add_issue(
                            "error",
                            path,
                            line_no,
                            child_path,
                            f"evidence_quote is too long ({len(child)} chars).",
                            f"Shorten evidence_quote to {MAX_EVIDENCE_QUOTE_CHARS} chars or less.",
                        )
                self.check_evidence_quotes(path, line_no, child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                child_path = f"{field_path}[{index}]"
                self.check_evidence_quotes(path, line_no, child, child_path)

    def check_noise_and_comment_rules(self) -> None:
        ok = True
        extracted_paths = [
            self.processed_path(Path("extracted_records.jsonl")),
            self.processed_path(Path("noise_comments.jsonl")),
        ]
        noise_record_ids: set[str] = set()

        for path in extracted_paths:
            for line_no, record in self.read_jsonl(path):
                if record.get("record_type") == "irrelevant_noise" or record.get("is_relevant") is False:
                    record_id = record.get("record_id")
                    if isinstance(record_id, str) and record_id:
                        noise_record_ids.add(record_id)
                    if record.get("record_type") == "irrelevant_noise":
                        if record.get("is_relevant") is not False:
                            ok = False
                            self.add_issue(
                                "error",
                                path,
                                line_no,
                                "is_relevant",
                                "irrelevant_noise record is marked relevant.",
                                "Set is_relevant to false for irrelevant_noise records.",
                            )
                        if record.get("noise_reason") in {"", "none", None}:
                            ok = False
                            self.add_issue(
                                "error",
                                path,
                                line_no,
                                "noise_reason",
                                "irrelevant_noise record has no noise reason.",
                                "Set noise_reason to account_invitation, too_short, off_topic, or another allowed value.",
                            )
                if record.get("section_role") == "comment" and record.get("confidence") == "high":
                    ok = False
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        "confidence",
                        "Comment-derived record is high confidence.",
                        "Lower comment-derived confidence to medium or low unless independently verified.",
                    )

        merged_path = self.processed_path(Path("merged_rules.jsonl"))
        for line_no, rule in self.read_jsonl(merged_path):
            for field in ("supporting_sources", "opposing_sources", "comment_signals", "minority_view"):
                sources = rule.get(field, [])
                if not isinstance(sources, list):
                    ok = False
                    self.add_issue(
                        "error",
                        merged_path,
                        line_no,
                        field,
                        "Rule source field is not a list.",
                        "Store source references as an array of objects.",
                    )
                    continue
                for index, source in enumerate(sources):
                    if not isinstance(source, dict):
                        continue
                    record_id = source.get("record_id")
                    if record_id in noise_record_ids or source.get("record_type") == "irrelevant_noise":
                        ok = False
                        self.add_issue(
                            "error",
                            merged_path,
                            line_no,
                            f"{field}[{index}]",
                            "irrelevant_noise record entered the rule library.",
                            "Remove this source from merged_rules.jsonl and keep it in noise audit files only.",
                        )
                    if source.get("section_role") == "comment" and source.get("confidence") == "high":
                        ok = False
                        self.add_issue(
                            "error",
                            merged_path,
                            line_no,
                            f"{field}[{index}].confidence",
                            "Comment source is high confidence inside a merged rule.",
                            "Lower the confidence or add non-comment evidence before treating it as strong support.",
                        )

            noisy_text = " ".join(
                str(rule.get(field, ""))
                for field in ("condition", "recommended_action", "reasoning")
            )
            if "register?code" in noisy_text or "私信" in noisy_text and len(noisy_text) < 80:
                ok = False
                self.add_issue(
                    "error",
                    merged_path,
                    line_no,
                    "condition/recommended_action",
                    "Rule text appears to contain promotional or social noise.",
                    "Move irrelevant social or promotional content out of the rule library.",
                )
        self.add_check("noise and comment confidence", "pass" if ok else "fail")

    def check_eval_files(self) -> None:
        ok = True
        path = self.skill_path(Path("evals/test_cases.jsonl"))
        records = self.read_jsonl(path)
        if len(records) < MIN_EVAL_CASES:
            ok = False
            self.add_issue(
                "error",
                path,
                "-",
                "__count__",
                f"Eval set has {len(records)} cases; at least {MIN_EVAL_CASES} are required.",
                "Add more test cases covering the required scenario list.",
            )

        seen_ids: set[str] = set()
        t009: dict[str, Any] | None = None
        for line_no, record in records:
            for field in EVAL_FIELDS:
                if field not in record:
                    ok = False
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        field,
                        "Required eval field is missing.",
                        "Add the field to the test case object.",
                    )
            case_id = record.get("case_id")
            if isinstance(case_id, str):
                if case_id in seen_ids:
                    ok = False
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        "case_id",
                        "Duplicate case_id.",
                        "Use a unique case_id for each eval case.",
                    )
                seen_ids.add(case_id)
                if case_id == "T009":
                    t009 = record
            for array_field in (
                "expected_must_include",
                "expected_must_not_include",
                "related_reference_files",
            ):
                if array_field in record and not isinstance(record[array_field], list):
                    ok = False
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        array_field,
                        "Eval field must be an array.",
                        "Use a JSON array for this field.",
                    )
            for ref in record.get("related_reference_files", []):
                if isinstance(ref, str) and not self.skill_path(Path(ref)).is_file():
                    ok = False
                    self.add_issue(
                        "error",
                        path,
                        line_no,
                        "related_reference_files",
                        f"Referenced file does not exist: {ref}.",
                        "Use a valid reference path relative to the skill directory.",
                    )

        if t009 is None:
            ok = False
            self.add_issue(
                "error",
                path,
                "-",
                "case_id",
                "Dedicated low-ACOS regression case T009 is missing.",
                "Add T009 with the required low-ACOS / high-ad-share expectations.",
            )
        else:
            self.check_expected_terms(
                path,
                "T009",
                t009.get("expected_must_include", []),
                T009_REQUIRED_MUST_INCLUDE,
                "expected_must_include",
            )
            self.check_expected_terms(
                path,
                "T009",
                t009.get("expected_must_not_include", []),
                T009_REQUIRED_MUST_NOT_INCLUDE,
                "expected_must_not_include",
            )
            if any(
                issue.file == self.display_path(path)
                and issue.line == "T009"
                and issue.severity == "error"
                for issue in self.issues
            ):
                ok = False

        expected_path = self.skill_path(Path("evals/expected_outputs.md"))
        if expected_path.is_file():
            text = expected_path.read_text(encoding="utf-8")
            for phrase in T009_REQUIRED_MUST_INCLUDE + T009_REQUIRED_MUST_NOT_INCLUDE:
                if phrase not in text:
                    ok = False
                    self.add_issue(
                        "error",
                        expected_path,
                        "-",
                        "content",
                        f"Expected outputs guide is missing required phrase: {phrase}.",
                        "Add the phrase to the dedicated regression section.",
                    )
        self.add_check("eval set", "pass" if ok else "fail")

    def check_expected_terms(
        self,
        path: Path,
        line: int | str,
        actual_terms: Any,
        required_terms: list[str],
        field: str,
    ) -> None:
        if not isinstance(actual_terms, list):
            self.add_issue(
                "error",
                path,
                line,
                field,
                "Expected terms field is not an array.",
                "Use a JSON array of strings.",
            )
            return
        missing = [term for term in required_terms if term not in actual_terms]
        for term in missing:
            self.add_issue(
                "error",
                path,
                line,
                field,
                f"Required regression expectation is missing: {term}.",
                "Add this exact phrase to the T009 expectation list.",
            )

    def check_references(self) -> None:
        ok = True
        references_dir = self.skill_path(Path("references"))
        reference_files = sorted(references_dir.glob("*.md")) if references_dir.is_dir() else []
        if not reference_files:
            ok = False
            self.add_issue(
                "error",
                references_dir,
                "-",
                "__directory__",
                "References directory has no Markdown files.",
                "Add reference Markdown files used by SKILL.md.",
            )
        for path in reference_files:
            if path.stat().st_size == 0:
                ok = False
                self.add_issue(
                    "error",
                    path,
                    "-",
                    "__file__",
                    "Reference file is empty.",
                    "Fill the reference file or remove it from the skill map.",
                )
        self.add_check("references non-empty", "pass" if ok else "fail")

    def check_examples(self) -> None:
        ok = True
        examples_dir = self.skill_path(Path("examples"))
        example_files = sorted(examples_dir.glob("*.md")) if examples_dir.is_dir() else []
        combined_text = ""
        for path in example_files:
            text = path.read_text(encoding="utf-8")
            combined_text += "\n" + text
            if not text.strip():
                ok = False
                self.add_issue(
                    "error",
                    path,
                    "-",
                    "__file__",
                    "Example file is empty.",
                    "Add a reusable example.",
                )
        for phrase in EXAMPLE_COVERAGE_PHRASES:
            if phrase not in combined_text:
                ok = False
                self.add_issue(
                    "error",
                    examples_dir,
                    "-",
                    "coverage",
                    f"Examples do not cover required scenario phrase: {phrase}.",
                    "Add the scenario to an example input or output file.",
                )

        for relative in (
            Path("examples/example_output_ads_diagnosis.md"),
            Path("examples/example_output_keyword_strategy.md"),
            Path("examples/example_output_case_diagnosis.md"),
        ):
            path = self.skill_path(relative)
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for section in OUTPUT_SECTIONS:
                if section not in text:
                    ok = False
                    self.add_issue(
                        "error",
                        path,
                        "-",
                        "output_format",
                        f"Output example is missing required section: {section}.",
                        "Use the full 11-section output format from SKILL.md.",
                    )
        self.add_check("examples format and coverage", "pass" if ok else "fail")

    def check_source_review_artifacts(self) -> None:
        """Validate optional source-review outputs when a review has been run."""
        manifest_path = self.processed_path(Path("source_manifest.jsonl"))
        claim_path = self.processed_path(Path("claim_review.jsonl"))
        report_path = self.processed_path(Path("source_validation_report.md"))
        if not manifest_path.exists() and not claim_path.exists() and not report_path.exists():
            self.add_check("source review artifacts", "not run")
            return

        ok = True
        manifest_records = self.read_jsonl(manifest_path)
        manifest_ids: set[str] = set()
        if not manifest_path.is_file():
            ok = False
            self.add_issue(
                "error",
                manifest_path,
                "-",
                "__file__",
                "Claim/source review artifacts exist without source_manifest.jsonl.",
                "Run review_sources.py to create a source manifest first.",
            )
        for line_no, record in manifest_records:
            missing = [field for field in SOURCE_MANIFEST_FIELDS if field not in record]
            if missing:
                ok = False
                self.add_issue(
                    "error",
                    manifest_path,
                    line_no,
                    "fields",
                    f"Source manifest record is missing fields: {', '.join(missing)}.",
                    "Regenerate the manifest with review_sources.py.",
                )
            source_id = record.get("source_id")
            if not isinstance(source_id, str) or not source_id:
                ok = False
                self.add_issue(
                    "error",
                    manifest_path,
                    line_no,
                    "source_id",
                    "Source manifest source_id must be a non-empty string.",
                    "Use a stable source ID generated from path and content hash.",
                )
            elif source_id in manifest_ids:
                ok = False
                self.add_issue(
                    "error",
                    manifest_path,
                    line_no,
                    "source_id",
                    "Duplicate source_id in source manifest.",
                    "Deduplicate source records while retaining evidence_cluster.",
                )
            else:
                manifest_ids.add(source_id)

        if claim_path.is_file():
            if not report_path.is_file():
                ok = False
                self.add_issue(
                    "error",
                    report_path,
                    "-",
                    "__file__",
                    "claim_review.jsonl exists without source_validation_report.md.",
                    "Generate the coverage report with review_sources.py.",
                )
            for line_no, claim in self.read_jsonl(claim_path):
                missing = [field for field in CLAIM_REVIEW_FIELDS if field not in claim]
                if missing:
                    ok = False
                    self.add_issue(
                        "error",
                        claim_path,
                        line_no,
                        "fields",
                        f"Claim review record is missing fields: {', '.join(missing)}.",
                        "Regenerate claim reviews with the documented claim schema.",
                    )
                if claim.get("source_id") not in manifest_ids:
                    ok = False
                    self.add_issue(
                        "error",
                        claim_path,
                        line_no,
                        "source_id",
                        "Claim references a source not present in source_manifest.jsonl.",
                        "Add the source to the manifest or correct the claim source_id.",
                    )
                if claim.get("status") not in CLAIM_STATUSES:
                    ok = False
                    self.add_issue(
                        "error",
                        claim_path,
                        line_no,
                        "status",
                        "Claim review has an invalid status.",
                        "Use one of the documented source-review statuses.",
                    )
                if claim.get("status") == "confirmed_error":
                    if not claim.get("opposing_evidence") or not claim.get("verification_test"):
                        ok = False
                        self.add_issue(
                            "error",
                            claim_path,
                            line_no,
                            "confirmed_error",
                            "confirmed_error lacks direct opposing evidence or a verification test.",
                            "Downgrade the status or add the required evidence fields.",
                        )
        elif report_path.is_file():
            self.add_issue(
                "warning",
                report_path,
                "-",
                "claim_review",
                "Source report exists without claim_review.jsonl; this can be valid NOT_READY state.",
                "Supply atomic claims when claim-level review is ready.",
            )
        self.add_check("source review artifacts", "pass" if ok else "fail")

    def write_report(self) -> None:
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        errors = [issue for issue in self.issues if issue.severity == "error"]
        warnings = [issue for issue in self.issues if issue.severity == "warning"]
        status = "FAIL" if errors else "PASS"

        lines = [
            "# Amazon Ads Skill Validation Report",
            "",
            f"- Generated at: {datetime.now().isoformat(timespec='seconds')}",
            f"- Skill directory: `{self.display_path(self.skill_dir)}`",
            f"- Processed directory: `{self.display_path(self.processed_dir)}`",
            f"- Status: **{status}**",
            f"- Errors: {len(errors)}",
            f"- Warnings: {len(warnings)}",
            "",
            "## Checks",
            "",
            "| Check | Status |",
            "| --- | --- |",
        ]
        lines.extend(f"| {name} | {status} |" for name, status in self.checks)

        lines.extend(["", "## Issues", ""])
        if not self.issues:
            lines.append("No blocking errors or warnings found.")
        else:
            lines.extend(
                [
                    "| Severity | File | Line | Field | Error reason | Fix suggestion |",
                    "| --- | --- | --- | --- | --- | --- |",
                ]
            )
            for issue in self.issues:
                lines.append(
                    "| {severity} | `{file}` | {line} | `{field}` | {reason} | {suggestion} |".format(
                        severity=issue.severity,
                        file=issue.file,
                        line=issue.line,
                        field=issue.field,
                        reason=issue.reason.replace("|", "\\|"),
                        suggestion=issue.suggestion.replace("|", "\\|"),
                    )
                )

        self.output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_FILE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return Validator(args.skill_dir, args.processed_dir, args.output_file).run()


if __name__ == "__main__":
    raise SystemExit(main())
