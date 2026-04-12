# P4 · Self-Improving 架构设计

**版本**: v0.1  
**创建**: 2026-03-25 16:44  
**执行**: 太一 + 素问  
**优先级**: P4

---

## 🎯 目标

实现太一自我改进机制：AI 输出 → 人工修改 → diff 对比 → 规则提取 → 自动写回 → 持续进化

---

## 📋 架构设计

### 核心流程

```
太一输出初稿
    ↓
SAYELF 修改（微信/Telegram）
    ↓
自动保存两版（original + modified）
    ↓
diff 对比分析
    ↓
提取修改模式（规则）
    ↓
宪法审查（质量把关）
    ↓
写入 MEMORY.md / 更新技能
    ↓
下次使用改进版本
```

---

## 🔧 技术实现

### 组件 1: 版本追踪器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/suwen/version-tracker.py

import json
import hashlib
from pathlib import Path
from datetime import datetime

class VersionTracker:
    """输出版本追踪器"""
    
    def __init__(self):
        self.history_dir = Path.home() / ".taiyi" / "output-history"
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    def save_output(self, session_id, content, role="assistant"):
        """保存输出（原始版本）"""
        timestamp = datetime.now().isoformat()
        file_id = hashlib.md5(f"{session_id}{timestamp}".encode()).hexdigest()[:8]
        
        file_path = self.history_dir / f"{session_id}_{file_id}_original.md"
        with open(file_path, "w") as f:
            f.write(f"# Original Output\n\n")
            f(f"**Session**: {session_id}\n")
            f(f"**Time**: {timestamp}\n")
            f(f"**Role**: {role}\n\n")
            f.write(content)
        
        return file_path
    
    def save_modification(self, original_path, modified_content):
        """保存修改版本"""
        modified_path = original_path.with_name(original_path.stem.replace("_original", "_modified") + ".md")
        
        with open(modified_path, "w") as f:
            f.write(f"# Modified Output\n\n")
            f.write(f"**Original**: {original_path.name}\n")
            f(f"**Time**: {datetime.now().isoformat()}\n\n")
            f.write(modified_content)
        
        return modified_path
    
    def get_pairs(self, session_id=None):
        """获取成对的原始/修改文件"""
        pairs = []
        for original in self.history_dir.glob("*_original.md"):
            modified = original.with_name(original.stem.replace("_original", "_modified") + ".md")
            if modified.exists():
                pairs.append({
                    "original": original,
                    "modified": modified,
                    "session": session_id or original.stem.split("_")[0]
                })
        return pairs
```

---

### 组件 2: diff 对比学习器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/suwen/diff-learner.py

import difflib
from pathlib import Path

class DiffLearner:
    """diff 对比学习器"""
    
    def __init__(self):
        pass
    
    def compare_versions(self, original_path, modified_path):
        """对比两个版本，返回差异"""
        with open(original_path, "r") as f:
            original_lines = f.readlines()
        
        with open(modified_path, "r") as f:
            modified_lines = f.readlines()
        
        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile="original",
            tofile="modified",
            lineterm=""
        )
        
        return list(diff)
    
    def extract_patterns(self, diff_lines):
        """从 diff 中提取修改模式"""
        patterns = []
        
        current_hunk = []
        for line in diff_lines:
            if line.startswith("@@"):
                if current_hunk:
                    patterns.append(self._analyze_hunk(current_hunk))
                current_hunk = []
            else:
                current_hunk.append(line)
        
        if current_hunk:
            patterns.append(self._analyze_hunk(current_hunk))
        
        return patterns
    
    def _analyze_hunk(self, hunk):
        """分析一个 diff hunk，提取规则"""
        removed = [l[1:] for l in hunk if l.startswith("-")]
        added = [l[1:] for l in hunk if l.startswith("+")]
        
        return {
            "removed": removed,
            "added": added,
            "change_type": self._classify_change(removed, added)
        }
    
    def _classify_change(self, removed, added):
        """分类修改类型"""
        if len(removed) > 0 and len(added) == 0:
            return "deletion"
        elif len(removed) == 0 and len(added) > 0:
            return "addition"
        elif len(removed) == len(added):
            return "replacement"
        else:
            return "mixed"
```

