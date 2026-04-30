#!/bin/bash
# 智能自动化系统启动脚本

echo "=== 智能自动化系统启动 ==="

# 设置工作目录
cd /home/nicola/.openclaw/workspace

# 检查必要的环境变量
echo "检查环境变量..."
if [ -z "$BAILIAN_API_KEY" ]; then
    echo "警告: BAILIAN_API_KEY 未设置"
fi

if [ -z "$GOOGLE_API_KEY" ]; then
    echo "警告: GOOGLE_API_KEY 未设置"
fi

# 检查 Ollama 是否运行
echo "检查 Ollama 服务..."
OLLAMA_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/api/tags)
if [ "$OLLAMA_STATUS" = "200" ]; then
    echo "✅ Ollama 服务正常运行"
else
    echo "❌ Ollama 服务未运行，尝试启动..."
    ollama serve &
    sleep 5
    OLLAMA_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/api/tags)
    if [ "$OLLAMA_STATUS" = "200" ]; then
        echo "✅ Ollama 服务已启动"
    else
        echo "❌ 无法启动 Ollama 服务"
    fi
fi

# 检查必要的 Python 包
echo "检查 Python 依赖..."
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装缺失的 Python 包..."
    pip3 install requests
fi

# 检查智能自动化组件
echo "检查智能自动化组件..."
COMPONENTS=("smart_ai_router.py" "smart_gateway.py" "smart_communication.py" "smart_auto_controller.py")

for component in "${COMPONENTS[@]}"; do
    if [ -f "skills/$component" ]; then
        echo "✅ $component 存在"
    else
        echo "❌ $component 不存在"
    fi
done

# 启动智能自动化控制器
echo "启动智能自动化控制器..."
python3 -c "
import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills')
try:
    from smart_auto_controller import SmartAutomationController
    controller = SmartAutomationController()
    if controller.initialize_system():
        print('✅ 智能自动化系统初始化成功')
        controller.start_monitoring(interval=60)
        print('✅ 后台监控已启动')
        controller.save_state()
        print('✅ 系统状态已保存')
    else:
        print('❌ 智能自动化系统初始化失败')
except Exception as e:
    print(f'❌ 启动过程中出现错误: {e}')
"

echo "=== 智能自动化系统启动完成 ==="

# 显示当前运行的服务
echo "当前运行的相关进程:"
ps aux | grep -E "(openclaw|ollama|gateway)" | grep -v grep