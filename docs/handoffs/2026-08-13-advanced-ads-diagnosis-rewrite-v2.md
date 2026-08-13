# 2026-08-13 进阶广告诊断文字整理版（1）整合交接

## 任务

完整阅读并学习 `C:\Users\liuya\Downloads\亚马逊专题课-进阶广告诊断有优化全指导-文字整理版 (1).docx`，与项目语料、既有讲义和当前 Amazon 官方资料交叉验证；保留案例，标记条件化、未支持和未决内容，并在后续相关问答中主动提示。

## 阅读证据

- 文件 SHA-256：`4734b1a90fb07b7590e979f68b3aa5bdb70895cc225a0538c95f2d4e32151651`
- 解析方式：OOXML 完整读取 540 个非空段落、26 个表格、17,329 个字符；原文件未修改。
- 来源 ID：`SRC-3328e6e7662e`。
- 该文件与上一份进阶广告整理版来自同一套 PDF 课程，视为同一证据家族，不重复计票。

## 产物

- `data/processed/amazon_ads_skill/source_manifest_advanced_ads_rewrite_v2.jsonl`
- `data/processed/amazon_ads_skill/advanced_ads_rewrite_v2_claims.jsonl`（22 条主张）
- `data/processed/amazon_ads_skill/claim_review_advanced_ads_rewrite_v2.jsonl`
- `data/processed/amazon_ads_skill/advanced_ads_rewrite_v2_cases_input.jsonl`（人工案例输入）
- `data/processed/amazon_ads_skill/source_case_records_advanced_ads_rewrite_v2.jsonl`（6 条校验通过的来源案例）
- `data/processed/amazon_ads_skill/source_validation_advanced_ads_rewrite_v2_report.md`
- `.agents/skills/amazon-ads-keyword-strategy/references/18_advanced_ads_diagnosis_rewrite_v2_integration.md`
- 更新 `SKILL.md`、README、`references/09_case_library.md`、`references/11_source_index.md`、T050 eval

## 关键判断

- `supported`：漏斗诊断、ACOS 公式分解、父子体汇总后重算比例、报告分工、搜索词报告是诊断/词库工具、合规排除虚假交易。
- `context_dependent`：库存月数、2倍毛利率、20/100点击、商品投放相关性、关键词来源、变体拆分、测试阶段、旺季和清库存周期。
- `unsupported`：广告位 +20%/−10%/+30%、ACOS≤20%预算 +50% 等固定比例。
- `unresolved`：8周/双周/7天归因、小时报告回溯、旧课件中的 UI/受众竞价更新。
- 2点击1订单、户外座垫属性、四类诊断、广告位预算比例和生命周期参数均保留为案例，不升级为通用规则。

## 后续使用协议

当问题涉及 2 点击 1 订单、2 倍毛利率、20/100 点击、广告位/预算比例、BSR Top20-100、2周×4轮、旺季两周或六个月清库存时，必须先提示：

`讲义案例提示：SRC-3328e6e7662e 是同一课程 PDF 的另一份整理版，不是独立官方证据；以下内容按来源状态和案例边界使用。`

输出中区分来源观察、作者解释、实际动作和未验证因果；列出关键不匹配、缺失数据、保守路线、测试路线、成功标准和停止标准。

## 验证结果

- 来源/主张/案例审查：无契约错误。
- 22 条主张状态：`supported` 7、`context_dependent` 11、`unsupported` 2、`unresolved` 2。
- 来源覆盖：`PARTIAL`；8 个相关来源被引用，但未逐条覆盖项目全部 100 篇原文；DOCX 自动清单仍标为二进制扩展名限制，内容已完成 OOXML 阅读。
- Skill 校验：`PASS`；`git diff --check`：通过。首次校验发现 T049 与既有 eval 重号，已将本轮新增测试调整为 T050 后重新通过。
