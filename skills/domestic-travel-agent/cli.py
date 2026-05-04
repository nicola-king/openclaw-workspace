#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅游探路者 v2.0 - 国内游 Agent 统一 CLI

使用方式:
    python3 cli.py plan --city 北京 --days 3 --budget 5000
    python3 cli.py weather --city 成都
    python3 cli.py hotels --city 上海 --keyword 外滩
    python3 cli.py restaurants --city 成都 --cuisine 川菜
    python3 cli.py attractions --city 北京 --category 历史
    python3 cli.py services --city 北京 --type tour_guide
    python3 cli.py guide --city 北京 --full
    python3 cli.py intel --city 成都
    python3 cli.py search --city 北京 --query 故宫门票

作者：太一 AGI
创建：2026-05-04
"""

import sys
import json
import argparse
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent / "core"))

from base import TravelCoreModule
from planner import TripPlanner
from weather_safety import WeatherSafety
from intelligence_hub import IntelligenceHub
from local_services import LocalServices
from hotels import Hotels
from restaurants import Restaurants
from attractions import Attractions
from destination_guide import DestinationGuide


def cmd_plan(args):
    planner = TripPlanner()
    if args.with_hotels or args.with_restaurants:
        result = planner.plan_with_addons(
            args.city, args.days, args.budget, args.preferences,
            include_hotel=args.with_hotels, include_restaurant=args.with_restaurants,
            start_date=args.start_date or ''
        )
    else:
        result = planner.plan(args.city, args.days, args.budget, args.preferences, args.start_date or '')
    _print_result(result, args)
    if args.save:
        path = planner.save_json(result, f"plan_{args.city}_{args.days}d")
        print(f"✅ 已保存: {path}")


def cmd_weather(args):
    ws = WeatherSafety()
    if args.advice:
        result = ws.get_safety_advice(args.city, args.month)
    elif args.best_months:
        result = ws.get_best_travel_months(args.city)
    else:
        result = ws.get_climate(args.city, args.month)
    _print_result(result, args)
    if args.save:
        path = ws.save_json(result, f"weather_{args.city}")
        print(f"✅ 已保存: {path}")


def cmd_hotels(args):
    h = Hotels()
    if args.max_price:
        result = h.get_by_price_range(args.city, args.max_price)
    else:
        result = h.search(args.city, args.keyword or '')
    _print_result(result, args)
    if args.save:
        path = h.save_json(result, f"hotels_{args.city}")
        print(f"✅ 已保存: {path}")


def cmd_restaurants(args):
    r = Restaurants()
    if args.min_rating:
        result = r.get_by_rating(args.city, args.min_rating)
    elif args.max_price:
        result = r.get_by_price(args.city, args.max_price)
    else:
        result = r.search(args.city, args.cuisine or '')
    _print_result(result, args)
    if args.save:
        path = r.save_json(result, f"restaurants_{args.city}")
        print(f"✅ 已保存: {path}")


def cmd_attractions(args):
    a = Attractions()
    result = a.search(args.city, args.category or '', args.keyword or '')
    _print_result(result, args)
    if args.save:
        path = a.save_json(result, f"attractions_{args.city}")
        print(f"✅ 已保存: {path}")


def cmd_services(args):
    ls = LocalServices()
    if args.tour_guides:
        result = ls.get_tour_guides(args.city)
    elif args.car_rentals:
        result = ls.get_car_rentals(args.city)
    else:
        result = ls.get_services(args.city, args.type or '')
    _print_result(result, args)
    if args.save:
        path = ls.save_json(result, f"services_{args.city}")
        print(f"✅ 已保存: {path}")


def cmd_guide(args):
    dg = DestinationGuide()
    if args.customs:
        result = dg.get_customs(args.city)
    elif args.safety:
        result = dg.get_safety(args.city)
    elif args.emergency:
        result = dg.get_emergency(args.city)
    else:
        result = dg.get_full_guide(args.city)
    _print_result(result, args)
    if args.save:
        path = dg.save_json(result, f"guide_{args.city}")
        print(f"✅ 已保存: {path}")


def cmd_intel(args):
    ih = IntelligenceHub()
    result = ih.assess(args.city, args.type or 'destination', args.keywords or '')
    _print_result(result, args)
    if args.save:
        path = ih.save_json(result, f"intel_{args.city}")
        print(f"✅ 已保存: {path}")


def cmd_search(args):
    ih = IntelligenceHub()
    result = ih.search_travel_info(args.query)
    _print_result(result, args)


def cmd_stats(args):
    base = TravelCoreModule()
    if base.db:
        stats = base.db.get_statistics(args.city)
        print(f"\n📊 {args.city} 数据统计")
        print(f"{'='*40}")
        for table, count in stats.items():
            names = {'hotels': '酒店', 'restaurants': '餐馆', 'attractions': '景点',
                    'local_services': '本地服务', 'destination_guides': '目的地指南',
                    'intelligence_ratings': '评分', 'weather_safety': '天气数据'}
            print(f"  {names.get(table, table)}: {count} 条")
    else:
        print("数据库未加载")


def cmd_init_city(args):
    """初始化城市数据"""
    base = TravelCoreModule()
    if not base.db:
        print("数据库未加载，无法初始化")
        return

    # 从各模块的示例数据加载
    from hotels import Hotels
    from restaurants import Restaurants
    from attractions import Attractions
    from local_services import SAMPLE_SERVICES
    from destination_guide import DOMESTIC_GUIDES

    city = args.city.lower()

    # 加载酒店
    h = Hotels()
    hotels_result = h.search(city)
    print(f"🏨 加载 {city} 酒店: {hotels_result.get('count', 0)} 家")

    # 加载餐馆
    r = Restaurants()
    rests_result = r.search(city)
    print(f"🍽️ 加载 {city} 餐馆: {rests_result.get('count', 0)} 家")

    # 加载景点
    a = Attractions()
    attr_result = a.search(city)
    print(f"🏛️ 加载 {city} 景点: {attr_result.get('count', 0)} 个")

    # 加载服务
    ls = LocalServices()
    svc_result = ls.get_services(city)
    print(f"🏢 加载 {city} 服务: {svc_result.get('count', 0)} 条")

    # 加载指南
    dg = DestinationGuide()
    guide = dg.get_full_guide(city)
    if guide.get('status') == 'success':
        from db import TravelDatabase
        for section, items in guide.items():
            if isinstance(items, list) and items:
                for item in items:
                    if isinstance(item, str):
                        base.db.save_guide(city, section, item[:100], item)

    if base.db:
        stats = base.db.get_statistics(city)
        print(f"\n✅ 初始化完成: {city}")
        print(f"  数据库: {base.db_path}")


def _print_result(result, args):
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, dict) and result.get('status') == 'error':
        print(f"❌ {result.get('message')}")
    elif isinstance(result, dict):
        # 简洁输出
        pass  # 各个命令自己的 print
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description='太一旅游探路者 v2.0 - 国内游 Agent')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    parser.add_argument('--save', action='store_true', help='保存到文件')
    sub = parser.add_subparsers(dest='command', required=True)

    # plan
    p = sub.add_parser('plan', help='行程规划')
    p.add_argument('--city', required=True)
    p.add_argument('--days', type=int, default=3)
    p.add_argument('--budget', type=float, default=5000)
    p.add_argument('--preferences', default='综合')
    p.add_argument('--start-date')
    p.add_argument('--with-hotels', action='store_true')
    p.add_argument('--with-restaurants', action='store_true')

    # weather
    p = sub.add_parser('weather', help='天气与安全')
    p.add_argument('--city', required=True)
    p.add_argument('--month', type=int, default=0)
    p.add_argument('--advice', action='store_true')
    p.add_argument('--best-months', action='store_true')

    # hotels
    p = sub.add_parser('hotels', help='酒店信息')
    p.add_argument('--city', required=True)
    p.add_argument('--keyword')
    p.add_argument('--max-price', type=float)

    # restaurants
    p = sub.add_parser('restaurants', help='餐馆信息')
    p.add_argument('--city', required=True)
    p.add_argument('--cuisine')
    p.add_argument('--min-rating', type=float)
    p.add_argument('--max-price', type=float)

    # attractions
    p = sub.add_parser('attractions', help='景点信息')
    p.add_argument('--city', required=True)
    p.add_argument('--category')
    p.add_argument('--keyword')

    # services
    p = sub.add_parser('services', help='落地服务')
    p.add_argument('--city', required=True)
    p.add_argument('--type', choices=['tour_guide', 'car_rental', 'translator', 'local_agency'])
    p.add_argument('--tour-guides', action='store_true')
    p.add_argument('--car-rentals', action='store_true')

    # guide
    p = sub.add_parser('guide', help='目的地指南')
    p.add_argument('--city', required=True)
    p.add_argument('--customs', action='store_true')
    p.add_argument('--safety', action='store_true')
    p.add_argument('--emergency', action='store_true')

    # intel
    p = sub.add_parser('intel', help='综合情报')
    p.add_argument('--city', required=True)
    p.add_argument('--type', default='destination')
    p.add_argument('--keywords')

    # search
    p = sub.add_parser('search', help='搜索旅游信息')
    p.add_argument('--query', required=True)
    p.add_argument('--city')

    # stats
    p = sub.add_parser('stats', help='数据统计')
    p.add_argument('--city', required=True)

    # init-city
    p = sub.add_parser('init', help='初始化城市数据')
    p.add_argument('--city', required=True)

    args = parser.parse_args()

    # 分发命令
    commands = {
        'plan': cmd_plan,
        'weather': cmd_weather,
        'hotels': cmd_hotels,
        'restaurants': cmd_restaurants,
        'attractions': cmd_attractions,
        'services': cmd_services,
        'guide': cmd_guide,
        'intel': cmd_intel,
        'search': cmd_search,
        'stats': cmd_stats,
        'init': cmd_init_city,
    }

    cmd_fn = commands.get(args.command)
    if cmd_fn:
        cmd_fn(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
