---
name: amazon-ads-keyword-strategy
description: Use this skill when analyzing Amazon advertising, keyword strategy, search term reports, competitor keyword data, Keepa trends, product lifecycle strategy, ACOS/TACOS optimization, ranking diagnosis, and launch-stage ad planning.
---

# Purpose

Diagnose Amazon ads, keyword ranking, search-term optimization, campaign structure, and product-stage strategy with evidence-backed, conditional recommendations.

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
3. Classify keywords by role: discovery, profit, defense, competitor attack, or natural-rank target.
4. Separate cases from rules and comments.
5. Diagnose campaign structure by goal and stage.
6. Review search terms with sample-size logic.
7. Interpret ACOS with TACOS, CVR, CPC, orders, ad order share, and natural rank.
8. Check whether ad-order terms match natural-rank target terms.
9. Compare with case library only as a similarity anchor.
10. Resolve conflicts conditionally using product stage, margin, budget, sample size, ad goal, natural-rank target, inventory, and keyword type.
11. Produce a 7-day, 14-day, and 30-day action plan.

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

# Explicit Prohibitions

- 不要给泛泛建议。
- 不要只看 ACOS。
- 不要忽略 TACOS、CVR、CTR、CPC、广告单占比、自然排名。
- 不要忽略产品阶段。
- 不要忽略样本量。
- 不要把案例直接当成规则。
- 不要把评论区观点当成确定性结论。
- 不要把无关评论进入规则库。
- 冲突观点必须条件化处理。

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
- Resolve conflicts conditionally.
- State confidence and missing data.
- Keep recommendations tied to evidence and business objective.
