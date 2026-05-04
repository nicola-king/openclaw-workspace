# GitHub 账号配置指南

> **账号**: shanyejingling@gmail.com
> **配置时间**: 2026-05-04
> **状态**: 🟡 等待 Token 认证

---

## ✅ 已完成配置

### Git 本地配置
```bash
git config --global user.email "shanyejingling@gmail.com"
git config --global user.name "SAYELF"
```

**验证**:
```bash
$ git config --list | grep user
user.email=shanyejingling@gmail.com
user.name=SAYELF
```

---

## 🟡 待完成: GitHub CLI 认证

### 方式1: 浏览器认证 (推荐)

```bash
gh auth login
```

步骤:
1. 选择 `GitHub.com`
2. 选择 `HTTPS`
3. 选择 `Login with a web browser`
4. 复制验证码到浏览器
5. 使用 `shanyejingling@gmail.com` 登录
6. 授权完成

### 方式2: Token 认证

```bash
# 生成 Token 后执行
echo "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" | gh auth login --with-token
```

**Token 获取步骤**:
1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 填写 Note: `太一系统`
4. 选择权限:
   - ✅ `repo` (仓库访问)
   - ✅ `workflow` (工作流)
   - ✅ `gist` (代码片段)
   - ✅ `read:org` (组织读取)
5. 点击 **Generate token**
6. **立即复制 Token** (只显示一次)

---

## 🔧 验证认证

```bash
# 检查认证状态
gh auth status

# 预期输出:
# github.com
#   ✓ Logged in to github.com as SAYELF (shanyejingling@gmail.com)
#   ✓ Git operations for github.com configured to use https protocol.
```

---

## 🚀 常用操作

### 克隆仓库
```bash
gh repo clone sayelf/taiyi-system
```

### 创建 Issue
```bash
gh issue create --title "Bug: 系统启动失败" --body "描述问题..."
```

### 创建 PR
```bash
gh pr create --title "功能: 添加新模块" --body "实现..."
```

### 查看工作流
```bash
gh run list
```

---

## 📁 配置文件

GitHub CLI 配置存储在:
- `~/.config/gh/hosts.yml` - 认证信息
- `~/.config/gh/config.yml` - 全局配置

---

## 🔒 安全提醒

- **Token 不要分享给他人**
- **不要在代码中硬编码 Token**
- **定期轮换 Token**
- **使用最小权限原则**

---

*太一 AGI · GitHub 配置指南*
