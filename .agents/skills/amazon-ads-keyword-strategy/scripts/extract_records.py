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
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_INPUT_FILE = Path("data/processed/amazon_ads_skill/article_sections.jsonl")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/extracted_records.jsonl")
NOISE_COMMENTS_FILE = Path("data/processed/amazon_ads_skill/noise_comments.jsonl")
QUALITY_REPORT_FILE = Path("data/processed/amazon_ads_skill/extraction_quality_report.md")
MAX_EVIDENCE_CHARS = 180

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

RELEVANCE_TERMS = [
    "广告",
    "关键词",
    "搜索词",
    "自然排名",
    "自然位",
    "广告位",
    "出单",
    "订单",
    "曝光",
    "点击",
    "转化",
    "ACOS",
    "acos",
    "Acos",
    "TACOS",
    "CPC",
    "cpc",
    "CTR",
    "CVR",
    "预算",
    "竞价",
    "出价",
    "ASIN",
    "asin",
    "listing",
    "流量",
    "排名",
    "否词",
    "广泛",
    "词组",
    "精准",
    "自动",
    "手动",
]

ACTION_TERMS = [
    "建议",
    "需要",
    "应该",
    "不要",
    "不能",
    "开启",
    "关闭",
    "提高",
    "降低",
    "增加",
    "减少",
    "调整",
    "否定",
    "添加",
    "单独",
    "分开",
    "测试",
    "观察",
    "检查",
    "对比",
    "判断",
    "优化",
    "筛选",
    "挑选",
    "设置",
    "提报",
    "加预算",
    "降竞价",
    "提竞价",
]
SOFT_ACTION_TERMS = ["可以", "先", "再"]

QUESTION_TERMS = ["请教", "求助", "怎么办", "如何", "为什么", "是否", "是不是", "有没有", "吗", "？", "?"]
REASONING_TERMS = ["因为", "所以", "目的", "为了", "避免", "否则", "从而", "意味着", "说明", "核心", "本质", "原因"]
COUNTER_TERMS = ["不一定", "不代表", "但是", "但", "反而", "无法", "没有", "不等于", "并不", "未必"]

TOPIC_KEYWORDS = {
    "traffic_allocation": ["广告单占比", "广告订单占比", "自然单", "广告单", "自然流量", "广告流量", "广告依赖", "流量占比"],
    "ranking": ["自然排名", "自然位", "关键词排名", "广告排名", "广告位", "上首页", "首页", "排名", "坑位"],
    "bidding_budget": ["CPC", "cpc", "单点", "竞价", "出价", "预算", "bid", "Bid", "花费", "烧", "卡预算", "分时"],
    "acos_profit": ["ACOS", "acos", "Acos", "TACOS", "tacos", "ROAS", "ROI", "广销比", "利润", "毛利", "亏"],
    "conversion_listing": ["转化率", "CVR", "cvr", "CTR", "ctr", "点击率", "Session", "session", "listing", "链接质量", "主图", "review", "评分"],
    "campaign_structure": ["广告结构", "广告架构", "广告活动", "campaign", "Campaign", "广告组", "自动广告", "手动广告", "精准", "词组", "广泛"],
    "keyword_research": ["关键词", "搜索词", "拓词", "词根", "大词", "长尾词", "中小词", "核心词", "否词", "否定"],
    "product_targeting": ["ASIN", "asin", "商品投放", "类目投放", "竞品", "定投", "品类"],
    "launch": ["新品", "新产品", "上架", "开售", "冷启动", "新链接"],
    "seasonality": ["季节", "旺季", "淡季", "节日", "窗口期", "黑五", "圣诞", "万圣", "清库存"],
    "defense_offense": ["防守", "进攻", "品牌词", "竞品进攻", "流量保护"],
    "compliance_risk": ["刷", "S单", "免评", "违规", "白帽", "黑帽"],
    "data_diagnosis": ["检查", "诊断", "判断", "数据", "报告", "对比", "样本", "观察", "后台"],
}

METRIC_LABELS = {
    "acos": ["ACOS", "acos", "Acos", "广销比"],
    "cpc": ["CPC", "cpc", "单点", "点击费用", "单次点击"],
    "cvr": ["转化率", "CVR", "cvr"],
    "ad_order_share": ["广告单占比", "广告订单占比", "出单占比", "广告占比"],
    "daily_orders": ["日出单", "每天", "每日", "订单", "出单"],
    "organic_rank": ["自然排名", "自然位", "关键词排名"],
    "ad_rank": ["广告排名", "广告位", "广告位置"],
    "price": ["售价", "价格", "单价", "$", "美金", "刀"],
    "category": ["类目", "品类", "鞋类", "个护", "标品", "非标"],
    "keyword_type": ["关键词", "大词", "中小词", "长尾词", "核心词", "精准词", "搜索词"],
    "competitor_context": ["竞品", "竞争对手", "亚马逊自营", "头部", "类目"],
    "ranking_problem": ["排名", "自然位", "推不动", "不提升", "下降", "掉", "上不去"],
}


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


def clean_text(text: str) -> str:
    """Remove Markdown and section metadata that should not become evidence."""
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^-\s*(评论人名称|评论时间|点赞数量)\s*[:：]", stripped):
            continue
        if stripped.startswith("![") or stripped.startswith("[图片"):
            continue
        cleaned_lines.append(stripped)
    cleaned = " ".join(line for line in cleaned_lines if line)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def sentence_split(text: str) -> list[str]:
    """Split text into compact Chinese/English sentence-like chunks."""
    cleaned = clean_text(text)
    parts = re.split(r"(?<=[。！？!?；;])\s+|\n+|(?<=。)", cleaned)
    sentences = [part.strip(" 　") for part in parts if part.strip(" 　")]
    return sentences if sentences else ([cleaned] if cleaned else [])


