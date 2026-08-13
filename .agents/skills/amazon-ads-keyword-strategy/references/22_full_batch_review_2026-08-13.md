# 全量统一批次审查（2026-08-13）

本文件是本项目当前“100 篇文章 + 对话内全部新资料”统一批次的审查边界、计数和结论。它是审查索引，不把来源观察自动升级为事实或无条件执行规则。

## 批次范围

- 项目文章：100 篇，来源 ID 为 `A001`–`A100`，均进入 `project_corpus`。
- 用户上传资料：8 个唯一文件，进入 `user_document`。其中原始课程 PDF 与两份文字改述属于同一证据家族，不重复计票，但每个文件仍保留来源覆盖记录和来源链。
- 统一来源清单：`data/processed/amazon_ads_skill/source_manifest_full_batch_2026-08-13.jsonl`，共 108 个来源。
- 统一主张输入：`full_batch_claims_2026-08-13.jsonl`，共 781 条；审查结果为 `full_batch_claim_review_2026-08-13.jsonl`。
- 统一案例输入/结果：`full_batch_cases_2026-08-13.jsonl` / `full_batch_case_records_2026-08-13.jsonl`，共 36 条，案例契约错误 0。
- 统一报告：`source_validation_report_full_batch_2026-08-13.md`。

## 逐条处理口径

项目文章的 2,006 条规范化记录中，1,413 条为噪声，593 条为决策相关记录；所有 593 条都生成独立审查项，并额外为每篇文章生成一条来源覆盖记录。A069 没有规范化记录，保留一条 `manual_coverage_fallback` 未决项，要求重新检查上游抽取器，不能把“无记录”解释成“无主张”。原始课程 PDF 没有独立 claim 文件，额外保留一条来源覆盖主张，明确它与文字改述同属证据家族。

项目语料记录按记录类型保守映射，不自动证明真伪：

| 原记录类型 | 批次状态 | 含义 |
|---|---|---|
| `executable_rule` | `context_dependent` | 可作为候选动作，但必须按阶段、目标、毛利、预算和样本验证 |
| `diagnostic_hypothesis` / `diagnostic_question` | `unresolved` | 保留假设或问题，缺少足够独立证据 |
| `counterexample` | `disputed` | 与其他口径存在真实或表面冲突，回答时必须给出适用条件 |
| `case_observation` | `context_dependent` | 只保留观察和动作，不代表因果规律 |
| `comment_signal` | `unsupported` | 评论/讨论信号，不作为事实依据 |

用户资料中的 86 条原子主张沿用先前的证据审查，不因进入统一批次而改变状态；原始课程 PDF 另有 1 条来源覆盖主张。所有争议、未决、证据不足、过时和条件化内容均保留；未进入 `merged_rules.jsonl` 只表示没有升级为无条件规则。

## 结果计数

- 状态总数：`supported` 131、`context_dependent` 187、`disputed` 25、`unresolved` 204、`unsupported` 227、`outdated` 3、`confirmed_error` 4。
- 100 篇项目文章贡献 694 条审查项（其中 100 条是来源覆盖记录）；8 个用户文件贡献 87 条审查项，其中 86 条是原子主张、1 条是原始课程 PDF 的来源覆盖记录。
- 所有 108 个来源均被 claim 或覆盖记录引用，未引用来源为 0；审查契约错误为 0。
- 自动读取器可直接解析 100 个 Markdown 来源；8 个二进制用户文件通过来源专用 OOXML/XLSX/PDF 提取或页面图像检查完成人工阅读，manifest 用 `manual_reviewed: true` 与 `readable: false` 分开记录。
- 因默认自动读取器不解析 DOCX/XLSX/PDF，机器报告状态保留为 `PARTIAL`。这表示“自动可读性未全通过”，不是“用户资料未读”或“主张未登记”。

## 交叉验证结论

1. 数学定义、指标关系和“没有统一健康 ACOS”这类低时效内容，只有在原子主张具备公式、定义或独立来源时才标为 `supported`；百分比、点击阈值、固定天数、预算倍数和自然排名因果一律保留条件化或未决状态。
2. 参考价/划线价资料不能直接当成“先抬价再打折”的操作规则。当前 Amazon 公告要求 List Price 近期在其他零售商提供过，或曾作为 Amazon Featured Offer 被购买；Typical Price 还受 90 天价格历史和促销处理影响。[Amazon reference pricing update](https://sellercentral.amazon.com/seller-forums/discussions/t/f48a1fe5-aa8e-4806-b687-2d9aeec5c351)
3. 返现换评、免费/折扣产品换评、review club、修改评价、虚假订单和补偿买家等内容保留为风险证据并标为 `confirmed_error`，不得转写为优化或规避检测步骤。[Amazon product reviews policy](https://sellercentral.amazon.com/seller-forums/discussions/t/9fab2fc9-b7dd-44b1-924c-77fb87462ac8)
4. 刷销量、接受/支付虚假订单、补偿买家购买和人为操纵销售排名属于政策风险，不能作为白帽广告打法。[Amazon sales-rank / traffic policy discussion](https://sellercentral.amazon.com/seller-forums/discussions/t/364ee6ee7f10c568a5c0959cfec596e3)
5. Sponsored Products 的否定投放、匹配类型和“至少 20 次点击后评估、改动后观察至少两周”属于 Amazon Ads 的具体建议；它不能推出 TOS 100%–200% 或 900% 溢价必然有效，也不能证明广告位必然提升自然排名。[Amazon Ads targeting guide](https://advertising.amazon.com/en-us/library/guides/targeting-with-sponsored-products/)

## 使用要求

回答涉及本批次案例或条件化主张时，必须显示：来源文件/证据家族、当前状态、适用条件、与当前账户的关键不匹配、缺失数据、可逆验证窗口、成功标准和停止标准。若状态为 `disputed`、`unresolved`、`unsupported` 或 `outdated`，同时给出至少两条可行路线或明确说明暂不能下结论。

本批次是“全量登记 + 原子化审查 + 证据状态保留”，不是对 781 条主张的逐条官方背书。后续若新增 Amazon 官方政策、账户报告或可复现实验，应只更新对应 claim 的证据和状态，不删除旧来源观察。
