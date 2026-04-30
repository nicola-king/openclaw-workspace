#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS 语音播报脚本 (离线版)
工具：pyttsx3 (完全离线免费)
场景：重大收益/止损提醒/每日简报
无需网络，完全离线！
"""

import os
import logging
import pyttsx3
from datetime import datetime

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/tts-offline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TTSOffline')

# 配置
CONFIG = {
    'telegram_bot_token': '8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY',
    'telegram_chat_id': '7073481596',
    'output_dir': '/home/nicola/.openclaw/workspace/audio/tts-offline',
    'rate': 150,  # 语速 (50-300)
    'volume': 1.0,  # 音量 (0.0-1.0)
    'voice_zh': None,  # 中文语音 (自动选择)
}

# 确保输出目录存在
os.makedirs(CONFIG['output_dir'], exist_ok=True)

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', CONFIG['rate'])
        self.engine.setProperty('volume', CONFIG['volume'])
        
        # 尝试设置中文语音
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'zh' in voice.languages or 'chinese' in voice.name.lower():
                CONFIG['voice_zh'] = voice.id
                logger.info(f"✅ 找到中文语音：{voice.name}")
                break
        
        if CONFIG['voice_zh']:
            self.engine.setProperty('voice', CONFIG['voice_zh'])
    
    def save_to_file(self, text, output_path):
        """保存语音到文件"""
        self.engine.save_to_file(text, output_path)
        self.engine.runAndWait()
        logger.info(f"✅ TTS 音频生成成功：{output_path}")
        return output_path
    
    def speak(self, text):
        """直接播放语音"""
        self.engine.say(text)
        self.engine.runAndWait()

# 全局引擎
tts_engine = None

def get_engine():
    """获取 TTS 引擎 (单例)"""
    global tts_engine
    if tts_engine is None:
        tts_engine = TTSEngine()
    return tts_engine

def generate_tts_audio(text, output_filename):
    """生成 TTS 语音"""
    engine = get_engine()
    output_path = os.path.join(CONFIG['output_dir'], output_filename)
    
    try:
        engine.save_to_file(text, output_path)
        return output_path
    except Exception as e:
        logger.error(f"TTS 生成失败：{e}")
        return None

def send_telegram_voice(chat_id, audio_path, caption):
    """发送 Telegram 语音消息"""
    import requests
    
    url = f"https://api.telegram.org/bot{CONFIG['telegram_bot_token']}/sendVoice"
    
    try:
        with open(audio_path, 'rb') as f:
            files = {'voice': f}
            data = {'chat_id': chat_id, 'caption': caption}
            response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                logger.info("✅ Telegram 语音发送成功")
                return True
            else:
                logger.error(f"Telegram 语音发送失败：{response.text}")
                return False
    except Exception as e:
        logger.error(f"Telegram 语音发送异常：{e}")
        return False

def celebrate_profit(pnl_pct, pnl_amount):
    """重大收益庆祝语音"""
    text = f"""太一向您报告！

今日交易收益为正百分之{pnl_pct:.1f}，
盈利{pnl_amount:.2f}美元。

策略运行正常，继续保持！

太一，AGI 执行总管。"""
    
    output_filename = f"profit_celebration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    audio_path = generate_tts_audio(text, output_filename)
    
    if audio_path:
        caption = f"🎉 收益庆祝：+${pnl_amount:.2f} (+{pnl_pct:.2f}%)"
        send_telegram_voice(CONFIG['telegram_chat_id'], audio_path, caption)

def alert_stop_loss(market_name, pnl_pct):
    """止损提醒语音"""
    text = f"""太一紧急提醒！

市场{market_name}触发止损，
当前亏损百分之{abs(pnl_pct*100):.1f}。

已自动平仓，请确认。

太一，AGI 执行总管。"""
    
    output_filename = f"stop_loss_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    audio_path = generate_tts_audio(text, output_filename)
    
    if audio_path:
        caption = f"⚠️ 止损提醒：{market_name} ({pnl_pct*100:.2f}%)"
        send_telegram_voice(CONFIG['telegram_chat_id'], audio_path, caption)

def test_tts():
    """测试 TTS 功能"""
    logger.info("🚀 离线 TTS 测试...")
    
    text = "你好，SAYELF！太一离线 TTS 语音功能已就绪。使用 pyttsx3 完全离线方案。"
    output_filename = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    audio_path = generate_tts_audio(text, output_filename)
    
    if audio_path:
        logger.info("✅ 离线 TTS 测试成功！")
        logger.info(f"音频文件：{audio_path}")
        return True
    else:
        logger.error("❌ 离线 TTS 测试失败")
        return False

def main():
    """主函数"""
    success = test_tts()
    
    if success:
        logger.info("\n✅ pyttsx3 离线 TTS 配置完成！")
        logger.info("\n特点:")
        logger.info("- 完全离线，无需网络")
        logger.info("- 无需 API Key，完全免费")
        logger.info("- 适合隐私敏感场景")
        logger.info("\n使用说明:")
        logger.info("1. 重大收益：celebrate_profit(pnl_pct, pnl_amount)")
        logger.info("2. 止损提醒：alert_stop_loss(market_name, pnl_pct)")

if __name__ == '__main__':
    main()
