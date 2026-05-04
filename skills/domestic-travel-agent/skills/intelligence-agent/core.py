#!/usr/bin/env python3
"""
旅游综合情报引擎 v1.0 — 搜索/权重/排序/推荐/情感引导
太一 AGI · 2026-05-04

管道: 多平台搜索 → 权重评分 → 性价比排序 → 情感引导 → 索引链接
"""
import json, sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus

# 权重配置
WEIGHTS = {
    "hotel": {"price": 0.25, "rating": 0.25, "location": 0.20, "reviews": 0.15, "value": 0.15},
    "restaurant": {"price": 0.20, "rating": 0.30, "cuisine_quality": 0.20, "ambience": 0.15, "location": 0.15},
    "attraction": {"rating": 0.30, "price_value": 0.20, "uniqueness": 0.25, "family_friendly": 0.25},
    "transport": {"price": 0.35, "speed": 0.25, "comfort": 0.20, "reliability": 0.20},
}

# ===== 社交平台大V/博主搜索 =====
SOCIAL_INFLUENCERS = {
    # 国内视频/社交
    "抖音旅游大V": [
        {"name": "房琪kiki", "url": "https://www.douyin.com/user/房琪kiki",
         "platform": "抖音", "followers": "2000万+", "style": "旅行Vlog/文案天花板"},
        {"name": "itsRae", "url": "https://www.douyin.com/user/itsRae",
         "platform": "抖音", "followers": "1500万+", "style": "旅行记录/真实感"},
        {"name": "幻想家姜时一", "url": "https://www.douyin.com/user/幻想家姜时一",
         "platform": "抖音", "followers": "1000万+", "style": "小众景点/深度游"},
        {"name": "旅游约吗", "url": "https://www.douyin.com/user/旅游约吗",
         "platform": "抖音", "followers": "800万+", "style": "酒店探店/旅行攻略"},
    ],
    "B站旅行UP主": [
        {"name": "徐云流浪中国", "url": "https://space.bilibili.com/徐云",
         "platform": "B站", "followers": "300万+", "style": "骑行/户外/纪实"},
        {"name": "小墨与阿猴", "url": "https://space.bilibili.com/小墨与阿猴",
         "platform": "B站", "followers": "200万+", "style": "旅行摄影/Vlog"},
        {"name": "破产兄弟BrokeBros", "url": "https://space.bilibili.com/破产兄弟",
         "platform": "B站", "followers": "150万+", "style": "穷游/深度体验"},
    ],
    "小红书旅行博主": [
        {"name": "旅行博主XXX", "url": "https://www.xiaohongshu.com/search_result?keyword=旅行博主+攻略",
         "platform": "小红书", "followers": "高", "style": "探店/打卡/攻略"},
        {"name": "自制攻略", "url": "https://www.xiaohongshu.com/search_result?keyword=旅游攻略+详细",
         "platform": "小红书", "followers": "高", "style": "详细攻略/预算"},
    ],
    "视频号/微信旅游": [
        {"name": "视频号旅游", "url": "https://channels.weixin.qq.com/search?q=旅游",
         "platform": "视频号", "followers": "—", "style": "微信生态旅行内容"},
    ],
    "微博旅游博主": [
        {"name": "微博旅游", "url": "https://weibo.com/搜索/旅游攻略",
         "platform": "微博", "followers": "—", "style": "热点头条/旅行话题"},
    ],
    # 国外视频/社交
    "YouTube Travel Creators": [
        {"name": "Mark Wiens", "url": "https://www.youtube.com/@MarkWiens",
         "platform": "YouTube", "followers": "1000万+", "style": "美食旅行/街头美食"},
        {"name": "Kara and Nate", "url": "https://www.youtube.com/@KaraandNate",
         "platform": "YouTube", "followers": "500万+", "style": "环球旅行/冒险"},
        {"name": "FunForLouis", "url": "https://www.youtube.com/@FunForLouis",
         "platform": "YouTube", "followers": "200万+", "style": "背包旅行/自驾"},
        {"name": "Drew Binsky", "url": "https://www.youtube.com/@DrewBinsky",
         "platform": "YouTube", "followers": "400万+", "style": "足迹遍布197国"},
        {"name": "Hey Nadine", "url": "https://www.youtube.com/@HeyNadine",
         "platform": "YouTube", "followers": "100万+", "style": "旅行攻略/省钱技巧"},
    ],
    "Instagram Travel Influencers": [
        {"name": "Travel + Leisure", "url": "https://www.instagram.com/travelandleisure/",
         "platform": "Instagram", "followers": "500万+", "style": "旅行灵感/目的地推荐"},
        {"name": "Beautiful Destinations", "url": "https://www.instagram.com/beautifuldestinations/",
         "platform": "Instagram", "followers": "3000万+", "style": "顶级旅行摄影"},
        {"name": "Passion Passport", "url": "https://www.instagram.com/passionpassport/",
         "platform": "Instagram", "followers": "200万+", "style": "社区旅行故事"},
    ],
    "Twitter/X Travel Community": [
        {"name": "Lonely Planet", "url": "https://twitter.com/lonelyplanet",
         "platform": "Twitter/X", "followers": "500万+", "style": "旅行指南/目的地"},
        {"name": "Travel Twitter", "url": "https://twitter.com/search?q=travel+guide",
         "platform": "Twitter/X", "followers": "—", "style": "实时旅行讨论"},
    ],
    "Facebook Travel Groups": [
        {"name": "Travel + Leisure", "url": "https://www.facebook.com/TravelandLeisure/",
         "platform": "Facebook", "followers": "800万+", "style": "旅行灵感"},
        {"name": "National Geographic Travel", "url": "https://www.facebook.com/natgeotravel/",
         "platform": "Facebook", "followers": "600万+", "style": "自然/探险旅行"},
    ],
    # ===== 美学大V =====
    "美学·摄影大V": [
        {"name": "Thomas看看世界", "url": "https://space.bilibili.com/Thomas看看世界",
         "platform": "B站", "followers": "300万+", "style": "摄影美学/全球旅行摄影/建筑视觉"},
        {"name": "摄影师刘聪", "url": "https://www.douyin.com/user/摄影师刘聪",
         "platform": "抖音", "followers": "500万+", "style": "城市美学/光影构图/建筑摄影"},
        {"name": "卷毛佟", "url": "https://www.xiaohongshu.com/user/卷毛佟",
         "platform": "小红书", "followers": "200万+", "style": "手机摄影/旅行美学/构图技巧"},
        {"name": "Brandon Woelfel", "url": "https://www.instagram.com/brandonwoelfel/",
         "platform": "Instagram", "followers": "400万+", "style": "梦幻光影/色彩美学/城市摄影"},
        {"name": "Chris Burkard", "url": "https://www.instagram.com/chrisburkard/",
         "platform": "Instagram", "followers": "500万+", "style": "自然景观/极简美学/冒险摄影"},
        {"name": "Morten Hilmer", "url": "https://www.youtube.com/@MortenHilmer",
         "platform": "YouTube", "followers": "100万+", "style": "荒野美学/自然摄影/北欧极简"},
    ],
    # ===== 历史大V =====
    "历史·古迹大V": [
        {"name": "中国国家地理", "url": "https://www.bilibili.com/中国国家地理",
         "platform": "B站", "followers": "500万+", "style": "地理历史/人文遗迹/自然奇观"},
        {"name": "历史那些事", "url": "https://www.douyin.com/user/历史那些事",
         "platform": "抖音", "followers": "2000万+", "style": "历史故事/古迹探秘"},
        {"name": "杨爸图说", "url": "https://www.bilibili.com/杨爸图说",
         "platform": "B站", "followers": "400万+", "style": "世界历史/文明遗产/博物馆"},
        {"name": "小璐歌", "url": "https://www.douyin.com/user/小璐歌",
         "platform": "抖音", "followers": "800万+", "style": "古建筑/历史文化/深度讲解"},
        {"name": "History Hit", "url": "https://www.youtube.com/@HistoryHit",
         "platform": "YouTube", "followers": "500万+", "style": "世界历史/古迹遗址/战争历史"},
        {"name": "Timeline World History", "url": "https://www.youtube.com/@TimelineWorldHistory",
         "platform": "YouTube", "followers": "300万+", "style": "古代文明/世界遗产/考古发现"},
        {"name": "National Geographic History", "url": "https://www.instagram.com/natgeo/",
         "platform": "Instagram", "followers": "2亿+", "style": "历史地理/自然文化"},
    ],
    # ===== 文化/人文大V =====
    "文化·人文大V": [
        {"name": "李子柒", "url": "https://www.youtube.com/@李子柒",
         "platform": "YouTube", "followers": "2000万+", "style": "传统文化/田园生活/非遗手艺"},
        {"name": "滇西小哥", "url": "https://www.youtube.com/@滇西小哥",
         "platform": "YouTube", "followers": "1000万+", "style": "云南少数民族文化/地方美食"},
        {"name": "阿木爷爷", "url": "https://www.youtube.com/@阿木爷爷",
         "platform": "YouTube", "followers": "500万+", "style": "传统木工/工匠精神"},
        {"name": "穷游锦囊", "url": "https://www.qyer.com/author/穷游锦囊",
         "platform": "穷游", "followers": "专业", "style": "深度文化/目的地人文指南"},
        {"name": "马蜂窝攻略", "url": "https://www.mafengwo.cn/author/攻略",
         "platform": "马蜂窝", "followers": "专业", "style": "人文旅行/在地文化体验"},
        {"name": "Drew Binsky", "url": "https://www.youtube.com/@DrewBinsky",
         "platform": "YouTube", "followers": "400万+", "style": "197国人文纪实/在地文化/真实体验"},
        {"name": "Yes Theory", "url": "https://www.youtube.com/@YesTheory",
         "platform": "YouTube", "followers": "800万+", "style": "人文挑战/文化交流/跨文化体验"},
        {"name": "Indigo Traveller", "url": "https://www.youtube.com/@IndigoTraveller",
         "platform": "YouTube", "followers": "200万+", "style": "小众国家人文/真实市井生活"},
    ],
}

