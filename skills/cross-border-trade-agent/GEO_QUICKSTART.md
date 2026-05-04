# GEO 优化快速启动指南

> **版本**: v1.0  
> **创建**: 2026-04-20 21:16  
> **状态**: ✅ 生产就绪  
> **预计启动时间**: 30 分钟

---

## 🚀 快速启动 (30 分钟)

### 步骤 1: 配置目标品牌和产品 (5 分钟)

编辑 `geo_config.json`:

```bash
cd /home/sayelf/.openclaw/workspace/skills/01-trading/cross-border-trade-agent
nano geo_config.json
```

修改以下字段:
```json
{
  "brand": "你的品牌名称",
  "product_keywords": [
    "你的产品 1",
    "你的产品 2",
    "你的产品 3"
  ],
  "target_markets": [
    "USA",
    "UK",
    "Germany",
    "Japan",
    "China"
  ]
}
```

---

### 步骤 2: 运行首次基线审计 (10 分钟)

```bash
# 运行 GEO 审计
python3 geo_auditor.py
```

**输出示例**:
```
🎯 开始 GEO 审计：YourBrand
📦 产品关键词：['wireless earbuds', 'smart water bottle']
🌍 目标市场：['USA', 'UK', 'Germany', 'Japan']
🤖 引擎数量：4
📝 查询模板：8

📊 总查询数：64

📊 GEO 审计报告摘要 - YourBrand
============================================================
审计日期：2026-04-20T21:16:18
测试查询：64
测试引擎：ChatGPT, Claude, Perplexity, Gemini
整体提及率：0.0%

优化建议 (Top 5):
  1. 📊 增强 E-E-A-T 信号：添加作者页面、专家引用、第三方验证
  2. 🏷️ 完善 Schema 标记：Product/Review/FAQPage/Organization
  3. 📰 建立 Earned Media 管道：PR、客座文章、媒体背书
  4. 🌐 多语言本地化：每个目标市场独立构建权威
  5. 📈 创建比较内容：'品牌 A vs 品牌 B'类型内容
============================================================
```

**注意**: 首次运行提及率为 0% 是正常的！这是基线，后续优化后会提升。

---

### 步骤 3: 初始化 Earned Media 追踪 (5 分钟)

```bash
# 初始化追踪器 (自动加载目标媒体列表)
python3 earned_media_tracker.py
```

**输出示例**:
```
✅ 加载 0 个媒体机会
🔍 发现媒体机会：['usa', 'china', 'global']
✅ 添加媒体机会：Digital Commerce 360 (优先级：58.0)
✅ 添加媒体机会：Ecommerce News EU (优先级：54.0)
...
✨ 新发现 15 个媒体机会

============================================================
📰 Earned Media 报告 - YourBrand
============================================================
报告日期：2026-04-20T21:16:18
总机会数：15
高优先级：5
进行中活动：0
已发布：0
平均 DA: 65.3
============================================================
```

---

### 步骤 4: 创建首批外展活动 (5 分钟)

```python
# 创建 Python 脚本快速添加活动
from earned_media_tracker import EarnedMediaTracker, OutreachStatus

tracker = EarnedMediaTracker(brand="YourBrand")

# 查看高优先级机会
high_priority = [
    opp for opp in tracker.opportunities
    if opp.priority_score >= 70
]

print(f"高优先级媒体：{len(high_priority)}")
for opp in high_priority[:5]:
    print(f"  - {opp.name} (DA: {opp.domain_authority}, 优先级：{opp.priority_score:.1f})")

# 为 Top 3 创建外展活动
for opp in high_priority[:3]:
    campaign = tracker.create_campaign(
        opportunity_id=opp.id,
        content_type="guest_post",
        notes=f"客座文章提案：{opp.name}"
    )
    print(f"✅ 创建外展活动：{opp.name}")
```

---

### 步骤 5: 配置定时任务 (5 分钟)

```bash
# 生成 crontab 配置
python3 geo_cron_config.py

# 查看生成的配置
cat geo_crontab.txt

# 安装 (需要确认)
crontab geo_crontab.txt

# 验证安装
crontab -l
```

**定时任务列表**:
| 任务 | 频率 | 时间 |
|------|------|------|
| 每周 GEO 审计 | 每周 | 周一 9:00 |
| 每日 Earned Media 检查 | 每天 | 10:00 |
| 每月 GEO 报告 | 每月 | 1 日 9:00 |
| 每季度策略复盘 | 每季度 | 首月 1 日 10:00 |

---

## 📊 KPI 仪表板使用

### 添加 KPI 记录

```bash
python3 geo_kpi_dashboard.py
```

### 手动添加记录 (示例)

