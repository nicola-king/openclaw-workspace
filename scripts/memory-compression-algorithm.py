#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆压缩算法

核心理念：Claude-Mem "知道什么该丢掉"
- 保留核心决策
- 丢弃重复内容
- 提取关键洞察

作者：太一 AGI
创建：2026-04-14
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
from collections import defaultdict

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
REPORTS_DIR = WORKSPACE / "reports"

# 确保目录存在
REPORTS_DIR.mkdir(exist_ok=True)


class MemoryCompressor:
    """记忆压缩器"""
    
    def __init__(self):
        self.compression_stats = {
            'original_tokens': 0,
            'compressed_tokens': 0,
            'compression_ratio': 0,
            'removed_duplicates': 0,
            'extracted_insights': 0,
        }
    
    def compress(self, content: str) -> str:
        """压缩记忆内容"""
        print("🗜️ 开始压缩记忆...")
        
        # 记录原始长度
        self.compression_stats['original_tokens'] = len(content.split())
        
        # Step 1: 移除重复内容
        content = self.remove_duplicates(content)
        
        # Step 2: 提取核心决策
        content = self.extract_core_decisions(content)
        
        # Step 3: 移除噪音
        content = self.remove_noise(content)
        
        # Step 4: 结构化整理
        content = self.structure_content(content)
        
        # 计算压缩率
        self.compression_stats['compressed_tokens'] = len(content.split())
        self.compression_stats['compression_ratio'] = (
            (1 - self.compression_stats['compressed_tokens'] / 
             max(self.compression_stats['original_tokens'], 1)) * 100
        )
        
        print(f"✅ 压缩完成：{self.compression_stats['compression_ratio']:.1f}% 减少")
        
        return content
    
    def remove_duplicates(self, content: str) -> str:
        """移除重复内容"""
        print("  📤 移除重复内容...")
        
        lines = content.split('\n')
        seen_lines: Set[str] = set()
        unique_lines = []
        duplicates = 0
        
        for line in lines:
            # 忽略空行和短行
            if len(line.strip()) < 10:
                unique_lines.append(line)
                continue
            
            # 检查是否重复
            line_hash = hash(line.strip().lower())
            if line_hash not in seen_lines:
                seen_lines.add(line_hash)
                unique_lines.append(line)
            else:
                duplicates += 1
        
        self.compression_stats['removed_duplicates'] = duplicates
        print(f"    移除 {duplicates} 个重复行")
        
        return '\n'.join(unique_lines)
    
    def extract_core_decisions(self, content: str) -> str:
        """提取核心决策"""
        print("  🎯 提取核心决策...")
        
        # 关键词识别核心决策
        decision_keywords = [
            '决策', '决定', '确定', '采用', '选择',
            '核心', '关键', '重要', '必须', '优先',
            '完成', '成功', '实现', '创建', '建立',
        ]
        
        lines = content.split('\n')
        core_lines = []
        insights = 0
        
        for line in lines:
            # 检查是否包含核心决策关键词
            if any(keyword in line for keyword in decision_keywords):
                core_lines.append(line)
                insights += 1
            # 保留标题和重要结构
            elif line.startswith('#') or line.startswith('##') or line.startswith('###'):
                core_lines.append(line)
            # 保留列表项
            elif line.strip().startswith('-') or line.strip().startswith('*'):
                core_lines.append(line)
        
        self.compression_stats['extracted_insights'] = insights
        print(f"    提取 {insights} 个核心决策/洞察")
        
        return '\n'.join(core_lines)
    
    def remove_noise(self, content: str) -> str:
        """移除噪音"""
        print("  🔇 移除噪音...")
        
        # 噪音模式
        noise_patterns = [
            r'^\s*#.*临时.*$',  # 临时标记
            r'^\s*#.*TODO.*$',  # TODO
            r'^\s*#.*FIXME.*$',  # FIXME
            r'^\s*#.*XXX.*$',  # XXX
            r'^\s*//.*$',  # 单行注释
            r'^\s*/\*.*\*/\s*$',  # 单行块注释
            r'^\s*import.*$',  # import 语句 (保留关键)
            r'^\s*from.*import.*$',  # from import
        ]
        
        lines = content.split('\n')
        clean_lines = []
        noise_count = 0
        
        for line in lines:
            is_noise = False
            for pattern in noise_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    is_noise = True
                    noise_count += 1
                    break
            
            if not is_noise:
                clean_lines.append(line)
        
        print(f"    移除 {noise_count} 个噪音行")
        
        return '\n'.join(clean_lines)
    
    def structure_content(self, content: str) -> str:
        """结构化整理"""
        print("  📋 结构化整理...")
        
        lines = content.split('\n')
        structured = []
        
        # 添加结构化头部
        structured.append(f"# 压缩记忆")
        structured.append(f"> **压缩时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        structured.append(f"> **压缩率**: {self.compression_stats['compression_ratio']:.1f}%")
        structured.append("")
        structured.append("---")
        structured.append("")
        
        # 添加内容
        structured.extend(lines)
        
        # 添加统计信息
        structured.append("")
        structured.append("---")
        structured.append("")
        structured.append("## 压缩统计")
        structured.append("")
        structured.append(f"- 原始 Tokens: {self.compression_stats['original_tokens']:,}")
        structured.append(f"- 压缩后 Tokens: {self.compression_stats['compressed_tokens']:,}")
        structured.append(f"- 压缩率：{self.compression_stats['compression_ratio']:.1f}%")
        structured.append(f"- 移除重复：{self.compression_stats['removed_duplicates']}")
        structured.append(f"- 提取洞察：{self.compression_stats['extracted_insights']}")
        
        return '\n'.join(structured)
    
    def compress_file(self, input_file: Path, output_file: Path = None):
        """压缩文件"""
        print(f"📂 压缩文件：{input_file}")
        
        if not input_file.exists():
            print(f"❌ 文件不存在：{input_file}")
            return None
        
        # 读取内容
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 压缩
        compressed = self.compress(content)
        
        # 保存
        if output_file is None:
            output_file = input_file.parent / f"{input_file.stem}-compressed{input_file.suffix}"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(compressed)
        
        print(f"✅ 压缩完成：{output_file}")
        return output_file
    
    def compress_memory_files(self):
        """压缩记忆文件"""
        print("🗜️ 批量压缩记忆文件...")
        
        # 查找记忆文件
        memory_files = list(MEMORY_DIR.glob("*.md"))
        
        compressed_files = []
        for memory_file in memory_files:
            # 跳过已压缩的文件
            if '-compressed' in memory_file.name:
                continue
            
            output_file = memory_file.parent / f"{memory_file.stem}-compressed.md"
            result = self.compress_file(memory_file, output_file)
            if result:
                compressed_files.append(result)
        
        print(f"✅ 压缩 {len(compressed_files)} 个记忆文件")
        return compressed_files
    
    def generate_report(self) -> Path:
        """生成压缩报告"""
        print("📝 生成压缩报告...")
        
        report_file = REPORTS_DIR / f"memory-compression-report-{datetime.now().strftime('%Y%m%d')}.md"
        
        content = f"""# 🗜️ 记忆压缩报告

> **压缩时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **核心理念**: Claude-Mem "知道什么该丢掉"

---

## 📊 压缩统计

| 指标 | 数值 |
|------|------|
| **原始 Tokens** | {self.compression_stats['original_tokens']:,} |
| **压缩后 Tokens** | {self.compression_stats['compressed_tokens']:,} |
| **压缩率** | {self.compression_stats['compression_ratio']:.1f}% |
| **移除重复** | {self.compression_stats['removed_duplicates']} |
| **提取洞察** | {self.compression_stats['extracted_insights']} |

---

## 🔍 压缩策略

### 1. 移除重复内容
```
- 检测重复行
- 基于哈希去重
- 保留首次出现
```

### 2. 提取核心决策
```
关键词识别:
- 决策/决定/确定
- 核心/关键/重要
- 完成/成功/实现
```

### 3. 移除噪音
```
噪音模式:
- 临时标记
- TODO/FIXME/XXX
- 单行注释
- Import 语句
```

### 4. 结构化整理
```
- 添加压缩头部
- 保留标题结构
- 添加统计信息
```

---

## 💡 优化建议

### 已实现
```
✅ 重复内容移除
✅ 核心决策提取
✅ 噪音识别移除
✅ 结构化整理
```

### 待实现 (P1)
```
⏳ LLM 辅助压缩
⏳ 语义相似度检测
⏳ 智能关键词提取
⏳ 跨文件引用优化
```

---

## 📊 预期效果

### Claude-Mem 验证
```
✅ Token 减少：95%
✅ 保留核心信息
✅ 跨会话连续
```

### 太一实现
```
🎯 Token 减少：70-85% (保守估计)
✅ 保留核心决策
✅ 保留关键洞察
✅ 结构化可查
```

---

## 🚀 下一步行动

### 今天 (2026-04-14)
- [x] 记忆压缩算法设计
- [x] 基础压缩实现
- [ ] LLM 辅助压缩

### 明天 (2026-04-15)
- [ ] 语义相似度检测
- [ ] 智能关键词提取
- [ ] 性能优化

### 本周
- [ ] 集成到自进化流程
- [ ] 自动化压缩
- [ ] 完整测试

---

*记忆压缩报告 · 太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        return report_file


def main():
    """主函数"""
    compressor = MemoryCompressor()
    
    # 压缩记忆文件
    compressed_files = compressor.compress_memory_files()
    
    # 生成报告
    report = compressor.generate_report()
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("🗜️ 记忆压缩摘要")
    print("=" * 60)
    print(f"压缩文件：{len(compressed_files)} 个")
    print(f"压缩报告：{report}")
    print(f"压缩率：{compressor.compression_stats['compression_ratio']:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
