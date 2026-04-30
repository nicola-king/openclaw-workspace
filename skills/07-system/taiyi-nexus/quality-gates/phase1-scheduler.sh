#!/bin/bash
# 太一 NEXUS Phase 1: 调度执行质量门禁
# 检查：任务 100% 执行

echo "🛡️ Phase 1: 调度执行质量门禁"
echo "================================"

# 检查 1: 任务执行率
echo "检查 1: 任务执行率..."
EXECUTION_RATE=$(python3 -c "
import json
from pathlib import Path

log_file = Path('monitoring/scheduler-log.json')
if log_file.exists():
    with open(log_file, 'r') as f:
        logs = json.load(f)
    if logs:
        success = sum(1 for log in logs[-10:] if log.get('success', False))
        rate = (success / len(logs[-10:])) * 100
        print(f'{rate:.1f}')
    else:
        print('0.0')
else:
    print('0.0')
")

if (( $(echo "$EXECUTION_RATE >= 100" | bc -l) )); then
    echo "  ✅ 任务执行率：${EXECUTION_RATE}%"
else
    echo "  ❌ 任务执行率：${EXECUTION_RATE}% (目标：100%)"
    exit 1
fi

# 检查 2: 无执行失败
echo "检查 2: 无执行失败..."
FAILURES=$(python3 -c "
import json
from pathlib import Path

log_file = Path('monitoring/scheduler-log.json')
if log_file.exists():
    with open(log_file, 'r') as f:
        logs = json.load(f)
    failures = sum(1 for log in logs[-10:] if not log.get('success', False))
    print(failures)
else:
    print('0')
")

if [ "$FAILURES" -eq 0 ]; then
    echo "  ✅ 执行失败：0 次"
else
    echo "  ❌ 执行失败：${FAILURES}次 (目标：0)"
    exit 1
fi

# 检查 3: 日志记录完整
echo "检查 3: 日志记录完整..."
if [ -f "monitoring/scheduler-log.json" ]; then
    echo "  ✅ 日志文件存在"
else
    echo "  ❌ 日志文件缺失"
    exit 1
fi

# 检查 4: 性能指标正常
echo "检查 4: 性能指标正常..."
AVG_DURATION=$(python3 -c "
import json
from pathlib import Path

log_file = Path('monitoring/scheduler-log.json')
if log_file.exists():
    with open(log_file, 'r') as f:
        logs = json.load(f)
    if logs:
        durations = [log.get('duration_seconds', 0) for log in logs[-10:]]
        avg = sum(durations) / len(durations)
        print(f'{avg:.2f}')
    else:
        print('0.00')
else:
    print('0.00')
")

if (( $(echo "$AVG_DURATION < 5" | bc -l) )); then
    echo "  ✅ 平均执行时间：${AVG_DURATION}秒"
else
    echo "  ⚠️ 平均执行时间：${AVG_DURATION}秒 (偏长)"
fi

echo ""
echo "✅ Phase 1: 调度执行质量门禁通过"
exit 0
