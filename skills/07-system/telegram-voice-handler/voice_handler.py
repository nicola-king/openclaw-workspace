#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 语音消息自动识别

功能:
- 监听 Telegram 语音消息
- 自动下载语音文件
- STT 识别 (Whisper/Azure)
- 转文字后发送给太一处理

作者：太一 AGI
创建：2026-04-15
"""

import os
import sys
import logging
import asyncio
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
AUDIO_DIR = WORKSPACE / "audio" / "telegram"
LOG_DIR = WORKSPACE / "logs"

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_DIR / "telegram-voice.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TelegramVoiceHandler')


class TelegramVoiceHandler:
    """Telegram 语音处理器"""
    
    def __init__(self):
        self.audio_dir = AUDIO_DIR
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # 检测 STT 引擎
        self.whisper_available = self._check_whisper()
        self.azure_available = self._check_azure()
        
        # 优先使用 Whisper (免费本地)
        self.stt_engine = "whisper" if self.whisper_available else ("azure" if self.azure_available else None)
        
        logger.info(f"🎤 Telegram 语音处理器已初始化")
        logger.info(f"  STT 引擎：{self.stt_engine or '未配置'}")
        logger.info(f"  Whisper: {'✅' if self.whisper_available else '❌'}")
        logger.info(f"  Azure: {'✅' if self.azure_available else '❌'}")
    
    def _check_whisper(self) -> bool:
        """检查 Whisper 是否可用"""
        try:
            import whisper
            return True
        except ImportError:
            return False
    
    def _check_azure(self) -> bool:
        """检查 Azure Speech 是否可用"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            # 检查是否有配置
            azure_key = os.getenv("AZURE_SPEECH_KEY")
            azure_region = os.getenv("AZURE_SPEECH_REGION")
            return bool(azure_key and azure_region)
        except ImportError:
            return False
    
    async def download_voice(self, file_id: str, output_path: Path) -> bool:
        """
        下载 Telegram 语音文件
        
        Args:
            file_id: Telegram 文件 ID
            output_path: 保存路径
        
        Returns:
            是否成功
        """
        try:
            from telegram import Bot
            
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            if not bot_token:
                logger.error("❌ TELEGRAM_BOT_TOKEN 未配置")
                return False
            
            bot = Bot(token=bot_token)
            file = await bot.get_file(file_id)
            
            # 下载到本地
            await file.download_to_drive(output_path)
            
            logger.info(f"✅ 语音下载成功：{output_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ 下载失败：{e}")
            return False
    
    def transcribe_with_whisper(self, audio_path: Path) -> Optional[str]:
        """使用 Whisper 识别"""
        try:
            import whisper
            
            logger.info(f"🎯 使用 Whisper 识别：{audio_path}")
            
            # 加载模型 (tiny 最快，large 最准)
            model = whisper.load_model("tiny")
            
            # 识别 (中文)
            result = model.transcribe(str(audio_path), language="zh")
            
            text = result["text"].strip()
            logger.info(f"✅ 识别结果：{text}")
            
            return text
        
        except Exception as e:
            logger.error(f"❌ Whisper 识别失败：{e}")
            return None
    
    def transcribe_with_azure(self, audio_path: Path) -> Optional[str]:
        """使用 Azure Speech 识别"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            logger.info(f"🎯 使用 Azure Speech 识别：{audio_path}")
            
            speech_key = os.getenv("AZURE_SPEECH_KEY")
            speech_region = os.getenv("AZURE_SPEECH_REGION")
            
            speech_config = speechsdk.SpeechConfig(
                subscription=speech_key,
                region=speech_region
            )
            speech_config.speech_recognition_language = "zh-CN"
            
            audio_config = speechsdk.AudioConfig(filename=str(audio_path))
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            result = recognizer.recognize_once_async().get()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                text = result.text.strip()
                logger.info(f"✅ 识别结果：{text}")
                return text
            else:
                logger.error(f"❌ Azure 识别失败：{result.reason}")
                return None
        
        except Exception as e:
            logger.error(f"❌ Azure 识别失败：{e}")
            return None
    
    def transcribe(self, audio_path: Path) -> Optional[str]:
        """
        语音识别 (自动选择引擎)
        
        Args:
            audio_path: 音频文件路径
        
        Returns:
            识别的文字
        """
        if self.stt_engine == "whisper":
            return self.transcribe_with_whisper(audio_path)
        elif self.stt_engine == "azure":
            return self.transcribe_with_azure(audio_path)
        else:
            logger.error("❌ 无可用 STT 引擎")
            return None
    
    async def process_voice_message(self, file_id: str, chat_id: str, message_id: int) -> Optional[str]:
        """
        处理语音消息
        
        Args:
            file_id: Telegram 文件 ID
            chat_id: 聊天 ID
            message_id: 消息 ID
        
        Returns:
            识别的文字
        """
        logger.info(f"🎤 开始处理语音消息：{file_id}")
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.audio_dir / f"voice_{timestamp}.ogg"
        
        # 下载语音
        if not await self.download_voice(file_id, output_path):
            return None
        
        # 识别语音
        text = self.transcribe(output_path)
        
        if text:
            logger.info(f"✅ 语音识别完成：{text}")
            return text
        else:
            logger.error("❌ 语音识别失败")
            return None
    
    def send_to_taiyi(self, text: str, chat_id: str) -> bool:
        """
        发送识别结果给太一处理
        
        Args:
            text: 识别的文字
            chat_id: 聊天 ID
        
        Returns:
            是否成功
        """
        try:
            # 通过 OpenClaw 发送消息
            cmd = [
                "openclaw", "message", "send",
                "--channel", "telegram",
                "--target", chat_id,
                "--message", f"🎤 语音识别结果：{text}"
            ]
            
            import subprocess
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"✅ 已发送给太一处理")
                return True
            else:
                logger.error(f"❌ 发送失败：{result.stderr.decode()}")
                return False
        
        except Exception as e:
            logger.error(f"❌ 发送失败：{e}")
            return False


async def main():
    """测试主函数"""
    logger.info("🎤 Telegram 语音处理器测试")
    print("=" * 60)
    
    handler = TelegramVoiceHandler()
    
    print(f"\nSTT 引擎：{handler.stt_engine}")
    print(f"Whisper 可用：{handler.whisper_available}")
    print(f"Azure 可用：{handler.azure_available}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("\n💡 使用方法:")
    print("1. 在 Telegram 中发送语音消息给 Bot")
    print("2. Bot 自动下载并识别")
    print("3. 识别结果发送给太一处理")


if __name__ == "__main__":
    asyncio.run(main())
