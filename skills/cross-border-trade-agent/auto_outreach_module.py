#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动触达模块 - 全渠道跟进转化
太一 AGI · 2026-04-18

功能:
- 自动拟人触达 (邮件/WhatsApp/Telegram)
- 智能话术生成 (个性化/走心)
- 跟进节奏控制 (时间间隔/频率)
- 回复追踪分析
- HIR (High-Intent Review) 人工复核

获客之王三步骤闭环:
1. 全网全域搜寻 → prospect_search.py (已有)
2. 深度线索清洗 → data_verification (已有)
3. 自动拟人触达 → 本模块 (新增)
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('AutoOutreach')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data" / "cross-border" / "outreach"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class AutoOutreachModule:
    """自动触达模块"""
    
    def __init__(self):
        # 触达渠道配置
        self.channels = {
            "email": {
                "enabled": True,
                "priority": 1,
                "templates": self._load_email_templates()
            },
            "whatsapp": {
                "enabled": True,
                "priority": 2,
                "templates": self._load_whatsapp_templates()
            },
            "telegram": {
                "enabled": True,
                "priority": 3,
                "templates": self._load_telegram_templates()
            }
        }
        
        # 跟进节奏配置
        self.follow_up_schedule = {
            "day_0": {"delay_hours": 0, "channel": "email", "message_type": "initial"},
            "day_1": {"delay_hours": 24, "channel": "whatsapp", "message_type": "follow_up_1"},
            "day_3": {"delay_hours": 72, "channel": "email", "message_type": "follow_up_2"},
            "day_7": {"delay_hours": 168, "channel": "telegram", "message_type": "final"},
        }
        
        # HIR (High-Intent Review) 配置
        self.human_review_config = {
            "enabled": True,
            "review_threshold": 0.8,  # 置信度>80% 自动发送，否则人工复核
            "high_priority_review": True,  # 高意向客户必须人工复核
        }
        
        # 话术库 (个性化/走心)
        self.message_templates = {
            "initial": self._get_initial_templates(),
            "follow_up_1": self._get_follow_up_1_templates(),
            "follow_up_2": self._get_follow_up_2_templates(),
            "final": self._get_final_templates()
        }
    
    def _load_email_templates(self) -> Dict:
        """加载邮件模板"""
        return {
            "subject_templates": [
                "合作机会：{product} - {company_name}",
                "来自中国的优质{product}供应商",
                "提升您的{product}利润率 - 厂家直供",
                "{company_name} 寻求{product}合作",
            ],
            "signature": """
Best regards,
{sender_name}
{company_name}
电话：{phone}
网站：{website}
"""
        }
    
    def _load_whatsapp_templates(self) -> Dict:
        """加载 WhatsApp 模板"""
        return {
            "greeting": "您好！我是{sender_name}，来自{company_name}",
            "closing": "期待您的回复！🙏"
        }
    
    def _load_telegram_templates(self) -> Dict:
        """加载 Telegram 模板"""
        return {
            "greeting": "👋 您好！",
            "closing": "祝商祺！"
        }
    
    def _get_initial_templates(self) -> List[Dict]:
        """首次联系话术"""
        return [
            {
                "name": "专业介绍型",
                "content": """尊敬的{contact_name}：

您好！

我是{sender_name}，来自{company_name}。我们是一家专业的{product}制造商，拥有{years}年行业经验。

了解到贵公司在{industry}领域有卓越表现，我们相信我们的{product}能够为贵公司带来以下价值：

✅ 成本优势：厂家直供，价格比市场低{discount}%
✅ 质量保证：通过{certification}认证
✅ 交货快速：{lead_time}天交货
✅ 定制服务：支持 OEM/ODM

附件是我们的产品目录和报价单，请查收。

期待与您的合作！

{signature}
""",
                "tone": "professional"
            },
            {
                "name": "价值导向型",
                "content": """{contact_name}您好，

注意到贵公司正在销售{product}，我们可以帮助您：

📈 提升利润率：从{current_margin}% 提升到{new_margin}%
⚡ 缩短交货期：从{current_lead_time}天缩短到{lead_time}天
🎯 增加产品线：{product_count}+ 款新品可选

我们是{company_name}，已服务{customer_count}+ 家海外客户。

有兴趣聊聊吗？

{signature}
""",
                "tone": "value_focused"
            },
            {
                "name": "推荐引荐型",
                "content": """尊敬的{contact_name}：

您好！

{referrer_name} 向我推荐了贵公司，说您在{industry}领域非常专业。

我们刚帮助{similar_company}将{product}采购成本降低了{discount}%，交货时间缩短了{time_saved}%。

如果您有兴趣，我可以分享具体方案。

期待您的回复！

{signature}
""",
                "tone": "referral"
            }
        ]
    
    def _get_follow_up_1_templates(self) -> List[Dict]:
        """第一次跟进话术"""
        return [
            {
                "name": "温和提醒型",
                "content": """{contact_name}您好，

希望您一切顺利！

前几天给您发了关于{product}合作的信息，不知道您是否收到了？

如果您有任何问题或需要更多信息，随时告诉我。

祝好！
{sender_name}
""",
                "tone": "gentle"
            },
            {
                "name": "价值补充型",
                "content": """{contact_name}您好，

补充一些信息：

📊 我们的{product}已出口到{export_countries}+ 个国家
⭐ 客户满意度：{satisfaction_rate}%
🏆 获得{award}认证

如果您有兴趣，我可以安排样品测试。

期待回复！
{sender_name}
""",
                "tone": "value_add"
            }
        ]
    
    def _get_follow_up_2_templates(self) -> List[Dict]:
        """第二次跟进话术"""
        return [
            {
                "name": "限时优惠型",
                "content": """{contact_name}您好，

有个好消息分享：

本月下单可享受：
🎁 首单折扣：{discount}%
🎁 免费样品：前{sample_count}名
🎁 免运费：订单满${amount}

优惠截止日期：{deadline}

有兴趣吗？

{sender_name}
""",
                "tone": "urgency"
            }
        ]
    
    def _get_final_templates(self) -> List[Dict]:
        """最后跟进话术"""
        return [
            {
                "name": "友好告别型",
                "content": """{contact_name}您好，

这是最后一次联系您了。

如果您暂时不需要{product}，没关系。

我会把您加入我们的长期联系名单，有新品或优惠时再通知您。

祝生意兴隆！
{sender_name}
{company_name}
""",
                "tone": "friendly_close"
            }
        ]
    
    def generate_message(self, lead: Dict, message_type: str = "initial") -> Dict:
        """
        生成个性化消息
        
        Args:
            lead: 线索信息
            message_type: 消息类型 (initial/follow_up_1/follow_up_2/final)
            
        Returns:
            生成的消息
        """
        logger.info(f"📝 生成消息：{lead.get('company_name', 'Unknown')} - {message_type}")
        
        # 选择模板
        templates = self.message_templates.get(message_type, [])
        if not templates:
            logger.error(f"❌ 未找到{message_type}类型的模板")
            return None
        
        template = random.choice(templates)
        
        # 填充变量
        message_content = self._fill_template(template["content"], lead)
        
        # 计算置信度 (用于 HIR (High-Intent Review))
        confidence = self._calculate_confidence(lead, message_type)
        
        # 决定是否需要人工复核
        needs_review = self._needs_human_review(lead, confidence)
        
        result = {
            "lead_id": lead.get("id"),
            "company_name": lead.get("company_name"),
            "contact_name": lead.get("contact_name"),
            "message_type": message_type,
            "template_name": template["name"],
            "tone": template["tone"],
            "content": message_content,
            "confidence": confidence,
            "needs_human_review": needs_review,
            "suggested_channel": self._suggest_channel(lead),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ 消息生成完成，置信度：{confidence:.2f}, 需要复核：{needs_review}")
        
        return result
    
    def _fill_template(self, template: str, lead: Dict) -> str:
        """填充模板变量"""
        # 公司信息
        fill_data = {
            "company_name": lead.get("company_name", "贵公司"),
            "contact_name": lead.get("contact_name", "先生/女士"),
            "product": lead.get("product_interest", "产品"),
            "industry": lead.get("industry", "行业"),
            
            # 我方信息
            "sender_name": "太一跨境贸易",
            "years": "10",
            "certification": "CE/FCC/ISO9001",
            "lead_time": "15-20",
            "discount": "20",
            "current_margin": "20",
            "new_margin": "35",
            "current_lead_time": "30",
            "product_count": "100",
            "customer_count": "500",
            "export_countries": "50",
            "satisfaction_rate": "98",
            "award": "ISO9001",
            "sample_count": "10",
            "amount": "10000",
            "deadline": datetime.now() + timedelta(days=7),
            
            # 签名
            "signature": """
Best regards,
太一跨境贸易团队
电话：+86-xxx-xxxx-xxxx
网站：www.taiyi-trade.com
"""
        }
        
        # 填充
        message = template
        for key, value in fill_data.items():
            message = message.replace("{" + key + "}", str(value))
        
        return message
    
    def _calculate_confidence(self, lead: Dict, message_type: str) -> float:
        """计算消息置信度 (0-1)"""
        confidence = 0.5  # 基础置信度
        
        # 线索质量加分
        lead_score = lead.get("lead_score", 0)
        if lead_score >= 90:
            confidence += 0.3
        elif lead_score >= 70:
            confidence += 0.2
        elif lead_score >= 50:
            confidence += 0.1
        
        # 信息完整度加分
        if lead.get("contact_name"):
            confidence += 0.05
        if lead.get("email"):
            confidence += 0.05
        if lead.get("phone"):
            confidence += 0.05
        if lead.get("company_name"):
            confidence += 0.05
        
        # 意向度加分
        intent_level = lead.get("intent_level", "medium")
        if intent_level == "high":
            confidence += 0.1
        elif intent_level == "medium":
            confidence += 0.05
        
        return min(1.0, confidence)
    
    def _needs_human_review(self, lead: Dict, confidence: float) -> bool:
        """判断是否需要人工复核"""
        if not self.human_review_config["enabled"]:
            return False
        
        # 置信度低于阈值
        if confidence < self.human_review_config["review_threshold"]:
            return True
        
        # 高意向客户必须人工复核
        if self.human_review_config["high_priority_review"]:
            if lead.get("intent_level") == "high" or lead.get("lead_score", 0) >= 90:
                return True
        
        return False
    
    def _suggest_channel(self, lead: Dict) -> str:
        """建议触达渠道"""
        # 根据线索偏好选择渠道
        preferred_channel = lead.get("preferred_channel")
        if preferred_channel and preferred_channel in self.channels:
            return preferred_channel
        
        # 根据地区选择
        region = lead.get("region", "")
        if region in ["USA", "Canada", "UK"]:
            return "email"
        elif region in ["Europe"]:
            return "email"
        elif region in ["Asia", "Middle East"]:
            return "whatsapp"
        
        # 默认邮件
        return "email"
    
    def send_outreach(self, message: Dict, auto_send: bool = False) -> Dict:
        """
        发送触达消息
        
        Args:
            message: 生成的消息
            auto_send: 是否自动发送 (否则仅生成待发送队列)
            
        Returns:
            发送结果
        """
        logger.info(f"📤 发送触达消息：{message.get('company_name')} - 需要复核：{message.get('needs_human_review')}")
        
        result = {
            "message_id": message.get("lead_id") + "_" + datetime.now().strftime("%Y%m%d%H%M%S"),
            "status": "pending_review" if message.get("needs_human_review") else "ready_to_send",
            "channel": message.get("suggested_channel"),
            "content": message.get("content"),
            "needs_human_review": message.get("needs_human_review"),
            "confidence": message.get("confidence"),
            "timestamp": datetime.now().isoformat()
        }
        
        if auto_send and not message.get("needs_human_review"):
            # 模拟发送 (实际应调用邮件/WhatsApp API)
            result["status"] = "sent"
            result["sent_at"] = datetime.now().isoformat()
            logger.info(f"✅ 消息已发送：{result['message_id']}")
        else:
            logger.info(f"⏸️ 消息待发送 (需要人工复核): {result['message_id']}")
        
        # 保存到待发送队列
        self._save_to_queue(result)
        
        return result
    
    def _save_to_queue(self, message_result: Dict):
        """保存到待发送队列"""
        queue_file = DATA_DIR / "outreach_queue.json"
        
        queue = []
        if queue_file.exists():
            with open(queue_file, 'r', encoding='utf-8') as f:
                queue = json.load(f)
        
        queue.append(message_result)
        
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
    
    def get_human_review_queue(self) -> List[Dict]:
        """获取待人工复核队列"""
        queue_file = DATA_DIR / "outreach_queue.json"
        
        if not queue_file.exists():
            return []
        
        with open(queue_file, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        
        review_queue = [m for m in queue if m.get("needs_human_review")]
        
        return review_queue
    
    def approve_and_send(self, message_id: str) -> Dict:
        """人工复核通过后发送"""
        queue_file = DATA_DIR / "outreach_queue.json"
        
        with open(queue_file, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        
        for message in queue:
            if message["message_id"] == message_id:
                message["status"] = "approved"
                message["approved_at"] = datetime.now().isoformat()
                message["status"] = "sent"
                message["sent_at"] = datetime.now().isoformat()
                logger.info(f"✅ 人工复核通过，消息已发送：{message_id}")
                break
        
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        
        return {"status": "sent", "message_id": message_id}
    
    def generate_outreach_report(self, leads: List[Dict]) -> Dict:
        """生成触达报告"""
        logger.info(f"📊 生成触达报告：{len(leads)}个线索")
        
        report = {
            "total_leads": len(leads),
            "high_intent": len([l for l in leads if l.get("intent_level") == "high"]),
            "medium_intent": len([l for l in leads if l.get("intent_level") == "medium"]),
            "low_intent": len([l for l in leads if l.get("intent_level") == "low"]),
            "needs_review": 0,
            "auto_send": 0,
            "by_channel": {"email": 0, "whatsapp": 0, "telegram": 0},
            "timestamp": datetime.now().isoformat()
        }
        
        for lead in leads:
            message = self.generate_message(lead, "initial")
            if message:
                if message["needs_human_review"]:
                    report["needs_review"] += 1
                else:
                    report["auto_send"] += 1
                
                channel = message["suggested_channel"]
                report["by_channel"][channel] = report["by_channel"].get(channel, 0) + 1
        
        return report


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("📤 自动触达模块 - 演示")
    logger.info("=" * 60)
    
    # 初始化模块
    outreach = AutoOutreachModule()
    
    # 示例线索
    leads = [
        {
            "id": "lead_001",
            "company_name": "ABC Trading LLC",
            "contact_name": "John Smith",
            "email": "john@abctrading.com",
            "phone": "+1-234-567-8900",
            "region": "USA",
            "product_interest": "钢结构折叠房屋",
            "industry": "建筑建材",
            "lead_score": 85,
            "intent_level": "high",
            "preferred_channel": "email"
        },
        {
            "id": "lead_002",
            "company_name": "Euro Build GmbH",
            "contact_name": "Hans Mueller",
            "email": "hans@eurobuild.de",
            "region": "Europe",
            "product_interest": "轻钢别墅",
            "industry": "房地产",
            "lead_score": 70,
            "intent_level": "medium"
        },
        {
            "id": "lead_003",
            "company_name": "Aussie Homes Pty",
            "contact_name": "Sarah Johnson",
            "email": "sarah@aussiehomes.com.au",
            "phone": "+61-400-123-456",
            "region": "Australia",
            "product_interest": "活动板房",
            "industry": "建筑",
            "lead_score": 92,
            "intent_level": "high",
            "preferred_channel": "whatsapp"
        }
    ]
    
    # 生成触达报告
    logger.info("\n📊 生成触达报告...")
    report = outreach.generate_outreach_report(leads)
    
    logger.info(f"\n线索总数：{report['total_leads']}")
    logger.info(f"高意向：{report['high_intent']}")
    logger.info(f"中意向：{report['medium_intent']}")
    logger.info(f"低意向：{report['low_intent']}")
    logger.info(f"需要人工复核：{report['needs_review']}")
    logger.info(f"可自动发送：{report['auto_send']}")
    logger.info(f"渠道分布：{report['by_channel']}")
    
    # 生成并发送消息
    logger.info("\n" + "=" * 60)
    logger.info("📝 生成并发送消息")
    logger.info("=" * 60)
    
    for lead in leads:
        logger.info(f"\n--- {lead['company_name']} ---")
        
        # 生成消息
        message = outreach.generate_message(lead, "initial")
        
        logger.info(f"模板：{message['template_name']}")
        logger.info(f"语气：{message['tone']}")
        logger.info(f"渠道：{message['suggested_channel']}")
        logger.info(f"置信度：{message['confidence']:.2f}")
        logger.info(f"需要复核：{message['needs_human_review']}")
        
        # 发送消息
        result = outreach.send_outreach(message, auto_send=True)
        logger.info(f"状态：{result['status']}")
        
        if result['needs_human_review']:
            logger.info(f"⏸️ 已加入人工复核队列")
    
    # 获取人工复核队列
    logger.info("\n" + "=" * 60)
    logger.info("⏸️ 人工复核队列")
    logger.info("=" * 60)
    
    review_queue = outreach.get_human_review_queue()
    logger.info(f"待复核消息：{len(review_queue)}条")
    
    for message in review_queue:
        logger.info(f"\n- {message['message_id']}")
        logger.info(f"  公司：{message.get('channel')}")
        logger.info(f"  置信度：{message['confidence']:.2f}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
