{
  "name": "cross-border-trade-agent",
  "version": "10.0.0",
  "description": "太一跨境贸易 Agent v10.0 - 穿透式蒸馏 · 模块化 · 自进化",
  "author": "太一 AGI",
  "license": "MIT",
  "distillation_sources": [
    "宪法层: Elon 五步算法, 负熵法则, 冰山理论, 第一性原理, 二阶思维",
    "策略层: 流量优先策略, 情报引流策略, 开源引流策略, 反封号策略",
    "能力层: 天机 (聪明钱追踪), 金融情报 Agent, 知几情绪, 山木内容",
    "架构层: 跨域融合矩阵, Bot 协作协议, 任务委派协议"
  ],
  "modules": {
    "cross-border-core": {
      "version": "10.0.0",
      "path": "modules/cross-border-core",
      "dependencies": [],
      "description": "核心框架/路由/调度/事件总线/Bot 协作/跨域融合",
      "distilled_from": [
        "太一总控",
        "Bot 协作协议",
        "跨域融合矩阵"
      ]
    },
    "guike-zhilu": {
      "version": "10.0.0",
      "path": "modules/guike-zhilu",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "贵客之路闭环：搜寻→清洗→触达→培育 + 情报引流",
      "distilled_from": [
        "贵客之路",
        "情报引流策略"
      ]
    },
    "geo-outbound": {
      "version": "10.0.0",
      "path": "modules/geo-outbound",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "GEO 外贸开发：市场分析→潜客名单→内容营销→监测优化 + 流量优先 + 开源引流",
      "distilled_from": [
        "GEO 优化",
        "流量优先策略",
        "开源引流策略",
        "山木内容"
      ]
    },
    "data-integrator": {
      "version": "10.0.0",
      "path": "modules/data-integrator",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "7+ 大数据源整合：海关/电商/互联网/搜索/报告/物流/广告",
      "distilled_from": [
        "7 大数据源",
        "互联网平台 Top30"
      ]
    },
    "intelligence-hub": {
      "version": "10.0.0",
      "path": "modules/intelligence-hub",
      "dependencies": [
        "cross-border-core",
        "data-integrator"
      ],
      "description": "智能分析中心：天机+知几+Elon 质疑→竞品分析/选品评分/趋势预测/聪明钱",
      "distilled_from": [
        "天机 (聪明钱追踪)",
        "知几情绪",
        "Elon 五步算法",
        "冰山理论"
      ]
    },
    "conversion-optimizer": {
      "version": "10.0.0",
      "path": "modules/conversion-optimizer",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "转化优化中心：二阶思维→漏斗分析/ROI 追踪/渠道对比/A-B 测试",
      "distilled_from": [
        "二阶思维",
        "漏斗分析"
      ]
    },
    "transaction-support": {
      "version": "10.0.0",
      "path": "modules/transaction-support",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "交易支持中心：物流优化/价格对比/销售预测/多语言客服 + 金融情报",
      "distilled_from": [
        "金融情报 Agent",
        "物流优化",
        "销售预测"
      ]
    },
    "self-evolution": {
      "version": "10.0.0",
      "path": "modules/self-evolution",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "自我进化系统：宪法学习循环 + 技能结晶 + Token 优化 + Elon 质疑",
      "distilled_from": [
        "宪法层",
        "Elon 五步算法",
        "负熵法则",
        "技能结晶"
      ]
    },
    "report-engine": {
      "version": "10.0.0",
      "path": "modules/report-engine",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "报告系统：智能报告/推送/ES 引擎/Markdown 生成",
      "distilled_from": [
        "报告系统",
        "智能推送"
      ]
    },
    "real-data-verifier": {
      "version": "10.0.0",
      "path": "modules/real-data-verifier",
      "dependencies": [
        "cross-border-core",
        "data-integrator"
      ],
      "description": "真实数据验证：公司验证/电话验证/邮箱验证/官网验证",
      "distilled_from": [
        "七源验证",
        "公司验证"
      ]
    },
    "task-scheduler": {
      "version": "10.0.0",
      "path": "modules/task-scheduler",
      "dependencies": [
        "cross-border-core",
        "report-engine",
        "intelligence-hub",
        "self-evolution"
      ],
      "description": "任务调度中心：情报推送/竞品监控/任务自检/月度战略/委派协议",
      "distilled_from": [
        "定时任务",
        "任务委派协议"
      ]
    },
    "compliance-engine": {
      "version": "10.0.0",
      "path": "modules/compliance-engine",
      "dependencies": [
        "cross-border-core",
        "data-integrator"
      ],
      "description": "🆕 合规与清关自动化：法规追踪/合规检查/清关自动化/关税计算",
      "distilled_from": [
        "海关数据",
        "法规库",
        "认证标准",
        "负熵法则"
      ]
    },
    "risk-manager": {
      "version": "10.0.0",
      "path": "modules/risk-manager",
      "dependencies": [
        "cross-border-core",
        "intelligence-hub"
      ],
      "description": "🆕 风险管理与对冲：风险识别/预警系统/对冲策略/二阶思维分析",
      "distilled_from": [
        "二阶思维",
        "天机风控",
        "知几情绪",
        "反封号策略"
      ]
    },
    "cultural-adapter": {
      "version": "10.0.0",
      "path": "modules/cultural-adapter",
      "dependencies": [
        "cross-border-core",
        "geo-outbound"
      ],
      "description": "🆕 跨文化本地化：文化适配/多语言内容/本地化策略/山木内容蒸馏",
      "distilled_from": [
        "山木内容",
        "GEO 本地化",
        "多语言客服",
        "流量优先"
      ]
    },
    "supply-chain": {
      "version": "10.0.0",
      "path": "modules/supply-chain",
      "dependencies": [
        "cross-border-core",
        "transaction-support"
      ],
      "description": "🆕 供应链全链路：供应商管理/库存优化/物流调度/需求预测",
      "distilled_from": [
        "物流优化",
        "供应商匹配",
        "销售预测",
        "天机趋势",
        "冰山理论"
      ]
    },
    "payment-settlement": {
      "version": "10.0.0",
      "path": "modules/payment-settlement",
      "dependencies": [
        "cross-border-core",
        "transaction-support"
      ],
      "description": "🆕 支付结算与汇率管理：支付通道/汇率管理/结算优化/金融情报融合",
      "distilled_from": [
        "金融情报 Agent",
        "天机汇率预测",
        "二阶思维",
        "价格对比"
      ]
    },
    "contract-legal": {
      "version": "10.0.0",
      "path": "modules/contract-legal",
      "dependencies": [
        "cross-border-core",
        "compliance-engine"
      ],
      "description": "🆕 合同与法律支持：合同生成/法律审查/条款库/合规框架",
      "distilled_from": [
        "合同模板",
        "法律框架",
        "合规要求",
        "宪法级合规"
      ]
    },
    "company-enricher": {
      "version": "1.0.0",
      "path": "modules/company-enricher",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "公司信息增强：ABN查询/官网爬取/地址验证/邮箱发现/LinkedIn关联"
    }
  },
  "shared": {
    "api": "shared/api",
    "utils": "shared/utils"
  },
  "install": {
    "script": "deploy/install.sh",
    "uninstall": "deploy/uninstall.sh",
    "update": "deploy/update.sh"
  },
  "evolution": {
    "dimensions": 7,
    "trade_evolution": "+8%/代",
    "insight_evolution": "+10%/代",
    "solution_evolution": "+12%/代",
    "strategy_evolution": "+10%/代",
    "compliance_evolution": "+15%/代",
    "cultural_evolution": "+12%/代",
    "recursive_optimization": "≥85%"
  }
}