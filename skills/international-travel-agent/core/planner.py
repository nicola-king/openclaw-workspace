#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅游探路者 v2.0 - 模块1: 旅游规划 (Trip Planner)

功能：
- 行程规划引擎
- 天数/预算/偏好输入
- 自动生成行程表
- 多日行程优化

作者：太一 AGI
创建：2026-05-04
"""

import json
import logging
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from .base import TravelCoreModule

logger = logging.getLogger('trip-planner')

# 国内城市景点示例数据
DOMESTIC_CITY_ATTRACTIONS = {
    'beijing': [
        {'name': '故宫博物院', 'name_cn': '故宫', 'category': '历史', 'duration': 240, 'rating': 4.8, 'address': '北京市东城区景山前街4号', 'ticket_price': '60元', 'opening_hours': '08:30-17:00'},
        {'name': '长城（八达岭）', 'name_cn': '八达岭长城', 'category': '历史', 'duration': 300, 'rating': 4.7, 'address': '北京市延庆区G6京藏高速58号', 'ticket_price': '40元', 'opening_hours': '06:30-19:00'},
        {'name': '天坛公园', 'name_cn': '天坛', 'category': '历史', 'duration': 120, 'rating': 4.6, 'address': '北京市东城区天坛内东里7号', 'ticket_price': '15元', 'opening_hours': '06:00-22:00'},
        {'name': '颐和园', 'name_cn': '颐和园', 'category': '园林', 'duration': 180, 'rating': 4.7, 'address': '北京市海淀区新建宫门路19号', 'ticket_price': '30元', 'opening_hours': '06:30-18:00'},
        {'name': '北海公园', 'name_cn': '北海公园', 'category': '园林', 'duration': 120, 'rating': 4.5, 'address': '北京市西城区文津街1号', 'ticket_price': '10元', 'opening_hours': '06:30-21:00'},
        {'name': '南锣鼓巷', 'name_cn': '南锣鼓巷', 'category': '街区', 'duration': 90, 'rating': 4.3, 'address': '北京市东城区南锣鼓巷', 'ticket_price': '免费', 'opening_hours': '全天'},
        {'name': '国家博物馆', 'name_cn': '国博', 'category': '文化', 'duration': 180, 'rating': 4.6, 'address': '北京市东城区东长安街16号', 'ticket_price': '免费', 'opening_hours': '09:00-17:00'},
        {'name': '后海/什刹海', 'name_cn': '什刹海', 'category': '街区', 'duration': 120, 'rating': 4.4, 'address': '北京市西城区什刹海', 'ticket_price': '免费', 'opening_hours': '全天'},
    ],
    'shanghai': [
        {'name': '外滩', 'name_cn': '外滩', 'category': '景观', 'duration': 90, 'rating': 4.7, 'address': '上海市黄浦区中山东一路', 'ticket_price': '免费', 'opening_hours': '全天'},
        {'name': '东方明珠塔', 'name_cn': '东方明珠', 'category': '地标', 'duration': 120, 'rating': 4.5, 'address': '上海市浦东新区世纪大道1号', 'ticket_price': '199元', 'opening_hours': '08:00-21:30'},
        {'name': '迪士尼乐园', 'name_cn': '迪士尼', 'category': '乐园', 'duration': 540, 'rating': 4.8, 'address': '上海市浦东新区川沙镇黄赵路310号', 'ticket_price': '475元', 'opening_hours': '08:30-21:30'},
        {'name': '豫园', 'name_cn': '豫园', 'category': '园林', 'duration': 120, 'rating': 4.5, 'address': '上海市黄浦区安仁街132号', 'ticket_price': '30元', 'opening_hours': '09:00-16:30'},
        {'name': '南京路步行街', 'name_cn': '南京路', 'category': '购物', 'duration': 120, 'rating': 4.4, 'address': '上海市黄浦区南京东路', 'ticket_price': '免费', 'opening_hours': '全天'},
        {'name': '上海博物馆', 'name_cn': '上海博物馆', 'category': '文化', 'duration': 150, 'rating': 4.6, 'address': '上海市黄浦区人民大道201号', 'ticket_price': '免费', 'opening_hours': '09:00-17:00'},
        {'name': '朱家角古镇', 'name_cn': '朱家角', 'category': '古镇', 'duration': 180, 'rating': 4.3, 'address': '上海市青浦区朱家角镇', 'ticket_price': '免费', 'opening_hours': '08:30-16:30'},
        {'name': '武康路', 'name_cn': '武康路', 'category': '街区', 'duration': 90, 'rating': 4.4, 'address': '上海市徐汇区武康路', 'ticket_price': '免费', 'opening_hours': '全天'},
    ],
    'chengdu': [
        {'name': '大熊猫繁育研究基地', 'name_cn': '熊猫基地', 'category': '自然', 'duration': 180, 'rating': 4.8, 'address': '成都市成华区熊猫大道1375号', 'ticket_price': '55元', 'opening_hours': '07:30-17:30'},
        {'name': '武侯祠', 'name_cn': '武侯祠', 'category': '历史', 'duration': 90, 'rating': 4.5, 'address': '成都市武侯区武侯祠大街231号', 'ticket_price': '50元', 'opening_hours': '08:00-19:00'},
        {'name': '宽窄巷子', 'name_cn': '宽窄巷子', 'category': '街区', 'duration': 120, 'rating': 4.4, 'address': '成都市青羊区长顺街', 'ticket_price': '免费', 'opening_hours': '全天'},
        {'name': '锦里', 'name_cn': '锦里', 'category': '街区', 'duration': 90, 'rating': 4.3, 'address': '成都市武侯区武侯祠大街', 'ticket_price': '免费', 'opening_hours': '全天'},
        {'name': '都江堰', 'name_cn': '都江堰', 'category': '历史', 'duration': 240, 'rating': 4.7, 'address': '成都市都江堰市公园路', 'ticket_price': '80元', 'opening_hours': '08:00-17:30'},
        {'name': '青城山', 'name_cn': '青城山', 'category': '自然', 'duration': 360, 'rating': 4.6, 'address': '成都市都江堰市青城山镇', 'ticket_price': '90元', 'opening_hours': '08:00-17:30'},
        {'name': '文殊院', 'name_cn': '文殊院', 'category': '宗教', 'duration': 60, 'rating': 4.4, 'address': '成都市青羊区文殊院街66号', 'ticket_price': '免费', 'opening_hours': '08:00-17:00'},
    ],
}


class TripPlanner(TravelCoreModule):
    """行程规划引擎"""

    def __init__(self, agent_type: str = 'domestic', db_dir: Optional[Path] = None):
        super().__init__(agent_type, db_dir)
        self.default_meal_budget = 150  # 每餐预算（元）

    def plan(self, city: str, days: int = 3, budget: float = 5000,
             preferences: str = '综合', start_date: str = '') -> Dict[str, Any]:
        """
        生成行程规划

        Args:
            city: 城市
            days: 天数
            budget: 总预算（元）
            preferences: 偏好（综合/历史/自然/美食/购物/亲子）
            start_date: 开始日期 (YYYY-MM-DD)

        Returns:
            行程规划详情
        """
        logger.info(f"🗺️ 生成行程规划：{city} {days}天 预算¥{budget}")
        city_key = city.lower()

        # 获取该城市景点
        attractions = DOMESTIC_CITY_ATTRACTIONS.get(city_key, [])
        if not attractions:
            # 从数据库或搜索尝试获取
            if self.db:
                db_attractions = self.db.get_attractions(city)
                if db_attractions:
                    attractions = db_attractions

        if not attractions:
            return {
                'status': 'error',
                'message': f'未找到城市"{city}"的景点数据，请先通过 attractions 模块搜索',
                'city': city
            }

        # 根据偏好筛选
        if preferences and preferences not in ('综合', 'comprehensive'):
            pref_map = {'历史': '历史', '自然': '自然', '美食': '街区',
                       '购物': '购物', '亲子': '乐园', '冒险': '运动'}
            target_category = pref_map.get(preferences, preferences)
            filtered = [a for a in attractions if a.get('category') == target_category]
            if filtered:
                attractions = filtered

        # 按评分排序
        attractions = sorted(attractions, key=lambda x: x.get('rating', 0), reverse=True)

        # 计算每日预算分配
        daily_budget = budget / days
        attraction_budget = daily_budget * 0.4
        meal_budget = daily_budget * 0.25
        transport_budget = daily_budget * 0.2
        misc_budget = daily_budget * 0.15

        # 生成每日行程
        itinerary = []
        attractions_per_day = max(2, min(4, days * 2))  # 根据天数调整
        start = datetime.strptime(start_date, '%Y-%m-%d') if start_date else datetime.now()

        for day in range(1, days + 1):
            current_date = start + timedelta(days=day - 1)
            day_attractions = attractions[(day - 1) * 2:day * 2] if len(attractions) >= day * 2 else attractions[-2:]

            day_plan = {
                'day': day,
                'date': current_date.strftime('%Y-%m-%d'),
                'weekday': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][current_date.weekday()],
                'schedule': []
            }

            # 上午安排
            if len(day_attractions) > 0:
                day_plan['schedule'].append({
                    'time': '09:00-12:00',
                    'activity': f"参观 {day_attractions[0].get('name_cn') or day_attractions[0].get('name', '景点')}",
                    'detail': day_attractions[0].get('name', ''),
                    'duration': f"{day_attractions[0].get('duration', 120)}分钟",
                    'cost': self._extract_price(day_attractions[0].get('ticket_price', '免费')),
                    'category': day_attractions[0].get('category', ''),
                })
                day_plan['schedule'].append({'time': '12:00-13:30', 'activity': '午餐', 'detail': '推荐当地特色餐厅', 'cost': self.default_meal_budget})

            # 下午安排
            if len(day_attractions) > 1:
                day_plan['schedule'].append({
                    'time': '14:00-17:00',
                    'activity': f"参观 {day_attractions[1].get('name_cn') or day_attractions[1].get('name', '景点')}",
                    'detail': day_attractions[1].get('name', ''),
                    'duration': f"{day_attractions[1].get('duration', 120)}分钟",
                    'cost': self._extract_price(day_attractions[1].get('ticket_price', '免费')),
                    'category': day_attractions[1].get('category', ''),
                })
                day_plan['schedule'].append({'time': '17:00-18:30', 'activity': '自由活动', 'detail': '逛街/休息', 'cost': 0})

            # 晚上
            day_plan['schedule'].append({'time': '18:30-20:00', 'activity': '晚餐', 'detail': '品尝当地美食', 'cost': self.default_meal_budget})

            # 计算本日总花费
            total_day_cost = sum(item.get('cost', 0) for item in day_plan['schedule']) + misc_budget
            day_plan['total_estimated_cost'] = round(total_day_cost, 2)
            day_plan['estimated_cost_breakdown'] = {
                'attractions': round(attraction_budget, 2),
                'meals': round(meal_budget, 2),
                'transport': round(transport_budget, 2),
                'misc': round(misc_budget, 2),
            }

            itinerary.append(day_plan)

        # 生成推荐组合
        self._save_to_db(city, itinerary, budget, preferences)

        return {
            'status': 'success',
            'city': city,
            'days': days,
            'total_budget': budget,
            'preferences': preferences,
            'start_date': start_date or datetime.now().strftime('%Y-%m-%d'),
            'daily_budget': round(daily_budget, 2),
            'itinerary': itinerary,
            'tips': self._generate_tips(city, itinerary),
            'generated_at': datetime.now().isoformat(),
        }

    def plan_with_addons(self, city: str, days: int = 3, budget: float = 5000,
                         preferences: str = '综合', include_hotel: bool = True,
                         include_restaurant: bool = True, start_date: str = '') -> Dict[str, Any]:
        """含酒店和餐厅推荐的增强版行程规划"""
        plan = self.plan(city, days, budget, preferences, start_date)

        if include_hotel and self.db:
            hotels = self.db.get_hotels(city)
            if hotels:
                plan['recommended_hotels'] = [
                    {'name': h.get('name'), 'price_range': h.get('price_range'),
                     'rating': h.get('rating')} for h in hotels[:3]
                ]
            else:
                plan['recommended_hotels'] = [{'name': '请搜索酒店', 'info': '未找到数据'}]

        if include_restaurant and self.db:
            restaurants = self.db.get_restaurants(city)
            if restaurants:
                plan['recommended_restaurants'] = [
                    {'name': r.get('name'), 'cuisine': r.get('cuisine'),
                     'price_per_person': r.get('price_per_person')} for r in restaurants[:3]
                ]
            else:
                plan['recommended_restaurants'] = [{'name': '请搜索餐馆', 'info': '未找到数据'}]

        return plan

    def _save_to_db(self, city: str, itinerary: List[Dict], budget: float, preferences: str):
        """保存行程到数据库"""
        if self.db:
            try:
                self.db.save_plan(
                    plan_name=f"{city}_{len(itinerary)}d_{datetime.now().strftime('%m%d')}",
                    city=city, days=len(itinerary), budget=budget,
                    preferences=preferences, plan_data={'itinerary': itinerary}
                )
            except Exception as e:
                logger.warning(f"保存行程失败: {e}")

    def _extract_price(self, price_str: str) -> float:
        """从价格字符串提取数值"""
        if not price_str or price_str == '免费' or price_str == 'free':
            return 0
        import re
        numbers = re.findall(r'\d+\.?\d*', str(price_str))
        return float(numbers[0]) if numbers else 0

    def _generate_tips(self, city: str, itinerary: List[Dict]) -> List[str]:
        """生成旅行建议"""
        tips = [
            f"建议提前预订景点门票，避免现场排队",
            f"当地公共交通可使用支付宝/微信乘车码",
            f"带好身份证，部分景点需要实名购票",
            f"建议预留半天机动时间应对突发情况",
        ]
        budget = sum(d.get('total_estimated_cost', 0) for d in itinerary)
        tips.append(f"预估总花费约 ¥{budget:.0f}，请预留 ¥{budget * 0.2:.0f} 应急资金")
        return tips


def main():
    """CLI 入口"""
    parser = argparse.ArgumentParser(description='太一旅游探路者 - 行程规划')
    parser.add_argument('--city', required=True, help='城市')
    parser.add_argument('--days', type=int, default=3, help='天数')
    parser.add_argument('--budget', type=float, default=5000, help='总预算(元)')
    parser.add_argument('--preferences', default='综合', help='偏好: 综合/历史/自然/美食/购物/亲子')
    parser.add_argument('--start-date', help='开始日期 YYYY-MM-DD')
    parser.add_argument('--with-hotels', action='store_true', help='包含酒店推荐')
    parser.add_argument('--with-restaurants', action='store_true', help='包含餐馆推荐')
    parser.add_argument('--save', action='store_true', help='保存到文件')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    planner = TripPlanner()

    if args.with_hotels or args.with_restaurants:
        result = planner.plan_with_addons(
            args.city, args.days, args.budget, args.preferences,
            include_hotel=args.with_hotels, include_restaurant=args.with_restaurants,
            start_date=args.start_date or ''
        )
    else:
        result = planner.plan(args.city, args.days, args.budget, args.preferences, args.start_date or '')

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"🗺️  {result.get('city')} {result.get('days')}日游 行程规划")
        print(f"预算: ¥{result.get('total_budget')} | 偏好: {result.get('preferences')}")
        print(f"{'='*60}")
        for day in result.get('itinerary', []):
            print(f"\n📅 第{day['day']}天 ({day['date']} {day['weekday']})")
            print(f"{'─'*40}")
            for item in day.get('schedule', []):
                cost_str = f"¥{item['cost']}" if item['cost'] > 0 else '免费'
                print(f"  {item['time']} | {item['activity']} ({cost_str})")
                if item.get('detail'):
                    print(f"          {item['detail']}")
            print(f"  💰 本日预估: ¥{day.get('total_estimated_cost', 0)}")

        print(f"\n💡 旅行建议:")
        for tip in result.get('tips', []):
            print(f"  • {tip}")

        if result.get('recommended_hotels'):
            print(f"\n🏨 推荐酒店:")
            for h in result['recommended_hotels']:
                print(f"  • {h.get('name')} - {h.get('price_range')} 评分{h.get('rating')}")

        if result.get('recommended_restaurants'):
            print(f"\n🍽️ 推荐餐馆:")
            for r in result['recommended_restaurants']:
                print(f"  • {r.get('name')} - {r.get('cuisine')} 人均{r.get('price_per_person')}")

    if args.save:
        path = planner.save_json(result, f"plan_{args.city}_{args.days}d")
        print(f"\n✅ 已保存: {path}")


if __name__ == '__main__':
    main()
