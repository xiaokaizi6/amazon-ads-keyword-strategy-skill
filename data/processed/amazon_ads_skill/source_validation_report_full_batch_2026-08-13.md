# Source Validation Report

- Scope source count: 108
- Machine-readable source count: 100
- Manually reviewed source count: 8
- Reviewable source count: 108
- Claim count: 781
- Checked source count: 108
- Validation errors: 0
- Source cases extracted: 36
- Source case validation errors: 0
- Status: **PARTIAL**

## Source Types

- project_corpus: 100
- user_document: 8

## Review Inputs

- Claims file: `data/processed/amazon_ads_skill/full_batch_claims_2026-08-13.jsonl`
- Source cases file: `data/processed/amazon_ads_skill/full_batch_cases_2026-08-13.jsonl`
- Claim review is not a text-only truth classifier; statuses require explicit evidence references.

## Coverage

- Unreviewed source IDs: none
- Unreadable source IDs: SRC-214ee7c1e651, SRC-2c0a32e82d29, SRC-3328e6e7662e, SRC-3a9e4ddd5371, SRC-3d7548bc16d9, SRC-ceb5e990430e, SRC-d9b87550b32a, SRC-f564d5134e68
- Unreadable here means the default automated parser could not read the binary file; a source may still be manually reviewed and marked `manual_reviewed: true`.

## Claim Status Counts

- confirmed_error: 4
- context_dependent: 187
- disputed: 25
- outdated: 3
- supported: 131
- unresolved: 204
- unsupported: 227
