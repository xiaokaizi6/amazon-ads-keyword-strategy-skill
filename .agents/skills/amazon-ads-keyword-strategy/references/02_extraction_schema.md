# Extraction Schema

## Contents

- [Record Shape](#record-shape)
- [Field Definitions](#field-definitions)
- [Allowed Values](#allowed-values)
- [Record-Type Requirements](#record-type-requirements)

This schema defines the JSONL contract for:

```text
data/processed/amazon_ads_skill/extracted_records.jsonl
```

Each line is one complete JSON object. The file must not contain arrays, Markdown, comments, or trailing commas.

## Record Shape

Every record must include all top-level fields below, even when the value is empty:

```json
{
  "record_id": "A001-R001",
  "source_id": "A001",
  "section_id": "A001-S001",
  "post_type": "case_post",
  "record_type": "case_observation",
  "section_role": "author_body",
  "is_relevant": true,
  "noise_reason": "none",
  "topic": "ranking",
  "product_stage": "stable",
  "ad_type": "Sponsored Products",
  "match_type": "exact",
  "condition": "",
  "action": "",
  "metric_threshold": "",
  "reasoning": "",
  "case_metrics": {},
  "evidence_quote": "",
  "comment_signal": "none",
  "confidence": "medium",
  "limitations": "",
  "contradiction_key": "",
  "tags": []
}
```

## Field Definitions

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `record_id` | string | yes | Stable id in `{source_id}-R###` format. Number records by extraction order within a source, not by section. |
| `source_id` | string | yes | Source article id, such as `A001`. Must match `articles_index.jsonl` and `article_sections.jsonl`. |
| `section_id` | string | yes | Section id that produced the record, such as `A001-S002`. |
| `post_type` | enum string | yes | Overall source post type. See allowed values below. |
| `record_type` | enum string | yes | Atomic extracted content type. See allowed values below. |
| `section_role` | string | yes | Source section role, normally `metadata`, `author_body`, `author_update`, `comment`, or `unknown`. |
| `is_relevant` | boolean | yes | `true` for usable ads/keyword/operation records, `false` for `irrelevant_noise`. |
| `noise_reason` | enum string | yes | `none` unless `record_type = "irrelevant_noise"`. |
| `topic` | string | yes | Main topic from taxonomy, such as `ranking`, `bidding_budget`, or `conversion_listing`. Empty string allowed when unknown. |
| `product_stage` | string | yes | Stage from taxonomy, such as `new_launch`, `stable`, or `seasonal_peak`. Use `unknown` when unclear. |
| `ad_type` | string | yes | Normalized ad/campaign type. Use `unknown` when unclear. |
| `match_type` | string | yes | Normalized targeting/match type. Use `unknown` when unclear. |
| `condition` | string | yes | Situation under which the record applies. Required for `executable_rule`; recommended for hypotheses. |
| `action` | string | yes | Concrete operation or next step. Required for `executable_rule`. |
| `metric_threshold` | string | yes | Numeric or qualitative trigger, such as `ACOS 10%`, `预算每天提前耗尽`, or `广告单占比 70%`. Empty when not given. |
| `reasoning` | string | yes | Source's causal logic or diagnostic rationale. Required for `executable_rule`. |
| `case_metrics` | object | yes | Source-faithful metrics for case observations. Empty object when not applicable. |
| `evidence_quote` | string | yes | Short direct quote from the source section. Must support the record. |
| `comment_signal` | string | yes | Comment signal taxonomy value. Use `none` for non-comment records. |
| `confidence` | enum string | yes | `high`, `medium`, or `low`. Comment viewpoints default to no higher than `medium`. |
| `limitations` | string | yes | Scope, caveats, missing data, or cases where the rule/hypothesis may not apply. Required for `executable_rule`. |
| `contradiction_key` | string | yes | Stable grouping key for counterexamples or contradictions. Empty when not applicable. |
| `tags` | array of strings | yes | Optional searchable labels, for example `["low_acos", "ad_dependency"]`. |

## Allowed Values

### `post_type`

```text
tutorial_article
question_post
case_post
discussion_post
mixed
unknown
```

### `record_type`

```text
executable_rule
case_observation
diagnostic_hypothesis
diagnostic_question
counterexample
comment_signal
irrelevant_noise
```

### `noise_reason`

```text
none
account_invitation
social_reply
thanks_only
off_topic
too_short
unreadable
```

### `confidence`

```text
high
medium
low
```

## `case_metrics`

`case_metrics` is an object with optional source-faithful string values. It may contain only these keys:

```json
{
  "category": "",
  "price": "",
  "cpc": "",
  "acos": "",
  "cvr": "",
  "ad_order_share": "",
  "daily_orders": "",
  "organic_rank": "",
  "ad_rank": "",
  "keyword_type": "",
  "competitor_context": "",
  "ranking_problem": ""
}
```

Rules:

- Include only keys supported by the evidence.
- Preserve wording such as `约`, `左右`, `以上`, `7 页开外`, and ranges like `20-40 单`.
- Do not calculate missing metrics unless the source explicitly provides the formula and values.
- Keep `case_metrics` empty for pure rules, hypotheses, diagnostic questions, and noise.

## Record-Type Requirements

### `case_observation`

Use for concrete source cases and measured observations.

Required content:

- `evidence_quote`
- at least one useful `case_metrics` key or a concrete observed result in `reasoning`
- `topic`
- `confidence` usually `medium` or `high` depending on data quality

Preferred extraction:

- Publisher body real product/ad/ranking data has priority over inferred rules.
- If a question post includes real case metrics, extract the metrics as `case_observation` and extract the author's uncertainty separately as `diagnostic_question`.

### `diagnostic_hypothesis`

Use for possible explanations that require checking.

Required content:

- `condition` or source problem being diagnosed
- `reasoning`
- `evidence_quote`
- `limitations` when the hypothesis depends on missing data

Comment-derived hypotheses:

- `section_role` should be `comment`.
- `comment_signal` should usually be `alternative_explanation` or `diagnostic_check`.
- `confidence` must be `medium` or `low` unless future validation adds hard evidence.

### `diagnostic_question`

Use for specific missing-data checks or questions.

Required content:

- `condition` describing the current uncertainty
- `action` phrased as a check/question to perform
- `evidence_quote`

Do not convert the questioner's doubt into an `executable_rule` unless the section also gives condition, action, reasoning, and limitations as a stated recommendation.

### `executable_rule`

Use only when a record is directly actionable.

All four fields must be non-empty:

- `condition`
- `action`
- `reasoning`
- `limitations`

Also required:

- `evidence_quote`
- `topic`
- `confidence`

Reject as `executable_rule` when:

- It is only a broad principle or slogan.
- It is a question from the publisher.
- It lacks a clear condition.
- It gives an action but no reasoning or no limitations.
- It is a comment with absolute wording but no supporting context; use `diagnostic_hypothesis` instead.

### `counterexample`

Use when a source narrows or contradicts a common operating rule.

Required content:

- `condition`
- `reasoning`
- `evidence_quote`
- `contradiction_key`
- `limitations`

Example contradiction keys:

```text
low_acos_not_enough_for_ranking
ad_rank_not_equal_organic_rank
budget_increase_not_always_solution
broad_match_can_outperform_exact
ad_orders_can_cannibalize_natural_orders
```

### `comment_signal`

Use for comment content that is relevant but too weak to become a rule, hypothesis, question, or counterexample.

Required content:

- `section_role = "comment"`
- `comment_signal` not `none`
- `evidence_quote`
- `confidence = "low"` or `"medium"`

### `irrelevant_noise`

Use for explicit noise sections/comments.

Required values:

- `record_type = "irrelevant_noise"`
- `is_relevant = false`
- `noise_reason` not `none`
- `comment_signal = "noise"` when from a comment
- `confidence = "low"`

Other fields should be empty strings or empty objects/arrays unless needed for traceability.

## Extraction Priority

1. Extract real publisher case data as `case_observation` before deriving rules.
2. Extract publisher questions as `diagnostic_question`, not certain rules.
3. Extract comment advice as `diagnostic_hypothesis` unless it satisfies every `executable_rule` requirement.
4. Extract comment operational rules only when condition, action, reasoning, and limitations are all explicit or tightly supported.
5. Extract counterexamples when the source provides evidence that limits a common rule.
6. Mark irrelevant comment content as `irrelevant_noise`.
7. Drop ordinary summaries: if the text only says what the section is about, it is not a record.

## Validation Rules

The extractor or validator should fail a record when:

- Any top-level field is missing.
- Any enum field contains a value outside this schema.
- `record_type = "executable_rule"` and any of `condition`, `action`, `reasoning`, or `limitations` is empty.
- `record_type = "irrelevant_noise"` and `is_relevant` is not `false`.
- `record_type != "irrelevant_noise"` and `noise_reason` is not `none`.
- `record_type = "case_observation"` and both `case_metrics` and `reasoning` are empty.
- A comment-derived record has `confidence = "high"` without explicit later validation.
- `evidence_quote` is empty for any non-noise record.
- A generic summary is emitted as a record.

## JSONL Examples

### Case Observation

```json
{"record_id":"A017-R001","source_id":"A017","section_id":"A017-S002","post_type":"case_post","record_type":"case_observation","section_role":"author_body","is_relevant":true,"noise_reason":"none","topic":"ranking","product_stage":"stable","ad_type":"Sponsored Products","match_type":"exact","condition":"","action":"","metric_threshold":"","reasoning":"广告数据看起来有效，但自然排名没有同步进入前三页，说明需要把广告表现和自然排名拆开诊断。","case_metrics":{"category":"鞋类","price":"$30","cpc":"约 $0.2","acos":"约 10%","cvr":"约 4%-5%","ad_order_share":"70%","daily_orders":"20-40 单","organic_rank":"7 页开外","ad_rank":"第一位","keyword_type":"精准中小词","ranking_problem":"广告数据好看但自然排名无法进入前三页"},"evidence_quote":"广告排名第一位...广告单占比70%...自然排名7页开外","comment_signal":"none","confidence":"medium","limitations":"仅为单个案例，缺少 CTR、整体转化率和类目均值对比。","contradiction_key":"","tags":["ad_dependency","organic_rank_stagnation"]}
```

### Comment Diagnostic Hypothesis

```json
{"record_id":"A017-R005","source_id":"A017","section_id":"A017-S006","post_type":"case_post","record_type":"diagnostic_hypothesis","section_role":"comment","is_relevant":true,"noise_reason":"none","topic":"data_diagnosis","product_stage":"unknown","ad_type":"Sponsored Products","match_type":"unknown","condition":"案例表现为低 ACOS 但自然排名推不动。","action":"检查高峰期广告位置、CTR，并比较广告转化率、产品整体转化率和类目平均转化率。","metric_threshold":"低 ACOS","reasoning":"低 ACOS 可能来自低 CPC，不一定代表转化率或链接质量足以推动自然排名。","case_metrics":{},"evidence_quote":"低 ACOS 可能只是 CPC 低，还要看高峰期位置、CTR 和转化率对比","comment_signal":"alternative_explanation","confidence":"medium","limitations":"评论区观点，缺少后台数据验证，不能写成绝对规则。","contradiction_key":"low_acos_not_enough_for_ranking","tags":["low_acos","ctr_check","conversion_check"]}
```

### Irrelevant Noise

```json
{"record_id":"A017-R003","source_id":"A017","section_id":"A017-S004","post_type":"case_post","record_type":"irrelevant_noise","section_role":"comment","is_relevant":false,"noise_reason":"account_invitation","topic":"","product_stage":"unknown","ad_type":"unknown","match_type":"unknown","condition":"","action":"","metric_threshold":"","reasoning":"","case_metrics":{},"evidence_quote":"互关交流","comment_signal":"noise","confidence":"low","limitations":"","contradiction_key":"","tags":[]}
```
