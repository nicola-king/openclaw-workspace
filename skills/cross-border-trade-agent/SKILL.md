---
name: cross-border-trade-agent
version: 11.0.0
description: '太一跨境贸易 Agent - v11分层架构：总控→共享Agent→共享Skills→产品Agent→品类Skills'
category: trading
tags: ['trading', 'cross-border', 'e-commerce', 'agent-architecture']
status: active
---

# 跨境贸易 Agent v11.0 — 分层架构

> v11 = v10 全部 18 模块 + 分层架构重组
> 无功能丢失，所有模块代码保留在 `modules/`，通过 `agents/` 接入分层体系

## 架构总览

```
🏢 总Agent（太一）
调度 / 报告聚合 / 自进化 / 资源仲裁
│
├── 基础设施层
│   ├── cross-border-core      核心框架/事件总线/Bot协作
│   ├── data-integrator        7大数据源整合
│   └── task-scheduler         定时任务调度
│
├── 共享Agent x5
│   ├── 情报Agent    — 竞品监控 + 市场分析 + 趋势预警
│   ├── 富化Agent    — 公司清洗 + 7源验证 + 信息增强
│   ├── 履约Agent    — 供应链 + 支付 + 合同 + 物流
│   ├── 风控Agent    — 风险识别 + 对冲策略 + 二阶思维
│   └── 进化Agent    — 技能结晶 + 浏览器自愈 + Token优化
│
├── 共享Skills x11
│   web_crawler · company_verify · linkedin_search
│   contact_enrich · db_writer · report_engine · geo_optimizer
│   real_data_verify · data_integrator · culture_adapter
│   payment_settle
│
├── 常规工业品Agent
│   Skills: amazon_radar · source_matcher · listing_optimizer
│           price_monitor · review_analyzer · fba_calculator
│           supplier_scorer · platform_monitor · bulk_mail_composer
│           catalog_pusher · stock_alert · quick_quote
│   策略：富化输出100家 → 批量开发信 → 48h全发 → 快速报价
│
├── 定制产品Agent
│   Skills: persona_builder · solution_composer · rfq_parser
│           relationship_log · sample_tracker · tech_doc_pack
│   ├── 钢结构集成房：project_radar / spec_builder / compliance_check
│   ├── 变压器：tender_monitor / cert_tracker / load_calculator
│   ├── 摩配汽配：oem_matcher / catalog_builder / warranty_tracker
│   └── 储能：policy_radar / roi_calculator / bms_spec_parser
│   策略：富化输出10家 → 深度画像 → 1对1方案 → 长周期跟进
│
└── 转化优化中心
    ├── conversion-optimizer   漏斗分析/ROI/渠道对比/AB测试
    └── transaction-support    物流优化/比价/销售预测/多语言
```

## 完整模块全景（v10 全部保留 + v11 新增）

### P0 — 核心产品（买家情报平台）

| 模块 | 功能 | 位置 | 来源 |
|------|------|------|------|
| 买家情报引擎 | 项目雷达/采购机会/人脉库/订阅 | `modules/buyer-intel/` | v11新增 |
| 订阅计费 | 3级方案(free/¥299/¥999) | `modules/buyer-intel/subscriptions/` | v11新增 |
| 情报验证管道 | 5项验证→可信度评分 | `modules/buyer-intel/` | v11新增 |
| 工厂触达记录 | 触达→跟进→成单追踪 | `modules/buyer-intel/data/outreach.json` | v11新增 |

### P1 — 情报与搜索

| 模块 | 功能 | 位置 | 来源 |
|------|------|------|------|
| 贵客之路(guike-zhilu) | 搜索→清洗→触达→培育闭环 | `modules/guike-zhilu/` | v10 |
| 情报中心(intelligence-hub) | 竞品监控/趋势预警/选品评分 | `modules/intelligence-hub/` | v10 |
| 多源搜索增强 | 12国搜索资源/SERP/黄页 | `modules/guike-zhilu/multi_source_search.py` | v10 |
| 搜索Agent v4 | Scrapling自适应搜索 | `scripts/scraper_v4.py` | v11新增 |
| GEO优化(geo-outbound) | 市场分析/潜客名单/内容营销 | `modules/geo-outbound/` | v10 |
| 公司富化(company-enricher) | 自动爬虫/搜索/A BN查询/验证 | `modules/company-enricher/` | v10 |

