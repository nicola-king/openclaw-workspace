---
name: tts-alternatives
version: 1.0.0
description: tts-alternatives skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# TTS 开源替代方案 (免费/离线/无需 API Key)

> 微软 VibeVoice 替代方案 | 完全免费开源 | 2026-04-02 创建

---

## 🎯 最佳免费开源 TTS 推荐

### 首推：Piper TTS ⭐⭐⭐⭐⭐

**GitHub**: https://github.com/rhasspy/piper  
**许可证**: MIT  
**状态**: ✅ 活跃维护

**核心优势**:
| 特性 | 说明 |
|------|------|
| **超轻量** | CPU 即可运行，无需 GPU |
| **超快速** | 实时合成，延迟<100ms |
| **离线** | 完全本地运行，无需联网 |
| **多语言** | 支持 30+ 种语言 (含中文) |
| **高质量** | 接近神经 TTS 质量 |
| **免费** | 完全免费，无限制 |

**安装**:
```bash
# 1. 安装 piper-tts
pip install piper-tts

# 2. 下载中文语音模型
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/zh_CN-Xiaoxiao-medium.tar.gz
tar -xzf zh_CN-Xiaoxiao-medium.tar.gz

# 3. 测试
echo "你好，我是太一" | piper --model zh_CN-Xiaoxiao-medium.onnx --output_file output.wav
```

**太一集成脚本**:
```python
# scripts/piper-tts.py
import subprocess
from pathlib import Path

class PiperTTS:
    def __init__(self, model_path="zh_CN-Xiaoxiao-medium.onnx"):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"模型文件不存在：{self.model_path}")
    
    def synthesize(self, text, output_path="output.wav"):
        """文本转语音"""
        cmd = [
            "piper",
            "--model", str(self.model_path),
            "--output_file", output_path
        ]
        proc = subprocess.run(cmd, input=text.encode(), capture_output=True)
        if proc.returncode != 0:
            raise Exception(f"TTS 失败：{proc.stderr.decode()}")
        return output_path
```

---

### 备选 1：Edge TTS (微软 Edge 浏览器引擎) ⭐⭐⭐⭐

**GitHub**: https://github.com/rany2/edge-tts  
**许可证**: MIT  
**状态**: ✅ 活跃维护

**核心优势**:
| 特性 | 说明 |
|------|------|
| **免费** | 无需 Azure API Key |
| **高质量** | 使用微软 Edge 在线 TTS |
| **多声音** | 400+ 种声音可选 |
| **简单** | 一行命令即可使用 |
| **缺点** | 需要联网 (调用 Edge 服务) |

**安装**:
```bash
# 1. 安装
pip install edge-tts

# 2. 查看可用声音
edge-tts --list-voices | grep zh-CN

# 3. 测试
edge-tts --voice zh-CN-XiaoxiaoNeural --text "你好，我是太一" --write-media output.wav
```

**太一集成脚本**:
```python
# scripts/edge-tts.py
import asyncio
import edge_tts

class EdgeTTS:
    def __init__(self, voice="zh-CN-XiaoxiaoNeural"):
        self.voice = voice
    
    async def synthesize_async(self, text, output_path="output.wav"):
        """文本转语音 (异步)"""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        return output_path
    
    def synthesize(self, text, output_path="output.wav"):
        """文本转语音 (同步)"""
        asyncio.run(self.synthesize_async(text, output_path))
        return output_path
```

---

### 备选 2：Coqui TTS (深度学习) ⭐⭐⭐⭐

**GitHub**: https://github.com/coqui-ai/TTS  
**许可证**: MPL-2.0  
**状态**: 🟡 维护放缓 (但可用)

**核心优势**:
| 特性 | 说明 |
|------|------|
| **深度学习** | 基于 Tacotron2/GlowTTS |
| **多语言** | 支持 100+ 种语言 |
| **声音克隆** | 支持自定义声音 |
| **高质量** | 接近真人发音 |
| **缺点** | 需要 GPU，安装复杂 |

**安装**:
```bash
# 1. 安装
pip install TTS

# 2. 查看可用模型
tts --list_models

# 3. 测试 (中文)
tts --text "你好，我是太一" --model_name tts_models/zh-CN/baker/tacotron2-DDC --out_path output.wav
```

---

### 备选 3：Sherpa-ONNX (Next-gen Kaldi) ⭐⭐⭐⭐

**GitHub**: https://github.com/k2-fsa/sherpa-onnx  
**许可证**: Apache-2.0  
**状态**: ✅ 活跃维护

**核心优势**:
| 特性 | 说明 |
|------|------|
| **下一代 Kaldi** | 最新语音技术 |
| **TTS + ASR** | 语音合成 + 识别 |
| **跨平台** | 支持 Linux/Mac/Windows/Android/iOS |
| **离线** | 完全本地运行 |
| **中文优化** | 针对中文优化 |

**安装**:
```bash
# 1. 安装
pip install sherpa-onnx

# 2. 下载中文模型
# https://github.com/k2-fsa/sherpa-onnx/releases

# 3. 测试
python -m sherpa_onnx --text "你好，我是太一" --output output.wav
```

---

### 备选 4：Mimic 3 (Mycroft AI) ⭐⭐⭐

**GitHub**: https://github.com/MycroftAI/mimic3  
**许可证**: AGPL-3.0  
**状态**: ✅ 活跃维护

