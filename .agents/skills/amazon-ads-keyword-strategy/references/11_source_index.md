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
| `source_manifest_advanced_ads_pdf_live_2026-08-13.jsonl` | Live manifest for the original 143-page image-only course PDF; SHA-256 and full-page manual review metadata retained. |
| `advanced_ads_pdf_live_claims_2026-08-13.jsonl` / `claim_review_advanced_ads_pdf_live_2026-08-13.jsonl` | 18 page-located atomic claims from the live PDF review, with current-platform cross-checks and uncertainty states. |
| `source_case_records_advanced_ads_pdf_live_2026-08-13.jsonl` | Four source-faithful PDF cases; same-family duplicates are retained for traceability but not counted as independent evidence. |
| `source_validation_report_advanced_ads_pdf_live_2026-08-13.md` | Full 143-page render/review coverage report; `PARTIAL` because the PDF has no usable machine text layer. |
| `advanced_ads_pdf_ocr_full_2026-08-18.jsonl` | 143-page, 10,245-line machine OCR retrieval layer for the original course PDF. Every row retains its original PDF page; 716 low-confidence lines remain uncorrected and require page-level verification. Portable copy is in `assets/knowledge/`. |
| `advanced_ads_pdf_ocr_derivative_manifest_2026-08-18.json` | Hashes, page/line counts, source authority, and retrieval limits for the OCR Word/JSONL derivative. |
| `cpc_playbook_full_content_2026-08-17.jsonl` | All 168 Word body nodes (142 paragraphs and 26 tables) from the bundled CPC playbook, preserved as source-faithful searchable records. |
| `source_case_records_cpc_playbook_full_2026-08-17.jsonl` | Eight source-faithful CPC worked examples and account observations, with reported metrics, author explanation, action, and applicability boundary kept separate. |
| `source_validation_report_cpc_playbook_full_2026-08-17.md` | CPC playbook full-content review; original Word is manually reviewed and retained, while the default binary reader keeps the machine status `PARTIAL`. |
| `24_live_market_data_mcp_decision_gate.md` | 西柚洞察 MCP live-data gate for current market, competitor, keyword, trend, ranking, and expansion decisions; includes query logging and blocked/partial rules. |
| `25_skill_first_decision_gate.md` | Mandatory Skill-first loading order before Amazon advertising recommendations, reference selection, status reporting, and generic-advice prohibition. |
| `portable_108_source_manifest.jsonl` | SHA-256-verified portable-asset map for all 108 reviewed sources: 100 project articles and 8 user documents. Stored in `assets/knowledge/`; preserves original paths separately from Skill-relative copies. |
| `27_portable_108_evidence_pack.md` | Mandatory retrieval and answer-evidence contract: name actual source/claim/case matches rather than presenting all 108 sources as direct support. |
| `full_content_coverage_108_2026-08-18.jsonl` | Source-by-source retrieval audit: 108/108 original assets and their full-text, cell, page-OCR or embedded-media-OCR layers; `incomplete` must be treated as a retrieval gap. |
| `portable_case_background_index_2026-08-18.jsonl` | 48 source-preserving case records for detailed background retrieval; retains metrics, observation, author explanation, action/unknown action and transfer boundary. |
| `28_full_content_retrieval_coverage_108_2026-08-18.md` | Retrieval-layer selection, audit interpretation, case-background answer contract, and OCR/original-source boundary. |
| `source_manifest_30_ad_tactics_2026-08-19.jsonl` / `claim_review_30_ad_tactics_2026-08-19.jsonl` | Separate, source-faithful review of the 7-page `30种捡漏广告玩法.pdf`: 8 retained claims and zero account cases; status is `PARTIAL` only because the original PDF is binary to the default manifest parser. |
| `portable_109_source_manifest_2026-08-19.jsonl` / `full_content_coverage_109_2026-08-19.jsonl` | Current portable scope: 100 project articles plus 9 user documents, 109/109 retrievable with source boundaries. The 48-case index remains unchanged because the new PDF contains tactics rather than source-faithful account cases. |
| `29_30_ad_tactics_integration_2026-08-19.md` | Mandatory source/claim/page boundary when answering questions about the new low-cost “捡漏” tactics PDF. |

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
| Live advanced-diagnosis PDF | 143-page visual review; report matrix, aggregation, targeting, negatives, keyword research, variants and lifecycle claims; current UI takes precedence over the PDF snapshot. | `SRC-3a9e4ddd5371`, `references/23_advanced_ads_pdf_live_review_2026-08-13.md` |
| Portable desktop evidence pack | Offline retrievable originals for the full reviewed batch; use SHA-256 manifest and list only actual question matches as evidence. | `assets/knowledge/portable_108_source_manifest.jsonl`, `references/27_portable_108_evidence_pack.md` |

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
