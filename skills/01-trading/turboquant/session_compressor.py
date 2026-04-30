#!/usr/bin/env python3
"""
Session Context Auto-Compressor
实现 context>80K 自动压缩集成

功能：
1. 监控 session context 大小
2. 自动触发压缩（80K 建议，100K 强制）
3. 无感知压缩（用户无中断）
4. 生成 memory 文件

集成点：
- OpenClaw session 管理模块
- TurboQuant compressor.py
- memory 文件系统
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass

# 导入 TurboQuant 压缩器
sys.path.insert(0, str(Path(__file__).parent))
from compressor import TurboQuantCompressor, CompressedConversation


@dataclass
class CompressionTrigger:
    """压缩触发条件"""
    threshold_suggest: int = 80000   # 80K 建议压缩
    threshold_force: int = 100000    # 100K 强制压缩
    check_interval: int = 60         # 检查间隔（秒）


@dataclass
class CompressionResult:
    """压缩结果"""
    success: bool
    triggered_at: str
    original_size: int
    compressed_size: int
    compression_ratio: float
    memory_file: str
    message: str


class SessionContextMonitor:
    """
    Session Context 监控器
    
    职责：
    1. 跟踪当前 session 的 context 大小
    2. 检测是否达到压缩阈值
    3. 触发自动压缩
    4. 管理压缩状态
    """
    
    def __init__(self, workspace_root: str = None):
        """
        初始化监控器
        
        Args:
            workspace_root: 工作区根目录（默认 ~/.openclaw/workspace）
        """
        if workspace_root is None:
            workspace_root = str(Path.home() / '.openclaw' / 'workspace')
        
        self.workspace_root = Path(workspace_root)
        self.memory_dir = self.workspace_root / 'memory'
        self.state_file = self.memory_dir / 'compression-state.json'
        
        # 确保目录存在
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化压缩器
        self.compressor = TurboQuantCompressor()
        
        # 触发阈值
        self.trigger = CompressionTrigger()
        
        # 当前 context 大小（tokens 近似为字符数）
        self.current_context_size = 0
        
        # 压缩历史
        self.compression_history = []
        
        # 加载状态
        self._load_state()
    
    def _load_state(self):
        """加载压缩状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.compression_history = state.get('history', [])
                    self.current_context_size = state.get('last_context_size', 0)
            except Exception as e:
                print(f"[session-compressor] 加载状态失败：{e}")
                self.compression_history = []
    
    def _save_state(self):
        """保存压缩状态"""
        state = {
            'history': self.compression_history[-100:],  # 保留最近 100 次
            'last_context_size': self.current_context_size,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[session-compressor] 保存状态失败：{e}")
    
    def update_context_size(self, size: int):
        """
        更新当前 context 大小
        
        Args:
            size: context 大小（字符数）
        """
        self.current_context_size = size
        self._save_state()
    
    def check_threshold(self) -> Optional[str]:
        """
        检查是否达到压缩阈值
        
        Returns:
            Optional[str]: 触发类型（'suggest'/'force'/None）
        """
        if self.current_context_size >= self.trigger.threshold_force:
            return 'force'
        elif self.current_context_size >= self.trigger.threshold_suggest:
            return 'suggest'
        return None
    
    def compress_and_save(
        self, 
        conversation: str, 
        session_id: str = None,
        force: bool = False
    ) -> CompressionResult:
        """
        压缩对话并保存到 memory
        
        Args:
            conversation: 原始对话文本
            session_id: Session ID（可选）
            force: 是否强制压缩（忽略阈值）
            
        Returns:
            CompressionResult: 压缩结果
        """
        triggered_at = datetime.now()
        
        # 检查是否需要压缩
        if not force:
            trigger_type = self.check_threshold()
            if trigger_type is None:
                return CompressionResult(
                    success=False,
                    triggered_at=triggered_at.isoformat(),
                    original_size=len(conversation),
                    compressed_size=0,
                    compression_ratio=0,
                    memory_file='',
                    message='未达到压缩阈值'
                )
        
        # 执行压缩
        try:
            compressed = self.compressor.compress(conversation)
            stats = self.compressor.get_compression_stats(conversation, compressed)
            
            # 生成 memory 文件名
            date_str = triggered_at.strftime('%Y-%m-%d')
            time_str = triggered_at.strftime('%H%M%S')
            
            if session_id:
                # 使用 session ID 生成唯一文件名
                session_hash = hashlib.md5(session_id.encode()).hexdigest()[:8]
                memory_filename = f'{date_str}-{time_str}-session-{session_hash}.md'
            else:
                memory_filename = f'{date_str}-{time_str}-compressed.md'
            
            memory_path = self.memory_dir / memory_filename
            
            # 生成 memory 文件内容
            memory_content = self._generate_memory_content(
                compressed, stats, triggered_at, session_id
            )
            
            # 写入文件
            with open(memory_path, 'w', encoding='utf-8') as f:
                f.write(memory_content)
            
            # 更新 context 大小
            self.current_context_size = stats['compressed_size']
            
            # 记录压缩历史
            self.compression_history.append({
                'timestamp': triggered_at.isoformat(),
                'original_size': stats['original_size'],
                'compressed_size': stats['compressed_size'],
                'compression_ratio': stats['compression_ratio'],
                'memory_file': str(memory_path),
                'session_id': session_id,
                'trigger_type': 'force' if force else self.check_threshold()
            })
            
            self._save_state()
            
            return CompressionResult(
                success=True,
                triggered_at=triggered_at.isoformat(),
                original_size=stats['original_size'],
                compressed_size=stats['compressed_size'],
                compression_ratio=stats['compression_ratio'],
                memory_file=str(memory_path),
                message=f'压缩完成：{stats["compression_ratio"]:.2f}x ({stats["original_size"]} → {stats["compressed_size"]} 字符)'
            )
            
        except Exception as e:
            return CompressionResult(
                success=False,
                triggered_at=triggered_at.isoformat(),
                original_size=len(conversation),
                compressed_size=0,
                compression_ratio=0,
                memory_file='',
                message=f'压缩失败：{e}'
            )
    
    def _generate_memory_content(
        self, 
        compressed: CompressedConversation,
        stats: dict,
        timestamp: datetime,
        session_id: str = None
    ) -> str:
        """
        生成 memory 文件内容
        
        Args:
            compressed: 压缩后的对话
            stats: 压缩统计
            timestamp: 时间戳
            session_id: Session ID
            
        Returns:
            str: Memory 文件内容
        """
        date_str = timestamp.strftime('%Y-%m-%d')
        time_str = timestamp.strftime('%H:%M:%S')
        
        content = []
        content.append(f"# Session 压缩记录 · {date_str} {time_str}")
        content.append("")
        content.append("## 元数据")
        content.append("")
        content.append(f"- **压缩时间**: {timestamp.isoformat()}")
        content.append(f"- **Session ID**: {session_id or 'N/A'}")
        content.append(f"- **原始大小**: {stats['original_size']:,} 字符")
        content.append(f"- **压缩后大小**: {stats['compressed_size']:,} 字符")
        content.append(f"- **压缩比**: {stats['compression_ratio']:.2f}x")
        content.append(f"- **核心占比**: {stats['core_percentage']:.1f}%")
        content.append(f"- **残差占比**: {stats['residual_percentage']:.1f}%")
        content.append("")
        content.append("## 核心内容")
        content.append("")
        
        # 解析核心内容（适配紧凑格式）
        try:
            core_data = json.loads(compressed.core)
            
            # 紧凑格式：{'v': [...], 'e': [...]}
            if 'v' in core_data and 'e' in core_data:
                vectors = core_data.get('v', [])
                entities = core_data.get('e', [])
                
                if vectors:
                    content.append("### 语义向量")
                    content.append("")
                    for v in vectors[:20]:
                        t = v.get('t', '?')
                        k = v.get('k', '')
                        p = v.get('p', 0)
                        type_map = {'d': '决策', 'c': '约束', 'a': '动作', 'i': '意图', 'e': '实体'}
                        type_name = type_map.get(t, '上下文')
                        content.append(f"- [{type_name}] {k} (位置 {p})")
                    content.append("")
                
                if entities:
                    content.append("### 实体")
                    content.append("")
                    for e in entities:
                        content.append(f"- {e}")
                    content.append("")
            else:
                # 旧格式：{'decisions': [], 'actions': [], ...}
                for category in ['decisions', 'actions', 'constraints', 'intents', 'entities', 'context']:
                    items = core_data.get(category, [])
                    if items:
                        content.append(f"### {category.upper()}")
                        content.append("")
                        for item in items:
                            content.append(f"- {item}")
                        content.append("")
        except Exception as e:
            content.append(f"```")
            content.append(compressed.core)
            content.append(f"```")
            content.append(f"(解析核心内容时出错：{e})")
            content.append("")
        
        content.append("## 残差标记")
        content.append("")
        if compressed.residual_markers:
            content.append(f"共 {len(compressed.residual_markers)} 处细节")
            content.append("")
            for i, marker in enumerate(compressed.residual_markers[:20]):
                # 适配紧凑格式：'p'=position, 't'=type, 'e'=entities
                pos = marker.get('p', marker.get('position', 0))
                typ = marker.get('t', marker.get('type', 'context'))
                entities = marker.get('e', marker.get('entities', []))
                
                detail = f"- [位置 {pos}] {typ}"
                if entities:
                    detail += f" → {', '.join(entities) if isinstance(entities, list) else entities}"
                content.append(detail)
            
            if len(compressed.residual_markers) > 20:
                content.append(f"- ... 还有 {len(compressed.residual_markers) - 20} 处")
        else:
            content.append("无残差标记")
        content.append("")
        
        content.append("## 元数据详情")
        content.append("")
        content.append(f"- **参与者**: {compressed.metadata.get('participant_count', 'N/A')} 人")
        content.append(f"- **行数**: {compressed.metadata.get('line_count', 'N/A')}")
        content.append(f"- **实体数**: {compressed.metadata.get('entity_count', 'N/A')}")
        content.append(f"- **语义密度**: {compressed.metadata.get('semantic_density', 0):.2f}")
        content.append(f"- **主题**: {', '.join(compressed.metadata.get('topics', []))}")
        content.append("")
        content.append(f"---")
        content.append("")
        content.append(f"*压缩文件：{compressed.reconstruction_hash}*")
        content.append(f"*归档时间：{timestamp.strftime('%Y-%m-%d %H:%M')}*")
        content.append("")
        
        return '\n'.join(content)
    
    def get_compression_report(self) -> dict:
        """
        获取压缩报告
        
        Returns:
            dict: 压缩统计报告
        """
        if not self.compression_history:
            return {
                'total_compressions': 0,
                'avg_compression_ratio': 0,
                'total_saved': 0,
                'last_compression': None
            }
        
        total_saved = sum(
            h['original_size'] - h['compressed_size'] 
            for h in self.compression_history
        )
        avg_ratio = sum(
            h['compression_ratio'] for h in self.compression_history
        ) / len(self.compression_history)
        
        return {
            'total_compressions': len(self.compression_history),
            'avg_compression_ratio': avg_ratio,
            'total_saved': total_saved,
            'last_compression': self.compression_history[-1] if self.compression_history else None,
            'current_context_size': self.current_context_size,
            'threshold_suggest': self.trigger.threshold_suggest,
            'threshold_force': self.trigger.threshold_force
        }


class AutoCompressionIntegration:
    """
    自动压缩集成模块
    
    与 OpenClaw session 管理模块集成：
    1. 在 session 启动时初始化监控器
    2. 在每次消息处理后检查 context 大小
    3. 达到阈值时自动触发压缩
    4. 压缩后通知用户（可选）
    """
    
    def __init__(self, workspace_root: str = None):
        """
        初始化集成模块
        
        Args:
            workspace_root: 工作区根目录
        """
        self.monitor = SessionContextMonitor(workspace_root)
        self.notification_callback = None
    
    def set_notification_callback(self, callback):
        """
        设置通知回调函数
        
        Args:
            callback: 函数 (message: str) -> None
        """
        self.notification_callback = callback
    
    def on_message_processed(self, message_text: str, session_id: str = None):
        """
        消息处理后的钩子函数
        
        在每次消息处理后调用，检查是否需要压缩
        
        Args:
            message_text: 消息文本
            session_id: Session ID
        """
        # 更新 context 大小（简单累加，实际应从 session 管理器获取）
        self.monitor.update_context_size(
            self.monitor.current_context_size + len(message_text)
        )
        
        # 检查阈值
        trigger_type = self.monitor.check_threshold()
        
        if trigger_type:
            # 触发压缩
            result = self.monitor.compress_and_save(
                message_text,  # 实际应传入完整对话历史
                session_id,
                force=(trigger_type == 'force')
            )
            
            if result.success and self.notification_callback:
                # 通知用户
                message = f"🗜️ Context 压缩完成\n\n"
                message += f"• 压缩比：{result.compression_ratio:.2f}x\n"
                message += f"• 节省：{result.original_size - result.compressed_size:,} 字符\n"
                message += f"• 文件：{Path(result.memory_file).name}"
                
                if trigger_type == 'force':
                    message += "\n\n⚠️ 已达到强制压缩阈值（100K），建议开启新对话"
                
                self.notification_callback(message)
    
    def manual_compress(self, conversation: str, session_id: str = None) -> CompressionResult:
        """
        手动触发压缩
        
        Args:
            conversation: 对话文本
            session_id: Session ID
            
        Returns:
            CompressionResult: 压缩结果
        """
        result = self.monitor.compress_and_save(conversation, session_id, force=True)
        
        if result.success and self.notification_callback:
            self.notification_callback(
                f"✅ 手动压缩完成\n\n"
                f"• 压缩比：{result.compression_ratio:.2f}x\n"
                f"• 文件：{Path(result.memory_file).name}"
            )
        
        return result
    
    def get_status(self) -> dict:
        """
        获取压缩状态
        
        Returns:
            dict: 状态信息
        """
        return self.monitor.get_compression_report()


# CLI 接口
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Session Context Auto-Compressor')
    parser.add_argument('--workspace', type=str, help='工作区根目录')
    parser.add_argument('--compress', type=str, help='压缩指定文件')
    parser.add_argument('--status', action='store_true', help='显示压缩状态')
    parser.add_argument('--session-id', type=str, help='Session ID')
    
    args = parser.parse_args()
    
    integration = AutoCompressionIntegration(args.workspace)
    
    if args.status:
        report = integration.get_status()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    elif args.compress:
        with open(args.compress, 'r', encoding='utf-8') as f:
            conversation = f.read()
        
        result = integration.manual_compress(conversation, args.session_id)
        print(json.dumps({
            'success': result.success,
            'message': result.message,
            'memory_file': result.memory_file
        }, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()
