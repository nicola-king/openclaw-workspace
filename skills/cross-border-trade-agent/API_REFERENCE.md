# 全域跨境贸易 Agent v8.6 API 参考文档

> **版本**: v8.6  
> **更新时间**: 2026-04-19  
> **API 状态**: 🟡 模拟数据 (可切换真实 API)

---

## 📋 API 总览

### 核心 API 分类

| 分类 | 模块数 | 说明 |
|------|--------|------|
| 获客 API | 6 | 潜客搜寻/验证/触达/培育 |
| GEO API | 7 | 市场分析/AI 搜索/内容/监测 |
| 决策 API | 4 | 选品/厂家/趋势/竞品 |
| 交易 API | 4 | 物流/价格/销售/客服 |
| 数据 API | 8 | 7 大数据源 + 整合中心 |
| 社媒 API | 11 | B2B/B2C 内容/规划/分析 |
| 运营 API | 4 | 内容/私域/品牌/自进化 |
| 工具 API | 5 | 自进化/定时/报告/渠道/合作 |

---

## 🔌 Google API 集成

### Google Trends API

**模块**: `google_trends_integrator.py`

**状态**: 🟡 模拟数据 (可切换真实 API)

**通用性**: ✅ Google AI API 通用

**系统内 Google API 配置**:

```json
// config/google_api_config.json
{
  "provider": "google_ai",
  "api_key": "${GOOGLE_API_KEY}",
  "endpoints": {
    "trends": "https://trends.google.com/api",
    "ads": "https://googleads.googleapis.com"
  },
  "rate_limit": {
    "requests_per_minute": 60,
    "requests_per_day": 10000
  }
}
```

**API 方法**:

```python
from google_trends_integrator import GoogleTrendsIntegrator

trends = GoogleTrendsIntegrator()

# 1. 获取关键词趋势
data = trends.get_keyword_trend(
    keyword="portable power station",
    geo="US",           # 国家/地区代码
    time_range="today 12-m"  # 时间范围
)
# 返回：{average_interest, trend_direction, growth_rate, ...}

# 2. 对比多个关键词
comparison = trends.compare_keywords(
    keywords=["portable power station", "solar generator"],
    geo="US"
)
# 返回：{ranking, insights, comparison}

# 3. 获取热门关键词
trending = trends.get_trending_keywords(
    category="all",
    geo="US",
    limit=10
)
# 返回：[{keyword, interest, growth}, ...]

# 4. 与 Google Ads 数据融合
integrated = trends.integrate_with_google_ads(
    keyword="portable power station",
    ads_data={
        "search_volume": 50000,
        "competition": "MEDIUM",
        "cpc": 2.5
    }
)
# 返回：{trends_data, ads_data, combined_insights, recommendation}
```

**真实 API 接入**:

```python
# 使用真实 Google Trends API (pytrends)
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

# 构建请求
pytrends.build_payload(
    kw_list=['portable power station'],
    timeframe='today 12-m',
    geo='US'
)

# 获取数据
data = pytrends.interest_over_time()
```

---

## 📊 7 大数据源 API

### 1. 全球海关数据 API

**模块**: `global_customs_integrator.py`

**状态**: 🟡 模拟数据

```python
from global_customs_integrator import GlobalCustomsIntegrator

customs = GlobalCustomsIntegrator()
data = customs.get_customs_data(
    hs_code="8507.60",
    country="US",
    date_range="2025-01-01_2025-12-31"
)
```

**真实 API**:
- 中国海关：`http://www.customs.gov.cn`
- 美国海关：`https://www.cbp.gov`
- 欧盟海关：`https://ec.europa.eu/taxation_customs`

---

### 2. 电商销售数据 API

**模块**: `ecommerce_integrator.py`

**状态**: 🟡 模拟数据

```python
from ecommerce_integrator import EcommerceIntegrator

ecom = EcommerceIntegrator()
data = ecom.get_sales_data(
    platform="Amazon",
    category="Electronics",
    date_range="2025-Q4"
)
```

**真实 API**:
- Amazon SP-API: `https://sellercentral.amazon.com/developer`
- eBay API: `https://developer.ebay.com`
- Shopify API: `https://shopify.dev/api`

---

### 3. 互联网平台 API

**模块**: `internet_platforms_integrator.py`

**状态**: 🟡 模拟数据

---

### 4. 搜索引擎 API

**模块**: `search_engines_integrator.py`

**状态**: 🟡 模拟数据

**真实 API**:
- Google Custom Search: `https://developers.google.com/custom-search`
- Bing Search: `https://www.microsoft.com/en-us/bing/apis`

---

### 5. 第三方报告 API

**模块**: `third_party_reports_integrator.py`

**状态**: 🟡 模拟数据

**真实 API**:
- Statista: `https://www.statista.com`
- Gartner: `https://www.gartner.com`
- IDC: `https://www.idc.com`

---

### 6. 物流数据 API

**模块**: `logistics_integrator.py`

**状态**: 🟡 模拟数据

**真实 API**:
- 17Track: `https://www.17track.net`
- AfterShip: `https://www.aftership.com`
- 船讯网：`https://www.shipxy.com`

---

### 7. Google Ads API

**模块**: `google_ads_integrator.py`

**状态**: 🟡 模拟数据

**真实 API**: `https://developers.google.com/google-ads/api`

---

## 📱 自媒体运营 API

### 内容生产 API

**模块**: `self_media_engine.py`

```python
from self_media_engine import SelfMediaEngine

engine = SelfMediaEngine()

# 内容规划
content = engine.plan_content(
    content_type="daily_news",
    topic="跨境贸易每日新闻"
)

# 流量追踪
traffic = engine.track_traffic(
    channel="seo",
    metrics={"views": 5000, "clicks": 500}
)

# 漏斗分析
funnel = engine.analyze_funnel({
    "traffic": 10000,
    "awareness_count": 200,
    "interest_count": 40
})
```

