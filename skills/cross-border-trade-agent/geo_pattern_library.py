#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO 结晶模式库 - 自进化系统集成
太一 AGI · 2026-04-19 18:55

功能:
- 存储 GEO 成功案例模式
- 模式匹配与推荐
- 模式效果追踪
- 模式持续优化
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('GEOPatternLibrary')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
PATTERN_DIR = WORKSPACE / "data" / "cross-border" / "geo" / "patterns"
PATTERN_DIR.mkdir(parents=True, exist_ok=True)


class GEOPatternLibrary:
    """GEO 结晶模式库"""
    
    def __init__(self):
        self.pattern_file = PATTERN_DIR / "geo_patterns.json"
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> List[Dict]:
        """加载结晶模式"""
        if self.pattern_file.exists():
            with open(self.pattern_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def create_pattern(self, success_data: Dict) -> str:
        """
        从 GEO 成功案例创建结晶模式
        
        Args:
            success_data: 成功案例数据
            
        Returns:
            pattern_id: 结晶模式 ID
        """
        logger.info(f"🧬 创建 GEO 结晶模式：{success_data.get('product', 'Unknown')}")
        
        # 生成模式 ID
        pattern_id = f"GEO_Success_{len(self.patterns) + 1:03d}"
        
        # 提取成功要素
        success_factors = self._extract_success_factors(success_data)
        
        # 创建结晶模式
        pattern = {
            "pattern_id": pattern_id,
            "pattern_name": f"GEO 高转化内容模式 - {success_data.get('product', 'Unknown')}",
            "product": success_data.get('product'),
            "success_factors": success_factors,
            "performance": {
                "ai_citation_rate": success_data.get('ai_citation_rate', '0%'),
                "lead_conversion": success_data.get('lead_conversion', '0%'),
                "content_authority": success_data.get('content_authority', 0)
            },
            "schema_annotation": success_data.get('schema_annotation', {}),
            "content_channels": success_data.get('content_channels', []),
            "update_frequency": success_data.get('update_frequency', 'weekly'),
            "created_at": datetime.now().isoformat(),
            "usage_count": 0,
            "last_used": None,
            "effectiveness_score": 0.0
        }
        
        # 保存到模式库
        self.patterns.append(pattern)
        self._save_patterns()
        
        logger.info(f"✅ GEO 结晶模式已创建：{pattern_id}")
        logger.info(f"  成功要素：{len(success_factors)}个")
        logger.info(f"  AI 引用率：{pattern['performance']['ai_citation_rate']}")
        logger.info(f"  潜客转化：{pattern['performance']['lead_conversion']}")
        
        return pattern_id
    
    def _extract_success_factors(self, success_data: Dict) -> List[str]:
        """提取成功要素"""
        factors = []
        
        # Schema 标注完整度
        if success_data.get('schema_completeness', 0) > 0.9:
            factors.append("Schema 标注完整度 >90%")
        
        # 多渠道互证
        channels = success_data.get('content_channels', [])
        if len(channels) >= 2:
            factors.append(f"多渠道互证 ({'+'.join(channels)})")
        
        # AI 引用次数
        if success_data.get('ai_citation_count', 0) > 10:
            factors.append(f"Perplexity AI 引用 >{success_data.get('ai_citation_count')}次/月")
        
        # 内容更新频率
        if success_data.get('update_frequency') == 'daily':
            factors.append("内容更新频率 每日")
        elif success_data.get('update_frequency') == 'weekly_3':
            factors.append("内容更新频率 每周 3 次")
        
        # 内容权威性
        if success_data.get('content_authority', 0) > 80:
            factors.append(f"内容权威性 >{success_data.get('content_authority')}分")
        
        # 潜客转化率
        lead_conv = success_data.get('lead_conversion', '0%')
        if isinstance(lead_conv, str):
            lead_conv = float(lead_conv.replace('%', '')) / 100
        if lead_conv > 0.05:
            factors.append(f"潜客转化率 >{lead_conv*100:.0f}%")
        
        return factors
    
    def query_patterns(self, query: Dict) -> List[Dict]:
        """
        根据查询条件推荐结晶模式
        
        Args:
            query: 查询条件
            
        Returns:
            推荐的结晶模式列表
        """
        logger.info(f"🔍 查询 GEO 结晶模式：{query}")
        
        matched_patterns = []
        
        for pattern in self.patterns:
            score = self._calculate_match_score(pattern, query)
            if score > 0.5:
                pattern['match_score'] = score
                matched_patterns.append(pattern)
        
        # 按匹配度排序
        matched_patterns = sorted(
            matched_patterns,
            key=lambda x: x['match_score'],
            reverse=True
        )
        
        logger.info(f"✅ 匹配到{len(matched_patterns)}个结晶模式")
        
        return matched_patterns[:5]  # 返回前 5 个
    
    def _calculate_match_score(self, pattern: Dict, query: Dict) -> float:
        """计算模式匹配度"""
        score = 0.0
        
        # 产品匹配
        if pattern.get('product') == query.get('product'):
            score += 0.4
        
        # 性能匹配
        if query.get('min_ai_citation'):
            pattern_citation = float(pattern['performance']['ai_citation_rate'].replace('%', ''))
            if pattern_citation >= query['min_ai_citation']:
                score += 0.2
        
        # 成功要素匹配
        if query.get('success_factors'):
            pattern_factors = set(pattern.get('success_factors', []))
            query_factors = set(query['success_factors'])
            overlap = len(pattern_factors & query_factors)
            if overlap > 0:
                score += 0.3 * (overlap / len(query_factors))
        
        # 使用次数匹配 (使用次数多的模式更可靠)
        usage_score = min(0.1, pattern.get('usage_count', 0) * 0.01)
        score += usage_score
        
        return score
    
    def update_pattern_usage(self, pattern_id: str, result: Dict):
        """
        更新结晶模式使用记录
        
        Args:
            pattern_id: 结晶模式 ID
            result: 应用结果
        """
        logger.info(f"📊 更新结晶模式使用记录：{pattern_id}")
        
        for pattern in self.patterns:
            if pattern['pattern_id'] == pattern_id:
                pattern['usage_count'] += 1
                pattern['last_used'] = datetime.now().isoformat()
                
                # 更新效果评分
                if 'effectiveness' in result:
                    old_score = pattern['effectiveness_score']
                    new_score = result['effectiveness']
                    # 移动平均更新
                    pattern['effectiveness_score'] = old_score * 0.8 + new_score * 0.2
                
                logger.info(f"✅ 结晶模式使用记录已更新")
                logger.info(f"  使用次数：{pattern['usage_count']}")
                logger.info(f"  效果评分：{pattern['effectiveness_score']:.2f}")
                break
        
        self._save_patterns()
    
    def _save_patterns(self):
        """保存结晶模式"""
        with open(self.pattern_file, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, indent=2, ensure_ascii=False)
    
    def get_pattern_statistics(self) -> Dict:
        """获取结晶模式统计"""
        if not self.patterns:
            return {
                "total_patterns": 0,
                "avg_usage_count": 0,
                "avg_effectiveness": 0
            }
        
        return {
            "total_patterns": len(self.patterns),
            "avg_usage_count": sum(p.get('usage_count', 0) for p in self.patterns) / len(self.patterns),
            "avg_effectiveness": sum(p.get('effectiveness_score', 0) for p in self.patterns) / len(self.patterns),
            "most_used_pattern": max(self.patterns, key=lambda x: x.get('usage_count', 0))['pattern_id'] if self.patterns else None
        }


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🧬 GEO 结晶模式库 - 演示")
    logger.info("=" * 60)
    
    # 初始化模式库
    library = GEOPatternLibrary()
    
    # 创建结晶模式
    logger.info("\n🧬 创建 GEO 结晶模式...")
    success_data = {
        "product": "便携式储能电源",
        "ai_citation_rate": "35%",
        "lead_conversion": "8%",
        "content_authority": 85,
        "schema_completeness": 0.95,
        "content_channels": ["LinkedIn", "Quora", "官网博客"],
        "ai_citation_count": 15,
        "update_frequency": "weekly_3"
    }
    
    pattern_id = library.create_pattern(success_data)
    logger.info(f"结晶模式 ID: {pattern_id}")
    
    # 查询结晶模式
    logger.info("\n🔍 查询结晶模式...")
    query = {
        "product": "便携式储能电源",
        "min_ai_citation": 20,
        "success_factors": ["Schema 标注完整度 >90%", "多渠道互证"]
    }
    
    matched_patterns = library.query_patterns(query)
    logger.info(f"匹配到{len(matched_patterns)}个结晶模式")
    
    for i, pattern in enumerate(matched_patterns, 1):
        logger.info(f"\n{i}. {pattern['pattern_name']}")
        logger.info(f"   匹配度：{pattern['match_score']:.2f}")
        logger.info(f"   使用次数：{pattern['usage_count']}")
        logger.info(f"   效果评分：{pattern['effectiveness_score']:.2f}")
    
    # 获取统计
    logger.info("\n📊 结晶模式统计...")
    stats = library.get_pattern_statistics()
    logger.info(f"总结晶模式：{stats['total_patterns']}")
    logger.info(f"平均使用次数：{stats['avg_usage_count']:.1f}")
    logger.info(f"平均效果评分：{stats['avg_effectiveness']:.2f}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