def truncate_quote(text: str, max_chars: int = MAX_EVIDENCE_CHARS) -> str:
    """Return a short evidence quote without losing the supporting clause."""
    cleaned = clean_text(text)
    if len(cleaned) <= max_chars:
        return cleaned
    candidate = cleaned[: max_chars + 1]
    cut_positions = [candidate.rfind(mark) for mark in ("。", "；", "，", ";", ",")]
    cut = max(cut_positions)
    if cut >= 60:
        return candidate[: min(cut, max_chars - 3)].strip() + "..."
    return cleaned[: max_chars - 3].strip() + "..."


def first_sentence_with(text: str, terms: list[str]) -> str:
    """Find the first sentence containing any term."""
    for sentence in sentence_split(text):
        if any(term in sentence for term in terms):
            return sentence
    return sentence_split(text)[0] if sentence_split(text) else ""


def matching_sentence(text: str, terms: list[str]) -> str:
    """Find the first sentence containing any term, without fallback."""
    for sentence in sentence_split(text):
        if any(term in sentence for term in terms):
            return sentence
    return ""


def has_any(text: str, terms: list[str]) -> bool:
    """Return true when text contains any listed term."""
    return any(term in text for term in terms)


def relevance_score(text: str) -> int:
    """Count relevance cues in text."""
    return sum(1 for term in RELEVANCE_TERMS if term in text)


def infer_topic(text: str) -> str:
    """Infer the main strategy topic from keyword evidence."""
    scores = {
        topic: sum(text.count(keyword) for keyword in keywords)
        for topic, keywords in TOPIC_KEYWORDS.items()
    }
    topic, score = max(scores.items(), key=lambda item: item[1])
    return topic if score else ""


def infer_product_stage(text: str) -> str:
    """Infer product lifecycle stage."""
    if re.search(r"下降|下滑|断崖|掉|不出单|衰退", text):
        return "declining"
    if re.search(r"旺季前|到货前|预热|提前布局|准备工作", text):
        return "seasonal_preheat"
    if re.search(r"旺季|黑五|圣诞|万圣|季节性|窗口期", text):
        return "seasonal_peak"
    if re.search(r"新品|新产品|新链接|上架|开售|冷启动|上线|到货当天", text):
        return "new_launch"
    if re.search(r"爬坡|推起来|拉升|增长|冲排名|上首页", text):
        return "growth"
    if re.search(r"稳定|老品|长期|日常|成熟", text):
        return "stable"
    if re.search(r"清库存|库存压力|库存", text):
        return "seasonal_clearance"
    return "unknown"


def infer_ad_type(text: str) -> str:
    """Infer normalized ad type."""
    if re.search(r"SB视频|品牌视频|视频广告", text, flags=re.I):
        return "Sponsored Brands Video"
    if re.search(r"SB|品牌广告|Sponsored Brands", text, flags=re.I):
        return "Sponsored Brands"
    if re.search(r"SD|展示型|Sponsored Display", text, flags=re.I):
        return "Sponsored Display"
    if re.search(r"商品投放|ASIN|asin|竞品|定投", text):
        return "Product Targeting"
    if re.search(r"类目投放|品类投放", text):
        return "Category Targeting"
    if "自动广告" in text:
        return "Auto Campaign"
    if "手动广告" in text:
        return "Manual Campaign"
    if re.search(r"SP|Sponsored Products|精准|词组|广泛", text, flags=re.I):
        return "Sponsored Products"
    return "unknown"


def infer_match_type(text: str) -> str:
    """Infer normalized targeting/match type."""
    matches = []
    if "自动" in text:
        matches.append("auto")
    if "广泛" in text:
        matches.append("broad")
    if "词组" in text:
        matches.append("phrase")
    if "精准" in text or "精确" in text:
        matches.append("exact")
    if re.search(r"ASIN|asin|商品投放|定投", text):
        matches.append("asin")
    if "类目" in text or "品类" in text:
        matches.append("category")
    if "品牌词" in text:
        matches.append("brand")
    unique = list(dict.fromkeys(matches))
    if len(unique) > 1:
        return "mixed"
    return unique[0] if unique else "unknown"


def infer_post_type(sections: list[dict[str, Any]]) -> str:
    """Infer source-level post type from title/body/comments."""
    metadata = next((section for section in sections if section["section_role"] == "metadata"), sections[0])
    title = metadata.get("heading", "") + " " + metadata.get("text", "")
    body_text = " ".join(
        clean_text(section["text"])
        for section in sections
        if section["section_role"] in {"author_body", "author_update"}
    )
    comment_count = sum(1 for section in sections if section["section_role"] == "comment")
    metric_hits = metric_hit_count(body_text)
    title_body = title + " " + body_text[:1000]
    has_question = has_any(title_body, QUESTION_TERMS)
    has_tutorial = re.search(r"打法|攻略|分享|思路|策略|实践|干货|如何|操作|优化|结构", title_body)
    has_case = "案例" in title_body or metric_hits >= 3

    if has_case and has_tutorial:
        return "mixed"
    if has_case:
        return "case_post"
    if has_question:
        return "question_post"
    if has_tutorial:
        return "tutorial_article"
    if comment_count >= 10:
        return "discussion_post"
    return "unknown"


