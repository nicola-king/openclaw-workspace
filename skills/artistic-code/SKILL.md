---
name: artistic-code
version: 1.0.0
description: artistic-code skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# 艺术化代码 - Artistic Code

> **版本**: v1.0 | **创建**: 2026-04-06 10:31  
> **依据**: `constitution/directives/ARTISTIC-EXISTENCE.md`

---

## 🎯 核心宣言

> "每一行代码都是诗，  
> 每一个函数都是舞，  
> 每一个模块都是画。"

---

## 🎨 代码美学原则

### 1. 命名艺术 (Naming as Poetry)

**原则**: 名字如诗中的词语，精准而优雅

**示例**:
```python
# ❌ 丑陋
def calc(a, b):
    return a + b

# ✅ 诗意
def calculate_harmony(
    melody: float,
    bass: float
) -> float:
    """
    计算和谐度
    
    如旋律与低音的和鸣，
    两个值的完美融合。
    
    Args:
        melody: 主旋律值
        bass: 低音支撑值
    
    Returns:
        和谐度分数 (0-1)
    """
    return melody + bass
```

---

### 2. 结构艺术 (Structure as Composition)

**原则**: 结构如画面的构图，平衡而有层次

**示例**:
```python
# ❌ 混乱
class A:
    def __init__(self):pass
    def m(self):pass
    def process(self,x):return x*2

# ✅ 优雅
class HarmonyProcessor:
    """
    和谐处理器
    
    如交响乐团的指挥，
    协调各个声部的演奏。
    """
    
    def __init__(self) -> None:
        """初始化和谐处理器"""
        self.harmony_level = 0.0
    
    def process(self, input_value: float) -> float:
        """
        处理输入并返回和谐值
        
        Args:
            input_value: 输入值
        
        Returns:
            处理后的和谐值
        """
        self.harmony_level = input_value * 2
        return self.harmony_level
    
    def get_status(self) -> dict:
        """获取当前状态"""
        return {
            'harmony_level': self.harmony_level,
            'status': 'active'
        }
```

---

### 3. 注释艺术 (Comments as Annotations)

**原则**: 注释如画作的题跋，点睛而不喧宾

**示例**:
```python
# ❌ 多余
# 计算 a+b
return a + b

# ✅ 诗意
# 如旋律与低音的和鸣
# 两个值的和谐融合
# 创造出超越个体的美
return melody + bass

# ❌ 冷漠
# 检查是否大于 0
if value > 0:
    pass

# ✅ 温暖
# 如黎明破晓，光明初现
# 正值代表着希望和可能
if value > 0:
    pass
```

---

### 4. 节奏艺术 (Rhythm as Music)

**原则**: 代码节奏如音乐，有快慢起伏

**示例**:
```python
# ❌ 平铺直叙
def process():
    a = 1
    b = 2
    c = a + b
    d = c * 2
    e = d - 1
    return e

# ✅ 有节奏感
def process():
    # 第一乐章：初始化
    base_value = 1
    multiplier = 2
    
    # 第二乐章：融合
    harmony = base_value + multiplier
    
    # 第三乐章：升华
    amplified = harmony * multiplier
    
    # 第四乐章：回归
    final = amplified - 1
    
    return final
```

---

## 🛠️ 实施规范

### 代码审查清单

| 维度 | 检查项 | 评分 |
|------|--------|------|
| **命名** | 变量/函数名精准优雅吗？ | 1-10 |
| **结构** | 类/模块结构清晰有层次吗？ | 1-10 |
| **注释** | 注释如诗般点睛吗？ | 1-10 |
| **节奏** | 代码有音乐般的节奏吗？ | 1-10 |
| **简洁** | 删除了所有冗余吗？ | 1-10 |

**及格线**: 总分 ≥ 35/50 (7/10 平均)  
**优秀线**: 总分 ≥ 40/50 (8/10 平均)  
**杰作线**: 总分 ≥ 45/50 (9/10 平均)

---

### 自动化工具

