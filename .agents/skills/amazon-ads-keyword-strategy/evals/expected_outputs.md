# Expected Outputs

This eval set checks whether the skill gives conditional Amazon ads and keyword strategy advice instead of generic ACOS-only answers.

## Required Output Shape

Every full answer should follow the skill format:

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

## Global Must Include

- Product stage and ad objective before strong recommendations.
- ACOS interpreted with TACOS, CPC, CTR, CVR, orders, ad order share, natural order share, natural rank, Session, and Unit Session Percentage where relevant.
- Separation of `出单词` and `排名目标词`.
- Search-term actions using add exact, keep observing, lower bid, negative exact, negative phrase, or budget isolation.
- Case library references as similarity anchors, not universal rules.
- Comment signals lowered to medium or low confidence unless they have condition, action, reasoning, limitation, and supporting evidence.
- Noise comments excluded from the rule library.
- Keyword library building is separate from keyword classification.
- Keyword library answers include source, type, status, metrics, priority, risk flags, and update cadence.
- `出单词` and `自然排名目标词` remain separate in the keyword library.

## Global Must Not Include

- Low ACOS automatically means natural ranking will improve.
- High ACOS automatically means the campaign should be closed.
- High ad order share is always bad or always normal without product-stage context.
- Comment-only advice as high confidence.
- Case posts converted into universal rules.
- Directly closing ads without checking objective, sample size, ad position, CTR, CVR, TACOS, and natural rank.
- Building only a plain keyword list when the user asks for a keyword library.
- Treating one source, such as comments or competitor reverse lookup, as enough to finalize the library.
- Declaring an unsupported lecture claim `confirmed_error` without direct higher-quality counterevidence.
- Silently deleting unresolved or disputed approaches instead of preserving their conditions and risks.

## New Source Conflict Regression

When the user supplies conflicting lectures or files, the answer must:

- create a source inventory and record actual cross-validation coverage;
- distinguish `confirmed_error`, `outdated`, `unsupported`, `context_dependent`, `disputed`, `unresolved`, and `supported`;
- treat copied or syndicated sources as one evidence cluster;
- retain unresolved meaningful views;
- explain each approach's applicable conditions, risks, missing data, and bounded validation test;
- avoid claiming all project documents were checked unless the coverage record proves it.

## Dedicated Regression Case

For `T009` the answer must contain:

- 不能只看 ACOS
- 要检查 CPC 是否过低
- 要检查广告位和 CTR
- 要检查广告出单词和自然排名目标词是否一致
- 要检查整体 CVR / Session / Unit Session Percentage
- 要提示广告依赖风险

The answer must not contain:

- 直接说广告效果很好不用调整
- 直接说低 ACOS 一定能推自然排名
- 直接建议关闭广告

## Coverage Map

| Coverage area | Case IDs |
| --- | --- |
| 新品期广告结构 | T001, T002, T033 |
| 自动广告跑词 | T003, T004, T030 |
| 手动精准广告优化 | T005, T006, T029 |
| 词组匹配优化 | T007, T008 |
| 广泛匹配烧预算 | T012, T040 |
| 点击多无订单 | T013, T030 |
| 样本量不足 | T014 |
| ACOS 高但自然排名提升 | T005, T010 |
| ACOS 低但自然排名不提升 | T009, T029 |
| TACOS 下降但 ACOS 上升 | T010, T011 |
| 广告单占比过高 | T015, T016, T034 |
| 自然单占比过低 | T016, T032, T034 |
| 竞品 ASIN 投放 | T017, T018, T035 |
| 品牌词防守 | T019, T032 |
| 旺季前广告放量 | T020 |
| 淡季控成本 | T021 |
| 清库存广告 | T022, T038 |
| 案例帖处理 | T023 |
| 评论区噪音过滤 | T024, T039 |
| 评论区诊断观点降置信度 | T004, T025, T026 |
| 关键词库建立 | T041 |
| 广告搜索词更新关键词库 | T042 |
| 出单词与自然排名目标词区分 | T027, T029, T035, T043 |
| 新讲义主张交叉验证 | T044, T045, T046 |
| 条件化保留争议观点 | T047 |
| 进阶诊断讲义案例和条件阈值 | T048 |
| 同一讲义第二份整理版、来源案例层和非独立证据 | T050 |
| 新来源案例保留与主动提示 | T049 |

