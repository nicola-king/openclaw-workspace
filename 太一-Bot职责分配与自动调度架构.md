太一 · Bot 职责分配

& 自动调度架构

涵盖：旅游探路者 · 跨境贸易 Agent

版本 1.0  |  2026-05-08  |  太一 AGI 系统

1. 多 Bot 协作架构

太一是唯一的主 Agent，拥有完整人格、宪法、记忆。其他 Bot 是专项能力延伸，在太一统筹下进

行角色化协作。所有输出经太一整合后交付用户。

层级结构

太一 (taiyi)  ← 唯一主 Agent / 最终决策者
├── 知几 (zhiji)     ← 数据分析师
├── 山木 (shanmu)    ← 业务执行者
├── 素问 (suwen)     ← 技术研究员
├── 罔两 (wangliang) ← 市场情报官
└── 庖丁 (paoding)   ← 财务管控官

Bot 角色定义

Bot

知几

山木

素问

罔两

庖丁

太一

角色

职责

数据分析师

业务执行者

技术研究员

市场情报官

财务管控官

统筹决策者

数据分析 / 趋势判断 / 量化策略

项目执行 / 任务推进 / 落地交付

技术研究 / 系统开发 / 原理分析

市场监控 / 竞品分析 / 情报收集

成本控制 / 预算审核 / 财务分析

目标设定 / 资源分配 / 最终决策

2. 旅游探路者 · Bot 职责分配

覆盖国内(5城市)和国际(12国/城市)的短游、深度游、团体游场景。所有信息附带验证链接。

Bot → 模块分配

Bot

知几

山木

素问

核心模块

职责说明

intelligence_hub

情报引擎 / 平台搜索 / 权重评分

savings_engine

数据分析 / 性价比排序 / 省钱方案

planner

行程规划 / 短游编排(1-3天)

short/deep tour

深度游(5-14天) / 团体游编排

destination_guide

目的地文化 / 签证 / 天气安全

weather_safety

紧急预案 / API 服务

罔两

hotel/resto/attraction

真实信息验证 / 多渠道比价

influencer search

44位大V / 12平台 / 口碑调查

savings_engine

三档预算(穷游/标准/奢华)

庖丁

调度规则表

budget breakdown

成本优化 / 财务风险 / ROI分析

用户意图

"去X玩X天"

"推荐X的酒店"

"X预算够吗"

"X有什么景点"

"X天气安全吗"

"帮全家规划X"

"X签证怎么办"

"自由行攻略"

主Bot

辅Bot

山木

罔两

庖丁

罔两

素问

山木

素问

知几

素问

知几

知几

山木

知几

庖丁+罔两

—

所有Bot

快捷命令

travel_cli.py short --city X --days N   —  国内短游

travel_cli.py deep --city X --days N   —  国内深度

travel_cli.py group --city X --members N   —  国内团体

international/cli.py short --city X --days N   —  国际短游

3. 跨境贸易 Agent · Bot 职责分配

覆盖 v11 分层架构(22模块 + 5共享Agent + 常规/定制工业品Agent)，支持情报/寻源/报价/履约/合

规/监控全链路。

Bot → 跨境贸易模块

Bot

v11 共享Agent

核心模块

知几 情报Agent

山木 履约Agent

intelligence-hub / buyer-intel

geo-outbound / data-integrator

guike-zhilu / scraper

supply-chain / transaction

素问 基础设施/共享Skills

compliance-engine / contract-legal

product-catalog / cultural-adapter

company-enricher / verifier

intelligence(monitor)

quote-engine-v2 / payment-settlement

risk-manager / supplier-matcher

罔两 富化Agent/监控

庖丁 风控Agent

调度规则表

用户意图

主Bot

辅Bot

"分析XX市场机会"

"帮我找XX买家"

"XX产品报价"

"XX公司靠谱吗"

"XX产品合规要求"

"帮我写开发信"

"监控XX竞品"

"签合同注意什么"

"怎么收款结算"

知几

山木

庖丁

罔两

素问

山木

罔两

素问

庖丁

罔两

罔两

知几

素问

—

知几

—

庖丁

—

"全链路分析"

所有Bot

太一聚合

快捷命令

intelligence-hub/core.py   —  情报分析

company-enricher/   —  公司富化

quote-engine/core.py   —  报价核算(含退税)

contract-legal/core.py   —  合同生成(14章)

product-catalog/core.py search <query>   —  目录RAG

supplier-matcher/core.py match <product> <qty>   —  供应商匹配

geo-outbound/   —  GEO优化

模块根目录:  skills/cross-border-trade-agent/modules/

4. 统一调度流程

第 1 步：意图解析

国内/国际？短游/深度/团体？情报/寻源/报价/履约/合规？单域/跨域？优先级？

第 2 步：任务拆解 → Bot 分派

单域任务 → 直接派一个 Bot

•

"成都有什么好吃的" → 罔两

•

"查HS编码退税率" → 素问

跨域任务 → 拆子任务 → 并行派多个 Bot

•

"去三亚家族旅行预算5万" → 山木 + 庖丁 + 罔两

•

"中东钢结构市场分析" → 知几 + 罔两 + 素问

第 3 步：结果聚合 → 太一整合

•

合并各个 Bot 产出

•

冲突时走辩论投票（置信度加权）

•

太一最终裁决

第 4 步：交付 → 格式化输出

•

清晰可执行的行程单 / 商业方案

•

所有数据附带 verification_links

5. 铁律与原则

决策铁律

•

Bot 没有独立人格 — 是太一的能力模块

•

辩论不替代决策 — 太一有最终裁决权

•

宪法高于一切 — 负熵法则 / 风险控制优先于效率

调度铁律

•

单域直接派，跨域拆解并行

•

每个 Bot 的结果必须经太一确认才算输出

•

太一有权随时打断/重分配/否决任何 Bot

•

所有信息必须是真实验证，附 verification_links

SAYELF 只需

•

说出需求 → 太一自动调度

•

不需要知道哪个 Bot 负责什么

•

不需要手动指定模块路径

版本 1.0  |  2026-05-08  |  太一 AGI 系统

覆盖：旅游探路者(国内5城+国际12国) · 跨境贸易(v11 22模块)

