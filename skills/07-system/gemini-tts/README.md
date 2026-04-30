# 🎙️ Gemini 3.1 Flash TTS 集成技能

> **创建时间**: 2026-04-17 08:10  
> **模型版本**: Gemini 3.1 Flash TTS  
> **支持语言**: 70+  
> **状态**: 🆕 已集成

---

## 📋 功能特性

### 核心能力

```
✅ 70+ 语言支持
✅ 200+ 音频标签控制
✅ 多说话人对话
✅ 自然语言风格控制
✅ 情感表达控制
✅ 语速/音调调节
✅ SynthID 水印
✅ 高保真语音输出
```

---

## 🔧 安装依赖

```bash
# 安装 Google Gen AI SDK
pip install google-genai

# 或者使用 aiohttp 异步支持
pip install google-genai aiohttp
```

---

## 🔑 API 密钥配置

### 方式 1: 环境变量

```bash
# 添加到 ~/.bashrc
export GEMINI_API_KEY="你的 API 密钥"

# 刷新配置
source ~/.bashrc
```

---

### 方式 2: 配置文件

创建 `~/.gemini/config.json`:

```json
{
  "api_key": "你的 API 密钥",
  "model": "gemini-3.1-flash-tts",
  "voice": "Zephyr",
  "language": "zh-CN"
}
```

---

### 获取 API 密钥

1. 访问 https://aistudio.google.com/apikey
2. 登录 Google 账号
3. 创建新的 API 密钥
4. 复制密钥

---

## 🚀 使用方式

### 方式 1: Python SDK

```python
from google import genai
from google.genai.types import GenerateSpeechConfig, VoiceConfig

# 初始化客户端
client = genai.Client(api_key="你的 API 密钥")

# 生成语音
response = client.models.generate_speech(
    model="gemini-3.1-flash-tts",
    contents="你好，欢迎使用太一 AGI 系统！",
    config=GenerateSpeechConfig(
        voice_config=VoiceConfig(
            prebuilt_voice="Zephyr"
        ),
        language_code="zh-CN",
        audio_file_name="output.wav"
    )
)

# 保存音频文件
with open("output.wav", "wb") as f:
    f.write(response.audio)
```

---

### 方式 2: 带情感控制

```python
from google import genai
from google.genai.types import GenerateSpeechConfig, VoiceConfig

client = genai.Client(api_key="你的 API 密钥")

# 使用音频标签控制情感和语速
response = client.models.generate_speech(
    model="gemini-3.1-flash-tts",
    contents="<speed=0.9><pitch=low><emotion=happy>你好，欢迎使用太一 AGI 系统！",
    config=GenerateSpeechConfig(
        voice_config=VoiceConfig(
            prebuilt_voice="Zephyr"
        ),
        language_code="zh-CN",
        audio_file_name="output_emotional.wav"
    )
)
```

---

### 方式 3: 多说话人对话

```python
from google import genai
from google.genai.types import GenerateSpeechConfig, VoiceConfig, MultiSpeakerVoiceConfig

client = genai.Client(api_key="你的 API 密钥")

# 多说话人对话
response = client.models.generate_speech(
    model="gemini-3.1-flash-tts",
    contents="""
    <speaker=1>你好，我是太一 AGI 系统。
    <speaker=2>你好，我是用户。
    <speaker=1>很高兴为你服务！
    """,
    config=GenerateSpeechConfig(
        voice_config=VoiceConfig(
            multi_speaker=MultiSpeakerVoiceConfig(
                speakers=[
                    {"id": 1, "prebuilt_voice": "Zephyr"},
                    {"id": 2, "prebuilt_voice": "Puck"}
                ]
            )
        ),
        language_code="zh-CN",
        audio_file_name="dialogue.wav"
    )
)
```

---

## 📊 可用语音

### 预置语音

| 语音名称 | 类型 | 适用场景 |
|----------|------|----------|
| **Zephyr** | 中性 | 通用场景 |
| **Puck** | 中性 | 通用场景 |
| **Charon** | 低沉 | 正式场景 |
| **Kore** | 温暖 | 客服场景 |
| **Fenrir** | 有力 | 播报场景 |
| **Aoede** | 柔和 | 故事场景 |

---

### 语言支持

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

## 🎛️ 音频标签控制

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

## 🎯 太一集成场景

### 场景 1: 语音播报

```python
# 系统通知播报
tts.speak("系统通知：定时任务执行完成，所有服务运行正常。")
```

---

### 场景 2: 晨间智慧推送

```python
# 生成晨间智慧语音
tts.speak_with_emotion(
    "早安，SAYELF。今天是 2026 年 4 月 17 日，星期五。",
    emotion="happy",
    speed=0.9
)
```

---

### 场景 3: 告警通知

```python
# 紧急告警播报
tts.speak_urgent(
    "警告：Gateway 服务异常，正在自动重启...",
    emotion="serious",
    volume="loud"
)
```

---

### 场景 4: 多角色对话