# 平台搜索链接模板
PLATFORM_SEARCH = {
    # 国内
    "携程": lambda q, city: f"https://www.ctrip.com/search?q={quote_plus(city+' '+q)}",
    "飞猪": lambda q, city: f"https://www.fliggy.com/search?q={quote_plus(city+' '+q)}",
    "美团": lambda q, city: f"https://www.meituan.com/search?q={quote_plus(city+' '+q)}",
    "马蜂窝": lambda q, city: f"https://www.mafengwo.cn/search/s.php?q={quote_plus(city+' '+q)}",
    "穷游": lambda q, city: f"https://www.qyer.com/search?q={quote_plus(city+' '+q)}",
    "小红书": lambda q, city: f"https://www.xiaohongshu.com/search_result?keyword={quote_plus(city+' '+q)}",
    "大众点评": lambda q, city: f"https://www.dianping.com/search/keyword/{city}/{quote_plus(q)}",
    "抖音": lambda q, city: f"https://www.douyin.com/search/{quote_plus(city+' '+q)}",
    "B站": lambda q, city: f"https://search.bilibili.com/all?keyword={quote_plus(city+' '+q)}",
    "视频号": lambda q, city: f"https://channels.weixin.qq.com/search?q={quote_plus(city+' '+q)}",
    "微博": lambda q, city: f"https://s.weibo.com/weibo?q={quote_plus(city+' '+q)}",
    # 国外
    "Booking": lambda q, city: f"https://www.booking.com/searchresults.html?ss={quote_plus(city)}",
    "TripAdvisor": lambda q, city: f"https://www.tripadvisor.com/Search?q={quote_plus(city+' '+q)}",
    "Google": lambda q, city: f"https://www.google.com/search?q={quote_plus(city+' '+q)}",
    "KLOOK": lambda q, city: f"https://www.klook.com/search/?keyword={quote_plus(city+' '+q)}",
    "YouTube": lambda q, city: f"https://www.youtube.com/results?search_query={quote_plus(city+' '+q)}",
    "Instagram": lambda q, city: f"https://www.instagram.com/explore/tags/{quote_plus(city.replace(' ',''))}/",
    "Twitter/X": lambda q, city: f"https://twitter.com/search?q={quote_plus(city+' '+q)}",
    "Facebook": lambda q, city: f"https://www.facebook.com/search/top?q={quote_plus(city+' '+q)}",
    "Agoda": lambda q, city: f"https://www.agoda.com/search?city={quote_plus(city)}",
}


