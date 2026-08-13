# Keyword Library Building

## Contents

- [Core Principle](#core-principle)
- [Required Sub-Libraries](#required-sub-libraries)
- [Keyword Sources](#keyword-sources)
- [Building Workflow](#building-workflow)
- [Keyword Status Rules](#keyword-status-rules)

关键词分类回答的是“这个词属于什么类型”。关键词库建立回答的是“这些词从哪里来、怎么筛、怎么验证、怎么沉淀、怎么进入广告结构、怎么更新”。两者必须分开处理。

## Core Principle

Do not build a keyword library as a plain word list. Build it as a structured operating database with source, type, status, metrics, priority, risk flags, and campaign action.

关键词库必须支持以下判断：

- 哪些词只是种子词或待验证词。
- 哪些词已经通过广告搜索词报告验证出单。
- 哪些词是自然排名目标词，不能只按 ACOS 判断。
- 哪些词应进入精准、词组、广泛、自动或 ASIN 投放结构。
- 哪些词应进入否定候选、否定精准或否定词组。
- 哪些词来自竞品、季节窗口、文章案例或评论信号。

## Required Sub-Libraries

| Library | 用途 | 关键动作 |
| --- | --- | --- |
| Seed Keyword Library | 初始种子词库 | 从产品、功能、场景、同义词建立第一批词。 |
| Core Keyword Library | 核心词库 | 识别类目主需求和战略流量词。 |
| Long-tail Keyword Library | 长尾词库 | 承接新品期、低预算、明确意图流量。 |
| Competitor Keyword Library | 竞品词库 | 管理竞品品牌词、ASIN、标题词和竞品反查词。 |
| Search Term Harvesting Library | 广告搜索词挖掘库 | 从自动、广泛、词组和商品投放中沉淀搜索词。 |
| Ranking Target Keyword Library | 自然排名目标词库 | 单独标记要推动自然排名的词。 |
| Conversion Keyword Library | 已验证转化词库 | 沉淀有订单、CVR/ACOS 可接受的词。 |
| Negative Keyword Library | 否定词库 | 管理否定候选、否定精准和否定词组。 |
| Seasonal Keyword Library | 季节词库 | 管理旺季、节日、时间窗口和趋势词。 |
| Risk Keyword Library | 风险词库 | 管理儿童导向、合规、低相关、误导性或易烧钱词。 |

最重要的五个库是：自然排名目标词库、已验证转化词库、广告搜索词挖掘库、否定词库、竞品词库。它们直接决定广告结构和预算隔离。

## Keyword Sources

关键词来源必须多源交叉，不允许只靠一个来源。

### Product Source

- Product title
- Bullet points
- Description
- Core function
- Use case
- Material, size, color, compatibility
- Target audience
- Problem solved
- Substitute product
- Synonyms and US phrasing

### Competitor Source

- Competitor ASIN reverse lookup
- Competitor organic ranking keywords
- Competitor sponsored keywords
- Competitor title words
- Competitor bullet words
- Competitor A+ high-frequency words
- Competitor review high-frequency words

### Advertising Source

- Auto campaign search terms
- Manual broad search terms
- Manual phrase search terms
- Product targeting ASINs and related queries
- High-click no-order terms
- Low-click high-conversion terms
- High-spend no-order terms

### Amazon Front-End Source

- Search box suggestions
- Category node terms
- Competitor title terms
- Related searches
- Frequently bought together
- Customers also bought

### Third-Party Source

- ABA / Brand Analytics
- SQP
- Keepa
- Helium 10
- SellerSprite
- Keyword reverse lookup exports
- Competitor monitoring sheets

### Article And Comment Source

- Methodology words from ad articles
- Special terms mentioned in comments
- Failed words from cases
- Converting words from cases
- Ranking target words from cases

Comment-derived words are not high confidence by default. Use them as `comment_signal` or `diagnostic_hypothesis` until validated by backend data.

## Building Workflow

### Step 1: Build Seed Keywords

Start from product noun, category noun, primary function, target user, use case, and direct synonyms. Mark source as `manual_seed` or `product_listing`.

### Step 2: Expand Synonyms And Scenario Terms

Add attribute words, scenario words, audience words, replacement-product words, and common US expressions. Keep broad scenario terms isolated if relevance is uncertain.

### Step 3: Import Competitor Reverse-Lookup Terms

Import competitor ASIN reverse lookup, title words, ranking words, and ad words. Mark `related_asins`. Do not mix competitor terms into core campaigns until price, review, rating, and offer competitiveness are checked.

### Step 4: Import Advertising Search Terms

Import auto, broad, phrase, exact, and product-targeting search terms. Preserve clicks, spend, orders, CPC, CTR, CVR, ACOS, TACOS, ad rank, and organic rank when available.

### Step 5: Deduplicate And Normalize

Normalize whitespace, case, punctuation, plural variants where safe, and repeated source rows. Keep original keyword text for audit.

### Step 6: Score Relevance

Score whether the word directly matches the product, attribute, scenario, audience, and purchase intent. Low relevance does not become useful only because it has high traffic.

### Step 7: Score Traffic And Competition

Use ABA/SQP/search-frequency, reverse lookup frequency, CPC level, and competitor density. If data is missing, mark `unknown` rather than inventing a level.

### Step 8: Score Conversion Potential

Use orders, CVR, ACOS, CPC, product fit, and listing readiness. A word with orders is not automatically a natural-rank target.

### Step 9: Score Natural Ranking Priority

Rank priority requires explicit business intent and current natural-rank tracking. Check whether ad orders happen on the same term as the natural-rank target.

### Step 10: Assign Advertising Structure

Assign match type, campaign role, budget isolation, and review cadence. Separate discovery, profit, defense, competitor attack, and rank-push terms.

### Step 11: Build Negative Keyword Library

Classify low-relevance, high-click no-order, high-spend no-order, and obviously irrelevant terms into `negative_candidate`, `negative_exact`, or `negative_phrase`. Do not over-negative before sample size is sufficient.

### Step 12: Update On 7 / 14 / 30 Day Cadence

- 7 days: update new search terms, obvious irrelevant terms, high-spend leaks, and early converting terms.
- 14 days: promote validated converting terms, split ranking targets, adjust bids and budgets.
- 30 days: rebuild priority layers, compare ACOS/TACOS/natural rank, archive stale tests, and refresh competitor/seasonal libraries.

## Keyword Status Rules

| Status | Meaning | Typical action |
| --- | --- | --- |
| `unverified` | 未验证词 | Keep in test or seed pool. |
| `testing` | 测试中 | Use controlled budget and sample-size rule. |
| `validated_converting` | 已验证转化词 | Move to exact or dedicated campaign. |
| `ranking_target` | 自然排名目标词 | Track natural rank and TACOS; do not judge only by ACOS. |
| `scale_word` | 可放量词 | Increase budget or bid only with margin and inventory support. |
| `defensive_word` | 防守词 | Keep separated from growth spend. |
| `negative_candidate` | 否定候选词 | Review sample size and relevance before final negative. |
| `negative_exact` | 否定精准词 | Block exact query. |
| `negative_phrase` | 否定词组词 | Block phrase pattern with caution. |
| `seasonal_word` | 季节词 | Activate before demand window; pause or reduce after window. |
| `risk_word` | 风险词 | Isolate, review compliance/relevance, or negative. |

## Advertising Structure Rules

- Core big words: do not start with all exact high-bid rank pushing unless budget, conversion rate, margin, and listing readiness support it.
- Core long-tail words: prioritize exact and phrase testing in launch stage.
- High-relevance scenario words: use phrase or low-budget broad for discovery.
- Competitor words: isolate into ASIN or competitor keyword campaigns with separate budget.
- Validated converting terms: move to manual exact and adjust bids by ACOS, CVR, rank objective, and TACOS.
- High-click no-order terms: decide by sample size, relevance, and expected CVR; do not negative too early.
- Low-relevance terms: move to negative candidate.
- Obviously irrelevant terms: use negative exact or negative phrase.
- Natural ranking target words: mark separately and review ad rank, CTR, CVR, orders, natural rank, and TACOS.

## Separating Converting Terms From Ranking Target Terms

This distinction is mandatory.

| Signal | Converting term | Ranking target term |
| --- | --- | --- |
| Main proof | Orders, CVR, ACOS | Natural rank objective and strategic traffic |
| Primary metric | Profitability and conversion | Rank movement, total orders, TACOS |
| Campaign action | Exact/scale/profit capture | Dedicated rank-push structure |
| Common mistake | Assuming every order term is strategic | Judging rank target only by ACOS |

If ad orders are concentrated in mid/small terms while the natural target is a big word, do not claim the big word is being pushed effectively without rank evidence.

## Common Mistakes

- Treating keyword classification as the same thing as keyword library building.
- Building a one-time keyword list and never updating statuses.
- Mixing competitor, defense, discovery, and rank-push terms in one campaign.
- Treating low ACOS converting terms as proof of natural-rank progress.
- Negative-phrasing broad patterns before enough sample size.
- Treating comment-derived keyword suggestions as high confidence.

## Quality Checklist

- Each keyword has source, type, status, priority, risk flags, and metrics.
- Source types include product, competitor, ads, Amazon front-end, third-party, or article/comment evidence.
- Converting terms and ranking targets are separate fields/statuses.
- Negative decisions include sample-size and relevance reasoning.
- Competitor terms are budget-isolated.
- 7-day, 14-day, and 30-day update actions are defined.
