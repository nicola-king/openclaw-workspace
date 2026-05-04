# supply-chain Skill

## 描述
供应链全链路管理引擎：供应商管理·库存优化·物流调度·需求预测

## 蒸馏来源
- 交易引擎：物流优化 + 供应商匹配
- 金融情报：销售预测 + 库存分析
- 天机系统：市场趋势预测
- 太一系统：冰山理论（关注供应链底层结构）

## 独立运行
```bash
python core.py --task optimize --product "折叠房屋" --market "澳大利亚"
```

## 依赖
- cross-border-core: ^10.0.0
- transaction-support: ^10.0.0

## 核心能力

### 1. 供应商管理
- 供应商评估与分级
- 多供应商对比
- 绩效追踪
- 风险预警

### 2. 库存优化
- 安全库存计算
- 补货策略
- 库存周转分析
- 滞销预警

### 3. 物流调度
- 运输方式优化
- 路线规划
- 时效预测
- 成本优化

### 4. 需求预测
- 基于市场趋势的需求预测
- 季节性调整
- 安全库存动态调整
- 供应链弹性评估

## API

### 输入
```json
{
  "task": "optimize",
  "product": "折叠房屋",
  "market": "澳大利亚",
  "suppliers": ["supplier_a", "supplier_b"]
}
```

### 输出
```json
{
  "status": "success",
  "supply_chain_score": 82,
  "suppliers": [...],
  "inventory_optimization": {...},
  "logistics_plan": {...},
  "demand_forecast": {...},
  "risks": [...]
}
```

## 配置
```json
{
  "supply_chain": {
    "enabled": true,
    "auto_optimize": true,
    "review_interval": 604800
  },
  "inventory": {
    "safety_stock_days": 30,
    "reorder_point_method": "EOQ",
    "abc_classification": true
  },
  "logistics": {
    "optimize_mode": "cost",
    "max_transit_time": 45,
    "multi_modal": true
  }
}
```

## 使用示例
```python
from core import SupplyChainManager

manager = SupplyChainManager(config_path="config.json")

# 供应链优化
result = manager.optimize(
    product="折叠房屋",
    market="澳大利亚",
    suppliers=["supplier_a", "supplier_b"]
)

# 库存优化
inventory = manager.optimize_inventory(
    product="折叠房屋",
    current_stock=100,
    lead_time=30
)

# 需求预测
forecast = manager.demand_forecast(
    product="折叠房屋",
    market="Australia",
    horizon_months=6
)
```
