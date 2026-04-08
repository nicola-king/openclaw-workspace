# 天机情报系统 v2.0 - last30days 整合

> 基于 last30days-skill | 版本：v2.0 | 创建：2026-03-27

---

## 🎯 核心功能对比

| 功能 | last30days | 太一天机 v1.0 | 太一天机 v2.0 |
|------|------------|-------------|-------------|
| **数据源** | 8 平台 | Polymarket+ 链上 | 8 平台 +Polymarket+ 链上 |
| **时间范围** | 30 天 | 实时 | 实时 +30 天历史 |
| **排序** | 互动量/相关性 | 置信度 | 多维排序 |
| **报告生成** | ✅ | ⏳ | ✅ 增强 |
| **A vs B 对比** | ✅ | ❌ | ✅ 新增 |
| **账号发现** | ✅ | ⏳ | ✅ 增强 |

---

## 🛠️ 技术整合方案

### 方案 1: 直接复用 last30days-skill

```bash
# 克隆 last30days-skill 代码
git clone https://github.com/your-repo/last30days-skill.git
cd last30days-skill

# 配置 API Keys
export REDDIT_CLIENT_ID=xxx
export REDDIT_CLIENT_SECRET=xxx
export TWITTER_API_KEY=xxx
# ...

# 运行
python last30days.py "Polymarket trading strategy"
```

**优势**:
- ✅ 快速启动
- ✅ 代码成熟
- ✅ 多平台支持

**劣势**:
- ❌ 需要配置多个 API
- ❌ 可能需要付费 API

---

### 方案 2: 太一自研增强版

```python
#!/usr/bin/env python3
"""
太一天机情报系统 v2.0

整合:
- last30days-skill (社交平台)
- Polymarket Gamma API (链上数据)
- 聪明钱钱包监控
- AI 摘要生成 (山木)
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta

# 数据源配置
DATA_SOURCES = {
    "reddit": {
        "endpoint": "https://oauth.reddit.com/search.json",
        "enabled": True
    },
    "twitter": {
        "endpoint": "https://api.twitter.com/2/tweets/search/recent",
        "enabled": True
    },
    "youtube": {
        "endpoint": "https://www.googleapis.com/youtube/v3/search",
        "enabled": True
    },
    "polymarket": {
        "endpoint": "https://gamma-api.polymarket.com/events",
        "enabled": True
    },
    # 添加更多...
}

# 搜索关键词
KEYWORDS = [
    "Polymarket strategy",
    "prediction market arbitrage",
    "crypto trading alpha",
    "DeFi yield farming",
]


async def fetch_reddit_posts(keyword: str, session: aiohttp.ClientSession) -> list:
    """获取 Reddit 热门帖子"""
    url = f"https://oauth.reddit.com/search.json?q={keyword}&sort=hot&t=month&limit=50"
    
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            posts = data.get("data", {}).get("children", [])
            
            return [{
                "platform": "Reddit",
                "title": post["data"]["title"],
                "url": f"https://reddit.com{post['data']['permalink']}",
                "score": post["data"]["score"],
                "comments": post["data"]["num_comments"],
                "created": datetime.fromtimestamp(post["data"]["created_utc"]),
                "subreddit": post["data"]["subreddit"]
            } for post in posts[:20]]
    
    return []


async def fetch_polymarket_events(session: aiohttp.ClientSession) -> list:
    """获取 Polymarket 热门事件"""
    url = "https://gamma-api.polymarket.com/events?limit=50&sortedBy=volume"
    
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            events = data.get("events", [])
            
            return [{
                "platform": "Polymarket",
                "title": event.get("question", "Unknown"),
                "url": f"https://polymarket.com/event/{event.get('slug', '')}",
                "volume": event.get("volume", 0),
                "liquidity": event.get("liquidity", 0),
                "endDate": event.get("endDate", "")
            } for event in events[:20]]
    
    return []


async def generate_report(data: dict) -> str:
    """生成情报报告"""
    report = f"""
# 太一天机情报报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
搜索范围：过去 30 天

━━━━━━━━━━━━━━━━━━━━━

## 📊 热门话题 Top 10

"""
    
    # 按热度排序
    all_items = []
    for platform, items in data.items():
        for item in items:
            score = item.get("score", item.get("volume", 0))
            all_items.append({**item, "score": score})
    
    all_items.sort(key=lambda x: x["score"], reverse=True)
    
    for i, item in enumerate(all_items[:10], 1):
        report += f"""
{i}. **{item['title']}**
   平台：{item['platform']}
   热度：{item['score']}
   链接：{item['url']}

"""
    
    report += """
━━━━━━━━━━━━━━━━━━━━━

## 🎯 交易信号

基于以上情报，发现以下交易机会：

1. [信号 1]
2. [信号 2]
3. [信号 3]

━━━━━━━━━━━━━━━━━━━━━

## 📈 趋势分析

- 上升趋势：[话题 1], [话题 2]
- 下降趋势：[话题 3]
- 新兴话题：[话题 4]

━━━━━━━━━━━━━━━━━━━━━

*太一 AGI · 天机情报系统 v2.0*
"""
    
    return report


async def main():
    """主函数"""
    print("🚀 太一天机情报系统 v2.0 启动...")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        # 并行获取各平台数据
        for keyword in KEYWORDS:
            if DATA_SOURCES["reddit"]["enabled"]:
                tasks.append(fetch_reddit_posts(keyword, session))
            
            if DATA_SOURCES["polymarket"]["enabled"]:
                tasks.append(fetch_polymarket_events(session))
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 整合数据
        report_data = {
            "reddit": [],
            "polymarket": []
        }
        
        for result in results:
            if isinstance(result, list):
                for item in result:
                    platform = item.get("platform", "unknown")
                    if platform.lower() in report_data:
                        report_data[platform.lower()].append(item)
        
        # 生成报告
        report = await generate_report(report_data)
        
        # 保存报告
        output_file = f"/home/nicola/.openclaw/workspace/reports/tianji-intel-{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✅ 情报报告已生成：{output_file}")


if __name__ == "__main__":
    asyncio.run(main())
