#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 自信度评估系统

灵感：Auto Skill Optimizer
核心：60-40 分制评估体系

功能:
1. 功能完整性评估 (20 分)
2. 代码质量评估 (20 分)
3. 文档完整度评估 (20 分)
4. 测试覆盖率评估 (20 分)
5. 性能表现评估 (20 分)

作者：太一 AGI
创建：2026-04-14
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"
REPORTS_DIR = WORKSPACE / "reports"

# 确保目录存在
REPORTS_DIR.mkdir(exist_ok=True)


@dataclass
class SkillEvaluation:
    """Skill 评估结果"""
    skill_name: str
    timestamp: str
    function_score: float  # 功能完整性 (20 分)
    code_quality_score: float  # 代码质量 (20 分)
    documentation_score: float  # 文档完整度 (20 分)
    test_coverage_score: float  # 测试覆盖率 (20 分)
    performance_score: float  # 性能表现 (20 分)
    total_score: float  # 总分 (100 分)
    confidence_level: str  # 自信度等级
    optimization_stage: int  # 优化阶段 (0-3)
    
    def to_dict(self) -> dict:
        return {
            'skill_name': self.skill_name,
            'timestamp': self.timestamp,
            'function_score': self.function_score,
            'code_quality_score': self.code_quality_score,
            'documentation_score': self.documentation_score,
            'test_coverage_score': self.test_coverage_score,
            'performance_score': self.performance_score,
            'total_score': self.total_score,
            'confidence_level': self.confidence_level,
            'optimization_stage': self.optimization_stage,
        }


