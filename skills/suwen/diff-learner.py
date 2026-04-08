#!/usr/bin/env python3
"""
P5 · diff 对比学习器

版本：v0.1
创建：2026-03-25 16:44
执行：素问
"""

import difflib
import json
from pathlib import Path
from datetime import datetime

class DiffLearner:
    """diff 对比学习器"""
    
    def __init__(self):
        self.history_dir = Path.home() / ".taiyi" / "output-history"
        self.rules_file = Path.home() / ".taiyi" / "improvement-rules.json"
        self.rules = self._load_rules()
    
    def _load_rules(self):
        """加载现有规则"""
        if self.rules_file.exists():
            with open(self.rules_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def compare_and_learn(self, original_text, modified_text, context="general"):
        """
        对比两个版本并学习
        
        Args:
            original_text: 原始文本
            modified_text: 修改后文本
            context: 上下文（writing/trading/code 等）
        
        Returns:
            学习到的规则列表
        """
        # 生成 diff
        diff = list(difflib.unified_diff(
            original_text.splitlines(keepends=True),
            modified_text.splitlines(keepends=True),
            fromfile="original",
            tofile="modified",
            lineterm=""
        ))
        
        # 提取修改模式
        patterns = self._extract_patterns(diff)
        
        # 生成规则
        new_rules = []
        for pattern in patterns:
            rule = self._generate_rule(pattern, context)
            if rule and self._add_rule(rule):
                new_rules.append(rule)
        
        return new_rules
    
    def _extract_patterns(self, diff_lines):
        """从 diff 中提取修改模式"""
        patterns = []
        current_hunk = []
        
        for line in diff_lines:
            if line.startswith("@@"):
                if current_hunk:
                    pattern = self._analyze_hunk(current_hunk)
                    if pattern:
                        patterns.append(pattern)
                current_hunk = []
            else:
                current_hunk.append(line)
        
        if current_hunk:
            pattern = self._analyze_hunk(current_hunk)
            if pattern:
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_hunk(self, hunk):
        """分析一个 diff hunk"""
        removed = [l[1:] for l in hunk if l.startswith("-") and not l.startswith("---")]
        added = [l[1:] for l in hunk if l.startswith("+") and not l.startswith("+++")]
        
        if not removed and not added:
            return None
        
        return {
            "removed": removed,
            "added": added,
            "change_type": self._classify_change(removed, added),
            "timestamp": datetime.now().isoformat()
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
    
    def _generate_rule(self, pattern, context):
        """从模式生成规则"""
        rule_type = pattern["change_type"]
        
        # 生成描述
        if rule_type == "addition":
            description = f"添加内容：{pattern['added'][0][:50]}..."
        elif rule_type == "deletion":
            description = f"删除内容：{pattern['removed'][0][:50]}..."
        elif rule_type == "replacement":
            description = f"替换：{pattern['removed'][0][:30]}... → {pattern['added'][0][:30]}..."
        else:
            description = f"混合修改（{len(pattern['removed'])} 行删除，{len(pattern['added'])} 行添加）"
        
        return {
            "pattern": {
                "removed": pattern["removed"][:3],  # 简化存储
                "added": pattern["added"][:3],
                "change_type": rule_type
            },
            "type": rule_type,
            "description": description,
            "context": context,
            "count": 1,
            "created_at": pattern["timestamp"]
        }
    
    def _add_rule(self, rule):
        """添加规则（去重）"""
        # 检查是否已有类似规则
        for existing in self.rules:
            if existing["pattern"]["removed"] == rule["pattern"]["removed"] and \
               existing["pattern"]["added"] == rule["pattern"]["added"]:
                existing["count"] += 1
                self._save_rules()
                return False
        
        self.rules.append(rule)
        self._save_rules()
        return True
    
    def _save_rules(self):
        """保存规则"""
        self.rules_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.rules_file, "w", encoding="utf-8") as f:
            json.dump(self.rules, f, indent=2, ensure_ascii=False)
    
    def get_rules(self, context=None, limit=10):
        """获取规则"""
        rules = self.rules
        if context:
            rules = [r for r in rules if r.get("context") == context]
        
        # 按学习次数排序
        rules = sorted(rules, key=lambda x: x["count"], reverse=True)
        return rules[:limit]
    
    def export_report(self):
        """导出学习报告"""
        report = f"""# Self-Improving 学习报告

**生成时间**: {datetime.now().isoformat()}
**总规则数**: {len(self.rules)}

## 规则统计

| 类型 | 数量 |
|------|------|
"""
        type_counts = {}
        for rule in self.rules:
            t = rule["type"]
            type_counts[t] = type_counts.get(t, 0) + 1
        
        for t, c in type_counts.items():
            report += f"| {t} | {c} |\n"
        
        report += f"""
## 高频规则（Top 10）

"""
        top_rules = self.get_rules(limit=10)
        for i, rule in enumerate(top_rules, 1):
            report += f"{i}. [{rule['type']}] {rule['description']} (学习{rule['count']}次)\n"
        
        return report


# ============ 测试 ============

if __name__ == "__main__":
    print("=" * 70)
    print("  P5 · diff 对比学习器 - 测试")
    print("=" * 70)
    print()
    
    learner = DiffLearner()
    
    # 测试 1: 写作风格学习
    print("【测试 1】写作风格学习")
    original = """
今天天气很好，我们去公园玩。公园里面有很多人，还有花。
"""
    modified = """
今日天朗气清，偕友游园。园中游人如织，繁花似锦。
"""
    
    rules = learner.compare_and_learn(original, modified, context="writing")
    print(f"学习到 {len(rules)} 条规则")
    for rule in rules:
        print(f"  - {rule['description']}")
    print()
    
    # 测试 2: 导出报告
    print("【测试 2】导出学习报告")
    report = learner.export_report()
    print(report)
    print()
    
    print("=" * 70)
    print("  测试完成")
    print("=" * 70)
