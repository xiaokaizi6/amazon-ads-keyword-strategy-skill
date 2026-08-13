# 21. 争议与不确定主张保留登记

## 强制规则

用户资料中的 `disputed`、`unresolved`、`unsupported`、`outdated` 和 `context_dependent` 内容必须保留在 Skill 的条件化知识层，并明确标记。不得因为它们不能直接成为通用规则而删除、改写成确定结论或从案例记录中移除。

保留位置：

- 原子主张：`data/processed/amazon_ads_skill/*claim*.jsonl` 或对应批次 claim 文件；
- 来源忠实案例：`data/processed/amazon_ads_skill/*case*.jsonl`；
- 可读的人工使用说明：`references/16_*` 至 `references/21_*`、`references/09_case_library.md`；
- 覆盖状态：对应 `source_validation_report*.md`。

`merged_rules.jsonl` 只接收满足规则契约的条件化 executable rule；保留在 claim/case 层不等于升级为默认动作。

## 状态使用

| 状态 | 必须保留的内容 | 后续回答方式 |
|---|---|---|
| `disputed` | View A、View B、证据、冲突原因和置信度 | 同时展示不同路线，不给唯一结论。 |
| `unresolved` | 当前无法判断的原因、缺失数据和验证测试 | 作为诊断假设，不称为平台事实。 |
| `unsupported` | 来源原说法、没有找到的支持、风险和边界 | 不作为默认建议；可作为备选实验假设。 |
| `outdated` | 原时间点说法、失效原因和当前复核入口 | 只作历史参考，执行前重新查官方控制台。 |
| `context_dependent` | 阶段、站点、类目、目标、毛利、预算和样本条件 | 只有条件匹配才可使用，并给可逆窗口。 |

## 当前批次登记

以下是 2026-08-13 批次中已经保留的代表性主张；完整字段以 claim review JSONL 为准：

- `PRC-CLM-002`：固定“10 单/一周/日均15单/六个月”形成划线价，`unsupported`。
- `PRC-CLM-004`、`PROM-CLM-002`、`PROM-CLM-004`：Deal/Prime/Typical Price/费用/窗口等时效字段，`outdated`。
- `PROM-CLM-001`、`PROM-CLM-003`、`NEW-CLM-001`、`NEW-CLM-003`、`ADREP-CLM-004`、`ADREP-CLM-005`：促销叠加、新品参数、否词、Placement 和 Purchased Product，`context_dependent`。
- `NEW-CLM-002`、`NEW-CLM-007`、`ADREP-CLM-003`、`ADREP-CLM-006`：ACOS50%、SD 竞价公式、TOS+900%、70%在线等，`unsupported`。
- `ADREP-CLM-002`：精准词/广告类型与自然排名因果，`disputed`。

更早批次的 `ADV2-CLM-002` 等 `unresolved` 主张，以及 `CASE-ADV-*` 和 `SRC-3328e6e7662e-CASE-*` 案例继续保留，不能因本次新增资料而覆盖或删除。

## 触发提示

用户问题命中上述主张或案例时，回答必须出现 `讲义案例提示`，并至少说明：

1. 来源 ID、原文位置和状态；
2. 与当前问题匹配的条件与关键不匹配；
3. 支持路线、保守路线或不可执行原因；
4. 缺失数据、成功标准、停止标准和可逆验证窗口。

安全/政策类 `confirmed_error` 仍然保留原主张和案例，但只能说明禁止边界与合规替代，不能提供优化、规避检测或扩大违规效果的步骤。
