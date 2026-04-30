# 知识自动学习模块 (learn)



> **名称**: taiyi-travel-learn  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 知识自动学习——博主内容/网站内容学习、攻略提取、学习报告


## 🎯 职责域



**核心功能**: 旅游博主内容学习、旅游网站学习、攻略提取、推荐算法更新、学习报告生成

**适用场景**:
- 自动学习旅游博主内容
- 自动学习旅游网站
- 提取旅行攻略/建议
- 生成学习报告


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `blogger.py` | 博主内容学习 |
| `website.py` | 网站学习 |
| `report.py` | 学习报告生成 |


## 🚀 使用方式



```python
from src.learn.blogger import BloggerLearner
from src.learn.website import WebsiteLearner

blogger = BloggerLearner()
blogger.learn(source="小红书", destination="东京")

website = WebsiteLearner()
website.learn(source="马蜂窝", destination="东京")
```


## 🔌 依赖



- `requests`


## 📦 发布



```bash
clawhub publish taiyi-travel-learn
```


*太一旅行探路者 · 知识自动学习模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48