#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每月战略定时任务 - 月首 10:00 自动执行
太一 AGI · 2026-04-19 00:07

功能:
- 每月 1 日 10:00 自动生成战略报告
- 推送到 Telegram/微信/邮件
- 保存报告到文件

Cron 配置:
0 10 1 * * python3 /path/to/monthly_strategy_job.py
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
logger = logging.getLogger('MonthlyStrategyJob')


def main():
    """主函数 - 每月战略任务"""
    logger.info("=" * 60)
    logger.info("📊 每月战略任务 - 启动")
    logger.info(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 初始化模块
        delivery = IntelligenceDeliveryModule()
        
        # 生成每月战略
        logger.info("\n📊 生成每月战略报告...")
        monthly_report = delivery.generate_monthly_strategy()
        
        # 格式化消息
        message = f"""📊 跨境贸易每月战略 - {monthly_report['month']}

🌍 市场概览:
• 市场规模：{monthly_report['market_overview']['total_market_size']}
• 增长率：{monthly_report['market_overview']['growth_rate']}
• 核心趋势：{', '.join(monthly_report['market_overview']['key_trends'])}

🎯 战略重点:
"""
        for i, focus in enumerate(monthly_report['strategic_focus'], 1):
            message += f"{i}. {focus['area']} ({focus['priority']}) - {focus['investment']}\n"
        
        message += "\n⚠️ 风险评估:\n"
        for risk in monthly_report['risk_assessment']:
            message += f"• {risk['risk']} ({risk['level']}) - {risk['mitigation']}\n"
        
        message += f"\n═══════════════════════════════════════\n"
        message += f"生成时间：{monthly_report['generated_at']}\n"
        message += f"太一 AGI · 跨境贸易战略系统"
        
        # 保存报告
        logger.info("\n💾 保存报告...")
        report_file = delivery.save_daily_report(monthly_report)
        logger.info(f"报告已保存：{report_file}")
        
        # 发送到渠道
        logger.info("\n📤 发送渠道...")
        send_result = delivery.send_to_channels(message)
        logger.info(f"发送结果：{send_result['status']}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 每月战略任务 - 完成")
        logger.info("=" * 60)
        
        return {"status": "success", "report_file": report_file}
        
    except Exception as e:
        logger.error(f"❌ 每月战略任务 - 失败：{str(e)}")
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    main()