## T046: CPC Playbook Claims Must Be Conditional

The answer must include:

- 20 次点击是 Amazon 官方建议的否词检查点，不是所有账户的自动否词命令
- TOS 100%-200% 等固定比例必须条件化，并说明需要账户数据验证
- “新品三个月流量扶持”保持未确认，不得写成平台通用机制
- quality-score 扣费公式不能在没有当前官方证据时写成 Amazon 平台机制
- 来源清单、原子主张和覆盖状态；`PARTIAL`/`NOT_READY` 不得写成全部资料已核对

The answer must not contain:

- 所有账户通用
- 已证明正确
- 已核对全部项目资料

## T047: Keep Unresolved Claims With Explicit Markers

The answer must include:

- `disputed`、`unresolved`、`unsupported` 等来源状态
- 适用条件、缺失数据、支持路线和保守路线
- 可逆验证窗口、成功标准和停止标准

The answer must not:

- 静默删除争议观点
- 将未验证观点写成通用规则
- 给出没有来源状态的确定性结论

## T048: Advanced Diagnosis Lecture Must Remain Conditional

The answer must include:

- `讲义案例提示` and the four `CASE-ADV-*` case anchors
- `context_dependent`, `unsupported`, and `unresolved` source-status markers
- 20/100 clicks as conditional checkpoints, not automatic commands
- inventory 1.5/3 months and placement +20%/−10% explicitly marked as lecture examples, not universal thresholds
- a reversible validation window, missing data, and alternative routes

The answer must not:

- call 1.5 months a platform inventory rule
- make +20% placement or −10% overall bid the default action
- say every account must wait for 100 clicks before a negative action
- call 2–6 months a platform support period

## T050: Second Rewrite Must Not Be Double-Counted

The answer must include:

- `讲义案例提示` and the fact that `SRC-3328e6e7662e` is another rewrite of the same lecture PDF, not independent corroboration
- source-case records for the 2-click/1-order example and the placement/budget examples
- `context_dependent`, `unsupported`, and `unresolved` markers for thresholds, UI windows, and lifecycle timing
- aggregation of parent/child metrics by totals before recomputing rates
- conditions, missing data, conservative route, test route, and a reversible validation window

The answer must not:

- call 2× gross margin a platform rule
- make ACOS ≤20% imply a mandatory 50% budget increase
- call BSR Top20–100 an official requirement
- call 2 weeks × 4 rounds a platform support period

## T049: Retain New-Source Cases With Their Evidence Boundary

The answer must include:

- `source_case_records.jsonl` and `case_observation`
- source-faithful observation, author explanation, and action as separate fields
- case confidence, matching facts, material mismatches, and source location
- a proactive `讲义案例提示` when a future diagnosis materially relates to the retained case
- clear statement that a case is not a universal executable rule

The answer must not:

- delete a meaningful case because its explanation is unsupported or conflicts with a rule
- turn a source case into a universal threshold or causal claim
- silently omit its evidence boundary in a related future answer

## T051: Pricing, Promotion, and Launch Sources Must Stay Conditional

The answer must include:

- `SRC-f564d5134e68`, `SRC-2c0a32e82d29`, and `SRC-d9b87550b32a` with source status and evidence-cluster limits
- reference-price validation, current marketplace/eligibility checks, and explicit rejection of fixed “10 orders/one week” rules
- promotion stacking and formula assumptions, with checkout verification rather than universal stacking claims
- `confirmed_error`/policy-risk markers for fake orders, review compensation, review clubs, related-account price manipulation, and artificial add-to-cart/wishlist
- a compliant alternative route and a reversible test window for conditional or unsupported launch parameters

The answer must not:

- recommend review manipulation, fake orders, related-account reference-price manufacturing, or ranking/traffic manipulation
- present 20%-25% margin, 5% Coupon, ACOS50%, or `Price×ACOS×CR` as universal rules
- treat old Deal/Prime fees, windows, or discount percentages as current without marketplace/date verification

