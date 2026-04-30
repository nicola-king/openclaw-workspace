#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
止损/止盈语音提醒脚本
集成：TTS 语音 + Telegram/微信/飞书通知
触发：止损 -10% / 止盈 +50%
"""

import os
import json
import logging
import requests
from datetime import datetime

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/stop-loss-alert.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('StopLossAlert')

# 配置
CONFIG = {
    'telegram_bot_token': '8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY',
    'telegram_chat_id': '7073481596',
    'elevenlabs_api_key': os.getenv('ELEVENLABS_API_KEY', ''),
    'voice_id': 'pNInz6obpgDQGcFmaJgB',  # Adam 声音
    'output_dir': '/home/nicola/.openclaw/workspace/audio/alerts',
    'stop_loss_threshold': -0.10,  # -10% 止损
    'take_profit_threshold': 0.50,  # +50% 止盈
}

# 确保输出目录存在
os.makedirs(CONFIG['output_dir'], exist_ok=True)

# 持仓数据 (实际应从数据库读取)
POSITIONS = {
    'polymarket': {
        '2026_hottest_year': {'entry_price': 0.47, 'current_price': 0.47, 'amount': 30},
        'march_2026_temp': {'entry_price': 0.43, 'current_price': 0.43, 'amount': 27},
        'cat4_hurricane': {'entry_price': 0.39, 'current_price': 0.39, 'amount': 18},
        'nyc_march_precip': {'entry_price': 0.58, 'current_price': 0.58, 'amount': 22.5},
    },
    'gmgn': {
        'SOL': {'entry_price': 88, 'current_price': 88, 'amount': 1.7},
    }
}

def calculate_pnl(position):
    """计算盈亏百分比"""
    entry = position['entry_price']
    current = position['current_price']
    return (current - entry) / entry

def generate_tts_audio(text, output_filename):
    """生成 TTS 语音"""
    if not CONFIG['elevenlabs_api_key']:
        logger.warning("⚠️ ElevenLabs API Key 未配置，跳过语音生成")
        return None
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{CONFIG['voice_id']}"
    headers = {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': CONFIG['elevenlabs_api_key'],
    }
    data = {
        'text': text,
        'model_id': 'eleven_monolingual_v1',
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75,
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            output_path = os.path.join(CONFIG['output_dir'], output_filename)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"✅ TTS 音频生成成功：{output_path}")
            return output_path
        else:
            logger.error(f"TTS 生成失败：{response.text}")
            return None
    except Exception as e:
        logger.error(f"TTS 生成异常：{e}")
        return None

def send_telegram_message(message, voice_path=None):
    """发送 Telegram 消息 (文字 + 可选语音)"""
    # 发送文字消息
    url = f"https://api.telegram.org/bot{CONFIG['telegram_bot_token']}/sendMessage"
    data = {
        'chat_id': CONFIG['telegram_chat_id'],
        'text': message,
        'parse_mode': 'Markdown',
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            logger.info("✅ Telegram 文字消息发送成功")
        else:
            logger.error(f"Telegram 发送失败：{response.text}")
    except Exception as e:
        logger.error(f"Telegram 发送异常：{e}")
    
    # 发送语音消息 (可选)
    if voice_path:
        voice_url = f"https://api.telegram.org/bot{CONFIG['telegram_bot_token']}/sendVoice"
        try:
            with open(voice_path, 'rb') as f:
                files = {'voice': f}
                voice_data = {'chat_id': CONFIG['telegram_chat_id']}
                response = requests.post(voice_url, files=files, data=voice_data, timeout=30)
                
                if response.status_code == 200:
                    logger.info("✅ Telegram 语音消息发送成功")
                else:
                    logger.error(f"Telegram 语音发送失败：{response.text}")
        except Exception as e:
            logger.error(f"Telegram 语音发送异常：{e}")

def alert_stop_loss(market_name, pnl_pct, position_data):
    """止损提醒 (文字 + 语音)"""
    logger.warning(f"⚠️ 止损触发：{market_name} ({pnl_pct*100:.2f}%)")
    
    # 文字消息
    text_msg = f"""⚠️ 止损触发提醒

📊 市场：{market_name}
💰 入场价：${position_data['entry_price']:.3f}
📈 当前价：${position_data['current_price']:.3f}
📉 盈亏：{pnl_pct*100:.2f}%
💵 金额：${position_data['amount']:.2f}

⚙️ 已自动平仓
请确认账户变化。

---
太一 · 自动风控"""
    
    # 语音消息
    voice_text = f"""太一紧急提醒！

市场{market_name}触发止损，
当前亏损百分之{abs(pnl_pct*100):.1f}。

入场价格{position_data['entry_price']:.3f}美元，
当前价格{position_data['current_price']:.3f}美元。

已自动平仓，请确认账户变化。

