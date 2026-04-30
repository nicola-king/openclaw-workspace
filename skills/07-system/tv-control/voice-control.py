#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音控制电视
唤醒词："电视" 或 "太一"
命令："开机" "关机" "增加音量" "减少音量" "静音" 等
"""

import os
import sys
import logging
import json
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    VOSK_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Vosk 未安装：{e}")
    print("安装命令：pip3 install vosk pyaudio")
    VOSK_AVAILABLE = False

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/voice-control.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('VoiceControl')

# 语音命令映射
COMMAND_MAP = {
    # 开机
    "开机": "on",
    "打开电视": "on",
    "启动电视": "on",
    
    # 关机
    "关机": "off",
    "关闭电视": "off",
    "关掉电视": "off",
    
    # 音量控制
    "增加音量": "vol+",
    "音量加大": "vol+",
    "音量大一点": "vol+",
    "减少音量": "vol-",
    "音量减小": "vol-",
    "音量小一点": "vol-",
    "静音": "mute",
    "取消静音": "vol+",
    
    # 频道控制
    "下一个频道": "ch+",
    "频道加": "ch+",
    "上一个频道": "ch-",
    "频道减": "ch-",
    
    # 状态查询
    "什么状态": "status",
    "电视状态": "status",
    "状态": "status",
}

# 唤醒词
WAKE_WORDS = ["电视", "太一"]

class VoiceController:
    """语音控制器"""
    
    def __init__(self, model_path="models/vosk-model-cn-0.15"):
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.audio = None
        self.stream = None
        self.wake_word_detected = False
        self.running = False
        
        # 初始化语音识别
        if VOSK_AVAILABLE:
            self._init_vosk()
    
    def _init_vosk(self):
        """初始化 Vosk"""
        try:
            # 检查模型是否存在
            if not os.path.exists(self.model_path):
                logger.error(f"❌ 语音模型不存在：{self.model_path}")
                logger.info("请下载模型：wget https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip")
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
    
    def listen(self, timeout=5):
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
    
    def check_wake_word(self, text):
        """检查唤醒词"""
        for wake_word in WAKE_WORDS:
            if wake_word in text:
                logger.info(f"✅ 唤醒词检测：{wake_word}")
                return True
        return False
    
    def parse_command(self, text):
        """解析语音命令"""
        # 移除唤醒词
        for wake_word in WAKE_WORDS:
            text = text.replace(wake_word, '').strip()
        
        # 匹配命令
        for command_text, command_code in COMMAND_MAP.items():
            if command_text in text:
                logger.info(f"✅ 命令匹配：{command_text} -> {command_code}")
                return command_code
        
        logger.warning(f"⚠️ 未识别命令：{text}")
        return None
    
    def execute_command(self, command_code):
        """执行命令"""
        if not command_code:
            return
        
        logger.info(f"🔧 执行命令：{command_code}")
        
        # 调用电视控制
        try:
            from tools.cec import CECController
            from tools.audio import AudioController
            
            cec = CECController()
            audio = AudioController()
            
            if command_code == 'on':
                cec.power_on()
                self.speak("好的，正在打开电视")
            elif command_code == 'off':
                cec.power_off()
                self.speak("好的，正在关闭电视")
            elif command_code == 'vol+':
                audio.volume_up()
                self.speak("好的，增加音量")
            elif command_code == 'vol-':
                audio.volume_down()
                self.speak("好的，减少音量")
            elif command_code == 'mute':
                audio.mute()
                self.speak("好的，静音")
            elif command_code == 'ch+':
                cec.channel_up()
                self.speak("好的，下一个频道")
            elif command_code == 'ch-':
                cec.channel_down()
                self.speak("好的，上一个频道")
            elif command_code == 'status':
                self.speak("电视状态正常")
        
        except Exception as e:
            logger.error(f"❌ 执行失败：{e}")
            self.speak("对不起，执行失败")
    
    def speak(self, text):
        """语音反馈 (TTS)"""
        logger.info(f"🔊 语音反馈：{text}")
        
        # 使用系统 TTS (如果有)
        try:
            import subprocess
            subprocess.run(['espeak', '-v', 'zh', text], timeout=10)
        except Exception:
            # 如没有 espeak，仅日志
            pass
    
    def run(self):
        """运行语音控制"""
        if not VOSK_AVAILABLE:
            logger.error("❌ Vosk 不可用，请安装依赖")
            return
        
        logger.info("🚀 语音控制启动...")
        logger.info(f"🎤 唤醒词：{', '.join(WAKE_WORDS)}")
        logger.info("📋 可用命令：开机，关机，增加音量，减少音量，静音")
        print("")
        print("=" * 50)
        print("🎤 语音控制电视已启动")
        print("=" * 50)
        print(f"唤醒词：{', '.join(WAKE_WORDS)}")
        print("命令：开机，关机，增加音量，减少音量，静音")
        print("按 Ctrl+C 停止")
        print("=" * 50)
        print("")
        
        self.running = True
        
        try:
            while self.running:
                # 监听语音
                text = self.listen()
                
                if text:
                    # 检查唤醒词
                    if self.check_wake_word(text):
                        self.speak("在")
                        self.wake_word_detected = True
                        
                        # 等待命令 (5 秒内)
                        import time
                        start_time = time.time()
                        
                        while time.time() - start_time < 5:
                            command_text = self.listen(timeout=1)
                            
                            if command_text:
                                command_code = self.parse_command(command_text)
                                self.execute_command(command_code)
                                self.wake_word_detected = False
                                break
                    
                    # 如果已唤醒，直接解析命令
                    elif self.wake_word_detected:
                        command_code = self.parse_command(text)
                        self.execute_command(command_code)
                        self.wake_word_detected = False
        
        except KeyboardInterrupt:
            logger.info("⏹️ 语音控制停止")
            self.stop()
    
    def stop(self):
        """停止语音控制"""
        self.running = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.audio:
            self.audio.terminate()
        
        logger.info("✅ 语音控制已停止")

def main():
    """主函数"""
    # 创建控制器
    controller = VoiceController()
    
    # 运行
    controller.run()

if __name__ == '__main__':
    main()
