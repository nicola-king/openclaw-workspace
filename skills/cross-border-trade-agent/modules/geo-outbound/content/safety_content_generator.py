#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2B 安全感内容生成模块
太一 AGI · 2026-04-19 19:46

功能:
- 工厂实景内容生成
- 出货记录内容生成
- 客户案例见证生成
- 认证资质内容生成
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SafetyContentGenerator')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
SAFETY_DIR = WORKSPACE / "data" / "cross-border" / "safety_content"
SAFETY_DIR.mkdir(parents=True, exist_ok=True)


class SafetyContentGenerator:
    """B2B 安全感内容生成器"""
    
    def __init__(self):
        self.content_file = SAFETY_DIR / "safety_content.json"
        self.contents = self._load_contents()
    
    def _load_contents(self) -> Dict:
        if self.content_file.exists():
            with open(self.content_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"factory": [], "shipping": [], "testimonials": [], "certifications": []}
    
    def generate_factory_proof(self, factory_data: Dict) -> Dict:
        """生成工厂实景内容"""
        content = {
            "id": f"FACTORY_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": "factory_proof",
            "title": f"{factory_data.get('name', '工厂')} 实景展示",
            "content": {
                "name": factory_data.get('name'),
                "location": factory_data.get('location'),
                "area": factory_data.get('area'),
                "employees": factory_data.get('employees'),
                "production_lines": factory_data.get('production_lines'),
                "capacity": factory_data.get('capacity'),
                "images": factory_data.get('images', []),
                "description": f"位于{factory_data.get('location')}，占地面积{factory_data.get('area')}，拥有{factory_data.get('employees')}名员工，{factory_data.get('production_lines')}条生产线"
            },
            "safety_score": 95,
            "created_at": datetime.now().isoformat()
        }
        self.contents["factory"].append(content)
        self._save_contents()
        logger.info(f"✅ 工厂实景内容已生成：{content['id']}")
        return content
    
    def generate_shipping_records(self, shipping_data: Dict) -> Dict:
        """生成出货记录内容"""
        content = {
            "id": f"SHIPPING_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": "shipping_records",
            "title": f"出货记录 - {shipping_data.get('destination', '全球')}",
            "content": {
                "destination": shipping_data.get('destination'),
                "total_shipments": shipping_data.get('total_shipments'),
                "on_time_rate": shipping_data.get('on_time_rate'),
                "countries": shipping_data.get('countries'),
                "recent_shipments": shipping_data.get('recent_shipments', []),
                "description": f"已出货{shipping_data.get('total_shipments')}票，准时交付率{shipping_data.get('on_time_rate')}%，覆盖{shipping_data.get('countries')}个国家"
            },
            "safety_score": 98,
            "created_at": datetime.now().isoformat()
        }
        self.contents["shipping"].append(content)
        self._save_contents()
        logger.info(f"✅ 出货记录内容已生成：{content['id']}")
        return content
    
    def generate_customer_testimonials(self, testimonial_data: Dict) -> Dict:
        """生成客户案例见证"""
        content = {
            "id": f"TESTIMONIAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": "customer_testimonial",
            "title": f"客户见证 - {testimonial_data.get('customer_name', '匿名')}",
            "content": {
                "customer_name": testimonial_data.get('customer_name'),
                "customer_country": testimonial_data.get('customer_country'),
                "product": testimonial_data.get('product'),
                "order_value": testimonial_data.get('order_value'),
                "testimonial": testimonial_data.get('testimonial'),
                "rating": testimonial_data.get('rating', 5),
                "cooperation_duration": testimonial_data.get('cooperation_duration'),
                "description": f"{testimonial_data.get('customer_country')}客户{testimonial_data.get('customer_name')}：{testimonial_data.get('testimonial')}"
            },
            "safety_score": 97,
            "created_at": datetime.now().isoformat()
        }
        self.contents["testimonials"].append(content)
        self._save_contents()
        logger.info(f"✅ 客户见证内容已生成：{content['id']}")
        return content
    
    def generate_certifications(self, cert_data: Dict) -> Dict:
        """生成认证资质内容"""
        content = {
            "id": f"CERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": "certifications",
            "title": f"认证资质 - {cert_data.get('company_name', '公司')}",
            "content": {
                "company_name": cert_data.get('company_name'),
                "certifications": cert_data.get('certifications', []),
                "licenses": cert_data.get('licenses', []),
                "patents": cert_data.get('patents', []),
                "description": f"拥有{len(cert_data.get('certifications', []))}项认证，{len(cert_data.get('licenses', []))}项执照，{len(cert_data.get('patents', []))}项专利"
            },
            "safety_score": 99,
            "created_at": datetime.now().isoformat()
        }
        self.contents["certifications"].append(content)
        self._save_contents()
        logger.info(f"✅ 认证资质内容已生成：{content['id']}")
        return content
    
    def _save_contents(self):
        with open(self.content_file, 'w', encoding='utf-8') as f:
            json.dump(self.contents, f, indent=2, ensure_ascii=False)
    
    def get_all_contents(self) -> Dict:
        return self.contents


def main():
    logger.info("=" * 60)
    logger.info("🏭 B2B 安全感内容生成模块 - 演示")
    logger.info("=" * 60)
    
    generator = SafetyContentGenerator()
    
    # 演示工厂实景
    factory_content = generator.generate_factory_proof({
        "name": "深圳兴旺工具厂",
        "location": "广东深圳",
        "area": "5000 平方米",
        "employees": 120,
        "production_lines": 8,
        "capacity": "月产 10 万件"
    })
    
    # 演示出货记录
    shipping_content = generator.generate_shipping_records({
        "destination": "全球",
        "total_shipments": 5000,
        "on_time_rate": "98.5%",
        "countries": 50
    })
    
    # 演示客户见证
    testimonial_content = generator.generate_customer_testimonials({
        "customer_name": "John Smith",
        "customer_country": "美国",
        "product": "数控工具套装",
        "order_value": "$50,000",
        "testimonial": "质量稳定，交期准时，合作 3 年非常满意",
        "rating": 5,
        "cooperation_duration": "3 年"
    })
    
    # 演示认证资质
    cert_content = generator.generate_certifications({
        "company_name": "深圳兴旺工具厂",
        "certifications": ["ISO9001", "CE", "FCC"],
        "licenses": ["营业执照", "出口许可证"],
        "patents": ["实用新型专利 5 项", "发明专利 2 项"]
    })
    
    logger.info(f"\n📊 安全感内容统计:")
    logger.info(f"  工厂实景：{len(generator.contents['factory'])}个")
    logger.info(f"  出货记录：{len(generator.contents['shipping'])}个")
    logger.info(f"  客户见证：{len(generator.contents['testimonials'])}个")
    logger.info(f"  认证资质：{len(generator.contents['certifications'])}个")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
