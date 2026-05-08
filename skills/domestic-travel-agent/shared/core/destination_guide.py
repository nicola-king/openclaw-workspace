#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅游探路者 v2.0 - 模块8: 目的地指南 (Destination Guide)

功能：
- 风俗习惯
- 法律法规
- 安全事项
- 旅游局联系方式
- 食品安全监督局
- 药店/医院
- 大使馆信息
- 紧急联系电话

作者：太一 AGI
创建：2026-05-04
"""

import json
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

from .base import TravelCoreModule

logger = logging.getLogger('destination-guide')

# 国内目的地指南
DOMESTIC_GUIDES = {
    'beijing': {
        'general': {
            'timezone': 'UTC+8',
            'language': '普通话（北京口音）',
            'currency': '人民币 (CNY)',
            'voltage': '220V / 50Hz (两孔/三孔插座)',
            'emergency_numbers': {
                'police': '110',
                'fire': '119',
                'ambulance': '120',
                'traffic_accident': '122',
            },
        },
        'customs': [
            '故宫等景点周一闭馆，请提前规划',
            '参观寺庙、宫殿时注意着装得体',
            '提前预约景点门票，旺季需提前一周',
            '市内地推荐地铁出行，避免高峰期打车',
            '北京话儿化音较多，听不懂可请对方重复',
        ],
        'laws_notices': [
            '公共场所禁止吸烟（有专门吸烟区）',
            '天安门广场等政治敏感区域遵守安检规定',
            '无人机飞行需报备，禁飞区内严禁飞行',
            '遵守交通规则，过马路走斑马线',
        ],
        'safety': [
            '保管好随身物品，特别是在景区和地铁',
            '谨防景区附近的黑车和黑导游',
            '北京干燥，注意补充水分和防晒',
            '冬季空气污染较重，建议戴口罩',
            '遇到消费纠纷可拨打12315投诉',
        ],
        'tourism_office': {
            'name': '北京市文化和旅游局',
            'phone': '+86-10-12345',
            'website': 'https://whlyj.beijing.gov.cn',
            'address': '北京市朝阳区建国门外大街28号',
            'service_hours': '工作日 09:00-17:00',
        },
        'medical': {
            'hospitals': [
                {'name': '北京协和医院', 'phone': '+86-10-6915-6114', 'address': '北京市东城区帅府园1号', 'rating': 5},
                {'name': '北京大学第三医院', 'phone': '+86-10-8226-6699', 'address': '北京市海淀区花园北路49号', 'rating': 4.5},
                {'name': '北京中医药大学东直门医院', 'phone': '+86-10-8401-3200', 'address': '北京市东城区海运仓5号', 'rating': 4.5},
            ],
            'pharmacies': [
                {'name': '同仁堂药店（大栅栏店）', 'phone': '+86-10-6303-1285', 'address': '北京市西城区大栅栏街24号'},
                {'name': '国大药房（王府井店）', 'address': '北京市东城区王府井大街'},
            ],
        },
        'food_safety': {
            'name': '北京市市场监督管理局',
            'phone': '12315',
            'website': 'https://scjgj.beijing.gov.cn',
            'tips': '如遇食品安全问题，可拨打12315投诉或保存证据后向市场监管部门举报',
        },
    },
    'shanghai': {
        'general': {
            'timezone': 'UTC+8',
            'language': '普通话/上海话',
            'currency': '人民币 (CNY)',
            'voltage': '220V / 50Hz',
            'emergency_numbers': {
                'police': '110',
                'fire': '119',
                'ambulance': '120',
                'traffic_accident': '122',
            },
        },
        'customs': [
            '上海地铁禁止饮食，违者罚款',
            '早晚高峰地铁非常拥挤，建议避开',
            '便利店遍布全城，支持支付宝/微信支付',
            '上海餐厅一般会加收10%服务费',
            '外滩拍照注意保管好手机相机',
        ],
        'laws_notices': [
            '公共场所垃圾分类，注意按规定投放',
            '地铁、公交等公共交通禁止吸烟',
            '骑行共享单车需将车停放在指定区域',
        ],
        'safety': [
            '南京路、外滩等人流密集区注意防盗',
            '谨防出租车/黑车欺诈，建议使用网约车',
            '夏季注意防暑降温和台风预警',
        ],
        'tourism_office': {
            'name': '上海市文化和旅游局',
            'phone': '+86-21-12345',
            'website': 'https://whlyj.sh.gov.cn',
            'address': '上海市黄浦区大沽路100号',
        },
        'medical': {
            'hospitals': [
                {'name': '复旦大学附属华山医院', 'phone': '+86-21-5288-9999', 'address': '上海市静安区乌鲁木齐中路12号'},
                {'name': '上海交通大学医学院附属瑞金医院', 'phone': '+86-21-6437-0045', 'address': '上海市黄浦区瑞金二路197号'},
            ],
            'pharmacies': [
                {'name': '国大药房（南京东路店）', 'address': '上海市黄浦区南京东路'},
            ],
        },
        'food_safety': {
            'name': '上海市市场监督管理局',
            'phone': '12315',
            'website': 'https://scjgj.sh.gov.cn',
        },
    },
    'chengdu': {
        'general': {
            'timezone': 'UTC+8',
            'language': '普通话/四川话',
            'currency': '人民币 (CNY)',
            'voltage': '220V / 50Hz',
            'emergency_numbers': {
                'police': '110',
                'fire': '119',
                'ambulance': '120',
                'traffic_accident': '122',
            },
        },
        'customs': [
            '成都人爱吃辣，不能吃辣的点餐时说明"不要辣"',
            '茶馆文化浓厚，可以去人民公园体验盖碗茶',
            '火锅店大多营业到凌晨，成都夜生活丰富',
            '宽窄巷子、锦里是游客聚集地，物价偏高',
        ],
        'laws_notices': [
            '大熊猫基地禁止投喂动物',
            '都江堰景区注意涉水安全',
        ],
        'safety': [
            '注意饮食卫生，肠胃敏感者备好药',
            '川菜偏辣，初次尝试建议微辣',
            '春秋最佳旅游季，但早晚温差大需带外套',
        ],
        'tourism_office': {
            'name': '成都市文化广电旅游局',
            'phone': '+86-28-12345',
            'website': 'https://cdwlj.chengdu.gov.cn',
            'address': '成都市锦江区天府大道北段1700号',
        },
        'medical': {
            'hospitals': [
                {'name': '四川大学华西医院', 'phone': '+86-28-8542-2114', 'address': '成都市武侯区国学巷37号'},
                {'name': '成都市第一人民医院', 'phone': '+86-28-8531-1722', 'address': '成都市高新区万象北路18号'},
            ],
            'pharmacies': [
                {'name': '一心堂药店（春熙路店）', 'address': '成都市锦江区春熙路'},
            ],
        },
        'food_safety': {
            'name': '成都市市场监督管理局',
            'phone': '12315',
            'website': 'https://scjgj.chengdu.gov.cn',
        },
    },
}


class DestinationGuide(TravelCoreModule):
    """目的地指南模块"""

    def __init__(self, agent_type: str = 'domestic', db_dir: Optional[Path] = None):
        super().__init__(agent_type, db_dir)

    def get_full_guide(self, city: str) -> Dict[str, Any]:
        """获取完整目的地指南"""
        city_key = city.lower()
        guide = DOMESTIC_GUIDES.get(city_key, {})

        if not guide:
            # 尝试从数据库获取
            if self.db:
                db_guides = self.db.get_guides(city)
                if db_guides:
                    guide = {'from_db': db_guides}
            if not guide:
                return {'status': 'error', 'message': f'未找到"{city}"的目的地指南'}

        result = {
            'status': 'success',
            'city': city,
            'general_info': guide.get('general', {}),
            'customs_etiquette': guide.get('customs', []),
            'laws_regulations': guide.get('laws_notices', []),
            'safety_tips': guide.get('safety', []),
            'tourism_office': guide.get('tourism_office', {}),
            'medical_info': guide.get('medical', {}),
            'food_safety': guide.get('food_safety', {}),
        }

        return result

    def get_customs(self, city: str) -> Dict[str, Any]:
        """获取风俗习惯"""
        guide = self.get_full_guide(city)
        return {'status': guide['status'], 'city': city,
                'customs': guide.get('customs_etiquette', [])}

    def get_safety(self, city: str) -> Dict[str, Any]:
        """获取安全事项"""
        guide = self.get_full_guide(city)
        return {'status': guide['status'], 'city': city,
                'safety_tips': guide.get('safety_tips', [])}

    def get_emergency(self, city: str) -> Dict[str, Any]:
        """获取紧急联系信息"""
        guide = self.get_full_guide(city)
        general = guide.get('general_info', {})
        emergency = general.get('emergency_numbers', {})
        medical = guide.get('medical_info', {})
        tourism = guide.get('tourism_office', {})
        food = guide.get('food_safety', {})

        return {
            'status': 'success',
            'city': city,
            'emergency_numbers': emergency,
            'hospitals': medical.get('hospitals', []),
            'pharmacies': medical.get('pharmacies', []),
            'tourism_office': tourism,
            'food_safety_authority': food,
        }

    def get_international_info(self, country: str) -> Dict[str, Any]:
        """获取国外目的地信息（大使馆、签证等）"""
        embassy_info = {
            'japan': {
                'embassy': {
                    'name': '中华人民共和国驻日本国大使馆',
                    'address': '〒106-0046 东京都港区元麻布3-4-33',
                    'phone': '+81-3-3403-3388',
                    'emergency_phone': '+81-3-3403-3064',
                    'website': 'http://www.china-embassy.or.jp',
                },
            },
            'thailand': {
                'embassy': {
                    'name': '中华人民共和国驻泰王国大使馆',
                    'address': '57 Ratchadaphisek Road, Bangkok 10400',
                    'phone': '+66-2-245-0088',
                    'emergency_phone': '+66-85-483-3327',
                    'website': 'http://www.chinaembassy.or.th',
                },
            },
            'australia': {
                'embassy': {
                    'name': '中华人民共和国驻澳大利亚大使馆',
                    'address': '15 Coronation Drive, Yarralumla, ACT 2600',
                    'phone': '+61-2-6228-5800',
                    'emergency_phone': '+61-2-6228-3999',
                    'website': 'http://au.china-embassy.gov.cn',
                },
            },
            'singapore': {
                'embassy': {
                    'name': '中华人民共和国驻新加坡共和国大使馆',
                    'address': '150 Tanglin Road, Singapore 247969',
                    'phone': '+65-6471-2117',
                    'emergency_phone': '+65-9638-2195',
                    'website': 'http://www.chinaembassy.org.sg',
                },
            },
        }

        return embassy_info.get(country.lower(), {})


def main():
    parser = argparse.ArgumentParser(description='太一旅游探路者 - 目的地指南')
    parser.add_argument('--city', required=True, help='城市')
    parser.add_argument('--customs', action='store_true', help='风俗习惯')
    parser.add_argument('--safety', action='store_true', help='安全事项')
    parser.add_argument('--emergency', action='store_true', help='紧急联系方式')
    parser.add_argument('--full', action='store_true', help='完整指南')
    parser.add_argument('--country', help='国外目的地国家(获取大使馆信息)')
    parser.add_argument('--save', action='store_true', help='保存到文件')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    dg = DestinationGuide()

    if args.country:
        result = dg.get_international_info(args.country)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'='*60}")
            print(f"🏛️  {args.country} 大使馆信息")
            print(f"{'='*60}")
            if result.get('embassy'):
                e = result['embassy']
                print(f"\n  📍 {e.get('name')}")
                print(f"  地址: {e.get('address')}")
                print(f"  电话: {e.get('phone')}")
                print(f"  紧急: {e.get('emergency_phone')}")
                print(f"  官网: {e.get('website')}")
            else:
                print(f"  未找到 {args.country} 的大使馆信息")
        return

    if args.customs:
        result = dg.get_customs(args.city)
    elif args.safety:
        result = dg.get_safety(args.city)
    elif args.emergency:
        result = dg.get_emergency(args.city)
    else:
        result = dg.get_full_guide(args.city)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"📖 目的地指南: {args.city}")
        print(f"{'='*60}")

        gi = result.get('general_info', {})
        if gi:
            print(f"\n📍 基本信息")
            print(f"  时区: {gi.get('timezone')}")
            print(f"  语言: {gi.get('language')}")
            print(f"  货币: {gi.get('currency')}")
            print(f"  电压: {gi.get('voltage')}")
            if gi.get('emergency_numbers'):
                print(f"  🆘 紧急电话: {gi['emergency_numbers']}")

        customs = result.get('customs_etiquette', [])
        if customs:
            print(f"\n🎎 风俗习惯:")
            for c in customs:
                print(f"  • {c}")

        laws = result.get('laws_regulations', [])
        if laws:
            print(f"\n⚖️ 法律法规:")
            for l in laws:
                print(f"  • {l}")

        safety = result.get('safety_tips', [])
        if safety:
            print(f"\n🛡️ 安全事项:")
            for s in safety:
                print(f"  • {s}")

        toffice = result.get('tourism_office', {})
        if toffice:
            print(f"\n🏛️ 旅游局: {toffice.get('name')}")
            print(f"  电话: {toffice.get('phone')}")
            print(f"  网站: {toffice.get('website')}")
            print(f"  地址: {toffice.get('address')}")

        medical = result.get('medical_info', {})
        if medical:
            hospitals = medical.get('hospitals', [])
            if hospitals:
                print(f"\n🏥 医院:")
                for h in hospitals:
                    print(f"  • {h.get('name')} - {h.get('phone')}")
            pharmacies = medical.get('pharmacies', [])
            if pharmacies:
                print(f"\n💊 药店:")
                for p in pharmacies:
                    print(f"  • {p.get('name')} - {p.get('address')}")

        fs = result.get('food_safety', {})
        if fs:
            print(f"\n🔬 食品安全: {fs.get('name')} (电话: {fs.get('phone')})")

    if args.save:
        path = dg.save_json(result, f"guide_{args.city}")
        print(f"\n✅ 已保存: {path}")


if __name__ == '__main__':
    main()
