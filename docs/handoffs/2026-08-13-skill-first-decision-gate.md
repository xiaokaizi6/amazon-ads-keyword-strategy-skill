# 2026-08-13 Skill-first 广告决策门槛交接

## 任务目标

确保 Codex 在给出 Amazon 广告优化建议前，必须先读取当前实际使用的 Skill 和相关 reference，不能脱离 Skill 凭通用经验直接回答。

## 已完成

- 在仓库 `SKILL.md` 的 Core Workflow 中加入 Skill-first 步骤：先加载入口、识别任务、读取 References Map、提取约束，再调用 MCP/账户数据并形成建议。
- 新增 `references/25_skill_first_decision_gate.md`，定义 LOADED/PARTIAL/BLOCKED/NOT_REQUIRED 状态、路径与已加载 reference 记录、版本差异处理和失败时禁止强动作。
- 在 Quality Checklist 中要求广告优化回答显示 `Skill 使用状态`、Skill 路径、任务相关 reference 和应用约束。
- 新增 T057 eval，要求不能只凭通用经验给出提价、否词、加预算、拆活动、排名或竞品动作。
- 同步更新 `AGENTS.md`、`docs/PROJECT_REQUIREMENTS.md`、`references/11_source_index.md` 和 `docs/CODEX_HANDOFF.md`。
- 将 Skill-first 核心规则和 `references/25_skill_first_decision_gate.md` 同步至 Codex 安装副本：`C:\Users\liuya\.codex\skills\ads_skill\skills\amazon-ads-keyword-strategy`。

## 验证

- 仓库 `validate_outputs.py`：PASS，`validation_report.md` 显示 Errors 0 / Warnings 0。
- 仓库 Skill `quick_validate.py`：PASS，输出 `Skill is valid!`。
- Codex 安装副本 `quick_validate.py`：PASS，输出 `Skill is valid!`。
- `git diff --check`：PASS；仅有 Git 的 LF→CRLF 提示，无 whitespace error。
- 本轮无具体广告账户决策，不调用西柚洞察 MCP；这是规则/文档变更任务。

## 后续规则

任何广告优化问题先读取 `SKILL.md` 和任务相关 reference，并在回答中标注 Skill 使用状态。若 Skill 不可读、版本冲突无法解决或关键 reference 缺失，应停止强动作建议，先报告阻塞并提出补充/同步或可逆测试方案。实时市场数据仍按 `references/24_live_market_data_mcp_decision_gate.md` 调用西柚洞察 MCP。

## 发布状态

- 已提交：`7d713bc3413d8b5158d8c21d7d122928a43be520`（`Add Skill-first decision gates`）。
- 已推送分支：`agent/skill-first-mcp-decision-gates`。
- 已创建草稿 PR：[ #3 ](https://github.com/xiaokaizi6/amazon-ads-keyword-strategy-skill/pull/3)。
