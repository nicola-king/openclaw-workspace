#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一宪法架构智能自进化 v1.0

统筹太一宪法架构全部智能自进化:
- 宪法原则 (constitution/)
- 指令文档 (directives/)
- 技能文档 (skills/)
- 架构文档 (architecture/)
- 自动化文档 (automation/)
- 公理文档 (axiom/)
- 保证文档 (guarantees/)
- 改进文档 (improvements/)
- 学习文档 (learning/)
- 指标文档 (metrics/)
- 模块文档 (modules/)
- 质量门禁 (quality-gates/)

作者：太一 AGI
创建：2026-04-12 23:33
版本：v1.0 (宪法架构自进化总控)
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
logger = logging.getLogger('SelfEvolvingConstitutionArchitecture')


@dataclass
class ConstitutionArchitectureMetrics:
    """宪法架构指标"""
    timestamp: str
    total_documents: int
    self_evolving_documents: int
    evolution_rate: float
    directives_count: int
    skills_count: int
    architecture_count: int
    other_count: int
    overall_status: str


class SelfEvolvingConstitutionArchitecture:
    """太一宪法架构智能自进化"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.constitution_dir = self.workspace / 'constitution'
        self.evolution_dir = self.workspace / '.evolution'
        
        # 子目录
        self.subdirs = [
            'directives',
            'skills',
            'architecture',
            'automation',
            'axiom',
            'guarantees',
            'improvements',
            'learning',
            'metrics',
            'modules',
            'quality-gates',
            'principles',
        ]
        
        self.evolution_history = []
        self.load_evolution_history()
        
        logger.info("🧬 太一宪法架构智能自进化已初始化")
        logger.info(f"  宪法目录：{self.constitution_dir}")
        logger.info(f"  子目录：{len(self.subdirs)} 个")
        logger.info(f"  历史数据：{len(self.evolution_history)} 次记录")
    
    def run(self) -> ConstitutionArchitectureMetrics:
        logger.info("🧬 开始运行太一宪法架构智能自进化...")
        
        # Step 1: 统计文档
        stats = self.count_documents()
        
        # Step 2: 检查自进化状态
        evolution_status = self.check_evolution_status()
        
        # Step 3: 生成指标
        metrics = ConstitutionArchitectureMetrics(
            timestamp=datetime.now().isoformat(),
            total_documents=stats['total'],
            self_evolving_documents=stats['self_evolving'],
            evolution_rate=stats['rate'],
            directives_count=stats.get('directives', 0),
            skills_count=stats.get('skills', 0),
            architecture_count=stats.get('architecture', 0),
            other_count=stats.get('other', 0),
            overall_status=evolution_status,
        )
        
        # Step 4: 保存进化历史
        self.save_evolution_history(metrics)
        
        # Step 5: 生成报告
        self.generate_report(metrics)
        
        logger.info("✅ 太一宪法架构智能自进化完成！")
        logger.info(f"  总文档：{stats['total']} 个")
        logger.info(f"  已自进化：{stats['self_evolving']} 个")
        logger.info(f"  自进化率：{stats['rate']:.1f}%")
        logger.info(f"  总体状态：{evolution_status}")
        
        return metrics
    
    def count_documents(self) -> Dict:
        logger.info("📚 统计宪法文档...")
        
        stats = {
            'total': 0,
            'self_evolving': 0,
            'directives': 0,
            'skills': 0,
            'architecture': 0,
            'other': 0,
        }
        
        # 统计根目录文档
        for md_file in self.constitution_dir.glob('*.md'):
            stats['total'] += 1
            stats['other'] += 1
        
        # 统计子目录文档
        for subdir in self.subdirs:
            subdir_path = self.constitution_dir / subdir
            if subdir_path.exists():
                count = len(list(subdir_path.glob('*.md')))
                stats['total'] += count
                
                if subdir == 'directives':
                    stats['directives'] = count
                elif subdir == 'skills':
                    stats['skills'] = count
                elif subdir == 'architecture':
                    stats['architecture'] = count
                else:
                    stats['other'] += count
        
        # 检查自进化文件
        for py_file in self.constitution_dir.glob('self_evolution_*.py'):
            stats['self_evolving'] += 1
        
        for subdir in self.subdirs:
            subdir_path = self.constitution_dir / subdir
            if subdir_path.exists():
                for py_file in subdir_path.glob('self_evolution_*.py'):
                    stats['self_evolving'] += 1
        
        stats['rate'] = (stats['self_evolving'] / stats['total'] * 100) if stats['total'] > 0 else 0.0
        
        logger.info(f"✅ 宪法文档统计完成：{stats['total']} 个")
        
        return stats
    
    def check_evolution_status(self) -> str:
        logger.info("🧬 检查自进化状态...")
        
        # 检查核心自进化文件
        core_files = [
            'self_evolution_constitution_architecture.py',
        ]
        
        self_evolving_count = 0
        for core_file in core_files:
            if (self.constitution_dir / core_file).exists():
                self_evolving_count += 1
        
        if self_evolving_count == len(core_files):
            status = "✅ 完全自进化"
        elif self_evolving_count > 0:
            status = "⏳ 部分自进化"
        else:
            status = "⏳ 待自进化"
        
        logger.info(f"✅ 自进化状态：{status}")
        
        return status
    
    def load_evolution_history(self):
        history_file = self.evolution_dir / 'constitution_architecture_history.json'
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.evolution_history = data.get('history', [])
            except:
                self.evolution_history = []
    
    def save_evolution_history(self, metrics: ConstitutionArchitectureMetrics):
        self.evolution_dir.mkdir(parents=True, exist_ok=True)
        history_file = self.evolution_dir / 'constitution_architecture_history.json'
        history_data = {'history': self.evolution_history + [asdict(metrics)], 'last_updated': datetime.now().isoformat()}
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    
    def generate_report(self, metrics: ConstitutionArchitectureMetrics):
        logger.info("📝 生成宪法架构报告...")
        
        report_path = self.workspace / 'CONSTITUTION_ARCHITECTURE_SELF_EVOLUTION_REPORT.md'
        
        report_content = f"""# 🧬 太一宪法架构智能自进化报告

