# 🎙️ Gemini 3.1 Flash TTS 技能

> **版本**: 1.0  
> **作者**: 太一 AGI  
> **创建**: 2026-04-17  
> **状态**: 🆕 已集成

---

## 📋 功能

- ✅ 70+ 语言语音生成
- ✅ 200+ 音频标签控制
- ✅ 多说话人对话
- ✅ 情感/语速/音调控制
- ✅ 高保真语音输出
- ✅ SynthID 水印

---

## 🔧 配置

### 安装依赖

```bash
pip install google-genai
```

---

### 配置 API 密钥

```bash
# 方式 1: 环境变量
export GEMINI_API_KEY="你的 API 密钥"

# 方式 2: 添加到 ~/.bashrc
echo 'export GEMINI_API_KEY="你的密钥"' >> ~/.bashrc
source ~/.bashrc
```

---

### 获取 API 密钥

1. 访问 https://aistudio.google.com/apikey
2. 登录 Google 账号
3. 创建新的 API 密钥
4. 复制密钥

---

## 🚀 使用

### 简单播报

```bash
python3 skills/07-system/gemini-tts/gemini_tts.py
```

---

### 带情感播报

```bash
python3 skills/07-system/gemini-tts/gemini_tts.py \
  --emotion happy \
  "你好，今天是美好的一天！"
```

---

### 紧急播报

```bash
python3 skills/07-system/gemini-tts/gemini_tts.py \
  --urgent \
  "警告：系统检测到异常！"
```

---

### Python API

```python
from skills_07_system.gemini_tts import GeminiTTS

tts = GeminiTTS()

# 简单播报
tts.speak("你好！")

# 带情感播报
tts.speak_with_emotion("太好了！", emotion="happy")

# 紧急播报
tts.speak_urgent("警告！")

# 自定义参数
tts.generate_speech(
    "你好",
    voice="Zephyr",
    speed=0.9,
    emotion="calm"
)
```

---

## 🎯 使用场景

### 1. 系统通知播报

```python
tts.speak("系统通知：定时任务执行完成，所有服务运行正常。")
```

---

### 2. 晨间智慧推送

```python
tts.speak_with_emotion(
    "早安，SAYELF。今天是 2026 年 4 月 17 日，星期五。",
    emotion="happy",
    speed=0.9
)
```

---

### 3. 告警通知

```python
tts.speak_urgent("警告：Gateway 服务异常，正在自动重启...")
```

---

### 4. 日报语音摘要

```python
tts.generate_daily_report(
    "reports/daily-report-20260417.md",
    "audio/daily-report-20260417.mp3"
)
```

---

## 🎛️ 音频标签

### 语速控制

```
<speed=0.8>  慢速 (80%)
<speed=1.0>  正常 (100%)
<speed=1.2>  快速 (120%)
```

---

### 音调控制

```
<pitch=low>    低音调
<pitch=normal> 正常音调
<pitch=high>   高音调
```

---

### 情感控制

```
<emotion=happy>    开心
<emotion=sad>      悲伤
<emotion=angry>    生气
<emotion=excited>  兴奋
<emotion=calm>     平静
<emotion=serious>  严肃
```

---

### 音量控制

```
<volume=soft>   轻柔
<volume=normal> 正常
<volume=loud>   大声
```

---

### 停顿控制

```
<break=0.5s>  停顿 0.5 秒
<break=1.0s>  停顿 1 秒
<break=2.0s>  停顿 2 秒
```

---

## 🎤 可用语音

| 语音 | 类型 | 适用场景 |
|------|------|----------|
| Zephyr | 中性 | 通用场景 |
| Puck | 中性 | 通用场景 |
| Charon | 低沉 | 正式场景 |
| Kore | 温暖 | 客服场景 |
| Fenrir | 有力 | 播报场景 |
| Aoede | 柔和 | 故事场景 |

---

## 🌍 支持语言

```
中文：zh-CN, zh-TW, zh-HK
英语：en-US, en-GB, en-AU, en-IN
日语：ja-JP
韩语：ko-KR
法语：fr-FR
德语：de-DE
西班牙语：es-ES, es-MX
葡萄牙语：pt-BR, pt-PT
意大利语：it-IT
俄语：ru-RU
... 共 70+ 语言
```

---

## 📁 文件结构

```
skills/07-system/gemini-tts/
├── SKILL.md           # 技能文档
├── gemini_tts.py      # 主程序
└── README.md          # 详细说明
```

---

## 🔗 相关链接

- **Google AI Studio**: https://aistudio.google.com/
- **API 密钥**: https://aistudio.google.com/apikey
- **官方文档**: https://ai.google.dev/gemini-api/docs/speech-generation
- **GitHub SDK**: https://github.com/googleapis/python-genai

---

*太一 AGI · Gemini 3.1 Flash TTS 技能 v1.0 · 2026-04-17*
