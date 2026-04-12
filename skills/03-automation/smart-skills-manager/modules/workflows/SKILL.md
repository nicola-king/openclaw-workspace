# Workflows Module - 工作流管理模块

> 版本：v1.0 | 创建：2026-04-03 22:17 | 负责 Bot：太一 / 守藏吏

---

## 🎯 职责

**工作流模板注册 + 执行追踪**，标准化任务执行流程

---

## 📋 工作流注册表

```python
# workflow-registry.py
from datetime import datetime

WORKFLOWS = {
    'content-creation': {
        'name': '内容创作工作流',
        'description': '从选题到发布的完整内容创作流程',
        'responsible_bot': '山木',
        'stages': [
            {'name': '选题', 'duration': '30m', 'output': '选题清单'},
            {'name': '大纲', 'duration': '30m', 'output': '文章大纲'},
            {'name': '草稿', 'duration': '1h', 'output': '初稿'},
            {'name': '审核', 'duration': '30m', 'output': '修改意见'},
            {'name': '发布', 'duration': '15m', 'output': '已发布'}
        ],
        'template': 'constitution/workflows/CONTENT-CREATION.md',
        'quality_gates': [
            '标题吸引力检查',
            '逻辑结构检查',
            '错别字检查',
            '格式规范检查'
        ]
    },
    
    'tech-development': {
        'name': '技术开发工作流',
        'description': '从需求到上线的完整开发流程',
        'responsible_bot': '素问',
        'stages': [
            {'name': '需求分析', 'duration': '1h', 'output': '需求文档'},
            {'name': '方案设计', 'duration': '2h', 'output': '技术方案'},
            {'name': '编码实现', 'duration': '4h', 'output': '功能代码'},
            {'name': '代码审查', 'duration': '1h', 'output': '审查意见'},
            {'name': '测试验证', 'duration': '2h', 'output': '测试报告'},
            {'name': '部署上线', 'duration': '30m', 'output': '已上线'}
        ],
        'template': 'constitution/workflows/TECH-DEVELOPMENT.md',
        'quality_gates': [
            '代码规范检查',
            '单元测试覆盖',
            '安全漏洞扫描',
            '性能基准测试'
        ]
    },
    
    'quant-trading': {
        'name': '量化交易工作流',
        'description': '从信号发现到交易执行的完整流程',
        'responsible_bot': '知几',
        'stages': [
            {'name': '信号发现', 'duration': '实时', 'output': '交易信号'},
            {'name': '策略验证', 'duration': '5m', 'output': '回测结果'},
            {'name': '风险评估', 'duration': '2m', 'output': '风险报告'},
            {'name': '执行确认', 'duration': '1m', 'output': '确认下单'},
            {'name': '交易执行', 'duration': '1m', 'output': '已成交'},
            {'name': '结果追踪', 'duration': '持续', 'output': '盈亏统计'}
        ],
        'template': 'constitution/workflows/QUANT-TRADING.md',
        'quality_gates': [
            '置信度>96%',
            '优势>2%',
            '风险<2%',
            '流动性>$100K'
        ]
    },
    
    'data-collection': {
        'name': '数据采集工作流',
        'description': '从数据源到入库的完整采集流程',
        'responsible_bot': '罔两',
        'stages': [
            {'name': '数据源确认', 'duration': '30m', 'output': '数据源清单'},
            {'name': '采集脚本', 'duration': '2h', 'output': '采集脚本'},
            {'name': '数据清洗', 'duration': '1h', 'output': '清洗后数据'},
            {'name': '数据入库', 'duration': '30m', 'output': '已入库'},
            {'name': '质量验证', 'duration': '30m', 'output': '验证报告'}
        ],
        'template': 'constitution/workflows/DATA-COLLECTION.md',
        'quality_gates': [
            '数据完整性>99%',
            '数据准确性>95%',
            '采集成功率>98%',
            '更新频率达标'
        ]
    },
    
    'learning-distillation': {
        'name': '学习蒸馏工作流',
        'description': '从信息输入到知识固化的完整流程',
        'responsible_bot': '太一',
        'stages': [
            {'name': '信息收集', 'duration': '1h', 'output': '原始素材'},
            {'name': '要点提炼', 'duration': '1h', 'output': '核心要点'},
            {'name': '知识关联', 'duration': '30m', 'output': '知识网络'},
            {'name': '文档固化', 'duration': '1h', 'output': '知识文档'},
            {'name': '归档索引', 'duration': '15m', 'output': '已归档'}
        ],
        'template': 'constitution/workflows/LEARNING-DISTILLATION.md',
        'quality_gates': [
            '信息完整性',
            '逻辑清晰度',
            '可操作性',
            '可检索性'
        ]
    }
}

def list_workflows():
    """列出所有工作流"""
    print("## 工作流注册表\n")
    print("| 工作流 | 负责 Bot | 阶段数 | 预计耗时 |")
    print("|--------|---------|--------|---------|")
    
    for wf_id, wf in WORKFLOWS.items():
        stages = len(wf['stages'])
        total_duration = sum_duration(wf['stages'])
        print(f"| {wf['name']} | {wf['responsible_bot']} | {stages} | {total_duration} |")

def sum_duration(stages):
    """计算总耗时"""
    total_minutes = 0
    for stage in stages:
        duration = stage['duration']
        if 'h' in duration:
            total_minutes += int(duration.replace('h', '')) * 60
        elif 'm' in duration:
            total_minutes += int(duration.replace('m', ''))
    # 忽略"实时"和"持续"
    return f"{total_minutes // 60}h{total_minutes % 60}m" if total_minutes > 0 else "可变"

if __name__ == '__main__':
    list_workflows()
```

