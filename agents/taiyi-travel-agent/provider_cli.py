#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅行服务供应商入驻 CLI - Travel Service Provider CLI

功能:
1. 酒店入驻
2. 饭店/餐厅入驻
3. 租车公司入驻
4. 落地导游入驻
5. 落地包车入驻
6. 供应商管理
7. 服务查询

使用方式:
python3 provider_cli.py hotel register --name "XX 酒店" --location "东京" --price 500
python3 provider_cli.py restaurant register --name "XX 餐厅" --location "东京" --cuisine "日本料理"
python3 provider_cli.py car_rental register --name "XX 租车" --location "东京" --car_type "舒适型"
python3 provider_cli.py guide register --name "王导" --location "东京" --language "中文/英文"
python3 provider_cli.py charter register --name "XX 包车" --location "东京" --car_type "舒适型"

作者：太一 AGI
创建：2026-04-14
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
AGENT_DIR = WORKSPACE / "agents" / "taiyi-travel-agent"
PROVIDERS_DIR = AGENT_DIR / "data" / "providers"

# 确保目录存在
PROVIDERS_DIR.mkdir(parents=True, exist_ok=True)


class TravelProviderCLI:
    """旅行服务供应商 CLI"""
    
    def __init__(self):
        self.providers_db = {
            "hotel": PROVIDERS_DIR / "hotels.json",
            "restaurant": PROVIDERS_DIR / "restaurants.json",
            "car_rental": PROVIDERS_DIR / "car_rentals.json",
            "guide": PROVIDERS_DIR / "guides.json",
            "charter": PROVIDERS_DIR / "charters.json",
        }
        
        # 初始化数据库
        for provider_type, db_file in self.providers_db.items():
            if not db_file.exists():
                with open(db_file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_providers(self, provider_type: str) -> List[Dict]:
        """加载供应商数据"""
        db_file = self.providers_db.get(provider_type)
        if not db_file or not db_file.exists():
            return []
        
        with open(db_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_providers(self, provider_type: str, providers: List[Dict]):
        """保存供应商数据"""
        db_file = self.providers_db.get(provider_type)
        if not db_file:
            return
        
        with open(db_file, 'w', encoding='utf-8') as f:
            json.dump(providers, f, ensure_ascii=False, indent=2)
    
    def register_provider(self, provider_type: str, **kwargs):
        """注册供应商"""
        print(f"\n📝 注册{provider_type}供应商")
        
        # 创建供应商记录
        provider = {
            "id": f"{provider_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": provider_type,
            "status": "pending",  # pending/approved/rejected
            "registered_at": datetime.now().isoformat(),
            **kwargs
        }
        
        # 加载现有数据
        providers = self._load_providers(provider_type)
        
        # 添加新供应商
        providers.append(provider)
        
        # 保存
        self._save_providers(provider_type, providers)
        
        print(f"  ✅ 注册成功")
        print(f"  ID: {provider['id']}")
        print(f"  名称：{provider.get('name', 'N/A')}")
        print(f"  位置：{provider.get('location', 'N/A')}")
        print(f"  状态：{provider['status']} (待审核)")
        
        return provider
    
    def list_providers(self, provider_type: str, location: str = None):
        """列出供应商"""
        print(f"\n📋 {provider_type}供应商列表")
        
        providers = self._load_providers(provider_type)
        
        # 按位置筛选
        if location:
            providers = [p for p in providers if p.get('location') == location]
        
        print(f"  总数：{len(providers)} 个")
        
        for provider in providers[:10]:  # 只显示前 10 个
            print(f"\n  - {provider.get('name', 'N/A')}")
            print(f"    ID: {provider['id']}")
            print(f"    位置：{provider.get('location', 'N/A')}")
            print(f"    状态：{provider.get('status', 'N/A')}")
            if provider.get('price'):
                print(f"    价格：¥{provider['price']}起")
            if provider.get('rating'):
                print(f"    评分：{provider['rating']}")
    
    def approve_provider(self, provider_type: str, provider_id: str):
        """审核通过供应商"""
        print(f"\n✅ 审核{provider_type}供应商：{provider_id}")
        
        providers = self._load_providers(provider_type)
        
        for provider in providers:
            if provider['id'] == provider_id:
                provider['status'] = 'approved'
                provider['approved_at'] = datetime.now().isoformat()
                self._save_providers(provider_type, providers)
                print(f"  ✅ 审核通过")
                return
        
        print(f"  ❌ 未找到供应商：{provider_id}")
    
    def search_providers(self, provider_type: str, **kwargs):
        """搜索供应商"""
        print(f"\n🔍 搜索{provider_type}供应商")
        
        providers = self._load_providers(provider_type)
        
        # 只搜索已审核通过的
        providers = [p for p in providers if p.get('status') == 'approved']
        
        # 筛选
        for key, value in kwargs.items():
            if value:
                providers = [p for p in providers if p.get(key) == value]
        
        print(f"  找到：{len(providers)} 个")
        
        # 按评分排序
        providers.sort(key=lambda x: x.get('rating', 0), reverse=True)
        
        return providers[:10]  # 返回前 10 个


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='太一旅行服务供应商入驻 CLI')
    
    subparsers = parser.add_subparsers(dest='provider_type', help='供应商类型')
    
    # 酒店
    hotel_parser = subparsers.add_parser('hotel', help='酒店服务')
    hotel_subparsers = hotel_parser.add_subparsers(dest='action')
    
    hotel_register = hotel_subparsers.add_parser('register', help='注册酒店')
    hotel_register.add_argument('--name', required=True, help='酒店名称')
    hotel_register.add_argument('--location', required=True, help='位置')
    hotel_register.add_argument('--price', type=float, required=True, help='价格 (元起)')
    hotel_register.add_argument('--rating', type=float, default=0, help='评分')
    hotel_register.add_argument('--amenities', nargs='*', help='设施')
    
    hotel_list = hotel_subparsers.add_parser('list', help='列出酒店')
    hotel_list.add_argument('--location', help='位置筛选')
    
    hotel_search = hotel_subparsers.add_parser('search', help='搜索酒店')
    hotel_search.add_argument('--location', help='位置')
    hotel_search.add_argument('--max_price', type=float, help='最高价格')
    
    # 餐厅
    restaurant_parser = subparsers.add_parser('restaurant', help='餐厅服务')
    restaurant_subparsers = restaurant_parser.add_subparsers(dest='action')
    
    restaurant_register = restaurant_subparsers.add_parser('register', help='注册餐厅')
    restaurant_register.add_argument('--name', required=True, help='餐厅名称')
    restaurant_register.add_argument('--location', required=True, help='位置')
    restaurant_register.add_argument('--cuisine', required=True, help='菜系')
    restaurant_register.add_argument('--price_range', help='价格区间')
    restaurant_register.add_argument('--rating', type=float, default=0, help='评分')
    
    restaurant_list = restaurant_subparsers.add_parser('list', help='列出餐厅')
    restaurant_list.add_argument('--location', help='位置筛选')
    
    # 租车
    car_rental_parser = subparsers.add_parser('car_rental', help='租车服务')
    car_rental_subparsers = car_rental_parser.add_subparsers(dest='action')
    
    car_rental_register = car_rental_subparsers.add_parser('register', help='注册租车公司')
    car_rental_register.add_argument('--name', required=True, help='公司名称')
    car_rental_register.add_argument('--location', required=True, help='位置')
    car_rental_register.add_argument('--car_types', nargs='*', help='车型')
    car_rental_register.add_argument('--price_per_day', type=float, required=True, help='日租金 (元起)')
    car_rental_register.add_argument('--rating', type=float, default=0, help='评分')
    
    car_rental_list = car_rental_subparsers.add_parser('list', help='列出租车公司')
    car_rental_list.add_argument('--location', help='位置筛选')
    
    # 导游
    guide_parser = subparsers.add_parser('guide', help='导游服务')
    guide_subparsers = guide_parser.add_subparsers(dest='action')
    
    guide_register = guide_subparsers.add_parser('register', help='注册导游')
    guide_register.add_argument('--name', required=True, help='导游姓名')
    guide_register.add_argument('--location', required=True, help='服务位置')
    guide_register.add_argument('--language', required=True, help='语言')
    guide_register.add_argument('--experience', help='经验年限')
    guide_register.add_argument('--price_per_day', type=float, required=True, help='日服务费 (元起)')
    guide_register.add_argument('--rating', type=float, default=0, help='评分')
    
    guide_list = guide_subparsers.add_parser('list', help='列出导游')
    guide_list.add_argument('--location', help='位置筛选')
    
    # 包车
    charter_parser = subparsers.add_parser('charter', help='包车服务')
    charter_subparsers = charter_parser.add_subparsers(dest='action')
    
    charter_register = charter_subparsers.add_parser('register', help='注册包车公司')
    charter_register.add_argument('--name', required=True, help='公司名称')
    charter_register.add_argument('--location', required=True, help='服务位置')
    charter_register.add_argument('--car_types', nargs='*', help='车型')
    charter_register.add_argument('--price_per_day', type=float, required=True, help='日租金 (元起)')
    charter_register.add_argument('--rating', type=float, default=0, help='评分')
    
    charter_list = charter_subparsers.add_parser('list', help='列出包车公司')
    charter_list.add_argument('--location', help='位置筛选')
    
    # 审核 (移到最外层)
    # approve 命令不使用 subparsers
    
    args = parser.parse_args()
    
    if not args.provider_type:
        parser.print_help()
        return
    
    cli = TravelProviderCLI()
    
    # 审核 (特殊处理)
    if args.provider_type == 'approve':
        return
    
    # 注册
    if hasattr(args, 'action') and args.action == 'register':
        kwargs = {k: v for k, v in vars(args).items() if k not in ['provider_type', 'action']}
        cli.register_provider(args.provider_type, **kwargs)
    # 列出
    elif hasattr(args, 'action') and args.action == 'list':
        cli.list_providers(args.provider_type, args.location if hasattr(args, 'location') else None)
    # 搜索
    elif hasattr(args, 'action') and args.action == 'search':
        providers = cli.search_providers(args.provider_type, location=args.location if hasattr(args, 'location') else None)
        for p in providers:
            print(f"  - {p.get('name')} (评分：{p.get('rating', 0)})")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
