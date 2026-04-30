#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 供应商 CLI 入口
"""

import argparse
import sys
from src.provider.models import Provider, ProviderType
from src.provider.registry import ProviderRegistry


class ProviderCLI:
    """供应商管理 CLI"""

    def __init__(self):
        self.registry = ProviderRegistry()

    def run(self, args: list = None) -> None:
        parser = argparse.ArgumentParser(description="太一旅行供应商管理")
        subparsers = parser.add_subparsers(dest="action")

        # register
        reg = subparsers.add_parser("register", help="注册供应商")
        reg.add_argument("type", choices=[t.value for t in ProviderType])
        reg.add_argument("--name", required=True)
        reg.add_argument("--location", required=True)
        reg.add_argument("--rating", type=float, default=0)
        reg.add_argument("--price", type=float, default=0)

        # list
        lst = subparsers.add_parser("list", help="列出供应商")
        lst.add_argument("type", choices=[t.value for t in ProviderType])
        lst.add_argument("--location", default=None)

        # approve
        apr = subparsers.add_parser("approve", help="审核供应商")
        apr.add_argument("type", choices=[t.value for t in ProviderType])
        apr.add_argument("provider_id")

        parsed = parser.parse_args(args)

        if not parsed.action:
            parser.print_help()
            return

        if parsed.action == "register":
            provider = Provider(
                name=parsed.name,
                provider_type=ProviderType(parsed.type),
                location=parsed.location,
                rating=parsed.rating,
                price=parsed.price,
            )
            result = self.registry.register(provider)
            print(f"✅ 注册成功: {result.id}")

        elif parsed.action == "list":
            providers = self.registry.list_providers(ProviderType(parsed.type), parsed.location)
            print(f"共 {len(providers)} 个供应商:")
            for p in providers[:10]:
                print(f"  - {p.name} ({p.location}) [{p.status.value}]")

        elif parsed.action == "approve":
            ok = self.registry.approve(ProviderType(parsed.type), parsed.provider_id)
            print(f"{'✅ 审核通过' if ok else '❌ 未找到'}")


def main() -> None:
    cli = ProviderCLI()
    cli.run()


if __name__ == "__main__":
    main()








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48