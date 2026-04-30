#!/usr/bin/env python3
"""
GMGN Cooking Module - 代币发射模块 ⚠️

⚠️ 金融执行操作 - 需要用户明确确认
功能：
- 代币创建 (create)
- 发射台统计 (stats)

参考 SKILL.md: gmgn-cooking
"""

from typing import Dict, Optional
from ..api.client import GMGNClient


class CookingModule:
    """代币发射模块 ⚠️"""
    
    def __init__(self, client: GMGNClient):
        self.client = client
    
    def get_stats(self) -> Dict:
        """
        获取发射台统计
        
        Returns:
            各发射台的代币创建数量
        """
        return self.client.get('/v1/launch/stats')
    
    def create_token(self, chain: str, dex: str, wallet_address: str,
                     name: str, symbol: str, buy_amount: float,
                     image_url: str = None, image_base64: str = None,
                     description: str = None, website: str = None,
                     twitter: str = None, telegram: str = None,
                     slippage: float = None, auto_slippage: bool = True,
                     priority_fee: float = None) -> Dict:
        """
        创建代币 ⚠️
        
        ⚠️ 需要用户明确确认！
        
        Args:
            chain: 链 (sol/bsc/base/eth/ton)
            dex: 发射台 (pump/fourmeme/pancakeswap 等)
            wallet_address: 钱包地址
            name: 代币名称
            symbol: 代币符号
            buy_amount: 初始买入数量 (人类可读单位，如 0.01 SOL)
            image_url: Logo URL
            image_base64: Logo base64
            description: 描述
            website: 网站
            twitter: Twitter
            telegram: Telegram
            slippage: 滑点
            auto_slippage: 自动滑点
            priority_fee: 优先费
        
        Returns:
            订单信息 (order_id/status)
        """
        data = {
            'chain': chain,
            'dex': dex,
            'from': wallet_address,
            'name': name,
            'symbol': symbol,
            'buy_amt': buy_amount
        }
        
        if image_url:
            data['image_url'] = image_url
        if image_base64:
            data['image'] = image_base64
        if description:
            data['description'] = description
        if website:
            data['website'] = website
        if twitter:
            data['twitter'] = twitter
        if telegram:
            data['telegram'] = telegram
        
        if slippage:
            data['slippage'] = slippage
        elif auto_slippage:
            data['auto_slippage'] = True
        
        if priority_fee:
            data['priority_fee'] = priority_fee
        
        # 需要签名认证
        return self.client.post('/v1/launch/create', data=data, requires_signature=True)
    
    def poll_token_creation(self, order_id: str, chain: str, 
                            max_attempts: int = 15, interval: int = 2) -> Dict:
        """
        轮询代币创建状态
        
        Args:
            order_id: 订单 ID
            chain: 链
            max_attempts: 最大轮询次数
            interval: 轮询间隔 (秒)
        
        Returns:
            最终状态 (包含 output_token 地址)
        """
        import time
        
        for i in range(max_attempts):
            result = self.client.get('/v1/trade/query_order', params={
                'chain': chain,
                'order_id': order_id
            })
            
            status = result.get('status', '')
            if status in ['confirmed', 'failed', 'expired']:
                return result
            
            time.sleep(interval)
        
        return {'error': 'TIMEOUT', 'message': '代币创建超时'}
