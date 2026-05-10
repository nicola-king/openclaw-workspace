#!/usr/bin/env python3
"""
美学过滤器模块测试
"""

import unittest
import json
import sys
from pathlib import Path

# 添加父目录到路径

sys.path.insert(0, str(Path(__file__).parent.parent))

from core import AestheticFilter, ContentType, QualityLevel


class TestAestheticFilter(unittest.TestCase):
    """美学过滤器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.filter = AestheticFilter()
    
    def test_detect_markdown(self):
        """测试 Markdown 检测"""
        content = "# 标题\n\n内容"
        result = self.filter._detect_content_type(content)
        self.assertEqual(result, ContentType.MARKDOWN)
    
    def test_detect_code(self):
        """测试代码检测"""
        content = "def hello():\n    print('hello')"
        result = self.filter._detect_content_type(content)
        self.assertEqual(result, ContentType.CODE)
    
    def test_detect_data(self):
        """测试数据检测"""
        content = '{"name": "test", "value": 123}'
        result = self.filter._detect_content_type(content)
        self.assertEqual(result, ContentType.DATA)
    
    def test_process_markdown(self):
        """测试 Markdown 处理"""
        content = "# 标题\n\n- 项目 1\n- 项目 2\n\n```python\nprint('hello')\n```"
        result = self.filter.process(content, content_type=ContentType.MARKDOWN)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["content_type"], "markdown")
        self.assertIn("quality_level", result)
        self.assertIn("changes", result)
        self.assertGreater(result["changes_count"], 0)
    
    def test_process_code(self):
        """测试代码处理"""
        content = "def hello():\n    print('hello')\n\n\ndef world():\n    print('world')"
        result = self.filter.process(content, content_type=ContentType.CODE)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["content_type"], "code")
    
    def test_process_data(self):
        """测试数据处理"""
        content = '{"name":"test","value":123}'
        result = self.filter.process(content, content_type=ContentType.DATA)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["content_type"], "data")
        # 检查 JSON 格式化
        self.assertIn('  ', result["content"])
    
    def test_process_report(self):
        """测试报告处理"""
        content = "# 市场报告\n\n## 摘要\n\n市场需求稳定增长"
        result = self.filter.process(content, content_type=ContentType.REPORT)
        
        self.assertEqual(result["status"], "success")
        # 报告本质上是 Markdown，但增加了额外处理
        self.assertIn(result["content_type"], ["report", "markdown"])
    
    def test_quality_assessment(self):
        """测试质量评估"""
        # 高质量 Markdown
        high_quality = """# 标题

## 子标题


- 项目 1
- 项目 2

```python
print('hello')
```

> 引用块

| 列 1 | 列 2 |
|------|------|
| 数据 | 数据 |
"""
        quality = self.filter._assess_markdown_quality(high_quality)
        self.assertIn(quality, [QualityLevel.S, QualityLevel.A])
    
    def test_file_processing(self):
        """测试文件处理"""
        # 创建测试文件
        test_file = Path("/tmp/test_artifact.md")
        test_file.write_text("# 测试文档\n\n内容", encoding="utf-8")
        
        result = self.filter.process_file(str(test_file))
        
        self.assertEqual(result["status"], "success")
        self.assertIn("output_file", result)
        
        # 清理
        test_file.unlink()
        output_file = Path(result["output_file"])
        if output_file.exists():
            output_file.unlink()
    
    def test_health_check(self):
        """测试健康检查"""
        result = self.filter.health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["module"], "aesthetic-filter")
        self.assertEqual(result["version"], "1.0.0")
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.filter.name, "aesthetic-filter")
        self.assertEqual(self.filter.version, "1.0.0")
        self.assertEqual(self.filter.dependencies, [])


if __name__ == "__main__":
    unittest.main()
