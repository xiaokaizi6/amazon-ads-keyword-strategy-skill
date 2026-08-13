# 19. 新增定价、促销与新品资料的交叉验证层

本文件把 2026-08-13 收到的三类新增资料纳入 Skill：

| 来源 | 稳定 ID | SHA-256 | 读取方式 | 证据簇 |
|---|---|---|---|---|
| `2025亚马逊划线价运营玩法.docx` | `SRC-f564d5134e68` | `b3628e229d3fd1cb2f3244117de4e134cc0e6c4fc26f7b48d9631de536911dd1` | DOCX OOXML 文本 + 11 张图片逐张检查 | `EC-b3628e229d3f` |
| `亚马逊折扣+促销说明.xlsx` | `SRC-2c0a32e82d29` | `7682d3dc8693f547676bdcadc840a79a59088d73bf4a2490a302895aa5ad40aa` | 4 个工作表、公式和显示值逐格读取 | `EC-7682d3dc8693` |
| `新品推广基础推广动作及流程(1).xlsx` | `SRC-d9b87550b32a` | `a05f577e2111fadcbf2bcfb5da0d2b3bcc0261cac55e6a0dbfef7b3008c3286b` | 2 个工作表逐格读取 | `EC-a05f577e2111` |

原件仍在用户提供的 Downloads 路径，未被改写。来源清单、原子主张审查和来源忠实案例记录见：

- `data/processed/amazon_ads_skill/source_manifest_2026-08-13_new_bundle.jsonl`
- `data/processed/amazon_ads_skill/new_source_bundle_claim_review.jsonl`
- `data/processed/amazon_ads_skill/new_source_bundle_case_records.jsonl`
- `data/processed/amazon_ads_skill/source_validation_report_2026-08-13_new_bundle.md`

## 1. 可纳入的共同方法

- 划线价/参考价、Coupon、Deal、Prime Discount 和 Sale Price 必须拆成不同字段处理；先核对目标 marketplace、当前控制台定义、价格历史、利润和活动 eligibility。
- 促销工作簿可用于演算折扣基数、叠加顺序和利润敏感性，但表内标注“冲突”的组合不能被自动合并；最终成交价必须用当前结算页或订单明细回算。
- 新品广告可以拆成自动发现、手动词验证、商品/类目拓展和利润控制等目标，但预算、竞价倍数、Coupon 百分比和 ACOS 线只能作为可逆测试起点。
- 否定词以相关性和样本量为先：完全不相关可即时排除；相关词应结合点击量、转化延迟、目标和损失上限，不能仅按“每两天”机械操作。
- 真实站外引流、合规 Coupon/Promotion、Amazon Vine（符合资格）和 Request a Review 可作为合规替代；评价请求不能与补偿、退款、赠品或正向评价绑定。

## 2. 状态化结论

| 主张范围 | 状态 | 如何使用 |
|---|---|---|
| List Price/参考价需要真实且可验证的近期市场或 Amazon 销售依据 | `supported`，高时效 | 可以作为价格诊断前提；每次执行前重查当前参考价政策和验证状态。 |
| “10 单/一周/日均15单/稳定六个月”可形成划线价 | `unsupported`，低置信度 | 只保留为历史经验；不得当作硬阈值。 |
| 通过关联店铺、朋友账户、跟卖或自买制造高参考价 | `confirmed_error` | 不得执行；改为真实成交、合规 Deal/Coupon 和价格历史审计。 |
| 30 天最低价、Typical Price、Deal 时长/费用、Prime 活动折扣 | `outdated` 或 `context_dependent` | 仅作历史注释；以当年、当站点 Seller Central eligibility 为准。 |
| none/group 促销叠加与工作簿公式 | `context_dependent` | 只在折扣基准、顺序、税费、运费和组合资格都确认后使用；先做结算测试。 |
| 新品毛利20%-25%、Coupon5%、预算10-20美元、ACOS50% | `context_dependent`/`unsupported` | 只能作为实验假设；必须用单位经济、库存、目标、CPC、CVR、TACOS和自然订单校准。 |
| 每两天否词 | `context_dependent` | 相关词等样本量，完全不相关可即时否定；保留可逆回滚。 |
| 刷单、评价返佣、第三方 review club、刷加购/心愿单、关联账户合并 | `confirmed_error` | 只作为风险证据留档；不得给出执行步骤。 |
| `Bid=Price×ACOS×CR` | `unsupported` | 不是官方 SD 公式；若研究只能作为账户内假设，按成本上限/利润回测。 |

官方核验入口（核验日期 2026-08-13）：[Amazon reference pricing update](https://sellercentral.amazon.com/seller-forums/discussions/t/f48a1fe5-aa8e-4806-b687-2d9aeec5c351)、[List Price 说明](https://sellercentral.amazon.com/seller-forums/discussions/t/4ac59442-db7d-4278-bf43-476dad64693b)、[Prime/Deal 活动说明](https://sellercentral.amazon.com/help/hub/reference/external/GM2ADTH3XH3A5N57)、[Amazon 评价政策摘录](https://sellercentral.amazon.com/seller-forums/discussions/t/b9781879bc69115e3993d8e30de88327)、[Amazon 销售/排名操纵政策摘录](https://sellercentral.amazon.com/seller-forums/discussions/t/364ee6ee7f10c568a5c0959cfec596e3)。Seller Central 帮助页可能要求登录，执行时应以账户当前页面为准。

## 3. 必须主动提示的案例

以下案例仅是来源观察，不是通用规则：

- `SRC-f564d5134e68-CASE-001/002`：高 List Price 与固定订单阈值的划线价经验，均为低置信度；只要问题提到“刷参考价、朋友店铺、10 单/一周”，必须显示“讲义案例提示：政策风险/未验证”，并明确不可执行。
- `SRC-2c0a32e82d29-CASE-001/002`：促销叠加和会员日逆算表；回答价格时必须标明公式假设、活动日期和实际结算验证边界。
- `SRC-d9b87550b32a-CASE-001`：新品固定预算/竞价/ACOS 示例；需要同时询问利润、库存、目标和样本量。
- `SRC-d9b87550b32a-CASE-002`：评价、返佣和刷行为方案；必须标为“讲义案例提示：confirmed_error/不可执行”，并给合规替代方案。
- `SRC-d9b87550b32a-CASE-003`：SD 自定义 bid 公式；标为未支持假设，不得称为平台公式。

## 4. 回答模板

当用户询问本组内容时，先给：`来源状态`、`原始案例位置`、`匹配条件`、`关键不匹配`、`可执行/不可执行边界`。若结论是 `disputed`、`unsupported`、`outdated` 或 `context_dependent`，提供另一条合规路线和 7-14 天可逆验证窗口；若是 `confirmed_error`，不提供优化该违规动作的细节。
