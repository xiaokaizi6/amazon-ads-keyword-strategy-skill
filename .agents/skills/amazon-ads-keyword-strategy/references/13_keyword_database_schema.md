# Keyword Database Schema

## Contents

- [Required Fields](#required-fields)
- [Allowed Types and Statuses](#allowed-keyword-types)
- [Metrics Object](#metrics-object)
- [Example Record](#example-record)
- [Update Semantics](#update-semantics)
- [Quality Checklist](#quality-checklist)

This file defines the `keyword_library.jsonl` record schema used by the Keyword Library Builder module.

Default outputs:

```text
data/processed/amazon_ads_skill/keyword_library.jsonl
data/processed/amazon_ads_skill/keyword_library.csv
data/processed/amazon_ads_skill/keyword_library_report.md
```

Optional operator export:

```text
outputs/keyword_library.xlsx
```

## Required Fields

| Field | Type | Required | Definition |
| --- | --- | --- | --- |
| `keyword_id` | string | yes | Stable ID such as `KW000001`. |
| `keyword` | string | yes | Original keyword text kept for human review. |
| `normalized_keyword` | string | yes | Lowercase, trimmed, punctuation-normalized keyword used for dedupe. |
| `keyword_type` | string | yes | Current keyword type. See allowed values below. |
| `source_type` | string | yes | Primary source type. Multiple sources can be summarized in `source_detail`. |
| `source_detail` | string | yes | Human-readable source note, such as file name, report name, ASIN, or method. |
| `related_asins` | array[string] | yes | Competitor or product ASINs related to the keyword. Empty array if none. |
| `product_stage` | string | yes | Product stage context, such as `new_launch`, `growth`, `stable`, `clearance`, or `seasonal`. |
| `search_intent` | string | yes | Intent such as `purchase`, `research`, `comparison`, `brand`, `defense`, or `unknown`. |
| `relevance_score` | number | yes | 0-100 score for product fit. Use 0 when irrelevant and avoid invented precision. |
| `traffic_level` | string | yes | `low`, `medium`, `high`, or `unknown`. |
| `competition_level` | string | yes | `low`, `medium`, `high`, or `unknown`. |
| `cpc_level` | string | yes | `low`, `medium`, `high`, or `unknown`. |
| `conversion_potential` | string | yes | `low`, `medium`, `high`, or `unknown`. |
| `ranking_priority` | string | yes | `low`, `medium`, `high`, or `none`. |
| `ad_priority` | string | yes | `low`, `medium`, `high`, or `none`. |
| `match_type_recommendation` | array[string] | yes | Recommended match types such as `exact`, `phrase`, `broad`, `product_targeting`. |
| `campaign_recommendation` | string | yes | Recommended campaign role or structure. |
| `negative_match_recommendation` | string | yes | Empty string, `negative_exact`, `negative_phrase`, or `negative_candidate`. |
| `risk_flags` | array[string] | yes | Risk labels such as `low_relevance`, `children_directed`, `competitor_brand`, `high_cpc`. |
| `metrics` | object | yes | Advertising, ranking, and performance metrics. |
| `status` | string | yes | Current workflow status. See allowed values below. |
| `last_updated` | string | yes | ISO date, such as `2026-06-01`. |

## Allowed Keyword Types

Use these values in `keyword_type`:

```text
seed_keyword
core_keyword
core_long_tail
long_tail
competitor_keyword
brand_keyword
defensive_keyword
attribute_keyword
scenario_keyword
seasonal_keyword
ranking_target_keyword
converting_keyword
negative_candidate
negative_exact
negative_phrase
risk_keyword
```

## Allowed Status Values

Use these values in `status`:

```text
unverified
testing
validated_converting
ranking_target
scale_word
defensive_word
negative_candidate
negative_exact
negative_phrase
seasonal_word
risk_word
```

## Recommended Source Types

Use these values when possible:

```text
manual_seed
product_title
product_bullets
product_description
competitor_reverse_lookup
competitor_organic_rank
competitor_ad_keyword
competitor_title
competitor_bullets
competitor_a_plus
competitor_review
advertising_search_term_report
auto_campaign_search_term
manual_broad_search_term
manual_phrase_search_term
product_targeting_report
amazon_search_suggestion
category_node
related_search
frequently_bought_together
customers_also_bought
aba
sqp
brand_analytics
keepa
seller_sprite
helium10
article_rule
case_observation
comment_signal
unknown
```

## Metrics Object

`metrics` must contain these keys. Use `null` when data is missing.

```json
{
  "impressions": null,
  "clicks": null,
  "ctr": null,
  "cpc": null,
  "orders": null,
  "cvr": null,
  "acos": null,
  "tacos": null,
  "spend": null,
  "sales": null,
  "organic_rank": null,
  "ad_rank": null
}
```

Percent values should be stored as decimals when possible: `0.36` means 36%. If the source file provides `36%`, the script may parse it to `0.36`.

## Example Record

```json
{
  "keyword_id": "KW000001",
  "keyword": "rolled ice cream maker",
  "normalized_keyword": "rolled ice cream maker",
  "keyword_type": "core_long_tail",
  "source_type": "competitor_reverse_lookup",
  "source_detail": "ASIN reverse lookup / search term report / manual seed / article rule",
  "related_asins": [],
  "product_stage": "new_launch",
  "search_intent": "purchase",
  "relevance_score": 80,
  "traffic_level": "medium",
  "competition_level": "medium",
  "cpc_level": "medium",
  "conversion_potential": "unknown",
  "ranking_priority": "high",
  "ad_priority": "high",
  "match_type_recommendation": ["exact", "phrase"],
  "campaign_recommendation": "Separate exact or phrase campaign if this is a natural-rank target; otherwise test with controlled budget.",
  "negative_match_recommendation": "",
  "risk_flags": [],
  "metrics": {
    "impressions": null,
    "clicks": null,
    "ctr": null,
    "cpc": null,
    "orders": null,
    "cvr": null,
    "acos": null,
    "tacos": null,
    "spend": null,
    "sales": null,
    "organic_rank": null,
    "ad_rank": null
  },
  "status": "unverified",
  "last_updated": "2026-06-01"
}
```

## CSV Export Rules

`keyword_library.csv` should include the same top-level fields. Array and object fields should be serialized as compact JSON strings:

- `related_asins`
- `match_type_recommendation`
- `risk_flags`
- `metrics`

## Update Semantics

- Same `normalized_keyword` means the same keyword row unless the marketplace or product scope later requires splitting.
- New sources should append to `source_detail` or preserve a source list before overwriting.
- Stronger evidence can upgrade `status`, but weak evidence should not downgrade a validated converting term without a review window.
- Negative status must include sample-size or relevance reasoning in `source_detail`, `risk_flags`, or the update report.
- Comment-sourced keywords should remain low or medium confidence until confirmed by ad, ranking, or third-party data.

## Common Mistakes

- Missing `normalized_keyword`, which breaks dedupe.
- Treating `keyword_type` and `status` as the same field.
- Using `converting_keyword` without orders or conversion evidence.
- Marking `ranking_target_keyword` without tracking natural rank.
- Overwriting a validated keyword with a weak comment signal.

## Quality Checklist

- Every record has all required fields.
- Every metrics object has all required metric keys.
- `keyword_type` and `status` use allowed values.
- Missing metrics are `null`, not fabricated zeros.
- CSV and JSONL exports contain the same records.
- Report summarizes source, type, status, and risk distribution.