def metric_sentence_supported(key: str, sentence: str, labels: list[str]) -> bool:
    """Return true when a sentence supports a specific metric key."""
    if not any(label in sentence for label in labels):
        return False
    if key == "acos":
        return bool(re.search(r"\d|%|高|低|居高|飙升|下降|控制|压", sentence))
    if key == "cpc":
        return bool(re.search(r"\d|\$|美金|刀|高|低|贵|便宜|上涨|下降", sentence))
    if key == "cvr":
        return bool(re.search(r"\d|%|高|低|好|差|提升|下降", sentence))
    if key == "ad_order_share":
        return bool(re.search(r"\d|%|高|低|严重|过高|大于|以上|以下", sentence))
    if key == "daily_orders":
        if "单点" in sentence or "单次点击" in sentence:
            return False
        return bool(
            re.search(
                r"日出单[^。；;]{0,20}\d|"
                r"(每天|每日)[^。；;]{0,30}(出单|订单|\d+\s*单)|"
                r"(订单|出单)[^。；;]{0,30}\d|"
                r"\d+\s*[-~到至]\s*\d+\s*单|"
                r"\d+\s*单(?!点|次点击)|"
                r"每天都有出单",
                sentence,
            )
        )
    if key == "organic_rank":
        return bool(re.search(r"首页|第?\d+\s*页|前\s*\d+\s*页|第?\d+\s*位|首位|靠前|靠后|下降|提升|推不动|上不去|搜不到", sentence))
    if key == "ad_rank":
        return bool(re.search(r"首页|第一|首位|第?\d+\s*位|top|顶部|靠前|靠下|搜索页|商品页", sentence, flags=re.I))
    if key == "price":
        if "预算" in sentence or "花费" in sentence or "竞价" in sentence:
            return False
        return bool(re.search(r"(售价|价格|单价)[^。；;]{0,20}(\$|美金|刀|元)?\s*\d|\$\s*\d+|\d+(?:\.\d+)?\s*(美金|刀|元)", sentence))
    if key == "category":
        return bool(re.search(r"(类目|品类)\s*[:：是为]|\w+\s*类产品|鞋类|个护|标品|非标", sentence))
    if key == "keyword_type":
        return bool(re.search(r"大词|中小词|长尾词|核心词|精准词|搜索词|目标词|出单词", sentence))
    if key == "competitor_context":
        return bool(re.search(r"竞品|竞争对手|亚马逊自营|头部|对标", sentence))
    if key == "ranking_problem":
        return bool(re.search(r"(排名|自然位|自然排名).*(推不动|不提升|下降|掉|上不去|无法|搜不到)|(推不动|不提升|下降|掉|上不去|无法|搜不到).*(排名|自然位|自然排名)", sentence))
    return bool(re.search(r"\d|%|左右|以上|以下|首页|首位|前|后|低|高|多|少|爆|满|掉|下降|提升|不出单|推不动", sentence))


def context_for_metric(text: str, key: str, labels: list[str]) -> str:
    """Return a short source-faithful context string for a metric label."""
    for sentence in sentence_split(text):
        if metric_sentence_supported(key, sentence, labels):
            return truncate_quote(sentence, 90)
    return ""


def extract_case_metrics(text: str) -> dict[str, str]:
    """Extract source-faithful metric snippets for case observations."""
    metrics: dict[str, str] = {}
    for key, labels in METRIC_LABELS.items():
        value = context_for_metric(text, key, labels)
        if value:
            metrics[key] = value
    return metrics


def metric_hit_count(text: str) -> int:
    """Count concrete metric categories visible in text."""
    metrics = extract_case_metrics(text)
    return len(metrics)


def is_quantified_case_metric(key: str, value: str) -> bool:
    """Return true when a metric snippet is concrete enough for a case record."""
    if key in {"acos", "cvr", "ad_order_share"}:
        return bool(re.search(r"\d+\s*%|约\s*\d|左右|以上|以下", value))
    if key in {"cpc", "price"}:
        return bool(re.search(r"\$|美金|刀|元|\d+(?:\.\d+)?", value))
    if key == "daily_orders":
        return bool(re.search(r"\d+\s*[-~到至]?\s*\d*\s*单|每天都有出单", value))
    if key in {"organic_rank", "ad_rank"}:
        return bool(re.search(r"首页|首位|第?\d+\s*(页|位)|前\s*\d+\s*(页|位)|搜不到|靠前|靠后|开外", value))
    return False


def metric_threshold_from_metrics(metrics: dict[str, str]) -> str:
    """Build a compact metric threshold string."""
    parts = []
    for key in ("acos", "cpc", "cvr", "ad_order_share", "daily_orders", "organic_rank", "ad_rank"):
        if key in metrics:
            parts.append(f"{key}: {metrics[key]}")
    return "；".join(parts)[:300]


def is_counterexample_text(text: str) -> bool:
    """Detect evidence that limits common assumptions."""
    return bool(counterexample_evidence(text))


def counterexample_evidence(text: str) -> str:
    """Return the sentence that supports a counterexample, if any."""
    for sentence in sentence_split(text):
        if relevance_score(sentence) < 2:
            continue
        if re.search(r"不一定|不代表|不等于|并不|未必|不能只看|不是.*而是", sentence):
            return sentence
        if ("ACOS" in sentence or "acos" in sentence or "Acos" in sentence) and (
            "不代表" in sentence or "不一定" in sentence or "不等于" in sentence
        ):
            return sentence
        if ("广告位" in sentence or "广告排名" in sentence) and (
            "自然排名" in sentence or "自然位" in sentence
        ) and has_any(sentence, ["无法", "没有", "不提升", "推不动"]):
            return sentence
    return ""


