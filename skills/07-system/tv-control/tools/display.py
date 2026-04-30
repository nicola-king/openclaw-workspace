#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示器控制工具
"""

import subprocess
import logging

logger = logging.getLogger('TVControl.Display')

class DisplayController:
    """显示器控制器"""
    
    def __init__(self):
        self.available = self._check_xset()
        
        if self.available:
            logger.info("✅ 显示器控制可用")
        else:
            logger.warning("⚠️ 显示器控制不可用，请安装 x11-xserver-utils")
    
    def _check_xset(self):
        """检查 xset 是否可用"""
        try:
            result = subprocess.run(
                ['which', 'xset'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"xset 检查失败：{e}")
            return False
    
    def _run_command(self, command):
        """执行显示命令"""
        if not self.available:
            return {'status': 'error', 'message': 'xset not available'}
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            logger.info(f"✅ 显示命令执行：{command}")
            return {'status': 'success', 'output': result.stdout}
        
        except Exception as e:
            logger.error(f"显示命令失败：{e}")
            return {'status': 'error', 'message': str(e)}
    
    def turn_on(self):
        """开启显示器"""
        logger.info("📺 开启显示器")
        return self._run_command('xset dpms force on')
    
    def turn_off(self):
        """关闭显示器"""
        logger.info("📺 关闭显示器")
        return self._run_command('xset dpms force off')
    
    def get_status(self):
        """获取显示器状态"""
        try:
            result = subprocess.run(
                'xset q | grep "Monitor is"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if 'on' in result.stdout.lower():
                return 'on'
            elif 'off' in result.stdout.lower():
                return 'off'
            else:
                return 'unknown'
        
        except Exception as e:
            logger.error(f"获取状态失败：{e}")
            return 'unknown'
