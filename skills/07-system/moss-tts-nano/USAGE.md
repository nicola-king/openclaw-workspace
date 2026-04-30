# 🎤 MOSS-TTS-Nano 智能自动化调用指南

> **更新时间**: 2026-04-14 15:26  
> **状态**: ✅ 已完成  
> **集成**: 太一 TTS 系统

---

## 🚀 快速开始

### 方法 1: 直接调用

```python
from skills.07-system.moss-tts-nano.moss_tts_auto_caller import MossTTSAutoCaller

caller = MossTTSAutoCaller()

# 生成语音
result = caller.generate_speech(
    text="你好，这是 MOSS-TTS-Nano 测试。",
    voice="default"
)

print(f"生成成功：{result}")
```

### 方法 2: 批量生成

```python
from skills.07-system.moss-tts-nano.moss_tts_auto_caller import MossTTSAutoCaller

caller = MossTTSAutoCaller()

# 批量生成
texts = [
    "第一条语音。",
    "第二条语音。",
    "第三条语音。",
]

results = caller.batch_generate(texts, prefix="batch")
print(f"生成 {len(results)} 个文件")
```

### 方法 3: 太一 TTS 系统 (推荐)

```python
from skills.07-system.taiyi-tts-system import TaiyiTTSSystem

tts = TaiyiTTSSystem()

# 智能生成 (自动选择最佳引擎)
result = tts.generate_speech("你好，这是太一 TTS 系统测试。")

# 为 Telegram 生成
result = tts.generate_for_telegram("这是 Telegram 语音消息。")

# 为微信生成
result = tts.generate_for_wechat("这是微信语音消息。")
```

---

## 📋 API 参考

### MossTTSAutoCaller

#### generate_speech()
```python
def generate_speech(
    text: str,
    output_name: Optional[str] = None,
    voice: str = "default",
    format: str = "wav"
) -> Optional[Path]
```

**参数**:
- `text`: 要转换的文本
- `output_name`: 输出文件名 (可选，自动生成)
- `voice`: 声音类型 (default/female_1/male_1/child_1)
- `format`: 输出格式 (wav/mp3)

**返回**: 输出文件路径

#### batch_generate()
```python
def batch_generate(
    texts: List[str],
    prefix: str = "batch"
) -> List[Path]
```

**参数**:
- `texts`: 文本列表
- `prefix`: 文件名前缀

**返回**: 文件路径列表

#### clone_voice()
```python
def clone_voice(
    reference_audio: Path,
    text: str,
    output_name: Optional[str] = None
) -> Optional[Path]
```

**参数**:
- `reference_audio`: 参考音频文件
- `text`: 要生成的文本
- `output_name`: 输出文件名

**返回**: 输出文件路径

---

### TaiyiTTSSystem

#### generate_speech()
```python
def generate_speech(
    text: str,
    engine: str = "auto",
    output_name: Optional[str] = None
) -> Optional[Path]
```

**参数**:
- `text`: 要转换的文本
- `engine`: 引擎选择 (auto/moss/other)
- `output_name`: 输出文件名

**返回**: 输出文件路径

#### generate_for_telegram()
```python
def generate_for_telegram(
    text: str,
    chat_id: str = "7073481596"
) -> Optional[Path]
```

**参数**:
- `text`: 文本内容
- `chat_id`: Telegram Chat ID

**返回**: 音频文件路径

#### generate_for_wechat()
```python
def generate_for_wechat(
    text: str
) -> Optional[Path]
```

**参数**:
- `text`: 文本内容

**返回**: 音频文件路径

---

## 🔧 命令行调用

### 直接 CLI
```bash
python3 /tmp/moss-tts-nano/moss_tts_nano/cli.py \
    --text "你好，这是测试。" \
    --output /tmp/speech.wav
```

### 自动化脚本
```bash
python3 /home/nicola/.openclaw/workspace/skills/07-system/moss-tts-nano/moss_tts_auto_caller.py
```

### 太一 TTS 系统
```bash
python3 /home/nicola/.openclaw/workspace/skills/07-system/taiyi-tts-system.py
```

---

## 📊 输出目录

**默认位置**: `/home/nicola/.openclaw/workspace/audio/moss-tts/`

**文件结构**:
```
audio/moss-tts/
├── moss_tts_20260414_152600.wav
├── batch_000.wav
├── batch_001.wav
├── batch_002.wav
├── telegram_7073481596_20260414_152700.wav
├── wechat_20260414_152800.wav
└── generation_log.json (生成日志)
```

---

## 🎯 使用场景

### 1. 视频配音
```python
caller = MossTTSAutoCaller()

script = [
    "欢迎观看本期视频。",
    "今天我们来聊聊 MOSS-TTS-Nano。",
    "这是一个非常强大的 TTS 模型。",
]

audio_files = caller.batch_generate(script, prefix="video_001")
```

### 2. Telegram 语音消息
```python
tts = TaiyiTTSSystem()

audio = tts.generate_for_telegram(
    "这是自动生成的语音消息。"
)

# 然后通过 Telegram Bot API 发送
```

### 3. 微信语音回复
```python
tts = TaiyiTTSSystem()

audio = tts.generate_for_wechat(
    "这是自动生成的微信语音回复。"
)
```

### 4. 语音克隆
```python
caller = MossTTSAutoCaller()

audio = caller.clone_voice(
    reference_audio=Path("/path/to/reference.wav"),
    text="这是用你的声音说的。",
    output_name="cloned_voice.wav"
)
```

---

## 📈 性能优化

### 批量生成
```python
# 推荐：批量生成比单个生成更高效
texts = [...] * 100  # 100 条文本
results = caller.batch_generate(texts, prefix="batch")
```

### 异步生成
```python
import asyncio

async def generate_async(texts):
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(
        None, 
        lambda: caller.batch_generate(texts)
    )
    return results
```

---

## 🔗 相关链接

- **MOSS-TTS-Nano**: https://github.com/openmoss/moss-tts-nano
- **太一 TTS 系统**: `skills/07-system/taiyi-tts-system.py`
- **自动化调用**: `skills/07-system/moss-tts-nano/moss_tts_auto_caller.py`

---

*MOSS-TTS-Nano 智能自动化调用指南 · 太一 AGI · 2026-04-14 15:26*
