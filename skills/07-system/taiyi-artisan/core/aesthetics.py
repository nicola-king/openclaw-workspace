#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aesthetics Engine - 美学引擎（艺术四原则）

来源：Art Director（蒸馏后）
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class AestheticPrinciple(Enum):
    """美学四原则"""
    EXISTENCE_IS_ART = "存在即艺术"
    FORM_FOLLOWS_FUNCTION = "形式追随功能"
    RESTRAINT_IS_ELEGANCE = "克制即优雅"
    CONSISTENCY_IS_HARMONY = "一致性和谐"


@dataclass
class ReviewResult:
    """美学审核结果"""
    passed: bool
    score: float  # 0-100
    issues: List[str]
    suggestions: List[str]
    principle_scores: dict  # 各原则得分


class AestheticsEngine:
    """美学引擎"""
    
    def __init__(self):
        self.principles = [
            AestheticPrinciple.EXISTENCE_IS_ART,
            AestheticPrinciple.FORM_FOLLOWS_FUNCTION,
            AestheticPrinciple.RESTRAINT_IS_ELEGANCE,
            AestheticPrinciple.CONSISTENCY_IS_HARMONY,
        ]
    
    def review(self, content: str, content_type: str = 'code') -> ReviewResult:
        """
        美学审核
        
        Args:
            content: 待审核内容
            content_type: 内容类型 (code/text/data/ui)
        
        Returns:
            ReviewResult: 审核结果
        """
        issues = []
        suggestions = []
        principle_scores = {}
        
        # 原则一：存在即艺术
        art_score = self._check_existence_is_art(content, content_type)
        principle_scores['existence_is_art'] = art_score
        if art_score < 60:
            issues.append("缺乏美感，需要提升艺术价值")
            suggestions.append("增加留白、优化排版、提升韵律感")
        
        # 原则二：形式追随功能
        function_score = self._check_form_follows_function(content, content_type)
        principle_scores['form_follows_function'] = function_score
        if function_score < 60:
            issues.append("形式与功能不匹配")
            suggestions.append("确保美学增强功能而非削弱")
        
        # 原则三：克制即优雅
        restraint_score = self._check_restraint_is_elegance(content, content_type)
        principle_scores['restraint_is_elegance'] = restraint_score
        if restraint_score < 60:
            issues.append("过度装饰或冗余")
            suggestions.append("删除不必要的元素，极简主义")
        
        # 原则四：一致性和谐
        harmony_score = self._check_consistency_is_harmony(content, content_type)
        principle_scores['consistency_is_harmony'] = harmony_score
        if harmony_score < 60:
            issues.append("风格不一致或混乱")
            suggestions.append("遵循 DESIGN.md，保持统一风格")
        
        # 计算总分
        total_score = (art_score + function_score + restraint_score + harmony_score) / 4
        passed = total_score >= 70 and all([
            art_score >= 60,
            function_score >= 60,
            restraint_score >= 60,
            harmony_score >= 60
        ])
        
        return ReviewResult(
            passed=passed,
            score=total_score,
            issues=issues,
            suggestions=suggestions,
            principle_scores=principle_scores
        )
    
    def _check_existence_is_art(self, content: str, content_type: str) -> float:
        """检查：存在即艺术"""
        # TODO: 实现具体检查逻辑
        # 当前返回默认分数
        return 75.0
    
    def _check_form_follows_function(self, content: str, content_type: str) -> float:
        """检查：形式追随功能"""
        # TODO: 实现具体检查逻辑
        return 75.0
    
    def _check_restraint_is_elegance(self, content: str, content_type: str) -> float:
        """检查：克制即优雅"""
        # TODO: 实现具体检查逻辑
        return 75.0
    
    def _check_consistency_is_harmony(self, content: str, content_type: str) -> float:
        """检查：一致性和谐"""
        # TODO: 实现具体检查逻辑
        return 75.0
    
    def suggest_improvements(self, review_result: ReviewResult) -> List[str]:
        """根据审核结果生成改进建议"""
        return review_result.suggestions
    
    def get_checklist(self) -> List[str]:
        """获取美学自检清单"""
        return [
            "□ 这个输出有美感吗？",
            "□ 是否遵循了 DESIGN.md？",
            "□ 有没有不必要的冗余？",
            "□ 色彩/排版是否一致？",
            "□ 是否有呼吸感（留白）？",
            "□ 代码/文案是否有韵律？",
            "□ 整体是否和谐？",
            "□ 功能是否被美学增强而非削弱？",
            "□ 是否有太一风格（可识别）？"
        ]
