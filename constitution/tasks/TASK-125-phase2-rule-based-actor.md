# RuleBasedActor 自定义实现 - 封装知几-E 策略

> 版本：1.0 | 创建时间：2026-04-04 | 状态：Phase 2

---

## 📋 设计目标

将知几-E 策略封装为 TorchTrade RuleBasedActor，实现：
1. 规则引擎决策（置信度阈值 + EV 阈值）
2. Quarter-Kelly 仓位管理
3. LMSR 浅水区检测
4. 与 TorchTrade 环境集成

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────┐
│      知几-E 策略层 (规则引擎)        │
│  - 置信度计算 (贝叶斯)               │
│  - EV 缺口扫描                       │
│  - LMSR 浅水区检测                   │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│    RuleBasedActor (适配器层)        │
│  - get_action(observation)          │
│  - 策略 → TorchTrade 动作映射        │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│   TorchTrade SequentialTradingEnv   │
│  - 环境状态管理                      │
│  - 回测/实盘执行                     │
└─────────────────────────────────────┘
```

---

## 🔧 核心接口

### TorchTrade Actor 接口
```python
class RuleBasedActor:
    def __init__(self, config):
        """初始化 Actor"""
        pass
    
    def get_action(self, observation, info=None):
        """
        根据观测获取动作
        
        Args:
            observation: 环境观测 (账户状态 + 市场数据)
            info: 额外信息
        
        Returns:
            action: 动作 (0=持有，1=买入，2=卖出)
            confidence: 置信度
        """
        pass
```

### 知几-E 策略接口
```python
class ZhijiEStrategy:
    def __init__(self, config):
        self.confidence_threshold = 0.85  # 85%
        self.edge_threshold = 0.045  # 4.5%
        self.kelly_divisor = 4  # Quarter-Kelly
    
    def calculate_confidence(self, features):
        """计算置信度 (贝叶斯更新)"""
        pass
    
    def calculate_ev(self, market_price, model_prob):
        """计算 EV 缺口"""
        ev = model_prob - market_price
        return ev
    
    def check_shallow_water(self, liquidity, volume):
        """LMSR 浅水区检测"""
        return liquidity < 50 or volume < 50
    
    def quarter_kelly(self, confidence, edge, balance):
        """Quarter-Kelly 仓位计算"""
        kelly_fraction = (confidence * edge - (1 - confidence)) / edge
        return (balance * kelly_fraction) / self.kelly_divisor
    
    def decide(self, observation):
        """
        策略决策
        
        Returns:
            action: 0=持有，1=买入，2=卖出
            position_size: 仓位大小
            confidence: 置信度
        """
        pass
```

---

## 📝 实现代码

### RuleBasedActor 实现
```python
import torch
from torchtrade.envs.core.actor_base import ActorBase
from torchtrade.envs.utils.timeframe import TimeFrame

class RuleBasedActor(ActorBase):
    """
    基于规则的 Actor - 封装知几-E 策略
    """
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.strategy = ZhijiEStrategy(config)
    
    def get_action(self, observation, info=None):
        """
        根据观测获取动作
        
        observation 结构:
        - account_state: [cash, position, pnl, ...]
        - market_data: [10 步 OHLCV]
        """
        # 提取特征
        account_state = observation['account_state']
        market_data = observation['market_data_1Hour_10']
        
        # 策略决策
        action, position_size, confidence = self.strategy.decide(
            account_state=account_state,
            market_data=market_data,
            info=info
        )
        
        # 映射到 TorchTrade 动作空间
        # 0=持有，1=买入，2=卖出
        torch_action = torch.tensor([action])
        
        return {
            'action': torch_action,
            'position_size': position_size,
            'confidence': confidence,
            'metadata': {
                'strategy': 'zhiji-e',
                'version': '2.2'
            }
        }
```

### 知几-E 策略实现
```python
import numpy as np

