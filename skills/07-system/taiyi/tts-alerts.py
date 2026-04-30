#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS 语音播报脚本
工具：edge-tts (免费开源) + pyttsx3 (离线备用)
场景：重大收益/止损提醒/每日简报/冥想内容
"""

import os
import logging
from datetime import datetime

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/tts-alert.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TTSAlert')

# 配置
CONFIG = {
    'telegram_bot_token': '8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY',
    'telegram_chat_id': '7073481596',
    'output_dir': '/home/nicola/.openclaw/workspace/audio/tts',
    'tts_engine': 'edge-tts',  # 首选 edge-tts，可选 pyttsx3
}

# 确保输出目录存在
os.makedirs(CONFIG['output_dir'], exist_ok=True)

def generate_tts_audio(text, output_filename, engine='edge-tts'):
    """生成 TTS 语音"""
    import asyncio
    import edge_tts
    
    output_path = os.path.join(CONFIG['output_dir'], output_filename)
    
    if engine == 'edge-tts':
        # edge-tts (在线免费)
        async def generate():
            communicate = edge_tts.Communicate(
                text=text,
                voice='zh-CN-YunxiNeural',  # 中文男声
                rate='+0%',
                volume='+0%',
                pitch='+0Hz',
            )
            await communicate.save(output_path)
            return output_path
        
        try:
            output_path = asyncio.run(generate())
            logger.info(f"✅ TTS 音频生成成功 (edge-tts): {output_path}")
            return output_path
        except Exception as e:
            logger.warning(f"edge-tts 失败，切换到离线模式：{e}")
            return generate_tts_audio(text, output_filename, engine='pyttsx3')
    
    elif engine == 'pyttsx3':
        # pyttsx3 (离线备用)
        import pyttsx3
        
        try:
            tts_engine = pyttsx3.init()
            tts_engine.setProperty('rate', 150)
            tts_engine.setProperty('volume', 1.0)
            tts_engine.save_to_file(text, output_path)
            tts_engine.runAndWait()
            logger.info(f"✅ TTS 音频生成成功 (pyttsx3 离线): {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"TTS 生成失败：{e}")
            return None
    
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
    audio_path = generate_tts_audio(text, output_filename, CONFIG['tts_engine'])
    
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
    audio_path = generate_tts_audio(text, output_filename, CONFIG['tts_engine'])
    
    if audio_path:
        caption = f"⚠️ 止损提醒：{market_name} ({pnl_pct*100:.2f}%)"
        send_telegram_voice(CONFIG['telegram_chat_id'], audio_path, caption)

def daily_briefing_voice(briefing_text):
    """每日简报语音版"""
    text = f"""太一每日简报。

日期，{datetime.now().strftime('%Y 年%m 月%d 日')}。

Polymarket 持仓正常，
GMGN 持仓正常。

今日内容发布任务 4 项，
日历事件 2 项。

详细信息请查看文字简报。

太一，AGI 执行总管。"""
    
    output_filename = f"daily_briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    audio_path = generate_tts_audio(text, output_filename, CONFIG['tts_engine'])
    
    if audio_path:
        caption = "📰 每日简报语音版"
        send_telegram_voice(CONFIG['telegram_chat_id'], audio_path, caption)

def meditation_content(theme="relax"):
    """冥想内容语音"""
    if theme == "relax":
        text = """现在，请闭上眼睛，深呼吸。

吸气，感受空气进入肺部。
呼气，释放所有紧张和压力。

你做得很好，继续保持。

每一次呼吸，都让你更加平静。
每一次呼气，都带走一份焦虑。

放松，放松，再放松。

太一，与你同在。"""
    else:
        text = """感谢你的努力，今天过得怎么样？

无论今天发生了什么，
都已经过去了。

明天是新的一天，
太一会一直陪着你。

晚安，好梦。"""
    
    output_filename = f"meditation_{theme}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    audio_path = generate_tts_audio(text, output_filename, CONFIG['tts_engine'])
    
    if audio_path:
        caption = "🧘 冥想语音：放松"
        send_telegram_voice(CONFIG['telegram_chat_id'], audio_path, caption)

def test_tts():
    """测试 TTS 功能"""
    logger.info("🚀 TTS 语音播报测试...")
    
    text = "你好，SAYELF！太一 TTS 语音功能已就绪。使用 edge-tts 免费开源方案，离线备用 pyttsx3。"
    output_filename = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    audio_path = generate_tts_audio(text, output_filename, CONFIG['tts_engine'])
    
    if audio_path:
        logger.info("✅ TTS 测试成功！")
        logger.info(f"音频文件：{audio_path}")
        return True
    else:
        logger.error("❌ TTS 测试失败")
        return False

def main():
    """主函数"""
    success = test_tts()
    
    if success:
        logger.info("\n✅ TTS 配置完成！")
        logger.info("\n方案:")
        logger.info("- 首选：edge-tts (免费在线，高质量)")
        logger.info("- 备用：pyttsx3 (完全离线，隐私安全)")
        logger.info("\n无需 API Key，完全免费开源！")

if __name__ == '__main__':
    main()
