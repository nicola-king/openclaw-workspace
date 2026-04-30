#!/usr/bin/env python3
"""
Scheduler Agent 监控告警脚本 v2.0
功能：
1. 每 5 分钟检查 Scheduler Agent 状态
2. 超过 1 小时未执行发送 Telegram 告警
3. 进程不存在时自动重启
4. ✅ 结果验证 - 检查定时任务是否实际创建文件
5. ✅ 虚假成功检测 - 检测"脚本执行成功但文件未创建"
6. ✅ 失败模式记录 - 记录到 memory 触发技能涌现
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MONITORING_DIR = WORKSPACE / "monitoring"
SCHEDULER_LOG = MONITORING_DIR / "scheduler-log.json"
QUALITY_LOG = MONITORING_DIR / "task-quality-log.json"
QUALITY_LOG_FILE = QUALITY_LOG  # 别名，保持一致
ALERT_LOG = MONITORING_DIR / "alert-log.json"  # 告警冷却日志
ALERT_COOLDOWN_MINUTES = 120  # 告警冷却时间：120 分钟 (2 小时)
ALERT_THRESHOLD_HOURS = 1  # 告警阈值：1 小时
CONSECUTIVE_FAILURE_THRESHOLD = 3  # 连续失败阈值：3 次才告警

# 定时任务预期输出文件配置
TASK_OUTPUT_FILES = {
    "daily-report-generator.py": {
        "expected_files": [
            "daily-report-{today}.md",
            "reports/daily-report-{today_nodash}.md",
        ],
        "schedule": "23:00",
        "grace_period_minutes": 5,  # 宽限期
    },
    "daily-constitution-study.py": {
        "expected_files": [
            "reports/constitution-study-{today}.md",
        ],
        "schedule": "06:00",
        "grace_period_minutes": 10,
    },
    "hourly-health-check.py": {
        "expected_files": [
            "reports/health-check-{today_hour}.md",
        ],
        "schedule": "hourly",
        "grace_period_minutes": 5,
    },
    "yijing-daily-study.py": {
        "expected_files": [
            "reports/yijing/yijing-{today}.md",
        ],
        "schedule": "07:00",
        "grace_period_minutes": 10,
    },
    "xianqin-daily-study.py": {
        "expected_files": [
            "reports/xianqin/xianqin-{today}.md",
        ],
        "schedule": "07:30",
        "grace_period_minutes": 10,
    },
    "weather-forecast.py": {
        "expected_files": [
            "reports/weather/weather-{today}.md",
        ],
        "schedule": "07:00",
        "grace_period_minutes": 10,
    },
}

def check_scheduler_execution():
    """检查 Scheduler Agent 执行情况"""
    if not SCHEDULER_LOG.exists():
        return None, 9999
    
    with open(SCHEDULER_LOG, "r", encoding="utf-8") as f:
        logs = json.load(f)
    
    if not logs:
        return None, 9999
    
    # 找到最近一次成功执行
    for log in reversed(logs):
        if log.get("success", False):
            last_time = datetime.fromisoformat(log["timestamp"])
            hours_ago = (datetime.now() - last_time).total_seconds() / 3600
            return last_time, hours_ago
    
    return None, 9999

def check_scheduler_process():
    """检查 Scheduler Agent 进程"""
    result = subprocess.run(
        ["pgrep", "-f", "scheduler.py"],
        capture_output=True
    )
    return result.returncode == 0


def check_task_output_quality():
    """检查定时任务输出质量（结果验证 + 虚假成功检测）"""
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    today_nodash = now.strftime("%Y%m%d")
    today_hour = now.strftime("%Y%m%d-%H%M")
    
    quality_issues = []
    
    # 加载质量日志
    quality_log = []
    if QUALITY_LOG_FILE.exists():
        try:
            with open(QUALITY_LOG_FILE, 'r', encoding='utf-8') as f:
                quality_log = json.load(f)
        except (json.JSONDecodeError, IOError):
            quality_log = []
    
    for script_name, config in TASK_OUTPUT_FILES.items():
        # 检查是否到了该任务执行时间
        schedule = config["schedule"]
        grace_period = timedelta(minutes=config["grace_period_minutes"])
        
        should_have_run = False
        
        if schedule == "hourly":
            # 每小时任务 - 检查当前小时是否已执行 (宽限期 10 分钟)
            # 例如：16:00-16:59 都应该检查 16 点的文件
            current_hour = now.strftime("%Y%m%d-%H")
            # 给 10 分钟宽限期，避免误判
            if now.minute < 10:
                should_have_run = False  # 前 10 分钟不检查
            else:
                should_have_run = True
        else:
            # 每日任务 - 检查是否已过执行时间 + 宽限期
            scheduled_time = datetime.strptime(schedule, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            if now >= scheduled_time + grace_period:
                should_have_run = True
        
        if not should_have_run:
            continue  # 还没到执行时间，跳过
        
        # 检查预期文件是否存在
        files_found = []
        files_missing = []
        
        for file_pattern in config["expected_files"]:
            # 替换占位符
            filename = file_pattern.format(
                today=today,
                today_nodash=today_nodash,
                today_hour=today_hour
            )
            file_path = WORKSPACE / filename
            
            if file_path.exists():
                # 检查文件是否足够大（不是空文件）
                file_size = file_path.stat().st_size
                if file_size > 50:  # 至少 50 字节
                    files_found.append(filename)
                else:
                    files_missing.append(f"{filename} (空文件，{file_size}B)")
            else:
                files_missing.append(filename)
        
        # 记录质量问题 (增加连续失败计数)
        if files_missing:
            # 检查连续失败次数
            failure_count = 0
            for i in range(len(quality_log)-1, -1, -1):
                if quality_log[i].get("script") == script_name:
                    if quality_log[i].get("status") == "failed":
                        failure_count += 1
                    else:
                        break
                else:
                    break
            
            # 只有连续失败 3 次才记录
            if failure_count >= CONSECUTIVE_FAILURE_THRESHOLD:
                issue = {
                    "script": script_name,
                    "schedule": schedule,
                    "timestamp": now.isoformat(),
                    "files_found": files_found,
                    "files_missing": files_missing,
                    "issue_type": "文件未创建" if not files_found else "文件不完整",
                    "severity": "high" if not files_found else "medium",
                    "consecutive_failures": failure_count,
                }
                quality_issues.append(issue)
                print(f"  ⚠️  质量问题：{script_name} - 文件缺失：{', '.join(files_missing)} (连续{failure_count}次)")
            else:
                print(f"  ℹ️  跳过告警：{script_name} - 连续失败{failure_count}次 < 阈值{CONSECUTIVE_FAILURE_THRESHOLD}")
        else:
            print(f"  ✅ 质量检查：{script_name} - 文件已创建")
    
    return quality_issues


def auto_fix_missing_files(issues):
    """自动修复缺失文件 - 运行对应脚本重新生成"""
    fixed = []
    
    # 脚本到文件路径的映射
    script_paths = {
        "daily-report-generator.py": "scripts/daily-report-generator.py",
        "daily-constitution-study.py": "scripts/daily-constitution-study.py",
        "hourly-health-check.py": "scripts/hourly-health-check.py",
        "yijing-daily-study.py": "skills/07-system/suwen/yijing-daily-study.py",
        "xianqin-daily-study.py": "skills/07-system/suwen/xianqin-daily-study.py",
        "weather-forecast.py": "skills/07-system/suwen/weather-forecast.py",
    }
    
    for issue in issues:
        script_name = issue["script"]
        if script_name in script_paths:
            script_path = WORKSPACE / script_paths[script_name]
            if script_path.exists():
                print(f"  🔧 自动修复：运行 {script_name}...")
                try:
                    result = subprocess.run(
                        ["python3", str(script_path)],
                        cwd=str(WORKSPACE),
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        print(f"  ✅ 自动修复成功：{script_name}")
                        fixed.append({
                            "script": script_name,
                            "status": "fixed",
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        print(f"  ⚠️ 自动修复失败：{script_name} - {result.stderr[:100]}")
                        fixed.append({
                            "script": script_name,
                            "status": "fix_failed",
                            "error": result.stderr[:100]
                        })
                except Exception as e:
                    print(f"  ⚠️ 自动修复异常：{script_name} - {str(e)}")
                    fixed.append({
                        "script": script_name,
                        "status": "fix_error",
                        "error": str(e)
                    })
    
    return fixed


def record_quality_issues(issues, auto_fix_results=None):
    """记录质量问题到日志（用于失败模式分析和技能涌现）"""
    if not issues:
        return
    
    # 加载现有日志
    quality_log = []
    if QUALITY_LOG.exists():
        try:
            with open(QUALITY_LOG, "r", encoding="utf-8") as f:
                quality_log = json.load(f)
        except:
            quality_log = []
    
    # 添加新问题（包含自动修复结果）
    for i, issue in enumerate(issues):
        issue_record = issue.copy()
        if auto_fix_results and i < len(auto_fix_results):
            fix_result = auto_fix_results[i]
            issue_record["auto_fix"] = fix_result
        quality_log.append(issue_record)
    
    # 保留最近 100 条记录
    quality_log = quality_log[-100:]
    
    # 保存日志
    QUALITY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(QUALITY_LOG, "w", encoding="utf-8") as f:
        json.dump(quality_log, f, indent=2, ensure_ascii=False)
    
    print(f"  📝 质量问题已记录：{len(issues)} 条")
    
    # 记录到 memory（触发技能涌现）
    memory_file = WORKSPACE / "memory" / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    if memory_file.exists():
        content = memory_file.read_text(encoding='utf-8')
        if "[定时任务质量问题]" not in content:
            append_content = f"""

