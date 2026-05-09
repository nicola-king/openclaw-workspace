---
name: cross-border-trade-agent
version: 12.0.0
description: '太一跨境贸易 Agent — v12 AI HOT 产品思维升级：精选/日报/全量三层路由 + 5版块归一化 + 三轨接入 + 人话输出'
category: trading
tags: ['trading', 'cross-border', 'e-commerce', 'ai-hot', 'three-layer-routing']
status: active
---

# 跨境贸易 Agent v12 — Agent 可执行协议

> 借鉴 AI HOT 产品思维。这不是架构文档，是 Agent 的调用协议。

---

## 一、触发规则（什么时候调用哪个模块）

### 用户意图 → 路由表

| 用户说 | 路由到 | 模式 |
|--------|--------|------|
| "今天有什么项目/买家/机会" | `modules/buyer-intel/` 精选层 | 默认精选 |
| "沙特/中东/非洲买家" | `buyer-intel` 每日 + 国家筛 | 日报层 |
| "全部/所有采购机会" | `buyer-intel` 全量层 | 全量层 |
| "竞品监控/谁在抢单" | `modules/intelligence-hub/` 竞品版块 | selected |
| "招标/招标信息" | `intelligence-hub` 招标版块 | selected |
| "政策法规/关税/合规" | `intelligence-hub` 政策版块 | selected |
| "行业趋势/市场分析" | `intelligence-hub` 趋势版块 | selected |
| "GEO优化/社媒内容" | `modules/geo-outbound/` | all |
| "搜索买家/找客户" | `modules/guike-zhilu/` | 全量 |
| "写开发信/触达" | `modules/cross-border-core/` outreach | 全量 |

**负向规则**：
- 用户没说"全部/所有/全量" —— 默认走精选层，不要走全量
- 用户没说"日报/报告/简报" —— 默认走列表式输出，不走聚合报告
- 用户只问"看看/随便看看" —— 走精选层 + 7天内

---

## 二、三层路由输出模板

### 模式 1: 精选层（默认）

用户问"今天有什么项目"、"沙特买家"等宽问题 → 精选（活跃+已验证，默认7天）

```markdown
**买家情报 · 精选**（最近 7 天）

1. **Jewel of the Bride 项目** — 沙特吉达
   ⏱ 2026.5启动 | 💰 20亿美元 | 🏗 劳工营/钢结构
   高峰期2-3万工人，需大量劳工营模块，5年以上持续性需求
   来源：Construction Week

2. **NEOM THE LINE** — 沙特
   ⏱ 建设中 | 💰 5000亿美元 | 🏗 基建/劳工营/能源
   5000亿超级项目
   来源：公开项目情报

---

共 N 条 | 数据：买家情报引擎
```

**如果精选不足 3 条** → 提示"近期活跃项目较少，试试全量层？"

### 模式 2: 日报层

用户说"中东日报"、"沙特项目雷达" → 按国家/品类打包聚合

```markdown
**中东买家情报日报** · 2026-05-09

📊 今日概况：共 12 个项目，沙特 5 个，阿联酋 3 个，伊拉克 2 个，卡塔尔 2 个

## 沙特 / 劳工营
1. **Jewel of the Bride** — 20亿美元，需求劳工营模块化住房
2. **NEOM** — 5000亿，基建/劳工营

## 沙特 / 钢结构
3. ...

## 阿联酋 / 变压器
4. ...

---

来源：买家情报引擎
```

### 模式 3: 全量层

用户说"全部采购机会"、"所有买家线索" → 含冷线索

```markdown
**全部买家线索**（共 30 条）

1. **Jewel of the Bride** — 沙特 · 劳工营 | 活跃
2. **NEOM** — 沙特 · 基建 | 活跃
3. **旧线索 A** — 伊拉克 · 钢结构 | 2025-12
...

---

共 30 条 | 含历史线索
```

---

## 三、5 版块归一化输出模板

情报中心（intelligence-hub）的所有输出归到 5 个固定版块：

| 版块 | 图标 | 覆盖内容 |
|------|------|---------|
| 竞品动态 | 🏢 | 竞品新品/价格变动/市场动作/营销策略 |
| 招标信息 | 📋 | 招标/采购/项目/RFQ |
| 政策法规 | 🏛 | 关税/认证/标准/合规变动 |
| 行业趋势 | 📈 | 市场分析/增长率/预测/机会 |
| 买家线索 | 🎯 | 采购需求/买家信息/线索 |

### 输出模板（用户问"最近情报"）

