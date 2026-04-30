#!/usr/bin/env python3
"""
太一 AGI - 本地声音克隆技能 (Coqui XTTS v2)
基于工控机 CPU 优化版本

硬件要求:
- 内存：8GB+ (推荐 16GB+)
- 存储：5GB+ 可用空间
- CPU: 4 核+ (支持 AVX2)

太一工控机配置:
- CPU: Intel N150 (4 核)
- 内存：32GB ✅
- 存储：1.8TB ✅
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 检查工作目录
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
VOICE_DIR = WORKSPACE / "voices"
OUTPUT_DIR = WORKSPACE / "audio"

# 确保目录存在
VOICE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


class LocalVoiceCloning:
    """本地声音克隆服务 (XTTS v2)"""
    
    def __init__(self):
        self.model = None
        self.speaker_wav = None
        self.language = "zh-cn"
        
    def setup(self):
        """安装依赖和下载模型"""
        print("🔧 正在安装依赖...")
        
        # 安装 Coqui TTS
        import subprocess
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-q",
            "TTS>=0.22.0",
            "torch>=2.0.0",
            "torchaudio"
        ])
        
        print("✅ 依赖安装完成")
        
        # 下载 XTTS v2 模型
        print("📥 正在下载 XTTS v2 模型 (约 2GB)...")
        from TTS.api import TTS
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print("✅ 模型下载完成")
        
    def clone_voice(self, name, audio_file, description=""):
        """克隆声音
        
        Args:
            name: 声音名称
            audio_file: 样本音频文件路径 (MP3/WAV)
            description: 声音描述 (可选)
        
        Returns:
            voice_config: 声音配置字典
        """
        print(f"🎙️ 正在克隆声音：{name}")
        print(f"样本文件：{audio_file}")
        
        # 验证音频文件
        if not Path(audio_file).exists():
            print(f"❌ 文件不存在：{audio_file}")
            return None
        
        # 保存声音配置
        voice_config = {
            "name": name,
            "speaker_wav": str(audio_file),
            "language": self.language,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "model": "xtts_v2"
        }
        
        # 保存到配置文件
        config_file = VOICE_DIR / f"{name}.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(voice_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 声音克隆成功：{name}")
        print(f"配置文件：{config_file}")
        
        return voice_config
    
    def text_to_speech(self, text, voice_name, output_file=None):
        """文本转语音 (使用克隆的声音)
        
        Args:
            text: 要转换的文本
            voice_name: 声音名称
            output_file: 输出文件路径
        
        Returns:
            output_file: 生成的音频文件路径
        """
        print(f"🔊 正在生成语音：{text[:50]}...")
        
        # 加载声音配置
        config_file = VOICE_DIR / f"{voice_name}.json"
        if not config_file.exists():
            print(f"❌ 声音配置不存在：{voice_name}")
            return None
        
        with open(config_file, "r", encoding="utf-8") as f:
            voice_config = json.load(f)
        
        # 生成输出文件名
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = OUTPUT_DIR / f"{voice_name}_{timestamp}.wav"
        else:
            output_file = Path(output_file)
        
        # 确保输出目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载模型 (如果未加载)
        if self.model is None:
            print("📥 正在加载模型...")
            from TTS.api import TTS
            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        
        # 生成语音
        print(f"⏳ 生成中... (CPU 推理约需 30-60 秒)")
        self.model.tts_to_file(
            text=text,
            speaker_wav=voice_config["speaker_wav"],
            language=voice_config["language"],
            file_path=str(output_file)
        )
        
        print(f"✅ 语音生成成功：{output_file}")
        return str(output_file)
    
    def list_voices(self):
        """列出所有克隆的声音"""
        voices = []
        for config_file in VOICE_DIR.glob("*.json"):
            with open(config_file, "r", encoding="utf-8") as f:
                voice_config = json.load(f)
                voices.append(voice_config)
        return voices
    
    def get_model_info(self):
        """获取模型信息"""
        return {
            "model": "XTTS v2",
            "provider": "Coqui AI",
            "languages": ["zh-cn", "en", "ja", "ko", "de", "fr", "es", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "hu"],
            "min_sample_duration": "3 秒",
            "recommended_sample_duration": "10-30 秒",
            "model_size": "~2GB",
            "ram_usage": "~4GB",
            "cpu_inference_speed": "0.5-1x 实时"
        }


def show_help():
    """显示帮助信息"""
    print("=" * 60)
    print("🎙️ 太一 AGI - 本地声音克隆技能")
    print("=" * 60)
    print()
    print("命令:")
    print("  setup          - 安装依赖和模型")
    print("  clone <name> <audio_file> - 克隆声音")
    print("  speak <voice_name> <text> - 文本转语音")
    print("  list           - 列出所有声音")
    print("  info           - 显示模型信息")
    print()
    print("示例:")
    print("  # 1. 安装 (首次运行)")
    print("  python3 local_voice_cloning.py setup")
    print()
    print("  # 2. 克隆声音 (准备 30 秒清晰录音)")
    print("  python3 local_voice_cloning.py clone 我的声音 sample.wav")
    print()
    print("  # 3. 生成语音")
    print("  python3 local_voice_cloning.py speak 我的声音 '你好，这是用我的声音生成的语音'")
    print()
    print("音频样本要求:")
    print("  - 时长：30 秒 -5 分钟 (推荐 1 分钟)")
    print("  - 格式：MP3, WAV, M4A")
    print("  - 质量：清晰、无背景噪音")
    print("  - 内容：自然说话、多种语调")
    print()
    print("=" * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    cloner = LocalVoiceCloning()
    
    if command == "setup":
        cloner.setup()
        
    elif command == "clone":
        if len(sys.argv) < 4:
            print("❌ 用法：clone <声音名称> <音频文件>")
            return
        name = sys.argv[2]
        audio_file = sys.argv[3]
        cloner.clone_voice(name, audio_file)
        
    elif command == "speak":
        if len(sys.argv) < 4:
            print("❌ 用法：speak <声音名称> <文本>")
            return
        voice_name = sys.argv[2]
        text = " ".join(sys.argv[3:])
        cloner.text_to_speech(text, voice_name)
        
    elif command == "list":
        voices = cloner.list_voices()
        if voices:
            print(f"\n📋 已克隆的声音 ({len(voices)}个):")
            for voice in voices:
                print(f"\n  名称：{voice['name']}")
                print(f"  语言：{voice['language']}")
                print(f"  创建时间：{voice['created_at']}")
                print(f"  样本：{voice['speaker_wav']}")
        else:
            print("\n⚠️  暂无克隆的声音")
            print("使用 'clone' 命令克隆第一个声音")
        
    elif command == "info":
        info = cloner.get_model_info()
        print("\n📊 XTTS v2 模型信息:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
    elif command in ["help", "--help", "-h"]:
        show_help()
        
    else:
        print(f"❌ 未知命令：{command}")
        show_help()


if __name__ == "__main__":
    main()
