#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 群聊对话自进化智能体 v2.0

功能:
1. 条件触发 (对话失败/无响应时触发)
2. 自动自愈 (重试/切换话题)
3. 学习能力 (分析对话效果)
4. 知识固化 (写入 PITFALLS.md)
5. @触发响应

作者：太一 AGI
创建：2026-04-23
版本：v2.0 (自进化智能体)
"""

import sys
from pathlib import Path

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
sys.path.insert(0, str(WORKSPACE / "skills" / "07-system"))
from self_evolving_task_base import SelfEvolvingTask, TaskResult

from telegram_smart_dialogue import TelegramSmartDialogue

class TelegramDialogueSelfEvolving(SelfEvolvingTask):
    """Telegram 群聊对话自进化智能体"""
    
    def __init__(self):
        super().__init__("telegram_dialogue")
        self.dialogue = TelegramSmartDialogue()
    
    def check(self) -> TaskResult:
        """条件检查 - 对话系统是否正常"""
        try:
            # 检查话题库
            if not self.dialogue.topics:
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error='话题库为空'
                )
            
            # 检查 Bot 列表
            if not self.dialogue.bot_evolution:
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error='Bot 列表为空'
                )
            
            # 检查最近活动
            status = self.dialogue.get_status()
            if status['total_messages'] == 0:
                return TaskResult(
                    task_id=self.task_id,
                    success=True,
                    need_heal=True,
                    error='对话系统未激活'
                )
            
            return TaskResult(
                task_id=self.task_id,
                success=True,
                need_heal=False,
                error=None
            )
            
        except Exception as e:
            return TaskResult(
                task_id=self.task_id,
                success=False,
                need_heal=True,
                error=f'检查失败：{str(e)}'
            )
    
    def heal(self, error: str) -> bool:
        """自动自愈 - 启动/恢复对话"""
        try:
            if '话题库为空' in error:
                # 重新加载默认话题
                self.dialogue.topics = self.dialogue.load_topics()
                return len(self.dialogue.topics) > 0
            
            elif 'Bot 列表为空' in error:
                # 重新加载 Bot 列表
                self.dialogue.bot_evolution = self.dialogue.load_bot_evolution()
                return len(self.dialogue.bot_evolution) > 0
            
            elif '未激活' in error:
                # 启动对话
                message_id = self.dialogue.start_random_dialogue()
                return message_id is not None
            
            else:
                return False
                
        except Exception as e:
            print(f"自愈失败：{str(e)}")
            return False

if __name__ == '__main__':
    agent = TelegramDialogueSelfEvolving()
    result = agent.execute()
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"💬 Telegram 群聊对话自进化智能体 v2.0")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"")
    print(f"执行结果：{'✅ 成功' if result.success else '❌ 失败'}")
    print(f"需要自愈：{'🔧 是' if result.need_heal else '❌ 否'}")
    if result.error:
        print(f"错误信息：{result.error}")
    print(f"")
    print(f"进化指标:")
    print(f"  总运行次数：{agent.metrics.total_runs}")
    print(f"  发现问题：{agent.metrics.issues_found}")
    print(f"  自愈成功：{agent.metrics.auto_healed}")
    print(f"  成功率：{agent.metrics.success_rate:.1f}%")
    print(f"")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
