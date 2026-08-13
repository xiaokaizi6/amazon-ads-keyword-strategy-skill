# 任务交接：Skill 协作与来源验证治理

## 任务目标

明确 GitHub 项目中 skill 的协作规范，为长期使用 Codex 建立项目要求和任务交接机制，并规定如何交叉验证后续广告讲义、识别错误说法及保留无法确定的不同观点。

## 实际完成

- 核对 Git remote，并 fetch `origin/main`；本地与远端均为提交 `d302203a24d6483853f829310514fc63c9401647`。
- 阅读现有 `SKILL.md`、使用说明、相关 taxonomy/schema/conflict/source 文档和校验入口。
- 新增根目录 `AGENTS.md`，作为 Codex 强制协作入口。
- 新增项目长期要求、滚动交接和本历史交接。
- 新增来源验证与观点冲突协议，并将其接入 skill、README、eval 和校验器。

## 修改文件及原因

- `AGENTS.md`：固化接管、执行、验证和交接规则。
- `docs/PROJECT_REQUIREMENTS.md`：解释长期治理、文档职责和完成定义。
- `docs/CODEX_HANDOFF.md`：让下一次 Codex 快速恢复当前状态。
- `docs/handoffs/2026-08-12-skill-collaboration-governance.md`：保留本轮不可覆盖的历史记录。
- `.agents/skills/amazon-ads-keyword-strategy/references/14_source_validation_and_conflict_protocol.md`：定义新资料的主张级验证协议。
- `.agents/skills/amazon-ads-keyword-strategy/SKILL.md`：把验证协议加入 agent 主流程。
- `.agents/skills/amazon-ads-keyword-strategy/README.md`：同步维护者使用说明。
- `.agents/skills/amazon-ads-keyword-strategy/evals/test_cases.jsonl` 与 `evals/expected_outputs.md`：增加冲突讲义回归场景。
- `.agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py`：将新 reference 纳入必需文件检查。
- `data/processed/amazon_ads_skill/validation_report.md`：由校验器刷新，记录本轮 `PASS`、0 errors、0 warnings。

## 新了解和决策

- 原 skill 已能区分案例、规则、评论和噪声，但没有定义何时可以认定讲义“错误”，也没有全范围覆盖证明。
- 采用 `confirmed_error`、`outdated`、`unsupported`、`context_dependent`、`disputed`、`unresolved`、`supported` 七类状态，避免把不确定性伪装成结论。
- 对无法确定的冲突不做强行合并；后续实际任务必须展示不同路线、条件、风险、缺失数据和测试方法。

## 验证

已执行：

- `python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py`：`PASS`，0 errors，0 warnings。
- JSONL 逐行解析检查：`PASS`，44 个 eval cases 可解析、ID 唯一、T044 存在。
- `git diff --check`：`PASS`；仅输出 Windows 的 LF/CRLF 提示，不是空白错误。
- `git status --short`：已检查；本轮文件保持未提交，且用户原有 zip 状态仍在。

未执行 commit、push、发布或部署。

## 风险和遗留事项

- 本轮没有处理用户已有的 zip 文件状态。
- 新协议是治理合同；未来收到真实讲义时仍需实现或运行对应的 claim review 数据产物。
- 匿名 GitHub 页面无法读取私有仓库；远端一致性来自成功的 Git fetch，而非网页内容。

## 下一步入口

读取 `AGENTS.md`、`docs/CODEX_HANDOFF.md` 和 `references/14_source_validation_and_conflict_protocol.md`，然后对新资料先盘点、后拆主张、再交叉验证。
