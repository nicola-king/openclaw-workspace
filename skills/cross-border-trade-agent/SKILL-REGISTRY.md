# 太一 Skill 注册中心 — 全技能目录

> 版本 1.0.0 | 生成: 2026-05-12
> 所有 Agent 能力的标准化目录，支持动态发现、延迟加载、跨 Bot 调用

---

## 使用方式

### 查询所有可用 Skill
```python
from modules.skill_registry.registry import SkillRegistry

reg = SkillRegistry()
skills = reg.search(owner="知几")            # 按 Bot 筛选
skills = reg.search(trigger="合规")          # 按关键词筛选
skills = reg.search(dependency="intel")      # 按依赖筛选
```

### 按需加载执行
```python
skill = reg.load("intelligence-hub.market-analysis")
result = skill.execute({"product": "钢结构", "market": "沙特"})
```

### Skill 注册格式
每个 Skill 必须包含 `manifest.json` 或符合标准格式的元数据。

---

## 目录

### 🧠 知几 — 数据分析 · 市场研究 · 情报挖掘

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `intelligence-hub.market-analysis` | 市场分析 | 基于多源数据做目标市场分析 | 市场分析, 市场机会, 趋势 | async |
| `intelligence-hub.competitor-monitor` | 竞品监控 | 竞品价格/新品/策略动态追踪 | 竞品, 对手, monitor | async |
| `intelligence-hub.product-scoring` | 选品评分 | 多维度产品机会评分 | 选品, 评分, 产品机会 | sync |
| `intelligence-hub.trend-analysis` | 趋势预测 | 行业趋势 + 聪明钱流向分析 | 趋势, 预测, 方向 | sync |
| `intelligence-hub.bidding-radar` | 招标雷达 | 全球招标/采购信息抓取 | 招标, 采购, RFQ | async |
| `intelligence-hub.policy-radar` | 政策监控 | 关税/认证/标准变动追踪 | 政策, 关税, 法规变动 | async |
| `buyer-intel.selected` | 买家情报·精选 | 7天活跃采购机会精选 | 买家, 项目, 采购机会 | sync |
| `buyer-intel.daily` | 买家情报·日报 | 按国家/品类打包日报 | 日报, 雷达 | sync |
| `buyer-intel.full` | 买家情报·全量 | 含冷线索的全部采购机会 | 全部, 全量, 所有 | sync |
| `geo-outbound.market-analysis` | GEO 市场分析 | 关键词策略 + 市场定位 | GEO, 市场分析 | sync |
| `data-integrator.multi-source` | 多源数据整合 | 7源数据聚合清洗 | 数据整合, 数据源 | sync |
| `report-engine.report` | 智能报告生成 | 结构化报告/Markdown/热点趋势 | 报告, 简报, 分析报告 | async |
| `trade-profile.profile` | 贸易画像 | 用户画像跨模块传播（新建）| 画像, 贸易画像, 用户轮廓 | sync |
| `trade-profile.consolidate` | 画像聚合 | 拉取所有模块数据整合（新建）| 聚合, 全览 | async |

### 🏔️ 山木 — 业务执行 · 触达推进 · 履约交付

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `guike-zhilu.search-outreach` | 搜索+触达 | 搜索目标买家→清洗→触达闭环 | 找买家, 触达, 开发信 | async |
| `guike-zhilu.outreach` | 主动触达 | 自动生成开发信+多轮触达 | 开发信, 联系, outreach | async |
| `guike-zhilu.nurture` | 线索培育 | 长周期跟进+关系维护 | 培育, 跟进, 维护 | async |
| `service-layer.supply-chain` | 供应链优化 | 库存/物流/需求预测 [MERGED] | 供应链, 物流, 库存 | async |
| `service-layer.transaction` | 订单履约 | 订单执行全流程管理 [MERGED] | 履约, 发货, 订单 | async |
| `transaction-support.localization` | 多语言内容 | 本地化内容生成 | 本地化, 翻译, 多语言 | sync |
| `cultural-adapter.content` | 跨文化适配 | 文化分析+本地化策略 | 文化适配, 本地化 | sync |

### 📚 素问 — 技术研究 · 合规 · 法律

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `service-layer.compliance` | VAT/退税/合规 | HS编码+退税率+合规检查 [MERGED] | 退税, HS, 合规 | sync |
| `service-layer.contract` | 合同生成+审查 | 中英双语合同/条款库+法律审查 [MERGED] | 合同, 协议, 条款 | sync |
| `service-layer.catalog` | 产品目录匹配 | TF-IDF需求匹配+推荐 [MERGED] | 产品匹配, 目录 | sync |

