#!/usr/bin/env python3
"""
太一 · 跨境贸易社群发现与参与模块 v1.0
=====================================
全面覆盖国内外跨境贸易相关社群，帮助工厂/供应商发现、加入、参与。

覆盖范围：

国内社群                          国际社群
──────────────────────────────────────────
微信行业群（建筑/建材/外贸）        Facebook Groups (Trade/Buyers)
QQ 行业群（外贸/跨境/物流）         LinkedIn Groups (Industry)
知乎行业圆桌/话题                  Discord Trade Servers
小红书行业垂类                     Slack Trade Communities
行业论坛（福步/FOB/中国制造网）     Reddit (r/importers, r/export)
行业展会线上社群（广交会线上）      Industry Forums (Alibaba, TradeKey)
钉钉行业圈                         WhatsApp Trade Groups
                                     Telegram Trade Channels
"""

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger("cross-border.community")

SKILL_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = SKILL_DIR / "modules" / "community-engagement" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════

@dataclass
class Community:
    """社群定义"""
    name: str
    platform: str          # wechat/qq/zhihu/xiaohongshu/discord/slack/reddit/facebook/linkedin/telegram/whatsapp/forum
    category: str          # trade/construction/steel/prefab/logistics/...
    region: str            # domestic / international / both
    language: str          # zh / en / both
    url: str = ""
    description: str = ""
    members: int = 0
    activity_level: str = "medium"  # high / medium / low
    relevance_score: int = 70      # 0-100
    tags: list = field(default_factory=list)
    engagement_strategy: str = ""  # 参与策略描述


@dataclass
class EngagementPlan:
    """参与计划"""
    community: str
    platform: str
    frequency: str           # daily / weekly / monthly
    content_type: str        # share / answer / post / comment
    topic_focus: list = field(default_factory=list)
    goals: list = field(default_factory=list)


# ═══════════════════════════════════════════════
# 社群知识库
# ═══════════════════════════════════════════════

