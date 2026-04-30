#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X 爬虫自进化智能体 - 统一架构版本

功能:
1. 条件触发 (爬取失败/数据异常时触发)
2. 自动自愈 (重试/切换账号)
3. 学习能力 (分析失败模式)
4. 知识固化 (写入 PITFALLS.md)

作者：太一 AGI
创建：2026-04-23
版本：v2.0 (自进化智能体)
"""

import sys
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
sys.path.insert(0, str(WORKSPACE / "skills" / "07-system"))
from self_evolving_task_base import SelfEvolvingTask, TaskResult

class XCrawlerSelfEvolving(SelfEvolvingTask):
    """X 爬虫自进化智能体"""
    
    def __init__(self):
        super().__init__("x_crawler")
        self.crawl_status = None
    
    def check(self) -> TaskResult:
        """条件检查 - 爬虫是否正常工作"""
        try:
            # 检查爬虫脚本
            crawler_script = WORKSPACE / "skills" / "01-trading" / "zhiji" / "x_crawler_cron.sh"
            
            if not crawler_script.exists():
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error='爬虫脚本不存在'
                )
            
            # 检查最近一次爬取结果
            social_signals_file = WORKSPACE / "data" / "x-social-crawler" / "social_signals_latest.json"
            trading_signals_file = WORKSPACE / "data" / "x-social-crawler" / "trading_signals_latest.json"
            
            has_social = social_signals_file.exists()
            has_trading = trading_signals_file.exists()
            
            if has_social and has_trading:
                return TaskResult(
                    task_id=self.task_id,
                    success=True,
                    need_heal=False,
                    error=None
                )
            elif has_social or has_trading:
                return TaskResult(
                    task_id=self.task_id,
                    success=True,
                    need_heal=False,
                    error='部分数据缺失'
                )
            else:
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error='爬虫数据完全缺失'
                )
                
        except Exception as e:
            return TaskResult(
                task_id=self.task_id,
                success=False,
                need_heal=True,
                error=f'检查失败：{str(e)}'
            )
    
    def heal(self, error: str) -> bool:
        """自动自愈 - 触发爬虫"""
        try:
            import subprocess
            
            if '脚本不存在' in error:
                return False
            
            # 触发爬虫脚本
            crawler_script = WORKSPACE / "skills" / "01-trading" / "zhiji" / "x_crawler_cron.sh"
            
            if crawler_script.exists():
                result = subprocess.run(
                    ['bash', str(crawler_script)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    self.write_to_pitfalls(
                        f'爬虫数据缺失：{error}',
                        '自动触发爬虫脚本执行'
                    )
                    return True
                else:
                    return False
            else:
                return False
                
        except Exception as e:
            print(f"自愈失败：{str(e)}")
            return False

if __name__ == '__main__':
    crawler = XCrawlerSelfEvolving()
    result = crawler.execute()
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🐦 X 爬虫自进化智能体")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"执行结果：{'✅ 成功' if result.success else '❌ 失败'}")
    print(f"需要自愈：{'🔧 是' if result.need_heal else '❌ 否'}")
    if result.error:
        print(f"错误信息：{result.error}")
    print(f"")
    print(f"进化指标:")
    print(f"  总运行次数：{crawler.metrics.total_runs}")
    print(f"  发现问题：{crawler.metrics.issues_found}")
    print(f"  自愈成功：{crawler.metrics.auto_healed}")
    print(f"  成功率：{crawler.metrics.success_rate:.1f}%")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
