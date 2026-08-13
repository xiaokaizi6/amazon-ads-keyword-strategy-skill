# 23. 进阶广告诊断 PDF 现场复核（2026-08-13）

## 现场范围

本轮直接复核来源：

- `SRC-3a9e4ddd5371`
- `C:/Users/liuya/Downloads/亚马逊专题课-进阶广告诊断有优化全指导.pdf`
- SHA-256：`3f75d0ed42cf8fd7e8818fa82beaf57d9d593cd01753a30b141e87054b7e86df`
- 143 页，使用 `pdftoppm -r 120 -png` 全量渲染并逐页检查。

该 PDF 是图片型文件，默认文本读取器报告 `readable:false`；这只表示机器文本层不可读，不表示页面没有被人工阅读。本轮现场人工复核覆盖 143/143 页，主张和案例分别写入：

- `data/processed/amazon_ads_skill/advanced_ads_pdf_live_claims_2026-08-13.jsonl`
- `data/processed/amazon_ads_skill/claim_review_advanced_ads_pdf_live_2026-08-13.jsonl`
- `data/processed/amazon_ads_skill/source_case_records_advanced_ads_pdf_live_2026-08-13.jsonl`
- `data/processed/amazon_ads_skill/source_validation_report_advanced_ads_pdf_live_2026-08-13.md`

## 新增内容与状态

本轮新增 18 条 PDF 专属原子主张和 4 条来源忠实案例。它们是“现场 PDF 审计层”，不替代同课 DOCX 改写，也不与同一 `evidence_cluster` 的来源重复计票。

| 范围 | 现场纳入内容 | 状态边界 |
|---|---|---|
| 报告矩阵 | 商品、购买商品、投放、搜索词展示份额、搜索词、广告位、广告活动、预算的联动诊断 | `context_dependent`；字段和回溯窗口按站点复核 |
| 聚合与公式 | 父 ASIN/多变体先汇总分子分母；ACOS = CPC ÷ (CVR × ASP) | 数学部分 `supported`；账户口径仍需一致 |
| 自动/商品投放 | 四类自动定向、商品/类目可比性检查 | 四类功能获 Amazon 官方支持；可比性为 `context_dependent` |
| 搜索词与特征词 | 展示份额诊断、词根拆分聚合 | 方法保留；不能把词根或份额直接当作提价充分条件 |
| 否词 | `1/CR`、`10/CR` 估算与 20/100 点击示例 | 估算可用；固定阈值为 `context_dependent`，完全不相关词和相关低效词分开处理 |
| 广告位/预算/时段 | 广告位、预算利用率、小时切片 | 可做诊断维度；不能把课程百分比和单小时结果升级成规则 |
| 关键词研究 | BSR/ABA/POE/前台多源验证 | 工具用途获官方支持；BSR Top20-100、100 ASIN 和属性练习是方法参数 |
| 相似度练习 | “75% 搜索结果相似度” | `unsupported` 的通用平台阈值；只能作为待验证启发式 |
| 变体/匹配类型 | 延迟拆分变体；Broad/Phrase/Exact 按目标分工 | `context_dependent`；当前匹配扩展和控制台需复核 |
| 生命周期 | 测试、盈利、季节、清库存和 PDCA | 框架保留；两周、四轮、旺季前两周、5%-30%、约六个月等为示例参数 |
| 案例与宣传页 | 四 SKU 座垫、特征词、核心词研究、生命周期案例 | 4 条 `case_observation` 单独保存；培训/二维码页是来源边界，不进入规则 |

## 交叉验证结论

1. 同课两份 DOCX 改写与本 PDF 属于同一证据家族；它们可以帮助定位页面和还原表格，但不能被当作三份独立支持。
2. Amazon 官方资料确认 Sponsored Products 自动定向的 Close match、Loose match、Substitutes、Complements 四类策略，并确认搜索词/展示份额和 Product Opportunity Explorer 等工具的当前用途。
3. PDF 的 2025-05 广告位/受众界面是历史快照。当前 Amazon 文档的广告位、浏览位置、受众及组合调整范围更广，执行前必须看当前控制台；PDF 不能作为当前 UI 事实的唯一依据。
4. Product Opportunity Explorer 官方说明其用于需求、趋势、竞争、搜索词和细分洞察，并不保证结果。因此 75% 搜索结果相似度不能升级为 Amazon 通用准入线。
5. `1/CR` 和 `10/CR` 是期望点击量的数学估算；20 点击精准否定、100 点击词组否定、最低 5/50 等属于课程经验参数。动作必须结合相关性、阶段、目标、归因延迟和样本量。
6. 阶段化和 PDCA 可以作为流程框架，但课程给出的两周/四轮、旺季前两周、预算增幅和清库存月数不能跨类目直接套用。

## 回答时的使用边界

当问题命中 `PDFLIVE-CLM-*` 或四条 `SRC-3a9e4ddd5371-CASE-*` 时，必须显示“讲义案例提示”，至少说明：

- PDF 页码、claim/case ID 和状态；
- 哪些是来源观察，哪些只是课程解释；
- 当前账户与案例的匹配条件和关键不匹配；
- 保守路线、备选路线、缺失数据和可逆验证窗口；
- 当前 Amazon UI/政策必须重新核对的部分。

不要把 `unsupported`、`outdated` 或 `context_dependent` 内容静默写入 `merged_rules.jsonl` 的无条件规则。案例可以用于相似性提示，但不能证明平台因果。

