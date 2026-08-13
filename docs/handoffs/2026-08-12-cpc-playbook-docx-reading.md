# 任务交接：完整阅读 CPC 广告打法知识体系 DOCX

## 任务目标

完整阅读用户提供的《亚马逊CPC广告打法知识体系全梳理v1_20260804(1).docx》，学习其内容，同时遵守项目的来源登记、证据分层和不确定性保留规范。

## 实际完成

- 读取 DOCX 的 OOXML `word/document.xml`，覆盖全部非空段落、表格、指标公式、阈值表、广告结构表、报告回溯期表、20 种打法表和附录 175 篇文章对照表。
- 核对 DOCX 包结构：无 `word/media/` 图片媒体，内容不是图片 OCR 结果；因此本轮没有遗漏隐藏图片文字的已知问题。
- 识别文档主线：公式与盈亏平衡 → SP 自动/手动/定位/广告位 → SB/SD → 产品阶段与架构 → 报告分析 → 20 种打法 → 大促和新功能 → 指标专项优化。
- 生成来源登记：`data/processed/amazon_ads_skill/source_manifest_cpc_playbook.jsonl`。
- 生成来源覆盖报告：`data/processed/amazon_ads_skill/source_validation_cpc_playbook.md`。
- 未创建 `claim_review.jsonl`，因为本轮没有逐条拆分原子主张并完成全库/官方证据核对；报告保持 `NOT_READY`。

## 已了解但尚未升级为规则的内容

- 文档反复使用 ACOS、ROAS、CPA、盈亏平衡 CPC、预算、订单、销售额、TACOS 的计算关系，并以 CTR/CVR/广告位/自然销售占比构建漏斗式诊断。
- 文档按 SP 自动、SP 手动、ASIN/类目定位、TOS/ROS/PP、SB、SD、新品阶段、报告和 20 种打法组织运营动作。
- 经验阈值、预算比例、TOS 溢价、自动转手动点击/订单阈值、报告回溯窗口、广告排名/质量得分机制、3 个月扶持期、SPV/Prompts 功能和叠词/马甲/海王/捡漏等打法全部保留为待审主张或案例口径。

## 证据与置信度

- 来源：用户提供的二手整理文档；文档自称整理公众号作者 175 篇文章，非 Amazon 官方一手资料。
- 文件 SHA-256：`123d25a4a09a3580fbe39aa183c86420c76e403283cf257fc1f8c11005de6693`。
- 来源清单可读性：脚本对 `.docx` 标为 `binary_or_unsupported_extension`；实际阅读通过 OOXML 结构解析完成。来源覆盖报告因此只能表示来源已登记，不能表示主张已核验。
- 当前没有任何主张标记为 `supported`、`confirmed_error` 或 `outdated`。

## 未完成/风险

- 尚未把重要段落拆成原子主张，尚未逐条与项目 raw/processed 资料、现有冲突/反例和当前 Amazon 官方文档交叉验证。
- 数学公式需要区分“代数关系”与平台报告归因/扣费定义；尤其质量得分扣费公式、Ad Rank 因果等不能直接作为平台机制。
- 所有阈值和功能说明都可能受站点、类目、产品阶段、广告目标、账户权限、时间窗口和平台改版影响。

## 下一步入口

若用户要求验证或纳入规则库：先以 `SRC-214ee7c1e651` 为来源，按 `references/14_source_validation_and_conflict_protocol.md` 建立原子 claim JSONL；再运行 `scripts/review_sources.py`，逐条检查项目资料与 Amazon 官方一手来源，保留 `context_dependent`、`disputed`、`unresolved` 等不同观点，最后才决定是否更新 `merged_rules.jsonl`、references 或 eval。

## 验证记录

- 已运行：DOCX OOXML 结构解析；结果：成功读取全部文档节点。
- 已运行：`scripts/review_sources.py --no-project-corpus --source-file ...`；结果：成功生成 1 条来源记录和 `NOT_READY` 覆盖报告。
- 未运行：原子主张审查、Amazon 官方逐条核验、规则库重建、模型 eval、DOCX 可视化渲染（当前环境没有 `soffice`/`libreoffice`）。
