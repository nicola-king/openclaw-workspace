---
name: tts
version: 1.0.0
description: tts skill
category: tools
tags: []
author: 太一 AGI
created: 2026-04-07
---


# TTS 语音技能 (Microsoft VibeVoice + Azure Speech)

> 微软音频开源集成 | 语音识别 + 语音合成 | 2026-04-02 创建

---

## 📚 微软音频开源项目概览

### 主要项目

| 项目 | 类型 | 状态 | 用途 |
|------|------|------|------|
| **VibeVoice** | TTS + ASR | ✅ 开源 | 语音合成 + 语音识别 |
| **Azure Speech Service** | TTS + ASR | ✅ 云服务 | 语音合成 + 语音识别 + 翻译 |
| **SpeechT5** | 多模态 | ✅ 开源 | 语音 + 文本统一模型 |
| **UniSpeech** | ASR | ✅ 开源 | 统一语音识别 |

---

## 🎯 VibeVoice (微软最新开源)

### 项目信息

- **GitHub**: https://github.com/microsoft/VibeVoice
- **主页**: https://vibevoice.io/
- **Hugging Face**: https://huggingface.co/microsoft/VibeVoice-1.5B
- **发布日期**: 2025-09-05
- **许可证**: MIT

### 核心特性

| 特性 | 说明 |
|------|------|
| **TTS (文本转语音)** | 生成富有表现力的长格式多说话人对话音频 |
| **ASR (语音识别)** | 统一语音转文本模型，支持 60 分钟长音频 |
| **超低帧率** | 7.5 Hz 连续语音 token 化器 |
| **多说话人** | 支持最多 4 个不同说话人 |
| **长格式** | 支持长达 90 分钟的音频生成 |
| **说话人一致性** | 保持说话人音色一致性 |

### 适用场景

- ✅ 播客生成
- ✅ 有声书朗读
- ✅ 多角色对话
- ✅ 语音助手
- ✅ 视频配音

---

## 🔧 Azure Speech Service (云服务)

### 服务信息

- **文档**: https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/
- **免费额度**: 每月 500 分钟 (标准层)
- **支持语言**: 100+ 种语言
- **声音数量**: 400+ 种神经语音

### 核心功能

| 功能 | 说明 |
|------|------|
| **语音识别 (STT)** | 语音转文本，准确率 98%+ |
| **语音合成 (TTS)** | 文本转语音，400+ 种声音 |
| **语音翻译** | 实时语音翻译 |
| **说话人识别** | 区分不同说话人 |
| **自定义语音** | 训练自定义模型 |

### 中文声音推荐

| 声音 | 性别 | 风格 | 适用场景 |
|------|------|------|---------|
| zh-CN-XiaoxiaoNeural | 女 | 温暖、友好 | 通用、助手 |
| zh-CN-YunxiNeural | 男 | 阳光、专业 | 新闻、播报 |
| zh-CN-YunjianNeural | 男 | 激情、运动 | 体育、激情 |
| zh-CN-XiaoyiNeural | 女 | 可爱、活泼 | 儿童、动画 |

---

## 🛠️ 安装方案

### 方案一：VibeVoice 本地部署 (推荐用于离线/隐私)

**系统要求**:
- Python 3.10+
- GPU (推荐 NVIDIA, 8GB+ VRAM)
- 10GB 磁盘空间

**安装步骤**:

```bash
# 1. 克隆仓库
git clone https://github.com/microsoft/VibeVoice.git
cd VibeVoice

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 下载模型
python scripts/download_models.py

# 5. 测试
python demo.py --text "你好，这是 VibeVoice 语音合成测试"
```

**太一集成脚本**:
```python
# scripts/vibevoice-tts.py
import torch
from vibevoice import VibeVoiceTTS

class VibeVoiceTTSWrapper:
    def __init__(self, model_path="microsoft/VibeVoice-1.5B"):
        self.model = VibeVoiceTTS.from_pretrained(model_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
    
    def synthesize(self, text, output_path="output.wav", speaker_id=0):
        """文本转语音"""
        audio = self.model.generate(text, speaker_id=speaker_id)
        audio.save(output_path)
        return output_path
    
    def transcribe(self, audio_path, language="zh-CN"):
        """语音转文本"""
        transcription = self.model.transcribe(audio_path, language=language)
        return transcription
```

---

### 方案二：Azure Speech Service (推荐用于生产/稳定)

**步骤**:

```bash
# 1. 注册 Azure 账号
# 访问：https://azure.microsoft.com/free/

# 2. 创建语音服务
# Azure 门户 → 创建资源 → AI + 机器学习 → 语音服务

# 3. 获取密钥和区域
# 密钥 1 / 密钥 2 / 区域 (如 eastasia)

# 4. 安装 Python SDK
pip install azure-cognitiveservices-speech
```

