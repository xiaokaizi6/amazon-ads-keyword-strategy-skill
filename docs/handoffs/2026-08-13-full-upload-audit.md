# 2026-08-13 对话上传资料总审计

## 结论口径

本次对话上传资料的决策相关内容已经阅读、拆分、交叉验证并纳入 Skill；但“完整阅读”不等于“每条经验都被官方证明”，也不等于“原文件逐字复制进 SKILL.md”。原始文件仍保留在用户 Downloads 路径，项目保存的是哈希、主张、案例、状态、证据边界和可读参考层。

## 文件覆盖

| 文件 | 阅读状态 | 纳入状态 | 主要产物/说明 |
|---|---|---|---|
| `亚马逊CPC广告打法知识体系全梳理v1_20260804(1).docx` | 完整 OOXML 段落、表格、附录阅读；无媒体 | 已纳入 21 条 claim；状态为 supported/context-dependent/disputed/unresolved/unsupported | `cpc_playbook_claims.jsonl`、`claim_review_cpc_playbook.jsonl`、`references/16_cpc_playbook_integration.md` |
| `亚马逊进阶广告诊断优化全指导-文字改述版.docx` | 完整文本、表格和 seat-cushion 四 SKU 案例阅读 | 已纳入 21 条 claim、4 条案例；未升级固定阈值为通用规则 | `advanced_ads_claims.jsonl`、`lecture_case_library_advanced_ads.jsonl`、`references/17_*` |
| `亚马逊专题课-进阶广告诊断有优化全指导-文字整理版 (1).docx` | 完整 OOXML 阅读，26 个表格；与同课程整理来源按证据家族处理 | 已纳入 22 条 claim、6 条案例；不重复计权 | `advanced_ads_rewrite_v2_claims.jsonl`、`source_case_records_advanced_ads_rewrite_v2.jsonl`、`references/18_*` |
| `新品推广基础推广动作及流程(1).xlsx` | 两个工作表逐格读取 | 已纳入 7 条 claim、3 条案例；刷单/评价/刷行为标记 `confirmed_error` 或政策风险 | `new_source_bundle_claim_review.jsonl`、`new_source_bundle_case_records.jsonl`、`references/19_*` |
| `2025亚马逊划线价运营玩法.docx` | 正文和 11 张图片逐张检查 | 已纳入 5 条 claim、2 条案例；虚构参考价方案禁止执行 | 同上，`SRC-f564d5134e68` |
| `亚马逊折扣+促销说明.xlsx` | 4 个工作表、公式和显示值读取 | 已纳入 4 条 claim、2 条案例；叠加公式与活动数字条件化/过时标记 | 同上，`SRC-2c0a32e82d29` |
| `亚马逊广告报告高效分析和优化-Word版 (1).docx` | 无正文；12 张图片逐张视觉检查 | 已纳入 6 条 claim、4 条案例；TOS/排名因果/预算阈值保留但不默认执行 | `references/20_image_ad_report_integration.md`、`SRC-3d7548bc16d9` |

## 状态汇总

- CPC 讲义：21 条 claim；`supported` 13、`context_dependent` 1、`disputed` 1、`unresolved` 5、`unsupported` 1。
- 第一份进阶诊断讲义：21 条 claim；`supported` 9、`context_dependent` 8、`unresolved` 2、`unsupported` 2；4 条案例。
- 同课程详细整理版：22 条 claim；`supported` 7、`context_dependent` 11、`unresolved` 2、`unsupported` 2；6 条案例。
- 新增定价/促销/新品/图片报告批次：22 条 claim；`supported` 1、`context_dependent` 8、`disputed` 1、`unresolved` 0、`unsupported` 5、`outdated` 3、`confirmed_error` 4；11 条案例。

所有不确定状态均保留在 claim/case/reference 层，统一规则见 `references/21_disputed_uncertain_claim_retention.md`。

## 交叉验证结论

### 可作为基础方法使用

- ACOS/ROAS 等定义、父子体先聚合分子分母再重算比例、广告诊断先看漏斗和目标、自动/手动/否定投放的基本结构、按报告拆分 Placement/Purchased Product/搜索词等。
- 这些也仍需匹配归因窗口、marketplace、广告产品和账户字段。

### 条件化保留

- 20/100 点击、库存月数、2 倍毛利率、ACOS 50%/60%、预算 70% 在线、+10%-20% Placement、促销叠加公式、新品预算/竞价倍数、`Price×ACOS×CR`。
- 这些只能作为来源假设或限时实验起点，不能作为 Amazon 通用阈值。

### 争议保留

- 精准关键词是否比 SB/SD 更能推动自然排名、广告位与自然排名的因果关系、Purchased Product 后是否应直接改投购买 ASIN。
- 回答时必须同时给出支持路线、保守路线、匹配条件、关键不匹配和验证窗口。

### 已判定不可执行/错误

- 虚假订单、自买、关联店铺或朋友账户制造参考价、评价返佣/退款/赠品、review club、刷加购/心愿单、第三方人为流量和排名操纵。
- 这些内容保留为风险案例和反证，不提供优化或规避检测步骤。Amazon 当前公开政策明确禁止评价补偿、虚假订单、销售排名操纵和人为流量。[评价政策](https://sellercentral.amazon.com/seller-forums/discussions/t/9fab2fc9-b7dd-44b1-924c-77fb87462ac8)、[销售排名/流量操纵政策](https://sellercentral.amazon.com/seller-forums/discussions/t/364ee6ee7f10c568a5c0959cfec596e3)

### 当前平台事实需复核

- List Price、Typical Price、Deal/Prime Discount 的资格、最低价窗口、费用、折扣比例和活动时长。
- Amazon 2026 参考价更新显示，List Price 验证与近期其他零售商价格或 Amazon Featured Offer 购买记录有关，Typical Price 口径也发生变化；因此讲义固定订单数和固定天数不能直接沿用。[Reference pricing update](https://sellercentral.amazon.com/seller-forums/discussions/t/f48a1fe5-aa8e-4806-b687-2d9aeec5c351)

## 未能声称为完全确定的部分

1. 自动来源审查器对 DOCX/XLSX/PDF 标记 `readable:false`；这是脚本扩展名限制，人工已阅读，但不能把自动覆盖写成 `PASS`。
2. 批次报告为 `PARTIAL`，因为没有把 100 篇项目文章与所有新资料的每条 claim 在同一批次重新逐条审查。
3. Seller Central 部分帮助页需要登录；账户级活动资格、费用和界面字段仍需在目标 marketplace 当前控制台复核。
4. 图片版资料的图片已检查，但原图中的小字、截图上下文和缺失分母不能被推断成完整实验数据。

## 后续回答规则

凡问题命中上述资料，必须显示 `讲义案例提示`，包括 source ID/claim ID 或 case ID、状态、案例置信度、匹配条件、关键差异、合规边界、缺失数据和可逆验证窗口。