class TravelIntelligence:
    """旅游综合情报引擎"""
    
    def __init__(self, city: str = ""):
        self.city = city
    
    # ===== 大V/博主搜索 =====
    def search_influencers(self, topic: str = "旅行") -> Dict:
        """搜索各平台大V/博主关于目的地的内容"""
        results = []
        for platform_type, influencers in SOCIAL_INFLUENCERS.items():
            platform_results = []
            for inf in influencers:
                # 添加城市搜索链接
                search_url = PLATFORM_SEARCH.get(inf["platform"], lambda q,c: "")(topic, self.city)
                platform_results.append({
                    "name": inf["name"],
                    "platform": inf["platform"],
                    "url": inf["url"],
                    "followers": inf["followers"],
                    "style": inf["style"],
                    "search_url": search_url,
                })
            results.append({"platform": platform_type, "influencers": platform_results})
        
        return {
            "city": self.city,
            "topic": topic,
            "platforms": results,
            "total_influencers": sum(len(r["influencers"]) for r in results),
        }
    
    def format_influencers(self, data: Dict) -> str:
        """格式化为可读文本"""
        lines = [
            f"\n{'='*50}",
            f"  📱 各平台大V推荐 · {data['city']} {data['topic']}",
            f"{'='*50}",
        ]
        for platform in data["platforms"]:
            lines.append(f"\n  📂 {platform['platform']}:")
            for inf in platform["influencers"]:
                lines.append(f"    👤 {inf['name']}")
                lines.append(f"       🏆 {inf['followers']}粉丝 | {inf['style']}")
                lines.append(f"       🔗 {inf['url']}")
                if inf['search_url']:
                    lines.append(f"       🔍 [{inf['platform']}搜索]({inf['search_url']})")
        return "\n".join(lines)
    
    # ===== 多平台搜索 =====
    def search_all_platforms(self, query: str, category: str = "") -> Dict:
        """生成所有平台的搜索链接"""
        category_queries = {
            "hotel": f"{query} 酒店",
            "restaurant": f"{query} 美食 餐馆",
            "attraction": f"{query} 景点",
            "transport": f"{query} 交通",
            "guide": f"{query} 导游 攻略",
        }
        search_query = category_queries.get(category, query)
        
        links = {}
        for platform, url_fn in PLATFORM_SEARCH.items():
            links[platform] = url_fn(search_query, self.city)
        
        return {
            "query": search_query,
            "category": category,
            "platforms_searched": len(links),
            "search_links": links,
            "verification": "\n".join([f"🔗 [{p}]({u})" for p, u in links.items()]),
        }
    
    # ===== 权重评分 =====
    def score_item(self, item: Dict, category: str) -> Tuple[float, str]:
        """多维度权重评分"""
        weights = WEIGHTS.get(category, WEIGHTS["hotel"])
        score = 0.0
        breakdown = []
        
        for dim, weight in weights.items():
            raw = item.get(dim, 5.0)
            dim_score = raw * weight
            score += dim_score
            star = "⭐" * min(5, int(dim_score / weight / 2))
            breakdown.append(f"    {dim}: {raw}/10 × {weight} = {dim_score:.1f} {star}")
        
        return round(score, 1), "\n".join(breakdown)
    
    # ===== 性价比排序 =====
    def rank_by_value(self, items: List[Dict], category: str) -> List[Dict]:
        """性价比排序"""
        for item in items:
            score, breakdown = self.score_item(item, category)
            item["_score"] = score
            item["_score_breakdown"] = breakdown
            # 性价比 = (评分 + 情感值) / 价格
            emotion = item.get("emotional_value", 5.0)
            price = item.get("price", 1000)
            item["_value_ratio"] = round((score * 0.6 + emotion * 0.4) / max(price, 1) * 1000, 2)
        
        items.sort(key=lambda x: x.get("_value_ratio", 0), reverse=True)
        return items
    
    # ===== 情感引导 =====
    def emotional_guide(self, category: str, name: str, score: float) -> str:
        """根据评分生成情感引导文案"""
        guides = {
            "hotel": [
                (9, "✨ 极致体验 — 这一晚的风景会让你们的回忆闪闪发光"),
                (7, "💫 值得拥有 — 性价比和品质的完美平衡点"),
                (5, "👍 稳妥之选 — 不会出错，适合过夜休息"),
                (0, "📌 预算考虑 — 满足基本需求，把钱花在其他地方"),
            ],
            "restaurant": [
                (9, "🔥 必吃！错过等于没来过这座城市"),
                (7, "🌟 推荐！本地人也常去的老字号"),
                (5, "👌 可以一试 — 不会踩雷的选择"),
                (0, "📌 填饱肚子 — 适合赶时间的时候"),
            ],
            "attraction": [
                (9, "🏆 此生必去！震撼程度超出你的想象"),
                (7, "🎯 很值得！建议留出半天时间慢慢逛"),
                (5, "📸 适合打卡 — 拍完照就算到此一游"),
                (0, "👀 顺路可去 — 专程去的话可能会失望"),
            ],
        }
        cat_guides = guides.get(category, guides["restaurant"])
        for threshold, text in cat_guides:
            if score >= threshold:
                return text
        return "📌 按需选择"
    
    # ===== 价值分析 =====
    def value_analysis(self, items: List[Dict], category: str, budget: float) -> str:
        """综合价值分析报告"""
        if not items:
            return "暂无数据"
        
        best = items[0]
        second = items[1] if len(items) > 1 else None
        
        lines = [
            f"\n📊 {category.upper()} 性价比分析",
            f"{'='*40}",
            f"\n🥇 最佳推荐: {best.get('name','')}",
            f"   综合评分: {best.get('_score',0)}/10",
            f"   性价比: {best.get('_value_ratio',0)}",
            f"   {self.emotional_guide(category, best.get('name',''), best.get('_score',0))}",
        ]
        
        if second:
            lines += [
                f"\n🥈 备选: {second.get('name','')}",
                f"   评分: {second.get('_score',0)}/10 | 性价比: {second.get('_value_ratio',0)}",
            ]
        
        # 预算建议
        total_cost = sum(item.get("price", 0) for item in items[:3])
        budget_ratio = total_cost / budget * 100 if budget > 0 else 0
        if budget_ratio > 50:
            lines.append(f"\n⚠️ 预算提示: 推荐3项占总预算 {budget_ratio:.0f}%, 建议适当缩减")
        else:
            lines.append(f"\n✅ 预算友好: 推荐3项仅占预算 {budget_ratio:.0f}%, 还有充足余量")
        
        return "\n".join(lines)
    
    # ===== 完整推荐 =====
    def recommend(self, category: str, items: List[Dict], budget: float = 30000) -> Dict:
        """完整推荐管道"""
        # 1. 权重评分
        ranked = self.rank_by_value(items, category)
        
        # 2. 情感引导
        for item in ranked[:3]:
            item["_emotion"] = self.emotional_guide(category, item.get("name",""), item.get("_score",0))
        
        # 3. 价值分析
        analysis = self.value_analysis(ranked, category, budget)
        
        # 4. 平台搜索
        platform_links = self.search_all_platforms(category, category)
        
        return {
            "category": category,
            "city": self.city,
            "ranked_items": ranked[:5],
            "value_analysis": analysis,
            "top_pick": ranked[0] if ranked else None,
            "platform_search_links": platform_links["search_links"],
        }
    
    # ===== 输出 =====
    def format_recommendation(self, result: Dict) -> str:
        """格式化为可读输出"""
        lines = [
            f"\n{'='*50}",
            f"  🏆 {result['city']} {result['category']} 推荐",
            f"{'='*50}",
        ]
        
        for i, item in enumerate(result.get("ranked_items", []), 1):
            icon = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][min(i-1, 4)]
            lines += [
                f"\n{icon} #{i} {item.get('name','')}",
                f"   ⭐ 综合评分: {item.get('_score',0)}/10 | 💰 ¥{item.get('price',0)}",
                f"   💎 性价比: {item.get('_value_ratio',0)}",
                f"   🎯 {item.get('_emotion','')}",
            ]
            if item.get("phone"):
                lines.append(f"   📞 {item['phone']}")
            if item.get("address"):
                lines.append(f"   📍 {item['address']}")
        
        lines.append(f"\n{result.get('value_analysis','')}")
        
        links = result.get("platform_search_links", {})
        top_platforms = list(links.items())[:5]
        if top_platforms:
            lines.append(f"\n🔗 索引链接 (多平台验证):")
            for name, url in top_platforms:
                lines.append(f"   [{name}]({url})")
        
        return "\n".join(lines)


