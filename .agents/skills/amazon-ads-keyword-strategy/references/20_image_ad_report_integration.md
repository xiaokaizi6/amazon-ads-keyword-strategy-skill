# 20. 图片版广告报告资料的交叉验证层

来源：`亚马逊广告报告高效分析和优化-Word版 (1).docx`，来源 ID `SRC-3d7548bc16d9`，SHA-256 `4f86052532fa78f574d886957bb66860351e4b845332a4addd6499b96c860e69`，证据簇 `EC-4f86052532fa`。该 Word 没有可提取的正文，实际读取为 12 张 1654×2339 图片并逐张检查；因此自动来源清单仍标记 `readable:false`，不能把“图片已人工检查”写成脚本自动可读。

原子主张和案例：

- `data/processed/amazon_ads_skill/new_source_bundle_claim_review.jsonl`：`ADREP-CLM-001` 至 `ADREP-CLM-006`
- `data/processed/amazon_ads_skill/new_source_bundle_case_records.jsonl`：`SRC-3d7548bc16d9-CASE-001` 至 `CASE-004`

## 1. 可以吸收的诊断框架

- Placement、Advertised Product、Purchased Product、Search Term、Targeting、Budget 和 Performance over time 可作为报告候选集合；先按当前广告产品/账户权限确认字段。
- 把活动按“排名目标、词发现、相关流量、利润”分组有助于定义 KPI，但不代表 Amazon 以此固定分配自然排名权重。
- Placement 报告应同时读展示、点击、CTR、CPC、订单、CVR、ACOS/TACOS，并将位置差异和目标（利润、增量、可见性）分开。
- Purchased Product 报告可以发现广告入口与实际购买 ASIN 不一致的路径；后续交叉销售、Brand Story、A+ 或 ASIN 投放都必须先验证相关性、利润、库存和重复样本。
- Budget 报告适合诊断预算耗尽与在线时长；加预算需要边际订单/利润和库存证据，而不是固定“70%在线”线。

## 2. 需要保留但不能升级的观点

| 观点 | 状态 | 回答时的边界 |
|---|---|---|
| SP 精准关键词“最有效/直接推动自然排名”，SB/SD 排名作用弱 | `disputed` | 可以作为一个假设路线；同时提示项目中“广告单高但自然位不升”的反例和 Amazon 资料只支持潜在关联。必须用自然位时间序列和对照验证。 |
| TOS `+900%`、基础 bid `$0.02/$0.2`、预算 `$5-$10` | `unsupported`/高风险 | 不得复制；若用户明确要求研究，只能设计极小、可逆、有利润上限的实验。 |
| 排名词 ACOS `50%-60%` 可以接受 | `context_dependent` | 仅在明确排名目标、毛利、库存、总订单和复盘窗口时讨论；不是平台线。 |
| Top 加价 `10%-20%`、Rest of Search 作为增量 | `context_dependent` | 先看位置级样本量、边际 CPC/CVR、库存和目标；一次只改一个 placement 变量。 |
| 在线时长超过 `70%` 即足够 | `unsupported` | 只作为来源例子；按时段需求、预算耗尽、边际利润和库存决定。 |

官方参考：[Sponsored Products targeting](https://advertising.amazon.com/en-us/library/guides/targeting-with-sponsored-products/)、[Sponsored Products best practices](https://advertising.amazon.com/en-us/library/guides/sponsored-products-best-practices/)、[placement 调整说明](https://advertising.amazon.com/resources/whats-new/improve-campaign-performance)、[Amazon 对视频广告与自然排名的研究](https://advertising.amazon.com/en-ca/library/news/video-ads-organic-ranking-impact)。这些资料支持目标化投放、报告分析和“可能的关联”，不支持固定 TOS/ACOS 数字或单一广告类型的排名保证。

## 3. 来源案例提示

- `SRC-3d7548bc16d9-CASE-001`：Top/Rest/Product Page/Offsite 的 CTR、CVR、订单差异。原始分母、日期和归因窗口缺失，置信度 `medium`；可用于演示位置级诊断，不能外推 +10%-20%。
- `SRC-3d7548bc16d9-CASE-002`：广告 ASIN `QW` 入口后购买 ASIN `RL` 约 9 件。可作为购买路径假设，不能凭单个案例改投 RL。
- `SRC-3d7548bc16d9-CASE-003`：三个活动在线时长 `34.94/45.98/41.10`。缺少小时定义、日期、预算耗尽与边际利润，不能推出70%阈值。
- `SRC-3d7548bc16d9-CASE-004`：`TOS +900%` 与 1-2 点击出单停止规则。置信度 `low`，属于高风险反例；不得当成模板。

## 4. 主动提示规则

问题涉及“广告能否推自然排名”“TOS 100%-200%/900%”“精准词是否一定比 SB/SD 强”“低 ACOS 是否可直接加预算”时，必须显示：`讲义案例提示`、来源 ID/案例 ID、状态、匹配条件、关键不匹配、另一种做法和可逆验证窗口。回答应把广告归因订单、自然订单、自然排名、TACOS、库存和 Listing/价格变化分开，不能把图文作者的因果解释改写成平台机制。
