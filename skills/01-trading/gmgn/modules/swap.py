#!/usr/bin/env python3
"""
GMGN Swap Module - 交易执行模块 ⚠️

⚠️ 金融执行操作 - 需要用户明确确认
功能：
- 代币交换 (swap)
- 报价查询 (quote)
- 订单状态查询 (order get)
- 策略订单 (limit/take-profit/stop-loss)

参考 SKILL.md: gmgn-swap
"""

from typing import Dict, Optional
from ..api.client import GMGNClient


class SwapModule:
    """交易执行模块 ⚠️"""
    
    def __init__(self, client: GMGNClient):
        self.client = client
        self.chain = 'sol'
    
    def set_chain(self, chain: str):
        """设置链：sol/bsc/base"""
        if chain not in ['sol', 'bsc', 'base']:
            raise ValueError(f"Invalid chain: {chain}. Must be sol/bsc/base")
        self.chain = chain
    
    def get_quote(self, wallet_address: str, input_token: str, output_token: str,
                  amount: int, slippage: float = 0.01) -> Dict:
        """
        获取交换报价 (不执行交易)
        
        Args:
            wallet_address: 钱包地址
            input_token: 输入代币地址
            output_token: 输出代币地址
            amount: 输入数量 (最小单位)
            slippage: 滑点容忍 (0.01 = 1%)
        
        Returns:
            报价信息 (output_amount/min_output_amount 等)
        """
        params = {
            'chain': self.chain,
            'from': wallet_address,
            'input_token': input_token,
            'output_token': output_token,
            'amount': amount,
            'slippage': slippage
        }
        
        return self.client.get('/v1/trade/quote', params=params)
    
    def swap(self, wallet_address: str, input_token: str, output_token: str,
             amount: int = None, percent: int = None, slippage: float = None,
             auto_slippage: bool = True, anti_mev: bool = True,
             priority_fee: float = None) -> Dict:
        """
        执行代币交换 ⚠️
        
        ⚠️ 需要用户明确确认！
        
        Args:
            wallet_address: 钱包地址
            input_token: 输入代币地址
            output_token: 输出代币地址
            amount: 输入数量 (最小单位，与 percent 互斥)
            percent: 卖出百分比 (1-100，与 amount 互斥)
            slippage: 滑点容忍 (与 auto_slippage 互斥)
            auto_slippage: 自动滑点
            anti_mev: 防 MEV 攻击
            priority_fee: 优先费 (SOL)
        
        Returns:
            订单信息 (order_id/hash/status)
        """
        data = {
            'chain': self.chain,
            'from': wallet_address,
            'input_token': input_token,
            'output_token': output_token
        }
        
        if amount is not None:
            data['amount'] = amount
        if percent is not None:
            data['percent'] = percent
        
        if slippage is not None:
            data['slippage'] = slippage
        elif auto_slippage:
            data['auto_slippage'] = True
        
        if anti_mev:
            data['anti_mev'] = True
        if priority_fee:
            data['priority_fee'] = priority_fee
        
        # 需要签名认证
        return self.client.post('/v1/trade/swap', data=data, requires_signature=True)
    
    def get_order_status(self, order_id: str) -> Dict:
        """
        查询订单状态
        
        Args:
            order_id: 订单 ID
        
        Returns:
            订单状态 (pending/processed/confirmed/failed/expired)
        """
        params = {
            'chain': self.chain,
            'order_id': order_id
        }
        
        return self.client.get('/v1/trade/query_order', params=params)
    
    def poll_order(self, order_id: str, max_attempts: int = 15, interval: int = 2) -> Dict:
        """
        轮询订单状态直到确认
        
        Args:
            order_id: 订单 ID
            max_attempts: 最大轮询次数
            interval: 轮询间隔 (秒)
        
        Returns:
            最终订单状态
        """
        import time
        
        for i in range(max_attempts):
            result = self.get_order_status(order_id)
            status = result.get('status', '')
            
            if status in ['confirmed', 'failed', 'expired']:
                return result
            
            time.sleep(interval)
        
        return {'error': 'TIMEOUT', 'message': '订单状态查询超时'}
    
    def create_strategy_order(self, wallet_address: str, base_token: str, quote_token: str,
                              side: str, check_price: float, amount_in: int = None,
                              amount_in_percent: int = None, slippage: float = 0.01) -> Dict:
        """
        创建策略订单 (限价/止盈/止损)
        
        Args:
            wallet_address: 钱包地址
            base_token: 基础代币地址
            quote_token: 报价代币地址
            side: 方向 (buy/sell)
            check_price: 触发价格
            amount_in: 输入数量
            amount_in_percent: 输入百分比
            slippage: 滑点容忍
        
        Returns:
            订单 ID
        """
        data = {
            'chain': self.chain,
            'from': wallet_address,
            'base_token': base_token,
            'quote_token': quote_token,
            'side': side,
            'check_price': str(check_price),
            'slippage': slippage
        }
        
        if amount_in:
            data['amount_in'] = amount_in
        if amount_in_percent:
            data['amount_in_percent'] = amount_in_percent
        
        return self.client.post('/v1/trade/strategy/create', data=data, requires_signature=True)
    
    def list_strategy_orders(self, order_type: str = 'open', limit: int = 10) -> Dict:
        """
        列出策略订单
        
        Args:
            order_type: 类型 (open/history)
            limit: 结果数量
        
        Returns:
            订单列表
        """
        params = {
            'chain': self.chain,
            'type': order_type,
            'limit': limit
        }
        
        return self.client.get('/v1/trade/strategy/list', params=params)
    
    def cancel_strategy_order(self, wallet_address: str, order_id: str) -> Dict:
        """
        取消策略订单
        
        Args:
            wallet_address: 钱包地址
            order_id: 订单 ID
        
        Returns:
            取消结果
        """
        data = {
            'chain': self.chain,
            'from': wallet_address,
            'order_id': order_id
        }
        
        return self.client.post('/v1/trade/strategy/cancel', data=data, requires_signature=True)
