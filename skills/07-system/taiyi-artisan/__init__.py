#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiyi Artisan - 太一艺境 v1.0

统一艺术引擎（美学 + 视觉 + 进化）

每一行代码都是诗，每一个输出都是画，每一次交互都是舞。
"""

from .core.aesthetics import AestheticsEngine, ReviewResult
from .core.evolution import EvolutionCore, Feedback
from .core.style import TaiyiStyle, StyleCategory
from .engines.wisdom import WisdomCardEngine
from .engines.charts import ChartsEngine
from .engines.cards import CardsEngine
from .design_systems.tokens import DesignTokens

__version__ = "1.0.0"
__author__ = "太一 AGI"
__created__ = "2026-04-13"

__all__ = [
    # 核心模块
    'AestheticsEngine',
    'ReviewResult',
    'EvolutionCore',
    'Feedback',
    'TaiyiStyle',
    'StyleCategory',
    
    # 视觉引擎
    'WisdomCardEngine',
]


class Artisan:
    """太一艺境主类"""
    
    def __init__(self, workspace: str = "~/.openclaw/workspace"):
        """
        初始化艺境
        
        Args:
            workspace: 工作目录
        """
        self.aesthetics = AestheticsEngine()
        self.evolution = EvolutionCore(workspace)
        self.style = TaiyiStyle()
        self.wisdom = WisdomCardEngine()
        self.charts = ChartsEngine()
        self.cards = CardsEngine()
        self.tokens = DesignTokens()
    
    def review(self, content: str, content_type: str = 'code'):
        """美学审核"""
        return self.aesthetics.review(content, content_type)
    
    def create_wisdom_card(self, category: str, quote: str, source: str):
        """生成智慧卡片"""
        return self.wisdom.create_card(category, quote, source)
    
    def generate_daily_wisdom(self, category: str = None):
        """生成每日智慧"""
        return self.wisdom.generate_daily(category)
    
    def create_chart(self, chart_type: str, **kwargs):
        """生成图表"""
        method = getattr(self.charts, f'create_{chart_type}', None)
        if method:
            return method(**kwargs)
        raise ValueError(f"不支持的图表类型：{chart_type}")
    
    def create_info_card(self, title: str, points: list, **kwargs):
        """生成信息卡片"""
        return self.cards.create_info_card(title, points, **kwargs)
    
    def review_design(self, content: str, content_type: str = 'ui'):
        """设计审核（新增）"""
        return self.aesthetics.review(content, content_type)
    
    def get_design_tokens(self) -> DesignTokens:
        """获取设计令牌"""
        return self.tokens
    
    def get_css_variables(self) -> str:
        """生成 CSS 变量"""
        return self.tokens.get_css_variables()
    
    def get_design_principles(self) -> dict:
        """获取设计原则"""
        return self.tokens.get_design_principles()
    
    def generate_ui(self, ui_type: str, style: str = 'taiyi-apple', **kwargs):
        """生成 UI（待实现）"""
        # TODO: 实现 UI 生成
        pass
    
    def collect_feedback(self, feedback: Feedback):
        """收集反馈"""
        self.evolution.collect_feedback(feedback)
    
    def evolve(self):
        """执行进化"""
        # 从日志读取反馈并进化
        # TODO: 实现完整逻辑
        pass
    
    def get_style_guide(self):
        """获取风格指南"""
        return self.style.get_style_guide()
    
    def get_checklist(self):
        """获取美学自检清单"""
        return self.aesthetics.get_checklist()


# 快捷函数
def create_artisan(workspace: str = "~/.openclaw/workspace") -> Artisan:
    """创建艺境实例"""
    return Artisan(workspace)


def review_output(content: str, content_type: str = 'code'):
    """快速美学审核"""
    artisan = Artisan()
    return artisan.review(content, content_type)


def generate_wisdom(category: str = None):
    """快速生成每日智慧"""
    artisan = Artisan()
    return artisan.generate_daily_wisdom(category)
