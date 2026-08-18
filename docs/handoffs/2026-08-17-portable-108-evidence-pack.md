# 2026-08-17：可携带 108 份证据包与回答依据契约

## 任务目标

继续上一轮已纳入两份原件的工作，把全项目 100 篇文章及全部 8 份用户资料制作成可安装到桌面 Codex Skill 的离线证据包；后续回答必须显示实际依据，而不是只给无来源的结论。

## 实际完成内容

- 将 `data/raw/amazon_ads_articles/` 的 100 篇原始 Markdown 文章复制到 Skill 的 `assets/source_materials/project_articles/`；原始 `data/raw/` 未改写。
- 将其余 6 份已纳入批次的用户文件保留为原件，复制到 `assets/source_materials/user_uploads/`。已在上一轮保留的 CPC Word 和 143 页 PDF 位于 `assets/source_materials/` 根目录，合计正好 8 份用户资料。
- 复制既有的 article index/sections、normalized records、规则/案例/冲突库、统一来源清单、781 条主张审查、36 条案例审查和批次报告到 `assets/knowledge/`，不重跑上游抽取和审查管线。
- 新增 `scripts/build_portable_evidence_manifest.py`，由既有 `source_manifest_full_batch_2026-08-13.jsonl` 生成 Skill 相对路径、保留原始路径、并用 SHA-256 匹配资产的 portable manifest。
- 新增 `scripts/verify_portable_evidence_pack.py`。项目版与桌面副本均得到 108 行、`project_corpus=100`、`user_document=8`、`Integrity errors: 0`。
- 新增 `references/27_portable_108_evidence_pack.md`，并更新 `SKILL.md`、`references/11_source_index.md`、T059 eval。规则要求每次回答只引用实际检索命中的来源/位置，分开写来源观察、作者解释、审查状态、结论依据和适用边界；全包存在不等于每一份都直接证明单条结论。
- 使用非删除式 `robocopy /E` 把项目 Skill 覆盖同步至 `C:\Users\liuya\.codex\skills\ads_skill\skills\amazon-ads-keyword-strategy`。桌面目录存在一个早有的额外 `README.md`，本轮没有删除它；项目所有 176 个文件均已在桌面副本中找到。

## 修改文件及原因

- `.agents/skills/amazon-ads-keyword-strategy/assets/source_materials/`：108 份保留原件，供离线完整上下文读取。
- `.agents/skills/amazon-ads-keyword-strategy/assets/knowledge/`：既有可检索/审查产物及新的 `portable_108_source_manifest.jsonl`。
- `.agents/skills/amazon-ads-keyword-strategy/scripts/build_portable_evidence_manifest.py` 与 `verify_portable_evidence_pack.py`：生成和验证可移植性，不写死用户本机绝对路径。
- `.agents/skills/amazon-ads-keyword-strategy/references/27_portable_108_evidence_pack.md`、`SKILL.md`、`references/11_source_index.md`：规定检索顺序和回答证据契约。
- `.agents/skills/amazon-ads-keyword-strategy/evals/expected_outputs.md`、`evals/test_cases.jsonl`：新增 T059，防止伪全量引用或把案例/阈值写成通用规则。
- `docs/CODEX_HANDOFF.md`：同步当前状态。

## 来源与结论边界

- 统一批次审查范围和既有计数来自 `references/22_full_batch_review_2026-08-13.md`：108 个来源、781 条主张、36 条案例；所有来源被覆盖，但二进制默认自动读取限制使报告状态为 `PARTIAL`。
- 本轮的 “108/108 完整可携带” 是对 Skill 资产存在性和 SHA-256 的结论，不是对 781 条业务主张真实性的重新认证。
- 原件是完整内容权威；JSONL 是检索/审查辅助层。案例中的结果、作者解释和实际动作继续分开，不能自动变成广告执行规则。

## 验证命令与真实结果

| 命令/检查 | 结果 |
| --- | --- |
| `python -m py_compile ...build_portable_evidence_manifest.py ...verify_portable_evidence_pack.py ...export_docx_source_content.py ...review_sources.py` | PASS |
| 项目版 `verify_portable_evidence_pack.py` | PASS：108 行、100 + 8、0 integrity errors |
| 项目版 `quick_validate.py` | PASS：`Skill is valid!` |
| `git diff --check` | PASS；仅 Git CRLF 预警 |
| 桌面副本 `verify_portable_evidence_pack.py` | PASS：108 行、100 + 8、0 integrity errors |
| 桌面副本 `quick_validate.py` | PASS：`Skill is valid!` |
| 项目文件存在性比较 | PASS：176 个项目文件，桌面缺失 0 |

## 风险与未执行项

- 本轮没有重新运行 `validate_outputs.py`：该脚本会写回默认 source manifest/report，上一轮已经验证过且已发生过覆盖风险；本轮使用不写入 canonical processed 产物的专用 portable verifier。
- CPC Word 的视觉渲染 QA 仍为 `BLOCKED`，运行时缺 `pdf2image`；这不影响原件哈希、Open XML 节点导出或 108 源资产完整性结论。
- 原件资产约 160 MB；未来提交/发布前仍须确认远端的大文件策略并取得用户授权。
- 未执行 commit、push、发布或删除。

## 下一步入口

用一个真实广告问题或资料检索问题进行 T059 风格的人工回答验收：检查输出是否只列出实际命中资料、是否区分来源观察/作者解释/审查状态，以及是否在缺直接支持时保留条件化边界。
