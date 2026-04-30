#!/usr/bin/env python3
"""
元认知模块 v0.1
分析思考过程，优化学习方法，进化进化策略

用法：
    python3 metacognition.py --analyze --session SESSION_ID
    python3 metacognition.py --improve-learning
    python3 metacognition.py --evolve-evolution
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import requests

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SESSIONS_DIR = WORKSPACE / "agents" / "taiyi" / "sessions"
MEMORY_DIR = WORKSPACE / "memory"
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"


class MetacognitionModule:
    def __init__(self):
        self.thinking_patterns = []
        self.learning_history = []
        self.evolution_history = []
    
    def analyze_thinking_process(self, session_id=None):
        """分析思考过程"""
        print("=" * 60)
        print("元认知模块 - 思考过程分析")
        print("=" * 60)
        
        # 加载会话日志
        sessions = self.load_recent_sessions(10 if not session_id else 1)
        
        if not sessions:
            print("❌ 无会话数据")
            return None
        
        # 分析思考模式
        patterns = self.identify_thinking_patterns(sessions)
        
        # 识别思维偏见
        biases = self.identify_cognitive_biases(sessions)
        
        # 生成改进建议
        suggestions = self.generate_improvement_suggestions(patterns, biases)
        
        # 输出报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'sessions_analyzed': len(sessions),
            'thinking_patterns': patterns,
            'cognitive_biases': biases,
            'suggestions': suggestions
        }
        
        self.save_analysis_report(report)
        self.print_report(report)
        
        return report
    
    def load_recent_sessions(self, count=10):
        """加载最近会话"""
        if not SESSIONS_DIR.exists():
            return []
        
        session_files = sorted(
            SESSIONS_DIR.glob("*.jsonl"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )[:count]
        
        sessions = []
        for session_file in session_files:
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = [json.loads(line) for line in f if line.strip()]
                sessions.append({
                    'id': session_file.stem,
                    'data': session_data,
                    'timestamp': datetime.fromtimestamp(session_file.stat().st_mtime)
                })
            except Exception as e:
                print(f"⚠️ 加载会话失败：{session_file.name} - {e}")
        
        return sessions
    
    def identify_thinking_patterns(self, sessions):
        """识别思考模式"""
        patterns = {
            'decision_making': [],      # 决策模式
            'problem_solving': [],       # 问题解决模式
            'information_gathering': [], # 信息收集模式
            'verification': []           # 验证模式
        }
        
        for session in sessions:
            messages = session['data']
            
            # 分析决策模式
            tool_calls = [m for m in messages if m.get('type') == 'toolCall']
            if tool_calls:
                patterns['decision_making'].append({
                    'session': session['id'],
                    'tool_count': len(tool_calls),
                    'tools_used': list(set([t['name'] for t in tool_calls]))
                })
            
            # 分析信息收集模式
            read_ops = [m for m in messages if m.get('name') == 'read']
            if read_ops:
                patterns['information_gathering'].append({
                    'session': session['id'],
                    'reads': len(read_ops)
                })
        
        # 总结模式
        summary = {}
        for pattern_type, instances in patterns.items():
            if instances:
                summary[pattern_type] = {
                    'frequency': len(instances),
                    'avg_count': sum([i.get('tool_count', i.get('reads', 0)) for i in instances]) / len(instances),
                    'trend': 'stable'  # 简化，实际应该分析趋势
                }
        
        return summary
    
    def identify_cognitive_biases(self, sessions):
        """识别思维偏见"""
        biases = []
        
        # 检查确认偏见（只找支持自己观点的信息）
        # 检查锚定偏见（过度依赖首次信息）
        # 检查可用性偏见（过度依赖容易获取的信息）
        
        # 简化实现：检查是否经常重复同样的错误
        error_patterns = self.detect_repeated_errors(sessions)
        if error_patterns:
            biases.append({
                'type': 'repeated_error',
                'description': '检测到重复错误模式',
                'instances': error_patterns,
                'severity': 'medium'
            })
        
        return biases
    
    def detect_repeated_errors(self, sessions):
        """检测重复错误"""
        errors = []
        error_counts = {}
        
        for session in sessions:
            messages = session['data']
            tool_results = [m for m in messages if m.get('type') == 'toolResult' and m.get('isError')]
            
            for result in tool_results:
                error_msg = str(result.get('content', ''))[:100]
                error_counts[error_msg] = error_counts.get(error_msg, 0) + 1
        
        # 找出重复出现的错误
        for error, count in error_counts.items():
            if count >= 2:
                errors.append({'error': error, 'count': count})
        
        return errors
    
    def generate_improvement_suggestions(self, patterns, biases):
        """生成改进建议"""
        suggestions = []
        
        # 基于思考模式
        if patterns.get('information_gathering', {}).get('avg_count', 0) > 10:
            suggestions.append({
                'area': '信息收集',
                'issue': '单次会话读取文件过多',
                'suggestion': '考虑实现批量读取或缓存策略',
                'priority': 'medium'
            })
        
        # 基于思维偏见
        for bias in biases:
            if bias['type'] == 'repeated_error':
                suggestions.append({
                    'area': '错误预防',
                    'issue': '检测到重复错误',
                    'suggestion': '创建错误检查清单或自动化测试',
                    'priority': 'high'
                })
        
        return suggestions
    
    def improve_learning_method(self):
        """改进学习方法"""
        print("=" * 60)
        print("元认知模块 - 学习方法优化")
        print("=" * 60)
        
        # 分析历史学习效果
        learning_history = self.load_learning_history()
        
        if not learning_history:
            print("📊 无足够学习历史数据")
            return None
        
        # 识别高效学习模式
        effective_patterns = self.identify_effective_learning_patterns(learning_history)
        
        # 生成优化建议
        recommendations = self.generate_learning_recommendations(effective_patterns)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'history_analyzed': len(learning_history),
            'effective_patterns': effective_patterns,
            'recommendations': recommendations
        }
        
        self.save_learning_report(report)
        self.print_report(report)
        
        return report
    
    def load_learning_history(self):
        """加载学习历史"""
        # 从记忆文件中提取学习相关记录
        history = []
        
        for md_file in MEMORY_DIR.glob("*.md"):
            if md_file.name.startswith("2026-"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 简单提取学习相关内容
                    if '学习' in content or 'learn' in content.lower():
                        history.append({
                            'date': md_file.stem,
                            'content': content[:500]  # 简化
                        })
                except Exception as e:
                    pass
        
        return history
    
    def identify_effective_learning_patterns(self, history):
        """识别高效学习模式"""
        # 简化实现
        return {
            'pattern': '从实践中学习',
            'effectiveness': 0.8,
            'frequency': len(history)
        }
    
    def generate_learning_recommendations(self, patterns):
        """生成学习建议"""
        return [
            {
                'recommendation': '增加反思环节',
                'rationale': '从经验中学习后，花 5 分钟反思可以加深理解',
                'implementation': '在每日 23:00 自我评估中添加反思问题'
            },
            {
                'recommendation': '建立知识关联',
                'rationale': '将新知识与已有知识关联可以提高记忆保持率',
                'implementation': '在 Obsidian 中使用双链关联新概念'
            }
        ]
    
    def evolve_evolution_strategy(self):
        """进化进化策略"""
        print("=" * 60)
        print("元认知模块 - 进化策略优化")
        print("=" * 60)
        
        # 分析历史进化效果
        evolution_history = self.load_evolution_history()
        
        if not evolution_history:
            print("📊 无足够进化历史数据")
            return None
        
        # 识别成功的进化模式
        successful_patterns = self.identify_successful_evolution_patterns(evolution_history)
        
        # 提出进化策略优化
        optimizations = self.propose_evolution_optimizations(successful_patterns)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'history_analyzed': len(evolution_history),
            'successful_patterns': successful_patterns,
            'optimizations': optimizations
        }
        
        self.save_evolution_report(report)
        self.print_report(report)
        
        return report
    
    def load_evolution_history(self):
        """加载进化历史"""
        history = []
        
        # 从实验记录中提取
        exp_dir = MEMORY_DIR / "experiments"
        if exp_dir.exists():
            for exp_file in exp_dir.glob("*.md"):
                try:
                    with open(exp_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    history.append({
                        'id': exp_file.stem,
                        'content': content
                    })
                except:
                    pass
        
        return history
    
    def identify_successful_evolution_patterns(self, history):
        """识别成功的进化模式"""
        # 简化实现
        return {
            'pattern': '小步快跑',
            'success_rate': 0.75,
            'characteristics': ['小变更', '快速验证', '自动回滚']
        }
    
    def propose_evolution_optimizations(self, patterns):
        """提出进化策略优化"""
        return [
            {
                'optimization': '增加 A/B 测试样本量',
                'rationale': '更大样本量可以提高统计显著性',
                'expected_improvement': '+10% 实验可靠性'
            },
            {
                'optimization': '缩短实验周期',
                'rationale': '更快验证可以加速进化循环',
                'expected_improvement': '+20% 进化速度'
            }
        ]
    
    def save_analysis_report(self, report):
        """保存分析报告"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        report_file = DATA_DIR / f"metacognition-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 报告已保存：{report_file}")
    
    def save_learning_report(self, report):
        """保存学习报告"""
        self.save_analysis_report(report)  # 简化
    
    def save_evolution_report(self, report):
        """保存进化报告"""
        self.save_analysis_report(report)  # 简化
    
    def print_report(self, report):
        """打印报告"""
        print("\n" + "=" * 60)
        print("分析报告")
        print("=" * 60)
        
        for key, value in report.items():
            if key != 'timestamp':
                print(f"\n{key}:")
                print(f"  {value}")
        
        print("\n" + "=" * 60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="元认知模块")
    parser.add_argument("--analyze", action="store_true", help="分析思考过程")
    parser.add_argument("--session", help="会话 ID")
    parser.add_argument("--improve-learning", action="store_true", help="优化学习方法")
    parser.add_argument("--evolve-evolution", action="store_true", help="进化进化策略")
    
    args = parser.parse_args()
    
    module = MetacognitionModule()
    
    if args.analyze:
        module.analyze_thinking_process(args.session)
    
    elif args.improve_learning:
        module.improve_learning_method()
    
    elif args.evolve_evolution:
        module.evolve_evolution_strategy()
    
    else:
        print("元认知模块 v0.1")
        print("用法：")
        print("  --analyze              分析思考过程")
        print("  --improve-learning     优化学习方法")
        print("  --evolve-evolution     进化进化策略")


if __name__ == "__main__":
    main()
