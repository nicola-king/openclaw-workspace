#!/usr/bin/env python3
"""
GMGN Token Module - 代币信息模块

功能：
- 基本信息 (info)
- 安全检测 (security)
- 池子信息 (pool)
- 持仓分布 (holders)
- 交易排行 (traders)

参考 SKILL.md: gmgn-token
"""

from typing import Dict, List, Optional
from ..api.client import GMGNClient


class TokenModule:
    """代币信息模块"""
    
    def __init__(self, client: GMGNClient):
        self.client = client
        self.chain = 'sol'
    
    def set_chain(self, chain: str):
        """设置链：sol/bsc/base"""
        if chain not in ['sol', 'bsc', 'base']:
            raise ValueError(f"Invalid chain: {chain}. Must be sol/bsc/base")
        self.chain = chain
    
    def get_info(self, token_address: str) -> Dict:
        """
        获取代币基本信息
        
        Args:
            token_address: 代币合约地址
        
        Returns:
            代币信息 (price/market_cap/liquidity/holders/social 等)
        """
        params = {
            'chain': self.chain,
            'address': token_address
        }
        
        return self.client.get('/v1/token/info', params=params)
    
    def get_security(self, token_address: str) -> Dict:
        """
        获取代币安全信息
        
        ⚠️ 买入前必须检查！
        
        Args:
            token_address: 代币合约地址
        
        Returns:
            安全信息 (honeypot/rug_ratio/tax/holder_concentration 等)
        """
        params = {
            'chain': self.chain,
            'address': token_address
        }
        
        return self.client.get('/v1/token/security', params=params)
    
    def get_pool(self, token_address: str) -> Dict:
        """
        获取代币池子信息
        
        Args:
            token_address: 代币合约地址
        
        Returns:
            池子信息 (liquidity/reserves/dex 等)
        """
        params = {
            'chain': self.chain,
            'address': token_address
        }
        
        return self.client.get('/v1/token/pool_info', params=params)
    
    def get_holders(self, token_address: str, limit: int = 20,
                    order_by: str = 'amount_percentage', direction: str = 'desc',
                    tag: str = None) -> Dict:
        """
        获取代币持仓分布
        
        Args:
            token_address: 代币合约地址
            limit: 结果数量 (max 100)
            order_by: 排序字段 (amount_percentage/profit/unrealized_profit 等)
            direction: 排序方向
            tag: 钱包标签过滤 (smart_degen/renowned)
        
        Returns:
            持仓列表
        """
        params = {
            'chain': self.chain,
            'address': token_address,
            'limit': min(limit, 100),
            'order_by': order_by,
            'direction': direction
        }
        
        if tag:
            params['tag'] = tag
        
        return self.client.get('/v1/market/token_top_holders', params=params)
    
    def get_traders(self, token_address: str, limit: int = 20,
                    order_by: str = 'profit', direction: str = 'desc',
                    tag: str = None) -> Dict:
        """
        获取代币交易排行
        
        Args:
            token_address: 代币合约地址
            limit: 结果数量 (max 100)
            order_by: 排序字段 (profit/buy_volume/sell_volume 等)
            direction: 排序方向
            tag: 钱包标签过滤 (smart_degen/renowned)
        
        Returns:
            交易排行列表
        """
        params = {
            'chain': self.chain,
            'address': token_address,
            'limit': min(limit, 100),
            'order_by': order_by,
            'direction': direction
        }
        
        if tag:
            params['tag'] = tag
        
        return self.client.get('/v1/market/token_top_traders', params=params)
    
    def quick_score(self, token_address: str) -> Dict:
        """
        快速获取代币安全评分
        
        Args:
            token_address: 代币合约地址
        
        Returns:
            评分卡 (risk_level/verdict/key_signals)
        """
        # 获取安全信息
        security = self.get_security(token_address)
        info = self.get_info(token_address)
        
        if 'error' in security or 'error' in info:
            return {'error': 'Failed to fetch token data'}
        
        # 解析安全数据
        sec_data = security.get('data', {})
        info_data = info.get('data', {})
        
        # 硬停止检查
        if sec_data.get('is_honeypot') == 'yes':
            return {
                'risk_level': 'critical',
                'verdict': '🚫 HONEYPOT - DO NOT BUY',
                'hard_stop': True
            }
        
        # 风险评分
        rug_ratio = sec_data.get('rug_ratio', 0)
        top_10_holder = sec_data.get('top_10_holder_rate', 0)
        smart_wallets = info_data.get('wallet_tags_stat', {}).get('smart_wallets', 0)
        
        risk_score = 0
        signals = []
        
        if rug_ratio > 0.3:
            risk_score += 3
            signals.append('🔴 High rug ratio')
        elif rug_ratio > 0.1:
            risk_score += 1
            signals.append('🟡 Medium rug ratio')
        
        if top_10_holder > 0.5:
            risk_score += 3
            signals.append('🔴 High holder concentration')
        elif top_10_holder > 0.2:
            risk_score += 1
            signals.append('🟡 Medium holder concentration')
        
        if smart_wallets >= 3:
            signals.append('🟢 Strong smart money interest')
        elif smart_wallets == 0:
            signals.append('⚪ No smart money interest')
        
        # 判定
        if risk_score >= 3:
            verdict = '🔴 High risk - skip or verify manually'
            risk_level = 'high'
        elif risk_score >= 1:
            verdict = '🟡 Mixed signals - proceed with caution'
            risk_level = 'medium'
        else:
            verdict = '🟢 Clean - worth researching'
            risk_level = 'low'
        
        return {
            'risk_level': risk_level,
            'verdict': verdict,
            'signals': signals,
            'rug_ratio': rug_ratio,
            'top_10_holder': top_10_holder,
            'smart_wallets': smart_wallets
        }
