# 🔐 GitHub 快速认证指南

> **紧急认证** - 完成 9 大 Agent 上线

---

## ⚡ 方式 1: GitHub CLI 认证 (推荐，30 秒)

```bash
# 执行认证命令
gh auth login

# 选择:
# 1. GitHub.com
# 2. SSH
# 3. 按提示打开浏览器
# 4. 登录并授权
# 5. 完成！
```

**认证后执行**:
```bash
bash /home/nicola/.openclaw/workspace/scripts/auto-deploy-github.sh
```

---

## ⚡ 方式 2: GitHub Token (1 分钟)

### Step 1: 获取 Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写 Note: `taiyi-deploy`
4. 勾选权限：✅ `repo` (Full control of private repositories)
5. 点击 "Generate token"
6. **复制 Token** (格式：`ghp_xxxxxxxxxxxx`)

### Step 2: 设置环境变量

```bash
export GITHUB_TOKEN="ghp_你的 token"
```

### Step 3: 执行部署

```bash
bash /home/nicola/.openclaw/workspace/scripts/auto-deploy-github.sh
```

---

## 📊 认证状态检查

```bash
# 检查 CLI 认证
gh auth status

# 检查 Token
echo $GITHUB_TOKEN
```

---

## 🚀 一键部署命令

**CLI 方式**:
```bash
gh auth login && bash /home/nicola/.openclaw/workspace/scripts/auto-deploy-github.sh
```

**Token 方式**:
```bash
export GITHUB_TOKEN="ghp_xxx" && bash /home/nicola/.openclaw/workspace/scripts/auto-deploy-github.sh
```

---

## 📝 9 大 Agent 列表

即将上线的仓库:
1. polymarket-trading-agent
2. gmgn-trading-agent
3. binance-trading-agent
4. cross-border-trade-agent
5. taiyi-voice-agent
6. taiyi-memory-system-v3
7. taiyi-education-agent
8. taiyi-office-agent
9. taiyi-diagram-agent

---

## ✅ 完成后查看

```bash
# 查看我的 GitHub 仓库
https://github.com/nicola-king?tab=repositories
```

---

**🔐 完成认证后，9 大 Agent 自动上线！**

**太一 AGI · 2026-04-12**
