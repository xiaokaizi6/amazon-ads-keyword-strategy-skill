# 2026-08-17 Full Source Assets And Cases

## 目标

将用户重新提供的 CPC Word 与 143 页进阶广告诊断 PDF 的完整原件、案例和作者思路纳入可移植 Amazon Ads Skill；不能只保留最终结论，也不能把讲义观察升级为通用广告规则。

## 实际完成

- 将两份未改写原件置于 `.agents/skills/amazon-ads-keyword-strategy/assets/source_materials/`，并核对 SHA-256：CPC Word 为 `123d25a4a09a3580fbe39aa183c86420c76e403283cf257fc1f8c11005de6693`，PDF 为 `3f75d0ed42cf8fd7e8818fa82beaf57d9d593cd01753a30b141e87054b7e86df`。
- 新增 `export_docx_source_content.py`，从 Word Open XML 导出 168 个正文节点（142 段、26 表）到 `cpc_playbook_full_content_2026-08-17.jsonl`，保留节点顺序和原始表格单元格内容。
- 新增 8 条 CPC 来源忠实案例；每条分开保存来源观察、作者解释、实际动作、指标、可比性边界和案例置信度。
- 新增 `references/26_full_source_materials.md` 与 T058 eval，要求引用时列明具体 Word 节点或 PDF 页码/claim/case，并区分来源观察、作者思路/解释和审查状态。
- 将完整原件和检索用 JSONL 层同步到桌面安装副本 `C:\Users\liuya\.codex\skills\ads_skill\skills\amazon-ads-keyword-strategy`；项目文件没有缺失，两个桌面原件哈希一致。

## 修改文件及原因

- `.agents/skills/amazon-ads-keyword-strategy/assets/`：完整原件与可移植检索层。
- `.agents/skills/amazon-ads-keyword-strategy/scripts/export_docx_source_content.py`：不依赖外部 Word 库的完整正文/表格导出。
- `.agents/skills/amazon-ads-keyword-strategy/references/26_full_source_materials.md`、`SKILL.md`、`references/11_source_index.md`：增加原件读取入口、证据分层与产物索引。
- `data/processed/amazon_ads_skill/*cpc_playbook*2026-08-17*`：来源清单、全文节点、案例输入/输出、claim review 与报告。
- `evals/test_cases.jsonl`、`evals/expected_outputs.md`：覆盖完整来源、案例和作者思路的回答契约。

## 来源与置信度

- 两个二进制原件为用户提供的讲义，均非 Amazon 官方来源。
- CPC 完整节点和案例是来源忠实保留；其 21 条原子主张状态沿用既有审查（supported 13、context_dependent 1、disputed 1、unresolved 5、unsupported 1）。
- PDF 的 18 条页码主张和 4 条案例沿用既有 143/143 页现场审查。与同课文字改述同属一证据家族，不能重复计票。

## 验证

- `python .../export_docx_source_content.py ...`：PASS，168 节点。
- 节点连续性检查：PASS，142 段、26 表、0 空内容。
- `review_sources.py --manifest-input ... --claims-file ... --cases-file ...`：PARTIAL；21 条 claim 与 8 条案例均为 0 契约错误，`PARTIAL` 仅因 DOCX 默认读取器不可读而非人工未读。
- `validate_outputs.py`：PASS；该脚本会重写默认清单/报告，已恢复其历史内容，未将该副作用纳入任务修改。
- 项目与桌面 Skill 的 `quick_validate.py`：PASS。
- 原件 SHA-256 与桌面同步哈希：PASS。
- `git diff --check`：PASS。
- Documents Skill Word 渲染：BLOCKED，运行时缺少 `pdf2image`；未将视觉渲染写为通过。

## 风险与下一步

- 原始 PDF 约 150 MB；提交、发布或再分发前先确认远端大文件和包体积策略。
- 当前桌面包携带这两份完整原件与检索层；若要把所有 100 篇项目文章及其余 6 个上传文件也做成完全离线可检索包，应另开范围明确的打包任务。
