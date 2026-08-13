# 2026-08-13 新增定价、促销、新品与图片广告报告资料交接

## 任务目标

完整阅读用户提供的 5 个文件，和项目已有 raw/processed 资料、现有 Skill 规则/案例/冲突登记以及当前 Amazon 官方资料交叉验证；保留来源案例，区分可用规则、条件性观点、证据不足、过时数字、真实冲突和政策错误，并让后续相关问答主动提示。

## 实际完成

- 识别课程文字整理版 `SRC-3328e6e7662e` 为之前已处理的同一 PDF 证据家族，未重复计票；其现有 22 条 claim、6 条案例继续有效。
- 完整读取并核对 `SRC-d9b87550b32a` 新品流程工作簿两个 sheet。
- 完整读取并核对 `SRC-f564d5134e68` 划线价 DOCX 的正文和 11 张图片。
- 完整读取并核对 `SRC-2c0a32e82d29` 折扣/促销工作簿 4 个 sheet、公式和显示值。
- 完整逐张检查 `SRC-3d7548bc16d9` 图片版广告报告 12 张图片；由于 DOCX 无正文，自动来源清单保持 `readable:false`。
- 新增 22 条原子主张和 11 条来源忠实案例，并运行来源审查脚本；案例契约和主张契约无错误，整体覆盖状态 `PARTIAL`。
- 将结果纳入 `references/19_pricing_promotion_launch_integration.md`、`references/20_image_ad_report_integration.md`、`references/09_case_library.md`、`references/11_source_index.md`、`SKILL.md`、`README.md` 与 T051/T052 eval。

## 关键判断

- List Price/参考价必须按当前 Amazon 验证条件和真实近期市场/Amazon 销售依据处理；“10单/一周/日均15单/稳定六个月”不是已验证平台阈值。
- 关联店铺、朋友账户、跟卖、自买、刷单造高价参考、返佣评价、review club、刷加购/心愿单和人为流量/排名信号均标为 `confirmed_error` 或政策风险证据，不得执行。
- 促销叠加、Coupon/Deal/Prime 资格、费用、窗口和折扣比例标为 `context_dependent` 或 `outdated`；工作簿公式只能在基准价/顺序/税费/结算验证后使用。
- 新品 20%-25% 毛利、5% Coupon、10-20 美元预算、ACOS50% 和 `Price×ACOS×CR` 公式未升级为通用规则。
- 图片广告报告中的精准词排名因果、TOS +900%、50%-60% ACOS、+10%-20% placement、70%在线时长均保留为条件性/争议/未支持观点；Placement 和 Purchased Product 案例只用于提出诊断假设。

## 产物

- `data/processed/amazon_ads_skill/source_manifest_2026-08-13_new_bundle.jsonl`
- `data/processed/amazon_ads_skill/new_source_bundle_claims.jsonl`
- `data/processed/amazon_ads_skill/new_source_bundle_claim_review.jsonl`
- `data/processed/amazon_ads_skill/new_source_bundle_cases.jsonl`
- `data/processed/amazon_ads_skill/new_source_bundle_case_records.jsonl`
- `data/processed/amazon_ads_skill/source_validation_report_2026-08-13_new_bundle.md`
- `references/19_pricing_promotion_launch_integration.md`
- `references/20_image_ad_report_integration.md`

## 验证命令和真实结果

- `python .agents/skills/amazon-ads-keyword-strategy/scripts/review_sources.py ... --claims-file ... --cases-file ...`：成功；22 条 claim、11 条案例，契约错误 0，报告 `PARTIAL`。
- Python 标准库 JSONL 解析：成功，claims/cases 均可解析。
- `git diff --check`：通过（无 whitespace 错误）。
- `python .agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py`：通过，报告 `PASS`，0 errors/0 warnings。
- `python C:\Users\liuya\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/amazon-ads-keyword-strategy`：通过，输出 `Skill is valid!`。

## 遗留风险与下一步

- 自动 manifest 对 DOCX/XLSX 仍标记不可读；这是脚本可读性限制，不代表人工未读。若要将覆盖提升到 `PASS`，需扩展 manifest 的 OOXML/XLSX 可读性适配，并把全项目相关来源作为同一批 claims 输入。
- Seller Central 帮助页部分需登录；价格和促销执行前必须在目标站点当前控制台复核。
- 后续问题一旦涉及划线价、刷单/评价、促销逆算、TOS 100%-200%/900%、精准词排名或低 ACOS 加预算，必须先显示 `讲义案例提示`、来源状态、案例置信度、匹配条件、不匹配、合规路线和可逆测试。
- 不自动修改原始上传文件，不自动 commit/push。
