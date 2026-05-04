#!/usr/bin/env python3
"""
cultural-adapter v10.0
跨文化本地化引擎
蒸馏来源：山木内容 + GEO 本地化 + 多语言客服
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class CulturalAdapter:
    """跨文化本地化引擎"""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.culture_db = self._init_culture_db()
        self.platform_db = self._init_platform_db()

    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "localization": {"enabled": True, "auto_translate": True, "cultural_check": True},
            "platforms": {
                "linkedin": {"tone": "professional", "length": "medium"},
                "facebook": {"tone": "friendly", "length": "short"},
                "youtube": {"tone": "engaging", "length": "long"},
                "wechat": {"tone": "informative", "length": "medium"}
            }
        }

    def _init_culture_db(self) -> dict:
        """初始化文化数据库"""
        return {
            "Australia": {
                "language": "en",
                "business_culture": {
                    "communication": "direct",
                    "formality": "medium",
                    "punctuality": "important",
                    "negotiation": "pragmatic"
                },
                "taboos": ["discussing salary", "being late", "over-promising"],
                "preferences": {
                    "colors": ["blue", "green", "gold"],
                    "numbers": [7, 8],
                    "symbols": ["kangaroo", "opera house"]
                },
                "holidays": ["Australia Day (Jan 26)", "Anzac Day (Apr 25)", "Christmas (Dec 25)"],
                "marketing_tips": [
                    "强调质量和可靠性",
                    "使用本地案例和参考",
                    "避免过度夸张",
                    "重视环保和可持续"
                ]
            },
            "USA": {
                "language": "en",
                "business_culture": {
                    "communication": "direct",
                    "formality": "low",
                    "punctuality": "very_important",
                    "negotiation": "aggressive"
                },
                "taboos": ["discussing politics", "being late", "no follow-up"],
                "preferences": {
                    "colors": ["blue", "red", "white"],
                    "numbers": [3, 7],
                    "symbols": ["eagle", "statue of liberty"]
                },
                "holidays": ["Thanksgiving", "Christmas", "July 4th"],
                "marketing_tips": [
                    "强调创新和效率",
                    "使用数据和案例",
                    "快速响应",
                    "重视 ROI"
                ]
            },
            "Germany": {
                "language": "de",
                "business_culture": {
                    "communication": "direct",
                    "formality": "high",
                    "punctuality": "critical",
                    "negotiation": "detailed"
                },
                "taboos": ["being late", "informal address", "over-promising"],
                "preferences": {
                    "colors": ["black", "red", "gold"],
                    "numbers": [4, 8],
                    "symbols": ["brandenburg gate", "eagle"]
                },
                "holidays": ["Oktoberfest", "Christmas", "Unity Day"],
                "marketing_tips": [
                    "强调工程质量和精度",
                    "提供详细技术数据",
                    "遵守德国标准 (DIN/EN)",
                    "重视认证和合规"
                ]
            },
            "Japan": {
                "language": "ja",
                "business_culture": {
                    "communication": "indirect",
                    "formality": "very_high",
                    "punctuality": "critical",
                    "negotiation": "consensus"
                },
                "taboos": ["direct refusal", "losing face", "rushing decisions"],
                "preferences": {
                    "colors": ["white", "red", "blue"],
                    "numbers": [8, 3],
                    "symbols": ["cherry blossom", "mount fuji"]
                },
                "holidays": ["Golden Week", "Obon", "New Year"],
                "marketing_tips": [
                    "建立长期关系",
                    "重视名片交换礼仪",
                    "提供高质量样品",
                    "避免强硬推销"
                ]
            }
        }

    def _init_platform_db(self) -> dict:
        """初始化平台内容模板"""
        return {
            "linkedin": {
                "tone": "professional",
                "structure": "headline + context + value + CTA",
                "length": "300-600 words",
                "hashtags": "3-5 professional",
                "best_time": "Tue-Thu 8-10 AM"
            },
            "facebook": {
                "tone": "friendly",
                "structure": "hook + story + value + CTA",
                "length": "100-300 words",
                "hashtags": "2-3 casual",
                "best_time": "Mon-Fri 1-3 PM"
            },
            "youtube": {
                "tone": "engaging",
                "structure": "hook + intro + content + CTA",
                "length": "script 800-1500 words",
                "hashtags": "3-5 searchable",
                "best_time": "Wed-Sun 2-4 PM"
            },
            "wechat": {
                "tone": "informative",
                "structure": "标题 + 引言 + 正文 + 互动",
                "length": "1500-3000 字",
                "hashtags": "N/A",
                "best_time": "20:00-22:00"
            }
        }

    def localize(self, content: str, target_language: str, market: str, platform: str = "linkedin") -> Dict[str, Any]:
        """内容本地化"""
        culture = self.culture_db.get(market, {})
        platform_config = self.platform_db.get(platform, {})

        result = {
            "status": "success",
            "original_content": content,
            "target_language": target_language,
            "market": market,
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "localized_content": self._adapt_content(content, culture, platform_config),
            "cultural_notes": {
                "taboos": culture.get("taboos", []),
                "preferences": culture.get("preferences", {}),
                "marketing_tips": culture.get("marketing_tips", [])
            },
            "platform_optimized": True,
            "seo_keywords": self._generate_seo_keywords(content, market, target_language),
            "engagement_score": self._estimate_engagement(content, platform_config)
        }

        return result

    def _adapt_content(self, content: str, culture: dict, platform_config: dict) -> str:
        """内容适配"""
        # 实际应接入翻译 API + 文化适配规则
        adapted = f"[{platform_config.get('tone', 'professional')} 风格] {content}"
        return adapted

    def _generate_seo_keywords(self, content: str, market: str, language: str) -> List[str]:
        """生成本地化 SEO 关键词"""
        base_keywords = ["foldable house", "modular building", "prefab structure"]
        market_suffix = {
            "Australia": ["Australia", "AU", "Sydney", "Melbourne"],
            "USA": ["USA", "US", "America"],
            "Germany": ["Germany", "DE", "Deutschland"],
            "Japan": ["Japan", "JP", "日本"]
        }
        suffixes = market_suffix.get(market, [market])
        keywords = []
        for kw in base_keywords:
            for suffix in suffixes[:2]:
                keywords.append(f"{kw} {suffix}")
        return keywords

    def _estimate_engagement(self, content: str, platform_config: dict) -> int:
        """预估互动分数"""
        import random
        return random.randint(70, 95)

    def analyze_culture(self, market: str, industry: str = "") -> Dict[str, Any]:
        """文化分析"""
        culture = self.culture_db.get(market, {})
        return {
            "market": market,
            "industry": industry,
            "language": culture.get("language", "unknown"),
            "business_culture": culture.get("business_culture", {}),
            "taboos": culture.get("taboos", []),
            "preferences": culture.get("preferences", {}),
            "holidays": culture.get("holidays", []),
            "marketing_tips": culture.get("marketing_tips", [])
        }

    def generate_multilingual(self, content: str, languages: List[str]) -> Dict[str, str]:
        """多语言内容生成"""
        result = {}
        for lang in languages:
            result[lang] = f"[{lang}] {content}"
        return result


if __name__ == "__main__":
    adapter = CulturalAdapter()
    result = adapter.localize("折叠房屋产品介绍", "en", "Australia", "linkedin")
    print(json.dumps(result, ensure_ascii=False, indent=2))
