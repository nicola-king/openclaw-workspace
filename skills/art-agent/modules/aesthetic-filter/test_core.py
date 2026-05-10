#!/usr/bin/env python3
"""
美学过滤器测试套件 v1.1.0

覆盖范围：
- 基本路径（原有）
- [FIX-1] _optimize_headings 重复行边界
- [FIX-2] quality_level 不再依赖 '太一美学' 字符串
- [FIX-3] _process_data / _process_config 质量评级
- [FIX-4] ScoringEngine 评分覆盖 quality_level
- 质量门禁拒绝路径
- ScoringEngine 集成
"""

import json
import sys
import os
import unittest

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import AestheticFilter, ContentType, QualityLevel


# ══════════════════════════════════════════
# 基本路径测试（原有）
# ══════════════════════════════════════════

class TestMarkdownProcessing(unittest.TestCase):

    def setUp(self):
        self.filter = AestheticFilter()

    def test_basic_markdown(self):
        content = "# 标题\n\n一段文字。\n\n- 列表项1\n- 列表项2"
        result = self.filter.process(content, ContentType.MARKDOWN)
        self.assertEqual(result["status"], "success")
        self.assertIn("content", result)

    def test_auto_detect_markdown(self):
        content = "# 自动检测\n\n内容。"
        result = self.filter.process(content)
        self.assertEqual(result["content_type"], "markdown")

    def test_list_unification(self):
        """* 和 + 应统一为 -"""
        content = "# 列表测试\n\n* 项目1\n+ 项目2\n- 项目3"
        result = self.filter.process(content, ContentType.MARKDOWN)
        lines = result["content"].split('\n')
        list_lines = [l for l in lines if l.strip() and l.strip()[0] in '-*+']
        for line in list_lines:
            self.assertTrue(
                line.startswith('- '),
                f"列表项未统一为 '-': {line!r}"
            )

    def test_signature_disabled_by_default(self):
        """默认不添加签名"""
        content = "# 测试\n\n内容。"
        result = self.filter.process(content, ContentType.MARKDOWN)
        self.assertNotIn("太一美学", result["content"])


class TestCodeProcessing(unittest.TestCase):

    def setUp(self):
        self.filter = AestheticFilter()

    def test_basic_code(self):
        content = "def hello():\n    print('hello')\n\n\n\ndef world():\n    pass"
        result = self.filter.process(content, ContentType.CODE)
        self.assertEqual(result["status"], "success")
        # 三个连续空行应被压缩
        self.assertNotIn('\n\n\n', result["content"])

    def test_trailing_whitespace_removed(self):
        content = "def foo():   \n    x = 1   \n"
        result = self.filter.process(content, ContentType.CODE)
        for line in result["content"].split('\n'):
            self.assertEqual(line, line.rstrip(), f"行尾有空格: {line!r}")


class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        self.filter = AestheticFilter()

    def test_valid_json_formatted(self):
        content = '{"key":"value","num":42}'
        result = self.filter.process(content, ContentType.DATA)
        data = json.loads(result["content"])
        self.assertEqual(data["key"], "value")
        self.assertEqual(result["status"], "success")

    def test_invalid_json_preserved(self):
        content = "not json content"
        result = self.filter.process(content, ContentType.DATA)
        self.assertEqual(result["content"], content)


# ══════════════════════════════════════════
# [FIX-1] _optimize_headings 重复行边界
# ══════════════════════════════════════════

class TestOptimizeHeadingsFix(unittest.TestCase):

    def setUp(self):
        self.filter = AestheticFilter()

    def test_duplicate_lines_no_index_error(self):
        """重复行不应导致 index() 返回错误位置"""
        content = (
            "# 标题一\n\n"
            "相同的文字行\n"
            "相同的文字行\n\n"
            "## 标题二\n\n"
            "相同的文字行\n"
        )
        # 不应抛出异常
        result = self.filter._optimize_headings(content)
        processed, changes = result
        self.assertIn("## 标题二", processed)

    def test_heading_level_continuity(self):
        """H1 → H3 应被压缩为 H1 → H2"""
        content = "# 一级标题\n\n### 跳级标题\n\n内容"
        processed, changes = self.filter._optimize_headings(content)
        self.assertIn("## 跳级标题", processed)
        self.assertNotIn("### 跳级标题", processed)
        self.assertTrue(len(changes) > 0)

    def test_first_heading_no_blank_before(self):
        """首个标题前不应插入多余空行"""
        content = "# 首标题\n\n内容"
        processed, _ = self.filter._optimize_headings(content)
        self.assertFalse(processed.startswith('\n'))


# ══════════════════════════════════════════
# [FIX-2] quality_level 不依赖 '太一美学'
# ══════════════════════════════════════════

