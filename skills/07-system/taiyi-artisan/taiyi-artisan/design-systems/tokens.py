#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Design Tokens - 设计令牌系统

来源：Apple Design + IBM Carbon + 东方美学 + 中国传统
融合原则：苹果 80% + 东方 15% + 中国 5%
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class ColorToken:
    """颜色令牌"""
    name: str
    value: str
    source: str  # apple/oriental/chinese
    usage: str


@dataclass
class SpacingToken:
    """间距令牌"""
    name: str
    value: int  # px
    base: str  # 4px baseline


@dataclass
class RadiusToken:
    """圆角令牌"""
    name: str
    value: int  # px
    usage: str


@dataclass
class ShadowToken:
    """阴影令牌"""
    name: str
    value: str
    usage: str


class DesignTokens:
    """设计令牌系统"""
    
    # 配色系统
    COLORS: Dict[str, ColorToken] = {
        # 苹果主色（80%）
        'primary': ColorToken('primary', '#8E8E93', 'apple', '次要文字'),
        'background': ColorToken('background', '#FFFFFF', 'apple', '背景色'),
        'text': ColorToken('text', '#1D1D1F', 'apple', '主要文字'),
        'accent': ColorToken('accent', '#007AFF', 'apple', '强调/链接'),
        'success': ColorToken('success', '#34C759', 'apple', '成功状态'),
        'warning': ColorToken('warning', '#FF9500', 'apple', '警告状态'),
        'error': ColorToken('error', '#FF3B30', 'apple', '错误状态'),
        
        # 东方色（15%）
        'zen': ColorToken('zen', '#7D8447', 'oriental', '禅意绿'),
        'sakura': ColorToken('sakura', '#FFB7C5', 'oriental', '樱花粉'),
        'indigo': ColorToken('indigo', '#1E3A5F', 'oriental', '靛蓝'),
        'wabi': ColorToken('wabi', '#8B7355', 'oriental', '侘寂色'),
        
        # 中国色（5%）
        'skyblue': ColorToken('skyblue', '#87CEEB', 'chinese', '天青'),
        'cinnabar': ColorToken('cinnabar', '#E60000', 'chinese', '朱砂'),
        'dailan': ColorToken('dailan', '#4A5C8C', 'chinese', '黛蓝'),
        'moonwhite': ColorToken('moonwhite', '#D6ECF0', 'chinese', '月白'),
        'ink': ColorToken('ink', '#2C2C2C', 'chinese', '墨色'),
    }
    
    # 间距系统（4px 基准）
    SPACING: Dict[str, SpacingToken] = {
        '1': SpacingToken('spacing-1', 4, '4px baseline'),
        '2': SpacingToken('spacing-2', 8, '4px baseline'),
        '3': SpacingToken('spacing-3', 16, '4px baseline'),
        '4': SpacingToken('spacing-4', 24, '4px baseline'),
        '5': SpacingToken('spacing-5', 32, '4px baseline'),
        '6': SpacingToken('spacing-6', 48, '4px baseline'),
        '8': SpacingToken('spacing-8', 64, '4px baseline'),
    }
    
    # 圆角系统
    RADIUS: Dict[str, RadiusToken] = {
        'sm': RadiusToken('radius-sm', 8, '小圆角'),
        'md': RadiusToken('radius-md', 12, '中圆角'),
        'lg': RadiusToken('radius-lg', 20, '大圆角'),
        'xl': RadiusToken('radius-xl', 32, '超大圆角'),
        'full': RadiusToken('radius-full', 9999, '圆形'),
    }
    
    # 阴影系统
    SHADOWS: Dict[str, ShadowToken] = {
        'sm': ShadowToken('shadow-sm', '0 1px 2px rgba(0,0,0,0.05)', '小阴影'),
        'md': ShadowToken('shadow-md', '0 4px 8px rgba(0,0,0,0.1)', '中阴影'),
        'lg': ShadowToken('shadow-lg', '0 8px 16px rgba(0,0,0,0.15)', '大阴影'),
        'xl': ShadowToken('shadow-xl', '0 12px 24px rgba(0,0,0,0.2)', '超大阴影'),
    }
    
    # 字体系统
    FONTS = {
        'primary': '-apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif',
        'mono': '"SF Mono", "JetBrains Mono", "Fira Code", monospace',
    }
    
    # 字号系统（1.5 倍率）
    FONT_SIZES = {
        'xs': 12,
        'sm': 16,
        'base': 24,
        'lg': 32,
        'xl': 48,
        '2xl': 72,
    }
    
    # 动画系统
    TRANSITIONS = {
        'fast': '200ms ease-out',
        'base': '300ms ease-out',
        'slow': '500ms ease-out',
    }
    
    @classmethod
    def get_color(cls, name: str) -> str:
        """获取颜色值"""
        token = cls.COLORS.get(name)
        return token.value if token else '#000000'
    
    @classmethod
    def get_spacing(cls, name: str) -> int:
        """获取间距值"""
        token = cls.SPACING.get(name)
        return token.value if token else 0
    
    @classmethod
    def get_radius(cls, name: str) -> int:
        """获取圆角值"""
        token = cls.RADIUS.get(name)
        return token.value if token else 0
    
    @classmethod
    def get_shadow(cls, name: str) -> str:
        """获取阴影值"""
        token = cls.SHADOWS.get(name)
        return token.value if token else 'none'
    
    @classmethod
    def get_font(cls, type: str = 'primary') -> str:
        """获取字体"""
        return cls.FONTS.get(type, cls.FONTS['primary'])
    
    @classmethod
    def get_font_size(cls, name: str) -> int:
        """获取字号"""
        return cls.FONT_SIZES.get(name, 16)
    
    @classmethod
    def get_transition(cls, name: str = 'base') -> str:
        """获取动画时长"""
        return cls.TRANSITIONS.get(name, cls.TRANSITIONS['base'])
    
    @classmethod
    def get_css_variables(cls) -> str:
        """生成 CSS 变量"""
        css = [":root {"]
        
        # 颜色变量
        for name, token in cls.COLORS.items():
            css.append(f"  --taiyi-{name}: {token.value};")
        
        # 间距变量
        for name, token in cls.SPACING.items():
            css.append(f"  --taiyi-spacing-{name}: {token.value}px;")
        
        # 圆角变量
        for name, token in cls.RADIUS.items():
            css.append(f"  --taiyi-radius-{name}: {token.value}px;")
        
        # 阴影变量
        for name, token in cls.SHADOWS.items():
            css.append(f"  --taiyi-shadow-{name}: {token.value};")
        
        # 字体变量
        css.append(f"  --taiyi-font-primary: {cls.FONTS['primary']};")
        css.append(f"  --taiyi-font-mono: {cls.FONTS['mono']};")
        
        # 字号变量
        for name, size in cls.FONT_SIZES.items():
            css.append(f"  --taiyi-text-{name}: {size}px;")
        
        # 动画变量
        for name, duration in cls.TRANSITIONS.items():
            css.append(f"  --taiyi-transition-{name}: {duration};")
        
        css.append("}")
        return "\n".join(css)
    
    @classmethod
    def get_design_principles(cls) -> Dict:
        """获取设计原则"""
        return {
            'apple': {
                'deference': '内容优先，UI 退后',
                'clarity': '清晰易懂，无歧义',
                'depth': '层次感，视觉深度'
            },
            'oriental': {
                'ma': '间 - 留白的艺术',
                'wabi_sabi': '侘寂 - 不完美之美',
                'shibui': '渋い - 低调的优雅'
            },
            'chinese': {
                'tianqing': '天青 - 雨过天青云破处',
                'liubai': '留白 - 计白当黑',
                'qiyun': '气韵 - 生动流畅'
            }
        }
    
    @classmethod
    def get_fusion_ratio(cls) -> Dict:
        """获取融合比例"""
        return {
            'apple': 80,
            'oriental': 15,
            'chinese': 5
        }
