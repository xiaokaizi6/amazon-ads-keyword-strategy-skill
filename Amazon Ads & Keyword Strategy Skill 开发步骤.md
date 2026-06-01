# Amazon Ads & Keyword Strategy Skill 开发步骤

## 项目信息

项目根目录：

```text
F:\CODE\Amazon Ads & Keyword Strategy Skill
```

原始文章目录：

```text
F:\CODE\Amazon Ads & Keyword Strategy Skill\data\raw\amazon_ads_articles
```

请所有脚本统一使用相对路径，不要在代码里写死 Windows 绝对路径。

正确使用：

```text
data/raw/amazon_ads_articles
data/processed/amazon_ads_skill
.agents/skills/amazon-ads-keyword-strategy
```

不要写死：

```text
F:\CODE\Amazon Ads & Keyword Strategy Skill
```

因为路径中有空格和 `&`，PowerShell 执行命令时必须加英文双引号。

进入项目根目录：

```powershell
cd "F:\CODE\Amazon Ads & Keyword Strategy Skill"
```

---

# Phase 0：项目检查，不修改文件

请先只检查项目结构，不要创建、修改、删除任何文件。

任务：

1. 确认当前工作目录是否为：

```text
F:\CODE\Amazon Ads & Keyword Strategy Skill
```

2. 检查是否存在：

```text
data/raw/amazon_ads_articles
```

3. 统计该目录下 `.md` 文件数量。
4. 随机查看 5 个 `.md` 文件。
5. 判断这些文件属于哪种结构：

   * 教程文章
   * 问题帖
   * 案例帖
   * 评论讨论帖
   * 混合帖
6. 检查是否存在以下结构：

   * 标题
   * 文章链接
   * 发布人名称
   * 发布时间
   * 站内元信息
   * 发布人正文
   * 评论区
   * 多条评论
7. 输出是否可以进入 Phase 1。

输出内容：

```text
当前工作目录：
文章目录是否存在：
.md 文件数量：
随机抽查文件：
文件结构判断：
是否可以进入 Phase 1：
```

---

# Phase 1：创建项目骨架

请创建以下目录和文件。

```text
.agents/skills/amazon-ads-keyword-strategy/
  SKILL.md
  references/
    01_taxonomy.md
    02_extraction_schema.md
    03_keyword_classification.md
    04_campaign_structure.md
    05_search_term_optimization.md
    06_product_stage_strategy.md
    07_conflict_register.md
    08_metric_thresholds.md
    09_case_library.md
    10_noise_filter_rules.md
    11_source_index.md
  scripts/
    ingest_articles.py
    split_article_sections.py
    extract_records.py
    normalize_records.py
    build_rulebooks.py
    build_case_library.py
    detect_conflicts.py
    validate_outputs.py
  examples/
    example_input_search_term_report.md
    example_output_ads_diagnosis.md
    example_output_keyword_strategy.md
    example_output_case_diagnosis.md
  evals/
    test_cases.jsonl
    expected_outputs.md
```

同时创建处理输出目录：

```text
data/processed/amazon_ads_skill/
  articles_index.jsonl
  article_sections.jsonl
  extracted_records.jsonl
  normalized_records.jsonl
  merged_rules.jsonl
  case_library.jsonl
  conflict_candidates.jsonl
  noise_comments.jsonl
  extraction_report.md
  validation_report.md
```

`SKILL.md` 先写最小版本：

```yaml
---
name: amazon-ads-keyword-strategy
description: Use this skill when analyzing Amazon advertising, keyword strategy, search term reports, competitor keyword data, Keepa trends, product lifecycle strategy, ACOS/TACOS optimization, ranking diagnosis, and launch-stage ad planning.
---
```

要求：

1. 本阶段只创建骨架，不处理文章。
2. Python 脚本先写 docstring、输入路径、输出路径、CLI 参数。
3. 所有路径用相对路径。
4. 执行：

```powershell
git status
```

但不要自动 commit。

建议 commit message：

```text
phase-1: create amazon ads skill project skeleton
```

---

# Phase 2：建立文章索引

实现脚本：

```text
.agents/skills/amazon-ads-keyword-strategy/scripts/ingest_articles.py
```

读取：

```text
data/raw/amazon_ads_articles
```

输出：

```text
data/processed/amazon_ads_skill/articles_index.jsonl
```

每篇文章输出一行 JSON：

