# 转化优化中心 (Conversion Optimizer) Skill

## 描述
转化优化：漏斗分析/ROI 追踪/渠道对比/A/B 测试

## 独立运行
```bash
python core.py --task funnel --product "折叠房屋"
```

## 依赖
- cross-border-core: ^9.0.0

## API

### 输入
```json
{
  "task": "funnel",
  "product": "折叠房屋"
}
```

### 输出
```json
{
  "status": "success",
  "funnel": {...},
  "conversion_rate": 0.08
}
```

## 配置
```json
{
  "funnel": {
    "enabled": true,
    "stages": ["awareness", "interest", "decision", "action"]
  },
  "roi": {
    "enabled": true,
    "metrics": ["cost", "revenue", "efficiency"]
  },
  "ab_test": {
    "enabled": true,
    "variables": ["headline", "content", "timing"]
  }
}
```

## 使用示例
```python
from core import ConversionOptimizer

agent = ConversionOptimizer(config_path="config.json")
result = agent.execute(task="funnel", product="折叠房屋")
print(result)
```
