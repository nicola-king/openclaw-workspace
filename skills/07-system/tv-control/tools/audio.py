#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频控制工具
"""

import subprocess
import logging
import re

logger = logging.getLogger('TVControl.Audio')

class AudioController:
    """音频控制器"""
    
    def __init__(self, device='Master'):
        self.device = device
        self.available = self._check_audio()
        
        if self.available:
            logger.info("✅ 音频控制可用")
        else:
            logger.warning("⚠️ 音频控制不可用，请安装 alsa-utils")
    
    def _check_audio(self):
        """检查音频工具是否可用"""
        try:
            result = subprocess.run(
                ['which', 'amixer'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"音频检查失败：{e}")
            return False
    
    def _run_command(self, command):
        """执行音频命令"""
        if not self.available:
            return {'status': 'error', 'message': 'Audio not available'}
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            logger.info(f"✅ 音频命令执行：{command}")
            return {'status': 'success', 'output': result.stdout}
        
        except Exception as e:
            logger.error(f"音频命令失败：{e}")
            return {'status': 'error', 'message': str(e)}
    
    def volume_up(self, step=5):
        """音量+"""
        logger.info(f"🔊 音量+{step}%")
        return self._run_command(f'amixer set {self.device} {step}%+')
    
    def volume_down(self, step=5):
        """音量-"""
        logger.info(f"🔉 音量-{step}%")
        return self._run_command(f'amixer set {self.device} {step}%-')
    
    def set_volume(self, level):
        """设置音量"""
        logger.info(f"🔊 设置音量 {level}%")
        return self._run_command(f'amixer set {self.device} {level}%')
    
    def mute(self):
        """静音"""
        logger.info("🔇 静音")
        return self._run_command(f'amixer set {self.device} toggle')
    
    def get_volume(self):
        """获取音量"""
        try:
            result = subprocess.run(
                f'amixer get {self.device} | grep -o "[0-9]+%" | head -1',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            volume = result.stdout.strip()
            return volume
        except Exception as e:
            logger.error(f"获取音量失败：{e}")
            return 'unknown'
    
    def is_muted(self):
        """检查是否静音"""
        try:
            result = subprocess.run(
                f'amixer get {self.device} | grep -o "\\[on\\]\\|\\[off\\]" | head -1',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            return 'off' in result.stdout
        except Exception as e:
            logger.error(f"检查静音失败：{e}")
            return False
