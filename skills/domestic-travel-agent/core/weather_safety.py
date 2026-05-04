#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅游探路者 v2.0 - 模块2: 目的地天气及预防措施 (Weather & Safety)

功能：
- 天气查询（复用 weather skill）
- 自然灾害预警（台风/地震/洪水）
- 健康预防建议
- 最佳旅行季节推荐

作者：太一 AGI
创建：2026-05-04
"""

import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from .base import TravelCoreModule

logger = logging.getLogger('weather-safety')

# 国内城市气候数据
DOMESTIC_CLIMATE = {
    'beijing': {
        'name': '北京',
        'region': '华北',
        'climate_type': '温带季风气候',
        'best_travel_season': '春季(4-5月)和秋季(9-11月)',
        'best_travel_months': [4, 5, 9, 10, 11],
        'monthly': {
            1: {'avg_temp_high': 1, 'avg_temp_low': -9, 'avg_humidity': 43, 'rainfall_mm': 3, 'weather_notes': '寒冷干燥，注意保暖'},
            2: {'avg_temp_high': 5, 'avg_temp_low': -6, 'avg_humidity': 44, 'rainfall_mm': 5, 'weather_notes': '干燥，偶有风沙'},
            3: {'avg_temp_high': 12, 'avg_temp_low': 0, 'avg_humidity': 45, 'rainfall_mm': 9, 'weather_notes': '回暖，注意花粉过敏'},
            4: {'avg_temp_high': 20, 'avg_temp_low': 8, 'avg_humidity': 47, 'rainfall_mm': 22, 'weather_notes': '适宜旅游'},
            5: {'avg_temp_high': 26, 'avg_temp_low': 14, 'avg_humidity': 50, 'rainfall_mm': 35, 'weather_notes': '温暖舒适'},
            6: {'avg_temp_high': 30, 'avg_temp_low': 20, 'avg_humidity': 58, 'rainfall_mm': 70, 'weather_notes': '炎热，偶有降雨'},
            7: {'avg_temp_high': 31, 'avg_temp_low': 23, 'avg_humidity': 71, 'rainfall_mm': 165, 'weather_notes': '高温多雨，注意防暑'},
            8: {'avg_temp_high': 30, 'avg_temp_low': 22, 'avg_humidity': 73, 'rainfall_mm': 155, 'weather_notes': '炎热潮湿，雷阵雨多'},
            9: {'avg_temp_high': 26, 'avg_temp_low': 15, 'avg_humidity': 64, 'rainfall_mm': 50, 'weather_notes': '秋高气爽，最佳旅游季'},
            10: {'avg_temp_high': 19, 'avg_temp_low': 8, 'avg_humidity': 57, 'rainfall_mm': 20, 'weather_notes': '凉爽宜人'},
            11: {'avg_temp_high': 10, 'avg_temp_low': 0, 'avg_humidity': 50, 'rainfall_mm': 6, 'weather_notes': '转凉，注意添衣'},
            12: {'avg_temp_high': 3, 'avg_temp_low': -6, 'avg_humidity': 44, 'rainfall_mm': 2, 'weather_notes': '寒冷干燥'},
        },
        'disaster_risk': {
            'spring_dust': '春季偶有沙尘暴，注意戴口罩',
            'summer_storm': '夏季暴雨可能引发城区积水',
            'winter_cold': '冬季极端低温可达-15°C',
        },
        'health_notes': {
            'spring_allergy': '春季花粉浓度高，过敏者需注意',
            'summer_heatstroke': '夏季注意防暑降温，多饮水',
            'winter_flu': '冬季流感高发，建议接种疫苗',
        }
    },
    'shanghai': {
        'name': '上海',
        'region': '华东',
        'climate_type': '亚热带季风气候',
        'best_travel_season': '春季(3-5月)和秋季(9-11月)',
        'best_travel_months': [3, 4, 5, 9, 10, 11],
        'monthly': {
            1: {'avg_temp_high': 8, 'avg_temp_low': 1, 'avg_humidity': 71, 'rainfall_mm': 45, 'weather_notes': '湿冷'},
            2: {'avg_temp_high': 10, 'avg_temp_low': 3, 'avg_humidity': 72, 'rainfall_mm': 55, 'weather_notes': '阴冷多雨'},
            3: {'avg_temp_high': 14, 'avg_temp_low': 6, 'avg_humidity': 72, 'rainfall_mm': 85, 'weather_notes': '回暖，春雨绵绵'},
            4: {'avg_temp_high': 20, 'avg_temp_low': 12, 'avg_humidity': 71, 'rainfall_mm': 90, 'weather_notes': '温暖舒适'},
            5: {'avg_temp_high': 25, 'avg_temp_low': 17, 'avg_humidity': 73, 'rainfall_mm': 95, 'weather_notes': '舒适'},
            6: {'avg_temp_high': 29, 'avg_temp_low': 22, 'avg_humidity': 80, 'rainfall_mm': 175, 'weather_notes': '梅雨季，闷热潮湿'},
            7: {'avg_temp_high': 33, 'avg_temp_low': 26, 'avg_humidity': 78, 'rainfall_mm': 140, 'weather_notes': '高温酷暑'},
            8: {'avg_temp_high': 33, 'avg_temp_low': 26, 'avg_humidity': 78, 'rainfall_mm': 170, 'weather_notes': '高温，台风季'},
            9: {'avg_temp_high': 28, 'avg_temp_low': 21, 'avg_humidity': 76, 'rainfall_mm': 100, 'weather_notes': '秋老虎'},
            10: {'avg_temp_high': 23, 'avg_temp_low': 15, 'avg_humidity': 72, 'rainfall_mm': 55, 'weather_notes': '秋高气爽'},
            11: {'avg_temp_high': 17, 'avg_temp_low': 10, 'avg_humidity': 70, 'rainfall_mm': 45, 'weather_notes': '凉爽'},
            12: {'avg_temp_high': 11, 'avg_temp_low': 4, 'avg_humidity': 69, 'rainfall_mm': 35, 'weather_notes': '湿冷'},
        },
        'disaster_risk': {
            'typhoon': '7-9月台风季，关注台风预警',
            'heavy_rain': '梅雨季可能引发城市内涝',
            'summer_heatwave': '夏季高温可达40°C',
        },
        'health_notes': {
            'summer_mosquito': '夏季蚊虫多，注意防蚊',
            'mold_season': '梅雨季注意食品防霉',
            'winter_humid': '冬季湿冷，注意保暖防感冒',
        }
    },
    'chengdu': {
        'name': '成都',
        'region': '西南',
        'climate_type': '亚热带湿润季风气候',
        'best_travel_season': '春季(3-6月)和秋季(9-11月)',
        'best_travel_months': [3, 4, 5, 9, 10, 11],
        'monthly': {
            1: {'avg_temp_high': 10, 'avg_temp_low': 3, 'avg_humidity': 76, 'rainfall_mm': 8, 'weather_notes': '阴冷，少见阳光'},
            2: {'avg_temp_high': 12, 'avg_temp_low': 5, 'avg_humidity': 78, 'rainfall_mm': 12, 'weather_notes': '微冷'},
            3: {'avg_temp_high': 17, 'avg_temp_low': 9, 'avg_humidity': 74, 'rainfall_mm': 21, 'weather_notes': '回暖，百花盛开'},
            4: {'avg_temp_high': 22, 'avg_temp_low': 14, 'avg_humidity': 73, 'rainfall_mm': 44, 'weather_notes': '舒适'},
            5: {'avg_temp_high': 26, 'avg_temp_low': 18, 'avg_humidity': 72, 'rainfall_mm': 75, 'weather_notes': '温暖'},
            6: {'avg_temp_high': 29, 'avg_temp_low': 22, 'avg_humidity': 77, 'rainfall_mm': 104, 'weather_notes': '闷热'},
            7: {'avg_temp_high': 30, 'avg_temp_low': 23, 'avg_humidity': 82, 'rainfall_mm': 195, 'weather_notes': '炎热多雨'},
            8: {'avg_temp_high': 30, 'avg_temp_low': 22, 'avg_humidity': 82, 'rainfall_mm': 201, 'weather_notes': '炎热，降雨最多'},
            9: {'avg_temp_high': 25, 'avg_temp_low': 19, 'avg_humidity': 80, 'rainfall_mm': 121, 'weather_notes': '凉爽'},
            10: {'avg_temp_high': 21, 'avg_temp_low': 15, 'avg_humidity': 79, 'rainfall_mm': 35, 'weather_notes': '秋高气爽'},
            11: {'avg_temp_high': 17, 'avg_temp_low': 11, 'avg_humidity': 77, 'rainfall_mm': 15, 'weather_notes': '转凉'},
            12: {'avg_temp_high': 12, 'avg_temp_low': 6, 'avg_humidity': 76, 'rainfall_mm': 6, 'weather_notes': '阴冷'},
        },
        'disaster_risk': {
            'earthquake': '位于龙门山地震带，关注地震预警',
            'heavy_rain': '夏季强降雨可能引发山洪',
        },
        'health_notes': {
            'damp_climate': '气候潮湿，注意祛湿保暖',
            'spicy_food': '川菜麻辣，胃肠敏感者注意',
        }
    }
}


class WeatherSafety(TravelCoreModule):
    """天气与安全模块"""

    def __init__(self, agent_type: str = 'domestic', db_dir: Optional[Path] = None):
        super().__init__(agent_type, db_dir)

    def get_climate(self, city: str, month: int = 0) -> Dict[str, Any]:
        """获取城市气候数据"""
        city_key = city.lower()
        climate_data = DOMESTIC_CLIMATE.get(city_key)

        if not climate_data:
            # 尝试从数据库获取
            if self.db:
                rows = self.db.get_weather(city, month)
                if rows:
                    return {'status': 'success', 'city': city, 'data': rows}
            return {'status': 'error', 'message': f'未找到"{city}"的气候数据'}

        result = {
            'status': 'success',
            'city': climate_data['name'],
            'region': climate_data['region'],
            'climate_type': climate_data['climate_type'],
            'best_travel_season': climate_data['best_travel_season'],
            'disaster_risks': list(climate_data.get('disaster_risk', {}).values()),
            'health_notes': list(climate_data.get('health_notes', {}).values()),
        }

        if month:
            m = climate_data['monthly'].get(month)
            if m:
                result['current_month'] = {**m, 'month': month}
        else:
            result['monthly_overview'] = [
                {'month': m, **data} for m, data in climate_data['monthly'].items()
            ]

        # 判断当前是否在最佳旅行季
        current_month = month or datetime.now().month
        result['is_best_season'] = current_month in climate_data['best_travel_months']

        # 保存到数据库
        if self.db:
            for m, data in climate_data['monthly'].items():
                try:
                    self.db.save_weather(city, m, data)
                except Exception:
                    pass

        return result

    def get_safety_advice(self, city: str, month: int = 0) -> Dict[str, Any]:
        """获取安全建议"""
        climate = self.get_climate(city, month)
        if climate.get('status') == 'error':
            return climate

        month = month or datetime.now().month
        advice = {
            'city': city,
            'month': month,
            'general_safety': [
                '妥善保管个人证件和贵重物品',
                '注意交通规则，过街走斑马线',
                '避免深夜独自前往偏僻区域',
                '保存当地紧急联系电话',
                '购买旅行保险，涵盖医疗和意外',
            ],
            'weather_related': [],
            'disaster_precautions': climate.get('disaster_risks', []),
            'health_advice': climate.get('health_notes', []),
        }

        # 根据月份生成天气相关建议
        if month in [6, 7, 8, 9]:
            advice['weather_related'].append('高温时段(12:00-15:00)减少户外活动')
            advice['weather_related'].append('随身携带防晒霜和遮阳帽')
            advice['weather_related'].append('多饮水，预防中暑')
        elif month in [12, 1, 2]:
            advice['weather_related'].append('注意保暖，穿戴羽绒服/厚外套')
            advice['weather_related'].append('室内外温差大，注意预防感冒')
        elif month in [3, 4, 5]:
            advice['weather_related'].append('春季花粉多，过敏者戴口罩')
            advice['weather_related'].append('早晚温差大，注意增减衣物')

        return advice

    def get_best_travel_months(self, city: str) -> List[Dict[str, Any]]:
        """获取最佳旅行月份"""
        climate = self.get_climate(city)
        if climate.get('status') == 'error':
            return []

        best = []
        for item in climate.get('monthly_overview', []):
            m = item['month']
            if m in climate.get('best_travel_months', []) or True:
                score = self._score_month(item)
                if score >= 6:
                    best.append({
                        'month': m,
                        'score': score,
                        'avg_temp': f"{item['avg_temp_low']}~{item['avg_temp_high']}°C",
                        'notes': item['weather_notes'],
                        'is_best': m in climate.get('best_travel_months', []),
                    })

        return sorted(best, key=lambda x: x['score'], reverse=True)

    def _score_month(self, data: Dict) -> float:
        """评分月份适宜度"""
        safety_score = 10.0
        temp_range = data.get('avg_temp_high', 20) - data.get('avg_temp_low', 10)

        # 理想温度范围 15-28°C
        avg_temp = (data.get('avg_temp_high', 20) + data.get('avg_temp_low', 10)) / 2
        if avg_temp < 5 or avg_temp > 35:
            safety_score -= 4
        elif avg_temp < 10 or avg_temp > 30:
            safety_score -= 2

        # 降雨过多减分
        rainfall = data.get('rainfall_mm', 0)
        if rainfall > 150:
            safety_score -= 2
        elif rainfall > 80:
            safety_score -= 1

        return max(1, safety_score)


def main():
    parser = argparse.ArgumentParser(description='太一旅游探路者 - 天气与安全')
    parser.add_argument('--city', required=True, help='城市')
    parser.add_argument('--month', type=int, default=0, help='月份(1-12, 0=全年)')
    parser.add_argument('--advice', action='store_true', help='获取安全建议')
    parser.add_argument('--best-months', action='store_true', help='获取最佳旅行月')
    parser.add_argument('--save', action='store_true', help='保存到文件')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ws = WeatherSafety()

    if args.best_months:
        result = ws.get_best_travel_months(args.city)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'='*60}")
            print(f"🌤️  {args.city} 最佳旅行月份")
            print(f"{'='*60}")
            for m in result:
                badge = ' ✅' if m['is_best'] else ''
                print(f"  {m['month']}月 | 评分: {m['score']}/10 | 温度: {m['avg_temp']} | {m['notes']}{badge}")
    elif args.advice:
        result = ws.get_safety_advice(args.city, args.month)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            month_str = args.month or datetime.now().month
            print(f"\n{'='*60}")
            print(f"🛡️  {args.city} {month_str}月 安全与健康建议")
            print(f"{'='*60}")
            print(f"\n📋 一般安全:")
            for s in result.get('general_safety', []):
                print(f"  • {s}")
            print(f"\n🌦️ 天气相关:")
            for s in result.get('weather_related', []):
                print(f"  • {s}")
            print(f"\n⚠️ 自然灾害风险:")
            for s in result.get('disaster_precautions', []):
                print(f"  • {s}")
            print(f"\n💊 健康建议:")
            for s in result.get('health_advice', []):
                print(f"  • {s}")
    else:
        result = ws.get_climate(args.city, args.month)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'='*60}")
            print(f"🌤️  {result.get('city')} 气候信息")
            print(f"{'='*60}")
            print(f"  区域: {result.get('region')}")
            print(f"  气候类型: {result.get('climate_type')}")
            print(f"  最佳旅行季: {result.get('best_travel_season')}")
            print(f"  当前是否最佳: {'✅ 是' if result.get('is_best_season') else '⚠️ 不是'}")
            if args.month and result.get('current_month'):
                cm = result['current_month']
                print(f"\n  {args.month}月: {cm.get('weather_notes')}")
                print(f"    温度: {cm.get('avg_temp_low')}~{cm.get('avg_temp_high')}°C")
                print(f"    湿度: {cm.get('avg_humidity')}%")
                print(f"    降雨: {cm.get('rainfall_mm')}mm")

    if args.save:
        path = ws.save_json(result, f"weather_{args.city}")
        print(f"\n✅ 已保存: {path}")


if __name__ == '__main__':
    main()
