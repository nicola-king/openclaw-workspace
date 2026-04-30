#!/usr/bin/env python3
"""
Q&A 对提取器 - 从政府文件中提取条款和问答
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 路径配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
QUOTA_MD_DIR = WORKSPACE / "skills" / "07-system" / "cost-agent" / "quota_md"
DATA_DIR = Path(__file__).parent.parent / "data"


class QAExtractor:
    """Q&A 对提取器"""

    def __init__(self):
        self.qa_pairs: List[Dict] = []

    def extract_from_file(self, filepath: Path) -> List[Dict]:
        """从单个文件提取 Q&A 对"""
        pairs = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            filename = filepath.name

            # 1. 提取标准 Q&A 对 (问题?\n答：回答)
            qa_pattern = re.compile(
                r'(\d+)\.\s*(.+?)\s*\n答[：:]\s*(.+?)(?=\n\d+\.|\n## |\n---|\Z)',
                re.DOTALL | re.MULTILINE
            )

            for match in qa_pattern.finditer(content):
                q_num = match.group(1)
                question = match.group(2).strip()
                answer = match.group(3).strip()

                pairs.append({
                    'id': f"{filename.replace('.md', '')}-{q_num}",
                    'source_file': filename,
                    'q_num': q_num,
                    'question': question,
                    'answer': answer,
                    'type': 'qa'
                })

            # 2. 提取条款 (第 X 条 内容)
            article_pattern = re.compile(
                r'第[一二三四五六七八九十百\d]+条[：:]\s*(.+?)(?=第[一二三四五六七八九十百\d]+条|\Z)',
                re.DOTALL
            )

            for match in article_pattern.finditer(content):
                article_text = match.group(1).strip()
                if len(article_text) > 20:  # 过滤太短的
                    pairs.append({
                        'id': f"{filename.replace('.md', '')}-article-{len(pairs)}",
                        'source_file': filename,
                        'question': f"相关条款",
                        'answer': article_text,
                        'type': 'article'
                    })

            # 3. 提取编号列表 (1. 内容 / 一、内容)
            list_pattern = re.compile(
                r'([一二三四五六七八九十]+|[1-9]\d*)[、.]\s*(.+?)(?=\n[一二三四五六七八九十]+[、.]|\n[1-9]\d*[、.]|\n## |\Z)',
                re.DOTALL | re.MULTILINE
            )

            for match in list_pattern.finditer(content):
                list_num = match.group(1)
                list_text = match.group(2).strip()
                if len(list_text) > 30 and '答' not in list_text:
                    pairs.append({
                        'id': f"{filename.replace('.md', '')}-list-{list_num}",
                        'source_file': filename,
                        'question': f"第{list_num}条",
                        'answer': list_text,
                        'type': 'list_item'
                    })

        except Exception as e:
            print(f"⚠️ 提取 {filepath.name} 失败: {e}")

        return pairs

    def extract_all(self) -> List[Dict]:
        """从所有政府文件提取 Q&A 对"""
        all_pairs = []

        # 遍历所有 MD 文件
        for filepath in QUOTA_MD_DIR.glob('*.md'):
            pairs = self.extract_from_file(filepath)
            all_pairs.extend(pairs)
            print(f"  ✅ {filepath.name}: {len(pairs)} 条")

        return all_pairs

    def save(self, output_path: Path = None):
        """保存提取结果"""
        if output_path is None:
            output_path = DATA_DIR / "qa_pairs_extended.json"

        os.makedirs(output_path.parent, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.qa_pairs, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 已保存 {len(self.qa_pairs)} 条 Q&A 对到 {output_path}")


def main():
    print("🔍 开始提取 Q&A 对...")

    extractor = QAExtractor()
    pairs = extractor.extract_all()

    print(f"\n📊 提取统计:")
    print(f"  总计: {len(pairs)} 条")

    # 按类型统计
    type_counts = {}
    for pair in pairs:
        t = pair.get('type', 'unknown')
        type_counts[t] = type_counts.get(t, 0) + 1

    for t, count in type_counts.items():
        print(f"  {t}: {count} 条")

    # 保存
    extractor.qa_pairs = pairs
    extractor.save()


if __name__ == '__main__':
    main()
