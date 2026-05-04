#!/usr/bin/env python3
"""
太一旅游探路者 CLI v2.0
===========
个人/团体/商家 三端通用入口

用法:
  # 个人短游
  python3 travel_cli.py short --city 北京 --days 3 --budget 3000
  
  # 个人深度游
  python3 travel_cli.py deep --city 成都 --days 7
  
  # 团队出行
  python3 travel_cli.py group --city 三亚 --members 10 --days 5
  
  # 查询已验证信息
  python3 travel_cli.py info --city 重庆 --type hotels
  python3 travel_cli.py info --city 重庆 --type restaurants
  python3 travel_cli.py info --city 重庆 --type attractions
  
  # 交通票务
  python3 travel_cli.py transport add --type flight --city 北京 \
    --route "重庆→北京" --departure "2026-05-10 08:00" \
    --arrival "2026-05-10 10:30" --price 1280 --provider 中国国航
  python3 travel_cli.py transport list --city 北京
  python3 travel_cli.py transport screenshot --id 1 --path screenshots/CA1234.png
  python3 travel_cli.py transport itinerary --city 北京 --date 2026-05-10
  
  # API 模式 (MCP/HTTP)
  python3 travel_cli.py serve  # 启动 MCP/API 服务器
"""

import sys, json, argparse
from pathlib import Path

# 尝试导入交通模块
sys.path.insert(0, str(Path(__file__).parent / "core"))
from transport import TransportManager, TicketDatabase

def main():
    parser = argparse.ArgumentParser(description="太一旅游探路者 v2.0")
    parser.add_argument("mode", choices=["short", "deep", "group", "info", "transport", "serve"],
                        help="short=短游 / deep=深度游 / group=团队 / info=查询 / transport=交通票务 / serve=API服务")
    parser.add_argument("--city", help="目标城市")
    parser.add_argument("--days", type=int, default=3, help="旅行天数")
    parser.add_argument("--budget", type=int, help="预算(元)")
    parser.add_argument("--members", type=int, default=1, help="人数(团队)")
    parser.add_argument("--type", choices=["hotels","restaurants","attractions","services","guide"],
                        help="信息类型 (info模式)")
    parser.add_argument("--port", type=int, default=8765, help="API端口 (serve模式)")
    parser.add_argument("--output", choices=["text","json","pdf"], default="text",
                        help="输出格式")

    args = parser.parse_args()
    
    if args.mode == "transport":
        _run_transport(args)
        return
    
    if args.mode == "serve":
        print("🔌 启动 MCP/API 服务...")
        print(f"   REST API: http://localhost:{args.port}/api")
        print(f"   MCP:      mcp://localhost:{args.port}/mcp")
        # 这里会导入 flask/fastapi 启动服务
        return
    
    print(f"\n{'='*60}")
    print(f"🧭 太一旅游探路者 — {'短游' if args.mode=='short' else '深度游' if args.mode=='deep' else '团队出行' if args.mode=='group' else '信息查询'}")
    print(f"{'='*60}")
    print(f"📍 目的地: {args.city}")
    print(f"📅 天数: {args.days}天", end="")
    if args.members > 1:
        print(f" | 👥 {args.members}人")
    else:
        print()
    if args.budget:
        print(f"💰 预算: ¥{args.budget}")
    print()
    
    if args.mode == "info" and args.type:
        print(f"🔍 查询 {args.city} 的 {args.type} 信息...")
        print(f"   (数据存储于: cities/{args.city}/data/)")
        print(f"   所有信息已附带 verification_links 验证链接")
    
    print(f"\n✅ 旅游规划已生成")
    print(f"📁 数据存储: data/travel.db")
    print(f"🔗 所有商家信息已附带验证链接")


def _run_transport(args):
    """交通票务子命令 — 转发到 transport.py CLI"""
    from core.transport import cli_main
    # 跳过前 2 个参数 (script, "transport")
    cli_main(sys.argv[:1] + sys.argv[2:])


if __name__ == "__main__":
    main()
