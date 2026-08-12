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
