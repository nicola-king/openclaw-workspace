#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一 TTS 系统 - MOSS-TTS-Nano 集成

功能:
1. 统一 TTS 接口
2. 智能路由 (MOSS/其他 TTS)
3. 自动化调用
4. 与 Telegram/微信集成

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
from pathlib import Path
from typing import Optional
import subprocess

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
AUDIO_DIR = WORKSPACE / "audio"
MOSS_CLI = Path("/tmp/moss-tts-nano/moss_tts_nano/cli.py")


class TaiyiTTSSystem:
    """太一 TTS 系统"""
    
    def __init__(self):
        self.audio_dir = AUDIO_DIR
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # 检测可用 TTS 引擎
        self.moss_available = MOSS_CLI.exists()
        
        print(f"🎤 太一 TTS 系统初始化")
        print(f"  MOSS-TTS-Nano: {'✅ 可用' if self.moss_available else '❌ 不可用'}")
    
    def generate_speech(self, text: str, engine: str = "auto", 
                       output_name: Optional[str] = None) -> Optional[Path]:
        """
        智能生成语音
        
        Args:
            text: 要转换的文本
            engine: 引擎选择 (auto/moss/other)
            output_name: 输出文件名
        
        Returns:
            输出文件路径
        """
        # 智能路由
        if engine == "auto":
            engine = "moss" if self.moss_available else "other"
        
        print(f"🎯 使用引擎：{engine}")
        
        if engine == "moss":
            return self._generate_with_moss(text, output_name)
        else:
            return self._generate_with_other(text, output_name)
    
    def _generate_with_moss(self, text: str, output_name: Optional[str] = None) -> Optional[Path]:
        """使用 MOSS-TTS-Nano 生成"""
        if not self.moss_available:
            print("❌ MOSS-TTS 不可用")
            return None
        
        import datetime
        if not output_name:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"tts_{timestamp}.wav"
        
        output_path = self.audio_dir / output_name
        
        # 构建命令
        cmd = [
            "python3", str(MOSS_CLI),
            "--text", text,
            "--output", str(output_path),
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ MOSS 生成成功：{output_path}")
                return output_path
            else:
                print(f"❌ MOSS 生成失败：{result.stderr.decode()}")
                return None
        except Exception as e:
            print(f"❌ MOSS 生成失败：{e}")
            return None
    
    def _generate_with_other(self, text: str, output_name: Optional[str] = None) -> Optional[Path]:
        """使用其他 TTS 引擎 (备用)"""
        print("⚠️ 使用备用 TTS 引擎")
        # TODO: 集成其他 TTS (如 Edge TTS, Google TTS 等)
        return None
    
    def generate_for_telegram(self, text: str, chat_id: str = "7073481596") -> Optional[Path]:
        """
        为 Telegram 生成语音
        
        Args:
            text: 文本内容
            chat_id: Telegram Chat ID
        
        Returns:
            音频文件路径
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"telegram_{chat_id}_{timestamp}.wav"
        
        return self.generate_speech(text, engine="auto", output_name=output_name)
    
    def generate_for_wechat(self, text: str) -> Optional[Path]:
        """
        为微信生成语音
        
        Args:
            text: 文本内容
        
        Returns:
            音频文件路径
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"wechat_{timestamp}.wav"
        
        return self.generate_speech(text, engine="auto", output_name=output_name)


def main():
    """测试"""
    print("🎤 太一 TTS 系统测试")
    print("=" * 60)
    
    tts = TaiyiTTSSystem()
    
    # 测试 1: 智能生成
    print("\n📝 测试 1: 智能生成")
    result = tts.generate_speech("你好，这是太一 TTS 系统测试。")
    if result:
        print(f"✅ 生成成功：{result}")
    
    # 测试 2: Telegram 生成
    print("\n📱 测试 2: Telegram 生成")
    result = tts.generate_for_telegram("这是 Telegram 语音消息。")
    if result:
        print(f"✅ 生成成功：{result}")
    
    # 测试 3: 微信生成
    print("\n💬 测试 3: 微信生成")
    result = tts.generate_for_wechat("这是微信语音消息。")
    if result:
        print(f"✅ 生成成功：{result}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")


if __name__ == "__main__":
    main()