## T052: Image-Only Ad Report Must Preserve Cases and Ranking Uncertainty

The answer must include:

- `SRC-3d7548bc16d9` and the fact that the Word source was manually read from 12 images while the automated manifest remains `readable:false`
- `SRC-3d7548bc16d9-CASE-001` through `CASE-004` as source observations with confidence and missing denominators
- `disputed`/`unsupported`/`context_dependent` markers for exact-match ranking claims, TOS +900%, 50%-60% ACOS, +10%-20% placement, and 70% budget-online thresholds
- Purchased Product and Placement as diagnostic hypotheses, not automatic campaign changes
- matching conditions, mismatches, alternative route, and reversible validation window

The answer must not:

- claim exact keywords or TOS guarantee organic ranking
- copy +900% TOS, fixed $0.02/$0.2 bids, or 1-2-click stop rules as defaults
- call a single image case or fixed online percentage a platform rule

## T053: Disputed and Uncertain Content Must Remain in the Skill

The answer must include:

- explicit retention of `disputed`, `unresolved`, `unsupported`, `outdated`, and `context_dependent` claims
- source ID, claim ID, original location, conditions, missing evidence, and verification test
- `references/21_disputed_uncertain_claim_retention.md` and the claim-review JSONL as the retention layer
- `references/22_full_batch_review_2026-08-13.md` as the unified-batch coverage/truth boundary
- a clear distinction between “retained in the Skill” and “promoted into `merged_rules.jsonl`”

The answer must not:

- delete or silently ignore a claim because it lacks support or conflicts with another source
- rewrite a disputed view as a universal rule
- claim that a claim is absent from the Skill merely because it is not in `merged_rules.jsonl`

## T054: Full Corpus and Uploaded Materials Must Share One Audit Batch

The answer must include:

- one unified manifest covering 100 project articles plus all in-scope uploaded documents
- one unified claim review and one unified source-case review, with checked and unreviewed source IDs
- conservative status assignment for corpus records rather than treating extracted article records as proven facts
- an honest `PARTIAL`/`PASS`/`NOT_READY` result and explicit unreadable/visual-review limitations

The answer must not:

- run separate reports and call them one full-batch review
- claim all 100 articles were factually validated merely because their source IDs are present
- hide A069/manual extraction gaps, binary document limitations, or the distinction between coverage and truth verification

## T055: Skill Structure and Progressive Disclosure

The answer must include:

- `SKILL.md` as the only required execution entry with `name` and `description` frontmatter
- `agents/openai.yaml` as UI metadata, when the skill is intended for Codex discovery
- references loaded on demand through a direct References Map rather than copying every long source into `SKILL.md`
- a distinction between full-diagnosis output and narrow/source-review output
- structural validation with `quick_validate.py` and project validation with `validate_outputs.py`

The answer must not:

- claim that `README.md` is required for Codex skill discovery
- force an unrelated narrow question into all 11 diagnosis sections
- claim that structural validation proves model answer quality

## T056: Live Market Data MCP Must Gate Current Decisions

The answer must include:

- a required 西柚洞察 MCP call for current market, competitor, keyword, demand, trend, ranking, or expansion decisions
- `实时数据调用状态` with an honest `COMPLETE`, `PARTIAL`, `BLOCKED`, or `NOT_REQUIRED` value
- marketplace/site, ASIN or keyword, requested/returned time window, actual operation name, freshness, returned fields, and missing data
- a clear separation between MCP market evidence, user account reports, project claims/cases, and Amazon official policy/function evidence
- conditional alternatives or a reversible low-risk test when MCP data is missing or incomplete

The answer must not:

- invent an MCP operation, field, date, record count, or result
- claim a market-dependent decision was validated without a successful, sufficiently scoped call
- use search volume or competitor rank alone as proof of organic-ranking causality
- issue a mandatory bid, negative-keyword, budget, or campaign action after a failed MCP call

## T057: Skill Must Be Loaded Before Advertising Advice

The answer must include:

