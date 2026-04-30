#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolution Core - L5 自进化核心

来源：Aesthetic Evolution（蒸馏后）
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class Feedback:
    """用户反馈"""
    timestamp: str
    output_type: str
    output_id: str
    reaction: str  # positive/negative/suggestion
    details: str = ""
    score: Optional[float] = None  # 0-100


@dataclass
class EvolutionState:
    """进化状态"""
    total_feedbacks: int = 0
    positive_count: int = 0
    negative_count: int = 0
    style_params: Dict = field(default_factory=dict)
    last_evolution: Optional[str] = None
    l5_progress: float = 45.0  # L5 进度百分比


class EvolutionCore:
    """L5 自进化核心"""
    
    def __init__(self, workspace: str = "~/.openclaw/workspace"):
        self.workspace = Path(workspace).expanduser()
        self.state_file = self.workspace / "skills/taiyi-artisan/evolution_state.json"
        self.feedback_log = self.workspace / "skills/taiyi-artisan/feedback_log.jsonl"
        self.state = self._load_state()
    
    def _load_state(self) -> EvolutionState:
        """加载进化状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return EvolutionState(**data)
        return EvolutionState()
    
    def _save_state(self):
        """保存进化状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_feedbacks': self.state.total_feedbacks,
                'positive_count': self.state.positive_count,
                'negative_count': self.state.negative_count,
                'style_params': self.state.style_params,
                'last_evolution': self.state.last_evolution,
                'l5_progress': self.state.l5_progress
            }, f, ensure_ascii=False, indent=2)
    
    def collect_feedback(self, feedback: Feedback):
        """
        收集反馈
        
        Args:
            feedback: 反馈对象
        """
        # 记录到日志
        with open(self.feedback_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback.__dict__, ensure_ascii=False) + '\n')
        
        # 更新状态
        self.state.total_feedbacks += 1
        if feedback.reaction == 'positive':
            self.state.positive_count += 1
        elif feedback.reaction == 'negative':
            self.state.negative_count += 1
        
        self._save_state()
    
    def analyze_feedback(self, feedback: Feedback) -> Dict:
        """
        分析反馈
        
        Args:
            feedback: 反馈对象
        
        Returns:
            分析结果（洞察）
        """
        insights = {
            'sentiment': feedback.reaction,
            'output_type': feedback.output_type,
            'timestamp': feedback.timestamp
        }
        
        if feedback.score:
            insights['quality_score'] = feedback.score
        
        if feedback.details:
            insights['keywords'] = self._extract_keywords(feedback.details)
        
        return insights
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词（简化版）"""
        # TODO: 实现更智能的关键词提取
        keywords = ['美', '丑', '简洁', '复杂', '喜欢', '不喜欢', '好', '不好']
        return [kw for kw in keywords if kw in text]
    
    def evolve_style(self, insights: List[Dict]) -> Dict:
        """
        根据洞察进化风格
        
        Args:
            insights: 分析结果列表
        
        Returns:
            新生成的风格标准
        """
        # 统计正面/负面反馈模式
        positive_patterns = []
        negative_patterns = []
        
        for insight in insights:
            if insight.get('sentiment') == 'positive':
                positive_patterns.append(insight)
            else:
                negative_patterns.append(insight)
        
        # 更新风格参数
        if positive_patterns:
            # 强化正面特征
            for pattern in positive_patterns:
                feature = pattern.get('output_type')
                if feature:
                    current = self.state.style_params.get(feature, 1.0)
                    self.state.style_params[feature] = min(2.0, current + 0.1)
        
        if negative_patterns:
            # 调整负面特征
            for pattern in negative_patterns:
                feature = pattern.get('output_type')
                if feature:
                    current = self.state.style_params.get(feature, 1.0)
                    self.state.style_params[feature] = max(0.5, current - 0.1)
        
        # 更新进化时间
        self.state.last_evolution = datetime.now().isoformat()
        
        # 计算 L5 进度（简化版）
        self._calculate_l5_progress()
        
        self._save_state()
        
        return {
            'style_params': self.state.style_params,
            'l5_progress': self.state.l5_progress,
            'evolved_at': self.state.last_evolution
        }
    
    def _calculate_l5_progress(self):
        """计算 L5 进度"""
        # 维度权重
        dimensions = {
            'style': 0.60,  # 风格识别
            'paradigm': 0.30,  # 范式定义
            'evolution': 0.40,  # 自主进化
            'innovation': 0.50  # 美学驱动
        }
        
        # 基于反馈数量调整进度
        feedback_factor = min(1.0, self.state.total_feedbacks / 100)
        
        # 计算总进度
        base_progress = sum(dimensions.values()) / len(dimensions) * 100
        self.state.l5_progress = min(95.0, base_progress + feedback_factor * 20)
    
    def check_taiyi_style(self, output: str) -> bool:
        """
        检查是否具有太一风格
        
        Args:
            output: 输出内容
        
        Returns:
            是否符合太一风格
        """
        # TODO: 实现风格检查逻辑
        # 当前返回默认值
        return True
    
    def get_evolution_report(self) -> Dict:
        """生成进化报告"""
        return {
            'total_feedbacks': self.state.total_feedbacks,
            'positive_ratio': (
                self.state.positive_count / self.state.total_feedbacks * 100
                if self.state.total_feedbacks > 0 else 0
            ),
            'l5_progress': self.state.l5_progress,
            'style_params': self.state.style_params,
            'last_evolution': self.state.last_evolution
        }
    
    def get_l5_milestones(self) -> List[Dict]:
        """获取 L5 里程碑状态"""
        return [
            {
                'name': '风格识别',
                'description': '用户能识别"太一风格"',
                'target_date': '2026-04-17',
                'status': '进行中',
                'progress': 60
            },
            {
                'name': '范式定义',
                'description': '创造 1 个可借鉴模式',
                'target_date': '2026-04-24',
                'status': '待达成',
                'progress': 30
            },
            {
                'name': '自主进化',
                'description': '美学系统能自主学习',
                'target_date': '2026-05-01',
                'status': '待达成',
                'progress': 40
            },
            {
                'name': '美学驱动',
                'description': '3 次因美学而创新',
                'target_date': '2026-05-08',
                'status': '进行中',
                'progress': 50
            }
        ]
