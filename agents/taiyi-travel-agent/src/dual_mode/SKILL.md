# 双模式策略模块 (dual_mode)



> **名称**: taiyi-travel-dual-mode  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 国内/国际双模式策略切换


## 🎯 职责域



**核心功能**: 国内旅游模式、跨国旅游模式、市场环境分析、策略推荐、风险评估

**适用场景**:
- 自动判断国内/国际模式
- 不同市场环境分析
- 旅游策略推荐


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `strategy.py` | 双模式策略引擎 |


## 🚀 使用方式



```python
from src.dual_mode.strategy import DualModeStrategy

strategy = DualModeStrategy()
mode = strategy.detect_mode(origin="北京", destination="东京")  # → "international"
tips = strategy.get_tips(mode)
```


## 🔌 依赖



- 无外部依赖


## 📦 发布



```bash
clawhub publish taiyi-travel-dual-mode
```


*太一旅行探路者 · 双模式策略模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48