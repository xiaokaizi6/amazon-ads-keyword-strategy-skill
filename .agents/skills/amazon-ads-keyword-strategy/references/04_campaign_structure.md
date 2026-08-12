# Campaign Structure

Evidence base: normalized rules contain the most support for bidding/budget, ranking, keyword research, and campaign structure. Case evidence is strongest for ranking stalls, ad dependency, CPC pressure, and exact/auto/product-targeting interactions. Campaign structures below are decision frameworks, not universal defaults.

## Stage-Based Structures

### 新品期广告结构

- Purpose: collect exposure, clicks, search-term data, and early orders without losing budget control.
- Suggested structure: auto campaign for discovery, phrase/broad for controlled exploration, exact for a small set of known target terms, and ASIN/category tests only when competitor fit is clear.
- Budget rule: separate test budget from rank-push budget; define stop-loss by clicks, spend, and relevance.
- Confidence: medium. Several rules and conflicts support this, but product margin and listing readiness change the answer.

### 爬坡期广告结构

- Purpose: convert discovered terms into repeatable traffic and test natural-rank movement.
- Suggested structure: isolate proven search terms into exact; keep broad/phrase for discovery with lower budget; track target natural rank separately.
- Budget rule: increase only where CPC, CVR, order count, and natural-rank target align.
- Key risk:出单词 and排名目标词 may be different.

### 稳定期广告结构

- Purpose: protect profitable flow, reduce waste, and prevent ad dependency from hiding weak natural traffic.
- Suggested structure: exact for stable profitable terms, brand defense, selected ASIN/product targeting, and controlled discovery campaigns.
- Budget rule: evaluate ACOS together with TACOS, natural order share, ad order share, and ranking.
- Key risk: cutting all ads because ACOS is high or keeping all ads because ACOS is low.

### 旺季广告结构

- Purpose: preempt compressed demand windows and rising CPC.
- Suggested structure: seasonal preheat campaigns before peak, broader discovery earlier, exact and product targeting during peak, tighter budget controls as CPC rises.
- Budget rule: use trend timing and inventory pressure. Seasonal posts support starting before peak, but exact timing is category-dependent.
- Confidence: medium; many seasonal recommendations are tutorial-style and need category validation.

### 淡季广告结构

- Purpose: preserve rank and data without overpaying for low demand.
- Suggested structure: retain best exact/defense terms, reduce broad exploration, test only if CPC drops enough to justify data collection.
- Budget rule: compare spend against realistic demand and inventory plan.
- Confidence: low to medium; direct case support is weaker than for launch/ranking cases.

### 清库存广告结构

- Purpose: sell through inventory while controlling loss.
- Suggested structure: exact terms with proven CVR, product targeting against weaker competitors, deal/activity support if margin allows.
- Budget rule: inventory pressure can justify higher ACOS only when cash recovery is the goal.
- Confidence: low; keep decisions explicitly tied to inventory and margin.

## Campaign Type Notes

### 自动广告

- Best use: discovery, listing relevance check, ASIN/category signal, early data.
- Do not use: as the only growth structure after search-term data is available.
- Action: separate bids or campaigns when testing close/substitute/loose/complement style traffic; move proven search terms out.
- Caveat: comments suggest CPC tiers can change auto traffic composition; keep comment-derived claims at medium or low confidence.

Official boundary: Amazon currently describes automatic targeting as close match, loose match, substitutes, and complements; manual keyword targeting as broad, phrase, and exact. These definitions support separating discovery and controlled targeting, but do not prove that one match type always has the best CVR or ACOS. See `references/16_cpc_playbook_integration.md` (CPC-CLM-003 to CPC-CLM-006).

### 手动精准

- Best use: known converting terms, rank target terms, controlled budget, and repeatable measurement.
- Do not assume: exact always converts better than broad/phrase in every case.
- Action: split profit exact terms from rank-push exact terms; measure by different goals.

### 手动词组

- Best use: controlled expansion around a root or attribute.
- Action: harvest converting variants; negative irrelevant patterns.
- Caveat: phrase can still drift if the root is broad.

### 手动广泛

- Best use:拓词, early exploration, discovering modifiers.
- Required controls: isolated budget, frequent search-term review, negative rules, sample-size thresholds.
- Conflict: broad match can discover valuable terms, but can also burn budget. See conflict C004.

### ASIN 投放

- Best use: competitor page interception, weaker competitor targeting, own-ASIN defense, product discovery.
- Required checks: price, review count, rating, image, offer, coupon, competitor strength, CPC.
- Caveat: product targeting can produce orders without helping keyword natural rank directly.

### 品牌防守

- Best use: protect own brand and product page traffic.
- Measurement: do not mix brand defense with new customer acquisition.
- Action: keep separate campaigns and budgets.

### 竞品进攻

- Best use: when your offer has a concrete advantage over the competitor.
- Required checks: competitor relevance, price/review/rating edge, page position, CPC ceiling.
- Caveat: aggressive competitor targeting without conversion advantage is budget risk.

### 广告目标隔离

- Keep discovery, profit capture, defense, conquest, and rank-test objectives in separate campaigns or ad groups when the budget, bidding logic, or success metric differs.
- Amazon's official guidance also recommends organizing campaigns around objectives and grouping related products; this supports the structure principle but does not prescribe one universal naming hierarchy.
- Product targeting and category targeting should be measured separately when the decision depends on page placement, relevance, or competitor strength.

## Evidence Anchors

- CASE001/CASE002: ad rank and ad orders did not guarantee natural rank movement.
- CASE011/CASE015: product targeting can work, but CPC and placement may limit strategic value.
- Conflicts C003, C004, C007, and C008 condition campaign choices by stage, budget, sample size, keyword type, and natural-rank target.

## Common Mistakes

- Mixing discovery, profit capture, defense, and rank-push goals in one campaign.
- Evaluating every campaign by ACOS alone.
- Treating auto/broad data as clean ranking evidence.
- Running ASIN targeting without checking whether the competitor is beatable.
- Keeping comment-suggested structures as high-confidence rules.

## Quality Checklist

- Each campaign has one primary goal.
- Match type, ad type, and budget are separated by goal.
- Search-term harvesting and negative rules are defined.
- CTR, CVR, CPC, ACOS, TACOS, orders, ad order share, and natural rank are reviewed together.
- Product stage and margin are stated.
- Case evidence is used as comparison, not proof.
