# Example Output Keyword Strategy

Example response for Scenario A: launch-stage campaign structure and keyword strategy.

## 1. 当前诊断

新品第 12 天只有一个自动广告，数据不足以支撑自然排名推进。当前结构缺少跑词、转化验证、排名目标词和防浪费边界的拆分，容易出现自动广告吃满预算但无法判断哪些词该加精准、哪些词该否定。

## 2. 数据完整性检查

已有产品阶段、价格、毛利、日预算、目标词、CPC、CTR、CVR、ACOS。缺少搜索词报告、广告位、Session、Unit Session Percentage、类目平均 CTR/CVR、竞品价格评论、自然排名初始记录、TACOS。

## 3. 产品阶段判断

这是新品期，核心目标是获取有效搜索词和建立目标词自然排名，不应按稳定期利润逻辑直接砍掉高 ACOS 广告。ACOS 58% 需要监控，但只要样本在积累、词相关且自然排名有推进，可以接受阶段性偏高。

## 4. 关键词分类

| Keyword | Role | Strategy |
| --- | --- | --- |
| under sink organizer | 核心词 / 排名目标词 | 单独精准组，记录广告位和自然排名 |
| bathroom cabinet organizer | 核心词 / 排名目标词 | 单独精准或 phrase 验证组 |
| under sink storage rack | 属性词 / 长尾词 | phrase 或 exact，低预算验证 |
| cabinet shelf organizer | 探索词 | 自动和 broad 中跑词 |
| own brand terms | 防守词 | 有品牌搜索后再低预算防守 |

## 5. 广告结构诊断

建议拆为 5 类广告：自动跑词、手动 broad 探索、手动 phrase 控制相关流量、手动 exact 排名目标、ASIN/商品投放测试。每类广告必须有独立预算和判断标准，避免自动广告和排名词互相抢预算。

## 6. 搜索词动作表

| Source | Rule | Action |
| --- | --- | --- |
| 自动广告 | 出单且相关 | 提取到 exact 或 phrase |
| 自动广告 | 点击多无单且意图不相关 | 否定精准或否定词组 |
| broad | 有点击无单但样本不足 | 继续低预算观察 |
| phrase | CVR 接近类目平均 | 提到 exact 验证 |
| exact rank target | 排名提升但 ACOS 高 | 看 TACOS、自然排名和总订单，不直接关闭 |

## 7. 竞价和预算调整

日预算 80 美金可先拆为：自动 20、broad 15、phrase 15、exact 排名目标 25、ASIN 测试 5。exact 排名目标词用固定或动态只降低策略时要先确认广告位；如果 CTR 低，先处理主图、标题、价格或广告位，而不是只加竞价。

## 8. 自然排名与广告关系判断

要把“出单词”和“排名目标词”分开。自动或 broad 跑出的中小词能证明链接有部分转化能力，但不代表 `under sink organizer` 这种大词自然排名会同步提升。目标词必须单独跟踪广告位、CTR、CVR、订单数、自然排名和 TACOS。

## 9. 案例相似性提示

CASE001/CASE002 提醒：广告单多、低 ACOS 或广告位靠前，都不能自动推出自然排名会提升。新品期可以允许广告单占比高，但 14-30 天内必须看到自然排名、自然单占比或 TACOS 的改善。

## 10. 风险和例外

如果类目 CPC 普遍高、评论少、价格无优势，强攻核心词会快速消耗预算。若 Session 和 Unit Session Percentage 低于类目均值，优先修 listing 和转化，不要把所有问题都用竞价解决。

## 11. 7 天 / 14 天 / 30 天行动计划

7 天：拆 5 类广告；记录两个目标词自然排名基线；每天导出搜索词；补广告位和 CTR。

14 天：把有订单的相关搜索词迁移到 exact；否定明显无关词；比较 target exact 的 CVR 与类目均值。

30 天：复盘目标词是否进入前 3 页；若 TACOS 下降且自然排名改善，保留排名预算；若只出中小词订单而大词不动，降低大词冲刺强度并重选更可达的阶段目标。
