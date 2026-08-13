# Taxonomy

## Contents

- [Extraction Unit](#extraction-unit)
- [Record Types](#record-types)
- [Topic Taxonomy](#topic-taxonomy)
- [Confidence](#confidence)

This taxonomy defines what can become an extracted strategy record from Amazon ads and keyword strategy source posts.

The extractor must not reduce source material to generic "rules" only. It must preserve case data, diagnostic uncertainty, questions, actionable rules, counterexamples, comment signals, and irrelevant noise so later phases can separate case libraries, rule candidates, and low-value comments without losing context.

## Extraction Unit

A record is an evidence-backed atomic observation, hypothesis, question, rule, counterexample, signal, or noise item from one `section_id`.

Do not create a record for a plain summary, restatement, headline, or topic label. A valid record must be anchored to a specific source quote and must carry enough context for later review.

One section may produce zero, one, or many records:

- Long author case posts may produce multiple `case_observation` records when they describe distinct products, stages, keywords, campaigns, or ranking problems.
- Comment sections may produce useful `diagnostic_hypothesis`, `executable_rule`, `comment_signal`, or `irrelevant_noise` records.
- Metadata-only sections usually produce no records unless the metadata itself is needed for noise classification or post typing.

## Post Types

Use one value for the whole source post and copy it onto every extracted record from that source.

| Value | Meaning | Typical cues |
| --- | --- | --- |
| `tutorial_article` | Author explains a strategy, method, framework, or operational playbook. | Step-by-step guidance, principles, "how to", "打法", no personal unresolved problem. |
| `question_post` | Author asks for help and does not provide enough operational data to be a case. | Many question marks, "请教", "怎么办", limited metrics. |
| `case_post` | Author provides real product, ads, ranking, sales, or metric details. | Price, CPC, ACOS, CVR, order volume, ranks, keyword context, campaign settings. |
| `discussion_post` | Source is mainly debate, opinion exchange, or conceptual discussion. | Multiple viewpoints, no single case owner, broad claims. |
| `mixed` | Combines tutorial, question, and/or case content in material ways. | Case plus advice, article plus comments with substantial new advice. |
| `unknown` | Insufficient evidence to classify confidently. | Truncated, unreadable, or ambiguous source. |

## Section Roles

Use the `section_role` already assigned during section splitting when available:

- `metadata`: source title, link, publisher, time, tags, counts.
- `author_body`: main post body from the publisher.
- `author_update`: later clarification or follow-up from the publisher.
- `comment`: individual public comment or reply.
- `unknown`: section could not be classified.

Extraction priority depends on role:

1. Publisher body and updates with real data are preferred as `case_observation`.
2. Comment advice is preferred as `diagnostic_hypothesis` or `executable_rule`, not as confirmed fact.
3. Irrelevant comments must be retained as `irrelevant_noise` when they are visible in the source and identifiable.

## Record Types

| Value | Use when | Do not use when |
| --- | --- | --- |
| `case_observation` | A source reports concrete case data, metrics, product stage, campaign setup, ranking movement, failure mode, or observed result. | The text is only a recommendation without observed data. |
| `diagnostic_hypothesis` | A commenter or author proposes a possible explanation that needs verification. | The source gives a directly executable step with condition, action, reasoning, and limitations. |
| `diagnostic_question` | The source raises a specific check or asks for missing facts needed to diagnose the case. | The question is rhetorical or too broad to guide diagnosis. |
| `executable_rule` | The source gives an actionable operating rule with condition, action, reasoning, and limitations. | The text is a question, case-only observation, slogan, or unsupported absolute claim. |
| `counterexample` | The source provides a case or claim that contradicts or limits a common rule. | It merely disagrees without evidence or comparable context. |
| `comment_signal` | A comment adds weak but relevant market, platform, operational, or sentiment signal that is not enough for a rule or hypothesis. | The comment is actionable enough to be a hypothesis/rule or irrelevant enough to be noise. |
| `irrelevant_noise` | The section is visible but irrelevant, unreadable, account promotion, thanks-only, social chatter, or off-topic. | It contains useful diagnostic or operational content. |

## Noise Reasons

Use `noise_reason = "none"` for all records except `irrelevant_noise`.

| Value | Meaning |
| --- | --- |
| `none` | Relevant record or non-noise extraction. |
| `account_invitation` | Account exchange, invite code, contact request, group invite, private-message request, or lead capture. |
| `social_reply` | Lightweight social interaction such as jokes, agreement, compliments, or chat without usable ads/keyword content. |
| `thanks_only` | Only thanks, bookmarking, "学习了", "收藏", or similar. |
| `off_topic` | Content is unrelated to Amazon ads, keyword ranking, product operations, or the source problem. |
| `too_short` | Too short to classify or extract meaning. |
| `unreadable` | Garbled, missing, broken formatting, or image-only content without extractable text. |

## Topic Taxonomy

Use the most specific topic supported by the evidence. Leave blank only when the content is relevant but topic cannot be determined.

| Topic | Includes |
| --- | --- |
| `ranking` | Keyword natural rank, ad rank, homepage/top-of-search position, rank push failure. |
| `keyword_research` | Keyword selection, root words, long-tail words, brand words, search term mining. |
| `campaign_structure` | Campaign/ad group architecture, separating auto/manual/exact/phrase/broad/product targeting. |
| `bidding_budget` | CPC, bid, budget, placement adjustment, budget exhaustion, dayparting. |
| `acos_profit` | ACOS, TACOS, ROI, profitability, ad spend pressure. |
| `conversion_listing` | CVR, CTR, click quality, listing quality, review, price, main image. |
| `traffic_allocation` | Natural vs ad orders, ad order share, traffic source mix, cannibalization. |
| `product_targeting` | ASIN targeting, category targeting, competitor page placement. |
| `launch` | New product launch, cold start, first traffic, early review/data accumulation. |
| `seasonality` | Seasonal window, pre-season testing, peak demand timing, inventory timing. |
| `defense_offense` | Defensive ads, competitor attack, brand protection, traffic moat. |
| `compliance_risk` | Brushing, manipulation, policy risk, brand keyword legality. |
| `data_diagnosis` | Checks requiring reports, CTR/CVR comparison, search term evidence, attribution limits. |

## Product Stage

| Value | Meaning |
| --- | --- |
| `new_launch` | Newly listed, cold start, first 0-60 days, no stable keyword/ranking base. |
| `growth` | Sales and rank are improving but not yet stable. |
| `stable` | Product has regular orders/ranking and is being optimized. |
| `declining` | Rank, traffic, conversion, or sales are falling. |
| `seasonal_preheat` | Before seasonal demand window. |
| `seasonal_peak` | In seasonal peak demand. |
| `seasonal_clearance` | Late season, inventory clearance or demand decline. |
| `unknown` | Stage cannot be inferred. |

## Ad Type

Prefer normalized English values:

- `Sponsored Products`
- `Sponsored Brands`
- `Sponsored Brands Video`
- `Sponsored Display`
- `Product Targeting`
- `Category Targeting`
- `Auto Campaign`
- `Manual Campaign`
- `unknown`

If the source only says "广告" and no type can be inferred, use `unknown`.

## Match Type

Use one value when applicable:

- `auto`
- `broad`
- `phrase`
- `exact`
- `asin`
- `category`
- `brand`
- `mixed`
- `unknown`

## Comment Signal Taxonomy

`comment_signal` captures whether a comment is usable and how strong it is.

| Value | Meaning |
| --- | --- |
| `none` | No comment signal or record is not from a comment. |
| `actionable_advice` | Comment suggests a specific next step. |
| `diagnostic_check` | Comment asks for data or proposes a test/check. |
| `alternative_explanation` | Comment gives a possible cause different from the author's assumption. |
| `contradiction` | Comment challenges a claim or provides a counterexample. |
| `weak_agreement` | Comment agrees but adds little evidence. |
| `noise` | Comment is retained only as irrelevant noise. |

Comment-derived viewpoints default to `confidence = "medium"` or lower unless the comment supplies concrete data, clear reasoning, and scoped limitations.

## Confidence

| Value | Meaning |
| --- | --- |
| `high` | Strong source evidence, concrete metrics, clear causal or operational scope, and no obvious contradiction. Rare for comments. |
| `medium` | Plausible and useful but missing some evidence, metric support, or verification. Default for comments with substance. |
| `low` | Weak, speculative, broad, or incomplete. Use for vague comments and under-specified hypotheses. |

## Case Metrics

Extract metric values as source-faithful strings. Do not normalize away uncertainty such as "约", "左右", "50% 以上", or "7 页开外".

Allowed `case_metrics` keys:

- `category`
- `price`
- `cpc`
- `acos`
- `cvr`
- `ad_order_share`
- `daily_orders`
- `organic_rank`
- `ad_rank`
- `keyword_type`
- `competitor_context`
- `ranking_problem`

Only include a key when the source provides or strongly implies it. Do not invent missing numbers.

## Counterexamples And Contradictions

Use `counterexample` when the source narrows or challenges a common assumption, for example:

- Low ACOS does not automatically mean the keyword can push natural ranking.
- High ad rank does not guarantee natural rank improvement.
- More budget does not always improve ranking if conversion or click quality is weak.
- Product targeting can work for traffic interception but may fail when competitors have stronger price/review advantages.

Set `contradiction_key` to a stable short phrase for later grouping, such as:

- `low_acos_not_enough_for_ranking`
- `ad_rank_not_equal_organic_rank`
- `budget_increase_not_always_solution`
- `broad_match_can_outperform_exact`
- `ad_orders_can_cannibalize_natural_orders`

## Relevance Rules

Relevant records must connect to Amazon ads, keyword strategy, ranking, traffic, conversion, product lifecycle, or marketplace competition.

Irrelevant records include:

- Account invitations or private-contact requests.
- Pure thanks/bookmarking/social chatter.
- Generic business, tax, sourcing, or platform talk with no ads/keyword/operation insight.
- Unreadable or image-only sections with no extractable text.

## Decision Rules

1. Extract publisher body real data first as `case_observation`.
2. Keep the questioner's doubts as `diagnostic_question` unless the source provides evidence for a rule.
3. Extract comment advice as `diagnostic_hypothesis` or `executable_rule` depending on whether it is conditional and actionable.
4. Never upgrade a comment viewpoint above `medium` confidence by default.
5. Mark irrelevant comments as `irrelevant_noise` instead of silently dropping them when they are explicit comment items.
6. Do not create records from ordinary summaries.
7. `executable_rule` must have non-empty `condition`, `action`, `reasoning`, and `limitations`.
