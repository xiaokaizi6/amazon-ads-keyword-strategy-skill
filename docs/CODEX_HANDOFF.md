# Codex 当前交接

- 最后更新：2026-08-18
- 当前分支：`main`
- 最新已核对远端提交：`dff050ac88dcbe26822cbf58a18a96f3af121a27`
- 最新任务记录：`docs/handoffs/2026-08-18-108-full-content-retrieval-audit.md`

## 当前状态

2026-08-18 已按“可检索内容覆盖”而非仅文件数量复审 108 份资料。`assets/knowledge/full_content_coverage_108_2026-08-18.jsonl` 对 portable manifest 的 100 篇项目文章和 8 份用户资料逐一验证：108/108 为 `available_with_source_boundaries`、无 `validation_issues`。覆盖层包括 2,002 个文章分段、CPC Word 168 个正文/表格节点、原 PDF 143 页 OCR、两份进阶诊断 Word 的 194/79 个节点、图片广告报告 12 张嵌入图 OCR、划线价 Word 的 64 个节点+11 图 OCR、折扣 Excel 1,097 个单元格+1 图 OCR，以及新品流程 Excel 309 个单元格。原件仍保留在 `assets/source_materials/` 并是内容权威；OCR 仅为检索定位层，精确表格、图片、数字、公式及低置信度内容必须回查原件。

新增 `assets/knowledge/portable_case_background_index_2026-08-18.jsonl`，合并且去重 48 条来源忠实案例（原统一批次 36 条、CPC 原件 8 条、原 PDF 4 条）。每条保留 source ID/位置、指标、来源观察、作者解释、动作或 unknown 与交叉验证边界，供后续回答给出详细案例背景。新增 `references/28_full_content_retrieval_coverage_108_2026-08-18.md`、Skill `18k`、T062 eval 及可重复运行的 XLSX 全单元格导出、Office 嵌入媒体 OCR、覆盖审计与案例索引脚本。后续相关问题须先检索实际匹配的全文层与案例索引，按“结论—资料背景—是否命中上传案例—结论理由—来源状态/适用边界”回答；没有相似案例必须写 `未命中具体案例`，不得以 108 个文件均可检索暗示其中所有观点已证实。

本轮已把 20 个新增/更新的 Skill 规则、脚本、全文层、案例索引和 eval 同步到桌面安装副本 `C:\Users\liuya\.codex\skills\ads_skill\skills\amazon-ads-keyword-strategy`。桌面副本的 20/20 文件哈希一致、108/108 覆盖清单路径均可定位、48 条案例唯一，并通过 `quick_validate.py`。项目版验证真实结果：覆盖/案例 JSONL Python 解析与字段断言 `PASS`；`quick_validate.py` `PASS`；62 条 eval JSONL 的唯一 ID/T062 检查 `PASS`；`git diff --check` `PASS`（仅 CRLF 警告）。未重新进行 Word 视觉渲染 QA；其因缺少 LibreOffice/`soffice` 的 `BLOCKED` 状态不影响本次内容检索审计。

2026-08-19 已按用户授权直接发布至 GitHub `main`，未创建分支或 PR。提交 `925f49bc56b0202b4ad9162d69dd9ed4b0e9175a`（`Integrate 108-source evidence pack`）已推送至 `origin/main`；143 页原始 PDF（149,818,945 bytes）由 Git LFS 上传成功。未提交 `tmp/` 与根目录 `outputs/` 的临时/交付副本；其余 Skill 资料包、检索层、处理产物与交接记录均在该提交范围内。

2026-08-18 用户明确知识问答目标：不需要查看原 PDF 的 PNG、截图或 Word 视觉渲染；只需要在后续问题中得到结论、上传资料背景、是否命中上传案例、结论理由和来源/适用边界。已新增 Skill `18j`、`references/27_portable_108_evidence_pack.md` 的 `User Knowledge-Answer Priority` 及 T061 eval。对上传资料的窄问题应先给 `结论`，再按 `资料背景`、`是否命中上传案例`、`结论理由`、`来源状态与适用边界` 回答；只列本次实际命中的来源，不要求用户先查看 PNG/OCR/Word。内部仍可在需要核对精确表格、截图、公式或低置信度 OCR 时回查原件，但不能用“视觉 QA 未完成”代替业务结论。

