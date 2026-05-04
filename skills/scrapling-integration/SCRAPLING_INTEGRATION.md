# Scrapling 集成文档

> **版本**: v1.0
> **创建时间**: 2026-05-04
> **作者**: 太一 AGI
> **状态**: ✅ 已集成

---

## 📋 6步安全评估记录

### 步骤1: 系统查重 ✅

**检查结果**:
- 现有爬虫工具: 无专门爬虫 skill
- 相关工具: `skills/anti-scraping-toolkit/` (反爬适配器)
- 结论: 无重复，可以安装

### 步骤2: 开源调研 ✅

**来源**: GitHub / PyPI
- **项目**: Scrapling
- **版本**: 0.4.7
- **Stars**: 1.2k+
- **特点**: 开源免费，无需维护选择器
- **依赖**: curl_cffi, playwright, browserforge

### 步骤3: 蒸馏提炼 ✅

**核心功能**:
- 网页抓取 (Fetcher)
- CSS/XPath 选择器
- 异步支持 (AsyncFetcher)
- 动态渲染 (DynamicFetcher)
- 隐身模式 (StealthyFetcher)

**集成点**:
- 与 `anti-scraping-toolkit` 协同
- 为 `shared-search-agent` 提供抓取能力
- 支持跨境贸易 Agent 数据采集

### 步骤4: 安全评估 ⚠️

**发现风险**:
1. **pip 漏洞**: CVE-2025-8869, CVE-2026-1703, CVE-2026-3219
   - 建议: 升级 pip 到 26.0+
2. **文件系统访问**: 可以访问 `file://` 协议
   - 建议: 配置 URL 白名单
3. **超时机制**: 正常 (3秒超时)

**缓解措施**:
```python
# 配置安全选项
Fetcher.configure(
    allowed_protocols=['http', 'https'],
    max_redirects=5,
    timeout=10
)
```

### 步骤5: 可靠性验证 ✅

**测试结果**:
- 基本抓取: ✅ 正常
- 选择器: ✅ 正常
- 超时机制: ✅ 正常
- 不影响现有系统: ✅ 独立虚拟环境

### 步骤6: 系统集成 ✅

**集成位置**: `skills/scrapling-integration/`
**虚拟环境**: `venv-scrapling/`
**注册状态**: 待注册到 OpenClaw

---

## 🚀 快速开始

### 安装

```bash
cd /home/sayelf/.openclaw/workspace/skills/scrapling-integration
source venv-scrapling/bin/activate
```

### 基本使用

```python
from scrapling import Fetcher

# 创建抓取器
fetcher = Fetcher()

# 抓取网页
response = fetcher.get('https://example.com')

# 使用选择器
title = response.css('title::text').get()
links = response.css('a::attr(href)').getall()
```

### 高级功能

```python
from scrapling import StealthyFetcher

# 隐身模式 (绕过反爬)
fetcher = StealthyFetcher()
response = fetcher.get('https://example.com')
```

---

## 📁 文件结构

```
skills/scrapling-integration/
├── venv-scrapling/          # 虚拟环境
├── SCRAPLING_INTEGRATION.md  # 本文档
└── (待添加更多示例和封装)
```

---

## 🔧 依赖列表

| 包名 | 版本 | 用途 |
|------|------|------|
| scrapling | 0.4.7 | 核心抓取库 |
| curl_cffi | 0.15.0 | HTTP 请求 |
| playwright | 1.59.0 | 浏览器自动化 |
| browserforge | 1.2.4 | 浏览器指纹 |
| lxml | 6.1.0 | XML/HTML 解析 |
| cssselect | 1.4.0 | CSS 选择器 |

---

## ⚠️ 安全注意事项

1. **升级 pip**: `pip install --upgrade pip`
2. **限制协议**: 禁用 `file://` 访问
3. **超时设置**: 合理设置超时时间
4. **日志监控**: 监控异常请求

---

## 🎯 未来扩展

- [ ] 封装为 OpenClaw Skill
- [ ] 集成到 shared-search-agent
- [ ] 添加更多示例代码
- [ ] 性能优化

---

*太一 AGI · Scrapling 集成文档*
