#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Skill Generator - 技能自动生成核心模块

版本：v1.0 | 创建：2026-04-08
功能：从任务经验中自动提取可复用模式，生成技能草稿
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TaskParser:
    """任务解析器 - 解析会话日志"""
    
    def __init__(self):
        self.step_patterns = [
            r'太一，(.*?)\n',
            r'执行：(.*?)\n',
            r'步骤 [1-9]：(.*?)\n',
            r'第一步 [：:](.*?)\n',
        ]
    
    def parse(self, session_log: str) -> Dict:
        """解析任务会话日志"""
        return {
            'intent': self._extract_intent(session_log),
            'steps': self._extract_steps(session_log),
            'tools_used': self._extract_tools(session_log),
            'files_created': self._extract_files(session_log, 'created'),
            'files_modified': self._extract_files(session_log, 'modified'),
            'decisions_made': self._extract_decisions(session_log),
            'success_criteria': self._extract_success_criteria(session_log),
            'duration': self._estimate_duration(session_log),
            'complexity': self._calculate_complexity(session_log)
        }
    
    def _extract_intent(self, log: str) -> str:
        """提取用户意图"""
        # 查找用户第一条消息
        match = re.search(r'(?:SAYELF|用户)[：:]\s*(.+?)(?:\n|$)', log)
        return match.group(1).strip() if match else '未知任务'
    
    def _extract_steps(self, log: str) -> List[str]:
        """提取执行步骤"""
        steps = []
        for pattern in self.step_patterns:
            matches = re.findall(pattern, log, re.IGNORECASE)
            steps.extend([m.strip() for m in matches])
        return steps if steps else ['执行任务']
    
    def _extract_tools(self, log: str) -> List[str]:
        """提取使用的工具"""
        tools = []
        tool_patterns = [
            r'web_search', r'web_fetch', r'exec', r'process',
            r'read', r'write', r'edit', r'sessions_send'
        ]
        for pattern in tool_patterns:
            if re.search(pattern, log):
                tools.append(pattern)
        return tools if tools else ['unknown']
    
    def _extract_files(self, log: str, action: str) -> List[str]:
        """提取文件操作"""
        files = []
        if action == 'created':
            matches = re.findall(r'成功写入.*?(/[\w/.-]+\.md)', log)
            files.extend(matches)
        elif action == 'modified':
            matches = re.findall(r'成功替换.*?(/[\w/.-]+\.md)', log)
            files.extend(matches)
        return files
    
    def _extract_decisions(self, log: str) -> List[str]:
        """提取关键决策"""
        decisions = []
        patterns = [r'决定 (.*?)\n', r'选择 (.*?)\n', r'采用 (.*?)\n']
        for pattern in patterns:
            matches = re.findall(pattern, log)
            decisions.extend(matches)
        return decisions
    
    def _extract_success_criteria(self, log: str) -> str:
        """提取成功标准"""
        if '✅' in log or '完成' in log:
            return '任务成功完成'
        return '待验证'
    
    def _estimate_duration(self, log: str) -> int:
        """估算执行时长（分钟）"""
        # 简单估算：根据日志长度
        lines = len(log.split('\n'))
        return max(1, lines // 10)
    
    def _calculate_complexity(self, log: str) -> int:
        """计算复杂度评分 (1-10)"""
        score = 0
        # 步骤数量
        steps = len(self._extract_steps(log))
        score += min(steps, 5)
        # 工具数量
        tools = len(self._extract_tools(log))
        score += min(tools, 3)
        # 文件操作
        files = len(self._extract_files(log, 'created'))
        score += min(files, 2)
        return min(10, score)


class ReusabilityScorer:
    """可复用性评分器"""
    
    def __init__(self):
        self.weights = {
            'repetition': 0.3,
            'steps_clarity': 0.2,
            'tool_reuse': 0.2,
            'file_output': 0.2,
            'complexity': 0.1
        }
    
    def score(self, task: Dict, similar_tasks_count: int = 0) -> float:
        """评估任务可复用性 (0-1)"""
        score = 0.0
        
        # 重复出现 (+0.3)
        if similar_tasks_count >= 3:
            score += self.weights['repetition']
        elif similar_tasks_count >= 2:
            score += self.weights['repetition'] * 0.5
        
        # 步骤清晰 (+0.2)
        steps = len(task.get('steps', []))
        if 3 <= steps <= 10:
            score += self.weights['steps_clarity']
        
        # 工具复用 (+0.2)
        tools = len(task.get('tools_used', []))
        if tools >= 2:
            score += self.weights['tool_reuse']
        
        # 有文件产出 (+0.2)
        files = len(task.get('files_created', []))
        if files >= 1:
            score += self.weights['file_output']
        
        # 复杂度适中 (+0.1)
        complexity = task.get('complexity', 5)
        if 3 <= complexity <= 7:
            score += self.weights['complexity']
        
        return round(score, 2)


class PatternExtractor:
    """模式提取器"""
    
    def extract(self, task: Dict) -> Dict:
        """从任务中提取可复用模式"""
        return {
            'name': self._generate_name(task['intent']),
            'description': self._summarize(task),
            'triggers': self._extract_triggers(task['intent']),
            'steps': self._generalize_steps(task['steps']),
            'tools': task['tools_used'],
            'templates': self._extract_templates(task['files_created']),
            'parameters': self._extract_parameters(task),
            'validation': self._extract_validation(task)
        }
    
    def _generate_name(self, intent: str) -> str:
        """生成技能名称"""
        # 从意图提取关键词
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,}', intent)
        if keywords:
            # 移除"太一"等通用词
            keywords = [k for k in keywords if k not in ['太一']]
            return ''.join(keywords[:3]) + 'Skill'
        return 'AutoSkill'
    
    def _summarize(self, task: Dict) -> str:
        """生成任务摘要"""
        intent = task['intent']
        # 移除"太一，"前缀
        intent = re.sub(r'^太一 [，,]?\s*', '', intent)
        # 移除"今日"等时间词
        intent = re.sub(r'今日 | 明日 | 当前', '', intent)
        return f"自动化{intent}"
    
    def _extract_triggers(self, intent: str) -> List[str]:
        """提取触发关键词"""
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,}', intent)
        return keywords[:3] if keywords else ['auto']
    
    def _generalize_steps(self, steps: List[str]) -> List[str]:
        """泛化执行步骤"""
        generalized = []
        for step in steps:
            # 移除具体参数，保留动作
            step = re.sub(r'\d+', 'N', step)  # 数字→N
            step = re.sub(r'/[\w/.-]+/', '[PATH]/', step)  # 路径→[PATH]
            generalized.append(step)
        return generalized
    
    def _extract_templates(self, files: List[str]) -> List[str]:
        """提取文件模板"""
        return files[:3] if files else []
    
    def _extract_parameters(self, task: Dict) -> Dict:
        """提取参数"""
        return {
            'input': '用户输入',
            'output': '生成的文件',
            'options': {}
        }
    
    def _extract_validation(self, task: Dict) -> List[str]:
        """提取验证规则"""
        return ['文件存在性检查', '内容格式检查']


