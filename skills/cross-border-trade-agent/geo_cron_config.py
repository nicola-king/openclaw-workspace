#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO 定时任务配置
版本：v1.0
创建：2026-04-20 21:16
功能：配置 GEO 审计和监测的定时任务
"""

import json
from pathlib import Path
from datetime import datetime

# Cron 配置
CRON_CONFIG = {
    # 每周 GEO 审计 (周一 9:00)
    "weekly_audit": {
        "schedule": "0 9 * * 1",
        "command": "cd /home/sayelf/.openclaw/workspace/skills/01-trading/cross-border-trade-agent && python3 geo_auditor.py --report",
        "description": "每周 GEO 可见度审计",
        "enabled": True,
    },
    
    # 每日 Earned Media 检查 (每天 10:00)
    "daily_earned_media_check": {
        "schedule": "0 10 * * *",
        "command": "cd /home/sayelf/.openclaw/workspace/skills/01-trading/cross-border-trade-agent && python3 earned_media_tracker.py --check",
        "description": "每日 Earned Media 状态检查",
        "enabled": True,
    },
    
    # 每月 GEO 报告 (每月 1 日 9:00)
    "monthly_geo_report": {
        "schedule": "0 9 1 * *",
        "command": "cd /home/sayelf/.openclaw/workspace/skills/01-trading/cross-border-trade-agent && python3 geo_auditor.py --monthly-report",
        "description": "每月 GEO 综合报告",
        "enabled": True,
    },
    
    # 每季度策略复盘 (每季度首月 1 日 10:00)
    "quarterly_review": {
        "schedule": "0 10 1 1,4,7,10 *",
        "command": "cd /home/sayelf/.openclaw/workspace/skills/01-trading/cross-border-trade-agent && python3 earned_media_tracker.py --quarterly-review",
        "description": "每季度 GEO 策略复盘",
        "enabled": True,
    },
}

def generate_crontab():
    """生成 crontab 配置"""
    crontab_lines = [
        "# GEO 定时任务配置",
        f"# 生成时间：{datetime.now().isoformat()}",
        "# 使用方法：crontab -e 然后粘贴以下内容",
        "",
        "# 环境变量",
        "SHELL=/bin/bash",
        "PATH=/usr/local/bin:/usr/bin:/bin",
        "PYTHONIOENCODING=utf-8",
        "",
    ]
    
    for task_name, config in CRON_CONFIG.items():
        if config.get("enabled", True):
            line = f"{config['schedule']} {config['command']} >> /tmp/geo_{task_name}.log 2>&1"
            comment = f"# {config['description']}"
            crontab_lines.extend([comment, line, ""])
    
    return "\n".join(crontab_lines)

def install_crontab():
    """安装 crontab (需要手动确认)"""
    crontab_content = generate_crontab()
    
    output_file = Path(__file__).parent / "geo_crontab.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(crontab_content)
    
    print(f"✅ Crontab 配置已生成：{output_file}")
    print("\n📋 安装方法:")
    print("1. 查看配置：cat geo_crontab.txt")
    print("2. 安装配置：crontab geo_crontab.txt")
    print("3. 验证安装：crontab -l")
    print("\n⚠️  注意：安装 crontab 需要人工确认")
    
    return output_file

def main():
    """主函数"""
    print("\n🕐 GEO 定时任务配置生成器")
    print("=" * 60)
    
    # 显示任务列表
    print("\n📋 计划任务:")
    for task_name, config in CRON_CONFIG.items():
        status = "✅" if config.get("enabled", True) else "❌"
        print(f"{status} {task_name}:")
        print(f"   时间：{config['schedule']}")
        print(f"   说明：{config['description']}")
        print()
    
    # 生成配置
    output_file = install_crontab()
    
    # 保存配置为 JSON
    config_file = Path(__file__).parent / "geo_cron_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(CRON_CONFIG, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 配置已保存：{config_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
