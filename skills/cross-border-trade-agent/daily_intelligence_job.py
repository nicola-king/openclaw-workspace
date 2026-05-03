#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日情报定时任务 - 08:00 自动执行
太一 AGI · 2026-04-19 00:00

功能:
- 每日 08:00 自动生成情报
- 推送到 Telegram/微信/邮件
- 保存报告到文件

Cron 配置:
0 8 * * * python3 /path/to/daily_intelligence_job.py
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from intelligence_delivery_module import IntelligenceDeliveryModule

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('DailyIntelligenceJob')


def main():
    """主函数 - 每日情报任务"""
    logger.info("=" * 60)
    logger.info("📊 每日情报任务 - 启动")
    logger.info(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 初始化模块
        delivery = IntelligenceDeliveryModule()
        
        # 生成每日情报
        logger.info("\n📊 生成每日情报...")
        daily_report = delivery.generate_daily_intelligence()
        
        # 格式化消息
        message = delivery.format_daily_message(daily_report)
        
        # 保存报告
        logger.info("\n💾 保存报告...")
        report_file = delivery.save_daily_report(daily_report)
        logger.info(f"报告已保存：{report_file}")
        
        # 发送到渠道
        logger.info("\n📤 发送渠道...")
        send_result = delivery.send_to_channels(message)
        logger.info(f"发送结果：{send_result['status']}")
        logger.info(f"发送渠道：{send_result['channels']}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 每日情报任务 - 完成")
        logger.info("=" * 60)
        
        return {"status": "success", "report_file": report_file}
        
    except Exception as e:
        logger.error(f"❌ 每日情报任务 - 失败：{str(e)}")
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    main()
