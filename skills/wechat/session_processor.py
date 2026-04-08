#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信会话处理器 - 用户模型自动更新

每次会话后自动更新用户模型
"""

import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/semantic-search')

from user_model_updater import UserModelUpdater


def handle_session_end(session_log: str) -> dict:
    """处理会话结束，更新用户模型"""
    updater = UserModelUpdater()
    
    try:
        # 更新用户模型
        updated_model = updater.update(session_log)
        
        # 检测认知转变
        shifts = detect_cognitive_shifts(session_log)
        
        # 返回更新摘要
        return {
            'updated': True,
            'recent_attention': updated_model['evolutionary']['recent_attention'][-5:],
            'cognitive_shifts': shifts,
            'updated_at': updated_model['updated_at']
        }
    
    finally:
        pass  # 不需要关闭，JSON 文件


def detect_cognitive_shifts(session_log: str) -> list:
    """检测认知转变"""
    shifts = []
    
    # 认知转变模式
    patterns = [
        (r'我觉得 (.*?) 更重要', '价值观'),
        (r'我现在 (.*?) 以前', '偏好'),
        (r'我发现 (.*?) 更有效', '方法'),
        (r'我决定 (.*?) 不再', '行为'),
    ]
    
    import re
    for pattern, shift_type in patterns:
        matches = re.findall(pattern, session_log, re.IGNORECASE)
        for match in matches:
            shifts.append({
                'type': shift_type,
                'content': match,
                'date': '2026-04-09'
            })
    
    return shifts


def get_user_summary() -> str:
    """获取用户摘要（用于个性化响应）"""
    updater = UserModelUpdater()
    model = updater.get_model()
    
    summary = {
        'communication_style': model['core']['basic_preferences']['communication_style'],
        'current_topics': model['contextual']['learning_mode']['current_topics'][-3:],
        'recent_attention': model['evolutionary']['recent_attention'][-3:]
    }
    
    return summary


# 测试
if __name__ == '__main__':
    # 测试会话日志
    session_log = """
SAYELF: 我最近开始关注 Hermes Agent 的自学习机制
SAYELF: 我觉得太一也应该有类似的自动技能生成能力
SAYELF: 正在开发地理感知路由 v2.0
SAYELF: 我发现实践驱动的学习方式更有效
"""
    
    # 更新用户模型
    result = handle_session_end(session_log)
    
    print("✅ 用户模型已更新")
    print(f"最近关注：{result['recent_attention']}")
    print(f"认知转变：{result['cognitive_shifts']}")
    print(f"更新时间：{result['updated_at']}")
    
    # 获取用户摘要
    summary = get_user_summary()
    print(f"\n📊 用户摘要:")
    print(f"沟通风格：{summary['communication_style']}")
    print(f"当前主题：{summary['current_topics']}")
    print(f"最近关注：{summary['recent_attention']}")
