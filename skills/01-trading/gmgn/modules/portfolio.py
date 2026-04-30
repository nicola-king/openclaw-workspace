#!/usr/bin/env python3
"""
GMGN Portfolio Module - 钱包组合模块

功能：
- 钱包信息 (user info)
- 持仓查询 (holdings)
- 交易记录 (activity)
- 交易统计 (stats)
- 代币余额 (token balance)

参考 SKILL.md: gmgn-portfolio
"""

from typing import Dict, List, Optional
from ..api.client import GMGNClient


class PortfolioModule:
    """钱包组合模块"""
    
    def __init__(self, client: GMGNClient):
        self.client = client
        self.chain = 'sol'
    
    def set_chain(self, chain: str):
        """设置链：sol/bsc/base"""
        if chain not in ['sol', 'bsc', 'base']:
            raise ValueError(f"Invalid chain: {chain}. Must be sol/bsc/base")
        self.chain = chain
    
    def get_wallet_info(self) -> Dict:
        """
        获取 API Key 绑定的钱包信息
        
        Returns:
            钱包信息 (地址/余额等)
        """
        return self.client.get('/v1/user/info')
    
    def get_holdings(self, wallet_address: str, limit: int = 20,
                     order_by: str = 'usd_value', direction: str = 'desc',
                     include_sold: bool = False) -> Dict:
        """
        获取钱包持仓
        
        Args:
            wallet_address: 钱包地址
            limit: 结果数量
            order_by: 排序字段 (usd_value/realized_profit 等)
            direction: 排序方向
            include_sold: 是否包含已卖出的持仓
        
        Returns:
            持仓列表
        """
        params = {
            'chain': self.chain,
            'wallet': wallet_address,
            'limit': limit,
            'order_by': order_by,
            'direction': direction
        }
        
        if include_sold:
            params['hide_closed'] = 'false'
        
        return self.client.get('/v1/user/wallet_holdings', params=params)
    
    def get_activity(self, wallet_address: str, token_address: str = None,
                     tx_type: str = None, limit: int = 20, cursor: str = None) -> Dict:
        """
        获取钱包交易记录
        
        Args:
            wallet_address: 钱包地址
            token_address: 代币地址过滤
            tx_type: 交易类型 (buy/sell/transfer)
            limit: 结果数量
            cursor: 分页游标
        
        Returns:
            交易记录列表 + next cursor
        """
        params = {
            'chain': self.chain,
            'wallet': wallet_address,
            'limit': limit
        }
        
        if token_address:
            params['token'] = token_address
        if tx_type:
            params['type'] = tx_type
        if cursor:
            params['cursor'] = cursor
        
        return self.client.get('/v1/user/wallet_activity', params=params)
    
    def get_stats(self, wallet_address: str, period: str = '7d') -> Dict:
        """
        获取钱包交易统计
        
        Args:
            wallet_address: 钱包地址
            period: 统计周期 (7d/30d)
        
        Returns:
            交易统计数据 (PnL/winrate 等)
        """
        params = {
            'chain': self.chain,
            'wallet': wallet_address,
            'period': period
        }
        
        return self.client.get('/v1/user/wallet_stats', params=params)
    
    def get_token_balance(self, wallet_address: str, token_address: str) -> Dict:
        """
        获取钱包的特定代币余额
        
        Args:
            wallet_address: 钱包地址
            token_address: 代币地址
        
        Returns:
            余额信息
        """
        params = {
            'chain': self.chain,
            'wallet': wallet_address,
            'token': token_address
        }
        
        return self.client.get('/v1/user/wallet_token_balance', params=params)
    
    def batch_get_stats(self, wallet_addresses: List[str], period: str = '7d') -> Dict:
        """
        批量获取多个钱包的统计
        
        Args:
            wallet_addresses: 钱包地址列表
            period: 统计周期
        
        Returns:
            统计数据列表
        """
        params = {
            'chain': self.chain,
            'wallet': wallet_addresses,  # 重复参数
            'period': period
        }
        
        return self.client.get('/v1/user/wallet_stats', params=params)
