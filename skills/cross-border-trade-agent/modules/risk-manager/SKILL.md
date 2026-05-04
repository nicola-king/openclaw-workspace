# risk-manager Skill

## 描述
风险管理与对冲引擎：风险识别·预警系统·对冲策略·二阶思维分析

## 蒸馏来源
- 宪法层：二阶思维（预判后果的后果）+ 冰山理论（关注底层结构）
- 天机系统：聪明钱追踪 + 市场机会识别
- 知几情绪：市场情绪分析
- 太一系统：反封号策略 → 操作风险防控

## 独立运行
```bash
python core.py --task risk --product "折叠房屋" --market "澳大利亚"
```

## 依赖
- cross-border-core: ^10.0.0
- intelligence-hub: ^10.0.0

## 核心能力

### 1. 风险识别
- 市场风险（需求波动/竞争加剧）
- 政策风险（关税变化/法规调整）
- 汇率风险（汇率波动/支付安全）
- 供应链风险（供应商中断/物流延迟）
- 操作风险（合规违规/账号封禁）

### 2. 预警系统
- 实时风险评分
- 多级预警（绿/黄/橙/红）
- 自动通知推送

### 3. 对冲策略
- 市场多元化（降低单一市场依赖）
- 汇率对冲（远期合约/期权）
- 供应链备份（多供应商策略）
- 合规对冲（提前获取认证）

### 4. 二阶思维分析
- 直接后果分析
- 间接后果推演
- 连锁反应预测
- 最坏情景模拟

## API

### 输入
```json
{
  "task": "risk",
  "product": "折叠房屋",
  "market": "澳大利亚",
  "risk_types": ["market", "policy", "exchange", "supply", "operation"]
}
```

### 输出
```json
{
  "status": "success",
  "overall_risk_score": 35,
  "risk_level": "LOW",
  "risks": [
    {"type": "policy", "score": 45, "level": "MEDIUM", "description": "关税可能上调"},
    {"type": "market", "score": 25, "level": "LOW", "description": "市场需求稳定"}
  ],
  "hedge_strategies": [...],
  "second_order_effects": [...],
  "alert": null
}
```

## 配置
```json
{
  "risk": {
    "enabled": true,
    "check_interval": 3600,
    "alert_threshold": 70
  },
  "hedge": {
    "enabled": true,
    "max_risk_exposure": 0.3,
    "diversification_target": 5
  },
  "second_order": {
    "enabled": true,
    "depth": 3,
    "scenario_count": 5
  }
}
```

## 使用示例
```python
from core import RiskManager

manager = RiskManager(config_path="config.json")

# 风险评估
result = manager.assess(
    product="折叠房屋",
    market="澳大利亚",
    risk_types=["market", "policy", "exchange"]
)

# 二阶思维分析
effects = manager.second_order_analysis(
    decision="进入澳大利亚市场",
    depth=3
)

# 对冲策略生成
strategies = manager.generate_hedge_strategies(
    risks=result["risks"]
)
```
