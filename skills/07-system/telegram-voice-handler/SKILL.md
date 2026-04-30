---
name: telegram-voice-handler
version: 1.0.0
description: Telegram 语音消息自动识别
category: system
tags: ['telegram', 'voice', 'stt', 'speech-recognition']
author: 太一 AGI
created: 2026-04-15
status: active
---

# Telegram 语音消息自动识别

> 版本：v1.0 | 创建：2026-04-15  
> 功能：语音消息 → 自动下载 → STT 识别 → 太一处理

---

## 🎯 功能

- ✅ 监听 Telegram 语音消息
- ✅ 自动下载语音文件
- ✅ 语音识别 (Whisper / Azure Speech)
- ✅ 转文字后发送给太一处理
- ✅ 支持中文识别

---

## 🛠️ 安装

### 1. 安装 Whisper (推荐，免费本地)

```bash
pip3 install openai-whisper
```

### 2. 或配置 Azure Speech (云端，免费 500 分钟/月)

```bash
# 安装 SDK
pip3 install azure-cognitiveservices-speech

# 配置环境变量
cat >> ~/.openclaw/.env << EOF
AZURE_SPEECH_KEY=你的密钥
AZURE_SPEECH_REGION=eastasia
EOF
```

### 3. 配置 Telegram Bot Token

```bash
cat >> ~/.openclaw/.env << EOF
TELEGRAM_BOT_TOKEN=你的 Bot Token
EOF
```

---

## 🚀 使用

### 自动处理

```python
from voice_handler import TelegramVoiceHandler
import asyncio

handler = TelegramVoiceHandler()

# 处理语音消息
text = await handler.process_voice_message(
    file_id="xxx",
    chat_id="xxx",
    message_id=123
)

# 发送给太一
handler.send_to_taiyi(text, chat_id)
```

### 测试

```bash
cd /home/nicola/.openclaw/workspace/skills/07-system/telegram-voice-handler
python3 voice_handler.py
```

---

## 📊 STT 引擎对比

| 引擎 | 准确率 | 成本 | 延迟 | 推荐 |
|------|--------|------|------|------|
| **Whisper (tiny)** | 90%+ | 免费 | <2s | ✅ 推荐 |
| **Whisper (base)** | 93%+ | 免费 | <3s | ✅ 推荐 |
| **Whisper (large)** | 97%+ | 免费 | <5s | 高精度 |
| **Azure Speech** | 98%+ | 免费 500 分钟/月 | <1s | 生产环境 |

---

## 📁 文件结构

```
telegram-voice-handler/
├── voice_handler.py      # 核心处理器
├── SKILL.md              # 技能定义
├── requirements.txt      # 依赖
└── README.md             # 使用说明
```

---

## 🔗 相关链接

- Whisper: https://github.com/openai/whisper
- Azure Speech: https://azure.microsoft.com/zh-cn/products/cognitive-services/speech-to-text/
- Telegram Bot API: https://core.telegram.org/bots/api

---

*太一 AGI · 2026-04-15*
