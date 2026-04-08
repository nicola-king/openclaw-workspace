#!/usr/bin/env python3
"""
响应时间监控脚本
记录每次 session 的响应时间，用于实验数据收集

用法：
    python3 response-monitor.py --log --session_id=xxx
"""

import os
import json
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DATA_FILE = WORKSPACE / "data" / "response-times.json"
CACHE_ENABLED_FILE = WORKSPACE / "data" / "cache-enabled.flag"


def is_cache_enabled():
    """检查缓存是否启用"""
    return CACHE_ENABLED_FILE.exists()


def enable_cache():
    """启用缓存"""
    CACHE_ENABLED_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_ENABLED_FILE.touch()
    print("✅ 缓存已启用")


def disable_cache():
    """禁用缓存"""
    if CACHE_ENABLED_FILE.exists():
        CACHE_ENABLED_FILE.unlink()
    print("❌ 缓存已禁用")


def log_response_time(session_id, response_time_ms, cache_enabled):
    """记录响应时间"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"records": []}
    
    record = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "response_time_ms": response_time_ms,
        "cache_enabled": cache_enabled,
        "group": "B" if cache_enabled else "A"
    }
    
    data["records"].append(record)
    
    # 保留最近 1000 条记录
    if len(data["records"]) > 1000:
        data["records"] = data["records"][-1000:]
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"📊 已记录：{response_time_ms}ms (缓存：{'是' if cache_enabled else '否'})")


def get_stats():
    """获取统计数据"""
    if not DATA_FILE.exists():
        return {"error": "无数据"}
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = data["records"]
    
    if not records:
        return {"error": "无记录"}
    
    # 分组统计
    group_a = [r for r in records if not r["cache_enabled"]]
    group_b = [r for r in records if r["cache_enabled"]]
    
    def calc_stats(group, name):
        if not group:
            return None
        
        times = [r["response_time_ms"] for r in group]
        return {
            "group": name,
            "count": len(times),
            "avg_ms": round(sum(times) / len(times), 2),
            "min_ms": min(times),
            "max_ms": max(times),
        }
    
    stats_a = calc_stats(group_a, "A (无缓存)")
    stats_b = calc_stats(group_b, "B (有缓存)")
    
    result = {
        "group_a": stats_a,
        "group_b": stats_b,
    }
    
    if stats_a and stats_b:
        improvement = ((stats_a["avg_ms"] - stats_b["avg_ms"]) / stats_a["avg_ms"]) * 100
        result["improvement"] = f"{improvement:.1f}%"
    
    return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="响应时间监控")
    parser.add_argument("--log", type=int, help="记录响应时间（毫秒）")
    parser.add_argument("--session-id", default="unknown", help="Session ID")
    parser.add_argument("--enable", action="store_true", help="启用缓存")
    parser.add_argument("--disable", action="store_true", help="禁用缓存")
    parser.add_argument("--stats", action="store_true", help="查看统计")
    
    args = parser.parse_args()
    
    if args.enable:
        enable_cache()
    
    elif args.disable:
        disable_cache()
    
    elif args.log:
        cache_enabled = is_cache_enabled()
        log_response_time(args.session_id, args.log, cache_enabled)
    
    elif args.stats:
        stats = get_stats()
        print("\n【响应时间统计】")
        
        if "error" in stats:
            print(f"错误：{stats['error']}")
        else:
            if stats["group_a"]:
                a = stats["group_a"]
                print(f"\nA 组（无缓存）:")
                print(f"  样本数：{a['count']}")
                print(f"  平均：{a['avg_ms']}ms")
                print(f"  范围：{a['min_ms']}ms - {a['max_ms']}ms")
            
            if stats["group_b"]:
                b = stats["group_b"]
                print(f"\nB 组（有缓存）:")
                print(f"  样本数：{b['count']}")
                print(f"  平均：{b['avg_ms']}ms")
                print(f"  范围：{b['min_ms']}ms - {b['max_ms']}ms")
            
            if "improvement" in stats:
                print(f"\n🚀 性能提升：{stats['improvement']}")
    
    else:
        cache_status = "✅ 已启用" if is_cache_enabled() else "❌ 已禁用"
        print(f"响应时间监控")
        print(f"缓存状态：{cache_status}")
        print(f"\n用法:")
        print(f"  --log <ms> --session-id <id>  # 记录响应时间")
        print(f"  --enable                      # 启用缓存")
        print(f"  --disable                     # 禁用缓存")
        print(f"  --stats                       # 查看统计")


if __name__ == "__main__":
    main()
