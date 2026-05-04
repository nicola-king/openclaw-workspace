#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一飞书集成核心类
采用系统内部信息，不依赖外部API
"""

import json
import time
import hashlib
import base64
import hmac
import requests
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FeishuMessage:
    """飞书消息数据类"""
    msg_type: str  # text, markdown, card, image, file
    content: Dict
    chat_id: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class FeishuCommand:
    """飞书指令数据类"""
    command: str
    args: List[str]
    user_id: str
    chat_id: str
    message_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class FeishuIntegration:
    """
    太一飞书集成类
    
    采用系统内部信息架构:
    - 不依赖外部API
    - 直接读取系统状态
    - 推送内部任务结果
    """
    
    def __init__(self, config_path: str = "config/feishu.yaml"):
        self.config = self._load_config(config_path)
        self.webhook_url = self.config.get("webhook_url", "")
        self.app_id = self.config.get("app_id", "")
        self.app_secret = self.config.get("app_secret", "")
        self.default_chat_id = self.config.get("default_chat_id", "")
        self.admin_open_id = self.config.get("admin_open_id", "")
        
        # 指令路由表
        self.command_handlers: Dict[str, Callable] = {}
        
        # 消息历史
        self.message_history: List[FeishuMessage] = []
        
        logger.info("✅ 飞书集成初始化完成")
    
    def _load_config(self, path: str) -> Dict:
        """加载配置"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"⚠️ 配置文件不存在: {path}，使用默认配置")
            return self._default_config()
        except json.JSONDecodeError:
            logger.warning(f"⚠️ 配置文件格式错误: {path}，使用默认配置")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "webhook_url": "",
            "app_id": "",
            "app_secret": "",
            "default_chat_id": "",
            "admin_open_id": "",
            "message_limit": 1000
        }
    
    # ==================== 消息推送 ====================
    
    def send_text(self, text: str, chat_id: Optional[str] = None) -> bool:
        """
        发送文本消息
        
        Args:
            text: 消息内容
            chat_id: 目标群ID，默认使用配置中的default_chat_id
        
        Returns:
            bool: 是否发送成功
        """
        target = chat_id or self.default_chat_id
        if not target:
            logger.error("❌ 未指定chat_id")
            return False
        
        message = {
            "msg_type": "text",
            "content": {"text": text}
        }
        
        return self._send_message(message, target)
    
    def send_markdown(self, markdown: str, chat_id: Optional[str] = None) -> bool:
        """
        发送Markdown消息
        
        Args:
            markdown: Markdown格式内容
            chat_id: 目标群ID
        
        Returns:
            bool: 是否发送成功
        """
        target = chat_id or self.default_chat_id
        if not target:
            logger.error("❌ 未指定chat_id")
            return False
        
        message = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": markdown
                        }
                    }
                ]
            }
        }
        
        return self._send_message(message, target)
    
    def send_card(self, card: Dict, chat_id: Optional[str] = None) -> bool:
        """
        发送卡片消息
        
        Args:
            card: 卡片内容
            chat_id: 目标群ID
        
        Returns:
            bool: 是否发送成功
        """
        target = chat_id or self.default_chat_id
        if not target:
            logger.error("❌ 未指定chat_id")
            return False
        
        message = {
            "msg_type": "interactive",
            "card": card
        }
        
        return self._send_message(message, target)
    
    def _send_message(self, message: Dict, chat_id: str) -> bool:
        """
        发送消息到飞书
        
        采用系统内部信息架构:
        - 如果配置了webhook_url，使用webhook推送
        - 否则记录到本地日志
        """
        if not self.webhook_url:
            # 系统内部模式：记录到日志
            logger.info(f"📨 [飞书消息] Chat: {chat_id}")
            logger.info(f"   内容: {json.dumps(message, ensure_ascii=False)[:200]}...")
            
            # 保存到消息历史
            self.message_history.append(FeishuMessage(
                msg_type=message.get("msg_type", "unknown"),
                content=message,
                chat_id=chat_id
            ))
            
            return True
        
        try:
            # 使用webhook推送
            response = requests.post(
                self.webhook_url,
                json=message,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    logger.info(f"✅ 消息发送成功: {chat_id}")
                    return True
                else:
                    logger.error(f"❌ 消息发送失败: {result.get('msg')}")
                    return False
            else:
                logger.error(f"❌ HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 发送异常: {e}")
            return False
    
    # ==================== 系统内部信息推送 ====================
    
    def push_system_status(self, status: Dict, chat_id: Optional[str] = None):
        """
        推送系统状态
        
        Args:
            status: 系统状态字典
            chat_id: 目标群ID
        """
        markdown = f"""# 🤖 太一系统状态

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 系统资源
- **CPU**: {status.get('cpu', 'N/A')}%
- **内存**: {status.get('memory', 'N/A')}%
- **磁盘**: {status.get('disk', 'N/A')}%
- **运行时间**: {status.get('uptime', 'N/A')}

## Agent状态
"""
        
        for agent_name, agent_status in status.get('agents', {}).items():
            emoji = "🟢" if agent_status.get('running') else "🔴"
            markdown += f"- {emoji} **{agent_name}**: {agent_status.get('status', '未知')}\n"
        
        markdown += f"""
## 任务队列
- **待处理**: {status.get('pending_tasks', 0)}
- **执行中**: {status.get('running_tasks', 0)}
- **已完成**: {status.get('completed_tasks', 0)}
"""
        
        self.send_markdown(markdown, chat_id)
    
    def push_task_completion(self, task: Dict, chat_id: Optional[str] = None):
        """
        推送任务完成通知
        
        Args:
            task: 任务信息字典
            chat_id: 目标群ID
        """
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "✅ 任务完成"},
                "template": "green"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**任务**: {task.get('name', '未知')}\n**耗时**: {task.get('duration', 'N/A')}s\n**结果**: {task.get('result', '成功')}"
                    }
                }
            ]
        }
        
        if task.get('details'):
            card["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**详情**: {task['details']}"
                }
            })
        
        self.send_card(card, chat_id)
    
    def push_alert(self, alert: Dict, chat_id: Optional[str] = None):
        """
        推送告警信息
        
        Args:
            alert: 告警信息字典
            chat_id: 目标群ID
        """
        level = alert.get('level', 'warning')
        level_colors = {
            'info': 'blue',
            'warning': 'yellow',
            'error': 'red',
            'critical': 'red'
        }
        
        level_emojis = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'critical': '🚨'
        }
        
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{level_emojis.get(level, '⚠️')} 系统告警"
                },
                "template": level_colors.get(level, 'yellow')
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**类型**: {alert.get('type', '未知')}\n**级别**: {level.upper()}\n**消息**: {alert.get('message', '')}"
                    }
                }
            ]
        }
        
        if alert.get('suggestion'):
            card["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**建议**: {alert['suggestion']}"
                }
            })
        
        self.send_card(card, chat_id)
    
    def push_daily_report(self, report: Dict, chat_id: Optional[str] = None):
        """
        推送日报
        
        Args:
            report: 日报数据字典
            chat_id: 目标群ID
        """
        markdown = f"""# 📊 太一日报

**日期**: {report.get('date', datetime.now().strftime('%Y-%m-%d'))}

## 今日完成
"""
        
        for item in report.get('completed', []):
            markdown += f"- ✅ {item}\n"
        
        markdown += "\n## 进行中\n"
        for item in report.get('in_progress', []):
            markdown += f"- 🔄 {item}\n"
        
        markdown += "\n## 待处理\n"
        for item in report.get('pending', []):
            markdown += f"- ⏳ {item}\n"
        
        markdown += f"""
## 统计
- **完成任务**: {len(report.get('completed', []))}
- **进行中**: {len(report.get('in_progress', []))}
- **待处理**: {len(report.get('pending', []))}
"""
        
        self.send_markdown(markdown, chat_id)
    
    # ==================== 指令路由 ====================
    
    def register_command(self, command: str, handler: Callable):
        """
        注册指令处理器
        
        Args:
            command: 指令名称 (如 "/汇率")
            handler: 处理函数
        """
        self.command_handlers[command] = handler
        logger.info(f"✅ 注册指令: {command}")
    
    def handle_command(self, command: FeishuCommand) -> str:
        """
        处理飞书指令
        
        Args:
            command: 指令对象
        
        Returns:
            str: 处理结果
        """
        handler = self.command_handlers.get(command.command)
        
        if handler:
            try:
                result = handler(command.args)
                return result
            except Exception as e:
                logger.error(f"❌ 指令处理异常: {e}")
                return f"❌ 处理失败: {str(e)}"
        else:
            return f"❌ 未知指令: {command.command}\n可用指令: {', '.join(self.command_handlers.keys())}"
    
    # ==================== 系统内部信息读取 ====================
    
    def get_system_status(self) -> Dict:
        """
        获取系统内部状态
        
        Returns:
            Dict: 系统状态信息
        """
        import psutil
        
        # CPU信息
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 内存信息
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # 磁盘信息
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        
        # 启动时间
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return {
            "cpu": round(cpu_percent, 1),
            "memory": round(memory_percent, 1),
            "disk": round(disk_percent, 1),
            "uptime": str(uptime).split('.')[0],
            "timestamp": datetime.now().isoformat()
        }
    
    def get_agent_status(self) -> Dict:
        """
        获取Agent状态
        
        Returns:
            Dict: Agent状态信息
        """
        # 这里读取系统内部Agent状态
        # 实际实现中会从各Agent获取状态
        return {
            "cross_border_trade": {
                "running": True,
                "status": "运行中",
                "tasks_completed": 156
            },
            "travel_explorer": {
                "running": True,
                "status": "运行中",
                "tasks_completed": 89
            },
            "maigret": {
                "running": False,
                "status": "待机",
                "tasks_completed": 45
            },
            "moss_tts": {
                "running": True,
                "status": "运行中",
                "tasks_completed": 234
            }
        }
    
    # ==================== 工具方法 ====================
    
    def get_message_history(self, limit: int = 100) -> List[FeishuMessage]:
        """
        获取消息历史
        
        Args:
            limit: 返回数量限制
        
        Returns:
            List[FeishuMessage]: 消息列表
        """
        return self.message_history[-limit:]
    
    def clear_history(self):
        """清空消息历史"""
        self.message_history.clear()
        logger.info("✅ 消息历史已清空")


