#!/usr/bin/env bash
# Token & Cost Monitor v3 — 按平台/按天/按月全量统计
set -e

WORKSPACE="/home/sayelf/.openclaw/workspace"
DATA_DIR="$WORKSPACE/data/token-monitor"
STORE="/home/sayelf/.openclaw/agents/main/sessions/sessions.json"
mkdir -p "$DATA_DIR"

[ ! -f "$STORE" ] && echo "⚠️ 会话存储文件不存在" && exit 1

python3 << 'PYEOF'
import json, os, sys, time
from datetime import datetime, timezone
from collections import defaultdict

STORE = os.path.expanduser("~/.openclaw/agents/main/sessions/sessions.json")
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/data/token-monitor")
os.makedirs(DATA_DIR, exist_ok=True)

with open(STORE) as f:
    data = json.load(f)

# Platform groupings
PLATFORMS = {
    "deepseek": ["deepseek", "deepseek-v4-flash", "deepseek-v4-pro", "deepseek-chat"],
    "moonshot": ["moonshot", "kimi", "kimi-k2.6"],
    "qwen": ["qwen", "qwen3", "qwen-max"],
    "gemini": ["gemini", "google"],
}

def classify_platform(model):
    """Classify model into platform group"""
    ml = (model or "").lower()
    for plat, models in PLATFORMS.items():
        for m in models:
            if m in ml:
                return plat
    return "other"

now = time.time() * 1000

# Aggregate all sessions
by_platform = defaultdict(lambda: {"sessions": 0, "in": 0, "out": 0, "tokens": 0, "cost": 0.0})
by_day = defaultdict(lambda: defaultdict(lambda: {"in": 0, "out": 0, "cost": 0.0, "sessions": 0}))
by_agent = defaultdict(lambda: {"in": 0, "out": 0, "cost": 0.0, "sessions": 0})
by_platform_day = defaultdict(lambda: defaultdict(lambda: {"in": 0, "out": 0, "cost": 0.0}))

total_cost = 0.0
total_in = 0
total_out = 0
total_sessions = 0
month_cost = 0.0
today_cost = 0.0

today_str = datetime.now().strftime("%Y-%m-%d")
month_str = datetime.now().strftime("%Y-%m")

for key, s in data.items():
    updated = s.get("updatedAt", 0)
    cost = s.get("estimatedCostUsd", 0.0)
    inp = s.get("inputTokens", 0)
    out = s.get("outputTokens", 0)
    model = s.get("model", "unknown")
    kind = s.get("kind", "unknown")
    agent = s.get("agentId", "unknown")
    day = datetime.fromtimestamp(updated/1000, tz=timezone.utc).strftime("%Y-%m-%d") if updated else "unknown"
    s_month = day[:7] if day != "unknown" else "unknown"

    if not updated or updated < 1719782400000:  # Before July 2025 - ignore ancient
        continue

    plat = classify_platform(model)
    
    # Accumulate
    total_cost += cost
    total_in += inp
    total_out += out
    total_sessions += 1
    
    by_platform[plat]["sessions"] += 1
    by_platform[plat]["in"] += inp
    by_platform[plat]["out"] += out
    by_platform[plat]["tokens"] += inp + out
    by_platform[plat]["cost"] += cost
    
    by_day[day][plat]["in"] += inp
    by_day[day][plat]["out"] += out
    by_day[day][plat]["cost"] += cost
    by_day[day][plat]["sessions"] += 1
    
    by_platform_day[plat][day]["in"] += inp
    by_platform_day[plat][day]["out"] += out
    by_platform_day[plat][day]["cost"] += cost
    
    # Agent categorization (from session key)
    if ":cron:" in key:
        agent_label = "cron"
    elif ":subagent:" in key:
        agent_label = "subagent"
    elif ":telegram:" in key:
        agent_label = "telegram"
    elif ":feishu:" in key:
        agent_label = "feishu"
    elif ":weixin:" in key or "wechat" in key:
        agent_label = "weixin"
    elif ":main" in key:
        agent_label = "direct"
    else:
        agent_label = kind
    
    # Parent agent
    if agent:
        agent_label = agent_label
    
    by_agent[agent_label]["in"] += inp
    by_agent[agent_label]["out"] += out
    by_agent[agent_label]["cost"] += cost
    by_agent[agent_label]["sessions"] += 1
    
    if s_month == month_str:
        month_cost += cost
    if day == today_str:
        today_cost += cost

