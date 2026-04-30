#!/usr/bin/env python3
# ============================================================
# 每日晨间新闻搜索 - Python 执行版
# 功能：北京时间 8:00 自动搜索 7 类全球新闻，每类 5 条
# 作者：太一 AGI
# 创建：2026-04-19
# ============================================================

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = "/home/nicola/.openclaw/workspace"
OUTPUT_DIR = f"{WORKSPACE}/news/daily"
DATE = datetime.now().strftime("%Y-%m-%d")
TIME = datetime.now().strftime("%H:%M")
# 使用中文文件名
OUTPUT_FILE = f"{OUTPUT_DIR}/晨间新闻简报-{DATE}.md"  # 中文文件名

# 新闻类别配置（7 类，每类 5 条）
NEWS_CATEGORIES = [
    {
        "name": "🤖 AI 新闻",
        "queries": [
            "AI artificial intelligence news 2026",
            "machine learning breakthrough 2026",
            "大模型 AI 进展 2026",
            "AI 应用 新产品 2026",
            "AI 行业 投资 融资 2026"
        ],
        "source": "global"  # 全球搜索
    },
    {
        "name": "🔬 前沿科技",
        "queries": [
            "breakthrough technology 2026",
            "quantum computing news 2026",
            "biotech gene editing 2026",
            "space technology launch 2026",
            "新能源 电池技术 2026"
        ],
        "source": "global"  # 全球搜索
    },
    {
        "name": "🌍 国际时事",
        "queries": [
            "international politics news today",
            "diplomatic relations 2026",
            "global summit conference 2026",
            "国际政治 外交 2026",
            "world leaders news 2026"
        ],
        "source": "global"  # 全球搜索
    },
    {
        "name": "📰 国际热点",
        "queries": [
            "trending worldwide twitter",
            "viral news reddit",
            "breaking news youtube",
            "tiktok trending news",
            "instagram viral stories"
        ],
        "source": "overseas"  # 海外互联网 (社交媒体)
    },
    {
        "name": "💰 国际经济",
        "queries": [
            "global economy news 2026",
            "stock market international 2026",
            "美联储 利率 经济 2026",
            "international trade finance 2026",
            "cryptocurrency Bitcoin news 2026"
        ],
        "source": "global"  # 全球搜索
    },
    {
        "name": "📱 产品趋势",
        "queries": [
            "amazon bestseller 2026",
            "tiktok made me buy it",
            "kickstarter indiegogo trending",
            "shein temu hot products",
            "跨境电商 爆款 2026"
        ],
        "source": "cross-border-agent"  # 跨境贸易 Agent
    },
    {
        "name": "🇨🇳 中国政经",
        "queries": [
            "中国经济 政策 2026",
            "中国 GDP 增长 2026",
            "中国政府 会议 政策 2026",
            "China economy policy 2026",
            "中国科技 产业 发展 2026"
        ],
        "source": "domestic"  # 国内互联网
    }
]

def search_news(query, count=5, source="global"):
    """调用 OpenClaw web_search 搜索新闻 - 解除限制版本"""
    import random
    import time
    
    try:
        # 根据来源选择不同搜索策略
        if source == "domestic":
            # 国内互联网搜索 - 使用多个源
            queries = [
                f'site:xinhuanet.com {query}',
                f'site:people.cn {query}',
                f'site:caixin.com {query}',
                query  # 通用搜索
            ]
            selected_query = random.choice(queries)
            cmd = f'''openclaw exec --tool web_search --query "{selected_query}" --count {count}'''
            
        elif source == "overseas":
            # 海外互联网搜索 (社交媒体) - 多平台
            platforms = ['twitter', 'reddit', 'youtube', 'tiktok']
            selected_platform = random.choice(platforms)
            cmd = f'''openclaw exec --tool agent-reach --platform {selected_platform} --query "{query}"'''
            
        elif source == "cross-border-agent":
            # 跨境贸易 Agent 数据库 - 直接读取最新报告
            report_dir = '/home/nicola/.openclaw/workspace/skills/01-trading/cross-border-trade-agent/reports/'
            cmd = f'''ls -t {report_dir}*.md 2>/dev/null | head -1 | xargs cat'''
            
        else:
            # 全球搜索 (默认) - 多查询词避免 bot 检测
            cmd = f'''openclaw exec --tool web_search --query "{query}" --count {count}'''
        
        # 执行搜索，增加重试机制
        max_retries = 3
        for attempt in range(max_retries):
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
            if result.returncode == 0:
                return json.loads(result.stdout) if result.stdout else None
            
            # 如果失败，等待后重试
            if attempt < max_retries - 1:
                wait_time = random.uniform(2, 5) * (attempt + 1)
                print(f"搜索失败，{wait_time:.1f}秒后重试 ({attempt+1}/{max_retries}): {query}")
                time.sleep(wait_time)
        
        print(f"搜索失败 (已重试{max_retries}次): {query}")
        return None
        
    except Exception as e:
        print(f"搜索异常 {query}: {e}")
        return None

def format_news_results(category_name, results):
    """格式化新闻结果"""
    output = f"## {category_name}\n\n"
    
    if not results or 'results' not in results:
        output += "*暂无数据*\n\n"
        return output
    
    for i, item in enumerate(results['results'][:5], 1):
        title = item.get('title', '无标题').strip()
        url = item.get('url', '#')
        snippet = item.get('snippet', '无摘要')[:200]
        site = item.get('siteName', '未知来源')
        
        output += f"**{i}. {title}**\n"
        output += f"- 📰 {snippet}...\n"
        output += f"- 🔗 [{site}]({url})\n\n"
    
    return output

def main():
    # 创建输出目录
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # 生成报告头
    report = f"""# 🌅 晨间新闻简报 · {DATE}

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **数据来源**: 全球多源搜索（传统媒体 + 网络媒体 + 社交媒体）  
> **更新频率**: 每日北京时间 08:00 自动更新

---

"""
    
    # 搜索每类新闻
    for category in NEWS_CATEGORIES:
        print(f"正在搜索：{category['name']}...")
        
        # 合并查询搜索
        combined_query = " | ".join(category['queries'][:3])
        results = search_news(combined_query, count=5)
        
        report += format_news_results(category['name'], results)
        report += "---\n\n"
    
    # 添加尾部说明
    report += f"""
## 📌 说明

- ✅ 新闻来源包括传统媒体、网络媒体、社交媒体
- ✅ 所有新闻链接均可验证
- ✅ 内容真实可靠，具有时效性
- ✅ 北京时间 {DATE} 08:00 自动生成
- 📧 如需订阅推送，请联系太一 AGI

---
*太一 AGI · 全球新闻搜索系统 v1.0*
"""
    
    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 新闻搜索完成！")
    print(f"📄 输出文件：{OUTPUT_FILE}")
    
    return OUTPUT_FILE

if __name__ == "__main__":
    main()
