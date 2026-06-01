# Keyword Classification

Evidence base: `merged_rules.jsonl`, `case_library.jsonl`, and `conflict_candidates.jsonl`. The strongest repeated themes are keyword ranking, search-term mining, bidding/budget control, and the separation between profitable order terms and natural-rank target terms. Comment-derived ideas are usable only as `medium` or `low confidence` diagnostic inputs.

## Core Principle

Do not classify a keyword by name alone. Classify it by role:

- whether it is intended to generate profitable orders,
- whether it is intended to push natural ranking,
- whether it is only a discovery/testing term,
- whether the product can actually convert under that search intent,
- whether the current product stage can afford the CPC and sample size.

## Keyword Types

| Type | Definition | 判断标准 | 适合广告结构 | 适合产品阶段 | 常见误判 | 优化动作 |
| --- | --- | --- | --- | --- | --- | --- |
| 核心词 | Directly describes the product's main demand and usually carries strategic traffic. | Search intent matches product; competitor set is relevant; rank movement matters to the business. | Manual exact for rank tracking; phrase/broad or auto for expansion; separate budget if it is a ranking target. | New launch after listing readiness, growth, stable, seasonal preheat. | Treating every high-volume word as a core word. | Track ad rank and natural rank separately; compare CTR/CVR with category level; do not judge by ACOS alone. |
| 长尾词 | More specific keyword with modifiers, attributes, use cases, or lower volume. | Lower competition, clearer intent, usually easier to convert. | Phrase, exact, or broad from known root; move proven terms into exact. | New launch, growth, low-budget testing, seasonal preheat. | Assuming long tail cannot help ranking or profit. | Use for early conversion and data; if orders accumulate, map to related core word but do not assume automatic rank transfer. |
| 竞品词 | Competitor brand, ASIN, or product-specific search path. | Searcher is comparing or already near a competitor page. | ASIN targeting, product targeting, category/price/review filters, defensive or offensive manual structure. | Stable/growth with clear competitor advantage; selective new launch if product has price/review edge. | Targeting strong competitors without checking competitiveness. | Compare price, review, rating, image, offer, CPC, and page position; cap budget until CVR is proven. |
| 品牌词 | Own brand or competitor brand query. | Brand name or branded phrase is the primary intent. | Brand defense exact; Sponsored Brands; limited competitor attack if legally and commercially appropriate. | Stable and growth; new launch after brand assets exist. | Mixing brand defense with generic acquisition. | Separate reporting; keep low-cost defense; check policy and relevance before competitor brand targeting. |
| 防守词 | Terms used to protect own traffic from competitors. | Own brand, own ASIN, own product family, high repeat buyer intent. | Exact, product targeting on own ASINs, Sponsored Brands, Sponsored Display where appropriate. | Stable, mature, seasonal peak. | Treating defense spend as the same as growth spend. | Measure incremental protection and TACOS; keep budget efficient. |
| 属性词 | Material, size, color, function, compatibility, or price-related modifier. | Attribute appears in product detail and buyer intent. | Phrase/exact for known attributes; broad only when noise is controlled. | All stages if listing supports the attribute. | Bidding attributes that the listing does not clearly satisfy. | Verify listing text and image support; split high-CVR attributes into exact campaigns. |
| 场景词 | Use case, occasion, season, audience, or problem-solution query. | Intent depends on context rather than product noun alone. | Phrase/broad for discovery; exact after conversion; seasonal campaign if time-bound. | Seasonal preheat, new launch, growth. | Entering too late in a short seasonal window. | Use pre-season search trend and competitor sales data; do not wait for peak week to begin testing. |
| 低相关词 | Search term has some lexical overlap but weak buyer fit. | Clicks appear but conversion is weak, or product fails the intent. | Usually exclude or isolate in test campaigns only. | Limited tests only. | Keeping it because it has high search volume. | Lower bid, isolate, or negative after sufficient sample; check if listing can be repositioned before final denial. |
| 垃圾词 | Irrelevant, misleading, accidental, or budget-wasting query. | No product fit; no conversion path; repeated spend without signal. | Should not enter rule or active growth campaigns. | None. | Calling a term garbage before sample is sufficient. | Negative exact/phrase depending on search-term pattern; document evidence. |
| 中小词 | Mid/small search volume word with manageable competition. | Can generate orders but may not represent the core ranking target. | Exact for profitable terms; phrase/broad to find variants; budget can be controlled. | New launch, growth, stable profit capture. | Assuming中小词出单 will push大词自然排名. | Keep for profit and base conversion; separately track大词 natural rank target. |
| 大词 | High-volume, highly competitive generic or core-category word. | High search volume, high CPC, strong competitors, strategic natural-rank value. | Dedicated exact/rank-push campaign; test with long-tail path first; strict budget boundary. | Growth or stable; new launch only with adequate review, conversion, budget, and margin. | Burning budget because the word is "important". | Define ranking target, acceptable TACOS, sample size, and stop-loss before bidding up. |
| 出单词 | Search term that has produced attributed ad orders. | Search-term report shows orders under the term. | Move to exact; isolate if volume and strategic value justify. | All stages. | Treating any出单词 as the natural ranking target. | Check if it matches product strategy, margin, and natural-rank target; compare CVR, CPC, ACOS, TACOS. |
| 排名目标词 | Keyword whose natural rank improvement is an explicit objective. | Natural rank is tracked and business needs that traffic source. | Separate exact campaign, rank tracking, budget/rank review cadence. | Growth, stable, seasonal preheat; selective launch. | Using low ACOS on unrelated terms as proof ranking work is succeeding. | Track ad position, CTR, CVR, orders, natural rank, TACOS, and whether ad orders occur under the same target term. |

## Source-Based Notes

- CASE001 and CASE002 show that low ACOS, ad rank, and order volume can coexist with weak natural rank; this supports separating `出单词` from `排名目标词`.
- Conflict C008 and C009 require checking whether the ad-order term and natural-rank target are the same term.
- Conflict C004 requires treating broad match as a testing structure, not a default growth answer.
- If the only support is a comment, keep the recommendation at `medium` or `low confidence`.

## Common Mistakes

- Classifying keywords only by search volume.
- Treating low ACOS as proof that a keyword can push natural rank.
- Moving every converting long-tail term into the same campaign as core rank targets.
- Calling a term garbage before reaching a meaningful click/order sample.
- Ignoring margin, budget, and product stage when deciding whether to attack a big word.
- Treating comment advice as confirmed rule without backend evidence.

## Quality Checklist

- Keyword role is labeled: profit, discovery, defense, competitor attack, or ranking target.
- Product stage is stated.
- Search-term data includes clicks, spend, orders, CPC, CVR, ACOS, and ideally TACOS.
- Natural rank target and ad-order term are compared explicitly.
- Low-confidence items are marked when evidence comes only from comments or isolated cases.
- Cases are cited as examples, not universal rules.
