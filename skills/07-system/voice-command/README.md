# 🎤 太一语音命令

> 电脑麦克风语音控制 · 随叫随到

---

## 🚀 快速开始

### 一键安装

```bash
cd /home/nicola/.openclaw/workspace/skills/07-system/voice-command
bash install.sh
```

### 手动安装

```bash
# 1. 系统依赖
sudo apt-get install -y portaudio19-dev python3-pyaudio espeak

# 2. Python 依赖
pip3 install --break-system-packages vosk pyaudio

# 3. 下载模型 (500MB)
cd /tmp
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip
unzip vosk-model-cn-0.15.zip
mkdir -p ~/workspace/models
mv vosk-model-cn-0.15 ~/workspace/models/
```

### 启动

```bash
cd /home/nicola/.openclaw/workspace/skills/07-system/voice-command
python3 voice_command.py
```

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
| **太一帮我 XXX** | 执行通用任务 |

---

## 💡 使用示例

### 示例 1: 系统自检

```
你：太一系统自检
太一：在
      [运行自检...]
      系统自检完成，所有系统正常
```

### 示例 2: 打开 Dashboard

```
你：太一打开 dashboard
太一：在
      [打开 Dashboard...]
      Dashboard 已打开，访问地址是 localhost 端口 5001
```

### 示例 3: 通用任务

```
你：太一帮我创建一个 GitHub 仓库叫 test-project
太一：在
      [发送任务给太一...]
      任务已发送给太一处理
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

### 问题 2: 模型不存在

```bash
ls ~/workspace/models/vosk-model-cn-0.15
```

### 问题 3: Vosk 未安装

```bash
pip3 install --break-system-packages vosk pyaudio
```

---

## 📊 技术架构

```
麦克风 → PyAudio → Vosk 识别 → 命令解析 → 执行
                              ↓
                        唤醒词检测
                              ↓
                        语音反馈 (TTS)
```

---

## 🎯 下一步

- [ ] 支持更多命令
- [ ] 自定义唤醒词
- [ ] 多语言支持
- [ ] 离线 TTS 集成

---

*太一 AGI · 2026-04-15*

**🎤 语音控制，随叫随到！**
