#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统资源监控模块 - 太一贵客
太一 AGI · 2026-04-19 20:39

功能:
- CPU 使用率监控
- 内存使用率监控
- 磁盘使用率监控
- 进程状态监控
- 告警通知
"""

import json
import logging
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SystemMonitor')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
MONITOR_DIR = WORKSPACE / "data" / "cross-border" / "system_monitor"
MONITOR_DIR.mkdir(parents=True, exist_ok=True)


class SystemMonitor:
    """系统资源监控"""
    
    # 告警阈值
    THRESHOLDS = {
        "cpu_warning": 80,
        "cpu_critical": 95,
        "memory_warning": 80,
        "memory_critical": 95,
        "disk_warning": 80,
        "disk_critical": 95
    }
    
    def __init__(self):
        self.monitor_file = MONITOR_DIR / "system_monitor.json"
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        if self.monitor_file.exists():
            with open(self.monitor_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"history": [], "alerts": []}
    
    def check_cpu(self) -> Dict:
        """检查 CPU 使用率"""
        cpu_percent = psutil.cpu_percent(interval=1)
        
        result = {
            "type": "cpu",
            "value": cpu_percent,
            "unit": "%",
            "status": "normal",
            "checked_at": datetime.now().isoformat()
        }
        
        if cpu_percent >= self.THRESHOLDS["cpu_critical"]:
            result["status"] = "critical"
            self._send_alert("CPU 使用率过高", cpu_percent, "critical")
        elif cpu_percent >= self.THRESHOLDS["cpu_warning"]:
            result["status"] = "warning"
            self._send_alert("CPU 使用率偏高", cpu_percent, "warning")
        
        logger.info(f"CPU 使用率：{cpu_percent}% [{result['status']}]")
        return result
    
    def check_memory(self) -> Dict:
        """检查内存使用率"""
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        result = {
            "type": "memory",
            "value": memory_percent,
            "unit": "%",
            "total_gb": round(memory.total / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "status": "normal",
            "checked_at": datetime.now().isoformat()
        }
        
        if memory_percent >= self.THRESHOLDS["memory_critical"]:
            result["status"] = "critical"
            self._send_alert("内存使用率过高", memory_percent, "critical")
        elif memory_percent >= self.THRESHOLDS["memory_warning"]:
            result["status"] = "warning"
            self._send_alert("内存使用率偏高", memory_percent, "warning")
        
        logger.info(f"内存使用率：{memory_percent}% (已用{result['used_gb']}GB/总共{result['total_gb']}GB) [{result['status']}]")
        return result
    
    def check_disk(self, path: str = "/") -> Dict:
        """检查磁盘使用率"""
        disk = psutil.disk_usage(path)
        disk_percent = disk.percent
        
        result = {
            "type": "disk",
            "path": path,
            "value": disk_percent,
            "unit": "%",
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "status": "normal",
            "checked_at": datetime.now().isoformat()
        }
        
        if disk_percent >= self.THRESHOLDS["disk_critical"]:
            result["status"] = "critical"
            self._send_alert("磁盘使用率过高", disk_percent, "critical")
        elif disk_percent >= self.THRESHOLDS["disk_warning"]:
            result["status"] = "warning"
            self._send_alert("磁盘使用率偏高", disk_percent, "warning")
        
        logger.info(f"磁盘使用率：{disk_percent}% (已用{result['used_gb']}GB/总共{result['total_gb']}GB) [{result['status']}]")
        return result
    
    def check_processes(self) -> Dict:
        """检查进程状态"""
        # 检查 Python 进程
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if 'python' in proc.info['name'].lower():
                    python_processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "memory_percent": proc.info['memory_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        result = {
            "type": "processes",
            "total_python_processes": len(python_processes),
            "processes": python_processes[:10],  # 只显示前 10 个
            "checked_at": datetime.now().isoformat()
        }
        
        logger.info(f"Python 进程数：{len(python_processes)}")
        return result
    
    def _send_alert(self, message: str, value: float, level: str):
        """发送告警"""
        alert = {
            "id": f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "message": message,
            "value": value,
            "level": level,
            "created_at": datetime.now().isoformat()
        }
        
        self.data["alerts"].append(alert)
        self._save_data()
        
        logger.warning(f"🚨 告警 [{level}]: {message} ({value}%)")
    
    def run_full_check(self) -> Dict:
        """执行完整检查"""
        logger.info("=" * 60)
        logger.info("🔍 太一贵客系统资源监控")
        logger.info("=" * 60)
        
        result = {
            "check_time": datetime.now().isoformat(),
            "cpu": self.check_cpu(),
            "memory": self.check_memory(),
            "disk": self.check_disk("/"),
            "processes": self.check_processes(),
            "overall_status": "normal"
        }
        
        # 计算整体状态
        statuses = [result["cpu"]["status"], result["memory"]["status"], result["disk"]["status"]]
        if "critical" in statuses:
            result["overall_status"] = "critical"
        elif "warning" in statuses:
            result["overall_status"] = "warning"
        
        # 保存历史数据
        self.data["history"].append(result)
        # 只保留最近 100 条记录
        if len(self.data["history"]) > 100:
            self.data["history"] = self.data["history"][-100:]
        
        self._save_data()
        
        logger.info(f"\n📊 系统整体状态：{result['overall_status']}")
        logger.info("=" * 60)
        
        return result
    
    def generate_report(self) -> Dict:
        """生成监控报告"""
        if not self.data["history"]:
            return {"status": "no_data"}
        
        latest = self.data["history"][-1]
        
        report = {
            "id": f"MONITOR_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "check_time": latest["check_time"],
            "overall_status": latest["overall_status"],
            "summary": {
                "cpu": f"{latest['cpu']['value']}% [{latest['cpu']['status']}]",
                "memory": f"{latest['memory']['value']}% [{latest['memory']['status']}]",
                "disk": f"{latest['disk']['value']}% [{latest['disk']['status']}]"
            },
            "alerts_count": len(self.data["alerts"]),
            "history_count": len(self.data["history"]),
            "generated_at": datetime.now().isoformat()
        }
        
        logger.info(f"📊 监控报告已生成：整体状态 {report['overall_status']}")
        return report
    
    def _save_data(self):
        with open(self.monitor_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def get_summary(self) -> Dict:
        """获取监控摘要"""
        if not self.data["history"]:
            return {"status": "no_data"}
        
        latest = self.data["history"][-1]
        return {
            "overall_status": latest["overall_status"],
            "cpu": latest["cpu"]["value"],
            "memory": latest["memory"]["value"],
            "disk": latest["disk"]["value"],
            "alerts_count": len(self.data["alerts"]),
            "last_check": latest["check_time"]
        }


def main():
    logger.info("=" * 60)
    logger.info("🔍 太一贵客系统资源监控")
    logger.info("=" * 60)
    
    monitor = SystemMonitor()
    
    # 执行完整检查
    result = monitor.run_full_check()
    
    # 生成报告
    report = monitor.generate_report()
    
    # 获取摘要
    summary = monitor.get_summary()
    logger.info(f"\n📊 监控摘要:")
    logger.info(f"  整体状态：{summary.get('overall_status', 'N/A')}")
    logger.info(f"  CPU: {summary.get('cpu', 'N/A')}%")
    logger.info(f"  内存：{summary.get('memory', 'N/A')}%")
    logger.info(f"  磁盘：{summary.get('disk', 'N/A')}%")
    logger.info(f"  告警数：{summary.get('alerts_count', 0)}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 系统监控完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
