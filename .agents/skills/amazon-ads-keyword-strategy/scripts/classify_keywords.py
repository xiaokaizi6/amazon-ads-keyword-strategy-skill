"""Classify Amazon keyword-library records.

Input path: optional JSONL or CSV keyword records.
Output path: optional JSONL classified keyword records.

CLI arguments:
  --input-file: JSONL or CSV input with keyword/search-term fields.
  --output-file: JSONL output path.
  --keyword: keyword text; can be passed multiple times.
  --product-stage: product stage used for classification context.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/classified_keywords.jsonl")

KEYWORD_TYPES = {
    "seed_keyword",
    "core_keyword",
    "core_long_tail",
    "long_tail",
    "competitor_keyword",
    "brand_keyword",
    "defensive_keyword",
    "attribute_keyword",
    "scenario_keyword",
    "seasonal_keyword",
    "ranking_target_keyword",
    "converting_keyword",
    "negative_candidate",
    "negative_exact",
    "negative_phrase",
    "risk_keyword",
}

STATUSES = {
    "unverified",
    "testing",
    "validated_converting",
    "ranking_target",
    "scale_word",
    "defensive_word",
    "negative_candidate",
    "negative_exact",
    "negative_phrase",
    "seasonal_word",
    "risk_word",
}

METRIC_FIELDS = [
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

KEYWORD_FIELD_ALIASES = [
    "keyword",
    "search_term",
    "customer_search_term",
    "customer search term",
    "query",
    "search query",
    "targeting",
    "target_keyword",
    "term",
]

METRIC_ALIASES = {
    "impressions": ["impressions", "impression", "展示", "曝光"],
    "clicks": ["clicks", "click", "点击"],
    "ctr": ["ctr", "点击率"],
    "cpc": ["cpc", "cost_per_click", "点击费用", "单次点击成本"],
    "orders": ["orders", "purchases", "units", "7 day total orders", "订单", "出单"],
    "cvr": ["cvr", "conversion_rate", "转化率"],
    "acos": ["acos", "advertising cost of sales", "广告销售成本比"],
    "tacos": ["tacos", "total acos"],
    "spend": ["spend", "cost", "花费", "广告花费"],
    "sales": ["sales", "revenue", "销售额", "广告销售额"],
    "organic_rank": ["organic_rank", "organic rank", "自然排名", "自然位"],
    "ad_rank": ["ad_rank", "ad rank", "广告排名", "广告位"],
}

COMPETITOR_HINTS = {
    "ninja",
    "creami",
    "cuisinart",
    "kitchenaid",
    "whynter",
    "nostalgia",
}
SEASONAL_HINTS = {
    "christmas",
    "halloween",
    "thanksgiving",
    "black friday",
    "prime day",
    "summer",
    "winter",
    "holiday",
    "easter",
}
RISK_HINTS = {"kids", "children", "child", "baby", "toddler", "toy", "safe for kids"}
ATTRIBUTE_HINTS = {
    "stainless",
    "electric",
    "manual",
    "mini",
    "portable",
    "commercial",
    "home",
}
PRODUCT_NOUN_HINTS = {"maker", "machine", "pan", "plate", "tool", "kit"}
SCENARIO_HINTS = {
    "party",
    "home",
    "kitchen",
    "dessert",
    "birthday",
    "family",
    "for",
    "maker for",
}


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", type=Path)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_FILE)
    parser.add_argument("--keyword", action="append", default=[])
    parser.add_argument("--product-stage", default="unknown")
    return parser.parse_args()


def normalize_keyword(keyword: str) -> str:
    """Normalize a keyword for dedupe and comparison."""
    normalized = keyword.strip().lower()
    normalized = re.sub(r"[\u2010-\u2015_/]+", " ", normalized)
    normalized = re.sub(r"[^\w\s]", " ", normalized, flags=re.UNICODE)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def parse_number(value: Any) -> float | None:
    """Parse numbers and percentages from common report formats."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"none", "null", "nan", "--", "-"}:
        return None
    text = text.replace(",", "").replace("$", "").replace("￥", "")
    is_percent = text.endswith("%")
    text = text.rstrip("%")
    try:
        number = float(text)
    except ValueError:
        return None
    if is_percent:
        return number / 100
    return number


def first_value(row: dict[str, Any], aliases: list[str]) -> Any:
    """Return the first matching value from a case-insensitive row."""
    lowered = {str(key).strip().lower(): value for key, value in row.items()}
    for alias in aliases:
        if alias.lower() in lowered:
            return lowered[alias.lower()]
    return None


