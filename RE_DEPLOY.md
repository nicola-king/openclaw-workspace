# 🚀 太一 9 大 Agent 重新部署指南

> **问题**: GitHub 仓库未成功创建  
> **原因**: GitHub CLI 会话过期  
> **解决**: 使用 Token 重新部署  
> **时间**: 2026-04-12 18:30

---

## ❌ 当前状态

**GitHub API 检查结果**:
```
✅ 账户：nicola-king (存在)
❌ 仓库：9 大 Agent 仓库不存在
⚠️ 只有一个仓库：- (自由职业)
```

**本地 Git 状态**:
```
✅ 9 大 Agent 代码已准备
✅ 本地 Git 已初始化
✅ Remote 已配置
❌ 推送失败 (仓库不存在)
```

---

## 🔐 解决方案

### 方式 1: 使用 Token 自动创建 + 推送 (推荐)

**Step 1: 获取新 Token**

1. 访问：https://github.com/settings/tokens
2. 使用 `shanyejingling@gmail.com` 登录
3. 点击 "Generate new token (classic)"
4. Note: `taiyi-deploy-20260412`
5. 勾选权限：
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `delete_repo` (可选，删除失败仓库)
6. 点击 "Generate token"
7. **复制 Token** (格式：`ghp_xxxxxxxxxxxx` 或 `github_pat_xxx`)

**Step 2: 设置 Token 并执行部署**

```bash
# 设置 Token (替换为你的实际 Token)
export GITHUB_TOKEN="ghp_你的 token"

# 执行自动部署
cd /home/nicola/.openclaw/workspace
bash scripts/auto-deploy-github.sh
```

---

### 方式 2: 手动创建仓库 + SSH 推送

**Step 1: 手动创建 9 个仓库**

访问以下链接逐个创建:

| # | 仓库名 | 创建链接 |
|---|--------|---------|
| 1 | polymarket-trading-agent | https://github.com/new?name=polymarket-trading-agent |
| 2 | gmgn-trading-agent | https://github.com/new?name=gmgn-trading-agent |
| 3 | binance-trading-agent | https://github.com/new?name=binance-trading-agent |
| 4 | cross-border-trade-agent | https://github.com/new?name=cross-border-trade-agent |
| 5 | taiyi-voice-agent | https://github.com/new?name=taiyi-voice-agent |
| 6 | taiyi-memory-system-v3 | https://github.com/new?name=taiyi-memory-system-v3 |
| 7 | taiyi-education-agent | https://github.com/new?name=taiyi-education-agent |
| 8 | taiyi-office-agent | https://github.com/new?name=taiyi-office-agent |
| 9 | taiyi-diagram-agent | https://github.com/new?name=taiyi-diagram-agent |

**创建要求**:
- ✅ 设置为 **Public** (公开)
- ❌ **不要** 勾选 "Add a README file"
- ❌ **不要** 添加 .gitignore
- ❌ **不要** 添加 License

**Step 2: 执行 SSH 推送**

```bash
cd /home/nicola/.openclaw/workspace
bash scripts/deploy-with-ssh.sh
```

---

## 📝 验证部署

**检查仓库是否创建**:
```bash
curl -s https://api.github.com/users/nicola-king/repos | grep '"name"'
```

**访问仓库页面**:
```
https://github.com/nicola-king?tab=repositories
```

**应显示 9 个新仓库**:
- polymarket-trading-agent
- gmgn-trading-agent
- binance-trading-agent
- cross-border-trade-agent
- taiyi-voice-agent
- taiyi-memory-system-v3
- taiyi-education-agent
- taiyi-office-agent
- taiyi-diagram-agent

---

## 🔍 故障排查

**问题 1: "Repository not found"**
```
原因：仓库不存在
解决：先创建仓库，再推送
```

**问题 2: "Permission denied"**
```
原因：SSH Key 未配置
解决：ssh-keygen -t ed25519 并添加到 GitHub
```

**问题 3: "Authentication failed"**
```
原因：Token 过期或无效
解决：生成新 Token 并重新设置
```

**问题 4: "CLI not logged in"**
```
原因：GitHub CLI 未认证
解决：gh auth login 或使用 Token 方式
```

---

## ✅ 成功标志

**部署成功后应显示**:
```
✅ polymarket-trading-agent - 已推送
✅ gmgn-trading-agent - 已推送
✅ binance-trading-agent - 已推送
✅ cross-border-trade-agent - 已推送
✅ taiyi-voice-agent - 已推送
✅ taiyi-memory-system-v3 - 已推送
✅ taiyi-education-agent - 已推送
✅ taiyi-office-agent - 已推送
✅ taiyi-diagram-agent - 已推送
```

**GitHub 仓库页面**:
```
https://github.com/nicola-king?tab=repositories
显示 9 个新仓库，每个都有代码内容
```

---

**🚀 重新部署 9 大 Agent 到 GitHub！**

**太一 AGI · 2026-04-12**
