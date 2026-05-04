#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务配置 - 自媒体运营自动化
太一 AGI · 2026-04-19 20:15

功能:
- 配置定时任务
- 生成 crontab 配置
- 任务调度管理
"""

import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('CronConfig')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
CRON_DIR = WORKSPACE / "data" / "cross-border" / "cron"
CRON_DIR.mkdir(parents=True, exist_ok=True)


class CronConfigGenerator:
    """定时任务配置生成器"""
    
    # 定时任务配置
    CRON_TASKS = {
        "daily_news": {
            "name": "晨间新闻推送",
            "schedule": "0 8 * * *",
            "script": "self_media_engine.py",
            "action": "plan_content",
            "params": {"type": "daily_news", "topic": "跨境贸易每日新闻"}
        },
        "weekly_analysis": {
            "name": "周度深度分析",
            "schedule": "0 9 * * 1-5",
            "script": "self_media_engine.py",
            "action": "plan_content",
            "params": {"type": "deep_analysis"}
        },
        "traffic_report": {
            "name": "流量数据汇总",
            "schedule": "0 20 * * *",
            "script": "self_media_engine.py",
            "action": "generate_daily_report"
        },
        "funnel_analysis": {
            "name": "转化漏斗分析",
            "schedule": "0 18 * * 5",
            "script": "self_media_engine.py",
            "action": "analyze_funnel"
        },
        "evolution_report": {
            "name": "自进化报告",
            "schedule": "0 22 * * 0",
            "script": "self_evolution_engine.py",
            "action": "generate_evolution_report"
        },
        "brand_report": {
            "name": "品牌健康度报告",
            "schedule": "0 10 * * 1",
            "script": "brand_building_engine.py",
            "action": "generate_brand_report"
        },
        "private_traffic_report": {
            "name": "私域运营报告",
            "schedule": "0 11 * * 1",
            "script": "private_traffic_engine.py",
            "action": "generate_segment_report"
        },
        "data_backup": {
            "name": "数据备份",
            "schedule": "0 3 * * *",
            "script": "backup.py",
            "action": "backup_all_data"
        }
    }
    
    def __init__(self):
        self.config_file = CRON_DIR / "cron_config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"tasks": {}, "crontab": "", "status": {}}
    
    def generate_crontab(self) -> str:
        """生成 crontab 配置"""
        logger.info(f"📅 生成 crontab 配置")
        
        crontab_lines = [
            "# 太一全域跨境贸易 Agent - 定时任务配置",
            f"# 生成时间：{datetime.now().isoformat()}",
            "",
            "# ========== 自媒体运营任务 =========="
        ]
        
        for task_id, task in self.CRON_TASKS.items():
            cron_line = f"{task['schedule']} cd {WORKSPACE}/skills/01-trading/cross-border-trade-agent && python3 {task['script']} # {task['name']}"
            crontab_lines.append(cron_line)
        
        crontab_lines.extend([
            "",
            "# ========== 系统维护任务 ==========",
            "0 3 * * * find /tmp -type f -mtime +7 -delete # 清理 7 天前临时文件",
            "0 4 * * 0 cd /home/sayelf/.openclaw/workspace && git add -A && git commit -m '自动备份' # 每周备份"
        ])
        
        crontab = "\n".join(crontab_lines)
        self.config["crontab"] = crontab
        self._save_config()
        
        logger.info(f"✅ crontab 配置已生成")
        return crontab
    
    def install_crontab(self) -> Dict:
        """安装 crontab 配置"""
        logger.info(f"📥 安装 crontab 配置")
        
        crontab = self.generate_crontab()
        
        # 保存 crontab 文件
        cron_file = CRON_DIR / "openclaw_cron"
        with open(cron_file, 'w', encoding='utf-8') as f:
            f.write(crontab)
        
        result = {
            "status": "success",
            "file": str(cron_file),
            "task_count": len(self.CRON_TASKS),
            "message": f"crontab 配置已保存到 {cron_file}，请手动执行：crontab {cron_file}"
        }
        
        self.config["status"] = result
        self._save_config()
        
        logger.info(f"✅ crontab 配置已保存：{cron_file}")
        return result
    
    def list_tasks(self) -> List[Dict]:
        """列出所有任务"""
        logger.info(f"📋 列出所有定时任务")
        
        tasks = []
        for task_id, task in self.CRON_TASKS.items():
            tasks.append({
                "id": task_id,
                "name": task["name"],
                "schedule": task["schedule"],
                "script": task["script"],
                "action": task.get("action", "main")
            })
        
        logger.info(f"✅ 共{len(tasks)}个定时任务")
        return tasks
    
    def get_task_schedule(self, task_id: str) -> Dict:
        """获取任务调度信息"""
        if task_id not in self.CRON_TASKS:
            return {"error": "任务不存在"}
        
        task = self.CRON_TASKS[task_id]
        return {
            "id": task_id,
            "name": task["name"],
            "schedule": task["schedule"],
            "schedule_human": self._cron_to_human(task["schedule"]),
            "script": task["script"],
            "action": task.get("action", "main")
        }
    
    def _cron_to_human(self, cron_expr: str) -> str:
        """将 cron 表达式转换为人类可读格式"""
        parts = cron_expr.split()
        if len(parts) != 5:
            return cron_expr
        
        minute, hour, day, month, weekday = parts
        
        time_str = f"{hour.zfill(2)}:{minute.zfill(2)}"
        
        if day == "*" and month == "*":
            if weekday == "*":
                return f"每日 {time_str}"
            elif weekday == "1-5":
                return f"工作日 {time_str}"
            elif weekday == "0":
                return f"每周日 {time_str}"
            elif weekday == "1":
                return f"每周一 {time_str}"
            elif weekday == "5":
                return f"每周五 {time_str}"
        
        return cron_expr
    
    def _save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_config_summary(self) -> Dict:
        """获取配置摘要"""
        return {
            "total_tasks": len(self.CRON_TASKS),
            "crontab_generated": bool(self.config.get("crontab")),
            "status": self.config.get("status", {})
        }


def main():
    logger.info("=" * 60)
    logger.info("📅 定时任务配置 - 自媒体运营自动化")
    logger.info("=" * 60)
    
    generator = CronConfigGenerator()
    
    # 列出所有任务
    logger.info(f"\n📋 定时任务列表:")
    tasks = generator.list_tasks()
    for task in tasks:
        schedule = generator.get_task_schedule(task["id"])
        logger.info(f"  {task['id']}: {task['name']}")
        logger.info(f"    时间：{schedule['schedule_human']}")
        logger.info(f"    脚本：{task['script']}")
    
    # 生成 crontab
    logger.info(f"\n📅 生成 crontab 配置...")
    crontab = generator.generate_crontab()
    logger.info(f"\n{crontab}")
    
    # 安装 crontab
    logger.info(f"\n📥 安装 crontab 配置...")
    result = generator.install_crontab()
    logger.info(f"  状态：{result['status']}")
    logger.info(f"  文件：{result['file']}")
    logger.info(f"  任务数：{result['task_count']}")
    logger.info(f"  说明：{result['message']}")
    
    # 获取摘要
    logger.info(f"\n📊 配置摘要:")
    summary = generator.get_config_summary()
    logger.info(f"  总任务数：{summary['total_tasks']}")
    logger.info(f"  crontab 已生成：{summary['crontab_generated']}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    from typing import List
    main()