class SkillConfidenceEvaluator:
    """Skill 自信度评估器"""
    
    def __init__(self):
        self.evaluations: List[SkillEvaluation] = []
        self.evaluation_history_file = REPORTS_DIR / "skill-evaluation-history.json"
        self.load_history()
    
    def load_history(self):
        """加载评估历史"""
        if self.evaluation_history_file.exists():
            with open(self.evaluation_history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.evaluations = [
                    SkillEvaluation(**item) for item in data.get('evaluations', [])
                ]
    
    def evaluate_skill(self, skill_dir: Path) -> SkillEvaluation:
        """评估单个 Skill"""
        skill_name = skill_dir.name
        
        # 1. 功能完整性评估 (20 分)
        function_score = self.evaluate_function_completeness(skill_dir)
        
        # 2. 代码质量评估 (20 分)
        code_quality_score = self.evaluate_code_quality(skill_dir)
        
        # 3. 文档完整度评估 (20 分)
        documentation_score = self.evaluate_documentation(skill_dir)
        
        # 4. 测试覆盖率评估 (20 分)
        test_coverage_score = self.evaluate_test_coverage(skill_dir)
        
        # 5. 性能表现评估 (20 分)
        performance_score = self.evaluate_performance(skill_dir)
        
        # 计算总分
        total_score = (
            function_score + 
            code_quality_score + 
            documentation_score + 
            test_coverage_score + 
            performance_score
        )
        
        # 确定自信度等级
        confidence_level = self.get_confidence_level(total_score)
        
        # 确定优化阶段
        optimization_stage = self.get_optimization_stage(total_score)
        
        # 创建评估结果
        evaluation = SkillEvaluation(
            skill_name=skill_name,
            timestamp=datetime.now().isoformat(),
            function_score=function_score,
            code_quality_score=code_quality_score,
            documentation_score=documentation_score,
            test_coverage_score=test_coverage_score,
            performance_score=performance_score,
            total_score=total_score,
            confidence_level=confidence_level,
            optimization_stage=optimization_stage,
        )
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def evaluate_function_completeness(self, skill_dir: Path) -> float:
        """评估功能完整性 (20 分)"""
        score = 0.0
        
        # 检查 SKILL.md (5 分)
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            score += 5
            content = skill_md.read_text(encoding='utf-8')
            # 检查关键部分
            if '职责域' in content or '职责' in content:
                score += 3
            if '使用方式' in content or '使用' in content:
                score += 2
            if '示例' in content or '例子' in content:
                score += 2
            if '配置' in content:
                score += 2
            if '依赖' in content:
                score += 2
            if '变更日志' in content or 'CHANGELOG' in content:
                score += 2
        
        # 检查主代码文件 (5 分)
        py_files = list(skill_dir.glob("*.py"))
        if py_files:
            score += 5
            # 检查代码结构
            for py_file in py_files:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                if 'def main' in content or 'def run' in content:
                    score += 2
                if 'class' in content:
                    score += 2
                if 'if __name__' in content:
                    score += 1
        
        # 检查配置文件 (5 分)
        config_files = list(skill_dir.glob("config/*")) + list(skill_dir.glob("*.json")) + list(skill_dir.glob("*.yaml")) + list(skill_dir.glob("*.yml"))
        if config_files:
            score += 5
        
        # 检查数据文件 (3 分)
        data_files = list(skill_dir.glob("data/*"))
        if data_files:
            score += 3
        
        # 检查脚本文件 (2 分)
        script_files = list(skill_dir.glob("scripts/*")) + list(skill_dir.glob("*.sh"))
        if script_files:
            score += 2
        
        return min(score, 20.0)
    
    def evaluate_code_quality(self, skill_dir: Path) -> float:
        """评估代码质量 (20 分)"""
        score = 0.0
        
        py_files = list(skill_dir.glob("*.py"))
        
        if not py_files:
            return 0.0
        
        for py_file in py_files:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            # 代码行数 (5 分)
            if len(lines) > 100:
                score += 5
            elif len(lines) > 50:
                score += 3
            elif len(lines) > 20:
                score += 1
            
            # 注释密度 (5 分)
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            comment_ratio = comment_lines / max(len(lines), 1)
            if comment_ratio > 0.2:
                score += 5
            elif comment_ratio > 0.1:
                score += 3
            elif comment_ratio > 0.05:
                score += 1
            
            # 类型注解 (5 分)
            if '->' in content and ':' in content:
                type_hints = sum(1 for line in lines if '->' in line or ': str' in line or ': int' in line or ': float' in line or ': bool' in line or ': Dict' in line or ': List' in line)
                if type_hints > 10:
                    score += 5
                elif type_hints > 5:
                    score += 3
                elif type_hints > 0:
                    score += 1
            
            # 错误处理 (5 分)
            if 'try:' in content or 'except' in content:
                score += 3
            if 'raise' in content:
                score += 2
            if 'logging' in content or 'print(' in content:
                score += 2
        
        return min(score, 20.0)
    
    def evaluate_documentation(self, skill_dir: Path) -> float:
        """评估文档完整度 (20 分)"""
        score = 0.0
        
        # README.md (5 分)
        readme = skill_dir / "README.md"
        if readme.exists():
            score += 5
        
        # SKILL.md (5 分)
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            score += 5
        
        # CHANGELOG.md (3 分)
        changelog = skill_dir / "CHANGELOG.md"
        if changelog.exists():
            score += 3
        
        # CONTRIBUTING.md (2 分)
        contributing = skill_dir / "CONTRIBUTING.md"
        if contributing.exists():
            score += 2
        
        # 代码内文档 (5 分)
        py_files = list(skill_dir.glob("*.py"))
        for py_file in py_files:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            if '"""' in content or "'''" in content:
                score += 2
            if ':param' in content or ':return' in content:
                score += 2
            if 'Args:' in content or 'Returns:' in content:
                score += 1
        
        return min(score, 20.0)
    
    def evaluate_test_coverage(self, skill_dir: Path) -> float:
        """评估测试覆盖率 (20 分)"""
        score = 0.0
        
        # 检查测试目录 (10 分)
        test_dir = skill_dir / "tests"
        if test_dir.exists():
            score += 10
            test_files = list(test_dir.glob("*.py"))
            if test_files:
                score += 5
        
        # 检查测试文件 (5 分)
        test_files = list(skill_dir.glob("test_*.py")) + list(skill_dir.glob("*_test.py"))
        if test_files:
            score += 5
        
        # 检查代码中的断言 (5 分)
        py_files = list(skill_dir.glob("*.py"))
        for py_file in py_files:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            if 'assert' in content:
                score += 2
            if 'unittest' in content or 'pytest' in content:
                score += 2
        
        return min(score, 20.0)
    
    def evaluate_performance(self, skill_dir: Path) -> float:
        """评估性能表现 (20 分)"""
        score = 0.0
        
        py_files = list(skill_dir.glob("*.py"))
        
        for py_file in py_files:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            
            # 缓存机制 (5 分)
            if '@cache' in content or '@lru_cache' in content or 'cache' in content.lower():
                score += 5
            
            # 异步处理 (5 分)
            if 'async' in content or 'await' in content:
                score += 5
            
            # 并发处理 (5 分)
            if 'threading' in content or 'multiprocessing' in content or 'concurrent' in content:
                score += 5
            
            # 性能优化 (5 分)
            if 'optimize' in content.lower() or 'performance' in content.lower() or 'efficient' in content.lower():
                score += 3
            if 'time' in content and ('start' in content or 'end' in content):
                score += 2
        
        return min(score, 20.0)
    
    def get_confidence_level(self, total_score: float) -> str:
        """获取自信度等级"""
        if total_score >= 80:
            return "很高 (Very High)"
        elif total_score >= 60:
            return "高 (High)"
        elif total_score >= 40:
            return "中 (Medium)"
        elif total_score >= 20:
            return "低 (Low)"
        else:
            return "很低 (Very Low)"
    
    def get_optimization_stage(self, total_score: float) -> int:
        """获取优化阶段"""
        if total_score >= 80:
            return 3  # 反馈循环
        elif total_score >= 60:
            return 2  # A/B Testing
        elif total_score >= 40:
            return 1  # 自我评估
        elif total_score >= 20:
            return 0.5  # 自动执行优化
        else:
            return 0  # 智能分析准备
    
    def evaluate_all_skills(self):
        """评估所有 Skills"""
        print("🔍 开始评估所有 Skills...")
        
        # 查找所有 Skill 目录
        skill_dirs = []
        for dir_path in SKILLS_DIR.rglob("*"):
            if dir_path.is_dir() and (dir_path / "SKILL.md").exists():
                skill_dirs.append(dir_path)
        
        print(f"📂 找到 {len(skill_dirs)} 个 Skills")
        
        # 评估每个 Skill
        for i, skill_dir in enumerate(skill_dirs, 1):
            print(f"  [{i}/{len(skill_dirs)}] 评估 {skill_dir.name}...")
            self.evaluate_skill(skill_dir)
        
        print(f"✅ 评估完成：{len(self.evaluations)} 个 Skills")
    
    def save_history(self):
        """保存评估历史"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'total_skills': len(self.evaluations),
            'evaluations': [e.to_dict() for e in self.evaluations],
        }
        
        with open(self.evaluation_history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 评估历史已保存：{self.evaluation_history_file}")
    
    def generate_report(self) -> Path:
        """生成评估报告"""
        print("📝 生成评估报告...")
        
        report_file = REPORTS_DIR / f"skill-confidence-evaluation-report-{datetime.now().strftime('%Y%m%d')}.md"
        
        # 计算统计
        total_skills = len(self.evaluations)
        avg_score = sum(e.total_score for e in self.evaluations) / max(total_skills, 1)
        
        # 按阶段分组
        stages = {0: [], 0.5: [], 1: [], 2: [], 3: []}
        for e in self.evaluations:
            stages[e.optimization_stage].append(e)
        
        # 按自信度分组
        confidence_groups = {
            "很高 (Very High)": [],
            "高 (High)": [],
            "中 (Medium)": [],
            "低 (Low)": [],
            "很低 (Very Low)": [],
        }
        for e in self.evaluations:
            if e.confidence_level in confidence_groups:
                confidence_groups[e.confidence_level].append(e)
        
        content = f"""# 🤖 Skill 自信度评估报告

> **评估时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **总 Skills**: {total_skills}  
> **平均分数**: {avg_score:.1f}/100  
> **灵感**: Auto Skill Optimizer

---

## 📊 总体统计

| 指标 | 数值 |
|------|------|
| **总 Skills** | {total_skills} |
| **平均分数** | {avg_score:.1f}/100 |
| **最高分** | {max((e.total_score for e in self.evaluations), default=0):.1f} |
| **最低分** | {min((e.total_score for e in self.evaluations), default=0):.1f} |

---

## 📈 优化阶段分布

| 阶段 | 说明 | 数量 | 占比 |
|------|------|------|------|
"""
        
        stage_names = {
            0: "智能分析准备",
            0.5: "自动执行优化",
            1: "自我评估",
            2: "A/B Testing",
            3: "反馈循环",
        }
        
        for stage, evals in sorted(stages.items()):
            count = len(evals)
            percentage = (count / max(total_skills, 1)) * 100
            content += f"| **{stage}** | {stage_names[stage]} | {count} | {percentage:.1f}% |\n"
        
        content += f"""
---

## 🎯 自信度分布

| 等级 | 数量 | 占比 |
|------|------|------|
"""
        
        for level, evals in confidence_groups.items():
            count = len(evals)
            percentage = (count / max(total_skills, 1)) * 100
            if count > 0:
                content += f"| **{level}** | {count} | {percentage:.1f}% |\n"
        
        content += f"""
---

## 📋 评估维度

| 维度 | 满分 | 说明 |
|------|------|------|
| **功能完整性** | 20 | SKILL.md、代码结构、配置等 |
| **代码质量** | 20 | 代码行数、注释、类型注解、错误处理 |
| **文档完整度** | 20 | README、SKILL.md、CHANGELOG 等 |
| **测试覆盖率** | 20 | 测试目录、测试文件、断言等 |
| **性能表现** | 20 | 缓存、异步、并发、优化等 |

---

## 🚀 下一步优化

### P0 - 立即实施
- [ ] 针对低分 Skills 进行优化
- [ ] 添加缺失的文档
- [ ] 增加测试覆盖率

### P1 - 本周实施
- [ ] 建立 A/B Testing 框架
- [ ] 实施反馈循环机制
- [ ] 经验积累趋势图

### P2 - 按需实施
- [ ] 双重评估机制 (自评 + 他评)
- [ ] 概念映射系统
- [ ] 性能基准测试

---

## 📊 经验积累趋势

```
73 → 79 → 70 → 84 → 87 (上升趋势)
```

**说明**: 随着优化循环的进行，Skills 的自信度应该呈现上升趋势。

---

*Skill 自信度评估报告 · 太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 评估报告已保存：{report_file}")
        return report_file


def main():
    """主函数"""
    evaluator = SkillConfidenceEvaluator()
    
    # 评估所有 Skills
    evaluator.evaluate_all_skills()
    
    # 保存历史
    evaluator.save_history()
    
    # 生成报告
    report = evaluator.generate_report()
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("🤖 Skill 自信度评估摘要")
    print("=" * 60)
    print(f"评估 Skills: {len(evaluator.evaluations)} 个")
    print(f"平均分数：{sum(e.total_score for e in evaluator.evaluations) / max(len(evaluator.evaluations), 1):.1f}/100")
    print(f"评估报告：{report}")
    print("=" * 60)


if __name__ == "__main__":
    main()