### 🔍 罔两 — 市场情报 · 验证 · 监控

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `company-enricher.verify` | 公司验证 | 7源交叉验证公司真实性 | 验证, 查公司, 靠谱吗 | sync |
| `company-enricher.enrich` | 信息富化 | ABN/官网/社媒/LinkedIn多源增强 [含verify] | 富化, 详情, 增强 | async |
| `intelligence-hub.competitor-list` | 竞品列表 | 指定品类竞品全量列表 | 竞品列表, 谁在做 | sync |
| `intelligence-hub.platform-monitor` | 平台监控 | Amazon/1688等平台价格监控 | 平台监控, 价格监控 | async |

### 💰 庖丁 — 财务 · 报价 · 风控

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `service-layer.quote` | 报价计算(含退税) | FOB/CFR/到岸价+退税+利润分析 [P2优化] | 报价, 成本, 核算 | sync |
| `service-layer.payment` | 支付结算 | 支付方式对比+汇率管理 [MERGED] | 支付, 收款, 结算 | sync |
| `service-layer.risk` | 风控评估 | 交易对手+市场+政策风险 [MERGED] | 风险, 预警 | sync |
| `service-layer.supplier` | 供应商匹配 | 评分排名+成本对比 [MERGED] | 供应商, 工厂, 找厂家 | sync |
| `service-layer.service-report` | 一键报告 | 报价+合同+合规三合一报告 [P2优化] | 报告, 全览, 分析 | sync |

### 🌟 太一 — 统筹 · 调度 · 进化

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `cross-border-core.route` | 意图路由 | 自然语言→任务路由分派 | 路由, 调度 (内部) | sync |
| `cross-border-core.squad` | 动态编队 | 复杂任务自动组建 Agent 小队 | squad, 编队 (内部) | async |
| `cross-border-core.scheduler` | 定时任务 | cron/一次/周期任务管理 [MERGED] | 定时, 自动, 监控 | async |
| `cross-border-core.evolution` | 自愈/结晶/优化 | 系统自进化+技能固化 [MERGED] | 自愈, 固化, 优化 (内部) | async |
| `cross-border-core.data-integrate` | 数据整合 | 7源数据聚合清洗 [MERGED] | 数据整合, 数据源 | sync |
| `orchestrator.launch` | 冷启动编排 | 产品 Idea→完整跨境方案 | 启动, 推入, 冷启动 | async |
| `orchestrator.diagnose` | 运营诊断 | 现有业务全维度诊断 | 诊断, 分析, 评估 | async |

---

## 统计

| 维度 | 数量 |
|------|------|
| Skill 总数 | 37 |
| 知几 | 12 |
| 山木 | 6 |
| 素问 | 3 |
| 罔两 | 4 |
| 庖丁 | 5 |
| 太一 | 7 |
| sync 模式 | 20 |
| async 模式 | 17 |

> **合并状态**: 28个物理模块 → 18个活跃模块 (P1合并精简)
> 新增 `service-layer` 统一入口 (9模块→1)
> `data-integrator/self-evolution/skill-registry/task-scheduler` → `cross-border-core`
> `conversion-optimizer/cultural-adapter` → `geo-outbound`
> `real-data-verifier` → `company-enricher`
> `data` (空) → [已移除]

---

## 注册流程（新增 Skill）

1. 在对应模块的 `SKILL.md` 增加标准元数据头
2. 在本目录增加一行注册
3. 确保 `entry_point` 路径可 import

**新增注册格式**：
```markdown
| `{module}.{action}` | 中文名 | 一句话功能 | 触发词 | sync/async |
```

---

*维护：太一 · 更新于每次新增 Skill 时*

---

### 📦 service-layer — P1合并统一入口

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `service-layer.trade` | 贸易服务 | 报价+产品目录+供应商匹配（合并） | 报价, 产品, 供应商 | sync |
| `service-layer.legal` | 法律合规 | 合同+合规检查+风险评估（合并） | 合同, 合规, 风控 | sync |
| `service-layer.payment` | 支付交易 | 支付结算+交易支持+供应链（合并） | 支付, 交易, 供应链 | sync |

### ✅ data-verifier-dedup — P1数据验证去重

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `data-verifier-dedup.verify` | 数据验证 | ABN/官网/电话/邮箱多源交叉验证 | 验证, 可信度, 核实 | sync |
| `data-verifier-dedup.dedup` | 合并去重 | 同名/同站/同邮箱自动合并保留最优 | 去重, 合并, 重复 | sync |
| `data-verifier-dedup.quality` | 质量评分 | 完整度/新鲜度/唯一性/一致性评分 | 质量, 评分, 数据质量 | sync |

---

> **合并状态**: `quote-engine/product-catalog/supplier-matcher/contract-legal/compliance-engine/risk-manager/payment-settlement/transaction-support/supply-chain` → `service-layer` (9合1)
> **吸收状态**: `conversion-optimizer/cultural-adapter` → `geo-outbound` | `real-data-verifier` → `company-enricher` | `self-evolution/skill-registry/task-scheduler/data-integrator` → `cross-border-core`
> **新增**: `data-verifier-dedup` (P1数据验证去重)