- `Skill 使用状态` with `LOADED`, `PARTIAL`, `BLOCKED`, or `NOT_REQUIRED`
- confirmation that the current `SKILL.md` was read before the recommendation, plus the actual Skill path when available
- the task-relevant References Map entries and the applied stage, objective, data, evidence, and compliance constraints
- a clear prohibition on giving Amazon advertising actions from generic memory outside the Skill
- diagnostic questions or reversible tests when the Skill or required reference cannot be loaded

The answer must not:

- issue a bid, budget, negative-keyword, campaign, ranking, or competitor action solely from general experience
- claim to have followed the Skill without loading it
- treat `merged_rules.jsonl` as the only Skill knowledge layer
- bypass the Skill-first gate because the user requested a short or direct answer

## T058: Full Source Content, Cases, And Author Reasoning

When a user asks for the CPC playbook or advanced-diagnosis PDF beyond a short conclusion, the answer must include:

- `references/26_full_source_materials.md` and the relevant `SRC-*` source ID;
- a specific DOCX body node or PDF page/claim/case location;
- separate `来源观察`, `作者思路/解释`, and reviewed source status;
- the original asset as the complete-content authority and the searchable JSONL/review layer as a retrieval aid;
- an explicit boundary that source cases and numeric thresholds are not automatic executable rules.

The answer must not:

- claim that a claim/case summary replaces the original source content;
- turn author commentary or a worked example into a universal Amazon platform fact;
- omit source status when using an empirical threshold, causal claim, or historical UI detail.

## T059: Portable 108-Source Background Must Show Actual Evidence

The answer must include:

- `references/27_portable_108_evidence_pack.md` and the 108-source scope (100 project articles plus 8 user documents);
- actual matched source ID/file and claim/case/location, rather than a generic claim that the pack was used;
- separate source observation, author reasoning/explanation, reviewed status, conclusion basis, and applicability boundary;
- a statement that original assets are complete-content authority and JSONL is a retrieval/review aid;
- an honest no-direct-match boundary when the pack does not support the requested conclusion.

The answer must not:

- list all 108 sources as if every one directly supports the answer;
- convert a case, author explanation, or numeric threshold into a universal rule;
- claim the binary-document `PARTIAL` review state means the material was unread or that all claims are proven.

## T060: Image-Only PDF OCR Must Preserve Page-Level Source Authority

The answer must include:

- `SRC-3a9e4ddd5371`, the original PDF page, and `references/26_full_source_materials.md` when using the OCR derivative;
- a clear `OCR 派生文本` marker and the distinction between a retrieval aid and original-source authority;
- a warning to verify tables, screenshots, formulas, numbers, proper nouns, or low-confidence OCR text against the original PDF page.

The answer must not:

- cite OCR text as if it were verified verbatim original text;
- silently fix uncertain OCR wording or use it as a universal advertising rule;
- claim that OCR makes the image-only PDF automatically machine-verified.

## T061: Uploaded-Material Questions Must Answer With Background And Reasons

The answer must include:

- a direct conclusion before lengthy process detail;
- actual matched uploaded-source background and location;
- `是否命中上传案例`, including case ID and material match/mismatch or an honest `未命中具体案例`;
- the conclusion reason, separating source observation, author explanation, and reviewed conclusion;
- source status and applicability boundary.

The answer must not:

- require the user to inspect PNGs, screenshots, OCR intermediates, or Word visual QA before receiving the conclusion;
- present all uploaded materials as direct proof when only one source/case was actually matched;
- turn a source case or author threshold into a universal advertising action.

## T062: 108-Source Questions Must Use Full Retrieval And Detailed Case Background

The answer must include:

- `references/28_full_content_retrieval_coverage_108_2026-08-18.md` when relying on the full pack;
- the 108/108 retrieval-coverage scope and the actual matched source/content location;
- a search of the detailed case-background index and, if matched, case ID, conditions, metrics, observation, author explanation, action/unknown action, and transfer boundary;
- an honest `未命中具体案例` when no matching retained case exists;
- an OCR/original-source boundary for image, PDF, table, formula, number, or low-confidence text evidence.

The answer must not:

- assert that all lecture claims are verified merely because all files are retrievable;
- use a case title alone as its background or turn a case into a default action;
- call a file integrated when its audit status is `incomplete`.