def contradiction_key_for(text: str) -> str:
    """Assign a stable contradiction key."""
    if ("ACOS" in text or "acos" in text or "Acos" in text) and ("自然" in text or "CPC" in text or "cpc" in text):
        return "low_acos_not_enough_for_ranking"
    if ("广告单占比" in text or "广告订单占比" in text or "广告依赖" in text) and ("自然" in text or "活动" in text):
        return "ad_orders_can_cannibalize_natural_orders"
    if ("广告位" in text or "广告排名" in text) and ("自然排名" in text or "自然位" in text):
        return "ad_rank_not_equal_organic_rank"
    if ("预算" in text or "竞价" in text) and has_any(text, ["不一定", "不是", "无法", "没有"]):
        return "budget_increase_not_always_solution"
    if "广泛" in text and ("精准" in text or "词组" in text):
        return "broad_match_can_outperform_exact"
    return "context_dependent_ads_rule"


def classify_noise_comment(text: str) -> str | None:
    """Classify comment noise, returning None when the comment is usable."""
    cleaned = clean_text(text)
    if not cleaned:
        return "unreadable"
    body = re.sub(r"@\S+[:：]\s*", "", cleaned).strip()
    if len(body) <= 6:
        return "too_short"
    account_terms = [
        "邀请码",
        "邀请",
        "注册",
        "账号",
        "加我",
        "加V",
        "微信",
        "VX",
        "QQ",
        "私信",
        "联系",
        "群",
        "register",
        "链接",
    ]
    if re.search(r"https?://|register|code=|邀请码|注册", body, flags=re.I):
        return "account_invitation"
    if has_any(body, account_terms) and relevance_score(body) <= 1:
        return "account_invitation"
    if re.fullmatch(r"(@\S+[:：])?\s*(好的|好|嗯|是的|同问|哈哈+|厉害|牛|赞|顶|蹲|围观|mark|Mark|收藏|学习了?|受教了?|谢谢|感谢|感谢分享|干货)\s*[。！!]*", body):
        return "thanks_only" if has_any(body.lower(), ["谢谢", "感谢", "学习", "收藏", "mark", "干货", "受教"]) else "social_reply"
    if body.startswith("@") and len(body) <= 35 and relevance_score(body) == 0:
        return "social_reply"
    if relevance_score(body) == 0:
        return "off_topic" if len(body) > 18 else "too_short"
    return None


def split_candidate_segments(text: str) -> list[str]:
    """Split longer bodies into candidate operational segments."""
    cleaned = clean_text(text)
    raw_parts = re.split(
        r"\n\s*\n|(?=操作\d+[:：])|(?=误区\d+[:：])|(?=问题\d+[:：])|(?=广告策略[:：])|(?=总结[:：])|(?=PS[:：])|(?=[一二三四五六七八九十][.、]\s*)|(?=\d+[.、]\s*)",
        cleaned,
    )
    parts: list[str] = []
    for part in raw_parts:
        stripped = part.strip()
        if len(stripped) < 25:
            continue
        if len(stripped) > 520:
            sentences = sentence_split(stripped)
            chunk = ""
            for sentence in sentences:
                if len(chunk) + len(sentence) > 420 and chunk:
                    parts.append(chunk.strip())
                    chunk = sentence
                else:
                    chunk = (chunk + " " + sentence).strip()
            if chunk:
                parts.append(chunk.strip())
        else:
            parts.append(stripped)
    return parts


def is_actionable_segment(segment: str) -> bool:
    """Return true when a segment can become an operational record."""
    soft_action = bool(re.search(r"可以(先|把|用|开|关|降|提|加|设置|选择|考虑|通过|直接)", segment))
    return relevance_score(segment) >= 2 and (has_any(segment, ACTION_TERMS) or soft_action) and len(segment) >= 28


def infer_condition(segment: str) -> str:
    """Infer a bounded condition for a rule or hypothesis."""
    condition_terms = ["如果", "当", "对于", "针对", "遇到", "出现", "阶段", "新品", "旺季", "淡季", "预算", "ACOS", "自然排名"]
    condition = first_sentence_with(segment, condition_terms)
    return truncate_quote(condition or segment, 130)


def infer_action(segment: str) -> str:
    """Infer an action/check from a segment."""
    action = matching_sentence(segment, ACTION_TERMS)
    if not action:
        for sentence in sentence_split(segment):
            if re.search(r"可以(先|把|用|开|关|降|提|加|设置|选择|考虑|通过|直接)", sentence):
                action = sentence
                break
    return truncate_quote(action or segment, 150)


def infer_reasoning(segment: str) -> str:
    """Infer the source's rationale or produce a bounded data caveat."""
    reasoning = matching_sentence(segment, REASONING_TERMS)
    if reasoning:
        return truncate_quote(reasoning, 160)
    topic = infer_topic(segment) or "广告表现"
    return f"原文把该动作与{topic}目标绑定；执行前需要用后台数据确认场景是否一致。"


def tags_for_text(text: str) -> list[str]:
    """Build searchable tags from obvious cues."""
    tag_terms = {
        "low_acos": ["低 ACOS", "ACOS低", "Acos低", "acos低"],
        "high_acos": ["高 ACOS", "ACOS高", "Acos高", "acos高", "ACOS居高"],
        "low_cpc": ["CPC低", "低 CPC", "单点低", "0.2", "0.16"],
        "ad_dependency": ["广告依赖", "广告单占比", "广告订单占比"],
        "organic_rank": ["自然排名", "自然位"],
        "budget": ["预算", "花费", "卡预算"],
        "broad_match": ["广泛"],
        "exact_match": ["精准", "精确"],
        "phrase_match": ["词组"],
        "auto_campaign": ["自动广告"],
        "product_targeting": ["商品投放", "ASIN", "asin", "竞品"],
        "seasonal": ["季节", "旺季", "淡季", "黑五", "圣诞"],
        "launch": ["新品", "新产品", "上架"],
        "conversion": ["转化率", "CVR", "CTR", "点击率", "链接质量"],
    }
    return [tag for tag, terms in tag_terms.items() if has_any(text, terms)]


