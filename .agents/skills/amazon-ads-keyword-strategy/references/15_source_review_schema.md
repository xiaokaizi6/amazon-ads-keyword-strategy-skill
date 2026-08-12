# Source Review Schema

本文件是 `scripts/review_sources.py` 的数据契约。它把来源盘点和主张审查变成可重复的文件流程，但不把文本自动分类器伪装成事实核查器。

## 1. 来源清单

输出：`data/processed/amazon_ads_skill/source_manifest.jsonl`

每行至少包含：

```json
{
  "source_id": "SRC-abc123",
  "file_name": "lecture.md",
  "file_path": "path/to/lecture.md",
  "title": "",
  "author_or_org": "unknown",
  "published_date": "",
  "acquired_date": "2026-08-12",
  "version": "",
  "source_type": "user_document",
  "marketplace": "unknown",
  "ad_products": [],
  "product_stages": [],
  "is_first_party": false,
  "evidence_cluster": "EC-abc123",
  "content_sha256": "",
  "byte_count": 0,
  "extension": ".md",
  "readable": true,
  "readability_issues": [],
  "included_in_scope": true
}
```

内容哈希相同的文件共享 `evidence_cluster`，不能被当成独立证据重复计票。不可读的 PDF、DOCX、图片或损坏文件仍要登记，但必须列出限制。

## 2. 主张输入与审查输出

输入和输出均为 JSONL。输入可以由 Codex 在阅读文件后创建，也可以由用户提供；原文文件本身保持不变。

每条主张至少需要：

```json
{
  "claim_id": "CLM-001",
  "source_id": "SRC-abc123",
  "source_location": "lecture.md#第3节",
  "evidence_quote": "不超过必要上下文的原文摘录",
  "normalized_claim": "可独立判断的主张",
  "claim_type": "causal_mechanism",
  "conditions": [],
  "time_sensitivity": "unknown",
  "status": "unresolved",
  "confidence": "low",
  "checked_source_ids": ["SRC-abc123"],
  "supporting_evidence": [],
  "opposing_evidence": [],
  "missing_evidence": ["需要同类目账户数据"],
  "verification_test": "定义一个限时、可逆的测试",
  "reviewed_at": "2026-08-12"
}
```

`supporting_evidence`、`opposing_evidence` 和 `checked_source_ids` 可以放字符串 source ID，也可以放带 `source_id` 的对象。脚本会校验来源是否存在、是否可读，并计算整体覆盖率。

## 3. 状态约束

- `confirmed_error` 必须同时提供反对证据和验证测试；没有直接反证时改为 `unsupported`、`disputed` 或 `unresolved`。
- `disputed`、`context_dependent`、`unresolved` 必须提供缺失证据或下一步验证测试。
- `supported` 也必须保留适用条件和来源，不代表所有类目或阶段都适用。
- 覆盖报告的 `PASS` 只表示清单中的来源已覆盖且主张契约无错误，不表示脚本自动证明了主张真实。
- 没有 claims 输入时报告为 `NOT_READY`，不生成空的 `claim_review.jsonl`。

## 4. 输出报告

`source_validation_report.md` 必须包含：来源总数、可读数、主张数、已检查来源数、未检查来源 ID、不可读来源 ID、验证错误数、主张状态计数和整体状态。

状态含义：

- `PASS`：有主张、来源全覆盖、没有契约错误或不可读来源。
- `PARTIAL`：有主张但仍有未覆盖或不可读来源。
- `FAIL`：存在主张契约错误，例如未知来源或不合格的 `confirmed_error`。
- `NOT_READY`：尚未提供主张文件，只完成来源盘点。

## Common Mistakes

- 把相同内容的转载当作多个独立来源。
- 只登记来源而声称主张已验证。
- 用缺少支持的主张直接填 `confirmed_error`。
- 把不可读文件静默排除。
- 在覆盖率为 `PARTIAL` 或 `NOT_READY` 时写成全部资料已检查。

## Quality Checklist

- 每个来源有哈希、稳定 ID、证据簇和可读性状态。
- 每条主张都有原文位置和来源 ID。
- 支持证据、反对证据、缺失证据和验证测试分开。
- `confirmed_error` 有直接反证。
- 报告明确列出未覆盖和不可读来源。
- 没有 claims 文件时不生成虚假的空审查结果。
