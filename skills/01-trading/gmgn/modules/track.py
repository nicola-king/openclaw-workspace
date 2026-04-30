#!/usr/bin/env python3
"""
GMGN Track Module - 链上追踪模块

功能：
- 关注钱包交易 (follow-wallet)
- KOL 交易记录 (kol)
- Smart Money 交易 (smartmoney)

参考 SKILL.md: gmgn-track
"""

from typing import Dict, List, Optional
from ..api.client import GMGNClient


class TrackModule:
    """链上追踪模块"""
    
    def __init__(self, client: GMGNClient):
        self.client = client
        self.chain = 'sol'
    
    def set_chain(self, chain: str):
        """设置链：sol/bsc/base"""
        if chain not in ['sol', 'bsc', 'base']:
            raise ValueError(f"Invalid chain: {chain}. Must be sol/bsc/base")
        self.chain = chain
    
    def get_follow_wallet_trades(self, wallet_address: str = None,
                                  side: str = None, limit: int = 10,
                                  min_amount_usd: float = None,
                                  max_amount_usd: float = None) -> Dict:
        """
        获取关注钱包的交易记录
        
        ⚠️ 需要用户已在 GMGN 平台关注钱包
        
        Args:
            wallet_address: 特定钱包地址过滤
            side: 交易方向 (buy/sell)
            limit: 结果数量
            min_amount_usd: 最小 USD 金额
            max_amount_usd: 最大 USD 金额
        
        Returns:
            交易记录列表
        """
        params = {
            'chain': self.chain,
            'limit': limit
        }
        
        if wallet_address:
            params['wallet'] = wallet_address
        if side:
            params['side'] = side
        if min_amount_usd:
            params['min_amount_usd'] = min_amount_usd
        if max_amount_usd:
            params['max_amount_usd'] = max_amount_usd
        
        # 需要签名认证
        return self.client.get('/v1/trade/follow_wallet', params=params)
    
    def get_kol_trades(self, side: str = None, limit: int = 50) -> Dict:
        """
        获取 KOL 交易记录
        
        Args:
            side: 交易方向 (buy/sell)
            limit: 结果数量 (max 200)
        
        Returns:
            KOL 交易列表
        """
        params = {
            'chain': self.chain,
            'limit': min(limit, 200)
        }
        
        if side:
            params['side'] = side
        
        return self.client.get('/v1/user/kol', params=params)
    
    def get_smart_money_trades(self, side: str = None, limit: int = 50) -> Dict:
        """
        获取 Smart Money 交易记录
        
        Args:
            side: 交易方向 (buy/sell)
            limit: 结果数量 (max 200)
        
        Returns:
            Smart Money 交易列表
        """
        params = {
            'chain': self.chain,
            'limit': min(limit, 200)
        }
        
        if side:
            params['side'] = side
        
        return self.client.get('/v1/user/smartmoney', params=params)
    
    def detect_cluster_signals(self, trades: List[Dict], time_window: int = 1800) -> List[Dict]:
        """
        检测集群信号 (多个钱包交易同一代币)
        
        Args:
            trades: 交易记录列表
            time_window: 时间窗口 (秒，默认 30 分钟)
        
        Returns:
            集群信号列表
        """
        import time
        
        # 按代币地址分组
        token_trades = {}
        for trade in trades:
            token = trade.get('base_address') or trade.get('base_token', {}).get('address')
            if not token:
                continue
            
            if token not in token_trades:
                token_trades[token] = []
            token_trades[token].append(trade)
        
        # 检测集群
        clusters = []
        current_time = int(time.time())
        
        for token, token_trade_list in token_trades.items():
            # 按时间排序
            token_trade_list.sort(key=lambda x: x.get('timestamp', 0))
            
            # 检查时间窗口内的交易
            recent_trades = [t for t in token_trade_list 
                           if current_time - t.get('timestamp', 0) <= time_window]
            
            if len(recent_trades) >= 2:
                # 检查方向一致性
                buy_count = sum(1 for t in recent_trades if t.get('side') == 'buy')
                sell_count = len(recent_trades) - buy_count
                
                if buy_count >= 2 or sell_count >= 2:
                    clusters.append({
                        'token': token,
                        'trade_count': len(recent_trades),
                        'buy_count': buy_count,
                        'sell_count': sell_count,
                        'direction': 'buy' if buy_count > sell_count else 'sell',
                        'signal_strength': 'STRONG' if len(recent_trades) >= 3 else 'MEDIUM',
                        'trades': recent_trades
                    })
        
        return clusters
