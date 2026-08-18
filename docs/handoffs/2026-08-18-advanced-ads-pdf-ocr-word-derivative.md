# 2026-08-18：进阶广告诊断 PDF OCR 可检索 Word 派生物

## 任务目标

根据用户确认的正确方向，将图片型 PDF `亚马逊专题课-进阶广告诊断有优化全指导.pdf` 转为可搜索 Word，以便阅读内容；原 PDF 必须保留并保持内容权威，不能被 OCR 输出替代。

## 实际完成内容

- 使用既有的 143 页 PDF PNG 页面材料，对 `SRC-3a9e4ddd5371` 逐页运行 `rapidocr-onnxruntime 1.4.4` 中文 OCR。
- 生成 `outputs/亚马逊专题课-进阶广告诊断有优化全指导-OCR文字检索版.docx`。文稿含原始 PDF 哈希、派生物说明，并按连续的 `原 PDF 第 N 页` 标题保留 143 页来源定位。
- 生成 `data/processed/amazon_ads_skill/advanced_ads_pdf_ocr_full_2026-08-18.jsonl`。每页记录 OCR 文本、每行 bbox、置信度、页面图片名、原 PDF 页码与 `machine_ocr_derived_not_source_authority` 使用状态。
- 全量覆盖校验：143 页连续、10,245 OCR 行、119,644 OCR 字符、0 个空页；716 行置信度低于 0.8，未被自动修正。Word 使用深色标记低置信度行，提醒读者回查原 PDF。
- 将 OCR JSONL 复制至 Skill `assets/knowledge/`，将 OCR Word 复制至 `assets/derivatives/`；新增派生物 manifest，并更新 `references/26_full_source_materials.md`、`references/11_source_index.md` 与 T060 eval。

## 来源与边界

- 原 PDF：`assets/source_materials/亚马逊专题课-进阶广告诊断有优化全指导.pdf`，SHA-256 `3f75d0ed42cf8fd7e8818fa82beaf57d9d593cd01753a30b141e87054b7e86df`，143 页，仍为唯一完整内容权威。
- OCR Word SHA-256：`d12781a0731bc3315be8a65470958767633335ca3616ad5f6a9b106294db44b7`。
- OCR JSONL SHA-256：`b2fd66ffe48b0efd1b9a5999df273c4b674efeef91ca0b382a82e212e4829758`。
- OCR 使页面文字可检索，但不能证明 OCR 逐字准确；表格、截图、公式、数字、专有名词及低置信度文本必须依据相同页码回查原 PDF。OCR 文字不能被当作平台事实、通用广告规则或原文逐字引语。

## 验证命令与真实结果

| 检查 | 结果 |
| --- | --- |
| RapidOCR 第 1 页试运行 | PASS：识别中文/英文标题与课件文字 |
| 143 页 OCR 输出 | PASS：143 行 JSONL 页面记录，页码 1–143 连续 |
| OCR 完整性检查 | PASS：10,245 行、119,644 字符、0 空页、716 低置信度行保留 |
| Word 结构检查 | PASS：10,391 段、143 个连续页码标题 |
| Documents Skill `render_docx.py` | BLOCKED：缺少 LibreOffice/`soffice`，无 PNG 输出 |

## 风险、未执行项与下一步

- 没有逐行人工校对 10,245 条 OCR。低置信度标记与原页定位降低了误用风险，但不等于文本已逐字校勘。
- 新 Word 的视觉渲染 QA 未执行成功：当前环境仍无 LibreOffice/`soffice`。不要把结构检查或原 PDF 页面审阅写成 Word 排版通过。
- 原 PDF 未被改写；未删除、提交、推送或发布。
- 下一步：安装并验证 LibreOffice 后，使用 Documents Skill 标准渲染器对 OCR Word 生成 PNG，逐页检查文本截断、表格/标题分页和低置信度颜色标记。