class SkillGenerator:
    """技能草稿生成器"""
    
    def __init__(self, workspace_root: str = '/home/nicola/.openclaw/workspace'):
        self.workspace_root = Path(workspace_root)
    
    def generate(self, pattern: Dict) -> str:
        """生成 SKILL.md 草稿"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        draft = f"""---
name: {self._slugify(pattern['name'])}
version: 1.0.0
description: {pattern['description']}
category: auto-generated
tags: {pattern['triggers']}
author: 太一 AGI (Auto-Generated)
created: {timestamp}
---

# {pattern['name']} Skill

> 版本：v1.0 | 创建：{timestamp} | 优先级：P2
> 来源：从任务经验中自动提取

---

## 🎯 职责

{pattern['description']}

---

## 🔍 触发条件

{self._format_triggers(pattern['triggers'])}

---

## 🛠️ 执行流程

{self._format_steps(pattern['steps'])}

---

## 📁 相关文件

{self._format_files(pattern['templates'])}

---

## 📋 使用示例

{self._format_examples(pattern['parameters'])}

---

## ✅ 质量检查

- [ ] 命名规范检查
- [ ] 元数据完整检查
- [ ] 触发条件清晰检查
- [ ] 步骤可执行检查
- [ ] 无硬编码检查
- [ ] 有使用示例检查
- [ ] 有错误处理检查

---

