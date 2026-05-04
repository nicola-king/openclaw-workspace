#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅游探路者 v2.0 - 国际游 Agent 统一 CLI

使用方式:
    python3 cli.py plan --city tokyo --country japan --days 5
    python3 cli.py weather --city tokyo --country japan
    python3 cli.py embassy --country japan

作者：太一 AGI
创建：2026-05-04
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "domestic-travel-agent" / "core"))

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
    planner = TripPlanner(agent_type='international')
    if args.with_hotels or args.with_restaurants:
        result = planner.plan_with_addons(
            args.city, args.days, args.budget, args.preferences,
            include_hotel=args.with_hotels, include_restaurant=args.with_restaurants
        )
    else:
        result = planner.plan(args.city, args.days, args.budget, args.preferences)
    _print_result(result, args)


def cmd_weather(args):
    ws = WeatherSafety(agent_type='international')
    result = ws.get_climate(args.city, args.month) if not args.advice else ws.get_safety_advice(args.city, args.month)
    _print_result(result, args)


def cmd_guide(args):
    dg = DestinationGuide(agent_type='international')
    if args.country:
        result = dg.get_international_info(args.country)
        _print_result(result, args)
    elif args.customs:
        result = dg.get_customs(args.city)
    elif args.emergency:
        result = dg.get_emergency(args.city)
    else:
        result = dg.get_full_guide(args.city)
    _print_result(result, args)
    if args.save:
        path = dg.save_json(result, f"guide_{args.city}")
        print(f"✅ 已保存: {path}")


def cmd_intel(args):
    ih = IntelligenceHub(agent_type='international')
    result = ih.assess(args.city, args.type or 'destination')
    _print_result(result, args)


def cmd_search(args):
    ih = IntelligenceHub(agent_type='international')
    result = ih.search_travel_info(args.query)
    _print_result(result, args)


def _print_result(result, args):
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, dict) and result.get('status') == 'error':
        print(f"❌ {result.get('message')}")


def main():
    parser = argparse.ArgumentParser(description='太一旅游探路者 v2.0 - 国际游 Agent')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    parser.add_argument('--save', action='store_true', help='保存到文件')
    sub = parser.add_subparsers(dest='command', required=True)

    p = sub.add_parser('plan', help='行程规划')
    p.add_argument('--city', required=True)
    p.add_argument('--country')
    p.add_argument('--days', type=int, default=5)
    p.add_argument('--budget', type=float, default=10000)
    p.add_argument('--preferences', default='综合')
    p.add_argument('--with-hotels', action='store_true')
    p.add_argument('--with-restaurants', action='store_true')

    p = sub.add_parser('weather', help='天气')
    p.add_argument('--city', required=True)
    p.add_argument('--month', type=int, default=0)
    p.add_argument('--advice', action='store_true')

    p = sub.add_parser('guide', help='目的地指南')
    p.add_argument('--city')
    p.add_argument('--country')
    p.add_argument('--customs', action='store_true')
    p.add_argument('--emergency', action='store_true')

    p = sub.add_parser('intel', help='综合情报')
    p.add_argument('--city', required=True)
    p.add_argument('--type', default='destination')

    p = sub.add_parser('search', help='搜索')
    p.add_argument('--query', required=True)

    args = parser.parse_args()

    commands = {
        'plan': cmd_plan,
        'weather': cmd_weather,
        'guide': cmd_guide,
        'intel': cmd_intel,
        'search': cmd_search,
    }
    cmd_fn = commands.get(args.command)
    if cmd_fn:
        cmd_fn(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
