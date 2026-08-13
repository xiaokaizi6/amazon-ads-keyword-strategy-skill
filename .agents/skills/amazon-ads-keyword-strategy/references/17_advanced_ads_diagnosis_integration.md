# 进阶广告诊断讲义整合层

## 来源边界

来源：`亚马逊进阶广告诊断优化全指导-文字改述版.docx`，SHA-256 `142418a3961cc5bdcd175ef5d16000c5907070ea339df93a5597b3c774707261`，来源 ID `SRC-ceb5e990430e`。

该文件是对亚马逊全球开店官方讲堂课件的文字改述，保留了课程方法和案例，但不是独立的官方政策核验。DOCX 原件保持不变；逐条主张见 `data/processed/amazon_ads_skill/advanced_ads_claims.jsonl` 和 `claim_review_advanced_ads.jsonl`，覆盖报告当前为 `PARTIAL`。不要把“已读”表述成“所有平台机制均已证实”。

## 可直接采用的稳定原则

1. 先诊断再优化：先确认阶段、目标、毛利、库存、数据窗口，再区分展示、点击、详情页转化、订单和利润问题。
2. ACOS、TACOS、ROAS 使用统一口径重算；ACOS 不能单独证明盈利、自然排名或广告质量。
3. 搜索词、定位、广告位、活动、预算和 Business Report 需要组合阅读；动作必须绑定证据和可逆观察窗口。
4. 关键词库按角色分层，至少分离出单词、自然排名目标词、核心词、搜索词、否定词、季节词和风险词。
5. 广泛/词组/精准的结构可作为起点，但触发细节必须以当前市场和账户控制台为准。

## 案例保留与使用

结构化案例保存在 `data/processed/amazon_ads_skill/lecture_case_library_advanced_ads.jsonl`。

- `CASE-ADV-001`：A 灰单，235,017 展示、1,220 点击、CTR 0.52%、CR 4.75%、ACOS 43.33%、TACOS 42.43%，在课程 30% 教学毛利假设下优先检查广告漏斗。
- `CASE-ADV-002`：B 黑单，181,424 展示、897 点击、CTR 0.49%、CR 3.90%、ACOS 63.86%、TACOS 33.89%，数据量足够但亏损信号明显，检查定向/竞价/搜索词/广告位/详情页。
- `CASE-ADV-003`：C 黑套与 D 灰套，分别为 CR 2.85%/1.41%、ACOS 54.22%/137.47%；课程要求同时排查详情页、价格、评论、变体和竞争，不得从案例直接推断“广告无关”。
- `CASE-ADV-004`：20 点击初筛、100 点击提高把握、广告位 +20% 与整体 −10% 联动，是讲义操作参数，不是通用阈值。

引用案例时必须输出：相似指标、关键不匹配、来源状态、缺失数据和验证窗口。案例只作相似性锚点，不得升级为全账户规则。

## 条件化、争议和未决主张

下列内容保留，但必须带标记：

| 内容 | 状态 | 使用限制 |
|---|---|---|
| 30% 毛利粗筛 | `context_dependent` | 必须补充退款、税费、佣金、仓储、促销和现金流成本 |
| 20/100 点击参数 | `context_dependent` | 20 次可作检查点，不能自动否词；结合相关性、AOV、CVR 和目标 |
| 库存 1.5/3 个月 | `unsupported` | 仅为讲义案例阈值，按实际销量、补货周期和季节性重算 |
| 广告位 +20%、整体 −10% | `unsupported` | 仅可作为隔离活动中的小幅可逆测试 |
| 2–6 个月测试期、固定 4–8 周/7 天窗口 | `unresolved` | 不得写成平台扶持或普遍周期；用阶段门槛和归因窗口验证 |
| ABA/POE/前台约 75% 相似、BSR Top20–100 | `context_dependent` | 讲义研究方法，需按市场、类目和工具权限验证 |
| 变体各自独立活动、分时投放 | `context_dependent` | 只有在目标、预算、库存和小时级样本支持时采用 |

亚马逊官方资料（2026-08-13 复核）可确认定义、报告用途和 20 点击否词检查点，但不能替讲义案例证明其余固定比例或时间窗。官方参考：

- [ACOS](https://advertising.amazon.com/en-ca/library/guides/acos-advertising-cost-of-sales)
- [Sponsored Products targeting](https://advertising.amazon.com/en-us/library/guides/targeting-with-sponsored-products/)
- [Sponsored Products best practices](https://advertising.amazon.com/en-us/library/guides/sponsored-products-best-practices/)
- [Search term report](https://advertising.amazon.com/help/G3HEFZYWZF84NPS9)

## 对话提示协议

当用户的问题匹配上述案例或阈值时，必须显式提示：

> `讲义案例提示`：以下结论来自 `SRC-ceb5e990430e` 的课程改述；来源状态为 `supported/context_dependent/unsupported/unresolved`。我会同时给出适用条件、不同路线、缺失数据和可逆验证窗口，不把案例数字当成通用阈值。

如果用户只提供 ACOS、点击或某一个广告位比例，应先请求利润、目标、阶段、库存、CVR、TACOS、自然排名和归因窗口，不得直接套用 A/B/C/D 案例。
