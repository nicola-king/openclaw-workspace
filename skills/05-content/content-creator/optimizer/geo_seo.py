#!/usr/bin/env python3
"""
GEO SEO Optimizer - 针对 AI 搜索引擎优化内容
"""

import re
from typing import List, Dict


class GEOOptimizer:
    """GEO 优化器"""
    
    def __init__(self):
        self.title_templates = {
            'xiaohongshu': [
                "这 X 个...让我...",
                "...必备！...",
                "...｜...",
                "我用...实现了...",
                "...的 N 个真相",
            ],
            'zhihu': [
                "如何评价...？",
                "...是一种怎样的体验？",
                "有哪些...？",
                "...全攻略",
                "为什么...？",
            ],
            'wechat': [
                "【深度】...",
                "...全攻略",
                "为什么我建议你...",
                "...的真相",
                "从 0 到 1：...",
            ],
        }
    
    def geo_optimize(
        self,
        content: str,
        target_ai: List[str] = None,
        keywords: List[str] = None
    ) -> str:
        """
        GEO 优化内容
        
        Args:
            content: 原始内容
            target_ai: 目标 AI 引擎 ['perplexity', 'chatgpt', 'gemini']
            keywords: 核心关键词
        
        Returns:
            优化后的内容
        """
        optimized = content
        
        # 添加 TL;DR 摘要
        if not "TL;DR" in optimized and not "执行摘要" in optimized:
            summary = self._generate_summary(content, keywords)
            optimized = f"## TL;DR\n{summary}\n\n" + optimized
        
        # 优化结构
        optimized = self._optimize_structure(optimized)
        
        # 添加引用优化
        if keywords:
            optimized = self._add_citations(optimized, keywords)
        
        return optimized
    
    def _generate_summary(self, content: str, keywords: List[str] = None) -> str:
        """生成执行摘要"""
        # 简单实现：提取第一段
        paragraphs = content.split('\n\n')
        if paragraphs:
            return paragraphs[0][:200] + "..." if len(paragraphs[0]) > 200 else paragraphs[0]
        return "本文详细介绍了相关内容。"
    
    def _optimize_structure(self, content: str) -> str:
        """优化结构"""
        # 确保有清晰的标题层级
        lines = content.split('\n')
        optimized_lines = []
        
        for line in lines:
            # 确保标题格式正确
            if line.startswith('#') and not line.startswith('##'):
                optimized_lines.append(line)
            elif line.startswith('-') and not line.startswith('- '):
                optimized_lines.append('- ' + line[1:].strip())
            else:
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _add_citations(self, content: str, keywords: List[str]) -> str:
        """添加引用优化"""
        # 简单实现：在关键词后添加引用标记
        for keyword in keywords[:3]:
            if keyword in content and "根据" not in content:
                content = content.replace(keyword, f"{keyword}（行业共识）", 1)
        return content
    
    def generate_viral_titles(
        self,
        topic: str,
        platform: str = 'xiaohongshu',
        count: int = 10
    ) -> List[str]:
        """
        生成爆款标题
        
        Args:
            topic: 主题
            platform: 平台
            count: 生成数量
        
        Returns:
            标题列表
        """
        templates = self.title_templates.get(platform, self.title_templates['xiaohongshu'])
        titles = []
        
        for template in templates:
            title = template.replace("...", topic)
            titles.append(title)
        
        # 添加 emoji（小红书）
        if platform == 'xiaohongshu':
            emojis = ['✨', '🔥', '💡', '📈', '🎯']
            titles = [f"{emojis[i % len(emojis)]} {t}" for i, t in enumerate(titles)]
        
        return titles[:count]
    
    def check_conceptual_density(
        self,
        content: str,
        core_concept: str
    ) -> float:
        """
        检查概念密度
        
        Args:
            content: 内容
            core_concept: 核心概念
        
        Returns:
            密度分数 (0-100)
        """
        # 简单实现：计算核心概念及相关词的出现频率
        related_terms = [core_concept]
        # 可以扩展同义词库
        
        count = sum(content.count(term) for term in related_terms)
        word_count = len(content.split())
        
        if word_count == 0:
            return 0.0
        
        density = (count / word_count) * 100
        return min(100.0, density * 10)  # 归一化到 0-100
