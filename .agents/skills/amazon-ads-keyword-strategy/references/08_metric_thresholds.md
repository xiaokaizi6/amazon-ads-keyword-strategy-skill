# Metric Thresholds

Evidence base: extracted records include repeated mentions of ACOS, CPC, CVR, natural rank, orders, and ad order share. The corpus does not support universal numeric thresholds across categories. Preserve source thresholds when present and otherwise use metrics as diagnostic gates.

## Metric Guide

| Metric | Meaning | Use In Decisions | Threshold Guidance |
| --- | --- | --- | --- |
| CTR | Ad click-through rate or search result attraction. | Diagnose image, title, price, ad position, keyword relevance. | No universal threshold in corpus. Compare with category, term, and placement. |
| CVR | Conversion rate after click/session. | Decide whether traffic quality or listing quality can support rank push. | CASE001 has about 4%-5% ad CVR and ranking did not move; CASE014 has exact ad CVR around 20% but auto CVR lower. Use category comparison. |
| CPC | Cost per click. | Controls sample cost, ACOS, and feasibility of big-word attack. | Preserve actual CPC: CASE001 about $0.2, update $0.16; CASE010 mentions high CPC 1.2-1.5; CASE015 mentions competitor ASIN CPC 2.6. |
| ACOS | Ad spend / ad sales. | Profit and campaign efficiency signal. | Never use alone. Low ACOS can still fail ranking; high ACOS may be acceptable in rank push if TACOS/rank improves. |
| TACOS | Total ad spend / total sales. | Whole-account health and ad dependency. | Required when judging whether high ACOS or high ad order share is acceptable. |
| ROAS | Ad sales / ad spend. | Inverse efficiency view of ACOS. | Treat as a reporting translation, not a separate causal metric. |
| 点击数 | Click sample. | Determines whether a term has enough data for add/negative/bid action. | Calculate from expected CVR and margin; do not use a fixed universal click count. |
| 订单数 | Order count. | Confirms conversion and ranking signal strength. | CASE004 uses target-order allocation by keyword; preserve such source-specific calculations. |
| 广告单占比 | Share of orders from ads. | Measures ad dependency and launch/rank-push intensity. | CASE001 70%; CASE002 50%+. High share is not automatically bad; stage and TACOS decide. |
| 自然单占比 | Share of orders from organic traffic. | Indicates whether ads are building independent traffic. | Use with ad order share and natural rank. |
| 花费 | Spend. | Budget control and sample cost. | Must be evaluated by goal: discovery spend, profit spend, rank-push spend, or clearance spend. |
| 毛利 | Gross margin or contribution margin. | Sets allowable CPC, ACOS, and rank-push tolerance. | If unavailable, mark profitability recommendations `low confidence`. |
| 自然排名 | Organic keyword position. | Measures rank-push success. | Track by exact target term; ad orders on other terms are not proof. |
| 广告排名 | Sponsored position. | Shows placement and potential traffic quality. | High ad rank does not guarantee natural-rank improvement. |
| BSR | Best Sellers Rank. | Broad sales/rank context. | Use as supporting context only; not a substitute for keyword rank. |
| Session | Buyer sessions. | Listing traffic denominator. | Needed to separate click quality from listing conversion. |
| Unit Session Percentage | Unit/session conversion. | Product-level conversion quality. | Required when ad CVR and business-report conversion diverge. |

## Diagnostic Combinations

### 官方定义与经验阈值分离

- ACOS and ROAS formulas are stable metric definitions: ACOS is ad spend divided by attributed ad revenue, while ROAS is attributed ad revenue divided by ad spend.
- Amazon does not define one universal good ACOS. Break-even depends on the relevant profit/contribution margin and the campaign objective; the project must not promote the DOCX values such as `CTR >= 0.5%`, `CVR > 10%`, `ACOS <= 15%`, or `广告:自然 4:6` as universal health thresholds.
- Any click, bid, placement, budget, or launch-day number from a lecture remains a source-specific test hypothesis unless category, marketplace, stage, goal, and sample evidence support it.

Source: `references/16_cpc_playbook_integration.md` (CPC-CLM-001, CPC-CLM-002, CPC-CLM-013, CPC-CLM-014).

### Low ACOS + Weak Natural Rank

- Check CPC, ad position, CTR, CVR, order volume, ad-order term versus target natural term.
- CASE001 is the anchor case.
- Confidence: medium as a diagnostic pattern, not a universal rule.

### High ACOS + Rank Objective

- Check whether the ad is intentionally buying ranking signal.
- Continue only if natural rank, total orders, or TACOS supports the spend.
- Otherwise lower bid, restructure, or stop the term.

### High Ad Order Share

- New launch: may be normal temporarily.
- Stable phase: diagnose ad dependency, natural order share, and TACOS.
- Never reduce ads blindly without checking whether rank or total orders collapse.

### Clicks Without Orders

- Compare sample size to expected CVR.
- If sample is enough and relevance is weak: negative.
- If sample is not enough and relevance is strong: observe or lower bid.

## Common Mistakes

- Setting one ACOS target for every stage.
- Ignoring TACOS and natural order share.
- Treating low CPC as proof of good traffic.
- Comparing ad CVR without checking Session and Unit Session Percentage.
- Using universal click thresholds for否词.

## Quality Checklist

- Source-provided thresholds are preserved as written.
- Missing metrics are listed before giving a decision.
- Margin and product stage are included.
- ACOS is interpreted with TACOS, CVR, CPC, order count, and rank.
- Evidence from comments is capped at medium confidence.
