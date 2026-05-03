#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAQ 内容库模块 - Top 20 客户常问问题
太一 AGI · 2026-04-19 19:46

功能:
- 整理 Top 20 客户常问问题
- 生成 FAQ 内容 (帖子/短视频脚本)
- 问答形式发布
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('FAQContentLibrary')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
FAQ_DIR = WORKSPACE / "data" / "cross-border" / "faq"
FAQ_DIR.mkdir(parents=True, exist_ok=True)


class FAQContentLibrary:
    """FAQ 内容库模块"""
    
    TOP_20_QUESTIONS = [
        {"category": "MOQ", "question": "最小起订量 (MOQ) 是多少？"},
        {"category": "MOQ", "question": "可以混批吗？"},
        {"category": "Price", "question": "价格是多少？有折扣吗？"},
        {"category": "Price", "question": "FOB/CIF 价格分别是多少？"},
        {"category": "Quality", "question": "产品质量如何保证？"},
        {"category": "Quality", "question": "有质量保证期吗？多久？"},
        {"category": "Certification", "question": "有哪些认证？(CE/FCC/ISO 等)"},
        {"category": "Certification", "question": "产品符合出口标准吗？"},
        {"category": "Delivery", "question": "交货期是多久？"},
        {"category": "Delivery", "question": "可以加急生产吗？"},
        {"category": "Shipping", "question": "运费怎么算？"},
        {"category": "Shipping", "question": "支持哪些物流方式？"},
        {"category": "Payment", "question": "支持哪些付款方式？"},
        {"category": "Payment", "question": "可以账期吗？"},
        {"category": "Sample", "question": "可以提供样品吗？"},
        {"category": "Sample", "question": "样品免费吗？"},
        {"category": "Customization", "question": "支持定制吗？"},
        {"category": "Customization", "question": "定制周期多久？"},
        {"category": "AfterSales", "question": "售后政策是什么？"},
        {"category": "AfterSales", "question": "出现质量问题怎么处理？"}
    ]
    
    def __init__(self):
        self.faq_file = FAQ_DIR / "faq_content.json"
        self.faqs = self._load_faqs()
    
    def _load_faqs(self) -> Dict:
        if self.faq_file.exists():
            with open(self.faq_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"questions": [], "posts": [], "videos": []}
    
    def generate_all_faqs(self) -> List[Dict]:
        """生成全部 Top 20 FAQ 内容"""
        logger.info(f"📝 生成 Top 20 FAQ 内容...")
        
        for q in self.TOP_20_QUESTIONS:
            faq = self.generate_faq_content(q["question"], q["category"])
        
        logger.info(f"✅ 已生成{len(self.TOP_20_QUESTIONS)}个 FAQ 内容")
        return self.faqs["questions"]
    
    def generate_faq_content(self, question: str, category: str, answer_template: str = "") -> Dict:
        """生成单个 FAQ 内容"""
        answer = answer_template or self._generate_answer(question, category)
        
        faq = {
            "id": f"FAQ_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "category": category,
            "question": question,
            "answer": answer,
            "post_version": self._generate_post_version(question, answer),
            "video_script": self._generate_video_script(question, answer),
            "hashtags": self._generate_hashtags(category),
            "created_at": datetime.now().isoformat()
        }
        
        self.faqs["questions"].append(faq)
        self._save_faqs()
        logger.info(f"✅ FAQ 已生成：{question[:30]}...")
        return faq
    
    def _generate_answer(self, question: str, category: str) -> str:
        """生成答案模板"""
        answers = {
            "MOQ": "我们的 MOQ 是 [数量] 件，支持混批。首次合作可享受优惠 MOQ 政策，详情请联系销售团队。",
            "Price": "价格根据订单数量和规格而定。批量订购可享受优惠折扣。FOB/CIF 价格请提供具体目的地获取报价。",
            "Quality": "我们拥有 ISO9001 质量管理体系认证，每批产品都经过严格质检。提供 [X] 年质量保证期。",
            "Certification": "我们的产品已通过 CE、FCC、ISO9001 等多项国际认证，符合欧美出口标准。",
            "Delivery": "标准产品交货期为 [X-X] 天，定制产品 [X-X] 天。支持加急生产，详情请联系。",
            "Shipping": "支持海运、空运、快递等多种物流方式。运费根据目的地和重量计算，可提供到门服务。",
            "Payment": "支持 T/T、L/C、PayPal 等多种付款方式。长期合作客户可申请账期支持。",
            "Sample": "支持提供样品，样品费可退还。常规样品 3-5 天发出，定制样品 7-10 天。",
            "Customization": "支持 OEM/ODM 定制，包括 logo、包装、规格等。定制周期根据复杂度 10-30 天不等。",
            "AfterSales": "提供完善的售后服务，质量问题免费退换。专业技术团队 24 小时在线支持。"
        }
        return answers.get(category, "详情请联系我们的销售团队获取专业解答。")
    
    def _generate_post_version(self, question: str, answer: str) -> str:
        """生成帖子版本"""
        return f"""【客户常问】{question}

{answer}

💡 还有其他问题？欢迎私信咨询！

#外贸 #B2B #FAQ #行业知识"""
    
    def _generate_video_script(self, question: str, answer: str) -> str:
        """生成短视频脚本"""
        return f"""【短视频脚本】{question}

开场 (0-3 秒):
"经常有客户问：{question[:20]}..."

主体 (3-15 秒):
"{answer[:50]}..."

结尾 (15-30 秒):
"还有其他问题？评论区留言！"

画面建议：工厂实景/产品展示/团队工作场景"""
    
    def _generate_hashtags(self, category: str) -> List[str]:
        """生成标签"""
        base_tags = ["#外贸", "#B2B", "#FAQ"]
        category_tags = {
            "MOQ": ["#起订量", "#批发"],
            "Price": ["#价格", "#报价"],
            "Quality": ["#质量", "#品控"],
            "Certification": ["#认证", "#标准"],
            "Delivery": ["#交货期", "#物流"],
            "Shipping": ["#运输", "#货运"],
            "Payment": ["#付款", "#账期"],
            "Sample": ["#样品", "#试单"],
            "Customization": ["#定制", "#OEM"],
            "AfterSales": ["#售后", "#服务"]
        }
        return base_tags + category_tags.get(category, [])
    
    def generate_post(self, question_id: str) -> Dict:
        """生成可发布的帖子内容"""
        for faq in self.faqs["questions"]:
            if faq["id"] == question_id:
                post = {
                    "type": "post",
                    "content": faq["post_version"],
                    "hashtags": faq["hashtags"],
                    "platform": ["LinkedIn", "Facebook"]
                }
                self.faqs["posts"].append(post)
                self._save_faqs()
                return post
        return {}
    
    def generate_video(self, question_id: str) -> Dict:
        """生成可拍摄的视频脚本"""
        for faq in self.faqs["questions"]:
            if faq["id"] == question_id:
                video = {
                    "type": "video",
                    "script": faq["video_script"],
                    "duration": "30 秒",
                    "platform": ["YouTube", "TikTok", "LinkedIn"]
                }
                self.faqs["videos"].append(video)
                self._save_faqs()
                return video
        return {}
    
    def _save_faqs(self):
        with open(self.faq_file, 'w', encoding='utf-8') as f:
            json.dump(self.faqs, f, indent=2, ensure_ascii=False)
    
    def get_faqs_by_category(self, category: str) -> List[Dict]:
        """按分类获取 FAQ"""
        return [f for f in self.faqs["questions"] if f["category"] == category]


def main():
    logger.info("=" * 60)
    logger.info("❓ FAQ 内容库模块 - Top 20 客户常问问题")
    logger.info("=" * 60)
    
    library = FAQContentLibrary()
    
    # 生成全部 Top 20 FAQ
    logger.info(f"\n📝 生成 Top 20 FAQ 内容...")
    faqs = library.generate_all_faqs()
    
    logger.info(f"\n📊 FAQ 分类统计:")
    categories = {}
    for faq in faqs:
        cat = faq["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  {cat}: {count}个")
    
    logger.info(f"\n📱 示例帖子:")
    if faqs:
        logger.info(faqs[0]["post_version"])
    
    logger.info(f"\n🎬 示例视频脚本:")
    if faqs:
        logger.info(faqs[0]["video_script"])
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
