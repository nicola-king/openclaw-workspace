#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOSS-TTS-Nano 本地 TTS 引擎

特点:
- 仅 0.1B 参数
- CPU 运行 (无需 GPU)
- 多语言支持
- 实时语音生成
- 轻量级集成

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
from pathlib import Path
from typing import Optional

# 尝试导入 moss-tts-nano
try:
    import torch
    from moss_tts_nano import MOSSTTSNano
    MOSS_AVAILABLE = True
except ImportError:
    MOSS_AVAILABLE = False
    print("⚠️ MOSS-TTS-Nano 未安装，使用备用方案")


class MossTTSEngine:
    """MOSS-TTS 引擎"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model = None
        self.available = MOSS_AVAILABLE
        
        if self.available:
            self.load_model()
    
    def load_model(self):
        """加载模型"""
        if not MOSS_AVAILABLE:
            return
        
        try:
            self.model = MOSSTTSNano.from_pretrained("openmoss/moss-tts-nano")
            print(f"✅ MOSS-TTS-Nano 模型已加载")
        except Exception as e:
            print(f"⚠️ 模型加载失败：{e}")
            self.available = False
    
    def generate_speech(self, text: str, output_path: str, voice: str = "default"):
        """生成语音"""
        if not self.available:
            print("❌ MOSS-TTS 不可用")
            return False
        
        try:
            # 生成语音
            audio = self.model.generate(text, voice=voice)
            
            # 保存
            self.model.save_audio(audio, output_path)
            
            print(f"✅ 语音生成成功：{output_path}")
            return True
        except Exception as e:
            print(f"❌ 语音生成失败：{e}")
            return False
    
    def list_voices(self):
        """列出可用声音"""
        if not self.available:
            return []
        
        try:
            return self.model.list_voices()
        except:
            return []


def main():
    """测试"""
    print("🎤 MOSS-TTS-Nano 测试")
    print("=" * 60)
    
    if not MOSS_AVAILABLE:
        print("⚠️ MOSS-TTS-Nano 未安装")
        print("\n安装命令:")
        print("  cd /tmp/moss-tts-nano")
        print("  pip install -r requirements.txt")
        print("  pip install -e .")
        return
    
    # 创建引擎
    engine = MossTTSEngine()
    
    # 列出声音
    voices = engine.list_voices()
    print(f"\n可用声音：{len(voices)} 个")
    for voice in voices[:5]:
        print(f"  - {voice}")
    
    # 测试生成
    test_text = "你好，这是 MOSS-TTS-Nano 的测试。"
    output_file = "/tmp/moss-tts-test.wav"
    
    print(f"\n测试生成：{test_text}")
    success = engine.generate_speech(test_text, output_file)
    
    if success:
        print(f"✅ 测试成功：{output_file}")
    else:
        print("❌ 测试失败")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
