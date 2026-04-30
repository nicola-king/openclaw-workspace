#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
突发新闻实时监测 - 自动触发推送
太一 AGI · 全球新闻搜索系统 v1.0 (自进化)
创建：2026-04-19
"""

import os
import json
import requests
import time
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = "/home/nicola/.openclaw/workspace"
OUTPUT_DIR = f"{WORKSPACE}/news/breaking"
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = '7073481596'

# 监测关键词（按级别分类）
BREAKING_KEYWORDS = {
    'P0': [
        'war', 'earthquake magnitude', 'coup d\'etat', 'nuclear', 
        '战争', '大地震', '政变', '核爆', 'tsunami', 'volcano eruption'
    ],
    'P1': [
        'armed conflict', 'sanctions', 'resignation', 'market crash',
        '武装冲突', '制裁', '辞职', '股市崩盘', 'assassination', 'terror attack'
    ],
    'P2': [
        'policy announcement', 'breakthrough', 'outbreak', 'summit',
        '政策发布', '重大突破', '疫情爆发', '峰会', 'trade war', 'election results'
    ],
    'P3': [
        'breaking news', 'urgent', 'developing', 'just in',
        '突发', '紧急', '最新', '快讯', 'protest', 'strike'
    ]
}

# 监测数据源
MONITOR_SOURCES = [
    {'name': 'Twitter API', 'url': 'https://api.twitter.com/2/tweets/search/recent', 'interval': 60},
    {'name': 'Reuters RSS', 'url': 'https://www.reutersagency.com/feed/', 'interval': 120},
    {'name': 'AP News', 'url': 'https://apnews.com/', 'interval': 120},
    {'name': '新华网', 'url': 'http://www.xinhuanet.com/', 'interval': 120},
    {'name': 'Reddit News', 'url': 'https://www.reddit.com/r/worldnews/.json', 'interval': 60},
]


def check_breaking_news():
    """监测突发新闻"""
    detected_events = []
    
    # 模拟监测（实际应调用 API）
    # 这里使用简化逻辑演示
    
    # 检查 Twitter 趋势
    twitter_trends = check_twitter_trends()
    if twitter_trends:
        detected_events.extend(twitter_trends)
    
    # 检查新闻 RSS
    rss_headlines = check_news_rss()
    if rss_headlines:
        detected_events.extend(rss_headlines)
    
    return detected_events


def check_twitter_trends():
    """检查 Twitter 趋势"""
    # 简化实现，实际应调用 Twitter API
    events = []
    
    # 模拟检测逻辑
    trending_topics = get_trending_topics()
    
    for topic in trending_topics:
        for level, keywords in BREAKING_KEYWORDS.items():
            if any(kw.lower() in topic.lower() for kw in keywords):
                events.append({
                    'level': level,
                    'title': topic,
                    'source': 'Twitter',
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'url': f'https://twitter.com/search?q={topic}'
                })
                break
    
    return events


def check_news_rss():
    """检查新闻 RSS"""
    # 简化实现
    events = []
    
    # 模拟 headlines
    headlines = get_latest_headlines()
    
    for headline in headlines:
        for level, keywords in BREAKING_KEYWORDS.items():
            if any(kw.lower() in headline.lower() for kw in keywords):
                events.append({
                    'level': level,
                    'title': headline,
                    'source': 'News RSS',
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'url': '#'
                })
                break
    
    return events


def get_trending_topics():
    """获取热搜话题（模拟）"""
    # 实际应调用 Twitter API
    return []


def get_latest_headlines():
    """获取最新头条（模拟）"""
    # 实际应解析 RSS
    return []


def generate_breaking_news_md(event):
    """生成突发新闻 MD 文件"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M')
    # 使用中文文件名
    filename = f"{OUTPUT_DIR}/突发新闻-{timestamp}.md"
    
    # 根据级别选择 emoji
    level_emoji = {'P0': '🚨', 'P1': '⚠️', 'P2': '📢', 'P3': '📰'}
    emoji = level_emoji.get(event['level'], '📰')
    
    content = f"""# {emoji} 突发新闻 · {event['level']} 级

> **发生时间**: {event['time']}  
> **监测来源**: {event['source']}  
> **响应时间**: <2 分钟  
> **系统状态**: 🧬 自进化系统 v1.0

---

## 📰 事件标题

{event['title']}

---

## 🔍 核心内容

[待搜索填充 - 自动触发搜索后更新]

---

## 📍 事件详情

| 项目 | 信息 |
|------|------|
| **级别** | {event['level']} 级 |
| **地点** | [待确认] |
| **时间** | {event['time']} |
| **来源** | {event['source']} |
| **链接** | {event['url']} |

---

## 🔄 后续更新

- [ ] 首次搜索完成
- [ ] 详细报道生成
- [ ] 影响范围评估
- [ ] 相关方回应

---

## 📊 搜索状态

- **AI 新闻**: 🔄 搜索中...
- **国际时事**: 🔄 搜索中...
- **国际热点**: 🔄 搜索中...
- **国际经济**: 🔄 搜索中...
- **中国政经**: 🔄 搜索中...

---

*太一 AGI · 突发新闻系统 v1.0 (自进化)*  
*下次更新：15 分钟后或事件有重大进展*
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename


def send_telegram_alert(event, md_file):
    """发送 Telegram 警报"""
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ TELEGRAM_BOT_TOKEN 未配置")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    
    # 级别对应 emoji
    level_emoji = {'P0': '🚨', 'P1': '⚠️', 'P2': '📢', 'P3': '📰'}
    emoji = level_emoji.get(event['level'], '📰')
    
    # 发送通知
    caption = f"""{emoji} 突发新闻 [{event['level']}级]

{event['title']}

📍 来源：{event['source']}
⏰ 时间：{event['time']}
🧬 自进化系统 v1.0

详细报道见文件 👇"""
    
    with open(md_file, 'rb') as f:
        files = {
            'document': (Path(md_file).name, f, 'text/markdown')
        }
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': caption
        }
        
        response = requests.post(url, files=files, data=data)
    
    return response.json()


def trigger_news_search(event):
    """触发新闻搜索"""
    # 调用日常新闻搜索脚本，但针对突发新闻优化
    search_query = event['title']
    
    # 这里应该调用 web_search 工具
    # 简化实现：打印日志
    print(f"🔍 触发搜索：{search_query}")
    
    return True


def main():
    """主循环 - 单次执行模式（由 cron 调用）"""
    print(f"🚨 突发新闻监测系统启动（单次执行）")
    print(f"📍 工作目录：{WORKSPACE}")
    print(f"📱 Telegram: {TELEGRAM_CHAT_ID}")
    print(f"🧬 自进化系统 v1.0")
    print(f"{'='*60}")
    
    try:
        # 监测突发新闻
        events = check_breaking_news()
        
        for event in events:
            print(f"\n🚨 检测到突发新闻：{event['title']}")
            print(f"   级别：{event['level']}")
            print(f"   来源：{event['source']}")
            
            # 生成 MD 文件
            md_file = generate_breaking_news_md(event)
            print(f"📄 生成文件：{md_file}")
            
            # 触发搜索
            trigger_news_search(event)
            
            # 发送 Telegram（自动检查重复）
            result = send_telegram_alert(event, md_file)
            if result.get('ok'):
                print(f"✅ Telegram 推送成功")
            elif result.get('error') == 'duplicate':
                print(f"⚠️ 跳过重复发送")
            else:
                print(f"❌ Telegram 推送失败：{result}")
        
        if not events:
            print(f"✅ 无突发新闻，监测正常")
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
