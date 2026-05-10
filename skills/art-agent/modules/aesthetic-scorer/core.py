#!/usr/bin/env python3
"""
Aesthetic Scorer v1.0.0
太一系统美学评分引擎 - 多维度质量评估
"""

import json
import re
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from enum import Enum


class ContentType(Enum):
    """内容类型"""
    MARKDOWN = "markdown"
    CODE = "code"
    DATA = "data"
    REPORT = "report"
    CONFIG = "config"


class QualityLevel(Enum):
    """质量等级"""
    S = "S"  # 出版级
    A = "A"  # 专业级
    B = "B"  # 可用级
    C = "C"  # 草稿级


class AestheticScorer:
    """美学评分器主类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.score_history: List[Dict[str, Any]] = []
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "quality_threshold": "B",
            "auto_fix": True,
            "style_guide": "taiyi-standard",
            "output_format": "markdown"
        }
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("aesthetic-scorer")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def score(
        self,
        content: str,
        content_type: ContentType = None,
        **kwargs
    ) -> Dict[str, Any]:
        """评分内容
        
        Args:
            content: 原始内容
            content_type: 内容类型
            
        Returns:
            评分结果
        """
        start_time = datetime.now()
        
        # 自动检测内容类型
        if content_type is None:
            content_type = self._detect_content_type(content)
        
        self.logger.info(f"评分内容：类型={content_type.value}")
        
        # 执行多维度评分
        result = self._score_dimensions(content, content_type)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # 记录历史
        self.score_history.append({
            "timestamp": start_time.isoformat(),
            "type": content_type.value,
            "score": result["score"],
            "level": result["level"],
            "elapsed": elapsed
        })
        
        return result
    
    def _detect_content_type(self, content: str) -> ContentType:
        """自动检测内容类型"""
        # 检测 Markdown
        if re.search(r'^#{1,6}\s', content, re.MULTILINE):
            return ContentType.MARKDOWN
        
        # 检测代码
        if re.search(r'^(def |class |import |from |function |const |let |var )', content, re.MULTILINE):
            return ContentType.CODE
        
        # 检测数据
        if content.strip().startswith('{') or content.strip().startswith('['):
            try:
                json.loads(content)
                return ContentType.DATA
            except:
                pass
        
        # 默认为 Markdown
        return ContentType.MARKDOWN
    
    def _score_dimensions(self, content: str, content_type: ContentType) -> Dict[str, Any]:
        """多维度评分"""
        dimensions = {}
        
        # 可读性
        dimensions["readability"] = self._score_readability(content, content_type)
        
        # 一致性
        dimensions["consistency"] = self._score_consistency(content, content_type)
        
        # 美学
        dimensions["aesthetics"] = self._score_aesthetics(content, content_type)
        
        # 功能性
        dimensions["functionality"] = self._score_functionality(content, content_type)
        
        # 结构性
        dimensions["structure"] = self._score_structure(content, content_type)
        
        # 语义性
        dimensions["semantics"] = self._score_semantics(content, content_type)
        
        # 计算总分
        total_score = sum(dim["score"] * dim["weight"] for dim in dimensions.values())
        
        # 确定等级
        level = self._determine_level(total_score)
        
        return {
            "status": "success",
            "content_type": content_type.value,
            "score": round(total_score, 1),
            "level": level,
            "dimensions": dimensions
        }
    
    def _score_readability(self, content: str, content_type: ContentType) -> Dict[str, Any]:
        """可读性评分"""
        score = 85  # 基础分
        weight = 0.20
        
        # 句子长度
        sentences = re.split(r'[。！？.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            avg_len = sum(len(s) for s in sentences) / len(sentences)
            if avg_len > 50:
                score -= 10
            elif avg_len < 5:
                score -= 5
        
        return {
            "name": "可读性",
            "score": max(0, min(100, score)),
            "weight": weight
        }
    
    def _score_consistency(self, content: str, content_type: ContentType) -> Dict[str, Any]:
        """一致性评分"""
        score = 90
        weight = 0.20
        
        # 列表格式一致性
        list_items = re.findall(r'^[\-\*\+]\s', content, re.MULTILINE)
        if list_items:
            dash_count = sum(1 for l in content.split('\n') if l.startswith('- '))
            star_count = sum(1 for l in content.split('\n') if l.startswith('* '))
            
            if dash_count > 0 and star_count > 0:
                score -= 10
        
        return {
            "name": "一致性",
            "score": max(0, min(100, score)),
            "weight": weight
        }
    
    def _score_aesthetics(self, content: str, content_type: ContentType) -> Dict[str, Any]:
        """美学评分"""
        score = 85
        weight = 0.20
        
        # 签名检查
        if '太一美学' in content or '品质保证' in content:
            score += 10
        
        return {
            "name": "美学",
            "score": max(0, min(100, score)),
            "weight": weight
        }
    
    def _score_functionality(self, content: str, content_type: ContentType) -> Dict[str, Any]:
        """功能性评分"""
        score = 80
        weight = 0.20
        
        # 信息完整度
        words = len(content.split())
        if words < 50:
            score -= 15
        
        return {
            "name": "功能性",
            "score": max(0, min(100, score)),
            "weight": weight
        }
    
    def _score_structure(self, content: str, content_type: ContentType) -> Dict[str, Any]:
        """结构性评分"""
        score = 85
        weight = 0.10
        
        # 标题层级
        headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        if headings:
            score += 5
        
        return {
            "name": "结构性",
            "score": max(0, min(100, score)),
            "weight": weight
        }
    
    def _score_semantics(self, content: str, content_type: ContentType) -> Dict[str, Any]:
        """语义性评分"""
        score = 85
        weight = 0.10
        
        # 歧义检测
        ambiguous = ['可能', '也许', '大概']
        found = sum(1 for w in ambiguous if w in content)
        if found > 3:
            score -= 10
        
        return {
            "name": "语义性",
            "score": max(0, min(100, score)),
            "weight": weight
        }
    
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
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "status": "healthy",
            "module": "aesthetic-scorer",
            "version": "1.0.0",
            "total_scored": len(self.score_history),
            "config": self.config
        }
    
    @property
    def name(self) -> str:
        return "aesthetic-scorer"
    
    @property
    def version(self) -> str:
        return "1.0.0"


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="美学评分引擎")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    parser.add_argument("--input", "-i", help="输入文件路径")
    parser.add_argument("--type", "-t", choices=["markdown", "code", "data", "report", "config"], help="内容类型")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--health", action="store_true", help="健康检查")
    
    args = parser.parse_args()
    
    scorer = AestheticScorer(config_path=args.config)
    
    if args.health:
        print(json.dumps(scorer.health_check(), indent=2, ensure_ascii=False))
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content_type = ContentType(args.type) if args.type else None
        result = scorer.score(content, content_type=content_type)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"评分：{result['score']}/100 ({result['level']})")
            for dim_name, dim in result['dimensions'].items():
                print(f"  {dim['name']}: {dim['score']}/100")
    else:
        print(json.dumps(scorer.health_check(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
