# 🏗️ 跨境贸易 Agent v8.4 详细架构

> **版本**: v8.4 (获客之王完全融合版)  
> **创建**: 2026-04-18 23:45  
> **作者**: 太一 AGI  
> **定位**: 跨境贸易全流程自动化架构文档

---

## 📐 系统架构总览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        跨境贸易 Agent v8.4                               │
│                    获客之王完全融合架构                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           用户交互层 (User Layer)                        │
├─────────────────────────────────────────────────────────────────────────┤
│  Telegram  │  微信  │  Web UI  │  CLI  │  API  │  Dashboard            │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                         智能路由层 (Router Layer)                        │
├─────────────────────────────────────────────────────────────────────────┤
│  任务识别  │  模型调度  │  技能路由  │  优先级队列  │  HIR 复核触发          │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        核心业务层 (Core Business Layer)                  │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    获客之王闭环 (Acquisition Loop)               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │ 全网搜寻 │→ │ 线索清洗 │→ │ 自动触达 │→ │ 线索培育 │       │   │
│  │  │ Search   │  │ Clean    │  │ Outreach │  │ Nurture  │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    智能决策中心 (Decision Center)                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │ 选品评分 │  │ 厂家推荐 │  │ 竞品分析 │  │ 趋势预测 │       │   │
│  │  │ Scoring  │  │ Manufacturer│Competitor│ Forecast │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    转化优化中心 (Conversion Center)              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │ 漏斗分析 │  │ ROI 追踪  │  │ 渠道对比 │  │ A/B 测试  │       │   │
│  │  │ Funnel   │  │ ROI      │  │ Channel  │  │ A/B Test │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    交易支持中心 (Transaction Center)             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │ 物流优化 │  │ 价格对比 │  │ 销售预测 │  │ 多语言客服│      │   │
│  │  │ Logistics│  │ Price    │  │ Sales    │  │ Support  │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        数据整合层 (Data Integration Layer)               │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 海关数据 │  │ 电商数据 │  │ 互联网  │  │ 搜索引擎 │              │
│  │ Customs  │  │ Ecommerce│  │ Platforms│  │ Search   │              │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 第三方  │  │ 物流数据 │  │ Google  │  │ 厂家数据 │              │
│  │ Reports  │  │ Logistics│  │ Ads     │  │ Suppliers│              │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        基础设施层 (Infrastructure Layer)                 │
├─────────────────────────────────────────────────────────────────────────┤
│  OpenClaw Gateway  │  SQLite/JSON  │  Redis  │  Cron  │  Git           │
│  模型调度 (Qwen/Gemini) │  文件存储  │  日志系统  │  监控告警            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 模块分层架构

### Layer 1: 用户交互层

| 模块 | 接口 | 协议 | 用途 |
|------|------|------|------|
| Telegram Bot | API | HTTPS | 消息推送/交互 |
| 微信 | API | HTTPS | 中国市场触达 |
| Web UI | HTTP | REST API | 可视化界面 |
| CLI | 命令行 | Local | 开发者工具 |
| API | REST | JSON | 第三方集成 |
| Dashboard | Web | WebSocket | 实时监控 |

---

### Layer 2: 智能路由层

| 模块 | 文件 | 功能 |
|------|------|------|
| 任务识别 | `task_orchestrator.py` | 50+ Agent 协同/7 种任务类型 |
| 模型调度 | `smart_model_router.py` | 百炼→Gemini→本地 |
| 技能路由 | `smart_router.py` | 根据任务类型/成本/延迟 |
| 优先级队列 | `priority_queue.py` | P0/P1/P2/P3 优先级 |
| HIR 复核触发 | `hir_review.py` | 高意向客户人工复核 |

---

### Layer 3: 核心业务层

#### 3.1 获客之王闭环 (Acquisition Loop)

| 步骤 | 模块 | 文件 | 功能 |
|------|------|------|------|
| **1. 全网搜寻** | prospect_search | `prospect_search.py` | 7 大数据源整合/冰山理论蒸馏 |
| **2. 线索清洗** | data_verification | `data_verification.py` | 数据验证/智能分级 (S/A/B/C) |
| **3. 自动触达** | auto_outreach | `auto_outreach_module.py` | 5 渠道/智能话术/HIR 复核 |
| **4. 线索培育** | lead_nurturing | `lead_nurturing_module.py` | 4 阶段流程/持续跟进 |

#### 3.2 智能决策中心 (Decision Center)

| 模块 | 文件 | 功能 | 权重 |
|------|------|------|------|
| 选品评分 | `product_scoring_module.py` | 5 大维度评分 | - |
| 厂家推荐 | `manufacturer_recommendation_module.py` | 真实厂家推荐 | - |
| 竞品分析 | (内置于 scoring) | 价格/策略/动态 | 20% |
| 趋势预测 | `product_trend_forecaster.py` | 时间序列分析 | 30% |

