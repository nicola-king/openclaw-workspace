#!/usr/bin/env python3
"""
知几-E 自动投放策略
根据表现自动调整策略参数
"""

import json
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class StrategyConfig:
    """策略配置"""
    name: str
    confidence_threshold: float
    kelly_fraction: float
    max_exposure: float
    stop_loss: float

class AutoStrategyManager:
    """自动策略管理器"""
    
    def __init__(self):
        # 策略模板
        self.templates = {
            'conservative': StrategyConfig(
                name='保守型',
                confidence_threshold=0.98,
                kelly_fraction=0.25,
                max_exposure=0.03,
                stop_loss=0.05
            ),
            'balanced': StrategyConfig(
                name='平衡型',
                confidence_threshold=0.96,
                kelly_fraction=0.50,
                max_exposure=0.05,
                stop_loss=0.10
            ),
            'aggressive': StrategyConfig(
                name='激进型',
                confidence_threshold=0.94,
                kelly_fraction=0.75,
                max_exposure=0.08,
                stop_loss=0.15
            ),
        }
        
        # 当前策略
        self.current = self.templates['balanced']
        
        # 表现追踪
        self.performance_history = []
    
    def adjust_strategy(self, performance: Dict):
        """根据表现调整策略"""
        win_rate = performance.get('win_rate', 0.5)
        roi = performance.get('roi', 0)
        drawdown = performance.get('drawdown', 0)
        
        # 调整逻辑
        if win_rate > 0.6 and roi > 0.1:
            # 表现好，增加风险
            return self._increase_exposure()
        elif win_rate < 0.4 or roi < -0.1:
            # 表现差，降低风险
            return self._decrease_exposure()
        elif drawdown > 0.15:
            # 回撤大，保守
            return self._switch_to('conservative')
        else:
            # 保持当前
            return self.current
    
    def _increase_exposure(self) -> StrategyConfig:
        """增加敞口"""
        if self.current.name == '保守型':
            return self.templates['balanced']
        elif self.current.name == '平衡型':
            return self.templates['aggressive']
        else:
            return self.current
    
    def _decrease_exposure(self) -> StrategyConfig:
        """降低敞口"""
        if self.current.name == '激进型':
            return self.templates['balanced']
        elif self.current.name == '平衡型':
            return self.templates['conservative']
        else:
            return self.current
    
    def _switch_to(self, strategy_name: str) -> StrategyConfig:
        """切换策略"""
        self.current = self.templates[strategy_name]
        return self.current
    
    def get_current_config(self) -> Dict:
        """获取当前配置"""
        return {
            'name': self.current.name,
            'confidence_threshold': self.current.confidence_threshold,
            'kelly_fraction': self.current.kelly_fraction,
            'max_exposure': self.current.max_exposure,
            'stop_loss': self.current.stop_loss,
        }
    
    def record_performance(self, performance: Dict):
        """记录表现"""
        self.performance_history.append({
            'timestamp': datetime.now().isoformat(),
            **performance
        })

class AutoBetExecutor:
    """自动下注执行器"""
    
    def __init__(self, strategy_manager: AutoStrategyManager):
        self.manager = strategy_manager
    
    def should_bet(self, market_data: Dict) -> bool:
        """判断是否下注"""
        config = self.manager.get_current_config()
        
        # 检查置信度
        if market_data['confidence'] < config['confidence_threshold']:
            return False
        
        # 检查敞口
        if market_data['exposure'] > config['max_exposure']:
            return False
        
        # 检查止损
        if market_data['drawdown'] > config['stop_loss']:
            return False
        
        return True
    
    def calculate_bet_size(self, market_data: Dict) -> float:
        """计算下注大小"""
        config = self.manager.get_current_config()
        
        # Kelly 公式
        kelly = market_data['kelly']
        
        # 应用 Kelly 分数
        bet_size = kelly * config['kelly_fraction']
        
        # 限制在最大敞口内
        bet_size = min(bet_size, config['max_exposure'])
        
        return bet_size

# 测试
if __name__ == '__main__':
    manager = AutoStrategyManager()
    executor = AutoBetExecutor(manager)
    
    print("=" * 60)
    print("知几-E 自动投放策略")
    print("=" * 60)
    
    # 当前策略
    config = manager.get_current_config()
    print(f"\n📊 当前策略：{config['name']}")
    print(f"  置信度：{config['confidence_threshold']:.0%}")
    print(f"  Kelly: {config['kelly_fraction']:.2f}")
    print(f"  最大敞口：{config['max_exposure']:.1%}")
    print(f"  止损：{config['stop_loss']:.1%}")
    
    # 模拟表现
    print(f"\n📈 表现调整测试:")
    test_cases = [
        {'win_rate': 0.65, 'roi': 0.15, 'drawdown': 0.05},  # 好
        {'win_rate': 0.35, 'roi': -0.15, 'drawdown': 0.10},  # 差
        {'win_rate': 0.50, 'roi': 0.02, 'drawdown': 0.20},  # 回撤大
    ]
    
    for i, perf in enumerate(test_cases):
        new_strategy = manager.adjust_strategy(perf)
        print(f"  场景{i+1}: {manager.current.name}")
    
    # 下注判断
    print(f"\n💰 下注判断:")
    market = {
        'confidence': 0.97,
        'kelly': 0.20,
        'exposure': 0.04,
        'drawdown': 0.08
    }
    
    should_bet = executor.should_bet(market)
    bet_size = executor.calculate_bet_size(market) if should_bet else 0
    
    print(f"  是否下注：{'✅ 是' if should_bet else '❌ 否'}")
    print(f"  下注大小：{bet_size:.2%}")
    
    print("\n✅ 自动投放策略就绪")
    print("=" * 60)
