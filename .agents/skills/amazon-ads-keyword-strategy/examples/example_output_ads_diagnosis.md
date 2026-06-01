# Example Output Ads Diagnosis

Example response for Scenario B and Scenario C: search term report optimization with a high-ACOS rank-push exception.

## 1. 当前诊断

不能只按 ACOS 做统一开关。当前账户同时存在三类词：可保留的排名目标词、可否定或降权的无效探索词、需要单独防守的品牌词。`under sink organizer` ACOS 高，但自然排名从 58 位升到 21 位、TACOS 从 24% 降到 19%，更像排名推进中的阶段性高 ACOS，而不是直接失败。

## 2. 数据完整性检查

已有点击、花费、订单、Sales、CPC、CTR、CVR、ACOS、自然排名。缺少毛利下的目标 ACOS、类目平均 CTR/CVR、广告位分布、Session、Unit Session Percentage、自然单占比和搜索词到自然排名目标词的一致性校验。

## 3. 产品阶段判断

Scenario B 是稳定期控成本，Scenario C 是排名爬坡期。两个目标不能混在一个预算池里判断：控成本词看利润和无效花费，排名词看自然排名、总订单和 TACOS 是否改善。

## 4. 关键词分类

| Keyword | Classification | Reason |
| --- | --- | --- |
| under sink organizer | 核心词 / 排名目标词 | 有自然排名推进目标，当前从 58 位到 21 位 |
| bathroom cabinet organizer | 核心词 / 候选排名目标词 | 订单和 CVR 可用，但自然排名仍在 page 4 |
| plastic sink shelf | 探索词 / 待验证词 | 有点击无订单，相关性需要复查 |
| kitchen rack replacement | 无关词 / 否定候选 | 搜索意图不匹配且无订单 |
| brand name organizer | 防守词 | 自有品牌词，高 CVR、低 ACOS |

## 5. 广告结构诊断

排名目标词应从普通控成本广告中拆出，独立预算、独立竞价和独立复盘周期。无关 broad 流量不能和核心词共用预算，否则会稀释排名词样本。品牌防守词应保留低预算，不用拿来证明全账户增长。

## 6. 搜索词动作表

| Search term | Action | Reason | Review window |
| --- | --- | --- | --- |
| under sink organizer | 保留独立精准排名组，暂不因 ACOS 78% 关闭 | 自然排名和 TACOS 同时改善 | 7 天看排名、TACOS、总订单 |
| bathroom cabinet organizer | 加入精准或提高 phrase 权重，小幅提预算 | 41 点击 4 单，CVR 9.8%，自然排名 page 4 | 14 天看能否进 page 3 |
| plastic sink shelf | 降竞价或继续小预算观察 | 64 点击无订单，样本已偏弱但需确认相关性 | 7 天或再给有限测试预算 |
| kitchen rack replacement | 否定精准，必要时否定词组 | 意图不相关且 37 点击无订单 | 立即 |
| brand name organizer | 保留防守，不扩成增长预算 | 高 CVR、低 ACOS，但属于品牌流量 | 每周看增量和 TACOS |

## 7. 竞价和预算调整

`under sink organizer` 不建议直接降竞价，应先看广告位和 CTR。如果排名目标是继续进首页，可保留当前竞价或小幅调整，但必须设止损：自然排名停滞、TACOS 上升、CVR 低于类目均值时停止加预算。无订单 broad 词先降 20%-30% 或限制预算。

## 8. 自然排名与广告关系判断

高 ACOS 不等于广告失败。这个词的自然排名从 58 位到 21 位，且 TACOS 下降，说明广告可能在带动总流量结构改善。判断重点是广告出单词是否就是目标排名词，以及排名提升是否带来自然单和总 Session 增长。

## 9. 案例相似性提示

该输入更接近“高 ACOS 但排名改善”的排名推进场景，不应套用低 ACOS 案例。可以对照 CASE001 的反面提醒：广告数据好看也不一定推动自然排名，所以本例需要持续跟踪自然排名和 TACOS，不能只看广告报表。

## 10. 风险和例外

如果毛利无法承受 78% ACOS，或排名 7 天内停止改善，继续烧词会变成预算浪费。如果广告位主要在商品页而非搜索结果页，该词对自然搜索排名的帮助可能弱于预期。评论区观点只能作为假设，不能作为高置信规则。

## 11. 7 天 / 14 天 / 30 天行动计划

7 天：拆分排名目标精准组；否定 `kitchen rack replacement`；补广告位、CTR、Session、Unit Session Percentage、TACOS。

14 天：复盘 `under sink organizer` 是否继续进位；把 `bathroom cabinet organizer` 建精准组；压缩无订单 broad 预算。

30 天：比较自然单占比和 TACOS；若排名词进入 page 1-2 且自然单增长，逐步降低排名组竞价；若排名停滞，重新评估 listing CVR、价格、评论和类目竞争。
