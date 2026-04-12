#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ant Design Template - Phase 4: 范式定义

来源：Ant Design 5.0 (2026)
融合：太一风格（苹果 80% + 东方 15% + 中国 5%）
"""

from typing import Dict


ANT_DESIGN = {
    'name': 'Ant Design 5.0',
    'version': '2026',
    'fusion_ratio': {
        'ant': 60,
        'taiyi_apple': 25,
        'taiyi_oriental': 10,
        'taiyi_chinese': 5
    },
    
    # 色彩系统
    'colors': {
        'primary': '#1677FF',  # Ant Blue
        'success': '#52C41A',
        'warning': '#FAAD14',
        'error': '#FF4D4F',
        
        # 太一融合
        'taiyi_primary': '#8E8E93',
        'taiyi_accent': '#007AFF',
        'taiyi_zen': '#7D8447',
        'taiyi_skyblue': '#87CEEB'
    },
    
    # 字体系统
    'typography': {
        'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif',
        'font_family_code': '"SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace',
        'scale': {
            'xxl': '38px',
            'xl': '30px',
            'lg': '24px',
            'md': '20px',
            'sm': '16px',
            'xs': '14px'
        }
    },
    
    # 间距系统（4px 基准）
    'spacing': {
        'xs': 4,
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 20,
        'xxl': 24,
        'xxxl': 32
    },
    
    # 圆角系统
    'radius': {
        'xs': 2,
        'sm': 4,
        'md': 6,
        'lg': 8,
        'xl': 12,
        'xxl': 16
    },
    
    # 阴影系统
    'shadows': {
        'none': 'none',
        'sm': '0 1px 2px 0 rgba(0,0,0,0.03)',
        'md': '0 2px 8px 0 rgba(0,0,0,0.06)',
        'lg': '0 4px 12px 0 rgba(0,0,0,0.08)',
        'xl': '0 8px 24px 0 rgba(0,0,0,0.12)'
    },
    
    # 核心原则
    'principles': [
        '确定性 (Deterministic)',
        '意义感 (Meaningful)',
        '生长性 (Growth)',
        '自然 (Natural)',
        '企业级 (Enterprise-grade)'
    ],
    
    # 与太一融合点
    'fusion_points': {
        'ant_taiyi': [
            'Ant 的企业级 + 太一的极简 = 专业简洁',
            'Ant 的确定性 + 太一的克制 = 可靠优雅',
            'Ant 的生长性 + 太一的进化 = 持续生长',
            'Ant 的自然 + 太一的东方哲学 = 道法自然'
        ]
    }
}


def get_css_variables() -> str:
    """生成 CSS 变量"""
    css = [":root {"]
    
    # 颜色变量
    for name, value in ANT_DESIGN['colors'].items():
        css.append(f"  --ant-{name}: {value};")
    
    # 间距变量
    for name, value in ANT_DESIGN['spacing'].items():
        css.append(f"  --ant-spacing-{name}: {value}px;")
    
    # 圆角变量
    for name, value in ANT_DESIGN['radius'].items():
        css.append(f"  --ant-radius-{name}: {value}px;")
    
    # 阴影变量
    for name, value in ANT_DESIGN['shadows'].items():
        css.append(f"  --ant-shadow-{name}: {value};")
    
    css.append("}")
    return "\n".join(css)


def get_design_tokens() -> Dict:
    """获取设计令牌"""
    return ANT_DESIGN