**5 大维度评分权重**:
- 趋势数据：30%
- 搜索关键词：25%
- 竞品数据：20%
- 利润率：15%
- 社交声量：10%

#### 3.3 转化优化中心 (Conversion Center)

| 模块 | 文件 | 功能 |
|------|------|------|
| 漏斗分析 | `conversion_funnel_module.py` | 7 阶段转化追踪 |
| ROI 追踪 | (内置于 funnel) | 成本/收入/效率计算 |
| 渠道对比 | `multi_channel_outreach_module.py` | 5 渠道效果对比 |
| A/B 测试 | (内置于 multi_channel) | 话术/时间/内容优化 |

**7 阶段转化漏斗**:
1. 线索获取 → 2. 线索清洗 → 3. 首次触达
4. 互动培育 → 5. 商机确认 → 6. 报价谈判
7. 成交

#### 3.4 交易支持中心 (Transaction Center)

| 模块 | 文件 | 功能 |
|------|------|------|
| 物流优化 | `logistics_optimizer.py` | 海运/空运/快递/中欧班列 |
| 价格对比 | `price_comparator.py` | 跨平台比价 (20+ 平台) |
| 销售预测 | `sales_forecaster.py` | 12 个月 AI 预测 |
| 多语言客服 | `multilingual_support.py` | 10 种语言支持 |

---

### Layer 4: 数据整合层

#### 7 大数据源

| 数据源 | 文件 | 覆盖范围 | 更新频率 |
|--------|------|---------|---------|
| 全球海关数据 | `global_customs_integrator.py` | 9 大官方机构 | 每周 |
| 电商销售数据 | `ecommerce_integrator.py` | Top 20 平台 | 每日 |
| 互联网平台 | `internet_platforms_integrator.py` | Top 30 平台 | 每日 |
| 搜索引擎 | `search_engines_integrator.py` | Top 10 引擎 | 每日 |
| 第三方报告 | `third_party_reports_integrator.py` | 10 大机构 | 每月 |
| 海陆空运输 | `logistics_integrator.py` | 6 大来源 | 每周 |
| Google Ads | `google_ads_integrator.py` | 全球广告数据 | 每日 |

#### 冰山理论数据蒸馏

```
水面以上 (10%) - 可见数据:
• 海关出口数据
• 电商销售排名
• 搜索趋势
• 价格信息

水面以下 (90%) - 深层洞察:
• 市场机会分析
• 竞争格局
• 风险因素
• 战略建议
```

---

### Layer 5: 基础设施层

| 组件 | 技术 | 用途 |
|------|------|------|
| OpenClaw Gateway | OpenClaw 4.11 | 消息路由/技能调度 |
| 数据库 | SQLite/JSON | 数据存储 |
| 缓存 | Redis | 高性能缓存 |
| 定时任务 | Cron | 每日/每周/每月任务 |
| 版本控制 | Git | 代码管理 |
| 模型调度 | Qwen/Gemini/本地 | 智能模型路由 |
| 文件存储 | Local FS | 报告/日志存储 |
| 日志系统 | Python logging | 系统日志 |
| 监控告警 | scheduler-monitor.py | 健康检查/告警 |

---

## 🔄 数据流架构

### 获客闭环数据流

```
用户请求
    ↓
[1] prospect_search.py
    ├─→ 7 大数据源查询
    ├─→ 冰山理论蒸馏
    └─→ 输出：50+ 意向客户
    ↓
[2] data_verification.py
    ├─→ 数据验证
    ├─→ 智能分级 (S/A/B/C)
    └─→ 输出：45 家验证通过客户
    ↓
[3] auto_outreach_module.py
    ├─→ 生成个性化话术
    ├─→ 选择触达渠道 (5 大渠道)
    ├─→ HIR 复核判断 (置信度评估)
    ├─→ HIR 复核队列 (S/A 级客户)
    └─→ 输出：自动触达 + 人工复核
    ↓
[4] lead_nurturing_module.py
    ├─→ 4 阶段培育流程
    ├─→ 持续跟进
    └─→ 输出：商机确认
    ↓
[5] conversion_funnel_module.py
    ├─→ 转化漏斗追踪
    ├─→ ROI 计算
    └─→ 输出：转化报告 + 优化建议
    ↓
[6] multi_channel_outreach_module.py
    ├─→ 渠道效果对比
    ├─→ A/B 测试优化
    └─→ 输出：渠道优化建议
    ↓
成交 → 订单管理 → 物流 → 售后
```

---

## 📁 文件系统架构