def demo():
    """演示：新加坡酒店推荐"""
    engine = TravelIntelligence("新加坡")
    
    hotels = [
        {"name": "YOTEL Singapore Orchard Road", "price": 400, "rating": 8.5,
         "location": 9, "reviews": 8.0, "value": 8.5,
         "emotional_value": 8.0, "phone": "+65 6868 8000",
         "address": "366 Orchard Rd, Singapore 238904"},
        {"name": "Hotel Boss", "price": 280, "rating": 7.5,
         "location": 8, "reviews": 7.0, "value": 9.0,
         "emotional_value": 6.5, "phone": "+65 6809 6888",
         "address": "500 Jalan Sultan, Singapore 199020"},
        {"name": "Village Hotel Bugis", "price": 350, "rating": 8.0,
         "location": 8.5, "reviews": 7.5, "value": 8.5,
         "emotional_value": 7.5, "phone": "+65 6297 1777",
         "address": "390 Victoria St, Singapore 188061"},
        {"name": "Studio M Hotel", "price": 500, "rating": 8.5,
         "location": 7.5, "reviews": 8.0, "value": 7.5,
         "emotional_value": 8.5, "phone": "+65 6808 8888",
         "address": "3 Nanson Rd, Singapore 238910"},
        {"name": "Marina Bay Sands", "price": 2500, "rating": 9.5,
         "location": 10, "reviews": 9.0, "value": 6.0,
         "emotional_value": 9.5, "phone": "+65 6688 8868",
         "address": "10 Bayfront Ave, Singapore 018956"},
    ]
    
    result = engine.recommend("hotel", hotels, budget=30000)
    print(engine.format_recommendation(result))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        print("用法: python3 intelligence/platform_ranker.py --demo")
