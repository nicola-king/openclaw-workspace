#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 处理器
"""

import logging
import requests
from datetime import datetime

logger = logging.getLogger('TVControl.Telegram')

class TelegramHandler:
    """Telegram Bot 处理器"""
    
    def __init__(self, bot_token, chat_id, skill):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.skill = skill
        self.running = False
        
        logger.info("📱 Telegram Bot 初始化完成")
    
    def send_message(self, message):
        """发送 Telegram 消息"""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown',
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Telegram 消息发送成功")
                return True
            else:
                logger.error(f"Telegram 发送失败：{response.text}")
                return False
        except Exception as e:
            logger.error(f"Telegram 发送异常：{e}")
            return False
    
    def handle_command(self, command, args=None):
        """处理 Bot 命令"""
        logger.info(f"📱 收到命令：{command}")
        
        # 执行技能
        result = self.skill.handle_command(command, args)
        
        # 发送结果
        if result['status'] == 'success':
            emoji_map = {
                'on': '🔌',
                'off': '🔌',
                'vol+': '🔊',
                'vol-': '🔉',
                'mute': '🔇',
                'ch+': '📺',
                'ch-': '📺',
            }
            emoji = emoji_map.get(command, '📺')
            
            message = f"""{emoji} 电视控制

指令：{command}
状态：✅ 成功

---
太一 · 电视控制"""
        else:
            message = f"""❌ 电视控制失败

指令：{command}
错误：{result.get('message', '未知错误')}

---
太一 · 电视控制"""
        
        self.send_message(message)
        return result
    
    def start(self):
        """启动 Bot (轮询模式)"""
        logger.info("🚀 Telegram Bot 启动...")
        self.running = True
        
        # TODO: 实现轮询逻辑
        # 这里简化为仅日志
        logger.info("✅ Telegram Bot 已启动 (轮询模式待实现)")
    
    def stop(self):
        """停止 Bot"""
        self.running = False
        logger.info("⏹️ Telegram Bot 已停止")