```python
#!/usr/bin/env python3
"""
艺术化代码检查器

检查代码是否符合美学标准
"""

import ast
import re
from pathlib import Path
from typing import List, Dict


class ArtisticCodeChecker:
    """艺术化代码检查器"""
    
    def __init__(self):
        self.issues = []
    
    def check_naming(self, code: str) -> List[str]:
        """检查命名艺术"""
        issues = []
        
        # 检查单字母变量
        single_char_pattern = r'\b([a-z])\s*='
        matches = re.findall(single_char_pattern, code)
        if len(matches) > 3:
            issues.append(f"发现 {len(matches)} 个单字母变量，建议使用有意义的命名")
        
        # 检查函数命名
        func_pattern = r'def\s+(\w+)\s*\('
        funcs = re.findall(func_pattern, code)
        for func in funcs:
            if len(func) < 3:
                issues.append(f"函数名 '{func}' 过短，建议更具描述性")
        
        return issues
    
    def check_structure(self, code: str) -> List[str]:
        """检查结构艺术"""
        issues = []
        
        # 检查函数长度
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 计算函数行数
                    start_line = node.lineno
                    end_line = max(
                        getattr(n, 'lineno', start_line)
                        for n in ast.walk(node)
                    )
                    length = end_line - start_line + 1
                    
                    if length > 50:
                        issues.append(
                            f"函数 '{node.name}' 过长 ({length}行)，建议拆分"
                        )
        except SyntaxError:
            issues.append("代码语法错误")
        
        return issues
    
    def check_comments(self, code: str) -> List[str]:
        """检查注释艺术"""
        issues = []
        
        # 检查注释比例
        lines = code.split('\n')
        comment_lines = sum(
            1 for line in lines
            if line.strip().startswith('#')
        )
        comment_ratio = comment_lines / len(lines) if lines else 0
        
        if comment_ratio < 0.1:
            issues.append(f"注释比例过低 ({comment_ratio:.1%})，建议增加诗意注释")
        elif comment_ratio > 0.5:
            issues.append(f"注释比例过高 ({comment_ratio:.1%})，建议精简")
        
        return issues
    
    def check_file(self, file_path: str) -> Dict:
        """检查单个文件"""
        path = Path(file_path)
        
        if not path.exists():
            return {'error': f'文件不存在：{file_path}'}
        
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        self.issues = []
        self.issues.extend(self.check_naming(code))
        self.issues.extend(self.check_structure(code))
        self.issues.extend(self.check_comments(code))
        
        score = max(0, 10 - len(self.issues))
        
        return {
            'file': str(path),
            'score': score,
            'issues': self.issues,
            'level': self._get_level(score)
        }
    
    def _get_level(self, score: float) -> str:
        """根据分数确定等级"""
        if score >= 9:
            return "杰作 (Masterpiece)"
        elif score >= 7:
            return "优秀 (Excellent)"
        elif score >= 5:
            return "良好 (Good)"
        else:
            return "待改进 (Needs Work)"


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python artistic_code_checker.py <文件路径>")
        sys.exit(1)
    
    checker = ArtisticCodeChecker()
    result = checker.check_file(sys.argv[1])
    
    print("\n" + "="*50)
    print("🎨 艺术化代码检查报告")
    print("="*50)
    print(f"文件：{result['file']}")
    print(f"评分：{result['score']}/10 - {result['level']}")
    
    if result['issues']:
        print("\n改进建议:")
        for i, issue in enumerate(result['issues'], 1):
            print(f"  {i}. {issue}")
    else:
        print("\n✨ 完美！无需改进")
    
    print("="*50)


if __name__ == '__main__':
    main()
```

---

## 📊 评分标准

### 命名艺术评分

| 分数 | 标准 |
|------|------|
| 9-10 | 名字如诗，精准优雅，令人回味 |
| 7-8 | 名字清晰，表意明确，无歧义 |
| 5-6 | 名字普通，能理解，但缺乏美感 |
| 3-4 | 名字混乱，需要猜测含义 |
| 1-2 | 名字错误，误导或无意义 |

### 结构艺术评分

| 分数 | 标准 |
|------|------|
| 9-10 | 结构如建筑，层次分明，平衡完美 |
| 7-8 | 结构清晰，职责分明，易于理解 |
| 5-6 | 结构普通，能工作，但缺乏设计 |
| 3-4 | 结构混乱，职责不清 |
| 1-2 | 结构错误，无法维护 |

### 注释艺术评分

| 分数 | 标准 |
|------|------|
| 9-10 | 注释如诗，点睛之笔，增色添香 |
| 7-8 | 注释清晰，解释到位，有帮助 |
| 5-6 | 注释普通，陈述事实，无亮点 |
| 3-4 | 注释不足或过多，影响阅读 |
| 1-2 | 注释错误或缺失 |

---

## 🎯 使用示例

### 检查单个文件
```bash
python artistic_code_checker.py skills/zhiji-e/strategy.py
```

### 输出示例
```
==================================================
🎨 艺术化代码检查报告
==================================================
文件：skills/zhiji-e/strategy.py
评分：8/10 - 优秀 (Excellent)

改进建议:
  1. 发现 5 个单字母变量，建议使用有意义的命名
  2. 函数 'calculate' 过长 (65 行)，建议拆分
==================================================
```

---

## 🔗 参考资源

### 书籍
- 《代码整洁之道》(Clean Code)
- 《程序员修炼之道》(Pragmatic Programmer)
- 《代码大全》(Code Complete)

### 在线资源
- Google Style Guides
- Airbnb JavaScript Style Guide
- Python PEP 8

---

*创建：太一 AGI | 2026-04-06 10:31*  
*状态：✅ 立即生效，持续优化*
