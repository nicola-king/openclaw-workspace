#!/usr/bin/env python3
"""
太一系统自进化触发器 - 智能涌现创建新 Skill/Agent

功能:
1. 检测能力涌现信号
2. 分析是否需要新 Skill/Agent
3. 自动创建 Skill/Agent 框架
4. 生成能力涌现报告

运行时间：每 15 分钟自动检查 + 事件触发

作者：太一 AGI
创建：2026-04-10
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
LOGS_DIR = WORKSPACE / "logs"
REPORTS_DIR = WORKSPACE / "reports"
SKILLS_DIR = WORKSPACE / "skills"
AGENTS_DIR = WORKSPACE / "agents"

# 确保目录存在
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


class SelfEvolutionTrigger:
    """太一系统自进化触发器"""
    
    def __init__(self):
        self.triggers = []
        self.created_skills = []
        self.created_agents = []
        self.start_time = datetime.now()
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.triggers.append(log_entry)
        print(log_entry)
    
    def check_emergence_signals(self):
        """检测能力涌现信号"""
        self.log("🔍 检测能力涌现信号...")
        
        signals = []
        
        # 信号 1: 同类任务重复出现 ≥3 次
        self.log("  📊 检查任务重复模式...")
        task_patterns = self.analyze_task_patterns()
        if task_patterns['repeated'] >= 3:
            signals.append({
                'type': 'repeated_task',
                'pattern': task_patterns['pattern'],
                'count': task_patterns['repeated'],
                'trigger': '同类任务重复出现≥3 次'
            })
            self.log(f"  ✅ 发现重复任务模式：{task_patterns['pattern']} ({task_patterns['repeated']}次)")
        
        # 信号 2: 职责域超出已有 Bot 能力
        self.log("  📊 检查职责域边界...")
        domain_gaps = self.analyze_domain_gaps()
        if domain_gaps['gaps']:
            signals.append({
                'type': 'domain_gap',
                'gaps': domain_gaps['gaps'],
                'trigger': '新职责域超出已有 Bot 能力'
            })
            self.log(f"  ✅ 发现职责域空白：{domain_gaps['gaps']}")
        
        # 信号 3: 用户明确请求创建
        self.log("  📊 检查用户请求...")
        user_requests = self.check_user_requests()
        if user_requests['requests']:
            signals.append({
                'type': 'user_request',
                'requests': user_requests['requests'],
                'trigger': '用户明确请求创建'
            })
            self.log(f"  ✅ 发现用户请求：{user_requests['requests']}")
        
        # 信号 4: 学习循环产生新洞察
        self.log("  📊 检查学习洞察...")
        insights = self.check_learning_insights()
        if insights['insights']:
            signals.append({
                'type': 'learning_insight',
                'insights': insights['insights'],
                'trigger': '学习循环产生新洞察'
            })
        
        # 信号 5: 造价 Agent 自进化检测
        self.log("  📊 检查造价 Agent 自进化...")
        cost_agent_signal = self.check_cost_agent_evolution()
        if cost_agent_signal:
            signals.append(cost_agent_signal)
            self.log(f"  ✅ 发现造价 Agent 自进化信号")
            self.log(f"  ✅ 发现学习洞察：{insights['insights']}")
        
        self.log(f"✅ 能力涌现信号检测完成，发现 {len(signals)} 个信号")
        return signals
    
    def analyze_task_patterns(self):
        """分析任务模式"""
        # 简化实现：检查 HEARTBEAT.md 中的任务
        heartbeat_file = WORKSPACE / "HEARTBEAT.md"
        
        if not heartbeat_file.exists():
            return {'repeated': 0, 'pattern': None}
        
        with open(heartbeat_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检测重复任务关键词
        task_keywords = ['Dashboard', '美学', '诗词', '书画', '学习', '研究']
        repeated_count = 0
        repeated_pattern = None
        
        for keyword in task_keywords:
            count = content.count(keyword)
            if count >= 3:
                repeated_count = count
                repeated_pattern = keyword
                break
        
        return {
            'repeated': repeated_count,
            'pattern': repeated_pattern
        }
    
    def analyze_domain_gaps(self):
        """分析职责域空白"""
        # 简化实现：检查 Skills 目录结构
        existing_domains = set()
        
        for skill_dir in SKILLS_DIR.iterdir():
            if skill_dir.is_dir():
                # 提取领域关键词
                domain = skill_dir.name.split('-')[0]
                existing_domains.add(domain)
        
        # 检测潜在新领域
        potential_gaps = []
        
        # 检查最近学习的内容是否已有对应 Skill
        recent_topics = ['色彩', '纹样', '园林', '建筑', '诗词', '书法', '国画']
        for topic in recent_topics:
            if topic not in existing_domains:
                potential_gaps.append(topic)
        
        return {
            'gaps': potential_gaps[:3]  # 最多返回 3 个
        }
    
    def check_user_requests(self):
        """检查用户请求"""
        # 简化实现：检查最近会话记录
        requests = []
        
        # 实际应该分析对话历史
        # 这里简化处理
        
        return {
            'requests': requests
        }
    
    def check_learning_insights(self):
        """检查学习洞察"""
        insights = []
        
        # 检查凌晨学习报告
        learning_reports = list(REPORTS_DIR.glob("midnight-learning-*.json"))
        
        if learning_reports:
            latest_report = max(learning_reports)
            with open(latest_report, "r", encoding="utf-8") as f:
                report = json.load(f)
            
            innovations = report.get('innovations', [])
            if len(innovations) >= 3:
                insights.append(f"融合创新产出 {len(innovations)} 个")
        
        return {
            'insights': insights
        }
    

    def check_cost_agent_evolution(self):
        """检查造价 Agent 自进化"""
        # 检查造价 Agent 目录
        cost_agent_dir = SKILLS_DIR / '08-emerged' / 'cost-agent'
        
        if not cost_agent_dir.exists():
            return None
        
        # 检查自进化脚本
        evolution_script = cost_agent_dir / 'self_evolution_cost_agent.py'
        if not evolution_script.exists():
            return None
        
        # 检查最近的自进化报告
        reports_dir = cost_agent_dir / 'reports'
        if reports_dir.exists():
            reports = list(reports_dir.glob('cost-agent-evolution-*.json'))
            if reports:
                latest_report = max(reports)
                mtime = datetime.fromtimestamp(latest_report.stat().st_mtime)
                age = datetime.now() - mtime
                
                # 如果 1 小时内有自进化报告，返回信号
                if age.seconds < 3600:
                    return {
                        'type': 'cost_agent_evolution',
                        'agent': 'cost-agent',
                        'trigger': '造价 Agent 自进化检测',
                        'last_evolution': mtime.isoformat(),
                    }
        
        return None

    def run_cost_agent_evolution(self):
        """运行造价 Agent 自进化"""
        cost_agent_dir = SKILLS_DIR / '08-emerged' / 'cost-agent'
        evolution_script = cost_agent_dir / 'self_evolution_cost_agent.py'
        
        if evolution_script.exists():
            try:
                result = subprocess.run(
                    ['python3', str(evolution_script)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    self.log("  ✅ 造价 Agent 自进化成功")
                else:
                    self.log(f"  ⚠️ 造价 Agent 自进化失败：{result.stderr}")
            except Exception as e:
                self.log(f"  ⚠️ 造价 Agent 自进化错误：{e}")

    def decide_creation(self, signals):
        """决策是否创建新 Skill/Agent"""
        if not signals:
            return None
        
        # 决策逻辑
        if any(s['type'] == 'repeated_task' for s in signals):
            return {
                'type': 'skill',
                'reason': '同类任务重复出现',
                'priority': 'P0'
            }
        
        if any(s['type'] == 'domain_gap' for s in signals):
            return {
                'type': 'skill',
                'reason': '新职责域空白',
                'priority': 'P1'
            }
        
        if any(s['type'] == 'learning_insight' for s in signals):
            return {
                'type': 'skill',
                'reason': '学习洞察涌现',
                'priority': 'P2'
            }
        
        return None
    
    def create_skill_framework(self, decision):
        """创建 Skill 框架"""
        self.log("🎨 开始创建 Skill 框架...")
        
        # 生成 Skill 名称
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        skill_name = f"emerged-skill-{timestamp}"
        skill_dir = SKILLS_DIR / skill_name
        
        # 创建目录结构
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "config").mkdir(exist_ok=True)
        (skill_dir / "tests").mkdir(exist_ok=True)
        
        # 创建 SKILL.md 框架
        skill_md = skill_dir / "SKILL.md"
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(f"""---
name: {skill_name}
version: 1.0.0
description: 能力涌现自动创建 - {decision['reason']}
category: emerged
tags: ['emerged', 'self-evolution', 'auto-created']
author: 太一 AGI (自进化系统)
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
status: active
priority: {decision['priority']}
---

