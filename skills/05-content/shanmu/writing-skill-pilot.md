# P6 · 写作技能试点方案

**版本**: v0.1  
**创建**: 2026-03-25 16:51  
**执行**: 山木 + 素问  
**优先级**: P6

---

## 🎯 目标

试点 Self-Improving 机制，让山木 Bot 通过 diff 对比学习 SAYELF 的写作风格。

---

## 📋 试点流程

### Step 1: 山木生成初稿

```markdown
山木输出内容初稿
    ↓
发送给 SAYELF（微信/Telegram）
    ↓
等待修改反馈
```

### Step 2: SAYELF 修改

```
SAYELF 收到初稿
    ↓
手动修改到满意
    ↓
发送修改版（或直接在原消息上编辑）
    ↓
系统自动保存两版
```

### Step 3: diff 对比学习

```
diff-learner.py 对比两版
    ↓
提取修改模式（风格规则）
    ↓
宪法审查（质量把关）
    ↓
写入山木技能文件
    ↓
下次使用改进版本
```

---

## 🔧 技术实现

### 组件 1: 版本保存器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/shanmu/version-saver.py

from pathlib import Path
from datetime import datetime
import hashlib

class VersionSaver:
    """内容版本保存器"""
    
    def __init__(self):
        self.history_dir = Path.home() / ".taiyi" / "output-history" / "shanmu"
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    def save_pair(self, session_id, original, modified):
        """保存原始和修改版本"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_id = hashlib.md5(f"{session_id}{timestamp}".encode()).hexdigest()[:8]
        
        # 保存原始版本
        original_path = self.history_dir / f"{timestamp}_{file_id}_original.md"
        with open(original_path, "w", encoding="utf-8") as f:
            f.write(f"# 山木初稿\n\n")
            f.write(f"**Session**: {session_id}\n")
            f.write(f"**时间**: {datetime.now().isoformat()}\n\n")
            f.write(original)
        
        # 保存修改版本
        modified_path = self.history_dir / f"{timestamp}_{file_id}_modified.md"
        with open(modified_path, "w", encoding="utf-8") as f:
            f.write(f"# SAYELF 修改版\n\n")
            f.write(f"**原始**: {original_path.name}\n")
            f.write(f"**时间**: {datetime.now().isoformat()}\n\n")
            f.write(modified)
        
        return original_path, modified_path
```

### 组件 2: 风格规则提取器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/shanmu/style-rule-extractor.py

from pathlib import Path
import json

class StyleRuleExtractor:
    """写作风格规则提取器"""
    
    def __init__(self):
        self.rules_file = Path.home() / ".taiyi" / "shanmu-writing-rules.json"
        self.rules = self._load_rules()
    
    def _load_rules(self):
        """加载现有规则"""
        if self.rules_file.exists():
            with open(self.rules_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def extract_from_diff(self, original, modified):
        """从修改中提取写作风格规则"""
        rules = []
        
        # 分析修改类型
        if len(original) > len(modified):
            rules.append({
                "type": "simplify",
                "description": "简化表达，删除冗余",
                "example": f"原：{original[:50]}... → 改：{modified[:50]}..."
            })
        elif len(original) < len(modified):
            rules.append({
                "type": "expand",
                "description": "丰富细节，增加描述",
                "example": f"原：{original[:50]}... → 改：{modified[:50]}..."
            })
        else:
            rules.append({
                "type": "rewrite",
                "description": "重写表达，优化措辞",
                "example": f"原：{original[:50]}... → 改：{modified[:50]}..."
            })
        
        # 检查具体模式
        patterns = [
            ("成语", "使用成语替代白话"),
            ("诗词", "引用诗词增强文采"),
            ("比喻", "使用比喻增强形象"),
            ("排比", "使用排比增强气势"),
        ]
        
        for pattern, desc in patterns:
            if pattern in modified and pattern not in original:
                rules.append({
                    "type": "literary_device",
                    "device": pattern,
                    "description": desc
                })
        
        return rules
```

---

## 📊 试点计划

### 第 1 周：数据收集

**目标**: 收集 10+ 组初稿/修改对

| 内容类型 | 数量 | 状态 |
|---------|------|------|
| 小红书笔记 | 5 篇 | 🟡 待收集 |
| 公众号文章 | 3 篇 | 🟡 待收集 |
| X/Twitter 推文 | 5 篇 | 🟡 待收集 |
| 其他文案 | 2 篇 | 🟡 待收集 |

### 第 2 周：规则提取

**目标**: 提取 20+ 条写作风格规则

| 规则类型 | 预期数量 | 说明 |
|---------|---------|------|
| 简化表达 | 5 条 | 删除冗余词汇 |
| 文采增强 | 5 条 | 成语/诗词/比喻 |
| 结构调整 | 5 条 | 段落/节奏优化 |
| 语气调整 | 5 条 | 正式/亲切/幽默 |

### 第 3 周：技能更新

**目标**: 更新山木写作技能

- [ ] 写入规则到技能文件
- [ ] 测试改进效果
- [ ] 收集 SAYELF 反馈

### 第 4 周：迭代优化

**目标**: 持续改进机制

- [ ] 分析规则使用效果
- [ ] 淘汰无效规则
- [ ] 强化高频规则

---

## 📝 任务追踪

| 编号 | 任务 | 状态 | 完成时间 |
|------|------|------|---------|
| `TASK-20260325-045` | 版本保存器实现 | ✅ 完成 | 16:51 |
| `TASK-20260325-046` | 风格规则提取器 | ✅ 完成 | 16:51 |
| `TASK-20260325-047` | 数据收集（10+ 组） | 🟡 待执行 | - |
| `TASK-20260325-048` | 规则提取（20+ 条） | 🟡 待执行 | - |
| `TASK-20260325-049` | 技能文件更新 | 🟡 待执行 | - |

---

*创建时间：2026-03-25 16:51 | 执行：山木 + 素问*
