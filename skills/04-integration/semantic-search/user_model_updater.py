#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Model Updater - 用户模型自动更新

版本：v1.0 | 创建：2026-04-08
功能：从对话中自动学习，更新用户模型
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class UserModelUpdater:
    """用户模型更新器"""
    
    def __init__(self, model_path: str = '/home/nicola/.openclaw/workspace/memory/user-model.json'):
        self.model_path = Path(model_path)
        self.model = self._load_model()
    
    def _load_model(self) -> Dict:
        """加载用户模型"""
        if self.model_path.exists():
            with open(self.model_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_default_model()
    
    def _create_default_model(self) -> Dict:
        """创建默认模型"""
        return {
            "version": "2.0",
            "updated_at": datetime.now().isoformat(),
            "core": {
                "values": ["负熵", "效率", "艺术化存在", "第一性原理"],
                "long_term_goals": ["AGI 实现", "知识传承", "太一体系完善"],
                "basic_preferences": {
                    "communication_style": "极简黑客风",
                    "decision_making": "第一性原理",
                    "learning_style": "费曼技巧",
                    "work_rhythm": "深度工作优先"
                }
            },
            "contextual": {
                "work_mode": {
                    "focus_hours": "09:00-12:00, 14:00-18:00, 22:00-23:00",
                    "preferred_tools": ["CLI", "Python", "Git", "OpenClaw"],
                    "collaboration_style": "异步优先",
                    "current_projects": ["太一 AGI 系统"]
                },
                "learning_mode": {
                    "current_topics": [],
                    "learning_pace": "密集型",
                    "preferred_format": "实践驱动",
                    "recent_insights": []
                },
                "creation_mode": {
                    "output_types": ["技能", "宪法", "文档"],
                    "quality_standard": "生产就绪",
                    "iteration_style": "快速原型→完善"
                }
            },
            "evolutionary": {
                "recent_attention": [],
                "skill_growth": [],
                "cognitive_shifts": [],
                "future_self": {
                    "1_month": "",
                    "3_months": "",
                    "6_months": "",
                    "1_year": ""
                }
            },
            "change_log": []
        }
    
    def update(self, session_log: str) -> Dict:
        """从对话中更新用户模型"""
        # 1. 提取新信息
        new_info = self._extract_user_info(session_log)
        
        # 2. 检测认知转变
        shifts = self._detect_cognitive_shifts(session_log)
        
        # 3. 更新情境层
        self._merge_contextual(new_info)
        
        # 4. 更新演化层
        if shifts:
            self._add_cognitive_shifts(shifts)
        
        # 5. 更新近期关注
        self._update_recent_attention(new_info)
        
        # 6. 更新时间戳
        self.model['updated_at'] = datetime.now().isoformat()
        
        # 7. 保存
        self._save_model()
        
        return self.model
    
    def _extract_user_info(self, log: str) -> Dict:
        """从对话中提取用户信息"""
        info = {
            'topics': [],
            'preferences': [],
            'projects': [],
            'insights': []
        }
        
        # 提取学习主题
        topic_patterns = [
            r'(?:关注 | 学习 | 研究)[：:]\s*([\u4e00-\u9fa5\w\s,]+)',
            r'最近在看 ([\u4e00-\u9fa5\w\s,]+)',
        ]
        for pattern in topic_patterns:
            matches = re.findall(pattern, log, re.IGNORECASE)
            info['topics'].extend(matches)
        
        # 提取偏好
        pref_patterns = [
            r'(?:喜欢 | 偏好 | 倾向于)[：:]\s*([\u4e00-\u9fa5\w\s,]+)',
            r'我觉得 ([\u4e00-\u9fa5\w\s]+) 更好',
        ]
        for pattern in pref_patterns:
            matches = re.findall(pattern, log, re.IGNORECASE)
            info['preferences'].extend(matches)
        
        # 提取项目
        project_patterns = [
            r'(?:在做 | 开发 | 构建)[：:]\s*([\u4e00-\u9fa5\w\s,]+)',
            r'当前项目 [：:]\s*([\u4e00-\u9fa5\w\s,]+)',
        ]
        for pattern in project_patterns:
            matches = re.findall(pattern, log, re.IGNORECASE)
            info['projects'].extend(matches)
        
        # 提取洞察
        insight_patterns = [
            r'(?:发现 | 意识到 | 学到)[：:]\s*([\u4e00-\u9fa5\w\s,]+)',
            r'关键洞察 [：:]\s*([\u4e00-\u9fa5\w\s,]+)',
        ]
        for pattern in insight_patterns:
            matches = re.findall(pattern, log, re.IGNORECASE)
            info['insights'].extend(matches)
        
        return info
    
    def _detect_cognitive_shifts(self, log: str) -> List[Dict]:
        """检测认知转变"""
        shifts = []
        
        # 模式 1: 明确陈述
        patterns = [
            (r'我觉得 (.*?) 更重要', '价值观'),
            (r'我现在 (.*?) 以前', '偏好'),
            (r'我发现 (.*?) 更有效', '方法'),
            (r'我决定 (.*?) 不再', '行为'),
            (r'从 (.*?) 到 (.*?)', '转变'),
        ]
        
        for pattern, shift_type in patterns:
            matches = re.findall(pattern, log, re.IGNORECASE)
            for match in matches:
                shifts.append({
                    'type': shift_type,
                    'evidence': match,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'confidence': 0.8
                })
        
        return shifts
    
    def _merge_contextual(self, new_info: Dict):
        """合并情境层信息"""
        # 更新学习主题
        if new_info['topics']:
            current_topics = set(self.model['contextual']['learning_mode']['current_topics'])
            current_topics.update(new_info['topics'])
            self.model['contextual']['learning_mode']['current_topics'] = list(current_topics)
        
        # 更新当前项目
        if new_info['projects']:
            current_projects = set(self.model['contextual']['work_mode']['current_projects'])
            current_projects.update(new_info['projects'])
            self.model['contextual']['work_mode']['current_projects'] = list(current_projects)
        
        # 更新最近洞察
        if new_info['insights']:
            current_insights = self.model['contextual']['learning_mode']['recent_insights']
            current_insights.extend(new_info['insights'])
            self.model['contextual']['learning_mode']['recent_insights'] = current_insights[-10:]  # 保留最近 10 条
    
    def _add_cognitive_shifts(self, shifts: List[Dict]):
        """添加认知转变"""
        for shift in shifts:
            # 添加到认知转变列表
            shift_summary = f"{shift['type']}: {shift['evidence']}"
            if shift_summary not in self.model['evolutionary']['cognitive_shifts']:
                self.model['evolutionary']['cognitive_shifts'].append(shift_summary)
            
            # 添加到变更日志
            self.model['change_log'].append({
                'date': shift['date'],
                'type': 'cognitive_shift',
                'description': shift_summary,
                'impact': '用户模型自动更新',
                'related_files': []
            })
    
    def _update_recent_attention(self, new_info: Dict):
        """更新近期关注"""
        attention = []
        attention.extend(new_info['topics'])
        attention.extend(new_info['projects'])
        
        if attention:
            current_attention = set(self.model['evolutionary']['recent_attention'])
            current_attention.update(attention)
            self.model['evolutionary']['recent_attention'] = list(current_attention)[-10:]  # 保留最近 10 条
    
    def _save_model(self):
        """保存用户模型"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, 'w', encoding='utf-8') as f:
            json.dump(self.model, f, ensure_ascii=False, indent=2)
    
    def get_model(self) -> Dict:
        """获取用户模型"""
        return self.model
    
    def query(self, field: str) -> any:
        """查询特定字段"""
        keys = field.split('.')
        value = self.model
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value


# 使用示例
if __name__ == '__main__':
    updater = UserModelUpdater()
    
    # 示例对话
    session_log = """
SAYELF: 我最近开始关注 Hermes Agent 的自学习机制
SAYELF: 我觉得太一也应该有类似的自动技能生成能力
SAYELF: 正在开发地理感知路由 v2.0
SAYELF: 我发现实践驱动的学习方式更有效
"""
    
    # 更新模型
    updated_model = updater.update(session_log)
    
    print("用户模型已更新：")
    print(f"最近关注：{updated_model['evolutionary']['recent_attention']}")
    print(f"认知转变：{updated_model['evolutionary']['cognitive_shifts']}")
    print(f"变更日志：{len(updated_model['change_log'])} 条")
