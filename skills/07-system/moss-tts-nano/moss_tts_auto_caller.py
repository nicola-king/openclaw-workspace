#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOSS-TTS-Nano 智能自动化调用

功能:
1. 文本转语音自动化
2. 批量生成
3. 语音克隆
4. 与太一系统集成

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MOSS_PATH = Path("/tmp/moss-tts-nano")
CLI_PATH = MOSS_PATH / "moss_tts_nano" / "cli.py"
OUTPUT_DIR = WORKSPACE / "audio" / "moss-tts"

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class MossTTSAutoCaller:
    """MOSS-TTS 智能自动化调用器"""
    
    def __init__(self):
        self.cli_path = CLI_PATH
        self.output_dir = OUTPUT_DIR
        self.available = CLI_PATH.exists()
        
        if not self.available:
            print(f"⚠️ MOSS-TTS CLI 不存在：{CLI_PATH}")
    
    def generate_speech(self, text: str, output_name: Optional[str] = None, 
                       voice: str = "default", format: str = "wav") -> Optional[Path]:
        """
        智能生成语音
        
        Args:
            text: 要转换的文本
            output_name: 输出文件名 (可选，自动生成)
            voice: 声音类型 (default/female_1/male_1)
            format: 输出格式 (wav/mp3)
        
        Returns:
            输出文件路径，失败返回 None
        """
        if not self.available:
            print("❌ MOSS-TTS 不可用")
            return None
        
        # 自动生成文件名
        if not output_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"moss_tts_{timestamp}.{format}"
        
        output_path = self.output_dir / output_name
        
        # 构建命令
        cmd = [
            "python3", str(self.cli_path),
            "--text", text,
            "--output", str(output_path),
        ]
        
        if voice != "default":
            cmd.extend(["--voice", voice])
        
        if format == "mp3":
            cmd.extend(["--format", "mp3"])
        
        try:
            # 执行
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ 语音生成成功：{output_path}")
                self._log_generation(text, output_path, voice)
                return output_path
            else:
                print(f"❌ 语音生成失败：{result.stderr.decode()}")
                return None
        except subprocess.TimeoutExpired:
            print("❌ 生成超时")
            return None
        except Exception as e:
            print(f"❌ 生成失败：{e}")
            return None
    
    def batch_generate(self, texts: List[str], prefix: str = "batch") -> List[Path]:
        """
        批量生成语音
        
        Args:
            texts: 文本列表
            prefix: 文件名前缀
        
        Returns:
            生成的文件路径列表
        """
        results = []
        
        for i, text in enumerate(texts):
            output_name = f"{prefix}_{i:03d}.wav"
            result = self.generate_speech(text, output_name)
            if result:
                results.append(result)
        
        print(f"✅ 批量生成完成：{len(results)}/{len(texts)} 个")
        return results
    
    def clone_voice(self, reference_audio: Path, text: str, 
                   output_name: Optional[str] = None) -> Optional[Path]:
        """
        语音克隆
        
        Args:
            reference_audio: 参考音频文件
            text: 要生成的文本
            output_name: 输出文件名
        
        Returns:
            输出文件路径
        """
        if not reference_audio.exists():
            print(f"❌ 参考音频不存在：{reference_audio}")
            return None
        
        # 构建命令
        cmd = [
            "python3", str(self.cli_path),
            "--text", text,
            "--output", str(self.output_dir / (output_name or "cloned.wav")),
            "--reference", str(reference_audio),
            "--clone",
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=180)
            
            if result.returncode == 0:
                output_path = self.output_dir / (output_name or "cloned.wav")
                print(f"✅ 语音克隆成功：{output_path}")
                return output_path
            else:
                print(f"❌ 语音克隆失败：{result.stderr.decode()}")
                return None
        except Exception as e:
            print(f"❌ 克隆失败：{e}")
            return None
    
    def list_voices(self) -> List[str]:
        """列出可用声音"""
        return ["default", "female_1", "male_1", "child_1"]
    
    def _log_generation(self, text: str, output_path: Path, voice: str):
        """记录生成日志"""
        log_file = self.output_dir / "generation_log.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "text": text[:100],
            "output_path": str(output_path),
            "voice": voice,
            "duration_seconds": None,  # TODO: 从音频获取
        }
        
        # 读取现有日志
        logs = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        # 添加新日志
        logs.append(log_entry)
        
        # 保存
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)


def main():
    """测试"""
    print("🎤 MOSS-TTS-Nano 智能自动化调用测试")
    print("=" * 60)
    
    caller = MossTTSAutoCaller()
    
    # 测试 1: 单文本生成
    print("\n📝 测试 1: 单文本生成")
    result = caller.generate_speech(
        text="你好，这是 MOSS-TTS-Nano 智能自动化调用测试。",
        voice="default"
    )
    if result:
        print(f"✅ 生成成功：{result}")
    
    # 测试 2: 批量生成
    print("\n📦 测试 2: 批量生成")
    texts = [
        "第一条测试语音。",
        "第二条测试语音。",
        "第三条测试语音。",
    ]
    results = caller.batch_generate(texts, prefix="test_batch")
    print(f"✅ 生成 {len(results)} 个文件")
    
    # 测试 3: 列出声音
    print("\n🎵 测试 3: 可用声音")
    voices = caller.list_voices()
    for voice in voices:
        print(f"  - {voice}")
    
    # 测试 4: 查看日志
    print("\n📊 测试 4: 生成日志")
    log_file = OUTPUT_DIR / "generation_log.json"
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
            print(f"  总记录：{len(logs)} 条")
            if logs:
                print(f"  最新：{logs[-1]['timestamp']}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")


if __name__ == "__main__":
    main()
