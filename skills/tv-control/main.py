#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TV Control Skill - 太一电视控制
主程序入口
"""

import os
import sys
import logging
import yaml
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.cec import CECController
from tools.audio import AudioController
from tools.display import DisplayController
from handlers.telegram import TelegramHandler
from handlers.http import HTTPServer

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/tv-control.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TVControl')

# 加载配置
def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    
    if not os.path.exists(config_path):
        logger.warning(f"配置文件不存在：{config_path}")
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    logger.info(f"✅ 配置文件加载：{config_path}")
    return config

class TVControlSkill:
    """电视控制 Skill 主类"""
    
    def __init__(self, config=None):
        self.config = config or load_config()
        
        # 初始化控制器
        self.cec = CECController()
        self.audio = AudioController()
        self.display = DisplayController()
        
        # 初始化处理器
        self.telegram = None
        self.http_server = None
        
        # 状态
        self.running = False
        
        logger.info("🚀 太一电视控制初始化完成")
    
    def handle_command(self, command, args=None):
        """处理控制指令"""
        logger.info(f"📺 处理指令：{command}")
        
        command_map = {
            'on': self.cec.power_on,
            'off': self.cec.power_off,
            'vol+': self.audio.volume_up,
            'vol-': self.audio.volume_down,
            'mute': self.audio.mute,
            'ch+': self.cec.channel_up,
            'ch-': self.cec.channel_down,
            'status': self.get_status,
        }
        
        if command in command_map:
            result = command_map[command]()
            logger.info(f"✅ 指令执行成功：{command}")
            return result
        else:
            logger.error(f"❌ 未知指令：{command}")
            return {'status': 'error', 'message': 'Unknown command'}
    
    def get_status(self):
        """获取电视状态"""
        return {
            'power': self.cec.get_power_status(),
            'volume': self.audio.get_volume(),
            'mute': self.audio.is_muted(),
        }
    
    def start_telegram(self):
        """启动 Telegram Bot"""
        if self.config.get('telegram', {}).get('enabled'):
            self.telegram = TelegramHandler(
                bot_token=self.config['telegram']['bot_token'],
                chat_id=self.config['telegram']['chat_id'],
                skill=self
            )
            self.telegram.start()
            logger.info("✅ Telegram Bot 已启动")
    
    def start_http_server(self):
        """启动 HTTP API 服务"""
        if self.config.get('api', {}).get('enabled'):
            self.http_server = HTTPServer(
                host=self.config['api'].get('host', '0.0.0.0'),
                port=self.config['api'].get('port', 5001),
                token=self.config['api'].get('token', 'secret'),
                skill=self
            )
            self.http_server.start()
            logger.info(f"✅ HTTP API 已启动 (端口 {self.config['api']['port']})")
    
    def run(self):
        """运行服务"""
        logger.info("🚀 太一电视控制启动...")
        self.running = True
        
        # 启动处理器
        self.start_telegram()
        self.start_http_server()
        
        # 主循环
        try:
            while self.running:
                # 保持运行
                pass
        except KeyboardInterrupt:
            logger.info("⏹️ 服务停止")
            self.stop()
    
    def stop(self):
        """停止服务"""
        self.running = False
        
        if self.telegram:
            self.telegram.stop()
        
        if self.http_server:
            self.http_server.stop()
        
        logger.info("✅ 服务已停止")

def main():
    """主函数"""
    # 加载配置
    config = load_config()
    
    # 创建 Skill 实例
    skill = TVControlSkill(config)
    
    # 运行
    skill.run()

if __name__ == '__main__':
    main()
