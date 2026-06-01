"""Detect conflicting Amazon ads strategy records.

Input paths:
  data/processed/amazon_ads_skill/merged_rules.jsonl
  data/processed/amazon_ads_skill/case_library.jsonl

Output paths:
  data/processed/amazon_ads_skill/conflict_candidates.jsonl
  .agents/skills/amazon-ads-keyword-strategy/references/07_conflict_register.md

CLI arguments:
  --rules-file: JSONL merged rules path.
  --cases-file: JSONL case library path.
  --output-file: JSONL conflict candidates path.
  --register-file: Markdown conflict register path.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_RULES_FILE = Path("data/processed/amazon_ads_skill/merged_rules.jsonl")
DEFAULT_CASES_FILE = Path("data/processed/amazon_ads_skill/case_library.jsonl")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/conflict_candidates.jsonl")
DEFAULT_REGISTER_FILE = Path(".agents/skills/amazon-ads-keyword-strategy/references/07_conflict_register.md")


CONFLICT_SPECS = [
    {
        "conflict_title": "低 ACOS 是否一定代表广告有效",
        "view_a": "低 ACOS 说明广告成本可控，可以继续保留或放量。",
        "view_b": "低 ACOS 可能只是 CPC 低或流量小，不一定能推动自然排名和整体销量。",
        "why_conflict_exists": "ACOS 只描述广告花费与广告销售额的比例，无法单独解释 CPC、CVR、点击质量、订单规模、自然排名和广告目标。",
        "decision_rule": "先判断目标是利润、跑词、排名还是放量。低 ACOS 同时满足足够点击量、订单量、目标词相关、CVR 不低于类目或竞品、自然排名有改善时，可以放量；若低 ACOS 来自低 CPC、小词或低流量，应继续诊断而不是直接判定有效。",
        "applies_when": "稳定期控成本、目标词已有转化、预算没有明显浪费、自然排名或整体订单同步改善。",
        "avoid_when": "新品期需要曝光、目标是推自然排名、样本量不足、低 CPC 只带来中小词订单、广告单占比过高。",
        "required_data": ["产品阶段", "毛利", "预算", "样本量", "广告目标", "自然排名目标", "关键词类型", "CPC", "CVR", "订单量", "ACOS", "TACOS"],
        "keywords": ["低ACOS", "ACOS", "CPC", "自然排名", "转化率", "广告单占比", "low_acos"],
    },
    {
        "conflict_title": "广告单占比高是否一定要降广告",
        "view_a": "广告单占比高意味着链接依赖广告，应降低广告或削减预算。",
        "view_b": "新品、冲排名、活动承接或自然流量未稳定时，广告单占比高可能是阶段性投入。",
        "why_conflict_exists": "广告单占比是流量结构信号，不等于利润结论；同一占比在新品期、稳定期和清库存期含义不同。",
        "decision_rule": "先看产品阶段和目标。稳定期且 TACOS 高、自然单不增长、广告词与自然目标词不一致时，降低或重分配广告；新品期或排名爬坡期若毛利和库存允许，可保留广告并用自然排名、TACOS 和总订单评估。",
        "applies_when": "广告依赖明显、TACOS 上升、自然单占比低、广告词不带动目标自然排名。",
        "avoid_when": "新品冷启动、关键词上首页阶段、库存压力需要放量、活动流量正在承接。",
        "required_data": ["产品阶段", "毛利", "预算", "广告目标", "自然排名目标", "库存压力", "广告单占比", "自然单占比", "TACOS"],
        "keywords": ["广告单占比", "广告订单占比", "广告依赖", "自然单", "TACOS", "ad_dependency"],
    },
    {
        "conflict_title": "新品期放量 vs 新品期控 ACOS",
        "view_a": "新品期要尽快放量，先积累曝光、点击、转化和关键词数据。",
        "view_b": "新品期如果不控 ACOS，预算可能被无效流量吃掉，现金流和毛利承压。",
        "why_conflict_exists": "新品期同时需要数据学习和成本边界，冲突来自目标优先级不同。",
        "decision_rule": "先定义新品期目标。以收录、跑词、排名为目标时，允许阶段性 ACOS 高于利润线，但必须设预算上限、否词规则和样本量复盘；以保本为目标时，优先控 ACOS 和精准流量。",
        "applies_when": "0-45 天新品、关键词未收录、需要快速测试搜索词和广告位。",
        "avoid_when": "毛利低、预算小、库存不足、链接转化基础差、评论或主图尚未准备好。",
        "required_data": ["产品阶段", "毛利", "预算", "样本量", "广告目标", "库存压力", "CTR", "CVR", "CPC", "ACOS"],
        "keywords": ["新品", "新产品", "上架", "放量", "ACOS", "预算", "launch"],
    },
    {
        "conflict_title": "广泛匹配拓词 vs 广泛匹配烧预算",
        "view_a": "广泛匹配适合拓词和发现高转化搜索词。",
        "view_b": "广泛匹配相关性不稳定，容易烧预算并污染广告组数据。",
        "why_conflict_exists": "广泛匹配的价值取决于预算边界、否词频率、词根质量和产品阶段。",
        "decision_rule": "广泛匹配应作为测试流量池使用，单独 campaign/ad group、设置预算上限、按点击和订单样本否词；若词根不清晰、预算小或转化差，应先用精准/词组/自动验证相关性。",
        "applies_when": "新品跑词、长尾词发现、预算可承受、搜索词报告复盘频率高。",
        "avoid_when": "预算紧、类目词泛、产品差异弱、点击多无订单且样本已足够。",
        "required_data": ["预算", "样本量", "关键词类型", "广告目标", "CTR", "CVR", "CPC", "搜索词报告", "否词记录"],
        "keywords": ["广泛", "拓词", "否词", "预算", "搜索词", "broad_match"],
    },
    {
        "conflict_title": "点击多无订单立即否词 vs 样本不足继续观察",
        "view_a": "点击多无订单说明该搜索词浪费预算，应立即否定。",
        "view_b": "样本不足时过早否词会误杀潜在转化词，尤其新品和高客单产品。",
        "why_conflict_exists": "点击阈值要结合 CVR、客单价、CPC、毛利和转化周期，而不是固定点击数。",
        "decision_rule": "先按目标 CVR 和盈亏点击数估算样本阈值。超过阈值仍无订单且相关性弱时否词；未到阈值但相关性强、目标词重要时继续观察或降竞价。",
        "applies_when": "搜索词报告优化、广告预算有限、点击已形成可判断样本。",
        "avoid_when": "样本量不足、高客单低频转化、新品学习期、目标排名词需要战略曝光。",
        "required_data": ["样本量", "毛利", "CPC", "CVR", "订单量", "关键词类型", "广告目标", "搜索词相关性"],
        "keywords": ["点击多", "不出单", "否定", "否词", "样本", "观察", "CPC", "CVR"],
    },
    {
        "conflict_title": "高 ACOS 关停 vs 高 ACOS 可能是在推自然排名",
        "view_a": "高 ACOS 广告亏损，应降低竞价、降预算或关停。",
        "view_b": "高 ACOS 如果带动目标词自然排名、收录或总订单，可能是阶段性投入。",
        "why_conflict_exists": "ACOS 是广告归因指标，推排名要同时看 TACOS、自然排名、自然单和总利润。",
        "decision_rule": "高 ACOS 先拆目标。利润型广告按毛利线处理；排名型广告看目标词自然位、TACOS、总订单和库存。如果自然排名无改善且样本足够，应降价/降竞价/换词；若排名改善且总盘可承受，可限期保留。",
        "applies_when": "关键词冲排名、新品爬坡、目标词具备战略价值。",
        "avoid_when": "毛利无法承受、库存不足、自然排名无变化、广告词与目标自然词不一致。",
        "required_data": ["毛利", "预算", "广告目标", "自然排名目标", "库存压力", "ACOS", "TACOS", "自然单", "广告单", "排名变化"],
        "keywords": ["高ACOS", "ACOS", "自然排名", "排名", "TACOS", "毛利", "预算"],
    },
    {
        "conflict_title": "精准广告提高竞价 vs 精准广告控制预算",
        "view_a": "精准词相关性高，应提高竞价抢位置和订单。",
        "view_b": "精准词 CPC 高时需要控制预算，否则利润和 TACOS 会恶化。",
        "why_conflict_exists": "精准匹配既可能是排名进攻工具，也可能是利润收割工具，取决于词的角色。",
        "decision_rule": "把精准词分为目标排名词、稳定出单词和防守词。目标排名词可限期提竞价抢位置；稳定出单词按毛利和 TACOS 控预算；防守词关注品牌保护和低成本覆盖。",
        "applies_when": "词相关性强、CVR 有优势、目标排名明确或自然位需要突破。",
        "avoid_when": "CPC 高于毛利承受、CVR 弱、预算不足、精准词并非目标自然排名词。",
        "required_data": ["关键词类型", "毛利", "预算", "广告目标", "自然排名目标", "CPC", "CVR", "ACOS", "TACOS"],
        "keywords": ["精准", "竞价", "预算", "CPC", "自然排名", "exact_match"],
    },
    {
        "conflict_title": "广告出单词排名好 vs 自然排名不提升",
        "view_a": "某词广告出单好，理论上应推动该词自然排名。",
        "view_b": "广告出单好不一定推动自然排名，可能因为词不一致、广告位不同、CVR 不足或竞争强。",
        "why_conflict_exists": "广告订单、自然排名和关键词权重之间不是一一映射，需要核对出单词、搜索路径和自然目标词。",
        "decision_rule": "先确认广告出单词是否就是自然排名目标词，再检查广告位、CTR、CVR、订单量、类目均值和竞品转化。如果出单集中在中小词或商品页，不能期待大词自然位同步提升。",
        "applies_when": "广告有订单但自然排名停滞、广告单占比高、广告位和自然位表现不一致。",
        "avoid_when": "缺少搜索词级订单、自然位跟踪、广告位位置和 CVR 数据。",
        "required_data": ["广告目标", "自然排名目标", "关键词类型", "广告位", "CTR", "CVR", "订单量", "自然排名", "搜索词报告"],
        "keywords": ["广告出单", "自然排名", "广告位", "CTR", "CVR", "订单", "中小词", "大词", "organic_rank"],
    },
    {
        "conflict_title": "中小词出单 vs 大词自然排名目标",
        "view_a": "中小词出单能带来订单和权重，应该继续做。",
        "view_b": "中小词出单不一定能推动大词自然排名，大词仍需要单独预算和节奏。",
        "why_conflict_exists": "中小词和大词的搜索意图、竞争强度、订单权重和流量规模不同。",
        "decision_rule": "中小词负责利润和基础转化，大词负责战略排名。若目标是大词自然位，需单独跟踪大词广告位、点击、CVR、订单和自然位；不要用中小词 ACOS 代替大词排名进度。",
        "applies_when": "广告出单集中在长尾/中小词，但业务目标是核心大词首页。",
        "avoid_when": "预算不足以支撑大词测试、链接在大词下竞争力不足、库存和毛利无法承压。",
        "required_data": ["关键词类型", "预算", "广告目标", "自然排名目标", "CPC", "CVR", "订单量", "自然排名"],
        "keywords": ["中小词", "大词", "长尾词", "核心词", "自然排名", "关键词", "订单"],
    },
    {
        "conflict_title": "广告依赖 vs 活动流量补充",
        "view_a": "广告依赖高说明流量结构脆弱，需要降低广告占比。",
        "view_b": "广告依赖严重时，可以用秒杀、活动或其他流量补充来积累权重和订单。",
        "why_conflict_exists": "降低广告和补充活动都可能改善流量结构，但适用条件取决于毛利、库存、转化率和阶段目标。",
        "decision_rule": "先判断广告依赖是成本问题还是流量入口单一问题。若毛利不足、TACOS 高且自然单不动，应降广告和重构词；若库存充足、CVR 合格但流量入口少，可用活动流量补充，但必须复盘活动后自然排名和自然单。",
        "applies_when": "广告单占比高、自然流量弱、链接需要额外转化数据或活动承接。",
        "avoid_when": "库存不足、活动亏损不可承受、链接 CVR 差、活动后无法追踪自然排名变化。",
        "required_data": ["产品阶段", "毛利", "预算", "库存压力", "广告目标", "自然排名目标", "广告单占比", "自然单占比", "CVR", "TACOS"],
        "keywords": ["广告依赖", "广告单占比", "活动", "秒杀", "自然流量", "CVR", "TACOS"],
    },
]


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules-file", type=Path, default=DEFAULT_RULES_FILE)
    parser.add_argument("--cases-file", type=Path, default=DEFAULT_CASES_FILE)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_FILE)
    parser.add_argument("--register-file", type=Path, default=DEFAULT_REGISTER_FILE)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load JSONL rows."""
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
    """Write JSONL rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def searchable_rule_text(rule: dict[str, Any]) -> str:
    """Flatten a rule for keyword matching."""
    parts = [
        rule.get("topic", ""),
        rule.get("condition", ""),
        rule.get("recommended_action", ""),
        rule.get("metric_threshold", ""),
        rule.get("reasoning", ""),
        rule.get("limitations", ""),
        " ".join(rule.get("tags", [])),
    ]
    for source in rule.get("supporting_sources", []) + rule.get("opposing_sources", []):
        parts.append(source.get("evidence_quote", ""))
    return " ".join(parts).lower()


def searchable_case_text(case: dict[str, Any]) -> str:
    """Flatten a case for keyword matching."""
    return " ".join(
        [
            case.get("case_title", ""),
            case.get("case_topic", ""),
            json.dumps(case.get("case_metrics", {}), ensure_ascii=False),
            case.get("problem", ""),
            case.get("evidence_quote", ""),
        ]
    ).lower()


def score_text(text: str, keywords: list[str]) -> int:
    """Score keyword overlap."""
    lowered = text.lower()
    return sum(1 for keyword in keywords if keyword.lower() in lowered)


def related_rules(rules: list[dict[str, Any]], keywords: list[str], limit: int = 20) -> list[dict[str, Any]]:
    """Find related rules by keyword overlap."""
    scored = [
        (score_text(searchable_rule_text(rule), keywords), rule)
        for rule in rules
    ]
    return [rule for score, rule in sorted(scored, key=lambda item: (-item[0], item[1]["rule_id"])) if score > 0][:limit]


def related_cases(cases: list[dict[str, Any]], keywords: list[str], limit: int = 12) -> list[dict[str, Any]]:
    """Find related cases by keyword overlap."""
    scored = [
        (score_text(searchable_case_text(case), keywords), case)
        for case in cases
    ]
    return [case for score, case in sorted(scored, key=lambda item: (-item[0], item[1]["case_id"])) if score > 0][:limit]


def supporting_sources_from(rules: list[dict[str, Any]], cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build compact supporting source references."""
    sources: list[dict[str, Any]] = []
    for rule in rules[:6]:
        for source in rule.get("supporting_sources", [])[:2]:
            sources.append(
                {
                    "rule_id": rule["rule_id"],
                    "source_id": source.get("source_id", ""),
                    "record_id": source.get("record_id", ""),
                    "evidence_quote": source.get("evidence_quote", ""),
                    "confidence": source.get("confidence", ""),
                }
            )
    for case in cases[:4]:
        sources.append(
            {
                "case_id": case["case_id"],
                "source_id": case["source_id"],
                "evidence_quote": case.get("evidence_quote", ""),
                "confidence": case.get("confidence", "case_data"),
            }
        )

    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for source in sources:
        key = json.dumps(source, ensure_ascii=False, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        unique.append(source)
    return unique


def build_conflicts(rules: list[dict[str, Any]], cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build conflict candidates from templates and local evidence."""
    conflicts: list[dict[str, Any]] = []
    for index, spec in enumerate(CONFLICT_SPECS, start=1):
        matched_rules = related_rules(rules, spec["keywords"])
        matched_cases = related_cases(cases, spec["keywords"])
        confidence = "medium" if len(matched_rules) + len(matched_cases) >= 3 else "low"
        conflicts.append(
            {
                "conflict_id": f"C{index:03d}",
                "conflict_title": spec["conflict_title"],
                "view_a": spec["view_a"],
                "view_b": spec["view_b"],
                "why_conflict_exists": spec["why_conflict_exists"],
                "decision_rule": spec["decision_rule"],
                "applies_when": spec["applies_when"],
                "avoid_when": spec["avoid_when"],
                "required_data": spec["required_data"],
                "confidence": confidence,
                "related_rule_ids": [rule["rule_id"] for rule in matched_rules],
                "related_case_ids": [case["case_id"] for case in matched_cases],
                "supporting_sources": supporting_sources_from(matched_rules, matched_cases),
            }
        )
    return conflicts


def write_register(path: Path, conflicts: list[dict[str, Any]]) -> None:
    """Write Markdown conflict register."""
    lines = [
        "# Conflict Register",
        "",
        "This register stores conditional decision rules for common Amazon ads strategy conflicts. It does not declare one side universally correct.",
        "",
        "## Index",
        "",
        "| ID | Conflict | Confidence | Related Rules | Related Cases |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for conflict in conflicts:
        lines.append(
            f"| {conflict['conflict_id']} | {conflict['conflict_title']} | {conflict['confidence']} | "
            f"{len(conflict['related_rule_ids'])} | {len(conflict['related_case_ids'])} |"
        )

    for conflict in conflicts:
        lines.extend(
            [
                "",
                f"## {conflict['conflict_id']} {conflict['conflict_title']}",
                "",
                f"- View A: {conflict['view_a']}",
                f"- View B: {conflict['view_b']}",
                f"- Why conflict exists: {conflict['why_conflict_exists']}",
                f"- Conditional decision rule: {conflict['decision_rule']}",
                f"- Applies when: {conflict['applies_when']}",
                f"- Avoid when: {conflict['avoid_when']}",
                f"- Required data: {', '.join(conflict['required_data'])}",
                f"- Confidence: {conflict['confidence']}",
                f"- Related rule IDs: {', '.join(conflict['related_rule_ids']) if conflict['related_rule_ids'] else 'none'}",
                f"- Related case IDs: {', '.join(conflict['related_case_ids']) if conflict['related_case_ids'] else 'none'}",
                "",
                "### Evidence Notes",
                "",
            ]
        )
        if conflict["supporting_sources"]:
            for source in conflict["supporting_sources"][:8]:
                source_id = source.get("record_id") or source.get("case_id") or source.get("source_id", "")
                quote = source.get("evidence_quote", "")
                lines.append(f"- {source_id}: {quote}")
        else:
            lines.append("- No direct source match; keep as low-confidence framework until more records support it.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """Run conflict detection."""
    args = parse_args()
    rules = load_jsonl(args.rules_file)
    cases = load_jsonl(args.cases_file)
    conflicts = build_conflicts(rules, cases)
    write_jsonl(args.output_file, conflicts)
    write_register(args.register_file, conflicts)
    print(f"Wrote {len(conflicts)} conflicts to {args.output_file}")
    print(f"Wrote register to {args.register_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