```json
{
  "source_id": "A001",
  "file_name": "",
  "file_path": "",
  "title": "",
  "article_url": "",
  "publisher_name": "",
  "publish_date": "",
  "site_meta": "",
  "tags": [],
  "raw_reply_count": null,
  "raw_comment_count": null,
  "char_count": 0,
  "has_author_body": true,
  "has_comments": true,
  "detected_headings": [],
  "content_hash": "",
  "status": "ok",
  "error_message": ""
}
```

要求：

1. 从 Markdown 顶部尽量提取：

   * 文章链接
   * 发布人名称
   * 发布时间
   * 站内元信息
   * 圈子/标签
   * 爬取到的公开回复数
   * 爬取到的评论数
2. 用 hash 识别重复文件。
3. 空文件标记为 `empty`。
4. 重复文件标记为 `duplicate`。
5. 出错文件标记为 `error`。
6. 不修改原始 `.md` 文件。

执行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/ingest_articles.py"
```

检查前 5 行：

```powershell
Get-Content "data/processed/amazon_ads_skill/articles_index.jsonl" -TotalCount 5
```

建议 commit message：

```text
phase-2: index raw amazon ads markdown articles
```

---

# Phase 3：拆分文章结构

实现脚本：

```text
.agents/skills/amazon-ads-keyword-strategy/scripts/split_article_sections.py
```

读取：

```text
data/raw/amazon_ads_articles
data/processed/amazon_ads_skill/articles_index.jsonl
```

输出：

```text
data/processed/amazon_ads_skill/article_sections.jsonl
```

每条 section 输出：

```json
{
  "source_id": "A001",
  "file_name": "",
  "section_id": "A001-S001",
  "section_type": "author_body",
  "section_role": "author_body",
  "comment_index": null,
  "comment_author": "",
  "comment_time": "",
  "heading": "",
  "text": "",
  "char_count": 0,
  "extraction_notes": ""
}
```

`section_role` 可选值：

```text
metadata
author_body
author_update
comment
reply
unknown
```

拆分规则：

1. 顶部文章链接、发布人、发布时间、站内元信息、圈子/标签归入 `metadata`。
2. `## 发布人正文` 下的主体内容归入 `author_body`。
3. 类似 `2.25日，图片补充` 这种内容归入 `author_update`。
4. `## 评论区` 下每个 `### 评论 X` 单独拆成一条 `comment`。
5. 不要把所有评论合并成一个大块。
6. 不能丢失原文。
7. 无法判断的内容放入 `unknown`。

执行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/split_article_sections.py"
```

重点检查示例文件：

```text
017_q31734_广告关键词为何无法推动自然排名上升，广告单占比非常高.md
```

要求该文件拆出：

```text
metadata
author_body
author_update
comment 1
comment 2
comment 3
```

建议 commit message：

```text
phase-3: split posts into metadata author body updates and comments
```

---

# Phase 4：定义提取 schema

完善：

```text
.agents/skills/amazon-ads-keyword-strategy/references/01_taxonomy.md
.agents/skills/amazon-ads-keyword-strategy/references/02_extraction_schema.md
```

核心原则：

这些 `.md` 文件不能只提取“规则”，还要提取：

```text
案例数据
诊断假设
诊断问题
可执行规则
反例
评论信号
无关噪音
```

最终输出文件：

```text
data/processed/amazon_ads_skill/extracted_records.jsonl
```

每条 record 字段：

```json
{
  "record_id": "A001-R001",
  "source_id": "A001",
  "section_id": "A001-S001",
  "post_type": "case_post",
  "record_type": "case_observation",
  "section_role": "author_body",
  "is_relevant": true,
  "noise_reason": "none",
  "topic": "ranking",
  "product_stage": "stable",
  "ad_type": "Sponsored Products",
  "match_type": "exact",
  "condition": "",
  "action": "",
  "metric_threshold": "",
  "reasoning": "",
  "case_metrics": {},
  "evidence_quote": "",
  "comment_signal": "none",
  "confidence": "medium",
  "limitations": "",
  "contradiction_key": "",
  "tags": []
}
```

`post_type` 可选值：

```text
tutorial_article
question_post
case_post
discussion_post
mixed
unknown
```

`record_type` 可选值：

```text
executable_rule
case_observation
diagnostic_hypothesis
diagnostic_question
counterexample
comment_signal
irrelevant_noise
```

`noise_reason` 可选值：

```text
none
account_invitation
social_reply
thanks_only
off_topic
too_short
unreadable
```

`case_metrics` 可包含：

```json
{
  "category": "",
  "price": "",
  "cpc": "",
  "acos": "",
  "cvr": "",
  "ad_order_share": "",
  "daily_orders": "",
  "organic_rank": "",
  "ad_rank": "",
  "keyword_type": "",
  "competitor_context": "",
  "ranking_problem": ""
}
```

要求：

1. 发布人正文中的真实数据优先提取为 `case_observation`。
2. 评论区建议优先提取为 `diagnostic_hypothesis` 或 `executable_rule`。
3. 评论区无关内容标记为 `irrelevant_noise`。
4. 评论区观点默认 `confidence` 不高于 `medium`。
5. 提问者的疑问不能直接当成确定性规则。
6. 普通摘要不能算 record。
7. 可执行规则必须包含：

   * condition
   * action
   * reasoning
   * limitations

建议 commit message：

```text
phase-4: define record extraction schema for cases rules diagnostics and noise
```

---

# Phase 5：用示例文件做小样本测试

实现脚本：

```text
.agents/skills/amazon-ads-keyword-strategy/scripts/extract_records.py
```

先不要处理全部 100 篇。

重点测试文件：

```text
017_q31734_广告关键词为何无法推动自然排名上升，广告单占比非常高.md
```

输出：

```text
data/processed/amazon_ads_skill/extracted_records_sample.jsonl
```

执行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/extract_records.py" --include-source-id A017 --output "data/processed/amazon_ads_skill/extracted_records_sample.jsonl"
```

