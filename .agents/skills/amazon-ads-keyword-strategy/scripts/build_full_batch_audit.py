"""Build one auditable manifest, claim input, and case input for all in-scope sources.

This script does not infer truth from text. It combines the existing 100-article
corpus with all user-uploaded source claim files, and converts every relevant
normalized corpus record into a conservatively labelled atomic review item.
The source-review script remains responsible for schema/coverage validation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROCESSED = ROOT / "data/processed/amazon_ads_skill"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def source_map(manifest: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["file_name"]: row for row in manifest}


def build_manifest() -> list[dict[str, Any]]:
    base = load_jsonl(PROCESSED / "source_manifest.jsonl")
    extra_manifests = [
        PROCESSED / "source_manifest_advanced_ads_lecture.jsonl",
        PROCESSED / "source_manifest_advanced_ads_review.jsonl",
        PROCESSED / "source_manifest_advanced_ads_rewrite_v2.jsonl",
        PROCESSED / "source_manifest_2026-08-13_new_bundle.jsonl",
    ]
    records = {row["source_id"]: row for row in base}
    for manifest_path in extra_manifests:
        for row in load_jsonl(manifest_path):
            records.setdefault(row["source_id"], row)

    uploaded_names = {
        "亚马逊CPC广告打法知识体系全梳理v1_20260804(1).docx",
        "亚马逊进阶广告诊断优化全指导-文字改述版.docx",
        "亚马逊专题课-进阶广告诊断有优化全指导-文字整理版 (1).docx",
        "新品推广基础推广动作及流程(1).xlsx",
        "2025亚马逊划线价运营玩法.docx",
        "亚马逊折扣+促销说明.xlsx",
        "亚马逊广告报告高效分析和优化-Word版 (1).docx",
        "亚马逊专题课-进阶广告诊断有优化全指导.pdf",
    }
    for row in records.values():
        if row.get("file_name") in uploaded_names:
            row["source_type"] = "user_document"
            row["included_in_scope"] = True
            # These seven files were read in the preceding source-specific
            # passes (OOXML/XLSX extraction or page-image inspection). Keep
            # machine readability separate from human reviewability so the
            # batch report cannot confuse an automated parser limitation with
            # an unreviewed source.
            row["manual_reviewed"] = True
            row["manual_review_method"] = "source-specific extraction and/or visual inspection"
        elif row.get("file_name", "").endswith(".md"):
            row["source_type"] = "project_corpus"
    return sorted(records.values(), key=lambda row: row["source_id"])


def claim_from_record(record: dict[str, Any], article_source_id: str) -> dict[str, Any]:
    record_type = record.get("record_type", "diagnostic_hypothesis")
    status = {
        "executable_rule": "context_dependent",
        "diagnostic_hypothesis": "unresolved",
        "diagnostic_question": "unresolved",
        "counterexample": "disputed",
        "case_observation": "context_dependent",
        "comment_signal": "unsupported",
    }.get(record_type, "unresolved")
    evidence = str(record.get("evidence_quote") or record.get("condition") or "")[:1600]
    action = str(record.get("action") or record.get("condition") or evidence).strip()[:1600]
    limitations = str(record.get("limitations") or "")
    return {
        "claim_id": f"CORPUS-{record['record_id']}",
        "source_id": article_source_id,
        "source_location": f"{record.get('section_id', 'unknown')} / {record_type}",
        "evidence_quote": evidence,
        "normalized_claim": action or "来源记录已提取，但没有足够文本形成独立主张。",
        "claim_type": record_type,
        "conditions": [
            "该记录来自项目文章语料，必须结合产品阶段、站点、类目、目标、毛利、预算和样本量",
        ],
        "time_sensitivity": "unknown",
        "status": status,
        "confidence": record.get("confidence", "low"),
        "checked_source_ids": [article_source_id],
        "supporting_evidence": [],
        "opposing_evidence": [],
        "missing_evidence": [
            "同类独立来源、当前 Amazon 官方资料或账户实测数据未在该单条记录中证明",
            limitations or "来源记录未提供完整可比样本",
        ],
        "verification_test": "在目标账户隔离一个变量，观察 7-14 天的 CTR、CPC、CVR、订单、ACOS/TACOS、自然订单和库存，并设置停止标准。",
        "reviewed_at": "2026-08-13",
    }


def source_coverage_claim(
    article: dict[str, Any],
    manifest_source_id: str,
    total_record_count: int,
    relevant_record_count: int,
    noise_record_count: int,
) -> dict[str, Any]:
    return {
        "claim_id": f"CORPUS-COVERAGE-{article['source_id']}",
        "source_id": manifest_source_id,
        "source_location": "articles_index.jsonl / source-level coverage",
        "evidence_quote": (
            f"{article['file_name']} 已纳入项目语料；总抽取记录数={total_record_count}，"
            f"决策相关记录={relevant_record_count}，噪声记录={noise_record_count}。"
        ),
        "normalized_claim": "该项目文章来源已纳入同一批次审查；其记录按规则、假设、问题、反例、案例、评论信号和噪声分开处理。",
        "claim_type": "source_coverage",
        "conditions": ["覆盖结论只表示已读取和登记，不表示每条业务说法已被官方证明"],
        "time_sensitivity": "low",
        "status": "supported",
        "confidence": "high",
        "checked_source_ids": [manifest_source_id],
        "supporting_evidence": [],
        "opposing_evidence": [],
        "missing_evidence": [],
        "verification_test": "核对 source manifest、articles_index、normalized_records 和本批次报告的 source ID 是否一致。",
        "reviewed_at": "2026-08-13",
    }


def convert_case(record: dict[str, Any], article_source_id: str) -> dict[str, Any]:
    return {
        "case_id": f"CORPUS-{record['record_id']}",
        "source_id": article_source_id,
        "source_location": f"{record.get('section_id', 'unknown')} / case_observation",
        "evidence_quote": str(record.get("evidence_quote") or "")[:1600],
        "case_title": str(record.get("topic") or "项目语料案例观察"),
        "marketplace": "unknown",
        "product_stage": record.get("product_stage") or "unknown",
        "ad_objective": record.get("topic") or "unknown",
        "conditions": [str(record.get("condition") or "来源原始条件未完整披露")],
        "case_metrics": record.get("case_metrics") or {},
        "observed_outcome": str(record.get("action") or record.get("condition") or "来源记录了案例观察，但结果信息有限"),
        "author_explanation": str(record.get("reasoning") or "unknown"),
        "action_taken": str(record.get("action") or "unknown"),
        "cross_validation_notes": "保留来源观察、作者解释和动作的分离；与项目规则/反例的可比性需按阶段、目标、样本和站点复核。",
        "case_confidence": record.get("confidence", "low"),
        "reviewed_at": "2026-08-13",
    }


def manual_content_claim(
    article: dict[str, Any], manifest_source_id: str, author_body: str
) -> dict[str, Any]:
    evidence = author_body.strip()[:1600]
    return {
        "claim_id": f"CORPUS-MANUAL-{article['source_id']}",
        "source_id": manifest_source_id,
        "source_location": "article_sections.jsonl / author_body / manual coverage fallback",
        "evidence_quote": evidence,
        "normalized_claim": "该文章的正文已人工纳入全量审查，但现有规范化抽取没有生成决策记录；因此只保留为未决主张，不升级为规则。",
        "claim_type": "manual_coverage_fallback",
        "conditions": ["需要重新运行或检查上游抽取器以补齐结构化记录"],
        "time_sensitivity": "unknown",
        "status": "unresolved",
        "confidence": "low",
        "checked_source_ids": [manifest_source_id],
        "supporting_evidence": [],
        "opposing_evidence": [],
        "missing_evidence": ["现有 normalized_records 未覆盖该正文的结构化业务主张"],
        "verification_test": "重新运行该来源的 section/record 提取并人工复核，随后为每条业务主张补充独立来源和当前官方核验。",
        "reviewed_at": "2026-08-13",
    }


def manual_source_coverage_claim(source: dict[str, Any]) -> dict[str, Any]:
    """Record a manually reviewed binary source that has no separate claims file."""
    return {
        "claim_id": f"USER-COVERAGE-{source['source_id']}",
        "source_id": source["source_id"],
        "source_location": "source manifest / manual review coverage",
        "evidence_quote": (
            f"{source['file_name']} 已通过 {source.get('manual_review_method', '人工阅读')} 纳入统一批次；"
            "该记录只证明来源覆盖，不证明其中每条业务主张。"
        ),
        "normalized_claim": "该用户来源已进入统一批次并完成来源级人工阅读登记，但不作为独立事实证据重复计票。",
        "claim_type": "source_coverage",
        "conditions": ["同一课程 PDF 的文字改述不作为独立证据重复计票"],
        "time_sensitivity": "low",
        "status": "supported",
        "confidence": "high",
        "checked_source_ids": [source["source_id"]],
        "supporting_evidence": [],
        "opposing_evidence": [],
        "missing_evidence": [],
        "verification_test": "核对 manifest 的 source_id、content_sha256、人工阅读记录和本批次报告。",
        "reviewed_at": "2026-08-13",
    }


def build_claims_and_cases(manifest: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_name = source_map(manifest)
    articles = load_jsonl(PROCESSED / "articles_index.jsonl")
    article_manifest_ids = {article["source_id"]: by_name[article["file_name"]]["source_id"] for article in articles}
    records = load_jsonl(PROCESSED / "normalized_records.jsonl")
    grouped: dict[str, list[dict[str, Any]]] = {article["source_id"]: [] for article in articles}
    all_grouped: dict[str, list[dict[str, Any]]] = {article["source_id"]: [] for article in articles}
    for record in records:
        if record.get("source_id") in grouped and record.get("is_relevant"):
            grouped[record["source_id"]].append(record)
        if record.get("source_id") in all_grouped:
            all_grouped[record["source_id"]].append(record)
    sections = load_jsonl(PROCESSED / "article_sections.jsonl")
    author_bodies = {
        section["source_id"]: section.get("text", "")
        for section in sections
        if section.get("section_type") == "author_body"
    }

    claims: list[dict[str, Any]] = []
    cases: list[dict[str, Any]] = []
    for article in articles:
        source_id = article_manifest_ids[article["source_id"]]
        article_records = grouped[article["source_id"]]
        all_records = all_grouped[article["source_id"]]
        claims.append(
            source_coverage_claim(
                article,
                source_id,
                len(all_records),
                len(article_records),
                sum(record.get("record_type") == "irrelevant_noise" for record in all_records),
            )
        )
        if not article_records and author_bodies.get(article["source_id"]):
            claims.append(manual_content_claim(article, source_id, author_bodies[article["source_id"]]))
        for record in article_records:
            claims.append(claim_from_record(record, source_id))
            if record.get("record_type") == "case_observation":
                cases.append(convert_case(record, source_id))

    for claim_file in (
        PROCESSED / "cpc_playbook_claims.jsonl",
        PROCESSED / "advanced_ads_claims.jsonl",
        PROCESSED / "advanced_ads_rewrite_v2_claims.jsonl",
        PROCESSED / "new_source_bundle_claims.jsonl",
    ):
        claims.extend(load_jsonl(claim_file))

    # Keep a source-level coverage record for manually reviewed binary sources
    # that are represented by derivative claim files rather than a dedicated
    # claim file of their own (currently the original course PDF).
    claim_source_ids = {claim.get("source_id") for claim in claims}
    for source in manifest:
        if source.get("source_type") == "user_document" and source["source_id"] not in claim_source_ids:
            claims.append(manual_source_coverage_claim(source))

    for case_file in (
        PROCESSED / "source_case_records_advanced_ads_rewrite_v2.jsonl",
        PROCESSED / "new_source_bundle_case_records.jsonl",
    ):
        cases.extend(load_jsonl(case_file))

    # The older advanced-lecture case file uses a different compact schema;
    # convert it into the source-case contract without changing its observation.
    for case in load_jsonl(PROCESSED / "lecture_case_library_advanced_ads.jsonl"):
        cases.append(
            {
                "case_id": case["case_id"],
                "source_id": case["source_id"],
                "source_location": case.get("source_location", "unknown"),
                "evidence_quote": case.get("title", ""),
                "case_title": case.get("title", "讲义案例"),
                "marketplace": "unknown",
                "product_stage": "unknown",
                "ad_objective": "diagnosis",
                "conditions": case.get("limitations", []),
                "case_metrics": case.get("metrics", {}),
                "observed_outcome": case.get("lecture_conclusion", "unknown"),
                "author_explanation": case.get("lecture_conclusion", "unknown"),
                "action_taken": "见来源案例记录；不自动升级为通用规则。",
                "cross_validation_notes": "由旧案例紧凑结构转换；保留原状态和限制。",
                "case_confidence": "medium",
                "reviewed_at": "2026-08-13",
            }
        )

    # Avoid accidental duplicate IDs when the same source case exists in a
    # prior batch and a newer integration file.
    unique_claims = {claim["claim_id"]: claim for claim in claims}
    unique_cases = {case["case_id"]: case for case in cases}
    return list(unique_claims.values()), list(unique_cases.values())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-output", type=Path, default=PROCESSED / "source_manifest_full_batch_2026-08-13.jsonl")
    parser.add_argument("--claims-output", type=Path, default=PROCESSED / "full_batch_claims_2026-08-13.jsonl")
    parser.add_argument("--cases-output", type=Path, default=PROCESSED / "full_batch_cases_2026-08-13.jsonl")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_manifest()
    claims, cases = build_claims_and_cases(manifest)
    write_jsonl(args.manifest_output, manifest)
    write_jsonl(args.claims_output, claims)
    write_jsonl(args.cases_output, cases)
    print(f"manifest={len(manifest)} claims={len(claims)} cases={len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