```
cross-border-trade-agent/
│
├── 📂 获客模块 (Acquisition)
│   ├── prospect_search.py              # 全网全域搜寻
│   ├── data_verification.py            # 深度线索清洗
│   ├── auto_outreach_module.py         # 自动触达 (5 渠道)
│   ├── lead_nurturing_module.py        # 线索培育 (S/A/B/C)
│   ├── hir_review.py                   # HIR 人工复核 (新增)
│   └── outreach_templates/             # 话术模板库
│       ├── email_templates.json
│       ├── whatsapp_templates.json
│       └── telegram_templates.json
│
├── 📂 转化模块 (Conversion)
│   ├── conversion_funnel_module.py     # 转化漏斗分析
│   ├── multi_channel_outreach_module.py # 全渠道扩展
│   ├── ab_test_manager.py              # A/B 测试管理 (新增)
│   └── roi_tracker.py                  # ROI 追踪 (新增)
│
├── 📂 决策模块 (Decision)
│   ├── product_scoring_module.py       # 智能选品评分
│   ├── manufacturer_recommendation_module.py # 厂家推荐
│   ├── competitor_analysis.py          # 竞品分析 (新增)
│   └── trend_forecasting.py            # 趋势预测 (新增)
│
├── 📂 交易支持模块 (Transaction)
│   ├── logistics_optimizer.py          # 物流优化
│   ├── price_comparator.py             # 价格对比
│   ├── sales_forecaster.py             # 销售预测
│   └── multilingual_support.py         # 多语言客服
│
├── 📂 数据整合模块 (Data Integration)
│   ├── data_integration_center.py      # 数据整合中心
│   ├── global_customs_integrator.py    # 海关数据
│   ├── ecommerce_integrator.py         # 电商数据
│   ├── internet_platforms_integrator.py # 互联网平台
│   ├── search_engines_integrator.py    # 搜索引擎
│   ├── third_party_reports_integrator.py # 第三方报告
│   ├── logistics_integrator.py         # 物流数据
│   └── google_ads_integrator.py        # Google Ads
│
├── 📂 路由调度模块 (Router)
│   ├── task_orchestrator.py            # 任务调度
│   ├── smart_model_router.py           # 模型路由
│   └── smart_router.py                 # 技能路由
│
├── 📂 自进化模块 (Self-Evolution)
│   ├── darwin_evolution.py             # 达尔文进化
│   ├── self_learning.py                # 自学习
│   └── knowledge_base.py               # 知识库
│
├── 📂 监控告警模块 (Monitoring)
│   ├── scheduler-monitor.py            # Scheduler 监控
│   ├── hourly-health-check.py          # 每小时健康检查
│   └── alert_manager.py                # 告警管理
│
├── 📂 配置文件 (Config)
│   ├── config.json                     # 主配置
│   ├── channels_config.json            # 渠道配置
│   ├── hir_config.json                 # HIR 配置
│   └── scoring_weights.json            # 评分权重
│
├── 📂 数据目录 (Data)
│   ├── cross-border/
│   │   ├── product-scoring/            # 评分报告
│   │   ├── manufacturers/              # 厂家数据
│   │   ├── leads/                      # 线索数据
│   │   ├── outreach/                   # 触达记录
│   │   ├── funnel/                     # 漏斗分析
│   │   └── channels/                   # 渠道分析
│   └── memory/                         # 记忆存储
│
├── 📂 报告目录 (Reports)
│   ├── daily/                          # 日报
│   ├── weekly/                         # 周报
│   ├── monthly/                        # 月报
│   └── adhoc/                          # 临时报告
│
├── 📂 文档 (Documentation)
│   ├── README.md                       # 项目说明
│   ├── COMPLETE_WORKFLOW.md            # 完整工作流程
│   ├── ARCHITECTURE_V84.md             # 架构文档 (本文件)
│   ├── LEARNING_DISTILLATION_REPORT.md # 深度学习报告
│   └── API.md                          # API 文档
│
└── 📂 测试 (Tests)
    ├── test_prospect_search.py
    ├── test_auto_outreach.py
    ├── test_lead_nurturing.py
    └── test_conversion_funnel.py
```

---

## 🔐 HIR (High-Intent Review) 架构

### HIR 工作流程

```
线索分级完成
    ↓
判断等级
    ├── S 级 (90+ 分) → HIR 必须复核 ✅
    ├── A 级 (75-89 分) → HIR 必须复核 ✅
    ├── B 级 (50-74 分) → HIR 可选复核
    └── C 级 (0-49 分) → 自动触达
    ↓
置信度评估
    ├── 置信度 < 80% → HIR 复核
    └── 置信度 ≥ 80% → 可自动发送
    ↓
HIR 复核队列
    ├── 人工审核
    ├── 修改话术 (可选)
    ├── 批准发送
    └── 记录决策
    ↓
发送触达
    └── 追踪回复
```

### HIR 配置文件

