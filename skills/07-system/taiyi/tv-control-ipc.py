#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一电视控制技能 (工控机直连版)
控制方式：HDMI-CEC + 系统命令
无需网络协议，直接控制！
"""

import os
import subprocess
import logging
import requests
from datetime import datetime
from flask import Flask, request, jsonify

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/tv-control.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TVControlIPC')

# Flask API
app = Flask(__name__)

# 配置
CONFIG = {
    'telegram_bot_token': '8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY',
    'telegram_chat_id': '7073481596',
    'api_port': 5001,
    'api_token': 'taiyi_tv_control_secret',
    'control_method': 'cec',  # 'cec' 或 'xset'
}

class TVControllerIPC:
    """工控机直连电视控制器"""
    
    def __init__(self):
        self.cec_available = self._check_cec()
        self.display_type = self._detect_display()
        logger.info(f"📺 检测到显示设备：{self.display_type}")
        logger.info(f"🔌 HDMI-CEC 状态：{'✅ 可用' if self.cec_available else '❌ 不可用'}")
    
    def _check_cec(self):
        """检查 HDMI-CEC 是否可用"""
        try:
            result = subprocess.run(
                ['which', 'cec-client'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"CEC 检查失败：{e}")
            return False
    
    def _detect_display(self):
        """检测显示器类型"""
        try:
            result = subprocess.run(
                ['xrandr'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'connected' in result.stdout:
                return 'X11'
        except Exception:
            pass
        return 'unknown'
    
    def _run_command(self, command):
        """执行系统命令"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            logger.info(f"✅ 命令执行成功：{command}")
            logger.debug(f"输出：{result.stdout}")
            return {'status': 'success', 'output': result.stdout}
        except Exception as e:
            logger.error(f"❌ 命令执行失败：{e}")
            return {'status': 'error', 'message': str(e)}
    
    def power_on(self):
        """开机"""
        logger.info("📺 电视开机")
        
        if self.cec_available:
            # HDMI-CEC 开机
            return self._run_command('echo "on" | cec-client -s')
        else:
            # 唤醒显示器
            return self._run_command('xset dpms force on')
    
    def power_off(self):
        """关机"""
        logger.info("📺 电视关机")
        
        if self.cec_available:
            # HDMI-CEC 待机
            return self._run_command('echo "standby" | cec-client -s')
        else:
            # 关闭显示器
            return self._run_command('xset dpms force off')
    
    def volume_up(self):
        """音量+"""
        logger.info("🔊 音量+")
        return self._run_command('amixer set Master 5%+')
    
    def volume_down(self):
        """音量-"""
        logger.info("🔉 音量-")
        return self._run_command('amixer set Master 5%-')
    
    def mute(self):
        """静音"""
        logger.info("🔇 静音")
        return self._run_command('amixer set Master toggle')
    
    def get_status(self):
        """获取状态"""
        logger.info("📊 查询状态")
        
        status = {
            'power': 'unknown',
            'volume': 'unknown',
            'mute': 'unknown',
        }
        
        # 检查显示器电源状态
        try:
            result = subprocess.run(
                'xset q | grep "Monitor is"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'on' in result.stdout.lower():
                status['power'] = 'on'
            elif 'off' in result.stdout.lower():
                status['power'] = 'off'
            else:
                status['power'] = 'unknown'
        except Exception:
            pass
        
        # 检查音量
        try:
            result = subprocess.run(
                'amixer get Master | grep -o "[0-9]+%" | head -1',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            status['volume'] = result.stdout.strip()
        except Exception:
            pass
        
        # 检查静音
        try:
            result = subprocess.run(
                'amixer get Master | grep -o "\\[on\\]\\|\\[off\\]" | head -1',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            status['mute'] = 'off' if 'on' in result.stdout else 'on'
        except Exception:
            pass
        
        return status

# 全局控制器
tv_controller = None

def get_controller():
    """获取控制器 (单例)"""
    global tv_controller
    if tv_controller is None:
        tv_controller = TVControllerIPC()
    return tv_controller

def send_telegram_message(message):
    """发送 Telegram 消息"""
    url = f"https://api.telegram.org/bot{CONFIG['telegram_bot_token']}/sendMessage"
    data = {
        'chat_id': CONFIG['telegram_chat_id'],
        'text': message,
        'parse_mode': 'Markdown',
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            logger.info("✅ Telegram 消息发送成功")
            return True
        else:
            logger.error(f"Telegram 发送失败：{response.text}")
            return False
    except Exception as e:
        logger.error(f"Telegram 发送异常：{e}")
        return False

def handle_tv_command(command, args=None):
    """处理电视控制指令"""
    controller = get_controller()
    
    command_map = {
        'on': controller.power_on,
        'off': controller.power_off,
        'vol+': controller.volume_up,
        'vol-': controller.volume_down,
        'mute': controller.mute,
        'status': controller.get_status,
    }
    
    if command in command_map:
        result = command_map[command]()
        
        if command == 'status':
            status = result
            message = f"""📺 电视状态

电源：{status.get('power', '未知')}
音量：{status.get('volume', '未知')}
静音：{status.get('mute', '未知')}

控制方式：{"HDMI-CEC" if controller.cec_available else "xset"}

---
太一 · 电视控制 (工控机直连)"""
            send_telegram_message(message)
            return {'status': 'success', 'data': status}
        else:
            if result['status'] == 'success':
                emoji_map = {
                    'on': '🔌',
                    'off': '🔌',
                    'vol+': '🔊',
                    'vol-': '🔉',
                    'mute': '🔇',
                }
                emoji = emoji_map.get(command, '📺')
                message = f"""{emoji} 电视控制

指令：{command}
状态：✅ 成功
方式：{"HDMI-CEC" if controller.cec_available else "xset"}

---
太一 · 电视控制 (工控机直连)"""
                send_telegram_message(message)
            else:
                message = f"""❌ 电视控制失败

指令：{command}
错误：{result.get('message', '未知错误')}

---
太一 · 电视控制 (工控机直连)"""
                send_telegram_message(message)
            
            return result
    else:
        message = f"""❌ 未知电视指令

可用指令：
- /tv on - 开机
- /tv off - 关机
- /tv vol+ - 音量+
- /tv vol- - 音量-
- /tv mute - 静音
- /tv status - 查询状态

---
太一 · 电视控制 (工控机直连)"""
        send_telegram_message(message)
        return {'status': 'error', 'message': 'Unknown command'}

# HTTP API 端点
@app.route('/tv/control', methods=['POST'])
def api_control():
    """电视控制 API"""
    data = request.json
    token = data.get('token', '')
    
    if token != CONFIG['api_token']:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    
    command = data.get('command', '')
    args = data.get('args', {})
    
    result = handle_tv_command(command, args)
    return jsonify(result)

@app.route('/tv/status', methods=['GET'])
def api_status():
    """电视状态 API"""
    controller = get_controller()
    status = controller.get_status()
    return jsonify(status)

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'service': 'taiyi-tv-control-ipc'})

def install_dependencies():
    """安装依赖"""
    logger.info("📦 检查依赖...")
    
    # 检查 cec-utils
    cec_result = subprocess.run(['which', 'cec-client'], capture_output=True)
    if cec_result.returncode != 0:
        logger.warning("⚠️ cec-client 未安装")
        logger.info("安装命令：sudo apt-get install cec-utils")
    else:
        logger.info("✅ cec-utils 已安装")
    
    # 检查 alsa-utils
    amixer_result = subprocess.run(['which', 'amixer'], capture_output=True)
    if amixer_result.returncode != 0:
        logger.warning("⚠️ amixer 未安装")
        logger.info("安装命令：sudo apt-get install alsa-utils")
    else:
        logger.info("✅ alsa-utils 已安装")

def main():
    """主函数"""
    logger.info("🚀 太一电视控制启动 (工控机直连版)...")
    
    # 检查依赖
    install_dependencies()
    
    # 初始化控制器
    controller = get_controller()
    
    # 测试连接
    logger.info("🧪 测试控制...")
    status = controller.get_status()
    logger.info(f"📊 当前状态：{status}")
    
    # 启动 HTTP API
    logger.info(f"🌐 HTTP API 启动在端口 {CONFIG['api_port']}")
    app.run(host='0.0.0.0', port=CONFIG['api_port'], debug=False)

if __name__ == '__main__':
    main()
