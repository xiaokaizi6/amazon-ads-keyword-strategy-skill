# Amazon Ads & Keyword Strategy Skill 使用说明

这个 skill 用于诊断 Amazon 广告、关键词策略、搜索词优化、自然排名推动、竞品 ASIN 投放、ACOS/TACOS 异常、广告单占比过高、低 ACOS 但排名不涨等问题。

它的核心原则是：不要给泛泛建议，不要只看 ACOS，所有结论都必须结合产品阶段、广告目标、样本量、TACOS、CVR、CTR、CPC、广告单占比、自然排名和预算约束来判断。

## 目录位置

```text
.agents/skills/amazon-ads-keyword-strategy/
|-- SKILL.md
|-- README.md
|-- examples/
|-- references/
|-- scripts/
`-- evals/
```

## 什么时候使用

当用户的问题涉及以下场景时，使用这个 skill：

- Amazon PPC 广告诊断
- 系统建立和更新关键词库
- 搜索词报告优化
- 关键词分类和排名计划
- ACOS、TACOS、CPC、CVR、CTR 诊断
- 广告单占比和自然单占比判断
- 新品期、成长期、成熟期、清货期广告策略
- 竞品 ASIN 定向和防守广告
- 广告出单但自然排名不涨
- 低 ACOS 看起来好，但总表现或排名弱

## 建议输入

为了给出可靠建议，尽量提供以下信息：

- 产品阶段：新品、成长、成熟、衰退、清货、季节性
- 站点和类目
- 售价、毛利率、可接受 ACOS
- 当前广告目标：盈利、冲排名、测词、防守、清库存、季节性抢量
- 预算、花费、订单量、销售额
- 搜索词报告或广告活动数据
- 关键词库来源：手动种子词、产品 listing、竞品反查、广告搜索词、ABA/SQP、Keepa、亚马逊前台词、文章和评论信号
- 目标关键词和当前自然排名
- 广告类型、匹配类型、投放位置
- CTR、CVR、CPC、ACOS、TACOS
- 广告单占比、自然单占比
- 库存压力和促销计划

如果数据不完整，先做数据完整性检查，并把缺失项标成诊断问题，不要直接下最终结论。

## 标准输出结构

使用这个 skill 输出诊断时，必须保持以下结构：

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

## 使用参考资料

详细规则拆在 `references/` 目录中。按任务需要读取对应文件，不需要一次性加载全部内容。

- `01_taxonomy.md`: 记录类型、主题、置信度和噪音分类
- `02_extraction_schema.md`: JSONL 提取结构和校验规则
- `03_keyword_classification.md`: 关键词角色和动作
- `04_campaign_structure.md`: 不同阶段的广告结构
- `05_search_term_optimization.md`: 搜索词动作和样本量逻辑
- `06_product_stage_strategy.md`: 产品阶段策略
- `07_conflict_register.md`: 冲突观点的条件化处理
- `08_metric_thresholds.md`: 指标解释和阈值限制
- `09_case_library.md`: 案例锚点和相似性判断
- `10_noise_filter_rules.md`: 评论和噪音过滤
- `11_source_index.md`: 来源集群和已处理数据索引
- `12_keyword_library_building.md`: 关键词库建立流程、子库、状态、更新节奏和广告结构分配
- `13_keyword_database_schema.md`: `keyword_library.jsonl` 字段、枚举值、指标对象和更新规则

## 关键词库模块

新增模块用于生成和维护结构化关键词库，不只是关键词列表。

默认输出：

```text
data/processed/amazon_ads_skill/keyword_library.jsonl
data/processed/amazon_ads_skill/keyword_library.csv
data/processed/amazon_ads_skill/keyword_library_report.md
```

核心脚本：

- `scripts/build_keyword_library.py`: 从多个来源构建关键词库，去重、标准化、分类、评分并输出 JSONL/CSV/报告。
- `scripts/classify_keywords.py`: 根据关键词文本、来源、指标和产品阶段判断类型、优先级、风险标签和状态。
- `scripts/update_keyword_library_from_ads.py`: 根据广告搜索词报告更新关键词状态和否定候选。

关键词库必须区分：

- 初始种子词库
- 核心词库
- 长尾词库
- 竞品词库
- 广告搜索词挖掘库
- 自然排名目标词库
- 已验证转化词库
- 否定词库
- 季节词库
- 风险词库

## 示例文件

`examples/` 目录提供输入和输出样例：

- `example_input_search_term_report.md`
- `example_output_ads_diagnosis.md`
- `example_output_case_diagnosis.md`
- `example_output_keyword_strategy.md`

参考示例时，只把它当作格式和判断方式的样例，不要把示例中的结论直接套到新案例。

## 维护规则

- `SKILL.md` 保持为 agent 执行规则的主入口。
- `README.md` 只写给人看的使用说明，不承载新的业务判断规则。
- 新增可执行判断规则时，优先放入 `SKILL.md` 或对应 `references/` 文件。
- 新增案例时，放入案例库或结构化数据，不要把案例改写成通用规则。
- 新增评论区观点时，先分类为 `diagnostic_hypothesis`、`counterexample`、`comment_signal` 或 `irrelevant_noise`。
- 新增关键词库规则时，优先更新 `references/12_keyword_library_building.md` 和 `references/13_keyword_database_schema.md`。
- 冲突观点必须进入条件化判断，不要声明单边观点永远正确。

## 快速检查清单

交付诊断前检查：

- 是否说明了产品阶段和广告目标
- 是否检查了 TACOS、CVR、CTR、CPC、广告单占比和自然排名
- 是否根据样本量决定搜索词动作
- 是否区分了案例、规则、评论信号和噪音
- 是否避免把低 ACOS 或高 ACOS 直接等同于好坏
- 是否区分了出单词和自然排名目标词
- 如果建立关键词库，是否包含来源、类型、状态、指标、优先级和风险标签
- 是否给出了 7 天、14 天、30 天行动计划
- 是否标明置信度和缺失数据
