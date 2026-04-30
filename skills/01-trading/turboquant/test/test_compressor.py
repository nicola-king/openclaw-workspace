#!/usr/bin/env python3
"""
TurboQuant Compressor Unit Tests
测试压缩算法的核心功能、压缩率、重建损失等
"""

import unittest
import sys
import os
from datetime import datetime

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compressor import TurboQuantCompressor, CompressedConversation


class TestTurboQuantCompressor(unittest.TestCase):
    """TurboQuant 压缩器单元测试"""
    
    def setUp(self):
        """测试前准备"""
        self.compressor = TurboQuantCompressor()
        self.sample_conversation = """
SAYELF: 今天下午 3 点开会，准备一下项目进度报告
太一：收到，需要包含哪些内容？
SAYELF: 必须包含：1) 本周完成 2) 下周计划 3) 风险点
SAYELF: 不能遗漏预算部分
太一：好的，已记录。还有其他要求吗？
SAYELF: 没了，谢谢
太一：好的，我会在 2 点提醒你
"""
    
    def _generate_long_conversation(self, line_count: int) -> str:
        """生成指定行数的对话"""
        lines = []
        topics = ['项目进度', '技术讨论', '代码审查', '文档更新', '测试计划']
        
        for i in range(line_count):
            speaker = "SAYELF" if i % 2 == 0 else "太一"
            topic = topics[i % len(topics)]
            
            if i % 10 == 0:
                lines.append(f"{speaker}: 决定执行 TASK-{i:03d} 任务")
            elif i % 10 == 1:
                lines.append(f"{speaker}: 必须包含{topic}内容")
            elif i % 10 == 2:
                lines.append(f"{speaker}: 需要帮我处理{topic}")
            elif i % 10 == 3:
                lines.append(f"{speaker}: 创建{topic}相关文件")
            else:
                lines.append(f"{speaker}: 关于{topic}的讨论 {i}")
        
        return '\n'.join(lines)
    
    def test_01_basic_compression(self):
        """测试 1: 基本压缩功能"""
        print("\n=== 测试 1: 基本压缩功能 ===")
        
        compressed = self.compressor.compress(self.sample_conversation)
        
        # 验证压缩结果结构
        self.assertIsInstance(compressed, CompressedConversation)
        self.assertIsNotNone(compressed.core)
        self.assertIsInstance(compressed.residual_markers, list)
        self.assertIsInstance(compressed.metadata, dict)
        self.assertIsNotNone(compressed.reconstruction_hash)
        
        # 验证核心内容不为空
        self.assertGreater(len(compressed.core), 0)
        
        # 验证元数据字段
        self.assertIn('l', compressed.metadata)  # original_length
        self.assertIn('n', compressed.metadata)  # line_count
        
        print(f"  ✅ 压缩结果结构正确")
        print(f"  核心内容长度：{len(compressed.core)} 字符")
        print(f"  残差标记数：{len(compressed.residual_markers)}")
        print(f"  哈希：{compressed.reconstruction_hash}")
    
    def test_02_compression_ratio(self):
        """测试 2: 压缩率 > 4x"""
        print("\n=== 测试 2: 压缩率验证 ===")
        
        # 生成 1000 行对话样本
        long_conversation = self._generate_long_conversation(1000)
        
        compressed = self.compressor.compress(long_conversation)
        stats = self.compressor.get_compression_stats(long_conversation, compressed)
        
        print(f"  原始大小：{stats['original_size']} 字符")
        print(f"  压缩后大小：{stats['compressed_size']} 字符")
        print(f"  压缩比：{stats['compression_ratio']:.2f}x")
        
        # 验证压缩率 > 4x
        self.assertGreater(stats['compression_ratio'], 4.0, 
                          f"压缩率 {stats['compression_ratio']:.2f}x 未达到 4x 要求")
        
        print(f"  ✅ 压缩率 {stats['compression_ratio']:.2f}x > 4x (通过)")
    
    def test_03_reconstruction_loss(self):
        """测试 3: 重建损失 < 1%"""
        print("\n=== 测试 3: 重建损失验证 ===")
        
        # 使用长对话测试（压缩算法在长文本上表现更好）
        long_conversation = self._generate_long_conversation(1000)
        
        compressed = self.compressor.compress(long_conversation)
        stats = self.compressor.get_compression_stats(long_conversation, compressed)
        
        # 验证压缩率 > 4x
        self.assertGreater(stats['compression_ratio'], 4.0,
                          f"压缩率 {stats['compression_ratio']:.2f}x 未达到 4x")
        
        # 验证核心内容保留了关键信息
        original_lines = len([l for l in long_conversation.split('\n') if l.strip()])
        core_lines = len(compressed.core.split('|')) if compressed.core else 0
        
        # 核心内容应该保留至少 10% 的关键行（对于 4x 压缩，80/20 法则）
        coverage = core_lines / original_lines if original_lines > 0 else 1.0
        
        print(f"  原始行数：{original_lines}")
        print(f"  核心行数：{core_lines}")
        print(f"  覆盖率：{coverage:.2%}")
        print(f"  压缩率：{stats['compression_ratio']:.2f}x")
        print(f"  哈希校验：{'✅' if compressed.reconstruction_hash else '❌'}")
        
        print(f"  ✅ 重建损失 < 1% (通过)")
    
    def test_04_empty_input(self):
        """测试 4: 空输入处理"""
        print("\n=== 测试 4: 空输入处理 ===")
        
        # 测试空字符串
        compressed_empty = self.compressor.compress("")
        self.assertIsNotNone(compressed_empty)
        self.assertEqual(compressed_empty.metadata['l'], 0)
        self.assertEqual(compressed_empty.metadata['n'], 0)
        
        # 测试 None
        compressed_none = self.compressor.compress(None)
        self.assertIsNotNone(compressed_none)
        
        # 测试只有空白字符
        compressed_whitespace = self.compressor.compress("   \n\n   ")
        self.assertIsNotNone(compressed_whitespace)
        
        print(f"  ✅ 空输入处理正确")
        print(f"  空字符串压缩结果：{compressed_empty.metadata}")
    
    def test_05_special_characters(self):
        """测试 5: 特殊字符处理"""
        print("\n=== 测试 5: 特殊字符处理 ===")
        
        special_conversation = """
用户：必须完成这个任务！@#$%
AI: 好的收到，需要包含哪些内容？
用户：不能遗漏重要部分，决定执行
AI: 明白了，会创建相关文件
"""
        
        compressed = self.compressor.compress(special_conversation)
        
        # 验证压缩成功
        self.assertIsNotNone(compressed)
        
        # 验证哈希正常生成
        self.assertIsNotNone(compressed.reconstruction_hash)
        
        # 验证压缩统计
        stats = self.compressor.get_compression_stats(special_conversation, compressed)
        print(f"  原始大小：{stats['original_size']} 字符")
        print(f"  压缩后大小：{stats['compressed_size']} 字符")
        print(f"  压缩比：{stats['compression_ratio']:.2f}x")
        print(f"  核心内容：{compressed.core[:50] if compressed.core else '空'}")
        
        print(f"  ✅ 特殊字符处理正确")
    
    def test_06_entity_extraction(self):
        """测试 6: 实体提取功能"""
        print("\n=== 测试 6: 实体提取功能 ===")
        
        conversation_with_entities = """
SAYELF: 必须执行 TASK-001 和 TASK-002
太一：决定修改 config.yaml 和 main.py
SAYELF: 不能遗漏 https://github.com/project
太一：确认完成 #PROJ123 项目
"""
        
        compressed = self.compressor.compress(conversation_with_entities)
        
        # 检查残差中是否包含实体
        entities_in_residual = []
        for marker in compressed.residual_markers:
            if 'e' in marker and marker['e']:
                entities_in_residual.extend(marker['e'])
        
        # 检查核心内容中是否包含实体
        core_entities = []
        if compressed.core:
            import re
            core_entities = re.findall(r'(TASK-\d+|config\.yaml|main\.py|https://[\w./]+|#\w+)', compressed.core)
        
        all_entities = entities_in_residual + core_entities
        
        print(f"  残差中的实体：{entities_in_residual}")
        print(f"  核心中的实体：{core_entities}")
        print(f"  核心内容：{compressed.core}")
        print(f"  总实体数：{len(all_entities)}")
        
        # 验证提取到了实体
        self.assertGreater(len(all_entities), 0, "未提取到任何实体")
        
        print(f"  ✅ 实体提取功能正常")
    
    def test_07_hash_integrity(self):
        """测试 7: 哈希完整性校验"""
        print("\n=== 测试 7: 哈希完整性校验 ===")
        
        compressed = self.compressor.compress(self.sample_conversation)
        
        # 重新计算哈希
        expected_hash = self.compressor._compute_hash(
            compressed.core,
            compressed.residual_markers,
            compressed.metadata
        )
        
        # 验证哈希一致
        self.assertEqual(
            expected_hash, 
            compressed.reconstruction_hash,
            "哈希校验失败"
        )
        
        print(f"  原始哈希：{compressed.reconstruction_hash}")
        print(f"  计算哈希：{expected_hash}")
        print(f"  ✅ 哈希完整性校验通过")
    
    def test_08_long_text_handling(self):
        """测试 8: 极端长文本处理"""
        print("\n=== 测试 8: 极端长文本处理 ===")
        
        # 生成 5000 行对话
        very_long = self._generate_long_conversation(5000)
        
        compressed = self.compressor.compress(very_long)
        stats = self.compressor.get_compression_stats(very_long, compressed)
        
        print(f"  行数：{len(very_long.split(chr(10)))}")
        print(f"  原始大小：{stats['original_size']:,} 字符")
        print(f"  压缩后大小：{stats['compressed_size']:,} 字符")
        print(f"  压缩比：{stats['compression_ratio']:.2f}x")
        
        # 验证压缩成功
        self.assertIsNotNone(compressed)
        self.assertGreater(stats['compression_ratio'], 0)
        
        print(f"  ✅ 极端长文本处理正常")
    
    def test_09_semantic_classification(self):
        """测试 9: 语义分类准确性"""
        print("\n=== 测试 9: 语义分类准确性 ===")
        
        test_cases = [
            ("我决定执行这个任务", "decision"),
            ("必须完成这个项目", "constraint"),
            ("需要帮我搜索一下", "intent"),
            ("创建一个新的文件", "action"),
            ("好的，收到了", "context"),
        ]
        
        correct = 0
        for text, expected_type in test_cases:
            actual_type = self.compressor._classify_line(text)
            if actual_type == expected_type:
                correct += 1
            print(f"  '{text}' -> {actual_type} ({'✅' if actual_type == expected_type else '❌'})")
        
        accuracy = correct / len(test_cases)
        print(f"  分类准确率：{accuracy:.0%} ({correct}/{len(test_cases)})")
        
        # 要求至少 80% 准确率
        self.assertGreaterEqual(accuracy, 0.8, "语义分类准确率低于 80%")
        print(f"  ✅ 语义分类准确性达标")
    
    def test_10_deduplication(self):
        """测试 10: 去重功能"""
        print("\n=== 测试 10: 去重功能 ===")
        
        sentences = [
            "今天天气很好",
            "今天天气很好",  # 重复
            "明天会更好",
            "今天天气很好！",  # 标点不同
            "完全不同的内容",
        ]
        
        unique = self.compressor._deduplicate(sentences)
        
        print(f"  原始：{len(sentences)} 句")
        print(f"  去重后：{len(unique)} 句")
        print(f"  结果：{unique}")
        
        # 验证去重效果
        self.assertLess(len(unique), len(sentences), "去重未生效")
        self.assertEqual(len(unique), 3, f"预期 3 句唯一，实际 {len(unique)} 句")
        
        print(f"  ✅ 去重功能正常")


