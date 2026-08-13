# 任务交接：CPC 广告打法讲义交叉验证与 Skill 融入

## 任务目标

将用户提供的《亚马逊CPC广告打法知识体系全梳理v1_20260804(1).docx》融入 Amazon Ads skill，并与项目语料及 Amazon 官方资料交叉验证；不得把未证实的经验阈值或平台机制直接升级为通用规则。

## 实际完成

- 建立 21 条原子主张，输入为 `data/processed/amazon_ads_skill/cpc_playbook_claims.jsonl`。
- 使用 `scripts/review_sources.py` 生成标准来源清单、claim review 和覆盖报告：
  - `data/processed/amazon_ads_skill/source_manifest.jsonl`
  - `data/processed/amazon_ads_skill/claim_review.jsonl`
  - `data/processed/amazon_ads_skill/source_validation_report.md`
- 交叉检查用户 DOCX、项目中与广告结构/新品/排名停滞最相关的 6 个来源，以及 Amazon Ads 官方 ACOS、ROAS、Sponsored Products targeting、best practices、search term report、placement bid adjustment、Sponsored Products video 页面。
- 新增 `references/16_cpc_playbook_integration.md`，将支持的定义和条件化策略写入 skill，并明确列出不能泛化的 TOS 百分比、三个月扶持期、quality-score 扣费公式、固定报告回溯期和 Prompts 说法。
- 更新 `SKILL.md`、`references/04_campaign_structure.md`、`05_search_term_optimization.md`、`06_product_stage_strategy.md`、`08_metric_thresholds.md`、eval 测试集及期望输出。

## 审查结果

21 条主张：`supported=13`、`context_dependent=1`、`disputed=1`、`unresolved=5`、`unsupported=1`，验证错误数为 0。覆盖状态为 `PARTIAL`：清单共有 101 个项目/用户来源，但本轮只逐条检查了用户 DOCX 和 6 个高相关项目来源；其余来源列在报告的未覆盖列表中。

## 已融入的稳定结论

- ACOS/ROAS 的计算关系；没有跨类目、阶段、目标通用的“好 ACOS”。
- 自动定向四种策略；手动关键词 broad/phrase/exact 的官方定义。
- search term report 至少一次点击、targeting report 至少一次展示的报告边界。
- 相关且样本充分的搜索词提取到 exact/phrase；低效/不相关目标可降价或否定，但不能只看 ACOS。
- Amazon 官方建议 negative target 至少观察 20 次点击；该数字是检查点，不是自动否词命令。
- discovery/profit/defense/conquest/rank-test 目标隔离；placement 按 TOS/ROS/product pages 分开诊断。

## 保留为争议或未决

- 广告订单是否直接提升目标词自然排名：项目反例与讲义策略并存，必须做同词、同窗口、带自然订单和排名跟踪的验证。
- TOS 50%-200% 溢价、TOS CVR 是 PP 2-3 倍、新品 3 个月扶持期：无足够通用证据，不能写成规则。
- quality-score 扣费公式/简化 Ad Rank：官方当前资料未确认，不能作为平台机制。
- 报告具体回溯窗口、Prompts：时效性高，必须按目标账号和市场重新核对。

## 验证记录

- `python .agents/skills/amazon-ads-keyword-strategy/scripts/review_sources.py ... --claims-file ...`：成功生成 21 条 claim review，`PARTIAL`，0 个 schema 错误。
- `python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py --output-file data/processed/amazon_ads_skill/validation_report_after_cpc_playbook.md`：`PASS`，0 errors，0 warnings。
- `git diff --check`：通过（仅有换行符提示）。
- 未运行：规则库重建、模型 eval runner、完整 100 篇来源逐条 claim 审查。

## 下一步

收到新的讲义或用户要求继续核验时，先补充相关来源和原子主张，重新生成 claim review；只有覆盖状态达到可接受范围、且主张有条件和证据时，才考虑将其转成 `merged_rules.jsonl` 的 executable rule。
