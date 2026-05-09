---
name: intelligence-hub
description: '情报中心 — 5版块归一化情报。输出始终按 竞品动态/招标信息/政策法规/行业趋势/买家线索 五个版块组织'
---

# 情报中心 — Agent 调用协议

## 触发规则

| 用户说 | 路由 |
|--------|------|
| "竞品/对手/谁在抢单" | feed(mode=selected, bucket=competitors) |
| "招标/tender/项目采购" | feed(mode=selected, bucket=tenders) |
| "政策/法规/关税/合规" | feed(mode=selected, bucket=policies) |
| "趋势/市场/行业分析" | feed(mode=selected, bucket=trends) |
| "买家/线索/客户需求" | feed(mode=selected, bucket=leads) |
| "最近情报/有什么消息" | feed(mode=selected) — 全部5版块 |
| "全部情报/所有信息" | feed(mode=all) |

## 5 版块归一化

所有原始情报经过 `normalize()` 自动归到以下 5 桶：

```
竞品动态  → 竞品新品/价格变动/市场动作/营销策略
招标信息  → 招标/采购/RFQ/项目公告
政策法规  → 关税/认证/标准/合规变动
行业趋势  → 市场分析/增长率/预测/机会
买家线索  → 采购需求/直接买家/线索
```

## 调用方式

```python
from core import IntelligenceHub

hub = IntelligenceHub()

# 精选层（默认）— 最近7天
hub.feed(mode="selected")
hub.feed(mode="selected", bucket="competitors")
hub.feed(mode="selected", bucket="tenders", days=3)

# 日报层 — 按版块打包聚合
hub.feed(mode="daily")

# 全量层
hub.feed(mode="all")
```

## 输出格式

```python
# feed() 返回格式
{
  "mode": "selected|daily|all",
  "count": 12,
  "items": [{"bucket": "competitors", "title": "...", ...}]  # selected/all
  "groups": {"competitors": {"label": "竞品动态", "items": [...]}}  # daily
}
```

## 负向规则

- 不要用 `execute(task="competitor")` 这种旧接口绕过5版块归一化
- 不要混合 category 时不用版块分组 — 默认按桶分组输出
- 用户没说 bucket 时输出全部 5 版块
- 用户没说"全部"时默认走 selected 精选层
