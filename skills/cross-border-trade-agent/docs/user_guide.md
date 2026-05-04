# 全域跨境贸易 Agent v8.6 用户指南

> **版本**: v8.6  
> **更新时间**: 2026-04-19  
> **适用对象**: 跨境贸易从业者/外贸企业/运营团队

---

## 📖 快速开始

### 1. 系统架构

```
全域跨境贸易 Agent v8.6
├── 贵客之路 (6 模块) - 搜寻→清洗→触达→培育→转化
├── GEO 外贸开发 (7 模块) - 市场分析→潜客→内容→监测
├── 智能决策 (4 模块) - 选品/厂家/趋势/竞品
├── 交易支持 (4 模块) - 物流/价格/销售/客服
├── 数据整合 (8 模块) - 7 大数据源统一接口
├── 外贸社媒 (11 模块) - B2B/B2C 内容/规划/分析
├── 自媒体运营 (4 模块) - 内容/私域/品牌/自进化
└── P1/P2/P3 (5 模块) - 自进化/定时/报告/渠道/合作
```

### 2. 核心能力

| 能力 | 说明 | 使用场景 |
|------|------|---------|
| **智能贵客** | 7 大数据源搜寻潜客 | 外贸客户开发 |
| **GEO 外贸** | Google Trends+AI 搜索 | 市场趋势分析 |
| **B2B 运营** | 安全感内容生成 | LinkedIn/Facebook |
| **B2C 运营** | 画面感内容生成 | Instagram/TikTok |
| **自媒体** | 内容生产 + 私域运营 | 品牌建设 |
| **自进化** | 结晶模式 + 技能记忆 | 持续优化 |

---

## 🚀 使用指南

### 场景 1: 寻找新客户

```python
# 使用贵客之路模块
from prospect_search import ProspectSearch

search = ProspectSearch()
leads = search.search_by_hs_code("8507.60")  # HS 编码搜索
verified = search.verify_leads(leads)  # 数据验证
```

### 场景 2: 市场趋势分析

```python
# 使用 Google Trends 模块
from google_trends_integrator import GoogleTrendsIntegrator

trends = GoogleTrendsIntegrator()
data = trends.get_keyword_trend("portable power station")
```

### 场景 3: B2B 内容生成

```python
# 使用 B2B 安全感内容模块
from b2b_platform_module import B2BPlatformModule

b2b = B2BPlatformModule()
b2b.generate_factory_proof({"name": "深圳兴旺工具厂"})
b2b.generate_customer_testimonials({"customer": "美国某企业"})
```

### 场景 4: B2C 内容生成

```python
# 使用 B2C 画面感内容模块
from b2c_platform_module import B2CPlatformModule

b2c = B2CPlatformModule()
b2c.generate_desire_content("product_showcase", {"product": "储能电源"})
b2c.generate_desire_content("scarcity", {"discount": "50% OFF"})
```

### 场景 5: 自媒体运营

```python
# 使用自媒体运营引擎
from self_media_engine import SelfMediaEngine

engine = SelfMediaEngine()
engine.plan_content("daily_news", "跨境贸易每日新闻")
engine.track_traffic("seo", {"views": 5000})
engine.analyze_funnel({"traffic": 10000, "awareness_count": 200})
```

### 场景 6: 私域用户管理

```python
# 使用私域运营引擎
from private_traffic_engine import PrivateTrafficEngine

engine = PrivateTrafficEngine()
user = engine.add_user({"name": "张总", "total_value": 150000})
engine.add_tag(user["id"], "高价值")
engine.record_interaction(user["id"], {"type": "call", "result": "意向强烈"})
```

### 场景 7: 品牌建设

```python
# 使用品牌建设引擎
from brand_building_engine import BrandBuildingEngine

engine = BrandBuildingEngine()
engine.define_brand_positioning({"name": "太一 AGI"})
engine.collect_reputation({"type": "testimonial", "rating": 5})
score = engine.calculate_brand_score()
```

### 场景 8: 自进化

```python
# 使用自进化引擎
from self_evolution_engine import SelfEvolutionEngine

engine = SelfEvolutionEngine()
engine.extract_pattern({"pattern": "晨间推送=用户粘性 +80%", "confidence": 0.95})
engine.store_memory({"type": "运营经验", "content": "深度分析 + 案例=高转化"})
report = engine.generate_evolution_report()
```

---

## ⚙️ 定时任务配置

### 已配置任务

| 任务 | 时间 | 说明 |
|------|------|------|
| 晨间新闻推送 | 每日 08:00 | 7 类×5 条新闻 |
| 周度深度分析 | 工作日 09:00 | 行业分析 |
| 流量数据汇总 | 每日 20:00 | 全渠道汇总 |
| 转化漏斗分析 | 每周五 18:00 | 瓶颈识别 |
| 自进化报告 | 每周日 22:00 | 结晶/记忆/优化 |
| 品牌健康度报告 | 每周一 10:00 | 品牌评分 |
| 私域运营报告 | 每周一 11:00 | 用户分层 |
| 数据备份 | 每日 03:00 | 自动备份 |

