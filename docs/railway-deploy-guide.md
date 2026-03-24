# Railway 部署完整指南

**状态：** 🟡 待 SAYELF 注册
**预计时间：** 2 小时
**成本：** $0 (免费额度内)

---

## 步骤 1：注册 Railway (SAYELF 执行)

1. 访问 https://railway.app/
2. 点击 "Start a New Project"
3. 使用 GitHub 账号登录
4. 验证邮箱

**截图位置：** 注册成功后截图保存

---

## 步骤 2：创建项目 (太一协助)

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
cd /home/nicola/.openclaw/workspace
railway init
```

---

## 步骤 3：配置环境变量

需要配置：
- TELEGRAM_BOT_TOKEN
- OPENCLAW_API_KEY
- DATABASE_URL (Railway 自动提供)

---

## 步骤 4：部署

```bash
railway up
```

---

## 步骤 5：配置 Webhook

获取部署 URL 后，配置 Telegram Webhook：
```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=<RAILWAY_URL>/webhook
```

---

## 下一步

**SAYELF 请先完成步骤 1 注册**，然后告诉我，我继续执行后续步骤。
