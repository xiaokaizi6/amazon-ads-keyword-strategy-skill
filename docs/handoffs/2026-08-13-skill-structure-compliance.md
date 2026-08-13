# Skill 结构规范审查交接（2026-08-13）

## 任务目标

检查本项目的 Amazon Ads Skill 是否符合 Codex/Agent Skill 写作规范，并修正入口、渐进披露、引用导航、UI 元数据和输出结构问题。

## 规范依据

- 本地 `C:\Users\liuya\.codex\skills\.system\skill-creator\SKILL.md`。
- 官方 OpenAI Codex GitHub 的 `skill-creator` 样例，重点核对 `SKILL.md` frontmatter、`agents/openai.yaml`、资源分层和 reference 导航。[OpenAI Codex skill-creator sample](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md)
- 官方 `openai.yaml` 字段说明，核对 `display_name`、`short_description`、`default_prompt` 和可选隐式调用策略。[openai.yaml reference](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/references/openai_yaml.md)

项目自身的 GitHub 远端当前可通过 Git remote 访问，但匿名网页打开返回 404；因此没有把远端网页内容冒充为可核对规范，而是采用官方 OpenAI Codex 样例和本地 skill-creator 规则作为规范来源。

## 已完成修改

- 新增 `.agents/skills/amazon-ads-keyword-strategy/agents/openai.yaml`。
- 保持 `SKILL.md` 为唯一业务入口，frontmatter 只包含 `name` 和 `description`；description 增加上传资料、原子主张、案例、交叉验证和冲突保留触发条件。
- 将维护者说明从 Skill 目录移至 `docs/AMAZON_ADS_SKILL_MAINTAINER_GUIDE.md`。删除 Skill 内重复的 `README.md`，避免把不参与加载的辅助文档与 Skill 资源混在一起。
- 为超过 100 行的 11 个 reference 增加 Contents 导航，符合渐进披露要求。
- 在 `SKILL.md` References Map 加入 `22_full_batch_review_2026-08-13.md`。
- 将输出模板从“所有问题必须 11 节”改为“完整诊断使用 11 节；窄问题只使用相关部分；source-review 任务使用来源/主张/案例/覆盖结构”，避免强制无关内容。
- 同步 `docs/CODEX_HANDOFF.md`、维护指南和本交接记录。

## 当前结构

```text
.agents/skills/amazon-ads-keyword-strategy/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
├── evals/
└── examples/
```

`SKILL.md` 为 352 行，低于 skill-creator 建议的 500 行上限；reference 详细内容按需加载。

## 规范判断

当前结构已满足：

- 必需 `SKILL.md` 与有效 YAML frontmatter。
- 清晰、可触发的 description。
- 推荐的 `agents/openai.yaml` UI 元数据。
- 详细知识放入 references，脚本放入 scripts，结构化测试放入 evals。
- 长 reference 有导航，入口直接引用 reference，不依赖深层级跳转。
- 业务状态、证据边界、案例层与规则层分离。

仍需注意：

- 当前 eval 仍主要验证结构和规则约束，不是模型回答质量评测。
- 尚未在隔离线程中做真实任务 forward-test；如要验证泛化，应使用不泄漏预期答案的独立测试任务。
- `README.md` 不再位于 Skill 目录；维护说明在 `docs/AMAZON_ADS_SKILL_MAINTAINER_GUIDE.md`。

## 验证结果

```text
python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py   PASS
python C:\Users\liuya\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/amazon-ads-keyword-strategy   PASS
git diff --check   PASS（仅有 Git 的 LF/CRLF 提示）
```

## 下一步

如果继续升级 Skill，优先增加隔离 forward-test 和针对 source-review、keyword-library、low-ACOS/high-ad-share 三类任务的回答质量评测；不要继续把更多长篇讲义直接塞入 `SKILL.md`。
