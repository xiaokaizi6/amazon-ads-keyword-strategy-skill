# 任务交接：将未决讲义观点纳入条件化主张层

## 任务目标

根据用户要求，不删除讲义中无法升级为通用规则的内容；将其写入 skill，并通过状态标签和验证条件控制使用方式。

## 实际完成

- 更新 `.agents/skills/amazon-ads-keyword-strategy/SKILL.md`，新增 `Conditional Source Claims`：
  - `supported`：满足条件时可作为规则；
  - `context_dependent`：必须匹配阶段、站点、类目、毛利、预算和样本；
  - `disputed`：并列输出不同路线，不能给单向结论；
  - `unresolved`：只能作为诊断假设或限时测试；
  - `unsupported`：保留审计和替代思路，不作为默认动作；
  - `outdated`：只保留历史上下文，使用前重新核对；
  - `confirmed_error`：不推荐，但保留反证链。
- 更新 `references/16_cpc_playbook_integration.md`，增加条件化主张输出模板和 3 个具体示例：TOS 溢价、广告单与自然排名、新品三个月扶持、质量得分公式。
- 更新 README、T047 eval 和期望输出，要求 Codex 以后不能静默删除争议观点，也不能把未验证内容写成通用规则。
- 更新 `docs/CODEX_HANDOFF.md`，明确条件化主张层是可使用的 skill 知识层，区别于无条件 `merged_rules.jsonl`。

## 使用协议

以后使用讲义观点时，回答至少要出现：来源状态、适用条件、支持/保守路线、缺失数据、验证窗口、成功标准和停止标准。`disputed` 必须同时保留 View A/View B；`unresolved` 和 `unsupported` 只能用于假设、诊断问题或可逆测试。

## 验证

- 待运行：`validate_outputs.py`、`git diff --check`。
- 未修改：原始讲义、用户 zip 文件、既有规则库生成逻辑。
- 未完成：将未决主张升级成通用 `merged_rules.jsonl` executable rule；这是有意保留的边界。

## 下一步

新讲义继续使用 `cpc_playbook_claims.jsonl` / `claim_review.jsonl` 的原子主张流程；如果后续覆盖证据充分，再单独评估某一主张是否可以升级为条件化 executable rule。
