# CPC Playbook Integration and Cross-Validation

## Contents

- [审查范围和状态](#审查范围和状态)
- [可纳入 skill 的稳定内容](#可纳入-skill-的稳定内容)
- [必须条件化或保留争议的内容](#必须条件化或保留争议的内容)
- [条件化主张的使用模板](#条件化主张的使用模板)

本文件把用户提供的《亚马逊CPC广告打法知识体系全梳理v1_20260804(1).docx》纳入 skill，但不把整理稿当成 Amazon 官方规则。原子主张审查记录位于：

- `data/processed/amazon_ads_skill/cpc_playbook_claims.jsonl`
- `data/processed/amazon_ads_skill/claim_review_cpc_playbook.jsonl`
- `data/processed/amazon_ads_skill/source_validation_cpc_playbook_review.md`
- 来源：`SRC-214ee7c1e651`
- SHA-256：`123d25a4a09a3580fbe39aa183c86420c76e403283cf257fc1f8c11005de6693`
- 审查日期：2026-08-12

## 审查范围和状态

本批 claim 与用户文档、项目语料中与 ACOS、匹配方式、广告结构、排名停滞、新品和商品定位最相关的记录交叉检查，并核对 Amazon Ads 官方页面。项目清单共 101 个来源，但本批只直接检查了 6 个项目来源和该 DOCX，因此覆盖报告为 `PARTIAL`，不能声称已经核对全部项目资料。

21 条原子主张的状态：

| 状态 | 数量 | 处理方式 |
| --- | ---: | --- |
| `supported` | 13 | 可作为带条件的规则或平台定义使用 |
| `context_dependent` | 1 | 保留策略，但必须声明前提 |
| `disputed` | 1 | 同时保留支持和反例，不做单向因果结论 |
| `unresolved` | 5 | 保留为待验证主张，不进入强规则 |
| `unsupported` | 1 | 保留来源观点，但不得作为通用阈值 |

## 可纳入 skill 的稳定内容

### 1. 公式和目标

- `ACOS = ad spend / attributed ad sales`，`ROAS = attributed ad sales / ad spend`。公式成立不代表目标相同。
- 不存在跨类目、阶段和目标通用的“好 ACOS”。先确定利润、放量、排名、品牌防守或清库存目标，再用贡献毛利、TACOS、订单、CVR、CPC 和自然排名判断。
- 盈亏平衡 ACOS 与可用于广告的利润/贡献毛利有关；成本口径必须在账户中明确，不能把“毛利率”未经定义直接当作可承受 ACOS。

### 2. Sponsored Products 定向

- 自动定向包括 close match、loose match、substitutes、complements。
- 手动关键词包括 broad、phrase、exact。Broad 可扩展同义词、变体和相关意图；phrase 更受限；exact 更受限但不保证在所有产品上表现最好。
- 同一个词放入多个 match type 不自动等于自我竞价；应在隔离预算和不同目标下比较实际查询、CPC、CVR、订单和排名。
- 商品定向可以选择单个商品、类目、品牌或商品特征；ASIN 与类目要按目标和竞品可战性拆分测量。

### 3. 报告和搜索词动作

- Search term report 只包含至少产生一次广告点击的搜索词；它不能解释所有零点击展示。
- Targeting report 用于查看至少有一次展示的关键词/商品/类目投放；advertised product、placement、performance over time 等报告承担不同维度，不能互相替代。
- 相关且有足够样本的高表现搜索词可以提取到 exact/phrase；低表现或不相关目标可以降价或添加 negative，但不能只看 ACOS。
- Amazon 官方建议在添加 negative target 前至少观察 20 次点击；这是检查点，不是适用于所有类目和目标的转化阈值。

### 4. 广告结构和广告位

- discovery、profit、defense、conquest、rank-test 等目标应拆开 campaign/ad group，便于预算和结果解释。
- TOS、ROS、product pages 要分别读 placement report；placement bid adjustment 是测试杠杆，不是固定的 2-3 倍 CVR 或 50%-200% 溢价规则。
- exact 高于 phrase、phrase 高于 broad 可以作为 Amazon 官方的起始建议，但仍需用本账户的 CPC、CVR、订单、TACOS 和目标判断。

## 必须条件化或保留争议的内容

### 1. 自动转手动

文档中的“1,000 次点击、单词 100 次点击、至少 3 次转化”等数字不能升级为通用门槛。可保留的规则是：相关搜索词达到足够样本后，复制到隔离的手动活动测试，同时保留发现源，避免把一次偶然出单当成稳定词。

### 2. 广告订单与自然排名

文档支持“精准广告集中预算可以推排名”，项目 CASE001、CASE002、CASE009、CASE012 也显示广告数据好看时自然排名可能仍停滞。当前结论为 `disputed`：必须确认广告订单是否来自同一个目标词、自然订单占比、自然排名历史、Listing CVR、广告位和 TACOS；不得直接说“广告单一定提升自然排名”或“广告单一定无效”。

### 3. TOS、阶段时间轴和经验阈值

“新品 0-1 个月不碰 TOS”“1-3 个月 TOS+BID 100%-200%”“TOS CVR 通常是 PP 2-3 倍”“新品有 3 个月流量扶持”均不是当前可泛化的官方规则。保留为来源经验/待测假设，必须结合站点、类目、利润、库存、广告目标和控制组验证。

### 4. 平台机制和时效功能

- DOCX 的 quality-score 扣费公式和简化 Ad Rank 因果没有被当前官方页面确认，不能写成平台机制。
- 报告回溯天数、Prompts 等功能和后台名称随账户/市场变化，使用前必须查当前 Ads Console/API 或官方帮助。
- Sponsored Products video 的当前官方指南支持 1-5 个产品功能视频、每个至少 7 秒且没有固定最长时长；具体资格和创意政策仍要按目标市场检查。

## 官方核对来源（2026-08-12）

- [Amazon Ads: ACOS](https://advertising.amazon.com/en-ca/library/guides/acos-advertising-cost-of-sales)
- [Amazon Ads: ROAS](https://advertising.amazon.com/library/guides/return-on-ad-spend-roas)
- [Amazon Ads: Sponsored Products targeting](https://advertising.amazon.com/en-us/library/guides/targeting-with-sponsored-products/)
- [Amazon Ads: Sponsored Products best practices](https://advertising.amazon.com/en-us/library/guides/sponsored-products-best-practices/)
- [Amazon Ads: Sponsored Products search term report](https://advertising.amazon.com/help/G3HEFZYWZF84NPS9)
- [Amazon Ads: rest-of-search placement bid adjustment](https://advertising.amazon.com/resources/whats-new/improve-campaign-performance)
- [Amazon Ads: Sponsored Products video](https://advertising.amazon.com/library/guides/sponsored-products-video)

## 操作时的强制检查

1. 先写产品阶段、广告目标、站点、类目、价格、可用利润和库存。
2. 把出单词、自然排名目标词和广告位分开记录。
3. 对每个动作同时查看 CTR、CVR、CPC、订单、ACOS、TACOS、广告/自然订单占比和自然排名。
4. 否词前先检查相关性和样本；20 次点击是官方检查点，不是自动否词命令。
5. 任何固定百分比、固定天数、固定点击阈值和平台机制说法都标记来源、适用条件、验证窗口和停止标准。
6. 交叉验证覆盖为 `PARTIAL` 或 `NOT_READY` 时，回答中不得写“已核对全部项目资料”。

## 条件化主张的使用模板

当用户要求使用下列未升级为通用规则的内容时，必须按模板输出，而不是删除它们：

```text
主张：<原子主张>
来源状态：context_dependent / disputed / unresolved / unsupported
支持路线：<什么条件下可以尝试>
保守路线：<什么条件下不采用或采用较低风险动作>
缺失数据：<站点、类目、阶段、毛利、预算、样本、目标词、自然排名等>
验证窗口：<7/14/30 天或足够点击/订单后的复盘点>
成功标准：<目标指标>
停止标准：<预算、TACOS、库存、排名或转化恶化阈值>
```

### 示例：TOS 100%-200% 溢价

- 来源状态：`unresolved` / `unsupported`，不是平台通用阈值。
- 支持路线：目标是首页曝光或排名、Listing CVR 已经可接受、库存和预算允许，并且 placement report 显示有测试空间时，做小幅、限时增量测试。
- 保守路线：利润目标、库存紧张、TACOS 已超边界或 placement CVR 不足时，不按讲义比例直接加价；先保持基础出价或拆出独立测试活动。
- 缺失数据：TOS/ROS/PP 分位数据、同词自然排名、毛利、预算消耗速度、库存天数。
- 验证窗口：7-14 天；成功标准为目标词曝光/排名改善且 TACOS、CVR 在边界内；停止标准为花费失控、CVR 下滑或自然排名无变化。

### 示例：广告单是否推动自然排名

- 来源状态：`disputed`。
- 支持路线：广告订单来自同一自然排名目标词，且自然排名、自然订单或总订单同步改善时，限期保留排名测试。
- 保守路线：广告订单主要来自品牌词、中小词、ASIN 或商品页，目标大词排名不变时，不把广告单视为排名证据；拆分预算并检查 Listing/相关性。
- 缺失数据：同词广告订单、自然订单、排名历史、广告位、归因窗口、整体 Session/Unit Session Percentage。
- 验证窗口：至少 7-14 天或预设订单样本；成功标准必须包含自然排名变化，不能只看 ACOS。

### 示例：新品三个月流量扶持

- 来源状态：`unresolved`。
- 使用方式：只能作为待验证的阶段假设，用 cohort 数据观察曝光、CVR、总订单、TACOS、自然排名和库存，不得直接据此延长预算或断言平台机制。

### 示例：质量得分扣费公式

- 来源状态：`unresolved`。
- 使用方式：可作为讲义中保留的解释模型，但回答必须声明 Amazon 当前官方资料未确认该公式；实际决策只使用可观测的出价、实际 CPC、placement、CTR、CVR、订单和花费。

## Common Mistakes

- 把整理者的“老板视角点评”当成 175 个独立证据。
- 把同一个来源中的案例、阈值和因果机制合并成一条规则。
- 用官方定义证明一个未被官方定义的排名因果。
- 把 20 次点击、TOS 百分比或 3 个月时间轴变成所有账户的自动化动作。
- 只看 ACOS，不看 TACOS、目标词、自然排名和样本量。

## Quality Checklist

- 新主张有来源 ID、原文位置、状态、置信度和验证测试。
- `supported` 只用于定义或条件清楚且有适用证据的内容。
- `disputed`、`context_dependent`、`unresolved` 的不同路线没有被删除。
- 平台机制和功能有当前官方来源与核对日期。
- 覆盖报告明确列出未检查来源和不可读来源。