```json
{
  "hir_config": {
    "enabled": true,
    "review_threshold": 0.80,
    "high_priority_review": true,
    "grades_requiring_review": ["S", "A"],
    "review_timeout_hours": 24,
    "auto_approve_after_timeout": false,
    "reviewers": ["user@example.com"],
    "notification_channels": ["telegram", "email"]
  }
}
```

---

## 📊 性能指标架构

### 核心 KPI

| 指标 | 计算公式 | 目标值 |
|------|---------|--------|
| 触达效率 | 触达数量/时间 | +300% |
| 转化率 | 成交客户/总线索 | 12.5% |
| 人力成本 | 人工时间/总时间 | -70% |
| ROI | (收入 - 成本)/成本 | 250% |
| 线索响应时间 | 首次触达时间 | <1 小时 |
| HIR 复核通过率 | 批准发送/提交复核 | >80% |
| 渠道回复率 | 回复数量/发送数量 | >25% |
| 漏斗转化率 | 各阶段转化比 | 行业基准 +20% |

---

## 🎯 部署架构

### 本地部署

```
┌─────────────────────────────────────┐
│         用户设备 (Local)             │
├─────────────────────────────────────┤
│  OpenClaw Gateway                   │
│  ├── cross-border-trade-agent       │
│  ├── Python 3.11+                   │
│  ├── SQLite/JSON Storage            │
│  └── Cron Jobs                      │
└─────────────────────────────────────┘
```

### 云端部署

```
┌─────────────────────────────────────┐
│         云服务器 (VPS)               │
├─────────────────────────────────────┤
│  Docker Container                   │
│  ├── OpenClaw Gateway               │
│  ├── cross-border-trade-agent       │
│  ├── Redis Cache                    │
│  └── PostgreSQL                     │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│         用户设备 (Remote)            │
├─────────────────────────────────────┤
│  Telegram/微信/Web UI               │
└─────────────────────────────────────┘
```

---

## 🔗 外部集成架构

### API 集成

| 服务 | 用途 | 频率限制 |
|------|------|---------|
| Google Trends | 搜索趋势 | 免费 |
| Amazon API | 电商数据 | 按需 |
| Alibaba API | 供应商数据 | 按需 |
| Telegram Bot API | 消息推送 | 30 消息/秒 |
| 微信 API | 中国市场 | 按需 |
| LinkedIn API | B2B 开发 | 有限制 |
|海关数据 API | 进出口数据 | 付费 |

---

## 📈 扩展性架构

### 水平扩展

- ✅ 多实例部署 (Redis 共享状态)
- ✅ 分布式任务队列 (Celery)
- ✅ 数据库读写分离

### 垂直扩展

- ✅ 模块插件化 (新增技能无需改动核心)
- ✅ 配置驱动 (JSON 配置热更新)
- ✅ API 标准化 (RESTful 接口)

---

## 🛡️ 安全架构

### 数据安全

- ✅ 本地存储 (隐私保护)
- ✅ 敏感信息加密 (API Keys)
- ✅ HIR 人工复核 (防止误发)
- ✅ 访问控制 (权限管理)

### 合规性

- ✅ GDPR 合规 (欧洲客户数据)
- ✅ 反垃圾邮件 (CAN-SPAM)
- ✅ 渠道政策遵守 (LinkedIn/微信)

---

## 📊 监控告警架构

```
┌─────────────────────────────────────┐
│         监控系统                     │
├─────────────────────────────────────┤
│  scheduler-monitor.py               │
│  ├── 每 5 分钟检查                   │
│  ├── 健康状态评估                   │
│  ├── 告警触发 (冷却 120 分钟)          │
│  └── Telegram 推送                   │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│         自愈系统                     │
├─────────────────────────────────────┤
│  hourly-health-check.py             │
│  ├── 每小时执行                     │
│  ├── 自动修复脚本                   │
│  └── 结果验证                       │
└─────────────────────────────────────┘
```

---

## 🎊 架构总结

### v8.4 架构特点

| 特点 | 说明 |
|------|------|
| **分层清晰** | 5 层架构 (交互/路由/业务/数据/基础设施) |
| **模块化** | 8 大核心模块，独立部署 |
| **可扩展** | 插件化设计，新增技能无需改动核心 |
| **高可用** | 监控告警 + 自愈系统 |
| **安全** | 本地存储 + HIR 复核 + 加密 |
| **智能** | 模型路由 + 技能路由 + 任务调度 |
| **数据驱动** | 7 大数据源 + 冰山理论蒸馏 |
| **闭环** | 获客→培育→转化→成交全流程 |

---

**🏗️ 跨境贸易 Agent v8.4 详细架构 · 2026-04-18 23:45**

**✅ 5 层架构！8 大核心模块！7 大数据源！HIR 复核机制！完整数据流！Git 已提交！**