---

## 📊 执行追踪

```python
# execution-tracker.py
import json
from datetime import datetime

class ExecutionTracker:
    def __init__(self):
        self.log_file = 'logs/workflow-executions.jsonl'
    
    def start_execution(self, workflow_id, bot, context):
        """开始执行工作流"""
        record = {
            'event': 'start',
            'timestamp': datetime.now().isoformat(),
            'workflow_id': workflow_id,
            'bot': bot,
            'context': context,
            'stages_completed': 0,
            'status': 'running'
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        return record
    
    def complete_stage(self, workflow_id, stage_name, output, duration_minutes):
        """完成阶段"""
        record = {
            'event': 'stage_complete',
            'timestamp': datetime.now().isoformat(),
            'workflow_id': workflow_id,
            'stage_name': stage_name,
            'output': output,
            'duration_minutes': duration_minutes
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def complete_execution(self, workflow_id, final_output, success=True):
        """完成执行"""
        record = {
            'event': 'complete',
            'timestamp': datetime.now().isoformat(),
            'workflow_id': workflow_id,
            'final_output': final_output,
            'success': success,
            'status': 'completed' if success else 'failed'
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def get_execution_history(self, workflow_id=None, limit=10):
        """获取执行历史"""
        executions = []
        
        with open(self.log_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if workflow_id and record['workflow_id'] != workflow_id:
                    continue
                if record['event'] == 'start':
                    executions.append(record)
        
        return executions[-limit:]
    
    def generate_report(self, workflow_id=None):
        """生成执行报告"""
        executions = self.get_execution_history(workflow_id)
        
        report = f"## 工作流执行报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        report += f"**统计范围**: {'所有工作流' if not workflow_id else workflow_id}\n\n"
        
        if not executions:
            report += "暂无执行记录\n"
            return report
        
        # 统计成功率
        success_count = sum(1 for e in executions if e.get('status') == 'completed')
        success_rate = success_count / len(executions) * 100 if executions else 0
        
        report += "### 执行统计\n\n"
        report += f"| 指标 | 值 |\n"
        report += f"|------|-----|\n"
        report += f"| 总执行次数 | {len(executions)} |\n"
        report += f"| 成功次数 | {success_count} |\n"
        report += f"| 成功率 | {success_rate:.1f}% |\n\n"
        
        report += "### 最近执行\n\n"
        report += "| 时间 | 工作流 | 负责 Bot | 状态 |\n"
        report += "|------|--------|---------|------|\n"
        
        for exec_record in executions[-10:]:
            time_str = exec_record['timestamp'][:16].replace('T', ' ')
            workflow = exec_record['workflow_id']
            bot = exec_record['bot']
            status = '✅' if exec_record.get('status') == 'completed' else '🟡'
            report += f"| {time_str} | {workflow} | {bot} | {status} |\n"
        
        return report

if __name__ == '__main__':
    tracker = ExecutionTracker()
    print(tracker.generate_report())
```

---

## 📋 使用命令

```bash
# 列出所有工作流
python3 modules/workflows/workflow-registry.py

# 查看执行历史
python3 modules/workflows/execution-tracker.py

# 生成执行报告
python3 modules/workflows/execution-tracker.py --report

# 查看特定工作流历史
python3 modules/workflows/execution-tracker.py --workflow content-creation
```

---

## 📊 输出格式

```markdown
## 工作流执行报告

**生成时间**: 2026-04-03 22:30
**统计范围**: 所有工作流

### 执行统计
| 指标 | 值 |
|------|-----|
| 总执行次数 | 48 |
| 成功次数 | 46 |
| 成功率 | 95.8% |

### 最近执行
| 时间 | 工作流 | 负责 Bot | 状态 |
|------|--------|---------|------|
| 2026-04-03 22:00 | quant-trading | 知几 | ✅ |
| 2026-04-03 21:30 | content-creation | 山木 | ✅ |
| 2026-04-03 21:00 | data-collection | 罔两 | ✅ |
| 2026-04-03 20:30 | tech-development | 素问 | 🟡 |

### 工作流效率分析
| 工作流 | 平均耗时 | 计划耗时 | 效率 |
|--------|---------|---------|------|
| content-creation | 2h15m | 2h45m | ✅ 提前 18% |
| tech-development | 10h30m | 10h30m | ✅ 准时 |
| quant-trading | 10m | 10m | ✅ 准时 |

### 改进建议
1. tech-development 偶有延期 → 增加缓冲时间
2. content-creation 效率提升 → 可考虑批量处理
```

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `modules/workflows/SKILL.md` | 本文档 |
| `modules/workflows/workflow-registry.py` | 工作流注册表 |
| `modules/workflows/execution-tracker.py` | 执行追踪器 |
| `constitution/workflows/README.md` | 工作流模板库 |

---

*创建：2026-04-03 22:17 | 太一 AGI · 守藏吏主责*
