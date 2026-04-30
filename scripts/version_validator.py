#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本锁定校验器

太一 v4.0 - 执行前版本校验（Claude Code 精华融合）

功能：
- 检查 Skills 版本是否锁定
- 验证模型可用性
- 确认配置完整性
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path('/home/nicola/.openclaw/workspace')
SKILLS_LOCK_FILE = WORKSPACE / 'skills-lock.json'
LOG_DIR = WORKSPACE / 'logs' / 'version-check'
LOG_DIR.mkdir(parents=True, exist_ok=True)


def load_skills_lock() -> dict:
    """加载版本锁定配置"""
    if not SKILLS_LOCK_FILE.exists():
        return {
            'version': 'unknown',
            'skills': {},
            'models': {},
            'validation': {'enabled': False}
        }
    
    with open(SKILLS_LOCK_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_skill(skill_name: str, lock_config: dict) -> dict:
    """
    验证单个 Skill
    
    返回:
        {
            'passed': bool,
            'error': str (optional),
            'warning': str (optional)
        }
    """
    skills = lock_config.get('skills', {})
    
    if skill_name not in skills:
        return {
            'passed': True,  # 未锁定的技能允许使用
            'warning': f'Skill {skill_name} 未在 skills-lock.json 中定义'
        }
    
    skill_info = skills[skill_name]
    
    # 检查是否锁定
    if not skill_info.get('locked', False):
        return {
            'passed': True,
            'warning': f'Skill {skill_name} 未锁定（版本可能变化）'
        }
    
    # 检查是否有 commit
    if not skill_info.get('commit'):
        return {
            'passed': False,
            'error': f'Skill {skill_name} 已锁定但未指定 commit'
        }
    
    # 验证通过
    return {
        'passed': True,
        'info': f'{skill_name} v{skill_info.get("version")} ({skill_info.get("commit")[:8]})'
    }


def validate_model(model_type: str, lock_config: dict) -> dict:
    """
    验证模型配置
    
    返回:
        {
            'passed': bool,
            'error': str (optional),
            'model': str (optional)
        }
    """
    models = lock_config.get('models', {})
    
    if model_type not in models:
        return {
            'passed': True,
            'warning': f'模型类型 {model_type} 未配置，使用默认模型'
        }
    
    model_config = models[model_type]
    
    # 检查主模型
    if not model_config.get('model'):
        return {
            'passed': False,
            'error': f'模型类型 {model_type} 未指定主模型'
        }
    
    # 检查 fallback
    if not model_config.get('fallback'):
        return {
            'passed': True,
            'warning': f'模型类型 {model_type} 未指定 fallback'
        }
    
    return {
        'passed': True,
        'model': model_config.get('model'),
        'fallback': model_config.get('fallback')
    }


def validate_before_execute(
    required_skills: list,
    model_type: str = 'default'
) -> dict:
    """
    执行前完整校验
    
    参数:
        required_skills: 需要的 Skills 列表
        model_type: 使用的模型类型
    
    返回:
        {
            'passed': bool,
            'errors': list,
            'warnings': list,
            'info': list
        }
    """
    lock_config = load_skills_lock()
    
    result = {
        'passed': True,
        'errors': [],
        'warnings': [],
        'info': [],
        'timestamp': datetime.now().isoformat()
    }
    
    # 检查是否启用校验
    validation = lock_config.get('validation', {})
    if not validation.get('enabled', False):
        result['warnings'].append('版本校验未启用')
        return result
    
    # 验证 Skills
    for skill in required_skills:
        skill_result = validate_skill(skill, lock_config)
        
        if not skill_result['passed']:
            result['passed'] = False
            result['errors'].append(skill_result['error'])
        elif 'warning' in skill_result:
            result['warnings'].append(skill_result['warning'])
        elif 'info' in skill_result:
            result['info'].append(skill_result['info'])
    
    # 验证模型
    model_result = validate_model(model_type, lock_config)
    
    if not model_result['passed']:
        result['passed'] = False
        result['errors'].append(model_result['error'])
    elif 'warning' in model_result:
        result['warnings'].append(model_result['warning'])
    elif 'model' in model_result:
        result['info'].append(f"模型：{model_result['model']} (fallback: {model_result['fallback']})")
    
    # 记录日志
    log_validation(result)
    
    return result


def log_validation(result: dict):
    """记录校验日志"""
    log_file = LOG_DIR / f"validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"📝 校验日志：{log_file}")


def main():
    """命令行测试"""
    if len(sys.argv) < 2:
        print("用法：python3 version_validator.py <skill1> [skill2] ... [--model <model_type>]")
        print("示例：python3 version_validator.py zhiji-e paoding --model trading")
        sys.exit(1)
    
    # 解析参数
    required_skills = []
    model_type = 'default'
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--model':
            model_type = sys.argv[i + 1]
            i += 2
        else:
            required_skills.append(sys.argv[i])
            i += 1
    
    # 执行校验
    result = validate_before_execute(required_skills, model_type)
    
    # 输出结果
    print(f"\n{'✅' if result['passed'] else '❌'} 版本校验{'通过' if result['passed'] else '失败'}")
    
    if result['info']:
        print(f"\n信息:")
        for info in result['info']:
            print(f"  - {info}")
    
    if result['warnings']:
        print(f"\n警告:")
        for warning in result['warnings']:
            print(f"  - {warning}")
    
    if result['errors']:
        print(f"\n错误:")
        for error in result['errors']:
            print(f"  - {error}")
    
    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
