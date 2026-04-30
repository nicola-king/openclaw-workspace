# 🎤 MOSS-TTS-Nano 安装状态

> **最后更新**: 2026-04-14 15:25  
> **状态**: 🟡 部分完成

---

## 📊 安装进度

| 步骤 | 状态 | 说明 |
|------|------|------|
| **克隆仓库** | ✅ 完成 | `/tmp/moss-tts-nano/` |
| **安装 torch** | 🟡 进行中 | pip install 执行中 |
| **安装 moss-tts-nano** | ⏳ 待执行 | 依赖 torch |
| **测试导入** | ❌ 失败 | CLI 方式可用 |
| **引擎封装** | ✅ 完成 | `moss_tts_engine.py` |

---

## 🔧 当前状态

**仓库位置**: `/tmp/moss-tts-nano/`

**文件结构**:
```
/tmp/moss-tts-nano/
├── moss_tts_nano/
│   ├── cli.py (CLI 接口)
│   ├── defaults.py
│   ├── __init__.py
│   └── __main__.py
├── app.py (Demo 应用)
├── infer.py (推理脚本)
├── requirements.txt
└── README.md
```

**使用方式**:
```bash
# CLI 方式
python3 /tmp/moss-tts-nano/moss_tts_nano/cli.py \
    --text "你好，这是测试。" \
    --output /tmp/speech.wav
```

---

## 🚀 下一步

### 需要执行
```bash
# 安装依赖 (需要 sudo)
sudo apt install -y python3.12-venv

# 或使用 --break-system-packages
pip install --break-system-packages torch torchaudio
pip install --break-system-packages -e /tmp/moss-tts-nano
```

### 或使用 Docker
```bash
docker run --rm -it openmoss/moss-tts-nano \
    --text "你好，这是测试。" \
    --output /tmp/speech.wav
```

---

## 📋 太一集成

**引擎封装**: `skills/07-system/moss-tts-nano/moss_tts_engine.py`

**使用示例**:
```python
from skills.07-system.moss-tts-nano.moss_tts_engine import MossTTSEngine

engine = MossTTSEngine()
engine.generate_speech(
    text="你好，这是 MOSS-TTS-Nano 的测试。",
    output_path="/tmp/speech.wav"
)
```

---

*MOSS-TTS-Nano 安装状态 · 太一 AGI · 2026-04-14 15:25*
