#!/bin/bash
# 智能自动化系统定时自检自愈脚本
# 每 30 分钟自动执行一次

LOG_FILE="/home/nicola/.openclaw/workspace/logs/self-heal-$(date +%Y%m%d).log"
REPORT_FILE="/home/nicola/.openclaw/workspace/memory/self-heal-report.json"

# 创建日志目录
mkdir -p /home/nicola/.openclaw/workspace/logs

echo "========================================" >> "$LOG_FILE"
echo "自检开始：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

cd /home/nicola/.openclaw/workspace

# 执行自检
python3 << 'PYTHON_SCRIPT' >> "$LOG_FILE" 2>&1
import sys
import os
import json
import requests
from datetime import datetime

sys.path.insert(0, '/home/nicola/.openclaw/workspace/scripts')

# 1. Gateway 检查
try:
    gateway_response = requests.get('http://127.0.0.1:18789/', timeout=5)
    gateway_status = 'healthy' if gateway_response.status_code == 200 else 'degraded'
except:
    gateway_status = 'unhealthy'

# 2. Ollama 检查
try:
    ollama_response = requests.get('http://localhost:11434/api/tags', timeout=10)
    if ollama_response.status_code == 200:
        models = [m['name'] for m in ollama_response.json().get('models', [])]
        ollama_status = 'healthy' if 'qwen2.5:7b-instruct-q4_K_M' in models else 'degraded'
    else:
        ollama_status = 'unhealthy'
except:
    ollama_status = 'unhealthy'

# 3. 组件检查
components = {
    'smart_ai_router.py': '/home/nicola/.openclaw/workspace/skills/smart_ai_router.py',
    'smart_gateway.py': '/home/nicola/.openclaw/workspace/skills/smart_gateway.py',
    'smart_communication.py': '/home/nicola/.openclaw/workspace/skills/smart_communication.py',
    'smart_auto_controller.py': '/home/nicola/.openclaw/workspace/skills/smart_auto_controller.py',
    'enhanced_smart_automation.py': '/home/nicola/.openclaw/workspace/scripts/enhanced_smart_automation.py'
}
components_status = {name: 'present' if os.path.exists(path) else 'missing' for name, path in components.items()}

# 4. 本地模型测试
try:
    test_response = requests.post(
        'http://localhost:11434/api/generate',
        json={'model': 'qwen2.5:7b-instruct-q4_K_M', 'prompt': '测试', 'stream': False, 'options': {'num_predict': 20}},
        timeout=30
    )
    model_test_status = 'healthy' if test_response.status_code == 200 and 'response' in test_response.json() else 'degraded'
except:
    model_test_status = 'unhealthy'

# 5. 自愈操作
self_heal_actions = []
if gateway_status == 'unhealthy':
    os.system('openclaw gateway restart &')
    self_heal_actions.append('gateway_restart')
if ollama_status == 'unhealthy':
    os.system('systemctl --user restart ollama 2>/dev/null || true')
    self_heal_actions.append('ollama_restart')

# 6. 生成报告
report = {
    'timestamp': datetime.now().isoformat(),
    'gateway_status': gateway_status,
    'ollama_status': ollama_status,
    'model_test_status': model_test_status,
    'components_status': components_status,
    'self_heal_actions': self_heal_actions,
    'overall_health': 'healthy' if all([
        gateway_status == 'healthy',
        ollama_status == 'healthy',
        model_test_status in ['healthy', 'degraded'],
        all(s == 'present' for s in components_status.values())
    ]) else 'degraded'
}

with open('/home/nicola/.openclaw/workspace/memory/self-heal-report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"自检完成 | 状态：{report['overall_health'].upper()} | 自愈操作：{len(self_heal_actions)}项")
PYTHON_SCRIPT

echo "自检完成：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 如果系统不健康，发送通知
if [ -f "$REPORT_FILE" ]; then
    HEALTH_STATUS=$(python3 -c "import json; print(json.load(open('$REPORT_FILE'))['overall_health'])" 2>/dev/null)
    if [ "$HEALTH_STATUS" = "degraded" ] || [ "$HEALTH_STATUS" = "unhealthy" ]; then
        echo "⚠️ 系统健康状态异常：$HEALTH_STATUS" | tee -a "$LOG_FILE"
        # 可以添加通知逻辑，如发送邮件/消息
    fi
fi