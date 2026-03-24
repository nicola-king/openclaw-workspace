# Railway 部署下一步

**状态：** 🟡 CLI 已安装，等待登录

---

## ✅ 已完成

- Railway CLI 安装成功
- 部署脚本就绪

---

## 🔐 步骤 1: 登录 Railway

**SAYELF 需要执行：**

```bash
railway login
```

这会打开浏览器，使用 GitHub 登录。

**或者告诉我：**
- "已登录" - 我继续下一步
- 或提供 Railway 项目 URL

---

## 📁 步骤 2: 初始化项目

登录后执行：
```bash
cd /home/nicola/.openclaw/workspace
railway init
```

---

## ⚙️ 步骤 3: 配置环境变量

```bash
railway variables set POLYMARKET_API_KEY=019d1b31-787e-7829-87b7-f8382effbab2
railway variables set POLYMARKET_WALLET=0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf
railway variables set TELEGRAM_BOT_TOKEN=待配置
```

---

## 🚀 步骤 4: 部署

```bash
railway up
```

---

## 📋 快速执行

**SAYELF，请执行：**
```bash
railway login
```

然后告诉我"完成"，我继续后续步骤。

---

*更新时间：2026-03-24 00:02*
