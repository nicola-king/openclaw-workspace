#!/usr/bin/env python3
"""
太一 TTS 语音合成脚本
支持：Edge TTS (在线) + Piper TTS (离线)
"""

import asyncio
import subprocess
from pathlib import Path
from datetime import datetime

# 配置
VOICE = "zh-CN-XiaoxiaoNeural"  # Edge TTS 中文女声
PIPER_MODEL = Path.home() / ".local/share/piper/zh_CN-huayan-medium.onnx"  # Piper 中文模型
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "tts-output"

def synthesize_piper(text: str, output_path: str = None) -> str:
    """使用 Piper TTS (离线)"""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUT_DIR / f"taiyi_piper_{timestamp}.wav"
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = ["piper", "-m", str(PIPER_MODEL), "-f", str(output_path)]
    proc = subprocess.run(cmd, input=text.encode(), capture_output=True)
    
    if proc.returncode != 0:
        raise Exception(f"Piper TTS 失败：{proc.stderr.decode()}")
    
    return str(output_path)

async def synthesize_edge(text: str, output_path: str = None) -> str:
    """使用 Edge TTS (在线)"""
    import edge_tts
    
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUT_DIR / f"taiyi_edge_{timestamp}.wav"
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(output_path))
    
    return str(output_path)

def tts(text: str, output_path: str = None, offline: bool = False) -> str:
    """
    文本转语音
    
    Args:
        text: 要合成的文本
        output_path: 输出文件路径
        offline: True=使用 Piper (离线), False=使用 Edge (在线)
    
    Returns:
        输出文件路径
    """
    if offline and PIPER_MODEL.exists():
        return synthesize_piper(text, output_path)
    else:
        return asyncio.run(synthesize_edge(text, output_path))

if __name__ == "__main__":
    import sys
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 解析参数
    offline = "--offline" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--offline"]
    
    # 获取文本
    if len(args) > 0:
        text = " ".join(args)
    else:
        text = "你好，我是太一"
    
    # 选择引擎
    if offline and PIPER_MODEL.exists():
        engine = "Piper (离线)"
        output = synthesize_piper(text)
    else:
        engine = "Edge TTS (在线)"
        output = asyncio.run(synthesize_edge(text))
    
    print(f"✅ 语音已生成：{output}")
    print(f"📝 文本：{text}")
    print(f"🎙️ 引擎：{engine}")
    print(f"🎵 声音：{VOICE if not offline else 'zh_CN-huayan-medium'}")