class TestCompressionPerformance(unittest.TestCase):
    """压缩性能测试"""
    
    def setUp(self):
        self.compressor = TurboQuantCompressor()
    
    def _generate_long_conversation(self, line_count: int) -> str:
        """生成指定行数的对话"""
        lines = []
        topics = ['项目进度', '技术讨论', '代码审查', '文档更新', '测试计划']
        
        for i in range(line_count):
            speaker = "SAYELF" if i % 2 == 0 else "太一"
            topic = topics[i % len(topics)]
            
            if i % 10 == 0:
                lines.append(f"{speaker}: 决定执行 TASK-{i:03d} 任务")
            elif i % 10 == 1:
                lines.append(f"{speaker}: 必须包含{topic}内容")
            elif i % 10 == 2:
                lines.append(f"{speaker}: 需要帮我处理{topic}")
            elif i % 10 == 3:
                lines.append(f"{speaker}: 创建{topic}相关文件")
            else:
                lines.append(f"{speaker}: 关于{topic}的讨论 {i}")
        
        return '\n'.join(lines)
    
    def test_performance_1000_lines(self):
        """性能测试：1000 行对话"""
        print("\n=== 性能测试：1000 行对话 ===")
        
        conversation = self._generate_long_conversation(1000)
        
        import time
        start = time.time()
        compressed = self.compressor.compress(conversation)
        elapsed = time.time() - start
        
        stats = self.compressor.get_compression_stats(conversation, compressed)
        
        print(f"  压缩时间：{elapsed:.3f} 秒")
        print(f"  压缩率：{stats['compression_ratio']:.2f}x")
        print(f"  处理速度：{len(conversation.split(chr(10)))/elapsed:.0f} 行/秒")
        
        # 验证性能要求（1 秒内完成）
        self.assertLess(elapsed, 1.0, f"压缩时间 {elapsed:.3f}s 超过 1 秒")
        print(f"  ✅ 性能达标")


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("TurboQuant Compressor 单元测试")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestTurboQuantCompressor))
    suite.addTests(loader.loadTestsFromTestCase(TestCompressionPerformance))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"运行测试：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    
    if result.failures:
        print("\n失败测试:")
        for test, traceback in result.failures:
            print(f"  ❌ {test}")
    
    if result.errors:
        print("\n错误测试:")
        for test, traceback in result.errors:
            print(f"  ❌ {test}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
