# Case Library

Evidence base: `case_library.jsonl` contains 15 extracted case observations. Cases are not rules. They are comparison anchors for diagnosis, counterexamples, and similarity checks.

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

## Common Mistakes

- Saying "this case proves the rule".
- Ignoring product stage, margin, and keyword type when comparing.
- Matching only ACOS while ignoring CPC, CVR, ad order share, and natural rank.
- Using weak comments as case facts.

## Quality Checklist

- Case ID and source ID are cited.
- Metrics are source-faithful and not normalized into invented thresholds.
- Problem statement is separated from recommendation.
- Similarity and difference from the user's case are both stated.
- Confidence is `case_data`; derived rules remain separate.
