# Source Index

Evidence base generated from 100 markdown posts split into 2002 sections. The extraction produced 2006 records: 15 cases, 144 executable rules, 113 diagnostic hypotheses, 81 diagnostic questions, 23 counterexamples, 217 weak comment signals, and 1413 irrelevant-noise records.

## Processed Data Files

| File | Purpose |
| --- | --- |
| `articles_index.jsonl` | Raw markdown article index with source IDs. |
| `article_sections.jsonl` | Metadata, author body, updates, comments, and unknown sections. |
| `extracted_records.jsonl` | Evidence-backed extracted records. |
| `noise_comments.jsonl` | Comment noise separated from usable records. |
| `normalized_records.jsonl` | Extracted records with normalized types and source refs. |
| `merged_rules.jsonl` | Rule and diagnostic-candidate library. |
| `case_library.jsonl` | Case observations kept separate from rules. |
| `conflict_candidates.jsonl` | Conditional conflict decision rules. |

## High-Signal Source Clusters

| Cluster | Typical Use | Example Sources |
| --- | --- | --- |
| Low ACOS but rank not moving | Diagnose ACOS/CPC/CVR/ad-share/rank mismatch. | A017, A082 |
| Ad dependency and natural traffic weakness | Diagnose high ad order share and low natural order share. | A017, A057, A080 |
| Keyword rank push and budget planning | Estimate click/order needs and target keyword structure. | A043, A054, A091 |
| Broad/phrase/exact structure | Separate discovery from rank push and profit exact. | A011, A023, A046 |
| Product/ASIN targeting | Compare competitor targeting, CPC, page placement, and conversion. | A001, A080, A098 |
| Seasonal product timing | Preheat, peak, and compressed optimization windows. | A002, A003, A005, A006 |
| Noise-heavy comment threads | Filter account links, social replies, thanks, off-topic talk. | A004, A020, A075 |

## Confidence Notes

- Author body with concrete metrics is stronger than comments.
- Extracted cases remain `case_data` and do not become rules.
- Comment-derived hypotheses and counterexamples remain capped at medium confidence.
- Many merged rules have broad limitations because the source corpus spans different categories and stages.
- Numeric thresholds should be preserved from source, not generalized across categories.

## Conflict Map

The conflict register currently contains 10 conditional conflicts:

- C001 low ACOS versus real ad effectiveness,
- C002 high ad order share versus ad reduction,
- C003 launch scaling versus ACOS control,
- C004 broad match discovery versus budget burn,
- C005 immediate negative versus insufficient sample,
- C006 high ACOS shutdown versus rank investment,
- C007 exact bid increase versus budget control,
- C008 ad-order term versus natural-rank movement,
- C009 medium/small word orders versus big-word target,
- C010 ad dependency versus activity traffic supplement.

## Common Mistakes

- Looking only at `merged_rules.jsonl` and ignoring `case_library.jsonl`.
- Treating `comment_signal` as rule evidence.
- Losing source IDs when summarizing.
- Using conflict candidates as absolute decisions instead of conditional frameworks.

## Quality Checklist

- Source IDs are retained in summaries.
- Cases, rules, conflicts, and noise stay separate.
- Comment confidence limits are preserved.
- Metrics are not invented when missing.
- Conflicts are resolved with product stage, margin, budget, sample size, ad goal, natural-rank target, inventory, and keyword type.
