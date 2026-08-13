# 全量统一批次交接（2026-08-13）

## 目标

按用户要求，把项目 100 篇文章和本次对话出现的全部新资料放入同一批次，逐条登记、原子化审查、保留案例，并把争议、未决、证据不足、过时和条件化内容继续留在 Skill 知识库中。

## 已完成

- 新增并运行 `.agents/skills/amazon-ads-keyword-strategy/scripts/build_full_batch_audit.py`。
- 使用 `review_sources.py --manifest-input` 对混合来源清单执行统一 schema、引用覆盖和案例契约校验。
- 生成 108 个来源：100 个 `project_corpus` + 8 个 `user_document`（含原始课程 PDF）。
- 生成并审查 781 条主张：项目文章 694 条（含 100 条来源覆盖记录），用户文件 87 条（86 条原子主张 + 1 条原始 PDF 来源覆盖记录）。
- 生成并校验 36 条来源案例：案例契约错误 0。
- 所有 108 个来源均有引用记录，未引用来源 0，主张契约错误 0。
- A069 没有规范化抽取记录，已保留一条 `manual_coverage_fallback` 未决项，避免把缺失记录误判为空内容。
- 8 个二进制用户文件已在前序批次完成 OOXML/XLSX/PDF 提取或页面图像检查；统一 manifest 以 `readable: false` 表示默认解析器限制，以 `manual_reviewed: true` 表示人工已读。

## 结果

统一报告：`data/processed/amazon_ads_skill/source_validation_report_full_batch_2026-08-13.md`

| 状态 | 数量 |
|---|---:|
| supported | 131 |
| context_dependent | 187 |
| disputed | 25 |
| unresolved | 204 |
| unsupported | 227 |
| outdated | 3 |
| confirmed_error | 4 |

报告状态是 `PARTIAL`，原因只有默认自动读取器不解析 8 个 DOCX/XLSX/PDF。报告同时记录机器可读 100、人工已读 8、可审查 108；不能把 `PARTIAL` 解读为用户资料没有阅读，也不能解读为全部业务主张已被官方证明。

## 交叉验证决定

- 低时效数学定义和有独立证据的定义类主张可以 `supported`；CTR/CVR/ACOS 健康值、TOS 溢价、预算倍增、固定测试天数、广告位导致自然排名等保持条件化或未决。
- 划线价/参考价内容按 Amazon 当前参考价公告处理，不把人为抬价制造折扣锚点写成打法。
- 返现换评、review club、虚假订单、补偿买家、刷销量/销售排名和人为流量等保留为 `confirmed_error` 风险证据，只能用于风险提示，不能提供执行或规避步骤。
- Sponsored Products 否定投放的“至少 20 次点击评估、改动后观察至少两周”是具体平台建议，不推导 TOS 100%–200%/900% 或自然排名保证。
- 重复改述的进阶诊断资料按同一证据家族处理，不重复计票；其案例仍保留来源链和差异说明。

## 交接要求

后续回答命中本批次 claim 或案例时，必须主动提示 `来源状态`/案例置信度、适用条件、关键不匹配、缺失数据、可逆验证窗口、成功标准和停止标准。`disputed`、`unresolved`、`unsupported`、`outdated`、`context_dependent` 仍是 Skill 知识库内容，但不得直接写入 `merged_rules.jsonl` 作为无条件规则。

## 验证命令

```powershell
python .agents/skills/amazon-ads-keyword-strategy/scripts/build_full_batch_audit.py
python .agents/skills/amazon-ads-keyword-strategy/scripts/review_sources.py --manifest-input data/processed/amazon_ads_skill/source_manifest_full_batch_2026-08-13.jsonl --manifest-output data/processed/amazon_ads_skill/source_manifest_full_batch_2026-08-13.jsonl --claims-file data/processed/amazon_ads_skill/full_batch_claims_2026-08-13.jsonl --claim-output data/processed/amazon_ads_skill/full_batch_claim_review_2026-08-13.jsonl --cases-file data/processed/amazon_ads_skill/full_batch_cases_2026-08-13.jsonl --case-output data/processed/amazon_ads_skill/full_batch_case_records_2026-08-13.jsonl --report-output data/processed/amazon_ads_skill/source_validation_report_full_batch_2026-08-13.md
python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py
python C:\Users\liuya\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/amazon-ads-keyword-strategy
git diff --check
```

## 未完成/边界

本批次完成的是全量来源登记、逐条结构化审查和证据状态保留，不是 781 条主张逐条得到 Amazon 官方背书。后续若有官方帮助页、账户报告或可复现实验，应更新对应 claim 的证据和状态，而不是删除来源观察或把条件化案例改成通用规则。
