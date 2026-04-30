# GitHub CLI 认证指南

> 创建时间：2026-04-10 22:40

---

## 📦 已安装组件

| 组件 | 状态 | 版本 |
|------|------|------|
| **Git** | ✅ 已配置 | - |
| **GitHub CLI** | ✅ 已安装 | v2.45.0 |
| **SSH 密钥** | ✅ 已配置 | id_ed25519 |
| **GitHub 账号** | ✅ 已登录 (网页) | nicola-king |

---

## 🔐 认证方式

### 方式 1: SSH 密钥认证 (推荐)

**状态**: ✅ SSH 密钥已配置并验证

**测试**:
```bash
ssh -T git@github.com
# 输出：Hi nicola-king! You've successfully authenticated
```

**配置**:
- SSH 公钥：`~/.ssh/id_ed25519.pub`
- 已添加到 GitHub 账号
- Git 已配置使用 SSH

**优点**:
- ✅ 无需重复认证
- ✅ 安全性高
- ✅ 适合自动化脚本

---

### 方式 2: GitHub CLI Token 认证

**状态**: ⏳ 待完成

**完成认证**:

**方法 A: 网页认证**
```bash
gh auth login
```
然后：
1. 选择 GitHub.com
2. 选择 SSH 协议
3. 按 Enter 打开浏览器
4. 在浏览器中授权
5. 返回终端完成

**方法 B: 使用现有登录**
```bash
gh auth login \
  --hostname github.com \
  --git-protocol ssh \
  --skip-ssh-key
```

**方法 C: Personal Access Token**
1. 访问 https://github.com/settings/tokens
2. 创建新 token (勾选 repo, workflow 权限)
3. 复制 token
4. 运行：
```bash
gh auth login --with-token < token.txt
```

---

## ✅ 当前可用功能

### Git SSH (已可用)

**状态**: ✅ 完全可用

**功能**:
- ✅ git clone/push/pull
- ✅ 自动提交
- ✅ 远程仓库同步
- ✅ 太一自动备份

**测试**:
```bash
cd /home/nicola/.openclaw/workspace
git status
git log --oneline -5
```

---

### GitHub CLI (待认证)

**状态**: 🟡 部分可用

**无需认证可用**:
- ❌ gh repo list (需要认证)
- ❌ gh issue list (需要认证)
- ❌ gh pr create (需要认证)

**认证后可用**:
- ✅ gh repo list - 列出仓库
- ✅ gh issue list - 列出 Issue
- ✅ gh pr create - 创建 PR
- ✅ gh workflow run - 运行 Actions
- ✅ gh gist create - 创建 Gist
- ✅ gh auth status - 查看认证状态

---

## 🎯 推荐配置

### 完成 GitHub CLI 认证

**最简单方式**:
```bash
gh auth login
```

然后在浏览器中：
1. 点击 "Authorize github"
2. 复制验证码 (如果需要)
3. 粘贴到终端

**或使用已有 SSH**:
```bash
gh auth login \
  --hostname github.com \
  --git-protocol ssh \
  --skip-ssh-key
```

---

## 📋 验证命令

**检查 Git 配置**:
```bash
git config --global user.name
git config --global user.email
git remote -v
```

**检查 SSH 认证**:
```bash
ssh -T git@github.com
```

**检查 GitHub CLI**:
```bash
gh --version
gh auth status
```

**列出仓库**:
```bash
gh repo list nicola-king --limit 10
```

---

## 🔗 相关文档

- `docs/github-integration.md` - GitHub 集成总览
- `workspace-taiyi/config/github-config.json` - 配置文件

---

*太一 AGI | 2026-04-10 22:40*
