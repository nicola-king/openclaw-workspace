#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiyi Style - 太一风格定义 v1.0

来源：Art Director + Aesthetic Evolution（蒸馏后）
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum


class StyleCategory(Enum):
    """风格分类"""
    DAOIST = "道家"
    BUDDHIST = "佛家"
    GENERAL = "通用"


@dataclass
class ColorPalette:
    """配色方案"""
    name: str
    background_top: Tuple[int, int, int]
    background_bottom: Tuple[int, int, int]
    accent: Tuple[int, int, int]
    ink: Tuple[int, int, int]
    seal: Tuple[int, int, int]


@dataclass
class TypographyStyle:
    """排版风格"""
    font_family: str
    title_size: int
    body_size: int
    meta_size: int
    line_height: float


class TaiyiStyle:
    """太一风格定义 v1.0"""
    
    # 配色方案
    PALETTES: Dict[StyleCategory, ColorPalette] = {
        StyleCategory.DAOIST: ColorPalette(
            name="道家·竹青",
            background_top=(252, 250, 245),    # 宣纸白
            background_bottom=(245, 248, 243), # 淡青灰
            accent=(120, 135, 120),            # 竹青
            ink=(45, 45, 50),                  # 墨色
            seal=(155, 55, 55)                 # 朱红
        ),
        StyleCategory.BUDDHIST: ColorPalette(
            name="佛家·檀褐",
            background_top=(252, 250, 245),    # 宣纸白
            background_bottom=(248, 243, 238), # 淡褐灰
            accent=(135, 120, 105),            # 檀褐
            ink=(40, 40, 45),                  # 深墨
            seal=(150, 45, 45)                 # 朱砂红
        ),
        StyleCategory.GENERAL: ColorPalette(
            name="通用·古铜",
            background_top=(253, 251, 247),    # 米白
            background_bottom=(248, 245, 240), # 淡茶
            accent=(139, 115, 85),             # 古铜
            ink=(44, 44, 44),                  # 墨色
            seal=(160, 50, 50)                 # 朱红
        )
    }
    
    # 排版风格
    TYPOGRAPHY = TypographyStyle(
        font_family="Noto Serif CJK",
        title_size=64,
        body_size=52,
        meta_size=32,
        line_height=1.5
    )
    
    # 装饰元素
    DECORATIONS = {
        StyleCategory.DAOIST: {
            'plant': 'bamboo',      # 竹
            'seal_char': '道',
            'corner_seals': ['智', '慧', '静']
        },
        StyleCategory.BUDDHIST: {
            'plant': 'plum',        # 梅
            'seal_char': '禅',
            'corner_seals': ['智', '慧', '空']
        },
        StyleCategory.GENERAL: {
            'plant': None,
            'seal_char': '太一',
            'corner_seals': ['智', '慧']
        }
    }
    
    # 画布规格
    CANVAS_SIZES = {
        'mobile_portrait': (1080, 1600),   # 手机竖屏
        'mobile_square': (1080, 1080),     # 朋友圈方图
        'desktop': (1920, 1080),           # 桌面
        'print_a4': (2480, 3508)           # A4 打印（300dpi）
    }
    
    @classmethod
    def get_palette(cls, category: StyleCategory = StyleCategory.GENERAL) -> ColorPalette:
        """获取配色方案"""
        return cls.PALETTES.get(category, cls.PALETTES[StyleCategory.GENERAL])
    
    @classmethod
    def get_decoration(cls, category: StyleCategory = StyleCategory.GENERAL) -> Dict:
        """获取装饰元素"""
        return cls.DECORATIONS.get(category, cls.DECORATIONS[StyleCategory.GENERAL])
    
    @classmethod
    def get_canvas(cls, size_name: str = 'mobile_portrait') -> Tuple[int, int]:
        """获取画布尺寸"""
        return cls.CANVAS_SIZES.get(size_name, cls.CANVAS_SIZES['mobile_portrait'])
    
    @classmethod
    def get_style_guide(cls) -> Dict:
        """获取完整风格指南"""
        return {
            'version': '1.0',
            'created': '2026-04-13',
            'palettes': {
                cat.value: {
                    'name': palette.name,
                    'background_top': palette.background_top,
                    'background_bottom': palette.background_bottom,
                    'accent': palette.accent,
                    'ink': palette.ink,
                    'seal': palette.seal
                }
                for cat, palette in cls.PALETTES.items()
            },
            'typography': {
                'font_family': cls.TYPOGRAPHY.font_family,
                'title_size': cls.TYPOGRAPHY.title_size,
                'body_size': cls.TYPOGRAPHY.body_size,
                'meta_size': cls.TYPOGRAPHY.meta_size,
                'line_height': cls.TYPOGRAPHY.line_height
            },
            'decorations': {
                cat.value: deco
                for cat, deco in cls.DECORATIONS.items()
            },
            'canvas_sizes': cls.CANVAS_SIZES
        }
    
    @classmethod
    def get_code_style(cls) -> Dict:
        """获取代码风格指南"""
        return {
            'version': '1.0',
            'principles': [
                '命名如诗 - 有意义，读如散文',
                '结构如建筑 - 函数短小，单一职责',
                '注释如俳句 - 解释「为什么」而非「是什么」',
                '留白如艺术 - 空行分组，视觉节奏'
            ],
            'example': '''
def distill_wisdom_from_chaos(data: Chaos) -> Wisdom:
    """从混沌中蒸馏智慧
    
    如秋风扫落叶
    如春雨润万物
    美在简洁中
    """
    # 去粗取精
    refined = remove_noise(data)
    
    # 去伪存真
    truth = extract_essence(refined)
    
    return truth  # 简洁如诗
'''
        }
    
    @classmethod
    def get_writing_style(cls) -> Dict:
        """获取文案风格指南"""
        return {
            'version': '1.0',
            'principles': [
                '短句如刀，精准有力',
                '长句如河，流畅自然',
                '留白如诗，呼吸自在',
                'emoji 如画，点睛不扰'
            ],
            'characteristics': [
                '极简黑客风（已内化）',
                '有画面感（进化中）',
                '有节奏韵律（进化中）',
                '有情感温度（进化中）'
            ]
        }