### P2 — 业务工具（服务层）

| 模块 | 功能 | 位置 | 来源 |
|------|------|------|------|
| 报价引擎 v2 | FOB/CFR/到岸价 + 退税13%/9% | `modules/quote-engine/` | v10→v11增强 |
| 合同模板 | 14章中英双语 + SASO/SIAC仲裁 | `modules/contract-legal/` | v10 |
| 合规引擎 | HS退税查询 + SASO合规 | `modules/compliance-engine/` | v10 |
| 供应商匹配 | 9家工厂评分排名 | `modules/supplier-matcher/` | v11新增 |
| 产品目录RAG | TF-IDF+买家需求匹配 | `modules/product-catalog/` | v11新增 |

### P2 — 交易与履约

| 模块 | 功能 | 位置 | 来源 |
|------|------|------|------|
| 交易支持(transaction-support) | 物流优化/比价/销售预测/多语言客服 | `modules/transaction-support/` | v10 |
| 供应链(supply-chain) | 供应商管理/库存优化/需求预测 | `modules/supply-chain/` | v10 |
| 支付结算(payment-settlement) | 支付通道/汇率管理/结算优化 | `modules/payment-settlement/` | v10 |

### P2 — 转化与优化

| 模块 | 功能 | 位置 | 来源 |
|------|------|------|------|
| 转化优化(conversion-optimizer) | 漏斗分析/ROI追踪/渠道对比/AB测试 | `modules/conversion-optimizer/` | v10 |
| 跨文化适配(cultural-adapter) | 内容本地化/多语言/SEO/文化分析 | `modules/cultural-adapter/` | v10 |

### P2 — 风控与进化

| 模块 | 功能 | 位置 | 来源 |
|------|------|------|------|
| 风险管理(risk-manager) | 风险识别/预警/对冲策略/二阶思维 | `modules/risk-manager/` | v10 |
| 自我进化(self-evolution) | 技能结晶/浏览器自愈/Token效率 | `modules/self-evolution/` | v10 |
| 真实数据验证(real-data-verifier) | 公司/电话/邮箱/官网 单项验证 | `modules/real-data-verifier/` | v10 |

### P3 — 基础设施

| 模块 | 功能 | 位置 | 来源 |
|------|------|------|------|
| 核心框架(cross-border-core) | 路由/调度/事件总线/Bot协作 | `modules/cross-border-core/` | v10 |
| 数据整合(data-integrator) | 7源整合(海关/电商/搜索/报告/物流/广告) | `modules/data-integrator/` | v10 |
| 任务调度(task-scheduler) | 定时任务/自检/推送/SimpleCron | `modules/task-scheduler/` | v10 |
| 报告引擎(report-engine) | 智能报告/ES引擎/Markdown生成 | `modules/report-engine/` | v10 |

## 治理规则

| 层级 | 范围 | 方式 |
|------|------|------|
| 自动进化 | 选品权重 / 关键词库 / 开发信AB测试 | 无人介入 |
| 推送你确认 | 新品市场 / 方案模板大改 / 触达策略调整 | 推你决策 |
| 硬锁定 | 报价参数 / 合同条款 / 财务承诺 | 不可更改 |

---

## 模块详述

### 报价引擎 v2 — 含出口退税

```
位置：modules/quote-engine/core.py
用途：钢结构折叠房屋报价 + 退税计算

HS编码库：
  73089000  钢铁结构体 → 退税率 9%
  94069000  预制房屋   → 退税率 13%

输入：出厂价 + 规格 + 目的地
输出：FOB/CFR + 利润 + 退税 + 沙特到岸价

依赖：config.json（汇率/运费/利润率默认值）
```

### 合规引擎 — 退税政策更新

```
位置：modules/compliance-engine/core.py
新类：ExportRebateChecker
功能：HS编码退税查询 + 政策变动提醒
```

### 架构集成（卖家视角）

```
┌─ 对话层 ─────────────────┐
│ 意图识别 → RAG知识检索    │ ← 待建
└──────────────────────────┘
┌─ 业务工具层 ──────────────┘
│ 报价引擎(含退税)        ✅ │
│ 合规检查(SASO+退税)     ✅ │
│ 产品目录RAG             ✅ │
│ 供应商匹配              ✅ │
│ 合同模板                ✅ │
│ 转化优化(漏斗/ROI/AB)   ✅ │
│ 交易支持(物流/比价/预测) ✅ │
│ 跨文化适配(本地化/多语言) ✅ │
│ 风险管理(预警/对冲)      ✅ │
│ 供应链(库存/需求预测)    ✅ │
│ 支付结算(汇率/通道)      ✅ │
└──────────────────────────┘
```

