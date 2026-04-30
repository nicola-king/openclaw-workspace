#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 个性配置系统
太一 AGI · 2026-04-18

功能:
- 加载用户偏好配置
- 动态调整 Agent 个性
- 记忆用户习惯
- 智能推荐配置

用法:
    from agent_personality_config import AgentPersonalityConfig
    config = AgentPersonalityConfig()
    config.apply_personality('zhiji', {'voice': '冷静理性'})
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class AgentPersonalityConfig:
    """Agent 个性配置管理器"""
    
    def __init__(self, config_path: str = None):
        """初始化配置管理器"""
        self.config_path = config_path or "/home/nicola/.openclaw/workspace/memory/user-preferences.json"
        self.config = self._load_config()
        self.history = []
        
        print("🎭 Agent 个性配置系统已初始化")
        print(f"   配置文件：{self.config_path}")
        print()
    
    def _load_config(self) -> Dict:
        """加载用户配置"""
        path = Path(self.config_path)
        if not path.exists():
            print(f"⚠️  配置文件不存在，使用默认配置")
            return self._get_default_config()
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_default_config(self) -> Dict:
        """默认配置"""
        return {
            "communication": {
                "preferred_channel": "wechat",
                "emoji_preference": "abundant",
                "format_preference": "structured"
            },
            "agent_preferences": {
                "zhiji": {
                    "voice": "冷静理性",
                    "detail_level": "detailed",
                    "risk_tolerance": "中等"
                },
                "shanmu": {
                    "voice": "温暖亲切",
                    "content_style": "创意优美"
                },
                "suwen": {
                    "voice": "温和专业",
                    "focus": "中医养生"
                },
                "wangliang": {
                    "voice": "严谨专业",
                    "alert_threshold": "P1"
                },
                "paoding": {
                    "voice": "技术极客",
                    "code_comments": "detailed"
                }
            }
        }
    
    def get_agent_personality(self, agent_name: str) -> Dict:
        """获取指定 Agent 的个性配置"""
        agents = self.config.get('agent_preferences', {})
        return agents.get(agent_name, {})
    
    def apply_personality(self, agent_name: str, personality: Dict) -> bool:
        """应用个性配置到 Agent"""
        if 'agent_preferences' not in self.config:
            self.config['agent_preferences'] = {}
        
        if agent_name not in self.config['agent_preferences']:
            self.config['agent_preferences'][agent_name] = {}
        
        # 更新配置
        self.config['agent_preferences'][agent_name].update(personality)
        
        # 记录历史
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'agent': agent_name,
            'changes': personality
        })
        
        # 保存到文件
        self._save_config()
        
        print(f"✅ 已更新 {agent_name} 的个性配置")
        print(f"   更新内容：{personality}")
        return True
    
    def get_communication_preference(self) -> Dict:
        """获取通讯偏好"""
        return self.config.get('communication', {})
    
    def get_report_preference(self, report_type: str) -> Dict:
        """获取报告偏好"""
        reports = self.config.get('report_preferences', {})
        return reports.get(report_type, {})
    
    def recommend_configuration(self, agent_name: str) -> Dict:
        """基于使用习惯推荐配置"""
        # 分析历史使用记录
        agent_history = [h for h in self.history if h['agent'] == agent_name]
        
        if not agent_history:
            # 无历史记录，返回默认推荐
            return self._get_default_recommendation(agent_name)
        
        # 分析最常修改的配置项
        config_changes = {}
        for record in agent_history:
            for key in record['changes']:
                config_changes[key] = config_changes.get(key, 0) + 1
        
        # 返回推荐
        return {
            'agent': agent_name,
            'frequent_adjustments': config_changes,
            'recommendation': '基于使用习惯，建议固定以下配置',
            'suggested_config': self.get_agent_personality(agent_name)
        }
    
    def _get_default_recommendation(self, agent_name: str) -> Dict:
        """默认推荐配置"""
        recommendations = {
            'zhiji': {
                'voice': '冷静理性',
                'detail_level': 'detailed',
                'include_charts': True
            },
            'shanmu': {
                'voice': '温暖亲切',
                'content_style': '创意优美',
                'require_review': True
            },
            'suwen': {
                'voice': '温和专业',
                'focus': '中医养生',
                'include_recipes': True
            },
            'wangliang': {
                'voice': '严谨专业',
                'alert_threshold': 'P1',
                'report_frequency': 'daily'
            },
            'paoding': {
                'voice': '技术极客',
                'code_comments': 'detailed',
                'require_review': True
            }
        }
        
        return {
            'agent': agent_name,
            'recommendation': '新 Agent，建议使用默认配置',
            'suggested_config': recommendations.get(agent_name, {})
        }
    
    def _save_config(self):
        """保存配置到文件"""
        self.config['updated'] = datetime.now().strftime('%Y-%m-%d')
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def show_config(self):
        """显示当前配置"""
        print("\n📋 当前配置概览")
        print("=" * 50)
        
        # 通讯偏好
        comm = self.get_communication_preference()
        print(f"\n📱 通讯偏好:")
        for key, value in comm.items():
            print(f"   {key}: {value}")
        
        # Agent 偏好
        print(f"\n Agent 偏好:")
        for agent, prefs in self.config.get('agent_preferences', {}).items():
            print(f"\n   {agent}:")
            for key, value in prefs.items():
                print(f"      {key}: {value}")
        
        # 报告偏好
        print(f"\n📊 报告偏好:")
        for report_type, prefs in self.config.get('report_preferences', {}).items():
            enabled = "✅" if prefs.get('enabled') else "❌"
            time = prefs.get('time', 'N/A')
            print(f"   {enabled} {report_type}: {time}")
        
        print()


if __name__ == '__main__':
    # 测试配置系统
    config = AgentPersonalityConfig()
    config.show_config()
    
    # 测试更新配置
    config.apply_personality('zhiji', {
        'voice': '冷静理性',
        'risk_tolerance': '中等偏保守'
    })
    
    # 获取推荐
    rec = config.recommend_configuration('zhiji')
    print(f"\n💡 配置推荐：{rec}")
