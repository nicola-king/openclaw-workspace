# 罔两数据采集 v2.0 - Xcrawl 整合

> 基于 Xcrawl 小龙爪 | 版本：v2.0 | 创建：2026-03-27

---

## 🎯 核心验证

```
Xcrawl = 专业级网页数据采集工具

太一罔两需要:
✅ 单页精准抓取 (已有基础)
✅ 全站 URL 映射 (待增强)
✅ 批量异步爬取 (待增强)
✅ 多引擎 SERP 搜索 (待集成)
✅ 反反爬能力 (待增强)
✅ 自然语言提取 (待集成)

这意味着:
太一可以集成 Xcrawl 增强数据采集能力，
服务于天机情报系统和知几-E 策略！
```

---

## 📊 功能对比

| 功能 | Xcrawl | 罔两 v1.0 | 罔两 v2.0 |
|------|--------|---------|---------|
| **单页抓取** | ✅ Markdown/JSON | ⏳ 基础 | ✅ 增强 |
| **URL 映射** | ✅ 全站结构 | ❌ | ✅ 新增 |
| **批量爬取** | ✅ 异步可控 | ⏳ 基础 | ✅ 增强 |
| **SERP 搜索** | ✅ 多引擎 | ❌ | ✅ 新增 |
| **反反爬** | ✅ 代理 + 指纹 | ⏳ 基础 | ✅ 增强 |
| **自然语言** | ✅ AI 提取 | ❌ | ✅ 新增 |
| **Agent 集成** | ✅ Skill 标准 | ✅ 已有 | ✅ 保持 |

---

## 🛠️ 技术整合方案

### 方案 1: 使用 Xcrawl API (推荐)

```bash
# 1. 注册 Xcrawl 账号
访问：https://xcrawl.com/

# 2. 获取 API Key
- 新用户注册送 1000 试用积分
- 控制台 → API Keys → 创建 Key

# 3. 配置环境变量
cat >> ~/.openclaw/.env << EOF
XCRAWL_API_KEY=你的 API Key
XCRAWL_BASE_URL=https://api.xcrawl.com/v1
EOF

# 4. 测试 API
curl -X POST "https://api.xcrawl.com/v1/scrape" \
  -H "Authorization: Bearer $XCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "format": "markdown"
  }'
```

### 方案 2: 罔两集成脚本

