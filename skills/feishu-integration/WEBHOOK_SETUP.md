# 飞书 Webhook 配置指南

> **应用**: 太一 AI (cli_a9086d6b5779dcc1)
> **时间**: 2026-05-04
> **状态**: 需要配置 Webhook 接收消息

---

## 🔴 问题分析

**现象**: 在飞书发送消息给 Bot，没有收到回复

**原因**: 
1. 没有配置消息接收 Webhook
2. 飞书事件没有推送到本地服务
3. 没有启动消息监听服务

---

## 🔧 解决方案

### 方案1: 使用飞书开放平台 Webhook (推荐)

#### 步骤1: 配置事件订阅

1. 访问 https://open.feishu.cn/app/cli_a9086d6b5779dcc1/baseinfo
2. 点击左侧菜单 **"事件订阅"**
3. 在 **"请求地址配置"** 中填写：
   ```
   https://your-server.com/webhook/feishu
   ```
   
   **注意**: 本地开发需要使用内网穿透工具 (如 ngrok)

#### 步骤2: 使用 ngrok 内网穿透 (本地开发)

```bash
# 安装 ngrok
npm install -g ngrok

# 启动 ngrok (映射本地 8080 端口)
ngrok http 8080

# 获取公网地址，例如：
# https://abc123.ngrok.io
```

#### 步骤3: 配置事件类型

在 **"事件订阅"** 页面添加：
- ✅ `im.message.receive_v1` (接收消息)
- ✅ `im.message.message_read_v1` (消息已读)

#### 步骤4: 启动本地服务

```bash
cd /home/sayelf/.openclaw/workspace/skills/feishu-integration
source /home/sayelf/.openclaw/workspace/venv-feishu/bin/activate
python3 webhook_server.py
```

---

### 方案2: 使用飞书 CLI 事件监听

```bash
# 使用 lark-cli 监听事件
lark-cli event consume im.message.receive_v1
```

---

### 方案3: 使用 OpenClaw 内置飞书集成

如果 OpenClaw 已配置飞书渠道，可以直接使用：

```yaml
# openclaw.yaml
channels:
  feishu:
    enabled: true
    app_id: cli_a9086d6b5779dcc1
    app_secret: tXHOop03ZHQynCRuEPkambASNori3KhZ
    encrypt_key: 6qyZOZsfIj892Q9zTXYNIed5iawiUyk8
    verification_token: wmWId1pTZ9oiZWJr3zcnTbWWS5Be1Ub8
```

---

## 📝 Webhook 服务器代码

创建 `webhook_server.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书 Webhook 服务器
接收飞书消息事件
"""

import json
import hmac
import hashlib
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# 配置
ENCRYPT_KEY = "6qyZOZsfIj892Q9zTXYNIed5iawiUyk8"
VERIFICATION_TOKEN = "wmWId1pTZ9oiZWJr3zcnTbWWS5Be1Ub8"


def decrypt_encrypt(encrypt_key, encrypt_text):
    """解密飞书消息"""
    # 实现解密逻辑
    pass


@app.route('/webhook/feishu', methods=['POST'])
def webhook():
    """接收飞书 Webhook"""
    data = request.get_json()
    
    # 验证 token
    token = data.get('token', '')
    if token != VERIFICATION_TOKEN:
        return jsonify({'error': 'invalid token'}), 403
    
    # 处理挑战请求 (首次配置)
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})
    
    # 处理消息事件
    event_type = data.get('header', {}).get('event_type', '')
    
    if event_type == 'im.message.receive_v1':
        event_data = data.get('event', {})
        message = event_data.get('message', {})
        
        # 获取消息内容
        content = json.loads(message.get('content', '{}'))
        text = content.get('text', '')
        
        # 获取发送者
        sender = event_data.get('sender', {}).get('sender_id', {}).get('open_id', '')
        
        print(f"收到消息: {text} from {sender}")
        
        # TODO: 调用太一处理消息
        # response = process_message(text, sender)
        
        return jsonify({'status': 'ok'})
    
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## ✅ 验证步骤

### 1. 检查事件订阅配置

访问 https://open.feishu.cn/app/cli_a9086d6b5779dcc1/event/subscribe

确认：
- ✅ 请求地址已配置
- ✅ `im.message.receive_v1` 已订阅
- ✅ 连接测试通过

### 2. 发送测试消息

在飞书中找到 Bot，发送：
```
你好
```

### 3. 检查日志

查看本地服务日志，确认收到消息：
```bash
tail -f logs/webhook.log
```

---

## 🔗 相关链接

- [飞书事件订阅文档](https://open.feishu.cn/document/server-docs/getting-started/event-subscription)
- [消息事件说明](https://open.feishu.cn/document/server-docs/im-v1/message/events/message_received)
- [ngrok 官网](https://ngrok.com/)

---

*太一 AGI · 飞书 Webhook 配置指南*
