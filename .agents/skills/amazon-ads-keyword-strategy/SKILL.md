---
name: amazon-ads-keyword-strategy
description: Use this skill when analyzing Amazon advertising, keyword strategy, keyword library building, search term reports, competitor keyword data, Keepa trends, product lifecycle strategy, ACOS/TACOS optimization, ranking diagnosis, and launch-stage ad planning.
---

# Purpose

Diagnose Amazon ads, keyword ranking, keyword library building, search-term optimization, campaign structure, and product-stage strategy with evidence-backed, conditional recommendations.

This skill must avoid generic advice. It should separate:

- case observations,
- executable rules,
- diagnostic hypotheses,
- diagnostic questions,
- counterexamples,
- comment signals,
- irrelevant noise.

# When to Use This Skill

Use this skill for:

- Amazon PPC diagnosis,
- search term report optimization,
- keyword classification and rank planning,
- ACOS/TACOS/CPC/CVR/CTR diagnosis,
- ad order share and natural order share problems,
- launch-stage and seasonal ad planning,
- competitor ASIN targeting,
- cases where ad orders exist but natural ranking does not improve,
- cases where low ACOS looks good but ranking or total performance is weak.

# Required Inputs

Ask for or infer these before making strong recommendations:

- product stage,
- category and marketplace,
- product price and gross margin,
- ad objective: profit, ranking, launch data, defense, clearance, or seasonal capture,
- budget and current spend,
- search term report or campaign metrics,
- target keywords and current natural rank,
- keyword library sources: manual seeds, product listing terms, competitor reverse lookup, ad search terms, ABA/SQP, Keepa, Amazon front-end terms, articles, or comments,
- campaign type and match type,
- CTR, CVR, CPC, ACOS, TACOS, orders, spend,
- ad order share and natural order share,
- inventory pressure and promotion calendar.

# Optional Inputs

Helpful but not always required:

- Keepa/competitor trend data,
- ABA/search frequency data,
- competitor price/review/rating comparison,
- BSR history,
- Session and Unit Session Percentage,
- ad placement data,
- dayparting or budget exhaustion timing,
- prior negative keyword list,
- launch calendar or seasonal demand window.

# Core Workflow

1. Identify the product stage and primary ad goal.
2. Check data completeness and mark missing metrics.
3. Build or update the keyword library when the task includes seed words, competitor terms, ad search terms, front-end terms, third-party keyword exports, article terms, or comment signals.
4. Classify keywords by role: discovery, profit, defense, competitor attack, conversion, negative, risk, seasonal, or natural-rank target.
5. Validate keywords with source, metrics, product stage, sample size, and ranking objective.
6. Update keyword statuses: unverified, testing, validated converting, ranking target, scale word, defensive word, negative candidate, negative exact, negative phrase, seasonal word, or risk word.
7. Maintain negative keyword library with sample-size and relevance logic.
8. Separate cases from rules and comments.
9. Diagnose campaign structure by goal and stage.
10. Review search terms with sample-size logic.
11. Interpret ACOS with TACOS, CVR, CPC, orders, ad order share, and natural rank.
12. Check whether ad-order terms match natural-rank target terms.
13. Compare with case library only as a similarity anchor.
14. Resolve conflicts conditionally using product stage, margin, budget, sample size, ad goal, natural-rank target, inventory, and keyword type.
15. When new lectures or files are supplied, apply `references/14_source_validation_and_conflict_protocol.md` before promoting any claim into the rule library.
16. Use `scripts/review_sources.py` to create a source manifest and claim-level coverage report; do not create a claim review without atomic claim input.
17. Use `references/16_cpc_playbook_integration.md` as the validated/conditional integration layer for the CPC playbook; it is not a replacement for the raw source or claim review.
18. Produce a 7-day, 14-day, and 30-day action plan.

# Keyword Library Module

Use `references/12_keyword_library_building.md` and `references/13_keyword_database_schema.md` when the user asks to build, maintain, update, or audit a keyword library.

The keyword library must not be a plain keyword list. It must be a structured database that separates:

- seed keyword library,
- core keyword library,
- long-tail keyword library,
- competitor keyword library,
- search-term harvesting library,
- ranking target keyword library,
- conversion keyword library,
- negative keyword library,
- seasonal keyword library,
- risk keyword library.

Required outputs:

- `data/processed/amazon_ads_skill/keyword_library.jsonl`
- `data/processed/amazon_ads_skill/keyword_library.csv`
- `data/processed/amazon_ads_skill/keyword_library_report.md`

Optional operator export:

- `outputs/keyword_library.xlsx`

Important rules:

