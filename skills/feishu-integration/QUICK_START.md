# 飞书 Bot 快速启动指南

> **应用**: 太一 AI (cli_a9086d6b5779dcc1)
> **时间**: 2026-05-04
> **状态**: 需要配置 Webhook

---

## 🚀 快速配置 (3步)

### 步骤1: 配置飞书事件订阅

1. 访问 https://open.feishu.cn/app/cli_a9086d6b5779dcc1/event/subscribe
2. 在 **"请求地址配置"** 中填写你的服务器地址：
   ```
   https://your-server.com/webhook/feishu
   ```
   
   **本地开发**: 使用 ngrok 内网穿透
   ```bash
   # 安装 ngrok
   npm install -g ngrok
   
   # 启动 ngrok (映射本地 8080 端口)
   ngrok http 8080
   
   # 获取公网地址，例如 https://abc123.ngrok.io
   # 配置到飞书: https://abc123.ngrok.io/webhook/feishu
   ```

3. 点击 **"保存"**

### 步骤2: 订阅事件类型

在 **"事件订阅"** 页面添加：
- ✅ `im.message.receive_v1` (接收消息)
- ✅ `im.message.message_read_v1` (消息已读)

### 步骤3: 启动本地服务

```bash
cd /home/sayelf/.openclaw/workspace/skills/feishu-integration
source /home/sayelf/.openclaw/workspace/venv-feishu/bin/activate
python3 webhook_server.py
```

服务启动后：
- Webhook 地址: http://localhost:8080/webhook/feishu
- 健康检查: http://localhost:8080/health

---

## ✅ 验证

### 1. 检查服务状态

```bash
curl http://localhost:8080/health
```

预期输出：
```json
{"status": "ok", "service": "feishu-webhook"}
```

### 2. 发送测试消息

在飞书中找到 **"太一 AI"** Bot，发送：
```
你好
```

### 3. 检查日志

查看终端输出，确认收到消息：
```
收到消息: '你好' from ou_xxxxxxxxxxxxxxxx
```

---

## 🔧 故障排除

### 问题1: 无法保存 Webhook 地址

**原因**: 地址无法访问或验证失败

**解决**:
1. 确保服务已启动
2. 确保地址可公网访问
3. 检查防火墙设置

### 问题2: 收到消息但没有回复

**原因**: 没有配置消息发送权限

**解决**:
1. 访问 https://open.feishu.cn/app/cli_a9086d6b5779dcc1/permission
2. 添加权限 `im:message:send`
3. 发布版本并审批

### 问题3: Token 验证失败

**原因**: Verification Token 不匹配

**解决**:
1. 检查 `config.yaml` 中的 `verification_token`
2. 确保与飞书开放平台一致

---

## 📚 相关文档

- [WEBHOOK_SETUP.md](WEBHOOK_SETUP.md) - 详细 Webhook 配置
- [PERMISSION_SETUP.md](PERMISSION_SETUP.md) - 权限配置指南
- [TEST_RESULT.md](TEST_RESULT.md) - 测试结果报告

---

*太一 AGI · 飞书 Bot 快速启动指南*
