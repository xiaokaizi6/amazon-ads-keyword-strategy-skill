# Full Source Materials And Retrieval Contract

## Scope

This reference preserves full-source access for two user-provided learning materials. It supplements, rather than replaces, atomic claims, source-faithful cases, and the original binaries.

| Source | Original asset | Searchable/structured layer | Use boundary |
| --- | --- | --- | --- |
| `SRC-214ee7c1e651` CPC playbook | `assets/source_materials/亚马逊CPC广告打法知识体系全梳理v1_20260804.docx` | `assets/knowledge/cpc_playbook_full_content_2026-08-17.jsonl`, claim review, and source-case records; canonical copies remain in `data/processed/amazon_ads_skill/` | 168 DOCX body nodes retain paragraphs and tables. The document's author commentary, figures, thresholds, and examples remain source observations unless their claim record says otherwise. |
| `SRC-3a9e4ddd5371` advanced diagnosis course | `assets/source_materials/亚马逊专题课-进阶广告诊断有优化全指导.pdf` | `assets/knowledge/advanced_ads_pdf_live_claims_2026-08-13.jsonl`, `assets/knowledge/source_case_records_advanced_ads_pdf_live_2026-08-13.jsonl`, and the 143-page OCR layer `assets/knowledge/advanced_ads_pdf_ocr_full_2026-08-18.jsonl`; a readable derivative is `assets/derivatives/亚马逊专题课-进阶广告诊断有优化全指导-OCR文字检索版.docx` | The original is a 143-page image-only PDF and remains the complete source. OCR is machine-derived retrieval text: it keeps original page numbers but must be checked against the PDF for tables, screenshots, formulas, numbers, proper nouns, and low-confidence lines. Derivative metadata is in `advanced_ads_pdf_ocr_derivative_manifest_2026-08-18.json`. |

## Required Retrieval Order

For a question about either source:

1. Search the relevant structured layer for source IDs, claim IDs, case IDs, and terms.
2. For the image-only PDF, search the page-located review records and OCR layer first; read the matching original PDF page when the question needs fuller context, a table, a worked example, author reasoning, or any exact text.
3. Keep the answer layers separate: `来源观察` (what the author reports), `作者思路/解释`, and `可用结论` (the claim status after review).
4. State the actual source location. Do not imply that every passage in a source supports the conclusion.

## Answer Contract

When either source materially informs an answer, include:

```text
讲义依据
- 来源：<source ID + file name + node/page or case/claim ID>
- 来源观察：<what the material reports>
- 作者思路/解释：<author reasoning, or unknown>
- 审查状态：supported / context_dependent / disputed / unresolved / unsupported / outdated
- 当前适用边界：<conditions, missing data, and any current-platform check>
```

The original assets preserve all source content. The structured layers make it searchable; they do not convert every paragraph, case, threshold, or author opinion into an executable rule.

The OCR Word and OCR JSONL are derived aids, not a replacement source. State `OCR 派生文本` when they materially inform an answer, cite the original PDF page, and do not silently correct or upgrade machine-recognized text.
