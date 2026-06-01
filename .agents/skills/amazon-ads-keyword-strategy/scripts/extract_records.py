"""Extract structured strategy records from article sections.

Input path: data/processed/amazon_ads_skill/article_sections.jsonl
Output path: data/processed/amazon_ads_skill/extracted_records.jsonl

CLI arguments:
  --input-file: JSONL section input path.
  --output / --output-file: JSONL extracted records path.
  --include-source-id: only extract records from a source id.
  --include-file-name: only extract records from a raw markdown file name.
  --limit: only process the first N source posts after filtering.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_INPUT_FILE = Path("data/processed/amazon_ads_skill/article_sections.jsonl")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/extracted_records.jsonl")
POST_TYPE = "case_post"

RECORD_FIELDS = [
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

POST_TYPES = {
    "tutorial_article",
    "question_post",
    "case_post",
    "discussion_post",
    "mixed",
    "unknown",
}
RECORD_TYPES = {
    "executable_rule",
    "case_observation",
    "diagnostic_hypothesis",
    "diagnostic_question",
    "counterexample",
    "comment_signal",
    "irrelevant_noise",
}
NOISE_REASONS = {
    "none",
    "account_invitation",
    "social_reply",
    "thanks_only",
    "off_topic",
    "too_short",
    "unreadable",
}
CONFIDENCE_VALUES = {"high", "medium", "low"}


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", type=Path, default=DEFAULT_INPUT_FILE)
    parser.add_argument(
        "--output",
        "--output-file",
        dest="output_file",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
    )
    parser.add_argument("--include-source-id", action="append", default=[])
    parser.add_argument("--include-file-name", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load JSONL objects from a file."""
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on {path}:{line_number}: {exc}") from exc
    return rows


def filter_sections(
    sections: list[dict[str, Any]],
    include_source_ids: list[str],
    include_file_names: list[str],
    limit: int | None,
) -> list[dict[str, Any]]:
    """Filter sections by source id, file name, and source-count limit."""
    selected = sections
    if include_source_ids:
        source_ids = set(include_source_ids)
        selected = [section for section in selected if section["source_id"] in source_ids]

    if include_file_names:
        file_names = {Path(file_name).name for file_name in include_file_names}
        selected = [
            section
            for section in selected
            if section["file_name"] in file_names
            or any(file_name in section["file_name"] for file_name in file_names)
        ]

    if limit is not None:
        if limit < 1:
            raise ValueError("--limit must be a positive integer")
        allowed_sources: list[str] = []
        for section in selected:
            source_id = section["source_id"]
            if source_id not in allowed_sources:
                allowed_sources.append(source_id)
            if len(allowed_sources) >= limit:
                break
        selected = [section for section in selected if section["source_id"] in allowed_sources]

    return selected


def group_sections_by_source(
    sections: list[dict[str, Any]],
) -> list[tuple[str, list[dict[str, Any]]]]:
    """Group sections by source id while preserving input order."""
    grouped: list[tuple[str, list[dict[str, Any]]]] = []
    index_by_source: dict[str, int] = {}
    for section in sections:
        source_id = section["source_id"]
        if source_id not in index_by_source:
            index_by_source[source_id] = len(grouped)
            grouped.append((source_id, []))
        grouped[index_by_source[source_id]][1].append(section)
    return grouped


