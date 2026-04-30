#!/usr/bin/env python3
"""
GMGN - 统一 GMGN.AI 链上交易技能
v2.0 整合版：统一 API 封装 + 模块化设计

模块:
- market: 市场数据 (K 线/热度榜/Trenches)
- portfolio: 钱包组合 (持仓/交易/统计)
- swap: 交易执行 ⚠️ (需要用户确认)
- token: 代币信息 (安全检测/持仓分布)
- track: 链上追踪 (Smart Money/KOL)
- cooking: 代币发射 (独立子模块)
"""

from .api.client import GMGNClient, create_client
from .modules.market import MarketModule
from .modules.portfolio import PortfolioModule
from .modules.swap import SwapModule
from .modules.token import TokenModule
from .modules.track import TrackModule


class GMGN:
    """
    GMGN 统一入口
    
    使用示例:
        gmgn = GMGN()
        gmgn.set_chain('sol')
        
        # 市场数据
        trending = gmgn.market.get_trending(limit=20)
        
        # 钱包组合
        holdings = gmgn.portfolio.get_holdings('WALLET_ADDRESS')
        
        # ⚠️ 交易执行 (需要确认)
        # result = gmgn.swap.swap(...)
    """
    
    def __init__(self, api_key: str = None, private_key: str = None):
        """
        初始化 GMGN 客户端
        
        Args:
            api_key: GMGN API Key (可选，从环境变量读取)
            private_key: 私钥 (用于交易执行，可选)
        """
        self.client = GMGNClient(api_key, private_key)
        
        # 初始化模块
        self.market = MarketModule(self.client)
        self.portfolio = PortfolioModule(self.client)
        self.swap = SwapModule(self.client)
        self.token = TokenModule(self.client)
        self.track = TrackModule(self.client)
    
    def set_chain(self, chain: str):
        """
        设置默认链
        
        Args:
            chain: sol/bsc/base
        """
        self.market.set_chain(chain)
        self.portfolio.set_chain(chain)
        self.swap.set_chain(chain)
        self.token.set_chain(chain)
        self.track.set_chain(chain)
    
    def is_authenticated(self) -> bool:
        """检查是否已认证"""
        return self.client.is_authenticated()
    
    def has_private_key(self) -> bool:
        """检查是否有私钥 (用于交易执行)"""
        return self.client.has_private_key()


# 便捷函数
def create_gmgn(api_key: str = None, private_key: str = None) -> GMGN:
    """创建 GMGN 实例"""
    return GMGN(api_key, private_key)


__all__ = ['GMGN', 'GMGNClient', 'create_client', 'create_gmgn']