# 🆕 Emerged Skill - {skill_name}

> **版本**: 1.0.0 | **创建**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **触发**: 能力涌现自动创建  
> **原因**: {decision['reason']}

---

## 🎯 职责

TODO: 定义技能职责

---

## 🚀 使用方式

```python
# TODO: 使用示例
```

---

## 📋 变更日志

### v1.0.0 ({datetime.now().strftime('%Y-%m-%d')})
- ✅ 能力涌现自动创建
- 🟡 职责定义 (待完善)
- 🟡 功能实现 (待开发)

---

*创建：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 太一 AGI · 自进化系统*
""")
        
        self.created_skills.append({
            'name': skill_name,
            'path': str(skill_dir),
            'reason': decision['reason']
        })
        
        self.log(f"✅ Skill 框架已创建：{skill_name}")
        return skill_dir
    
    def generate_report(self):
        """生成能力涌现报告"""
        report = {
            "session_start": self.start_time.isoformat(),
            "session_end": datetime.now().isoformat(),
            "duration_minutes": (datetime.now() - self.start_time).total_seconds() / 60,
            "signals_detected": len(self.triggers),
            "skills_created": len(self.created_skills),
            "agents_created": len(self.created_agents),
            "triggers": self.triggers,
            "created_skills": self.created_skills,
            "created_agents": self.created_agents
        }
        
        # 保存报告
        report_file = REPORTS_DIR / f"self-evolution-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 能力涌现报告已保存：{report_file}")
        return report, report_file
    
    def run_full_check(self):
        """运行完整检查"""
        self.log("🧬 太一系统自进化触发器启动")
        self.log("="*50)
        
        # 检测能力涌现信号
        signals = self.check_emergence_signals()
        self.log("")
        
        # 决策是否创建
        decision = self.decide_creation(signals)
        if decision:
            self.log(f"🎯 决策结果：创建 {decision['type']} (优先级：{decision['priority']})")
            self.log(f"   原因：{decision['reason']}")
            self.log("")
            
            # 创建 Skill/Agent
            if decision['type'] == 'skill':
                self.create_skill_framework(decision)
        else:
            self.log("ℹ️  无需创建新 Skill/Agent")
            self.log("   系统将继续观察和学习")
            self.log("")
        
        # 生成报告
        report, report_file = self.generate_report()
        self.log("")
        
        # 生成小时汇总报告
        hourly_summary = self.generate_hourly_summary()
        self.log("")
        
        # 发送 Telegram 通知
        self.send_telegram_notification(report, hourly_summary)
        self.log("")
        
        # 总结
        self.log("📊 自进化检查总结:")
        self.log(f"   开始时间：{self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"   结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"   持续时间：{report['duration_minutes']:.1f} 分钟")
        self.log(f"   信号检测：{len(signals)} 个")
        self.log(f"   新创建：{len(self.created_skills)} 个 Skill, {len(self.created_agents)} 个 Agent")
        self.log("")
        self.log("✅ 太一系统自进化检查完成")
        
        return report
    
    def generate_hourly_summary(self):
        """生成小时汇总报告"""
        self.log("📊 生成小时汇总报告...")
        
        # 收集过去 1 小时的报告
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        
        reports = []
        reports_dir = REPORTS_DIR
        
        for report_file in reports_dir.glob('self-evolution-*.json'):
            try:
                mtime = datetime.fromtimestamp(report_file.stat().st_mtime)
                if one_hour_ago <= mtime <= now:
                    with open(report_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        reports.append(data)
            except Exception as e:
                self.log(f"  ⚠️ 读取失败：{report_file} - {e}")
        
        # 生成汇总
        summary = {
            'timestamp': now.isoformat(),
            'period_start': one_hour_ago.isoformat(),
            'period_end': now.isoformat(),
            'total_executions': len(reports),
            'total_skills_created': sum(r.get('skills_created', 0) for r in reports),
            'total_signals': sum(r.get('signals_detected', 0) for r in reports),
        }
        
        # 保存汇总报告
        timestamp = now.strftime('%Y%m%d-%H0000')
        summary_file = reports_dir / f'hourly-summary-{timestamp}.json'
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        self.log(f"  ✅ 汇总报告已保存：{summary_file}")
        self.log(f"  总执行：{summary['total_executions']} 次")
        self.log(f"  总技能创建：{summary['total_skills_created']} 个")
        self.log(f"  总信号检测：{summary['total_signals']} 个")
        
        return summary
    
    def send_telegram_notification(self, report, hourly_summary):
        """发送 Telegram 通知"""
        self.log("📱 准备发送 Telegram 通知...")
        
        message = f"""📊 太一自进化小时报告