def make_record(
    section: dict[str, Any],
    *,
    record_type: str,
    is_relevant: bool,
    noise_reason: str = "none",
    topic: str = "",
    product_stage: str = "unknown",
    ad_type: str = "unknown",
    match_type: str = "unknown",
    condition: str = "",
    action: str = "",
    metric_threshold: str = "",
    reasoning: str = "",
    case_metrics: dict[str, str] | None = None,
    evidence_quote: str = "",
    comment_signal: str = "none",
    confidence: str = "medium",
    limitations: str = "",
    contradiction_key: str = "",
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """Build one schema-complete extracted record."""
    return {
        "record_id": "",
        "source_id": section["source_id"],
        "section_id": section["section_id"],
        "post_type": POST_TYPE,
        "record_type": record_type,
        "section_role": section["section_role"],
        "is_relevant": is_relevant,
        "noise_reason": noise_reason,
        "topic": topic,
        "product_stage": product_stage,
        "ad_type": ad_type,
        "match_type": match_type,
        "condition": condition,
        "action": action,
        "metric_threshold": metric_threshold,
        "reasoning": reasoning,
        "case_metrics": case_metrics or {},
        "evidence_quote": evidence_quote,
        "comment_signal": comment_signal,
        "confidence": confidence,
        "limitations": limitations,
        "contradiction_key": contradiction_key,
        "tags": tags or [],
    }


def first_section_by_role(
    sections: list[dict[str, Any]],
    section_role: str,
) -> dict[str, Any] | None:
    """Find the first section with a role."""
    return next(
        (section for section in sections if section["section_role"] == section_role),
        None,
    )


def comment_section_by_index(
    sections: list[dict[str, Any]],
    comment_index: int,
) -> dict[str, Any] | None:
    """Find a comment section by comment index."""
    return next(
        (
            section
            for section in sections
            if section["section_role"] == "comment"
            and section.get("comment_index") == comment_index
        ),
        None,
    )


def extract_a017_records(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract the Phase 5 sample records from A017."""
    records: list[dict[str, Any]] = []
    author_body = first_section_by_role(sections, "author_body")
    author_update = first_section_by_role(sections, "author_update")
    comment_1 = comment_section_by_index(sections, 1)
    comment_2 = comment_section_by_index(sections, 2)
    comment_3 = comment_section_by_index(sections, 3)

    if author_body:
        records.append(
            make_record(
                author_body,
                record_type="case_observation",
                is_relevant=True,
                topic="ranking",
                product_stage="stable",
                ad_type="Sponsored Products",
                match_type="exact",
                condition="鞋类产品广告排名第一、ACOS 约 10%，但自然排名长期在 7 页开外。",
                metric_threshold=(
                    "ACOS 约 10%；广告转化率约 4%-5%；广告单占比 70%；"
                    "关键词份额 15%-20%；自然排名 7 页开外"
                ),
                reasoning=(
                    "广告数据好看、广告排名高和自然排名提升并未同步，案例需要从转化率、"
                    "点击质量、关键词容量和广告依赖继续诊断。"
                ),
                case_metrics={
                    "category": "鞋类",
                    "price": "$30",
                    "cpc": "约 $0.2",
                    "acos": "约 10%",
                    "cvr": "约 4%-5%",
                    "ad_order_share": "70%",
                    "daily_orders": "20-40 单",
                    "organic_rank": "7 页开外，始终无法进入前三页",
                    "ad_rank": "第一位",
                    "keyword_type": "精准中小词；关键词份额 15%-20%",
                    "ranking_problem": "广告数据好看，但自然排名无法进入前三页，且广告依赖严重",
                },
                evidence_quote=(
                    "鞋类产品，广告数据非常好看，售价$30,单点0.2刀，ACOS 10%左右，"
                    "转化率约4-5%，广告单占比70%，广告排名一直在第一位...自然排名一直很低，在7页开外"
                ),
                confidence="medium",
                limitations="单个卖家案例，缺少 CTR、自然流量、类目均值和竞品转化率对照。",
                contradiction_key="ad_rank_not_equal_organic_rank",
                tags=[
                    "shoe_category",
                    "low_acos",
                    "ad_dependency",
                    "organic_rank_stagnation",
                ],
            )
        )
        records.append(
            make_record(
                author_body,
                record_type="case_observation",
                is_relevant=True,
                topic="ranking",
                product_stage="new_launch",
                ad_type="Sponsored Products",
                match_type="unknown",
                condition="新产品日常 40-70 单、广告单占比 50% 以上，但关键词排名难进第一页。",
                metric_threshold="日常 40-70 单；广告单占比 50% 以上；关键词排名进入前 5 页但难进第一页",
                reasoning=(
                    "第二个产品同样出现广告依赖和自然排名推进困难，说明问题可能不是单一产品偶发。"
                ),
                case_metrics={
                    "cvr": "约 5%",
                    "ad_order_share": "50% 以上",
                    "daily_orders": "40-70 单",
                    "organic_rank": "进入前 5 页，但难进第一页",
                    "competitor_context": "同类竞品只有亚马逊自营压着",
                    "ranking_problem": "广告依赖严重，关键词排名进入前 5 页后仍无法推进到第一页",
                },
                evidence_quote=(
                    "今年又做了一款新产品，日常40-70单波动，也遇到了广告依赖症，"
                    "出单占比为50%以上，同类竞品只有亚马逊自营压着，关键词排名进入前5页"
                ),
                confidence="medium",
                limitations="缺少具体广告活动、关键词、CTR、CPC、ACOS 和自然转化数据。",
                contradiction_key="ad_orders_can_cannibalize_natural_orders",
                tags=["new_product", "ad_dependency", "ranking_bottleneck"],
            )
        )
        records.append(
            make_record(
                author_body,
                record_type="diagnostic_question",
                is_relevant=True,
                topic="conversion_listing",
                product_stage="unknown",
                ad_type="Sponsored Products",
                match_type="unknown",
                condition="两款产品转化率都约 5%，并且都存在广告依赖和自然排名推进困难。",
                action="检查转化率是否低于类目平均、竞品水平和自然排名推进所需水平。",
                metric_threshold="转化率约 5%",
                reasoning="提问者只是怀疑转化率是共同因素，当前证据不足以写成确定性规则。",
                evidence_quote="两款差不多都在5%左右...是否是因为这个因素导致的呢？",
                confidence="low",
                limitations="这是提问者疑问，不是已验证结论；需要类目平均 CVR、竞品 CVR、CTR 和流量结构数据。",
                tags=["conversion_question", "diagnostic_question"],
            )
        )

    if author_update:
        records.append(
            make_record(
                author_update,
                record_type="case_observation",
                is_relevant=True,
                topic="bidding_budget",
                product_stage="stable",
                ad_type="Sponsored Products",
                match_type="exact",
                condition="作者补充说明关键词 CPC 很低且广告花费基本每天花满。",
                metric_threshold="CPC 最低 $0.16；广告花费基本每天花满；关键词搜索量中等偏小",
                reasoning="作者将出单不多解释为关键词搜索量中等偏小，而不是广告没有花费。",
                case_metrics={
                    "cpc": "最低 $0.16",
                    "keyword_type": "搜索量中等偏小的词",
                    "ranking_problem": "花费基本每天花满，但出单不多",
                },
                evidence_quote="单点最低0.16，花费基本每天都是满的，出单不多是因为这几个关键词是搜索量中等偏小的词",
                confidence="medium",
                limitations="补充依赖图片证据但当前文本只保留描述；缺少截图中的详细点击、花费和订单数据。",
                tags=["author_update", "low_cpc", "budget_spent", "medium_small_keywords"],
            )
        )

    if comment_1:
        records.append(
            make_record(
                comment_1,
                record_type="irrelevant_noise",
                is_relevant=False,
                noise_reason="account_invitation",
                product_stage="unknown",
                ad_type="unknown",
                match_type="unknown",
                evidence_quote="想注册知无不言账号...不能邀请她，有人可以帮忙邀请一下吗",
                comment_signal="noise",
                confidence="low",
            )
        )

    if comment_2:
        records.append(
            make_record(
                comment_2,
                record_type="irrelevant_noise",
                is_relevant=False,
                noise_reason="social_reply",
                product_stage="unknown",
                ad_type="unknown",
                match_type="unknown",
                evidence_quote="@大涂小改: 好的",
                comment_signal="noise",
                confidence="low",
            )
        )

    if comment_3:
        records.append(
            make_record(
                comment_3,
                record_type="diagnostic_hypothesis",
                is_relevant=True,
                topic="data_diagnosis",
                product_stage="unknown",
                ad_type="Sponsored Products",
                match_type="unknown",
                condition="低 ACOS 但自然排名推不动，且 CPC 很低。",
                action="检查高峰期大词广告位置是否占优势，并检查广告 CTR。",
                metric_threshold="低 ACOS；低 CPC",
                reasoning="低 ACOS 可能来自 CPC 低，不代表转化率好；广告位置和 CTR 可能影响后续转化判断。",
                evidence_quote="你的Acos低，不是因为转化率好，而是因为cpc低...高峰期的时候，大词的广告位置在哪里...广告的点击率如何",
                comment_signal="alternative_explanation",
                confidence="medium",
                limitations="评论区诊断假设，缺少后台 CTR、分时位置和关键词报表验证，不能写成绝对规则。",
                contradiction_key="low_acos_not_enough_for_ranking",
                tags=["low_acos", "low_cpc", "ctr_check", "peak_position_check"],
            )
        )
        records.append(
            make_record(
                comment_3,
                record_type="diagnostic_hypothesis",
                is_relevant=True,
                topic="conversion_listing",
                product_stage="unknown",
                ad_type="Sponsored Products",
                match_type="unknown",
                condition="广告转化率看起来偏低，且作者怀疑转化率影响自然排名。",
                action="比较广告转化率、产品整体转化率和类目平均转化率，判断是否还有上升空间。",
                metric_threshold="广告转化率约 4%-5%；评论者推测产品转化率 16%~20%",
                reasoning="只看广告转化率不足以判断链接质量，需要放到产品整体和类目平均转化水平中比较。",
                evidence_quote="广告的转化率是产品的转化率的一半...这个转化率跟类目平均转化率相比，是否还有上升的空间",
                comment_signal="diagnostic_check",
                confidence="medium",
                limitations="评论者使用经验推测产品转化率，缺少后台 session、订单和类目基准验证。",
                tags=["cvr_check", "category_average", "listing_quality"],
            )
        )
        records.append(
            make_record(
                comment_3,
                record_type="diagnostic_hypothesis",
                is_relevant=True,
                topic="traffic_allocation",
                product_stage="stable",
                ad_type="Sponsored Products",
                match_type="unknown",
                condition="产品对广告依赖严重，需要寻找广告以外的流量来源。",
                action="评估是否可以每周提报秒杀等活动流量来积累产品权重。",
                metric_threshold="广告依赖严重",
                reasoning="评论者认为活动和广告都是重要流量来源，活动流量可能缓解单一广告依赖。",
                evidence_quote="活动和广告是产品流量的两大重要来源，产品对广告依赖严重，是否可考虑每周提报秒杀",
                comment_signal="actionable_advice",
                confidence="medium",
                limitations="评论建议未提供利润、库存、秒杀资格和活动效果数据，不能保证改善自然排名。",
                tags=["ad_dependency", "deal_traffic", "traffic_mix"],
            )
        )
        records.append(
            make_record(
                comment_3,
                record_type="diagnostic_hypothesis",
                is_relevant=True,
                topic="conversion_listing",
                product_stage="unknown",
                ad_type="Sponsored Products",
                match_type="unknown",
                condition="缺少广告点击、访问量和浏览量之间的关系数据。",
                action="检查广告点击、访问量、浏览量的数值关系，用于判断链接质量。",
                metric_threshold="广告点击相对访问量高很多",
                reasoning="如果广告点击显著高于访问量对应表现，可能说明链接质量或流量承接存在问题。",
                evidence_quote="看不到你的点击数量以及访问量和浏览量的数值联系...如果高很多，则说明你的链接质量有待提升",
                comment_signal="diagnostic_check",
                confidence="medium",
                limitations="评论区假设，需用业务报告验证点击、session、page view 和订单归因口径。",
                tags=["clicks_sessions_pageviews", "listing_quality", "data_check"],
            )
        )

    return records


def assign_record_ids(records: list[dict[str, Any]]) -> None:
    """Assign stable record ids per source."""
    counts_by_source: dict[str, int] = {}
    for record in records:
        source_id = record["source_id"]
        counts_by_source[source_id] = counts_by_source.get(source_id, 0) + 1
        record["record_id"] = f"{source_id}-R{counts_by_source[source_id]:03d}"


def validate_record(record: dict[str, Any]) -> None:
    """Validate the Phase 4 schema requirements used by Phase 5."""
    missing = [field for field in RECORD_FIELDS if field not in record]
    if missing:
        raise ValueError(f"{record.get('record_id', '<unassigned>')} missing fields: {missing}")
    if record["post_type"] not in POST_TYPES:
        raise ValueError(f"{record['record_id']} has invalid post_type: {record['post_type']}")
    if record["record_type"] not in RECORD_TYPES:
        raise ValueError(f"{record['record_id']} has invalid record_type: {record['record_type']}")
    if record["noise_reason"] not in NOISE_REASONS:
        raise ValueError(f"{record['record_id']} has invalid noise_reason: {record['noise_reason']}")
    if record["confidence"] not in CONFIDENCE_VALUES:
        raise ValueError(f"{record['record_id']} has invalid confidence: {record['confidence']}")
    if record["record_type"] == "irrelevant_noise":
        if record["is_relevant"]:
            raise ValueError(f"{record['record_id']} noise record must be irrelevant")
        if record["noise_reason"] == "none":
            raise ValueError(f"{record['record_id']} noise record needs a noise_reason")
    elif record["noise_reason"] != "none":
        raise ValueError(f"{record['record_id']} relevant record cannot have noise_reason")
    if record["record_type"] == "executable_rule":
        required = ["condition", "action", "reasoning", "limitations"]
        empty = [field for field in required if not record[field]]
        if empty:
            raise ValueError(f"{record['record_id']} executable_rule missing: {empty}")
    if record["section_role"] == "comment" and record["confidence"] == "high":
        raise ValueError(f"{record['record_id']} comment-derived confidence cannot be high")


def extract_records(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract records from selected sections."""
    records: list[dict[str, Any]] = []
    for _, source_sections in group_sections_by_source(sections):
        file_name = source_sections[0]["file_name"]
        source_id = source_sections[0]["source_id"]
        if source_id == "A017" or file_name.startswith("017_q31734_"):
            records.extend(extract_a017_records(source_sections))

    assign_record_ids(records)
    for record in records:
        validate_record(record)
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write records as JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> int:
    """Run record extraction."""
    args = parse_args()
    sections = load_jsonl(args.input_file)
    selected_sections = filter_sections(
        sections,
        args.include_source_id,
        args.include_file_name,
        args.limit,
    )
    records = extract_records(selected_sections)
    write_jsonl(args.output_file, records)
    print(f"Wrote {len(records)} records to {args.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
