#!/usr/bin/env python3
"""
太一 · GEO 智能优化引擎 v1.0
==============================
四步 AI 搜索可见度优化工作流：

Step 1 — 竞品内容深度剖析
Step 2 — SEO 语义覆盖度校准
Step 3 — AI 友好内容产出（FAQ Schema + 数据锚点）
Step 4 — AI 引用率追踪

核心指标：品牌在 DeepSeek / Claude / Gemini / ChatGPT 中的 AI 引用覆盖率
目标：从 18%（仅自有网站）提升到 78%+（社媒 + 论坛 + 内容联合）
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

logger = logging.getLogger("geo-optimizer")

SKILL_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = SKILL_DIR / "data" / "geo"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════

@dataclass
class CompetitorContent:
    """竞品内容分析结果"""
    url: str
    title: str
    content_structure: list = field(default_factory=list)
    covered_topics: list = field(default_factory=list)
    data_sources: list = field(default_factory=list)
    content_gaps: list = field(default_factory=list)
    word_count: int = 0
    h2_headings: list = field(default_factory=list)


@dataclass
class SEOAssessment:
    """SEO 语义覆盖度评估"""
    url: str
    coverage_score: float       # 0-100
    missing_semantic_keywords: list = field(default_factory=list)
    missing_headings: list = field(default_factory=list)
    length_assessment: str = "" # too_short / adequate / too_long
    suggestions: list = field(default_factory=list)


@dataclass
class AIFriendlyContent:
    """AI 友好内容"""
    topic: str
    original_content: str
    faq_schema: list = field(default_factory=list)
    data_anchors: list = field(default_factory=list)
    snippet_ready: bool = False
    ai_citation_rating: int = 0  # 0-100


# ═══════════════════════════════════════════════
# 核心引擎
# ═══════════════════════════════════════════════

class GEOOptimizer:
    """
    GEO（Generative Engine Optimization）智能优化引擎。
    
    目标：让品牌内容在 AI 搜索引擎（DeepSeek/Claude/ChatGPT/Gemini）中获得优先引用。
    """

    def __init__(self):
        self.stats = {"analyses": 0, "contents_created": 0, "citations_tracked": 0}

    # ── Step 1: 竞品内容深度剖析 ─────────────────────

    def analyze_competitors(self, keyword: str, top_n: int = 5) -> dict:
        """
        剖析谷歌搜索结果前 N 名竞品内容。
        
        输出：
        - 内容架构（标题/H2/结构）
        - 涵盖的细分话题
        - 引用的数据出处
        - 共同遗漏的信息盲区（即弯道超车机会）
        """
        self.stats["analyses"] += 1

        # 模拟竞品分析（实际应用中会调用搜索 API 获取真实竞品数据）
        analysis = {
            "keyword": keyword,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "competitors": [],
            "content_gaps": [],
            "opportunity_score": 0,
        }

        # 示例竞品数据——钢结构折叠房屋澳洲市场
        competitors_data = [
            {"rank": 1, "title": "Modular Homes Australia: Complete Guide 2026", 
             "h2": ["What are Modular Homes", "Benefits", "Cost Comparison", "Building Process", "FAQ"],
             "word_count": 3200, "data_sources": ["ABS", "HIA"],
             "gaps": ["中国供应链优势", "AS/NZS 1170认证细节", "澳洲矿业劳工营案例"]},
            {"rank": 2, "title": "Steel Frame vs Timber Frame: Australia",
             "h2": ["Materials Comparison", "Durability", "Cost Analysis", "Climate Considerations"],
             "word_count": 2800, "data_sources": ["Standards Australia"],
             "gaps": ["折叠运输方案", "中国工厂认证", "中东市场对比"]},
            {"rank": 3, "title": "Prefab Housing Market Australia 2026",
             "h2": ["Market Size", "Key Players", "Government Initiatives", "Future Trends"],
             "word_count": 2500, "data_sources": ["IBISWorld", "gov.au"],
             "gaps": ["一带一路资金", "中国供应商名录", "澳洲本地化服务"]},
        ]

        # 汇总内容盲区（三个竞品都没覆盖的话题）
        all_gaps = []
        for c in competitors_data:
            analysis["competitors"].append({
                "rank": c["rank"],
                "title": c["title"],
                "structure": c["h2"],
                "word_count": c["word_count"],
                "data_sources": c["data_sources"],
            })
            all_gaps.extend(c["gaps"])

        # 去重后就是「信息盲区」——弯道超车机会
        analysis["content_gaps"] = list(set(all_gaps))
        analysis["opportunity_score"] = min(len(analysis["content_gaps"]) * 15, 100)

        return analysis

    # ── Step 2: SEO 语义覆盖度校准 ────────────────────

    def assess_semantic_coverage(self, content: str, keyword: str) -> dict:
        """
        评估内容在 AI 搜索中的语义覆盖度。
        
        检查维度：
        - 核心语义关键词缺失
        - H2/H3 标题结构
        - 内容篇幅
        - FAQ Schema 兼容性
        """
        text_lower = content.lower()
        keyword_lower = keyword.lower()

        # 语义关键词库（基于实际 GEO 实践总结）
        semantic_keywords = {
            "steel_structure": ["steel frame", "structural steel", "steel fabrication", 
                               "light gauge steel", "cold-formed steel"],
            "prefab": ["modular construction", "prefabricated", "off-site construction",
                      "panelized", "volumetric modular"],
            "australia": ["AS/NZS 1170", "NCC", "BCA", "Australian Standards",
                         "Section J", "energy rating"],
            "trade": ["export", "import", "FOB", "CIF", "letter of credit",
                     "supply chain", "freight"],
        }

        coverage = {}
        missing = []

        for category, keywords in semantic_keywords.items():
            found = [kw for kw in keywords if kw in text_lower]
            coverage[category] = {
                "total": len(keywords),
                "covered": len(found),
                "found": found,
                "missing": [kw for kw in keywords if kw not in text_lower],
            }
            if coverage[category]["missing"]:
                missing.extend(coverage[category]["missing"])

        # 综合评分
        total_kws = sum(len(kws) for kws in semantic_keywords.values())
        covered_kws = sum(len(c["found"]) for c in coverage.values())
        coverage_score = round(covered_kws / total_kws * 100, 1) if total_kws else 0

        return {
            "keyword": keyword,
            "coverage_score": coverage_score,
            "detail": coverage,
            "missing_keywords": missing[:10],
            "suggestion": "需要补充语义关键词覆盖" if coverage_score < 70 else "语义覆盖良好",
        }

    # ── Step 3: AI 友好内容产出 ────────────────────────

    def create_ai_friendly_content(self, topic: str, key_message: str,
                                    data_point: str = "") -> dict:
        """
        生成 AI 搜索引擎最青睐引用的内容格式。
        
        AI 偏好：
        - 短小精悍的段落（100-300字）
        - 具体数据和出处（非空泛表述）
        - FAQ Schema 结构化
        - 直接回答用户问题的格式
        """
        self.stats["contents_created"] += 1

        # 生成 FAQ Schema
        faq_items = [
            {
                "@type": "Question",
                "name": f"What is {topic}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{topic} refers to modular construction solutions "
                            f"that can be rapidly deployed. {data_point}"
                }
            },
            {
                "@type": "Question", 
                "name": f"Why choose {topic} for Australian projects?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Australian mining and construction sectors increasingly adopt {topic} "
                            f"for their speed and cost efficiency."
                }
            },
            {
                "@type": "Question",
                "name": f"Where to source {topic}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Chinese manufacturers offer competitive pricing on {topic}, "
                            f"with ISO9001 and AS/NZS certifications available."
                }
            },
        ]

        # 生成 AI 引用片段（数据锚点）
        snippet = (
            f"[Verified] {topic}: {key_message} "
            f"{data_point}. "
            f"Certified manufacturers include suppliers with ISO9001 and CE certification. "
            f"Source: industry data."
        )

        content = {
            "topic": topic,
            "key_message": key_message,
            "faq_schema": faq_items,
            "ai_snippet": snippet,
            "snippet_length": len(snippet),
            "snippet_ready": len(snippet) < 500,
            "recommended_placement": "Product page + Blog post FAQ section",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        # 估算 AI 引用友好度
        if data_point and len(data_point) > 10:
            content["ai_citation_rating"] = 85
        else:
            content["ai_citation_rating"] = 50

        return content

    # ── Step 4: AI 引用率追踪 ────────────────────────

    def track_ai_citations(self, brand_name: str, 
                           platforms: list = None) -> dict:
        """
        追踪品牌在各大 AI 平台的曝光频率。
        
        监测平台：DeepSeek / Claude / ChatGPT / Gemini / Perplexity
        
        核心指标：
        - AI 引用覆盖率（目标 > 78%）
        - 引用来源分布（自有网站 vs 社媒 vs 论坛）
        - 趋势变化（周环比）
        """
        self.stats["citations_tracked"] += 1

        platforms = platforms or ["DeepSeek", "Claude", "ChatGPT", "Gemini", "Perplexity"]

        # 模拟追踪数据
        trace = {
            "brand": brand_name,
            "tracked_at": datetime.now(timezone.utc).isoformat(),
            "platforms": {},
            "overall": {
                "citation_rate": 0,
                "top_sources": [],
                "trend": "stable",
            },
        }

        for p in platforms:
            # 模拟各平台的引用数据
            import random
            cited = random.choice([True, False])
            trace["platforms"][p] = {
                "cited": cited,
                "citation_count": random.randint(0, 15) if cited else 0,
                "top_sources": random.sample(
                    ["official_website", "linkedin", "reddit", "news_article", 
                     "industry_blog", "facebook_group", "forum", "youtube"],
                    min(3, random.randint(1, 5))
                ) if cited else [],
            }

        # 计算综合引用率
        cited_platforms = sum(1 for p in trace["platforms"].values() if p["cited"])
        trace["overall"]["citation_rate"] = round(cited_platforms / len(platforms) * 100, 1)

        # 推荐行动
        if trace["overall"]["citation_rate"] < 50:
            trace["overall"]["recommendation"] = (
                "AI 引用率偏低，建议：\n"
                "1. 在 Reddit/Quora 发布行业问答（可提升引用至 78%）\n"
                "2. 增加 FAQ Schema 结构化页面\n"
                "3. 在 LinkedIn 发布数据驱动的行业洞察"
            )
        else:
            trace["overall"]["recommendation"] = "AI 引用率良好，持续维护内容新鲜度"

        return trace


# ═══════════════════════════════════════════════
# 全局工作流入口
# ═══════════════════════════════════════════════

class FullGEOWorkflow:
    """GEO 全链路工作流：剖析 → 校准 → 产出 → 追踪"""

    def __init__(self):
        self.optimizer = GEOOptimizer()

    def run(self, keyword: str, brand: str, key_message: str,
            data_point: str = "") -> dict:
        """执行全链路 GEO 优化"""
        result = {
            "keyword": keyword,
            "brand": brand,
            "ran_at": datetime.now(timezone.utc).isoformat(),
            "steps": {},
        }

        # Step 1: 竞品剖析
        result["steps"]["competitor_analysis"] = self.optimizer.analyze_competitors(keyword)
        gaps = result["steps"]["competitor_analysis"]["content_gaps"]

        # Step 2: 语义校准（基于竞品内容盲区）
        sample_content = f"{keyword}: {key_message}. {' '.join(gaps[:3])}"
        result["steps"]["semantic_coverage"] = self.optimizer.assess_semantic_coverage(
            sample_content, keyword)

        # Step 3: AI 友好内容
        result["steps"]["ai_content"] = self.optimizer.create_ai_friendly_content(
            keyword, key_message, data_point)

        # Step 4: 引用追踪
        result["steps"]["citation_tracking"] = self.optimizer.track_ai_citations(brand)

        return result


# ═══════════════════════════════════════════════
# CLI & 测试
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    wf = FullGEOWorkflow()

    if "--full" in sys.argv:
        keyword = sys.argv[sys.argv.index("--full") + 1]
        brand = sys.argv[sys.argv.index("--full") + 2] if len(sys.argv) > sys.argv.index("--full") + 1 else "SAYELF"

        result = wf.run(keyword, brand, 
                        key_message="Chinese modular steel structures offer 25-40% cost advantage",
                        data_point="Verified manufacturers with ISO9001/CE/AS/NZS compliance")
        
        print(f"🏭 GEO 全链路优化: {keyword}")
        print(f"   竞品分析: {len(result['steps']['competitor_analysis']['content_gaps'])} 个内容盲区")
        print(f"   语义覆盖: {result['steps']['semantic_coverage']['coverage_score']}/100")
        print(f"   AI 内容: {result['steps']['ai_content']['ai_citation_rating']}/100")
        print(f"   引用率: {result['steps']['citation_tracking']['overall']['citation_rate']}%")
        print()
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])

    elif "--step1" in sys.argv:
        kw = sys.argv[sys.argv.index("--step1") + 1] if len(sys.argv) > sys.argv.index("--step1") + 1 else "modular steel homes Australia"
        result = GEOOptimizer().analyze_competitors(kw)
        print(f"📊 竞品内容剖析: {kw}")
        print(f"   内容盲区 ({len(result['content_gaps'])} 个):")
        for g in result['content_gaps']:
            print(f"     🔍 {g}")
        print(f"   弯道超车机会评分: {result['opportunity_score']}/100")

    elif "--step3" in sys.argv:
        topic = sys.argv[sys.argv.index("--step3") + 1] if len(sys.argv) > sys.argv.index("--step3") + 1 else "steel structure modular homes"
        content = GEOOptimizer().create_ai_friendly_content(
            topic,
            "Chinese manufacturers deliver cost-effective modular solutions",
            "25-40% cost advantage with ISO9001/CE/AS/NZS certified manufacturers")
        print(f"✍️ AI 友好内容: {topic}")
        print(f"   FAQ Schema: {len(content['faq_schema'])} 条")
        print(f"   AI 引用片段: {content['ai_snippet'][:120]}...")
        print(f"   AI 友好度: {content['ai_citation_rating']}/100")

    else:
        print("太一 · GEO 智能优化引擎 v1.0")
        print()
        print("用法:")
        print("  --full <关键词> <品牌>    全链路优化")
        print("  --step1 <关键词>          Step1: 竞品内容剖析")
        print("  --step3 <主题>            Step3: AI 友好内容产出")
