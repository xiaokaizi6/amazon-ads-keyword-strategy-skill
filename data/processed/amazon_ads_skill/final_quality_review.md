# Final Quality Review: Amazon Ads Keyword Strategy Skill

- Review date: 2026-08-12
- Scope: `.agents/skills/amazon-ads-keyword-strategy`
- Validation command: `python ".agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py"`
- Validation result: PASS, 0 errors, 0 warnings
- Report: `data/processed/amazon_ads_skill/validation_report.md`

## Overall Conclusion

The skill is ready for use as an Amazon ads and keyword strategy diagnostic skill. It has usable examples, a 45-case eval set, executable rebuild scripts for rules and cases, and a source-review workflow that inventories files and reports claim coverage without overstating certainty.

The main operating principle is preserved: recommendations must be conditional, evidence-backed, and never based on ACOS alone.

## Review Checklist

| Area | Result | Notes |
| --- | --- | --- |
| SKILL.md invocation quality | PASS | Frontmatter has `name` and `description`; the body states when to use the skill, required inputs, workflow, record types, output format, references, prohibitions, and quality checklist. |
| References coverage | PASS | References cover taxonomy, extraction schema, keyword classification, campaign structure, search-term optimization, product-stage strategy, conflict handling, metric thresholds, case library, noise filtering, source index, source-validation protocol, and source-review schema. |
| Advertising coverage | PASS | Campaign structure covers launch, growth, stable, seasonal peak/preheat, off-season, clearance, auto, exact, phrase, broad, ASIN targeting, defense, and competitor attack. |
| Keyword strategy coverage | PASS | Keyword classification separates core terms, long-tail terms, competitor terms, defense terms, discovery terms, big terms, order-producing terms, and ranking target terms. |
| Search-term workflow | PASS | Search-term logic includes add exact, negative exact, negative phrase, bid down, bid up, observe, and sample-size handling. |
| Ranking diagnosis | PASS | The skill explicitly checks ad-rank/natural-rank relationships, target keyword alignment, natural rank movement, and cases where ad orders do not move natural rank. |
| Case library handling | PASS | CASE001, CASE002, CASE010, CASE012, CASE015 and other anchors are positioned as comparison evidence, not universal rules. |
| Noise filter | PASS | Noise rules exclude invitations, registration links, thanks-only replies, short replies, off-topic chatter, unsupported absolute claims, and duplicate comments from rule logic. |
| Conflict register | PASS | Conflict register resolves low ACOS, high ad order share, high ACOS rank push, exact/broad/auto tensions, and ad dependency with conditional rules. |
| ACOS over-dependence | PASS | SKILL.md, metric thresholds, examples, evals, and validation expectations all prohibit ACOS-only decisions. |
| Metrics completeness | PASS | Required diagnosis checks include TACOS, CVR, CTR, CPC, ad order share, natural order share, natural rank, Session, and Unit Session Percentage where relevant. |
| Low ACOS but rank not moving | PASS | Example output and eval T009 cover low ACOS, low CPC, high ad order share, top ad position, and natural rank outside page 7. |
| Advertising dependency | PASS | CASE001/CASE002, conflict C002/C010, examples, and evals require stage-aware handling of high ad order share. |
| 出单词 vs 排名目标词 | PASS | Keyword classification, search-term logic, case diagnosis example, and evals explicitly require separating these terms. |
| 中小词 vs 大词 | PASS | CASE003/CASE010 and eval T027 cover the risk that medium/small-term orders do not necessarily move big-word natural rank. |
| Stage strategy | PASS | Launch, stable, seasonal preheat/peak, off-season, and clearance strategies are covered in references, examples, and evals. |
| Examples | PASS | Four example files cover launch structure, search-term optimization, high ACOS with ranking improvement, and low ACOS with no ranking movement/high ad-share dependency. Output examples follow the 11-section skill format. |
| Evals | PASS | `test_cases.jsonl` has 45 cases, exceeding the 35-case minimum, and covers all requested categories plus regression cases. |
| Validation script | PASS | `validate_outputs.py` executes successfully and checks the skill, processed schemas, optional source-review artifacts, and structured issue reporting. |

## Phase 12 Review

Examples are reusable and not merely placeholders:

- `example_input_search_term_report.md` contains four compact input scenarios.
- `example_output_ads_diagnosis.md` demonstrates search-term optimization and the high-ACOS rank-push exception.
- `example_output_keyword_strategy.md` demonstrates launch-stage ad structure and keyword planning.
- `example_output_case_diagnosis.md` demonstrates the low-ACOS/no-ranking-movement case with ad dependency risk.

The case diagnosis example covers all required points:

- Low ACOS does not guarantee natural ranking improvement.
- High ad order share implies dependency risk.
- Order-producing terms must be separated from ranking target terms.
- Ad placement, CTR, CVR, category-average conversion rate, Session, and Unit Session Percentage must be checked.
- Medium/small-term orders may not push big-term natural rank.

## Phase 13 Review

The eval set has 40 JSONL cases. It covers:

- launch-stage structure,
- auto discovery,
- exact optimization,
- phrase optimization,
- broad-match budget burn,
- clicks without orders,
- insufficient sample size,
- high ACOS with natural rank improvement,
- low ACOS without natural rank improvement,
- TACOS down with ACOS up,
- high ad order share,
- low natural order share,
- competitor ASIN targeting,
- brand defense,
- seasonal pre-peak scaling,
- off-season cost control,
- clearance ads,
- case-post handling,
- comment noise filtering,
- downgraded confidence for comment diagnostics.

Dedicated regression case `T009` contains the required low-ACOS/high-ad-share expectations and the prohibited wrong answers.

## Phase 14 Review

`validate_outputs.py` checks:

- required directories and files,
- SKILL.md frontmatter,
- JSONL legality,
- required fields for `extracted_records.jsonl`, `merged_rules.jsonl`, and `case_library.jsonl`,
- irrelevant noise exclusion from merged rules,
- high-confidence comment violations,
- evidence quote length,
- eval count and T009 expectations,
- non-empty references,
- example coverage and 11-section output format.

Current execution result is PASS.

## Residual Risk

This review verifies artifact quality, rebuildability, and source-review contracts. It does not run live model-output scoring against every eval case. Future evaluation can add an automated runner that feeds each `user_input` to a model and checks `expected_must_include` / `expected_must_not_include` against actual responses. Source claim review remains evidence-assisted rather than an automatic truth classifier.

The source corpus includes forum cases and comments, so recommendations should remain conditional and confidence-aware even when a pattern appears repeatedly.
