# Case Library

## Contents

- [High-Value Cases](#high-value-cases)
- [Case Similarity Signals](#case-similarity-signals)
- [How To Use Cases](#how-to-use-cases)

Evidence base: `case_library.jsonl` contains 15 extracted case observations. New user-source cases first remain in `source_case_records.jsonl` or an equivalently structured, batch-specific case file with source location, observation, claimed explanation, and cross-validation boundary; only durable diagnostic anchors are additionally summarized here. Cases are not rules. They are comparison anchors for diagnosis, counterexamples, and similarity checks.

Cases and claims with `disputed`, `unresolved`, `unsupported`, `outdated`, or `context_dependent` status remain valid retained knowledge even when they are not promoted into `case_library.jsonl` or `merged_rules.jsonl`; see `references/21_disputed_uncertain_claim_retention.md`.

## High-Value Cases

### CASE001: 低 ACOS + 高广告单占比 + 自然排名无法提升

- Source: A017.
- Facts: shoe product, price $30, CPC about $0.2, ACOS about 10%, ad CVR about 4%-5%, ad order share 70%, daily orders 20-40, ad rank first, natural rank outside page 7.
- Problem: ad data looked efficient but natural ranking did not enter the first three pages.
- Use as: diagnostic anchor for "low ACOS does not prove ranking success".
- Do not use as: universal proof that low ACOS is bad.

### CASE002: 新产品广告依赖 + 关键词进入前 5 页但难进第一页

- Source: A017.
- Facts: daily orders 40-70, ad order share above 50%, competitor context includes Amazon retail, keyword ranking reached first five pages but not page one.
- Problem: ad dependency and ranking bottleneck.
- Use as: comparison for ad share, product stage, and target-rank gap.

### CASE003: 低 CPC + 花费基本花满 + 中小词出单不多

- Source: A017 author update.
- Facts: CPC as low as $0.16, spend basically full, keywords are medium/small search volume.
- Use as: reminder to distinguish low CPC and small keyword capacity from high strategic performance.

### CASE009: 广告出单集中但自然排名长期上不去

- Source: A057.
- Facts: three products promoted for about six months, daily ad budget about $100, many keywords stayed page 2-3, ad order share too high, link lost money.
- Use as: rank-push failure comparison.
- Diagnostic points: target term choice, conversion, budget allocation, ad-order term versus target rank term.

### CASE010: 中小词/低预算目标与大词自然排名目标冲突

- Source: A080.
- Facts: low-price kitchen/tableware product, CPC 1.2-1.5 or higher, some small terms held top 10/top 5 natural rank, daily budget around $110, natural order share about 50%.
- Use as: anchor for中小词出单 vs大词自然排名目标.

### CASE011: 广告结构中增加大卖定向后效果可用

- Source: A080.
- Facts: three exact campaigns retained, added large-seller targeting, ACOS around 40%-50%, conversion acceptable.
- Use as: product-targeting support case, with margin caution.

### CASE012: 出单词自然排名不显示或不提升

- Source: A082.
- Facts: 220+ exact keywords before launch, auto plus several exact groups, CPC strategy around 50% of suggested bid, some ordered terms did not show natural rank.
- Use as: ad-order term and organic-rank tracking mismatch case.

### CASE014: 低售价产品精准 CVR 高但自动 CVR 低

- Source: A093.
- Facts: price 7.99 USD, exact ad conversion around 20%, auto ad conversion lower.
- Use as: match-type and traffic-quality comparison.

### CASE015: 商品广告 CPC 高且权重积累不如关键词投放

- Source: A098.
- Facts: competitor ASIN CPC 2.6, product ads appear on product pages, source claims keyword-weight accumulation is weaker than keyword targeting.
- Use as: product targeting limitation, not as absolute rule.

## Case Similarity Signals

- Low ACOS but no natural-rank movement: compare with CASE001 and C001.
- High ad order share: compare with CASE001, CASE002, CASE009, and C002.
- Medium/small terms producing orders while big term remains weak: compare with CASE003, CASE010, and C009.
- High CPC or limited budget: compare with CASE010, CASE011, CASE015.
- Exact versus auto performance gap: compare with CASE014.

## How To Use Cases

1. Match the user's product stage, category, price, CPC, CVR, ad order share, and rank issue.
2. Use the case to ask better diagnostic questions.
3. Do not convert a single case into a universal recommendation.
4. If the case is supported by comments only, mark it `low confidence`.
5. When a case conflicts with a rule, use conflict register conditions.
6. When a retained case is materially relevant, proactively state its case confidence, matching facts, and material mismatches; distinguish reported observation from unverified causal explanation.

## Common Mistakes

- Saying "this case proves the rule".
- Ignoring product stage, margin, and keyword type when comparing.
- Matching only ACOS while ignoring CPC, CVR, ad order share, and natural rank.
- Using weak comments as case facts.
- Dropping a case because its explanation conflicts with the current skill instead of preserving the observation and marking the explanation boundary.

## Supplemental Lecture Cases: 进阶广告诊断讲义

The structured records for these cases are in `data/processed/amazon_ads_skill/lecture_case_library_advanced_ads.jsonl`; the source-level review is in `references/17_advanced_ads_diagnosis_integration.md`.

- `CASE-ADV-001` / `CASE-ADV-002`: seat-cushion A/B cases where ACOS/TACOS exceed the lecture's 30% teaching margin. Use to prioritize funnel diagnosis, never as universal ACOS cutoffs.
- `CASE-ADV-003`: seat-cushion C/D cases with weak conversion. Use to check listing, price, reviews, variants, competitiveness, and traffic match alongside ads.
- `CASE-ADV-004`: 20-click screening, 100-click higher-confidence example, and placement bid examples. Use only as conditional test parameters.

When a user asks about these patterns, display the `讲义案例提示` marker, source status, matching/mismatching metrics, missing data, and a reversible test window.

## Supplemental Lecture Cases: 文字整理版（1）

The second rewrite of the same lecture PDF is not independent evidence. Its six source-faithful cases are validated in `data/processed/amazon_ads_skill/source_case_records_advanced_ads_rewrite_v2.jsonl` and summarized in `references/18_advanced_ads_diagnosis_rewrite_v2_integration.md`.

- `SRC-3328e6e7662e-CASE-001`: 2 clicks / 1 order for `office chair cushion`; small-sample signal only.
- `SRC-3328e6e7662e-CASE-002`: four diagnostic patterns covering high spend/loss, low inventory, low data, and mismatched traffic.
- `SRC-3328e6e7662e-CASE-003`: outdoor-cushion keyword research exercise with explicit attributes; do not infer product facts.
- `SRC-3328e6e7662e-CASE-004`: placement and budget percentage examples; unsupported as defaults.
- `SRC-3328e6e7662e-CASE-005`: test, seasonal, and clearance timing examples; conditional stage parameters.
- `SRC-3328e6e7662e-CASE-006`: inventory-month and 2× gross-margin reference examples; not platform thresholds.

Use the same `讲义案例提示` protocol and always distinguish the source observation from the author's explanation.

## Supplemental Source Cases: 定价、促销与新品资料

These cases are preserved in `data/processed/amazon_ads_skill/new_source_bundle_case_records.jsonl` and are not executable rules. The claim statuses are in `new_source_bundle_claim_review.jsonl`.

- `SRC-f564d5134e68-CASE-001/002`: inflated reference-price and fixed-order-count strike-through tactics; `low confidence`, policy-risk/unsupported. Never recommend related-account orders or fixed “10 orders/one week” thresholds.
- `SRC-2c0a32e82d29-CASE-001/002`: promotion stacking and event-price reverse calculations; use only to explain assumptions, then verify current eligibility and checkout math.
- `SRC-d9b87550b32a-CASE-001`: fixed launch budgets/bids/ACOS50%; `medium` case completeness but not a universal threshold.
- `SRC-d9b87550b32a-CASE-002`: review compensation, fake orders, related accounts, and artificial behavior; `low confidence` as a performance case and `confirmed_error` as a policy route. Preserve only as risk evidence.
- `SRC-d9b87550b32a-CASE-003`: SD custom bid formula; unsupported hypothesis.

If a user asks about strike-through price formation, review targets, fake orders, or launch ACOS thresholds, display `讲义案例提示` and state the source status, policy boundary, compliant alternative, and reversible test window.

## Supplemental Source Cases: 图片版广告报告

The image-only report cases are preserved in the same batch file and summarized in `references/20_image_ad_report_integration.md`:

- `SRC-3d7548bc16d9-CASE-001`: position-level CTR/CVR/order differences; use for placement diagnosis, not fixed bid percentages.
- `SRC-3d7548bc16d9-CASE-002`: advertised ASIN `QW` to purchased ASIN `RL` (~9 units); use as a cross-sell hypothesis only.
- `SRC-3d7548bc16d9-CASE-003`: three campaigns' online-time values; no evidence for a universal 70% threshold.
- `SRC-3d7548bc16d9-CASE-004`: TOS +900% and 1-2-click stop rule; low-confidence high-risk counterexample, never a default.

When the question involves exact-match ranking, TOS 100%-200%/900%, placement scaling, or low-ACOS budget increases, display `讲义案例提示`, compare against CASE001/CASE009/CASE012/CASE015, and separate reported observations from unverified causal explanations.

## Quality Checklist

- Case ID and source ID are cited.
- Metrics are source-faithful and not normalized into invented thresholds.
- Problem statement is separated from recommendation.
- Similarity and difference from the user's case are both stated.
- Confidence is `case_data`; derived rules remain separate.