class CommunityDatabase:
    """跨境贸易社群数据库"""

    # 国内社群模板
    DOMESTIC_COMMUNITIES = [
        Community("福步外贸论坛", "forum", "trade", "domestic", "zh",
                  url="https://bbs.fobshanghai.com",
                  description="中国最大外贸从业者论坛，每日数万帖",
                  members=2000000, activity_level="high", relevance_score=95,
                  tags=["外贸", "B2B", "开发客户", "物流"],
                  engagement_strategy="每日签到 + 专业问题回答 + 分享经验帖"),
        Community("阿里巴巴外贸圈", "forum", "trade", "domestic", "zh",
                  url="https://waimaoquan.alibaba.com",
                  description="阿里系外贸人社区，聚焦平台运营和跨境",
                  members=500000, activity_level="high", relevance_score=90,
                  tags=["Alibaba", "跨境", "平台运营"],
                  engagement_strategy="分享阿里国际站运营经验 + 产品发布技巧"),
        Community("知乎-外贸话题", "zhihu", "trade", "domestic", "zh",
                  url="https://www.zhihu.com/topic/19551421",
                  description="知乎外贸话题，高质量问答",
                  members=300000, activity_level="medium", relevance_score=85,
                  tags=["外贸", "职业发展", "行业分析"],
                  engagement_strategy="每周1篇深度回答 + 行业洞察长文"),
        Community("小红书-外贸/跨境", "xiaohongshu", "trade", "domestic", "zh",
                  url="https://www.xiaohongshu.com",
                  description="年轻外贸人聚集，图文+短视频",
                  members=200000, activity_level="high", relevance_score=75,
                  tags=["跨境", "年轻创业者", "副业"],
                  engagement_strategy="发布工厂探访/产品评测短视频"),
        Community("微信-建筑建材外贸群", "wechat", "construction", "domestic", "zh",
                  url="https://weixin.qq.com/cgi-bin/readtemplate?t=page/favorite/link_page&type=help", description="微信行业群，即时交流+商机对接（需邀请加入）",
                  members=500, activity_level="high", relevance_score=90,
                  tags=["建材", "建筑", "钢结构", "外贸"],
                  engagement_strategy="每日分享行业资讯 + 回答采购询价"),
        Community("QQ-外贸钢结构群", "qq", "construction", "domestic", "zh",
                  url="https://qun.qq.com/", description="QQ 行业技术交流群（搜: 外贸钢结构）",
                  members=2000, activity_level="medium", relevance_score=80,
                  tags=["钢结构", "技术交流", "图纸"],
                  engagement_strategy="分享技术方案 + 解答施工问题"),
        Community("中国制造网内贸社区", "forum", "trade", "domestic", "zh",
                  url="https://cn.Made-in-China.com",
                  description="中国制造网供应商社区",
                  members=100000, activity_level="medium", relevance_score=75,
                  tags=["B2B", "供应商", "采购"],
                  engagement_strategy="完善企业页面 + 参与采购需求响应"),
        Community("广交会云展厅", "forum", "trade", "domestic", "zh",
                  url="https://www.cantonfair.org.cn",
                  description="广交会线上社群和展商交流",
                  members=50000, activity_level="seasonal", relevance_score=85,
                  tags=["展会", "广交会", "线下对接"],
                  engagement_strategy="展会前集中参与 + 展后跟进"),
    ]

    # 国际社群模板
    INTERNATIONAL_COMMUNITIES = [
        Community("LinkedIn - Construction & Engineering Group", "linkedin", "construction", "international", "en",
                  url="https://www.linkedin.com/groups/36792/",  # Civil                   url="https://www.linkedin.com/groups/36792/"  # Civil # Civil url="https://linkedin.com/groups/12345" Structural Engineering Structural Engineering Professionals, Structural Engineering Professionals
                  description="Global construction professionals group",
                  members=500000, activity_level="high", relevance_score=90,
                  tags=["construction", "engineering", "modular", "steel"],
                  engagement_strategy="每周分享项目案例 + 参与技术讨论"),
        Community("Facebook - Global Prefab Housing", "facebook", "prefab", "international", "en",
                  url="https://facebook.com/groups/prefabhousing",
                  description="International prefab and modular construction community",
                  members=80000, activity_level="high", relevance_score=95,
                  tags=["prefab", "modular", "container house"],
                  engagement_strategy="分享成功案例 + 产品照片 + 回答技术问题"),
        Community("Facebook - Steel Structure Buyers & Importers", "facebook", "steel", "international", "en",
                  url="https://www.facebook.com/search/groups/?q=steel+structure+export", description="Global steel structure procurement group",
                  members=15000, activity_level="high", relevance_score=95,
                  tags=["steel", "import", "buyers"],
                  engagement_strategy="主动回应采购需求 + 分享工厂资质"),
        Community("Reddit r/importers", "reddit", "trade", "international", "en",
                  url="https://reddit.com/r/importers",
                  description="Global importers community",
                  members=50000, activity_level="medium", relevance_score=80,
                  tags=["import", "supply chain", "logistics"],
                  engagement_strategy="回答 sourcing 问题 + 分享中国工厂经验"),
        Community("Reddit r/construction", "reddit", "construction", "international", "en",
                  url="https://reddit.com/r/construction",
                  description="Construction industry discussion",
                  members=200000, activity_level="high", relevance_score=75,
                  tags=["construction", "materials", "methods"],
                  engagement_strategy="分享钢结构/预制建筑技术观点"),
        Community("Alibaba Trade Forums", "forum", "trade", "international", "en",
                  url="https://tradeforum.alibaba.com",
                  description="Alibaba global trade community",
                  members=1000000, activity_level="high", relevance_score=85,
                  tags=["Alibaba", "B2B", "sourcing"],
                  engagement_strategy="回答采购商问题 + 完善Gold Supplier页面"),
        Community("TradeKey Community", "forum", "trade", "international", "en",
                  url="https://www.tradekey.com/forum",
                  description="Global B2B trade community",
                  members=200000, activity_level="medium", relevance_score=70,
                  tags=["B2B", "sourcing", "leads"],
                  engagement_strategy="发布产品信息 + 回应采购需求"),
        Community("Discord - Construction Tech", "discord", "construction", "international", "en",
                  url="https://discord.gg/invite/construction", description="Construction technology discord server（搜disboard.org）",
                  members=10000, activity_level="medium", relevance_score=65,
                  tags=["construction", "tech", "innovation"],
                  engagement_strategy="参与技术讨论 + 分享行业新闻"),
        Community("WhatsApp - Global Trade Groups", "whatsapp", "trade", "international", "en",
                  url="https://chat.whatsapp.com/", description="WhatsApp trade groups（通过Alibaba群组/Facebook获取邀请）",
                  members=500, activity_level="high", relevance_score=85,
                  tags=["trade", "B2B", "leads"],
                  engagement_strategy="每日发送产品信息 + 回应询价"),
        Community("Telegram - Construction Materials", "telegram", "construction", "international", "en",
                  url="https://t.me/s/construction_news", description="Telegram construction materials channels（搜t.me的频道目录）",
                  members=3000, activity_level="medium", relevance_score=75,
                  tags=["construction", "materials", "pricing"],
                  engagement_strategy="发布价格信息 + 参与行情讨论"),
    ]

    @classmethod
    def get_all(cls) -> list[Community]:
        return cls.DOMESTIC_COMMUNITIES + cls.INTERNATIONAL_COMMUNITIES

    @classmethod
    def filter(cls, region: str = "", platform: str = "",
               category: str = "", min_relevance: int = 70) -> list[Community]:
        """筛选社群"""
        results = cls.get_all()
        if region:
            results = [c for c in results if c.region == region]
        if platform:
            results = [c for c in results if c.platform == platform]
        if category:
            results = [c for c in results if c.category == category]
        results = [c for c in results if c.relevance_score >= min_relevance]
        return sorted(results, key=lambda c: -c.relevance_score)


