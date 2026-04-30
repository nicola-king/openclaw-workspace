#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四层记忆架构更新脚本

功能:
1. 每日更新情境记忆
2. 每周汇总演化记忆
3. 每月提炼 MEMORY.md
4. 维护记忆流动机制

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
REPORTS_DIR = WORKSPACE / "reports"

# 确保目录存在
MEMORY_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


class FourLayersMemoryUpdater:
    """四层记忆更新器"""
    
    def __init__(self):
        self.core_file = MEMORY_DIR / "core.md"
        self.context_file = MEMORY_DIR / "context.md"
        self.evolution_file = MEMORY_DIR / "evolution.md"
        self.residual_file = MEMORY_DIR / "residual.md"
        self.memory_file = WORKSPACE / "MEMORY.md"
    
    def daily_update(self):
        """每日更新情境记忆"""
        print("📅 执行每日记忆更新...")
        
        # 读取今日日志
        today = datetime.now().strftime("%Y-%m-%d")
        today_log = MEMORY_DIR / f"{today}.md"
        
        if not today_log.exists():
            print("  ⚠️ 今日日志不存在，跳过")
            return
        
        with open(today_log, "r", encoding="utf-8") as f:
            log_content = f.read()
        
        # 提取情境信息
        context_content = self.extract_context(log_content)
        
        # 更新情境记忆
        self.update_context(context_content)
        
        # 提取核心信息
        core_insights = self.extract_core_insights(log_content)
        
        # 更新核心记忆
        self.update_core(core_insights)
        
        # 提取演进事件
        evolution_events = self.extract_evolution_events(log_content)
        
        # 更新演化记忆
        self.update_evolution(evolution_events)
        
        print("  ✅ 每日记忆更新完成")
    
    def weekly_update(self):
        """每周汇总演化记忆"""
        print("📅 执行每周记忆汇总...")
        
        # 读取本周所有日志
        week_logs = []
        now = datetime.now()
        
        for i in range(7):
            date = now - timedelta(days=i)
            log_file = MEMORY_DIR / f"{date.strftime('%Y-%m-%d')}.md"
            
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    week_logs.append(f.read())
        
        # 汇总本周情境
        weekly_context = self.summarize_weekly_context(week_logs)
        
        # 更新演化记忆
        self.update_evolution(weekly_context, weekly=True)
        
        # 清理过期情境（>7 天）
        self.cleanup_old_context()
        
        # 生成周报
        self.generate_weekly_report(weekly_context)
        
        print("  ✅ 每周记忆汇总完成")
    
    def monthly_update(self):
        """每月提炼 MEMORY.md"""
        print("📅 执行每月记忆提炼...")
        
        # 读取本月所有演化记忆
        month_events = self.extract_month_events()
        
        # 提炼到 MEMORY.md
        self.refine_to_memory(month_events)
        
        # 检查核心记忆大小
        self.check_core_size()
        
        print("  ✅ 每月记忆提炼完成")
    
    def extract_context(self, log_content):
        """提取情境信息"""
        # 简化实现：提取最近的任务和决策
        lines = log_content.split("\n")
        context_lines = []
        
        for line in lines:
            if "任务" in line or "决策" in line or "完成" in line:
                context_lines.append(line)
        
        return "\n".join(context_lines[:50])  # 限制长度
    
    def extract_core_insights(self, log_content):
        """提取核心洞察"""
        # 简化实现：提取重要洞察
        lines = log_content.split("\n")
        insights = []
        
        for line in lines:
            if "洞察" in line or "原则" in line or "价值" in line:
                insights.append(line)
        
        return "\n".join(insights[:20])
    
    def extract_evolution_events(self, log_content):
        """提取演进事件"""
        # 简化实现：提取能力涌现和技能创建
        lines = log_content.split("\n")
        events = []
        
        for line in lines:
            if "涌现" in line or "Skill" in line or "Agent" in line:
                events.append(line)
        
        return "\n".join(events[:30])
    
    def update_context(self, content):
        """更新情境记忆"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        with open(self.context_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n\n## {timestamp}\n\n")
            f.write(content)
    
    def update_core(self, content):
        """更新核心记忆"""
        if not content.strip():
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        with open(self.core_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n### {timestamp}\n\n")
            f.write(content)
    
    def update_evolution(self, content, weekly=False):
        """更新演化记忆"""
        if not content.strip():
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        prefix = "📅 本周汇总" if weekly else "📅 每日记录"
        
        with open(self.evolution_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n\n## {prefix} · {timestamp}\n\n")
            f.write(content)
    
    def summarize_weekly_context(self, week_logs):
        """汇总本周情境"""
        summary = []
        
        for i, log in enumerate(week_logs):
            summary.append(f"### Day {i+1}\n\n{log[:500]}...")
        
        return "\n\n".join(summary)
    
    def cleanup_old_context(self):
        """清理过期情境"""
        # 保留最近 7 天的情境
        print("  🗑️ 清理过期情境...")
        
        # 简化实现：截断文件
        with open(self.context_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        lines = content.split("\n")
        
        # 保留最后 100 行
        if len(lines) > 100:
            with open(self.context_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines[-100:]))
    
    def generate_weekly_report(self, weekly_context):
        """生成周报"""
        report_file = REPORTS_DIR / f"memory-weekly-{datetime.now().strftime('%Y%m%d')}.md"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"# 四层记忆周报 · {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(weekly_context[:2000])
    
    def extract_month_events(self):
        """提取本月事件"""
        # 读取本月所有演化记忆
        events = []
        
        with open(self.evolution_file, "r", encoding="utf-8") as f:
            content = f.read()
            events = content.split("---")[-10:]  # 最近 10 个事件
        
        return "\n".join(events)
    
    def refine_to_memory(self, month_events):
        """提炼到 MEMORY.md"""
        if not self.memory_file.exists():
            return
        
        with open(self.memory_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n\n## 本月演进 · {datetime.now().strftime('%Y-%m')}\n\n")
            f.write(month_events[:1000])
    
    def check_core_size(self):
        """检查核心记忆大小"""
        if not self.core_file.exists():
            return
        
        with open(self.core_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 如果超过 50K，提炼到 MEMORY.md
        if len(content) > 50000:
            print("  ⚠️ 核心记忆超过 50K，触发提炼...")
            # 简化实现：截断
            with open(self.core_file, "w", encoding="utf-8") as f:
                f.write(content[-40000:])  # 保留最后 40K
    
    def run(self, mode="daily"):
        """运行更新"""
        print("=" * 60)
        print("🧬 四层记忆架构更新")
        print("=" * 60)
        
        if mode == "daily":
            self.daily_update()
        elif mode == "weekly":
            self.weekly_update()
        elif mode == "monthly":
            self.monthly_update()
        
        print("\n✅ 更新完成！")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        mode = "daily"
    else:
        mode = sys.argv[1]
    
    updater = FourLayersMemoryUpdater()
    updater.run(mode)


if __name__ == "__main__":
    main()