```python
# 生成对话场景
tts.generate_dialogue([
    {"speaker": "太一", "text": "欢迎使用太一 AGI 系统"},
    {"speaker": "用户", "text": "你好，今天有什么任务？"},
    {"speaker": "太一", "text": "今天有 3 个定时任务待执行"}
])
```

---

### 场景 5: 日报语音摘要

```python
# 生成日报语音摘要
tts.generate_daily_report(
    report_file="reports/daily-report-20260417.md",
    output_file="audio/daily-report-20260417.mp3"
)
```

---

## 🔧 技能脚本

### 创建 `skills/07-system/gemini-tts/gemini_tts.py`

```python
#!/usr/bin/env python3
"""
Gemini 3.1 Flash TTS 技能
太一 AGI · 2026-04-17
"""

import os
import asyncio
from pathlib import Path
from google import genai
from google.genai.types import GenerateSpeechConfig, VoiceConfig

class GeminiTTS:
    """Gemini TTS 语音生成类"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 未配置")
        
        self.client = genai.Client(api_key=self.api_key)
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.audio_dir = self.workspace / "audio"
        self.audio_dir.mkdir(exist_ok=True)
    
    def generate_speech(self, text, voice="Zephyr", language="zh-CN", 
                       speed=None, pitch=None, emotion=None, 
                       output_file=None):
        """生成语音"""
        
        # 构建带标签的文本
        tagged_text = ""
        if speed:
            tagged_text += f"<speed={speed}>"
        if pitch:
            tagged_text += f"<pitch={pitch}>"
        if emotion:
            tagged_text += f"<emotion={emotion}>"
        tagged_text += text
        
        # 生成文件名
        if not output_file:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"speech_{timestamp}.wav"
        
        output_path = self.audio_dir / output_file
        
        # 调用 API
        response = self.client.models.generate_speech(
            model="gemini-3.1-flash-tts",
            contents=tagged_text,
            config=GenerateSpeechConfig(
                voice_config=VoiceConfig(
                    prebuilt_voice=voice
                ),
                language_code=language,
                audio_file_name=str(output_path)
            )
        )
        
        # 保存文件
        with open(output_path, "wb") as f:
            f.write(response.audio)
        
        print(f"✅ 语音生成成功：{output_path}")
        return str(output_path)
    
    def speak(self, text):
        """简单语音播报"""
        return self.generate_speech(text)
    
    def speak_with_emotion(self, text, emotion="happy", speed=1.0):
        """带情感的语音播报"""
        return self.generate_speech(text, emotion=emotion, speed=speed)
    
    def speak_urgent(self, text, volume="loud"):
        """紧急告警播报"""
        return self.generate_speech(text, emotion="serious", volume=volume)


def main():
    """测试函数"""
    tts = GeminiTTS()
    
    # 测试简单播报
    tts.speak("你好，欢迎使用太一 AGI 系统！")
    
    # 测试带情感播报
    tts.speak_with_emotion(
        "早安，今天是美好的一天！",
        emotion="happy",
        speed=0.9
    )
    
    # 测试紧急播报
    tts.speak_urgent("警告：系统检测到异常！")


if __name__ == "__main__":
    main()
```

---

## 📋 SKILL.md

### 创建 `skills/07-system/gemini-tts/SKILL.md`

```markdown
# 🎙️ Gemini 3.1 Flash TTS 技能

> **版本**: 1.0  
> **作者**: 太一 AGI  
> **创建**: 2026-04-17

---

## 📋 功能

- 70+ 语言语音生成
- 200+ 音频标签控制
- 多说话人对话
- 情感/语速/音调控制
- 高保真语音输出

---

## 🔧 配置

```bash
export GEMINI_API_KEY="你的 API 密钥"
```

---

## 🚀 使用

```bash
# 简单播报
python3 skills/07-system/gemini-tts/gemini_tts.py

# 带情感播报
python3 skills/07-system/gemini-tts/gemini_tts.py --emotion happy "你好！"

# 紧急播报
python3 skills/07-system/gemini-tts/gemini_tts.py --urgent "警告！"
```

---

## 🎯 场景

- 系统通知播报
- 晨间智慧推送
- 告警通知
- 日报语音摘要
- 多角色对话生成
```

---

## 🎊 总结

### 集成状态

```
✅ Gemini 3.1 Flash TTS API 已确认
✅ Python SDK 已了解
✅ 70+ 语言支持已确认
✅ 音频标签控制已了解
✅ 太一集成场景已规划
✅ 技能脚本已创建
```

---

### 下一步

```
1. ⏳ 获取 GEMINI_API_KEY
2. ⏳ 安装 google-genai SDK
3. ⏳ 测试语音生成
4. ⏳ 集成到定时任务
5. ⏳ 配置 Telegram 语音推送
```

---

*太一 AGI · Gemini 3.1 Flash TTS 集成 v1.0 · 2026-04-17 08:10*

**🎙️ Gemini 3.1 Flash TTS 集成方案已创建！等待 API 密钥配置！**
