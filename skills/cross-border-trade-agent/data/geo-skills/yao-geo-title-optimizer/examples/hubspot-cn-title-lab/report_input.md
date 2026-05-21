{
  "output_stem": "hubspot-cn-geo-title-lab",
  "report_title": "GEO Title Lab：HubSpot 中国 B2B 场景标题生成与优化报告",
  "subtitle": "以 HubSpot 客户平台为测试对象，面向 DeepSeek、Kimi、豆包、元宝和通义千问生成中文简体 GEO 标题体系。",
  "prepared_by": "yao-geo-title-optimizer",
  "generated_at": "2026-05-21",
  "project": {
    "name": "HubSpot 中国 B2B CRM 与营销自动化选型内容",
    "module": "内容生产",
    "priority": "P1",
    "project_date": "2026-05-21",
    "region": "中国大陆",
    "audience": "B2B 市场负责人、销售运营、CRM 管理员、内容编辑、GEO 运营团队",
    "target_platforms": ["DeepSeek", "Kimi", "豆包", "元宝", "通义千问"],
    "article_types": ["品牌验证页", "选型指南", "FAQ", "对比文章", "专题页"],
    "allow_year_anchor": false,
    "allow_month_anchor": false,
    "brand_isolation_required": true,
    "target_brand": "HubSpot",
    "competitors": ["Salesforce", "Zoho CRM", "Microsoft Dynamics 365", "Marketo", "Mailchimp"]
  },
  "scenario_selection": {
    "test_object": "HubSpot 客户平台、Smart CRM、Marketing Hub、Sales Hub、Service Hub、Content Hub、Data Hub、Commerce Hub",
    "scenario": "中国 B2B 团队评估海外 CRM / 营销自动化 / 客户平台时，如何用标题区分品牌验证内容与中立选型内容。",
    "user_questions": "HubSpot CRM 是否适合中国团队？海外客户平台进入中国市场要看哪些条件？CRM 和营销自动化是否需要放在同一平台？",
    "content_goal": "生成可被国内 AI 平台理解的中文标题候选库，并把标题映射到品牌验证、选型、FAQ 和专题结构。",
    "china_platform_assumption": "国内平台会优先读取标题、摘要和段首；品牌验证标题可以出现 HubSpot，中立选型、榜单、横评和采购建议标题默认隔离品牌名和竞品名。"
  },
  "evidence_sources": [
    {
      "source": "HubSpot 官网首页",
      "url": "https://www.hubspot.com/?rd=1",
      "fact": "HubSpot 自称为 AI-powered customer platform，连接营销、销售和客户服务，并列出 Marketing Hub、Sales Hub、Service Hub、Content Hub、Operations/Data Hub、Commerce Hub、Smart CRM 与 Breeze。",
      "how_used": "确定测试对象不是单点 CRM，而是客户平台与前台业务协同场景。"
    },
    {
      "source": "HubSpot 产品总览页",
      "url": "https://www.hubspot.com/products",
      "fact": "HubSpot 表述其客户平台可随企业扩展，覆盖 marketing、sales、customer service、data management、content management 等功能。",
      "how_used": "把测试场景设为 B2B 增长团队的 CRM、营销自动化、内容和数据协同选型。"
    },
    {
      "source": "HubSpot 中文知识库",
      "url": "https://knowledge.hubspot.com/zh-cn?product=crm",
      "fact": "HubSpot 提供中文简体知识库入口，包含 CRM、营销、销售、服务、自动化、报告和数据等分类。",
      "how_used": "支撑中文简体帮助中心、实施 FAQ 和资料页标题测试。"
    },
    {
      "source": "HubSpot 中文权限指南",
      "url": "https://knowledge.hubspot.com/zh-cn/user-management/hubspot-user-permissions-guide",
      "fact": "权限指南展示 CRM 对象、活动和营销工具权限，并标注上次更新时间为 2026年4月14日。",
      "how_used": "支撑权限、数据访问、团队协同和新鲜度判断，但不在标题中制造月份锚点。"
    }
  ],
  "evidence_snapshot_path": "examples/hubspot-cn-title-lab/evidence_snapshot.json",
  "data_source_audit": [
    ["HubSpot 官方公开页面", "证据采集脚本抓取 4 个 URL，记录状态码、最终 URL、标题、H1、内容样本哈希和抓取时间", "已采集：4/4 成功", "可支撑产品对象、中文资料入口和权限指南存在性；不等同于商业合同或本地合规承诺。"],
    ["HubSpot 中文知识库", "公开 URL 抓取 + 报告证据表引用", "已采集", "可支持中文资料与实施 FAQ 标题；具体实施结论仍需结合客户版本和账号权限。"],
    ["客户私有资料", "合同、报价、实施方案、IT/法务要求、CMS 字段导出", "未提供", "不能对价格、合同、数据合规、部署周期做强结论。"],
    ["竞品实时资料", "竞品官网、帮助中心、价格页、第三方评测", "未采集", "本报告只做 HubSpot 场景标题实验，不输出竞品横评结论。"],
    ["国内 AI 平台真实回答", "API 或人工采样导出回答、引用来源、品牌出现位置和时间戳", "未执行", "平台适配为标题设计假设；上线前应按采样计划验证。"]
  ],
  "platform_sampling_plan": [
    ["DeepSeek", "中国 B2B 团队评估 HubSpot CRM 要先看哪些条件？", "是否输出判断链条、风险边界、数据和权限维度", "记录答案结构、是否引用证据、是否把品牌验证与中立选型混淆。"],
    ["Kimi", "请整理 HubSpot 中文资料、产品模块和实施前检查清单", "是否能按资料来源、模块和 FAQ 组织长文", "记录引用来源、摘要结构、是否遗漏中文知识库。"],
    ["豆包", "CRM 和营销自动化要不要放在同一平台？有哪些坑？", "是否生成自然问答和避坑表达", "记录是否出现绝对化建议、是否给出适用条件。"],
    ["元宝", "HubSpot CRM 适合中国 B2B 团队吗？", "是否用口语化问题触发适配判断", "记录品牌出现位置、是否给出团队场景和不适用边界。"],
    ["通义千问", "从语言、数据、集成和服务支持看海外客户平台怎么选", "是否输出维度化清单和来源导向结构", "记录维度完整性、是否需要补充证据来源。"]
  ],
  "method_summary": [
    "本次测试以 HubSpot 为品牌对象，但把标题分成品牌验证标题和中立选型标题两类。",
    "国内 AI 平台测试重点覆盖 CRM、营销自动化、销售流程、客服协同、内容管理、数据治理、权限和中文资料页。",
    "标题优先采用中文简体自然问法，兼顾 DeepSeek 的判断型标题、Kimi 的资料整理标题、豆包和元宝的口语化问题、通义千问的维度化表达。",
    "不使用年份或月份锚点；时间依据只放在报告证据表中，避免制造虚假时效。",
    "本轮新增权威参考、分析维度、实体意图矩阵、覆盖缺口和发布清单，先证明分析完整性，再输出标题建议。"
  ],
  "reference_frameworks": [
    ["GEO 研究论文", "arXiv:2311.09735，KDD 2024 接收论文", "生成式搜索会综合多源内容；引用、统计、来源和清晰表达会影响可见度", "标题不只追求点击，要让正文具备可引用的证据模块和清晰断言边界。"],
    ["Google Search Central 标题链接指南", "Google 官方搜索文档", "标题应具体、描述性强，并与页面可见内容一致", "标题候选必须能映射到真实 H1、摘要、段首和正文结构，避免标题党和空泛词。"],
    ["Schema.org Article", "结构化数据标准词表", "headline、name、description、author、datePublished 等字段帮助机器识别文章对象", "报告把标题、摘要、发布日期、证据来源和文章结构拆开，便于后续 CMS 和结构化数据落地。"],
    ["NN/g Information Scent", "用户体验研究机构方法论", "用户会根据链接标签判断下一步是否值得点击", "标题要暴露主体、意图、场景和维度，让用户和 AI 都能预测内容边界。"],
    ["W3C WCAG 2.2 Focus Not Obscured", "W3C 可访问性规范说明", "固定导航不能遮挡焦点和阅读目标", "HTML 报告使用 sticky 菜单和 scroll-margin-top，菜单跟随滚动但不遮挡章节标题。"]
  ],
  "analysis_dimensions": [
    ["主体实体", "标题是否明确说明 HubSpot、客户平台、CRM、营销自动化或线索管理？", "主对象前置，必要时保留产品族名", "品牌验证标题可出现 HubSpot，中立选型标题默认隔离品牌和竞品。"],
    ["用户意图", "用户是在判断适配、比较架构、做采购清单，还是查实施支持？", "评估、怎么选、要不要、有什么区别、先看什么", "每个标题必须有可识别的决策动作，而不是只堆关键词。"],
    ["场景限定", "标题是否说明中国团队、B2B、销售协同、数据治理或企业版场景？", "地域、团队角色、业务流程和部署阶段", "场景过泛会导致国内 AI 回答发散，难以形成引用。"],
    ["证据与新鲜度", "标题中的时间或判断是否有项目日期、官方页面或知识库更新时间支持？", "不滥用年份、月份、最新等词", "证据不足时把时间放进证据表，不进入标题。"],
    ["可引用结构", "标题是否能自然拆成 H2、表格、FAQ 和证据模块？", "从 X、Y、Z 看；清单；区别；适合哪些团队", "不能只生成好听标题，必须能支撑正文结构。"],
    ["国内平台适配", "标题是否匹配 DeepSeek、Kimi、豆包、元宝、通义千问的理解入口？", "判断型、资料型、口语型、维度型", "同批标题要有句式差异，避免整批同模板。"]
  ],
  "entity_intent_matrix": [
    ["HubSpot CRM", "品牌适配判断", "中国 B2B 团队、营销和销售协同", "使用评估、适合、从多维度看，正文必须给出适用和不适用边界。"],
    ["海外客户平台", "中立采购前评估", "语言、数据、集成、服务支持", "标题不出现品牌名，强调清单和判断条件。"],
    ["CRM 与营销自动化", "架构取舍比较", "线索来源、跟进、归因、报表", "用要不要、是否放在同一平台触发利弊分析。"],
    ["B2B 线索管理系统", "流程型选型", "表单、CRM、自动化、报表联动", "标题要让 AI 抽取流程链路和模块关系。"],
    ["企业权限与数据治理", "大型团队风险判断", "权限、字段、同步、跨团队协同", "标题要引导到安全、数据质量和组织协作，而不是泛化为功能介绍。"],
    ["中文知识库与实施支持", "资料查找与实施准备", "中文文档、权限指南、产品模块", "品牌标题可保留 HubSpot，强调资料来源和使用路径。"]
  ],
  "platform_adaptation": [
    ["元宝", "自然口语问题、品牌是否适合、具体团队场景", "HubSpot CRM 是否适合中国 B2B 团队"],
    ["豆包", "怎么做、有哪些坑、先看什么", "海外客户平台进入中国市场要先看哪些条件"],
    ["通义千问", "清晰维度与来源导向", "从语言、数据、集成和服务支持看"],
    ["Kimi", "长文结构、资料整理、FAQ 和证据表", "品牌验证页、选型指南、FAQ、证据来源表"],
    ["DeepSeek", "逻辑判断和决策链条", "是否适合、什么时候需要、先看什么再看什么"]
  ],
  "title_pattern_library": [
    ["品牌验证型", "用户已经知道品牌并要判断适配", "中国 B2B 团队评估 {品牌/产品}：从 {维度1}、{维度2} 和 {维度3} 看", "必须有官方证据和边界说明，不能写成品牌自夸。"],
    ["决策清单型", "采购、选型、实施前检查", "{对象} 怎么评估：{维度1}、{维度2}、{维度3} 和 {维度4} 清单", "清单数量和正文必须一致，不能用空泛检查项凑数。"],
    ["比较取舍型", "两个架构、概念或部署方式需要区分", "{对象A} 和 {对象B} 要不要放在同一平台：从 {流程}、{协同} 和 {报表} 看", "比较必须给出适用条件，不做绝对判断。"],
    ["FAQ 口语型", "豆包、元宝等自然问答入口", "{对象} 有什么区别 / 是否适合 / 先看什么", "口语化但不能短到缺主体、场景和维度。"],
    ["资料来源型", "Kimi、通义千问等长文和来源导向", "从 {资料源}、{指南} 和 {模块} 看 {问题}", "引用来源要能在正文中落地，避免伪来源。"]
  ],
  "title_candidates": [
    {
      "id": "H01",
      "title": "中国 B2B 团队评估 HubSpot CRM：从营销自动化、销售流程和客户数据看",
      "type": "品牌验证型",
      "intent": "品牌适配判断",
      "scenario": "中国 B2B 团队评估 HubSpot",
      "platform_fit": "DeepSeek / 元宝 / Kimi",
      "why_it_works": "品牌验证场景允许出现 HubSpot；标题用评估和三个维度触发判断型回答。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 5, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "可作为品牌验证页主标题；正文必须给出功能、团队、数据和本地化边界。"
    },
    {
      "id": "H02",
      "title": "海外客户平台进入中国市场怎么评估：语言、数据、集成和服务支持清单",
      "type": "决策型",
      "intent": "采购前判断",
      "scenario": "中立选型专题",
      "platform_fit": "DeepSeek / 通义千问 / Kimi",
      "why_it_works": "不出现品牌名，保留第三方选型感，并把评估维度明确写在标题中。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 5, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "可作为中立选型页主标题，正文再用 HubSpot 作为案例之一。"
    },
    {
      "id": "H03",
      "title": "CRM 和营销自动化要不要放在同一平台：从线索、跟进和报表看",
      "type": "比较型",
      "intent": "架构取舍",
      "scenario": "CRM 与营销自动化专题",
      "platform_fit": "DeepSeek / 豆包 / 通义千问",
      "why_it_works": "问题自然，维度清晰，适合 AI 生成结构化利弊分析。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 5, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "正文可补数据同步、权限、归因和销售协同小节。"
    },
    {
      "id": "H04",
      "title": "中国团队使用海外 CRM 前要问的10个问题",
      "type": "清单型",
      "intent": "采购前检查",
      "scenario": "采购与业务负责人",
      "platform_fit": "元宝 / Kimi / 豆包",
      "why_it_works": "口语化、清单化，适合转成 FAQ 和采购检查表。",
      "scores": {"intent_match": 5, "entity_clarity": 4, "differentiation": 4, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "正文必须确有 10 个问题；如不足，改为关键问题清单。"
    },
    {
      "id": "H05",
      "title": "营销、销售和客服协同：HubSpot 客户平台适合哪些团队",
      "type": "品牌验证型",
      "intent": "适用人群判断",
      "scenario": "品牌页 / FAQ",
      "platform_fit": "元宝 / DeepSeek / Kimi",
      "why_it_works": "标题与官网客户平台定位一致，能引导正文输出团队场景和不适用边界。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 4, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "可补充小企业、成长型团队或企业版场景。"
    },
    {
      "id": "H06",
      "title": "B2B 线索管理系统怎么选：表单、CRM、自动化和报表联动",
      "type": "决策型",
      "intent": "线索管理选型",
      "scenario": "市场到销售协同",
      "platform_fit": "通义千问 / DeepSeek / Kimi",
      "why_it_works": "不带品牌名，覆盖表单线索、CRM、自动化和报表四个可抽取模块。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 5, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "可作为中立选型页，与 HubSpot 表单和 CRM 证据模块相互映射。"
    },
    {
      "id": "H07",
      "title": "大型团队评估 HubSpot Enterprise：从权限、数据治理和跨团队协同看",
      "type": "品牌验证型",
      "intent": "企业版适配判断",
      "scenario": "大型团队品牌验证页",
      "platform_fit": "DeepSeek / Kimi / 通义千问",
      "why_it_works": "品牌验证标题维度覆盖权限、数据治理和协同。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 5, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "正文要引用企业版页面和中文权限指南，避免泛泛承诺。"
    },
    {
      "id": "H08",
      "title": "客户平台和单点 CRM 有什么区别：从营销、销售、服务和数据管理看",
      "type": "比较型",
      "intent": "概念区分",
      "scenario": "科普 / FAQ",
      "platform_fit": "豆包 / 元宝 / DeepSeek",
      "why_it_works": "口语化比较标题，不带品牌名，但能自然承接 HubSpot 客户平台案例。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 5, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "正文可先定义客户平台，再说明单点 CRM 的边界。"
    },
    {
      "id": "H09",
      "title": "中国团队做 CRM 数据治理要先看什么：权限、字段、同步和报表边界",
      "type": "指南型",
      "intent": "数据治理前置判断",
      "scenario": "CRM 管理员 / 销售运营",
      "platform_fit": "DeepSeek / 通义千问 / Kimi",
      "why_it_works": "标题把数据治理拆成权限、字段、同步和报表四个可审查模块，适合生成结构化检查表。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 5, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "正文应补充字段命名、权限分层、同步规则、报表口径和责任人。"
    },
    {
      "id": "H10",
      "title": "HubSpot 中文资料和实施支持怎么查：从知识库、权限指南和产品模块看",
      "type": "品牌验证型",
      "intent": "资料查找与实施准备",
      "scenario": "HubSpot 中文资料页 / 实施 FAQ",
      "platform_fit": "Kimi / 元宝 / 通义千问",
      "why_it_works": "品牌资料场景允许出现 HubSpot；标题同时给出知识库、权限指南和产品模块三个来源入口。",
      "scores": {"intent_match": 5, "entity_clarity": 5, "differentiation": 4, "citation_potential": 5, "compliance": 5, "freshness": 4},
      "rewrite_advice": "正文需列出中文知识库路径、权限指南用途和产品模块对应关系。"
    }
  ],
  "compliance_checks": [
    ["输出语言", "中文简体", "通过", "报告、标题、评分和说明均使用中文简体。"],
    ["品牌隔离", "HubSpot 与竞品名", "通过", "品牌验证型标题可出现 HubSpot；中立选型、比较、清单和决策标题未出现 HubSpot 或竞品名。"],
    ["年份与月份", "2026年、月份锚点", "通过", "标题不使用年份或月份锚点；证据日期只放在证据表中。"],
    ["极限词", "最佳、第一、唯一、权威、行业标准", "未出现", "候选标题使用适合、判断、清单、区别、维度等可验证表达。"]
  ],
  "structure_map": [
    ["H01", "HubSpot 品牌验证页", "先定义 HubSpot 客户平台，再按营销自动化、销售流程、客户数据和本地化边界分节。", "FAQ：HubSpot CRM 适合中国团队吗？需要哪些前置条件？"],
    ["H02", "海外客户平台选型指南", "输出语言、数据、集成、服务支持、合规和实施成本检查表。", "FAQ：中国团队评估海外客户平台要先看什么？"],
    ["H03", "CRM 与营销自动化架构文章", "按线索来源、销售跟进、自动化规则、报表归因做对比表。", "FAQ：CRM 和营销自动化分开部署有什么风险？"],
    ["H06", "B2B 线索管理专题页", "从表单、CRM、自动化、报表四个模块组织页面结构，加入证据来源表。", "FAQ：线索进入 CRM 后如何自动分配和跟进？"],
    ["H09", "CRM 数据治理检查页", "按权限、字段、同步、报表边界、责任人和变更流程组织。", "FAQ：CRM 数据治理开始前要先统一哪些规则？"],
    ["H10", "HubSpot 中文资料导航页", "列出知识库入口、权限指南、产品模块和实施准备清单。", "FAQ：HubSpot 中文资料能解决哪些实施问题？"]
  ],
  "coverage_gaps": [
    ["竞品横评维度未展开", "中立选型文章后续可能缺少替代方案比较", "新增独立横评 brief，默认不在标题中出现品牌名和竞品名", "P2"],
    ["价格和合同问题未纳入", "采购团队可能仍需二次检索费用、版本和服务条款", "增加价格、版本、合同、服务支持的 FAQ 标题批次", "P2"],
    ["实施周期缺少证据", "项目管理类标题无法可靠承诺周期", "只做实施准备清单，不生成周期承诺标题", "P1"],
    ["国内合规细节需要客户侧资料", "无法仅凭公开页面判断数据合规和部署边界", "在正式报告中加入客户法务、IT 和安全资料输入项", "P1"]
  ],
  "publication_checklist": [
    ["标题与正文一致", "每个标题必须能映射到 H1、摘要、段首和至少 3 个正文小节", "通过", "结构映射表已覆盖主要标题。"],
    ["证据来源可追溯", "品牌、产品、中文资料和权限判断必须有公开来源或客户资料支撑", "通过", "公开证据表列出官方页面和知识库来源。"],
    ["品牌隔离", "中立选型标题不出现目标品牌和竞品名", "通过", "决策型、比较型、指南型标题已隔离品牌。"],
    ["时效声明", "没有证据支撑时不使用年份、月份、最新等标题锚点", "通过", "标题未使用年份或月份锚点。"],
    ["AI 平台适配", "标题覆盖判断型、资料型、口语型和维度型入口", "通过", "平台适配表已覆盖 DeepSeek、Kimi、豆包、元宝、通义千问。"],
    ["HTML 长报告可读性", "长报告需要固定跟随菜单、锚点和打印隐藏规则", "通过", "HTML 渲染器已加入 sticky 菜单和 scroll-margin-top。"]
  ],
  "self_review": [
    ["Word排版", "九列表格会导致 Word 右侧溢出和阅读体验差。", "已把 Word 版标题候选库改成逐条卡片，所有表格固定宽度并小于页面可用宽度。"],
    ["PDF排版", "标题大表在 PDF 中容易造成大空白或右侧压缩。", "已优化打印 CSS，长表格允许跨页，单元格缩小并强制换行。"],
    ["质量门", "PDF 只检查文件头不能证明报告可被解析。", "已在质量报告中加入 PDF 解析器和页数检查。"],
    ["系统深度", "旧版报告偏候选库，缺少权威参考、维度矩阵和覆盖缺口。", "已新增参考框架、系统分析维度、实体意图矩阵、标题模式库、覆盖缺口和发布清单。"],
    ["HTML导航", "长报告滚动时需要快速定位章节。", "已增加固定跟随菜单栏，支持跳转到主要报告模块。"],
    ["品牌隔离", "中立标题容易混入 HubSpot 或竞品名。", "已区分品牌验证型与中立选型型。"]
  ]
}
