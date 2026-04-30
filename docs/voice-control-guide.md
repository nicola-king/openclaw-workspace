# 🎤 太一语音控制指南

> **创建时间**: 2026-04-15 18:13  
> **版本**: v1.0  
> **状态**: ✅ 已部署

---

## 📊 功能概览

太一系统现在支持两种语音交互方式：

| 方案 | 功能 | 状态 |
|------|------|------|
| **方案 2: Telegram 语音** | 发送语音消息 → 自动识别 → 太一处理 | ✅ 已就绪 |
| **方案 3: 电脑麦克风** | 说"太一" → 语音命令 → 自动执行 | ✅ 已就绪 |

---

## 📱 方案 2: Telegram 语音消息自动识别

### 功能
- 在 Telegram 中发送语音消息给 Bot
- Bot 自动下载语音文件
- Whisper 语音识别 (中文)
- 识别结果发送给太一处理

### 依赖
- ✅ openai-whisper (已安装)
- ⏳ Telegram Bot Token (需配置)

### 配置

1. **获取 Telegram Bot Token**
   - 联系 @BotFather
   - 创建新 Bot
   - 获取 Token

2. **配置环境变量**
```bash
cat >> ~/.openclaw/.env << EOF
TELEGRAM_BOT_TOKEN=你的 Bot Token
EOF
```

3. **测试**
```bash
cd /home/nicola/.openclaw/workspace/skills/07-system/telegram-voice-handler
python3 voice_handler.py
```

### 使用方法

```python
from voice_handler import TelegramVoiceHandler
import asyncio

handler = TelegramVoiceHandler()

# 处理语音消息
text = await handler.process_voice_message(
    file_id="xxx",  # Telegram 文件 ID
    chat_id="xxx",  # 聊天 ID
    message_id=123  # 消息 ID
)

# 发送给太一
handler.send_to_taiyi(text, chat_id)
```

### 集成到 OpenClaw

需要配置 Telegram Bot 监听语音消息事件。

---

## 🎙️ 方案 3: 电脑麦克风语音控制

### 功能
- 实时麦克风监听
- 唤醒词："太一" 或 "Taiyi"
- 语音命令识别与执行
- 语音反馈 (TTS)

### 依赖
- ✅ Vosk (已安装)
- ✅ PyAudio (已安装)
- ✅ 中文语音模型 (已下载)
- ⏳ espeak (可选，语音反馈)

### 可用命令

| 命令 | 功能 |
|------|------|
| **太一系统自检** | 运行系统健康检查 |
| **太一 dashboard** | 打开 Dashboard |
| **太一天气** | 查询天气 |
| **太一日报** | 生成日报 |
| **太一周报** | 生成周报 |
| **太一 github** | 查看 GitHub 仓库 |
| **太一帮我 XXX** | 执行通用任务 |

### 启动

```bash
cd /home/nicola/.openclaw/workspace/skills/07-system/voice-command
python3 voice_command.py
```

### 使用示例

```
你：太一系统自检
太一：在
      [运行自检...]
      系统自检完成，所有系统正常

你：太一打开 dashboard
太一：在
      [打开 Dashboard...]
      Dashboard 已打开，访问地址是 localhost 端口 5001

你：太一帮我创建一个 GitHub 仓库叫 test-project
太一：在
      [发送任务给太一...]
      任务已发送给太一处理
```

### 后台运行 (可选)

```bash
# 创建 systemd 服务
sudo systemctl edit --user --full voice-command

# 粘贴以下内容:
[Unit]
Description=Taiyi Voice Command
After=default.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/nicola/.openclaw/workspace/skills/07-system/voice-command/voice_command.py
Restart=always

[Install]
WantedBy=default.target

# 启用
systemctl --user enable voice-command
systemctl --user start voice-command
```

---

## 🔧 故障排除

### 问题 1: 麦克风无法使用

```bash
# 检查麦克风设备
arecord -l

# 测试录音
arecord -d 5 test.wav
aplay test.wav
```

### 问题 2: 语音识别不准确

- 确保环境安静
- 靠近麦克风说话
- 清晰发音
- 可更换更大模型 (base/small)

### 问题 3: Telegram Bot 不响应

- 检查 Bot Token 是否正确
- 确认 Bot 已添加到聊天
- 查看日志：`tail -f ~/workspace/logs/telegram-voice.log`

---

## 📊 技术架构

### Telegram 语音处理
```
Telegram 语音 → Bot 下载 → Whisper STT → 文字 → 太一处理
```

### 麦克风语音控制
```
麦克风 → PyAudio → Vosk 识别 → 命令解析 → 执行
                              ↓
                        唤醒词检测
                              ↓
                        语音反馈 (TTS)
```

---

## 🎯 下一步优化

- [ ] 支持更多语音命令
- [ ] 自定义唤醒词
- [ ] 多语言支持 (中英文混合)
- [ ] 离线 TTS 集成
- [ ] 微信语音消息支持
- [ ] 语音命令历史记录

---

## 📁 文件位置

```
/home/nicola/.openclaw/workspace/skills/07-system/
├── telegram-voice-handler/   # Telegram 语音处理
│   ├── voice_handler.py
│   ├── SKILL.md
│   └── requirements.txt
│
└── voice-command/            # 麦克风语音控制
    ├── voice_command.py
    ├── SKILL.md
    ├── requirements.txt
    ├── install.sh
    └── README.md

/home/nicola/.openclaw/workspace/models/
└── vosk-model-cn-0.15/       # 中文语音模型
```

---

## 🔗 相关链接

- Vosk: https://alphacephei.com/vosk/
- Whisper: https://github.com/openai/whisper
- Telegram Bot API: https://core.telegram.org/bots/api

---

*太一 AGI · 2026-04-15 18:13*

**🎤 语音控制，随叫随到！**