### 安装 crontab

```bash
# 查看配置
cat data/cross-border/cron/openclaw_cron

# 安装
crontab data/cross-border/cron/openclaw_cron

# 验证
crontab -l
```

---

## 📊 运营报告

### 生成报告

```python
# 每日报告
from operation_report_generator import OperationReportGenerator

generator = OperationReportGenerator()
daily = generator.generate_daily_report()
md = generator.export_report(daily["id"], format="md")

# 每周报告
weekly = generator.generate_weekly_report()

# 每月报告
monthly = generator.generate_monthly_report()
```

### 报告位置

- 每日报告：`reports/cross-border/operation/`
- 每周报告：`reports/cross-border/operation/`
- 每月报告：`reports/cross-border/operation/`

---

## 🔌 API 集成

### Google Trends API

```python
# 使用系统内 Google API (如果已配置)
from google_trends_integrator import GoogleTrendsIntegrator

trends = GoogleTrendsIntegrator()

# 获取趋势数据
data = trends.get_keyword_trend(
    keyword="portable power station",
    geo="US",
    time_range="today 12-m"
)

# 对比多个关键词
comparison = trends.compare_keywords(
    keywords=["portable power station", "solar generator"],
    geo="US"
)

# 与 Google Ads 数据融合
integrated = trends.integrate_with_google_ads(
    keyword="portable power station",
    ads_data={"search_volume": 50000, "competition": "MEDIUM"}
)
```

### 7 大数据源 API

| 数据源 | 模块 | API 状态 |
|--------|------|---------|
| 全球海关数据 | global_customs_integrator.py | 🟡 模拟数据 |
| 电商销售数据 | ecommerce_integrator.py | 🟡 模拟数据 |
| 互联网平台 | internet_platforms_integrator.py | 🟡 模拟数据 |
| 搜索引擎 | search_engines_integrator.py | 🟡 模拟数据 |
| 第三方报告 | third_party_reports_integrator.py | 🟡 模拟数据 |
| 物流数据 | logistics_integrator.py | 🟡 模拟数据 |
| Google Ads | google_ads_integrator.py | 🟡 模拟数据 |

**注**: 当前使用模拟数据，接入真实 API 需配置对应密钥。

---

## 📁 数据管理

### 数据目录

```
data/cross-border/
├── b2b_platform/          # B2B 平台数据
├── b2c_platform/          # B2C 平台数据
├── self_media/            # 自媒体运营数据
├── private_traffic/       # 私域运营数据
├── brand_building/        # 品牌建设数据
├── self_evolution/        # 自进化数据
├── cron/                  # 定时任务配置
├── trends/                # Google Trends 数据
└── optimization/          # 流程优化数据
```

### 数据备份

```bash
# 手动备份
python3 scripts/backup.py

# 自动备份 (每日 03:00)
# 已配置 crontab 任务
```

---

## 🎯 最佳实践

### 1. B2B 内容策略

- ✅ 工厂实景展示 (建立信任)
- ✅ 出货记录公示 (证明实力)
- ✅ 客户案例见证 (社会证明)
- ✅ 认证资质展示 (合规合法)
- ✅ 售后服务承诺 (消除顾虑)

### 2. B2C 内容策略

- ✅ 高清产品图片 (视觉冲击)
- ✅ 使用场景展示 (画面感)
- ✅ 用户评价晒图 (社会证明)
- ✅ 限时折扣促销 (紧迫感)
- ✅ 开箱视频 (期待感)

### 3. 自媒体运营

- ✅ 每日晨间推送 (用户粘性)
- ✅ 每周深度分析 (专业度)
- ✅ 每月直播分享 (互动转化)
- ✅ 持续私域运营 (复购转介绍)

### 4. 自进化循环

```
运营执行 → 数据采集 → 分析洞察 → 结晶提取
    ↓                            ↑
    ← 自动优化 ← 技能记忆 ←──────┘
```

---

## ❓ 常见问题

### Q1: 如何接入真实 API 数据？

**A**: 在 `config/api_keys.json` 中配置对应 API 密钥，然后修改对应模块的数据获取方法。

### Q2: 定时任务不执行怎么办？

**A**: 
1. 检查 crontab 是否安装：`crontab -l`
2. 检查 cron 服务状态：`systemctl status cron`
3. 查看日志：`grep CRON /var/log/syslog`

### Q3: 如何查看运营报告？

**A**: 报告位于 `reports/cross-border/operation/` 目录，Telegram 可直接打开.md 文件。

### Q4: 自进化数据在哪里？

**A**: `data/cross-border/self_evolution/self_evolution_engine.json`

---

## 🔗 相关文档

- 架构文档：`ARCHITECTURE_V85.md`
- 自媒体运营方案：`self_media_operation_plan.md`
- 集成测试报告：`INTEGRATION_TEST_REPORT.md`
- API 文档：`API_REFERENCE.md` (待创建)

---

*太一全域跨境贸易 Agent v8.6 · 用户指南 v1.0*  
*更新时间：2026-04-19 20:23*  
*文档状态：✅ 完成*
