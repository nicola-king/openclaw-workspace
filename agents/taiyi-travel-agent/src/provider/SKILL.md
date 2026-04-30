# 供应商管理模块 (provider)



> **名称**: taiyi-travel-provider  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 供应商注册/审核/搜索 CLI


## 🎯 职责域



**核心功能**: 酒店/餐厅/租车/导游/包车供应商入驻、审核、搜索

**适用场景**:
- 新供应商注册
- 供应商审核
- 供应商搜索


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `cli.py` | CLI 入口 |
| `registry.py` | 供应商注册/审核 |
| `models.py` | 数据模型 |


## 🚀 使用方式



### CLI



```bash
python3 -m src.provider.cli hotel register --name "XX 酒店" --location "东京" --price 500
python3 -m src.provider.list guide --location "东京"
```

### Python



```python
from src.provider.registry import ProviderRegistry

registry = ProviderRegistry()
registry.register("hotel", name="XX 酒店", location="东京", price=500)
```


## 🔌 依赖



- 无外部依赖


## 📦 发布



```bash
clawhub publish taiyi-travel-provider
```


*太一旅行探路者 · 供应商管理模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48