时间：{hourly_summary['period_start'][:16]} - {hourly_summary['period_end'][:16]}

执行统计:
- 执行次数：{hourly_summary['total_executions']} 次
- 技能创建：{hourly_summary['total_skills_created']} 个
- 信号检测：{hourly_summary['total_signals']} 个

状态：✅ 正常
"""
        
        # 保存到发送日志
        log_file = LOGS_DIR / 'telegram-send.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now()}] {message}\n")
        
        self.log(f"📱 Telegram 消息已记录到日志")
        
        # 实际发送到 Telegram (使用专用的小时报告发送脚本)
        self.log(f"📱 发送 Telegram 消息...")
        try:
            import subprocess
            script_path = WORKSPACE / 'scripts' / 'send-hourly-report.py'
            if script_path.exists():
                result = subprocess.run(
                    ['python3', str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    self.log(f"  ✅ Telegram 发送成功")
                else:
                    self.log(f"  ⚠️ Telegram 发送失败：{result.stderr[:100]}")
            else:
                self.log(f"  ⚠️ 发送脚本不存在：{script_path}")
        except Exception as e:
            self.log(f"  ⚠️ Telegram 发送错误：{str(e)[:100]}")


def main():
    """主函数"""
    system = SelfEvolutionTrigger()
    report = system.run_full_check()
    
    return 0 if report else 1


if __name__ == "__main__":
    sys.exit(main())

    def check_cost_agent_evolution(self):
        """检查造价 Agent 自进化"""
        # 检查造价 Agent 目录
        cost_agent_dir = SKILLS_DIR / '08-emerged' / 'cost-agent'
        
        if not cost_agent_dir.exists():
            return None
        
        # 检查自进化脚本
        evolution_script = cost_agent_dir / 'self_evolution_cost_agent.py'
        if not evolution_script.exists():
            return None
        
        # 检查最近的自进化报告
        reports_dir = cost_agent_dir / 'reports'
        if reports_dir.exists():
            reports = list(reports_dir.glob('cost-agent-evolution-*.json'))
            if reports:
                latest_report = max(reports)
                mtime = datetime.fromtimestamp(latest_report.stat().st_mtime)
                age = datetime.now() - mtime
                
                # 如果 1 小时内有自进化报告，返回信号
                if age.seconds < 3600:
                    return {
                        'type': 'cost_agent_evolution',
                        'agent': 'cost-agent',
                        'trigger': '造价 Agent 自进化检测',
                        'last_evolution': mtime.isoformat(),
                    }
        
        return None
    
    def run_cost_agent_evolution(self):
        """运行造价 Agent 自进化"""
        cost_agent_dir = SKILLS_DIR / '08-emerged' / 'cost-agent'
        evolution_script = cost_agent_dir / 'self_evolution_cost_agent.py'
        
        if evolution_script.exists():
            try:
                result = subprocess.run(
                    ['python3', str(evolution_script)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    self.log("  ✅ 造价 Agent 自进化成功")
                else:
                    self.log(f"  ⚠️ 造价 Agent 自进化失败：{result.stderr}")
            except Exception as e:
                self.log(f"  ⚠️ 造价 Agent 自进化错误：{e}")
