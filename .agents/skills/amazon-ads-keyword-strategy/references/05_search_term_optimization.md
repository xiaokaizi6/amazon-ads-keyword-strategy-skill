# Search Term Optimization

## Contents

- [搜索词报告诊断逻辑](#搜索词报告诊断逻辑)
- [加精准逻辑](#加精准逻辑)
- [否定与竞价动作](#否定精准逻辑)
- [样本不足处理](#样本不足处理)
- [高广告依赖诊断](#广告单占比过高的诊断逻辑)

Evidence base: search-term logic is supported by keyword-research, bidding/budget, ranking, and conversion records. The extracted corpus contains both direct rules and counterexamples, so every action must be conditional.

## 搜索词报告诊断逻辑

For each search term, inspect:

- relevance to product and listing promise,
- clicks and spend,
- orders and CVR,
- CPC and ACOS,
- TACOS or total-account impact when available,
- match type and campaign source,
- whether it is a profit term, discovery term, or ranking target,
- natural rank movement for the same term.

Do not judge a term only by ACOS. Low ACOS may come from low CPC or low volume; high ACOS may be acceptable during rank-push or launch if total goals are improving.

### 官方报告边界与否词检查点

- Amazon 官方说明 Sponsored Products search term report 只列出至少产生一次广告点击的搜索词；零点击展示应回到 targeting/placement/campaign 数据诊断。
- Amazon 官方建议在添加 negative target 前至少观察 20 次点击。项目将其作为 review checkpoint，而不是跨类目、客单价和转化周期通用的自动否词阈值。
- 20 次点击之后仍要结合相关性、预期 CVR、CPC、毛利、产品阶段和广告目标；战略排名词或高客单低频产品可先降价/隔离测试。

Source: `references/16_cpc_playbook_integration.md` (CPC-CLM-007, CPC-CLM-021; Amazon Ads official pages checked 2026-08-12).

## 加精准逻辑

Add a search term into exact when:

- it has orders or strong conversion signal,
- relevance is high,
- CPC is within margin tolerance or rank-push budget,
- it matches either a profit target or a natural-rank target,
- the term has enough sample to avoid accidental promotion.

If the term is only a comment-suggested opportunity, mark `low confidence` until backend data verifies it.

## 否定精准逻辑

Use negative exact when:

- the exact query is irrelevant,
- sample size is enough and no orders occur,
- CPC/spend exceeds the planned test budget,
- the term conflicts with product positioning.

Avoid negative exact when the term is a strategic ranking target and the sample is still too small; consider lowering bid or isolating the test first.

## 否定词组逻辑

Use negative phrase when:

- a repeated irrelevant pattern appears across search terms,
- a modifier changes intent away from the product,
- broad/phrase is repeatedly matching off-target traffic.

Do not use phrase negative for a single weak term if related modifiers may still be valuable.

## 降竞价逻辑

Lower bids when:

- CPC is above margin tolerance,
- clicks are accumulating without conversion after sufficient sample,
- ACOS/TACOS is above the target and no ranking objective justifies the spend,
- ad position is too expensive relative to conversion.

Do not lower solely because ACOS is high if the campaign is explicitly pushing natural ranking and natural rank, total orders, or TACOS are improving.

## 提竞价逻辑

Raise bids when:

- term is relevant and has conversion proof,
- current ad position is below the needed test/rank position,
- budget and margin allow more sample,
- target natural rank requires exposure and orders under the same term.

Set a review window before raising. For high-CPC or big-word campaigns, define the stop-loss first.

## 继续观察逻辑

Continue observing when:

- sample is below the calculated click/order threshold,
- relevance is high but the term has not had enough traffic,
- product is in new launch learning phase,
- high-ticket or low-frequency products need longer conversion windows.

Continue observing does not mean unlimited spend. Cap the budget and schedule the next review.

## 样本不足处理

Sample size is insufficient when clicks, spend, or order opportunity are too small to compare with expected CVR. Use:

- expected CVR,
- CPC,
- gross margin,
- target order count,
- keyword role,
- product stage.

If exact thresholds are unavailable, mark decision as `low confidence` and avoid hard negatives.

## 低 ACOS 但自然排名不动的诊断逻辑

Check in this order:

1. Is low ACOS caused by low CPC rather than strong CVR?
2. Is order volume enough to influence the target term?
3. Is the ad-order term the same as the natural-rank target term?
4. Is ad position actually on the search page or mostly product pages?
5. Are CTR, CVR, Session, and Unit Session Percentage competitive?
6. Is ad order share high while natural order share is weak?
7. Are orders concentrated in中小词 while the goal is大词?

CASE001 is the anchor example: ACOS around 10%, low CPC, high ad order share, ad rank first, but natural rank stayed weak. Treat it as a diagnostic case, not a universal law.

## 广告单占比过高的诊断逻辑

Check:

- product stage,
- ad objective,
- natural order share,
- TACOS,
- natural rank movement,
- whether ad spend is buying the target term or only auxiliary terms,
- whether activities/deals can supplement traffic,
- whether lowering ads would collapse rank or only remove waste.

Conflict C002 says high ad order share is not automatically good or bad; stage and goal decide the action.

## Common Mistakes

-否词 before sample size is meaningful.
- Adding every converting term to exact without checking role and margin.
- Raising bid on high-CPC exact terms without a natural-rank target.
- Treating low ACOS as proof of keyword ranking progress.
- Ignoring Session and Unit Session Percentage when diagnosing conversion.

## Quality Checklist

- Search term relevance is stated.
- Clicks, spend, orders, CPC, CVR, ACOS, and TACOS are reviewed where available.
- Sample-size status is explicit.
- Action is one of: add exact, negative exact, negative phrase, lower bid, raise bid, continue observation.
- Natural-rank target is checked separately from ad orders.
- Low-confidence decisions are marked when data is missing.