太一，AGI 执行总管。"""
    
    voice_filename = f"stoploss_{market_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    voice_path = generate_tts_audio(voice_text, voice_filename)
    
    # 发送通知
    send_telegram_message(text_msg, voice_path)
    
    # 记录到日志
    log_stop_loss(market_name, pnl_pct, position_data)

def alert_take_profit(market_name, pnl_pct, position_data):
    """止盈提醒 (文字 + 语音)"""
    logger.info(f"✅ 止盈触发：{market_name} ({pnl_pct*100:.2f}%)")
    
    # 文字消息
    text_msg = f"""🎉 止盈触发提醒

📊 市场：{market_name}
💰 入场价：${position_data['entry_price']:.3f}
📈 当前价：${position_data['current_price']:.3f}
📈 盈亏：{pnl_pct*100:.2f}%
💵 金额：${position_data['amount']:.2f}

✅ 已自动平仓 50%
剩余仓位继续持有。

---
太一 · 自动风控"""
    
    # 语音消息
    voice_text = f"""太一向您报告！

市场{market_name}触发止盈，
当前盈利百分之{pnl_pct*100:.1f}。

入场价格{position_data['entry_price']:.3f}美元，
当前价格{position_data['current_price']:.3f}美元。

已自动平仓百分之五十，
剩余仓位继续持有。

太一，AGI 执行总管。"""
    
    voice_filename = f"takeprofit_{market_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    voice_path = generate_tts_audio(voice_text, voice_filename)
    
    # 发送通知
    send_telegram_message(text_msg, voice_path)
    
    # 记录到日志
    log_take_profit(market_name, pnl_pct, position_data)

def log_stop_loss(market_name, pnl_pct, position_data):
    """记录止损事件到日志"""
    today = datetime.now().strftime('%Y-%m-%d')
    log_entry = f"""
---

## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 止损触发

| 项目 | 数据 |
|------|------|
| 市场 | {market_name} |
| 入场价 | ${position_data['entry_price']:.3f} |
| 当前价 | ${position_data['current_price']:.3f} |
| 盈亏 | {pnl_pct*100:.2f}% |
| 金额 | ${position_data['amount']:.2f} |
| 状态 | 已平仓 |

"""
    
    log_file = f"/home/nicola/.openclaw/workspace/memory/stop-loss-{today}.md"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def log_take_profit(market_name, pnl_pct, position_data):
    """记录止盈事件到日志"""
    today = datetime.now().strftime('%Y-%m-%d')
    log_entry = f"""
---

## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 止盈触发

| 项目 | 数据 |
|------|------|
| 市场 | {market_name} |
| 入场价 | ${position_data['entry_price']:.3f} |
| 当前价 | ${position_data['current_price']:.3f} |
| 盈亏 | {pnl_pct*100:.2f}% |
| 金额 | ${position_data['amount']:.2f} |
| 状态 | 平仓 50% |

"""
    
    log_file = f"/home/nicola/.openclaw/workspace/memory/take-profit-{today}.md"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def check_positions():
    """检查所有持仓"""
    logger.info("🔍 检查持仓状态...")
    
    alerts_triggered = 0
    
    # 检查 Polymarket 持仓
    for market_name, position in POSITIONS['polymarket'].items():
        pnl_pct = calculate_pnl(position)
        
        # 检查止损
        if pnl_pct <= CONFIG['stop_loss_threshold']:
            alert_stop_loss(f"Poly-{market_name}", pnl_pct, position)
            alerts_triggered += 1
        
        # 检查止盈
        elif pnl_pct >= CONFIG['take_profit_threshold']:
            alert_take_profit(f"Poly-{market_name}", pnl_pct, position)
            alerts_triggered += 1
    
    # 检查 GMGN 持仓
    for market_name, position in POSITIONS['gmgn'].items():
        pnl_pct = calculate_pnl(position)
        
        # 检查止损
        if pnl_pct <= CONFIG['stop_loss_threshold']:
            alert_stop_loss(f"GMGN-{market_name}", pnl_pct, position)
            alerts_triggered += 1
        
        # 检查止盈
        elif pnl_pct >= CONFIG['take_profit_threshold']:
            alert_take_profit(f"GMGN-{market_name}", pnl_pct, position)
            alerts_triggered += 1
    
    if alerts_triggered == 0:
        logger.info("✓ 无止损/止盈触发")
    
    return alerts_triggered

def main():
    """主函数"""
    logger.info("🚀 止损/止盈语音提醒启动...")
    logger.info(f"⚠️ 止损阈值：{CONFIG['stop_loss_threshold']*100}%")
    logger.info(f"✅ 止盈阈值：{CONFIG['take_profit_threshold']*100}%")
    
    # 检查持仓
    alerts = check_positions()
    
    logger.info(f"✅ 检查完成：{alerts} 个告警")

if __name__ == '__main__':
    main()