class ZhijiEStrategy:
    """
    知几-E 策略引擎 v2.2
    """
    
    def __init__(self, config):
        self.confidence_threshold = getattr(config, 'confidence_threshold', 0.85)
        self.edge_threshold = getattr(config, 'edge_threshold', 0.045)
        self.kelly_divisor = getattr(config, 'kelly_divisor', 4)
        self.max_position_pct = getattr(config, 'max_position_pct', 0.25)
        self.shallow_water_threshold = getattr(config, 'shallow_water_threshold', 50)
    
    def decide(self, account_state, market_data, info=None):
        """
        策略决策主函数
        
        Args:
            account_state: [cash, position, pnl, leverage, margin, risk]
            market_data: [10, 5] OHLCV 数据
        
        Returns:
            action: 0=持有，1=买入，2=卖出
            position_size: 仓位大小 (USDT)
            confidence: 置信度 (0-1)
        """
        cash = float(account_state[0])
        current_position = float(account_state[1])
        
        # 1. 计算置信度 (基于市场数据特征)
        confidence = self._calculate_confidence(market_data, info)
        
        # 2. 计算 EV 缺口
        market_price = float(market_data[-1, 3])  # 最新收盘价
        model_prob = self._estimate_model_prob(market_data, info)
        ev = self.calculate_ev(market_price, model_prob)
        
        # 3. LMSR 浅水区检测
        liquidity = info.get('liquidity', float('inf')) if info else float('inf')
        is_shallow = self.check_shallow_water(liquidity)
        
        # 4. 决策逻辑
        if is_shallow:
            # 浅水区 - 观望
            action = 0
            position_size = 0
            confidence = 0
        elif confidence >= self.confidence_threshold and ev >= self.edge_threshold:
            # 高置信度 + 正 EV - 买入
            if current_position <= 0:
                action = 1  # 买入
                position_size = self.quarter_kelly(confidence, ev, cash)
            else:
                action = 0  # 已有仓位，持有
                position_size = 0
        elif confidence <= (1 - self.confidence_threshold) and ev <= -self.edge_threshold:
            # 低置信度 + 负 EV - 卖出/平仓
            if current_position > 0:
                action = 2  # 卖出
                position_size = current_position  # 全平
            else:
                action = 0  # 无仓位，观望
                position_size = 0
        else:
            # 其他情况 - 观望
            action = 0
            position_size = 0
            confidence = 0
        
        return action, position_size, confidence
    
    def _calculate_confidence(self, market_data, info=None):
        """
        计算置信度
        
        简化版本：基于价格趋势 + 波动率
        完整版本：贝叶斯更新 + 多因子模型
        """
        if market_data.shape[0] < 5:
            return 0.5  # 数据不足
        
        # 价格趋势
        closes = market_data[:, 3]  # 收盘价
        trend = (closes[-1] - closes[0]) / closes[0]
        
        # 波动率
        returns = np.diff(closes) / closes[:-1]
        volatility = np.std(returns)
        
        # 简化置信度计算
        confidence = 0.5 + 0.3 * np.tanh(trend / 0.01) - 0.2 * volatility
        
        # 如果有额外信息 (如气象预测)，增强置信度
        if info and 'weather_confidence' in info:
            confidence = 0.7 * confidence + 0.3 * info['weather_confidence']
        
        return np.clip(confidence, 0.1, 0.95)
    
    def _estimate_model_prob(self, market_data, info=None):
        """估计模型概率"""
        # 简化版本：基于趋势外推
        closes = market_data[:, 3]
        trend = (closes[-1] - closes[0]) / closes[0]
        
        # 逻辑斯蒂映射到概率
        model_prob = 1 / (1 + np.exp(-trend * 100))
        
        return model_prob
    
    def calculate_ev(self, market_price, model_prob):
        """计算 EV 缺口"""
        return model_prob - market_price
    
    def check_shallow_water(self, liquidity):
        """LMSR 浅水区检测"""
        return liquidity < self.shallow_water_threshold
    
    def quarter_kelly(self, confidence, edge, balance):
        """
        Quarter-Kelly 仓位计算
        
        Kelly fraction = (p * b - q) / b
        其中 p=置信度，q=1-p，b=赔率 (edge)
        
        Quarter-Kelly: Kelly / 4
        """
        if edge <= 0:
            return 0
        
        p = confidence
        q = 1 - p
        b = edge
        
        kelly_fraction = (p * b - q) / b
        
        if kelly_fraction <= 0:
            return 0
        
        # Quarter-Kelly
        quarter_kelly = kelly_fraction / self.kelly_divisor
        
        # 限制最大仓位
        quarter_kelly = min(quarter_kelly, self.max_position_pct)
        
        position_size = balance * quarter_kelly
        
        return position_size
```

---

## 🔗 集成示例

### 使用 RuleBasedActor 运行回测
```python
from torchtrade.envs import SequentialTradingEnv, SequentialTradingEnvConfig
from rule_based_actor import RuleBasedActor

# 1. 创建环境
config = SequentialTradingEnvConfig(
    symbol='BTC/USD',
    time_frames='1Hour',
    window_sizes=10,
    initial_cash=10000,
    transaction_fee=0.001,
    leverage=1,
)

env = SequentialTradingEnv(df=df, config=config)

# 2. 创建 Actor
actor_config = type('Config', (), {
    'confidence_threshold': 0.85,
    'edge_threshold': 0.045,
    'kelly_divisor': 4,
    'max_position_pct': 0.25,
})()

actor = RuleBasedActor(config=actor_config)

# 3. 运行回测
obs, info = env.reset()
done = False

while not done:
    # Actor 获取动作
    action_output = actor.get_action(obs, info)
    action = action_output['action']
    
    # 环境执行
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

env.close()
```

---

## 📊 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `confidence_threshold` | 0.85 | 置信度阈值 (85%) |
| `edge_threshold` | 0.045 | EV 阈值 (4.5%) |
| `kelly_divisor` | 4 | Quarter-Kelly |
| `max_position_pct` | 0.25 | 最大仓位 (25%) |
| `shallow_water_threshold` | 50 | 浅水区阈值 |

---

## 🧪 测试计划

### 单元测试
- [ ] 置信度计算测试
- [ ] EV 计算测试
- [ ] Kelly 仓位测试
- [ ] 浅水区检测测试

### 集成测试
- [ ] RuleBasedActor + SequentialTradingEnv
- [ ] 回测运行测试
- [ ] 性能基准测试

---

## 📁 文件结构

```
workspace/
├── skills/
│   └── torchtrade-integration/
│       ├── SKILL.md
│       ├── rule_based_actor.py  ← RuleBasedActor 实现
│       └── zhiji_e_strategy.py  ← 知几-E 策略
├── config/
│   └── zhiji-e-torchtrade.yaml  ← 配置文件
└── scripts/
    └── test-rule-based-actor.py ← 测试脚本
```

---

*创建时间：2026-04-04 | 太一 AGI · Phase 2*