# ==================== 便捷函数 ====================

def get_feishu_integration() -> FeishuIntegration:
    """获取飞书集成实例 (单例)"""
    if not hasattr(get_feishu_integration, "_instance"):
        get_feishu_integration._instance = FeishuIntegration()
    return get_feishu_integration._instance


def send_system_status(chat_id: Optional[str] = None):
    """便捷函数: 发送系统状态"""
    feishu = get_feishu_integration()
    status = feishu.get_system_status()
    status["agents"] = feishu.get_agent_status()
    feishu.push_system_status(status, chat_id)


def send_task_completion(task_name: str, duration: float, result: str, chat_id: Optional[str] = None):
    """便捷函数: 发送任务完成通知"""
    feishu = get_feishu_integration()
    feishu.push_task_completion({
        "name": task_name,
        "duration": duration,
        "result": result
    }, chat_id)


def send_alert(alert_type: str, level: str, message: str, suggestion: str = "", chat_id: Optional[str] = None):
    """便捷函数: 发送告警"""
    feishu = get_feishu_integration()
    feishu.push_alert({
        "type": alert_type,
        "level": level,
        "message": message,
        "suggestion": suggestion
    }, chat_id)


# ==================== 测试 ====================

if __name__ == "__main__":
    print("🚀 太一飞书集成测试")
    
    # 初始化
    feishu = FeishuIntegration()
    
    # 测试1: 发送文本消息
    print("\n📨 测试1: 发送文本消息")
    feishu.send_text("太一系统启动完成 ✅")
    
    # 测试2: 发送Markdown
    print("\n📨 测试2: 发送Markdown")
    feishu.send_markdown("""
# 系统状态

- CPU: 45%
- 内存: 60%
- 磁盘: 30%
""")
    
    # 测试3: 推送系统状态
    print("\n📨 测试3: 推送系统状态")
    status = feishu.get_system_status()
    status["agents"] = feishu.get_agent_status()
    feishu.push_system_status(status)
    
    # 测试4: 推送任务完成
    print("\n📨 测试4: 推送任务完成")
    feishu.push_task_completion({
        "name": "跨境贸易选品分析",
        "duration": 2.3,
        "result": "成功",
        "details": "找到3个高潜力产品"
    })
    
    # 测试5: 推送告警
    print("\n📨 测试5: 推送告警")
    feishu.push_alert({
        "type": "资源不足",
        "level": "warning",
        "message": "磁盘空间不足80%",
        "suggestion": "建议清理日志文件"
    })
    
    # 测试6: 推送日报
    print("\n📨 测试6: 推送日报")
    feishu.push_daily_report({
        "date": "2026-05-04",
        "completed": [
            "跨境贸易Agent迁移完成",
            "旅游探路者部署完成",
            "反爬对抗工具包创建"
        ],
        "in_progress": [
            "Maigret OSINT工具安装",
            "MOSS-TTS语音合成测试"
        ],
        "pending": [
            "OpenClaw Gateway Skill注册",
            "系统监控配置"
        ]
    })
    
    print("\n✅ 所有测试完成")
    print(f"📊 消息历史: {len(feishu.get_message_history())} 条")
