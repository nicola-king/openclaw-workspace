#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台内容采集框架 - 主入口
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from loguru import logger

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core.base import BaseCrawler
from platforms.x_crawler import XCrawler
from platforms.wechat_crawler import WechatCrawler


def setup_logger():
    """配置日志"""
    logger.remove()
    logger.add(
        "output/logs/crawler_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="7 days",
        level="INFO",
        format="{time:HH:mm:ss} | {level} | {message}"
    )
    logger.add(
        sys.stdout,
        level="INFO",
        format="{time:HH:mm:ss} | {level} | {message}"
    )


def load_config() -> Dict:
    """加载配置"""
    config_path = Path(__file__).parent / "config" / "targets.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


async def run_platform(platform: str, config: Dict) -> Dict:
    """运行单个平台采集"""
    logger.info(f"========== 开始采集 {platform} ==========")
    
    if not config.get("enabled", False):
        logger.warning(f"{platform} 未启用，跳过")
        return {"platform": platform, "status": "skipped"}
    
    # 初始化采集器
    if platform == "x":
        crawler = XCrawler(max_results=config.get("max_results", 50))
        targets = (
            config.get("accounts", []) +
            config.get("keywords", []) +
            config.get("hashtags", [])
        )
    elif platform == "wechat":
        crawler = WechatCrawler(max_results=config.get("max_results", 20))
        targets = config.get("accounts", []) + config.get("keywords", [])
    else:
        logger.error(f"未知平台：{platform}")
        return {"platform": platform, "status": "error", "message": "Unknown platform"}
    
    if not targets:
        logger.warning(f"{platform} 没有配置目标，跳过")
        return {"platform": platform, "status": "skipped", "message": "No targets"}
    
    # 执行采集
    try:
        stats = await crawler.run(targets)
        stats["status"] = "success"
        return stats
    except Exception as e:
        logger.error(f"{platform} 采集失败：{e}")
        return {"platform": platform, "status": "error", "message": str(e)}


async def main(platforms: List[str] = None):
    """主函数"""
    setup_logger()
    logger.info(f"🚀 多平台采集框架启动 | {datetime.now().isoformat()}")
    
    config = load_config()
    
    # 确定要运行的平台
    if platforms is None:
        platforms = [p for p, c in config.items() if c.get("enabled", False)]
    
    if not platforms:
        logger.warning("没有启用的平台，请配置 config/targets.json")
        return
    
    logger.info(f"启用的平台：{', '.join(platforms)}")
    
    # 运行采集
    results = []
    for platform in platforms:
        result = await run_platform(platform, config[platform])
        results.append(result)
    
    # 汇总报告
    logger.info("========== 采集完成 ==========")
    for r in results:
        status_icon = "✅" if r["status"] == "success" else "⚠️" if r["status"] == "skipped" else "❌"
        logger.info(f"{status_icon} {r['platform']}: {r['status']}")
        if "results" in r:
            logger.info(f"   采集 {r.get('targets', 0)} 个目标 → {r['results']} 条结果")
    
    # 保存汇总报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "platforms": platforms,
        "results": results
    }
    
    report_path = Path(__file__).parent / "output" / "reports"
    report_path.mkdir(parents=True, exist_ok=True)
    
    report_file = report_path / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"📊 报告已保存：{report_file}")
    
    return report


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="多平台内容采集框架")
    parser.add_argument(
        "--platform",
        type=str,
        nargs="+",
        choices=["x", "wechat", "xiaohongshu"],
        help="指定平台（不指定则运行所有启用的平台）"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="运行测试"
    )
    
    args = parser.parse_args()
    
    if args.test:
        logger.info("运行测试模式...")
        crawler = XCrawler()
        asyncio.run(crawler.test())
    else:
        asyncio.run(main(args.platform))
