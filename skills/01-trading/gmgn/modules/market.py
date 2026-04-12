#!/usr/bin/env python3
"""
GMGN Market Module - 市场数据模块

功能：
- K 线数据 (token_kline)
- 热度榜单 (trending)
- Trenches 代币列表 (new/near_completion/graduated)

参考 SKILL.md: gmgn-market
"""

from typing import Dict, List, Optional
from ..api.client import GMGNClient


class MarketModule:
    """市场数据模块"""
    
    def __init__(self, client: GMGNClient):
        self.client = client
        self.chain = 'sol'  # default: solana
    
    def set_chain(self, chain: str):
        """设置链：sol/bsc/base"""
        if chain not in ['sol', 'bsc', 'base']:
            raise ValueError(f"Invalid chain: {chain}. Must be sol/bsc/base")
        self.chain = chain
    
    def get_kline(self, token_address: str, resolution: str = '1h', 
                  from_ts: int = None, to_ts: int = None) -> Dict:
        """
        获取 K 线数据
        
        Args:
            token_address: 代币合约地址
            resolution: K 线周期 (1m/5m/15m/1h/4h/1d)
            from_ts: 开始时间 (Unix 秒)
            to_ts: 结束时间 (Unix 秒)
        
        Returns:
            K 线数据列表
        """
        import time
        params = {
            'chain': self.chain,
            'address': token_address,
            'resolution': resolution
        }
        
        if from_ts:
            params['from'] = from_ts
        elif resolution.endswith('h'):
            # 默认获取最近 24 小时
            hours = int(resolution[:-1])
            params['from'] = int(time.time()) - (24 * 3600)
        
        if to_ts:
            params['to'] = to_ts
        
        return self.client.get('/v1/market/token_kline', params=params)
    
    def get_trending(self, interval: str = '1h', limit: int = 50,
                     order_by: str = 'volume', direction: str = 'desc',
                     filters: List[str] = None, platforms: List[str] = None) -> Dict:
        """
        获取热度榜单
        
        Args:
            interval: 时间窗口 (1m/5m/1h/6h/24h)
            limit: 结果数量 (max 100)
            order_by: 排序字段 (volume/swaps/marketcap/etc.)
            direction: 排序方向 (asc/desc)
            filters: 过滤标签 (renounced/frozen/not_honeypot 等)
            platforms: 平台过滤 (Pump.fun/letsbonk 等)
        
        Returns:
            热度榜单列表
        """
        params = {
            'chain': self.chain,
            'interval': interval,
            'limit': min(limit, 100),
            'order_by': order_by,
            'direction': direction
        }
        
        if filters:
            params['filter'] = filters
        if platforms:
            params['platform'] = platforms
        
        return self.client.get('/v1/market/rank', params=params)
    
    def get_trenches(self, types: List[str] = None, launchpad_platforms: List[str] = None,
                     limit: int = 80, sort_by: str = 'smart_degen_count',
                     filter_preset: str = None) -> Dict:
        """
        获取 Trenches 代币列表 (新发射代币)
        
        Args:
            types: 类别 (new_creation/near_completion/completed)
            launchpad_platforms: 发射台过滤
            limit: 每类别最大数量 (max 80)
            sort_by: 排序字段
            filter_preset: 过滤预设 (safe/smart-money/strict)
        
        Returns:
            Trenches 数据 (new_creation/pump/completed 三个类别)
        """
        data = {
            'chain': self.chain,
            'limit': min(limit, 80),
            'sort_by': sort_by,
            'direction': 'desc'
        }
        
        if types:
            data['type'] = types
        if launchpad_platforms:
            data['launchpad_platform'] = launchpad_platforms
        if filter_preset:
            data['filter_preset'] = filter_preset
        
        return self.client.post('/v1/trenches', data=data)
    
    def get_token_rank(self, token_address: str) -> Optional[Dict]:
        """
        获取代币在热度榜中的排名信息
        
        Args:
            token_address: 代币地址
        
        Returns:
            排名信息或 None
        """
        result = self.get_trending(limit=100)
        if 'data' in result and 'rank' in result['data']:
            for item in result['data']['rank']:
                if item.get('address') == token_address:
                    return item
        return None