如果 source_id 不一定是 A017，则支持用文件名筛选：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/extract_records.py" --include-file-name "017_q31734_广告关键词为何无法推动自然排名上升，广告单占比非常高.md" --output "data/processed/amazon_ads_skill/extracted_records_sample.jsonl"
```

该示例必须正确提取：

## A. 案例 1：鞋类产品广告依赖

```text
类目：鞋类
售价：$30
CPC：约 $0.2
ACOS：约 10%
广告转化率：约 4%-5%
广告单占比：70%
广告排名：第一位
主要关键词：精准中小词
日出单：20-40 单
关键词份额：15%-20%
自然排名：7 页开外
问题：广告数据好看，但自然排名无法进入前三页，且广告依赖严重
record_type：case_observation
```

## B. 案例 2：新产品广告依赖

```text
日常订单：40-70 单
广告单占比：50% 以上
竞品环境：同类竞品只有亚马逊自营压着
关键词排名：进入前 5 页，但难进第一页
record_type：case_observation
```

## C. 作者补充

```text
CPC 最低：$0.16
广告花费：基本每天花满
出单不多原因：关键词是中等偏小词
section_role：author_update
```

## D. 噪音评论

评论 1：

```text
账号邀请，无关
record_type：irrelevant_noise
noise_reason：account_invitation
```

评论 2：

```text
简单社交回复，无关
record_type：irrelevant_noise
noise_reason：social_reply
```

## E. 评论 3 的诊断假设

必须提取为 `diagnostic_hypothesis`，不能高于 `medium confidence`：

```text
低 ACOS 可能来自低 CPC，不代表转化率好
需要检查高峰期广告位置
需要检查广告 CTR
需要比较广告转化率、产品整体转化率和类目平均转化率
广告依赖严重时，可以考虑活动流量
需要检查广告点击、访问量、浏览量关系，判断链接质量
```

禁止：

```text
不要写成普通摘要
不要把“低 ACOS 一定无法推自然排名”写成绝对规则
不要把评论 3 标成 high confidence
不要把无关评论进入规则库
```

建议 commit message：

```text
phase-5: validate extraction on sample case discussion post
```

---

# Phase 6：小批量处理 10 篇文章

不要直接跑 100 篇，先跑 10 篇。

输出：

```text
data/processed/amazon_ads_skill/extracted_records_batch10.jsonl
data/processed/amazon_ads_skill/extraction_report_batch10.md
```

执行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/extract_records.py" --limit 10 --output "data/processed/amazon_ads_skill/extracted_records_batch10.jsonl"
```

检查重点：

1. 是否有普通摘要混入。
2. 是否把案例误判成规则。
3. 是否把评论区噪音误判为有效内容。
4. 是否把评论区观点标成 high confidence。
5. 是否漏掉重要指标。
6. 是否能提取 ACOS、CPC、CVR、广告单占比、自然排名、订单量等数据。
7. 是否保留 evidence_quote，但不要过长。

如果问题多，修正脚本后重新跑。

建议 commit message：

```text
phase-6: run batch extraction on first ten markdown posts
```

---

# Phase 7：批量处理全部文章

