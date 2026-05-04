#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Earned Media Tracker - Earned Media 管道管理
版本：v1.0 (跨境贸易 Agent v8.2)
创建：2026-04-20 21:10
功能：Earned Media 机会发现 + 追踪 + 效果评估

基于 Pranjal Aggarwal (arXiv) 研究:
- AI 强烈偏好 earned media（70-90% 引用来自第三方）
- 最高杠杆点：.edu/.gov/权威媒体背书
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import Enum


class MediaType(Enum):
    """媒体类型"""
    NEWS = "news"  # 新闻媒体
    BLOG = "blog"  # 行业博客
    ACADEMIC = "academic"  # 学术 (.edu)
    GOVERNMENT = "government"  # 政府 (.gov)
    INFLUENCER = "influencer"  # 意见领袖
    FORUM = "forum"  # 论坛/社区
    PODCAST = "podcast"  # 播客
    VIDEO = "video"  # 视频 (YouTube/B 站)
    REVIEW_SITE = "review_site"  # 评测网站


class OutreachStatus(Enum):
    """触达状态"""
    IDENTIFIED = "identified"  # 已识别
    RESEARCHING = "researching"  # 调研中
    CONTACTED = "contacted"  # 已联系
    RESPONDED = "responded"  # 已回复
    NEGOTIATING = "negotiating"  # 协商中
    PUBLISHED = "published"  # 已发布
    TRACKING = "tracking"  # 追踪效果


@dataclass
class MediaOpportunity:
    """媒体机会"""
    id: str
    name: str
    type: str
    url: str
    domain_authority: int  # 域名权威 (0-100)
    trust_score: int  # 信任分数 (0-100)
    audience_size: Optional[int]  # 受众规模
    geo_focus: List[str]  # 地理覆盖
    topics: List[str]  # 覆盖主题
    contact_info: Optional[str]  # 联系信息
    notes: str = ""
    priority_score: float = 0.0  # 优先级评分
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        # 计算优先级评分
        self.priority_score = self._calculate_priority()
    
    def _calculate_priority(self) -> float:
        """计算优先级评分"""
        # 基础分：域名权威 + 信任分数
        score = (self.domain_authority * 0.4 + self.trust_score * 0.4)
        
        # 类型加成
        type_bonus = {
            MediaType.ACADEMIC.value: 15,
            MediaType.GOVERNMENT.value: 15,
            MediaType.NEWS.value: 10,
            MediaType.REVIEW_SITE.value: 10,
            MediaType.INFLUENCER.value: 8,
            MediaType.BLOG.value: 5,
            MediaType.PODCAST.value: 5,
            MediaType.VIDEO.value: 5,
            MediaType.FORUM.value: 3,
        }
        score += type_bonus.get(self.type, 0)
        
        # 地理匹配加成
        # TODO: 根据目标市场动态计算
        
        return min(score, 100)


@dataclass
class OutreachCampaign:
    """外展活动"""
    id: str
    opportunity_id: str
    opportunity_name: str
    status: str
    outreach_date: Optional[str] = None
    response_date: Optional[str] = None
    publish_date: Optional[str] = None
    content_type: Optional[str] = None  # guest_post/interview/mention/review
    content_url: Optional[str] = None
    cost: Optional[float] = None  # 成本（如有）
    results: Dict = field(default_factory=dict)  # 效果数据
    notes: str = ""
    
    def __post_init__(self):
        if not self.id:
            self.id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


@dataclass
class EarnedMediaReport:
    """Earned Media 报告"""
    brand: str
    report_date: str
    total_opportunities: int
    by_type: Dict[str, int]  # 按类型统计
    by_status: Dict[str, int]  # 按状态统计
    high_priority_count: int  # 高优先级数量
    active_campaigns: int  # 进行中活动
    published_pieces: int  # 已发布内容
    total_reach: int  # 总覆盖
    average_domain_authority: float  # 平均 DA
    recommendations: List[str]


