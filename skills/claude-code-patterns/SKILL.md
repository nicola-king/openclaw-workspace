---
name: claude-code-patterns
description: Claude Code 实践模式蒸馏 — 钩子系统·CLAUDE.md模板·安全检查·Conventional Commits
version: 1.0.0
author: 太一 AGI
tags: [patterns, hooks, security, git, templates]
---

# Claude Code 模式 · 太一集成

蒸馏自 `claude-code-best-practices` + `claude-code-guide`

## 核心映射

| Claude Code | 太一系统 | 状态 |
|------------|---------|------|
| `CLAUDE.md` | `SOUL.md` + `MEMORY.md` + `AGENTS.md` | ✅ 已有 |
| `.claude/skills/` | `skills/` 36个 | ✅ 已有 |
| `.claude/hooks/` | `hooks/` + 34个 cron | ✅ 已适配 |
| MCP Servers | `mcp-integration` skill | ✅ 已有 |
| Cost Management | Token 监控 cron | ✅ 已有 |
| Multi-Agent | 8 Agent 体系 | ✅ 已有 |

## 新增组件

### 1. 安全检查钩子 (`hooks/`)
- `block-secrets.sh` — 防止敏感信息泄露到 Git
- `format-on-write.sh` — 文件写入时自动格式化
- `pre-git-backup.sh` — 备份前扫描 output/notes/ 目录

### 2. Conventional Commits 模式
已在 Git 备份 cron 中使用的提交信息格式：
```
[自动备份] YYYY-MM-DD
[能力涌现] 新 Skill 名称
[修复] 问题描述
[配置] 修改项
```

### 3. CLAUDE.md 模板精华
- 明确的项目边界声明（DO/DON'T 列表）
- 技术栈偏好声明
- 测试规范和命名约定
- 构建与部署工作流

## 集成方式
- Hooks 由 `skills/claude-code-patterns/hooks/` 提供
- 安全检查集成到 Git 备份 cron
- 模式文档供所有 Agent 参考
