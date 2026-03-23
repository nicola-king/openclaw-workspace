# 部署流程简化方案

**创建时间：** 2026-03-23 20:59
**状态：** 🟡 准备中
**目标：** 一键部署太一系统

---

## 当前部署流程

### 现有步骤

```
1. git clone 仓库
2. npm install
3. 配置环境变量
4. 配置 Bot Token
5. 启动 Gateway
6. 测试连接
```

**耗时：** 约 30 分钟

---

## 优化后流程

### 一键部署

```
1. Railway 登录 (GitHub)
2. 点击"Deploy"
3. 自动配置环境变量
4. 自动部署 (5 分钟)
5. 获取部署 URL
```

**耗时：** 约 10 分钟

---

## 部署脚本

### 本地部署脚本

```bash
#!/bin/bash
# deploy.sh

echo "🚀 太一系统部署"

# 1. 安装依赖
npm install

# 2. 配置环境变量
cp .env.example .env
echo "请配置 Bot Token 和 API Key"

# 3. 启动 Gateway
npm run gateway:start

# 4. 测试连接
npm run test

echo "✅ 部署完成"
```

### Railway 部署

```yaml
# railway.toml

[build]
builder = "NIXPACKS"

[deploy]
healthcheck_path = "/health"
healthcheck_timeout = 300

[env]
NODE_ENV = "production"
```

---

## 配置模板

### .env.example

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_token_here

# OpenClaw
OPENCLAW_API_KEY=your_api_key_here

# Database (Railway 自动提供)
DATABASE_URL=postgresql://...

# Optional
SENTRY_DSN=your_sentry_dsn
POSTHOG_API_KEY=your_posthog_key
```

---

## 执行计划

| 任务 | 时间 | 状态 |
|------|------|------|
| **部署脚本** | 1 小时 | 🟡 待执行 |
| **配置模板** | 30 分钟 | 🟡 待执行 |
| **测试文档** | 30 分钟 | 🟡 待执行 |

---

*状态：待执行 | 预计时间：2 小时*
