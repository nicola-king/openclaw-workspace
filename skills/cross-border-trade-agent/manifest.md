{
  "name": "cross-border-trade-agent",
  "version": "12.0.0",
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
    },
    "skill-registry": {
      "version": "1.0.0",
      "path": "modules/skill-registry",
      "dependencies": [
        "cross-border-core"
      ],
      "description": "🆕 Skill 注册中心：标准化注册/动态发现/延迟加载/跨 Bot 调用"
    },
    "orchestrator": {
      "version": "1.0.0",
      "path": "modules/orchestrator",
      "dependencies": [
        "cross-border-core",
        "skill-registry"
      ],
      "description": "🆕 冷启动编排器：产品 Idea → 30分钟完整跨境方案 + 运营诊断"
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
---

## P1 合并 (2026-05-25)

**28个模块 → 18个活跃模块**

### 合并映射

| 新位置 | 合并来源 | 旧模块被标记为 |
|--------|---------|--------------|
| `modules/service-layer/` (新建) | quote-engine, product-catalog, supplier-matcher, contract-legal, compliance-engine, risk-manager, payment-settlement, transaction-support, supply-chain | `[MERGED → service-layer]` |
| `modules/cross-border-core/` (吸收) | self-evolution, skill-registry, task-scheduler, data-integrator | `[MERGED → cross-border-core]` |
| `modules/geo-outbound/` (吸收) | conversion-optimizer, cultural-adapter | `[MERGED → geo-outbound]` |
| `modules/company-enricher/` (吸收) | real-data-verifier | `[MERGED → company-enricher]` |
| `modules/data/` | 空目录 | [已移除] |

### 活跃模块清单 (18个)

| 模块 | 描述 |
|------|------|
| `buyer-intel` | P0核心 — 买家情报引擎 |
| `company-enricher` | P0核心 — 公司富化+7源验证 |
| `orchestrator` | P0核心 — 冷启动编排+自动触发 |
| `trade-profile` | P0核心 — 贸易画像跨模块传播 |
| `intelligence-hub` | 情报中心 —5版块归一化 |
| `geo-outbound` | GEO优化 — 含转化优化+文化适配 |
| `guike-zhilu` | 贵客之路 — 搜索→触达→培育 |
| `cross-border-core` | 核心框架 — 含调度/自进化/数据整合 |
| `report-engine` | 报告系统 |
| `service-layer` | **新建** — 统一入口(报价/合同/合规/支付/风控) |
| 另有8个配置/工具/数据目录 | |

### P2 三项优化 (2026-05-25)

1. **P2-1**: 报价引擎一键生成（含退税自动计算+利润明细）→ `P2QuoteOptimizer`
2. **P2-2**: 合同模板（中东专版）自动化填充 → `P2ContractOptimizer`
3. **P2-3**: 合规验证一键出报告 → `P2ComplianceOptimizer`

---

## 架构变更 (2026-05-25)

### P0 自动化
- buyer-intel 全自动化：cron爬虫(06:00/18:00) + 冷启动自动触发(工作日07:00/19:00)
- trade-profile Agent 激活：用户画像跨模块传播
- ABN 自动验证集成到 company-enricher

### P1 模块合并 (28→18活跃) + 数据验证去重
- `service-layer/` — 9模块统一入口（报价/产品/供应商/合同/合规/风控/支付/交易/供应链）
- `data-verifier-dedup/` — **新增** 数据验证+去重+质量评分
- `geo-outbound` 吸收 conversion-optimizer + cultural-adapter
- `company-enricher` 吸收 real-data-verifier
- `cross-border-core` 吸收 self-evolution/skill-registry/task-scheduler/data-integrator

### P2 三项优化 (service-layer 内置)
1. P2-1 选题优化 → `P2TopicOptimizer`
2. P2-2 审核优化 → `P2ReviewOptimizer`
3. P2-3 API 优化 → `P2ApiOptimizer`
