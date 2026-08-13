# 2026-08-13 实时市场数据 MCP 决策门槛交接

## 任务目标

把用户的新要求写入 Amazon Ads Skill：凡是需要当前市场、竞品、关键词、趋势、排名或放量事实的决策，先调用 Codex 已安装的西柚洞察 MCP，再给出动作；不能用记忆、讲义或未记录的搜索结果代替实时数据。

## 已完成

- 在 `SKILL.md` 的 Required Inputs、Core Workflow、References Map 和 Quality Checklist 中加入 MCP 决策闸门。
- 新增 `references/24_live_market_data_mcp_decision_gate.md`，定义必须调用场景、最小数据选择、调用记录、数据新鲜度、`COMPLETE`/`PARTIAL`/`BLOCKED`/`NOT_REQUIRED` 状态、证据边界和回答格式。
- 将 MCP 市场证据与用户账户报告、项目 claim/case、Amazon 官方政策/功能证据分层，禁止用市场搜索量或竞品排名单独证明自然排名因果。
- 新增 T056 评估用例和期望输出，覆盖无调用不得声称已验证、MCP 失败不得给强决策、不得虚构工具名/字段/日期等约束。
- 更新 `docs/PROJECT_REQUIREMENTS.md` 和 `references/11_source_index.md`。

## 本轮验证

- `python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py`：PASS，`validation_report.md` 显示 Errors 0 / Warnings 0。
- `quick_validate.py`（仓库 Skill）：PASS，输出 `Skill is valid!`。
- `quick_validate.py`（Codex 安装副本）：PASS，输出 `Skill is valid!`。
- `git diff --check`：PASS；仅有 Git 的 LF→CRLF 提示，无 whitespace error。
- 本轮没有具体广告账户或市场问题，因此没有实际调用西柚洞察 MCP；当前会话工具列表没有暴露该 MCP 的具体 operation，未伪造调用结果。

## 后续执行规则

处理关键词扩量、竞品投放、市场机会、排名诊断、预算放量等任务时，先读取 `references/24_live_market_data_mcp_decision_gate.md`，再使用当前会话实际可见的西柚操作。若工具未暴露、权限失败、数据为空或字段不足，应向用户说明 `BLOCKED`/`PARTIAL`，列出需要补充的站点、ASIN/关键词、日期和字段，并只提供可逆、低风险、非强制性的下一步。

## 未完成

- 已将本轮 MCP 决策门槛的核心 SKILL.md 指令和 `references/24_live_market_data_mcp_decision_gate.md` 同步到 `C:\Users\liuya\.codex\skills\ads_skill\skills\amazon-ads-keyword-strategy` 安装副本；该目录仍不是本仓库 Git 追踪路径，后续完整 Skill 版本升级时应继续采用明确的安装/同步流程，避免两份 Skill 漂移。
- 后续已通过 PR [#3](https://github.com/xiaokaizi6/amazon-ads-keyword-strategy-skill/pull/3) 合并到 `main`，合并提交为 `dff050ac88dcbe26822cbf58a18a96f3af121a27`；发布分支已删除。
