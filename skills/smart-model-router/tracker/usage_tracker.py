"""
模型用量追踪器
记录、分析、优化模型使用成本
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timedelta


class UsageTracker:
    """模型用量追踪器"""
    
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = Path.home() / '.openclaw' / 'workspace' / 'data'
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.usage_file = self.data_dir / 'model-usage-stats.json'
        self.daily_log_file = self.data_dir / 'model-usage-daily.json'
        
        self.stats = self._load_stats()
        self.daily_log = self._load_daily_log()
    
    def _load_stats(self) -> Dict[str, Any]:
        """加载总用量统计"""
        if self.usage_file.exists():
            with open(self.usage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_stats(self):
        """保存总用量统计"""
        with open(self.usage_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
    
    def _load_daily_log(self) -> Dict[str, Any]:
        """加载日用量日志"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if self.daily_log_file.exists():
            with open(self.daily_log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 只保留今天的日志
                if today in data:
                    return {today: data[today]}
        return {today: {}}
    
    def _save_daily_log(self):
        """保存日用量日志"""
        with open(self.daily_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.daily_log, f, indent=2, ensure_ascii=False)
    
    def record(self, model: str, tokens_in: int, tokens_out: int, 
               cost: float, duration_ms: int, task_type: str = 'general'):
        """
        记录一次模型调用
        
        Args:
            model: 模型名称
            tokens_in: 输入 tokens
            tokens_out: 输出 tokens
            cost: 成本 (元)
            duration_ms: 耗时 (毫秒)
            task_type: 任务类型
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 初始化模型统计
        if model not in self.stats:
            self.stats[model] = {
                'total_calls': 0,
                'total_tokens_in': 0,
                'total_tokens_out': 0,
                'total_cost': 0.0,
                'total_duration_ms': 0,
                'first_used': None,
                'last_used': None,
                'by_task_type': {}
            }
        
        # 更新总统计
        stats = self.stats[model]
        stats['total_calls'] += 1
        stats['total_tokens_in'] += tokens_in
        stats['total_tokens_out'] += tokens_out
        stats['total_cost'] += cost
        stats['total_duration_ms'] += duration_ms
        
        if stats['first_used'] is None:
            stats['first_used'] = datetime.now().isoformat()
        stats['last_used'] = datetime.now().isoformat()
        
        # 按任务类型统计
        if task_type not in stats['by_task_type']:
            stats['by_task_type'][task_type] = {
                'calls': 0,
                'cost': 0.0,
                'tokens': 0
            }
        stats['by_task_type'][task_type]['calls'] += 1
        stats['by_task_type'][task_type]['cost'] += cost
        stats['by_task_type'][task_type]['tokens'] += tokens_in + tokens_out
        
        # 更新衍生统计
        stats['avg_tokens_in'] = stats['total_tokens_in'] / stats['total_calls']
        stats['avg_tokens_out'] = stats['total_tokens_out'] / stats['total_calls']
        stats['avg_cost'] = stats['total_cost'] / stats['total_calls']
        stats['avg_duration_ms'] = stats['total_duration_ms'] / stats['total_calls']
        
        # 更新今日日志
        if today not in self.daily_log:
            self.daily_log[today] = {}
        
        if model not in self.daily_log[today]:
            self.daily_log[today][model] = {
                'calls': 0,
                'tokens_in': 0,
                'tokens_out': 0,
                'cost': 0.0,
                'duration_ms': 0
            }
        
        daily = self.daily_log[today][model]
        daily['calls'] += 1
        daily['tokens_in'] += tokens_in
        daily['tokens_out'] += tokens_out
        daily['cost'] += cost
        daily['duration_ms'] += duration_ms
        
        # 保存
        self._save_stats()
        self._save_daily_log()
    
    def get_stats(self, model: Optional[str] = None) -> Dict[str, Any]:
        """获取用量统计"""
        if model:
            return self.stats.get(model, {})
        return self.stats
    
    def get_daily_cost(self, date: Optional[str] = None) -> float:
        """获取指定日期的总成本"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        daily = self.daily_log.get(date, {})
        total_cost = sum(m.get('cost', 0.0) for m in daily.values())
        return round(total_cost, 2)
    
    def get_daily_summary(self, date: Optional[str] = None) -> Dict[str, Any]:
        """获取指定日期的用量摘要"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        daily = self.daily_log.get(date, {})
        
        total_calls = sum(m.get('calls', 0) for m in daily.values())
        total_cost = sum(m.get('cost', 0.0) for m in daily.values())
        total_tokens = sum(m.get('tokens_in', 0) + m.get('tokens_out', 0) for m in daily.values())
        
        return {
            'date': date,
            'total_calls': total_calls,
            'total_cost': round(total_cost, 2),
            'total_tokens': total_tokens,
            'models_used': list(daily.keys()),
            'breakdown': daily
        }
    
    def get_cost_trend(self, days: int = 7) -> List[Dict[str, Any]]:
        """获取成本趋势 (最近 N 天)"""
        trend = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            cost = self.get_daily_cost(date)
            calls = sum(m.get('calls', 0) for m in self.daily_log.get(date, {}).values())
            
            trend.append({
                'date': date,
                'cost': cost,
                'calls': calls
            })
        
        return trend
    
    def get_optimization_suggestions(self) -> List[str]:
        """获取优化建议"""
        suggestions = []
        
        # 分析总统计
        total_cost = sum(m.get('total_cost', 0.0) for m in self.stats.values())
        
        # 检查本地模型使用率
        local_calls = sum(
            m.get('total_calls', 0) 
            for m in self.stats.values() 
            if m.get('provider') == 'local' or 'local' in list(self.stats.keys())
        )
        total_calls = sum(m.get('total_calls', 0) for m in self.stats.values())
        
        if total_calls > 0:
            local_ratio = local_calls / total_calls
            if local_ratio < 0.5:
                suggestions.append(f"本地模型使用率仅 {local_ratio:.1%}，建议提高至 80% 以上以降低成本")
        
        # 检查高成本模型
        for model, stats in self.stats.items():
            if stats.get('total_cost', 0) > total_cost * 0.3:
                suggestions.append(f"模型 {model} 占总成本 {stats['total_cost']/total_cost:.1%}，考虑优化使用策略")
        
        # 检查每日预算
        today_cost = self.get_daily_cost()
        if today_cost > 50:
            suggestions.append(f"今日成本已达 {today_cost} 元，接近预算上限")
        
        return suggestions
