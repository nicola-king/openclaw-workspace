---
name: understand-anything
description: 太一智能自动化识别与调用 — 将任意代码库/知识库/文档转化为交互式知识图谱。自动检测场景，智能匹配最佳子技能，无需用户手动选择命令。
---

# Understand-Anything — 太一自动化调度中枢

## 概述

[Understand Anything](https://github.com/Lum1104/Understand-Anything) (18.4K ⭐) 是一个开源工具，通过多 Agent 流水线将代码库/知识库/文档转化为交互式知识图谱，支持可视化探索、语义搜索、差异影响分析和自动导览。

## 太一智能调度规则

太一**自动判断**场景并调用对应子技能，无需用户记住命令。

### 场景匹配矩阵

| 用户意图 | 触发关键词 | 调度子技能 | 说明 |
|---------|-----------|-----------|------|
| 理解/分析代码库 | "理解这个项目""分析代码""看架构""代码怎么组织的" | `understand` | 运行多Agent流水线，生成知识图谱 |
| 启动可视化看板 | "看可视化""打开看板""图形化""图谱" | `understand-dashboard` | 启动交互式 Web 知识图谱看板 |
| 提问代码库 | "XXXX怎么工作的""XXXX的作用""这个项目是怎么" | `understand-chat` | 基于已有知识图谱回答问题 |
| 差异影响分析 | "修改会影响什么""改了XXX会怎样""变更影响" | `understand-diff` | 分析 Git 差异的影响范围 |
| 深度解释某文件/函数 | "解释这个文件""这个函数什么意思""解释一下" | `understand-explain` | 对特定文件或函数做深度解读 |
| 生成上手指南 | "新手上手指南""新人看什么""帮团队成员入门" | `understand-onboard` | 生成 Markdown 版上手指南 |
| 分析业务领域 | "业务流程图""领域模型""业务逻辑" | `understand-domain` | 提取业务领域、流程和业务步骤 |
| 分析知识库/wiki | "分析知识库""理解wiki""看知识库的结构" | `understand-knowledge` | 提取实体、关系和声明 |

### 自动触发条件（无需显式用户请求）

太一在以下情况下**主动建议**调用 Understand-Anything：

1. **用户分享/上传代码库** → 自动判断是否需要分析理解
2. **用户询问项目架构** → 检测是否已有知识图谱，有则 `understand-chat`，无则建议 `understand`
3. **用户讨论代码变更** → 检测 Git 差异，调用 `understand-diff`
4. **新人接入手册需求** → 调用 `understand-onboard`
5. **项目规模判断** → 用户提及 "大项目""新项目""接手" 等自动触发

### 自动匹配规则（代码库分析）

```yaml
# 太一自动识别规则
language_detection:
  - extensions: [.js, .ts, .jsx, .tsx, .py, .go, .rs, .java, .rb, .php, .cpp, .cs, .swift, .kt, .vue, .css, .sql, .yaml, .tf, .graphql, .proto, .sh, .dockerfile, .html, .json, .md]
    action: check_project_size → if files > 20 ⇒ suggest /understand
  - threshold: 20 files or 1 major framework detected

wiki_detection:
  - pattern: "index.md + wikilinks [[...]]"
    action: → /understand-knowledge

diff_detection:
  - pattern: user asks "what changed" or "impact of" or mentions git diff
    action: → /understand-diff

domain_extraction:
  - pattern: user asks about business logic, workflows, processes
    action: → /understand-domain
```

## 调用流程

### 场景 1：分析代码库

```
太一检测 → 用户提到项目/代码库
    ├─ 检查 .understand-anything/knowledge-graph.json 是否存在
    │   ├─ 存在且未过时 → 直接调用 understand-chat 或 understand-dashboard
    │   └─ 不存在/过时 → 调用 understand 运行分析流水线
    │       └─ 分析完成 → 自动启动 understand-dashboard
    └─ 回报结果给用户
```

### 场景 2：可视化探索

```
太一检测 → 用户想看图谱
    ├─ 检查知识图谱是否存在
    │   ├─ 存在 → 启动 understand-dashboard
    │   └─ 不存在 → 先 /understand 再 /understand-dashboard
    └─ 返回 Dashboard URL
```

### 场景 3：提问

```
太一检测 → 用户问关于项目的问题
    ├─ 检查知识图谱是否存在
    │   ├─ 存在 → 调用 understand-chat，注入图谱上下文
    │   └─ 不存在 → 告知用户需先运行分析
    └─ 基于图谱回答问题
```

## 安装说明

已通过 OpenClaw 方式安装（folder symlink）：

```
~/.openclaw/skills/understand-anything/  →  8个子技能
~/.understand-anything-plugin/           →  插件根目录
```

**构建 Dashboard 依赖（首次使用需要）：**
```bash
cd ~/.understand-anything-plugin && pnpm install --frozen-lockfile 2>/dev/null || pnpm install
cd ~/.understand-anything-plugin && pnpm --filter @understand-anything/core build
```

## 依赖

- **Node.js >= 22** — 已满足
- **pnpm** — 包管理器
- **Dashboard** 需要构建后使用 React/Vite 开发服务器

## 子技能速查

| 技能 | SKILL.md 位置 |
|------|--------------|
| `understand` | `~/.openclaw/skills/understand-anything/understand/SKILL.md` |
| `understand-chat` | `~/.openclaw/skills/understand-anything/understand-chat/SKILL.md` |
| `understand-dashboard` | `~/.openclaw/skills/understand-anything/understand-dashboard/SKILL.md` |
| `understand-diff` | `~/.openclaw/skills/understand-anything/understand-diff/SKILL.md` |
| `understand-explain` | `~/.openclaw/skills/understand-anything/understand-explain/SKILL.md` |
| `understand-onboard` | `~/.openclaw/skills/understand-anything/understand-onboard/SKILL.md` |
| `understand-domain` | `~/.openclaw/skills/understand-anything/understand-domain/SKILL.md` |
| `understand-knowledge` | `~/.openclaw/skills/understand-anything/understand-knowledge/SKILL.md` |
