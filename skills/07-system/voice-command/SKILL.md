---
name: voice-command
version: 1.0.0
description: 太一语音命令 - 电脑麦克风语音控制
category: system
tags: ['voice', 'speech-recognition', 'microphone', 'command']
author: 太一 AGI
created: 2026-04-15
status: active
---

# 太一语音命令

> 版本：v1.0 | 创建：2026-04-15  
> 功能：麦克风监听 → 语音识别 → 命令执行

---

## 🎯 功能

- ✅ 实时麦克风监听
- ✅ 中文语音识别 (Vosk)
- ✅ 唤醒词检测 ("太一")
- ✅ 命令解析与执行
- ✅ 语音反馈 (TTS)

---

## 🎤 唤醒词

- **"太一"** (中文)
- **"Taiyi"** (英文)

---

## 📋 可用命令

| 命令 | 功能 |
|------|------|
| **太一系统自检** | 运行系统健康检查 |
| **太一 dashboard** | 打开 Dashboard |
| **太一天气** | 查询天气 |
| **太一日报** | 生成日报 |
| **太一周报** | 生成周报 |
| **太一 github** | 查看 GitHub 仓库 |
| **太一 [任意]** | 执行通用任务 |

---

## 🛠️ 安装

### 1. 安装依赖

```bash
pip3 install vosk pyaudio
```

### 2. 下载语音模型

```bash
cd /tmp
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip
unzip vosk-model-cn-0.15.zip
mkdir -p ~/workspace/models
mv vosk-model-cn-0.15 ~/workspace/models/
```

### 3. 安装 TTS (可选，语音反馈)

```bash
sudo apt-get install espeak
```

---

## 🚀 使用

### 启动语音控制

```bash
cd /home/nicola/.openclaw/workspace/skills/07-system/voice-command
python3 voice_command.py
```

### 使用示例

```
你说：太一系统自检
太一：在
      [运行自检...]
      系统自检完成，所有系统正常

你说：太一打开 dashboard
太一：在
      [打开 Dashboard...]
      Dashboard 已打开，访问地址是 localhost 端口 5001

你说：太一帮我创建一个 GitHub 仓库
太一：在
      [发送任务给太一...]
      任务已发送给太一处理
```

---

## 🔧 故障排除

### Vosk 未安装

```bash
pip3 install vosk pyaudio
```

### 模型不存在

```bash
ls ~/workspace/models/vosk-model-cn-0.15
```

### 麦克风无法使用

```bash
# 检查麦克风权限
arecord -l

# 测试录音
arecord -d 5 test.wav
aplay test.wav
```

---

## 📁 文件结构

```
voice-command/
├── voice_command.py    # 核心控制器
├── SKILL.md            # 技能定义
├── requirements.txt    # 依赖
└── README.md           # 使用说明
```

---

## 🔗 相关链接

- Vosk: https://alphacephei.com/vosk/
- 中文模型：https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip
- PyAudio: https://pypi.org/project/PyAudio/

---

*太一 AGI · 2026-04-15*

**🎤 语音控制，随叫随到！**
