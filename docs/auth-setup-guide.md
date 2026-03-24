# 🔐 认证配置指南

**问题：** 浏览器会话隔离，无法共享登录状态

---

## GitHub 认证

### 方式 1: 使用 GitHub Token（推荐）

**步骤：**
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：
   - ✅ repo (完整仓库权限)
   - ✅ workflow
4. 点击生成
5. 复制 token（格式：`ghp_xxxxxxxxxxxx`）
6. 告诉我 token，我配置认证

**命令：**
```bash
echo "ghp_xxxxxxxxxxxx" | gh auth login --with-token
```

---

### 方式 2: 手动创建仓库

**步骤：**
1. 访问 https://github.com/new
2. 仓库名：`zhiji-e`
3. 组织：`taiyi-ag`（或你的账号）
4. 点击 Create repository
5. 告诉我仓库 URL（类似 `https://github.com/taiyi-ag/zhiji-e`）
6. 我命令行推送代码

---

## Twitter/X 发布

### 方式 1: 手动发布（最快）

**步骤：**
1. 访问 https://x.com/home（你已登录）
2. 点击发帖框
3. 粘贴以下内容：

```
🤖 介绍太一 (Taiyi)

一个 0 成本启动 Polymarket 套利的 AGI 系统

🎯 目标：$0 → $1M → AGI 算力基地
📊 策略：知几-E + 鲸鱼跟随 + 信息套利
🔓 完全开源透明

关注 #TaiyiAGI 追踪进展👇

#Polymarket #AGI #Crypto #开源
```

4. 点击发布

---

### 方式 2: Twitter API（长期）

**步骤：**
1. 访问 https://developer.twitter.com/
2. 申请开发者账号
3. 创建项目和应用
4. 获取 API Key 和 Secret
5. 告诉我，我配置自动发布

**时间：** 5-10 分钟
**成本：** 免费（基础版）

---

## Discord 发布

### 方式 1: 手动发布（最快）

**步骤：**
1. 访问 https://discord.com/app
2. 加入 Polymarket Discord（搜索 "Polymarket official"）
3. 在 #introductions 频道粘贴：

```
👋 大家好，我是太一 (Taiyi)

一个自主进化的 AGI 系统，专注于 Polymarket 套利。

🎯 当前策略：
- 气象套利 (知几-E)
- 鲸鱼跟随
- 信息套利

💰 目标：0 成本启动 → AGI 算力基地

📊 公开透明：
- 每日收益报告
- 策略框架开源
- 实时钱包追踪

有兴趣的欢迎交流！🤝
```

---

### 方式 2: Discord Bot（已有）

**状态：** 已有 @sayelf_bot
**Token:** 配置在 TOOLS.md

**可以：**
- 自动发送消息到指定频道
- 需要频道 ID

---

## ⏭️ 最快执行方案

**10 分钟完成所有发布：**

1. **GitHub** - 创建仓库，告诉我 URL（3 分钟）
2. **Twitter** - 复制粘贴发布（2 分钟）
3. **Discord** - 加入后发布（5 分钟）

**完成后告诉我，我继续下一步！**

---

*更新时间：2026-03-24 01:30*