## 定时任务

| 时间 | 任务 | 模块 | 推送 |
|------|------|------|------|
| 03:00 | Git备份 | task-scheduler | 静默 |
| 06:00 | 自进化引擎 | self-evolution | 静默 |
| 07:00 | 情报Agent备料 | intelligence-hub | 静默 |
| 08:00 | 晨间简报 | report-engine | 推送你 |
| 09:00 | 富化Agent | company-enricher | 静默 |
| 12:00 | 触达Agent开发信 | guike-zhilu | 静默 |
| 14:00 | GEO优化报告 | geo-outbound | 推送你 |
| 14:30 | 触达Agent发送 | guike-zhilu | 静默 |
| 18:00 | 竞品监控日报 | intelligence-hub | 推送你 |
| 每小时 | 健康检查+调度 | task-scheduler | 静默 |
| 周一09:00 | 周度分析 | report-engine | 推送你 |
| 每月1日 | 月度报告 | report-engine | 推送你 |

## 目录说明（物理结构）

```
agents/                          # v11 分层架构（symlink → 已有模块）
│
├── infrastructure/              # 基础设施层
│   ├── core                     → modules/cross-border-core
│   ├── data-integrator          → modules/data-integrator
│   └── scheduler                → modules/task-scheduler
│
├── shared/intelligence/         # 情报Agent ×5
│   ├── core                     → modules/intelligence-hub
│   ├── guike                    → modules/guike-zhilu
│   ├── geo                      → modules/geo-outbound
│   └── buyer-intel              → modules/buyer-intel
│
├── shared/enrichment/           # 富化Agent
│   ├── company-enricher         → modules/company-enricher
│   └── verifier                 → modules/real-data-verifier
│
├── shared/fulfillment/          # 履约Agent
│   ├── transaction              → modules/transaction-support
│   ├── supply-chain             → modules/supply-chain
│   ├── payment                  → modules/payment-settlement
│   └── contract                 → modules/contract-legal
│
├── shared/risk/                 # 风控Agent
│   └── core                     → modules/risk-manager
│
├── shared/evolution/            # 进化Agent
│   ├── core                     → modules/self-evolution
│   └── scheduler                → modules/task-scheduler
│
├── services/                    # 业务工具服务层
│   ├── quote-engine             → modules/quote-engine
│   ├── product-catalog          → modules/product-catalog
│   ├── supplier-matcher         → modules/supplier-matcher
│   └── compliance-engine        → modules/compliance-engine
│
├── conversion/                  # 转化优化中心
│   ├── optimizer                → modules/conversion-optimizer
│   ├── cultural                 → modules/cultural-adapter
│   └── transaction              → modules/transaction-support
│
├── skills/                      # 共享Skills池（11个，symlink）
│   ├── web_crawler              → scripts/scraper_v4.py
│   ├── linkedin_search          → skills/shared-search-agent
│   ├── contact_enrich           → modules/company-enricher
│   ├── report_engine            → modules/report-engine
│   ├── geo_optimizer            → modules/geo-outbound
│   ├── real_data_verify         → modules/real-data-verifier
│   ├── data_integrator          → modules/data-integrator
│   ├── culture_adapter          → modules/cultural-adapter
│   ├── payment_settle           → modules/payment-settlement
│   ├── cross-border-core        → modules/cross-border-core
│   └── db_writer                → modules/data-integrator
│
├── standard-products/           # 常规工业品Agent
│   ├── orchestrator.py
│   └── skills/                  (12 README)
│
└── custom-products/             # 定制产品Agent
    ├── orchestrator.py
    ├── skills/                  (6 README)
    └── categories/              (4品类x3技能 README)

modules/                         # 全部22个模块代码（symlink源）
├── buyer-intel / quote-engine / product-catalog / supplier-matcher
├── contract-legal / compliance-engine / company-enricher
├── intelligence-hub / guike-zhilu / geo-outbound
├── cross-border-core / data-integrator / conversion-optimizer
├── transaction-support / self-evolution / real-data-verifier
├── task-scheduler / risk-manager / cultural-adapter
├── supply-chain / payment-settlement / report-engine
```

