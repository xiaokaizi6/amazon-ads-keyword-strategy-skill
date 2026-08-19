# 《30种花样捡漏广告玩法》接入说明（2026-08-19）

## 来源与完整性

- 来源 ID：`SRC-4c37c63ff3a0`；用户提供 PDF 原件保存在 `assets/source_materials/30种捡漏广告玩法.pdf`，SHA-256 为 `4c37c63ff3a0d206ab55bd824adee732b906eb8423103120032e0482f8daefad`。
- 该 PDF 共 7 页。原件逐页渲染并完成视觉阅读；`assets/knowledge/30_ad_tactics_pdf_ocr_full_2026-08-19.jsonl` 提供 7 页、156 行 OCR 检索层，`assets/derivatives/30种捡漏广告玩法-OCR文字检索版.docx` 是同一检索用途的派生 Word。原 PDF 才是内容权威；OCR 和 Word 不能替代原页，尤其不能替代数字、专名、截图或低置信度文字。
- 标题为“30种花样捡漏广告玩法”，但可定位的编号为 1 至 28，末尾另有错拼词工具补充；原件内未定位编号 29、30。该差异保留为 `T30-CLM-008` 的 `unresolved`，不得补写不存在的两项。
- 文内称“阿波罗提供”，但作者身份、适用站点、日期、产品数据和账户绩效均未独立核验。PDF 元数据日期仅作文件信息，不作为出版或平台规则日期。

## 资料背景与可检索内容

这是一份低成本“捡漏”广告玩法清单，按自动投放、搜索词复投、自然单/Review 前提、SKU、品牌/错拼词/西语词、词根、海量铺词、ASIN、类目、SP 到 SB/SD 扩展排列。它给出了许多固定数值和操作组合（如 `0.02`、`0.2`、平均 CPC 比例、TOS `900%`、每活动 `$5`、`30%` 价格筛选、`1000` 美元历史花费），但没有提供对应账户的时间段、站点、类目、曝光、点击、订单、CPC、ACOS、TACOS、利润或对照组。

因此，这份材料的“玩法”是作者建议/假设，不是来源忠实的账户案例。`data/processed/amazon_ads_skill/30_ad_tactics_cases_input_2026-08-19.jsonl` 经校验为 0 条案例；后续相关回答必须写 `是否命中上传案例：未命中具体案例`，不能把玩法标题、适用场景或固定数字改写成已验证案例。

## 交叉审查结论

- `T30-CLM-001`：独立活动承载探索目标为 `context_dependent`。其价值是隔离学习与成本，不意味着所有账户都应新增活动。
- `T30-CLM-002`：平均 CPC 0.4–0.5 倍、0.02/0.2 起始竞价及 TOS 900% 为 `unsupported`。Amazon 官方资料确认自动/固定/动态竞价和展示位调整是可用机制，但没有支持这些固定阈值；需要账户级、可回滚测试。
- `T30-CLM-003`：SP 自动投放四组的存在可由当前 Amazon Ads 文档核对；材料主张“全开/先开两组”的选择为 `context_dependent`，不能把机制存在误写成全开策略已证明。
- `T30-CLM-004`：从搜索词报告把已出单的词或 ASIN 迁入手动投放是 `context_dependent` 候选迁移思路。必须核对相关性、样本、利润和迁移增量。
- `T30-CLM-005`：对无订单词“铺开增投”与“及时止损”是 `disputed`。项目既有冲突框架要求先区分样本不足、转化滞后、目标和相关性，不能只按“有无订单”执行。
- `T30-CLM-006`：品牌、错拼、外语、人工词根或海铺词“不用筛相关性”的主张为 `unsupported`。Amazon Ads 当前政策要求关键词/目标商品与被推广产品相关；不得将该说法作为执行方案。
- `T30-CLM-007`：将 SP 高表现关键词/ASIN 扩展到 SB/SD 为 `context_dependent`。先核对账户资格、当前控制台、创意/落地页、商品相关性、归因和预算竞争；不得复用文中的固定 0.2 出价。

平台机制核对日期为 2026-08-19，使用的 Amazon Ads 一手资料为《Best practices for your Sponsored Products ads》、《Guide to dynamic bidding - up and down with Sponsored Products》、《What is Keyword Targeting?》及《Sponsored Brands and display ads moderation》。它们用于验证当前可用的自动投放组、竞价策略、报告迁移思路、产品/关键词相关性要求和 SB/SD 定向范围；不为本 PDF 的因果效果、数值阈值或作者方法背书。

## 后续回答契约

命中本资料时，按 `结论 → 资料背景 → 是否命中上传案例 → 结论理由 → 来源状态/适用边界` 回答，并至少说明：

1. 实际命中的 PDF 页码、`T30-CLM-*` 或 OCR 位置；
2. 它是作者建议、来源观察还是来源忠实案例；本资料没有账户案例时明确写“未命中具体案例”；
3. 固定数值、旧界面词或机制性结论的状态，以及需要的账户数据；
4. 若用户要求当前广告动作，先加载 `references/25_skill_first_decision_gate.md` 与对应业务 reference，并在需要当前市场/竞品数据时遵守 `references/24_live_market_data_mcp_decision_gate.md`。

## 相关产物与验证

- 单来源清单/主张/报告：`assets/knowledge/source_manifest_30_ad_tactics_2026-08-19.jsonl`、`claim_review_30_ad_tactics_2026-08-19.jsonl`、`source_validation_report_30_ad_tactics_2026-08-19.md`。
- 单来源审查状态为 `PARTIAL`：8 条主张契约通过、0 条来源案例、原 PDF 由默认清单器标记为二进制不可读；这不是未阅读，也不表示 8 条主张已被证实。
- 当前便携范围为 109 个来源。`portable_109_source_manifest_2026-08-19.jsonl` 与 `full_content_coverage_109_2026-08-19.jsonl` 为 109/109 `available_with_source_boundaries`；新 PDF 的逐页 OCR 已在审计中定位。案例背景索引仍为 48 条，因为本来源没有可保留的账户案例。
