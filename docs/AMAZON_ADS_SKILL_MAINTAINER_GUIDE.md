# Amazon Ads Skill 维护说明

该项目的可发现 Skill 入口是：

`.agents/skills/amazon-ads-keyword-strategy/SKILL.md`

Skill 目录只保留 Codex 执行任务所需的入口、`agents/openai.yaml`、`references/`、`scripts/`、`evals/` 和示例资源。详细方法按任务从 References Map 按需读取，避免把全部讲义和规则一次性塞进上下文。

## 维护入口

- 业务入口：`.agents/skills/amazon-ads-keyword-strategy/SKILL.md`
- UI 元数据：`.agents/skills/amazon-ads-keyword-strategy/agents/openai.yaml`
- 运行脚本：`.agents/skills/amazon-ads-keyword-strategy/scripts/`
- 方法与证据协议：`.agents/skills/amazon-ads-keyword-strategy/references/`
- 结构化评估：`.agents/skills/amazon-ads-keyword-strategy/evals/`
- 当前交接：[docs/CODEX_HANDOFF.md](CODEX_HANDOFF.md)

## 验证命令

```powershell
python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py
python C:\Users\liuya\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/amazon-ads-keyword-strategy
git diff --check
```

新增讲义或报告时，先按 `references/14_source_validation_and_conflict_protocol.md` 登记来源，再拆分原子主张和案例；不要把讲义、评论或单个案例直接升级为无条件规则。`disputed`、`unresolved`、`unsupported`、`outdated` 和 `context_dependent` 必须保留并在回答相关问题时提示来源状态。

全量复核使用：

```powershell
python .agents/skills/amazon-ads-keyword-strategy/scripts/build_full_batch_audit.py
```

随后将生成的混合 manifest 传给 `review_sources.py --manifest-input`，并分别报告来源覆盖、主张状态、案例校验和二进制文件可读性限制。
