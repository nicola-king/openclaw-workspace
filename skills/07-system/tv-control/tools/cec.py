#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HDMI-CEC 控制工具
"""

import subprocess
import logging

logger = logging.getLogger('TVControl.CEC')

class CECController:
    """HDMI-CEC 控制器"""
    
    def __init__(self, adapter=0):
        self.adapter = adapter
        self.available = self._check_cec()
        
        if self.available:
            logger.info("✅ HDMI-CEC 可用")
        else:
            logger.warning("⚠️ HDMI-CEC 不可用，请安装 cec-utils")
    
    def _check_cec(self):
        """检查 CEC 是否可用"""
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
    
    def _send_command(self, command):
        """发送 CEC 命令"""
        if not self.available:
            return {'status': 'error', 'message': 'CEC not available'}
        
        try:
            cmd = f'echo "{command}" | cec-client -s'
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            logger.info(f"✅ CEC 命令执行：{command}")
            logger.debug(f"输出：{result.stdout}")
            
            return {'status': 'success', 'command': command, 'output': result.stdout}
        
        except Exception as e:
            logger.error(f"CEC 命令失败：{e}")
            return {'status': 'error', 'message': str(e)}
    
    def power_on(self):
        """开机"""
        logger.info("📺 开机")
        return self._send_command('on')
    
    def power_off(self):
        """关机"""
        logger.info("📺 关机")
        return self._send_command('standby')
    
    def volume_up(self):
        """音量+"""
        logger.info("🔊 音量+")
        return self._send_command('volup')
    
    def volume_down(self):
        """音量-"""
        logger.info("🔉 音量-")
        return self._send_command('voldown')
    
    def mute(self):
        """静音"""
        logger.info("🔇 静音")
        return self._send_command('mute')
    
    def channel_up(self):
        """频道+"""
        logger.info("📺 频道+")
        return self._send_command('chup')
    
    def channel_down(self):
        """频道-"""
        logger.info("📺 频道-")
        return self._send_command('chdown')
    
    def get_power_status(self):
        """获取电源状态"""
        # TODO: 实现电源状态查询
        return 'unknown'
    
    def scan(self):
        """扫描 CEC 设备"""
        logger.info("🔍 扫描 CEC 设备")
        return self._send_command('scan')
