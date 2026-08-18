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

## 结果

- 已提交并推送 `main`：`925f49bc56b0202b4ad9162d69dd9ed4b0e9175a`（`Integrate 108-source evidence pack`）。
- Git LFS 已成功上传原始 PDF：149,818,945 bytes；远端分支由 `3b276a0` 前进至 `925f49b`。
- 初次传输因失效的本机代理 `127.0.0.1:7897` 挂起并超时；清空 `ALL_PROXY`、`HTTP_PROXY`、`HTTPS_PROXY` 后直连 GitHub 成功。该代理未作为仓库配置写入。
