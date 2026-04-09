#!/usr/bin/env python3
"""
错误处理与自愈系统 - 根因分析与自动修复

作者：太一 AGI
创建：2026-04-09
"""

import os
import sys
import time
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable, Any
from functools import wraps
from dataclasses import dataclass, asdict
import json

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
LOG_DIR = WORKSPACE / "logs"
LOG_DIR.mkdir(exist_ok=True)

ERROR_LOG = LOG_DIR / "error_analysis.jsonl"
METRICS_FILE = LOG_DIR / "error_metrics.json"


@dataclass
class ErrorRecord:
    """错误记录"""
    timestamp: str
    error_type: str
    error_message: str
    file_path: str
    function_name: str
    line_number: int
    stack_trace: str
    root_cause: str
    fix_applied: str
    recurrence_count: int


class ErrorAnalyzer:
    """错误分析器"""
    
    def __init__(self):
        self.error_history = self.load_error_history()
        self.metrics = self.load_metrics()
    
    def load_error_history(self) -> list:
        """加载错误历史"""
        if ERROR_LOG.exists():
            with open(ERROR_LOG, "r", encoding="utf-8") as f:
                return [json.loads(line) for line in f]
        return []
    
    def load_metrics(self) -> dict:
        """加载指标"""
        if METRICS_FILE.exists():
            with open(METRICS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "total_errors": 0,
            "by_type": {},
            "by_root_cause": {},
            "recurrence_rate": 0.0
        }
    
    def record_error(self, error: Exception, func_name: str, file_path: str):
        """记录错误"""
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno if exc_tb else 0
        
        # 分析根因
        root_cause = self.analyze_root_cause(error)
        
        # 检查是否重复
        recurrence = self.check_recurrence(error_type=type(error).__name__, root_cause=root_cause)
        
        # 创建记录
        record = ErrorRecord(
            timestamp=datetime.now().isoformat(),
            error_type=type(error).__name__,
            error_message=str(error),
            file_path=file_path,
            function_name=func_name,
            line_number=line_number,
            stack_trace=traceback.format_exc(),
            root_cause=root_cause,
            fix_applied=self.suggest_fix(root_cause),
            recurrence_count=recurrence
        )
        
        # 保存
        self.error_history.append(asdict(record))
        self.save_error_history()
        
        # 更新指标
        self.update_metrics(record)
        
        # 自动修复
        self.auto_fix(root_cause, file_path)
        
        return record
    
    def analyze_root_cause(self, error: Exception) -> str:
        """分析根因"""
        error_msg = str(error).lower()
        error_type = type(error).__name__
        
        # 文件/目录相关
        if "no such file" in error_msg or "not found" in error_msg:
            return "目录未创建"
        if "permission denied" in error_msg:
            return "权限不足"
        
        # Git 相关
        if "lock" in error_msg or "index.lock" in error_msg:
            return "Git 锁冲突"
        
        # 网络/端口相关
        if "address already in use" in error_msg or "bind" in error_msg:
            return "端口占用"
        
        # 变量/命名相关
        if "not defined" in error_msg or "cannot access" in error_msg:
            return "变量名错误"
        
        # 路径相关
        if "relative path" in error_msg or "absolute path" in error_msg:
            return "路径错误"
        
        # 默认
        return f"{error_type}: {error_msg[:50]}"
    
    def check_recurrence(self, error_type: str, root_cause: str) -> int:
        """检查重复次数"""
        count = 0
        for record in self.error_history[-100:]:  # 最近 100 条
            if (record["error_type"] == error_type and 
                record["root_cause"] == root_cause):
                count += 1
        return count
    
    def suggest_fix(self, root_cause: str) -> str:
        """建议修复方案"""
        fixes = {
            "目录未创建": "创建目录后再写文件：Path.mkdir(parents=True, exist_ok=True)",
            "权限不足": "检查文件权限：chmod +x 或使用 sudo",
            "Git 锁冲突": "删除锁文件：rm .git/index.lock 或 git gc",
            "端口占用": "清理旧进程：lsof -i :PORT | xargs kill -9",
            "变量名错误": "统一命名规范：检查大小写一致性",
            "路径错误": "统一使用绝对路径：Path(__file__).parent"
        }
        return fixes.get(root_cause, "需要人工分析")
    
    def auto_fix(self, root_cause: str, file_path: str):
        """自动修复"""
        if root_cause == "目录未创建":
            # 确保目录存在
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        elif root_cause == "Git 锁冲突":
            # 清理 Git 锁
            git_lock = WORKSPACE / ".git" / "index.lock"
            if git_lock.exists():
                git_lock.unlink()
        
        elif root_cause == "端口占用":
            # 清理端口 (简化实现)
            pass
    
    def update_metrics(self, record: ErrorRecord):
        """更新指标"""
        self.metrics["total_errors"] += 1
        
        # 按类型统计
        error_type = record.error_type
        self.metrics["by_type"][error_type] = self.metrics["by_type"].get(error_type, 0) + 1
        
        # 按根因统计
        root_cause = record.root_cause
        self.metrics["by_root_cause"][root_cause] = self.metrics["by_root_cause"].get(root_cause, 0) + 1
        
        # 计算重复率
        if record.recurrence_count > 0:
            total = sum(self.metrics["by_root_cause"].values())
            recurring = sum(1 for r in self.error_history if r["recurrence_count"] > 0)
            self.metrics["recurrence_rate"] = recurring / total if total > 0 else 0
        
        self.save_metrics()
    
    def save_error_history(self):
        """保存错误历史"""
        with open(ERROR_LOG, "w", encoding="utf-8") as f:
            for record in self.error_history:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    def save_metrics(self):
        """保存指标"""
        with open(METRICS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
    
    def get_top_root_causes(self, limit: int = 5) -> list:
        """获取主要根因"""
        sorted_causes = sorted(
            self.metrics["by_root_cause"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_causes[:limit]
    
    def generate_report(self) -> str:
        """生成错误分析报告"""
        report = f"""# 错误分析报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 总体指标

- 总错误数：{self.metrics['total_errors']}
- 重复率：{self.metrics['recurrence_rate']:.1%}

## 主要根因 (Top 5)

"""
        for i, (cause, count) in enumerate(self.get_top_root_causes(), 1):
            report += f"{i}. **{cause}**: {count} 次\n"
        
        report += "\n## 建议修复措施\n\n"
        for cause, count in self.get_top_root_causes():
            fix = self.suggest_fix(cause)
            report += f"- **{cause}** ({count}次): {fix}\n"
        
        return report


def error_handler(func: Callable) -> Callable:
    """错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        analyzer = ErrorAnalyzer()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            record = analyzer.record_error(
                error=e,
                func_name=func.__name__,
                file_path=str(Path(inspect.getfile(func)).absolute())
            )
            
            # 记录日志
            logging.error(f"错误：{record.error_type} - {record.root_cause}")
            
            # 重试逻辑 (如果是可恢复错误)
            if record.recurrence_count < 3:
                logging.info(f"尝试重试 (第{record.recurrence_count + 1}次)...")
                time.sleep(1)
                try:
                    return func(*args, **kwargs)
                except Exception as retry_error:
                    logging.error(f"重试失败：{retry_error}")
            
            # 抛出异常
            raise
    return wrapper


# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "error_handler.log"),
        logging.StreamHandler()
    ]
)


def main():
    """测试"""
    analyzer = ErrorAnalyzer()
    
    print("🔍 错误分析器测试")
    print()
    
    # 显示报告
    print(analyzer.generate_report())
    
    print()
    print("错误日志位置:", ERROR_LOG)
    print("指标文件位置:", METRICS_FILE)


if __name__ == "__main__":
    import inspect
    main()