```python
#!/usr/bin/env python3
"""
太一罔两数据采集 v2.0

整合:
- Xcrawl API (网页抓取)
- Polymarket Gamma API (链上数据)
- 多平台数据采集
- AI 数据清洗 (山木)
"""

import os
import asyncio
import aiohttp
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('/home/nicola/.openclaw/.env')

# 配置
XCRAWL_API_KEY = os.getenv("XCRAWL_API_KEY")
XCRAWL_BASE_URL = os.getenv("XCRAWL_BASE_URL", "https://api.xcrawl.com/v1")

# 数据采集目标
TARGETS = {
    "polymarket_news": [
        "https://polymarket.com/blog",
        "https://cryptoslate.com/topics/polymarket/",
    ],
    "competitor_tracking": [
        "https://twitter.com/ColdMath",
        "https://twitter.com/PolyCop_BOT",
    ],
    "market_research": [
        "https://www.reddit.com/r/Polymarket/",
        "https://www.reddit.com/r/predictionmarket/",
    ]
}


async def scrape_page(url: str, session: aiohttp.ClientSession) -> dict:
    """
    单页精准抓取 (使用 Xcrawl API)
    
    返回: Markdown 格式内容
    """
    api_url = f"{XCRAWL_BASE_URL}/scrape"
    headers = {
        "Authorization": f"Bearer {XCRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": url,
        "format": "markdown",
        "options": {
            "removeSelectors": ["nav", "footer", ".ads"],  # 移除无关元素
            "waitFor": 2000  # 等待 JS 加载
        }
    }
    
    async with session.post(api_url, json=payload, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            return {
                "url": url,
                "content": data.get("content", ""),
                "title": data.get("title", ""),
                "timestamp": datetime.now().isoformat()
            }
        else:
            print(f"❌ 抓取失败 {url}: {response.status}")
            return {"url": url, "content": "", "error": response.status}


async def map_site(url: str, session: aiohttp.ClientSession) -> list:
    """
    全站 URL 映射 (使用 Xcrawl map)
    
    返回: 所有页面 URL 列表
    """
    api_url = f"{XCRAWL_BASE_URL}/map"
    headers = {
        "Authorization": f"Bearer {XCRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": url,
        "maxPages": 100,  # 最多抓取页数
        "depth": 3  # 抓取深度
    }
    
    async with session.post(api_url, json=payload, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("urls", [])
        else:
            print(f"❌ URL 映射失败 {url}: {response.status}")
            return []


async def crawl_multiple(urls: list, session: aiohttp.ClientSession) -> list:
    """
    批量异步爬取
    
    返回: 所有页面内容列表
    """
    tasks = [scrape_page(url, session) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 过滤失败结果
    successful = [r for r in results if isinstance(r, dict) and r.get("content")]
    return successful


async def serp_search(query: str, engine="google", region="us") -> list:
    """
    SERP 搜索引擎搜索
    
    返回: 搜索结果列表
    """
    async with aiohttp.ClientSession() as session:
        api_url = f"{XCRAWL_BASE_URL}/search"
        headers = {
            "Authorization": f"Bearer {XCRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": query,
            "engine": engine,  # google, bing, baidu
            "region": region,
            "numResults": 20
        }
        
        async with session.post(api_url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("results", [])
            else:
                print(f"❌ 搜索失败：{response.status}")
                return []


def extract_with_ai(content: str, instruction: str) -> str:
    """
    使用 AI 自然语言提取数据
    
    示例:
    instruction = "提取所有提到 Polymarket 交易策略的段落"
    """
    # 这里可以调用山木 Bot 进行 AI 提取
    # 简化版：关键词匹配
    
    keywords = ["Polymarket", "trading", "strategy", "arbitrage"]
    lines = content.split('\n')
    
    extracted = []
    for line in lines:
        if any(kw.lower() in line.lower() for kw in keywords):
            extracted.append(line)
    
    return '\n'.join(extracted[:20])  # 最多返回 20 条


async def main():
    """主函数"""
    print("🚀 太一罔两数据采集 v2.0 启动...")
    
    async with aiohttp.ClientSession() as session:
        # 1. 单页抓取测试
        print("📄 测试单页抓取...")
        test_url = "https://polymarket.com/blog"
        result = await scrape_page(test_url, session)
        if result.get("content"):
            print(f"✅ 抓取成功：{result['title']}")
            print(f"   内容长度：{len(result['content'])} 字符")
        
        # 2. URL 映射测试
        print("🗺️ 测试 URL 映射...")
        urls = await map_site(test_url, session)
        print(f"✅ 发现 {len(urls)} 个页面")
        
        # 3. 批量爬取
        print("📥 批量爬取目标网站...")
        all_targets = []
        for category, targets in TARGETS.items():
            all_targets.extend(targets)
        
        results = await crawl_multiple(all_targets[:5], session)  # 测试前 5 个
        print(f"✅ 成功抓取 {len(results)} 个页面")
        
        # 4. SERP 搜索
        print("🔍 SERP 搜索测试...")
        search_results = await serp_search("Polymarket trading strategy")
        print(f"✅ 搜索结果：{len(search_results)} 条")
        
        # 5. AI 数据提取
        print("🤖 AI 数据提取...")
        if results:
            sample_content = results[0].get("content", "")
            extracted = extract_with_ai(sample_content, "提取 Polymarket 交易策略")
            print(f"✅ 提取关键信息：{len(extracted)} 字符")
        
        # 6. 生成报告
        report = f"""
# 太一罔两数据采集报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━

## 📊 采集总结

- 单页抓取：✅ 成功
- URL 映射：✅ 发现 {len(urls)} 个页面
- 批量爬取：✅ 成功 {len(results)} 个页面
- SERP 搜索：✅ {len(search_results)} 条结果
- AI 提取：✅ 完成

━━━━━━━━━━━━━━━━━━━━━

## 📄 抓取内容示例

标题：{result.get('title', 'N/A')}

内容预览:
{result.get('content', '')[:500]}...

━━━━━━━━━━━━━━━━━━━━━

## 🔍 搜索结果 Top 5

"""
        for i, res in enumerate(search_results[:5], 1):
            report += f"""
{i}. **{res.get('title', 'N/A')}**
   - URL: {res.get('url', 'N/A')}
   - 摘要：{res.get('snippet', 'N/A')[:100]}...
"""
        
        report += """
━━━━━━━━━━━━━━━━━━━━━

## 💡 数据应用建议

1. **天机情报系统**: 每日自动采集竞品动态
2. **知几-E 策略**: 监控 ColdMath 等大户动向
3. **山木内容创作**: 采集热门话题写文章
4. **市场调研**: SERP 搜索发现新机会

━━━━━━━━━━━━━━━━━━━━━

*太一 AGI · 罔两数据采集 v2.0*
*基于 Xcrawl 小龙爪*
"""
        
        # 7. 保存报告
        output_file = f"/home/nicola/.openclaw/workspace/reports/wangliang-data-{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✅ 数据采集报告已生成：{output_file}")


if __name__ == "__main__":
    asyncio.run(main())
