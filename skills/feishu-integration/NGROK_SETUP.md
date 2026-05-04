# ngrok 配置指南

> **时间**: 2026-05-04
> **状态**: 需要配置 authtoken

---

## 🔐 获取 ngrok Authtoken

1. 访问 https://dashboard.ngrok.com/get-started/your-authtoken
2. 注册/登录 ngrok 账号
3. 复制你的 authtoken

---

## 📝 配置步骤

### 步骤1: 配置 authtoken

```bash
/home/sayelf/.npm-global/bin/ngrok config add-authtoken YOUR_AUTHTOKEN
```

### 步骤2: 启动 ngrok

```bash
# 启动内网穿透 (映射本地 8080 端口)
nohup /home/sayelf/.npm-global/bin/ngrok http 8080 > logs/ngrok.log 2>&1 &
```

### 步骤3: 获取公网地址

```bash
# 查看公网地址
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool
```

预期输出：
```json
{
  "tunnels": [
    {
      "public_url": "https://abc123.ngrok.io",
      "config": {
        "addr": "localhost:8080"
      }
    }
  ]
}
```

---

## 🔧 配置飞书 Webhook

1. 访问 https://open.feishu.cn/app/cli_a9086d6b5779dcc1/event/subscribe
2. 在 **"请求地址配置"** 中填写：
   ```
   https://abc123.ngrok.io/webhook/feishu
   ```
   (替换为你的 ngrok 公网地址)
3. 点击 **"保存"**
4. 订阅事件：`im.message.receive_v1`

---

## ✅ 验证

### 1. 检查 ngrok 状态

```bash
curl -s http://localhost:4040/api/tunnels
```

### 2. 测试 Webhook

在飞书中发送消息给 Bot，检查本地日志：

```bash
tail -f /home/sayelf/.openclaw/workspace/skills/feishu-integration/logs/webhook.log
```

---

## 🚀 自动化脚本

创建启动脚本 `start_ngrok.sh`:

```bash
#!/bin/bash
# 启动 ngrok 内网穿透

# 配置 authtoken (只需执行一次)
# /home/sayelf/.npm-global/bin/ngrok config add-authtoken YOUR_AUTHTOKEN

# 启动 ngrok
echo "🚀 启动 ngrok..."
nohup /home/sayelf/.npm-global/bin/ngrok http 8080 > logs/ngrok.log 2>&1 &
echo $! > ngrok.pid

# 等待启动
sleep 5

# 显示公网地址
echo "📡 公网地址:"
curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tunnel in data.get('tunnels', []):
    print(f'  {tunnel[\"public_url\"]}')
"

echo ""
echo "✅ ngrok 已启动"
echo "🔧 请配置到飞书开放平台:"
echo "   https://open.feishu.cn/app/cli_a9086d6b5779dcc1/event/subscribe"
```

---

## 📚 相关链接

- [ngrok 官网](https://ngrok.com/)
- [ngrok 文档](https://ngrok.com/docs)
- [飞书事件订阅](https://open.feishu.cn/document/server-docs/getting-started/event-subscription)

---

*太一 AGI · ngrok 配置指南*
