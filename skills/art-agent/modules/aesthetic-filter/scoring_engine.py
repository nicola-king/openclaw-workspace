#!/usr/bin/env python3
"""
多维度美学评分引擎 v2.0
太一系统美学过滤器核心 - 6 维度精细评分
"""

import re
import json
import logging
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


class ContentType(Enum):
    MARKDOWN = "markdown"
    CODE = "code"
    DATA = "data"
    REPORT = "report"
    CONFIG = "config"


@dataclass
class DimensionScore:
    """单维度评分"""
    name: str
    score: float  # 0-100
    weight: float  # 权重 0-1
    details: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "score": round(self.score, 1),
            "weight": self.weight,
            "weighted_score": round(self.score * self.weight, 1),
            "details": self.details,
            "issues": self.issues,
            "suggestions": self.suggestions
        }


@dataclass
class QualityReport:
    """质量报告"""
    content_type: str
    total_score: float  # 0-100
    level: str  # S/A/B/C
    dimensions: Dict[str, DimensionScore]
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_type": self.content_type,
            "total_score": round(self.total_score, 1),
            "level": self.level,
            "dimensions": {k: v.to_dict() for k, v in self.dimensions.items()},
            "issues": self.issues,
            "suggestions": self.suggestions,
            "summary": self._generate_summary()
        }
    
    def _generate_summary(self) -> str:
        """生成总结"""
        strengths = []
        weaknesses = []
        
        for dim_name, dim in self.dimensions.items():
            if dim.score >= 80:
                strengths.append(f"{dim_name} ({dim.score:.0f}分)")
            elif dim.score < 60:
                weaknesses.append(f"{dim_name} ({dim.score:.0f}分)")
        
        parts = []
        if strengths:
            parts.append(f"✅ 优势: {', '.join(strengths)}")
        if weaknesses:
            parts.append(f"⚠️ 待改进: {', '.join(weaknesses)}")
        
        return " | ".join(parts) if parts else "📊 综合评分"


# ═══════════════════════════════════════════════════

# 评分维度实现

# ═══════════════════════════════════════════════════


