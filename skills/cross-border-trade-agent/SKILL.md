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
