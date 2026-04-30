# 信息蒸馏模块 (distill)



> **名称**: taiyi-travel-distill  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 9 源信息蒸馏融合（马蜂窝/穷游/携程/小红书/知乎/TripAdvisor/Lonely Planet/Booking/Airbnb）


## 🎯 职责域



**核心功能**: 国内信息源采集、国外信息源采集、信息蒸馏提炼、融合推荐、置信度评估

**适用场景**:
- 多源信息聚合
- 景点/酒店/餐厅综合评分
- 交叉验证信息可靠性


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `sources.py` | 9 个信息源定义 |
| `extractor.py` | 信息提取 |
| `fusion.py` | 融合算法 |
| `confidence.py` | 置信度评估 |


## 🚀 使用方式



```python
from src.distill.extractor import InfoExtractor
from src.distill.fusion import FusionEngine

extractor = InfoExtractor()
data = extractor.extract(destination="东京", sources=["mafengwo", "tripadvisor"])

fusion = FusionEngine()
result = fusion.fuse(data)
```


## 🔌 依赖



- 无外部依赖


## 📦 发布



```bash
clawhub publish taiyi-travel-distill
```


*太一旅行探路者 · 信息蒸馏模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48