## 情报分发

| 目标 | 订阅内容 |
|------|---------|
| 常规工业品Agent | 价格波动 / 平台询盘量 / 爆款SKU |
| 定制产品Agent | 大项目招标 / 行业展会 / 目标客户动态 |

## 数据分层

| 通道 | 输入 | 输出字段 | 目的 |
|------|------|---------|------|
| 轻富化（常规） | 热销品对应卖家 | 邮箱/规模/采购频率 | 找货源 |
| 深富化（定制） | 目标公司名单 | 全字段+persona+跟进 | 找买家 |

### 产品目录 RAG

```
位置：modules/product-catalog/
  core.py      — RAG引擎 (TF-IDF搜索 + 买家需求匹配)
  data/catalog.json — 5款产品数据

功能：
  search <query>             语义搜索（含中文）
  match <persons> <budget>   买家需求匹配（自动评分）
  info <product_id>          产品详情
  list                       列出全部

产品库（可扩展）：
  FS-LC-04  劳保型L系列    ¥18,500   14㎡  ⭐劳工营首选
  FS-KZG-01 标准型K系列    ¥28,000   18㎡
  FS-DXH-02 豪华型D系列    ¥45,000   18㎡  沙漠隔热
  FS-JZ-03  大空间J系列    ¥88,000   72㎡  食堂/仓库
  FS-GG-05  车棚GG系列     ¥12,000   21㎡
```

### 供应商匹配模块 v1

```
位置：modules/supplier-matcher/
  core.py           — 匹配引擎 (搜索 + 需求匹配评分)
  data/suppliers.json — 9家供应商数据

功能：
  search <query>               搜索供应商
  match <product> <qty> [tier] 匹配供应商到产品需求
  info <id>                    查看详情
  list                         全部列表

供应商库（9家）：
  SUP-GD-02  广东集成房屋   ¥2000万出口  CE+TUV   📞  ⭐折叠房屋首选
  SUP-FS-05  宏福模块       ¥4000万出口  CE       🔍
  SUP-FSL-01 法狮龙建材     ¥1000万出口  CE+SGS   📞
  SUP-QD-04  海容模块       ¥5000万出口  缺CE     🔍  量最大
  SUP-SH-03  邦山模块化     ¥800万出口   CE+BV   📞  高端
  SUP-TJ-06  北洋集装箱     ¥3000万出口  缺CE     🔍
  SUP-GD-09  华鑫钢构       ¥6000万出口  CE+AWS   🔍  大产能
  SUP-BJ-07  京冀集装箱     ¥2200万出口  无证     🔍
  SUP-JX-08  江西众鑫       无出口       ISO      🔍  已联系
```

匹配逻辑：产品类型(20分) + 产能(10分) + 认证(5分/项) + 中东经验(8分) + 质量档次(5分) + 联系方式(3分)

### 合同模板模块 — 中东专版

```
位置：modules/contract-legal/core.py

功能：
  generate            生成国际销售合同（中英双语）
  payment             查看支付条款选项
  delivery            查看交货条款
  arbitration         查看争议解决选项

14章节目录：
  合同方 / 产品规格 / 数量价格 / 支付条款
  交货运输 / 质量验收 / 包装标识 / SASO合规
  质保 / 违约赔偿 / 不可抗力 / 争议解决
  保密 / 其他

中东专有条款：
  ✅ SASO/SABER 合规 + SABER二维码标识
  ✅ 沙特信用证(UCP600) + 保兑建议
  ✅ 达曼/吉达港交货条款
  ✅ SIAC/DIAC/CIETAC 三种仲裁选项
  ✅ 阿拉伯语文件要求
  ✅ 伊斯兰金融合规选项

支付选项：
  tt_30_70    30%预付+70%提单副本   适合沙特新客户
  lc_at_sight 即期信用证(L/C)        适合$100K+大单
  lc_deferred 远期信用证(30-60天)    适合长期客户

交货选项：
  FOB上海 / CFR达曼 / CIF吉达 / DAP利雅得
```

合同模板 ✅ | 供应商匹配 ✅ | 产品目录 ✅ | 报价引擎 ✅ | 合规 ✅

## 买家情报引擎（核心产品）

