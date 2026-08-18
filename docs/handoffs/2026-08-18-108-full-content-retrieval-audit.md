# 108 份资料全文检索与案例背景审计

## 目标

确认 100 篇项目文章和 8 份用户资料不是仅被打包保存，而是均能被后续 Skill 检索；为命中问题提供可回溯的详细案例背景。

## 已完成

- 生成 4 份上传 Word 的正文/表格 JSONL、2 份 Excel 的全部非空单元格 JSONL，以及实际存在的 24 张 Word/Excel 嵌入图 OCR JSONL。
- 保留既有 100 篇文章 2,002 个分段、CPC Word 168 节点和原 PDF 143 页 OCR；原始文件未改写。
- 新增逐源覆盖审计 `full_content_coverage_108_2026-08-18.jsonl`：108/108 `available_with_source_boundaries`，0 个缺口。
- 新增去重案例背景索引 `portable_case_background_index_2026-08-18.jsonl`：48 条案例，保留来源位置、条件/指标、观察、作者解释、动作/unknown 和交叉验证边界。
- 新增引用说明 `references/28_full_content_retrieval_coverage_108_2026-08-18.md`、Skill `18k` 和 T062 eval，要求回答先检索全文层与案例索引，再给出实际证据。

## 修改文件及原因

- `scripts/export_xlsx_source_content.py`：导出全部非空 Excel 单元格及公式。
- `scripts/ocr_office_embedded_media.py`：OCR DOCX/XLSX 嵌入媒体；对不可 OCR 媒体保留可回查记录。
- `scripts/build_full_content_coverage_audit.py`、`scripts/build_case_background_index.py`：使覆盖和案例聚合可重复验证。
- `assets/knowledge/*_full_content_2026-08-18.jsonl`、`*_embedded_media_ocr_2026-08-18.jsonl`、`full_content_coverage_108_2026-08-18.jsonl`、`portable_case_background_index_2026-08-18.jsonl`：完整检索层与审计结果。
- `SKILL.md`、`references/11_source_index.md`、`references/28_full_content_retrieval_coverage_108_2026-08-18.md`、`evals/*`：将检索与详细案例背景写入后续回答契约。

## 来源与置信度

- 覆盖范围以 `portable_108_source_manifest.jsonl` 为准：100 个 `project_corpus`、8 个 `user_document`。
- 原件是内容权威。文本/单元格导出为来源忠实检索层；PDF 与嵌入图片 OCR 是机器派生层，图表、数字、公式、专名和低置信度文本需回查原件。
- “108/108 可检索”只证明资料与检索层完整，不证明所有课程观点、阈值或案例因果已被验证。

## 验证结果

- Python 覆盖/案例断言：`PASS`（108/108，100+8，48 唯一案例，派生 JSONL 可解析）。
- `python C:\Users\liuya\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/amazon-ads-keyword-strategy`：`PASS`。
- eval JSONL 唯一 ID/T062 检查：`PASS`（62 条）。
- `git diff --check`：`PASS`（仅 CRLF 警告）。
- 桌面安装副本同步：20/20 本轮文件 SHA-256 一致；其覆盖清单的 108/108 原件和检索层路径均可定位，48 条案例唯一；桌面副本 `quick_validate.py`：`PASS`。

## 风险与下一步

- Word 视觉渲染 QA 仍受缺少 LibreOffice/`soffice` 阻塞，未在本任务重试；与内容检索审计分开。
- 回答具体业务问题时只引用实际命中的来源/案例。没有相似案例时写 `未命中具体案例`，并给出资料背景和适用边界。
