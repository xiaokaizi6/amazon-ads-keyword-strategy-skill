# Example Input Search Term Report

Use these compact inputs to test whether the skill separates advertising efficiency, keyword ranking, product stage, and case evidence instead of giving generic ACOS-only advice.

## Scenario A: 新品期广告结构规划

用户输入:

> 美国站新品，类目是 kitchen organizer，上架第 12 天，售价 29.99 美金，毛利率约 38%。目标不是马上盈利，而是 30 天内跑出可转化搜索词，并把 `under sink organizer`、`bathroom cabinet organizer` 两个词的自然排名从无排名推进到前 3 页。预算每天 80 美金。现在只有一个自动广告，CPC 0.65，CTR 0.32%，CVR 6%，ACOS 58%，TACOS 暂无。请帮我规划广告结构和 7/14/30 天动作。

关键数据:

| Field | Value |
| --- | --- |
| product_stage | launch |
| objective | search term discovery + natural-rank push |
| price | 29.99 |
| gross_margin | 38% |
| daily_budget | 80 |
| current_campaigns | one auto campaign |
| target_rank_keywords | under sink organizer; bathroom cabinet organizer |
| current_metrics | CPC 0.65; CTR 0.32%; CVR 6%; ACOS 58% |

## Scenario B: 搜索词报告优化

用户输入:

> 这是过去 14 天搜索词报告。产品处于稳定期，目标是降无效花费，同时保留可能推自然排名的词。请给搜索词动作表。

| Search term | Match source | Clicks | Spend | Orders | Sales | CPC | CTR | CVR | ACOS | Natural rank |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| under sink organizer | exact | 86 | 92.88 | 7 | 209.93 | 1.08 | 0.48% | 8.1% | 44.2% | page 2 |
| plastic sink shelf | broad | 64 | 38.40 | 0 | 0 | 0.60 | 0.22% | 0% | N/A | no target |
| bathroom cabinet organizer | phrase | 41 | 43.05 | 4 | 119.96 | 1.05 | 0.54% | 9.8% | 35.9% | page 4 |
| kitchen rack replacement | broad | 37 | 18.50 | 0 | 0 | 0.50 | 0.18% | 0% | N/A | irrelevant |
| brand name organizer | exact | 24 | 9.60 | 5 | 149.95 | 0.40 | 1.20% | 20.8% | 6.4% | own brand |

## Scenario C: ACOS 高但可能在推自然排名

用户输入:

> 核心词 `under sink organizer` 最近 14 天 ACOS 78%，CPC 1.35，花费 486 美金，广告订单 12 单，总订单从每天 11 单涨到 19 单，自然排名从第 58 位到第 21 位，TACOS 从 24% 降到 19%。这个广告是不是应该因为 ACOS 高直接关掉？

关键数据:

| Field | Value |
| --- | --- |
| objective | rank push |
| keyword | under sink organizer |
| ACOS | 78% |
| CPC | 1.35 |
| ad_orders | 12 |
| total_orders | 11/day to 19/day |
| natural_rank | 58 to 21 |
| TACOS | 24% to 19% |

## Scenario D: ACOS 低但自然排名不提升、广告单占比高

用户输入:

> ACOS 10%，CPC 0.2，广告单占比 70%，广告位经常在首页第一位，但自然排名一直在 7 页开外。是不是广告效果很好，不用调整？要不要继续加预算？

关键数据:

| Field | Value |
| --- | --- |
| objective | unclear: profit vs natural-rank push |
| ACOS | 10% |
| CPC | 0.2 |
| ad_order_share | 70% |
| ad_rank | top of page |
| organic_rank | outside page 7 |
| missing_metrics | CTR, CVR, category CVR, Session, Unit Session Percentage, TACOS, term-level order mapping |
