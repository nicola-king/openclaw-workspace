#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务结果汇报系统
功能：收集所有 cron 任务执行结果，汇总汇报给 SAYELF
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
LOGS_DIR = WORKSPACE / "logs"
BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
CHAT_ID = "7073481596"

# 定时任务清单
TIMED_TASKS = {
    "宪法学习": {
        "cron": "0 6 * * *",
        "script": "scripts/daily-constitution.sh",
        "log": "logs/constitution.log",
        "frequency": "每日 06:00"
    },
    "AI 凌晨学习": {
        "cron": "01-06 0 * * *",
        "script": "scripts/ai-overnight-learning-v2.sh",
        "log": "logs/ai-learning.log",
        "frequency": "每日 01:00-06:00"
    },
    "小红书监控": {
        "cron": "0 8,12,18 * * *",
        "script": "skills/wangliang/xiaohongshu-monitor.sh",
        "log": "logs/xiaohongshu-monitor.log",
        "frequency": "每日 08:00/12:00/18:00"
    },
    "公众号采集": {
        "cron": "0 9 * * *",
        "script": "skills/shanmu/wechat-article-collect.sh",
        "log": "logs/wechat-collect.log",
        "frequency": "每日 09:00"
    },
    "AI 生图": {
        "cron": "30 9 * * *",
        "script": "skills/shanmu/ai-image-gen.sh",
        "log": "logs/shanmu-ai-image.log",
        "frequency": "每日 09:30"
    },
    "知几-X 发布": {
        "cron": "0 10 * * *",
        "script": "skills/zhiji/post-x-daily.sh",
        "log": "logs/cron-zhiji-x.log",
        "frequency": "每日 10:00"
    },
    "知几交易日报": {
        "cron": "0 18 * * *",
        "script": "skills/zhiji/daily-report.sh",
        "log": "logs/cron-zhiji.log",
        "frequency": "每日 18:00"
    },
    "庖丁支出记录": {
        "cron": "0 9 * * *",
        "script": "skills/paoding/daily-expense.sh",
        "log": "logs/cron-paoding.log",
        "frequency": "每日 09:00"
    },
    "鲸鱼追踪": {
        "cron": "0 */4 * * *",
        "script": "skills/zhiji/whale-monitor.sh",
        "log": "logs/cron-zhiji-whale.log",
        "frequency": "每 4 小时"
    },
    "热点追踪": {
        "cron": "0 */8 * * *",
        "script": "skills/wangliang/x-hot-search-v2.sh",
        "log": "logs/cron-x-hot.log",
        "frequency": "每 8 小时"
    },
    "监控狗": {
        "cron": "0 * * * *",
        "script": "scripts/cron-watchdog.sh",
        "log": "logs/cron-watchdog.log",
        "frequency": "每小时"
    },
    "5 分钟汇报": {
        "cron": "*/5 * * * *",
        "script": "scripts/auto-exec-cron.sh",
        "log": "logs/auto-exec-5m.log",
        "frequency": "每 5 分钟"
    },
    "日报生成": {
        "cron": "0 23 * * *",
        "script": "/opt/openclaw-report.sh daily",
        "log": "logs/daily-report.log",
        "frequency": "每日 23:00"
    },
    "记忆同步": {
        "cron": "0 * * * *",
        "script": "scripts/sync-memory-to-feishu.py",
        "log": "logs/memory-sync.log",
        "frequency": "每小时"
    },
    "Bot 健康检查": {
        "cron": "*/5 * * * *",
        "script": "scripts/bot-health-monitor.py",
        "log": "logs/bot-health.log",
        "frequency": "每 5 分钟"
    },
}

