# Codex 当前交接

- 最后更新：2026-08-12
- 当前分支：`main`
- 最新已核对远端提交：`d302203a24d6483853f829310514fc63c9401647`
- 最新任务记录：`docs/handoffs/2026-08-13-conditional-claim-layer.md`

## 当前状态

项目已有 100 篇原始 Amazon 广告文章及分阶段生成的索引、section、提取记录、规则库、案例库、冲突库、噪声库和关键词库。现有 skill 已要求条件化建议并区分案例、规则、假设、评论和噪声。

本轮新增项目级 Codex 协作规范、每任务交接闭环，以及新讲义进入后的全库交叉验证和冲突保留协议。后续 Codex 应先读根目录 `AGENTS.md`，再读本文件与任务相关 skill/reference。

本轮已实现规则库/案例库的独立重建脚本，并新增 `review_sources.py`、来源审查 schema 和可选来源审查产物校验。两个重建脚本复用 `normalize_records.py` 的同一套聚合逻辑，避免独立算法漂移。

本轮已阅读用户提供的《亚马逊专题课-进阶广告诊断有优化全指导.pdf》（143 页、以课件图像为主），并生成完整的中文文字改述 Word：`outputs/亚马逊进阶广告诊断优化全指导-文字改述版.docx`。文稿按诊断、ACOS 优化、搜索词、广告位 / 活动 / 预算、核心关键词、投放结构和商品阶段组织；案例未复制截图，而是提取 seat cushion 案例的指标、假设及处理逻辑。课程中的点击阈值、毛利判断、各站点基准图和功能说明均保留为课程 / 案例口径，未升级为通用规则。

## 已知工作区状态

本轮开始前已存在以下用户改动，本轮未处理：

- `ads-skill.zip`：Git 状态为删除。
- `ads_skill.zip`：Git 状态为未跟踪。

不得在没有用户授权的情况下恢复、删除或提交这两个文件。

## 已确定的长期规则

- 原始讲义不是事实权威；重要主张必须跨项目资料核对。
- 只有满足严格证据条件才使用 `confirmed_error`。
- 无法确定时保留所有有意义观点，并输出不同路线的适用条件和验证方法。
- 对时效敏感的平台事实优先核对当前 Amazon 官方一手资料。
- 每次实质性任务都要更新本文件并新增历史交接；只读任务以用户边界为先。

## 未决事项

- 当前尚未收到新的用户讲义或原子主张，因此没有在项目 processed 目录生成 `claim_review.jsonl`；来源审查脚本已可生成来源清单和 `NOT_READY` 报告，收到文件后再运行主张审查。
- 本轮讲义的单独来源清单为 `data/processed/amazon_ads_skill/source_manifest_advanced_ads_lecture.jsonl`，来源报告为 `data/processed/amazon_ads_skill/source_validation_advanced_ads_lecture.md`。脚本只把 PDF 识别为二进制 / 不支持的文本扩展名，故报告为 `NOT_READY`；实际内容已通过逐页渲染视觉阅读，未据此声称完成跨全库的主张验证。
- 本轮完整阅读用户提供的 `C:\Users\liuya\Downloads\亚马逊CPC广告打法知识体系全梳理v1_20260804(1).docx`：通过 OOXML 读取了全部非空段落、表格和附录对照表（文档自称整理 175 篇文章）。该文件不含图片媒体，主要内容为整理者对公式、SP/SB/SD 架构、广告报告、20 种打法和指标优化的文字总结。已生成 `data/processed/amazon_ads_skill/source_manifest_cpc_playbook.jsonl` 与 `data/processed/amazon_ads_skill/source_validation_cpc_playbook.md`；由于脚本默认不解析 DOCX，来源报告诚实保持 `NOT_READY`，但本轮已完成可读性结构化阅读。未将该文档的阈值、平台机制或打法升级为通用规则。
- 当前学习结论：ACOS/ROAS/CPA/TACOS 等算式可作为待核对的数学定义；CTR/CVR/ACOS 健康值、广告与自然销售占比、TOS 溢价、自动/手动迁移阈值和预算百分比均属于经验或案例口径，需按站点、类目、阶段、目标和样本量验证；“质量得分扣费公式”、广告排名因果、3 个月流量扶持、功能名称/回溯窗口、叠词/马甲/海王等打法及 Prompts/SPV 等功能描述属于高风险或时效性主张，后续必须拆成原子主张并核对项目资料与 Amazon 官方来源。文档中的账户数据和 175 篇文章摘要只作为来源观察，不作为独立规则证据。
- 本轮已完成该 DOCX 的第一批原子主张交叉验证并融入 skill。新增 `references/16_cpc_playbook_integration.md`，并更新 `SKILL.md`、广告结构、搜索词、指标阈值、产品阶段参考文档及 eval。21 条 claim 的状态为：supported 13、context_dependent 1、disputed 1、unresolved 5、unsupported 1；覆盖报告为 `PARTIAL`，因为逐条核对的是 6 个高相关项目来源、用户 DOCX 和 Amazon 官方页面，并未逐条覆盖全部 100 篇项目原文。
- 已生成标准来源审查产物：`data/processed/amazon_ads_skill/source_manifest.jsonl`、`claim_review.jsonl`、`source_validation_report.md`，以及可复用输入 `cpc_playbook_claims.jsonl`。验证器已检查 JSONL、来源字段、状态约束和引用完整性。
- 根据用户要求，未升级为通用规则的讲义内容现在也正式纳入 skill 的条件化主张层：`SKILL.md` 新增 `Conditional Source Claims` 规则，`references/16_cpc_playbook_integration.md` 新增状态标签、路线、缺失数据和验证窗口模板，README 与 T047 eval 已同步。`disputed`、`unresolved`、`unsupported` 不再被排除，但仍不能作为无条件 executable rule。
- Word 文件已做结构检查；标准 `render_docx.py` 因当前环境缺少 LibreOffice / soffice 而无法渲染。尝试本机 Word 自动化导出也未生成 PDF，因此视觉 QA 不能标记为通过。
- 尚未实现自动调用模型的 eval runner；当前 eval 校验的是测试集结构和规则约束，不是模型回答质量。
- GitHub 仓库网页对匿名访问返回 404，`gh` 当前未登录；本轮通过已配置的 Git remote 成功 fetch 并确认本地与 `origin/main` 一致。

## 推荐下一步

收到下一批讲义后，复用 `scripts/review_sources.py` 和 `references/16_cpc_playbook_integration.md` 的 claim 流程；先补齐剩余相关项目来源的逐条覆盖，再决定是否把任何未决主张升级为规则。未决主张可以保留在条件化主张层，但必须输出来源状态、适用条件、不同路线、缺失数据、验证窗口、成功标准和停止标准；不要直接写成 `merged_rules.jsonl` 的无条件规则。
