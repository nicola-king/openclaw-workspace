# 📐 太一代码规范 v2.0 - Karpathy 极简主义融合

> **版本**: v2.0 (Karpathy 风格)  
> **创建**: 2026-04-18 19:20  
> **灵感**: Karpathy/autoresearch  
> **状态**: ✅ 强制执行

---

## 🎯 核心原则

### Karpathy 代码哲学

```
✅ 极简 - 代码不超过 1000 行
✅ 可读 - 初中生都能看懂
✅ 可 hack - 30 分钟内理解并修改
✅ 无黑箱 - 所有逻辑透明
✅ 递归改进 - fork 后持续进化
```

---

## 📏 代码规模限制

### 模块大小

| 类型 | 最大行数 | 太一现状 | 改进 |
|------|---------|---------|------|
| **核心模块** | 1000 行 | ~500 行 ✅ | 保持 |
| **工具函数** | 200 行 | ~100 行 ✅ | 保持 |
| **配置文件** | 100 行 | ~50 行 ✅ | 保持 |
| **文档** | 500 行 | ~300 行 ✅ | 保持 |

---

## 📝 代码风格规范

### 1. 函数设计

```python
# ✅ 好：单一职责，不超过 50 行
def calculate_score(lead: Dict) -> int:
    """计算线索评分 (0-100)"""
    score = 0
    score += evaluate_company(lead) * 0.2
    score += evaluate_demand(lead) * 0.3
    score += evaluate_budget(lead) * 0.3
    score += evaluate_history(lead) * 0.2
    return int(score)

# ❌ 差：多功能，超过 100 行
def process_everything():
    # ... 100 行代码 ...
```

---

### 2. 类设计

```python
# ✅ 好：单一职责，不超过 300 行
class LeadScorer:
    """线索评分器"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def score(self, lead: Dict) -> int:
        """评分主函数"""
        pass
    
    def _evaluate_company(self, lead: Dict) -> int:
        """评估公司"""
        pass

# ❌ 差：上帝类，超过 1000 行
class EverythingManager:
    # ... 管理所有事情 ...
```

---

### 3. 注释规范

```python
# ✅ 好：解释为什么，不是做什么
# 使用加权平均，因为不同维度重要性不同
score = sum(dim * weight for dim, weight in dimensions)

# ❌ 差：重复代码
score = score + 10  # 加 10 分
```

---

### 4. 命名规范

```python
# ✅ 好：见名知义
def calculate_lead_score(lead: Dict) -> int:
    pass

# ❌ 差：缩写/模糊
def calc(d: Dict) -> int:
    pass
```

---

## 🔧 可 Hack 设计

### 1. 配置驱动

```python
# ✅ 好：配置与代码分离
# config.json
{
    "scoring_weights": {
        "company": 0.2,
        "demand": 0.3,
        "budget": 0.3,
        "history": 0.2
    }
}

# 代码
def load_config():
    with open("config.json") as f:
        return json.load(f)
```

---

### 2. 插件架构

```python
# ✅ 好：易于扩展
class SkillPlugin:
    """技能插件基类"""
    def execute(self):
        raise NotImplementedError

# 用户可轻松添加新插件
class MyCustomPlugin(SkillPlugin):
    def execute(self):
        # 自定义逻辑
        pass
```

---

### 3. 测试友好

```python
# ✅ 好：易于测试
def calculate_score(lead: Dict, weights: Dict = None) -> int:
    """
    计算线索评分
    
    Args:
        lead: 线索信息
        weights: 权重配置 (可选，便于测试)
    
    Returns:
        评分 (0-100)
    """
    pass

# 测试
def test_calculate_score():
    lead = {"company": "TechCorp"}
    score = calculate_score(lead, weights={"company": 1.0})
    assert score == 100
```

---

## 📚 文档规范

### 1. README 结构

```markdown
# 项目名称

一句话描述项目

## 🚀 快速开始

```bash
# 3 步运行
pip install -r requirements.txt
python main.py
```

## 📦 核心功能

- 功能 1
- 功能 2
- 功能 3

## 🔧 配置

```json
{
    "key": "value"
}
```

## 📝 使用示例

```python
from module import Class
obj = Class()
obj.method()
```

## 🤝 贡献

欢迎 Fork 并改进！
```

---

### 2. 代码内文档

```python
class LeadScorer:
    """
    线索评分器
    
    基于 8 维度评估线索质量:
    - 公司信息 (20 分)
    - 需求匹配 (30 分)
    - 预算意向 (30 分)
    - 互动历史 (20 分)
    
    使用示例:
        scorer = LeadScorer(config)
        score = scorer.score(lead)
    """
    
    def score(self, lead: Dict) -> int:
        """
        计算线索评分
        
        Args:
            lead: 线索字典，包含公司/需求/预算等信息
        
        Returns:
            评分 (0-100 分)
        
        Raises:
            ValueError: 当线索数据不完整时
        """
        pass
```

---

## 🔄 递归改进机制

### 1. Fork 友好

```
项目结构:
├── core/           # 核心代码 (不可变)
├── plugins/        # 插件目录 (可扩展)
├── configs/        # 配置文件 (可修改)
├── tests/          # 测试用例 (可参考)
└── examples/       # 使用示例 (可学习)
```

---

### 2. 改进指南

```markdown
## 如何改进本项目

### 1. Fork 项目

```bash
git fork https://github.com/nicola-king/taiyi
```

### 2. 添加功能

```python
# 在 plugins/ 目录添加新插件
class MyPlugin(SkillPlugin):
    def execute(self):
        # 你的逻辑
        pass
```

### 3. 提交改进

```bash
git commit -m "✨ 添加新功能"
git push
```

### 4. 发起 PR

描述你的改进...
```

---

## 📊 代码质量检查清单

### 自查清单

```
□ 代码是否<1000 行？
□ 函数是否<50 行？
□ 类是否<300 行？
□ 是否有完整 docstring？
□ 是否有使用示例？
□ 是否配置与代码分离？
□ 是否易于测试？
□ 是否易于扩展？
□ 初中生能否看懂？
□ 30 分钟内能否 hack？
```

---

## 🎯 与 Karpathy 对比

| 维度 | Karpathy | 太一 v2.0 | 差距 |
|------|---------|----------|------|
| **代码行数** | ~500 行 | ~1000 行 | -50% |
| **注释密度** | 高 | 中 | 待提升 |
| **示例数量** | 丰富 | 中等 | 待提升 |
| **可 hack 性** | 极高 | 高 | 待提升 |
| **文档完整** | 完整 | 完整 | ✅ |

---

## 🚀 改进行动

### 本周执行 (P0)

```
□ 简化跨境贸易 Agent 核心代码
□ 添加更多使用示例
□ 增强 docstring 注释
□ 创建 hack 指南
```

---

### 本月执行 (P1)

```
□ 重构超大模块 (>1000 行)
□ 添加交互式教程
□ 创建视频演示
□ 建立改进案例库
```

---

## 🎊 总结

### 核心原则

```
✅ 极简 - 代码不超过 1000 行
✅ 可读 - 初中生都能看懂
✅ 可 hack - 30 分钟内理解并修改
✅ 无黑箱 - 所有逻辑透明
✅ 递归改进 - fork 后持续进化
```

---

### 开源最高境界

```
一个人的代码 → 全世界的进化树

Karpathy autoresearch: 71k⭐ 10k🍴
Garry Tan gstack:     73k⭐ 10k🍴
太一 AGI:              进行中...
```

---

**📐 太一代码规范 v2.0 - 向 Karpathy 学习！**

**太一 AGI · 2026-04-18 19:20**
