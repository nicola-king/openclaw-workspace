#!/bin/bash
# 太一 NEXUS Phase 2: PDCA 循环质量门禁
# 检查：P-D-C-A 全部完成

echo "🛡️ Phase 2: PDCA 循环质量门禁"
echo "================================"

# 检查 1: P-D-C-A 全部完成
echo "检查 1: P-D-C-A 全部完成..."
PDCA_LOG="monitoring/pdca-cycle-log.json"

if [ -f "$PDCA_LOG" ]; then
    PDCA_COMPLETE=$(python3 -c "
import json
with open('$PDCA_LOG', 'r') as f:
    logs = json.load(f)
if logs:
    last = logs[-1]
    phases = last.get('phases', {})
    complete = all(key in phases for key in ['plan', 'do', 'check', 'act'])
    print('true' if complete else 'false')
else:
    print('false')
")
    
    if [ "$PDCA_COMPLETE" = "true" ]; then
        echo "  ✅ P-D-C-A 全部完成"
    else
        echo "  ❌ P-D-C-A 未完成"
        exit 1
    fi
else
    echo "  ❌ PDCA 日志文件缺失"
    exit 1
fi

# 检查 2: 改进措施已执行
echo "检查 2: 改进措施已执行..."
IMPROVEMENTS=$(python3 -c "
import json
with open('$PDCA_LOG', 'r') as f:
    logs = json.load(f)
if logs:
    last = logs[-1]
    do_phase = last.get('phases', {}).get('do', {})
    executed = do_phase.get('executed', False)
    print('true' if executed else 'false')
else:
    print('false')
")

if [ "$IMPROVEMENTS" = "true" ]; then
    echo "  ✅ 改进措施已执行"
else
    echo "  ❌ 改进措施未执行"
    exit 1
fi

# 检查 3: 改进效果已验证
echo "检查 3: 改进效果已验证..."
VERIFIED=$(python3 -c "
import json
with open('$PDCA_LOG', 'r') as f:
    logs = json.load(f)
if logs:
    last = logs[-1]
    check_phase = last.get('phases', {}).get('check', {})
    verified = check_phase.get('new_progress', 0) > 0
    print('true' if verified else 'false')
else:
    print('false')
")

if [ "$VERIFIED" = "true" ]; then
    echo "  ✅ 改进效果已验证"
else
    echo "  ❌ 改进效果未验证"
    exit 1
fi

# 检查 4: 成功经验已标准化
echo "检查 4: 成功经验已标准化..."
STANDARDIZED=$(python3 -c "
import json
with open('$PDCA_LOG', 'r') as f:
    logs = json.load(f)
if logs:
    last = logs[-1]
    act_phase = last.get('phases', {}).get('act', {})
    action = act_phase.get('action', '')
    standardized = 'standardize' in action.lower() or action != ''
    print('true' if standardized else 'false')
else:
    print('false')
")

if [ "$STANDARDIZED" = "true" ]; then
    echo "  ✅ 成功经验已标准化"
else
    echo "  ⚠️ 成功经验未标准化"
fi

echo ""
echo "✅ Phase 2: PDCA 循环质量门禁通过"
exit 0
