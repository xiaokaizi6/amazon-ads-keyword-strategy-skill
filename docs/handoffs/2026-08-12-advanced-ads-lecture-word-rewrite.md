# 2026-08-12 - 进阶广告诊断课件 Word 文字改述

## 任务目标

阅读用户提供的 `C:\Users\liuya\Downloads\亚马逊专题课-进阶广告诊断有优化全指导.pdf`，以自己的语言完整复述为 Word 文稿。案例不得传递原截图，应提取可用数据、背景、结论和边界。

## 实际完成内容

- 视觉阅读原 PDF 全部 143 页。PDF 的可提取文本极少，因此以 120 DPI 逐页渲染、4 页联系表方式检查全部页面。
- 新建 `outputs/亚马逊进阶广告诊断优化全指导-文字改述版.docx`。
- 文稿以七个主题段落组织：课程地图、广告诊断、ACOS 优化、核心关键词、投放结构、商品阶段规划和可执行检查表。
- 将室内坐垫案例改写为数据表与结论，保留课件中的毛利率假设、曝光、点击、CTR、CR、ACOS、TACOS 和处理方向；未复制任何商品照片、后台截图、二维码或培训推广页。
- 将点击样本、库存月数、毛利判断、站点基准区间、竞价功能等内容明确标注为课程或案例口径，未作为跨类目通用规则。
- 用 `review_sources.py` 为新课件生成单独来源清单和 `NOT_READY` 来源报告；没有创建虚假的空 `claim_review`。

## 修改文件及原因

| 文件 | 原因 |
| --- | --- |
| `outputs/亚马逊进阶广告诊断优化全指导-文字改述版.docx` | 用户请求的最终 Word 交付物。 |
| `data/processed/amazon_ads_skill/source_manifest_advanced_ads_lecture.jsonl` | 新资料的可追溯来源清单。 |
| `data/processed/amazon_ads_skill/source_validation_advanced_ads_lecture.md` | 如实记录本轮未进行原子主张审查，状态为 `NOT_READY`。 |
| `docs/CODEX_HANDOFF.md` | 同步当前状态、证据边界和验证状态。 |
| `docs/handoffs/2026-08-12-advanced-ads-lecture-word-rewrite.md` | 本次不可覆盖历史交接。 |

## 来源与置信度

- 原始来源：用户提供的 PDF，课件封面标注 Amazon 全球开店官方讲堂、讲师李尚明；PDF 元数据创建日期为 2026-06-29，143 页。
- 内容可读性：PDF 文本层很少，`review_sources.py` 仅支持文本型扩展名，因此其来源记录标为不可读；本任务的实际阅读证据是完整逐页视觉检查。
- 结论边界：Word 是对单一课件的准确改述，课程中的实操阈值与案例观察仍是 `context_dependent`，不构成独立的平台机制验证或跨项目资料交叉验证。

## 验证命令与真实结果

| 检查 | 命令 / 方法 | 结果 |
| --- | --- | --- |
| PDF 元数据 | `pdfinfo` | PASS：143 页、未加密。 |
| 全页阅读 | `pdftoppm` 后逐页联系表视觉检查 | PASS：已覆盖 1-143 页。 |
| Word 结构 | `uv run --with python-docx --python 3.11 ...` | PASS：79 个正文段落、22 个表格、1 个节、23 个标题层级。 |
| 来源登记 | `review_sources.py --no-project-corpus --source-file ...` | PASS：生成 1 条来源清单；主张审查状态 `NOT_READY`，未被写成已验证。 |
| Word 渲染视觉 QA | `render_docx.py` | BLOCKED：环境缺少 LibreOffice / soffice。 |
| Word 替代导出 | 本机 Word COM 导出 PDF | BLOCKED：超时且未生成 PDF。 |
| Git 空白检查 | `git diff --check` | 待最终运行。 |

## 风险 / 遗留事项

- 未执行跨项目 100 篇文章和 Amazon 官方页面的逐条主张审查；这不在用户要求的“阅读并复述”范围内。
- 无法完成 DOCX 的 PNG 视觉渲染检查；交付前已完成结构检查，但不能把版式视觉 QA 写成通过。
- 课程课件含有可能时效变化的控制台界面与报告名称；读者在实操前应检查当前站点后台与官方文档。

## 下一步入口

若用户希望把这份讲义沉淀为项目 skill 规则，应先以原子主张 JSONL 记录课件的关键说法，再在限定范围内运行 `review_sources.py` 并核对当前 Amazon 一手资料；不要直接把案例阈值并入通用 rulebook。