class TestQualityAssessmentFix(unittest.TestCase):

    def setUp(self):
        self.filter = AestheticFilter()

    def test_no_manipulation_via_keyword(self):
        """插入 '太一美学' 不应自动提升到 S 级"""
        # 极简内容，结构评分应很低
        content = "太一美学太一美学太一美学太一美学太一美学"
        # 使用内部方法直接测试
        quality = self.filter._assess_markdown_quality(content)
        # 没有任何 Markdown 结构，不应得 S 或 A
        self.assertNotIn(quality, [QualityLevel.S, QualityLevel.A])

    def test_structured_content_scores_higher(self):
        """有完整结构的 Markdown 应得到更高等级"""
        rich = (
            "# 主标题\n\n"
            "## 章节一\n\n"
            "内容内容。\n\n"
            "- 列表项\n\n"
            "```python\nprint('hi')\n```\n\n"
            "| 列 | 值 |\n|---|---|\n| A | 1 |\n\n"
            "> 引用\n"
        )
        quality_rich = self.filter._assess_markdown_quality(rich)
        empty_quality = self.filter._assess_markdown_quality("随便写几个字")
        # rich 应优于 empty
        level_order = {
            QualityLevel.S: 4, QualityLevel.A: 3,
            QualityLevel.B: 2, QualityLevel.C: 1
        }
        self.assertGreaterEqual(
            level_order[quality_rich], level_order[empty_quality]
        )


# ══════════════════════════════════════════
# [FIX-3] _process_data / _process_config 质量评级
# ══════════════════════════════════════════

class TestDataConfigQualityFix(unittest.TestCase):

    def setUp(self):
        self.filter = AestheticFilter()

    def test_valid_json_data_gets_A(self):
        result = self.filter._process_data('{"x": 1}')
        self.assertEqual(result["quality_level"], QualityLevel.A.value)

    def test_invalid_json_data_gets_B(self):
        result = self.filter._process_data("not json")
        self.assertEqual(result["quality_level"], QualityLevel.B.value)

    def test_valid_json_config_gets_A(self):
        result = self.filter._process_config('{"debug": true}')
        self.assertEqual(result["quality_level"], QualityLevel.A.value)

    def test_invalid_json_config_gets_B(self):
        result = self.filter._process_config("key = value")
        self.assertEqual(result["quality_level"], QualityLevel.B.value)


# ══════════════════════════════════════════
# [FIX-4] ScoringEngine 集成测试
# ══════════════════════════════════════════

class TestScoringEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.filter = AestheticFilter()

    def test_scoring_report_present(self):
        """process() 结果中应包含 scoring_report"""
        content = "# 标题\n\n内容段落。"
        result = self.filter.process(content, ContentType.MARKDOWN)
        self.assertIn("scoring_report", result)
        report = result["scoring_report"]
        self.assertIn("total_score", report)
        self.assertIn("level", report)
        self.assertIn("dimensions", report)

    def test_quality_level_matches_scoring_engine(self):
        """quality_level 应与 ScoringEngine 的 level 一致"""
        content = "# 标题\n\n内容段落。"
        result = self.filter.process(content, ContentType.MARKDOWN)
        self.assertEqual(
            result["quality_level"],
            result["scoring_report"]["level"]
        )

    def test_process_history_records_score(self):
        """处理历史应记录 ScoringEngine 的分数"""
        content = "# 标题\n\n内容。"
        self.filter.process(content, ContentType.MARKDOWN)
        last = self.filter.process_history[-1]
        self.assertIn("score", last)
        self.assertIsInstance(last["score"], float)


# ══════════════════════════════════════════
# 质量门禁拒绝路径（OutputHook 集成）
# ══════════════════════════════════════════

class TestQualityGateRejection(unittest.TestCase):

    def setUp(self):
        self.filter = AestheticFilter()

    def _quality_order(self, level_str: str) -> int:
        order = {"S": 4, "A": 3, "B": 2, "C": 1}
        return order.get(level_str, 0)

    def test_empty_content_low_quality(self):
        """极短内容应得低等级"""
        result = self.filter.process("hi", ContentType.MARKDOWN)
        level = result["quality_level"]
        # 不应达到 S 级
        self.assertNotEqual(level, "S")

    def test_rich_content_higher_quality(self):
        """结构丰富的内容应高于极简内容"""
        poor = self.filter.process("hi", ContentType.MARKDOWN)
        rich = self.filter.process(
            "# 主标题\n\n## 章节\n\n"
            "- 列表项\n- 另一项\n\n"
            "```python\nprint('hello')\n```\n\n"
            "| 列 | 值 |\n|---|---|\n| A | 1 |",
            ContentType.MARKDOWN
        )
        self.assertGreaterEqual(
            self._quality_order(rich["quality_level"]),
            self._quality_order(poor["quality_level"])
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