def check_log(log_path, hours=24):
    """检查日志文件，返回最近执行状态"""
    full_path = WORKSPACE / log_path
    
    if not full_path.exists():
        return {"status": "❌ 无日志", "error": "日志文件不存在"}
    
    try:
        # 获取文件修改时间
        mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
        age = datetime.now() - mtime
        
        # 读取最后 10 行
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[-10:]
        
        # 检查是否有错误
        has_error = any('error' in line.lower() or 'fail' in line.lower() or 'exception' in line.lower() 
                       for line in lines if line.strip())
        
        # 检查是否有成功标记
        has_success = any('✅' in line or '完成' in line or 'success' in line.lower() 
                         for line in lines if line.strip())
        
        if age > timedelta(hours=hours):
            status = "🟡 超时未执行" if hours == 24 else "🟡 超时"
        elif has_error:
            status = "❌ 执行失败"
        elif has_success:
            status = "✅ 执行成功"
        else:
            status = "🟢 运行中"
        
        return {
            "status": status,
            "last_run": mtime.strftime('%Y-%m-%d %H:%M'),
            "age_hours": round(age.total_seconds() / 3600, 1),
            "last_lines": ''.join(lines[-3:]) if lines else "无内容"
        }
    except Exception as e:
        return {"status": "❌ 读取失败", "error": str(e)}

def check_auto_exec_status():
    """检查自动执行状态"""
    status_file = Path("/tmp/auto-exec-status.json")
    if not status_file.exists():
        return {"status": "❌ 无状态文件"}
    
    try:
        with open(status_file, 'r') as f:
            return json.load(f)
    except:
        return {"status": "❌ 读取失败"}

def generate_report():
    """生成定时任务结果报告"""
    report = []
    report.append("📊 **定时任务执行结果汇报**")
    report.append(f"*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    report.append("")
    
    # 分类统计
    success_count = 0
    error_count = 0
    running_count = 0
    
    task_results = []
    
    for task_name, config in TIMED_TASKS.items():
        result = check_log(config["log"], hours=24)
        result["name"] = task_name
        result["frequency"] = config["frequency"]
        task_results.append(result)
        
        if "✅" in result["status"]:
            success_count += 1
        elif "❌" in result["status"]:
            error_count += 1
        else:
            running_count += 1
    
    # 汇总
    report.append("═══ 执行汇总 ═══")
    report.append(f"✅ 成功：{success_count} | ❌ 失败：{error_count} | 🟡 其他：{running_count}")
    report.append(f"总任务数：{len(TIMED_TASKS)}")
    report.append("")
    
    # 失败任务优先显示
    report.append("═══ 失败任务 (需关注) ═══")
    failed_tasks = [t for t in task_results if "❌" in t["status"]]
    if failed_tasks:
        for task in failed_tasks:
            report.append(f"❌ **{task['name']}** ({task['frequency']})")
            report.append(f"   状态：{task['status']}")
            if "error" in task:
                report.append(f"   错误：{task['error']}")
            report.append("")
    else:
        report.append("✅ 无失败任务")
        report.append("")
    
    # 所有任务状态
    report.append("═══ 全部任务状态 ═══")
    for task in sorted(task_results, key=lambda x: x["name"]):
        report.append(f"{task['status']} **{task['name']}** - {task['frequency']}")
        if "last_run" in task:
            report.append(f"   最后执行：{task['last_run']} ({task['age_hours']}h 前)")
    
    # 自动执行状态
    report.append("")
    report.append("═══ 5 分钟自动执行状态 ═══")
    auto_status = check_auto_exec_status()
    if "currentTask" in auto_status:
        report.append(f"当前任务：{auto_status.get('currentTask', '无')}")
        report.append(f"进度：{auto_status.get('progress', 0)}%")
        report.append(f"状态：{auto_status.get('status', '未知')}")
    
    return "\n".join(report)

def send_telegram_message(text):
    """发送 Telegram 消息"""
    import urllib.request
    import urllib.parse
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(data).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode()
    except Exception as e:
        return f"发送失败：{e}"

def main():
    print("生成定时任务结果报告...")
    report = generate_report()
    print(report)
    
    print("\n发送报告到 Telegram...")
    result = send_telegram_message(report)
    print(f"发送结果：{result[:200]}")
    
    # 保存报告
    report_file = WORKSPACE / "reports" / f"task-report-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存：{report_file}")

if __name__ == "__main__":
    main()
