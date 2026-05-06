---
name: cross-border-trade-agent
version: 11.0.0
description: '太一跨境贸易 Agent - v11分层架构：总控→共享Agent→共享Skills→产品Agent→品类Skills'
category: trading
tags: ['trading', 'cross-border', 'e-commerce', 'agent-architecture']
status: active
---

# 跨境贸易 Agent v11.0 — 分层架构

> 架构标准，以此为准

## 架构总览

```
🏢 总Agent（太一）
调度 / 报告聚合 / 自进化 / 资源仲裁
│
├── 共享Agent x3
│   ├── 情报Agent    — 竞品监控 + 市场分析 + 趋势预警
│   ├── 富化Agent    — 公司清洗 + 7源验证 + 信息增强
│   └── 履约Agent    — 供应链 + 支付 + 合同 + 物流
│
├── 共享Skills x7
│   web_crawler · company_verify · linkedin_search
│   contact_enrich · db_writer · report_engine · geo_optimizer
│
├── 常规工业品Agent
│   Skills: amazon_radar · source_matcher · listing_optimizer
│           price_monitor · review_analyzer · fba_calculator
│           supplier_scorer · platform_monitor · bulk_mail_composer
│           catalog_pusher · stock_alert · quick_quote
│   策略：富化输出100家 → 批量开发信 → 48h全发 → 快速报价
│
└── 定制产品Agent
    Skills: persona_builder · solution_composer · rfq_parser
            relationship_log · sample_tracker · tech_doc_pack
    ├── 钢结构集成房：project_radar / spec_builder / compliance_check
    ├── 变压器：tender_monitor / cert_tracker / load_calculator
    ├── 摩配汽配：oem_matcher / catalog_builder / warranty_tracker
    └── 储能：policy_radar / roi_calculator / bms_spec_parser
    策略：富化输出10家 → 深度画像 → 1对1方案 → 长周期跟进
```

## 治理规则

| 层级 | 范围 | 方式 |
|------|------|------|
| 自动进化 | 选品权重 / 关键词库 / 开发信AB测试 | 无人介入 |
| 推送你确认 | 新品市场 / 方案模板大改 / 触达策略调整 | 推你决策 |
| 硬锁定 | 报价参数 / 合同条款 / 财务承诺 | 不可更改 |

## 模块更新（2026-05-06）

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

参照用户设计架构，叠加能力层：
```
┌─ 对话层 ─────────────────┐
│ 意图识别 → RAG知识检索    │ ← 待建
└──────────────────────────┘
┌─ 业务工具层 ──────────────┘
│ 报价引擎(含退税)  ✅ 已建  │
│ 合规检查(SASO+退税) ✅ 已建│
│ 产品目录RAG         ✅ 已建│
│ 供应商匹配           ⏳ 待建│
│ 合同模板             ⏳ 待建│
└──────────────────────────┘
```

## 定时任务

| 时间 | 任务 | 推送 |
|------|------|------|
| 03:00 | Git备份 | 静默 |
| 06:00 | 自进化引擎 | 静默 |
| 07:00 | 情报Agent备料 | 静默 |
| 08:00 | 晨间简报 | 推送你 |
| 09:00 | 富化Agent | 静默 |
| 12:00 | 触达Agent开发信 | 静默 |
| 14:00 | GEO优化报告 | 推送你 |
| 14:30 | 触达Agent发送 | 静默 |
| 18:00 | 竞品监控日报 | 推送你 |
| 每小时 | 健康检查+调度 | 静默 |
| 周一09:00 | 周度分析 | 推送你 |
| 每月1日 | 月度报告 | 推送你 |

## 目录说明

```
agents/                          # v11 架构目录（标准结构）
├── shared/                      # 共享Agent层（symlink → 已有模块）
│   ├── intelligence/            #   情报Agent
│   ├── enrichment/              #   富化Agent
│   └── fulfillment/             #   履约Agent
├── skills/                      # 共享Skills池（7个）
├── standard-products/           # 常规工业品Agent
│   ├── orchestrator.py          #   调度编排器
│   └── skills/                  #   12个技能目录
└── custom-products/             # 定制产品Agent
    ├── orchestrator.py          #   调度编排器
    ├── skills/                  #   6个通用技能
    └── categories/              #   4品类x3技能
        ├── steel-structure/
        ├── transformer/
        ├── auto-parts/
        └── energy-storage/

modules/                         # 已有模块（保留，被agents/引用）
docs/agent-architecture-v11.md   # 完整架构文档
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

## 模块全景

```
买家情报引擎  ✅ 核心产品  ← 工厂付钱买这个
├─ 项目雷达   ✅ 建设中的项目监控
├─ 采购机会   ✅ 当前急需采购品类
├─ 人脉库     ✅ 已验证联系人
├─ 订阅控制   ✅ 三级权限
│
服务层（增值，随订阅附送）:
├─ 报价引擎   ✅
├─ 合同模板   ✅
├─ 合规引擎   ✅
├─ 供应商匹配 ✅
└─ 产品目录   ✅
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