---

### 组件 3: 规则提取器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/suwen/rule-extractor.py

import json
from pathlib import Path

class RuleExtractor:
    """规则提取器"""
    
    def __init__(self):
        self.rules_file = Path.home() / ".taiyi" / "improvement-rules.json"
        self.rules = self._load_rules()
    
    def _load_rules(self):
        """加载现有规则"""
        if self.rules_file.exists():
            with open(self.rules_file, "r") as f:
                return json.load(f)
        return []
    
    def add_rule(self, pattern, rule_type, description):
        """添加新规则"""
        rule = {
            "pattern": pattern,
            "type": rule_type,
            "description": description,
            "count": 1
        }
        
        # 检查是否已有类似规则
        for existing in self.rules:
            if existing["pattern"] == pattern:
                existing["count"] += 1
                self._save_rules()
                return False
        
        self.rules.append(rule)
        self._save_rules()
        return True
    
    def _save_rules(self):
        """保存规则"""
        with open(self.rules_file, "w") as f:
            json.dump(self.rules, f, indent=2, ensure_ascii=False)
    
    def get_rules(self, rule_type=None):
        """获取规则"""
        if rule_type:
            return [r for r in self.rules if r["type"] == rule_type]
        return self.rules
    
    def export_to_skill(self, skill_path):
        """导出规则到技能文件"""
        with open(skill_path, "a") as f:
            f.write("\n\n## 自动学习的规则\n\n")
            for rule in self.rules:
                f.write(f"- [{rule['type']}] {rule['description']}\n")
                f.write(f"  模式：{rule['pattern']}\n")
                f.write(f"  学习次数：{rule['count']}\n\n")
```

---

### 组件 4: 宪法审查器

```python
#!/usr/bin/env python3
# ~/.openclaw/workspace/skills/taiyi/constitution-reviewer.py

from pathlib import Path

class ConstitutionReviewer:
    """宪法审查器"""
    
    def __init__(self):
        self.negentropy_path = Path.home() / ".openclaw" / "workspace" / "constitution" / "directives" / "NEGENTROPY.md"
    
    def review_rule(self, rule):
        """审查规则是否符合宪法"""
        issues = []
        
        # 负熵法则检查
        if not self._check_negentropy(rule):
            issues.append("违反负熵法则：增加系统混乱")
        
        # 价值基石检查
        if not self._check_value(rule):
            issues.append("违反价值基石：未创造价值")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _check_negentropy(self, rule):
        """负熵法则检查"""
        # 简化版：规则描述不能为空
        return len(rule.get("description", "")) > 0
    
    def _check_value(self, rule):
        """价值基石检查"""
        # 简化版：规则必须有实际作用
        return rule.get("type") in ["addition", "replacement", "style", "clarity"]
```

---

## 📊 试点计划

### 试点 1: 山木写作技能

**目标**: 学习 SAYELF 的写作风格

**流程**:
1. 山木生成内容初稿
2. SAYELF 修改后发布
3. 自动保存两版
4. diff 对比提取风格规则
5. 写入山木技能

**预期成果**: 10+ 条写作风格规则

---

### 试点 2: 知几交易策略

**目标**: 学习交易参数调整模式

**流程**:
1. 知几生成交易信号
2. SAYELF 调整参数（置信度/下注金额）
3. 自动保存两版
4. diff 对比提取调整规则
5. 写入知几策略

**预期成果**: 5+ 条策略优化规则

---

## 📝 任务追踪

| 编号 | 任务 | 状态 | 完成时间 |
|------|------|------|---------|
| `TASK-20260325-039` | 架构设计 | ✅ 完成 | 16:44 |
| `TASK-20260325-040` | diff 对比学习器 | 🟡 待实现 | - |
| `TASK-20260325-041` | 规则提取器 | 🟡 待实现 | - |
| `TASK-20260325-042` | 山木写作试点 | 🟡 待执行 | - |
| `TASK-20260325-043` | 知几交易试点 | 🟡 待执行 | - |

---

*创建时间：2026-03-25 16:44 | 执行：太一 + 素问*
