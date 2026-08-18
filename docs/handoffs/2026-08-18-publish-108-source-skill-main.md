# 发布 108 来源证据包至 main

## 目标

按用户明确授权，将当前 Skill、108 来源资料包、检索/案例层和交接文件直接提交并推送到 `main`，不创建分支或 PR。

## 提交范围

- `amazon-ads-keyword-strategy` 的 Skill 规则、references、evals、可重复抽取/审计脚本和 portable assets。
- `data/processed/amazon_ads_skill/` 中与 CPC 全文层及 PDF OCR 相关的可追溯处理产物。
- 2026-08-17 至 2026-08-18 的项目交接记录和 `docs/CODEX_HANDOFF.md`。
- 143 页原始 PDF 超过 GitHub 普通 Git 单文件限制，使用精确 `.gitattributes` 规则以 Git LFS 跟踪；原件未被改写。

## 明确排除

- `tmp/` 的渲染、安装和临时文件。
- 根目录 `outputs/` 的交付型 OCR Word 副本；同一检索层已在 Skill assets 内随资料包提交。

## 验证与发布

- 发布前检查 Skill/桌面副本覆盖与结构校验、JSONL 解析和 `git diff --check`。
- 提交和推送仅在 `main` 执行；不创建分支、不创建 PR。
