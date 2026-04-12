#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feedback Collector - 反馈收集系统
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class FeedbackCollector:
    """反馈收集器"""
    
    def __init__(self, output_dir: str = "~/.openclaw/workspace/skills/taiyi-artisan/feedback"):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.output_dir / "feedback_log.jsonl"
    
    def collect(self, output_type: str, output_id: str, reaction: str, 
                details: str = "", score: Optional[float] = None) -> dict:
        """
        收集反馈
        
        Args:
            output_type: 输出类型 (wisdom_card/chart/code/text)
            output_id: 输出 ID（文件名或哈希）
            reaction: 反应 (positive/negative/suggestion)
            details: 详细反馈
            score: 评分（0-100）
        
        Returns:
            反馈记录
        """
        feedback = {
            'timestamp': datetime.now().isoformat(),
            'output_type': output_type,
            'output_id': output_id,
            'reaction': reaction,
            'details': details,
            'score': score
        }
        
        # 记录到日志
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback, ensure_ascii=False) + '\n')
        
        return feedback
    
    def get_recent(self, limit: int = 10) -> list:
        """获取最近的反馈"""
        if not self.log_file.exists():
            return []
        
        feedbacks = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    feedbacks.append(json.loads(line))
        
        return feedbacks[-limit:]
    
    def get_stats(self) -> dict:
        """获取反馈统计"""
        if not self.log_file.exists():
            return {'total': 0, 'positive': 0, 'negative': 0, 'avg_score': 0}
        
        feedbacks = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    feedbacks.append(json.loads(line))
        
        total = len(feedbacks)
        positive = sum(1 for f in feedbacks if f['reaction'] == 'positive')
        negative = sum(1 for f in feedbacks if f['reaction'] == 'negative')
        
        scores = [f['score'] for f in feedbacks if f.get('score')]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'total': total,
            'positive': positive,
            'negative': negative,
            'suggestions': total - positive - negative,
            'positive_ratio': positive / total * 100 if total > 0 else 0,
            'avg_score': avg_score
        }
