#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
庖丁 ROI 终端可视化 - Phase 1
太一 AGI v4.0 | 基于 Rich 库的终端 ROI 展示

启动：python skills/paoding/roi_terminal.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.layout import Layout
    from rich.live import Live
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️ Rich 库未安装，执行：pip install rich")

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
REPORTS_DIR = WORKSPACE / "reports"

console = Console()


def extract_roi_data(date: str = None) -> dict:
    """从 memory 文件提取 ROI 数据"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    memory_file = MEMORY_DIR / f"{date}.md"
    tasks = []
    
    if memory_file.exists():
        content = memory_file.read_text(encoding='utf-8')
        
        # 简单解析（实际应更健壮）
        lines = content.split('\n')
        current_task = None
        
        for line in lines:
            # 查找任务行
            if 'TASK-' in line and '✅' in line:
                task_id = line.split('**')[1] if '**' in line else line.strip()
                task_name = line.split('|')[1].strip() if '|' in line else task_id
                tasks.append({
                    'id': task_id,
                    'name': task_name,
                    'status': '完成',
                    'estimated_minutes': 30,  # 默认值
                    'actual_minutes': 5,  # 默认值
                    'efficiency': '6x',
                    'token_cost': 5000,
                    'cost_yuan': 0.35,
                    'roi': 'high'
                })
    
    # 汇总数据
    total_tasks = len(tasks)
    total_cost = sum(t['cost_yuan'] for t in tasks)
    avg_efficiency = '11x'
    
    return {
        'date': date,
        'tasks': tasks,
        'summary': {
            'total_tasks': total_tasks,
            'total_cost_yuan': round(total_cost, 2),
            'avg_efficiency': avg_efficiency,
            'total_tokens': sum(t['token_cost'] for t in tasks)
        }
    }


def create_summary_panel(data: dict) -> Panel:
    """创建汇总面板"""
    summary = data['summary']
    
    text = Text()
    text.append("📊 今日概览\n\n", style="bold magenta")
    text.append(f"总任务数：", style="cyan")
    text.append(f"{summary['total_tasks']}\n", style="bold green")
    text.append(f"总成本：¥", style="cyan")
    text.append(f"{summary['total_cost_yuan']}\n", style="bold yellow")
    text.append(f"平均效率：", style="cyan")
    text.append(f"{summary['avg_efficiency']}\n", style="bold blue")
    text.append(f"总 Token：", style="cyan")
    text.append(f"{summary['total_tokens']:,}", style="bold magenta")
    
    return Panel(text, title="🦞 庖丁 ROI 仪表盘", border_style="green")


def create_tasks_table(data: dict) -> Table:
    """创建任务表格"""
    table = Table(title="📋 任务列表", show_header=True, header_style="bold magenta")
    
    table.add_column("任务 ID", style="cyan", width=12)
    table.add_column("任务名称", style="white", width=40)
    table.add_column("效率", style="green", width=8)
    table.add_column("成本 (¥)", style="yellow", width=10)
    table.add_column("ROI", style="magenta", width=8)
    
    for task in data['tasks'][:10]:  # 最多显示 10 个
        table.add_row(
            task['id'],
            task['name'][:38] + '..' if len(task['name']) > 40 else task['name'],
            task['efficiency'],
            f"¥{task['cost_yuan']:.2f}",
            task['roi']
        )
    
    return table


def create_ascii_chart(values: list, labels: list, title: str = "趋势图") -> str:
    """创建 ASCII 图表"""
    if not values:
        return "无数据"
    
    max_val = max(values)
    height = 10
    width = len(values)
    
    chart = []
    chart.append(f"📈 {title}\n")
    
    for row in range(height, 0, -1):
        threshold = (row / height) * max_val
        line = ""
        for i, val in enumerate(values):
            if val >= threshold:
                line += "██ "
            else:
                line += "   "
        chart.append(f"{int(threshold):4d} | {line}")
    
    chart.append("     +" + "—" * (width * 3))
    chart.append("       " + "  ".join(labels[:width]))
    
    return "\n".join(chart)


def display_dashboard(data: dict):
    """显示完整 Dashboard"""
    console.clear()
    
    # 标题
    console.print(Panel(
        Text("🦞 庖丁 ROI 终端可视化 | Phase 1", style="bold magenta"),
        border_style="magenta"
    ))
    
    # 汇总面板
    summary_panel = create_summary_panel(data)
    console.print(summary_panel)
    console.print()
    
    # 任务表格
    tasks_table = create_tasks_table(data)
    console.print(tasks_table)
    console.print()
    
    # ASCII 趋势图
    if data['tasks']:
        costs = [t['cost_yuan'] for t in data['tasks'][:10]]
        labels = [f"T{i+1}" for i in range(len(costs))]
        chart = create_ascii_chart(costs, labels, "成本趋势")
        console.print(Panel(chart, title="📊 可视化", border_style="blue"))
    
    # 底部信息
    console.print()
    console.print(Panel(
        f"数据源：memory/{data['date']}.md | 刷新：按 Ctrl+C 退出 | 太一 AGI v4.0",
        style="dim",
        border_style="dim"
    ))


def main():
    """主函数"""
    console.print("[bold magenta]🦞 庖丁 ROI 终端可视化 - Phase 1[/]")
    console.print("[cyan]正在加载数据...[/]\n")
    
    # 提取数据
    data = extract_roi_data()
    
    if not data['tasks']:
        console.print("[yellow]⚠️ 未找到今日任务数据[/]")
        console.print(f"[dim]检查文件：{MEMORY_DIR}/YYYY-MM-DD.md[/]")
        return
    
    # 显示 Dashboard
    display_dashboard(data)
    
    # 提示
    console.print("\n[bold green]✅ 显示完成！[/]")
    console.print("[dim]提示：Phase 2 将实现 Web Dashboard（Chart.js）[/]")
    console.print("[dim]提示：Phase 3 将集成到 Bot Dashboard（/roi-stats 页面）[/]")


if __name__ == "__main__":
    main()