# ── Print Report ──
print()
print("╔══════════════════════════════════════════════════════════════╗")
print("║           OpenClaw Token 消费监控  v3                       ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()

# 1. Summary
print(f"📊 总览")
print(f"   {''.ljust(24)} TOKENS{'':>12}   费用")
print(f"   {'平台':<16} {'输入':>10} {'输出':>10} {'USD':>10}  {'CNY':>10}")
print(f"   {'─'*60}")
for plat in sorted(by_platform.keys(), key=lambda p: -by_platform[p]["cost"]):
    d = by_platform[plat]
    cny = d["cost"] * 7.3
    print(f"   {plat:<16} {d['in']:>10,} {d['out']:>10,} ${d['cost']:>8.5f}  ¥{cny:>8.4f}")
print(f"   {'─'*60}")
print(f"   {'总计':<16} {total_in:>10,} {total_out:>10,} ${total_cost:>8.5f}  ¥{total_cost*7.3:>8.4f}")
print(f"   总会话: {total_sessions}")
print()

# 2. Daily breakdown
print(f"📅 每日明细（最近14天）")
print(f"   {'日期':<12} {'平台':<12} {'输入':>10} {'输出':>10} {'费用':>10}")
print(f"   {'─'*56}")
sorted_days = sorted(by_day.keys(), reverse=True)[:14]
for day in sorted_days:
    day_plats = by_day[day]
    first = True
    for plat in sorted(day_plats.keys(), key=lambda p: -day_plats[p]["cost"]):
        d = day_plats[plat]
        if first:
            print(f"   {day:<12} {plat:<12} {d['in']:>10,} {d['out']:>10,} ${d['cost']:>8.5f}")
            first = False
        else:
            print(f"   {'':<12} {plat:<12} {d['in']:>10,} {d['out']:>10,} ${d['cost']:>8.5f}")
    day_total = sum(d["cost"] for d in day_plats.values())
    print(f"   {'':<12} {'─小计':<12} {'':>10} {'':>10} ${day_total:>8.5f}")
    print()

# 3. By agent type
print(f"👤 按渠道")
print(f"   {'渠道':<12} {'会话':>6} {'输入':>10} {'输出':>10} {'费用':>10}")
print(f"   {'─'*50}")
for agent in sorted(by_agent.keys(), key=lambda a: -by_agent[a]["cost"]):
    d = by_agent[agent]
    print(f"   {agent:<12} {d['sessions']:>6} {d['in']:>10,} {d['out']:>10,} ${d['cost']:>8.5f}")
print(f"   {'─'*50}")
print(f"   {'总计':<12} {total_sessions:>6} {total_in:>10,} {total_out:>10,} ${total_cost:>8.5f}")
print()

# 4. Monthly cumulative
print(f"📆 {month_str} 月度累计: ${month_cost:.5f} (¥{month_cost*7.3:.4f})")
print(f"   今日 ({today_str}): ${today_cost:.5f} (¥{today_cost*7.3:.4f})")
print()

# 5. DeepSeek account check
try:
    import subprocess
    ds_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if ds_key:
        result = subprocess.run(
            ["curl", "-s", "https://api.deepseek.com/user/balance",
             "-H", f"Authorization: Bearer {ds_key}"],
            capture_output=True, text=True, timeout=5
        )
        bal = json.loads(result.stdout)
        if bal.get("is_available"):
            total = float(bal["balance_infos"][0]["total_balance"])
            print(f"🏦 DeepSeek 账户余额: ¥{total:.2f}")
except:
    pass

print()

# ── Save snapshot for cumulative tracking ──
SNAPSHOT_FILE = os.path.join(DATA_DIR, f"{month_str}.jsonl")
snapshot = {
    "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "total_in": total_in,
    "total_out": total_out,
    "total_cost": round(total_cost, 6),
    "month_cost": round(month_cost, 6),
    "today_cost": round(today_cost, 6),
    "platforms": {k: {"in": v["in"], "out": v["out"], "cost": round(v["cost"], 6)} 
                  for k, v in by_platform.items()},
}
with open(SNAPSHOT_FILE, "a") as f:
    f.write(json.dumps(snapshot, ensure_ascii=False) + "\n")
PYEOF
