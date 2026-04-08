---
name: public-api
tier: 2
trigger: API/数据源/免费/公开
enabled: true
depends: []
---
# 公共 API 资源技能（罔两数据源）

## 核心原则

**负熵法则：** 降低数据获取成本

**价值基石：** 免费资源优先，减少 SAYELF 支出

**简化优先：** 精选高质量 API，避免信息过载

---

## 核心 API 库

### 1. public-apis (413k+ Stars)

**来源：** GitHub - `public-apis/public-apis`

**特点：**
- 最全面的免费 API 集合
- 1000+ 接口按主题分类
- 持续维护更新

**太一使用场景：**
| 类别 | API 示例 | 负责 Bot |
|------|----------|----------|
| 金融 | 股票/加密货币 | 知几 |
| 天气 | 天气预报 | 天气技能 |
| 新闻 | 新闻聚合 | 罔两 |
| 社交 | Twitter/Reddit | 山木 |

**链接：** https://github.com/public-apis/public-apis

---

### 2. public-api-lists (13.6k Stars)

**来源：** GitHub - `marceldempers/public-api-lists`

**特点：**
- 小众/冷门 API
- 加密货币行情
- AI 生成内容
- 游戏数据

**太一使用场景：**
- 加密货币数据（知几）
- AI 内容生成（山木）
- 热榜数据（罔两）

**链接：** https://github.com/public-api-lists/public-api-lists

---

### 3. vikiboss/60s (5k Stars)

**来源：** GitHub - `vikiboss/60s`

**特点：**
- 国内各大平台热榜
- 知乎/微博/B 站等
- 可本地部署

**太一使用场景：**
- 舆情监控（罔两）
- 热点追踪（山木）
- 早报素材（知几）

**链接：** https://github.com/vikiboss/60s

---

## API 分类与 Bot 映射

### 金融数据（知几职责）

| API | 用途 | 状态 |
|------|------|------|
| CoinGecko | 加密货币价格 | ✅ 免费 |
| Binance | 交易数据 | 🟡 需 API Key |
| Alpha Vantage | 股票数据 | ✅ 免费额度 |
| Yahoo Finance | 美股数据 | ✅ 免费 |

### 新闻/内容（山木职责）

| API | 用途 | 状态 |
|------|------|------|
| NewsAPI | 新闻聚合 | ✅ 免费额度 |
| Reddit | 热门话题 | ✅ 免费 |
| Hacker News | 技术新闻 | ✅ 免费 |

### 数据/热榜（罔两职责）

| API | 用途 | 状态 |
|------|------|------|
| 60s | 国内热榜 | ✅ 免费 |
| Twitter | 社交媒体 | 🟡 需 API Key |
| Google Trends | 搜索趋势 | ✅ 免费 |

### 工具/实用（素问职责）

| API | 用途 | 状态 |
|------|------|------|
| IP API | IP 地理位置 | ✅ 免费 |
| Weather API | 天气数据 | ✅ 免费 |
| Public Holidays | 节假日 | ✅ 免费 |

---

## API 使用规范

### 认证管理

**API Key 存储：**
```bash
# 写入 TOOLS.md 加密部分
export COINGECKO_API_KEY="xxx"
export NEWSAPI_KEY="xxx"
```

**安全原则：**
- 不硬编码在技能文件
- 使用环境变量
- 定期轮换

### 速率限制

| API | 限制 | 应对策略 |
|------|------|----------|
| CoinGecko | 10-50 次/分 | 缓存结果 |
| NewsAPI | 100 次/天 | 优先免费 |
| Twitter | 300 次/15 分钟 | 批量请求 |

### 错误处理

```markdown
【API 故障记录】
- API 名称：[名称]
- 故障时间：[时间]
- 错误信息：[详情]
- 应对方案：[备用 API/降级]
- 恢复时间：[时间]
```

---

## 集成流程

### L1 审查（新增 API）

**流程：**
```
发现 API → 评估价值 → 
测试可用性 → 写入 PUBLIC-API.md → 
更新 TOOLS.md 配置
```

### 评估标准

| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | 1-5 分 | 是否满足日常需求 |
| 稳定性 | 1-5 分 | SLA/历史可用性 |
| 文档质量 | 1-5 分 | 文档是否完整 |
| 社区支持 | 1-5 分 | GitHub Stars/活跃度 |

**准入门槛：** 总分 >= 15 分

---

## 快速参考

### API 推荐优先级

```
P1: CoinGecko (加密数据)
P1: 60s (国内热榜)
P2: NewsAPI (新闻聚合)
P3: 其他按需添加
```

### 配置位置

```
TOOLS.md → API Key 配置
PUBLIC-API.md → API 列表与说明
```

### 故障应对

```
API 故障 → 切换备用 API → 
记录故障 → 通知 SAYELF
```

---

## 总结

**定位：** 罔两的数据源管理技能

**价值：** 免费资源优先，降低支出

**边界：** 仅整合免费/低成本 API

**审查：** L1（太一自主添加）

---
*版本：1.0 | 生效日期：2026-03-22 | 最后更新：08:25*
