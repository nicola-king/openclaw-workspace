---
name: git-integration
version: 1.0.0
description: git-integration skill
category: cli
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Git Integration Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 素问
> **状态**: ✅ 已激活 | **优先级**: P0-01

---

## 📋 功能概述

提供完整的 Git 版本控制能力，覆盖 clone/commit/push/PR/branch/merge 等全工作流。

---

## 🛠️ 可用命令

### 基础操作

| 命令 | 功能 | 示例 |
|------|------|------|
| `git clone <url>` | 克隆仓库 | `git clone https://github.com/user/repo.git` |
| `git init` | 初始化仓库 | `git init` |
| `git status` | 查看状态 | `git status` |
| `git log` | 查看历史 | `git log --oneline -10` |

### 分支管理

| 命令 | 功能 | 示例 |
|------|------|------|
| `git branch` | 列出分支 | `git branch -a` |
| `git checkout <branch>` | 切换分支 | `git checkout main` |
| `git checkout -b <branch>` | 创建并切换 | `git checkout -b feature/new` |
| `git merge <branch>` | 合并分支 | `git merge feature/new` |

### 提交操作

| 命令 | 功能 | 示例 |
|------|------|------|
| `git add <file>` | 添加文件 | `git add .` |
| `git commit -m "<msg>"` | 提交变更 | `git commit -m "feat: add new feature"` |
| `git push` | 推送远程 | `git push origin main` |
| `git pull` | 拉取更新 | `git pull origin main` |

### 远程操作

| 命令 | 功能 | 示例 |
|------|------|------|
| `git remote -v` | 查看远程 | `git remote -v` |
| `git remote add <name> <url>` | 添加远程 | `git remote add origin https://...` |
| `git fetch` | 获取远程 | `git fetch --all` |

### PR/MR 操作（GitHub/GitLab）

| 命令 | 功能 | 示例 |
|------|------|------|
| `gh pr create` | 创建 PR | `gh pr create --title "feat: xxx" --body "desc"` |
| `gh pr list` | 列出 PR | `gh pr list --state open` |
| `gh pr merge <id>` | 合并 PR | `gh pr merge 123 --merge` |
| `gh pr review` | 审查 PR | `gh pr review --approve` |

---

## 🔧 工具实现

### exec 命令封装

```bash
# 克隆仓库
git clone <url> [directory]

# 初始化
git init

# 状态检查
git status --porcelain

# 添加文件
git add <files>

# 提交
git commit -m "<message>"

# 推送
git push <remote> <branch>

# 拉取
git pull <remote> <branch>

# 分支
git branch [-a] [-d <branch>]
git checkout [-b] <branch>

# 合并
git merge <branch>
git rebase <branch>

# 日志
git log [--oneline] [-n <count>]

# 差异
git diff [HEAD~1]

# 远程
git remote [-v] [add|remove] <name> <url>
git fetch [--all]
```

### GitHub CLI (gh) 封装

```bash
# PR 操作
gh pr create [--title <t>] [--body <b>] [--base <branch>]
gh pr list [--state <open|closed|all>] [--limit <n>]
gh pr view [<id|url>]
gh pr merge <id> [--merge|--squash|--rebase]
gh pr review [<id>] [--approve|--request-changes|--comment]
gh pr comment <id> --body "<text>"

# Issue 操作
gh issue create [--title <t>] [--body <b>]
gh issue list [--state <open|closed|all>]
gh issue view <id>
gh issue close <id>

# Repo 操作
gh repo create [<name>] [--public|--private]
gh repo fork [<repo>]
gh repo clone <repo>
```

---

## 📝 使用示例

### 示例 1: 克隆并创建新分支

```bash
# 太一，克隆这个仓库并创建功能分支
git clone https://github.com/user/repo.git
cd repo
git checkout -b feature/new-feature
```

### 示例 2: 提交并推送

```bash
# 太一，提交刚才的修改并推送
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

### 示例 3: 创建 Pull Request

```bash
# 太一，为这个分支创建 PR
gh pr create --title "feat: add new feature" --body "This PR adds..." --base main
```

### 示例 4: 查看并合并 PR

```bash
# 太一，列出所有开放的 PR
gh pr list --state open

# 太一，合并 PR #123
gh pr merge 123 --merge
```

---

## ⚠️ 安全限制

### 需要确认的操作
- [ ] 删除分支 (`git branch -D`)
- [ ] 强制推送 (`git push --force`)
- [ ] 重置历史 (`git reset --hard`)
- [ ] 删除远程仓库

### 自动执行的操作
- [x] clone/init/status/log
- [x] add/commit/push/pull
- [x] 创建分支
- [x] 创建 PR

---

## 🔍 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Authentication failed` | 未配置认证 | 配置 SSH key 或 PAT |
| `Conflict` | 合并冲突 | 手动解决冲突后提交 |
| `Remote not found` | 远程未配置 | `git remote add origin <url>` |
| `Branch not found` | 分支不存在 | 检查分支名或创建新分支 |

---

## 🧪 测试用例

```bash
# 测试 1: 克隆
git clone https://github.com/test/repo.git /tmp/test-clone

# 测试 2: 提交
cd /tmp/test-clone
echo "test" > test.txt
git add test.txt
git commit -m "test: initial commit"

# 测试 3: 分支
git checkout -b test-branch
git branch | grep test-branch

# 清理
rm -rf /tmp/test-clone
```

---

## 📚 相关文档

- [Git 官方文档](https://git-scm.com/docs)
- [GitHub CLI 文档](https://cli.github.com/manual/)
- [太一 Git 工作流](../../workflows/GIT-WORKFLOW.md)

---

*创建时间：2026-04-03 09:10 | 素问 | 太一 AGI v5.0*
