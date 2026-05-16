---
name: taiyi-aesthetics
description: >
  太一自动美学引擎。当你生成任何需要呈现给用户的报告、日报、摘要、分析结果时，
  自动调用 html-anything 或 art-agent 进行美化渲染。
  无需用户手动指定，系统根据内容类型和意图智能选择最佳工具。
trigger_keywords:
  - 美化
  - 排版
  - 设计
  - 品牌
  - 视觉
  - 风格
  - HTML
  - 报告
  - 日报
  - 周报
  - 月报
  - 美学
  - 生成
  - 输出
  - 好看
  - 做图
  - 卡片
  - logo
  - 配色
  - 海报
  - 小红书
  - XHS
  - 图文
  - 干货
---

# 太一自动美学引擎

## 核心规则

**每次生成任何需要呈现给用户的内容时，自动判断是否需要调用美学工具美化。**

优先走 **零 token 成本** 的静态渲染路径，仅在必要时触发消耗 token 的 Agent 渲染或 art-agent。

---

## 双引擎路由架构

```
用户内容
    │
    ▼
┌──────────────────────────────────────┐
│        太一美学路由器                    │
│                                        │
│ 内容类型 + 意图 + 格式 → 最佳工具选择    │
│                                        │
│  工具1: html-anything (HTML 排版美化)    │
│  工具2: art-agent (品牌/视觉/设计)       │
│  工具3: 两者级联 (先排版 → 再品牌化)     │
└──────────────────────────────────────┘
    │
    ├─ 内容需要 排版美化 ──→ html-anything
    ├─ 内容需要 品牌/视觉 ──→ art-agent
    ├─ 内容需要 小红书卡片 ──→ card-xiaohongshu
    ├─ 内容需要 品牌化报告 ──→ html-anything → art-agent
    └─ 纯文本即可 ─────────→ 直接输出
```

---

## 工具1: html-anything（HTML 排版美化）

### 功能
将 Markdown / CSV / JSON 渲染为设计级自包含 HTML 页面。

### 渲染方式选择

#### Tier 1 — 静态渲染（零 token 成本）
**默认路径**，80%+ 的场景走此路径：

| 内容类型 | 自动选用的模板 | 触发条件 |
|---------|--------------|---------|
| 系统状态/健康检查报告 | `doc-kami-parchment` | 含"健康/状态/检查" |
| 轨道运营日报 | `doc-kami-parchment` | 含"招标/轨道/运营" |
| GEO 日报 | `data-report` | 含"GEO/SEO/可见度/排名" |
| 竞品监控 | `data-report` | 含"竞品/监控/竞争" |
| 晨间简报 | `article-magazine` | 含"简报/摘要/今日" |
| 清单/列表 | `doc-kami-parchment` | 纯列表结构 |
| 数据分析 | `data-report` | 含表格/数字/KPI |

#### Tier 1.5 — 小红书卡片（零 token 成本）
小红书卡片 / 图文内容自动走 `card-xiaohongshu` 模板：

| 触发内容 | 自动选用 | 输出格式 |
|---------|---------|---------|
| 含"小红书 / XHS / 图文 / 卡片 / 干货 / 闪念" | `card-xiaohongshu` | 1080×1440 竖版多卡联排 HTML |
| `/oerv-card` 斜杠命令 | `card-xiaohongshu` | 闪念→小红书卡片全链路 |
| 用户说"发小红书 / 做小红书卡片" | `card-xiaohongshu` （Agent 版） | 设计级小红书图文 |
| 闪念记录/灵感 | `card-xiaohongshu`（静态） | 截图即可发 | 

通过 `html-render.py` 或 `html-agent.py` 生成，浏览器截图就能直接发小红书。

#### Tier 2 — Agent 渲染（消耗 token）
仅在以下场景自动升级：

| 内容类型 | 自动选用的模板 | 触发条件 |
|---------|--------------|---------|
| 公众号文章 | `article-magazine` | 需要发布到公众号 |
| 月报/季度报告 | `finance-report` | 月度/季度战略报告 |
| 小红书内容（高质量版） | `card-xiaohongshu` | Agent 驱动+品牌风格 |
| 幻灯片素材 | `deck-swiss-international` | 需要演示/分享 |
| 用户明确要求高质量 | 从 75 模板中选最佳 | 用户说"好看/设计/美" |

### 调用方式
```bash
# 静态渲染（默认，零成本）
python3 /home/sayelf/.openclaw/workspace/scripts/html-render.py <template> <input> [output]

# Agent 渲染（高价值内容）
python3 /home/sayelf/.openclaw/workspace/scripts/html-agent.py <template> <input> [output]
```

---

## 工具2: art-agent（品牌/视觉/设计）

### 功能
19 个模块覆盖品牌设计、视觉叙事、美学评分、内容创作。

### 适用场景
| 场景 | 调用 art-agent 模块 | 触发条件 |
|------|-------------------|---------|
| 品牌规范化 | `brand-studio`（58品牌规格） | 需要应用品牌规范 |
| 视觉设计 | `design-agent` | 做图/海报/卡片需要设计 |
| Logo 设计 | `taiyi-design` | 需要 logo / 图标 |
| 视觉叙事 | `visual-narrative` | 需要用视觉讲一个故事 |
| 美学过滤/审校 | `aesthetic-filter` | 需要对已有输出做美学审校 |
| 内容排期/优化 | `content-creator` | 社媒内容创作与排期 |

### 调用方式
art-agent 运行于端口 5200，通过其调度引擎调用各模块。

---

## 三级联合路由（完整决策树）

```
生成内容/收到需求
    │
    ├─ 纯文本汇报/简短回答 → 直接输出（不值得美化）
    │
    ├─ 需要品牌/视觉/设计产出？
    │   └─ 是 → art-agent（品牌工作室/设计Agent/视觉叙事）
    │
    ├─ 需要小红书卡片/图文？
    │   ├─ 闪念/简单内容 → html-render.py card-xiaohongshu（零成本）
    │   └─ 高质量/品牌化 → html-agent.py card-xiaohongshu（耗 token）
    │
    ├─ 需要 HTML 排版美化？
    │   ├─ 常规报告 → html-render.py（静态，零成本）
    │   └─ 高价值/外部发布 → html-agent.py（Agent，耗 token）
    │
    ├─ 需要品牌化报告？
    │   └─ 级联：html-render.py → art-agent brand-studio
    │
    └─ 用户明确说 "做图/设计/卡片"？
        └─ art-agent design-agent / taiyi-design
```

## 成本意识

| 路径 | token 成本 | 适用场景占比 |
|------|-----------|------------|
| 直接输出（不美化） | 0 | 简短回答 |
| html-render.py（静态，含 XHS 卡片） | **0** | **~80%** 的报告/日报/卡片 |
| html-agent.py（Agent） | 有消耗 | ~10% 高价值内容/小红书高质量版 |
| art-agent | 有消耗 | ~10% 视觉/设计需求 |
| 级联渲染 | 有消耗 | 品牌化报告 |

**遵守宪法 COST-EFFICIENCY 法则：保证系统正常运行，尽最大努力减少 token 消耗。**
