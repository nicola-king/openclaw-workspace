#!/usr/bin/env python3
"""
美学过滤器 (Aesthetic Filter) v1.1.0
太一系统美学引擎核心 - 为每个输出文件进行艺术处理

修复记录 v1.1.0:
- [FIX-1] _optimize_headings: 修复重复行导致 index() 返回错误索引
- [FIX-2] _assess_markdown_quality: 移除 '太一美学' 加 30 分的脆弱逻辑，改为结构化评分
- [FIX-3] _process_data/_process_config: 质量评级不再依赖字符串比对，改为布尔值
- [FIX-4] 对接真实 ScoringEngine 评分，quality_level 反映多维度结果
"""

import json
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from enum import Enum

from scoring_engine import ScoringEngine, ContentType as ScoringContentType


class ContentType(Enum):
    """内容类型"""
    MARKDOWN = "markdown"
    CODE = "code"
    DATA = "data"
    REPORT = "report"
    CONFIG = "config"


class QualityLevel(Enum):
    """质量等级"""
    S = "S"  # 出版级
    A = "A"  # 专业级
    B = "B"  # 可用级
    C = "C"  # 草稿级


class AestheticFilter:
    """美学过滤器主类"""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.process_history: List[Dict[str, Any]] = []
        self.scoring_engine = ScoringEngine()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "quality_threshold": "B",
            "auto_fix": True,
            "style_guide": "taiyi-standard",
            "output_format": "markdown",
            "add_signature": False,
            "signature_text": "太一美学 · 品质保证"
        }

    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("aesthetic-filter")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def process(
        self,
        content: str,
        content_type: ContentType = None,
        quality_threshold: QualityLevel = None,
        **kwargs
    ) -> Dict[str, Any]:
        """处理内容

        Args:
            content: 原始内容
            content_type: 内容类型（None 时自动检测）
            quality_threshold: 质量阈值

        Returns:
            处理结果
        """
        start_time = datetime.now()

        if content_type is None:
            content_type = self._detect_content_type(content)

        self.logger.info(f"处理内容：类型={content_type.value}")

        # 根据类型选择处理管道
        dispatch = {
            ContentType.MARKDOWN: self._process_markdown,
            ContentType.CODE:     self._process_code,
            ContentType.DATA:     self._process_data,
            ContentType.REPORT:   self._process_report,
            ContentType.CONFIG:   self._process_config,
        }
        handler = dispatch.get(content_type, self._process_generic)
        result = handler(content, quality_threshold)

        elapsed = (datetime.now() - start_time).total_seconds()

        # 多维度评分（使用 ScoringEngine 的结果覆盖 quality_level）
        try:
            scoring_ct = ScoringContentType(content_type.value)
        except ValueError:
            scoring_ct = ScoringContentType.MARKDOWN

        quality_report = self.scoring_engine.evaluate(
            result.get("content", content), scoring_ct
        )

        # [FIX-4] 用 ScoringEngine 的等级覆盖启发式等级
        result["quality_level"] = quality_report.level
        result["scoring_report"] = quality_report.to_dict()

        self.process_history.append({
            "timestamp": start_time.isoformat(),
            "type": content_type.value,
            "quality": result["quality_level"],
            "score": quality_report.total_score,
            "elapsed": elapsed,
            "changes": result["changes_count"]
        })

        return result

    def _detect_content_type(self, content: str) -> ContentType:
        """自动检测内容类型"""
        if re.search(r'^#{1,6}\s', content, re.MULTILINE):
            return ContentType.MARKDOWN

        if re.search(
            r'^(def |class |import |from |function |const |let |var )',
            content, re.MULTILINE
        ):
            return ContentType.CODE

        stripped = content.strip()
        if stripped.startswith('{') or stripped.startswith('['):
            try:
                json.loads(content)
                return ContentType.DATA
            except Exception:
                pass

        if re.search(r'^\s*[\w_]+\s*[:=]', content, re.MULTILINE):
            return ContentType.CONFIG

        return ContentType.MARKDOWN

    # ==================== 处理管道 ====================

    def _process_markdown(
        self, content: str, threshold: QualityLevel = None
    ) -> Dict[str, Any]:
        """处理 Markdown 文档"""
        self.logger.info("处理 Markdown 文档")

        changes: List[str] = []
        processed = content

        processed, c = self._optimize_headings(processed)
        changes.extend(c)

        processed, c = self._unify_lists(processed)
        changes.extend(c)

        processed, c = self._beautify_tables(processed)
        changes.extend(c)

        processed, c = self._enhance_code_blocks(processed)
        changes.extend(c)

        processed, c = self._optimize_quotes(processed)
        changes.extend(c)

        if self.config.get("add_signature", False):
            processed = self._add_signature(processed)
            changes.append("添加太一美学签名")

        # 启发式等级（后续会被 ScoringEngine 覆盖）
        quality = self._assess_markdown_quality(processed)

        return {
            "status": "success",
            "content": processed,
            "content_type": "markdown",
            "quality_level": quality.value,
            "changes": changes,
            "changes_count": len(changes)
        }

    def _process_code(
        self, content: str, threshold: QualityLevel = None
    ) -> Dict[str, Any]:
        """处理代码"""
        self.logger.info("处理代码")

        changes: List[str] = []
        processed = content

        processed, c = self._optimize_code_format(processed)
        changes.extend(c)

        # _optimize_naming / _enhance_comments 目前为 no-op，保留接口
        processed, c = self._optimize_naming(processed)
        changes.extend(c)

        processed, c = self._enhance_comments(processed)
        changes.extend(c)

        quality = self._assess_code_quality(processed)

        return {
            "status": "success",
            "content": processed,
            "content_type": "code",
            "quality_level": quality.value,
            "changes": changes,
            "changes_count": len(changes)
        }

    def _process_data(
        self, content: str, threshold: QualityLevel = None
    ) -> Dict[str, Any]:
        """处理数据"""
        self.logger.info("处理数据")

        changes: List[str] = []
        json_ok = False

        try:
            data = json.loads(content)
            processed = json.dumps(data, indent=2, ensure_ascii=False)
            changes.append("JSON 格式化")
            json_ok = True
        except Exception:
            processed = content
            changes.append("数据格式保持原样")

        # [FIX-3] 用布尔值而非字符串比对
        quality = QualityLevel.A if json_ok else QualityLevel.B

        return {
            "status": "success",
            "content": processed,
            "content_type": "data",
            "quality_level": quality.value,
            "changes": changes,
            "changes_count": len(changes)
        }

    def _process_report(
        self, content: str, threshold: QualityLevel = None
    ) -> Dict[str, Any]:
        """处理报告"""
        self.logger.info("处理报告")

        result = self._process_markdown(content, threshold)

        if "## 摘要" not in result["content"]:
            result["content"] = self._add_executive_summary(result["content"])
            result["changes"].append("添加执行摘要")
            result["changes_count"] += 1

        return result

    def _process_config(
        self, content: str, threshold: QualityLevel = None
    ) -> Dict[str, Any]:
        """处理配置文件"""
        self.logger.info("处理配置文件")

        changes: List[str] = []
        json_ok = False

        try:
            data = json.loads(content)
            processed = json.dumps(data, indent=2, ensure_ascii=False)
            changes.append("JSON 格式化")
            json_ok = True
        except Exception:
            processed = content

        # [FIX-3]
        quality = QualityLevel.A if json_ok else QualityLevel.B

        return {
            "status": "success",
            "content": processed,
            "content_type": "config",
            "quality_level": quality.value,
            "changes": changes,
            "changes_count": len(changes)
        }

    def _process_generic(
        self, content: str, threshold: QualityLevel = None
    ) -> Dict[str, Any]:
        """处理通用内容"""
        self.logger.info("处理通用内容")

        processed = content.strip()
        processed = re.sub(r'\n{3,}', '\n\n', processed)

        return {
            "status": "success",
            "content": processed,
            "content_type": "generic",
            "quality_level": QualityLevel.B.value,
            "changes": ["基本格式优化"],
            "changes_count": 1
        }

    # ==================== Markdown 处理函数 ====================

    def _optimize_headings(self, content: str) -> Tuple[str, List[str]]:
        """优化标题层级

        [FIX-1] 原实现用 lines.index(line) 会在重复行时返回第一次出现的索引，
        导致后续插入空行位置错误。改为 enumerate 直接使用行号。
        """
        changes: List[str] = []
        lines = content.split('\n')
        result: List[str] = []
        last_level = 0

        i = 0
        while i < len(lines):
            line = lines[i]
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()

                # 确保标题层级连续
                if last_level > 0 and level > last_level + 1:
                    level = last_level + 1
                    changes.append(f"调整标题层级 → H{level}: {title}")

                # 标题前保证空行（首行除外）
                if result and result[-1].strip() != '':
                    result.append('')

                result.append('#' * level + ' ' + title)

                # 标题后保证空行（非末尾）
                if i < len(lines) - 1:
                    result.append('')

                last_level = level
            else:
                result.append(line)

            i += 1

        return '\n'.join(result), changes

    def _unify_lists(self, content: str) -> Tuple[str, List[str]]:
        """统一列表格式为 '-'"""
        changes: List[str] = []
        lines = content.split('\n')
        result: List[str] = []
        unified = False

        for line in lines:
            if re.match(r'^[*+]\s', line):
                line = re.sub(r'^[*+]\s', '- ', line)
                unified = True
            result.append(line)

        if unified:
            changes.append("统一无序列表符号为 -")

        return '\n'.join(result), changes

    def _beautify_tables(self, content: str) -> Tuple[str, List[str]]:
        """美化表格（当前标记，未实际对齐）"""
        changes: List[str] = []
        table_pattern = r'\|.+\|\n\|[-:\s|]+\|'
        if re.search(table_pattern, content):
            changes.append("表格检测完成（对齐优化待实现）")
        return content, changes

    def _enhance_code_blocks(self, content: str) -> Tuple[str, List[str]]:
        """检测无语言标识的代码块"""
        changes: List[str] = []
        unmarked = len(re.findall(r'```\n', content))
        if unmarked:
            changes.append(f"发现 {unmarked} 个无语言标识的代码块（请手动补充）")
        return content, changes

    def _optimize_quotes(self, content: str) -> Tuple[str, List[str]]:
        """引用块优化（当前为透传）"""
        return content, []

    def _add_signature(self, content: str) -> str:
        """添加太一美学签名"""
        sig_text = self.config.get('signature_text', '太一美学 · 品质保证')
        ts = datetime.now().strftime('%Y-%m-%d %H:%M')
        signature = f"\n\n---\n\n> **{sig_text}**\n> 美学过滤器自动处理 · {ts}"
        return content + signature

    # ==================== 代码处理函数 ====================

    def _optimize_code_format(self, content: str) -> Tuple[str, List[str]]:
        """优化代码格式"""
        processed = re.sub(r'\n{3,}', '\n\n', content)
        lines = [line.rstrip() for line in processed.split('\n')]
        processed = '\n'.join(lines)
        return processed, ["去除多余空行", "去除行尾空格"]

    def _optimize_naming(self, content: str) -> Tuple[str, List[str]]:
        """命名优化（待实现）"""
        return content, []

    def _enhance_comments(self, content: str) -> Tuple[str, List[str]]:
        """注释增强（待实现）"""
        return content, []

    # ==================== 质量评估函数 ====================

    def _assess_markdown_quality(self, content: str) -> QualityLevel:
        """评估 Markdown 质量

        [FIX-2] 移除 '太一美学' 加 30 分逻辑（可被伪造），
        改为纯结构化评分，此处结果后续会被 ScoringEngine 覆盖。
        """
        score = 0

        if re.search(r'^# ', content, re.MULTILINE):
            score += 25   # H1 存在
        if re.search(r'^#{2,6}\s', content, re.MULTILINE):
            score += 15   # 子标题
        if re.search(r'^-\s', content, re.MULTILINE):
            score += 15   # 列表
        if '```' in content:
            score += 20   # 代码块
        if re.search(r'\|.+\|', content):
            score += 15   # 表格
        if re.search(r'^>\s', content, re.MULTILINE):
            score += 10   # 引用

        if score >= 85:
            return QualityLevel.S
        elif score >= 65:
            return QualityLevel.A
        elif score >= 45:
            return QualityLevel.B
        else:
            return QualityLevel.C

    def _assess_code_quality(self, content: str) -> QualityLevel:
        """评估代码质量"""
        score = 0

        if re.search(r'^    ', content, re.MULTILINE):
            score += 20
        if '#' in content or '"""' in content:
            score += 20
        if '\n\n' in content:
            score += 15
        if re.search(r'def \w+\(', content):
            score += 25

        if score >= 75:
            return QualityLevel.S
        elif score >= 55:
            return QualityLevel.A
        elif score >= 35:
            return QualityLevel.B
        else:
            return QualityLevel.C

    def _add_executive_summary(self, content: str) -> str:
        """在报告头部添加执行摘要"""
        preview = content[:200].strip()
        summary = f"## 执行摘要\n\n{preview}...\n\n---\n\n"
        return summary + content

    # ==================== 文件处理 ====================

    def process_file(self, file_path: str, output_path: str = None) -> Dict[str, Any]:
        """处理文件"""
        path = Path(file_path)

        if not path.exists():
            return {"status": "error", "message": f"文件不存在：{file_path}"}

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        result = self.process(content)

        if output_path is None:
            output_path = str(
                path.parent / f"{path.stem}_beautiful{path.suffix}"
            )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result["content"])

        result["input_file"] = str(path)
        result["output_file"] = output_path

        self.logger.info(
            f"文件处理完成：{path.name} → {Path(output_path).name}"
        )
        return result

    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "status": "healthy",
            "module": "aesthetic-filter",
            "version": "1.1.0",
            "total_processed": len(self.process_history),
            "config": self.config
        }

    @property
    def name(self) -> str:
        return "aesthetic-filter"

    @property
    def version(self) -> str:
        return "1.1.0"

    @property
    def dependencies(self) -> List[str]:
        return ["scoring_engine"]


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="美学过滤器")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    parser.add_argument("--input", "-i", help="输入文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument(
        "--type", "-t",
        choices=["markdown", "code", "data", "report", "config"],
        help="内容类型"
    )
    parser.add_argument("--text", help="直接输入文本")
    parser.add_argument("--health", action="store_true", help="健康检查")

    args = parser.parse_args()

    aesthetic_filter = AestheticFilter(config_path=args.config)

    if args.health:
        print(json.dumps(aesthetic_filter.health_check(), indent=2, ensure_ascii=False))
    elif args.input:
        result = aesthetic_filter.process_file(args.input, args.output)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.text:
        ct = ContentType(args.type) if args.type else None
        result = aesthetic_filter.process(args.text, content_type=ct)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(aesthetic_filter.health_check(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
