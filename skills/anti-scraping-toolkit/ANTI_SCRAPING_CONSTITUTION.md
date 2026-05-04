---
name: anti-scraping-toolkit
tier: 2
enabled: true
---
# 反爬对抗技能库 (Anti-Scraping Toolkit)

> **版本**: v1.0
> **融合时间**: 2026-05-04
> **定位**: Tier 2 上下文激活 (爬虫/数据采集任务时加载)
> **核心**: 开源反爬对抗技术蒸馏，免费无API密钥

---

## 🎯 深度学习法融合 (Elon 五步算法)

### 1. 质疑 (Question)

**问题**: 为什么现有爬虫总被封？
- 请求模式太规律 (固定间隔)
- 指纹太明显 (User-Agent/Canvas/WebGL)
- 缺少人类行为模拟 (鼠标轨迹、滚动)
- 单IP请求过多
- 不处理JS动态内容

**质疑结论**: 大多数爬虫失败不是因为技术不够，而是因为**行为不像人**。

### 2. 删除 (Delete)

**删除低效方案**:
- ❌ 付费代理池 (成本高，仍可能被封)
- ❌ 复杂指纹随机化 (过度工程，易检测)
- ❌ 多线程暴力爬取 (触发频率限制)
- ❌ 忽略robots.txt (法律风险)

**保留核心**:
- ✅ 行为模拟 (像人一样浏览)
- ✅ 请求分散 (时间/空间)
- ✅ 内容提取 (结构化输出)
- ✅ 错误处理 (优雅降级)

### 3. 简化 (Simplify)

**极简反爬策略**:

```
反爬核心 = 行为模拟 + 请求管理 + 内容提取
```

| 层级 | 策略 | 实现 |
|------|------|------|
| L1 | 请求间隔随机化 | random.uniform(1, 3) |
| L2 | User-Agent轮换 | 预设10个常见UA |
| L3 | 会话保持 | requests.Session + cookies |
| L4 | 动态内容 | Playwright/Selenium |
| L5 | 指纹伪装 | stealth插件 |

### 4. 加速 (Accelerate)

**并行策略**:
- 异步请求 (aiohttp)
- 分布式爬取 (多个IP)
- 缓存复用 (避免重复请求)
- 增量更新 (只抓变化内容)

### 5. 自动化 (Automate)

**自动反爬**:
- 自动检测封禁 → 切换代理
- 自动识别验证码 → 打码服务
- 自动调整频率 → 自适应限速
- 自动重试失败 → 指数退避

---

## 🛠️ 开源工具矩阵

### 核心工具 (已验证)

| 工具 | 功能 | 星级 | 适用场景 |
|------|------|------|---------|
| **Crawl4AI** | LLM友好型爬虫 | ⭐⭐⭐⭐⭐ | 结构化数据提取 |
| **Scrapling** | 自适应爬虫框架 | ⭐⭐⭐⭐ | 动态内容处理 |
| **Playwright** | 浏览器自动化 | ⭐⭐⭐⭐⭐ | JS渲染页面 |
| **cloudflare-bypass** | Cloudflare绕过 | ⭐⭐⭐ | 反Bot保护 |

### 辅助工具

| 工具 | 功能 | 免费 |
|------|------|------|
| **fake-useragent** | UA轮换 | ✅ |
| **requests-cache** | 请求缓存 | ✅ |
| **scrapy-rotating-proxies** | 代理轮换 | ✅ |
| **undetected-chromedriver** | 指纹伪装 | ✅ |

---

## 📋 反爬策略库

### 策略一：基础伪装 (Level 1)

```python
import random
import time
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# 随机延迟
time.sleep(random.uniform(1, 3))
```

### 策略二：会话管理 (Level 2)

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

# 重试策略
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
session.mount('https://', HTTPAdapter(max_retries=retries))

# 使用session保持cookies
response = session.get(url, headers=headers)
```

### 策略三：动态渲染 (Level 3)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()
    
    # 模拟人类行为
    page.goto(url)
    page.mouse.move(random.randint(100, 500), random.randint(100, 500))
    page.scroll(0, random.randint(300, 800))
    
    content = page.content()
    browser.close()
```

### 策略四：指纹伪装 (Level 4)

```python
# 使用 stealth 插件
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 注入 stealth 脚本
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        locale='zh-CN',
        timezone_id='Asia/Shanghai',
    )
    
    page = context.new_page()
    
    # 绕过 webdriver 检测
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
```

### 策略五：分布式爬取 (Level 5)

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results
```

---

## 🔄 与现有宪法的融合

| 反爬原则 | 对应宪法 | 关系 |
|---------|---------|------|
| 行为模拟 | 观察者协议 | 模拟人类行为，避免检测 |
| 请求管理 | 工具克制原则 | 控制频率，最小权限 |
| 错误处理 | 验证优先法则 | 验证 > 输出 |
| 缓存复用 | TurboQuant | 智能分离，减少重复 |

---

## ⚠️ 法律与道德边界

### 允许
- 爬取公开数据
- 遵守 robots.txt
- 控制请求频率
- 用于个人研究

### 禁止
- 爬取需要登录的私有数据
- 绕过明确的技术保护措施
- 用于商业竞争情报窃取
- 违反网站服务条款

---

## ✅ 自检清单 (爬虫任务前)

```
□ 目标网站是否允许爬取？
□ 是否设置了合理的请求间隔？
□ 是否模拟了人类行为？
□ 是否处理了动态内容？
□ 是否有错误重试机制？
□ 是否遵守了 robots.txt？
□ 是否设置了请求头伪装？
```

---

## 🚀 快速开始

```bash
# 安装核心依赖
pip install crawl4ai playwright fake-useragent requests-cache

# 安装浏览器
playwright install chromium

# 测试
python -c "import crawl4ai; print('crawl4ai ready')"
```

---

*太一 AGI · 反爬对抗技能库 v1.0*
*基于开源项目蒸馏: Crawl4AI, Scrapling, Playwright, cloudflare-bypass*
