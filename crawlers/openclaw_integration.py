#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 集成 - 定时任务和自动化
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from loguru import logger

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from main import main as run_crawler


def setup_logger():
    """配置日志"""
    logger.remove()
    logger.add(
        "output/logs/openclaw_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="7 days",
        level="INFO"
    )


async def daily_task():
    """每日定时任务"""
    setup_logger()
    logger.info("🕐 执行每日采集任务...")
    
    try:
        report = await run_crawler()
        
        # 发送到 OpenClaw 消息
        if report:
            summary = generate_summary(report)
            logger.info(f"📊 采集汇总：{summary}")
            
            # 可以集成到 OpenClaw 消息系统
            # await send_to_openclaw(summary)
            
        return report
        
    except Exception as e:
        logger.error(f"❌ 任务执行失败：{e}")
        return None


def generate_summary(report: dict) -> str:
    """生成汇总报告"""
    lines = ["📊 多平台采集日报", f"时间：{report.get('timestamp', '')}", ""]
    
    for result in report.get("results", []):
        platform = result.get("platform", "unknown")
        status = result.get("status", "unknown")
        
        icon = "✅" if status == "success" else "⚠️" if status == "skipped" else "❌"
        line = f"{icon} {platform}: {status}"
        
        if status == "success":
            targets = result.get("targets", 0)
            results_count = result.get("results", 0)
            line += f" | {targets} 目标 → {results_count} 条"
        
        lines.append(line)
    
    return "\n".join(lines)


# OpenClaw 命令入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 采集集成")
    parser.add_argument("action", choices=["daily", "weekly", "test"], help="执行动作")
    args = parser.parse_args()
    
    if args.action == "test":
        logger.info("运行测试...")
        from platforms.x_crawler import XCrawler
        crawler = XCrawler()
        asyncio.run(crawler.test())
    else:
        asyncio.run(daily_task())
