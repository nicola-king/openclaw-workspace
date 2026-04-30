# 多城路线优化模块 (router_core)



> **名称**: taiyi-travel-router  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 多城市路线优化引擎（TSP/VRP 算法）


## 🎯 职责域



**核心功能**: 多城市旅行路线优化、时间/成本双目标优化

**适用场景**:
- 多城市串联旅行（如：北京→东京→首尔→曼谷）
- 最短时间路线
- 最低成本路线
- 综合最优路线


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `optimizer.py` | 路线优化引擎（TSP/VRP 算法实现） |


## 🚀 使用方式



```python
from src.router_core.optimizer import RouteOptimizer

optimizer = RouteOptimizer()
route = optimizer.optimize(
    cities=["北京", "东京", "首尔", "曼谷"],
    mode="cost",  # or "time", "balanced"
    travelers=2
)
```


## 🔌 依赖



- 无外部依赖


## 📦 发布



```bash
clawhub publish taiyi-travel-router
```


*太一旅行探路者 · 多城路线优化模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48