```python
from geo_kpi_dashboard import GEOKPIDashboard

dashboard = GEOKPIDashboard(brand="YourBrand")

# 添加基线记录 (首次审计后)
dashboard.add_record(
    total_queries=100,
    mentioned_count=0,  # 基线可能是 0
    answer_share=0.0,
    positive_sentiment=0,
    neutral_sentiment=0,
    negative_sentiment=0,
    earned_media_count=0,
    owned_media_count=0,
    top_sources=[],
)

# 后续每次审计后更新
dashboard.add_record(
    total_queries=100,
    mentioned_count=25,  # 优化后提升
    answer_share=0.20,
    positive_sentiment=18,
    neutral_sentiment=5,
    negative_sentiment=2,
    earned_media_count=15,
    owned_media_count=10,
    top_sources=["forbes.com", "techcrunch.com"],
)

# 查看仪表板
dashboard.print_dashboard()
```

---

## 🎯 目标设定

基于专家建议，设定以下目标:

| 指标 | 基线 | 3 个月目标 | 6 个月目标 |
|------|------|-----------|-----------|
| 提及率 | 0% | 15% | 30% |
| 答案份额 | 0% | 15% | 25% |
| 正面情感 | 0% | 60% | 70% |
| Earned Media 比例 | 0% | 30% | 50% |

---

## 📋 外展策略

### 客座文章提案模板

```
主题：[你的专业领域] 趋势洞察/实战指南

尊敬的 [媒体名称] 编辑团队，

我是 [你的名字]，[你的公司] 的 [职位]。我在 [领域] 有 [X] 年经验，
曾 [成就/背书]。

我注意到贵站经常发布关于 [主题] 的内容，我想投稿一篇深度文章:

**标题**: [吸引人的标题]
**大纲**:
1. [要点 1]
2. [要点 2]
3. [要点 3]

**独特价值**:
- [原创数据/研究]
- [实战案例]
- [专家访谈]

这篇文章将为您的读者提供 [具体价值]。

期待您的回复！

此致，
[你的名字]
[联系方式]
[LinkedIn/网站]
```

### 跟进节奏

| 时间 | 动作 |
|------|------|
| Day 0 | 发送初始提案 |
| Day 3 | 第一次跟进 (礼貌询问) |
| Day 7 | 第二次跟进 (提供额外价值) |
| Day 14 | 第三次跟进 (最后尝试) |
| Day 21 | 标记为无响应，转向其他媒体 |

---

## 🔧 API 集成 (可选)

### 配置 AI API (需要预算审批)

编辑 `geo_config.json`:

```json
{
  "api_config": {
    "chatgpt_api_key": "sk-xxx",
    "claude_api_key": "sk-ant-xxx",
    "perplexity_api_key": "pplx-xxx",
    "gemini_api_key": "xxx"
  }
}
```

**预估成本** (按每月 4 次审计):
- ChatGPT API: ~$20/月
- Claude API: ~$20/月
- Perplexity API: ~$30/月
- Gemini API: ~$10/月
- **总计**: ~$80/月

---

## 📈 监测和迭代

### 每周检查 (周一 9:00 自动执行)

```bash
# 查看最新报告
cat geo_audit_report.json | jq '.overall_mention_rate'

# 对比上周数据
python3 geo_kpi_dashboard.py
```

### 每月复盘 (每月 1 日 9:00 自动执行)

1. 检查 KPI 进度
2. 分析哪些策略有效
3. 调整下月重点
4. 更新目标媒体列表

### 季度策略调整

1. 深度分析趋势
2. 评估 ROI
3. 调整预算分配
4. 探索新渠道

---

## ⚠️ 常见问题

### Q1: 为什么提及率一直是 0%?

**A**: 新品牌/小品牌通常需要 2-3 个月的持续优化才能看到明显提升。坚持执行:
- 每周审计追踪
- 持续产出 Earned Media (每月 2-4 篇)
- 完善网站 Schema 标记
- 创建高质量比较内容

### Q2: 应该优先哪些媒体?

**A**: 优先级排序:
1. **.edu/.gov** 域名 (AI 最信任)
2. **高 DA (>70)** 行业媒体
3. **目标市场本地** 媒体
4. **评测网站** (G2/Capterra)
5. **行业博主/ influencer**

### Q3: 如何衡量 GEO 的 ROI?

**A**: 追踪以下指标:
- AI 答案提及率 → 品牌曝光
- 网站直接流量变化 → 品牌搜索
- 询盘/转化 → 业务成果
- 对比传统 SEO 成本 → 效率提升

---

## 🔗 相关文档

- `GEO_EXPERT_FRAMEWORK.md` - 专家框架详解
- `geo_auditor.py` - 审计工具
- `earned_media_tracker.py` - 媒体追踪
- `geo_kpi_dashboard.py` - KPI 仪表板
- `geo_config.json` - 配置文件
- `earned_media_targets.json` - 目标媒体列表

---

*太一 AGI · 2026-04-20 21:16*  
*跨境贸易 Agent v8.2 · GEO 优化系统*