*本技能由太一自动生成，经 SAYELF 确认后激活。*
"""
        return draft
    
    def _slugify(self, name: str) -> str:
        """将名称转换为 slug"""
        # 移除"Skill"重复
        name = name.replace('SkillSkill', 'Skill')
        slug = re.sub(r'[^a-zA-Z0-9-]', '-', name)
        slug = re.sub(r'-+', '-', slug)  # 多个连字符变一个
        return slug.lower().strip('-') if slug else 'auto-skill'
    
    def _format_triggers(self, triggers: List[str]) -> str:
        """格式化触发条件"""
        # 过滤通用词
        triggers = [t for t in triggers if t not in ['太一']]
        if not triggers:
            return '- 用户提及相关任务'
        return '\n'.join([f'- 用户提及：{t}' for t in triggers[:3]])
    
    def _format_steps(self, steps: List[str]) -> str:
        """格式化执行步骤"""
        if not steps:
            return '1. 接收任务\n2. 执行\n3. 返回结果'
        return '\n'.join([f'{i+1}. {step}' for i, step in enumerate(steps[:10])])
    
    def _format_files(self, files: List[str]) -> str:
        """格式化相关文件"""
        if not files:
            return '- 无'
        return '\n'.join([f'- `{f}`' for f in files])
    
    def _format_examples(self, params: Dict) -> str:
        """格式化使用示例"""
        return f"""```
# 示例 1: 基础使用
太一，{params.get('input', '执行任务')}

# 示例 2: 带参数
太一，{params.get('input', '执行任务')} --option=value
```"""


class SkillValidator:
    """技能质量验证器"""
    
    def validate(self, draft: str) -> Tuple[bool, List[str]]:
        """验证技能草稿质量"""
        issues = []
        
        # 1. 命名规范检查
        if not re.search(r'name: [\w-]+', draft):
            issues.append('缺少技能名称')
        
        # 2. 元数据完整检查
        required_fields = ['name', 'version', 'description', 'category']
        for field in required_fields:
            if f'{field}:' not in draft:
                issues.append(f'缺少元数据：{field}')
        
        # 3. 触发条件清晰检查
        if '触发条件' not in draft:
            issues.append('缺少触发条件')
        
        # 4. 步骤可执行检查
        if '执行流程' not in draft:
            issues.append('缺少执行流程')
        
        # 5. 无硬编码检查（允许 workspace 路径）
        if re.search(r'/home/nicola/[^{]', draft):
            # 检查是否是 workspace 路径（允许）
            if '/home/nicola/.openclaw/workspace' not in draft:
                issues.append('包含硬编码路径')
        
        # 6. 有使用示例检查
        if '示例' not in draft:
            issues.append('缺少使用示例')
        
        # 7. 有错误处理检查
        if '错误' not in draft and '异常' not in draft:
            issues.append('缺少错误处理说明')
        
        return len(issues) == 0, issues


class AutoSkillGenerator:
    """技能自动生成器（主类）"""
    
    def __init__(self, workspace_root: str = '/home/nicola/.openclaw/workspace'):
        self.parser = TaskParser()
        self.scorer = ReusabilityScorer()
        self.extractor = PatternExtractor()
        self.generator = SkillGenerator(workspace_root)
        self.validator = SkillValidator()
        self.workspace_root = Path(workspace_root)
    
    def process(self, session_log: str, similar_tasks_count: int = 0) -> Dict:
        """处理会话日志，生成技能"""
        # 1. 解析任务
        task = self.parser.parse(session_log)
        
        # 2. 评分
        score = self.scorer.score(task, similar_tasks_count)
        
        # 3. 提取模式
        pattern = self.extractor.extract(task)
        
        # 4. 生成草稿
        draft = self.generator.generate(pattern)
        
        # 5. 验证
        is_valid, issues = self.validator.validate(draft)
        
        return {
            'task': task,
            'score': score,
            'pattern': pattern,
            'draft': draft,
            'is_valid': is_valid,
            'issues': issues,
            'should_generate': score >= 0.6 and is_valid
        }
    
    def save_draft(self, draft: str, skill_name: str) -> str:
        """保存技能草稿"""
        skill_dir = self.workspace_root / 'skills' / self._slugify(skill_name)
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_file = skill_dir / 'SKILL.md'
        skill_file.write_text(draft, encoding='utf-8')
        
        return str(skill_file)
    
    def _slugify(self, name: str) -> str:
        """将名称转换为 slug"""
        slug = re.sub(r'[^a-zA-Z0-9-]', '', name)
        return slug.lower() if slug else 'auto-skill'


# 使用示例
if __name__ == '__main__':
    # 示例会话日志
    session_log = """
SAYELF: 太一，生成日报
太一：收到，正在生成日报...
执行：web_search 搜索今日新闻
执行：write 写入日报文件
执行：sessions_send 发送结果
成功写入 /home/nicola/.openclaw/workspace/reports/2026-04-08-daily.md
✅ 日报生成完成
"""
    
    generator = AutoSkillGenerator()
    result = generator.process(session_log, similar_tasks_count=3)
    
    print(f"可复用性评分：{result['score']}")
    print(f"是否生成技能：{result['should_generate']}")
    print(f"验证问题：{result['issues']}")
    
    if result['should_generate']:
        skill_file = generator.save_draft(result['draft'], result['pattern']['name'])
        print(f"技能草稿已保存：{skill_file}")
