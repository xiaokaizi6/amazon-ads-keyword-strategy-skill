# 2026-08-17：CPC Word 视觉渲染依赖修复尝试

## 任务目标

处理 CPC Word 视觉渲染先前因缺少 `pdf2image` 而被阻塞的问题，目标是生成页面 PNG 并进行逐页版式检查；不改写原始 Word 内容。

## 实际完成内容

- 读取 Documents Skill 的渲染与 LibreOffice 故障排查流程；使用其标准 `render_docx.py` 作为验收命令。
- 已安装 `pdf2image 1.17.0`；检查确认 Poppler 的 `pdftoppm.exe` 与 `pdftocairo.exe` 在 PATH 中可用。
- 检查本机未安装 LibreOffice：`C:\Program Files\LibreOffice\program\soffice.exe` 不存在，`winget list --id TheDocumentFoundation.LibreOffice --exact` 也未发现已安装包。
- 确认官方 WinGet 包 `TheDocumentFoundation.LibreOffice 26.2.5.2` 及官方 MSI URL/公布 SHA-256 可取得。曾执行静默安装，但 WinGet 下载进程未完成；重新从官方 URL 下载同样受当前链路限制，未得到可校验 MSI，故没有使用不完整文件安装。
- 本机没有可用 Word 后备：注册表中不存在 `Word.Application` / `WINWORD.EXE` 路径，自动化尝试未成功启动可用 Word 进程。
- 使用补齐后的标准渲染命令重新执行。结果不再是 `pdf2image` 导入错误，而是在 DOCX→PDF 阶段抛出 `FileNotFoundError: [WinError 2]`，对应缺少 `soffice`；没有生成 PNG。

## 修改文件及原因

- `docs/CODEX_HANDOFF.md`：更新为当前真实阻塞点，避免下次重复诊断 `pdf2image`。
- 本文件：保留不可覆盖的任务记录。
- `tmp/cpc_word_visual_qa_2026-08-17/`：仅含本轮内部渲染尝试脚本/输出目录和未完成下载，不是 Skill 资产、未改写原件、未作为交付物。

## 验证命令与真实结果

| 检查 | 结果 |
| --- | --- |
| `python -c "import pdf2image"` | PASS |
| `Get-Command pdftoppm,pdftocairo` | PASS |
| `Test-Path C:\Program Files\LibreOffice\program\soffice.exe` | FAIL：不存在 |
| `winget show --id TheDocumentFoundation.LibreOffice --exact` | PASS：可定位官方 26.2.5.2 包 |
| Documents Skill `render_docx.py <CPC.docx> --output_dir ... --verbose` | BLOCKED：`FileNotFoundError [WinError 2]`，未生成 PNG |

## 结论、风险与下一步

- `pdf2image` 缺失已修复，但视觉 QA **尚未完成**；真实剩余前置条件是安装一个可运行的 LibreOffice/`soffice`（或可验证的 Word 转换器）。
- 不完整的 LibreOffice 下载文件没有被当作安装包或证据使用。
- 原始 CPC Word 未修改；其哈希、Open XML 内容导出和结构化来源审查仍有效，但不能替代视觉版式验收。
- 下一步：确认网络/安装权限后运行 `winget install --id TheDocumentFoundation.LibreOffice --exact --silent --accept-package-agreements --accept-source-agreements`；验证 `soffice.exe --version`；使用 Documents Skill `render_docx.py` 生成 PNG；以 100% 逐页检查并只在全部页面无缺字、重叠、裁切或表格错位时标为 PASS。