def coerce_list(value: Any) -> list[str]:
    """Return a normalized list of strings."""
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        if stripped.startswith("["):
            try:
                loaded = json.loads(stripped)
            except json.JSONDecodeError:
                loaded = None
            if isinstance(loaded, list):
                return [str(item).strip() for item in loaded if str(item).strip()]
        return [part.strip() for part in re.split(r"[;,|]", stripped) if part.strip()]
    return [str(value).strip()]


def extract_keyword(row: dict[str, Any]) -> str:
    """Extract keyword text from common field names."""
    value = first_value(row, KEYWORD_FIELD_ALIASES)
    return str(value).strip() if value is not None else ""


def extract_metrics(row: dict[str, Any]) -> dict[str, float | None]:
    """Extract known metric fields from a row."""
    metrics = dict(row.get("metrics", {})) if isinstance(row.get("metrics"), dict) else {}
    output: dict[str, float | None] = {}
    for field in METRIC_FIELDS:
        value = metrics.get(field)
        if value is None:
            value = first_value(row, METRIC_ALIASES.get(field, [field]))
        output[field] = parse_number(value)
    return output


def level_from_number(
    value: float | None,
    low_cutoff: float,
    high_cutoff: float,
    *,
    unknown: str = "unknown",
) -> str:
    """Map a number to low/medium/high."""
    if value is None:
        return unknown
    if value >= high_cutoff:
        return "high"
    if value >= low_cutoff:
        return "medium"
    return "low"


def infer_source_type(record: dict[str, Any]) -> str:
    """Infer source type from record fields."""
    source_type = str(record.get("source_type") or "").strip()
    if source_type:
        return source_type
    source_detail = str(record.get("source_detail") or "").lower()
    if "search term" in source_detail or "搜索词" in source_detail:
        return "advertising_search_term_report"
    if "asin" in source_detail or "competitor" in source_detail or "竞品" in source_detail:
        return "competitor_reverse_lookup"
    if "comment" in source_detail or "评论" in source_detail:
        return "comment_signal"
    if "article" in source_detail or "文章" in source_detail:
        return "article_rule"
    return "manual_seed"


def infer_keyword_type(
    normalized: str,
    source_type: str,
    metrics: dict[str, float | None],
    record: dict[str, Any],
) -> tuple[str, list[str]]:
    """Infer keyword type and risk flags."""
    source_lower = source_type.lower()
    detail_lower = str(record.get("source_detail") or "").lower()
    risk_flags: list[str] = coerce_list(record.get("risk_flags"))
    explicit_type = str(record.get("keyword_type") or "").strip()
    if explicit_type in KEYWORD_TYPES:
        return explicit_type, risk_flags

    if "negative_phrase" in source_lower or str(record.get("status")) == "negative_phrase":
        return "negative_phrase", risk_flags
    if "negative_exact" in source_lower or str(record.get("status")) == "negative_exact":
        return "negative_exact", risk_flags
    if "negative" in source_lower or str(record.get("status")) == "negative_candidate":
        return "negative_candidate", risk_flags

    if any(term in normalized for term in RISK_HINTS):
        risk_flags.append("children_directed")
        return "risk_keyword", sorted(set(risk_flags))
    if any(term in normalized for term in SEASONAL_HINTS) or "season" in source_lower:
        return "seasonal_keyword", sorted(set(risk_flags))
    if "ranking" in source_lower or "rank" in detail_lower or record.get("ranking_priority") == "high":
        return "ranking_target_keyword", sorted(set(risk_flags))
    if (metrics.get("orders") or 0) > 0:
        return "converting_keyword", sorted(set(risk_flags))
    if "competitor" in source_lower or "asin" in source_lower:
        risk_flags.append("competitor_context")
        return "competitor_keyword", sorted(set(risk_flags))
    if any(term in normalized for term in COMPETITOR_HINTS):
        risk_flags.append("competitor_brand")
        return "competitor_keyword", sorted(set(risk_flags))
    if "brand" in source_lower:
        return "brand_keyword", sorted(set(risk_flags))
    if "defense" in source_lower or "防守" in detail_lower:
        return "defensive_keyword", sorted(set(risk_flags))
    token_count = len(normalized.split())
    if "ice cream" in normalized and any(term in normalized for term in PRODUCT_NOUN_HINTS):
        if token_count <= 5:
            return "core_long_tail", sorted(set(risk_flags))
        return "long_tail", sorted(set(risk_flags))
    if any(term in normalized for term in ATTRIBUTE_HINTS):
        return "attribute_keyword", sorted(set(risk_flags))
    if any(term in normalized for term in SCENARIO_HINTS):
        return "scenario_keyword", sorted(set(risk_flags))

    if token_count >= 4:
        return "long_tail", sorted(set(risk_flags))
    if token_count == 3:
        return "core_long_tail", sorted(set(risk_flags))
    if source_type == "manual_seed":
        return "seed_keyword", sorted(set(risk_flags))
    return "core_keyword", sorted(set(risk_flags))


