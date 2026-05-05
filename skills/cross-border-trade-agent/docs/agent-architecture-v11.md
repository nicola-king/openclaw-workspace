# 跨境贸易 Agent v11.0 — 分层架构

> 更新时间：2026-05-05

## 总控层

**🏢 跨境贸易总Agent（太一）**
- 调度仲裁（任务分发/优先级管理）
- 报告聚合（聚合各Agent输出 → 推送你）
- 自进化管理（宪法学习/技能蒸馏/模块升级）
- 资源仲裁（API配额/并发控制/错误重试）

## 共享 Agent 层

| Agent | 职责 | 服务对象 |
|-------|------|---------|
| **情报Agent** | 竞品监控 + 市场分析 + 趋势预警 | 所有产品线共用 |
| **富化Agent** | 公司数据清洗 + 7源验证 + 信息增强 | 所有产品线共用 |
| **履约Agent** | 供应链 + 支付 + 合同 + 物流 | 所有产品线共用 |

## 共享 Skills 池

```
共享 Skills
 ├── web_crawler       — 多源爬虫
 ├── company_verify    — 工商/地址核验
 ├── linkedin_search   — LinkedIn搜索链接生成
 ├── contact_enrich    — 邮箱/电话补全
 ├── db_writer         — 写入company_enricher
 ├── report_engine     — 报告生成
 └── geo_optimizer     — GEO内容优化
```

## 产品 Agent 层

| Agent | 定位 | 特点 |
|-------|------|------|
| **常规工业品Agent** | 标准品批量 | C端/小B · 快节奏 · 高频触达 · 规模化 |
| **定制产品Agent** | 深度项目 | 大B端 · 长周期 · 深度跟进 · 定制化 |

每个产品Agent拥有独立的Skills，共享层Skills供所有Agent调用。

### 常规工业品 Skills

```
常规工业品 Skills
 ├── amazon_radar        — BSR榜单监控+利润计算
 ├── source_matcher      — 1688/工厂反查匹配货源
 ├── listing_optimizer   — 亚马逊标题/五点/A+内容生成
 ├── price_monitor       — 竞品动态定价追踪
 ├── review_analyzer     — 差评分析→产品改进建议
 ├── fba_calculator      — FBA费用+利润率估算
 ├── supplier_scorer     — 供应商评分（交期/质检/MOQ）
 ├── platform_monitor    — 阿里/MiC/GS平台询盘监控
 ├── bulk_mail_composer  — 批量个性化开发信（模板化）
 ├── catalog_pusher      — 产品目录/报价单自动发送
 ├── stock_alert         — 现货库存预警推送
 └── quick_quote         — 标准品快速报价生成
```

### 定制产品 Skills

```
定制产品 Skills
 ├── persona_builder      — 联系人深度画像
 ├── solution_composer   — 定制方案文档生成
 ├── rfq_parser          — RFQ解析+技术参数提取
 ├── relationship_log    — 长周期跟进记录
 ├── sample_tracker      — 打样进度管理
 └── tech_doc_pack       — 技术文档/认证资料打包
```

## 情报源架构

### 常规工业品情报

**数据源：**
```
├── 亚马逊 Best Sellers / Movers & Shakers
├── 速卖通热销榜
├── eBay Trending
├── Jungle Scout / Helium10（API或爬虫）
├── Google Trends
├── TikTok Shop 热销品
└── 1688反查（找国内货源）
```

**输出：** 每日热销品清单（含价格带/评论数/竞争密度/利润估算）→ 推送08:00晨报

---

### 定制产品情报（四品类）

**数据源：**
```
钢结构/集成房：
  ├── 建筑行业招标网 / Dodge Data / Barbour ABI
  ├── 澳洲DA申请公告 / 非洲/中东建设项目库

变压器/储能：
  ├── 能源项目招标 / BNEF / Wood Mackenzie
  ├── LinkedIn目标公司动态 / 展会参展商名单
  ├── （Solar Africa / Intersolar / RE+ 等）

摩配/汽配：
  ├── AAPEX/SEMA参展商 / 汽修连锁采购公告
  ├── Made-in-China / Global Sources 买家询盘
  └── 海关数据（谁在进口竞品）

通用：
  ├── Google Alerts（品类关键词）
  ├── 行业协会新闻
  └── 目标公司官网动态
```

