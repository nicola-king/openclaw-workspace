#!/usr/bin/env python3
"""
RuleBasedActor - 封装知几-E 策略
版本：1.1 | 创建时间：2026-04-04 | 修复：EV 计算
用途：将知几-E 策略集成到 TorchTrade 环境
"""

import torch
import numpy as np
from typing import Dict, Any, Optional, Tuple


class ZhijiEStrategy:
    """
    知几-E 策略引擎 v2.2
    
    核心逻辑:
    1. 置信度计算 (趋势 + 动量 + 波动率)
    2. EV 缺口扫描 (模型概率 vs 中性概率)
    3. LMSR 浅水区检测
    4. Quarter-Kelly 仓位管理
    """
    
    def __init__(self, config):
        self.confidence_threshold = getattr(config, 'confidence_threshold', 0.55)
        self.edge_threshold = getattr(config, 'edge_threshold', 0.05)  # EV > 5%
        self.kelly_divisor = getattr(config, 'kelly_divisor', 4)
        self.max_position_pct = getattr(config, 'max_position_pct', 0.25)
        self.shallow_water_threshold = getattr(config, 'shallow_water_threshold', 50)
    
    def decide(
        self,
        account_state: np.ndarray,
        market_data: np.ndarray,
        info: Optional[Dict[str, Any]] = None
    ) -> Tuple[int, float, float]:
        """策略决策"""
        cash = float(account_state[0])
        current_position = float(account_state[1])
        
        # 1. 计算置信度
        confidence = self._calculate_confidence(market_data, info)
        
        # 2. 计算模型概率和 EV
        model_prob = self._estimate_model_prob(market_data, info)
        ev = model_prob - 0.5  # EV = 模型概率 - 中性概率 (0.5)
        
        # 3. 浅水区检测
        liquidity = info.get('liquidity', float('inf')) if info else float('inf')
        is_shallow = self.check_shallow_water(liquidity)
        
        # 4. 决策
        if is_shallow:
            action, position_size = 0, 0.0
        elif confidence >= self.confidence_threshold and ev >= self.edge_threshold:
            if current_position <= 0:
                action, position_size = 1, self.quarter_kelly(confidence, ev, cash)
            else:
                action, position_size = 0, 0.0
        elif confidence <= (1 - self.confidence_threshold) and ev <= -self.edge_threshold:
            if current_position > 0:
                action, position_size = 2, abs(current_position)
            else:
                action, position_size = 0, 0.0
        else:
            action, position_size = 0, 0.0
        
        return action, position_size, confidence
    
    def _calculate_confidence(self, market_data: np.ndarray, info: Optional[Dict] = None) -> float:
        """置信度计算 (收益率形式数据)"""
        if market_data.shape[0] < 5:
            return 0.5
        
        closes = market_data[:, 3]  # 已经是收益率形式 (0 附近)
        trend = closes[-1] - closes[0]  # 直接计算差值
        
        # 波动率
        returns = np.diff(closes)
        volatility = np.std(returns)
        
        # 动量
        momentum = np.mean(returns[-3:]) if len(returns) >= 3 else (returns[-1] if len(returns) > 0 else 0)
        
        # 置信度
        confidence = 0.5 + 0.25 * np.tanh(trend * 50) + 0.15 * np.tanh(momentum * 50) - 0.1 * volatility
        
        if info and 'weather_confidence' in info:
            confidence = 0.6 * confidence + 0.4 * info['weather_confidence']
        
        return float(np.clip(confidence, 0.1, 0.95))
    
    def _estimate_model_prob(self, market_data: np.ndarray, info: Optional[Dict] = None) -> float:
        """模型概率估计 (收益率形式数据)"""
        closes = market_data[:, 3]
        trend = closes[-1] - closes[0]  # 收益率形式
        returns = np.diff(closes)
        momentum = np.mean(returns[-3:]) if len(returns) >= 3 else 0
        
        model_prob = 1 / (1 + np.exp(-(trend * 50 + momentum * 25)))
        return float(np.clip(model_prob, 0.1, 0.95))
    
    def check_shallow_water(self, liquidity: float) -> bool:
        return liquidity < self.shallow_water_threshold
    
    def quarter_kelly(self, confidence: float, edge: float, balance: float) -> float:
        """Quarter-Kelly 仓位 (简化版：Kelly ≈ EV)"""
        if edge <= 0 or confidence <= 0.5:
            return 0.0
        
        # 简化 Kelly: 当 p≈0.5 时，Kelly ≈ EV
        kelly_fraction = edge
        
        # Quarter-Kelly
        quarter_kelly = min(kelly_fraction / self.kelly_divisor, self.max_position_pct)
        
        return float(balance * quarter_kelly)


class RuleBasedActor:
    """RuleBasedActor - 封装知几-E 策略"""
    
    def __init__(self, config=None):
        if config is None:
            config = type('Config', (), {})()
        self.config = config
        self.strategy = ZhijiEStrategy(config)
    
    def get_action(self, observation: Dict[str, Any], info: Optional[Dict] = None) -> Dict:
        """获取动作"""
        if isinstance(observation, dict):
            account_state = observation.get('account_state', np.zeros(6))
            market_data = observation.get('market_data_1Hour_10', np.zeros((10, 5)))
        else:
            account_state = observation['account_state'].numpy()
            market_data = observation['market_data_1Hour_10'].numpy()
        
        action, position_size, confidence = self.strategy.decide(account_state, market_data, info)
        
        return {
            'action': torch.tensor([action], dtype=torch.int64),
            'position_size': position_size,
            'confidence': confidence,
            'metadata': {'strategy': 'zhiji-e', 'version': '2.2'}
        }


class ZhijiEActorConfig:
    """配置类"""
    def __init__(self, confidence_threshold=0.55, edge_threshold=0.05, kelly_divisor=4, max_position_pct=0.25, shallow_water_threshold=50):
        self.confidence_threshold = confidence_threshold
        self.edge_threshold = edge_threshold
        self.kelly_divisor = kelly_divisor
        self.max_position_pct = max_position_pct
        self.shallow_water_threshold = shallow_water_threshold
