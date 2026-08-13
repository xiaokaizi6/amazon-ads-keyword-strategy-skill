# 任务交接：新资料案例保留与主动证据提示

## 任务目标

按用户要求，把后续上传资料的完整阅读、交叉验证、条件化纳入和案例保留标准固化到 skill；对证据不足、条件化或真实冲突的内容保留并在相关回答中主动提示。

## 实际完成

- 更新 `SKILL.md`：后续资料完整阅读时必须保留所有决策相关案例；相关回答必须主动披露条件化主张状态或案例置信度、适用边界、关键不匹配和验证边界。
- 更新 `references/14_source_validation_and_conflict_protocol.md`：新增案例提取和保留流程。案例即使解释未证实或与既有观点冲突，也保留为来源忠实的 `case_observation`；来源观察、作者解释和动作分开。
- 更新 `references/15_source_review_schema.md`：定义 `source_case_records.jsonl` 字段与 `--cases-file` 校验入口；没有案例时必须在报告中如实记录 `0`，不得假装未检查。
- 更新 `references/09_case_library.md` 与 README：明确新来源案例先进入可追溯保留层，符合长期诊断锚点条件时才同步进案例库，且不是通用规则。
- 更新 `scripts/review_sources.py` 和 `scripts/validate_outputs.py`：前者校验人工提取的案例输入和来源关联，后者校验可选案例产物的字段、唯一 ID、来源和观察/解释/动作分离。
- 更新 T049 eval 与期望输出：覆盖案例保留、证据边界和未来相关答复的主动提醒。

## 来源与置信度

- 用户当前明确要求：高置信度，已直接写入主入口和验证参考。
- 既有项目来源验证协议、条件化主张层和工作区已有进阶讲义案例整合：高置信度，作为兼容基础；本轮未重判其中任何主张或案例。
- 未接收新的原始上传资料：未生成新的来源清单、案例记录或主张审查产物。

## 验证

- `python -m py_compile .agents/skills/amazon-ads-keyword-strategy/scripts/review_sources.py .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py`: PASS。
- `python .agents/skills/amazon-ads-keyword-strategy/scripts/review_sources.py --help`: PASS；确认 `--cases-file` 和 `--case-output` 已暴露。
- `python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py`: PASS；验证报告为 0 errors / 0 warnings。
- `git diff --check`: PASS。
- 未运行：`--cases-file` 的真实资料案例校验；本轮没有新案例输入，不能凭空生成案例产物。

## 风险与下一步

- 案例内容必须由完整阅读后人工结构化提取；脚本只验证契约与来源关系，不能替代阅读、交叉验证或官方事实核对。
- 下一批资料：保留原件和来源清单，完整阅读并建立原子主张与案例输入，运行 `review_sources.py --claims-file ... --cases-file ...`，再按覆盖报告和状态把内容纳入条件化主张层、案例层或规则层。
