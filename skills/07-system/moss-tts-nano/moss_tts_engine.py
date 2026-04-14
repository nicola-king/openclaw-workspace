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
import subprocess

try:
    # 检查 CLI 是否可用
    result = subprocess.run(
        ["python3", "/tmp/moss-tts-nano/moss_tts_nano/cli.py", "--help"],
        capture_output=True,
        timeout=10
    )
    MOSS_AVAILABLE = (result.returncode == 0)
except:
    MOSS_AVAILABLE = False


class MossTTSEngine:
    """MOSS-TTS 引擎 (CLI 方式)"""
    
    def __init__(self, moss_path: str = "/tmp/moss-tts-nano"):
        self.moss_path = Path(moss_path)
        self.cli_path = self.moss_path / "moss_tts_nano" / "cli.py"
        self.available = MOSS_AVAILABLE and self.cli_path.exists()
    
    def generate_speech(self, text: str, output_path: str, voice: str = "default"):
        """生成语音 (使用 CLI)"""
        if not self.available:
            print("❌ MOSS-TTS 不可用")
            return False
        
        try:
            # 使用 CLI 生成
            cmd = [
                "python3", str(self.cli_path),
                "--text", text,
                "--output", output_path,
            ]
            
            if voice != "default":
                cmd.extend(["--voice", voice])
            
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ 语音生成成功：{output_path}")
                return True
            else:
                print(f"❌ 语音生成失败：{result.stderr.decode()}")
                return False
        except Exception as e:
            print(f"❌ 语音生成失败：{e}")
            return False
    
    def list_voices(self):
        """列出可用声音"""
        if not self.available:
            return ["default", "female_1", "male_1"]
        
        # TODO: 从 CLI 获取
        return ["default", "female_1", "male_1"]


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