- Keyword classification and keyword library building are different tasks.
- Every keyword needs source, type, status, priority, risk flags, and metrics.
- Keyword sources should be multi-source; do not rely on one source only.
- `出单词` and `自然排名目标词` must be tracked separately.
- Comment-derived keywords are weak signals until validated by ad, ranking, or third-party data.
- Negative keywords need sample-size and relevance reasoning before final action.

# Record Types

- `case_observation`: concrete case data and metrics. Use for comparison, not universal rules.
- `executable_rule`: condition, action, reasoning, and limitations are all present.
- `diagnostic_hypothesis`: plausible explanation that needs verification.
- `diagnostic_question`: missing data or check required before deciding.
- `counterexample`: evidence that limits a common assumption.
- `comment_signal`: weak useful signal; do not use as a rule.
- `irrelevant_noise`: account invitations, thanks, short replies, off-topic discussion, or unsupported noise.

# Case Handling

Cases must stay separate from rules.

When using a case:

- cite the case pattern,
- list matching metrics,
- list mismatches,
- state confidence,
- explain what still needs verification.

Important anchors:

- CASE001: low ACOS, low CPC, high ad order share, ad rank first, but natural rank did not improve.
- CASE002: new product with 40-70 daily orders and 50%+ ad order share, but page-one ranking was difficult.
- CASE010: small/mid terms and budget pressure can conflict with big-word rank targets.
- CASE015: product targeting may have high CPC and may not help keyword ranking the same way keyword ads do.

# Comment Handling

Comments are never high confidence by default.

Use comments as:

- `diagnostic_hypothesis` when they propose a check or explanation,
- `counterexample` when they limit a common assumption,
- `comment_signal` when useful but weak,
- `irrelevant_noise` when social, promotional, too short, or off-topic.

Do not turn a comment into an absolute rule unless it has condition, action, reasoning, limitations, and supporting evidence.

# Noise Filtering

Exclude from rules:

- account invitations,
- registration links,
- thanks-only replies,
- simple social replies,
- off-topic chatter,
- emotional statements without data,
- unsupported absolute claims,
- too-short comments,
- duplicate comments.

Noise can be retained for audit, but it must not enter the rule library.

# Decision Rules

Every recommendation must be conditional.

Use:

- product stage,
- gross margin,
- budget,
- sample size,
- ad objective,
- natural-rank objective,
- inventory pressure,
- keyword type,
- campaign type and match type.

Examples:

- Low ACOS is not automatically good. Check CPC, CVR, order volume, TACOS, ad order share, and natural rank.
- High ACOS is not automatically bad. If the explicit goal is rank push, evaluate natural rank, total orders, TACOS, and review window.
- High ad order share is not automatically a reason to cut ads. New launch and rank-push stages may temporarily depend on ads.
- Broad match can discover terms, but it needs isolated budget, negative rules, and sample-size limits.

# Conflict Handling

Use `references/07_conflict_register.md` and `conflict_candidates.jsonl`.

For every conflict:

- state both views,
- do not declare one side universally correct,
- give a conditional decision,
- list required data,
- state when to avoid the action,
- keep case posts as support or counterexamples, not absolute rules.

# New Source Validation

Use `references/14_source_validation_and_conflict_protocol.md` whenever the user supplies lectures, documents, course notes, exports, or other knowledge sources.

- Preserve the original source and create a source inventory before evaluating claims.
- Cross-check material claims against all relevant project sources and all in-scope user-provided documents; record coverage and any unreadable or excluded files.
- For time-sensitive platform facts and policies, verify against current first-party Amazon sources and record the verification date.
- Do not call a claim wrong merely because it lacks evidence. Distinguish `confirmed_error`, `outdated`, `unsupported`, `context_dependent`, `disputed`, `unresolved`, and `supported`.
- If evidence cannot resolve a conflict, retain all meaningful views and explain each approach, conditions, risks, missing data, and a bounded validation test.
- Treat duplicated, syndicated, or mutually copied sources as one evidence cluster rather than independent confirmation.

# Conditional Source Claims

The skill must retain useful claims even when they are not universal rules. Use the claim status as an operating marker:

- `supported`: may be used as a conditional rule when the recorded conditions match; cite the source and limitations.
- `context_dependent`: may be used only after checking stage, marketplace, category, margin, budget, sample size, and objective; label it as conditional.
- `disputed`: show the meaningful View A and View B, explain the conflict, and do not return one unconditional action.
- `unresolved`: keep it as a diagnostic hypothesis or bounded test; do not state it as a platform fact or direct action.
- `unsupported`: preserve it for audit and alternative thinking, but do not use it as the default recommendation or threshold.
- `outdated`: retain historical context only and verify the current Amazon console/documentation before use.
- `confirmed_error`: do not recommend it; retain the direct counterevidence and verification trail.