**核心优势**:
| 特性 | 说明 |
|------|------|
| **Mycroft 官方** | Mycroft AI 官方 TTS |
| **快速** | 实时合成 |
| **离线** | 完全本地运行 |
| **缺点** | 中文支持较弱 |

---

## 📊 全面对比

| 方案 | 质量 | 速度 | 离线 | 中文 | 安装难度 | 推荐度 |
|------|------|------|------|------|---------|--------|
| **Piper TTS** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ | 简单 | ⭐⭐⭐⭐⭐ |
| **Edge TTS** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ✅ | 超简单 | ⭐⭐⭐⭐ |
| **Coqui TTS** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ✅ | 复杂 | ⭐⭐⭐⭐ |
| **Sherpa-ONNX** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ | 中等 | ⭐⭐⭐⭐ |
| **Mimic 3** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | 🟡 | 中等 | ⭐⭐⭐ |
| **VibeVoice** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ✅ | 复杂 | ⭐⭐⭐⭐ |
| **Azure Speech** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ✅ | 简单 | ⭐⭐⭐⭐ |

---

## 🎯 太一推荐方案

### 最佳选择：Piper TTS

**理由**:
1. ✅ 完全免费开源 (MIT 许可证)
2. ✅ CPU 即可运行 (无需 GPU)
3. ✅ 完全离线 (隐私保护)
4. ✅ 中文支持良好
5. ✅ 安装简单 (pip 一行)
6. ✅ 速度快 (<100ms 延迟)
7. ✅ 质量接近神经 TTS

**适用场景**: 太一语音消息、日常 TTS 需求

---

### 备选方案：Edge TTS

**理由**:
1. ✅ 免费 (无需 API Key)
2. ✅ 质量最佳 (微软 Edge 引擎)
3. ✅ 安装最简单
4. ❌ 需要联网

**适用场景**: 高质量需求、可接受联网

---

## 🛠️ 快速安装指南 (Piper TTS)

### 5 分钟快速开始

```bash
# 1. 安装 piper-tts (1 分钟)
pip install piper-tts

# 2. 下载中文语音模型 (2 分钟)
mkdir -p ~/.local/share/piper
cd ~/.local/share/piper
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/zh/zh_CN/zh_CN-Xiaoxiao-medium/zh_CN-Xiaoxiao-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/zh/zh_CN/zh_CN/zh_CN-Xiaoxiao-medium/zh_CN-Xiaoxiao-medium.onnx.json

# 3. 测试 (1 分钟)
echo "你好，我是太一" | piper --model zh_CN-Xiaoxiao-medium.onnx --output_file test.wav

# 4. 播放测试
aplay test.wav  # Linux
# 或
ffplay test.wav  # 跨平台
```

### 太一集成 (1 分钟)

```python
# ~/.openclaw/workspace/scripts/taiyi-tts.py
#!/usr/bin/env python3
import subprocess
from pathlib import Path

def tts(text, output_path="output.wav"):
    """太一 TTS 快速合成"""
    model = Path.home() / ".local/share/piper/zh_CN-Xiaoxiao-medium.onnx"
    cmd = ["piper", "--model", str(model), "--output_file", output_path]
    subprocess.run(cmd, input=text.encode(), check=True)
    return output_path

if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "你好，我是太一"
    output = tts(text)
    print(f"✅ 语音已生成：{output}")
```

---

## 📋 中文语音模型推荐

### Piper TTS 中文声音

| 声音 | 性别 | 风格 | 模型大小 |
|------|------|------|---------|
| zh_CN-Xiaoxiao | 女 | 温暖、友好 | ~60MB |
| zh_CN-Yunxi | 男 | 阳光、专业 | ~60MB |
| zh_CN-Yunjian | 男 | 激情、运动 | ~60MB |

**下载链接**:
- 完整列表：https://huggingface.co/rhasspy/piper-voices/tree/main/zh/zh_CN
- 推荐：zh_CN-Xiaoxiao-medium (平衡质量和大小)

---

## 🚀 立即执行

### 方案 A: Piper TTS (推荐)

```bash
# 复制粘贴执行
pip install piper-tts && \
mkdir -p ~/.local/share/piper && \
cd ~/.local/share/piper && \
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/zh/zh_CN/zh_CN-Xiaoxiao-medium/zh_CN-Xiaoxiao-medium.onnx && \
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/zh/zh_CN/zh_CN-Xiaoxiao-medium/zh_CN-Xiaoxiao-medium.onnx.json && \
echo "你好，我是太一" | piper --model zh_CN-Xiaoxiao-medium.onnx --output_file test.wav && \
echo "✅ 安装完成！测试文件：test.wav"
```

### 方案 B: Edge TTS (最简单)

```bash
# 复制粘贴执行
pip install edge-tts && \
edge-tts --voice zh-CN-XiaoxiaoNeural --text "你好，我是太一" --write-media test.wav && \
echo "✅ 安装完成！测试文件：test.wav"
```

---

## 📝 记忆点

- **Piper TTS**: 首推，CPU 可用，离线，快速，免费
- **Edge TTS**: 质量最佳，需联网，无需 API Key
- **Coqui TTS**: 深度学习，高质量，需要 GPU
- **Sherpa-ONNX**: 下一代 Kaldi，TTS+ASR
- **中文推荐**: zh_CN-Xiaoxiao (女声，温暖友好)

---

*创建时间：2026-04-02 | 太一 AGI | TTS 开源替代方案 v1.0*
