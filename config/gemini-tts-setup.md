# 🎙️ Gemini 3.1 Flash TTS 配置指南

> **更新时间**: 2026-04-17 08:15  
> **状态**: ✅ API 已配置，等待 SDK 安装

---

## 📋 快速开始

### 步骤 1: API 密钥 ✅ 已配置

**API 密钥已存储在太一记忆库**:
```
文件：/home/nicola/.openclaw/workspace/config/feishu/config.json
密钥：AIzaSyBbOg3I31WRifCfN5nF6UxGU5oHKdV0EfI
```

脚本会自动读取，无需手动配置！

---

### 步骤 2: 安装依赖

```bash
pip install google-genai
```

---

### 步骤 3: 测试

```bash
# 测试语音生成
python3 skills/07-system/gemini-tts/gemini_tts.py
```

---

## 🔧 详细配置

### API 密钥读取优先级

| 优先级 | 来源 | 说明 |
|--------|------|------|
| **1** | 函数参数 | `GeminiTTS(api_key="...")` |
| **2** | 环境变量 | `export GEMINI_API_KEY="..."` |
| **3** | 配置文件 | `config/feishu/config.json` ✅ |

---

### 环境变量 (可选)

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `GEMINI_API_KEY` | Google AI API 密钥 | 自动读取 |
| `GEMINI_VOICE` | 默认语音 | Zephyr |
| `GEMINI_LANGUAGE` | 默认语言 | zh-CN |

---

## 🚀 使用示例

### Python API

```python
from skills_07_system.gemini_tts import GeminiTTS

# 自动读取 API 密钥
tts = GeminiTTS()

# 简单播报
tts.speak("你好，欢迎使用太一 AGI 系统！")

# 带情感播报
tts.speak_with_emotion("太好了！", emotion="happy")

# 紧急播报
tts.speak_urgent("警告！")
```

---

### 命令行

```bash
# 测试语音生成
python3 skills/07-system/gemini-tts/gemini_tts.py
```

---

## 🎛️ 音频标签

### 语速

```
<speed=0.8>  慢速 (80%)
<speed=1.0>  正常 (100%)
<speed=1.2>  快速 (120%)
```

---

### 音调

```
<pitch=low>    低音调
<pitch=normal> 正常音调
<pitch=high>   高音调
```

---

### 情感

```
<emotion=happy>    开心
<emotion=sad>      悲伤
<emotion=angry>    生气
<emotion=excited>  兴奋
<emotion=calm>     平静
<emotion=serious>  严肃
```

---

### 音量

```
<volume=soft>   轻柔
<volume=normal> 正常
<volume=loud>   大声
```

---

### 停顿

```
<break=0.5s>  停顿 0.5 秒
<break=1.0s>  停顿 1 秒
<break=2.0s>  停顿 2 秒
```

---

## 🎤 可用语音

| 语音 | 类型 | 适用场景 |
|------|------|----------|
| **Zephyr** | 中性 | 通用场景 (默认) |
| **Puck** | 中性 | 通用场景 |
| **Charon** | 低沉 | 正式场景 |
| **Kore** | 温暖 | 客服场景 |
| **Fenrir** | 有力 | 播报场景 |
| **Aoede** | 柔和 | 故事场景 |

---

## 🌍 支持语言 (部分)

| 语言 | 代码 |
|------|------|
| 中文 (简体) | zh-CN |
| 中文 (繁体) | zh-TW, zh-HK |
| 英语 (美国) | en-US |
| 英语 (英国) | en-GB |
| 日语 | ja-JP |
| 韩语 | ko-KR |
| 法语 | fr-FR |
| 德语 | de-DE |
| 西班牙语 | es-ES, es-MX |

**共支持 70+ 语言**

---

## 🔗 相关链接

| 资源 | 链接 |
|------|------|
| **Google AI Studio** | https://aistudio.google.com/ |
| **API 密钥** | https://aistudio.google.com/apikey |
| **官方文档** | https://ai.google.dev/gemini-api/docs/speech-generation |
| **GitHub SDK** | https://github.com/googleapis/python-genai |

---

## ⚠️ 注意事项

### API 配额

- **免费层**: 每分钟 60 次请求
- **付费层**: 联系 Google 提高配额

---

### 音频格式

- **输出格式**: WAV/MP3
- **采样率**: 24kHz
- **位深度**: 16-bit

---

### SynthID 水印

所有生成的音频都包含 SynthID 水印，用于标识 AI 生成的内容。

---

## 🎊 总结

### 配置状态

```
✅ API 密钥 - 已配置 (太一记忆库)
⏳ SDK 安装 - 等待安装
⏳ 测试验证 - 等待执行
```

---

### 下一步

```
1. 安装 google-genai SDK
2. 测试语音生成
3. 集成到定时任务
4. 配置 Telegram 语音推送
```

---

*太一 AGI · Gemini 3.1 Flash TTS 配置指南 v1.0 · 2026-04-17 08:15*

**🎙️ API 密钥已配置！安装 SDK 后即可使用！**