def infer_status(
    keyword_type: str,
    metrics: dict[str, float | None],
    record: dict[str, Any],
) -> str:
    """Infer keyword workflow status."""
    explicit_status = str(record.get("status") or "").strip()
    if explicit_status in STATUSES:
        return explicit_status
    if keyword_type in {"negative_candidate", "negative_exact", "negative_phrase"}:
        return keyword_type
    if keyword_type == "risk_keyword":
        return "risk_word"
    if keyword_type == "seasonal_keyword":
        return "seasonal_word"
    if keyword_type == "ranking_target_keyword":
        return "ranking_target"
    if keyword_type == "converting_keyword":
        return "validated_converting"
    if keyword_type == "defensive_keyword":
        return "defensive_word"
    if (metrics.get("clicks") or 0) > 0:
        return "testing"
    return "unverified"


def infer_search_intent(keyword_type: str) -> str:
    """Infer coarse search intent from keyword type."""
    if keyword_type in {"brand_keyword", "defensive_keyword"}:
        return "brand"
    if keyword_type == "competitor_keyword":
        return "comparison"
    if keyword_type in {"negative_candidate", "negative_exact", "negative_phrase"}:
        return "unknown"
    if keyword_type == "risk_keyword":
        return "unknown"
    return "purchase"


def infer_priorities(
    keyword_type: str,
    metrics: dict[str, float | None],
    risk_flags: list[str],
) -> tuple[str, str]:
    """Infer ranking and ad priority."""
    if keyword_type in {"negative_candidate", "negative_exact", "negative_phrase", "risk_keyword"}:
        return "none", "low"
    if keyword_type == "ranking_target_keyword":
        return "high", "high"
    if keyword_type == "converting_keyword":
        return "medium", "high"
    if keyword_type in {"core_keyword", "core_long_tail"}:
        return "high", "high"
    if keyword_type in {"long_tail", "attribute_keyword", "scenario_keyword"}:
        return "medium", "medium"
    if keyword_type in {"competitor_keyword", "brand_keyword", "defensive_keyword"}:
        return "low", "medium"
    if (metrics.get("orders") or 0) > 0 and "low_relevance" not in risk_flags:
        return "medium", "high"
    return "low", "medium"


def infer_match_types(keyword_type: str) -> list[str]:
    """Infer recommended match types."""
    if keyword_type in {"negative_candidate", "negative_exact", "negative_phrase", "risk_keyword"}:
        return []
    if keyword_type == "competitor_keyword":
        return ["product_targeting", "exact"]
    if keyword_type in {"core_keyword", "core_long_tail", "ranking_target_keyword", "converting_keyword"}:
        return ["exact", "phrase"]
    if keyword_type in {"long_tail", "attribute_keyword", "scenario_keyword", "seasonal_keyword"}:
        return ["phrase", "broad"]
    return ["phrase"]


def infer_campaign(keyword_type: str, status: str) -> str:
    """Infer campaign recommendation."""
    if status in {"negative_candidate", "negative_exact", "negative_phrase"}:
        return "Do not scale; review for negative exact or negative phrase based on relevance and sample size."
    if keyword_type == "ranking_target_keyword":
        return "Use a dedicated rank-target exact campaign with natural-rank and TACOS review."
    if keyword_type == "converting_keyword":
        return "Move to manual exact or a controlled scaling campaign; review ACOS, CVR, and rank objective."
    if keyword_type == "competitor_keyword":
        return "Use isolated competitor keyword or ASIN campaign with separate budget and competitiveness check."
    if keyword_type == "seasonal_keyword":
        return "Use seasonal campaign with preheat, peak, and post-season budget windows."
    if keyword_type in {"core_keyword", "core_long_tail"}:
        return "Test in exact and phrase; isolate if it is a natural-rank target."
    if keyword_type in {"long_tail", "attribute_keyword", "scenario_keyword"}:
        return "Use phrase or low-budget broad discovery, then promote proven terms to exact."
    if keyword_type == "risk_keyword":
        return "Isolate or avoid until relevance, compliance, and conversion evidence are verified."
    return "Keep in keyword library as unverified; test only with controlled budget."


