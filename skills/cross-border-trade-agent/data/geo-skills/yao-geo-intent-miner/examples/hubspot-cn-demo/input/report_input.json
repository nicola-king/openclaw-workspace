{
  "slug": "hubspot-cn-ai-intent-miner-demo",
  "title": "HubSpot 中文简体 AI 搜索意图与问题集挖掘报告",
  "subtitle": "以 DeepSeek、豆包、千问、Kimi、元宝为国内 AI 平台测试场景，系统验证意图拓词、追问链路、查询重写、内容资产映射和四格式输出。",
  "brand_name": "HubSpot",
  "analysis_date": "2026-05-21",
  "prepared_by": "yao-geo-intent-miner",
  "limitations": "本报告用于测试 AI 搜索意图挖掘能力。问题集代表意图空间，不代表真实搜索量、真实 AI 答案分布、法律意见、采购建议或 HubSpot 官方报价；价格、合规、实施和合同判断必须以官方资料、合同条款和专业团队复核为准。",
  "summary_cards": [
    {
      "label": "测试对象",
      "value": "HubSpot",
      "note": "CRM、营销、销售、客服、内容、数据、商务和 AI 工具一体化场景。"
    },
    {
      "label": "国内平台",
      "value": "5 个",
      "note": "DeepSeek、豆包、千问、Kimi、元宝，分别覆盖复杂决策、口语问法、多轮追问和管理视角。"
    },
    {
      "label": "核心问题",
      "value": "18 条",
      "note": "覆盖信息、推荐、比较、交易、风险、价格、替代、场景和品牌验证意图。"
    },
    {
      "label": "真实数据",
      "value": "部分接入",
      "note": "官方事实已校准；搜索量、CRM、客服问答和国内 AI 平台真实回答仍需授权或采样。"
    },
    {
      "label": "交付资产",
      "value": "12 类",
      "note": "新增真实数据源状态、AI 采样计划和数据校准动作。"
    }
  ],
  "sections": [
    {
      "title": "执行摘要与关键发现",
      "paragraphs": [
        "HubSpot 在国内 AI 搜索中的核心问题不是“品牌是什么”单点解释，而是中国出海团队如何在一体化客户平台、预算、数据合规、实施复杂度和本地替代之间做取舍。",
        "本次示例把 HubSpot 作为全球 B2B SaaS 品牌测试对象，输出中文简体问题底座，便于内容策略、GEO 运营、SEO 和监测团队在内容生产前先统一问题空间。",
        "优先级最高的内容机会包括：HubSpot 适合谁、HubSpot 与 Salesforce/Zoho/国产 CRM 怎么选、价格和席位变量、数据合规边界、营销销售客服一体化场景、Breeze AI 能力解释。"
      ],
      "table": {
        "headers": [
          "关键发现",
          "业务含义",
          "建议动作"
        ],
        "rows": [
          [
            "P0 问题集中在选型、价格、风险和替代",
            "这些问题更容易触发 AI 给出推荐或比较答案",
            "优先建设选型页、价格 FAQ、风险 FAQ 和监测 Prompt"
          ],
          [
            "国内平台问法更口语且包含“适合谁、贵不贵、靠谱吗”",
            "内容不能只写产品功能，需要回答决策疑虑",
            "把每个产品线映射到角色、场景、预算和证据"
          ],
          [
            "涉及数据合规、价格和竞品比较时风险较高",
            "AI 答案必须保留边界，不能替代法务或采购判断",
            "输出禁止回答边界和证据补采任务"
          ]
        ]
      }
    },
    {
      "title": "研究依据与方法升级",
      "paragraphs": [
        "本报告将传统搜索意图、会话式查询重写、LLM 查询扩展和内容可信度自检结合起来。目标不是生成更多关键词，而是生成可被 AI 平台回答、可被内容团队生产、可被监测团队复盘的问题体系。",
        "Broder 的信息/导航/交易意图用于任务层分类；TREC CAsT 和会话式查询重写用于多轮追问链路；LLM Query Expansion、Query2doc 和 HyDE 用于解释为什么要生成多种查询表达；BEIR 和 MS MARCO 用于强调检索评测和证据校准；Google helpful content / E-E-A-T 用于约束内容资产要可验证、完整、对用户有帮助。"
      ],
      "table": {
        "headers": [
          "方法依据",
          "转化为本 skill 的能力",
          "HubSpot 示例落点"
        ],
        "rows": [
          [
            "Web 搜索意图分类",
            "先判断信息、导航/验证、交易/行动，再映射九类 GEO 操作意图",
            "HubSpot 是什么、HubSpot 是否值得买、HubSpot 与 Salesforce 怎么选"
          ],
          [
            "会话式查询重写",
            "追问必须改写成上下文独立问题，便于复现 Kimi 和千问的多轮链路",
            "“那国内团队呢？”改为“中国出海团队如何评估 HubSpot 的本地适配性？”"
          ],
          [
            "LLM 查询扩展与假设文档",
            "把口语问法、检索短语、证据查询和标题输入拆开，防止扩展结果混成事实",
            "把“HubSpot 贵不贵”拆成席位、模块、积分、实施、合同五类变量"
          ],
          [
            "检索评测与内容可信度",
            "每个高价值问题都要有证据查询、来源等级和可验证边界",
            "价格、Breeze AI、产品线和合规问题只引用官方或待确认事实"
          ]
        ]
      }
    },
    {
      "title": "测试场景与事实校准",
      "paragraphs": [
        "测试场景定位为：中国出海 B2B SaaS、跨境电商、外贸服务或海外销售团队，在国内 AI 平台上搜索 HubSpot 是否适合作为 CRM、营销自动化、销售管理、客服、内容和数据一体化平台。",
        "事实校准只采用公开来源。涉及 HubSpot 产品、Breeze、价格和席位的判断应优先参考 HubSpot 官方产品目录、官方产品页、官方 AI 页和官方定价/目录说明。"
      ],
      "table": {
        "headers": [
          "事实线索",
          "来源级别",
          "报告采用方式",
          "来源"
        ],
        "rows": [
          [
            "HubSpot 是由 Marketing Hub、Sales Hub、Service Hub、Content Hub、Data Hub、Commerce Hub、Smart CRM 和 Breeze 组成的客户平台",
            "A",
            "建立产品线、角色和场景问题",
            "https://legal.hubspot.com/hubspot-product-and-services-catalog"
          ],
          [
            "Breeze 是 HubSpot 集成在客户平台中的 AI 工具集合，部分能力可能涉及 HubSpot Credits",
            "A",
            "生成 AI 功能、积分、效率和边界问题",
            "https://legal.hubspot.com/hubspot-product-and-services-catalog"
          ],
          [
            "HubSpot 官方页面强调统一 CRM 数据、客户视图、自动化和 AI 助手能力",
            "A",
            "生成一体化、自动化和数据治理问题",
            "https://www.hubspot.com/products/pricing-cr115"
          ],
          [
            "Google helpful content 强调有用、可靠、以人为本，并建议说明 Who/How/Why",
            "A",
            "报告披露生成方式、限制和证据等级",
            "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
          ]
        ]
      }
    },
    {
      "title": "真实数据接入状态与校准模式",
      "paragraphs": [
        "本示例已接入的是公开官方事实和方法依据；未接入真实搜索量、站内搜索、客服问答、CRM 转化、投放词库和国内 AI 平台真实回答。因此当前问题库和评分矩阵属于“证据校准后的预测意图空间”，不是完整真实数据校准结果。",
        "升级后的 skill 会把真实数据分成 M0 未接入、M1 用户提供、M2 工具/连接器导入、M3 已采样校准四种模式。没有真实数据时，报告必须输出采样计划和授权/补采动作；有真实数据时，才把 AI 答案触发概率、内容缺口、平台覆盖度和商业价值升级为校准分。"
      ],
      "table": {
        "headers": [
          "数据类型",
          "当前状态",
          "能否用于校准",
          "下一步"
        ],
        "rows": [
          [
            "HubSpot 官方产品与价格目录",
            "已接入公开网页事实",
            "可用于事实校准和证据等级",
            "定期复查产品名、席位、Credits 和 AEO/Breeze 信息"
          ],
          [
            "国内 AI 平台真实回答",
            "未采样",
            "暂不能用于品牌提及率或答案排序校准",
            "按 Prompt 库对 DeepSeek、豆包、千问、Kimi、元宝做人工或接口采样"
          ],
          [
            "搜索量、站内搜索和内容点击",
            "未提供",
            "暂不能用于需求规模校准",
            "接入关键词工具、Search Console、站内搜索或内容数据"
          ],
          [
            "客服问答、销售话术和客户访谈",
            "未提供",
            "暂不能用于真实痛点频次校准",
            "导入文本、表格或 CRM 记录后重算问题簇权重"
          ],
          [
            "CRM 线索、成交和流失原因",
            "未授权",
            "暂不能用于商业价值校准",
            "在脱敏后接入线索、成交阶段和流失原因数据"
          ]
        ]
      }
    },
    {
      "title": "输入归一化与对象边界",
      "paragraphs": [
        "输入被归一化为品牌、产品线、目标人群、业务场景、竞品集合、证据来源和合规边界。这样可以避免问题只围绕“HubSpot CRM”一个词扩展，而遗漏营销、销售、客服、内容、数据和 AI 的完整问题空间。",
        "本示例不判断 HubSpot 在中国的实际采购可行性，不给出法律结论，不输出未经证实的折扣、真实成交价或实施承诺。"
      ],
      "table": {
        "headers": [
          "对象",
          "归一化结果",
          "用途"
        ],
        "rows": [
          [
            "品牌",
            "HubSpot",
            "品牌验证、价格、替代、推荐和风险问题"
          ],
          [
            "产品线",
            "Smart CRM、Marketing Hub、Sales Hub、Service Hub、Content Hub、Data Hub、Commerce Hub、Breeze",
            "模块化问题簇、页面模块和知识库映射"
          ],
          [
            "目标人群",
            "中国出海 B2B SaaS、跨境电商、外贸服务、增长团队、销售团队、客服团队、管理者、IT/合规",
            "角色化场景和追问链路"
          ],
          [
            "竞品/替代",
            "Salesforce、Zoho CRM、纷享销客、销售易、国产 SCRM/CRM、自建系统",
            "中性比较、替代型问题和选型矩阵"
          ],
          [
            "排除范围",
            "法律意见、最终采购建议、报价承诺、未证实负面竞品判断",
            "合规边界和质检"
          ]
        ]
      }
    },
    {
      "title": "用户角色与场景矩阵",
      "paragraphs": [
        "国内 AI 平台上的问题往往从真实业务角色出发。老板关心投入产出，市场关心线索和自动化，销售关心管线和跟进，客服关心工单和知识库，IT/合规关心数据、集成和权限。",
        "角色矩阵用于防止问题库只覆盖 SEO 流量词，而无法被内容团队直接写成页面、FAQ 或知识库条目。"
      ],
      "table": {
        "headers": [
          "角色",
          "典型场景",
          "核心疑虑",
          "优先资产"
        ],
        "rows": [
          [
            "创始人/老板",
            "判断是否统一客户平台",
            "贵不贵、适合谁、能否提升管理效率",
            "选型框架、管理者 FAQ"
          ],
          [
            "市场负责人",
            "海外线索培育、邮件营销、内容增长",
            "自动化能力、线索归因、内容和 AI 效率",
            "Marketing Hub 场景页、Breeze 解释页"
          ],
          [
            "销售负责人",
            "销售管线、销售自动化、报价和跟进",
            "团队上手、管线可视化、与 Salesforce/国产 CRM 对比",
            "Sales Hub 对比页、销售 FAQ"
          ],
          [
            "客服负责人",
            "工单、知识库、客户服务自动化",
            "客服数据统一、响应效率、AI 客服边界",
            "Service Hub 场景页、风险 FAQ"
          ],
          [
            "IT/合规/采购",
            "数据、集成、权限、合同和跨境使用",
            "隐私、DPA、成本、供应商管理",
            "合规模块、采购清单、证据补采"
          ]
        ]
      }
    },
    {
      "title": "双层意图地图",
      "paragraphs": [
        "HubSpot 在国内 AI 平台上的问题空间集中在“适不适合中国团队”“和 Salesforce/Zoho/国产 CRM 怎么选”“价格怎么算”“数据合规风险”“营销销售客服能否打通”“Breeze AI 是否有实际价值”。",
        "双层意图先判断用户任务，再映射 GEO 操作意图，确保每个问题能落到内容资产或监测 Prompt。"
      ],
      "table": {
        "headers": [
          "任务层",
          "GEO 意图",
          "核心问题方向",
          "建议资产"
        ],
        "rows": [
          [
            "信息获取",
            "信息型",
            "HubSpot 是什么，包含哪些产品？",
            "品牌解释页、知识库"
          ],
          [
            "交易与行动",
            "推荐型",
            "出海企业 CRM 和营销自动化工具推荐里 HubSpot 值得选吗？",
            "榜单文章、监测 Prompt"
          ],
          [
            "交易与行动",
            "比较型",
            "HubSpot 和 Salesforce、Zoho、国产 CRM 怎么选？",
            "对比页、选型矩阵"
          ],
          [
            "信息获取",
            "价格型",
            "HubSpot 的席位、模块、积分和实施费用怎么估？",
            "价格 FAQ、采购清单"
          ],
          [
            "信息获取",
            "风险型",
            "HubSpot 有哪些数据、实施、成本和合同风险？",
            "风险 FAQ、合规模块"
          ],
          [
            "信息获取",
            "品牌验证型",
            "HubSpot Breeze AI、Data Hub、Commerce Hub 是否是当前产品重点？",
            "官方事实页、监测 Prompt"
          ]
        ]
      }
    },
    {
      "title": "问题簇与优先级评分",
      "paragraphs": [
        "问题簇按品牌认知、出海选型、竞品对比、价格预算、替代方案、数据合规、营销自动化、销售管理、客服服务、AI 功能、数据治理、商务收款和实施风险聚合。",
        "评分采用十维模型：商业价值、AI 答案触发概率、内容缺口、品牌植入空间、证据可得性、竞争难度、对话延展价值、决策阶段价值、平台覆盖度、合规风险。合规风险为反向约束，高风险问题可以是 P0 监测问题，但不能直接输出未经验证结论。"
      ],
      "table": {
        "headers": [
          "问题簇",
          "代表问题",
          "优先级",
          "原因"
        ],
        "rows": [
          [
            "出海选型",
            "中国出海 B2B 公司适合用 HubSpot 吗？",
            "P0",
            "商业价值高、AI 推荐概率高、适合做选型内容和监测"
          ],
          [
            "竞品对比",
            "HubSpot 和 Salesforce/Zoho/国产 CRM 怎么选？",
            "P0",
            "强决策意图，容易触发对比答案"
          ],
          [
            "价格预算",
            "HubSpot 贵不贵，席位和模块怎么估？",
            "P0",
            "直接影响采购，但必须保留报价边界"
          ],
          [
            "数据合规",
            "HubSpot 在国内使用是否有客户数据风险？",
            "P0",
            "高风险高价值，适合做合规边界和证据补采"
          ],
          [
            "AI 功能",
            "Breeze AI 对市场、销售、客服有什么用？",
            "P1",
            "品牌验证价值高，需要官方产品事实支撑"
          ]
        ]
      }
    },
    {
      "title": "五段式查询重写",
      "paragraphs": [
        "每个核心问题保留口语问法、独立重写、检索短语、证据查询和标题输入。检索短语用于平台可能抓取的标准表达，证据查询用于事实校准，标题输入用于后续内容生产。",
        "五段式重写特别适合国内 AI 平台：豆包和元宝保留口语，DeepSeek 增加约束，Kimi 和千问保留追问链路。"
      ],
      "table": {
        "headers": [
          "口语问法",
          "独立重写",
          "检索短语",
          "证据查询",
          "标题输入"
        ],
        "rows": [
          [
            "HubSpot 适合中国出海公司用吗？",
            "中国出海 B2B 团队如何评估 HubSpot CRM 和营销自动化平台？",
            "HubSpot 出海企业 CRM 营销自动化 适合谁",
            "HubSpot customer platform Smart CRM Marketing Hub Sales Hub official",
            "HubSpot 适合中国出海企业吗"
          ],
          [
            "HubSpot 和 Salesforce 怎么选？",
            "中型 B2B 团队在 HubSpot 和 Salesforce 之间如何选型？",
            "HubSpot vs Salesforce CRM 选型 中型企业",
            "HubSpot Salesforce comparison official Sales Hub CRM",
            "HubSpot 与 Salesforce 选型对比"
          ],
          [
            "HubSpot 贵不贵？",
            "HubSpot 的订阅、席位、模块和积分价格对中国团队意味着什么？",
            "HubSpot 价格 席位 Core Seat View-Only Seat Credits",
            "HubSpot pricing seats credits product catalog official",
            "HubSpot 价格和采购边界说明"
          ],
          [
            "Breeze 是不是就是普通 AI 助手？",
            "HubSpot Breeze AI 在客户平台中覆盖哪些营销、销售和客服能力？",
            "HubSpot Breeze AI assistant agents credits",
            "HubSpot Breeze AI official product catalog",
            "HubSpot Breeze AI 能力与适用场景"
          ]
        ]
      }
    },
    {
      "title": "国内 AI 平台适配",
      "paragraphs": [
        "本测试不调用真实平台答案，只输出可用于 DeepSeek、豆包、千问、Kimi 和元宝的中文简体监测 Prompt。后续如接入采样，应记录答案日期、平台版本、引用来源、品牌提及位置、证据质量和风险提示。",
        "平台适配的重点不是给每个平台写不同结论，而是让同一意图用不同问法触发：复杂决策、日常口语、多轮追问、长上下文资料整合和管理者判断。"
      ],
      "table": {
        "headers": [
          "平台",
          "问法特征",
          "Prompt 设计",
          "追问策略"
        ],
        "rows": [
          [
            "DeepSeek",
            "复杂决策、约束权衡",
            "加入预算、团队规模、数据合规、实施周期和替代方案",
            "连续追问预算、风险和优先级"
          ],
          [
            "豆包",
            "日常口语、适合谁、好不好用",
            "用“公司想上 CRM”“贵不贵”“会不会复杂”等自然问法",
            "追问老板、销售、市场视角"
          ],
          [
            "千问",
            "资料整合、多轮追问",
            "保留追问链路并要求独立判断标准",
            "追问资料来源和比较维度"
          ],
          [
            "Kimi",
            "长上下文、文档比较",
            "要求列选型表、风险边界和待确认事项",
            "追问官方资料和合同待确认项"
          ],
          [
            "元宝",
            "偏日常咨询和管理决策",
            "强调老板、销售负责人、市场负责人视角",
            "追问通俗解释和下一步动作"
          ]
        ]
      }
    },
    {
      "title": "内容资产与 FAQ 映射",
      "paragraphs": [
        "P0 问题优先进入对比文章、品牌解释页、价格 FAQ、实施风险 FAQ、数据合规模块和国内 AI 平台监测 Prompt。P1 问题进入场景页、知识库和标题生成输入包。",
        "每个内容资产必须有主问题、支持问题、证据需求和禁止回答边界，避免内容团队拿到泛泛的问题后无法直接开写。"
      ],
      "table": {
        "headers": [
          "资产",
          "输入问题",
          "交付建议",
          "证据需求"
        ],
        "rows": [
          [
            "品牌解释页",
            "HubSpot 是什么，包含哪些产品？",
            "用官方产品结构解释 Smart CRM、各 Hub 和 Breeze",
            "HubSpot 产品目录、产品页"
          ],
          [
            "选型对比页",
            "HubSpot 和 Salesforce/Zoho/国产 CRM 怎么选？",
            "按规模、预算、实施、营销销售一体化、数据合规做矩阵",
            "官方功能页、公开定价页、客户案例"
          ],
          [
            "价格 FAQ",
            "HubSpot 贵不贵，价格怎么算？",
            "只解释定价变量，不写未经确认的折扣或最终报价",
            "官方 pricing、Product Catalog、合同待确认项"
          ],
          [
            "风险 FAQ",
            "HubSpot 在国内使用有什么风险？",
            "标注数据、集成、实施、合同和续费风险",
            "隐私政策、DPA、法务复核"
          ],
          [
            "Breeze AI 解释页",
            "Breeze AI 能帮市场、销售、客服做什么？",
            "拆分 Assistant、Agents、Credits 和场景边界",
            "官方 AI 页、产品目录"
          ]
        ]
      }
    },
    {
      "title": "监测 Prompt 与采样计划",
      "paragraphs": [
        "监测 Prompt 用于观察国内 AI 平台如何回答 HubSpot 相关问题，而不是一次性生成内容。建议按月采样 P0 问题，按季度复盘品牌提及、竞品对比、证据引用和风险提示变化。",
        "采样记录字段建议包括：平台、日期、Prompt、答案摘要、HubSpot 是否出现、出现位置、是否引用来源、来源质量、是否出现价格/合规不当断言、下一轮追问。"
      ],
      "table": {
        "headers": [
          "采样对象",
          "频率",
          "核心记录字段",
          "质检重点"
        ],
        "rows": [
          [
            "P0 选型 Prompt",
            "每月",
            "平台、日期、答案排名、品牌提及、引用来源、竞品",
            "是否中性比较，是否提到 HubSpot 适用场景"
          ],
          [
            "价格与合规 Prompt",
            "每月",
            "价格断言、来源、风险提示、人工确认建议",
            "不得把不确定价格或法律判断写成事实"
          ],
          [
            "Breeze AI 与产品线 Prompt",
            "每季度",
            "产品名、AI 能力、积分/限制、来源",
            "是否使用当前官方产品名称"
          ],
          [
            "多轮追问 Prompt",
            "每月",
            "root_question、follow_up、standalone_rewrite、答案漂移",
            "Kimi/千问是否保留上下文并给出可复核依据"
          ]
        ]
      }
    },
    {
      "title": "证据缺口与数据校准",
      "paragraphs": [
        "意图拓词结果代表问题空间，不等同于真实搜索量、真实转化率或真实 AI 答案分布。生产使用前需要接入搜索量、站内搜索、客服问答、销售话术、客户访谈、社群评论和真实 AI 平台采样数据。",
        "HubSpot 示例中的价格、数据合规、实施复杂度和竞品替代问题都需要二次证据校准。没有证据时只能写“需要确认哪些变量”，不能写确定结论。"
      ],
      "table": {
        "headers": [
          "缺口",
          "影响",
          "补采方式",
          "优先级"
        ],
        "rows": [
          [
            "真实搜索量和 AI 问答热度",
            "无法判断问题真实需求规模",
            "接入关键词工具、站内搜索、AI 平台采样日志",
            "P0"
          ],
          [
            "中国团队真实实施经验",
            "无法判断上手难度和迁移成本",
            "采集客户访谈、实施复盘、服务商案例",
            "P0"
          ],
          [
            "合同、价格和折扣",
            "无法给出最终预算建议",
            "以官方定价、报价单和采购沟通为准",
            "P0"
          ],
          [
            "数据跨境与隐私合规",
            "高风险行业不能直接回答结论",
            "法务、DPO、IT 安全团队复核",
            "P0"
          ]
        ]
      }
    },
    {
      "title": "合规与禁止回答边界",
      "paragraphs": [
        "HubSpot 测试场景涉及客户数据、跨境系统、价格、采购合同、竞品比较和实施效果。报告可以生成问题、证据需求和内容边界，但不应输出法律结论、最终采购建议、未经证实的折扣或竞品负面事实。",
        "高风险行业如医疗、金融、教育、政务、法律服务等，必须把合规等级上调，并把禁止回答边界写入 FAQ 和监测 Prompt。"
      ],
      "table": {
        "headers": [
          "风险项",
          "合规等级",
          "禁止回答边界",
          "允许回答方式"
        ],
        "rows": [
          [
            "价格与折扣",
            "L2",
            "不得声称实际成交价、隐藏费用或折扣比例，除非有可验证来源",
            "解释订阅、席位、模块、积分、实施和合同变量"
          ],
          [
            "数据合规",
            "L3",
            "不得给出法律结论，不得承诺跨境数据合法",
            "列待确认事项，并提示法务、DPO 或合规团队确认"
          ],
          [
            "竞品比较",
            "L2",
            "不得写竞品缺陷或负面事实，除非有公开证据",
            "按场景、预算、生态、实施和本地化做中性比较"
          ],
          [
            "实施效果",
            "L2",
            "不得承诺增长、转化、ROI 或上线周期",
            "说明影响因素和需要评估的实施条件"
          ],
          [
            "AI 功能",
            "L2",
            "不得承诺 Breeze 自动完成全部营销、销售或客服工作",
            "解释官方能力、适用场景、限制和人工复核需求"
          ]
        ]
      }
    },
    {
      "title": "30/60/90 天落地路线",
      "paragraphs": [
        "问题库落地不应一次性全部写完。建议先用 P0 问题建立可被 AI 引用的基础资产，再用监测 Prompt 观察平台答案变化，最后用真实数据反向校准问题权重。",
        "路线图把内容、页面、知识库、监测和证据补采放在同一个节奏中，避免只关注流量而忽略品牌植入空间和证据可得性。"
      ],
      "table": {
        "headers": [
          "阶段",
          "目标",
          "关键动作",
          "验收口径"
        ],
        "rows": [
          [
            "0-30 天",
            "建立 P0 问题底座",
            "完成选型页、价格 FAQ、风险 FAQ、Prompt 库首轮采样",
            "P0 问题均有资产映射和证据查询"
          ],
          [
            "31-60 天",
            "补齐场景与产品线内容",
            "建设 Marketing/Sales/Service/Breeze/Data Hub 场景页和知识库",
            "P1 问题进入内容生产排期"
          ],
          [
            "61-90 天",
            "用真实数据校准",
            "接入平台采样、客服问答、销售反馈和内容表现数据",
            "更新评分矩阵、删重和优先级"
          ],
          [
            "持续迭代",
            "监测 AI 答案变化",
            "按月复盘品牌提及、竞品排序、证据来源和风险断言",
            "形成可追踪的 GEO 意图地图"
          ]
        ]
      }
    }
  ],
  "question_bank": [
    {
      "question_id": "Q001",
      "cluster": "品牌认知",
      "intent_type": "信息型",
      "question": "HubSpot 是什么，和普通 CRM 有什么区别？",
      "standalone_rewrite": "HubSpot 的客户平台、Smart CRM 和各产品 Hub 分别是什么？",
      "retrieval_rewrite": "HubSpot customer platform Smart CRM Marketing Hub Sales Hub Service Hub",
      "evidence_query": "HubSpot official customer platform Smart CRM products",
      "content_asset": "品牌解释页、知识库条目",
      "priority": "P0",
      "compliance_level": "L1"
    },
    {
      "question_id": "Q002",
      "cluster": "出海团队选型",
      "intent_type": "推荐型",
      "question": "中国出海 B2B 公司适合用 HubSpot 吗？",
      "standalone_rewrite": "中国出海 B2B 公司如何评估 HubSpot 是否适合 CRM 和营销自动化？",
      "retrieval_rewrite": "HubSpot 出海企业 CRM 营销自动化 适合谁",
      "evidence_query": "HubSpot customer platform marketing sales service official",
      "content_asset": "选型文章、监测 Prompt",
      "priority": "P0",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q003",
      "cluster": "竞品对比",
      "intent_type": "比较型",
      "question": "HubSpot 和 Salesforce 相比，哪个更适合中型销售团队？",
      "standalone_rewrite": "中型销售团队如何在 HubSpot 和 Salesforce 之间做 CRM 选型？",
      "retrieval_rewrite": "HubSpot Salesforce CRM 选型 中型销售团队",
      "evidence_query": "HubSpot Sales Hub Smart CRM Salesforce comparison official",
      "content_asset": "对比文章、选型矩阵",
      "priority": "P0",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q004",
      "cluster": "价格预算",
      "intent_type": "价格型",
      "question": "HubSpot 贵不贵，国内团队一年预算怎么估？",
      "standalone_rewrite": "中国团队采购 HubSpot 时如何估算订阅、席位、模块、积分和实施成本？",
      "retrieval_rewrite": "HubSpot 价格 席位 Core Seat View-Only Seat Credits 模块",
      "evidence_query": "HubSpot pricing seats credits product catalog official",
      "content_asset": "价格 FAQ、采购清单",
      "priority": "P0",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q005",
      "cluster": "替代方案",
      "intent_type": "替代型",
      "question": "国内有没有 HubSpot 的替代品，怎么选？",
      "standalone_rewrite": "中国团队寻找 HubSpot 替代方案时应比较哪些 CRM 和营销自动化能力？",
      "retrieval_rewrite": "HubSpot 替代 国产 CRM SCRM 营销自动化",
      "evidence_query": "HubSpot alternatives CRM marketing automation China",
      "content_asset": "替代方案页、对比表",
      "priority": "P0",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q006",
      "cluster": "数据合规",
      "intent_type": "风险型",
      "question": "HubSpot 在国内用会不会有客户数据合规风险？",
      "standalone_rewrite": "中国团队使用 HubSpot 管理客户数据时需要评估哪些隐私和跨境数据合规问题？",
      "retrieval_rewrite": "HubSpot 数据合规 客户数据 跨境 隐私 DPA",
      "evidence_query": "HubSpot legal privacy data processing agreement official",
      "content_asset": "合规 FAQ、风险边界模块",
      "priority": "P0",
      "compliance_level": "L3"
    },
    {
      "question_id": "Q007",
      "cluster": "营销自动化",
      "intent_type": "场景型",
      "question": "HubSpot 适合做海外线索培育和营销自动化吗？",
      "standalone_rewrite": "出海营销团队如何评估 HubSpot Marketing Hub 的线索培育和营销自动化能力？",
      "retrieval_rewrite": "HubSpot Marketing Hub lead nurturing marketing automation",
      "evidence_query": "HubSpot Marketing Hub automation campaign official",
      "content_asset": "场景页、营销知识库",
      "priority": "P1",
      "compliance_level": "L1"
    },
    {
      "question_id": "Q008",
      "cluster": "销售管理",
      "intent_type": "场景型",
      "question": "销售团队用 HubSpot 管线管理好不好用？",
      "standalone_rewrite": "销售团队如何用 HubSpot Sales Hub 和 Smart CRM 管理销售管线？",
      "retrieval_rewrite": "HubSpot Sales Hub pipeline management Smart CRM",
      "evidence_query": "HubSpot Sales Hub pipeline management official",
      "content_asset": "销售场景页、FAQ",
      "priority": "P1",
      "compliance_level": "L1"
    },
    {
      "question_id": "Q009",
      "cluster": "AI 功能",
      "intent_type": "品牌验证型",
      "question": "HubSpot 的 AI 功能 Breeze 能帮市场和销售做什么？",
      "standalone_rewrite": "HubSpot Breeze AI 在营销、销售和客服流程中有哪些官方能力？",
      "retrieval_rewrite": "HubSpot Breeze AI marketing sales service assistant agents credits",
      "evidence_query": "HubSpot Breeze AI official features product catalog",
      "content_asset": "AI 功能解释页、监测 Prompt",
      "priority": "P1",
      "compliance_level": "L1"
    },
    {
      "question_id": "Q010",
      "cluster": "实施风险",
      "intent_type": "风险型",
      "question": "HubSpot 实施会不会很复杂，迁移成本高不高？",
      "standalone_rewrite": "企业从表格、国产 CRM 或其他 SaaS 迁移到 HubSpot 时需要评估哪些实施成本？",
      "retrieval_rewrite": "HubSpot implementation migration onboarding cost",
      "evidence_query": "HubSpot onboarding implementation migration official",
      "content_asset": "实施 FAQ、项目计划输入包",
      "priority": "P1",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q011",
      "cluster": "客服服务",
      "intent_type": "场景型",
      "question": "HubSpot 能不能统一客服工单、知识库和客户历史？",
      "standalone_rewrite": "客服团队如何评估 HubSpot Service Hub 的工单、知识库和客户视图能力？",
      "retrieval_rewrite": "HubSpot Service Hub ticketing knowledge base customer view",
      "evidence_query": "HubSpot Service Hub ticketing knowledge base official",
      "content_asset": "客服场景页、知识库",
      "priority": "P1",
      "compliance_level": "L1"
    },
    {
      "question_id": "Q012",
      "cluster": "内容运营",
      "intent_type": "场景型",
      "question": "HubSpot Content Hub 适合做官网吗，和 WordPress 怎么比？",
      "standalone_rewrite": "企业如何比较 HubSpot Content Hub 与 WordPress 在官网、内容和 CRM 打通方面的差异？",
      "retrieval_rewrite": "HubSpot Content Hub WordPress 对比 官网 内容 CRM",
      "evidence_query": "HubSpot Content Hub official website content management",
      "content_asset": "内容场景页、对比 FAQ",
      "priority": "P1",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q013",
      "cluster": "数据治理",
      "intent_type": "场景型",
      "question": "HubSpot Data Hub 能解决客户数据同步和去重吗？",
      "standalone_rewrite": "企业如何评估 HubSpot Data Hub 在数据同步、去重和客户数据治理中的作用？",
      "retrieval_rewrite": "HubSpot Data Hub data sync duplicate management data governance",
      "evidence_query": "HubSpot Data Hub official data sync duplicate management",
      "content_asset": "数据治理知识库、场景页",
      "priority": "P1",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q014",
      "cluster": "商务收款",
      "intent_type": "交易型",
      "question": "HubSpot Commerce Hub 对 B2B 报价、订单和收款有什么帮助？",
      "standalone_rewrite": "B2B 团队如何评估 HubSpot Commerce Hub 在报价、订单、订阅和收款流程中的价值？",
      "retrieval_rewrite": "HubSpot Commerce Hub quote invoice subscription payment B2B",
      "evidence_query": "HubSpot Commerce Hub official quotes invoices subscriptions",
      "content_asset": "商务场景页、采购 FAQ",
      "priority": "P2",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q015",
      "cluster": "本地化协作",
      "intent_type": "风险型",
      "question": "国内团队用 HubSpot 会不会遇到语言、时区、集成和支持问题？",
      "standalone_rewrite": "中国团队使用 HubSpot 时需要评估哪些本地化协作、集成、语言和支持因素？",
      "retrieval_rewrite": "HubSpot 中国团队 本地化 集成 语言 支持",
      "evidence_query": "HubSpot integrations support localization official China",
      "content_asset": "本地化风险 FAQ",
      "priority": "P1",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q016",
      "cluster": "中小企业适配",
      "intent_type": "推荐型",
      "question": "小团队适合先用 HubSpot 免费版还是直接买付费版？",
      "standalone_rewrite": "小型 B2B 团队如何判断从 HubSpot 免费工具升级到付费 Hub 的时机？",
      "retrieval_rewrite": "HubSpot free tools Starter Professional upgrade timing",
      "evidence_query": "HubSpot free tools pricing Starter Professional official",
      "content_asset": "入门指南、价格 FAQ",
      "priority": "P1",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q017",
      "cluster": "生态集成",
      "intent_type": "品牌验证型",
      "question": "HubSpot 能和我们现有的网站、邮件、客服和数据工具打通吗？",
      "standalone_rewrite": "企业在选择 HubSpot 前应如何评估 App Marketplace、API 和现有系统集成？",
      "retrieval_rewrite": "HubSpot App Marketplace API integrations website email support data",
      "evidence_query": "HubSpot App Marketplace API integrations official",
      "content_asset": "集成知识库、采购检查表",
      "priority": "P1",
      "compliance_level": "L2"
    },
    {
      "question_id": "Q018",
      "cluster": "监测复盘",
      "intent_type": "品牌验证型",
      "question": "AI 平台回答 CRM 推荐时会不会提到 HubSpot？",
      "standalone_rewrite": "如何监测国内 AI 平台在 CRM、营销自动化和出海选型问题中是否提及 HubSpot？",
      "retrieval_rewrite": "AI 搜索 HubSpot CRM 推荐 品牌提及 监测 Prompt",
      "evidence_query": "DeepSeek 豆包 千问 Kimi 元宝 CRM 推荐 HubSpot monitoring",
      "content_asset": "监测 Prompt、月度复盘",
      "priority": "P0",
      "compliance_level": "L1"
    }
  ],
  "scoring_matrix": [
    {
      "question_id": "Q001",
      "cluster": "品牌认知",
      "business_value": 4,
      "ai_answer_probability": 4,
      "content_gap": 3,
      "brand_insert_space": 5,
      "evidence_availability": 5,
      "competition_difficulty": 3,
      "conversation_extension": 3,
      "decision_stage_value": 3,
      "platform_coverage": 5,
      "compliance_risk": 1,
      "weighted_score": 4.05,
      "priority": "P0"
    },
    {
      "question_id": "Q002",
      "cluster": "出海团队选型",
      "business_value": 5,
      "ai_answer_probability": 5,
      "content_gap": 4,
      "brand_insert_space": 5,
      "evidence_availability": 4,
      "competition_difficulty": 4,
      "conversation_extension": 5,
      "decision_stage_value": 5,
      "platform_coverage": 5,
      "compliance_risk": 2,
      "weighted_score": 4.65,
      "priority": "P0"
    },
    {
      "question_id": "Q003",
      "cluster": "竞品对比",
      "business_value": 5,
      "ai_answer_probability": 5,
      "content_gap": 4,
      "brand_insert_space": 4,
      "evidence_availability": 4,
      "competition_difficulty": 5,
      "conversation_extension": 5,
      "decision_stage_value": 5,
      "platform_coverage": 5,
      "compliance_risk": 2,
      "weighted_score": 4.55,
      "priority": "P0"
    },
    {
      "question_id": "Q004",
      "cluster": "价格预算",
      "business_value": 5,
      "ai_answer_probability": 5,
      "content_gap": 4,
      "brand_insert_space": 4,
      "evidence_availability": 4,
      "competition_difficulty": 4,
      "conversation_extension": 4,
      "decision_stage_value": 5,
      "platform_coverage": 5,
      "compliance_risk": 3,
      "weighted_score": 4.35,
      "priority": "P0"
    },
    {
      "question_id": "Q005",
      "cluster": "替代方案",
      "business_value": 5,
      "ai_answer_probability": 5,
      "content_gap": 4,
      "brand_insert_space": 4,
      "evidence_availability": 3,
      "competition_difficulty": 5,
      "conversation_extension": 5,
      "decision_stage_value": 5,
      "platform_coverage": 5,
      "compliance_risk": 2,
      "weighted_score": 4.4,
      "priority": "P0"
    },
    {
      "question_id": "Q006",
      "cluster": "数据合规",
      "business_value": 5,
      "ai_answer_probability": 4,
      "content_gap": 5,
      "brand_insert_space": 3,
      "evidence_availability": 3,
      "competition_difficulty": 4,
      "conversation_extension": 5,
      "decision_stage_value": 5,
      "platform_coverage": 5,
      "compliance_risk": 5,
      "weighted_score": 4.05,
      "priority": "P0"
    },
    {
      "question_id": "Q007",
      "cluster": "营销自动化",
      "business_value": 4,
      "ai_answer_probability": 4,
      "content_gap": 3,
      "brand_insert_space": 5,
      "evidence_availability": 4,
      "competition_difficulty": 3,
      "conversation_extension": 4,
      "decision_stage_value": 4,
      "platform_coverage": 4,
      "compliance_risk": 1,
      "weighted_score": 4.0,
      "priority": "P1"
    },
    {
      "question_id": "Q008",
      "cluster": "销售管理",
      "business_value": 4,
      "ai_answer_probability": 4,
      "content_gap": 3,
      "brand_insert_space": 5,
      "evidence_availability": 4,
      "competition_difficulty": 3,
      "conversation_extension": 4,
      "decision_stage_value": 4,
      "platform_coverage": 4,
      "compliance_risk": 1,
      "weighted_score": 4.0,
      "priority": "P1"
    },
    {
      "question_id": "Q009",
      "cluster": "AI 功能",
      "business_value": 4,
      "ai_answer_probability": 4,
      "content_gap": 4,
      "brand_insert_space": 5,
      "evidence_availability": 4,
      "competition_difficulty": 3,
      "conversation_extension": 4,
      "decision_stage_value": 4,
      "platform_coverage": 5,
      "compliance_risk": 2,
      "weighted_score": 4.1,
      "priority": "P1"
    },
    {
      "question_id": "Q010",
      "cluster": "实施风险",
      "business_value": 4,
      "ai_answer_probability": 4,
      "content_gap": 4,
      "brand_insert_space": 3,
      "evidence_availability": 3,
      "competition_difficulty": 4,
      "conversation_extension": 4,
      "decision_stage_value": 4,
      "platform_coverage": 4,
      "compliance_risk": 3,
      "weighted_score": 3.75,
      "priority": "P1"
    },
    {
      "question_id": "Q011",
      "cluster": "客服服务",
      "business_value": 4,
      "ai_answer_probability": 3,
      "content_gap": 3,
      "brand_insert_space": 5,
      "evidence_availability": 4,
      "competition_difficulty": 3,
      "conversation_extension": 3,
      "decision_stage_value": 4,
      "platform_coverage": 4,
      "compliance_risk": 1,
      "weighted_score": 3.8,
      "priority": "P1"
    },
    {
      "question_id": "Q012",
      "cluster": "内容运营",
      "business_value": 3,
      "ai_answer_probability": 3,
      "content_gap": 4,
      "brand_insert_space": 4,
      "evidence_availability": 4,
      "competition_difficulty": 4,
      "conversation_extension": 3,
      "decision_stage_value": 3,
      "platform_coverage": 3,
      "compliance_risk": 2,
      "weighted_score": 3.35,
      "priority": "P1"
    },
    {
      "question_id": "Q013",
      "cluster": "数据治理",
      "business_value": 4,
      "ai_answer_probability": 3,
      "content_gap": 4,
      "brand_insert_space": 4,
      "evidence_availability": 4,
      "competition_difficulty": 3,
      "conversation_extension": 3,
      "decision_stage_value": 4,
      "platform_coverage": 4,
      "compliance_risk": 2,
      "weighted_score": 3.75,
      "priority": "P1"
    },
    {
      "question_id": "Q014",
      "cluster": "商务收款",
      "business_value": 3,
      "ai_answer_probability": 2,
      "content_gap": 4,
      "brand_insert_space": 3,
      "evidence_availability": 3,
      "competition_difficulty": 3,
      "conversation_extension": 2,
      "decision_stage_value": 3,
      "platform_coverage": 2,
      "compliance_risk": 2,
      "weighted_score": 2.85,
      "priority": "P2"
    },
    {
      "question_id": "Q015",
      "cluster": "本地化协作",
      "business_value": 4,
      "ai_answer_probability": 4,
      "content_gap": 4,
      "brand_insert_space": 3,
      "evidence_availability": 2,
      "competition_difficulty": 3,
      "conversation_extension": 4,
      "decision_stage_value": 4,
      "platform_coverage": 4,
      "compliance_risk": 3,
      "weighted_score": 3.55,
      "priority": "P1"
    },
    {
      "question_id": "Q016",
      "cluster": "中小企业适配",
      "business_value": 4,
      "ai_answer_probability": 4,
      "content_gap": 3,
      "brand_insert_space": 4,
      "evidence_availability": 4,
      "competition_difficulty": 3,
      "conversation_extension": 4,
      "decision_stage_value": 4,
      "platform_coverage": 4,
      "compliance_risk": 2,
      "weighted_score": 3.85,
      "priority": "P1"
    },
    {
      "question_id": "Q017",
      "cluster": "生态集成",
      "business_value": 4,
      "ai_answer_probability": 3,
      "content_gap": 3,
      "brand_insert_space": 4,
      "evidence_availability": 4,
      "competition_difficulty": 3,
      "conversation_extension": 3,
      "decision_stage_value": 4,
      "platform_coverage": 3,
      "compliance_risk": 2,
      "weighted_score": 3.55,
      "priority": "P1"
    },
    {
      "question_id": "Q018",
      "cluster": "监测复盘",
      "business_value": 5,
      "ai_answer_probability": 5,
      "content_gap": 4,
      "brand_insert_space": 5,
      "evidence_availability": 3,
      "competition_difficulty": 3,
      "conversation_extension": 5,
      "decision_stage_value": 5,
      "platform_coverage": 5,
      "compliance_risk": 1,
      "weighted_score": 4.55,
      "priority": "P0"
    }
  ],
  "prompt_library": [
    {
      "prompt_id": "P001",
      "platform": "DeepSeek",
      "intent_type": "复杂决策",
      "prompt": "我们是一家中国出海 B2B SaaS 公司，销售团队 30 人，市场团队 5 人，想统一 CRM、营销自动化和客服记录。HubSpot、Salesforce、Zoho 和国产 CRM 应该怎么选？请列判断标准、预算变量、数据合规风险和适合场景。",
      "usage": "复杂选型月度采样",
      "record_fields": [
        "品牌提及",
        "竞品排序",
        "证据来源",
        "风险提示"
      ]
    },
    {
      "prompt_id": "P002",
      "platform": "豆包",
      "intent_type": "日常场景",
      "prompt": "公司想做海外客户管理和邮件营销，HubSpot 会不会太贵太复杂？适合什么团队用？",
      "usage": "口语问法采样",
      "record_fields": [
        "是否提到适用团队",
        "是否提到价格边界",
        "是否提到替代工具"
      ]
    },
    {
      "prompt_id": "P003",
      "platform": "千问",
      "intent_type": "多轮追问",
      "prompt": "HubSpot 适合中国出海公司用吗？如果我们主要做欧美 B2B 线索培育、销售跟进和客服工单，再怎么判断是否值得买？",
      "usage": "追问链路采样",
      "record_fields": [
        "追问是否保留上下文",
        "判断标准",
        "来源质量"
      ]
    },
    {
      "prompt_id": "P004",
      "platform": "Kimi",
      "intent_type": "资料整合",
      "prompt": "请用中文简体整理 HubSpot 的 Smart CRM、Marketing Hub、Sales Hub、Service Hub、Content Hub、Data Hub、Commerce Hub 和 Breeze AI 的作用，并说明中国团队选型时要确认哪些官方资料。",
      "usage": "长上下文资料整合采样",
      "record_fields": [
        "产品名是否当前",
        "来源链接",
        "待确认事项"
      ]
    },
    {
      "prompt_id": "P005",
      "platform": "元宝",
      "intent_type": "管理决策",
      "prompt": "老板想知道 HubSpot 和国产 CRM 选哪个更合适：我们做外贸和跨境销售，团队不大，但想把线索、销售、客服和内容统一起来。请给一个通俗的判断框架。",
      "usage": "管理者视角采样",
      "record_fields": [
        "通俗解释",
        "下一步动作",
        "风险提示"
      ]
    },
    {
      "prompt_id": "P006",
      "platform": "DeepSeek",
      "intent_type": "价格与合规",
      "prompt": "如果中国团队要采购 HubSpot，需要评估哪些费用变量、数据合规问题、合同条款和实施成本？请不要给法律结论，只列待确认清单。",
      "usage": "高风险边界采样",
      "record_fields": [
        "是否避免法律结论",
        "价格变量",
        "人工确认建议"
      ]
    },
    {
      "prompt_id": "P007",
      "platform": "Kimi",
      "intent_type": "竞品比较",
      "prompt": "请用中性语气比较 HubSpot、Salesforce、Zoho CRM 和国产 CRM 在出海 B2B 团队中的适用场景、预算变量、实施复杂度、数据合规待确认项，不要写未经证实的负面评价。",
      "usage": "竞品中性比较采样",
      "record_fields": [
        "是否中性",
        "是否列待确认项",
        "品牌位置"
      ]
    }
  ],
  "follow_up_chains": [
    {
      "chain_id": "C001",
      "root_question_id": "Q002",
      "parent_question_id": "Q002",
      "follow_up_level": "L1",
      "context_dependency": "省略了中国出海 B2B 场景",
      "follow_up_question": "那如果主要做欧美市场呢？",
      "standalone_rewrite": "主要做欧美市场的中国出海 B2B 公司如何评估 HubSpot 是否适合？",
      "platform_fit": "Kimi、千问"
    },
    {
      "chain_id": "C002",
      "root_question_id": "Q004",
      "parent_question_id": "Q004",
      "follow_up_level": "L1",
      "context_dependency": "承接 HubSpot 价格预算问题",
      "follow_up_question": "如果销售 30 人、市场 5 人，大概看哪些费用？",
      "standalone_rewrite": "销售 30 人、市场 5 人的团队采购 HubSpot 时应评估哪些订阅、席位、模块、积分和实施费用？",
      "platform_fit": "DeepSeek、Kimi"
    },
    {
      "chain_id": "C003",
      "root_question_id": "Q006",
      "parent_question_id": "Q006",
      "follow_up_level": "L1",
      "context_dependency": "承接客户数据合规风险",
      "follow_up_question": "客户数据放进去会不会有问题？",
      "standalone_rewrite": "中国团队把客户数据存入 HubSpot 时需要评估哪些隐私、数据处理和跨境合规问题？",
      "platform_fit": "DeepSeek、千问"
    },
    {
      "chain_id": "C004",
      "root_question_id": "Q003",
      "parent_question_id": "Q003",
      "follow_up_level": "L1",
      "context_dependency": "承接 HubSpot 与 Salesforce 对比",
      "follow_up_question": "如果我们更重视营销自动化呢？",
      "standalone_rewrite": "更重视营销自动化的 B2B 团队在 HubSpot 和 Salesforce 之间如何选择？",
      "platform_fit": "Kimi、DeepSeek"
    },
    {
      "chain_id": "C005",
      "root_question_id": "Q005",
      "parent_question_id": "Q005",
      "follow_up_level": "L1",
      "context_dependency": "承接 HubSpot 替代方案",
      "follow_up_question": "国产 CRM 会不会更适合国内团队？",
      "standalone_rewrite": "中国国内销售团队在 HubSpot 和国产 CRM 之间应如何比较本地化、数据、集成和成本？",
      "platform_fit": "豆包、元宝、千问"
    },
    {
      "chain_id": "C006",
      "root_question_id": "Q009",
      "parent_question_id": "Q009",
      "follow_up_level": "L1",
      "context_dependency": "承接 Breeze AI 能力问题",
      "follow_up_question": "那 Breeze 会额外收费吗？",
      "standalone_rewrite": "HubSpot Breeze AI 哪些能力可能涉及 HubSpot Credits 或额外费用？",
      "platform_fit": "DeepSeek、Kimi"
    },
    {
      "chain_id": "C007",
      "root_question_id": "Q010",
      "parent_question_id": "Q010",
      "follow_up_level": "L1",
      "context_dependency": "承接实施迁移成本",
      "follow_up_question": "如果我们现在用表格和企业微信客户群呢？",
      "standalone_rewrite": "从表格和企业微信客户管理迁移到 HubSpot 时需要评估哪些数据、流程和集成问题？",
      "platform_fit": "豆包、元宝、千问"
    },
    {
      "chain_id": "C008",
      "root_question_id": "Q013",
      "parent_question_id": "Q013",
      "follow_up_level": "L1",
      "context_dependency": "承接 Data Hub 数据治理问题",
      "follow_up_question": "重复客户和多个系统的数据能处理吗？",
      "standalone_rewrite": "HubSpot Data Hub 在重复客户、数据同步和多系统客户数据治理中能解决哪些问题？",
      "platform_fit": "Kimi、千问"
    },
    {
      "chain_id": "C009",
      "root_question_id": "Q018",
      "parent_question_id": "Q018",
      "follow_up_level": "L1",
      "context_dependency": "承接 AI 平台品牌提及监测",
      "follow_up_question": "怎么判断 AI 回答里对 HubSpot 的描述准不准？",
      "standalone_rewrite": "监测国内 AI 平台回答 HubSpot 相关问题时，应如何记录事实准确性、来源质量和风险断言？",
      "platform_fit": "DeepSeek、Kimi、千问"
    }
  ],
  "data_sources": [
    {
      "source_id": "D001",
      "source_type": "官方事实",
      "provider": "HubSpot Product & Services Catalog",
      "access_status": "已连接",
      "record_count": "1 个公开网页",
      "date_range": "2026-05-21 校验",
      "calibration_use": "产品线、Breeze、Seats、Credits 和限制事实校准",
      "next_action": "每次生产报告前重新校验官方目录"
    },
    {
      "source_id": "D002",
      "source_type": "官方事实",
      "provider": "HubSpot Customer Platform / Pricing page",
      "access_status": "已连接",
      "record_count": "1 个公开网页",
      "date_range": "2026-05-21 校验",
      "calibration_use": "CRM 数据统一、自动化和 AI 助手能力事实校准",
      "next_action": "补充各 Hub 独立产品页"
    },
    {
      "source_id": "D003",
      "source_type": "国内 AI 平台真实回答",
      "provider": "DeepSeek、豆包、千问、Kimi、元宝",
      "access_status": "未采样",
      "record_count": "0",
      "date_range": "无",
      "calibration_use": "品牌提及、答案排序、引用来源和风险断言校准",
      "next_action": "按 Prompt 库执行首轮采样，不得用示例 Prompt 冒充真实答案"
    },
    {
      "source_id": "D004",
      "source_type": "搜索与内容数据",
      "provider": "关键词工具、Search Console、站内搜索、内容后台",
      "access_status": "待授权",
      "record_count": "0",
      "date_range": "无",
      "calibration_use": "搜索需求规模、内容缺口和页面优先级校准",
      "next_action": "导入搜索量、点击、展示、站内搜索词和页面表现"
    },
    {
      "source_id": "D005",
      "source_type": "客户与销售数据",
      "provider": "客服系统、CRM、销售话术、客户访谈",
      "access_status": "待提供",
      "record_count": "0",
      "date_range": "无",
      "calibration_use": "真实痛点频次、商业价值和 FAQ 优先级校准",
      "next_action": "脱敏导入客服问答、销售记录、访谈纪要和流失原因"
    }
  ],
  "ai_sampling_plan": [
    {
      "sample_id": "S001",
      "platform": "DeepSeek",
      "prompt": "我们是一家中国出海 B2B SaaS 公司，销售团队 30 人，市场团队 5 人，想统一 CRM、营销自动化和客服记录。HubSpot、Salesforce、Zoho 和国产 CRM 应该怎么选？",
      "status": "未采样",
      "brand_mentioned": "待记录",
      "cited_sources": "待记录",
      "risk_flags": "价格、合规、竞品负面判断",
      "next_action": "记录答案日期、品牌位置、竞品顺序和引用来源"
    },
    {
      "sample_id": "S002",
      "platform": "豆包",
      "prompt": "公司想做海外客户管理和邮件营销，HubSpot 会不会太贵太复杂？适合什么团队用？",
      "status": "未采样",
      "brand_mentioned": "待记录",
      "cited_sources": "待记录",
      "risk_flags": "未经验证价格、过度承诺实施效果",
      "next_action": "记录口语回答是否覆盖适合谁、贵不贵和替代方案"
    },
    {
      "sample_id": "S003",
      "platform": "千问",
      "prompt": "HubSpot 适合中国出海公司用吗？如果我们主要做欧美 B2B 线索培育、销售跟进和客服工单，再怎么判断是否值得买？",
      "status": "未采样",
      "brand_mentioned": "待记录",
      "cited_sources": "待记录",
      "risk_flags": "追问链路丢失、来源缺失",
      "next_action": "记录多轮追问是否保留上下文并输出独立判断标准"
    },
    {
      "sample_id": "S004",
      "platform": "Kimi",
      "prompt": "请用中文简体整理 HubSpot 的 Smart CRM、Marketing Hub、Sales Hub、Service Hub、Content Hub、Data Hub、Commerce Hub 和 Breeze AI 的作用，并说明中国团队选型时要确认哪些官方资料。",
      "status": "未采样",
      "brand_mentioned": "待记录",
      "cited_sources": "待记录",
      "risk_flags": "产品名过期、事实混淆",
      "next_action": "记录是否正确引用当前官方产品结构"
    },
    {
      "sample_id": "S005",
      "platform": "元宝",
      "prompt": "老板想知道 HubSpot 和国产 CRM 选哪个更合适：我们做外贸和跨境销售，团队不大，但想把线索、销售、客服和内容统一起来。请给一个通俗的判断框架。",
      "status": "未采样",
      "brand_mentioned": "待记录",
      "cited_sources": "待记录",
      "risk_flags": "采购结论过强、缺少待确认项",
      "next_action": "记录管理者视角是否包含下一步确认动作"
    }
  ],
  "calibration_actions": [
    {
      "action_id": "CA001",
      "signal": "国内 AI 平台品牌提及率",
      "affected_dimensions": "AI 答案触发概率、平台覆盖度、品牌植入空间",
      "current_status": "未采样，当前为预测分",
      "method": "对 5 个平台按月采样 P0 Prompt，统计 HubSpot 是否出现、出现位置和竞品顺序",
      "owner": "监测团队"
    },
    {
      "action_id": "CA002",
      "signal": "关键词搜索量与站内搜索频次",
      "affected_dimensions": "商业价值、内容缺口、决策阶段价值",
      "current_status": "未接入",
      "method": "导入搜索量、站内搜索词和内容点击后重算问题簇权重",
      "owner": "SEO/数据分析"
    },
    {
      "action_id": "CA003",
      "signal": "客服问答与销售话术频次",
      "affected_dimensions": "内容缺口、FAQ 优先级、证据可得性",
      "current_status": "未提供",
      "method": "对脱敏文本做问题抽取、同义合并和频次统计",
      "owner": "销售支持/客服团队"
    },
    {
      "action_id": "CA004",
      "signal": "CRM 线索、成交和流失原因",
      "affected_dimensions": "商业价值、资产优先级、落地路线",
      "current_status": "待授权",
      "method": "按线索阶段、成交金额和流失原因校准 P0/P1 优先级",
      "owner": "增长/销售运营"
    }
  ],
  "content_topics": [
    {
      "topic_id": "T001",
      "title": "HubSpot 适合中国出海企业吗：从 CRM、营销自动化到客服一体化的选型框架",
      "source_question": "Q002",
      "asset_type": "选型文章",
      "evidence_need": "官方产品结构、目标团队画像、实施前提",
      "priority": "P0"
    },
    {
      "topic_id": "T002",
      "title": "HubSpot 与 Salesforce、Zoho、国产 CRM 怎么选",
      "source_question": "Q003",
      "asset_type": "对比页",
      "evidence_need": "官方功能页、公开价格、实施条件",
      "priority": "P0"
    },
    {
      "topic_id": "T003",
      "title": "HubSpot 价格怎么估：席位、模块、积分、实施和合同变量清单",
      "source_question": "Q004",
      "asset_type": "价格 FAQ",
      "evidence_need": "官方 pricing、Product Catalog、合同待确认项",
      "priority": "P0"
    },
    {
      "topic_id": "T004",
      "title": "HubSpot 在国内团队使用的数据合规待确认清单",
      "source_question": "Q006",
      "asset_type": "风险 FAQ",
      "evidence_need": "隐私政策、DPA、法务复核",
      "priority": "P0"
    },
    {
      "topic_id": "T005",
      "title": "HubSpot Breeze AI 能做什么：Assistant、Agents、Credits 与业务场景",
      "source_question": "Q009",
      "asset_type": "AI 功能解释页",
      "evidence_need": "官方 AI 页、Product Catalog",
      "priority": "P1"
    },
    {
      "topic_id": "T006",
      "title": "从表格或国产 CRM 迁移到 HubSpot 前要准备什么",
      "source_question": "Q010",
      "asset_type": "实施知识库",
      "evidence_need": "迁移流程、字段清单、实施复盘",
      "priority": "P1"
    },
    {
      "topic_id": "T007",
      "title": "HubSpot Data Hub 如何处理客户数据同步、去重和治理",
      "source_question": "Q013",
      "asset_type": "数据治理知识库",
      "evidence_need": "官方 Data Hub 能力说明",
      "priority": "P1"
    },
    {
      "topic_id": "T008",
      "title": "如何监测国内 AI 平台是否推荐 HubSpot",
      "source_question": "Q018",
      "asset_type": "监测方法页",
      "evidence_need": "Prompt 库、采样记录模板、复盘口径",
      "priority": "P0"
    }
  ],
  "faq_bank": [
    {
      "faq_id": "F001",
      "question": "HubSpot 适合中国出海公司吗？",
      "answer_boundary": "可以给选型判断框架，不能替代最终采购建议。",
      "evidence_need": "官方产品页、客户场景、团队规模和预算信息",
      "target_asset": "选型文章、品牌解释页",
      "compliance_level": "L2"
    },
    {
      "faq_id": "F002",
      "question": "HubSpot 贵不贵？",
      "answer_boundary": "只能解释价格变量，不写未经验证的成交价或折扣。",
      "evidence_need": "官方定价页、Product Catalog、报价单",
      "target_asset": "价格 FAQ",
      "compliance_level": "L2"
    },
    {
      "faq_id": "F003",
      "question": "HubSpot 和 Salesforce 怎么选？",
      "answer_boundary": "中性比较适用场景，不输出未经证实的竞品负面判断。",
      "evidence_need": "官方功能页、公开定价、实施条件",
      "target_asset": "对比页",
      "compliance_level": "L2"
    },
    {
      "faq_id": "F004",
      "question": "HubSpot 在国内使用有数据合规风险吗？",
      "answer_boundary": "不得给法律结论，必须提示法务和合规团队确认。",
      "evidence_need": "隐私政策、DPA、数据处理条款、法务复核",
      "target_asset": "合规 FAQ",
      "compliance_level": "L3"
    },
    {
      "faq_id": "F005",
      "question": "Breeze AI 是否会额外收费？",
      "answer_boundary": "只能说明官方目录中提到的 Credits 或套餐变量，不能承诺具体账单。",
      "evidence_need": "HubSpot Product Catalog、AI 页",
      "target_asset": "Breeze AI FAQ",
      "compliance_level": "L2"
    },
    {
      "faq_id": "F006",
      "question": "HubSpot 实施周期多久？",
      "answer_boundary": "不能承诺上线周期，只列影响周期的变量。",
      "evidence_need": "实施范围、数据量、集成清单、团队资源",
      "target_asset": "实施 FAQ",
      "compliance_level": "L2"
    },
    {
      "faq_id": "F007",
      "question": "小团队可以先用免费版吗？",
      "answer_boundary": "可以说明升级判断变量，不替代具体采购方案。",
      "evidence_need": "官方 Free Tools、Starter、Professional 功能说明",
      "target_asset": "入门指南",
      "compliance_level": "L2"
    },
    {
      "faq_id": "F008",
      "question": "HubSpot 能和现有系统打通吗？",
      "answer_boundary": "只能列评估方向，具体集成可行性需要技术确认。",
      "evidence_need": "App Marketplace、API 文档、现有系统清单",
      "target_asset": "集成知识库",
      "compliance_level": "L2"
    }
  ],
  "knowledge_base_entries": [
    {
      "entry_id": "K001",
      "title": "HubSpot 产品线与 Smart CRM 基础概念",
      "entry_type": "解释型",
      "covered_questions": "Q001、Q009、Q013、Q014",
      "required_materials": "官方产品目录、产品页",
      "owner": "内容策略"
    },
    {
      "entry_id": "K002",
      "title": "HubSpot 价格变量与采购待确认清单",
      "entry_type": "价格型",
      "covered_questions": "Q004、Q016",
      "required_materials": "官方 pricing、Product Catalog、报价资料",
      "owner": "销售/采购"
    },
    {
      "entry_id": "K003",
      "title": "HubSpot 数据合规与隐私待确认清单",
      "entry_type": "风险型",
      "covered_questions": "Q006、Q015",
      "required_materials": "隐私政策、DPA、法务复核",
      "owner": "合规/IT"
    },
    {
      "entry_id": "K004",
      "title": "HubSpot 与 Salesforce、Zoho、国产 CRM 选型维度",
      "entry_type": "比较型",
      "covered_questions": "Q003、Q005",
      "required_materials": "官方功能页、公开资料、竞品矩阵",
      "owner": "GEO 运营"
    },
    {
      "entry_id": "K005",
      "title": "从表格或旧 CRM 迁移到 HubSpot 的准备清单",
      "entry_type": "流程型",
      "covered_questions": "Q010、Q017",
      "required_materials": "字段清单、集成清单、迁移方案",
      "owner": "实施/运营"
    },
    {
      "entry_id": "K006",
      "title": "国内 AI 平台 HubSpot 监测 Prompt 复盘方法",
      "entry_type": "监测型",
      "covered_questions": "Q018",
      "required_materials": "Prompt 库、采样记录、品牌提及数据",
      "owner": "监测团队"
    }
  ],
  "evidence_sources": [
    {
      "source": "HubSpot Product & Services Catalog",
      "level": "A",
      "use": "产品线、Breeze、Credits、功能和限制事实校准",
      "url": "https://legal.hubspot.com/hubspot-product-and-services-catalog",
      "status": "已用于示例事实校准"
    },
    {
      "source": "HubSpot Customer Platform / Pricing page",
      "level": "A",
      "use": "CRM 数据统一、自动化和 AI 助手能力事实校准",
      "url": "https://www.hubspot.com/products/pricing-cr115",
      "status": "已用于示例事实校准"
    },
    {
      "source": "HubSpot Breeze AI page",
      "level": "A",
      "use": "Breeze AI 能力线索和案例线索",
      "url": "https://www.hubspot.com/products/artificial-intelligence",
      "status": "作为后续内容证据线索"
    },
    {
      "source": "Broder, A taxonomy of web search",
      "level": "A",
      "use": "搜索意图任务层分类",
      "url": "https://sigir.org/files/forum/F2002/broder.pdf",
      "status": "已转化为方法基线"
    },
    {
      "source": "TREC CAsT 2020 Overview",
      "level": "A",
      "use": "会话搜索、追问链路和查询重写依据",
      "url": "https://pages.nist.gov/trec-browser/trec29/cast/overview/",
      "status": "已转化为方法基线"
    },
    {
      "source": "Query Expansion by Prompting Large Language Models",
      "level": "A",
      "use": "LLM 查询扩展和五段式重写依据",
      "url": "https://arxiv.org/abs/2305.03653",
      "status": "已转化为方法基线"
    },
    {
      "source": "BEIR Benchmark",
      "level": "A",
      "use": "跨域检索评测与证据查询依据",
      "url": "https://arxiv.org/abs/2104.08663",
      "status": "已转化为方法基线"
    },
    {
      "source": "Google Helpful, Reliable, People-First Content",
      "level": "A",
      "use": "内容可信度和报告披露依据",
      "url": "https://developers.google.com/search/docs/fundamentals/creating-helpful-content",
      "status": "已转化为报告质量要求"
    }
  ],
  "action_roadmap": [
    {
      "phase": "0-30 天",
      "task": "完成 P0 问题底座和首轮 AI 平台采样",
      "deliverable": "P0 问题库、选型页大纲、价格 FAQ、风险 FAQ、Prompt 库",
      "owner": "GEO 运营/内容策略",
      "acceptance": "P0 问题均有证据查询、资产映射和合规边界"
    },
    {
      "phase": "0-30 天",
      "task": "建设 HubSpot 品牌解释页和产品线知识库",
      "deliverable": "Smart CRM、各 Hub、Breeze、Data Hub、Commerce Hub 基础条目",
      "owner": "内容团队",
      "acceptance": "产品名与官方目录一致，附证据来源"
    },
    {
      "phase": "31-60 天",
      "task": "产出竞品中性对比和价格变量说明",
      "deliverable": "HubSpot vs Salesforce/Zoho/国产 CRM 对比页、采购清单",
      "owner": "SEO/销售支持",
      "acceptance": "不出现未经证实的竞品负面断言"
    },
    {
      "phase": "31-60 天",
      "task": "补齐场景页和 FAQ",
      "deliverable": "营销、销售、客服、数据治理、Breeze AI 场景页",
      "owner": "内容策略/产品营销",
      "acceptance": "P1 问题至少 70% 进入内容排期"
    },
    {
      "phase": "61-90 天",
      "task": "接入真实数据校准评分",
      "deliverable": "搜索量、站内搜索、客服问答、销售反馈和 AI 采样复盘表",
      "owner": "监测团队/数据分析",
      "acceptance": "评分矩阵按真实数据调整一次"
    },
    {
      "phase": "持续迭代",
      "task": "按月复盘国内 AI 平台答案",
      "deliverable": "品牌提及、引用来源、竞品排序、风险断言月报",
      "owner": "GEO 运营",
      "acceptance": "每月更新 Prompt 库和 P0/P1 优先级"
    }
  ]
}
