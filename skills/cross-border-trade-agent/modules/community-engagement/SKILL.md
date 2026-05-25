# 跨境贸易社群发现与参与模块 v1.0

> **职责**: 发现/加入/参与国内外跨境贸易社群
> **位置**: `modules/community-engagement/`
> **覆盖**: 国内8类 + 国际10类社群

---

## 覆盖范围

| 区域 | 平台 | 社群数 |
|:----|:----|:-----:|
| 🇨🇳 国内 | 福步论坛、知乎、小红书、微信、QQ、阿里外贸圈、中国制造网、广交会 | 8 |
| 🌐 国际 | LinkedIn、Facebook、Reddit、Discord、WhatsApp、Telegram、Alibaba、TradeKey | 10 |

---

## 使用

```python
from modules.community_engagement.core import CommunityEngagement

eng = CommunityEngagement()

# 发现相关社群
result = eng.discover(product="钢结构", only_high_relevance=True)

# 生成参与计划
plan = eng.create_engagement_plan("折叠房屋", "Australia", top_n=5)

# 记录参与
eng.log_participation("福步外贸论坛", "分享行业报告", result="收到3条询价")
```

## CLI

```bash
python3 core.py --discover 钢结构
python3 core.py --plan '折叠房屋' Australia
python3 core.py --log '福步外贸论坛' '发布产品信息'
```
