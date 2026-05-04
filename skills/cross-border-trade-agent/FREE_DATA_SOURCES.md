# 免费开源数据源清单

> **状态**: ✅ 已验证可用
> **更新**: 2026-05-04
> **原则**: 优先使用免费、公开、官方数据源

---

## ✅ 已验证可用

### 1. 汇率数据
| 来源 | URL | 类型 | 限制 |
|------|-----|------|------|
| ExchangeRate-API | https://api.exchangerate-api.com | 免费 API | 无限制 |

```python
import requests
r = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
data = r.json()
cny_rate = data['rates']['CNY']  # 6.84
```

### 2. 世界经济数据
| 来源 | URL | 类型 | 限制 |
|------|-----|------|------|
| World Bank API | https://api.worldbank.org | 免费 API | 无限制 |

```python
# 获取国家贸易数据
url = 'https://api.worldbank.org/v2/country/CHN/indicator/NE.EXP.GNFS.CD?format=json'
```

### 3. Google Trends
| 来源 | URL | 类型 | 限制 |
|------|-----|------|------|
| Google Trends | https://trends.google.com | 网页爬虫 | 需反爬处理 |

### 4. 电商平台 (公开数据)
| 来源 | URL | 类型 | 限制 |
|------|-----|------|------|
| Amazon Best Sellers | https://www.amazon.com/Best-Sellers | 网页爬虫 | 需反爬处理 |
| 阿里巴巴国际站 | https://www.alibaba.com | 网页爬虫 | 需反爬处理 |

---

## 🟡 部分可用/需处理

### 5. 海关数据
| 来源 | URL | 状态 | 说明 |
|------|-----|------|------|
| UN Comtrade | https://comtrade.un.org | 🟡 连接重置 | 需重试机制 |
| 中国海关总署 | http://www.customs.gov.cn | 🟡 403 | 需代理/Header |
| 海关统计数据 | http://stats.customs.gov.cn | 🟡 403 | 需代理/Header |

### 6. 物流/航运
| 来源 | URL | 状态 | 说明 |
|------|-----|------|------|
| MarineTraffic | https://www.marinetraffic.com | 🟡 403 | 需反爬处理 |

---

## 📋 推荐免费数据源组合

### 跨境贸易基础数据
```
汇率: ExchangeRate-API (实时)
经济指标: World Bank API (年度/季度)
趋势分析: Google Trends (实时)
竞品分析: Amazon/阿里巴巴 (爬虫)
```

### 替代方案 (当官方 API 不可用时)
```
海关数据 → 世界银行贸易数据
物流追踪 → 各船公司官网 (Maersk, COSCO)
HS 编码 → WCO 官网 (worldcustomsorganization.org)
```

---

## 🔧 爬虫工具 (免费开源)

| 工具 | 用途 | 安装 |
|------|------|------|
| requests | HTTP 请求 | 已安装 |
| urllib | 内置 HTTP | 已安装 |
| BeautifulSoup | HTML 解析 | 需安装 |
| Scrapy | 大规模爬虫 | 需安装 |
| Playwright | 动态页面 | 需安装 |

---

## ⚠️ 使用规范

1. **遵守 robots.txt** - 不爬取禁止内容
2. **控制频率** - 每秒不超过 1 次请求
3. **使用 User-Agent** - 标识爬虫身份
4. **缓存数据** - 避免重复请求
5. **异常处理** - 网络错误自动重试

---

*太一 AGI · 免费数据源清单*
