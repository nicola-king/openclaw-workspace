#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一系统定时任务诊断与自动修复脚本

功能:
- 检查所有定时任务状态
- 检测代理依赖问题
- 自动修复常见问题
- 生成诊断报告

作者：太一 AGI
创建：2026-04-22
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
LOGS_DIR = WORKSPACE / "logs"
REPORTS_DIR = WORKSPACE / "reports"

# 定时任务配置
CRON_TASKS = {
    "scheduler": {
        "name": "Scheduler Agent",
        "schedule": "*/5 * * * *",
        "log": LOGS_DIR / "scheduler.log",
        "check_interval": 300,  # 5 分钟
    },
    "quality_monitor": {
        "name": "质量监控 Agent",
        "schedule": "*/5 * * * *",
        "log": LOGS_DIR / "quality-monitor.log",
        "check_interval": 300,
    },
    "auto_bug_fix": {
        "name": "Auto Bug Fix",
        "schedule": "*/30 * * * *",
        "log": LOGS_DIR / "auto-bug-fix-cron.log",
        "check_interval": 1800,
    },
    "constitution_study": {
        "name": "宪法学习",
        "schedule": "0 6 * * *",
        "log": LOGS_DIR / "constitution-study.log",
        "check_interval": 86400,
    },
    "daily_report": {
        "name": "日报生成",
        "schedule": "0 23 * * *",
        "log": LOGS_DIR / "daily-report.log",
        "check_interval": 86400,
    },
    "dao_agent": {
        "name": "道 Agent 推送",
        "schedule": "0 8 * * *",
        "log": LOGS_DIR / "wisdom-scheduler/dao-cron.log",
        "check_interval": 86400,
    },
    "wu_agent": {
        "name": "悟 Agent 推送",
        "schedule": "0 20 * * *",
        "log": LOGS_DIR / "wisdom-scheduler/wu-cron.log",
        "check_interval": 86400,
    },
    "cross_border_daily": {
        "name": "跨境情报简报",
        "schedule": "0 8 * * *",
        "log": LOGS_DIR / "cross-border/daily-brief.log",
        "check_interval": 86400,
    },
    "cross_border_competitor": {
        "name": "竞品分析",
        "schedule": "0 18 * * *",
        "log": LOGS_DIR / "cross-border/competitor-analysis.log",
        "check_interval": 86400,
    },
    "breaking_news": {
        "name": "突发新闻监测",
        "schedule": "* * * * *",
        "log": LOGS_DIR / "breaking-news/monitor.log",
        "check_interval": 60,
    },
}

# Telegram 配置 (带代理)
TELEGRAM_CONFIG = {
    "bot_token": "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY",
    "chat_id": "7073481596",
    "proxy": {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }
}