读取：

```text
data/processed/amazon_ads_skill/article_sections.jsonl
```

输出：

```text
data/processed/amazon_ads_skill/extracted_records.jsonl
data/processed/amazon_ads_skill/extraction_report.md
data/processed/amazon_ads_skill/noise_comments.jsonl
```

执行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/extract_records.py" --output "data/processed/amazon_ads_skill/extracted_records.jsonl"
```

统计报告必须包含：

```text
总文章数
总 section 数
总 record 数
case_observation 数量
executable_rule 数量
diagnostic_hypothesis 数量
diagnostic_question 数量
counterexample 数量
irrelevant_noise 数量
评论区 record 占比
评论区噪音占比
topic 分布
confidence 分布
```

质量抽查：

```text
随机抽查 50 条 record
检查是否符合 schema
检查是否有空泛内容
检查是否有错误分类
检查是否有 evidence_quote 过长
检查是否有评论区 high confidence
```

输出：

```text
data/processed/amazon_ads_skill/extraction_quality_report.md
```

建议 commit message：

```text
phase-7: extract structured records from all markdown posts
```

---

# Phase 8：归一化和去重

实现：

```text
.agents/skills/amazon-ads-keyword-strategy/scripts/normalize_records.py
```

读取：

```text
data/processed/amazon_ads_skill/extracted_records.jsonl
```

输出：

```text
data/processed/amazon_ads_skill/normalized_records.jsonl
data/processed/amazon_ads_skill/merged_rules.jsonl
data/processed/amazon_ads_skill/case_library.jsonl
data/processed/amazon_ads_skill/normalization_report.md
```

处理逻辑：

1. `case_observation` 进入案例库。
2. `executable_rule` 进入规则库。
3. `diagnostic_hypothesis` 进入诊断规则候选。
4. `irrelevant_noise` 进入噪音记录，不进入规则库。
5. 意思相近的规则合并。
6. 保留所有 supporting_sources。
7. 少数观点保留为 minority_view。
8. 不同阈值不要强行合并为固定阈值。

`merged_rules.jsonl` 字段：

```json
{
  "rule_id": "R001",
  "topic": "",
  "product_stage": "",
  "ad_type": "",
  "match_type": "",
  "condition": "",
  "recommended_action": "",
  "metric_threshold": "",
  "reasoning": "",
  "supporting_sources": [],
  "opposing_sources": [],
  "case_sources": [],
  "comment_signals": [],
  "confidence": "",
  "limitations": "",
  "tags": []
}
```

`case_library.jsonl` 字段：

```json
{
  "case_id": "CASE001",
  "source_id": "",
  "case_title": "",
  "case_topic": "",
  "category": "",
  "case_metrics": {},
  "problem": "",
  "diagnostic_points": [],
  "related_rules": [],
  "evidence_quote": "",
  "confidence": "case_data"
}
```

执行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/normalize_records.py"
```

建议 commit message：

```text
phase-8: normalize records into rules cases and noise datasets
```

---

# Phase 9：冲突观点识别

实现：

```text
.agents/skills/amazon-ads-keyword-strategy/scripts/detect_conflicts.py
```

读取：

```text
data/processed/amazon_ads_skill/merged_rules.jsonl
data/processed/amazon_ads_skill/case_library.jsonl
```

输出：

```text
data/processed/amazon_ads_skill/conflict_candidates.jsonl
.agents/skills/amazon-ads-keyword-strategy/references/07_conflict_register.md
```

重点识别冲突：

```text
低 ACOS 是否一定代表广告有效
广告单占比高是否一定要降广告
新品期放量 vs 新品期控 ACOS
广泛匹配拓词 vs 广泛匹配烧预算
点击多无订单立即否词 vs 样本不足继续观察
高 ACOS 关停 vs 高 ACOS 可能是在推自然排名
精准广告提高竞价 vs 精准广告控制预算
广告出单词排名好 vs 自然排名不提升
中小词出单 vs 大词自然排名目标
广告依赖 vs 活动流量补充
```

每个冲突条目包含：

```json
{
  "conflict_id": "C001",
  "conflict_title": "",
  "view_a": "",
  "view_b": "",
  "why_conflict_exists": "",
  "decision_rule": "",
  "applies_when": "",
  "avoid_when": "",
  "required_data": [],
  "confidence": "",
  "related_rule_ids": [],
  "related_case_ids": [],
  "supporting_sources": []
}
```

要求：

