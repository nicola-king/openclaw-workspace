#!/usr/bin/env python3
"""
任务调度中心模块测试
"""

import unittest
import json
import sys
import time
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import TaskScheduler


class TestTaskScheduler(unittest.TestCase):
    """任务调度中心测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.scheduler = TaskScheduler()
        self.scheduler.initialize({})
    
    def test_add_job(self):
        """测试添加任务"""
        result = self.scheduler.execute(
            task="add_job",
            job_id="test_job",
            schedule="0 12 * * *",
            task_name="intelligence_report"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["job_id"], "test_job")
    
    def test_remove_job(self):
        """测试删除任务"""
        # 先添加
        self.scheduler.add_job("test_remove", "0 12 * * *", "intelligence_report")
        
        # 再删除
        result = self.scheduler.execute(task="remove_job", job_id="test_remove")
        self.assertEqual(result["status"], "success")
        self.assertNotIn("test_remove", self.scheduler.jobs)
    
    def test_list_jobs(self):
        """测试列出任务"""
        result = self.scheduler.execute(task="list_jobs")
        self.assertEqual(result["status"], "success")
        self.assertIn("jobs", result)
        self.assertGreater(result["total"], 0)
    
    def test_run_job(self):
        """测试手动运行任务"""
        result = self.scheduler.execute(task="run_job", job_id="daily_intelligence")
        self.assertEqual(result["status"], "success")
        self.assertIn("last_run", result)
    
    def test_job_history(self):
        """测试任务历史"""
        # 先运行一个任务
        self.scheduler.execute(task="run_job", job_id="daily_intelligence")
        
        # 查看历史
        result = self.scheduler.execute(task="job_history", limit=5)
        self.assertEqual(result["status"], "success")
        self.assertIn("history", result)
        self.assertGreater(result["total"], 0)
    
    def test_enable_disable_job(self):
        """测试启用/禁用任务"""
        # 禁用
        result = self.scheduler.disable_job("daily_intelligence")
        self.assertTrue(result)
        self.assertFalse(self.scheduler.jobs["daily_intelligence"]["enabled"])
        
        # 启用
        result = self.scheduler.enable_job("daily_intelligence")
        self.assertTrue(result)
        self.assertTrue(self.scheduler.jobs["daily_intelligence"]["enabled"])
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.scheduler.health_check()
        self.assertEqual(result["status"], "stopped")  # 未启动
        self.assertEqual(result["module"], "task-scheduler")
        self.assertEqual(result["version"], "9.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.scheduler.name, "task-scheduler")
        self.assertEqual(self.scheduler.version, "9.0.0")
        self.assertIn("cross-border-core", self.scheduler.dependencies)
        self.assertIn("report-engine", self.scheduler.dependencies)
        self.assertIn("intelligence-hub", self.scheduler.dependencies)
    
    def test_start_stop(self):
        """测试启动/停止"""
        self.scheduler.start()
        self.assertTrue(self.scheduler.running)
        
        time.sleep(1)  # 等待启动
        
        self.scheduler.stop()
        self.assertFalse(self.scheduler.running)
    
    def test_invalid_cron(self):
        """测试无效 cron 表达式"""
        result = self.scheduler.add_job("invalid_job", "invalid cron", "test_task")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
