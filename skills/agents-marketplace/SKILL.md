---
name: agents-marketplace
description: 融合 wshobson/agents（36K⭐）插件市场的 155 个 Skill + 191 个 Agent + 102 个命令到太一系统。自动识别用户意图并路由到最匹配的市场 Agent/插件，调用 Gemini CLI 执行。
---

# Agents Marketplace Skill — 太一融合层

融合 wshobson/agents 多引擎插件市场（MIT 开源，36K⭐）。

## 已装载能力

| 模块 | 数量 | 说明 |
|:----:|:----:|------|
| Skills | 155 | 按需加载的专业技能包 |
| Agents | 191 | 领域专家 Agent（@agent-name 调用） |
| Commands | 102 | 斜杠命令 |
| 插件 | 81 | 可组合的功能单元 |

## 跨境贸易相关 Agent 速查

### GEO 优化
| @Agent | 用途 |
|--------|------|
| @seo-content-auditor | SEO 内容审核 |
| @seo-content-planner | 内容策略规划 |
| @seo-keyword-strategist | 关键词策略 |
| @seo-meta-optimizer | Meta 标签优化 |
| @seo-authority-builder | 外链/权威建设 |
| @seo-cannibalization-detector | 关键词冲突检测 |
| @search-specialist | 搜索算法专家 |

### 商业分析
| @Agent | 用途 |
|--------|------|
| @business-analyst | 业务分析师 |
| @startup-analyst | 创业项目分析 |
| @customer-support | 客户服务 |
| @sales-automator | 销售自动化 |

### 量化交易
| @Agent | 用途 |
|--------|------|
| @quant-analyst | 量化分析师 |
| @risk-manager | 风险管理 |

### 数据/AI
| @Agent | 用途 |
|--------|------|
| @data-engineer | 数据工程师 |
| @ai-engineer | AI 工程师 |
| @prompt-engineer | Prompt 工程师 |

## 自动触发规则

| 用户意图 | 路由到 | 调用方式 |
|---------|--------|---------|
| "SEO/优化网站/关键词" | @seo-content-planner / @seo-keyword-strategist | Gemini CLI @agent |
| "内容/写文章/写博客" | @content-marketer / @seo-content-planner | Gemini CLI @agent |
| "客户/销售/开发信" | @sales-automator / @customer-support | Gemini CLI @agent |
| "数据分析/商业分析" | @business-analyst / @data-engineer | Gemini CLI @agent |
| "交易/量化/策略" | @quant-analyst / @risk-manager | Gemini CLI @agent |
| "AI/LLM/Prompt" | @ai-engineer / @prompt-engineer | Gemini CLI @agent |
| "启动/创业/项目评估" | @startup-analyst | Gemini CLI @agent |
| 其他领域任务 | 自动匹配 191 个 Agent 中最相关的 | Gemini CLI 智能路由 |

## 手动触发

```
@business-analyst: 分析这个市场的竞争格局
@seo-content-planner: 为折叠房屋写内容策略
@quant-analyst: 分析这个交易策略的风险
@content-marketer: 写一篇外贸社媒文章
```

## 安装/初始化

```bash
# 已完成
cd data/agents-marketplace && make generate HARNESS=gemini
# 已生成 155 skills + 191 agents
```

## 调用方式

### Gemini CLI 直接调用（推荐）
```bash
gemini -p "@seo-keyword-strategist: 为钢结构住宅做关键词策略"
```

### 通过太一自动路由
```
用户说："帮我优化一下这个关键词策略"
→ 太一 → 识别为SEO需求 → 路由到 @seo-keyword-strategist
→ 调 Gemini CLI 执行 → 返回结果
```

## 配置

`config/settings.json` — 路由映射表、Agent 偏好优先级。