class EarnedMediaTracker:
    """Earned Media 追踪器"""
    
    # 高信任域名类型（基于专家研究）
    HIGH_TRUST_DOMAINS = [
        ".edu", ".gov", ".ac.uk", ".gov.uk",
        "forbes.com", "bloomberg.com", "reuters.com",
        "techcrunch.com", "wired.com", "theverge.com",
    ]
    
    # 跨境贸易相关媒体（示例）
    TRADE_MEDIA = {
        "global": [
            "ecommercenews.eu", "digitalcommerce360.com",
            "retaildive.com", "supplychaindive.com",
        ],
        "china": [
            "rainnews.com", "crossborder.ninja",
            "AMZ123.com", "dianbaowang.com",
        ],
        "usa": [
            "practicalecommerce.com", "internetretailer.com",
        ],
    }
    
    def __init__(self, brand: str, data_dir: Optional[str] = None):
        """
        初始化追踪器
        
        Args:
            brand: 品牌名称
            data_dir: 数据存储目录
        """
        self.brand = brand
        self.data_dir = Path(data_dir) if data_dir else Path.cwd() / "earned_media_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.opportunities: List[MediaOpportunity] = []
        self.campaigns: List[OutreachCampaign] = []
        
        # 加载已有数据
        self._load_data()
    
    def _load_data(self):
        """加载已有数据"""
        opp_file = self.data_dir / "opportunities.json"
        camp_file = self.data_dir / "campaigns.json"
        
        if opp_file.exists():
            with open(opp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.opportunities = [
                    MediaOpportunity(**item) for item in data
                ]
            print(f"✅ 加载 {len(self.opportunities)} 个媒体机会")
        
        if camp_file.exists():
            with open(camp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.campaigns = [
                    OutreachCampaign(**item) for item in data
                ]
            print(f"✅ 加载 {len(self.campaigns)} 个外展活动")
    
    def save_data(self):
        """保存数据"""
        opp_file = self.data_dir / "opportunities.json"
        camp_file = self.data_dir / "campaigns.json"
        
        with open(opp_file, 'w', encoding='utf-8') as f:
            json.dump(
                [asdict(opp) for opp in self.opportunities],
                f, indent=2, ensure_ascii=False
            )
        
        with open(camp_file, 'w', encoding='utf-8') as f:
            json.dump(
                [asdict(camp) for camp in self.campaigns],
                f, indent=2, ensure_ascii=False
            )
        
        print(f"💾 数据已保存至 {self.data_dir}")
    
    def add_opportunity(
        self,
        name: str,
        type: str,
        url: str,
        domain_authority: int,
        trust_score: int,
        geo_focus: List[str],
        topics: List[str],
        contact_info: Optional[str] = None,
        notes: str = ""
    ) -> MediaOpportunity:
        """
        添加媒体机会
        
        Args:
            name: 媒体名称
            type: 媒体类型 (MediaType 枚举值)
            url: URL
            domain_authority: 域名权威 (0-100)
            trust_score: 信任分数 (0-100)
            geo_focus: 地理覆盖
            topics: 覆盖主题
            contact_info: 联系信息
            notes: 备注
            
        Returns:
            MediaOpportunity: 创建的媒体机会
        """
        opportunity = MediaOpportunity(
            id=f"opp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=name,
            type=type,
            url=url,
            domain_authority=domain_authority,
            trust_score=trust_score,
            audience_size=None,
            geo_focus=geo_focus,
            topics=topics,
            contact_info=contact_info,
            notes=notes,
        )
        
        self.opportunities.append(opportunity)
        self.save_data()
        
        print(f"✅ 添加媒体机会：{name} (优先级：{opportunity.priority_score:.1f})")
        return opportunity
    
    def discover_opportunities(
        self,
        target_markets: List[str],
        industry: str = "cross_border_trade"
    ) -> List[MediaOpportunity]:
        """
        发现媒体机会
        
        Args:
            target_markets: 目标市场
            industry: 行业
            
        Returns:
            List[MediaOpportunity]: 发现的媒体机会
        """
        print(f"\n🔍 发现媒体机会：{target_markets}")
        
        new_opportunities = []
        
        # 基于预定义列表发现（实际可集成 API）
        for market in target_markets:
            media_list = self.TRADE_MEDIA.get(market, self.TRADE_MEDIA["global"])
            
            for media_url in media_list:
                # 检查是否已存在
                if any(opp.url == media_url for opp in self.opportunities):
                    continue
                
                # 创建机会
                opp = self.add_opportunity(
                    name=media_url.split('.')[0].title(),
                    type=MediaType.BLOG.value,
                    url=f"https://{media_url}",
                    domain_authority=50,  # 示例值
                    trust_score=60,
                    geo_focus=[market],
                    topics=["cross_border", "ecommerce", "trade"],
                    notes=f"自动发现 - {market} 市场",
                )
                new_opportunities.append(opp)
        
        print(f"✨ 新发现 {len(new_opportunities)} 个媒体机会\n")
        return new_opportunities
    
    def create_campaign(
        self,
        opportunity_id: str,
        content_type: str = "guest_post",
        notes: str = ""
    ) -> OutreachCampaign:
        """
        创建外展活动
        
        Args:
            opportunity_id: 媒体机会 ID
            content_type: 内容类型
            notes: 备注
            
        Returns:
            OutreachCampaign: 创建的外展活动
        """
        # 查找机会
        opp = next(
            (o for o in self.opportunities if o.id == opportunity_id),
            None
        )
        
        if not opp:
            raise ValueError(f"未找到机会：{opportunity_id}")
        
        campaign = OutreachCampaign(
            id=f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            opportunity_id=opportunity_id,
            opportunity_name=opp.name,
            status=OutreachStatus.IDENTIFIED.value,
            content_type=content_type,
            notes=notes,
        )
        
        self.campaigns.append(campaign)
        self.save_data()
        
        print(f"🎯 创建外展活动：{opp.name} - {content_type}")
        return campaign
    
    def update_campaign_status(
        self,
        campaign_id: str,
        status: str,
        notes: str = ""
    ):
        """更新活动状态"""
        campaign = next(
            (c for c in self.campaigns if c.id == campaign_id),
            None
        )
        
        if not campaign:
            raise ValueError(f"未找到活动：{campaign_id}")
        
        campaign.status = status
        if notes:
            campaign.notes += f"\n[{datetime.now().isoformat()}] {notes}"
        
        # 状态变更时更新时间戳
        if status == OutreachStatus.CONTACTED.value:
            campaign.outreach_date = datetime.now().isoformat()
        elif status == OutreachStatus.RESPONDED.value:
            campaign.response_date = datetime.now().isoformat()
        elif status == OutreachStatus.PUBLISHED.value:
            campaign.publish_date = datetime.now().isoformat()
        
        self.save_data()
        print(f"✅ 更新活动状态：{campaign.opportunity_name} → {status}")
    
    def generate_report(self) -> EarnedMediaReport:
        """生成报告"""
        # 按类型统计
        by_type = {}
        for opp in self.opportunities:
            by_type[opp.type] = by_type.get(opp.type, 0) + 1
        
        # 按状态统计
        by_status = {}
        for camp in self.campaigns:
            by_status[camp.status] = by_status.get(camp.status, 0) + 1
        
        # 高优先级数量
        high_priority = sum(
            1 for opp in self.opportunities if opp.priority_score >= 70
        )
        
        # 已发布内容
        published = sum(
            1 for camp in self.campaigns
            if camp.status == OutreachStatus.PUBLISHED.value
        )
        
        # 平均 DA
        avg_da = (
            sum(opp.domain_authority for opp in self.opportunities) /
            len(self.opportunities) if self.opportunities else 0
        )
        
        # 基于专家共识的建议
        recommendations = [
            "📰 优先联系 .edu/.gov 域名（AI 最信任）",
            "🎯 聚焦高 DA (>60) 行业媒体",
            "🌐 每个目标市场至少 3 个本地媒体",
            "📝 准备高质量客座文章提案",
            "🤝 建立长期关系而非一次性合作",
            "📊 追踪每篇发布内容的 AI 引用情况",
            "⏰ 持续产出，每月至少 2-4 篇新内容",
        ]
        
        report = EarnedMediaReport(
            brand=self.brand,
            report_date=datetime.now().isoformat(),
            total_opportunities=len(self.opportunities),
            by_type=by_type,
            by_status=by_status,
            high_priority_count=high_priority,
            active_campaigns=len([
                c for c in self.campaigns
                if c.status not in [OutreachStatus.PUBLISHED.value]
            ]),
            published_pieces=published,
            total_reach=0,  # TODO: 计算
            average_domain_authority=avg_da,
            recommendations=recommendations,
        )
        
        return report
    
    def print_summary(self, report: EarnedMediaReport):
        """打印摘要"""
        print("\n" + "=" * 60)
        print(f"📰 Earned Media 报告 - {self.brand}")
        print("=" * 60)
        print(f"报告日期：{report.report_date}")
        print(f"总机会数：{report.total_opportunities}")
        print(f"高优先级：{report.high_priority_count}")
        print(f"进行中活动：{report.active_campaigns}")
        print(f"已发布：{report.published_pieces}")
        print(f"平均 DA: {report.average_domain_authority:.1f}")
        print(f"\n按类型:")
        for type_, count in report.by_type.items():
            print(f"  - {type_}: {count}")
        print(f"\n按状态:")
        for status, count in report.by_status.items():
            print(f"  - {status}: {count}")
        print(f"\n建议 (Top 3):")
        for rec in report.recommendations[:3]:
            print(f"  {rec}")
        print("=" * 60 + "\n")


def main():
    """示例用法"""
    tracker = EarnedMediaTracker(brand="YourBrand")
    
    # 发现机会
    tracker.discover_opportunities(
        target_markets=["usa", "china", "global"]
    )
    
    # 生成报告
    report = tracker.generate_report()
    tracker.print_summary(report)
    
    # 保存数据
    tracker.save_data()


if __name__ == "__main__":
    main()
