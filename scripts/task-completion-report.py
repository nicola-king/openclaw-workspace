#!/usr/bin/env python3
"""
定时任务完成率自动化汇报
每小时统计一次任务完成情况
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# 配置
MEMORY_DIR = Path("/home/nicola/.openclaw/workspace/memory")
HEARTBEAT_FILE = Path("/home/nicola/.openclaw/workspace/HEARTBEAT.md")
LOG_FILE = Path("/tmp/task-completion-report.log")

def log(message):
    """写日志"""
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def parse_heartbeat():
    """解析 HEARTBEAT.md 中的任务状态"""
    tasks = {
        "P0": {"total": 0, "completed": 0, "items": []},
        "P1": {"total": 0, "completed": 0, "items": []},
    }
    
    try:
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 解析 P0 任务
        in_p0_table = False
        for line in content.split("\n"):
            if "当前聚焦" in line or "P0 仅" in line:
                in_p0_table = True
                continue
            if in_p0_table and line.strip().startswith("|---"):
                continue
            if in_p0_table and line.strip().startswith("|"):
                if "P1" in line or "##" in line:
                    in_p0_table = False
                    continue
                parts = line.split("|")
                if len(parts) >= 5:
                    task_id = parts[1].strip()
                    task_name = parts[2].strip()
                    status = parts[3].strip()
                    
                    if task_id and task_name and not task_id.startswith("编号"):
                        tasks["P0"]["total"] += 1
                        is_completed = "✅" in status or "完成" in status
                        if is_completed:
                            tasks["P0"]["completed"] += 1
                        tasks["P0"]["items"].append({
                            "id": task_id,
                            "name": task_name,
                            "status": status,
                            "completed": is_completed
                        })
        
        # 解析 P1 任务 (刚完成部分)
        in_p1_table = False
        for line in content.split("\n"):
            if "刚完成" in line and "P0+P1" in line:
                in_p1_table = True
                continue
            if in_p1_table and line.strip().startswith("|---"):
                continue
            if in_p1_table and line.strip().startswith("|"):
                if "##" in line and "刚完成" not in line:
                    in_p1_table = False
                    continue
                parts = line.split("|")
                if len(parts) >= 4:
                    task_id = parts[1].strip()
                    task_name = parts[2].strip()
                    status = parts[3].strip()
                    
                    if task_id and task_name and not task_id.startswith("编号"):
                        tasks["P1"]["total"] += 1
                        is_completed = "✅" in status or "完成" in status
                        if is_completed:
                            tasks["P1"]["completed"] += 1
                        tasks["P1"]["items"].append({
                            "id": task_id,
                            "name": task_name,
                            "status": status,
                            "completed": is_completed
                        })
        
    except Exception as e:
        log(f"❌ 解析 HEARTBEAT.md 失败：{e}")
    
    return tasks

def generate_report():
    """生成任务完成率报告"""
    tasks = parse_heartbeat()
    
    lines = []
    lines.append("╔═══════════════════════════════════════════════════════════╗")
    lines.append("║  定时任务完成率汇报                      太一 AGI         ║")
    lines.append(f"║  统计时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}                          ║")
    lines.append("╠═══════════════════════════════════════════════════════════╣")
    
    # P0 任务
    p0_total = tasks["P0"]["total"]
    p0_completed = tasks["P0"]["completed"]
    p0_rate = (p0_completed / p0_total * 100) if p0_total > 0 else 0
    
    p0_filled = int(p0_rate) // 5
    p0_empty = 20 - p0_filled
    p0_bar = "🟦" * p0_filled + "⬜" * p0_empty
    
    lines.append(f"║  🎯 P0 任务完成率 [{p0_bar}] {p0_rate:5.1f}%  ║")
    lines.append(f"║     已完成 {p0_completed}/{p0_total} 任务                              ║")
    
    # P1 任务
    p1_total = tasks["P1"]["total"]
    p1_completed = tasks["P1"]["completed"]
    p1_rate = (p1_completed / p1_total * 100) if p1_total > 0 else 0
    
    p1_filled = int(p1_rate) // 5
    p1_empty = 20 - p1_filled
    p1_bar = "🟦" * p1_filled + "⬜" * p1_empty
    
    lines.append(f"║  🎯 P1 任务完成率 [{p1_bar}] {p1_rate:5.1f}%  ║")
    lines.append(f"║     已完成 {p1_completed}/{p1_total} 任务                              ║")
    
    # 总体
    total_all = p0_total + p1_total
    completed_all = p0_completed + p1_completed
    total_rate = (completed_all / total_all * 100) if total_all > 0 else 0
    
    total_filled = int(total_rate) // 5
    total_empty = 20 - total_filled
    total_bar = "🟦" * total_filled + "⬜" * total_empty
    
    lines.append("╠═══════════════════════════════════════════════════════════╣")
    lines.append(f"║  📊 总体完成率 [{total_bar}] {total_rate:5.1f}%  ║")
    lines.append(f"║     总计已完成 {completed_all}/{total_all} 任务                            ║")
    
    # P0 任务详情
    if tasks["P0"]["items"]:
        lines.append("╠═══════════════════════════════════════════════════════════╣")
        lines.append("║  📋 P0 任务详情：                                         ║")
        for item in tasks["P0"]["items"]:
            icon = "✅" if item["completed"] else "🟡"
            short_name = item["name"][:20].ljust(20)
            lines.append(f"║     {icon} {short_name} {item['status'][:10]:<10}  ║")
    
    lines.append("╠═══════════════════════════════════════════════════════════╣")
    lines.append("║  🤖 自动汇报 · 每小时更新 · 任务完成率监控                  ║")
    lines.append("╚═══════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)

def send_via_message_tool(channel, target, message):
    """使用 openclaw message send 命令发送"""
    import subprocess
    try:
        cmd = [
            "openclaw", "message", "send",
            "--channel", channel,
            "--target", target,
            "--message", message
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            log(f"✅ {channel} 发送成功")
            return True
        else:
            error_msg = result.stderr[:200] if result.stderr else "未知错误"
            log(f"❌ {channel} 发送失败：{error_msg}")
            return False
    except Exception as e:
        log(f"❌ {channel} 异常：{e}")
        return False

def main():
    log("🚀 定时任务完成率汇报启动")
    
    # 生成报告
    report = generate_report()
    log(f"生成报告：{len(report)} 字符")
    
    # 发送到 Telegram
    success = send_via_message_tool(
        "telegram",
        "7073481596",
        report
    )
    
    if success:
        log("✅ 任务完成率汇报发送成功")
        return True
    else:
        log("❌ 任务完成率汇报发送失败")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