---

## 🔧 定时任务质量问题（{datetime.now().strftime('%H:%M')}）

发现 {len(issues)} 个定时任务存在"虚假成功"问题：

"""
            for issue in issues:
                fix_status = "✅ 已自动修复" if auto_fix_results and auto_fix_results[issues.index(issue)].get("status") == "fixed" else "⏳ 待修复"
                append_content += f"- {issue['script']}: {', '.join(issue['files_missing'])} [{fix_status}]\n"
            append_content += f"""
**类型**: [定时任务质量问题] [虚假成功检测]
**状态**: 已记录到 monitoring/task-quality-log.json
**自动修复**: {'已启用 ✅' if auto_fix_results else '未触发'}
"""
            memory_file.write_text(content + append_content, encoding='utf-8')
            print(f"  🧠 质量问题已记录到 memory")

def should_send_alert(alert_key):
    """判断是否应该发送告警（告警冷却机制）"""
    now = datetime.now()
    
    # 读取告警日志
    if ALERT_LOG.exists():
        try:
            with open(ALERT_LOG, "r", encoding="utf-8") as f:
                alert_log = json.load(f)
        except:
            alert_log = {}
    else:
        alert_log = {}
    
    # 检查冷却时间
    if alert_key in alert_log:
        last_alert = datetime.fromisoformat(alert_log[alert_key])
        time_since_last = (now - last_alert).total_seconds() / 60
        
        if time_since_last < ALERT_COOLDOWN_MINUTES:
            print(f"  ℹ️  告警冷却期内 ({time_since_last:.1f}分钟前)，跳过发送")
            return False
    
    # 更新告警日志
    alert_log[alert_key] = now.isoformat()
    ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERT_LOG, "w", encoding="utf-8") as f:
        json.dump(alert_log, f, indent=2, ensure_ascii=False)
    
    return True


def send_telegram_alert(message, alert_key="general"):
    """发送 Telegram 告警"""
    script = WORKSPACE / "scripts" / "send-md-to-telegram.py"
    
    alert_md = f"""# 🚨 Scheduler Agent 告警

