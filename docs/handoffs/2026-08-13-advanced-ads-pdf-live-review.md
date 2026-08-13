# 2026-08-13 进阶广告诊断 PDF 现场复核交接

## 任务

现场重新阅读 `C:\Users\liuya\Downloads\亚马逊专题课-进阶广告诊断有优化全指导.pdf`，验证现有 Skill 是否遗漏内容，并补入可追溯的主张、案例和交叉验证结论。

## 已完成

- 用 `pdfinfo` 确认 PDF 共 143 页、SHA-256 为 `3f75d0ed42cf8fd7e8818fa82beaf57d9d593cd01753a30b141e87054b7e86df`。
- 用 `pdftoppm -r 120 -png` 重新渲染 143/143 页，并完成全页接触表视觉检查。
- 确认 PDF 为图片型、无可用文本层；manifest 保留 `readable:false`，同时标记 `manual_reviewed:true`、`rendered_page_count:143` 和完整人工复核方法。
- 新增 18 条 PDF 专属原子主张：报告矩阵、父 ASIN 聚合、ACOS 分解、自动/商品投放、搜索词展示份额、特征词、否词阈值、广告位历史快照、小时切片、预算、ABA/POE、75% 相似度、变体、匹配类型和生命周期。
- 新增 4 条 PDF 来源忠实案例：四 SKU 座垫、特征词聚合、户外座垫关键词研究、生命周期阶段化示例。
- 通过 `review_sources.py` 校验：18 条 claim、4 条 case，validation errors 为 0；报告状态为 `PARTIAL`，原因仅是机器文本层不可读，未掩盖人工覆盖。
- 依据当前 Amazon 一手文档复核自动定向、Product Opportunity Explorer、搜索词/展示份额和广告位控制；PDF 的 2025-05 UI 描述标为 `outdated`，75% 相似度标为 `unsupported`，固定数字保留为 `context_dependent`。

## 产物

- `references/23_advanced_ads_pdf_live_review_2026-08-13.md`
- `data/processed/amazon_ads_skill/source_manifest_advanced_ads_pdf_live_2026-08-13.jsonl`
- `data/processed/amazon_ads_skill/advanced_ads_pdf_live_claims_2026-08-13.jsonl`
- `data/processed/amazon_ads_skill/claim_review_advanced_ads_pdf_live_2026-08-13.jsonl`
- `data/processed/amazon_ads_skill/advanced_ads_pdf_live_cases_input_2026-08-13.jsonl`
- `data/processed/amazon_ads_skill/source_case_records_advanced_ads_pdf_live_2026-08-13.jsonl`
- `data/processed/amazon_ads_skill/source_validation_report_advanced_ads_pdf_live_2026-08-13.md`

## 交接规则

同课 DOCX 改写与 PDF 属于同一 `evidence_cluster`，不得重复计票。后续回答命中 `PDFLIVE-*` 或 `SRC-3a9e4ddd5371-CASE-*` 时必须显示 `讲义案例提示`，说明页码、状态、匹配条件、不匹配、缺失数据和可逆验证窗口。任何 `outdated`、`unsupported` 或 `context_dependent` 内容都不能静默升级为 `merged_rules.jsonl` 无条件规则。

## 未完成/后续

- 本轮未把新的 PDF claims 合并进全量 781 条批次文件；它们保留在 PDF 专属层，避免在同一证据家族内重复计数。若用户要求再次全量合批，应先按 evidence cluster 去重再生成新批次。
- 未提交或推送 GitHub；等待用户明确要求后再按项目 Git 工作流提交。

