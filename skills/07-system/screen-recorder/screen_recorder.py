#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Screen Recorder Skill · 录屏技能 v1.0
太一 AGI · 2026-04-21 16:11

核心能力:
- OBS Studio 控制
- Excalidraw 白板集成
- 摄像头画中画
- 录制文件管理
"""

import os
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('ScreenRecorder')


class ScreenRecorder:
    """录屏技能"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        "resolution": "1920x1080",
        "fps": 30,
        "bitrate": 6000,
        "format": "mp4",
        "audio": True,
        "camera": True,
        "camera_size": 150,
        "camera_position": "bottom_right",
        "whiteboard_url": "https://excalidraw.com"
    }
    
    # 录制目录
    RECORDINGS_DIR = Path.home() / ".openclaw" / "workspace" / "recordings"
    
    def __init__(self, config: Dict = None):
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.is_recording = False
        self.current_file = None
        self.start_time = None
        
        # 确保录制目录存在
        self.RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.info("🎬 Screen Recorder Skill v1.0 已初始化")
    
    def check_obs_installed(self) -> bool:
        """检查 OBS 是否已安装"""
        try:
            result = subprocess.run(
                ["which", "obs"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"检查 OBS 安装失败：{e}")
            return False
    
    def install_obs(self) -> bool:
        """安装 OBS Studio"""
        logger.info("📦 正在安装 OBS Studio...")
        
        try:
            # Linux 安装
            subprocess.run(
                ["sudo", "apt", "install", "-y", "obs-studio"],
                check=True
            )
            logger.info("✅ OBS Studio 安装成功")
            return True
        except Exception as e:
            logger.error(f"OBS 安装失败：{e}")
            return False
    
    def open_whiteboard(self) -> bool:
        """打开白板 (Excalidraw)"""
        logger.info(f"🎨 打开白板：{self.config['whiteboard_url']}")
        
        try:
            # 使用默认浏览器打开
            subprocess.run(
                ["xdg-open", self.config['whiteboard_url']],
                check=True
            )
            logger.info("✅ 白板已打开")
            return True
        except Exception as e:
            logger.error(f"打开白板失败：{e}")
            return False
    
    def start_recording(self, name: str = None) -> Dict:
        """开始录制"""
        logger.info("🔴 开始录制...")
        
        # 检查 OBS
        if not self.check_obs_installed():
            logger.warning("⚠️ OBS 未安装，尝试安装...")
            if not self.install_obs():
                return {"status": "error", "message": "OBS 安装失败"}
        
        # 生成文件名
        if not name:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            name = f"recording_{timestamp}"
        
        today_dir = self.RECORDINGS_DIR / datetime.now().strftime("%Y-%m-%d")
        today_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = today_dir / f"{name}.{self.config['format']}"
        
        # 构建 OBS 命令行
        cmd = [
            "obs",
            "--startrecording",
            "--recording-path", str(output_file)
        ]
        
        try:
            # 启动录制 (简化版本，实际应使用 OBS WebSocket API)
            subprocess.Popen(cmd)
            
            self.is_recording = True
            self.current_file = str(output_file)
            self.start_time = datetime.now()
            
            logger.info(f"✅ 录制已开始：{output_file}")
            
            return {
                "status": "success",
                "message": "录制已开始",
                "file": str(output_file),
                "start_time": self.start_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"开始录制失败：{e}")
            return {"status": "error", "message": str(e)}
    
    def stop_recording(self) -> Dict:
        """停止录制"""
        logger.info("⏹️ 停止录制...")
        
        if not self.is_recording:
            return {"status": "error", "message": "当前未录制"}
        
        try:
            # 停止录制 (简化版本)
            subprocess.run(["obs", "--stoprecording"], check=True)
            
            duration = (datetime.now() - self.start_time).total_seconds()
            
            result = {
                "status": "success",
                "message": "录制已停止",
                "file": self.current_file,
                "duration_seconds": duration,
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat()
            }
            
            self.is_recording = False
            self.current_file = None
            self.start_time = None
            
            logger.info(f"✅ 录制已停止：{result['duration_seconds']}秒")
            
            return result
            
        except Exception as e:
            logger.error(f"停止录制失败：{e}")
            return {"status": "error", "message": str(e)}
    
    def pause_recording(self) -> Dict:
        """暂停录制"""
        logger.info("⏸️ 暂停录制...")
        
        if not self.is_recording:
            return {"status": "error", "message": "当前未录制"}
        
        try:
            subprocess.run(["obs", "--pause"], check=True)
            logger.info("✅ 录制已暂停")
            return {"status": "success", "message": "录制已暂停"}
        except Exception as e:
            logger.error(f"暂停录制失败：{e}")
            return {"status": "error", "message": str(e)}
    
    def resume_recording(self) -> Dict:
        """继续录制"""
        logger.info("▶️ 继续录制...")
        
        if not self.is_recording:
            return {"status": "error", "message": "当前未录制"}
        
        try:
            subprocess.run(["obs", "--unpause"], check=True)
            logger.info("✅ 录制已继续")
            return {"status": "success", "message": "录制已继续"}
        except Exception as e:
            logger.error(f"继续录制失败：{e}")
            return {"status": "error", "message": str(e)}
    
    def get_recordings(self, days: int = 7) -> list:
        """获取录制文件列表"""
        logger.info(f"📋 获取最近{days}天的录制文件...")
        
        recordings = []
        today = datetime.now()
        
        for i in range(days):
            date = today - timedelta(days=i)
            date_dir = self.RECORDINGS_DIR / date.strftime("%Y-%m-%d")
            
            if date_dir.exists():
                for file in date_dir.glob(f"*.{self.config['format']}"):
                    recordings.append({
                        "file": str(file),
                        "date": date.strftime("%Y-%m-%d"),
                        "size_mb": round(file.stat().st_size / 1024 / 1024, 2)
                    })
        
        logger.info(f"✅ 找到{len(recordings)}个录制文件")
        return recordings
    
    def get_config(self) -> Dict:
        """获取当前配置"""
        return self.config
    
    def update_config(self, new_config: Dict) -> Dict:
        """更新配置"""
        logger.info("⚙️ 更新配置...")
        
        self.config.update(new_config)
        
        logger.info(f"✅ 配置已更新：{new_config}")
        return self.config
    
    def get_status(self) -> Dict:
        """获取录制状态"""
        return {
            "is_recording": self.is_recording,
            "current_file": self.current_file,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "duration_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            "config": self.config
        }


# 导入 timedelta
from datetime import timedelta


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🎬 Screen Recorder Skill · 录屏技能 v1.0")
    logger.info("=" * 60)
    
    recorder = ScreenRecorder()
    
    # 检查 OBS
    logger.info(f"\n🔍 检查 OBS 安装...")
    if recorder.check_obs_installed():
        logger.info("✅ OBS 已安装")
    else:
        logger.warning("⚠️ OBS 未安装")
    
    # 获取配置
    logger.info(f"\n⚙️ 当前配置:")
    config = recorder.get_config()
    for key, value in config.items():
        logger.info(f"  {key}: {value}")
    
    # 获取状态
    logger.info(f"\n📊 当前状态:")
    status = recorder.get_status()
    logger.info(f"  录制中：{status['is_recording']}")
    logger.info(f"  当前文件：{status['current_file']}")
    logger.info(f"  录制时长：{status['duration_seconds']}秒")
    
    # 获取录制文件
    logger.info(f"\n📋 最近录制文件:")
    recordings = recorder.get_recordings(days=7)
    for rec in recordings[:5]:
        logger.info(f"  {rec['file']} ({rec['size_mb']}MB)")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 录屏技能演示完成！")
    logger.info("=" * 60)
    
    # 使用说明
    logger.info("\n📋 使用方式:")
    logger.info("  1. 语音指令：'太一，开始录屏'")
    logger.info("  2. 文字指令：'/录屏 开始'")
    logger.info("  3. API 调用：recorder.start_recording()")


if __name__ == "__main__":
    main()
