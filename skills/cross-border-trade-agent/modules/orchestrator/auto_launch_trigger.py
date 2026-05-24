#!/usr/bin/env python3
"""
太一·冷启动自动触发器 v1.0
P0 改进#3：buyer-intel 新线索 → 自动触发冷启动评估

工作流：
  buyer-intel (data update)
    → auto_launch_trigger.py (匹配触发规则)
      → orchestrator.launch (冷启动编排)
        → Telegram 推送 / profile 更新

触发规则（TRIGGER_RULES）：
  1. 新买家线索 & 预算>5M USD → 全量冷启动
  2. 竞品发布新品 → 快速竞争分析
  3. 政策法规变更 → 合规冷启动

执行：
  python3 auto_launch_trigger.py --check   # 检查所有规则
  python3 auto_launch_trigger.py --dry-run # 模拟触发，不执行

Cron（OpenClaw cron）：
  0 7,19 * * 1-5 → auto_launch_trigger.py --check   # 工作日早晚各一次
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# 路径
SKILL_DIR = Path(__file__).resolve().parent.parent
BUYER_FILE = SKILL_DIR / "modules/buyer-intel/data/buyers.md"
COMPETITOR_FILE = SKILL_DIR / "data/real_companies.md"
OUTPUT_DIR = SKILL_DIR / "data/.trigger_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TRIGGER_LOG = OUTPUT_DIR / "trigger_log.json"

# ── 触发规则 ───────────────────────────
TRIGGER_RULES = [
    {
        "id": "TRG-001",
        "name": "高价值新线索",
        "condition": lambda buyer: (
            buyer.get("confirmed", False)
            and buyer.get("budget_usd", 0) and buyer["budget_usd"] > 5_000_000
        ),
        "action": "orchestrator.launch(mode=full)",
        "priority": "high",
    },
    {
        "id": "TRG-002",
        "name": "竞品变化检测",
        "condition": lambda comp: comp.get("changed_since_last", False),
        "action": "orchestrator.launch(mode=competitive)",
        "priority": "medium",
    },
    {
        "id": "TRG-003",
        "name": "战略买家跟进提醒",
        "condition": lambda buyer: (
            buyer.get("confirmed", False)
            and "劳工营" in str(buyer.get("procurement_needs", []))
        ),
        "action": "guike-zhilu.search-outreach",
        "priority": "high",
    },
]


def load_buyers() -> list:
    """从 buyers.md 加载买家数据"""
    if not BUYER_FILE.exists():
        return []
    text = BUYER_FILE.read_text()
    # 尝试 JSON 解析
    import re
    json_match = re.search(r'\[[\s\S]*\]', text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    return []


def load_competitor_monitor() -> list:
    """加载竞品监控上次报告"""
    report_file = SKILL_DIR / "data/auto_scraper_report.json"
    if report_file.exists():
        try:
            report = json.loads(report_file.read_text())
            return report.get("results", {}).get("competitors", [])
        except (json.JSONDecodeError, KeyError):
            pass
    return []


def check_triggers() -> list:
    """检查所有触发规则，返回触发的动作列表"""
    triggered = []
    buyers = load_buyers()
    competitors = load_competitor_monitor()

    for rule in TRIGGER_RULES:
        rule_id = rule["id"]
        rule_name = rule["name"]

        if "劳工营" in rule_name or "高价值" in rule_name:
            # 买家规则
            for buyer in buyers[:50]:  # 限制数量
                try:
                    if rule["condition"](buyer):
                        triggered.append({
                            "rule_id": rule_id,
                            "rule_name": rule_name,
                            "triggered_by": buyer.get("project_name", "unknown"),
                            "action": rule["action"],
                            "priority": rule["priority"],
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        })
                        break  # 同一规则只触发一次
                except Exception:
                    continue

        elif "竞品" in rule_name:
            for comp in competitors:
                if rule["condition"](comp):
                    triggered.append({
                        "rule_id": rule_id,
                        "rule_name": rule_name,
                        "triggered_by": comp.get("name", "unknown"),
                        "action": rule["action"],
                        "priority": rule["priority"],
                    })

    return triggered


def execute_actions(triggered: list, dry_run: bool = True):
    """执行（或模拟）触发动作 — 实际调用 orchestrator.launch()"""
    log_entries = []

    for t in triggered:
        entry = {
            **t,
            "executed": not dry_run,
            "dry_run": dry_run,
        }
        log_entries.append(entry)

        product = "钢结构/模块化建筑"  # 从画像或上下文中取
        market = "澳大利亚"

        if dry_run:
            print(f"[DRY-RUN] 🎯 {t['rule_id']} {t['rule_name']}")
            print(f"         触发源: {t.get('triggered_by', 'N/A')}")
            print(f"         动作: {t['action']} (product={product}, market={market})")
            print(f"         优先级: {t['priority']}")
            print()
        else:
            print(f"[EXEC] 🚀 {t['rule_id']} {t['rule_name']} → launching...")
            try:
                # 实际调用 orchestrator.launch()
                sys.path.insert(0, str(SKILL_DIR / "modules/orchestrator"))
                from launch_engine import LaunchOrchestrator
                engine = LaunchOrchestrator()
                result = engine.launch(product, market, mode="quick")
                entry["result"] = "done"
                print(f"       ✅ 冷启动完成: {result.get('task_id', 'unknown')}")
            except Exception as e:
                entry["result"] = f"failed: {e}"
                print(f"       ❌ 冷启动失败: {e}")

    # 保存日志
    history = []
    if TRIGGER_LOG.exists():
        try:
            history = json.loads(TRIGGER_LOG.read_text())
        except json.JSONDecodeError:
            pass
    history.extend(log_entries)
    history = history[-100:]  # 保留最近100条
    TRIGGER_LOG.write_text(json.dumps(history, indent=2, ensure_ascii=False))

    return log_entries


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="冷启动自动触发器")
    parser.add_argument("--check", action="store_true", help="检查所有规则")
    parser.add_argument("--dry-run", action="store_true", default=True, help="模拟（默认）")
    parser.add_argument("--exec", action="store_true", help="实际执行")
    parser.add_argument("--history", action="store_true", help="查看历史触发记录")
    args = parser.parse_args()

    if args.history:
        if TRIGGER_LOG.exists():
            log = json.loads(TRIGGER_LOG.read_text())
            for entry in log[-10:]:
                status = "✅" if entry.get("executed") else "🔍"
                print(f"{status} [{entry['timestamp'][:16]}] {entry['rule_name']} → {entry.get('triggered_by','')}")
        sys.exit(0)

    dry_run = not args.exec  # 默认 dry_run
    triggered = check_triggers()

    if not triggered:
        print("🔍 未触发任何规则。一切正常。")
        sys.exit(0)

    print(f"🎯 触发 {len(triggered)} 条规则:")
    print()

    results = execute_actions(triggered, dry_run=dry_run)

    if dry_run:
        print(f"--- 模拟完成 ({len(results)} 条)。使用 --exec 实际执行 ---")
    else:
        print(f"--- 执行完成 ({len(results)} 条) ---")
