# 反爬开源项目来源清单

> **状态**: ✅ 已调研
> **时间**: 2026-05-04
> **原则**: 免费开源，无需API密钥

---

## 核心项目

### 1. Crawl4AI ⭐⭐⭐⭐⭐
- **地址**: https://github.com/unclecode/crawl4ai
- **功能**: LLM友好型网页爬虫
- **特点**: 自动提取结构化数据，支持JS渲染
- **许可**: 开源
- **安装**: `pip install crawl4ai`

### 2. Scrapling ⭐⭐⭐⭐
- **地址**: https://github.com/D4Vinci/Scrapling
- **功能**: 自适应网页爬虫框架
- **特点**: 自动适配DOM变化，反爬对抗
- **许可**: 开源

### 3. Playwright ⭐⭐⭐⭐⭐
- **地址**: https://github.com/microsoft/playwright
- **功能**: 浏览器自动化
- **特点**: 支持Chromium/Firefox/WebKit，stealth模式
- **许可**: Apache-2.0
- **安装**: `pip install playwright`

### 4. cloudflare-bypass ⭐⭐⭐
- **地址**: https://github.com/HasData/cloudflare-bypass
- **功能**: Cloudflare反Bot绕过
- **特点**: Playwright + stealth插件
- **许可**: 开源

---

## 辅助工具

### 5. fake-useragent
- **功能**: 随机User-Agent生成
- **安装**: `pip install fake-useragent`

### 6. requests-cache
- **功能**: 请求缓存
- **安装**: `pip install requests-cache`

### 7. undetected-chromedriver
- **功能**: 绕过Chrome检测
- **安装**: `pip install undetected-chromedriver`

---

## 技术方案对比

| 方案 | 成本 | 复杂度 | 效果 | 适用场景 |
|------|------|--------|------|---------|
| requests + headers | 免费 | 低 | 60% | 简单静态页面 |
| requests + session | 免费 | 低 | 70% | 需要登录的页面 |
| Playwright | 免费 | 中 | 90% | JS渲染页面 |
| Playwright + stealth | 免费 | 中 | 95% | 高保护页面 |
| 付费代理池 | 高 | 中 | 85% | 大规模爬取 |

---

## 推荐组合

### 轻量级 (免费)
```
requests + fake-useragent + requests-cache
```

### 中量级 (免费)
```
Playwright + stealth + 随机延迟
```

### 重量级 (免费)
```
Crawl4AI + Playwright + 代理轮换
```

---

*太一 AGI · 反爬开源项目清单*
