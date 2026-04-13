#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillHub 每小时报告发送 Agent v3.0

每小时整点执行:
1. 收集过去 1 小时的自进化报告
2. 生成汇总报告
3. 发送到 Telegram
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SkillhubHourlyReporter')


class SkillhubHourlyReporter:
    """SkillHub 每小时报告发送 Agent"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.reports_dir = self.workspace / 'reports'
        
        logger.info("📊 SkillHub 每小时报告发送 Agent 已初始化")
    
    def run(self):
        """运行报告发送"""
        logger.info("📊 开始生成每小时报告...")
        
        # Step 1: 收集过去 1 小时的报告
        hourly_reports = self.collect_hourly_reports()
        
        # Step 2: 生成汇总报告
        summary = self.generate_summary(hourly_reports)
        
        # Step 3: 保存汇总报告
        self.save_summary(summary)
        
        # Step 4: 发送 Telegram (模拟)
        self.send_telegram(summary)
        
        logger.info("✅ 每小时报告发送完成！")
    
    def collect_hourly_reports(self) -> list:
        """收集过去 1 小时的报告"""
        logger.info("📂 收集过去 1 小时的报告...")
        
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        
        reports = []
        for report_file in self.reports_dir.glob('self-evolution-*.json'):
            try:
                mtime = datetime.fromtimestamp(report_file.stat().st_mtime)
                if one_hour_ago <= mtime <= now:
                    with open(report_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        reports.append(data)
            except Exception as e:
                logger.warning(f"  ⚠️ 读取失败：{report_file} - {e}")
        
        logger.info(f"  收集到报告：{len(reports)} 个")
        
        return reports
    
    def generate_summary(self, reports: list) -> dict:
        """生成汇总报告"""
        logger.info("📊 生成汇总报告...")
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'period_start': (datetime.now() - timedelta(hours=1)).isoformat(),
            'period_end': datetime.now().isoformat(),
            'total_executions': len(reports),
            'total_skills_created': sum(r.get('skills_created', 0) for r in reports),
            'total_signals': sum(r.get('signals_detected', 0) for r in reports),
            'reports': reports,
        }
        
        logger.info(f"  总执行：{summary['total_executions']} 次")
        logger.info(f"  总技能创建：{summary['total_skills_created']} 个")
        logger.info(f"  总信号检测：{summary['total_signals']} 个")
        
        return summary
    
    def save_summary(self, summary: dict):
        """保存汇总报告"""
        timestamp = datetime.now().strftime('%Y%m%d-%H0000')
        summary_file = self.reports_dir / f'hourly-summary-{timestamp}.json'
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 汇总报告已保存：{summary_file}")
    
    def send_telegram(self, summary: dict):
        """发送 Telegram (模拟)"""
        logger.info("📱 准备发送 Telegram...")
        
        message = f"""📊 太一自进化小时报告

时间：{summary['period_start'][:16]} - {summary['period_end'][:16]}

执行统计:
- 执行次数：{summary['total_executions']} 次
- 技能创建：{summary['total_skills_created']} 个
- 信号检测：{summary['total_signals']} 个

状态：✅ 正常
"""
        
        logger.info(f"📱 Telegram 消息:\n{message}")
        logger.info("✅ Telegram 发送完成 (模拟)")


def main():
    logger.info("📊 SkillHub 每小时报告发送 Agent 启动...")
    reporter = SkillhubHourlyReporter()
    reporter.run()


if __name__ == '__main__':
    main()