2026-08-18 已从 143 页图片型 `SRC-3a9e4ddd5371` 原 PDF 生成可搜索的 OCR 派生 Word：`outputs/亚马逊专题课-进阶广告诊断有优化全指导-OCR文字检索版.docx`。全量 OCR JSONL 为 `data/processed/amazon_ads_skill/advanced_ads_pdf_ocr_full_2026-08-18.jsonl`，连续覆盖 143/143 页、10,245 行、119,644 个字符，无空页；716 条低置信度 OCR 行原样保留而未静默修正。派生 Word 与 JSONL 已随 Skill 复制到 `assets/derivatives/` 和 `assets/knowledge/`，并以 `advanced_ads_pdf_ocr_derivative_manifest_2026-08-18.json` 记录原 PDF、派生物哈希、页数和使用边界。`references/26_full_source_materials.md`、source index 和 T060 已更新：OCR 仅是页码可检索的派生层，表格、截图、公式、数字、专有名词及低置信度文字必须回查原 PDF 页，原 PDF 仍是唯一内容权威。

新 Word 的结构检查通过（10,391 段、143 个连续“原 PDF 第 N 页”标题）；Documents Skill 标准视觉渲染仍因无 LibreOffice/`soffice` 而 `BLOCKED`，没有 PNG，不得表述为 Word 版式已视觉通过。原 PDF 的先前 143/143 页人工视觉审阅不等于这份新 Word 的渲染 QA。

2026-08-17 已复核 CPC Word 视觉渲染的依赖链：`pdf2image 1.17.0` 和 Poppler (`pdftoppm` / `pdftocairo`) 现已可用，故原先 `ModuleNotFoundError: pdf2image` 已解决。但 Documents Skill 的标准 `render_docx.py` 重新执行后明确因 `FileNotFoundError [WinError 2]` 无法启动 `soffice` 而停止，未产生页面 PNG；视觉 QA 仍是 `BLOCKED`，绝不能写为通过。官方 LibreOffice 26.2.5.2 安装包可由 WinGet 定位，但本轮下载/安装没有完成；本机无可用 Word 注册或 `WINWORD.EXE` 后备。下一次应先成功安装并验证 `C:\Program Files\LibreOffice\program\soffice.exe --version`，再用标准渲染器生成 PNG 并逐页检查。

2026-08-17 已将统一批次的 **108 份来源**制作成项目版与桌面 Codex 安装副本均可离线读取的证据包：100 篇项目文章放入 `assets/source_materials/project_articles/`，8 份用户资料保留为原件（6 份其余上传文件在 `user_uploads/`，CPC Word 与 143 页 PDF 保持在 `source_materials/` 根目录）。`assets/knowledge/portable_108_source_manifest.jsonl` 为每个来源保留原始获取路径、Skill 相对资产路径与 SHA-256；项目版和桌面副本均已验证为 108/108 可定位且哈希一致。为便于离线检索，Skill 同时携带 articles、sections、normalized records、规则/案例/冲突库及统一批次的 781 主张、36 案例和审查报告副本。

新增 `references/27_portable_108_evidence_pack.md`、Skill `18i` 和 T059 eval：每个使用资料包的广告/关键词回答必须列出本次**实际命中**的 source ID/文件及 claim/case/位置，并区分 `来源观察`、`作者思路/解释`、`审查状态`、`本次结论依据` 与 `当前适用边界`。108 份资料构成可检索背景，不允许把全部资料名当作每条结论的伪引用；无直接匹配时必须如实说明，不能强行给出来源支持的结论。`PARTIAL` 仍只表示默认二进制自动读取限制，不等于资料未读或全部业务主张已获证明。

2026-08-17 已把用户重新提供的两份原件纳入项目版和桌面 Codex 安装副本的 Skill 资产：`亚马逊CPC广告打法知识体系全梳理v1_20260804.docx`（SHA-256 `123d25…de6693`）和 143 页 `亚马逊专题课-进阶广告诊断有优化全指导.pdf`（SHA-256 `3f75d0…7e86df`）。新增 `references/26_full_source_materials.md`：对来源问题必须分开写来源观察、作者思路/解释和审查后结论；原件是完整内容权威，结构化层只用于检索，不能替代原件或把案例/阈值升级为规则。桌面副本位于 `C:\Users\liuya\.codex\skills\ads_skill\skills\amazon-ads-keyword-strategy`，已同步全部项目 Skill 文件与两份原件。

