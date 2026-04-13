#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通讯智能路由器 - 自动选择通讯渠道和流量路由

功能:
- 飞书消息 (国内流量)
- 微信消息 (国内流量)
- Telegram 消息 (代理流量)
- 智能渠道路由
"""

import os
import logging
from typing import Optional, List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SmartCommunication')

# 导入智能网关
import sys
import importlib.util

# 动态加载智能网关模块
gateway_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'smart-gateway', 'smart-gateway.py')
spec = importlib.util.spec_from_file_location('SmartGateway', gateway_path)
SmartGatewayModule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SmartGatewayModule)
SmartGateway = SmartGatewayModule.SmartGateway

class SmartCommunication:
    """通讯智能路由器"""
    
    def __init__(self):
        # 初始化智能网关 (依赖)
        self.gateway = SmartGateway()
        
        # 飞书配置
        self.feishu_app_id = os.getenv('FEISHU_APP_ID', '')
        self.feishu_app_secret = os.getenv('FEISHU_APP_SECRET', '')
        self.feishu_enabled = bool(self.feishu_app_id and self.feishu_app_secret)
        
        # 微信配置
        self.wechat_app_id = os.getenv('WECHAT_APP_ID', '')
        self.wechat_app_secret = os.getenv('WECHAT_APP_SECRET', '')
        self.wechat_enabled = bool(self.wechat_app_id and self.wechat_app_secret)
        
        # Telegram 配置
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '7073481596')
        self.telegram_enabled = bool(self.telegram_bot_token)
        
        # 渠道优先级
        self.channel_priority = {
            'high': ['telegram'],  # 高优先级→Telegram
            'normal': ['feishu'],  # 普通→飞书
            'low': ['feishu', 'wechat'],  # 低优先级→飞书/微信
        }
    
    def send_feishu(self, user_id: str, message: str, msg_type: str = 'text') -> bool:
        """
        发送飞书消息 (国内流量)
        
        Args:
            user_id: 用户 ID
            message: 消息内容
            msg_type: 消息类型 (text/post/image)
        
        Returns:
            bool: 发送成功与否
        """
        if not self.feishu_enabled:
            logger.warning("飞书未配置，跳过发送")
            return False
        
        try:
            # 获取访问令牌
            token = self._get_feishu_token()
            if not token:
                return False
            
            # 发送消息 (自动走国内流量)
            url = 'https://open.feishu.cn/open-apis/im/v1/messages'
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            payload = {
                'receive_id': user_id,
                'msg_type': msg_type,
                'content': {
                    'text': message
                }
            }
            
            response = self.gateway.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                logger.info(f"✅ 飞书消息发送成功：{user_id}")
                return True
            else:
                logger.error(f"❌ 飞书消息发送失败：{response.status_code}")
                return False
        
        except Exception as e:
            logger.error(f"❌ 飞书消息发送异常：{e}")
            return False
    
    def send_wechat(self, openid: str, message: str) -> bool:
        """
        发送微信消息 (国内流量)
        
        Args:
            openid: 用户 openid
            message: 消息内容
        
        Returns:
            bool: 发送成功与否
        """
        if not self.wechat_enabled:
            logger.warning("微信未配置，跳过发送")
            return False
        
        try:
            # 获取访问令牌 (自动走国内流量)
            token = self._get_wechat_token()
            if not token:
                return False
            
            # 发送客服消息
            url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}'
            payload = {
                'touser': openid,
                'msgtype': 'text',
                'text': {
                    'content': message
                }
            }
            
            response = self.gateway.post(url, json=payload)
            
            if response.status_code == 200:
                logger.info(f"✅ 微信消息发送成功：{openid}")
                return True
            else:
                logger.error(f"❌ 微信消息发送失败：{response.status_code}")
                return False
        
        except Exception as e:
            logger.error(f"❌ 微信消息发送异常：{e}")
            return False
    
    def send_telegram(self, chat_id: str, message: str, parse_mode: str = 'HTML') -> bool:
        """
        发送 Telegram 消息 (代理流量)
        
        Args:
            chat_id: 聊天 ID
            message: 消息内容
            parse_mode: 解析模式 (HTML/Markdown)
        
        Returns:
            bool: 发送成功与否
        """
        if not self.telegram_enabled:
            logger.warning("Telegram 未配置，跳过发送")
            return False
        
        try:
            # 发送消息 (自动走代理流量)
            url = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage'
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = self.gateway.post(url, json=payload)
            
            if response.status_code == 200:
                logger.info(f"✅ Telegram 消息发送成功：{chat_id}")
                return True
            else:
                logger.error(f"❌ Telegram 消息发送失败：{response.status_code}")
                return False
        
        except Exception as e:
            logger.error(f"❌ Telegram 消息发送异常：{e}")
            return False
    
    def send(self, message: str, priority: str = 'normal', channels: Optional[List[str]] = None) -> Dict:
        """
        智能发送 (自动选择渠道)
        
        Args:
            message: 消息内容
            priority: 优先级 (high/normal/low)
            channels: 指定渠道列表 (可选)
        
        Returns:
            dict: 发送结果
        """
        results = {
            'message': message,
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'channels': {}
        }
        
        # 确定发送渠道
        if channels:
            target_channels = channels
        else:
            target_channels = self.channel_priority.get(priority, ['feishu'])
        
        # 发送到各渠道
        for channel in target_channels:
            if channel == 'feishu' and self.feishu_enabled:
                # TODO: 需要用户 ID
                results['channels']['feishu'] = 'skipped (need user_id)'
            
            elif channel == 'wechat' and self.wechat_enabled:
                # TODO: 需要 openid
                results['channels']['wechat'] = 'skipped (need openid)'
            
            elif channel == 'telegram' and self.telegram_enabled:
                # 使用默认聊天 ID
                success = self.send_telegram('@sayelfbot', message)
                results['channels']['telegram'] = 'success' if success else 'failed'
            
            else:
                results['channels'][channel] = 'not configured'
        
        return results
    
    def _get_feishu_token(self) -> Optional[str]:
        """获取飞书访问令牌 (国内流量)"""
        try:
            url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
            payload = {
                'app_id': self.feishu_app_id,
                'app_secret': self.feishu_app_secret
            }
            
            response = self.gateway.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('tenant_access_token')
            else:
                logger.error(f"飞书令牌获取失败：{response.status_code}")
                return None
        
        except Exception as e:
            logger.error(f"飞书令牌获取异常：{e}")
            return None
    
    def _get_wechat_token(self) -> Optional[str]:
        """获取微信访问令牌 (国内流量)"""
        try:
            url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.wechat_app_id}&secret={self.wechat_app_secret}'
            
            response = self.gateway.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('access_token')
            else:
                logger.error(f"微信令牌获取失败：{response.status_code}")
                return None
        
        except Exception as e:
            logger.error(f"微信令牌获取异常：{e}")
            return None
    
    def get_status(self) -> str:
        """获取状态报告"""
        status = f"""
