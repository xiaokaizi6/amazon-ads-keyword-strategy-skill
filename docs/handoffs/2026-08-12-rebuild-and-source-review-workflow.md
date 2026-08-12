# 任务交接：规则/案例重建与来源审查工作流

## 任务目标

实现 `build_rulebooks.py`、`build_case_library.py` 两个占位脚本，并实现来源清单、主张审查和覆盖报告流程，为后续用户上传讲义和数据做准备。

## 实际完成

- 两个重建脚本已实现，均从 `normalized_records.jsonl` 读取，并复用 `normalize_records.py` 的规则聚合、反例挂载、案例关联和诊断点逻辑。
- 新增 `scripts/review_sources.py`：支持项目原始资料目录、单个用户文件、SHA-256、证据簇、可读性限制、原子主张 JSONL 和覆盖报告。
- 新增 `references/15_source_review_schema.md`，定义三类输出和状态约束。
- `validate_outputs.py` 已纳入新脚本、新 reference，并在可选来源审查产物存在时校验其 schema、来源 ID 和 `confirmed_error` 门槛。
- 更新 `SKILL.md`、README、source index、evals、最终质量审查和当前交接。

## 修改文件及原因

- `.agents/skills/amazon-ads-keyword-strategy/scripts/build_rulebooks.py`：移除占位异常，实现规则库独立重建。
- `.agents/skills/amazon-ads-keyword-strategy/scripts/build_case_library.py`：移除占位异常，实现案例库独立重建。
- `.agents/skills/amazon-ads-keyword-strategy/scripts/review_sources.py`：来源清单、主张契约校验、覆盖报告主流程。
- `.agents/skills/amazon-ads-keyword-strategy/references/15_source_review_schema.md`：来源审查输入输出 schema。
- `.agents/skills/amazon-ads-keyword-strategy/references/14_source_validation_and_conflict_protocol.md`：接入实际脚本和 NOT_READY 语义。
- `.agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py`：新增来源审查 artifact 检查。
- `.agents/skills/amazon-ads-keyword-strategy/SKILL.md`、README、source index：同步使用入口和产物说明。
- `evals/test_cases.jsonl`：新增 T045，覆盖没有主张输入时的 NOT_READY 行为。
- `data/processed/amazon_ads_skill/final_quality_review.md`：同步当前 45 条 eval 和新工作流状态。

## 设计决策

- 规则和案例脚本不复制业务聚合算法，而是复用 `normalize_records.py`，以保证单独重建和全量归一化结果一致。
- 来源清单不是主张验证。没有 claims 输入时只生成来源盘点，报告状态是 `NOT_READY`，不生成空的 `claim_review.jsonl`。
- 脚本不会从讲义文字自动推断 `confirmed_error`。该状态要求反对证据和验证测试；不确定状态必须记录缺失证据或下一步测试。
- 内容哈希相同的文件共享 `evidence_cluster`，不能重复计票。

## 验证命令与真实结果

- 两个重建脚本使用临时输出运行：均成功，输出与现有规则/案例记录数量一致（255 rules、15 cases）。
- `review_sources.py` 使用项目 100 篇原始文章运行到临时输出：成功生成 100 条来源记录和 `NOT_READY` 报告，未生成空 claim review。
- Python AST 解析：12 个 skill 脚本通过。
- `validate_outputs.py --output-file <临时报告>`：`PASS`，0 errors，0 warnings；无项目级 source-review 产物时该项为 `not run`。
- 最终默认验证 `python ".agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py"`：`PASS`，0 errors，0 warnings；source review artifacts 显示 `not run`（当前没有用户 claims 输入）。
- `git diff --check`：通过。

## 未完成和风险

- 当前没有用户新讲义或原子 claims，因此尚未生成正式 `source_manifest.jsonl`、`claim_review.jsonl` 到项目 processed 目录；这不是失败，而是保持 `NOT_READY` 的预期状态。
- 尚未实现自动调用模型评测 45 个 eval case 的 runner。
- 当前工作区已有的 zip 文件状态和此前未提交修改没有处理。

## 下一步入口

收到文件后，先运行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/review_sources.py" --no-project-corpus --source-file "path/to/file.md"
```

再按 `references/15_source_review_schema.md` 准备 claims JSONL，运行 `--claims-file` 生成主张审查和覆盖报告。
