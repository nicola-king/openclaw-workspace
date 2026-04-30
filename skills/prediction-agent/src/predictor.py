#!/usr/bin/env python3
"""
Prediction Agent - 预测分析智能体 v1.0
太一 AGI · 2026-04-15

时间序列预测，提前预警滞后
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class PredictionAgent:
    """预测分析智能体"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.monitoring_dir = self.workspace_root / "monitoring"
        self.config_path = self.workspace_root / "skills" / "prediction-agent" / "config" / "prediction-config.json"
        self.history_path = self.monitoring_dir / "prediction-history.json"
        self.forecast_path = self.monitoring_dir / "forecast.json"
        
        # 配置
        self.config = {
            "forecast_days": 7,
            "warning_threshold": 0.8,
            "critical_threshold": 0.5,
            "smoothing_window": 7,
            "trend_window": 14,
        }
        
        # 加载配置
        self._load_config()
        
        # 历史数据
        self.history = []
        self._load_history()
    
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text(encoding="utf-8"))
                self.config.update(config_data)
            except:
                pass
    
    def _load_history(self):
        """加载历史数据"""
        if self.history_path.exists():
            try:
                self.history = json.loads(self.history_path.read_text(encoding="utf-8"))
            except:
                pass
    
    def _save_history(self):
        """保存历史数据"""
        self.history_path.parent.mkdir(exist_ok=True)
        self.history_path.write_text(json.dumps(self.history, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def add_observation(self, date: str, progress: float, standardized: int, total: int):
        """添加观测数据"""
        self.history.append({
            "date": date,
            "progress": progress,
            "standardized": standardized,
            "total": total,
            "timestamp": datetime.now().isoformat(),
        })
        # 保留最近 90 天
        self.history = self.history[-90:]
        self._save_history()
    
    def simple_moving_average(self, data: List[float], window: int = 7) -> float:
        """简单移动平均"""
        if len(data) < window:
            return sum(data) / max(len(data), 1)
        return sum(data[-window:]) / window
    
    def exponential_moving_average(self, data: List[float], alpha: float = 0.3) -> float:
        """指数移动平均"""
        if not data:
            return 0.0
        
        ema = data[0]
        for value in data[1:]:
            ema = alpha * value + (1 - alpha) * ema
        return ema
    
    def linear_trend(self, data: List[float]) -> float:
        """计算线性趋势 (斜率)"""
        n = len(data)
        if n < 2:
            return 0.0
        
        # 简单线性回归
        x_mean = (n - 1) / 2
        y_mean = sum(data) / n
        
        numerator = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def forecast(self, days: int = None) -> Dict:
        """生成预测"""
        if days is None:
            days = self.config["forecast_days"]
        
        # 提取进度数据
        progress_data = [obs["progress"] for obs in self.history[-self.config["trend_window"]:]]
        
        if not progress_data:
            return {
                "status": "error",
                "message": "历史数据不足",
            }
        
        # 计算趋势
        trend = self.linear_trend(progress_data)
        current = progress_data[-1]
        
        # 生成预测
        forecast_values = []
        for d in range(1, days + 1):
            predicted = current + trend * d
            forecast_values.append({
                "day": d,
                "date": (datetime.now() + timedelta(days=d)).strftime("%Y-%m-%d"),
                "predicted": max(0.0, min(predicted, 2.0)),  # 限制在 0-200%
            })
        
        # 移动平均平滑
        sma = self.simple_moving_average(progress_data, self.config["smoothing_window"])
        ema = self.exponential_moving_average(progress_data)
        
        # 预警分析
        target = 0.2  # 短期目标 20%
        warnings = []
        
        for pred in forecast_values:
            if pred["predicted"] < target * self.config["critical_threshold"]:
                warnings.append({
                    "level": "critical",
                    "day": pred["day"],
                    "message": f"第{pred['day']}天预计严重滞后 ({pred['predicted']:.1%})",
                })
            elif pred["predicted"] < target * self.config["warning_threshold"]:
                warnings.append({
                    "level": "warning",
                    "day": pred["day"],
                    "message": f"第{pred['day']}天预计滞后 ({pred['predicted']:.1%})",
                })
        
        # 保存预测
        forecast_result = {
            "generated_at": datetime.now().isoformat(),
            "current": current,
            "trend": trend,
            "sma": sma,
            "ema": ema,
            "forecast": forecast_values,
            "warnings": warnings,
            "target": target,
        }
        
        self.forecast_path.parent.mkdir(exist_ok=True)
        self.forecast_path.write_text(json.dumps(forecast_result, indent=2, ensure_ascii=False), encoding="utf-8")
        
        return forecast_result
    
    def show_alerts(self):
        """显示预警"""
        forecast_result = self.forecast()
        
        print("\n" + "="*60)
        print("🚨 预测预警")
        print("="*60)
        
        warnings = forecast_result.get("warnings", [])
        
        if not warnings:
            print("✅ 无预警 - 预测正常")
        else:
            for warning in warnings:
                emoji = "🔴" if warning["level"] == "critical" else "🟡"
                print(f"{emoji} {warning['message']}")
        
        print(f"\n当前进度：{forecast_result.get('current', 0):.1%}")
        print(f"趋势：{'上升' if forecast_result.get('trend', 0) > 0 else '下降'}")
        print(f"{'='*60}")
        
        return warnings
    
    def evaluate_accuracy(self) -> Dict:
        """评估预测准确性"""
        # 简化版：使用最近预测与实际对比
        if not self.forecast_path.exists():
            return {"status": "no_forecast"}
        
        # TODO: 实现准确性评估
        return {
            "status": "ok",
            "accuracy": 0.85,  # 模拟值
            "message": "预测准确性评估功能开发中...",
        }
    
    def show_status(self):
        """显示状态"""
        print("\n" + "="*60)
        print("📊 Prediction Agent 状态")
        print("="*60)
        print(f"历史数据：{len(self.history)} 条")
        print(f"预测天数：{self.config['forecast_days']}")
        print(f"预警阈值：{self.config['warning_threshold']:.0%}")
        
        if self.history:
            latest = self.history[-1]
            print(f"最新数据：{latest['date']} - 进度 {latest['progress']:.1%}")
        
        print(f"{'='*60}")


def main():
    """主函数"""
    workspace_root = "/home/nicola/.openclaw/workspace"
    agent = PredictionAgent(workspace_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--status":
            agent.show_status()
        elif command == "--forecast":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            result = agent.forecast(days)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif command == "--alerts":
            agent.show_alerts()
        elif command == "--evaluate":
            result = agent.evaluate_accuracy()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"未知命令：{command}")
    else:
        agent.show_status()


if __name__ == "__main__":
    import sys
    main()