```markdown
**跨境情报 · 最近 7 天**

## 🏢 竞品动态
1. 土耳其 Karmod 中东订单量增长 40% — LinkedIn
2. 中国 DXH 在东南亚新开工厂 — Industry News

## 📋 招标信息
3. 沙特 NEOM 发布钢结构采购招标 — etimad.sa
4. 伊拉克 21 城重建计划新增住宅区 — Gov.IQ

## 🏛 政策法规
5. SASO 更新建筑产品防火认证要求 — SASO

## 📈 行业趋势
6. GCC 国家建筑市场年增长 15% — MEED

## 🎯 买家线索
7. 伊拉克 5 万套模块化住房需求 — Gov.IQ

---

共 7 条 | 来源：情报中心 | 按发布时间倒序
```

---

## 四、人话输出规则（不可违反）

1. **禁止暴露基础设施细节**
   - ❌ "mode=selected" / "category=paper" / "take=30"
   - ❌ "GET /api/items" / "POST /api/v1/query"
   - ❌ "限流 600 req/min" / "HTTP 200" / "cursor" / "hasNext"
   - ✅ 只写人话："共 10 条" / "最近 7 天" / "数据来源：X平台"

2. **时间必须转人话**
   - ❌ "2026-05-08T01:48:00.000Z"
   - ✅ "今天上午 09:48" / "2 小时前" / "5/7" / "昨天"

3. **错误信息必须给出下一步建议**
   - ❌ "API rate limited"
   - ✅ "数据源暂时繁忙，等 2 分钟后再试"

4. **Suggestion 字段**：所有 error 返回必须带 `suggestion`
   ```python
   # 正确
   {"status": "error", "error": "暂无沙特日报数据",
    "suggestion": "试试其他国家，或切换到精选模式"}
   ```

---

## 五、三轨接入

| 接入方式 | 端点/命令 | 用途 |
|---------|-----------|------|
| REST API | `http://<host>:8100/api/v1/query` | 跨系统集成（飞书/Shopify/WordPress） |
| RSS | `http://<host>:8100/api/v1/rss` | 公众号/Telegram Channel 订阅 |
| Agent CLI | `python3 <模块>/api_server.py` | 直接调用 |

### REST API 使用

```bash
# 精选查询
curl "http://localhost:8100/api/v1/query?mode=selected&q=沙特钢结构&days=7"

# 日报
curl "http://localhost:8100/api/v1/daily?country=沙特"

# RSS
curl "http://localhost:8100/api/v1/rss?mode=selected"

# RSS 写文件
curl -o feed.xml "http://localhost:8100/api/v1/rss"
```

### RSS 直接生成

```bash
python3 modules/buyer-intel/rss_feed.py --mode daily --output feed.xml
```

---

## 六、不要做的事（Do-Not-Do List）

1. ⛔ **不要绕过三层路由直接搜索全量** — 默认精选层，用户没说"全部"不走全量
2. ⛔ **不要暴露模块路径或端点参数** — 用户不是开发者
3. ⛔ **不要把摘要当原文引用** — 摘要由 LLM 生成，引用需核对 `url`
4. ⛔ **不要编造买家信息** — 以 `buyers.json` 的数据为准
5. ⛔ **不要同时发日报和竞品监控两个推送** — 合并输出，一个时段一条
6. ⛔ **不要在一次输出中混合多个 category** 时不用编号区分版块
7. ⛔ **不要在 Telegram 发无链接的线索** — 每条线索必须带 `source` 或 `url`
8. ⛔ **不要假设用户知道"三层路由"** — 用户看到的是情报，不是架构

---

## 七、架构总览（参考用，Agent 不需要展示给用户）

```
🏢 总Agent（太一）
├── buyer-intel         买家情报引擎（三层路由 + REST API + RSS）
├── intelligence-hub    情报中心（5版块归一化 + 竞品/趋势/选品）
├── geo-outbound        GEO 优化（市场分析 + 社媒内容）
├── guike-zhilu         贵客之路（搜索→触达→培育闭环）
├── company-enricher    公司富化 + 7源验证
├── report-engine       报告系统 + Telegram 推送
├── cross-border-core   核心框架 + 事件总线
├── conversion-optimizer 转化优化 + 漏斗分析 + ROI
└── ... 品类Agent（钢结构/变压器/储该/摩配）
```

**相对路径**：所有模块在 `modules/` 下，共享 Agent 在 `agents/` 下。

---

## 八、版本说明

| 版本 | 日期 | 变更 |
|------|------|------|
| v12 | 2026-05-09 | **AI HOT 产品思维升级**：三路由+5版块+三轨接入+人话输出规范 |
| v11 | 2026-05-05 | 分层架构重组 |

---

*更新时间：2026-05-09 | 协议优先于架构*