1. 不判断谁绝对正确。
2. 必须给出条件化决策。
3. 优先根据：

   * 产品阶段
   * 毛利
   * 预算
   * 样本量
   * 广告目标
   * 自然排名目标
   * 库存压力
   * 关键词类型
4. 案例帖只能作为支持或反例，不直接变成绝对规则。

建议 commit message：

```text
phase-9: detect conflicts and build decision rules
```

---

# Phase 10：生成 references 方法论文件

根据：

```text
merged_rules.jsonl
case_library.jsonl
conflict_candidates.jsonl
```

生成并完善：

```text
.agents/skills/amazon-ads-keyword-strategy/references/03_keyword_classification.md
.agents/skills/amazon-ads-keyword-strategy/references/04_campaign_structure.md
.agents/skills/amazon-ads-keyword-strategy/references/05_search_term_optimization.md
.agents/skills/amazon-ads-keyword-strategy/references/06_product_stage_strategy.md
.agents/skills/amazon-ads-keyword-strategy/references/08_metric_thresholds.md
.agents/skills/amazon-ads-keyword-strategy/references/09_case_library.md
.agents/skills/amazon-ads-keyword-strategy/references/10_noise_filter_rules.md
.agents/skills/amazon-ads-keyword-strategy/references/11_source_index.md
```

## 03_keyword_classification.md

包含：

```text
核心词
长尾词
竞品词
品牌词
防守词
属性词
场景词
低相关词
垃圾词
中小词
大词
出单词
排名目标词
```

每类词说明：

```text
定义
判断标准
适合广告结构
适合产品阶段
常见误判
优化动作
```

## 04_campaign_structure.md

包含：

```text
新品期广告结构
爬坡期广告结构
稳定期广告结构
旺季广告结构
淡季广告结构
清库存广告结构
自动广告
手动精准
手动词组
手动广泛
ASIN 投放
品牌防守
竞品进攻
```

## 05_search_term_optimization.md

包含：

```text
搜索词报告诊断逻辑
加精准逻辑
否定精准逻辑
否定词组逻辑
降竞价逻辑
提竞价逻辑
继续观察逻辑
样本不足处理
低 ACOS 但自然排名不动的诊断逻辑
广告单占比过高的诊断逻辑
```

## 06_product_stage_strategy.md

包含：

```text
上架前
新品 0-14 天
新品 15-45 天
爬坡期
稳定期
旺季前
旺季中
淡季
清库存期
```

## 08_metric_thresholds.md

包含：

```text
CTR
CVR
CPC
ACOS
TACOS
ROAS
点击数
订单数
广告单占比
自然单占比
花费
毛利
自然排名
广告排名
BSR
Session
Unit Session Percentage
```

## 09_case_library.md

包含高价值案例，例如：

```text
低 ACOS + 高广告单占比 + 自然排名无法提升
广告出单集中在中小词，但目标大词自然排名不动
广告数据好看，但整体链接质量可能不足
```

## 10_noise_filter_rules.md

定义哪些内容不能进入规则库：

```text
账号邀请
感谢
简单回复
无关闲聊
情绪表达
无数据支撑的绝对判断
过短评论
重复评论
```

每个 reference 文件最后都要有：

```text
Common Mistakes
Quality Checklist
```

要求：

1. 不能凭空编造。
2. 依据不足标注 low confidence。
3. 案例和规则要分开。
4. 评论区观点必须说明置信度限制。

建议 commit message：

```text
phase-10: generate references for rules cases metrics and noise filters
```

---

# Phase 11：编写最终 SKILL.md

完善：

```text
.agents/skills/amazon-ads-keyword-strategy/SKILL.md
```

必须包含：

```text
Purpose
When to Use This Skill
Required Inputs
Optional Inputs
Core Workflow
Record Types
Case Handling
Comment Handling
Noise Filtering
Decision Rules
Conflict Handling
Confidence Rules
Output Format
References Map
Quality Checklist
```

固定输出格式：

```text
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
```

明确禁止：

```text
不要给泛泛建议
不要只看 ACOS
不要忽略 TACOS、CVR、CTR、CPC、广告单占比、自然排名
不要忽略产品阶段
不要忽略样本量
不要把案例直接当成规则
不要把评论区观点当成确定性结论
不要把无关评论进入规则库
冲突观点必须条件化处理
```

建议 commit message：

```text
phase-11: write final skill workflow and output format
```

---

# Phase 12：创建 examples

完善：