---

### 私域运营 API

**模块**: `private_traffic_engine.py`

```python
from private_traffic_engine import PrivateTrafficEngine

engine = PrivateTrafficEngine()

# 添加用户
user = engine.add_user({
    "name": "张总",
    "source": "LinkedIn",
    "total_value": 150000
})

# 添加标签
engine.add_tag(user["id"], "高价值")

# 记录互动
engine.record_interaction(
    user["id"],
    {"type": "call", "channel": "电话", "result": "意向强烈"}
)

# 创建活动
campaign = engine.create_campaign({
    "name": "VIP 客户答谢会",
    "type": "offline_event",
    "target_segment": "vip"
})
```

---

### 品牌建设 API

**模块**: `brand_building_engine.py`

```python
from brand_building_engine import BrandBuildingEngine

engine = BrandBuildingEngine()

# 品牌定位
positioning = engine.define_brand_positioning({
    "name": "太一 AGI",
    "slogan": "太一出手，跨境无忧"
})

# 品牌内容
content = engine.create_brand_content({
    "type": "industry_report",
    "title": "2026 跨境贸易趋势报告"
})

# 品牌评分
score = engine.calculate_brand_score()
```

---

## 🧬 自进化 API

**模块**: `self_evolution_engine.py`

```python
from self_evolution_engine import SelfEvolutionEngine

engine = SelfEvolutionEngine()

# 结晶模式提取
pattern = engine.extract_pattern({
    "type": "content",
    "pattern": "晨间推送=用户粘性 +80%",
    "confidence": 0.95
})

# 技能记忆存储
memory = engine.store_memory({
    "type": "运营经验",
    "content": "深度分析 + 案例=高转化",
    "confidence": 0.90
})

# 自动优化执行
opt = engine.execute_optimization({
    "target": "内容发布频率",
    "action": "从每日 3 篇增加到每日 5 篇"
})

# 效果数据回流
feedback = engine.collect_feedback({
    "source": "LinkedIn",
    "type": "content_performance",
    "metrics": {"views": 5000, "engagement": 400}
})
```

---

## 📊 运营报告 API

**模块**: `operation_report_generator.py`

```python
from operation_report_generator import OperationReportGenerator

generator = OperationReportGenerator()

# 每日报告
daily = generator.generate_daily_report("2026-04-19")

# 每周报告
weekly = generator.generate_weekly_report("2026-04-14")

# 每月报告
monthly = generator.generate_monthly_report("2026-04")

# 导出报告
md_report = generator.export_report(daily["id"], format="md")
json_report = generator.export_report(daily["id"], format="json")
```

---

## 🔗 渠道扩展 API

**模块**: `channel_expansion_module.py`

```python
from channel_expansion_module import ChannelExpansionModule

module = ChannelExpansionModule()

# 发现渠道
channels = module.discover_channels(category="all")

# 评估渠道
evaluation = module.evaluate_channel({
    "name": "TikTok",
    "type": "短视频",
    "audience": "全球"
})

# 接入渠道
integration = module.integrate_channel({
    "name": "Amazon",
    "type": "电商"
})

# 优化渠道
optimization = module.optimize_channel(
    "Amazon",
    {"engagement_rate": 1.5, "posting_frequency": 2}
)
```

---

## 🤝 品牌合作 API

**模块**: `brand_partnership_module.py`

```python
from brand_partnership_module import BrandPartnershipModule

module = BrandPartnershipModule()

# 识别合作伙伴
partners = module.identify_partners(partner_type="all")

# 制定合作方案
proposal = module.create_proposal({
    "name": "外贸大咖李老师",
    "type": "kol",
    "audience": "50 万+"
})

# 执行合作
collab = module.execute_collaboration(proposal["id"])

# 评估合作
evaluation = module.evaluate_collaboration(
    collab["id"],
    {"investment": 10000, "return": 25000, "satisfaction": 4.5}
)
```

---

## 🔐 API 认证

### API 密钥配置

```json
// config/api_keys.json
{
  "google": {
    "api_key": "${GOOGLE_API_KEY}",
    "credentials": "${GOOGLE_APPLICATION_CREDENTIALS}"
  },
  "customs": {
    "api_key": "${CUSTOMS_API_KEY}"
  },
  "amazon": {
    "client_id": "${AMAZON_CLIENT_ID}",
    "client_secret": "${AMAZON_CLIENT_SECRET}"
  }
}
```

### 环境变量

```bash
# .env 文件
GOOGLE_API_KEY=your_google_api_key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
CUSTOMS_API_KEY=your_customs_api_key
AMAZON_CLIENT_ID=your_amazon_client_id
```

---

## 📈 速率限制

| API | 限制 | 说明 |
|-----|------|------|
| Google Trends | 60 次/分钟 | 免费额度 |
| Google Ads | 10000 次/天 | 需认证 |
| 海关数据 | 100 次/天 | 免费额度 |
| 电商数据 | 500 次/小时 | 需认证 |

---

## ❓ 常见问题

### Q1: Google AI API 是否通用？

**A**: ✅ 是的，Google AI API 通用。太一系统内已配置 Google API，可直接使用。

### Q2: 如何切换真实 API？

**A**: 在对应模块中修改数据获取方法，从模拟数据切换到真实 API 调用。

### Q3: API 密钥在哪里配置？

**A**: `config/api_keys.json` 或环境变量。

---

*太一全域跨境贸易 Agent v8.6 · API 参考文档 v1.0*  
*更新时间：2026-04-19 20:23*  
*API 状态：🟡 模拟数据 (可切换真实 API)*
