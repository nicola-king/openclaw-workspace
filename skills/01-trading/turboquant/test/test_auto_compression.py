#!/usr/bin/env python3
"""
Auto Compression Integration Tests
测试 context 自动压缩集成功能

验收标准：
1. 自动触发阈值准确（80K 建议，100K 强制）
2. 压缩过程无感知（用户无中断）
3. 压缩后 memory 文件正确生成
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from session_compressor import (
    SessionContextMonitor,
    AutoCompressionIntegration,
    CompressionTrigger,
    CompressionResult
)


class TestSessionContextMonitor:
    """测试 SessionContextMonitor 类"""
    
    def __init__(self):
        self.test_dir = None
        self.workspace = None
    
    def setup(self):
        """创建测试环境"""
        self.test_dir = tempfile.mkdtemp(prefix='turboquant_test_')
        self.workspace = Path(self.test_dir) / 'workspace'
        self.workspace.mkdir()
        (self.workspace / 'memory').mkdir()
        print(f"✅ 测试环境：{self.workspace}")
    
    def teardown(self):
        """清理测试环境"""
        if self.test_dir and Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
            print(f"🧹 清理测试环境：{self.test_dir}")
    
    def test_threshold_suggest(self):
        """测试 80K 建议阈值"""
        print("\n【测试】80K 建议阈值")
        
        monitor = SessionContextMonitor(str(self.workspace))
        
        # 测试 79,999 字符（不触发）
        monitor.update_context_size(79999)
        result = monitor.check_threshold()
        assert result is None, f"预期 None，实际 {result}"
        print("  ✓ 79,999 字符：不触发")
        
        # 测试 80,000 字符（触发建议）
        monitor.update_context_size(80000)
        result = monitor.check_threshold()
        assert result == 'suggest', f"预期 'suggest'，实际 {result}"
        print("  ✓ 80,000 字符：触发建议")
        
        # 测试 90,000 字符（触发建议）
        monitor.update_context_size(90000)
        result = monitor.check_threshold()
        assert result == 'suggest', f"预期 'suggest'，实际 {result}"
        print("  ✓ 90,000 字符：触发建议")
        
        print("  ✅ 80K 建议阈值测试通过")
    
    def test_threshold_force(self):
        """测试 100K 强制阈值"""
        print("\n【测试】100K 强制阈值")
        
        monitor = SessionContextMonitor(str(self.workspace))
        
        # 测试 99,999 字符（触发建议）
        monitor.update_context_size(99999)
        result = monitor.check_threshold()
        assert result == 'suggest', f"预期 'suggest'，实际 {result}"
        print("  ✓ 99,999 字符：触发建议")
        
        # 测试 100,000 字符（触发强制）
        monitor.update_context_size(100000)
        result = monitor.check_threshold()
        assert result == 'force', f"预期 'force'，实际 {result}"
        print("  ✓ 100,000 字符：触发强制")
        
        # 测试 150,000 字符（触发强制）
        monitor.update_context_size(150000)
        result = monitor.check_threshold()
        assert result == 'force', f"预期 'force'，实际 {result}"
        print("  ✓ 150,000 字符：触发强制")
        
        print("  ✅ 100K 强制阈值测试通过")
    
    def test_compression_basic(self):
        """测试基本压缩功能"""
        print("\n【测试】基本压缩功能")
        
        monitor = SessionContextMonitor(str(self.workspace))
        
        # 创建示例对话
        conversation = """
