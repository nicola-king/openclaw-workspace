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

### 🏔️ 山木 — 业务执行 · 触达推进 · 履约交付

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `guike-zhilu.search-outreach` | 搜索+触达 | 搜索目标买家→清洗→触达闭环 | 找买家, 触达, 开发信 | async |
| `guike-zhilu.outreach` | 主动触达 | 自动生成开发信+多轮触达 | 开发信, 联系, outreach | async |
| `guike-zhilu.nurture` | 线索培育 | 长周期跟进+关系维护 | 培育, 跟进, 维护 | async |
| `supply-chain.optimize` | 供应链优化 | 库存/物流/需求预测 | 供应链, 物流, 库存 | async |
| `transaction-support.fulfill` | 订单履约 | 订单执行全流程管理 | 履约, 发货, 订单 | async |
| `transaction-support.localization` | 多语言内容 | 本地化内容生成 | 本地化, 翻译, 多语言 | sync |
| `cultural-adapter.content` | 跨文化适配 | 文化分析+本地化策略 | 文化适配, 本地化 | sync |

### 📚 素问 — 技术研究 · 合规 · 法律

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `compliance-engine.vat-check` | VAT/退税查询 | HS编码+退税率+合规检查 | 退税, HS, 合规 | sync |
| `compliance-engine.regulation` | 法规追踪 | 目标市场法规变动监控 | 法规, 合规变动 | async |
| `compliance-engine.customs` | 清关自动化 | 海关文件+关税计算 | 清关, 海关, 关税 | sync |
| `contract-legal.generate` | 合同生成 | 中英双语合同/条款库 | 合同, 协议, 条款 | sync |
| `contract-legal.review` | 法律审查 | 合同条款审查+风险提示 | 审查, 法律风险 | sync |
| `cultural-adapter.compliance` | 跨文化合规 | 宗教/文化/商业惯例合规 | 文化合规, 习俗 | sync |
| `product-catalog.match` | 产品目录匹配 | TF-IDF需求匹配+推荐 | 产品匹配, 目录 | sync |

### 🔍 罔两 — 市场情报 · 验证 · 监控

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `company-enricher.verify` | 公司验证 | 7源交叉验证公司真实性 | 验证, 查公司, 靠谱吗 | sync |
| `company-enricher.enrich` | 信息富化 | ABN/官网/社媒/LinkedIn多源增强 | 富化, 详情, 增强 | async |
| `real-data-verifier.five-way` | 五项验证 | 公司/电话/邮箱/官网/LinkedIn全验证 | 验证, 查真伪 | sync |
| `intelligence-hub.competitor-list` | 竞品列表 | 指定品类竞品全量列表 | 竞品列表, 谁在做 | sync |
| `intelligence-hub.platform-monitor` | 平台监控 | Amazon/1688等平台价格监控 | 平台监控, 价格监控 | async |

### 💰 庖丁 — 财务 · 报价 · 风控

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `quote-engine.calculate` | 报价计算 | FOB/CFR/到岸价+退税+利润 | 报价, 成本, 核算 | sync |
| `quote-engine.profit-analysis` | 利润分析 | 多场景利润对比+建议 | 利润, 盈利 | sync |
| `payment-settlement.channel` | 支付通道 | 支付方式对比+汇率管理 | 支付, 收款, 结算 | sync |
| `payment-settlement.forex` | 汇率管理 | 实时汇率+趋势预测 | 汇率, 换汇 | sync |
| `risk-manager.identify` | 风险识别 | 交易对手+市场+政策风险识别 | 风险, 预警 | sync |
| `risk-manager.hedge` | 对冲策略 | 汇率/价格/信用对冲建议 | 对冲, 规避风险 | sync |
| `supplier-matcher.match` | 供应商匹配 | 9工厂评分排名+成本对比 | 供应商, 工厂, 找厂家 | sync |

### 🌟 太一 — 统筹 · 调度 · 进化

| Skill ID | 名称 | 描述 | 触发词 | 模式 |
|----------|------|------|--------|------|
| `cross-border-core.route` | 意图路由 | 自然语言→任务路由分派 | 路由, 调度 (内部) | sync |
| `cross-border-core.squad` | 动态编队 | 复杂任务自动组建 Agent 小队 | squad, 编队 (内部) | async |
| `task-scheduler.jobs` | 定时任务 | cron/一次/周期任务管理 | 定时, 自动, 监控 | async |
| `self-evolution.heal` | 自愈 | 系统健康检查+自动修复 | 自愈, 修复 (内部) | async |
| `self-evolution.crystallize` | 技能结晶 | 重复模式→固化技能 | 结晶, 固化 (内部) | async |
| `self-evolution.optimize` | Token 优化 | 压缩/精简/效率提升 | 优化, 压缩 (内部) | async |
| `orchestrator.launch` | 冷启动编排 | 产品 Idea→完整跨境方案 | 启动, 推入, 冷启动 | async |
| `orchestrator.diagnose` | 运营诊断 | 现有业务全维度诊断 | 诊断, 分析, 评估 | async |

---

## 统计

| 维度 | 数量 |
|------|------|
| Skill 总数 | 42 |
| 知几 | 12 |
| 山木 | 7 |
| 素问 | 8 |
| 罔两 | 5 |
| 庖丁 | 7 |
| 太一 | 8 |
| sync 模式 | 22 |
| async 模式 | 20 |

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
