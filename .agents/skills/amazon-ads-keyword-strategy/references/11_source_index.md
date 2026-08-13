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
| `source_manifest.jsonl` | Source inventory with content hashes, evidence clusters, and readability limits; generated when source review is run. |
| `claim_review.jsonl` | Claim-level review records; generated only when an atomic claims input is supplied. |
| `source_validation_report.md` | Coverage and review-status report; `NOT_READY` is valid before claims are supplied. |
| `source_manifest_advanced_ads_review.jsonl` / `claim_review_advanced_ads.jsonl` | Separate review artifacts for the advanced diagnosis lecture; current coverage is `PARTIAL`. |
| `lecture_case_library_advanced_ads.jsonl` | Four retained lecture cases (`CASE-ADV-001` to `CASE-ADV-004`), kept separate from generated universal rules. |
| `source_case_records_advanced_ads_rewrite_v2.jsonl` | Six source-faithful cases from the second rewrite of the same lecture PDF; validated separately and not independent evidence. |
| `source_manifest_2026-08-13_new_bundle.jsonl` | Five-file user-source inventory for the 2026-08-13 batch; DOCX/XLSX are manually read but remain `readable:false` to reflect the script limitation. |
| `new_source_bundle_claim_review.jsonl` | 22 atomic claims covering pricing, promotion, launch, and image-only ad-report materials. |
| `new_source_bundle_case_records.jsonl` | 11 source-faithful cases from the batch; risk cases remain separate from executable rules. |
| `source_validation_report_2026-08-13_new_bundle.md` | Batch coverage report; `PARTIAL` because the automated manifest cannot parse the binary files and full project-corpus claims were not re-run in this batch. |
| `21_disputed_uncertain_claim_retention.md` | Central retention registry for all disputed, unresolved, unsupported, outdated, and context-dependent claims; these are retained knowledge, not silently discarded content. |
| `source_manifest_full_batch_2026-08-13.jsonl` | Unified 108-source manifest: 100 project articles plus 8 uploaded documents, including the original course PDF. |
| `full_batch_claim_review_2026-08-13.jsonl` | Unified 781-claim review: corpus extracted records, all uploaded-source claims, and the original PDF coverage record. |
| `full_batch_case_records_2026-08-13.jsonl` | Unified 36-case source-observation validation output. |
| `source_validation_report_full_batch_2026-08-13.md` | Unified coverage report; all 108 source IDs checked, but binary user documents keep overall status `PARTIAL`. |

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
| Pricing/reference-price integrity | Validate List Price/Typical Price and reject manufactured anchors. | `SRC-f564d5134e68`, `references/19_pricing_promotion_launch_integration.md` |
| Promotion/event eligibility | Treat stacking, fees, windows, and discount percentages as time/market dependent. | `SRC-2c0a32e82d29`, `references/19_pricing_promotion_launch_integration.md` |
| Launch policy risk | Preserve launch cases while blocking review/order/traffic manipulation. | `SRC-d9b87550b32a`, `references/19_pricing_promotion_launch_integration.md` |
| Image-report placement and rank claims | Use placement/purchased-product cases diagnostically; do not guarantee organic rank. | `SRC-3d7548bc16d9`, `references/20_image_ad_report_integration.md` |
| Unified full-batch audit | 100 project articles + 8 user files; 108 sources, 781 claims, 36 cases; machine readability is separate from manual review. | `data/processed/amazon_ads_skill/source_manifest_full_batch_2026-08-13.jsonl`, `data/processed/amazon_ads_skill/full_batch_claim_review_2026-08-13.jsonl`, `data/processed/amazon_ads_skill/source_validation_report_full_batch_2026-08-13.md`, `references/22_full_batch_review_2026-08-13.md` |

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
- Treating a source manifest as proof that every claim was reviewed.

## Quality Checklist

- Source IDs are retained in summaries.
- Cases, rules, conflicts, and noise stay separate.
- Comment confidence limits are preserved.
- Metrics are not invented when missing.
- Conflicts are resolved with product stage, margin, budget, sample size, ad goal, natural-rank target, inventory, and keyword type.
- Source review reports list unreadable and unreviewed sources explicitly.
- `confirmed_error` claims have direct opposing evidence and a verification test.