# ═══════════════════════════════════════════════
# 社群引擎
# ═══════════════════════════════════════════════

class CommunityEngagement:
    """跨境贸易社群参与引擎"""

    def __init__(self):
        self.participation_log = []
        self._load_log()

    def _load_log(self):
        log_file = DATA_DIR / "engagement_log.json"
        if log_file.exists():
            try:
                self.participation_log = json.loads(log_file.read_text())
            except (json.JSONDecodeError, FileNotFoundError):
                self.participation_log = []

    def _save_log(self):
        log_file = DATA_DIR / "engagement_log.json"
        log_file.write_text(json.dumps(self.participation_log, indent=2, ensure_ascii=False))

    def discover(self, product: str = "", market: str = "",
                 only_high_relevance: bool = True,
                 include_domestic: bool = True,
                 include_international: bool = True) -> dict:
        """
        发现相关社群。
        
        Args:
            product: 产品关键词（用于匹配社群标签）
            market: 目标市场
            only_high_relevance: 只返回高相关度（>80）
            include_domestic: 包含国内社群
            include_international: 包含国际社群
        
        Returns:
            按平台分组的社群列表
        """
        all_communities = CommunityDatabase.get_all()

        # 按区域筛选
        if not include_domestic:
            all_communities = [c for c in all_communities if c.region != "domestic"]
        if not include_international:
            all_communities = [c for c in all_communities if c.region == "domestic"]

        # 按产品关键词匹配
        if product:
            kw = product.lower()
            all_communities = [
                c for c in all_communities
                if any(kw in tag.lower() for tag in c.tags)
                or kw in c.name.lower()
                or kw in c.description.lower()
            ]

        # 按相关度筛选
        if only_high_relevance:
            all_communities = [c for c in all_communities if c.relevance_score >= 80]

        # 按平台分组
        groups = {}
        for c in all_communities:
            platform_key = c.platform
            if platform_key not in groups:
                groups[platform_key] = {"label": _platform_label(platform_key), "communities": []}
            groups[platform_key]["communities"].append(c.__dict__)

        return {
            "total": len(all_communities),
            "platforms": len(groups),
            "groups": groups,
            "query": {"product": product, "market": market},
        }

    def create_engagement_plan(self, product: str, market: str,
                               top_n: int = 5) -> dict:
        """
        创建参与计划。
        
        返回优先级最高的 N 个社群 + 参与策略。
        """
        communities = CommunityDatabase.get_all()

        # 按产品匹配度排序
        scored = []
        for c in communities:
            score = c.relevance_score
            if product:
                kw = product.lower()
                tag_match = sum(1 for tag in c.tags if kw in tag.lower())
                name_match = 10 if kw in c.name.lower() else 0
                desc_match = 5 if kw in c.description.lower() else 0
                score += tag_match * 5 + name_match + desc_match
            scored.append((score, c))

        scored.sort(key=lambda x: -x[0])
        top = scored[:top_n]

        plan = {
            "product": product,
            "market": market,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_available": len(communities),
            "recommended": [],
        }

        for score, c in top:
            plan["recommended"].append({
                "name": c.name,
                "platform": c.platform,
                "platform_label": _platform_label(c.platform),
                "region": c.region,
                "relevance_score": score,
                "members": c.members,
                "activity": c.activity_level,
                "strategy": c.engagement_strategy,
                "weekly_actions": self._generate_weekly_actions(c),
            })

        return plan

    def _generate_weekly_actions(self, community: Community) -> list:
        """生成每周参与动作"""
        actions = []
        base = {
            "facebook": [
                "周一: 分享行业新闻或产品案例（图文帖）",
                "周三: 回复群组成员的问题（建立专家形象）",
                "周五: 发起话题讨论（引导互动）",
            ],
            "linkedin": [
                "周二: 发表行业洞察长文（500+字）",
                "周四: 参与热门讨论（评论优质帖子）",
                "分享公司/工厂最新动态（照片+文字）",
            ],
            "reddit": [
                "每周回答 3-5 个 sourcing/import 相关问题",
                "每周发布 1 篇行业洞察（非广告）",
                "参与 AMA 或行业话题讨论",
            ],
            "forum": [
                "每日签到，保持活跃度",
                "每周回答 5 个专业问题",
                "每月发布 1 篇经验分享帖",
            ],
            "wechat": [
                "每日分享行业资讯 1-2 条",
                "积极回应群友询价和问题",
                "每周发起一个话题讨论",
            ],
            "qq": [
                "每周参与技术讨论 2-3 次",
                "分享行业资料和标准文件",
                "协助解答技术问题",
            ],
            "zhihu": [
                "每周回答 2 个高质量问题",
                "每月发布 1 篇专栏长文",
                "参与行业圆桌讨论",
            ],
            "xiaohongshu": [
                "每周发布 2-3 条图文/短视频",
                "内容方向: 工厂日常/产品展示",
                "话题标签: #外贸 #跨境 #工厂",
            ],
            "discord": [
                "每周参与 2-3 次技术讨论",
                "分享行业新闻链接",
                "建立人脉",
            ],
            "telegram": [
                "每日查看采购/询价信息",
                "及时回应报价请求",
                "分享价格行情",
            ],
            "whatsapp": [
                "每日发送产品信息至目标群组",
                "及时回应询价和样品请求",
                "维护群内人脉关系",
            ],
        }
        return base.get(community.platform, ["加入社群", "观察了解", "逐步参与"])

    def log_participation(self, community_name: str, action: str,
                          result: str = "", notes: str = ""):
        """记录一次参与"""
        entry = {
            "community": community_name,
            "action": action,
            "result": result,
            "notes": notes,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.participation_log.append(entry)
        self._save_log()
        logger.info(f"📝 记录参与: {community_name} - {action}")

    def get_stats(self) -> dict:
        """获取参与统计"""
        total = len(self.participation_log)
        by_platform = {}
        for entry in self.participation_log:
            platform = entry.get("community", "unknown")
            if platform not in by_platform:
                by_platform[platform] = 0
            by_platform[platform] += 1

        return {
            "total_engagements": total,
            "by_community": by_platform,
            "recent": self.participation_log[-10:] if self.participation_log else [],
        }


# ═══════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════

def _platform_label(platform: str) -> str:
    labels = {
        "wechat": "微信行业群",
        "qq": "QQ行业群",
        "zhihu": "知乎",
        "xiaohongshu": "小红书",
        "forum": "行业论坛",
        "linkedin": "LinkedIn Groups",
        "facebook": "Facebook Groups",
        "reddit": "Reddit",
        "discord": "Discord",
        "telegram": "Telegram",
        "whatsapp": "WhatsApp",
        "slack": "Slack",
    }
    return labels.get(platform, platform)


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    eng = CommunityEngagement()

    if "--discover" in sys.argv:
        idx = sys.argv.index("--discover")
        product = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        result = eng.discover(product=product, only_high_relevance=True)
        print(f"🔍 发现 {result['total']} 个相关社群（{result['platforms']} 个平台）")
        print()
        for platform, group in result["groups"].items():
            print(f"── {group['label']} ──")
            for c in group["communities"]:
                stars = "⭐" * (c["relevance_score"] // 20)
                print(f"  {stars} {c['name']}")
                print(f"     成员: {c['members']:,} | 活跃: {c['activity_level']} | {c['region']}")
                print(f"     策略: {c['engagement_strategy'][:60]}...")
                print()

    elif "--plan" in sys.argv:
        idx = sys.argv.index("--plan")
        product = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "钢结构"
        market = sys.argv[idx + 2] if idx + 2 < len(sys.argv) else "Australia"
        plan = eng.create_engagement_plan(product, market, top_n=5)
        print(f"📋 参与计划: {plan['product']} → {plan['market']}")
        print(f"   候选社群: {plan['total_available']} 个")
        print()
        for i, rec in enumerate(plan["recommended"]):
            print(f"  {i+1}. {rec['name']} ({rec['platform_label']})")
            print(f"     相关度: {rec['relevance_score']}/100 | 成员: {rec['members']:,}")
            print(f"     策略: {rec['strategy']}")
            print()

    elif "--log" in sys.argv and len(sys.argv) > 2:
        eng.log_participation(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "查看",
                              notes="CLI 记录")
        print("✅ 已记录")
        print(json.dumps(eng.get_stats(), indent=2, ensure_ascii=False))

    else:
        print("太一 · 跨境贸易社群参与引擎 v1.0")
        print()
        print("用法:")
        print("  --discover <产品>     发现相关社群")
        print("  --plan <产品> <市场>  生成参与计划")
        print("  --log <社群> <动作>   记录参与")
        print()
        print("示例:")
        print("  python3 core.py --discover 钢结构")
        print("  python3 core.py --plan '折叠房屋' Australia")
        print("  python3 core.py --log '福步外贸论坛' '分享行业报告'")