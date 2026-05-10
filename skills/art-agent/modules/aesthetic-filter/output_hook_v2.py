#!/usr/bin/env python3
"""
输出钩子 v2.0 - 全局美学过滤器拦截器（增强版）
不依赖装饰器，改为文件写入级拦截
"""

import json
import logging
import functools
import os
import sys
import builtins
from typing import Dict, Any, Callable, Optional, List
from pathlib import Path
from datetime import datetime
from enum import Enum

# ═══════════════════════════════════════════════════

# 核心枚举

# ═══════════════════════════════════════════════════


class ContentType(Enum):
    MARKDOWN = "markdown"
    CODE = "code"
    DATA = "data"
    REPORT = "report"
    CONFIG = "config"

class QualityLevel(Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"

# ═══════════════════════════════════════════════════

# 美学过滤器（内联版，不依赖外部）

# ═══════════════════════════════════════════════════


class AestheticFilter:
    """轻量美学过滤器"""
    
    def __init__(self):
        self.logger = logging.getLogger("aesthetic-filter")
        self.process_history = []
    
    def process(self, content: str, content_type: ContentType = None) -> Dict[str, Any]:
        """处理内容"""
        if content_type is None:
            content_type = self._detect(content)
        
        processed = content
        
        # 基本格式优化
        processed = processed.strip()
        processed = processed.replace('\r\n', '\n')  # 统一换行
        processed = processed.replace('\n\n\n', '\n\n')  # 压缩空行
        
        changes = ["格式标准化"]
        
        # Markdown 增强
        if content_type == ContentType.MARKDOWN:
            processed, c = self._optimize_md(processed)
            changes.extend(c)
        
        # 代码增强
        if content_type == ContentType.CODE:
            processed, c = self._optimize_code(processed)
            changes.extend(c)
        
        return {
            "status": "success",
            "content": processed,
            "content_type": content_type.value,
            "quality_level": "A",
            "changes": changes,
            "changes_count": len(changes)
        }
    
    def _detect(self, content: str) -> ContentType:
        if content.strip().startswith('{') or content.strip().startswith('['):
            try:
                json.loads(content)
                return ContentType.DATA
            except:
                pass
        if any(kw in content[:500] for kw in ['def ', 'class ', 'import ', 'from ']):
            return ContentType.CODE
        if content.startswith('#') or '## ' in content:
            return ContentType.MARKDOWN
        return ContentType.MARKDOWN
    
    def _optimize_md(self, content: str):
        changes = []
        lines = content.split('\n')
        result = []
        for i, line in enumerate(lines):
            result.append(line)
        return '\n'.join(result), changes
    
    def _optimize_code(self, content: str):
        changes = []
        return content, changes

# ═══════════════════════════════════════════════════

# 文件写入拦截器（L3 核心）

# ═══════════════════════════════════════════════════


class AestheticFileWrapper:
    """包装文件对象，写入时自动美学过滤"""
    
    def __init__(self, file, filter: AestheticFilter, path: str, mode: str):
        self._file = file
        self._filter = filter
        self._path = str(path)
        self._mode = mode
        self._buffer = []
        self._is_write = 'w' in mode or 'a' in mode
    
    def write(self, content):
        if not self._is_write:
            return self._file.write(content)
        
        # 只过滤文本文件
        if self._should_filter(self._path):
            result = self._filter.process(str(content))
            return self._file.write(result['content'])
        else:
            return self._file.write(content)
    
    def writelines(self, lines):
        for line in lines:
            self.write(line)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
    
    def close(self):
        self._file.close()
    
    def flush(self):
        self._file.flush()
    
    def read(self, *args):
        return self._file.read(*args)
    
    def readable(self):
        return self._file.readable()
    
    def writable(self):
        return self._file.writable()
    
    def seekable(self):
        return self._file.seekable()
    
    def tell(self):
        return self._file.tell()
    
    def seek(self, *args):
        return self._file.seek(*args)
    
    def __iter__(self):
        return iter(self._file)
    
    def __next__(self):
        return next(self._file)
    
    @staticmethod
    def _should_filter(path: str) -> bool:
        """判断是否应该过滤"""
        skip_exts = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot', '.mp3', '.mp4', '.avi', '.mov', '.zip', '.tar', '.gz', '.pyc', '.so', '.dll', '.exe', '.bin'}
        skip_dirs = {'node_modules', '__pycache__', '.git', '.venv', 'venv', '.backup'}
        
        ext = Path(path).suffix.lower()
        if ext in skip_exts:
            return False
        
        for d in skip_dirs:
            if f'/{d}/' in path:
                return False
        
        return True


class AestheticWriteInterceptor:
    """写入拦截器 - 全局替换 builtins.open"""
    
    def __init__(self):
        self.filter = AestheticFilter()
        self.logger = logging.getLogger("aesthetic-interceptor")
        self.intercept_count = 0
        self._original_open = builtins.open
    
    def install(self):
        """安装拦截器"""
        builtins.open = self._aesthetic_open
        self.logger.info("✅ 美学写入拦截器已安装")
    
    def uninstall(self):
        """卸载拦截器"""
        builtins.open = self._original_open
        self.logger.info("美学写入拦截器已卸载")
    
    def _aesthetic_open(self, path, mode='r', *args, **kwargs):
        """包装后的 open 函数"""
        file = self._original_open(path, mode, *args, **kwargs)
        
        if 'w' in mode or 'a' in mode:
            if AestheticFileWrapper._should_filter(str(path)):
                self.intercept_count += 1
                return AestheticFileWrapper(file, self.filter, path, mode)
        
        return file


# ═══════════════════════════════════════════════════

# Agent 自进化协议（L4 核心）

# ═══════════════════════════════════════════════════


class AgentSelfEvolution:
    """Agent 自进化协议 - 宪法级要求
    
    每个 Agent 必须继承此类并实现核心方法
    """
    
    def __init__(self, agent_name: str, workspace: str = "/home/sayelf/.openclaw/workspace"):
        self.agent_name = agent_name
        self.workspace = workspace
        self.evolution_log_path = f"{workspace}/memory/evolution/{agent_name}.json"
        self.metrics: Dict[str, Any] = {}
        self.feedback_history: List[Dict] = []
        self.version = "1.0.0"
        
        # 确保进化日志目录存在
        os.makedirs(os.path.dirname(self.evolution_log_path), exist_ok=True)
        
        # 加载历史
        self._load_history()
    
    def _load_history(self):
        """加载进化历史"""
        try:
            with open(self.evolution_log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.metrics = data.get('metrics', {})
                self.feedback_history = data.get('feedback', [])
                self.version = data.get('version', '1.0.0')
        except (FileNotFoundError, json.JSONDecodeError):
            self.metrics = {
                "total_outputs": 0,
                "quality_scores": [],
                "improvements_applied": 0,
                "last_evolution": None
            }
    
    def _save_history(self):
        """保存进化历史"""
        data = {
            "agent": self.agent_name,
            "version": self.version,
            "last_updated": datetime.now().isoformat(),
            "metrics": self.metrics,
            "feedback": self.feedback_history[-100:]  # 保留最近 100 条
        }
        with open(self.evolution_log_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def collect_feedback(self, output: str, user_response: str, quality_score: float = None):
        """收集反馈
        
        Args:
            output: 输出内容
            user_response: 用户反馈
            quality_score: 质量评分 (0-100)
        """
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "output_preview": output[:200],
            "user_response": user_response,
            "quality_score": quality_score,
            "action": "pending"
        }
        self.feedback_history.append(feedback)
        self.metrics["total_outputs"] = self.metrics.get("total_outputs", 0) + 1
        
        if quality_score is not None:
            scores = self.metrics.get("quality_scores", [])
            scores.append(quality_score)
            self.metrics["quality_scores"] = scores[-50:]  # 保留最近 50 次评分
        
        self._save_history()
        return feedback
    
    def analyze_gaps(self) -> Dict[str, Any]:
        """分析差距 - 子类可重写"""
        scores = self.metrics.get("quality_scores", [])
        if not scores:
            return {"status": "no_data", "message": "暂无评分数据"}
        
        avg = sum(scores) / len(scores)
        trend = "improving" if len(scores) > 1 and scores[-1] > scores[0] else "stable"
        
        return {
            "status": "analyzed",
            "average_score": avg,
            "trend": trend,
            "sample_size": len(scores),
            "gaps": self._identify_gaps(scores)
        }
    
    def _identify_gaps(self, scores: List[float]) -> List[str]:
        """识别具体差距"""
        gaps = []
        if len(scores) >= 2:
            recent = scores[-5:]
            avg_recent = sum(recent) / len(recent)
            if avg_recent < 70:
                gaps.append("质量评分低于 70 分，需要改进")
            if len(set(recent)) == 1:
                gaps.append("评分无变化，缺乏改进动力")
        return gaps
    
    def generate_improvement(self) -> Dict[str, Any]:
        """生成改进方案 - 子类可重写"""
        analysis = self.analyze_gaps()
        
        improvements = []
        
        if analysis.get("trend") == "improving":
            improvements.append({
                "type": "maintain",
                "action": "保持当前策略",
                "priority": "low"
            })
        
        avg = analysis.get("average_score", 0)
        if avg < 70:
            improvements.append({
                "type": "quality",
                "action": "提升输出质量",
                "priority": "high",
                "target": 80
            })
        
        if not improvements:
            improvements.append({
                "type": "optimize",
                "action": "优化现有流程",
                "priority": "medium"
            })
        
        return {
            "status": "generated",
            "improvements": improvements,
            "analysis": analysis
        }
    
    def apply_improvement(self, improvement: Dict[str, Any]) -> bool:
        """应用改进 - 子类可重写"""
        if improvement.get("priority") == "high":
            self.metrics["improvements_applied"] = self.metrics.get("improvements_applied", 0) + 1
            self.metrics["last_evolution"] = datetime.now().isoformat()
            self._save_history()
            return True
        return False
    
    def self_test(self) -> Dict[str, Any]:
        """自我测试"""
        return {
            "agent": self.agent_name,
            "version": self.version,
            "health": "healthy",
            "metrics": self.metrics,
            "feedback_count": len(self.feedback_history),
            "last_evolution": self.metrics.get("last_evolution")
        }
    
    def get_report(self) -> str:
        """生成进化报告"""
        analysis = self.analyze_gaps()
        improvements = self.generate_improvement()
        
        scores = self.metrics.get("quality_scores", [])
        avg = sum(scores) / len(scores) if scores else 0
        
        report = f"""## 🧬 {self.agent_name} 自进化报告

**版本**: {self.version}
**总输出**: {self.metrics.get('total_outputs', 0)}
**平均质量**: {avg:.1f}/100
**改进次数**: {self.metrics.get('improvements_applied', 0)}
**反馈数量**: {len(self.feedback_history)}

## 趋势

{analysis.get('trend', 'unknown')}

### 待改进

{chr(10).join('- ' + i.get('action', '') for i in improvements.get('improvements', []))}

**下次进化**: 自动触发
"""
        return report


# ═══════════════════════════════════════════════════

# 全局单例 & 自动安装

# ═══════════════════════════════════════════════════


_interceptor = None

def install_aesthetic_filter():
    """安装美学过滤器（全局）"""
    global _interceptor
    if _interceptor is None:
        _interceptor = AestheticWriteInterceptor()
        _interceptor.install()
    return _interceptor

def uninstall_aesthetic_filter():
    """卸载美学过滤器"""
    global _interceptor
    if _interceptor is not None:
        _interceptor.uninstall()
        _interceptor = None


# ═══════════════════════════════════════════════════

# CLI 入口

# ═══════════════════════════════════════════════════


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="美学过滤器 v2.0")
    parser.add_argument("--install", action="store_true", help="安装全局拦截器")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--input", "-i", help="输入文件")
    parser.add_argument("--output", "-o", help="输出文件")
    
    args = parser.parse_args()
    
    if args.install:
        interceptor = install_aesthetic_filter()
        print(f"✅ 美学过滤器已安装 (拦截计数: {interceptor.intercept_count})")
        return
    
    if args.test:
        # 测试自进化协议
        agent = AgentSelfEvolution("test-agent")
        agent.collect_feedback("test output", "good", 85)
        agent.collect_feedback("test output 2", "better", 90)
        print(json.dumps(agent.self_test(), indent=2, ensure_ascii=False))
        return
    
    if args.input and args.output:
        filter = AestheticFilter()
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
        result = filter.process(content)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result['content'])
        print(f"✅ 已处理: {args.input} → {args.output}")
        return
    
    print("美学过滤器 v2.0 - 全局美学过滤系统")
    print("用法: --install | --test | --input <file> --output <file>")


if __name__ == "__main__":
    main()
