# 🚀 太一 GitHub 自动化部署指南

> **版本**: v1.0  
> **创建**: 2026-04-12 11:30  
> **方式**: GitHub CLI + API 结合

---

## 📋 部署前准备

### 方式 1: GitHub CLI 认证 (推荐)

```bash
# 执行认证
gh auth login

# 选择:
# - GitHub.com
# - SSH
# - 浏览器登录
```

### 方式 2: GitHub Token

```bash
# 获取 Token:
# 1. 访问 https://github.com/settings/tokens
# 2. Generate new token (classic)
# 3. 勾选 repo 权限
# 4. 复制 Token

# 设置环境变量
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

---

## 🚀 自动化部署

### 执行脚本

```bash
cd /home/nicola/.openclaw/workspace

# 方式 1: 已认证 GitHub CLI
bash scripts/auto-deploy-github.sh

# 方式 2: 使用 Token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
bash scripts/auto-deploy-github.sh
```

### 脚本功能

**自动检测**:
- ✅ 检测 GitHub CLI 认证状态
- ✅ 检测 GITHUB_TOKEN 环境变量
- ✅ 自动选择最佳部署方式

**自动执行**:
- ✅ 创建 GitHub 仓库
- ✅ 设置远程仓库
- ✅ 推送代码
- ✅ 报告成功/失败

**9 大 Agent**:
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

## 📊 部署流程

```
1. ✅ 检查认证状态
   ├─ GitHub CLI 已认证 → 使用 CLI
   └─ GITHUB_TOKEN 存在 → 使用 API

2. ✅ 遍历 9 大 Agent
   ├─ 创建 GitHub 仓库
   ├─ 设置远程仓库
   └─ 推送代码

3. ✅ 报告结果
   ├─ 成功列表
   └─ 失败列表 (需手动处理)
```

---

## 🔧 手动部署 (备选)

### 单个 Agent 部署

```bash
cd /home/nicola/.openclaw/workspace/skills/polymarket-trading-agent

# 设置远程
git remote add origin git@github.com:nicola-king/polymarket-trading-agent.git

# 推送
git push -u origin main
```

### 批量手动部署

```bash
for repo in polymarket-trading-agent gmgn-trading-agent binance-trading-agent cross-border-trade-agent taiyi-voice-agent taiyi-memory-v3 taiyi-education-agent taiyi-office-agent taiyi-diagram-agent; do
    cd /home/nicola/.openclaw/workspace/skills/$repo
    git remote add origin git@github.com:nicola-king/$repo.git
    git push -u origin main
done
```

---

## ✅ 部署后检查

**检查仓库**:
```bash
# 访问 GitHub
https://github.com/nicola-king?tab=repositories

# 或使用 CLI
gh repo list nicola-king
```

**检查内容**:
- [ ] README.md 存在
- [ ] 代码已推送
- [ ] 仓库为 Public
- [ ] 描述正确

**完善仓库**:
- [ ] 添加 LICENSE (MIT)
- [ ] 完善 README
- [ ] 添加 Topics 标签
- [ ] 设置 Website (可选)

---

## 📝 常见问题

### Q: "Repository not found"
**A**: 仓库未创建，使用脚本自动创建或手动创建

### Q: "Permission denied"
**A**: SSH Key 未配置，执行：
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
# 复制 ~/.ssh/id_ed25519.pub 到 GitHub SSH Keys
```

### Q: "Authentication failed"
**A**: GitHub CLI 未认证，执行：
```bash
gh auth login
```

---

## 🔗 相关链接

**GitHub**:
- 我的仓库：https://github.com/nicola-king?tab=repositories
- 创建仓库：https://github.com/new
- Token 设置：https://github.com/settings/tokens
- SSH Keys: https://github.com/settings/keys

**太一文档**:
- 发布报告：`GITHUB_PUBLISH_FINAL.md`
- 创建指南：`GITHUB_REPO_CREATION_GUIDE.md`

---

**🚀 太一 GitHub 自动化部署 - 一键上线 9 大 Agent！**

**太一 AGI · 2026-04-12**