{message}

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    alert_file = WORKSPACE / "scheduler-alert.md"
    alert_file.write_text(alert_md, encoding="utf-8")
    
    subprocess.run(["python3", str(script), str(alert_file)], capture_output=True)

def restart_scheduler():
    """重启 Scheduler Agent"""
    script = WORKSPACE / "skills" / "scheduler-agent" / "src" / "scheduler.py"
    
    subprocess.run(
        ["python3", str(script), "--run-all"],
        cwd=str(WORKSPACE),
        capture_output=True
    )

def main():
    print(f"[{datetime.now()}] 🏥 开始 Scheduler Agent 健康检查...")
    
    # 检查进程
    process_running = check_scheduler_process()
    print(f"  进程状态：{'✅ 运行中' if process_running else '❌ 未运行'}")
    
    # 检查执行时间
    last_time, hours_ago = check_scheduler_execution()
    if last_time:
        print(f"  最后执行：{last_time.strftime('%Y-%m-%d %H:%M:%S')} ({hours_ago:.1f}小时前)")
    else:
        print(f"  最后执行：无记录")
    
    # ✅ 新增：定时任务输出质量检查
    print(f"\n  📊 开始定时任务质量检查...")
    quality_issues = check_task_output_quality()
    
    auto_fix_results = []
    if quality_issues:
        print(f"  ⚠️  发现 {len(quality_issues)} 个质量问题")
        
        # ✅ 自动修复触发
        high_severity_issues = [i for i in quality_issues if i.get("severity") == "high"]
        if high_severity_issues:
            print(f"\n  🔧 开始自动修复 {len(high_severity_issues)} 个严重问题...")
            auto_fix_results = auto_fix_missing_files(high_severity_issues)
            fixed_count = sum(1 for r in auto_fix_results if r.get("status") == "fixed")
            print(f"  ✅ 自动修复完成：{fixed_count}/{len(high_severity_issues)} 成功\n")
        
        # 记录质量问题（包含自动修复结果）
        # 更新失败计数
        for issue in quality_issues:
            issue["status"] = "failed" if auto_fix_results and auto_fix_results[quality_issues.index(issue)].get("status") != "fixed" else "fixed"
        record_quality_issues(quality_issues, auto_fix_results)
    else:
        print(f"  ✅ 所有定时任务输出正常")
    
    # 告警逻辑
    alerts = []
    
    # 进程未运行
    if not process_running:
        alerts.append("❌ Scheduler Agent 进程未运行")
        print("  🚨 进程未运行，尝试重启...")
        restart_scheduler()
        print("  ✅ 已尝试重启 Scheduler Agent")
    
    # 超过阈值未执行
    if hours_ago > ALERT_THRESHOLD_HOURS:
        alerts.append(f"⚠️ Scheduler Agent 超过{hours_ago:.1f}小时未执行")
        print(f"  🚨 超过{hours_ago:.1f}小时未执行")
        
        # 告警冷却检查
        if should_send_alert("scheduler_not_running"):
            print("  📱 发送 Telegram 告警...")
            send_telegram_alert("\n".join(alerts), "scheduler_not_running")
            print("  ✅ 已发送 Telegram 告警")
        else:
            print("  ℹ️  告警已冷却，仅记录日志")
    
    # 质量问题告警（严重问题且自动修复失败）
    high_severity_issues = [i for i in quality_issues if i.get("severity") == "high"]
    if high_severity_issues:
        # 检查是否有修复失败的
        fix_failures = [r for r in auto_fix_results if r.get("status") in ["fix_failed", "fix_error"]]
        if fix_failures:
            alert_msg = f"🚨 定时任务质量问题（自动修复失败）\n\n以下问题自动修复失败，需人工干预:\n\n"
            for failure in fix_failures:
                alert_msg += f"❌ {failure['script']}: {failure.get('error', '未知错误')}\n"
            print(f"  🚨 发送质量问题告警（修复失败）...")
            # 严重问题不冷却，立即发送
            send_telegram_alert(alert_msg, "quality_fix_failed")
        else:
            # 全部修复成功，发送通知（冷却机制）
            alert_msg = f"✅ 定时任务质量自检\n\n发现 {len(high_severity_issues)} 个问题，已全部自动修复:\n\n"
            for issue in high_severity_issues:
                alert_msg += f"✅ {issue['script']}: 已修复\n"
            
            # 生成告警 key（基于问题脚本名）
            alert_key = "quality_" + "_".join([i['script'] for i in high_severity_issues])
            
            if should_send_alert(alert_key):
                print(f"  📱 发送质量修复通知...")
                send_telegram_alert(alert_msg, alert_key)
            else:
                print(f"  ℹ️  修复通知已冷却，仅记录日志")
    
    # 正常
    if not alerts and not quality_issues:
        print("\n  ✅ Scheduler Agent 运行正常 · 所有定时任务输出正常")
        return 0
    elif auto_fix_results and all(r.get("status") == "fixed" for r in auto_fix_results):
        print("\n  ✅ 发现问题，已全部自动修复")
        return 0
    else:
        print("\n  ⚠️ 发现问题，已处理/记录")
        # 返回 0 表示脚本执行成功（即使发现问题已处理）
        # 这样 systemd 不会认为服务失败
        return 0

if __name__ == "__main__":
    sys.exit(main())