CPC 原件已通过 Open XML 按正文顺序完整导出为 `cpc_playbook_full_content_2026-08-17.jsonl`：168 条来源忠实记录（142 段、26 表），并新增 8 条可检索来源案例，分别保留指标、观察结果、作者解释、动作与交叉验证边界。其 21 条既有原子主张和 8 条新案例均为 0 契约错误；单来源报告仍为 `PARTIAL`，仅因默认读取器不能直接解析二进制 DOCX，且 `manual_reviewed: true` 已记录。PDF 原件的既有 143/143 页人工视觉审查、18 条页码主张与 4 条来源案例已随包携带；同样不把图片型 PDF 的机器不可读状态误称为内容未读。

本轮新增 Skill-first 广告决策门槛：任何广告优化、关键词、竞品、预算、竞价、否词、排名或生命周期建议，都必须先读取当前实际使用的 `SKILL.md` 和任务相关 References Map 文件；输出需显示 `Skill 使用状态`、实际 Skill 路径、已加载 reference 和应用约束。Skill 或必要 reference 无法加载时，只能给诊断问题、补数要求或可逆测试，不能凭通用经验直接给广告动作。新增 `references/25_skill_first_decision_gate.md` 和 T057 eval，并同步到 Codex 安装副本的 MCP/Skill-first 核心规则。