class CronDiagnoser:
    """定时任务诊断器"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tasks": {},
            "issues": [],
            "fixes": [],
        }
    
    def check_clash_status(self):
        """检查 Clash 代理状态"""
        print("\n🔍 检查 Clash 代理状态...")
        
        try:
            result = subprocess.run(
                ["systemctl", "--user", "is-active", "clash.service"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout.strip() == "active":
                print("✅ Clash 代理运行正常")
                return True
            else:
                print(f"❌ Clash 代理状态异常：{result.stdout.strip()}")
                self.results["issues"].append({
                    "type": "clash_inactive",
                    "severity": "high",
                    "message": "Clash 代理未运行，影响 Telegram 推送",
                })
                return False
        except Exception as e:
            print(f"❌ 检查失败：{e}")
            return False
    
    def check_task_log(self, task_id, task_config):
        """检查任务日志"""
        log_file = task_config["log"]
        
        if not log_file.exists():
            print(f"⚠️  日志文件不存在：{log_file}")
            self.results["issues"].append({
                "type": "missing_log",
                "task": task_id,
                "severity": "medium",
                "message": f"日志文件不存在：{log_file}",
            })
            return False
        
        # 检查日志是否更新
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        age = (datetime.now() - mtime).total_seconds()
        
        if age > task_config["check_interval"] * 2:
            print(f"⚠️  日志过期：{task_config['name']} (最后更新：{age/3600:.1f}小时前)")
            self.results["issues"].append({
                "type": "stale_log",
                "task": task_id,
                "severity": "medium",
                "message": f"日志超过{task_config['check_interval']*2/3600:.1f}小时未更新",
            })
            return False
        
        # 检查日志中的错误
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                last_lines = f.readlines()[-50:]
            
            error_keywords = ["error", "failed", "exception", "❌"]
            for line in last_lines:
                if any(kw in line.lower() for kw in error_keywords):
                    if "telegram" in line.lower() and "proxy" in line.lower():
                        print(f"⚠️  发现代理相关错误：{line.strip()[:100]}")
                        self.results["issues"].append({
                            "type": "telegram_proxy_error",
                            "task": task_id,
                            "severity": "medium",
                            "message": "Telegram 推送代理错误",
                        })
                    break
            
            print(f"✅ {task_config['name']} 运行正常")
            return True
        except Exception as e:
            print(f"❌ 读取日志失败：{e}")
            return False
    
    def check_all_tasks(self):
        """检查所有定时任务"""
        print("\n📋 检查所有定时任务...")
        print("=" * 60)
        
        for task_id, task_config in CRON_TASKS.items():
            print(f"\n检查：{task_config['name']}")
            status = self.check_task_log(task_id, task_config)
            self.results["tasks"][task_id] = {
                "name": task_config["name"],
                "status": "ok" if status else "issue",
                "last_check": datetime.now().isoformat(),
            }
    
    def apply_fixes(self):
        """应用自动修复"""
        print("\n🔧 应用自动修复...")
        print("=" * 60)
        
        fixes_applied = []
        
        for issue in self.results["issues"]:
            issue_type = issue["type"]
            
            if issue_type == "clash_inactive":
                print("\n🔧 尝试重启 Clash 代理...")
                try:
                    subprocess.run(
                        ["systemctl", "--user", "restart", "clash.service"],
                        timeout=30
                    )
                    print("✅ Clash 代理已重启")
                    fixes_applied.append("clash_restart")
                except Exception as e:
                    print(f"❌ 重启失败：{e}")
            
            elif issue_type == "telegram_proxy_error":
                print("\n🔧 检查代理配置...")
                # 检查脚本是否包含代理配置
                scripts_to_check = [
                    WORKSPACE / "skills/01-trading/cross-border-trade-agent/intelligence_reporter.py",
                    WORKSPACE / "scripts/daily-report-generator.py",
                ]
                
                for script in scripts_to_check:
                    if script.exists():
                        with open(script, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if "proxies" not in content and "127.0.0.1:7890" not in content:
                            print(f"⚠️  脚本缺少代理配置：{script}")
                            fixes_applied.append(f"missing_proxy_config:{script}")
                        else:
                            print(f"✅ 脚本已配置代理：{script}")
        
        self.results["fixes"] = fixes_applied
    
    def generate_report(self):
        """生成诊断报告"""
        print("\n📊 生成诊断报告...")
        
        report = []
        report.append("# 太一系统定时任务诊断报告")
        report.append("")
        report.append(f"**生成时间**: {self.results['timestamp']}")
        report.append("")
        report.append("---")
        report.append("")
        
        # 任务状态汇总
        report.append("## 📋 任务状态汇总")
        report.append("")
        
        total = len(self.results["tasks"])
        ok = sum(1 for t in self.results["tasks"].values() if t["status"] == "ok")
        issue = total - ok
        
        report.append(f"| 状态 | 数量 | 比例 |")
        report.append(f"|------|------|------|")
        report.append(f"| ✅ 正常 | {ok} | {ok/total*100:.1f}% |")
        report.append(f"| ⚠️  异常 | {issue} | {issue/total*100:.1f}% |")
        report.append("")
        
        # 详细任务状态
        report.append("## 📊 详细任务状态")
        report.append("")
        report.append("| 任务 | 状态 | 最后检查 |")
        report.append("|------|------|---------|")
        
        for task_id, task_info in self.results["tasks"].items():
            status_emoji = "✅" if task_info["status"] == "ok" else "⚠️"
            report.append(f"| {task_info['name']} | {status_emoji} {task_info['status']} | {task_info['last_check']} |")
        
        report.append("")
        
        # 问题列表
        if self.results["issues"]:
            report.append("## ⚠️ 发现的问题")
            report.append("")
            
            for i, issue in enumerate(self.results["issues"], 1):
                report.append(f"{i}. **{issue['type']}** ({issue['severity']})")
                report.append(f"   - 任务：{issue.get('task', 'N/A')}")
                report.append(f"   - 说明：{issue['message']}")
                report.append("")
        else:
            report.append("## ✅ 未发现问题")
            report.append("")
        
        # 修复记录
        if self.results["fixes"]:
            report.append("## 🔧 已应用的修复")
            report.append("")
            
            for fix in self.results["fixes"]:
                report.append(f"- {fix}")
            
            report.append("")
        
        report.append("---")
        report.append("")
        report.append("*太一 AGI · 定时任务诊断系统*")
        
        return "\n".join(report)
    
    def send_report(self, report_text):
        """发送诊断报告到 Telegram"""
        print("\n📱 发送诊断报告到 Telegram...")
        
        import requests
        
        url = f"https://api.telegram.org/bot{TELEGRAM_CONFIG['bot_token']}/sendMessage"
        
        try:
            data = {
                'chat_id': TELEGRAM_CONFIG['chat_id'],
                'text': report_text[:4096],
                'parse_mode': 'Markdown',
            }
            
            response = requests.post(
                url,
                data=data,
                timeout=30,
                proxies=TELEGRAM_CONFIG['proxy']
            )
            
            if response.status_code == 200:
                print("✅ 报告发送成功")
                return True
            else:
                print(f"❌ 发送失败：{response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 发送异常：{e}")
            return False
    
    def run(self):
        """运行完整诊断流程"""
        print("=" * 60)
        print("🔍 太一系统定时任务诊断与修复")
        print("=" * 60)
        
        # 1. 检查 Clash 代理
        clash_ok = self.check_clash_status()
        
        # 2. 检查所有任务
        self.check_all_tasks()
        
        # 3. 应用自动修复
        self.apply_fixes()
        
        # 4. 生成报告
        report = self.generate_report()
        
        # 5. 保存报告
        report_file = REPORTS_DIR / f"cron-diagnose-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n💾 报告已保存：{report_file}")
        
        # 6. 发送报告
        if clash_ok:
            self.send_report(report)
        
        print("\n" + "=" * 60)
        print("✅ 诊断完成！")
        print("=" * 60)
        
        return self.results


def main():
    """主函数"""
    diagnoser = CronDiagnoser()
    results = diagnoser.run()
    
    # 返回退出码
    if results["issues"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
