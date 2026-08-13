# 2026-08-13 争议与不确定内容保留规范交接

## 用户要求

用户明确要求：争议内容、证据不足、无法确定、过时和有条件的内容也必须上传到 Skill，但要清楚标记；后续相关提问时必须主动提示。

## 完成内容

- 新增 `references/21_disputed_uncertain_claim_retention.md`，定义五类不确定状态的保留字段、回答方式和主动提示要求。
- 在 `SKILL.md`、`README.md`、`references/14_source_validation_and_conflict_protocol.md`、`references/15_source_review_schema.md`、`references/09_case_library.md` 和 `references/11_source_index.md` 中明确：未进入 `merged_rules.jsonl` 不等于未上传。
- 新增 T053 eval，检查争议/未决/unsupported/outdated/context_dependent 内容是否仍保留并带有 source ID、claim ID、条件、证据边界和验证测试。
- 更新 `docs/CODEX_HANDOFF.md`，将本规则作为长期协作要求。

## 保存边界

- 主张保存在批次 claim-review JSONL 或主张审查文件中。
- 案例保存在 source-case JSONL 或案例库中，观察、作者解释和动作分开。
- reference 文件提供可读索引和回答协议。
- `merged_rules.jsonl` 只保存可执行规则；争议内容不因未进入该文件而被删除。

## 验证

- `python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py`：通过，报告 `PASS`，0 errors/0 warnings。
- `python C:\Users\liuya\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/amazon-ads-keyword-strategy`：通过，输出 `Skill is valid!`。
- `git diff --check`：通过；仅有 Git 的换行符提示，无 whitespace 错误。
- eval JSONL 解析：通过，53 条用例、无重复 ID，最新为 T053。

## 后续回答要求

当问题命中争议主张或案例，必须显示 `讲义案例提示`，说明来源状态、来源位置、匹配条件、关键不匹配、不同路线、缺失数据和可逆验证窗口；不得把争议观点改写成唯一正确规则。
