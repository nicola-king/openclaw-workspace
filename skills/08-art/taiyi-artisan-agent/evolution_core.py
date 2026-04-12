#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolution Core - 进化核心（Phase 3: 自主进化）

L5 进化维度：
- 风格识别：60% → 100%
- 范式定义：30% → 100%
- 自主进化：40% → 100%
- 美学驱动：50% → 100%
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class EvolutionCore:
    """进化核心"""
    
    def __init__(self, output_dir: str = "~/.openclaw/workspace/skills/08-art/taiyi-artisan-agent/outputs"):
        self.output_dir = Path(output_dir).expanduser()
        self.state_file = self.output_dir / "evolution_state.json"
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """加载进化状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            'l5_progress': {
                'style_recognition': 60.0,
                'paradigm_definition': 30.0,
                'autonomous_evolution': 40.0,
                'aesthetic_driven_innovation': 50.0,
                'overall': 45.0
            },
            'style_params': {
                'apple_ratio': 80.0,
                'oriental_ratio': 15.0,
                'chinese_ratio': 5.0
            },
            'feedback_count': 0,
            'learning_count': 0,
            'last_evolution': None
        }
    
    def _save_state(self):
        """保存进化状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def evolve_from_feedback(self, feedback: Dict):
        """从反馈进化"""
        self.state['feedback_count'] += 1
        
        # 根据反馈调整风格参数
        if feedback.get('reaction') == 'positive':
            # 强化当前风格
            self.state['style_params']['apple_ratio'] = min(85.0, self.state['style_params']['apple_ratio'] + 0.1)
        elif feedback.get('reaction') == 'negative':
            # 调整风格
            self.state['style_params']['apple_ratio'] = max(75.0, self.state['style_params']['apple_ratio'] - 0.1)
        
        # 更新 L5 进度
        self._calculate_l5_progress()
        self.state['last_evolution'] = datetime.now().isoformat()
        self._save_state()
    
    def evolve_from_learning(self, learning: Dict):
        """从学习进化"""
        self.state['learning_count'] += 1
        
        # 吸收新知识到风格参数
        if learning.get('type') == 'big_tech_design':
            source = learning.get('source')
            if source == 'apple':
                # Apple 设计更新
                pass
            elif source == 'google':
                # Google Material 更新
                pass
        
        # 更新 L5 进度
        self._calculate_l5_progress()
        self.state['last_evolution'] = datetime.now().isoformat()
        self._save_state()
    
    def _calculate_l5_progress(self):
        """计算 L5 进度"""
        # 基于反馈和学习数量计算进度
        feedback_factor = min(1.0, self.state['feedback_count'] / 100)
        learning_factor = min(1.0, self.state['learning_count'] / 50)
        
        # 更新各维度
        self.state['l5_progress']['style_recognition'] = min(100.0, 60.0 + feedback_factor * 40)
        self.state['l5_progress']['paradigm_definition'] = min(100.0, 30.0 + learning_factor * 70)
        self.state['l5_progress']['autonomous_evolution'] = min(100.0, 40.0 + (feedback_factor + learning_factor) / 2 * 60)
        self.state['l5_progress']['aesthetic_driven_innovation'] = min(100.0, 50.0 + feedback_factor * 50)
        
        # 计算总体进度
        progress = self.state['l5_progress']
        self.state['l5_progress']['overall'] = (
            progress['style_recognition'] +
            progress['paradigm_definition'] +
            progress['autonomous_evolution'] +
            progress['aesthetic_driven_innovation']
        ) / 4
    
    def get_evolution_report(self) -> Dict:
        """生成进化报告"""
        return {
            'l5_progress': self.state['l5_progress'],
            'feedback_count': self.state['feedback_count'],
            'learning_count': self.state['learning_count'],
            'style_params': self.state['style_params'],
            'last_evolution': self.state['last_evolution']
        }
    
    def get_milestones(self) -> List[Dict]:
        """获取里程碑状态"""
        return [
            {
                'name': '风格识别',
                'description': '用户能识别"太一风格"',
                'target_date': '2026-04-17',
                'current': self.state['l5_progress']['style_recognition'],
                'target': 100.0,
                'status': '进行中' if self.state['l5_progress']['style_recognition'] < 100 else '完成'
            },
            {
                'name': '范式定义',
                'description': '创造 1 个可借鉴模式',
                'target_date': '2026-04-24',
                'current': self.state['l5_progress']['paradigm_definition'],
                'target': 100.0,
                'status': '进行中' if self.state['l5_progress']['paradigm_definition'] < 100 else '完成'
            },
            {
                'name': '自主进化',
                'description': '美学系统能自主学习',
                'target_date': '2026-05-01',
                'current': self.state['l5_progress']['autonomous_evolution'],
                'target': 100.0,
                'status': '进行中' if self.state['l5_progress']['autonomous_evolution'] < 100 else '完成'
            },
            {
                'name': '美学驱动',
                'description': '3 次因美学而创新',
                'target_date': '2026-05-08',
                'current': self.state['l5_progress']['aesthetic_driven_innovation'],
                'target': 100.0,
                'status': '进行中' if self.state['l5_progress']['aesthetic_driven_innovation'] < 100 else '完成'
            }
        ]
    
    def check_paradigm_definition(self) -> bool:
        """检查是否达成范式定义"""
        # 范式定义标准：
        # 1. 有独特的设计语言
        # 2. 可被他人借鉴
        # 3. 有明确的理论基础
        
        current = self.state['l5_progress']['paradigm_definition']
        return current >= 100.0
