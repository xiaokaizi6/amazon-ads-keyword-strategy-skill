# 2026-08-19：30 种捡漏广告玩法 PDF 融入

## 目标与范围

将用户提供的《30种捡漏广告玩法(1).pdf》完整纳入项目和桌面 Codex Skill 的可检索证据包；保留原件、全文检索层、条件化主张、案例边界和后续回答契约。范围不包括把讲义数值直接变成广告账户动作，也不包括提交或发布。

## 实际完成

- 原件复制为 `assets/source_materials/30种捡漏广告玩法.pdf`，SHA-256：`4c37c63ff3a0d206ab55bd824adee732b906eb8423103120032e0482f8daefad`。
- 用 Poppler 将 7 页渲染为 140 dpi 页面，逐页视觉阅读；用 RapidOCR 生成 7 页、156 行的 `30_ad_tactics_pdf_ocr_full_2026-08-19.jsonl`，以及 OCR 搜索 Word 派生件。
- 建立单来源 manifest、8 条原子主张、0 条来源忠实案例输入与审查报告。报告 `PARTIAL` 的唯一系统性原因是默认 manifest 不解析 PDF 二进制；页面阅读和 OCR 检索层已完成，不能将 `PARTIAL` 解释为未读或主张已获证明。
- 新建 `references/29_30_ad_tactics_integration_2026-08-19.md`，并修改 Skill、来源索引、T063 eval 和预期输出契约。
- 生成 109 来源便携 manifest 与全文覆盖审计：100 篇项目文章 + 9 份用户文件，109/109 `available_with_source_boundaries`。案例背景索引保留 48 条，因为此 PDF 没有账户案例、指标、时间窗或对照组。

## 来源、结论与边界

- 文内“阿波罗提供”仅是自述，身份、站点、账户、发布日期和绩效均未独立核验。
- PDF 标题称“30种”，原件只定位到 28 个编号玩法和末尾错拼词补充；`T30-CLM-008` 为 `unresolved`，没有补造第 29/30 项。
- 自动投放四个默认组、竞价策略、商品/关键词定向等平台机制在 2026-08-19 由 Amazon Ads 一手资料复核；该复核不证明讲义中 `0.02`、`0.2`、平均 CPC 比例、TOS `900%`、预算或“必然低成本/出单”的效果。
- 玩法的固定数值为 `unsupported`；活动拆分、搜索词迁移、自动四组和 SP→SB/SD 扩展为 `context_dependent`；无订单词增投/止损为 `disputed`；跳过相关性筛选为 `unsupported`。后续答复必须给页码/claim、条件、缺失数据和可逆验证方式。
- 本资料没有来源忠实账户案例，后续匹配它时需明确：`是否命中上传案例：未命中具体案例（本资料 0 条案例）`。

## 修改文件

- 原件和 Skill 可检索资产：`assets/source_materials/30种捡漏广告玩法.pdf`、`assets/derivatives/30种捡漏广告玩法-OCR文字检索版.docx`、`assets/knowledge/*30_ad_tactics*`、`portable_109_source_manifest_2026-08-19.jsonl`、`full_content_coverage_109_2026-08-19.jsonl`、`portable_case_background_index_109_2026-08-19.jsonl`。
- 处理层：`data/processed/amazon_ads_skill/*30_ad_tactics*`、对应 manifest/claim review/report。
- 规则与测试：`SKILL.md`、`references/11_source_index.md`、`references/29_30_ad_tactics_integration_2026-08-19.md`、`evals/test_cases.jsonl`、`evals/expected_outputs.md`。
- 交接：本文件和 `docs/CODEX_HANDOFF.md`。

## 验证

- `ocr_pdf_to_searchable_docx.py`：PASS，7 页、156 OCR 行。
- `review_sources.py --manifest-input ... --claims-file ... --cases-file ...`：PASS，8 条主张，0 条案例，报告状态 `PARTIAL`（正确保留 PDF 默认二进制边界）。
- `build_portable_evidence_manifest.py`：PASS，1/1 新增原件的 SHA-256 可定位且无缺失/歧义。
- `build_full_content_coverage_audit.py`：PASS，新增来源 1/1 可检索；组合清单为 109 行。
- Amazon Ads 官方资料核对：已运行，核对日期 2026-08-19；只用于当前平台机制和相关性边界。
- `validate_outputs.py`：PASS，0 errors、0 warnings；JSONL、source-review、eval、references 和 Skill 结构均通过。
- 109 来源清单的自定义断言：PASS，109 个唯一 source ID、109/109 检索状态、8 条新增主张零契约错误、T063 唯一。
- 桌面安装副本同步：PASS，18/18 新增/变更文件 SHA-256 一致；桌面副本的 109 来源便携包完整性错误为 0。
- `git diff --check`：PASS（仅 Git CRLF 转换警告）。

## 风险与下一步

- 不要把 OCR 文本、标题数量、作者的数字或“适用场景”当作原件以外的事实或账户案例；精确数字和低置信度 OCR 必须回查 PDF 原页。
- 若用户要求当前竞价、预算、否词、竞品或放量动作，须先加载对应 Skill reference；涉及当前市场/竞品/关键词数据时遵守西柚洞察 MCP 决策门槛。
- 已完成桌面安装副本同步；除非用户再次明确授权，不 commit/push。
