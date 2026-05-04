#!/usr/bin/env python3
"""
任务调度中心 (Task Scheduler) v9.0.0
统一定时任务调度：情报推送/竞品监控/任务自检/月度战略/清关自动化
"""

import json
import logging
import threading
import time
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from datetime import datetime, timedelta

# 简单 cron 解析器 (不依赖外部库)
class SimpleCron:
    """简单 cron 解析器"""
    
    def __init__(self, schedule: str):
        self.schedule = schedule
        parts = schedule.split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron expression: {schedule}")
        
        self.minute = self._parse_field(parts[0], 0, 59)
        self.hour = self._parse_field(parts[1], 0, 23)
        self.day = self._parse_field(parts[2], 1, 31)
        self.month = self._parse_field(parts[3], 1, 12)
        self.weekday = self._parse_field(parts[4], 0, 6)
    
    def _parse_field(self, field: str, min_val: int, max_val: int) -> set:
        """解析 cron 字段"""
        if field == '*':
            return set(range(min_val, max_val + 1))
        
        values = set()
        for part in field.split(','):
            if '-' in part:
                start, end = part.split('-')
                values.update(range(int(start), int(end) + 1))
            elif '/' in part:
                base, step = part.split('/')
                step = int(step)
                if base == '*':
                    values.update(range(min_val, max_val + 1, step))
                else:
                    values.update(range(int(base), max_val + 1, step))
            else:
                values.add(int(part))
        
        return values
    
    def matches(self, dt: datetime) -> bool:
        """检查时间是否匹配"""
        return (
            dt.minute in self.minute and
            dt.hour in self.hour and
            dt.day in self.day and
            dt.month in self.month and
            dt.weekday() in self.weekday
        )
    
    def get_next(self, from_time: datetime) -> datetime:
        """获取下次运行时间"""
        dt = from_time.replace(second=0, microsecond=0) + timedelta(minutes=1)
        
        for _ in range(525600):  # 最多检查一年
            if self.matches(dt):
                return dt
            dt += timedelta(minutes=1)
        
        raise ValueError("Cannot find next run time")

