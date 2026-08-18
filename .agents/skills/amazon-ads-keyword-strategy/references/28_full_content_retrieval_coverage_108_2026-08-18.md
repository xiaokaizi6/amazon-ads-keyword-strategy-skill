# 108 份资料全文检索覆盖审计（2026-08-18）

## 结论与边界

- 审计范围：`assets/knowledge/portable_108_source_manifest.jsonl` 的 108 个来源，即 100 篇项目文章和 8 份用户资料。
- 审计结果：`assets/knowledge/full_content_coverage_108_2026-08-18.jsonl` 逐源校验为 108/108 `available_with_source_boundaries`，0 个检索覆盖缺口。
- 这表示每个原件都保留在 `assets/source_materials/`，并具有对应的全文、结构化单元格或逐页/逐图检索层；不表示每条讲义观点已获事实证明，也不将 OCR 当成原件权威。
- 详细案例背景索引：`assets/knowledge/portable_case_background_index_2026-08-18.jsonl`，48 条唯一案例（全量批次 36 条、CPC 原件 8 条、原 PDF 4 条）；每条保留来源位置、指标、观察、作者解释、动作/未知项和交叉验证边界。

## 逐类覆盖

| 来源 | 可检索内容层 | 审计量 |
|---|---|---:|
| 100 篇项目 Markdown 文章 | 原始 Markdown + `article_sections.jsonl` | 2,002 个分段记录 |
| CPC 广告打法 Word | `cpc_playbook_full_content_2026-08-17.jsonl` | 168 个正文/表格节点 |
| 143 页进阶广告诊断 PDF | `advanced_ads_pdf_ocr_full_2026-08-18.jsonl` | 143 页 OCR 记录 |
| 进阶诊断文字整理版 Word | `advanced_ads_text_arrangement_docx_full_content_2026-08-18.jsonl` | 194 个正文/表格节点 |
| 进阶诊断文字改述版 Word | `advanced_ads_paraphrase_docx_full_content_2026-08-18.jsonl` | 79 个正文/表格节点 |
| 广告报告高效分析 Word | 图片 OCR | 12 张嵌入图 |
| 2025 划线价玩法 Word | 正文/表格 + 图片 OCR | 64 个节点 + 11 张图 |
| 折扣与促销 Excel | 全部非空单元格 + 图片 OCR | 1,097 个单元格 + 1 张图 |
| 新品推广流程 Excel | 全部非空单元格 | 309 个单元格 |

## 回答时的检索顺序

1. 先按问题关键词搜索与问题最相关的全文层和 `portable_case_background_index_2026-08-18.jsonl`，不要只依赖规则摘要。
2. 命中案例时，给出案例 ID、产品/阶段/目标、条件、指标、观察结果、作者解释、当时动作和不能直接照搬的原因。
3. 命中 OCR 文本、图片、表格、公式或数字时，回查 `original_asset` 指向的原件并标记原件位置；低置信度 OCR 不得静默修正。
4. 未命中相似案例时，明确写 `未命中具体案例`，仍可说明已命中的来源背景和证据边界。
5. 每次结论只能列出实际命中的来源、位置和案例；108 份资料是检索背景，不是每条结论的共同证明。

## 可重复审计

运行 `scripts/build_full_content_coverage_audit.py`，以 portable manifest、文章分段层和各用户文件的正文/单元格/OCR 派生层重新生成覆盖 JSONL。脚本同时核对 Office 包中实际嵌入媒体数量与 OCR 记录数量；缺失原件、文章分段、PDF 页 OCR、Office 正文或嵌入图片 OCR 时必须报告 `incomplete`。