Whenever a conditional source claim is used, the answer must include:

1. `来源状态` and source location;
2. applicable conditions and missing data;
3. the action route, alternative route, or reason to avoid the action;
4. a reversible validation window with success and stop criteria.

Do not silently drop `disputed`, `unresolved`, or `unsupported` claims. Do not silently promote them into `merged_rules.jsonl` as universal `executable_rule` records. Use `references/16_cpc_playbook_integration.md` and `data/processed/amazon_ads_skill/claim_review.jsonl` as the conditional claim layer.

# Confidence Rules

- `high`: rare; requires strong source evidence, concrete metrics, clear scope, and low contradiction.
- `medium`: useful but missing some data or category validation.
- `low`: weak, speculative, comment-only, missing metrics, or under-specified.
- Comments default to `medium` or `low`.
- Missing TACOS, CVR, CTR, CPC, ad order share, or natural rank lowers confidence.
- If data is insufficient, ask diagnostic questions instead of giving final action.

# Output Format

Always answer in this structure:

1. 当前诊断
2. 数据完整性检查
3. 产品阶段判断
4. 关键词分类
5. 广告结构诊断
6. 搜索词动作表
7. 竞价和预算调整
8. 自然排名与广告关系判断
9. 案例相似性提示
10. 风险和例外
11. 7 天 / 14 天 / 30 天行动计划

# References Map

- `01_taxonomy.md`: record taxonomy, topics, confidence, and noise types.
- `02_extraction_schema.md`: JSONL extraction schema and validation rules.
- `03_keyword_classification.md`: keyword roles and optimization actions.
- `04_campaign_structure.md`: stage and campaign-type structures.
- `05_search_term_optimization.md`: search-term actions and sample-size logic.
- `06_product_stage_strategy.md`: stage-specific strategy.
- `07_conflict_register.md`: conditional conflict decisions.
- `08_metric_thresholds.md`: metric interpretation and threshold limits.
- `09_case_library.md`: case anchors and similarity checks.
- `10_noise_filter_rules.md`: comment and noise exclusion rules.
- `11_source_index.md`: source clusters and processed data map.
- `12_keyword_library_building.md`: keyword library sources, sub-libraries, workflow, statuses, update cadence, and campaign assignment.
- `13_keyword_database_schema.md`: keyword library JSONL/CSV fields, allowed values, metrics object, and update semantics.
- `14_source_validation_and_conflict_protocol.md`: source inventory, claim-level cross-validation, error thresholds, uncertainty preservation, and coverage reporting.
- `15_source_review_schema.md`: JSONL contracts and status rules for source manifests, claim reviews, and coverage reports.
- `16_cpc_playbook_integration.md`: cross-validated integration of the user-provided CPC playbook, including supported definitions, conditional strategies, disputed ranking claims, and unresolved platform facts.

# Explicit Prohibitions

- 不要给泛泛建议。
- 不要只看 ACOS。
- 不要忽略 TACOS、CVR、CTR、CPC、广告单占比、自然排名。
- 不要忽略产品阶段。
- 不要忽略样本量。
- 不要把案例直接当成规则。
- 不要把评论区观点当成确定性结论。
- 不要把无关评论进入规则库。
- 不要把关键词分类等同于关键词库建立。
- 不要把出单词和自然排名目标词混为一谈。
- 冲突观点必须条件化处理。
- 不要把“缺少支持”直接写成“已证明错误”。
- 不要在没有覆盖记录时声称已检查全部项目资料。
- 无法确定的不同观点不得静默删除。

# Quality Checklist

Before finalizing:

- Do not give generic advice.
- Do not only look at ACOS.
- Do not ignore TACOS, CVR, CTR, CPC, ad order share, and natural rank.
- Do not ignore product stage.
- Do not ignore sample size.
- Do not treat a case as a universal rule.
- Do not treat comment viewpoints as certain conclusions.
- Do not allow irrelevant comments into the rule library.
- Do not treat keyword classification as the same thing as keyword library building.
- Separate converting keywords from natural-rank target keywords.
- If building a keyword library, include source, type, status, priority, metrics, and update cadence.
- Resolve conflicts conditionally.
- If new source material was supplied, record source coverage and claim status using the source-validation protocol.
- Reserve `confirmed_error` for claims with direct higher-quality counterevidence; preserve unresolved alternatives.
- When source files are supplied, use `scripts/review_sources.py` and report `PASS`, `PARTIAL`, `FAIL`, or `NOT_READY` coverage honestly.
- State confidence and missing data.
- Keep recommendations tied to evidence and business objective.
