#!/usr/bin/env python3
"""
Gemini 3.1 Flash TTS 技能
太一 AGI · 2026-04-17

功能:
- 70+ 语言语音生成
- 200+ 音频标签控制
- 多说话人对话
- 情感/语速/音调控制
- 高保真语音输出
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# 尝试导入 google.genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
    print("✅ google-genai 已加载")
except ImportError as e:
    GENAI_AVAILABLE = False
    print(f"⚠️  google-genai 未安装：{e}")
    print("请运行：pip install google-genai")

import json


class GeminiTTS:
    """Gemini TTS 语音生成类"""
    
    def __init__(self, api_key=None):
        """初始化 TTS 客户端
        
        Args:
            api_key: Google AI API 密钥，默认从配置文件读取
        """
        # 优先级：参数 > 环境变量 > 配置文件
        if api_key:
            self.api_key = api_key
        elif os.getenv("GEMINI_API_KEY"):
            self.api_key = os.getenv("GEMINI_API_KEY")
        else:
            # 从太一记忆库配置文件读取
            config_file = Path("/home/nicola/.openclaw/workspace/config/feishu/config.json")
            if config_file.exists():
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.api_key = config.get("gemini_api_key", "")
            else:
                self.api_key = ""
        
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY 未配置！\n"
                "请运行：export GEMINI_API_KEY='你的密钥'\n"
                "或访问：https://aistudio.google.com/apikey"
            )
        
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai 库未安装")
        
        # 初始化客户端
        self.client = genai.Client(api_key=self.api_key)
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.audio_dir = self.workspace / "audio"
        self.audio_dir.mkdir(exist_ok=True)
        
        # 默认配置
        self.default_voice = "Zephyr"
        self.default_language = "zh-CN"
    
    def generate_speech(self, text, voice=None, language=None, 
                       speed=None, pitch=None, emotion=None, 
                       volume=None, output_file=None):
        """生成语音
        
        Args:
            text: 要转换的文本
            voice: 语音名称 (Zephyr, Puck, Charon, Kore, Fenrir, Aoede)
            language: 语言代码 (zh-CN, en-US, ja-JP, etc.)
            speed: 语速 (0.8-1.2)
            pitch: 音调 (low, normal, high)
            emotion: 情感 (happy, sad, angry, excited, calm, serious)
            volume: 音量 (soft, normal, loud)
            output_file: 输出文件名
        
        Returns:
            输出文件路径
        """
        voice = voice or self.default_voice
        language = language or self.default_language
        
        # 构建带标签的文本
        tagged_text = ""
        if speed:
            tagged_text += f"<speed={speed}>"
        if pitch:
            tagged_text += f"<pitch={pitch}>"
        if emotion:
            tagged_text += f"<emotion={emotion}>"
        if volume:
            tagged_text += f"<volume={volume}>"
        tagged_text += text
        
        # 生成文件名
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"speech_{timestamp}.wav"
        
        output_path = self.audio_dir / output_file
        
        try:
            # 调用 API (使用 models.generate_content 配合 response_modalities)
            # 注意：TTS 功能可能需要特定的模型和配置
            import httpx
            # 创建不带代理的 http 客户端
            http_client = httpx.Client(
                timeout=60.0,
                limits=httpx.Limits(max_connections=1)
            )
            
            response = self.client.models.generate_content(
                model="gemini-3.1-flash-tts",
                contents=tagged_text,
                config=types.GenerateContentConfig(
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice
                            )
                        ),
                        language_code=language
                    ),
                    response_modalities=["AUDIO"]
                ),
                http_options=types.HttpOptions(
                    http_client=http_client
                )
            )
            
            # 保存音频文件
            if hasattr(response, 'audio') and response.audio:
                with open(output_path, "wb") as f:
                    f.write(response.audio)
                print(f"✅ 语音生成成功：{output_path}")
                return str(output_path)
            else:
                # 如果没有音频输出，保存文本响应
                print(f"⚠️  未生成音频，保存文本响应")
                with open(output_path.with_suffix('.txt'), "w", encoding="utf-8") as f:
                    f.write(response.text if hasattr(response, 'text') else str(response))
                return str(output_path.with_suffix('.txt'))
            
        except Exception as e:
            print(f"❌ 语音生成失败：{e}")
            # 降级：保存文本到文件
            output_txt = output_path.with_suffix('.txt')
            with open(output_txt, "w", encoding="utf-8") as f:
                f.write(f"文本：{tagged_text}\n错误：{e}")
            print(f"📝 已保存文本：{output_txt}")
            return str(output_txt)
    
    def speak(self, text, output_file=None):
        """简单语音播报
        
        Args:
            text: 要播报的文本
            output_file: 输出文件名
        
        Returns:
            输出文件路径
        """
        return self.generate_speech(text, output_file=output_file)
    
    def speak_with_emotion(self, text, emotion="happy", speed=1.0, output_file=None):
        """带情感的语音播报
        
        Args:
            text: 要播报的文本
            emotion: 情感 (happy, sad, angry, excited, calm, serious)
            speed: 语速 (0.8-1.2)
            output_file: 输出文件名
        
        Returns:
            输出文件路径
        """
        return self.generate_speech(
            text, 
            emotion=emotion, 
            speed=speed,
            output_file=output_file
        )
    
    def speak_urgent(self, text, volume="loud", output_file=None):
        """紧急告警播报
        
        Args:
            text: 要播报的文本
            volume: 音量 (soft, normal, loud)
            output_file: 输出文件名
        
        Returns:
            输出文件路径
        """
        return self.generate_speech(
            text,
            emotion="serious",
            volume=volume,
            output_file=output_file
        )
    
    def generate_daily_report(self, report_file, output_file=None):
        """生成日报语音摘要
        
        Args:
            report_file: 日报 MD 文件路径
            output_file: 输出文件名
        
        Returns:
            输出文件路径
        """
        report_path = Path(report_file)
        if not report_path.exists():
            print(f"❌ 报告文件不存在：{report_path}")
            return None
        
        # 读取报告内容
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取关键信息 (简化处理)
        lines = content.split("\n")
        summary = []
        for line in lines[:20]:  # 取前 20 行
            if line.strip() and not line.startswith("#"):
                summary.append(line.strip())
        
        text = "日报摘要：" + "。".join(summary[:5])
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d")
            output_file = f"daily-report-{timestamp}.mp3"
        
        return self.generate_speech(text, output_file=output_file)


def main():
    """测试函数"""
    print("🎙️ Gemini 3.1 Flash TTS 测试")
    print("=" * 50)
    
    # 检查 google-genai
    if not GENAI_AVAILABLE:
        print("❌ google-genai 未安装")
        print("\n请运行:")
        print("  pip install google-genai")
        return
    
    # 检查 API 密钥
    print("\n🔑 检查 API 密钥...")
    try:
        tts = GeminiTTS()
        print("✅ API 密钥已配置")
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    try:
        # 测试简单播报
        print("\n📝 测试 1: 简单播报")
        output = tts.speak("你好，欢迎使用太一 AGI 系统！")
        print(f"   输出：{output}")
        
        # 测试带情感播报
        print("\n📝 测试 2: 带情感播报")
        output = tts.speak_with_emotion(
            "早安，今天是美好的一天！",
            emotion="happy",
            speed=0.9
        )
        print(f"   输出：{output}")
        
        # 测试紧急播报
        print("\n📝 测试 3: 紧急播报")
        output = tts.speak_urgent("警告：系统检测到异常！")
        print(f"   输出：{output}")
        
        print("\n✅ 所有测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
