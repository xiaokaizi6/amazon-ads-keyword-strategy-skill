# Source Validation Report

- Scope source count: 1
- Machine-readable source count: 0
- Manually reviewed source count: 1
- Reviewable source count: 1
- Claim count: 18
- Checked source count: 1
- Validation errors: 0
- Source cases extracted: 4
- Source case validation errors: 0
- Status: **PARTIAL**

## Source Types

- course_lecture: 1

## Review Inputs

- Claims file: `data/processed/amazon_ads_skill/advanced_ads_pdf_live_claims_2026-08-13.jsonl`
- Source cases file: `data/processed/amazon_ads_skill/advanced_ads_pdf_live_cases_input_2026-08-13.jsonl`
- Claim review is not a text-only truth classifier; statuses require explicit evidence references.

## Coverage

- Unreviewed source IDs: none
- Unreadable source IDs: SRC-3a9e4ddd5371
- Unreadable here means the default automated parser could not read the binary file; a source may still be manually reviewed and marked `manual_reviewed: true`.

## Claim Status Counts

- context_dependent: 10
- outdated: 1
- supported: 6
- unsupported: 1

## Live rendering and evidence boundary

The source was re-rendered locally with `pdftoppm -r 120 -png` and all 143 rendered pages were checked. The PDF has an image-only / empty text layer, so the claim input is a human visual transcription with page locations, cross-checked against same-family rewritten lecture extracts. Those rewrites share the same evidence cluster and are not independent corroboration.

Current-platform checks were performed against Amazon first-party documentation on 2026-08-13. In particular, placement and audience bid controls have changed since the PDF's 2025-05 snapshot; the current console/documentation takes precedence. Product Opportunity Explorer is treated as an insight tool, not a guaranteed ranking or conversion threshold. The course's 20/100 negative thresholds, 75% result similarity, fixed test windows, budget percentages, and lifecycle dates remain conditional or unsupported rather than universal rules.

## Review artifacts

- Manifest: `data/processed/amazon_ads_skill/source_manifest_advanced_ads_pdf_live_2026-08-13.jsonl`
- Claims input: `data/processed/amazon_ads_skill/advanced_ads_pdf_live_claims_2026-08-13.jsonl`
- Claim review: `data/processed/amazon_ads_skill/claim_review_advanced_ads_pdf_live_2026-08-13.jsonl`
- Cases input: `data/processed/amazon_ads_skill/advanced_ads_pdf_live_cases_input_2026-08-13.jsonl`
- Case review: `data/processed/amazon_ads_skill/source_case_records_advanced_ads_pdf_live_2026-08-13.jsonl`

Pages 9-139 contain the decision-relevant report, metric, targeting, keyword, variant, match-type, lifecycle, and case material. Pages 141-143 are course/training and QR material; they are retained only as source-boundary observations and are excluded from rules. No rendered page was silently discarded.
