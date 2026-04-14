# 🎤 MOSS-TTS-Nano 安装指南

> **更新时间**: 2026-04-14 15:20  
> **状态**: ✅ 安装完成  
> **位置**: `/tmp/moss-tts-nano/`

---

## 📦 安装步骤

### 1. 克隆仓库
```bash
cd /tmp
git clone https://github.com/openmoss/moss-tts-nano.git
cd moss-tts-nano
```

### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\\Scripts\\activate  # Windows
```

### 3. 安装依赖
```bash
# 安装 PyTorch (CPU 版本)
pip install torch torchaudio

# 安装 MOSS-TTS-Nano
pip install -e .
```

### 4. 测试
```bash
python3 -c "from moss_tts_nano import MOSSTTSNano; print('✅ 安装成功')"
```

---

## 🚀 使用方法

### Python API
```python
from moss_tts_nano import MOSSTTSNano

# 加载模型
model = MOSSTTSNano.from_pretrained("openmoss/moss-tts-nano")

# 生成语音
audio = model.generate("你好，这是 MOSS-TTS-Nano 的测试。")

# 保存
model.save_audio(audio, "output.wav")
```

### 太一集成
```python
from skills.07-system.moss-tts-nano.moss_tts_engine import MossTTSEngine

# 创建引擎
engine = MossTTSEngine()

# 生成语音
engine.generate_speech(
    text="你好，这是 MOSS-TTS-Nano 的测试。",
    output_path="/tmp/speech.wav"
)
```

---

## 🎯 核心特点

### 轻量级
- **参数量**: 0.1B (1 亿)
- **运行环境**: CPU (无需 GPU)
- **部署难度**: 低

### 多语言
- **支持语言**: 中文/英文/多语言
- **混合支持**: 中英文混合
- **语音克隆**: 支持

### 实时性
- **生成速度**: 实时
- **延迟**: 低
- **流式输出**: 支持

---

## 📋 系统要求

| 要求 | 最低 | 推荐 |
|------|------|------|
| **CPU** | 4 核 | 8 核+ |
| **内存** | 4GB | 8GB+ |
| **存储** | 1GB | 2GB+ |
| **Python** | 3.8+ | 3.10+ |
| **GPU** | ❌ 不需要 | ❌ 不需要 |

---

## 🔗 相关链接

- **GitHub**: https://github.com/openmoss/moss-tts-nano
- **Huggingface**: https://huggingface.co/openmoss/moss-tts-nano
- **Demo**: https://huggingface.co/spaces/openmoss/moss-tts-nano
- **文档**: https://github.com/openmoss/moss-tts-nano/blob/main/README.md

---

*MOSS-TTS-Nano 安装指南 · 太一 AGI · 2026-04-14 15:20*
