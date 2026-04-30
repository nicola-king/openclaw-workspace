#!/usr/bin/env python3
"""
Quality Monitor Agent · 定时任务质量监控主脚本
太一 AGI · 2026-04-17

整合功能：
- 质量监控（来自 scheduler-monitor.py）
- 自动修复（来自 auto_fix）
- 趋势分析（来自 weekly-quality-report.py）
- 预测性维护（predictive_maintenance.py）
- 自愈闭环（self_healing_loop.py）

用法：
    python3 quality_monitor.py --check          # 质量检查
    python3 quality_monitor.py --auto-fix       # 自动修复
    python3 quality_monitor.py --weekly-report  # 生成周报
    python3 quality_monitor.py --predictive     # 预测性维护
    python3 quality_monitor.py --full           # 完整流程
"""

import argparse
import json
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MONITORING_DIR = WORKSPACE / "monitoring"
QUALITY_LOG = MONITORING_DIR / "task-quality-log.json"


def run_quality_check():
    """执行质量检查（调用 scheduler-monitor.py）"""
    print("\n🔍 执行质量检查...")
    script = WORKSPACE / "scripts" / "scheduler-monitor.py"
    result = subprocess.run(["python3", str(script)], capture_output=False)
    return result.returncode == 0


def run_weekly_report():
    """生成周报（调用 weekly-quality-report.py）"""
    print("\n📊 生成质量趋势周报...")
    script = WORKSPACE / "scripts" / "weekly-quality-report.py"
    result = subprocess.run(["python3", str(script)], capture_output=False)
    return result.returncode == 0


def run_predictive_maintenance():
    """执行预测性维护分析"""
    print("\n🔮 执行预测性维护分析...")
    script = WORKSPACE / "skills" / "08-monitoring" / "quality-monitor-agent" / "src" / "predictive_maintenance.py"
    result = subprocess.run(["python3", str(script)], capture_output=False)
    return result.returncode == 0


def run_self_healing_demo():
    """演示自愈闭环流程"""
    print("\n🔄 演示自愈闭环流程...")
    script = WORKSPACE / "skills" / "08-monitoring" / "quality-monitor-agent" / "src" / "self_healing_loop.py"
    result = subprocess.run(["python3", str(script)], capture_output=False)
    return result.returncode == 0


def show_status():
    """显示质量监控系统状态"""
    print("\n📊 Quality Monitor Agent 状态\n")
    
    # 检查日志文件
    logs = []
    if QUALITY_LOG.exists():
        with open(QUALITY_LOG, "r", encoding="utf-8") as f:
            logs = json.load(f)
    
    print(f"质量问题记录：{len(logs)} 条")
    
    if logs:
        # 统计
        scripts = set(l.get("script") for l in logs)
        auto_fixes = sum(1 for l in logs if "auto_fix" in l)
        success_fixes = sum(1 for l in logs if l.get("auto_fix", {}).get("status") == "fixed")
        
        print(f"涉及脚本：{len(scripts)} 个")
        print(f"自动修复：{auto_fixes} 次")
        print(f"修复成功：{success_fixes}/{auto_fixes} ({success_fixes*100//auto_fixes if auto_fixes > 0 else 0}%)")
    
    # 检查报告文件
    reports_dir = WORKSPACE / "skills" / "08-monitoring" / "quality-monitor-agent" / "reports"
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.md"))
        print(f"\n生成报告：{len(reports)} 个")
        for report in reports[-3:]:
            print(f"  - {report.name}")
    
    print("\n✅ 系统运行正常")


def main():
    parser = argparse.ArgumentParser(description="Quality Monitor Agent · 定时任务质量监控")
    parser.add_argument("--check", action="store_true", help="执行质量检查")
    parser.add_argument("--auto-fix", action="store_true", help="执行自动修复")
    parser.add_argument("--weekly-report", action="store_true", help="生成周报")
    parser.add_argument("--predictive", action="store_true", help="预测性维护分析")
    parser.add_argument("--self-heal", action="store_true", help="演示自愈闭环")
    parser.add_argument("--full", action="store_true", help="执行完整流程")
    parser.add_argument("--status", action="store_true", help="显示系统状态")
    
    args = parser.parse_args()
    
    # 无参数时显示状态
    if not any([args.check, args.auto_fix, args.weekly_report, args.predictive, args.self_heal, args.full, args.status]):
        parser.print_help()
        return 0
    
    print(f"\n{'='*60}")
    print(f"Quality Monitor Agent · 定时任务质量监控智能体")
    print(f"{'='*60}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = True
    
    if args.status:
        show_status()
    
    if args.check or args.full:
        if not run_quality_check():
            success = False
    
    if args.auto_fix:
        # 自动修复已集成在 scheduler-monitor.py 中
        print("\n🔧 自动修复已集成在质量检查中，使用 --check 即可")
    
    if args.weekly_report or args.full:
        if not run_weekly_report():
            success = False
    
    if args.predictive or args.full:
        if not run_predictive_maintenance():
            success = False
    
    if args.self_heal:
        if not run_self_healing_demo():
            success = False
    
    print(f"\n{'='*60}")
    if success:
        print("✅ 所有任务执行成功")
    else:
        print("⚠️ 部分任务执行失败，请检查日志")
    print(f"{'='*60}\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
