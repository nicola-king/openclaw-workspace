#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一自动录屏 v2.0
优化：语音指令后自动开始，用户只需操作屏幕

太一 AGI · 2026-04-21 16:45
"""

import os
import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('AutoRecorder')


class AutoRecorder:
    """太一自动录屏"""
    
    def __init__(self):
        self.videos_dir = Path.home() / "Videos"
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.is_recording = False
        self.current_file = None
        self.start_time = None
    
    def start_recording(self, auto_stop_minutes: int = 60) -> dict:
        """
        开始录制 - 一键自动化
        
        Args:
            auto_stop_minutes: 自动停止时间 (分钟)
        
        Returns:
            dict: 录制状态
        """
        logger.info("🔴 开始自动录制...")
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_file = self.videos_dir / f"{timestamp}.mp4"
        
        # 启动 OBS 录制 (后台运行)
        cmd = [
            "obs",
            "--startrecording",
            "--minimize-to-tray"
        ]
        
        try:
            # 后台启动 OBS
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            self.is_recording = True
            self.start_time = datetime.now()
            
            # 设置自动停止定时器
            if auto_stop_minutes > 0:
                self._schedule_auto_stop(auto_stop_minutes)
            
            logger.info(f"✅ 录制已开始：{self.current_file}")
            logger.info(f"⏳ 自动停止：{auto_stop_minutes}分钟后")
            
            return {
                "status": "success",
                "message": "录制已开始，请开始您的操作",
                "file": str(self.current_file),
                "auto_stop": auto_stop_minutes,
                "start_time": self.start_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ 录制启动失败：{e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def stop_recording(self) -> dict:
        """停止录制"""
        logger.info("⏹️ 停止录制...")
        
        if not self.is_recording:
            return {"status": "error", "message": "当前未录制"}
        
        try:
            # 停止 OBS 录制
            subprocess.run(
                ["obs", "--stoprecording"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            duration = (datetime.now() - self.start_time).total_seconds()
            
            result = {
                "status": "success",
                "message": "录制已停止",
                "file": str(self.current_file),
                "duration_seconds": duration,
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat()
            }
            
            self.is_recording = False
            self.current_file = None
            self.start_time = None
            
            logger.info(f"✅ 录制已停止：{duration}秒")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 停止录制失败：{e}")
            return {"status": "error", "message": str(e)}
    
    def _schedule_auto_stop(self, minutes: int):
        """设置自动停止"""
        import threading
        
        def auto_stop():
            import time
            time.sleep(minutes * 60)
            if self.is_recording:
                logger.info(f"⏰ 自动停止时间到")
                self.stop_recording()
        
        timer = threading.Timer(minutes * 60, auto_stop)
        timer.daemon = True
        timer.start()
        logger.info(f"⏰ 已设置{minutes}分钟后自动停止")
    
    def get_status(self) -> dict:
        """获取录制状态"""
        return {
            "is_recording": self.is_recording,
            "current_file": str(self.current_file) if self.current_file else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "duration_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        }


def main():
    """主函数 - 测试"""
    logger.info("=" * 60)
    logger.info("🎬 太一自动录屏 v2.0")
    logger.info("=" * 60)
    
    recorder = AutoRecorder()
    
    # 测试开始录制
    logger.info(f"\n🔴 测试开始录制...")
    result = recorder.start_recording(auto_stop_minutes=1)  # 1 分钟测试
    logger.info(f"状态：{result['status']}")
    logger.info(f"消息：{result['message']}")
    logger.info(f"文件：{result.get('file', 'N/A')}")
    logger.info(f"自动停止：{result.get('auto_stop', 0)}分钟")
    
    # 等待录制
    logger.info(f"\n⏳ 等待录制 (60 秒)...")
    import time
    time.sleep(60)
    
    # 测试停止录制
    logger.info(f"\n⏹️ 测试停止录制...")
    result = recorder.stop_recording()
    logger.info(f"状态：{result['status']}")
    logger.info(f"消息：{result['message']}")
    logger.info(f"时长：{result.get('duration_seconds', 0)}秒")
    
    # 获取状态
    logger.info(f"\n📊 录制状态:")
    status = recorder.get_status()
    logger.info(f"录制中：{status['is_recording']}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 自动录屏测试完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
