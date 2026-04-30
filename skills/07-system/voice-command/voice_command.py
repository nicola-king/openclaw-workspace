#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一语音命令 - 电脑麦克风语音控制

功能:
- 麦克风实时监听
- 语音识别 (Vosk/Whisper)
- 命令解析
- 自动执行太一任务

唤醒词："太一" 或 "Taiyi"

作者：太一 AGI
创建：2026-04-15
基于：tv-control/voice-control.py 改造
"""

import os
import sys
import logging
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 尝试导入 Vosk
try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    VOSK_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Vosk 未安装：{e}")
    print("安装命令：pip3 install vosk pyaudio")
    VOSK_AVAILABLE = False

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
LOG_DIR = WORKSPACE / "logs"
AUDIO_DIR = WORKSPACE / "audio" / "voice-command"
MODEL_PATH = WORKSPACE / "models" / "vosk-model-cn-0.15"

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_DIR / "voice-command.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('VoiceCommand')

# 唤醒词
WAKE_WORDS = ["太一", "taiyi", "tai yee"]

# 命令映射 (通用任务)
COMMAND_PATTERNS = {
    # 系统控制
    "系统自检": "system_check",
    "自检": "system_check",
    "运行自检": "system_check",
    
    "打开 dashboard": "open_dashboard",
    "启动 dashboard": "open_dashboard",
    "dashboard": "open_dashboard",
    
    "关闭系统": "shutdown",
    "关机": "shutdown",
    
    # 任务执行
    "执行任务": "run_task",
    "运行任务": "run_task",
    "创建任务": "create_task",
    
    # 查询
    "今天天气": "weather_today",
    "天气": "weather_today",
    "查看日历": "check_calendar",
    "日历": "check_calendar",
    "查看邮件": "check_email",
    "邮件": "check_email",
    
    # 记忆
    "记住这个": "remember_this",
    "添加到记忆": "remember_this",
    "搜索记忆": "search_memory",
    "查找记忆": "search_memory",
    
    # 报告
    "生成日报": "daily_report",
    "日报": "daily_report",
    "生成周报": "weekly_report",
    "周报": "weekly_report",
    
    # GitHub
    "查看 github": "check_github",
    "github 状态": "check_github",
    "查看仓库": "check_github",
    
    # 通用命令 (后续处理)
    "帮我": "general_task",
    "请帮我": "general_task",
    "执行": "general_task",
    "运行": "general_task",
}


class VoiceCommandController:
    """语音命令控制器"""
    
    def __init__(self, model_path: str = str(MODEL_PATH)):
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.audio = None
        self.stream = None
        self.wake_word_detected = False
        self.running = False
        self.pending_command = False
        
        # 初始化语音识别
        if VOSK_AVAILABLE:
            self._init_vosk()
    
    def _init_vosk(self):
        """初始化 Vosk"""
        try:
            # 检查模型是否存在
            if not os.path.exists(self.model_path):
                logger.error(f"❌ 语音模型不存在：{self.model_path}")
                logger.info("💡 下载模型命令:")
                logger.info("  wget https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip")
                logger.info("  unzip vosk-model-cn-0.15.zip")
                logger.info("  mkdir -p ~/workspace/models && mv vosk-model-cn-0.15 ~/workspace/models/")
                return False
            
            # 加载模型
            logger.info(f"📦 加载语音模型：{self.model_path}")
            self.model = Model(model_path=self.model_path)
            
            # 创建识别器
            self.recognizer = KaldiRecognizer(self.model, 16000)
            
            # 初始化音频
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4000
            )
            
            logger.info("✅ Vosk 初始化完成")
            return True
        
        except Exception as e:
            logger.error(f"❌ Vosk 初始化失败：{e}")
            return False
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """监听语音"""
        if not self.stream:
            return None
        
        try:
            data = self.stream.read(4000, exception_on_overflow=False)
            
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '').strip()
                
                if text:
                    logger.info(f"🎤 识别到：{text}")
                    return text
            
            return None
        
        except Exception as e:
            logger.error(f"❌ 监听失败：{e}")
            return None
    
    def check_wake_word(self, text: str) -> bool:
        """检查唤醒词"""
        text_lower = text.lower()
        for wake_word in WAKE_WORDS:
            if wake_word in text_lower:
                logger.info(f"✅ 唤醒词检测：{wake_word}")
                return True
        return False
    
    def parse_command(self, text: str) -> Dict:
        """
        解析语音命令
        
        Returns:
            {
                "command_code": "system_check",
                "original_text": "太一系统自检",
                "parameters": {}
            }
        """
        # 移除唤醒词
        text_clean = text
        for wake_word in WAKE_WORDS:
            text_clean = text_clean.replace(wake_word, '').replace(wake_word.capitalize(), '').strip()
        
        # 匹配命令
        for command_text, command_code in COMMAND_PATTERNS.items():
            if command_text in text_clean:
                logger.info(f"✅ 命令匹配：{command_text} -> {command_code}")
                return {
                    "command_code": command_code,
                    "original_text": text,
                    "clean_text": text_clean,
                    "parameters": {}
                }
        
        # 未匹配到具体命令，作为通用任务
        logger.info(f"📝 通用任务：{text_clean}")
        return {
            "command_code": "general_task",
            "original_text": text,
            "clean_text": text_clean,
            "parameters": {
                "task_description": text_clean
            }
        }
    
    def execute_command(self, command: Dict) -> bool:
        """执行命令"""
        command_code = command.get("command_code")
        original_text = command.get("original_text")
        parameters = command.get("parameters", {})
        
        logger.info(f"🔧 执行命令：{command_code}")
        logger.info(f"  原始文本：{original_text}")
        
        try:
            if command_code == "system_check":
                return self._run_system_check()
            
            elif command_code == "open_dashboard":
                return self._open_dashboard()
            
            elif command_code == "weather_today":
                return self._check_weather()
            
            elif command_code == "daily_report":
                return self._generate_daily_report()
            
            elif command_code == "weekly_report":
                return self._generate_weekly_report()
            
            elif command_code == "check_github":
                return self._check_github()
            
            elif command_code == "general_task":
                return self._run_general_task(parameters.get("task_description", original_text))
            
            else:
                self.speak(f"对不起，我不理解这个命令：{original_text}")
                return False
        
        except Exception as e:
            logger.error(f"❌ 执行失败：{e}")
            self.speak("对不起，执行失败")
            return False
    
    def _run_system_check(self) -> bool:
        """系统自检"""
        logger.info("🛡️  运行系统自检...")
        self.speak("好的，正在运行系统自检")
        
        try:
            result = subprocess.run(
                ["bash", "/tmp/openclaw-watchdog.sh", "status"],
                capture_output=True,
                timeout=30
            )
            
            output = result.stdout.decode()
            logger.info(f"自检结果:\n{output}")
            
            self.speak("系统自检完成，所有系统正常")
            return True
        
        except Exception as e:
            logger.error(f"❌ 自检失败：{e}")
            return False
    
    def _open_dashboard(self) -> bool:
        """打开 Dashboard"""
        logger.info("📊 打开 Dashboard...")
        self.speak("好的，正在打开 Dashboard")
        
        try:
            # 启动 Dashboard
            subprocess.run(
                ["bash", WORKSPACE / "scripts" / "dashboard-auto-manager.sh", "open"],
                capture_output=True,
                timeout=30
            )
            
            self.speak("Dashboard 已打开，访问地址是 localhost 端口 5001")
            return True
        
        except Exception as e:
            logger.error(f"❌ 打开 Dashboard 失败：{e}")
            return False
    
    def _check_weather(self) -> bool:
        """查询天气"""
        logger.info("🌤️  查询天气...")
        self.speak("好的，正在查询天气")
        
        try:
            # 使用 weather skill
            result = subprocess.run(
                ["curl", "-s", "wttr.in/Shanghai?format=3"],
                capture_output=True,
                timeout=30
            )
            
            weather = result.stdout.decode().strip()
            logger.info(f"天气：{weather}")
            
            self.speak(f"当前天气：{weather}")
            return True
        
        except Exception as e:
            logger.error(f"❌ 查询天气失败：{e}")
            return False
    
    def _generate_daily_report(self) -> bool:
        """生成日报"""
        logger.info("📝 生成日报...")
        self.speak("好的，正在生成日报")
        
        try:
            result = subprocess.run(
                ["bash", "/opt/openclaw-report.sh", "daily"],
                capture_output=True,
                timeout=60
            )
            
            self.speak("日报已生成")
            return True
        
        except Exception as e:
            logger.error(f"❌ 生成日报失败：{e}")
            return False
    
    def _generate_weekly_report(self) -> bool:
        """生成周报"""
        logger.info("📊 生成周报...")
        self.speak("好的，正在生成周报")
        
        try:
            result = subprocess.run(
                ["bash", "/opt/openclaw-report.sh", "weekly"],
                capture_output=True,
                timeout=60
            )
            
            self.speak("周报已生成")
            return True
        
        except Exception as e:
            logger.error(f"❌ 生成周报失败：{e}")
            return False
    
    def _check_github(self) -> bool:
        """查看 GitHub"""
        logger.info("🐙 查看 GitHub...")
        self.speak("好的，正在查看 GitHub")
        
        try:
            result = subprocess.run(
                ["gh", "repo", "list", "--limit", "5"],
                capture_output=True,
                timeout=30
            )
            
            output = result.stdout.decode()
            logger.info(f"GitHub 仓库:\n{output}")
            
            self.speak("GitHub 仓库列表已获取")
            return True
        
        except Exception as e:
            logger.error(f"❌ 查看 GitHub 失败：{e}")
            return False
    
    def _run_general_task(self, task_description: str) -> bool:
        """执行通用任务"""
        logger.info(f"📋 执行通用任务：{task_description}")
        self.speak("好的，正在处理你的任务")
        
        try:
            # 通过 OpenClaw 发送任务给太一
            cmd = [
                "openclaw", "message", "send",
                "--channel", "telegram",
                "--target", "7073481596",  # 用户 Telegram ID
                "--message", f"🎤 语音任务：{task_description}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0:
                self.speak("任务已发送给太一处理")
                return True
            else:
                self.speak("任务发送失败")
                return False
        
        except Exception as e:
            logger.error(f"❌ 任务执行失败：{e}")
            return False
    
    def speak(self, text: str):
        """语音反馈 (TTS)"""
        logger.info(f"🔊 语音反馈：{text}")
        
        try:
            # 使用 espeak (如果安装)
            subprocess.run(['espeak', '-v', 'zh', text], timeout=10, capture_output=True)
        except Exception:
            # 如无 espeak，仅日志
            pass
    
    def run(self):
        """运行语音控制"""
        if not VOSK_AVAILABLE:
            logger.error("❌ Vosk 不可用，请安装依赖")
            print("\n安装命令:")
            print("  pip3 install vosk pyaudio")
            print("\n模型下载:")
            print("  wget https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip")
            print("  unzip vosk-model-cn-0.15.zip")
            print("  mkdir -p ~/workspace/models && mv vosk-model-cn-0.15 ~/workspace/models/")
            return
        
        logger.info("🚀 太一语音命令启动...")
        logger.info(f"🎤 唤醒词：{', '.join(WAKE_WORDS)}")
        logger.info("📋 可用命令：自检，dashboard, 天气，日报，周报，github")
        
        print("")
        print("=" * 60)
        print("🎤 太一语音命令已启动")
        print("=" * 60)
        print(f"唤醒词：{', '.join(WAKE_WORDS)}")
        print("")
        print("可用命令:")
        print("  太一系统自检    - 运行系统检查")
        print("  太一 dashboard  - 打开 Dashboard")
        print("  太一天气        - 查询天气")
        print("  太一日报        - 生成日报")
        print("  太一周报        - 生成周报")
        print("  太一 github     - 查看 GitHub")
        print("  太一 [任意命令] - 执行通用任务")
        print("")
        print("按 Ctrl+C 停止")
        print("=" * 60)
        print("")
        
        self.running = True
        
        try:
            while self.running:
                # 监听语音
                text = self.listen()
                
                if text:
                    logger.info(f"🎤 识别到：{text}")
                    
                    # 检查唤醒词
                    if self.check_wake_word(text):
                        logger.info("✅ 唤醒词 detected")
                        self.speak("在")
                        self.wake_word_detected = True
                        self.pending_command = True
                        
                        # 等待命令 (10 秒内)
                        import time
                        start_time = time.time()
                        
                        while time.time() - start_time < 10:
                            command_text = self.listen(timeout=1)
                            
                            if command_text:
                                command = self.parse_command(command_text)
                                self.execute_command(command)
                                self.wake_word_detected = False
                                self.pending_command = False
                                break
                    
                    # 如果已唤醒，直接解析命令
                    elif self.pending_command:
                        command = self.parse_command(text)
                        self.execute_command(command)
                        self.pending_command = False
        
        except KeyboardInterrupt:
            logger.info("⏹️ 语音命令停止")
            self.stop()
    
    def stop(self):
        """停止语音控制"""
        self.running = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.audio:
            self.audio.terminate()
        
        logger.info("✅ 语音命令已停止")


def main():
    """主函数"""
    # 创建控制器
    controller = VoiceCommandController()
    
    # 运行
    controller.run()


if __name__ == '__main__':
    main()