```
位置：modules/buyer-intel/
  core.py           — 搜索/项目雷达/线索管理/订阅控制
  data/buyers.json  — 15条已验证买家数据

核心功能：
  search <query>            搜索买家/项目（按订阅层级控制可见）
  projects [country]        活跃项目与采购需求
  leads [country]           可联系线索
  opportunities [product]   当前采购机会匹配
  subscribe                 查看订阅方案

数据覆盖：
  项目: Jewel of the Bride($20亿) / NEOM($5000亿) / 伊拉克21城等 7个
  公司: Afco Steel / SBS Contracting / Zamil Steel 等 3家
  人脉: SAW Constructions / Crystalbrook Collection 等 5人

订阅分层：
  free    免费   3条/月    仅项目名称/国家
  basic   ¥299  20条/月   含预算/采购需求/买方类型
  pro     ¥999  不限      全部信息 + 联系方式
```

## 双模式运营

```
┌─ 核心模式 ──────────────────────────────────┐
│ 买家情报平台 → 工厂付费订阅                   │
│ 数据产品: 项目情报/采购线索/人脉              │
└─────────────────────────────────────────────┘
┌─ 机会模式 ──────────────────────────────────┐
│ 发现高利润匹配 → 亲自做中间贸易商              │
│ 条件: 好产品 + 可靠买家 + 足够利润             │
└─────────────────────────────────────────────┘
```

## 模块全景（完整）

```
P0 买家情报引擎    ✅  ← 工厂付钱买这个
├─ 项目雷达        ✅
├─ 采购机会        ✅
├─ 人脉库          ✅
├─ 订阅控制        ✅（3级权限）
│
P1 情报与搜索
├─ 贵客之路        ✅（搜索→清洗→触达→培育）
├─ 情报中心        ✅（竞品/趋势/选品）
├─ 多源搜索        ✅（12国搜索引擎+黄页）
├─ 搜索Agent v4    ✅（Scrapling自适应）
├─ GEO优化         ✅
└─ 公司富化        ✅
│
P2 业务工具（服务层）
├─ 报价引擎 v2     ✅（含退税）
├─ 合同模板        ✅（中东专版）
├─ 合规引擎        ✅
├─ 供应商匹配      ✅
├─ 产品目录RAG     ✅
├─ 转化优化        ✅（漏斗/ROI/AB测试）
├─ 交易支持        ✅（物流/比价/预测/多语言）
├─ 跨文化适配      ✅（本地化/多语言/SEO）
│
P2 风控与进化
├─ 风险管理        ✅（预警/对冲/二阶思维）
├─ 自我进化        ✅（技能结晶/浏览器自愈）
├─ 真实数据验证    ✅（官网/电话/邮箱/公司）
│
P3 基础设施
├─ 核心框架        ✅（路由/调度/Bot协作）
├─ 数据整合        ✅（7源：海关/电商/搜索/报告）
├─ 任务调度        ✅（定时任务/自检/推送）
├─ 支付结算        ✅（汇率/通道/结算）
├─ 供应链          ✅（库存/需求预测）
└─ 报告引擎        ✅
```

### buyer-intel 新增能力

```
能力1 — 情报验证管道
  verify <id> [method]      执行验证
  5项验证: 官网/电话/邮箱/LinkedIn/第三方
  通过≥3项 → 自动标记 confirmed = True
  输出: 可信度评分(0-1) + 验证明细

能力2 — 工厂触达记录
  outreach <intel_id> <工厂>   记录触达某工厂
  outreach-status [id]          查看触达进度
                              └ 跟进中 → 报价中 → 已合作

dashboard 运营主控台
  数据库 / 触达 / 验证 三栏总览
  一目了然：多少线索、联系了多少、成单率
```

### 订阅管理（计费引擎）

```
sub register <id> <名> [plan]   注册工厂订阅
sub list [id]                   查看订阅者
sub metrics                     订阅运营数据
sub paid <id> [月数]            记录续费
sub upgrade <id> <plan>         升级/降级方案
sub expired                     检查逾期

订阅方案：
  free        免费    3条/月    仅项目名
  free_trial  试用    10条/月   全部字段，7天
  basic       ¥299   20条/月   含预算/采购需求
  pro         ¥999   不限      全部信息+联系方式

运营数据示例：
  3个订阅者 | 2活跃 | 月收入 ¥598
  含试用转化／续费跟踪／限额控制
```
