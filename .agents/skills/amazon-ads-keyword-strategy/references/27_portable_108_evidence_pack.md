# Portable 108-Source Evidence Pack

## Scope And Integrity

This package makes the reviewed full batch available in a desktop Codex Skill without depending on the original machine paths.

- Scope: 108 sources: 100 `project_corpus` articles and 8 `user_document` files.
- Complete original assets: `assets/source_materials/`. Project articles are in `project_articles/`; six additional uploads are in `user_uploads/`; the CPC DOCX and 143-page PDF remain at the source-material root.
- Portable source map: `assets/knowledge/portable_108_source_manifest.jsonl`. It retains each original acquisition path and adds a Skill-relative asset path and SHA-256 integrity result.
- Retrieval indexes: `articles_index.jsonl`, `article_sections.jsonl`, `normalized_records.jsonl`, `merged_rules.jsonl`, `case_library.jsonl`, `conflict_candidates.jsonl`, `full_batch_claim_review_2026-08-13.jsonl`, and `full_batch_case_records_2026-08-13.jsonl`.
- Batch boundary: `references/22_full_batch_review_2026-08-13.md` and `assets/knowledge/source_validation_report_full_batch_2026-08-13.md`. Its `PARTIAL` status is the binary auto-read limitation, not a claim that all material was automatically proven true.

The original assets are the complete-content authority. JSONL indexes are retrieval and review layers. They do not turn every lecture statement, example, or threshold into an executable rule.

## Required Retrieval

For every Amazon advertising, keyword, ranking, budget, bid, campaign, or source-content answer:

1. Complete the Skill-first loading gate in `references/25_skill_first_decision_gate.md` and load the business references relevant to the question.
2. Search the portable manifest and relevant structured indexes for the question's terms, source IDs, claim IDs, and case IDs.
3. Open the matched original asset when the answer needs full context, a table, a worked example, or author reasoning. Do not cite an uninspected source merely because it is inside the 108-source pack.
4. Use only actual matches as evidence. A source that does not match the question is part of searchable background, not proof for the conclusion.
5. Apply the claim/case status and source-validation boundaries from references 14, 21, 22, and any source-specific integration reference.

If no direct source match is found, say so. Do not manufacture a source-backed conclusion; request the relevant account data or offer only a bounded diagnostic question/reversible test when the Skill allows it.

## Answer Evidence Contract

When the 108-source pack materially informs an answer, include a compact section like:

```text
证据依据
- 检索范围：108 份可携带资料包；实际命中 <source ID / filename / claim or case ID / location>
- 来源观察：<source-reported fact or case outcome>
- 作者思路/解释：<author reasoning, or unknown>
- 审查状态：<supported / context_dependent / disputed / unresolved / unsupported / outdated>
- 本次结论依据：<why the stated conclusion follows, including counterevidence if relevant>
- 当前适用边界：<stage, marketplace, margin, data gaps, and verification boundary>
```

For a narrow answer, list only the actual matched entries; never paste all 108 source names as performative citation. For a full source-review question, report both the pack-wide coverage count and the precise sources actually inspected.

Keep `来源观察`, `作者思路/解释`, and the reviewed conclusion separate. A worked case can be a similarity anchor, but it is not a universal Amazon mechanism or a default bid, budget, ACOS, ranking, or negative-keyword rule.

## User Knowledge-Answer Priority

For this user's questions about the uploaded learning materials, use this compact order unless a fuller diagnosis is requested:

```text
结论：<direct answer; state uncertainty when evidence cannot decide>
资料背景：<actual matched source ID/file/page/node or claim/case; explain what source context is relevant>
是否命中上传案例：<case ID + match/mismatch, or 未命中具体案例>
结论理由：<source observation, author explanation where relevant, review result, and why it supports or limits the conclusion>
来源状态与适用边界：<status, stage/objective/data gaps, and verification need>
```

Do not require the user to open a PNG, screenshot, OCR JSONL, or Word document before receiving the answer. Those are internal retrieval/verification aids. When an exact screenshot/table/formula is material, cite the original page location and explain the limitation in prose; only provide the image if the user specifically asks to see it.
