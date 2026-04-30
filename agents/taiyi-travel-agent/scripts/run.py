#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
太一旅行探路者 - 统一入口脚本

用法:
    python3 scripts/run.py plan --origin 北京 --destination 东京 --start 2026-05-01 --end 2026-05-07 --budget 15000
    python3 scripts/run.py route --cities 北京,东京,首尔
    python3 scripts/run.py deals --origin 北京 --destination 东京
    python3 scripts/run.py ground --destination 东京 --service charter
    python3 scripts/run.py evolve
    python3 scripts/run.py learn --source mafengwo --destination 东京
"""

import argparse
import json
import sys
from pathlib import Path

# 确保可以导入 src

AGENT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(AGENT_DIR))

from src.router import TravelRouter
from src.planner.engine import PlannerEngine
from src.planner.budget import BudgetManager
from src.planner.checklist import ChecklistGenerator
from src.evolve.experience_store import ExperienceStore
from src.evolve.pattern_recognition import PatternRecognizer
from src.evolve.emergence_detector import EmergenceDetector


def cmd_plan(args):
    """行程规划"""
    planner = PlannerEngine()
    budget_mgr = BudgetManager()
    checklist = ChecklistGenerator()

    plan = planner.plan_trip(
        origin=args.origin,
        destination=args.destination,
        start_date=args.start,
        end_date=args.end,
        budget=args.budget,
        travelers=args.travelers or 2,
    )

    allocation = budget_mgr.allocate(budget=args.budget, days=args.days or 5, travelers=args.travelers or 2)
    items = checklist.generate(destination=args.destination, days=args.days or 5)

    result = {
        "plan": plan,
        "budget_allocation": allocation,
        "checklist": items,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def cmd_route(args):
    """路线优化"""
    from src.router_core.optimizer import RouteOptimizer
    optimizer = RouteOptimizer()
    cities = [c.strip() for c in args.cities.split(",")]
    route = optimizer.optimize(cities=cities, mode=args.mode or "balanced")
    print(json.dumps(route, ensure_ascii=False, indent=2))
    return route


def cmd_deals(args):
    """优惠发现"""
    from src.deals.finder import DealFinder
    finder = DealFinder()
    deals = finder.find_deals(origin=args.origin, destination=args.destination)
    print(json.dumps(deals, ensure_ascii=False, indent=2))
    return deals


def cmd_ground(args):
    """地接服务"""
    service_map = {
        "charter": ("src.ground.charter", "CharterService"),
        "pickup": ("src.ground.airport_pickup", "AirportPickupService"),
        "guide": ("src.ground.guide", "GuideService"),
        "rental": ("src.ground.car_rental", "CarRentalService"),
        "package": ("src.ground.packages", "PackageService"),
    }
    module_name, class_name = service_map[args.service]
    __import__(module_name)
    module = sys.modules[module_name]
    cls = getattr(module, class_name)
    service = cls()
    results = service.search(destination=args.destination)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results


def cmd_evolve(args):
    """自进化"""
    store = ExperienceStore()
    recognizer = PatternRecognizer(store)
    detector = EmergenceDetector(store)

    patterns = recognizer.analyze()
    signals = detector.detect_all()

    result = {"patterns": patterns, "emergence_signals": signals}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def cmd_learn(args):
    """知识学习"""
    from src.learn.blogger import BloggerLearner
    from src.learn.website import WebsiteLearner

    if args.source in ("小红书", "抖音", "微博"):
        learner = BloggerLearner()
        result = learner.learn(source=args.source, destination=args.destination)
    else:
        learner = WebsiteLearner()
        result = learner.learn(source=args.source, destination=args.destination)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description="太一旅行探路者 Agent v2.0")
    subparsers = parser.add_subparsers(dest="command")

    # plan
    p_plan = subparsers.add_parser("plan", help="行程规划")
    p_plan.add_argument("--origin", required=True)
    p_plan.add_argument("--destination", required=True)
    p_plan.add_argument("--start", required=True)
    p_plan.add_argument("--end", required=True)
    p_plan.add_argument("--budget", type=float, required=True)
    p_plan.add_argument("--travelers", type=int, default=2)
    p_plan.add_argument("--days", type=int, default=5)

    # route
    p_route = subparsers.add_parser("route", help="路线优化")
    p_route.add_argument("--cities", required=True)
    p_route.add_argument("--mode", default="balanced")

    # deals
    p_deals = subparsers.add_parser("deals", help="优惠发现")
    p_deals.add_argument("--origin", required=True)
    p_deals.add_argument("--destination", required=True)

    # ground
    p_ground = subparsers.add_parser("ground", help="地接服务")
    p_ground.add_argument("--destination", required=True)
    p_ground.add_argument("--service", required=True, choices=["charter", "pickup", "guide", "rental", "package"])

    # evolve
    subparsers.add_parser("evolve", help="自进化")

    # learn
    p_learn = subparsers.add_parser("learn", help="知识学习")
    p_learn.add_argument("--source", required=True)
    p_learn.add_argument("--destination", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "plan": cmd_plan,
        "route": cmd_route,
        "deals": cmd_deals,
        "ground": cmd_ground,
        "evolve": cmd_evolve,
        "learn": cmd_learn,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()


---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48