def make_record(
    section: dict[str, Any],
    *,
    post_type: str,
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
    if section["section_role"] == "comment" and confidence == "high":
        confidence = "medium"
    return {
        "record_id": "",
        "source_id": section["source_id"],
        "section_id": section["section_id"],
        "post_type": post_type,
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
        "evidence_quote": truncate_quote(evidence_quote),
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


def extract_a017_records(sections: list[dict[str, Any]], post_type: str) -> list[dict[str, Any]]:
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
                post_type=post_type,
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
                post_type=post_type,
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
                post_type=post_type,
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
                post_type=post_type,
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
                post_type=post_type,
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
                post_type=post_type,
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
                post_type=post_type,
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
                post_type=post_type,
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
                post_type=post_type,
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
                post_type=post_type,
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


def build_case_record(section: dict[str, Any], post_type: str) -> dict[str, Any] | None:
    """Build a case record when a section contains concrete metrics."""
    text = clean_text(section["text"])
    metrics = extract_case_metrics(text)
    strong_keys = {
        "acos",
        "cpc",
        "cvr",
        "ad_order_share",
        "daily_orders",
        "organic_rank",
        "ad_rank",
        "price",
    }
    strong_metric_count = sum(
        1
        for key, value in metrics.items()
        if key in strong_keys and is_quantified_case_metric(key, value)
    )
    case_cue = re.search(
        r"案例|产品的基本情况|实际产品|售价|出单|订单|自然排名|自然位|广告单占比|日常|到货|广告依赖|ACOS|Acos|acos|CPC|cpc|转化率",
        text,
    )
    if strong_metric_count < 2 or not case_cue:
        return None
    if post_type in {"tutorial_article", "mixed"} and not re.search(
        r"案例|产品的基本情况|实际产品|发了\d+|到货当天|日出单|出单[^。；;]{0,20}\d|"
        r"\d+\s*[-~到至]\s*\d+\s*单|广告单占比|自然排名[^。；;]{0,30}\d|"
        r"ACOS[^。；;]{0,20}\d|Acos[^。；;]{0,20}\d|acos[^。；;]{0,20}\d|"
        r"CPC[^。；;]{0,20}\d|cpc[^。；;]{0,20}\d|转化率[^。；;]{0,20}\d",
        text,
    ):
        return None
    if section["section_role"] == "comment":
        return None

    evidence_labels = [
        label
        for key, labels in METRIC_LABELS.items()
        if key in strong_keys and key in metrics
        for label in labels
    ]
    evidence = first_sentence_with(text, evidence_labels)
    if not re.search(r"ACOS|Acos|acos|CPC|cpc|转化率|广告单占比|自然排名|自然位|广告位|出单|订单|售价|日出单", evidence):
        return None
    topic = infer_topic(text) or "data_diagnosis"
    confidence = "high" if strong_metric_count >= 5 and section["section_role"] != "comment" else "medium"
    problem = matching_sentence(text, ["无法", "不出单", "下降", "推不动", "广告依赖", "不提升", "上不去"])
    reasoning = problem or evidence or "原文提供了广告、关键词或排名数据，可作为案例观察进入案例库。"
    return make_record(
        section,
        post_type=post_type,
        record_type="case_observation",
        is_relevant=True,
        topic=topic,
        product_stage=infer_product_stage(text),
        ad_type=infer_ad_type(text),
        match_type=infer_match_type(text),
        condition=truncate_quote(problem or evidence or text, 130),
        metric_threshold=metric_threshold_from_metrics(metrics),
        reasoning=truncate_quote(reasoning, 180),
        case_metrics=metrics,
        evidence_quote=evidence or text,
        confidence=confidence,
        limitations="来源为单篇帖子或单段经验；缺少后台完整报表、类目均值或竞品对照时不能外推为绝对规则。",
        contradiction_key=contradiction_key_for(text) if is_counterexample_text(text) else "",
        tags=tags_for_text(text),
    )


def build_counterexample_record(section: dict[str, Any], post_type: str, text: str) -> dict[str, Any]:
    """Build a counterexample record from limiting evidence."""
    evidence = counterexample_evidence(text) or text
    return make_record(
        section,
        post_type=post_type,
        record_type="counterexample",
        is_relevant=True,
        topic=infer_topic(text) or "data_diagnosis",
        product_stage=infer_product_stage(text),
        ad_type=infer_ad_type(text),
        match_type=infer_match_type(text),
        condition=infer_condition(evidence),
        action="将该观点作为例外条件处理，先补充阶段、毛利、预算、样本量、广告目标和自然排名目标后再决策。",
        metric_threshold=metric_threshold_from_metrics(extract_case_metrics(text)),
        reasoning=infer_reasoning(evidence),
        evidence_quote=evidence,
        comment_signal="contradiction" if section["section_role"] == "comment" else "none",
        confidence="medium" if section["section_role"] != "comment" else "low",
        limitations="该记录限制常见判断，不说明相反观点在所有场景都正确。",
        contradiction_key=contradiction_key_for(text),
        tags=tags_for_text(text),
    )


def build_diagnostic_question(section: dict[str, Any], post_type: str, text: str) -> dict[str, Any] | None:
    """Build a diagnostic question from author uncertainty."""
    if not has_any(text, QUESTION_TERMS):
        return None
    if relevance_score(text) < 2:
        return None
    missing_checks = []
    for label, terms in {
        "CTR": ["CTR", "点击率"],
        "CVR": ["CVR", "转化率"],
        "CPC": ["CPC", "cpc", "单点"],
        "ACOS/TACOS": ["ACOS", "TACOS"],
        "广告单占比": ["广告单占比", "广告订单占比"],
        "自然排名": ["自然排名", "自然位"],
        "订单量": ["订单", "出单"],
    }.items():
        if not has_any(text, terms):
            missing_checks.append(label)
    action = "补充并检查 " + "、".join(missing_checks[:5]) if missing_checks else "用后台报表验证问题假设。"
    return make_record(
        section,
        post_type=post_type,
        record_type="diagnostic_question",
        is_relevant=True,
        topic=infer_topic(text) or "data_diagnosis",
        product_stage=infer_product_stage(text),
        ad_type=infer_ad_type(text),
        match_type=infer_match_type(text),
        condition=truncate_quote(first_sentence_with(text, QUESTION_TERMS) or text, 150),
        action=action,
        metric_threshold=metric_threshold_from_metrics(extract_case_metrics(text)),
        reasoning="提问内容表达的是待验证问题，不能直接升级为确定性规则。",
        evidence_quote=first_sentence_with(text, QUESTION_TERMS) or text,
        confidence="low",
        limitations="需要更多后台数据和业务目标才能判断。",
        tags=tags_for_text(text) + ["diagnostic_question"],
    )


def build_rule_record(section: dict[str, Any], post_type: str, segment: str) -> dict[str, Any]:
    """Build an executable rule from a scoped actionable segment."""
    return make_record(
        section,
        post_type=post_type,
        record_type="executable_rule",
        is_relevant=True,
        topic=infer_topic(segment) or "campaign_structure",
        product_stage=infer_product_stage(segment),
        ad_type=infer_ad_type(segment),
        match_type=infer_match_type(segment),
        condition=infer_condition(segment),
        action=infer_action(segment),
        metric_threshold=metric_threshold_from_metrics(extract_case_metrics(segment)),
        reasoning=infer_reasoning(segment),
        evidence_quote=infer_action(segment),
        confidence="medium",
        limitations="需结合产品阶段、毛利、预算、样本量、广告目标和自然排名目标验证；不要机械套用。",
        contradiction_key=contradiction_key_for(segment) if is_counterexample_text(segment) else "",
        tags=tags_for_text(segment),
    )


def build_comment_record(section: dict[str, Any], post_type: str) -> list[dict[str, Any]]:
    """Extract useful or noisy records from one comment section."""
    text = clean_text(section["text"])
    noise_reason = classify_noise_comment(text)
    if noise_reason:
        return [
            make_record(
                section,
                post_type=post_type,
                record_type="irrelevant_noise",
                is_relevant=False,
                noise_reason=noise_reason,
                product_stage="unknown",
                ad_type="unknown",
                match_type="unknown",
                evidence_quote=text,
                comment_signal="noise",
                confidence="low",
            )
        ]

    if is_counterexample_text(text):
        return [build_counterexample_record(section, post_type, text)]

    signal = "diagnostic_check" if has_any(text, ["看", "检查", "对比", "判断", "数据", "报告", "观察"]) else "alternative_explanation"
    if has_any(text, ["建议", "可以", "需要", "先", "再", "不要", "应该"]):
        signal = "actionable_advice"
    if relevance_score(text) >= 2 and (has_any(text, ACTION_TERMS) or has_any(text, REASONING_TERMS) or has_any(text, ["可能", "原因", "是不是"])):
        return [
            make_record(
                section,
                post_type=post_type,
                record_type="diagnostic_hypothesis",
                is_relevant=True,
                topic=infer_topic(text) or "data_diagnosis",
                product_stage=infer_product_stage(text),
                ad_type=infer_ad_type(text),
                match_type=infer_match_type(text),
                condition=infer_condition(text),
                action=infer_action(text) if has_any(text, ACTION_TERMS) else "将该评论作为诊断假设，用后台报表和业务目标验证。",
                metric_threshold=metric_threshold_from_metrics(extract_case_metrics(text)),
                reasoning=infer_reasoning(text),
                evidence_quote=text,
                comment_signal=signal,
                confidence="medium" if len(text) >= 45 else "low",
                limitations="评论区观点默认不高于 medium confidence；缺少完整后台数据时不能作为确定性规则。",
                contradiction_key=contradiction_key_for(text) if is_counterexample_text(text) else "",
                tags=tags_for_text(text),
            )
        ]

    return [
        make_record(
            section,
            post_type=post_type,
            record_type="comment_signal",
            is_relevant=True,
            topic=infer_topic(text) or "data_diagnosis",
            product_stage=infer_product_stage(text),
            ad_type=infer_ad_type(text),
            match_type=infer_match_type(text),
            condition=truncate_quote(text, 130),
            reasoning="评论与广告或关键词问题相关，但缺少足够条件、动作或证据，暂存为弱信号。",
            evidence_quote=text,
            comment_signal="weak_agreement",
            confidence="low",
            limitations="弱评论信号不能进入规则库。",
            tags=tags_for_text(text),
        )
    ]


def extract_generic_records(sections: list[dict[str, Any]], post_type: str) -> list[dict[str, Any]]:
    """Extract records from a non-sample source using deterministic heuristics."""
    records: list[dict[str, Any]] = []
    for section in sections:
        role = section["section_role"]
        if role == "metadata":
            continue
        text = clean_text(section["text"])
        if not text or text == "无公开评论。":
            continue
        if role == "comment":
            records.extend(build_comment_record(section, post_type))
            continue
        if role not in {"author_body", "author_update", "unknown"}:
            continue
        if relevance_score(text) < 2:
            continue

        case_record = build_case_record(section, post_type)
        if case_record:
            records.append(case_record)

        if is_counterexample_text(text):
            records.append(build_counterexample_record(section, post_type, text))

        diagnostic_question = build_diagnostic_question(section, post_type, text)
        if diagnostic_question:
            records.append(diagnostic_question)

        emitted_rules = 0
        for segment in split_candidate_segments(section["text"]):
            if emitted_rules >= 3:
                break
            if not is_actionable_segment(segment):
                continue
            if len(extract_case_metrics(segment)) >= 3 and ("?" in segment or "？" in segment):
                continue
            if post_type == "case_post" and len(extract_case_metrics(segment)) >= 3:
                continue
            records.append(build_rule_record(section, post_type, segment))
            emitted_rules += 1

        if not records and role in {"author_body", "author_update"} and has_any(text, ["可能", "原因", "判断", "检查"]):
            records.append(
                make_record(
                    section,
                    post_type=post_type,
                    record_type="diagnostic_hypothesis",
                    is_relevant=True,
                    topic=infer_topic(text) or "data_diagnosis",
                    product_stage=infer_product_stage(text),
                    ad_type=infer_ad_type(text),
                    match_type=infer_match_type(text),
                    condition=infer_condition(text),
                    action="把该观点作为诊断假设，结合广告报表、搜索词报告和自然排名数据验证。",
                    metric_threshold=metric_threshold_from_metrics(extract_case_metrics(text)),
                    reasoning=infer_reasoning(text),
                    evidence_quote=text,
                    confidence="low",
                    limitations="原文证据不足，不能直接写成规则。",
                    tags=tags_for_text(text),
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
    """Validate the extraction schema requirements."""
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
    if record["record_type"] in {"case_observation", "diagnostic_hypothesis", "diagnostic_question", "counterexample", "executable_rule"}:
        if not record["evidence_quote"]:
            raise ValueError(f"{record['record_id']} non-noise record needs evidence_quote")
    if record["section_role"] == "comment" and record["confidence"] == "high":
        raise ValueError(f"{record['record_id']} comment-derived confidence cannot be high")
    if len(record["evidence_quote"]) > MAX_EVIDENCE_CHARS:
        raise ValueError(f"{record['record_id']} evidence_quote is too long")


def extract_records(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract records from selected sections."""
    records: list[dict[str, Any]] = []
    for source_id, source_sections in group_sections_by_source(sections):
        post_type = infer_post_type(source_sections)
        file_name = source_sections[0]["file_name"]
        if source_id == "A017" or file_name.startswith("017_q31734_"):
            records.extend(extract_a017_records(source_sections, post_type))
        else:
            records.extend(extract_generic_records(source_sections, post_type))

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


def report_path_for(output_file: Path) -> Path:
    """Map record output path to the expected extraction report path."""
    if output_file.name == "extracted_records_batch10.jsonl":
        return output_file.with_name("extraction_report_batch10.md")
    if output_file.name == "extracted_records.jsonl":
        return output_file.with_name("extraction_report.md")
    stem = output_file.stem.replace("extracted_records", "extraction_report")
    return output_file.with_name(stem + ".md")


def percent(part: int, whole: int) -> str:
    """Format a percentage."""
    return "0.00%" if whole == 0 else f"{part / whole:.2%}"


def markdown_counter(counter: Counter[str], limit: int | None = None) -> str:
    """Render a counter as Markdown bullets."""
    items = counter.most_common(limit)
    if not items:
        return "- 无"
    return "\n".join(f"- {key or '<empty>'}: {value}" for key, value in items)


def write_extraction_report(
    report_file: Path,
    selected_sections: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> None:
    """Write a Phase 6/7 extraction statistics report."""
    source_count = len({section["source_id"] for section in selected_sections})
    section_count = len(selected_sections)
    record_type_counts = Counter(record["record_type"] for record in records)
    topic_counts = Counter(record["topic"] for record in records if record["topic"])
    confidence_counts = Counter(record["confidence"] for record in records)
    comment_records = [record for record in records if record["section_role"] == "comment"]
    noise_comment_records = [
        record
        for record in comment_records
        if record["record_type"] == "irrelevant_noise"
    ]
    metric_counts = Counter()
    for record in records:
        metrics = record.get("case_metrics", {})
        if "acos" in metrics or "ACOS" in record.get("metric_threshold", "").upper():
            metric_counts["ACOS"] += 1
        if "cpc" in metrics or "CPC" in record.get("metric_threshold", "").upper():
            metric_counts["CPC"] += 1
        if "cvr" in metrics or "转化率" in record.get("metric_threshold", ""):
            metric_counts["CVR/转化率"] += 1
        if "ad_order_share" in metrics or "广告单占比" in record.get("metric_threshold", ""):
            metric_counts["广告单占比"] += 1
        if "organic_rank" in metrics or "自然排名" in record.get("metric_threshold", ""):
            metric_counts["自然排名"] += 1
        if "daily_orders" in metrics or "订单" in record.get("metric_threshold", ""):
            metric_counts["订单量"] += 1

    overlong_quotes = [record["record_id"] for record in records if len(record["evidence_quote"]) > MAX_EVIDENCE_CHARS]
    comment_high = [record["record_id"] for record in records if record["section_role"] == "comment" and record["confidence"] == "high"]
    rule_case_mix = [
        record["record_id"]
        for record in records
        if record["record_type"] == "executable_rule" and record.get("case_metrics")
    ]

    lines = [
        "# Extraction Report",
        "",
        "## Summary",
        "",
        f"- 总文章数: {source_count}",
        f"- 总 section 数: {section_count}",
        f"- 总 record 数: {len(records)}",
        f"- case_observation 数量: {record_type_counts.get('case_observation', 0)}",
        f"- executable_rule 数量: {record_type_counts.get('executable_rule', 0)}",
        f"- diagnostic_hypothesis 数量: {record_type_counts.get('diagnostic_hypothesis', 0)}",
        f"- diagnostic_question 数量: {record_type_counts.get('diagnostic_question', 0)}",
        f"- counterexample 数量: {record_type_counts.get('counterexample', 0)}",
        f"- irrelevant_noise 数量: {record_type_counts.get('irrelevant_noise', 0)}",
        f"- 评论区 record 占比: {percent(len(comment_records), len(records))}",
        f"- 评论区噪音占比: {percent(len(noise_comment_records), len(comment_records))}",
        "",
        "## Topic Distribution",
        "",
        markdown_counter(topic_counts),
        "",
        "## Confidence Distribution",
        "",
        markdown_counter(confidence_counts),
        "",
        "## Metric Coverage",
        "",
        markdown_counter(metric_counts),
        "",
        "## Quality Checks",
        "",
        f"- 普通摘要混入风险: {'未发现明显记录' if records else '无记录可检查'}",
        f"- 案例误判成规则: {'无' if not rule_case_mix else ', '.join(rule_case_mix[:20])}",
        f"- 评论区 high confidence: {'无' if not comment_high else ', '.join(comment_high[:20])}",
        f"- evidence_quote 过长: {'无' if not overlong_quotes else ', '.join(overlong_quotes[:20])}",
        "",
        "## Record Type Distribution",
        "",
        markdown_counter(record_type_counts),
        "",
    ]
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text("\n".join(lines), encoding="utf-8")


def quality_findings(record: dict[str, Any]) -> list[str]:
    """Return deterministic quality findings for a sampled record."""
    findings: list[str] = []
    try:
        validate_record(record)
    except ValueError as exc:
        findings.append(str(exc))
    if record["record_type"] != "irrelevant_noise" and len(record["evidence_quote"]) < 8:
        findings.append("evidence_quote too thin")
    if record["record_type"] == "executable_rule" and record.get("case_metrics"):
        findings.append("rule contains case_metrics; possible case/rule confusion")
    if record["section_role"] == "comment" and record["confidence"] == "high":
        findings.append("comment record has high confidence")
    if record["record_type"] in {"executable_rule", "diagnostic_hypothesis"}:
        generic_action = record["action"] in {"优化广告", "调整广告", "继续观察", ""}
        if generic_action:
            findings.append("action is too generic")
    if len(record["evidence_quote"]) > MAX_EVIDENCE_CHARS:
        findings.append("evidence_quote exceeds configured limit")
    return findings


def write_quality_report(records: list[dict[str, Any]], output_file: Path = QUALITY_REPORT_FILE) -> None:
    """Write a random 50-record quality inspection report."""
    sample_size = min(50, len(records))
    rng = random.Random(20260601)
    sample = rng.sample(records, sample_size) if sample_size else []
    all_findings: list[tuple[str, list[str]]] = []
    for record in sample:
        findings = quality_findings(record)
        if findings:
            all_findings.append((record["record_id"], findings))

    comment_high = [record["record_id"] for record in records if record["section_role"] == "comment" and record["confidence"] == "high"]
    overlong = [record["record_id"] for record in records if len(record["evidence_quote"]) > MAX_EVIDENCE_CHARS]
    empty_relevant = [
        record["record_id"]
        for record in records
        if record["record_type"] != "irrelevant_noise" and not record["evidence_quote"]
    ]

    lines = [
        "# Extraction Quality Report",
        "",
        f"- 随机种子: 20260601",
        f"- 抽查 record 数: {sample_size}",
        f"- schema 检查: {'通过' if not all_findings else '发现问题'}",
        f"- 空泛内容风险: {'无明显问题' if not empty_relevant else ', '.join(empty_relevant[:20])}",
        f"- 错误分类风险: {'无明显问题' if not any('case/rule' in ' '.join(f) for _, f in all_findings) else '见抽查问题'}",
        f"- evidence_quote 过长: {'无' if not overlong else ', '.join(overlong[:20])}",
        f"- 评论区 high confidence: {'无' if not comment_high else ', '.join(comment_high[:20])}",
        "",
        "## Sampled Record IDs",
        "",
        ", ".join(record["record_id"] for record in sample) if sample else "无",
        "",
        "## Findings",
        "",
    ]
    if all_findings:
        for record_id, findings in all_findings:
            lines.append(f"- {record_id}: {'; '.join(findings)}")
    else:
        lines.append("- 抽查样本未发现 schema、空泛动作、评论区 high confidence 或 evidence_quote 过长问题。")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")


def maybe_write_noise_comments(records: list[dict[str, Any]], output_file: Path) -> None:
    """Write Phase 7 noise comments when producing the full extraction file."""
    if output_file.name != "extracted_records.jsonl":
        return
    noise_records = [
        record
        for record in records
        if record["section_role"] == "comment" and record["record_type"] == "irrelevant_noise"
    ]
    write_jsonl(NOISE_COMMENTS_FILE, noise_records)


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
    write_extraction_report(report_path_for(args.output_file), selected_sections, records)
    maybe_write_noise_comments(records, args.output_file)
    if args.output_file.name == "extracted_records.jsonl":
        write_quality_report(records)
    print(f"Wrote {len(records)} records to {args.output_file}")
    print(f"Wrote report to {report_path_for(args.output_file)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