💬 通讯智能路由器状态
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━ 渠道配置 ━━━

飞书 (国内流量):
  App ID: {self.feishu_app_id[:10] + '...' if self.feishu_app_id else '未配置'}
  状态：{'✅ 已配置' if self.feishu_enabled else '❌ 未配置'}

微信 (国内流量):
  App ID: {self.wechat_app_id[:10] + '...' if self.wechat_app_id else '未配置'}
  状态：{'✅ 已配置' if self.wechat_enabled else '❌ 未配置'}

Telegram (代理流量):
  Bot Token: {self.telegram_bot_token[:20] + '...' if self.telegram_bot_token else '未配置'}
  状态：{'✅ 已配置' if self.telegram_enabled else '❌ 未配置'}

━━━ 渠道路由 ━━━

高优先级：Telegram
普通优先级：飞书
低优先级：飞书 + 微信

━━━ 智能网关 ━━━

网关状态：{'✅ 已连接' if self.gateway else '❌ 未连接'}
"""
        return status


def main():
    """测试主函数"""
    comm = SmartCommunication()
    
    print("💬 通讯智能路由器测试\n")
    print("=" * 60)
    
    # 打印状态
    print(comm.get_status())
    
    # 测试发送
    print("\n" + "=" * 60)
    print("\n📤 测试发送:")
    
    # Telegram 测试
    if comm.telegram_enabled:
        result = comm.send_telegram(
            chat_id=comm.telegram_chat_id,
            message='🧪 通讯智能路由器测试消息'
        )
        print(f"Telegram: {'✅ 成功' if result else '❌ 失败'}")
    else:
        print("Telegram: ⚠️ 未配置")


if __name__ == '__main__':
    main()
