# 2026-08-13 进阶广告诊断讲义整合交接

## 任务

完整阅读并学习 `C:\Users\liuya\Downloads\亚马逊进阶广告诊断优化全指导-文字改述版.docx`，与项目语料和当前 Amazon 官方资料交叉验证，将可用规则、条件化观点、未决观点和案例纳入 skill，并在后续相关问题中主动提示。

## 阅读证据

- 文件 SHA-256：`142418a3961cc5bdcd175ef5d16000c5907070ea339df93a5597b3c774707261`
- 解析方式：OOXML 读取全部非空段落和表格；57 个段落、22 个表格，8,870 个非空字符；无图片媒体。
- 来源 ID：`SRC-ceb5e990430e`。
- 自动来源清单将 DOCX 标为 `readable=false`（扩展名限制），因此报告保留该限制；本轮实际已完成结构化全文阅读，不能把自动脚本的可读状态改写成平台事实核验。

## 产物

- `data/processed/amazon_ads_skill/source_manifest_advanced_ads_review.jsonl`
- `data/processed/amazon_ads_skill/advanced_ads_claims.jsonl`（21 条原子主张）
- `data/processed/amazon_ads_skill/claim_review_advanced_ads.jsonl`
- `data/processed/amazon_ads_skill/source_validation_advanced_ads_report.md`（`PARTIAL`）
- `data/processed/amazon_ads_skill/lecture_case_library_advanced_ads.jsonl`（4 个 `CASE-ADV-*` 案例）
- `.agents/skills/amazon-ads-keyword-strategy/references/17_advanced_ads_diagnosis_integration.md`
- 更新 `.agents/skills/amazon-ads-keyword-strategy/references/09_case_library.md`
- 更新 `SKILL.md`、README、T048 eval、`docs/CODEX_HANDOFF.md`

## 关键判断

- 支持：先诊断再优化、ACOS/TACOS/ROAS 定义、组合报告诊断、分层关键词库、匹配类型基础语义、案例作为相似性锚点。
- 条件化：30% 毛利粗筛、20/100 点击、变体拆分、分时投放、测试/盈利/清库存阶段、ABA/POE/前台选词方法、预算与在线时长关系。
- 未支持/未决：库存 1.5/3 个月、广告位 +20%/整体 −10%、2–6 个月测试期、固定 4–8 周/7 天窗口、约75%相似和 BSR Top20–100 的跨账户通用性。
- 没有主张仅因证据不足就判为 `confirmed_error`。

## 后续使用协议

当用户问到坐垫四 SKU、20/100 点击、库存月数、广告位比例、测试周期或相似漏斗问题时，必须先输出：

`讲义案例提示：来源 SRC-ceb5e990430e，状态为……；以下为案例/条件化参考，不是通用阈值。`

随后列出匹配指标、不匹配指标、缺失数据、保守路线、积极测试路线、成功标准和停止标准。不要把 `CASE-ADV-*` 直接写入 `merged_rules.jsonl` 的无条件规则。

## 验证状态

已运行：来源清单、21 条 claim 契约审查、JSONL 结构检查。覆盖状态为 `PARTIAL`，未运行模型级 eval runner；需在后续补充更多资料或账户数据后重新审查相关 claim。