**输出：** 项目机会清单 + 目标公司名单 → 进入富化Agent

---

## 情报分发策略

### 情报Agent 输出

```
情报Agent
 ├── → 常规工业品 Agent
 │   订阅：价格波动 / 平台询盘量 / 爆款SKU
 │
 └── → 定制产品 Agent
     订阅：大项目招标 / 行业展会 / 目标客户动态
```

## 产品线细分

定制产品 Agent 下按品类拆分，每个品类3个细分Skills：

### 钢结构集成房
```
├── project_radar      — 建筑项目早期预警（DA/招标）
├── spec_builder       — 房型规格书+3D效果图描述生成
└── compliance_check   — 目标市场建筑法规合规核查
```

### 变压器
```
├── tender_monitor     — 电力项目招标监控
├── cert_tracker       — IEC/UL/AS认证状态管理
└── load_calculator    — 容量需求初步估算工具
```

### 摩配汽配
```
├── oem_matcher        — OEM编号匹配+适配车型查询
├── catalog_builder    — 多品牌适配目录生成
└── warranty_tracker   — 质保索赔记录管理
```

### 储能
```
├── policy_radar       — 目标市场储能补贴政策监控
├── roi_calculator     — 项目投资回报估算
└── bms_spec_parser    — 电池管理系统规格解析
```

品类共享Skills：跨品类复用（如文档生成、邮件模板、报告引擎等）

## 数据分层策略

### company_enricher 数据库

```
company_enricher DB
 ├── 常规工业品 Agent 读取
 │   关注字段：邮箱、公司规模、采购频率
 │   不需要：个人爱好、职业轨迹
 │
 └── 定制产品 Agent 读取
     关注字段：全部字段
     额外写入：relationship_log（跟进记录）
```

## 富化通道

### 常规工业品通道（轻富化）

**输入：** 热销品对应的平台卖家/品牌方

**执行：**
```
├── 公司官网 / 联系方式核验
├── 是否有经销商招募信息
└── 写入DB（轻量字段）
```

**目的：** 找货源，不是找买家

---

### 定制产品通道（深富化）

**输入：** 情报Agent产出的目标公司名单

**执行：**
```
├── 工商核验（ABN/注册信息/地址）
├── LinkedIn 8角色搜索
│   钢结构：Project Manager / Procurement / Developer
│   变压器：Electrical Engineer / Asset Manager / CEO
│   摩配汽配：Parts Manager / Fleet Manager / Buyer
│   储能：Energy Manager / CTO / Investment Director
├── 邮箱/电话补全（Hunter.io / Apollo API）
├── persona_builder
│   职业轨迹 / 近期LinkedIn动态 / 关注话题 / 共同连接
└── 写入company_enricher（全字段）
```

---

## 运营策略

### 常规工业品 Agent

**目标：** 规模化覆盖，快速筛出有效询盘

**策略：**
1. 富化Agent输出100家公司
2. 批量生成开发信（共用模板+变量替换）
3. 48小时内全部发出
4. 有响应 → 快速报价 → 推入漏斗

**节奏：** 快 · 高频 · 模板化 · 广度优先

---

### 定制产品 Agent

**目标：** 精准渗透，建立深度信任

**策略：**
1. 富化Agent输出10家高价值公司
2. persona_builder生成每人背景画像
3. 1对1手工级开发信（AI起草，你微调）
4. 分3个接触点触达（邮件→LinkedIn→邮件）
5. 有响应 → solution_composer生成定制方案
6. 进入长周期跟进（relationship_log记录）

**节奏：** 慢 · 深度 · 个性化 · 精度优先

---

## 治理规则

### 可自动进化（无需你介入）
```
├── 常规工业品：选品评分权重（根据转化数据调整）
├── 各品类：目标市场关键词库
└── 开发信：AB测试后自动选胜出版本
```

### 推送你确认
```
├── 新增监控品类或市场
├── 定制产品方案模板大改
└── 触达策略调整（频率/渠道/角色优先级）
```

### 硬锁定（不可更改）
```
├── 报价参数
├── 合同条款
└── 任何对外财务承诺
```

## 数据流

```
太一（调度）→ 情报Agent → 数据分析
         → 富化Agent → 公司验证
         → 产品Agent → 触达/转化
         → 履约Agent → 交易完成
         ↓
    报告聚合 → 推送你
```