本轮变更已通过 PR [#3](https://github.com/xiaokaizi6/amazon-ads-keyword-strategy-skill/pull/3) 合并到 `main`，合并提交为 `dff050ac88dcbe26822cbf58a18a96f3af121a27`；发布分支已删除。

本轮新增实时市场数据 MCP 决策门槛：涉及当前市场、竞品、关键词、需求、趋势、排名或放量决策时，必须先调用已安装的西柚洞察 MCP，记录真实 operation、站点、ASIN/关键词、请求/返回窗口、字段、新鲜度和缺失项。新增 `references/24_live_market_data_mcp_decision_gate.md`、T056 eval 和项目长期要求。MCP 只负责当前市场证据，不替代 Amazon 官方政策/功能文档、用户账户报告或项目讲义证据；调用失败或字段不完整时，只能输出 `PARTIAL`/`BLOCKED` 下的条件化方案或可逆低风险测试，不能给出强制提价、否词、加预算或拆活动决策。本轮仅修改 Skill 规则和评估文件，没有具体广告账户决策，因此未调用实时市场 MCP；当前会话工具列表也未暴露西柚操作，未据此声称已完成市场数据验证。

项目已有 100 篇原始 Amazon 广告文章及分阶段生成的索引、section、提取记录、规则库、案例库、冲突库、噪声库和关键词库。现有 skill 已要求条件化建议并区分案例、规则、假设、评论和噪声。

本轮新增项目级 Codex 协作规范、每任务交接闭环，以及新讲义进入后的全库交叉验证和冲突保留协议。后续 Codex 应先读根目录 `AGENTS.md`，再读本文件与任务相关 skill/reference。

本轮已实现规则库/案例库的独立重建脚本，并新增 `review_sources.py`、来源审查 schema 和可选来源审查产物校验。两个重建脚本复用 `normalize_records.py` 的同一套聚合逻辑，避免独立算法漂移。

本轮已完整阅读用户提供的《亚马逊进阶广告诊断优化全指导-文字改述版.docx》（全部非空段落、表格和附录），并保留 seat cushion 四 SKU 案例的原始指标、假设及处理逻辑。课程中的点击阈值、毛利判断、库存月数、广告位比例、测试周期和功能说明均已拆成原子主张并标注状态，未升级为通用规则。

最新一轮完整阅读了同一套课程 PDF 的《亚马逊专题课-进阶广告诊断有优化全指导-文字整理版 (1).docx》：OOXML 读取 540 个非空段落、26 个表格、17,329 个字符；新增 22 条原子主张和 6 条来源忠实案例记录。它与上一份整理版属于同一证据家族，不作为独立证据重复计票。

2026-08-13 又完整处理了 5 个用户文件：上述课程文字整理版（识别为同一证据家族，不重复计票）、`新品推广基础推广动作及流程(1).xlsx`、`2025亚马逊划线价运营玩法.docx`、`亚马逊折扣+促销说明.xlsx` 和图片版 `亚马逊广告报告高效分析和优化-Word版 (1).docx`。新增批次共 5 个来源、22 条原子主张和 11 条来源忠实案例。图片版 Word 无正文，已逐张检查 12 张图片；自动 manifest 仍诚实标记二进制不可读。新增资料已写入 `references/19_pricing_promotion_launch_integration.md` 与 `references/20_image_ad_report_integration.md`，并在 Skill 中加入主动 `讲义案例提示` 规则。

用户进一步明确要求：争议、未决、证据不足、过时和条件化内容也必须上传到 Skill 并标记。已新增 `references/21_disputed_uncertain_claim_retention.md` 作为集中登记和回答协议，明确这些状态仍属于 Skill 知识库；未进入 `merged_rules.jsonl` 只表示未升级为无条件规则，不表示未保存。

本次对话上传资料总审计见 `docs/handoffs/2026-08-13-full-upload-audit.md`：7 个文件/来源均已完成决策相关内容阅读与结构化纳入；报告同时明确人工阅读、自动可读性、全项目交叉覆盖和当前平台复核之间的边界，不能将 `PARTIAL` 说成全部事实已被官方证明。

本轮已将 100 篇项目文章与对话内 8 个唯一用户文件（含原始课程 PDF）重新合并为同一批次，运行 `scripts/build_full_batch_audit.py` 生成 108 个来源、781 条主张和 36 条案例，再由 `review_sources.py --manifest-input` 统一校验。108 个来源均被引用，主张契约错误 0，案例契约错误 0；100 个 Markdown 来源可自动读取，8 个 DOCX/XLSX/PDF 已通过前序专用提取或图像检查完成人工阅读并在 manifest 标记 `manual_reviewed: true`。机器报告仍为 `PARTIAL`，仅表示默认自动解析器无法直接读取二进制文件。完整批次边界和结论见 `references/22_full_batch_review_2026-08-13.md` 与 `docs/handoffs/2026-08-13-full-batch-cross-audit.md`。

本轮按 OpenAI Codex `skill-creator` 规范检查并优化 Skill 结构：新增 `agents/openai.yaml` UI 元数据；将维护者说明移出 Skill 目录，改存为 `docs/AMAZON_ADS_SKILL_MAINTAINER_GUIDE.md`；为超过 100 行的 reference 增加 Contents 导航；将 source-review/full-batch reference 补入 References Map；扩展 frontmatter description 以覆盖资料审查、原子主张、案例和冲突保留；把“所有问题都强制使用 11 节输出”改为完整诊断使用、窄问题按需使用，减少无关模板文本。Skill 主入口保持 500 行以内。

本轮现场复核原始课程 PDF `亚马逊专题课-进阶广告诊断有优化全指导.pdf`：重新渲染并检查 143/143 页，确认 SHA-256 为 `3f75d0ed42cf8fd7e8818fa82beaf57d9d593cd01753a30b141e87054b7e86df`，PDF 为图片型且没有可用文本层。新增 18 条 PDF 专属原子主张和 4 条来源忠实案例，写入 `references/23_advanced_ads_pdf_live_review_2026-08-13.md` 及 `data/processed/amazon_ads_skill/*advanced_ads_pdf_live*` 产物。审查报告为 `PARTIAL`：人工页面覆盖完整，但同课改写不作为独立证据；2025-05 广告位界面被标为 `outdated`，75% 相似度被标为 `unsupported`，固定否词/预算/生命周期数字保留为 `context_dependent`，数学聚合与公式按边界标记为 `supported`。当前 Amazon 官方文档已作为时效性平台事实的复核入口，后续命中这些主张或案例必须显示 `讲义案例提示`。

## 已知工作区状态

本轮开始前已存在以下用户改动，本轮未处理：

- `ads-skill.zip`：Git 状态为删除。
- `ads_skill.zip`：Git 状态为未跟踪。

- 本轮新增原件资产包含约 150 MB 的 PDF；若后续准备提交或发布，先确认远端仓库的大文件策略、用户授权与下载包体积。原件未被改写。

不得在没有用户授权的情况下恢复、删除或提交这两个文件。

## 已确定的长期规则

- 原始讲义不是事实权威；重要主张必须跨项目资料核对。
- 只有满足严格证据条件才使用 `confirmed_error`。
- 无法确定时保留所有有意义观点，并输出不同路线的适用条件和验证方法。
- 对时效敏感的平台事实优先核对当前 Amazon 官方一手资料。
- 每次实质性任务都要更新本文件并新增历史交接；只读任务以用户边界为先。
- 后续上传资料完整阅读后，必须保留全部决策相关案例：来源观察、作者解释和实际动作分开记录；即使解释证据不足、具有条件或与既有观点冲突，案例也不能静默删除或升级成通用规则。重复改述同一底层资料时，必须合并证据家族，不能重复计票。
- 新增资料中的刷单、返佣评价、review club、刷加购/心愿单、关联店铺制造 List Price 和虚假订单已用 `confirmed_error` 标记并只作为风险证据；不得给出优化或规避检测的执行步骤。新品固定毛利/预算/ACOS、促销叠加公式、旧 Deal/Prime 数字、TOS +900% 和 70% 在线时长均未升级为通用规则。
- 所有 `disputed`、`unresolved`、`unsupported`、`outdated`、`context_dependent` 主张必须保留 claim ID、source ID、原文位置、证据边界、条件和验证方法；相关问题回答时必须主动显示 `讲义案例提示`。
- 当后续广告诊断触及这类案例或条件化主张时，必须主动显示来源状态 / 案例置信度、适用边界、关键不匹配及可逆验证方式。

## 未决事项

- CPC Word 的视觉渲染 QA 仍为 `BLOCKED`：`pdf2image` 和 Poppler 已补齐，但缺少 LibreOffice/`soffice`，Documents Skill 标准渲染器无法完成 DOCX→PDF 转换。原件哈希、Open XML 全文节点导出、来源/案例契约校验和桌面副本哈希均已完成；若需要视觉版 QA，先完成 LibreOffice 安装并验证可执行文件，再重跑标准渲染器。

- 当前已完成进阶诊断讲义的单独主张审查：`data/processed/amazon_ads_skill/advanced_ads_claims.jsonl`、`claim_review_advanced_ads.jsonl`、`source_manifest_advanced_ads_review.jsonl` 和 `source_validation_advanced_ads_report.md`。报告为 `PARTIAL`，因为 DOCX 被自动清单器标记为二进制不可读，且项目 100 篇原文未逐条全部覆盖；内容本身已通过 OOXML 全文解析和人工交叉判断。
- 最新整理版单独审查产物为 `advanced_ads_rewrite_v2_claims.jsonl`、`claim_review_advanced_ads_rewrite_v2.jsonl`、`source_manifest_advanced_ads_rewrite_v2.jsonl`、`source_case_records_advanced_ads_rewrite_v2.jsonl` 和 `source_validation_advanced_ads_rewrite_v2_report.md`。报告为 `PARTIAL`；22 条主张状态为 supported 7、context_dependent 11、unsupported 2、unresolved 2，6 条来源案例全部通过案例契约校验。
- 新增五文件批次的审查产物为 `source_manifest_2026-08-13_new_bundle.jsonl`、`new_source_bundle_claim_review.jsonl`、`new_source_bundle_case_records.jsonl` 和 `source_validation_report_2026-08-13_new_bundle.md`。22 条主张和11条案例通过契约校验；报告为 `PARTIAL`，因为 DOCX/XLSX 自动读取器标记为不可读，且本批次没有把项目全部 100 篇原文重新作为 claims 输入。人工已读取上传文件，不能把该报告写成全项目 `PASS`。
- 本轮讲义的历史单独来源清单为 `data/processed/amazon_ads_skill/source_manifest_advanced_ads_lecture.jsonl`，旧报告 `source_validation_advanced_ads_lecture.md` 仍保留其自动解析 `NOT_READY` 状态。现场复核的当前产物是 `source_manifest_advanced_ads_pdf_live_2026-08-13.jsonl`、`claim_review_advanced_ads_pdf_live_2026-08-13.jsonl`、`source_case_records_advanced_ads_pdf_live_2026-08-13.jsonl` 和 `source_validation_report_advanced_ads_pdf_live_2026-08-13.md`；后者记录完整人工页面覆盖但仍为 `PARTIAL`，不会把人工阅读夸大为机器可读或全部事实已被证明。
- 本轮完整阅读用户提供的 `C:\Users\liuya\Downloads\亚马逊CPC广告打法知识体系全梳理v1_20260804(1).docx`：通过 OOXML 读取了全部非空段落、表格和附录对照表（文档自称整理 175 篇文章）。该文件不含图片媒体，主要内容为整理者对公式、SP/SB/SD 架构、广告报告、20 种打法和指标优化的文字总结。已生成 `data/processed/amazon_ads_skill/source_manifest_cpc_playbook.jsonl` 与 `data/processed/amazon_ads_skill/source_validation_cpc_playbook.md`；由于脚本默认不解析 DOCX，来源报告诚实保持 `NOT_READY`，但本轮已完成可读性结构化阅读。未将该文档的阈值、平台机制或打法升级为通用规则。
- 当前学习结论：ACOS/ROAS/CPA/TACOS 等算式可作为待核对的数学定义；CTR/CVR/ACOS 健康值、广告与自然销售占比、TOS 溢价、自动/手动迁移阈值和预算百分比均属于经验或案例口径，需按站点、类目、阶段、目标和样本量验证；“质量得分扣费公式”、广告排名因果、3 个月流量扶持、功能名称/回溯窗口、叠词/马甲/海王等打法及 Prompts/SPV 等功能描述属于高风险或时效性主张，后续必须拆成原子主张并核对项目资料与 Amazon 官方来源。文档中的账户数据和 175 篇文章摘要只作为来源观察，不作为独立规则证据。
- 前一份 CPC 讲义的 21 条 claim 状态为 supported 13、context_dependent 1、disputed 1、unresolved 5、unsupported 1。本轮进阶诊断讲义新增 21 条 claim；最新整理版再新增 22 条 claim（supported 7、context_dependent 11、unresolved 2、unsupported 2），本批次新增22条 claim及11条案例，并新增 `references/19_*`、`references/20_*`、T051/T052 eval。
- 本轮新增 `references/21_disputed_uncertain_claim_retention.md` 和 T053 eval，未删除任何既有争议主张或案例。
- 当前全量统一批次产物为 `source_manifest_full_batch_2026-08-13.jsonl`、`full_batch_claim_review_2026-08-13.jsonl`、`full_batch_case_records_2026-08-13.jsonl` 和 `source_validation_report_full_batch_2026-08-13.md`。781 条主张状态为 supported 131、context_dependent 187、disputed 25、unresolved 204、unsupported 227、outdated 3、confirmed_error 4；这些状态是证据强度/适用边界，不是简单的真假二分类。
- 全量批次中 A069 没有规范化抽取记录，已保留 `manual_coverage_fallback` 未决项；后续应修复或复核上游抽取器，不得把空记录当成无内容。
- 当前 Skill 结构符合必需入口要求：`SKILL.md` 有仅含 `name`/`description` 的 YAML frontmatter，目录内有 `agents/openai.yaml`、`references/`、`scripts/`、`evals/` 和示例资源；不再保留会与 Skill 入口重复的 `README.md`。
- 已生成标准来源审查产物：`data/processed/amazon_ads_skill/source_manifest.jsonl`、`claim_review.jsonl`、`source_validation_report.md`，以及可复用输入 `cpc_playbook_claims.jsonl`。验证器已检查 JSONL、来源字段、状态约束和引用完整性。
- 根据用户要求，未升级为通用规则的讲义内容现在也正式纳入 skill 的条件化主张层。相关问题回答时必须显示 `讲义案例提示`，说明来源状态、适用条件、不同路线、缺失数据和可逆验证窗口；`disputed`、`unresolved`、`unsupported` 仍不能作为无条件 executable rule。
- Word 文件已做结构检查；标准 `render_docx.py` 因当前环境缺少 LibreOffice / soffice 而无法渲染。尝试本机 Word 自动化导出也未生成 PDF，因此视觉 QA 不能标记为通过。
- 尚未实现自动调用模型的 eval runner；当前 eval 校验的是测试集结构和规则约束，不是模型回答质量。结构校验已通过 `quick_validate.py`，但尚未进行隔离线程的真实任务 forward-test。
- GitHub 仓库网页对匿名访问返回 404，`gh` 当前未登录；本轮通过已配置的 Git remote 成功 fetch 并确认本地与 `origin/main` 一致。

## 推荐下一步

收到下一批讲义后，复用 `scripts/build_full_batch_audit.py`、`scripts/review_sources.py`、`references/16_cpc_playbook_integration.md`、`references/19_pricing_promotion_launch_integration.md`、`references/20_image_ad_report_integration.md`、`references/21_disputed_uncertain_claim_retention.md` 和 `references/22_full_batch_review_2026-08-13.md` 的流程；完整阅读后将决策相关案例作为人工结构化输入交给 `--cases-file` 校验，写入 `source_case_records.jsonl` 或保留同等字段的批次专用案例文件。重复改述同一底层资料时先合并证据家族。未决主张可以保留在条件化主张层，但必须输出来源状态、适用条件、不同路线、缺失数据、验证窗口、成功标准和停止标准；不要直接写成 `merged_rules.jsonl` 的无条件规则。若需对 Skill 进行结构变更，先对照 `docs/AMAZON_ADS_SKILL_MAINTAINER_GUIDE.md`、`skill-creator` 规范和官方 GitHub 示例，再运行全部结构/输出校验。
