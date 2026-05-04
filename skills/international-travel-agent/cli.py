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

sys.path.insert(0, str(Path(__file__).parent / "core"))
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
from transport import TransportManager, TicketDatabase


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


def cmd_transport(args):
    """国际交通票务命令"""
    mgr = TransportManager()
    if args.add:
        ticket_id = mgr.db.add_ticket(
            city=args.city, ticket_type=args.type, provider=args.provider or '',
            route=args.route or '', departure_time=args.departure or '',
            arrival_time=args.arrival or '', price=args.price or 0,
            confirmation_no=args.confirmation or '', status=args.status or 'booked',
        )
        print(f"✅ 已添加国际票务 #{ticket_id}")
        ticket = mgr.get_ticket(ticket_id)
        if args.json:
            print(json.dumps(ticket, indent=2, ensure_ascii=False))
        else:
            print(mgr.format_ticket(ticket))
    elif args.list:
        tickets = mgr.list_tickets(args.city, args.type, args.status)
        if args.json:
            print(json.dumps(tickets, indent=2, ensure_ascii=False))
        else:
            print(mgr.format_ticket_list(tickets))
    elif args.itinerary:
        from datetime import datetime
        date = args.date or datetime.now().strftime("%Y-%m-%d")
        it = mgr.get_itinerary_transport(args.city, date)
        if args.json:
            print(json.dumps(it, indent=2, ensure_ascii=False))
        else:
            print(mgr.format_itinerary(it))
    elif args.screenshot:
        mgr.add_screenshot(args.id, args.screenshot, args.ocr or '')
        print(f"✅ 截图已添加到票务 #{args.id}")
    elif args.get:
        ticket = mgr.get_ticket(args.id)
        if args.json:
            print(json.dumps(ticket, indent=2, ensure_ascii=False))
        elif ticket:
            print(mgr.format_ticket(ticket))
        else:
            print(f"❌ 票务 #{args.id} 不存在")
    elif args.stats:
        db = TicketDatabase()
        stats = db.get_statistics(args.city)
        if args.json:
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            print(f"\n📊 {args.city or '全部'} 国际票务统计")
            print(f"{'='*40}")
            print(f"  总票数: {stats['total']}")
            for ttype, count in stats['by_type'].items():
                label = TransportManager.TICKET_TYPE_LABELS.get(ttype, ttype)
                print(f"  {label}: {count} 张")
    elif args.delete:
        db = TicketDatabase()
        ticket = db.get_ticket(args.id)
        if ticket:
            label = TransportManager.TICKET_TYPE_LABELS.get(ticket['type'], '票务')
            print(f"🗑️  删除 {label}: {ticket.get('route', '')}")
            db.delete_ticket(args.id)
            print(f"✅ 已删除")
        else:
            print(f"❌ 票务 #{args.id} 不存在")


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

    p = sub.add_parser('transport', help='国际交通票务管理')
    p.add_argument('--add', action='store_true', help='添加票务')
    p.add_argument('--list', action='store_true', help='列出票务')
    p.add_argument('--get', type=int, help='查看单张票务 ID')
    p.add_argument('--screenshot', help='添加截图路径')
    p.add_argument('--ocr', help='OCR文本')
    p.add_argument('--itinerary', action='store_true', help='行程交通概览')
    p.add_argument('--stats', action='store_true', help='票务统计')
    p.add_argument('--delete', type=int, help='删除票务 ID')
    p.add_argument('--city', default='', help='城市')
    p.add_argument('--type', choices=['flight','train','ferry','bus',''],
                   default='', help='票务类型')
    p.add_argument('--route', help='路线 出发地→目的地')
    p.add_argument('--provider', help='提供商')
    p.add_argument('--departure', help='出发时间')
    p.add_argument('--arrival', help='到达时间')
    p.add_argument('--price', type=float, help='价格')
    p.add_argument('--confirmation', help='订单号/票号')
    p.add_argument('--status', default='booked', help='状态')
    p.add_argument('--date', help='日期 (itinerary模式)')
    p.add_argument('--id', type=int, help='票务 ID (screenshot/get/delete)')

    args = parser.parse_args()

    commands = {
        'plan': cmd_plan,
        'weather': cmd_weather,
        'guide': cmd_guide,
        'intel': cmd_intel,
        'transport': cmd_transport,
        'search': cmd_search,
    }
    cmd_fn = commands.get(args.command)
    if cmd_fn:
        cmd_fn(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