def negative_recommendation(keyword_type: str, metrics: dict[str, float | None]) -> str:
    """Infer negative match recommendation."""
    if keyword_type in {"negative_exact", "negative_phrase", "negative_candidate"}:
        return keyword_type
    if (metrics.get("clicks") or 0) >= 20 and (metrics.get("orders") or 0) == 0:
        return "negative_candidate"
    return ""


def classify_record(record: dict[str, Any], product_stage: str = "unknown") -> dict[str, Any]:
    """Classify and complete a keyword-library record."""
    keyword = str(record.get("keyword") or extract_keyword(record)).strip()
    if not keyword:
        raise ValueError("Keyword record has no keyword/search-term value.")

    normalized = normalize_keyword(str(record.get("normalized_keyword") or keyword))
    metrics = extract_metrics(record)
    source_type = infer_source_type(record)
    keyword_type, risk_flags = infer_keyword_type(normalized, source_type, metrics, record)
    status = infer_status(keyword_type, metrics, record)
    ranking_priority, ad_priority = infer_priorities(keyword_type, metrics, risk_flags)
    relevance_score = int(record.get("relevance_score") or 60)
    if keyword_type in {"negative_exact", "negative_phrase", "negative_candidate", "risk_keyword"}:
        relevance_score = min(relevance_score, 30)
    if keyword_type in {"core_keyword", "core_long_tail", "ranking_target_keyword"}:
        relevance_score = max(relevance_score, 80)
    if keyword_type == "converting_keyword":
        relevance_score = max(relevance_score, 70)
    if "low_relevance" in risk_flags:
        relevance_score = min(relevance_score, 35)

    negative_match = record.get("negative_match_recommendation") or negative_recommendation(
        keyword_type, metrics
    )
    return {
        "keyword_id": record.get("keyword_id", ""),
        "keyword": keyword,
        "normalized_keyword": normalized,
        "keyword_type": keyword_type,
        "source_type": source_type,
        "source_detail": str(record.get("source_detail") or source_type),
        "related_asins": coerce_list(record.get("related_asins")),
        "product_stage": str(record.get("product_stage") or product_stage),
        "search_intent": str(record.get("search_intent") or infer_search_intent(keyword_type)),
        "relevance_score": relevance_score,
        "traffic_level": str(
            record.get("traffic_level")
            or level_from_number(metrics.get("impressions"), 1000, 10000)
        ),
        "competition_level": str(
            record.get("competition_level") or level_from_number(metrics.get("cpc"), 0.5, 1.5)
        ),
        "cpc_level": str(record.get("cpc_level") or level_from_number(metrics.get("cpc"), 0.5, 1.5)),
        "conversion_potential": str(
            record.get("conversion_potential")
            or (
                "high"
                if (metrics.get("orders") or 0) > 0
                else "low"
                if (metrics.get("clicks") or 0) >= 20
                else "unknown"
            )
        ),
        "ranking_priority": str(record.get("ranking_priority") or ranking_priority),
        "ad_priority": str(record.get("ad_priority") or ad_priority),
        "match_type_recommendation": coerce_list(record.get("match_type_recommendation"))
        or infer_match_types(keyword_type),
        "campaign_recommendation": str(
            record.get("campaign_recommendation") or infer_campaign(keyword_type, status)
        ),
        "negative_match_recommendation": str(negative_match),
        "risk_flags": sorted(set(risk_flags)),
        "metrics": metrics,
        "status": status,
        "last_updated": str(record.get("last_updated") or datetime.now().date().isoformat()),
    }


def load_records(path: Path) -> list[dict[str, Any]]:
    """Load records from JSONL or CSV."""
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
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
    """Write records to JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> int:
    """Run keyword classification."""
    args = parse_args()
    records: list[dict[str, Any]] = []
    if args.input_file:
        records.extend(load_records(args.input_file))
    for keyword in args.keyword:
        records.append({"keyword": keyword, "source_type": "manual_seed"})

    classified = [
        classify_record(record, product_stage=args.product_stage)
        for record in records
        if extract_keyword(record) or record.get("keyword")
    ]
    for index, record in enumerate(classified, start=1):
        if not record["keyword_id"]:
            record["keyword_id"] = f"KW{index:06d}"
    write_jsonl(args.output_file, classified)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