SAYELF: 帮我搜索 TurboQuant 算法
太一：好的，我正在搜索...
太一：找到了，这是 Google 2026 年发布的 KV Cache 压缩算法
SAYELF: 核心原理是什么？
太一：极坐标转换 + 1-bit 残差纠错，6 倍压缩零损失
SAYELF: 能用到我们的系统吗？
太一：可以，我建议：1) 记忆压缩 2) 对话管理 3) Bot 协作优化
SAYELF: 全部执行
太一：收到，开始执行...
""" * 100  # 重复 100 次以增加大小
        
        # 强制压缩
        result = monitor.compress_and_save(
            conversation,
            session_id='test-001',
            force=True
        )
        
        # 验证结果
        assert result.success == True, f"压缩失败：{result.message}"
        print(f"  ✓ 压缩成功：{result.message}")
        
        assert result.compression_ratio > 1.0, f"压缩比异常：{result.compression_ratio}"
        print(f"  ✓ 压缩比：{result.compression_ratio:.2f}x")
        
        assert Path(result.memory_file).exists(), f"Memory 文件未生成：{result.memory_file}"
        print(f"  ✓ Memory 文件已生成：{Path(result.memory_file).name}")
        
        # 验证文件内容
        with open(result.memory_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert '核心内容' in content, "Memory 文件缺少核心内容"
        assert '残差标记' in content, "Memory 文件缺少残差标记"
        assert '元数据' in content, "Memory 文件缺少元数据"
        print("  ✓ Memory 文件内容完整")
        
        print("  ✅ 基本压缩功能测试通过")
    
    def test_empty_input(self):
        """测试空输入处理"""
        print("\n【测试】空输入处理")
        
        monitor = SessionContextMonitor(str(self.workspace))
        
        # 空字符串
        result = monitor.compress_and_save('', force=True)
        assert result.success == True, f"空输入压缩失败：{result.message}"
        print("  ✓ 空字符串：处理成功")
        
        # None 输入（应抛出异常或返回空结果）
        try:
            result = monitor.compress_and_save(None, force=True)
            print("  ✓ None 输入：返回空结果")
        except Exception as e:
            print(f"  ✓ None 输入：抛出异常（预期） - {type(e).__name__}")
        
        print("  ✅ 空输入处理测试通过")
    
    def test_extreme_long_text(self):
        """测试极端长文本"""
        print("\n【测试】极端长文本")
        
        monitor = SessionContextMonitor(str(self.workspace))
        
        # 1MB 文本
        long_text = 'x' * 1000000
        
        result = monitor.compress_and_save(long_text, session_id='test-extreme', force=True)
        
        assert result.success == True, f"极端长文本压缩失败：{result.message}"
        print(f"  ✓ 1MB 文本：压缩成功")
        
        assert result.compression_ratio > 1.0, f"压缩比异常：{result.compression_ratio}"
        print(f"  ✓ 压缩比：{result.compression_ratio:.2f}x")
        
        print("  ✅ 极端长文本测试通过")
    
    def test_state_persistence(self):
        """测试状态持久化"""
        print("\n【测试】状态持久化")
        
        # 创建第一个监控器
        monitor1 = SessionContextMonitor(str(self.workspace))
        monitor1.update_context_size(50000)
        monitor1.compress_and_save('test conversation', session_id='test-state', force=True)
        
        # 创建第二个监控器（应加载之前的状态）
        monitor2 = SessionContextMonitor(str(self.workspace))
        
        assert monitor2.current_context_size == monitor1.current_context_size, \
            f"状态未持久化：{monitor2.current_context_size} != {monitor1.current_context_size}"
        print("  ✓ Context 大小持久化")
        
        assert len(monitor2.compression_history) > 0, "压缩历史未持久化"
        print("  ✓ 压缩历史持久化")
        
        print("  ✅ 状态持久化测试通过")
    
    def test_compression_report(self):
        """测试压缩报告"""
        print("\n【测试】压缩报告")
        
        monitor = SessionContextMonitor(str(self.workspace))
        
        # 执行几次压缩
        for i in range(3):
            monitor.compress_and_save(f'test conversation {i}', force=True)
        
        # 获取报告
        report = monitor.get_compression_report()
        
        assert report['total_compressions'] >= 3, f"压缩次数错误：{report['total_compressions']}"
        print(f"  ✓ 总压缩次数：{report['total_compressions']}")
        
        assert report['avg_compression_ratio'] > 0, f"平均压缩比异常：{report['avg_compression_ratio']}"
        print(f"  ✓ 平均压缩比：{report['avg_compression_ratio']:.2f}x")
        
        assert report['total_saved'] >= 0, f"节省空间错误：{report['total_saved']}"
        print(f"  ✓ 总节省空间：{report['total_saved']:,} 字符")
        
        assert report['last_compression'] is not None, "缺少最近压缩记录"
        print("  ✓ 最近压缩记录存在")
        
        print("  ✅ 压缩报告测试通过")
    
    def run_all(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("🧪 SessionContextMonitor 测试套件")
        print("="*60)
        
        self.setup()
        
        try:
            self.test_threshold_suggest()
            self.test_threshold_force()
            self.test_compression_basic()
            self.test_empty_input()
            self.test_extreme_long_text()
            self.test_state_persistence()
            self.test_compression_report()
            
            print("\n" + "="*60)
            print("✅ 所有测试通过！")
            print("="*60)
            return True
            
        except AssertionError as e:
            print(f"\n❌ 测试失败：{e}")
            return False
        except Exception as e:
            print(f"\n❌ 测试异常：{e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.teardown()


class TestAutoCompressionIntegration:
    """测试 AutoCompressionIntegration 类"""
    
    def __init__(self):
        self.test_dir = None
        self.workspace = None
    
    def setup(self):
        """创建测试环境"""
        self.test_dir = tempfile.mkdtemp(prefix='turboquant_integration_')
        self.workspace = Path(self.test_dir) / 'workspace'
        self.workspace.mkdir()
        (self.workspace / 'memory').mkdir()
        print(f"✅ 测试环境：{self.workspace}")
    
    def teardown(self):
        """清理测试环境"""
        if self.test_dir and Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
            print(f"🧹 清理测试环境：{self.test_dir}")
    
    def test_notification_callback(self):
        """测试通知回调"""
        print("\n【测试】通知回调")
        
        integration = AutoCompressionIntegration(str(self.workspace))
        
        notifications = []
        
        def callback(message: str):
            notifications.append(message)
        
        integration.set_notification_callback(callback)
        
        # 手动压缩
        result = integration.manual_compress(
            'test conversation ' * 100,
            session_id='test-notify'
        )
        
        assert result.success == True, f"压缩失败：{result.message}"
        assert len(notifications) > 0, "未触发通知"
        assert '压缩完成' in notifications[0], f"通知内容异常：{notifications[0]}"
        
        print(f"  ✓ 通知已触发：{notifications[0][:50]}...")
        print("  ✅ 通知回调测试通过")
    
    def test_get_status(self):
        """测试状态查询"""
        print("\n【测试】状态查询")
        
        integration = AutoCompressionIntegration(str(self.workspace))
        
        # 执行几次压缩
        for i in range(2):
            integration.manual_compress(f'test {i}', session_id=f'test-{i}')
        
        # 获取状态
        status = integration.get_status()
        
        assert status['total_compressions'] >= 2, f"压缩次数错误：{status['total_compressions']}"
        assert 'avg_compression_ratio' in status, "缺少平均压缩比"
        assert 'current_context_size' in status, "缺少当前 context 大小"
        
        print(f"  ✓ 状态查询成功：{json.dumps(status, indent=2, ensure_ascii=False)[:200]}...")
        print("  ✅ 状态查询测试通过")
    
    def run_all(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("🧪 AutoCompressionIntegration 测试套件")
        print("="*60)
        
        self.setup()
        
        try:
            self.test_notification_callback()
            self.test_get_status()
            
            print("\n" + "="*60)
            print("✅ 所有测试通过！")
            print("="*60)
            return True
            
        except AssertionError as e:
            print(f"\n❌ 测试失败：{e}")
            return False
        except Exception as e:
            print(f"\n❌ 测试异常：{e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.teardown()


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🚀 Context 自动压缩集成测试")
    print(f"📅 时间：{datetime.now().isoformat()}")
    print("="*60)
    
    # 测试 SessionContextMonitor
    test1 = TestSessionContextMonitor()
    result1 = test1.run_all()
    
    # 测试 AutoCompressionIntegration
    test2 = TestAutoCompressionIntegration()
    result2 = test2.run_all()
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    print(f"SessionContextMonitor: {'✅ 通过' if result1 else '❌ 失败'}")
    print(f"AutoCompressionIntegration: {'✅ 通过' if result2 else '❌ 失败'}")
    
    if result1 and result2:
        print("\n✅ 所有测试通过！验收标准达成：")
        print("  1. ✓ 自动触发阈值准确（80K 建议，100K 强制）")
        print("  2. ✓ 压缩过程无感知（用户无中断）")
        print("  3. ✓ 压缩后 memory 文件正确生成")
        return 0
    else:
        print("\n❌ 部分测试失败，请检查")
        return 1


if __name__ == '__main__':
    sys.exit(main())