class ReadabilityScorer:
    """可读性评分 (权重: 0.20)"""
    
    NAME = "可读性"
    WEIGHT = 0.20
    
    def score(self, content: str, content_type: ContentType) -> DimensionScore:
        issues = []
        suggestions = []
        details = {}
        
        if content_type == ContentType.CODE:
            return self._score_code(content, issues, suggestions, details)
        
        return self._score_text(content, issues, suggestions, details)
    
    def _score_text(self, content: str, issues, suggestions, details) -> DimensionScore:
        """文本可读性评分"""
        score = 100
        
        # 1. 句子长度 (30分)
        sentences = re.split(r'[。！？.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            avg_len = sum(len(s) for s in sentences) / len(sentences)
            details["avg_sentence_length"] = round(avg_len, 1)
            details["sentence_count"] = len(sentences)
            
            if avg_len > 50:
                score -= 15
                issues.append(f"句子过长 (平均{avg_len:.0f}字)")
                suggestions.append("拆分长句，保持 20-40 字")
            elif avg_len > 35:
                score -= 8
                suggestions.append("部分句子偏长，可适当拆分")
            elif avg_len < 5:
                score -= 5
                suggestions.append("句子过短，可适当合并")
        
        # 2. 段落结构 (25分)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        details["paragraph_count"] = len(paragraphs)
        
        if paragraphs:
            long_paragraphs = sum(1 for p in paragraphs if len(p) > 300)
            details["long_paragraphs"] = long_paragraphs
            
            if long_paragraphs > len(paragraphs) * 0.3:
                score -= 12
                issues.append(f"长段落过多 ({long_paragraphs}/{len(paragraphs)})")
                suggestions.append("拆分长段落，每段 100-200 字")
        
        # 3. 词汇多样性 (25分)
        words = re.findall(r'[\u4e00-\u9fff\w]+', content)
        if words:
            unique_words = set(words)
            diversity = len(unique_words) / len(words)
            details["vocabulary_diversity"] = round(diversity, 2)
            details["total_words"] = len(words)
            
            if diversity < 0.3:
                score -= 10
                issues.append("词汇重复率高")
                suggestions.append("使用更多样化的词汇")
        
        # 4. 空白比例 (20分)
        blank_lines = content.count('\n\n')
        total_lines = content.count('\n') + 1
        blank_ratio = blank_lines / max(total_lines, 1)
        details["blank_ratio"] = round(blank_ratio, 2)
        
        if blank_ratio < 0.1:
            score -= 8
            issues.append("留白不足")
            suggestions.append("增加段落间空行")
        elif blank_ratio > 0.4:
            score -= 5
            suggestions.append("留白过多，可适当紧凑")
        
        return DimensionScore(
            name=self.NAME,
            score=max(0, min(100, score)),
            weight=self.WEIGHT,
            details=details,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_code(self, content: str, issues, suggestions, details) -> DimensionScore:
        """代码可读性评分"""
        score = 100
        
        lines = content.split('\n')
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        comment_lines = [l for l in lines if l.strip().startswith('#')]
        
        details["total_lines"] = len(lines)
        details["code_lines"] = len(code_lines)
        details["comment_lines"] = len(comment_lines)
        
        # 1. 注释率 (30分)
        if code_lines:
            comment_ratio = len(comment_lines) / len(code_lines)
            details["comment_ratio"] = round(comment_ratio, 2)
            
            if comment_ratio < 0.1:
                score -= 15
                issues.append("注释不足")
                suggestions.append("添加函数/类文档字符串和行注释")
            elif comment_ratio > 0.5:
                score -= 5
                suggestions.append("注释过多，可能影响代码可读性")
        
        # 2. 函数长度 (30分)
        functions = re.findall(r'def\s+(\w+)\s*\(', content)
        if functions:
            details["function_count"] = len(functions)
            
            # 简单估算函数长度
            in_func = False
            func_lines = 0
            max_func_lines = 0
            
            for line in lines:
                if line.strip().startswith('def '):
                    if in_func and func_lines > 30:
                        score -= 10
                        issues.append(f"函数过长 (>{func_lines}行)")
                    in_func = True
                    func_lines = 0
                elif in_func:
                    func_lines += 1
                    max_func_lines = max(max_func_lines, func_lines)
            
            details["max_function_lines"] = max_func_lines
        
        # 3. 命名规范 (20分)
        bad_names = re.findall(r'\b([a-z]{1,2})\s*=', content)
        if bad_names:
            score -= 10
            issues.append(f"变量名过短 ({', '.join(bad_names[:3])})")
            suggestions.append("使用有意义的变量名")
        
        # 4. 空行分组 (20分)
        blank_groups = re.findall(r'\n\n+', content)
        if len(blank_groups) < len(functions) * 0.5:
            score -= 8
            suggestions.append("函数间增加空行分组")
        
        return DimensionScore(
            name=self.NAME,
            score=max(0, min(100, score)),
            weight=self.WEIGHT,
            details=details,
            issues=issues,
            suggestions=suggestions
        )


class ConsistencyScorer:
    """一致性评分 (权重: 0.20)"""
    
    NAME = "一致性"
    WEIGHT = 0.20
    
    def score(self, content: str, content_type: ContentType) -> DimensionScore:
        issues = []
        suggestions = []
        details = {}
        
        score = 100
        
        if content_type == ContentType.MARKDOWN or content_type == ContentType.REPORT:
            score = self._score_markdown(content, issues, suggestions, details)
        elif content_type == ContentType.CODE:
            score = self._score_code(content, issues, suggestions, details)
        
        return DimensionScore(
            name=self.NAME,
            score=max(0, min(100, score)),
            weight=self.WEIGHT,
            details=details,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_markdown(self, content: str, issues, suggestions, details) -> int:
        """Markdown 一致性评分"""
        score = 100
        
        lines = content.split('\n')
        
        # 1. 标题层级一致性 (30分)
        headings = [(i, line) for i, line in enumerate(lines) if re.match(r'^#{1,6}\s', line)]
        if headings:
            levels = [len(re.match(r'^(#+)', h[1]).group(1)) for h in headings]
            details["heading_levels"] = levels
            
            # 检查层级跳跃
            for i in range(1, len(levels)):
                if levels[i] > levels[i-1] + 1:
                    score -= 10
                    issues.append(f"标题层级跳跃 (H{levels[i-1]} → H{levels[i]})")
                    suggestions.append("保持标题层级连续")
                    break
        
        # 2. 列表格式一致性 (25分)
        list_items = [l for l in lines if re.match(r'^[\-\*\+]\s', l)]
        if list_items:
            dash_count = sum(1 for l in list_items if l.startswith('- '))
            star_count = sum(1 for l in list_items if l.startswith('* '))
            plus_count = sum(1 for l in list_items if l.startswith('+ '))
            
            details["list_format"] = {"-": dash_count, "*": star_count, "+": plus_count}
            
            formats_used = sum(1 for c in [dash_count, star_count, plus_count] if c > 0)
            if formats_used > 1:
                score -= 12
                issues.append(f"列表符号不统一 (使用了{formats_used}种)")
                suggestions.append("统一使用 - 作为列表符号")
        
        # 3. 代码块语言标注 (25分)
        code_blocks = re.findall(r'```(\w*)', content)
        if code_blocks:
            unmarked = sum(1 for lang in code_blocks if not lang)
            details["code_blocks"] = len(code_blocks)
            details["unmarked_blocks"] = unmarked
            
            if unmarked > 0:
                score -= 10
                issues.append(f"{unmarked} 个代码块缺少语言标注")
                suggestions.append("为代码块添加语言标识 (如 ```python)")
        
        # 4. 表格对齐 (20分)
        tables = re.findall(r'\|.*\|\n\|[-:\s|]+\|\n(\|.*\|\n?)*', content)
        if tables:
            details["table_count"] = len(tables)
            # 简化检查，实际应解析表格内容
        
        return score
    
    def _score_code(self, content: str, issues, suggestions, details) -> int:
        """代码一致性评分"""
        score = 100
        
        lines = content.split('\n')
        
        # 1. 缩进一致性 (30分)
        indented = [l for l in lines if l and l[0] in ' \t']
        if indented:
            spaces = [len(l) - len(l.lstrip()) for l in indented if l.strip()]
            if spaces:
                from collections import Counter
                indent_counts = Counter(spaces)
                most_common = indent_counts.most_common(1)[0]
                details["indent_pattern"] = f"{most_common[0]} spaces"
                
                unique_indents = len(indent_counts)
                if unique_indents > 3:
                    score -= 15
                    issues.append("缩进不一致")
                    suggestions.append("统一使用 4 空格缩进")
        
        # 2. 引号一致性 (25分)
        single_quotes = len(re.findall(r"'[^']*'", content))
        double_quotes = len(re.findall(r'"[^"]*"', content))
        
        if single_quotes > 0 and double_quotes > 0:
            score -= 10
            issues.append("引号混用 (单引号和双引号)")
            suggestions.append("统一使用双引号")
        
        details["quotes"] = {"single": single_quotes, "double": double_quotes}
        
        # 3. 空行一致性 (25分)
        # 检查函数间空行
        func_positions = [i for i, l in enumerate(lines) if l.strip().startswith('def ')]
        if len(func_positions) > 1:
            gaps = [func_positions[i+1] - func_positions[i] for i in range(len(func_positions)-1)]
            if len(set(gaps)) > 2:
                score -= 10
                issues.append("函数间空行数不一致")
                suggestions.append("函数间保持 2 个空行")
        
        # 4. 行长度一致性 (20分)
        long_lines = sum(1 for l in lines if len(l) > 120)
        if long_lines > len(lines) * 0.1:
            score -= 8
            issues.append(f"长行过多 ({long_lines} 行 > 120 字符)")
            suggestions.append("保持行长度 < 120 字符")
        
        return score


class AestheticsScorer:
    """美学评分 (权重: 0.20)"""
    
    NAME = "美学"
    WEIGHT = 0.20
    
    def score(self, content: str, content_type: ContentType) -> DimensionScore:
        issues = []
        suggestions = []
        details = {}
        score = 100
        
        if content_type in (ContentType.MARKDOWN, ContentType.REPORT):
            score = self._score_markdown(content, issues, suggestions, details)
        elif content_type == ContentType.CODE:
            score = self._score_code(content, issues, suggestions, details)
        
        return DimensionScore(
            name=self.NAME,
            score=max(0, min(100, score)),
            weight=self.WEIGHT,
            details=details,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_markdown(self, content: str, issues, suggestions, details) -> int:
        """Markdown 美学评分"""
        score = 100
        
        # 1. 视觉层次 (30分)
        headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        if headings:
            details["heading_count"] = len(headings)
            
            # 检查标题长度
            long_titles = sum(1 for h in headings if len(h) > 30)
            if long_titles > len(headings) * 0.3:
                score -= 10
                issues.append("标题过长")
                suggestions.append("标题保持简洁 (< 30 字)")
        
        # 2. 装饰适度 (25分)
        emojis = re.findall(r'[\U0001F300-\U0001F9FF]', content)
        details["emoji_count"] = len(emojis)
        
        if len(emojis) > 20:
            score -= 10
            issues.append("emoji 过多")
            suggestions.append("适度使用 emoji，避免干扰")
        
        # 3. 引用块使用 (25分)
        quotes = re.findall(r'^>\s+', content, re.MULTILINE)
        details["quote_count"] = len(quotes)
        
        # 4. 太一美学签名 (20分)
        if '太一美学' in content or '品质保证' in content:
            details["has_signature"] = True
        else:
            details["has_signature"] = False
            score -= 5
            suggestions.append("添加太一美学签名")
        
        return score
    
    def _score_code(self, content: str, issues, suggestions, details) -> int:
        """代码美学评分"""
        score = 100
        
        lines = content.split('\n')
        
        # 1. 代码韵律 (30分)
        # 检查空行分组
        blank_groups = re.findall(r'\n\n+', content)
        details["blank_groups"] = len(blank_groups)
        
        # 2. 注释质量 (30分)
        docstrings = re.findall(r'"""[^"]*"""', content)
        details["docstring_count"] = len(docstrings)
        
        if not docstrings:
            score -= 15
            issues.append("缺少文档字符串")
            suggestions.append("为函数/类添加 docstring")
        
        # 3. 命名美感 (20分)
        function_names = re.findall(r'def\s+(\w+)\s*\(', content)
        if function_names:
            poetic_names = sum(1 for n in function_names if len(n) > 5 and '_' in n)
            details["poetic_naming_ratio"] = round(poetic_names / len(function_names), 2)
        
        # 4. 结构美感 (20分)
        # 检查类/函数组织
        classes = re.findall(r'class\s+(\w+)', content)
        details["class_count"] = len(classes)
        
        return score


class FunctionalityScorer:
    """功能性评分 (权重: 0.20)"""
    
    NAME = "功能性"
    WEIGHT = 0.20
    
    def score(self, content: str, content_type: ContentType) -> DimensionScore:
        issues = []
        suggestions = []
        details = {}
        score = 100
        
        if content_type in (ContentType.MARKDOWN, ContentType.REPORT):
            score = self._score_text(content, issues, suggestions, details)
        elif content_type == ContentType.CODE:
            score = self._score_code(content, issues, suggestions, details)
        
        return DimensionScore(
            name=self.NAME,
            score=max(0, min(100, score)),
            weight=self.WEIGHT,
            details=details,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_text(self, content: str, issues, suggestions, details) -> int:
        """文本功能性评分"""
        score = 100
        
        # 1. 信息完整度 (30分)
        words = len(content.split())
        details["word_count"] = words
        
        if words < 50:
            score -= 15
            issues.append("内容过短，信息可能不完整")
            suggestions.append("补充更多细节和说明")
        
        # 2. 逻辑清晰 (30分)
        # 检查连接词
        connectors = ['因此', '所以', '但是', '然而', '另外', '首先', '其次', '最后']
        found_connectors = [c for c in connectors if c in content]
        details["connectors"] = found_connectors
        
        if len(found_connectors) < 2 and words > 100:
            score -= 10
            suggestions.append("使用连接词增强逻辑连贯性")
        
        # 3. 可执行性 (20分)
        # 检查是否有明确结论/行动项
        action_words = ['建议', '需要', '应该', '必须', '可以', '推荐']
        has_action = any(w in content for w in action_words)
        details["has_action_items"] = has_action
        
        # 4. 数据支撑 (20分)
        numbers = re.findall(r'\d+', content)
        details["number_count"] = len(numbers)
        
        if len(numbers) < 3 and words > 200:
            score -= 8
            suggestions.append("添加数据支撑论点")
        
        return score
    
    def _score_code(self, content: str, issues, suggestions, details) -> int:
        """代码功能性评分"""
        score = 100
        
        # 1. 错误处理 (30分)
        has_try = 'try:' in content
        has_except = 'except' in content
        
        if has_try and not has_except:
            score -= 15
            issues.append("有 try 无 except")
            suggestions.append("添加异常处理")
        
        details["has_error_handling"] = has_try and has_except
        
        # 2. 类型注解 (25分)
        type_hints = re.findall(r':\s*(str|int|float|bool|list|dict|Any|Optional)', content)
        details["type_hint_count"] = len(type_hints)
        
        if not type_hints:
            score -= 10
            suggestions.append("添加类型注解")
        
        # 3. 返回值 (25分)
        returns = re.findall(r'\breturn\b', content)
        details["return_count"] = len(returns)
        
        # 4. 依赖管理 (20分)
        imports = re.findall(r'^(?:import|from)\s+', content, re.MULTILINE)
        details["import_count"] = len(imports)
        
        if len(imports) > 20:
            score -= 8
            issues.append("依赖过多")
            suggestions.append("减少不必要的依赖")
        
        return score


class StructureScorer:
    """结构性评分 (权重: 0.10)"""
    
    NAME = "结构性"
    WEIGHT = 0.10
    
    def score(self, content: str, content_type: ContentType) -> DimensionScore:
        issues = []
        suggestions = []
        details = {}
        score = 100
        
        if content_type in (ContentType.MARKDOWN, ContentType.REPORT):
            score = self._score_markdown(content, issues, suggestions, details)
        elif content_type == ContentType.CODE:
            score = self._score_code(content, issues, suggestions, details)
        elif content_type == ContentType.DATA:
            score = self._score_data(content, issues, suggestions, details)
        
        return DimensionScore(
            name=self.NAME,
            score=max(0, min(100, score)),
            weight=self.WEIGHT,
            details=details,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_markdown(self, content: str, issues, suggestions, details) -> int:
        """Markdown 结构性评分"""
        score = 100
        
        lines = content.split('\n')
        
        # 1. 标题层级 (30分)
        headings = [(i, line) for i, line in enumerate(lines) if re.match(r'^#{1,6}\s', line)]
        if headings:
            details["heading_count"] = len(headings)
            
            # 检查是否有 H1
            h1_count = sum(1 for _, h in headings if h.startswith('# '))
            if h1_count == 0:
                score -= 10
                issues.append("缺少 H1 标题")
                suggestions.append("添加 H1 作为文档标题")
            elif h1_count > 1:
                score -= 8
                issues.append("多个 H1 标题")
                suggestions.append("只保留一个 H1")
        
        # 2. 段落组织 (30分)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        details["paragraph_count"] = len(paragraphs)
        
        # 3. 导航元素 (20分)
        has_toc = '[TOC]' in content or '目录' in content
        has_links = 'http' in content or '[' in content
        details["has_toc"] = has_toc
        details["has_links"] = has_links
        
        # 4. 章节平衡 (20分)
        if headings:
            # 检查各章节长度是否均衡
            section_lengths = []
            for i in range(len(headings)):
                start = headings[i][0]
                end = headings[i+1][0] if i+1 < len(headings) else len(lines)
                section_lengths.append(end - start)
            
            if section_lengths:
                avg_len = sum(section_lengths) / len(section_lengths)
                details["avg_section_length"] = round(avg_len, 1)
        
        return score
    
    def _score_code(self, content: str, issues, suggestions, details) -> int:
        """代码结构性评分"""
        score = 100
        
        # 1. 模块组织 (30分)
        imports = re.findall(r'^(?:import|from)\s+', content, re.MULTILINE)
        details["import_count"] = len(imports)
        
        # 2. 类/函数组织 (30分)
        classes = re.findall(r'^class\s+', content, re.MULTILINE)
        functions = re.findall(r'^def\s+', content, re.MULTILINE)
        details["class_count"] = len(classes)
        details["function_count"] = len(functions)
        
        # 3. 依赖顺序 (20分)
        # 标准库 → 第三方 → 本地
        
        # 4. 导出接口 (20分)
        has_all = '__all__' in content
        details["has_all"] = has_all
        
        return score
    
    def _score_data(self, content: str, issues, suggestions, details) -> int:
        """数据结构评分"""
        score = 100
        
        try:
            data = json.loads(content)
            details["valid_json"] = True
            
            if isinstance(data, dict):
                details["key_count"] = len(data)
                depth = self._json_depth(data)
                details["max_depth"] = depth
                
                if depth > 5:
                    score -= 10
                    issues.append("JSON 嵌套过深")
                    suggestions.append("扁平化数据结构")
            elif isinstance(data, list):
                details["item_count"] = len(data)
        except json.JSONDecodeError:
            details["valid_json"] = False
            score -= 30
            issues.append("JSON 格式错误")
        
        return score
    
    def _json_depth(self, obj, current=1) -> int:
        if isinstance(obj, dict):
            return max((self._json_depth(v, current+1) for v in obj.values()), default=current)
        elif isinstance(obj, list):
            return max((self._json_depth(v, current+1) for v in obj), default=current)
        return current


class SemanticsScorer:
    """语义性评分 (权重: 0.10)"""
    
    NAME = "语义性"
    WEIGHT = 0.10
    
    def score(self, content: str, content_type: ContentType) -> DimensionScore:
        issues = []
        suggestions = []
        details = {}
        score = 100
        
        # 1. 歧义检测 (30分)
        ambiguous = ['可能', '也许', '大概', '差不多', '基本上', '某种程度上']
        found_ambiguous = [w for w in ambiguous if w in content]
        details["ambiguous_words"] = found_ambiguous
        
        if len(found_ambiguous) > 3:
            score -= 10
            issues.append("模糊词汇过多")
            suggestions.append("使用明确表述，减少歧义")
        
        # 2. 术语一致性 (30分)
        # 检查专业术语是否统一
        terms = re.findall(r'[\u4e00-\u9fff]{2,4}(?:系统|平台|工具|框架|模块|组件)', content)
        if terms:
            from collections import Counter
            term_counts = Counter(terms)
            details["term_usage"] = dict(term_counts.most_common(5))
        
        # 3. 表达精准 (20分)
        # 检查冗余表达
        redundancies = ['进行...操作', '做出...决定', '给予...支持']
        for red in redundancies:
            if red.replace('...', '') in content:
                score -= 5
                suggestions.append(f"精简表达: {red}")
        
        # 4. 情感色彩 (20分)
        positive = ['优秀', '良好', '成功', '高效', '优雅', '完美']
        negative = ['问题', '缺陷', '失败', '低效', '丑陋', '错误']
        
        pos_count = sum(1 for w in positive if w in content)
        neg_count = sum(1 for w in negative if w in content)
        
        details["sentiment"] = {
            "positive": pos_count,
            "negative": neg_count,
            "ratio": round(pos_count / max(neg_count, 1), 2)
        }
        
        return DimensionScore(
            name=self.NAME,
            score=max(0, min(100, score)),
            weight=self.WEIGHT,
            details=details,
            issues=issues,
            suggestions=suggestions
        )


# ═══════════════════════════════════════════════════

# 评分引擎主类

# ═══════════════════════════════════════════════════


class ScoringEngine:
    """多维度评分引擎"""
    
    def __init__(self):
        self.dimensions = {
            "readability": ReadabilityScorer(),
            "consistency": ConsistencyScorer(),
            "aesthetics": AestheticsScorer(),
            "functionality": FunctionalityScorer(),
            "structure": StructureScorer(),
            "semantics": SemanticsScorer(),
        }
        
        self.logger = logging.getLogger("scoring-engine")
    
    def evaluate(self, content: str, content_type: ContentType = ContentType.MARKDOWN) -> QualityReport:
        """执行多维度评分"""
        self.logger.info(f"开始评分: 类型={content_type.value}")
        
        dimensions = {}
        all_issues = []
        all_suggestions = []
        total_score = 0
        
        for key, scorer in self.dimensions.items():
            dim_score = scorer.score(content, content_type)
            dimensions[key] = dim_score
            total_score += dim_score.score * dim_score.weight
            all_issues.extend(dim_score.issues)
            all_suggestions.extend(dim_score.suggestions)
        
        # 内容长度惩罚：极短内容不得高于 B 级
        word_count = len(content.split())
        if word_count < 10:
            total_score = min(total_score, 59.9)
        elif word_count < 30:
            total_score = min(total_score, 74.9)
        
        # 确定等级
        level = self._determine_level(total_score)
        
        report = QualityReport(
            content_type=content_type.value,
            total_score=total_score,
            level=level,
            dimensions=dimensions,
            issues=all_issues,
            suggestions=all_suggestions
        )
        
        self.logger.info(f"评分完成: {level} ({total_score:.1f}分)")
        
        return report
    
    def _determine_level(self, score: float) -> str:
        """根据总分确定等级"""
        if score >= 90:
            return "S"
        elif score >= 75:
            return "A"
        elif score >= 60:
            return "B"
        else:
            return "C"
    
    def get_dimension_weights(self) -> Dict[str, float]:
        """获取各维度权重"""
        return {
            "可读性": ReadabilityScorer.WEIGHT,
            "一致性": ConsistencyScorer.WEIGHT,
            "美学": AestheticsScorer.WEIGHT,
            "功能性": FunctionalityScorer.WEIGHT,
            "结构性": StructureScorer.WEIGHT,
            "语义性": SemanticsScorer.WEIGHT,
        }


# ═══════════════════════════════════════════════════

# CLI 入口

# ═══════════════════════════════════════════════════


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="多维度美学评分引擎")
    parser.add_argument("--input", "-i", required=True, help="输入文件")
    parser.add_argument("--type", "-t", choices=["markdown", "code", "data", "report", "config"], default="markdown")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()
    
    engine = ScoringEngine()
    content_type = ContentType(args.type)
    report = engine.evaluate(content, content_type)
    
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"{'='*60}")
        print(f"📊 美学评分报告")
        print(f"{'='*60}")
        print(f"内容类型: {report.content_type}")
        print(f"总评分: {report.total_score:.1f}/100 ({report.level}级)")
        print(f"")
        
        print(f"维度评分:")
        for key, dim in report.dimensions.items():
            bar = "█" * int(dim.score / 5) + "░" * (20 - int(dim.score / 5))
            print(f"  {dim.name:8s} {bar} {dim.score:.0f}/100 (权重{dim.weight:.0%})")
        
        print(f"")
        print(f"总结: {report._generate_summary()}")
        
        if report.issues:
            print(f"")
            print(f"问题:")
            for issue in report.issues:
                print(f"  ⚠️ {issue}")
        
        if report.suggestions:
            print(f"")
            print(f"建议:")
            for sug in report.suggestions:
                print(f"  💡 {sug}")


if __name__ == "__main__":
    main()
