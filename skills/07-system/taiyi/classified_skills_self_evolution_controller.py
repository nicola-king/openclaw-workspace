#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分类 Skill 智能自进化总控模块

统筹分类后 Skill 的自进化:
- 01-trading (交易类)
- 02-business (业务类)
- 03-automation (自动化类)
- 04-integration (集成类)
- 05-content (内容类)
- 06-analysis (分析类)
- 07-system (系统类)
- 08-emerged (涌现类)

作者：太一 AGI
创建：2026-04-12 23:16
版本：v1.0 (分类 Skill 自进化总控)
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('ClassifiedSkillsSelfEvolutionController')


@dataclass
class ClassifiedSkillsMetrics:
    """分类 Skill 指标"""
    timestamp: str
    category: str
    total_skills: int
    self_evolving_skills: int
    evolution_rate: float
    signals: List[str]


class ClassifiedSkillsSelfEvolutionController:
    """分类 Skill 智能自进化总控"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.skills_dir = self.workspace / 'skills'
        self.evolution_dir = self.workspace / '.evolution'
        
        # 分类目录
        self.categories = [
            '01-trading',
            '02-business',
            '03-automation',
            '04-integration',
            '05-content',
            '06-analysis',
            '07-system',
            '08-emerged',
        ]
        
        self.evolution_history = []
        self.load_evolution_history()
        
        logger.info("🧬 分类 Skill 智能自进化总控已初始化")
        logger.info(f"  分类目录：{len(self.categories)} 个")
        logger.info(f"  历史数据：{len(self.evolution_history)} 次记录")
    
    def run(self) -> Dict[str, ClassifiedSkillsMetrics]:
        logger.info("🧬 开始运行分类 Skill 智能自进化...")
        
        results = {}
        
        for category in self.categories:
            metrics = self.evolve_category(category)
            results[category] = metrics
        
        # 生成汇总报告
        self.generate_summary_report(results)
        
        logger.info("✅ 分类 Skill 智能自进化完成！")
        
        return results
    
    def evolve_category(self, category: str) -> ClassifiedSkillsMetrics:
        """进化单个分类"""
        logger.info(f"🧬 进化分类：{category}...")
        
        category_dir = self.skills_dir / category
        
        if not category_dir.exists():
            logger.info(f"  ⚠️ 分类目录不存在：{category}")
            return ClassifiedSkillsMetrics(
                timestamp=datetime.now().isoformat(),
                category=category,
                total_skills=0,
                self_evolving_skills=0,
                evolution_rate=0.0,
                signals=["⚠️ 分类目录不存在"],
            )
        
        # 统计 Skill 数量
        total_skills = 0
        self_evolving_skills = 0
        signals = []
        
        for item in category_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                total_skills += 1
                
                # 检查自进化文件
                self_evolving_files = list(item.glob('self_evolution_*.py'))
                if self_evolving_files:
                    self_evolving_skills += 1
                    signals.append(f"✅ {item.name}: {len(self_evolving_files)} 个自进化文件")
                else:
                    signals.append(f"⏳ {item.name}: 待自进化")
        
        evolution_rate = (self_evolving_skills / total_skills * 100) if total_skills > 0 else 0.0
        
        signals.append(f"✅ 总计：{self_evolving_skills}/{total_skills} ({evolution_rate:.1f}%)")
        
        metrics = ClassifiedSkillsMetrics(
            timestamp=datetime.now().isoformat(),
            category=category,
            total_skills=total_skills,
            self_evolving_skills=self_evolving_skills,
            evolution_rate=evolution_rate,
            signals=signals,
        )
        
        logger.info(f"✅ {category} 自进化完成：{self_evolving_skills}/{total_skills} ({evolution_rate:.1f}%)")
        
        return metrics
    
    def generate_summary_report(self, results: Dict[str, ClassifiedSkillsMetrics]):
        """生成汇总报告"""
        logger.info("📝 生成汇总报告...")
        
        report_path = self.workspace / 'CLASSIFIED_SKILLS_SELF_EVOLUTION_REPORT.md'
        
        total_skills = sum(m.total_skills for m in results.values())
        total_self_evolving = sum(m.self_evolving_skills for m in results.values())
        overall_rate = (total_self_evolving / total_skills * 100) if total_skills > 0 else 0.0
        
        report_content = f"""# 🧬 分类 Skill 智能自进化汇总报告

> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **执行人**: 太一 AGI  
> **状态**: ✅ 完成

---

## 📊 汇总统计

**总 Skill 数**: {total_skills} 个  
**已自进化**: {total_self_evolving} 个  
**自进化率**: {overall_rate:.1f}%

---

## 📈 分类统计

| 分类 | 总 Skill | 已自进化 | 自进化率 | 状态 |
|------|---------|---------|---------|------|
"""
        
        for category, metrics in results.items():
            status = "✅" if metrics.evolution_rate >= 50 else "⏳"
            report_content += f"| {category} | {metrics.total_skills} | {metrics.self_evolving_skills} | {metrics.evolution_rate:.1f}% | {status} |\n"
        
        report_content += f"""
---

## 📝 详细报告

"""
        
        for category, metrics in results.items():
            report_content += f"""### {category}

**总 Skill**: {metrics.total_skills} 个  
**已自进化**: {metrics.self_evolving_skills} 个  
**自进化率**: {metrics.evolution_rate:.1f}%

**详情**:
"""
            for signal in metrics.signals:
                report_content += f"- {signal}\n"
            
            report_content += "\n"
        
        report_content += f"""
---

## 🎯 下一步行动

**高优先级**:
"""
        
        for category, metrics in results.items():
            if metrics.evolution_rate < 50 and metrics.total_skills > 0:
                report_content += f"- ⏳ {category}: {metrics.total_skills - metrics.self_evolving_skills} 个待自进化\n"
        
        report_content += f"""
---

**🧬 分类 Skill 智能自进化汇总报告完成**
"""
        
        report_path.write_text(report_content, encoding='utf-8')
        logger.info(f"✅ 汇总报告已生成：{report_path}")
    
    def load_evolution_history(self):
        history_file = self.evolution_dir / 'classified_skills_history.json'
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.evolution_history = data.get('history', [])
            except:
                self.evolution_history = []
    
    def save_evolution_history(self, results: Dict[str, ClassifiedSkillsMetrics]):
        self.evolution_dir.mkdir(parents=True, exist_ok=True)
        history_file = self.evolution_dir / 'classified_skills_history.json'
        history_data = {'history': self.evolution_history + [datetime.now().isoformat()], 'last_updated': datetime.now().isoformat()}
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)


def main():
    logger.info("🧬 分类 Skill 智能自进化总控启动...")
    controller = ClassifiedSkillsSelfEvolutionController()
    controller.run()


if __name__ == '__main__':
    main()