```text
.agents/skills/amazon-ads-keyword-strategy/examples/example_input_search_term_report.md
.agents/skills/amazon-ads-keyword-strategy/examples/example_output_ads_diagnosis.md
.agents/skills/amazon-ads-keyword-strategy/examples/example_output_keyword_strategy.md
.agents/skills/amazon-ads-keyword-strategy/examples/example_output_case_diagnosis.md
```

必须包含 4 类示例：

```text
新品期广告结构规划
搜索词报告优化
ACOS 高但可能在推自然排名
ACOS 低但自然排名不提升、广告单占比高
```

其中 `example_output_case_diagnosis.md` 必须覆盖：

```text
低 ACOS 不等于自然排名一定会上升
广告单占比高意味着依赖风险
需要区分出单词和目标排名词
需要检查广告位、CTR、CVR、类目平均转化率、Session、Unit Session Percentage
中小词出单不一定能推动大词自然排名
```

建议 commit message：

```text
phase-12: add examples for ad diagnosis keyword strategy and case reasoning
```

---

# Phase 13：建立测试集 evals

完善：

```text
.agents/skills/amazon-ads-keyword-strategy/evals/test_cases.jsonl
.agents/skills/amazon-ads-keyword-strategy/evals/expected_outputs.md
```

至少 35 个测试案例，覆盖：

```text
新品期广告结构
自动广告跑词
手动精准广告优化
词组匹配优化
广泛匹配烧预算
点击多无订单
样本量不足
ACOS 高但自然排名提升
ACOS 低但自然排名不提升
TACOS 下降但 ACOS 上升
广告单占比过高
自然单占比过低
竞品 ASIN 投放
品牌词防守
旺季前广告放量
淡季控成本
清库存广告
案例帖处理
评论区噪音过滤
评论区诊断观点降置信度
```

每条 test case：

```json
{
  "case_id": "T001",
  "user_input": "",
  "expected_must_include": [],
  "expected_must_not_include": [],
  "related_reference_files": [],
  "difficulty": "medium"
}
```

必须有专门测试：

```text
输入：ACOS 10%，CPC 0.2，广告单占比 70%，自然排名 7 页开外
正确输出必须包含：
- 不能只看 ACOS
- 要检查 CPC 是否过低
- 要检查广告位和 CTR
- 要检查广告出单词和自然排名目标词是否一致
- 要检查整体 CVR / Session / Unit Session Percentage
- 要提示广告依赖风险

错误输出不能包含：
- 直接说广告效果很好不用调整
- 直接说低 ACOS 一定能推自然排名
- 直接建议关闭广告
```

建议 commit message：

```text
phase-13: add eval cases for rule case and comment handling
```

---

# Phase 14：验证脚本

实现：

```text
.agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py
```

检查：

```text
必需目录是否存在
必需文件是否存在
SKILL.md 是否有 name 和 description
JSONL 是否合法
extracted_records.jsonl 字段是否完整
merged_rules.jsonl 字段是否完整
case_library.jsonl 字段是否完整
irrelevant_noise 是否没有进入规则库
评论区 high confidence 是否违规
evidence_quote 是否过长
evals 是否至少 35 条
references 是否为空
examples 是否符合输出格式
```

执行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py"
```

输出：

```text
data/processed/amazon_ads_skill/validation_report.md
```

如果有错误，必须指出：

```text
文件
行号
字段
错误原因
修复建议
```

建议 commit message：

```text
phase-14: add validation script for skill artifacts
```

---

# Phase 15：最终质量审查

完整检查：

```text
.agents/skills/amazon-ads-keyword-strategy
```

输出：

```text
data/processed/amazon_ads_skill/final_quality_review.md
```

检查重点：

```text
SKILL.md 是否能指导 Codex 正确调用
references 是否覆盖广告、关键词、搜索词、排名、阶段策略
case_library 是否保留案例而不是误当规则
noise_filter 是否过滤无关评论
conflict_register 是否解决冲突观点
是否过度依赖 ACOS
是否忽略 TACOS、CVR、CTR、CPC、广告单占比、自然排名
是否能处理低 ACOS 但自然排名不动的问题
是否能处理广告依赖症
是否能区分中小词出单和大词排名目标
是否能处理新品期、稳定期、旺季、淡季、清库存
examples 是否可复用
evals 是否能测试准确性
validate_outputs.py 是否通过
```

最后执行：

```powershell
python ".agents/skills/amazon-ads-keyword-strategy/scripts/validate_outputs.py"
git status
```

不要自动 commit。

建议 commit message：

```text
phase-15: finalize validate and review amazon ads keyword strategy skill
```
