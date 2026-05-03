#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品监控定时任务 - 每 4 小时自动执行
太一 AGI · 2026-04-19 00:07

功能:
- 每 4 小时自动监控竞品
- 发现动态立即预警
- 保存到文件

Cron 配置:
0 */4 * * * python3 /path/to/competitor_monitor_job.py
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from competitor_monitor import CompetitorMonitorModule

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('CompetitorMonitorJob')


def main():
    """主函数 - 竞品监控任务"""
    logger.info("=" * 60)
    logger.info("🔍 竞品监控任务 - 启动")
    logger.info(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 初始化模块
        monitor = CompetitorMonitorModule()
        
        # 监控所有竞品
        logger.info("\n🔍 监控所有竞品...")
        updates = monitor.monitor_all_competitors()
        
        # 生成报告
        logger.info("\n📋 生成竞品报告...")
        report = monitor.generate_competitor_report(updates)
        
        # 保存报告
        logger.info("\n💾 保存报告...")
        report_file = monitor.save_report(report)
        logger.info(f"报告已保存：{report_file}")
        
        # 发送预警
        logger.info("\n🚨 发送预警...")
        for update in updates:
            if update.get("level") in ["high", "critical"]:
                monitor.send_alert(update)
                logger.info(f"  → {update['competitor']}: 预警已发送")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 竞品监控任务 - 完成")
        logger.info(f"发现动态：{len(updates)}个")
        logger.info("=" * 60)
        
        return {"status": "success", "updates_count": len(updates)}
        
    except Exception as e:
        logger.error(f"❌ 竞品监控任务 - 失败：{str(e)}")
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    main()