**太一集成脚本**:
```python
# scripts/azure-speech-tts.py
import azure.cognitiveservices.speech as speechsdk

class AzureSpeechTTS:
    def __init__(self, api_key, region):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=api_key,
            region=region
        )
        # 设置中文语音
        self.speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
    
    def synthesize(self, text, output_path="output.wav"):
        """文本转语音"""
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return output_path
        else:
            raise Exception(f"TTS 失败：{result.reason}")
    
    def transcribe(self, audio_path, language="zh-CN"):
        """语音转文本"""
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_config.subscription,
            region=self.speech_config.region
        )
        speech_config.speech_recognition_language = language
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        result = recognizer.recognize_once_async().get()
        return result.text
```

---

## 📋 太一集成方案

### 推荐配置

**生产环境**: Azure Speech Service (稳定、高质量、免费额度够用)
**开发/测试**: VibeVoice 本地部署 (离线、隐私、无 API 调用限制)

### 配置文件

```json
// ~/.taiyi/tts/config.json
{
  "provider": "azure",  // 或 "vibevoice"
  "azure": {
    "api_key": "YOUR_AZURE_API_KEY",
    "region": "eastasia",
    "voice": "zh-CN-XiaoxiaoNeural"
  },
  "vibevoice": {
    "model_path": "microsoft/VibeVoice-1.5B",
    "device": "auto"  // auto/cuda/cpu
  }
}
```

### 使用示例

```python
# 太一 TTS 统一接口
from taiyi_tts import TaiyiTTS

tts = TaiyiTTS(config_path="~/.taiyi/tts/config.json")

# 文本转语音
audio_path = tts.synthesize("你好，我是太一")

# 语音转文本
text = tts.transcribe("voice_message.ogg")

# 发送语音消息 (Telegram)
import asyncio
asyncio.run(send_voice_message(chat_id, audio_path))
```

---

## 🎯 实施步骤

### 阶段一：Azure Speech Service (立即可用)

1. **注册 Azure** (5 分钟)
   - 访问 https://azure.microsoft.com/free/
   - 注册免费账号 (送$200 额度)

2. **创建语音服务** (5 分钟)
   - Azure 门户 → 创建资源 → 语音服务
   - 选择免费层 (F0)

3. **获取密钥** (1 分钟)
   - 复制密钥和区域到配置文件

4. **测试** (2 分钟)
   - 运行测试脚本验证

**总时间**: ~15 分钟

### 阶段二：VibeVoice 本地部署 (可选)

1. **检查 GPU** (1 分钟)
   - `nvidia-smi` 查看 GPU 状态

2. **安装依赖** (10 分钟)
   - 克隆仓库 + 安装依赖

3. **下载模型** (20 分钟)
   - 下载 1.5B 模型 (~3GB)

4. **测试** (2 分钟)
   - 运行 demo 测试

**总时间**: ~35 分钟 (需要 GPU)

---

## 📊 成本对比

| 方案 | 成本 | 质量 | 延迟 | 隐私 |
|------|------|------|------|------|
| **Azure Speech** | 免费 500 分钟/月 | ⭐⭐⭐⭐⭐ | <500ms | 云端 |
| **VibeVoice 本地** | 免费 (需 GPU) | ⭐⭐⭐⭐ | <200ms | 本地 |
| **ElevenLabs** | $5-99/月 | ⭐⭐⭐⭐⭐ | <1s | 云端 |
| **OpenAI TTS** | $0.015/1K chars | ⭐⭐⭐⭐ | <1s | 云端 |

---

## 🚀 下一步行动

### 立即可执行

1. **注册 Azure 账号** → 获取免费 TTS 额度
2. **创建语音服务** → 获取 API 密钥
3. **测试 TTS** → 验证语音合成
4. **集成太一** → 自动发送语音消息

### 后续优化

1. **声音定制** → 训练太一专属声音
2. **情感控制** → 根据内容调整语气
3. **多语言支持** → 支持中英文切换
4. **长音频优化** → 支持长文本分段合成

---

## 📝 记忆点

- **VibeVoice**: 微软最新开源 TTS+ASR，支持长格式多说话人
- **Azure Speech**: 云服务，免费 500 分钟/月，400+ 种声音
- **推荐**: 生产用 Azure，开发用 VibeVoice
- **中文声音**: 推荐 zh-CN-XiaoxiaoNeural (女声，温暖友好)

---

*创建时间：2026-04-02 | 太一 AGI | TTS 语音技能 v1.0*