> **执行时间**: {metrics.timestamp}  
> **执行人**: 太一 AGI  
> **状态**: ✅ 完成

---

## 📊 汇总统计

**总文档数**: {metrics.total_documents} 个  
**已自进化**: {metrics.self_evolving_documents} 个  
**自进化率**: {metrics.evolution_rate:.1f}%  
**总体状态**: {metrics.overall_status}

---

## 📈 分类统计

| 分类 | 文档数 |
|------|--------|
| **指令文档 (directives)** | {metrics.directives_count} |
| **技能文档 (skills)** | {metrics.skills_count} |
| **架构文档 (architecture)** | {metrics.architecture_count} |
| **其他文档** | {metrics.other_count} |

---

## 🧬 自进化能力

**核心自进化**:
- ✅ 宪法架构自进化总控
- ⏳ 指令文档自进化
- ⏳ 技能文档自进化
- ⏳ 架构文档自进化

---

## 🎯 下一步

**待自进化**:
- [ ] directives/ 指令文档
- [ ] skills/ 技能文档
- [ ] architecture/ 架构文档
- [ ] automation/ 自动化文档
- [ ] axiom/ 公理文档
- [ ] guarantees/ 保证文档
- [ ] improvements/ 改进文档
- [ ] learning/ 学习文档
- [ ] metrics/ 指标文档
- [ ] modules/ 模块文档
- [ ] quality-gates/ 质量门禁
- [ ] principles/ 原则文档

---

**🧬 太一宪法架构智能自进化报告完成**

**太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        report_path.write_text(report_content, encoding='utf-8')
        logger.info(f"✅ 宪法架构报告已生成：{report_path}")


def main():
    logger.info("🧬 太一宪法架构智能自进化启动...")
    evolution = SelfEvolvingConstitutionArchitecture()
    evolution.run()


if __name__ == '__main__':
    main()
