#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Material Design Template - Phase 4: 范式定义

来源：Material Design 3 (2026)
融合：太一风格（苹果 80% + 东方 15% + 中国 5%）
"""

from typing import Dict


GOOGLE_MATERIAL_DESIGN = {
    'name': 'Google Material Design 3',
    'version': '2026',
    'fusion_ratio': {
        'material': 70,
        'taiyi_apple': 20,
        'taiyi_oriental': 7,
        'taiyi_chinese': 3
    },
    
    # 色彩系统
    'colors': {
        'primary': '#4285F4',  # Google Blue
        'secondary': '#34A853',  # Google Green
        'tertiary': '#FBBC05',  # Google Yellow
        'error': '#EA4335',  # Google Red
        
        # 太一融合
        'taiyi_primary': '#8E8E93',  # 苹果灰
        'taiyi_accent': '#007AFF',  # 苹果蓝
        'taiyi_zen': '#7D8447',  # 东方禅意绿
        'taiyi_skyblue': '#87CEEB'  # 中国天青
    },
    
    # 字体系统
    'typography': {
        'font_family': 'Roboto, "Noto Sans SC", sans-serif',
        'scale': {
            'display_large': '57px',
            'display_medium': '45px',
            'display_small': '36px',
            'headline_large': '32px',
            'headline_medium': '28px',
            'headline_small': '24px',
            'title_large': '22px',
            'title_medium': '16px',
            'title_small': '14px',
            'body_large': '16px',
            'body_medium': '14px',
            'body_small': '12px',
            'label_large': '14px',
            'label_medium': '12px',
            'label_small': '11px'
        }
    },
    
    # 间距系统（8px 基准）
    'spacing': {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48,
        'xxxl': 64
    },
    
    # 圆角系统
    'radius': {
        'none': 0,
        'sm': 4,
        'md': 8,
        'lg': 12,
        'xl': 16,
        'xxl': 24,
        'full': 9999
    },
    
    # 阴影系统
    'shadows': {
        'none': 'none',
        'sm': '0 1px 2px rgba(0,0,0,0.3), 0 1px 3px 1px rgba(0,0,0,0.15)',
        'md': '0 1px 2px rgba(0,0,0,0.3), 0 2px 6px 2px rgba(0,0,0,0.15)',
        'lg': '0 1px 3px rgba(0,0,0,0.3), 0 4px 8px 3px rgba(0,0,0,0.15)',
        'xl': '0 1px 3px rgba(0,0,0,0.3), 0 8px 16px 4px rgba(0,0,0,0.15)',
        'xxl': '0 1px 3px rgba(0,0,0,0.3), 0 16px 32px 6px rgba(0,0,0,0.15)'
    },
    
    # 核心原则
    'principles': [
        'Material is texture (纸质质感)',
        'Bold, graphic, intentional (大胆/图形化/有意)',
        'Motion provides meaning (动效赋予意义)',
        'Adaptive design (自适应设计)',
        'Accessible to all (人人可用)'
    ],
    
    # 与太一融合点
    'fusion_points': {
        'material_taiyi': [
            'Material 的纸质质感 + 太一的极简 = 轻盈克制',
            'Material 的大胆用色 + 太一的苹果灰 = 专业活力',
            'Material 的动效 + 太一的留白 = 有意义的运动',
            'Material 的自适应 + 太一的东方哲学 = 道法自然'
        ]
    }
}


def get_css_variables() -> str:
    """生成 CSS 变量"""
    css = [":root {"]
    
    # 颜色变量
    for name, value in GOOGLE_MATERIAL_DESIGN['colors'].items():
        css.append(f"  --material-{name}: {value};")
    
    # 间距变量
    for name, value in GOOGLE_MATERIAL_DESIGN['spacing'].items():
        css.append(f"  --material-spacing-{name}: {value}px;")
    
    # 圆角变量
    for name, value in GOOGLE_MATERIAL_DESIGN['radius'].items():
        css.append(f"  --material-radius-{name}: {value}px;")
    
    # 阴影变量
    for name, value in GOOGLE_MATERIAL_DESIGN['shadows'].items():
        css.append(f"  --material-shadow-{name}: {value};")
    
    css.append("}")
    return "\n".join(css)


def get_design_tokens() -> Dict:
    """获取设计令牌"""
    return GOOGLE_MATERIAL_DESIGN
