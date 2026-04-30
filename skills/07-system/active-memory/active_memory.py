#!/usr/bin/env python3
"""
🧠 Active Memory (主动记忆) 插件

OpenClaw 4.10 核心功能集成
主回复前自动检索记忆/偏好/上下文

作者：太一 AGI
创建：2026-04-11
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ActiveMemory:
    """主动记忆插件"""
    
    def __init__(self, config_path: str = None):
        """初始化主动记忆"""
        self.config_path = config_path or "/home/nicola/.openclaw/workspace/config/active-memory/config.json"
        self.config = self._load_config()
        self.memory_palace = self._init_memory_palace()
        
        print("🧠 Active Memory (主动记忆) 已初始化")
        print(f"   模式：{self.config.get('mode', 'auto')}")
        print(f"   上下文：{self.config.get('context_mode', 'full')}")
        print()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_file = Path(self.config_path)
        if not config_file.exists():
            # 创建默认配置
            default_config = {
                "enabled": True,
                "mode": "auto",  # auto/manual
                "context_mode": "full",  # message/recent/full
                "verbose": False,
                "persist_transcript": True,
                "prompt_override": None,
                "thinking_override": None
            }
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _init_memory_palace(self):
        """初始化记忆宫殿"""
        try:
            import sys
            sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/taiyi-memory-palace')
            from memory_system_v2 import TaiyiMemoryPalaceV2
            return TaiyiMemoryPalaceV2()
        except Exception as e:
            print(f"⚠️  记忆宫殿初始化失败：{e}")
            return None
    
    def pre_reply_hook(self, context: Dict) -> Dict:
        """
        主回复前钩子 - OpenClaw 4.10 核心功能
        
        在回复前自动检索：
        - 用户偏好
        - 相关上下文
        - 历史记忆
        
        Args:
            context: 当前对话上下文
        
        Returns:
            融合后的记忆上下文
        """
        print("🧠 Active Memory: 主回复前检索...")
        
        if not self.config.get('enabled', True):
            print("   ⚠️  Active Memory 已禁用")
            return context
        
        # 1. 检索用户偏好
        preferences = self._retrieve_preferences(context)
        
        # 2. 检索相关上下文
        recent_context = self._retrieve_recent_context(context)
        
        # 3. 检索历史记忆
        history = self._retrieve_relevant_history(context)
        
        # 4. 融合记忆
        fused_memory = self._fuse_memories(preferences, recent_context, history)
        
        # 5. 注入上下文
        enhanced_context = self._inject_memory(context, fused_memory)
        
        if self.config.get('verbose', False):
            print(f"   ✅ 检索到 {len(fused_memory)} 条记忆")
            print(f"   - 偏好：{len(preferences)} 条")
            print(f"   - 上下文：{len(recent_context)} 条")
            print(f"   - 历史：{len(history)} 条")
        
        return enhanced_context
    
    def _retrieve_preferences(self, context: Dict) -> List[Dict]:
        """检索用户偏好"""
        preferences = []
        
        # 从记忆宫殿检索
        if self.memory_palace:
            results = self.memory_palace.search("偏好 设置 喜欢", category="identity", limit=5)
            preferences.extend(results)
        
        # 从配置检索
        user_prefs = self.config.get('user_preferences', {})
        if user_prefs:
            preferences.append({"type": "preference", "data": user_prefs})
        
        return preferences
    
    def _retrieve_recent_context(self, context: Dict) -> List[Dict]:
        """检索相关上下文"""
        recent = []
        
        # 从记忆宫殿检索
        if self.memory_palace:
            results = self.memory_palace.search("最近 上下文 对话", category="conversations", limit=10)
            recent.extend(results)
        
        return recent
    
    def _retrieve_relevant_history(self, context: Dict) -> List[Dict]:
        """检索历史记忆"""
        history = []
        
        # 从记忆宫殿检索
        if self.memory_palace:
            query = context.get('query', '')
            results = self.memory_palace.search(query, category="learning", limit=5)
            history.extend(results)
        
        return history
    
    def _fuse_memories(self, preferences: List, recent: List, history: List) -> Dict:
        """融合记忆"""
        return {
            "preferences": preferences,
            "recent_context": recent,
            "history": history,
            "fused_at": datetime.now().isoformat()
        }
    
    def _inject_memory(self, context: Dict, fused_memory: Dict) -> Dict:
        """注入记忆到上下文"""
        # 增强上下文
        context['active_memory'] = fused_memory
        
        # 添加系统提示
        if 'system_prompt' not in context:
            context['system_prompt'] = ""
        
        memory_hint = self._generate_memory_hint(fused_memory)
        context['system_prompt'] += f"\n\n{memory_hint}"
        
        return context
    
    def _generate_memory_hint(self, fused_memory: Dict) -> str:
        """生成记忆提示"""
        hints = []
        
        if fused_memory['preferences']:
            hints.append("已知用户偏好:")
            for pref in fused_memory['preferences']:
                if 'data' in pref:
                    hints.append(f"- {pref['data']}")
        
        if fused_memory['history']:
            hints.append("\n相关历史记忆:")
            for hist in fused_memory['history'][:3]:
                if 'text' in hist:
                    hints.append(f"- {hist['text'][:100]}...")
        
        return "\n".join(hints)
    
    def log_transcript(self, context: Dict, reply: str):
        """记录转录 (用于调试)"""
        if not self.config.get('persist_transcript', False):
            return
        
        log_dir = Path("/home/nicola/.openclaw/workspace/logs/active-memory")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"transcript-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        transcript = {
            "context": context,
            "reply": reply,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)
        
        print(f"   📝 转录已记录：{log_file}")
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "enabled": self.config.get('enabled', True),
            "mode": self.config.get('mode', 'auto'),
            "context_mode": self.config.get('context_mode', 'full'),
            "verbose": self.config.get('verbose', False),
            "memory_palace": "connected" if self.memory_palace else "disconnected"
        }


def main():
    """主函数 - 测试"""
    print("="*60)
    print("🧠 Active Memory (主动记忆) 测试")
    print("="*60)
    
    # 初始化
    memory = ActiveMemory()
    
    # 测试检索
    print("\n1. 测试主动检索...")
    context = {
        "query": "今天天气怎么样",
        "user_id": "7073481596",
        "channel": "telegram"
    }
    
    enhanced = memory.pre_reply_hook(context)
    
    # 获取统计
    print("\n2. 获取统计...")
    stats = memory.get_statistics()
    print(f"   已启用：{stats['enabled']}")
    print(f"   模式：{stats['mode']}")
    print(f"   上下文：{stats['context_mode']}")
    print(f"   记忆宫殿：{stats['memory_palace']}")
    
    print("\n✅ Active Memory 测试完成!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
