#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务自查定时任务 - 每日 05:00 自动执行
太一 AGI · 2026-04-19 00:16

功能:
- 每日 05:00 自动检查所有定时任务
- 发现问题自动修复
- 生成自查报告
- 发送告警 (如有严重问题)

Cron 配置:
0 5 * * * python3 /path/to/scheduled_task_self_check_job.py
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from scheduled_task_self_check import ScheduledTaskSelfCheckModule

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('SelfCheckJob')


def main():
    """主函数 - 自查任务"""
    logger.info("=" * 60)
    logger.info("🔍 定时任务自查任务 - 启动")
    logger.info(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 初始化模块
        self_check = ScheduledTaskSelfCheckModule()
        
        # 创建 cron 配置
        logger.info("\n📋 检查 cron 配置...")
        self_check._create_cron_config()
        
        # 检查所有任务
        logger.info("\n🔍 检查所有定时任务...")
        results = self_check.check_all_tasks()
        
        # 自动修复
        logger.info("\n🔧 自动修复问题...")
        fix_records = self_check.auto_fix_issues(results)
        
        # 生成报告
        logger.info("\n📋 生成报告...")
        report = self_check._generate_self_check_report(results)
        
        # 保存报告
        logger.info("\n💾 保存报告...")
        report_file = self_check.save_report(report)
        logger.info(f"报告已保存：{report_file}")
        
        # 导出摘要
        logger.info("\n📄 导出摘要...")
        summary_file = self_check.export_summary(report)
        logger.info(f"摘要已导出：{summary_file}")
        
        # 检查是否有严重问题
        error_count = report['summary']['error']
        if error_count > 0:
            logger.warning(f"\n⚠️ 发现{error_count}个严重错误，需要立即处理！")
            # 这里可以添加告警推送逻辑
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 定时任务自查任务 - 完成")
        logger.info(f"总任务数：{report['summary']['total_tasks']}")
        logger.info(f"正常：{report['summary']['ok']}")
        logger.info(f"警告：{report['summary']['warning']}")
        logger.info(f"错误：{report['summary']['error']}")
        logger.info(f"修复尝试：{len(fix_records)}个")
        logger.info("=" * 60)
        
        return {
            "status": "success",
            "total_tasks": report['summary']['total_tasks'],
            "ok": report['summary']['ok'],
            "warning": report['summary']['warning'],
            "error": report['summary']['error'],
            "fixes_attempted": len(fix_records)
        }
        
    except Exception as e:
        logger.error(f"❌ 定时任务自查任务 - 失败：{str(e)}")
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    main()