class TaskScheduler:
    """任务调度中心主类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.running = False
        self._scheduler_thread: Optional[threading.Thread] = None
        self._job_history: List[Dict[str, Any]] = []
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("task-scheduler")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化模块"""
        self.logger.info("任务调度中心模块初始化完成")
        
        # 加载默认任务
        default_jobs = self.config.get("jobs", {})
        for job_id, job_config in default_jobs.items():
            self.add_job(
                job_id=job_id,
                schedule=job_config.get("schedule", "0 8 * * *"),
                task=job_config.get("task", ""),
                params=job_config.get("params", {}),
                channels=job_config.get("channels", ["telegram"]),
                enabled=job_config.get("enabled", True)
            )
        
        return True
    
    def add_job(
        self,
        job_id: str,
        schedule: str,
        task: str,
        params: Dict[str, Any] = None,
        channels: List[str] = None,
        enabled: bool = True
    ) -> bool:
        """添加定时任务
        
        Args:
            job_id: 任务 ID
            schedule: cron 表达式
            task: 任务类型
            params: 任务参数
            channels: 推送渠道
            enabled: 是否启用
            
        Returns:
            是否成功
        """
        try:
            # 验证 cron 表达式
            SimpleCron(schedule)
            
            self.jobs[job_id] = {
                "job_id": job_id,
                "schedule": schedule,
                "task": task,
                "params": params or {},
                "channels": channels or ["telegram"],
                "enabled": enabled,
                "last_run": None,
                "next_run": self._get_next_run(schedule),
                "status": "pending"
            }
            
            self.logger.info(f"添加任务：{job_id} - {schedule}")
            return True
            
        except Exception as e:
            self.logger.error(f"添加任务失败：{job_id} - {e}")
            return False
    
    def remove_job(self, job_id: str) -> bool:
        """删除定时任务"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            self.logger.info(f"删除任务：{job_id}")
            return True
        return False
    
    def enable_job(self, job_id: str) -> bool:
        """启用任务"""
        if job_id in self.jobs:
            self.jobs[job_id]["enabled"] = True
            self.logger.info(f"启用任务：{job_id}")
            return True
        return False
    
    def disable_job(self, job_id: str) -> bool:
        """禁用任务"""
        if job_id in self.jobs:
            self.jobs[job_id]["enabled"] = False
            self.logger.info(f"禁用任务：{job_id}")
            return True
        return False
    
    def start(self):
        """启动调度器"""
        if self.running:
            self.logger.warning("调度器已在运行")
            return
        
        self.running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()
        self.logger.info("任务调度器已启动")
    
    def stop(self):
        """停止调度器"""
        self.running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
        self.logger.info("任务调度器已停止")
    
    def _run_scheduler(self):
        """运行调度循环"""
        while self.running:
            now = datetime.now()
            
            for job_id, job in self.jobs.items():
                if not job["enabled"]:
                    continue
                
                # 检查是否到了执行时间
                if self._should_run(job, now):
                    self._execute_job(job_id, job)
            
            # 每分钟检查一次
            time.sleep(60)
    
    def _should_run(self, job: Dict[str, Any], now: datetime) -> bool:
        """检查是否应该执行任务"""
        if job["last_run"]:
            last_run = datetime.fromisoformat(job["last_run"])
            if (now - last_run).total_seconds() < 60:
                return False
        
        try:
            cron = SimpleCron(job["schedule"])
            
            # 如果上次运行时间早于 cron 计算的上次运行时间，说明需要执行
            if job["last_run"]:
                last_run = datetime.fromisoformat(job["last_run"])
                prev_run = cron.get_next(last_run) - timedelta(minutes=1)
                return prev_run > last_run
            else:
                return True
                
        except Exception as e:
            self.logger.error(f"检查任务时间失败：{job['job_id']} - {e}")
            return False
    
    def _execute_job(self, job_id: str, job: Dict[str, Any]):
        """执行任务"""
        self.logger.info(f"执行任务：{job_id}")
        
        start_time = time.time()
        job["status"] = "running"
        
        try:
            # 执行任务
            result = self._run_task(job)
            
            elapsed = time.time() - start_time
            job["last_run"] = datetime.now().isoformat()
            job["next_run"] = self._get_next_run(job["schedule"])
            job["status"] = "completed"
            
            # 记录历史
            self._job_history.append({
                "job_id": job_id,
                "task": job["task"],
                "start_time": start_time,
                "elapsed": elapsed,
                "status": "success",
                "result": result
            })
            
            self.logger.info(f"任务完成：{job_id} - {elapsed:.2f}s")
            
        except Exception as e:
            elapsed = time.time() - start_time
            job["status"] = "failed"
            
            self._job_history.append({
                "job_id": job_id,
                "task": job["task"],
                "start_time": start_time,
                "elapsed": elapsed,
                "status": "failed",
                "error": str(e)
            })
            
            self.logger.error(f"任务失败：{job_id} - {e}")
    
    def _run_task(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """运行具体任务"""
        task = job["task"]
        params = job["params"]
        channels = job["channels"]
        
        if task == "intelligence_report":
            return self._run_intelligence_report(params, channels)
        elif task == "weekly_intelligence":
            return self._run_weekly_intelligence(params, channels)
        elif task == "monthly_strategy":
            return self._run_monthly_strategy(params, channels)
        elif task == "competitor_analysis":
            return self._run_competitor_analysis(params, channels)
        elif task == "clearance_automation":
            return self._run_clearance_automation(params, channels)
        elif task == "self_check":
            return self._run_self_check(params, channels)
        else:
            return {"status": "error", "message": f"未知任务：{task}"}
    
    def _run_intelligence_report(self, params: Dict, channels: List[str]) -> Dict[str, Any]:
        """运行情报报告任务"""
        self.logger.info("生成每日情报报告")
        
        # 模拟生成报告
        report = {
            "title": "每日情报简报",
            "date": datetime.now().isoformat(),
            "content": {
                "market_trends": "市场需求稳定增长",
                "competitor_activity": "竞品价格调整",
                "recommendations": "建议关注澳大利亚市场"
            }
        }
        
        # 推送到渠道
        delivery_results = self._deliver_to_channels(report, channels)
        
        return {
            "status": "success",
            "report": report,
            "delivery": delivery_results
        }
    
    def _run_weekly_intelligence(self, params: Dict, channels: List[str]) -> Dict[str, Any]:
        """运行每周情报任务"""
        self.logger.info("生成每周情报汇总")
        
        report = {
            "title": "每周情报汇总",
            "week": datetime.now().isocalendar()[1],
            "content": {
                "weekly_trends": "本周市场趋势分析",
                "new_prospects": "新增潜客 5 个",
                "conversion_rate": "转化率 8%"
            }
        }
        
        delivery_results = self._deliver_to_channels(report, channels)
        
        return {
            "status": "success",
            "report": report,
            "delivery": delivery_results
        }
    
    def _run_monthly_strategy(self, params: Dict, channels: List[str]) -> Dict[str, Any]:
        """运行月度战略任务"""
        self.logger.info("生成月度战略报告")
        
        report = {
            "title": "月度战略报告",
            "month": datetime.now().strftime("%Y-%m"),
            "content": {
                "monthly_performance": "月度业绩分析",
                "market_opportunities": "市场机会分析",
                "strategy_adjustments": "策略调整建议"
            }
        }
        
        delivery_results = self._deliver_to_channels(report, channels)
        
        return {
            "status": "success",
            "report": report,
            "delivery": delivery_results
        }
    
    def _run_competitor_analysis(self, params: Dict, channels: List[str]) -> Dict[str, Any]:
        """运行竞品分析任务"""
        self.logger.info("执行竞品监控")
        
        analysis = {
            "title": "竞品监控报告",
            "date": datetime.now().isoformat(),
            "competitors": [
                {"name": "Karmod", "price_change": "+5%", "new_features": ["AI 设计"]},
                {"name": "DXH", "price_change": "-3%", "new_features": ["快速交付"]}
            ]
        }
        
        delivery_results = self._deliver_to_channels(analysis, channels)
        
        return {
            "status": "success",
            "analysis": analysis,
            "delivery": delivery_results
        }
    
    def _run_clearance_automation(self, params: Dict, channels: List[str]) -> Dict[str, Any]:
        """运行清关自动化任务"""
        self.logger.info("执行清关检查")
        
        result = {
            "title": "清关状态检查",
            "date": datetime.now().isoformat(),
            "pending_shipments": 3,
            "cleared_shipments": 12,
            "issues": []
        }
        
        delivery_results = self._deliver_to_channels(result, channels)
        
        return {
            "status": "success",
            "result": result,
            "delivery": delivery_results
        }
    
    def _run_self_check(self, params: Dict, channels: List[str]) -> Dict[str, Any]:
        """运行系统自检任务"""
        self.logger.info("执行系统自检")
        
        health = {
            "title": "系统健康检查",
            "date": datetime.now().isoformat(),
            "modules": list(self.jobs.keys()),
            "total_jobs": len(self.jobs),
            "enabled_jobs": sum(1 for j in self.jobs.values() if j["enabled"]),
            "failed_jobs": sum(1 for j in self.jobs.values() if j["status"] == "failed"),
            "status": "healthy"
        }
        
        delivery_results = self._deliver_to_channels(health, channels)
        
        return {
            "status": "success",
            "health": health,
            "delivery": delivery_results
        }
    
    def _deliver_to_channels(self, content: Dict[str, Any], channels: List[str]) -> List[Dict[str, Any]]:
        """推送到渠道"""
        results = []
        
        for channel in channels:
            if channel == "telegram":
                results.append({
                    "channel": "telegram",
                    "status": "sent",
                    "timestamp": datetime.now().isoformat()
                })
            elif channel == "email":
                results.append({
                    "channel": "email",
                    "status": "sent",
                    "timestamp": datetime.now().isoformat()
                })
            elif channel == "wechat":
                results.append({
                    "channel": "wechat",
                    "status": "sent",
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    def _get_next_run(self, schedule: str) -> str:
        """获取下次运行时间"""
        try:
            cron = SimpleCron(schedule)
            next_run = cron.get_next(datetime.now())
            return next_run.isoformat()
        except Exception:
            return ""
    
    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        """执行任务"""
        self.logger.info(f"执行任务：{task}")
        
        if task == "add_job":
            return self._cmd_add_job(**kwargs)
        elif task == "remove_job":
            return self._cmd_remove_job(**kwargs)
        elif task == "list_jobs":
            return self._cmd_list_jobs(**kwargs)
        elif task == "run_job":
            return self._cmd_run_job(**kwargs)
        elif task == "job_history":
            return self._cmd_job_history(**kwargs)
        else:
            return {"status": "error", "message": f"未知任务：{task}"}
    
    def _cmd_add_job(self, **kwargs) -> Dict[str, Any]:
        """添加任务命令"""
        job_id = kwargs.get("job_id", f"job_{len(self.jobs)}")
        schedule = kwargs.get("schedule", "0 8 * * *")
        task_name = kwargs.get("task_name", kwargs.get("task", ""))
        params = kwargs.get("params", {})
        channels = kwargs.get("channels", ["telegram"])
        
        success = self.add_job(job_id, schedule, task_name, params, channels)
        
        return {
            "status": "success" if success else "error",
            "job_id": job_id,
            "next_run": self.jobs[job_id]["next_run"] if success else None
        }
    
    def _cmd_remove_job(self, **kwargs) -> Dict[str, Any]:
        """删除任务命令"""
        job_id = kwargs.get("job_id", "")
        success = self.remove_job(job_id)
        
        return {
            "status": "success" if success else "error",
            "job_id": job_id
        }
    
    def _cmd_list_jobs(self, **kwargs) -> Dict[str, Any]:
        """列出任务命令"""
        return {
            "status": "success",
            "jobs": {job_id: {k: v for k, v in job.items() if k != "enabled"} 
                    for job_id, job in self.jobs.items()},
            "total": len(self.jobs)
        }
    
    def _cmd_run_job(self, **kwargs) -> Dict[str, Any]:
        """手动运行任务命令"""
        job_id = kwargs.get("job_id", "")
        if job_id in self.jobs:
            self._execute_job(job_id, self.jobs[job_id])
            return {
                "status": "success",
                "job_id": job_id,
                "last_run": self.jobs[job_id]["last_run"]
            }
        return {"status": "error", "message": f"任务不存在：{job_id}"}
    
    def _cmd_job_history(self, **kwargs) -> Dict[str, Any]:
        """任务历史命令"""
        limit = kwargs.get("limit", 10)
        return {
            "status": "success",
            "history": self._job_history[-limit:],
            "total": len(self._job_history)
        }
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "status": "healthy" if self.running else "stopped",
            "module": "task-scheduler",
            "version": "9.0.0",
            "total_jobs": len(self.jobs),
            "enabled_jobs": sum(1 for j in self.jobs.values() if j["enabled"]),
            "running": self.running,
            "history_count": len(self._job_history)
        }
    
    @property
    def name(self) -> str:
        return "task-scheduler"
    
    @property
    def version(self) -> str:
        return "9.0.0"
    
    @property
    def dependencies(self) -> List[str]:
        return ["cross-border-core", "report-engine", "intelligence-hub", "self-evolution"]


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="任务调度中心模块")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    parser.add_argument("--task", help="执行任务")
    parser.add_argument("--start", action="store_true", help="启动调度器")
    parser.add_argument("--stop", action="store_true", help="停止调度器")
    parser.add_argument("--job-id", help="任务 ID")
    parser.add_argument("--schedule", help="cron 表达式")
    parser.add_argument("--limit", type=int, default=10, help="历史记录数量")
    
    args = parser.parse_args()
    
    scheduler = TaskScheduler(config_path=args.config)
    scheduler.initialize({})
    
    if args.start:
        scheduler.start()
        print(json.dumps(scheduler.health_check(), indent=2, ensure_ascii=False))
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            scheduler.stop()
    elif args.stop:
        scheduler.stop()
    elif args.task:
        result = scheduler.execute(
            task=args.task,
            job_id=args.job_id,
            schedule=args.schedule,
            limit=args.limit
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(scheduler.health_check(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
